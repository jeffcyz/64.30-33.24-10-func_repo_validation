"""Synthetic privacy-safe regression tests for incremental single-record merging."""
import importlib.util, json, tempfile, unittest
from pathlib import Path
FILE=Path(__file__).resolve().parents[1]/"tools/single_validation.py"
spec=importlib.util.spec_from_file_location("single_validation",FILE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
SPEC={"spec_status":"unresolved","execution_stage":"unknown","evaluation_scope":None,"required_data_points":[],"runtime_access_plan":[],"calculation_steps":[],"validation_logic":[],"source_references":[],"shared_pattern_references":[],"unresolved_questions":["No manual evidence supplied"],"implementation_readiness":"blocked"}
class SingleValidationTests(unittest.TestCase):
 def setUp(self):
    td=tempfile.TemporaryDirectory();self.addCleanup(td.cleanup);self.dir=Path(td.name)
    self.rows=[{"record_id":1,"parent_record_id":None,"row_type":"numbered","development_status":"developed"},{"record_id":2,"parent_record_id":None,"row_type":"numbered","development_status":"testing"},{"record_id":None,"parent_record_id":2,"row_type":"unnumbered_continuation","WARNING":"NaN"}]
    self.src=self.dir/"original.json";m.dump(self.src,self.rows)
    self.reg=self.dir/"registry.jsonl"
    keys=["R001","R002","C002-01"]
    self.reg.write_text("".join(json.dumps({"row_key":k,"source_index":i,"source_row_sha256":m.fingerprint(self.rows[i])})+"\n" for i,k in enumerate(keys)))
    self.patch=self.dir/"SPEC_R002.jsonl";self.items=[{"row_key":keys[i],"source_row_sha256":m.fingerprint(self.rows[i]),"implementation_spec":SPEC} for i in [1,2]]
    self.patch.write_text("".join(json.dumps(x)+"\n" for x in self.items))
    self.schema=FILE.parents[1]/"control/SPEC_SCHEMA.json"
 def test_complete_patch_and_incremental_merge(self):
    rows,idx=m.source_registry(self.src,self.reg)
    patch=m.validate(2,idx,self.patch,self.schema)
    a=type("args",(),{"output":self.dir/"final.json","replace":False})()
    m.merge(a,rows,idx,patch);result=m.load(a.output)
    self.assertNotIn("implementation_spec",result[0])
    self.assertEqual(result[1]["development_status"],"testing")
    self.assertIn("implementation_spec",result[2])
    with self.assertRaisesRegex(ValueError,"Already enriched"):m.merge(a,rows,idx,patch)
    a.replace=True;m.merge(a,rows,idx,patch)
    self.assertTrue((self.dir/"final.json.bak").exists())
 def test_missing_continuation_fails(self):
    rows,idx=m.source_registry(self.src,self.reg)
    self.patch.write_text(json.dumps(self.items[0])+"\n")
    with self.assertRaisesRegex(ValueError,"coverage mismatch"):m.validate(2,idx,self.patch,self.schema)
 def test_invalid_type_and_hash(self):
    rows,idx=m.source_registry(self.src,self.reg)
    bad=json.loads(json.dumps(self.items));bad[0]["implementation_spec"]["required_data_points"]="wrong"
    self.patch.write_text("".join(json.dumps(x)+"\n" for x in bad))
    with self.assertRaisesRegex(ValueError,"wrong type"):m.validate(2,idx,self.patch,self.schema)
    bad=json.loads(json.dumps(self.items));bad[0]["source_row_sha256"]="wrong"
    self.patch.write_text("".join(json.dumps(x)+"\n" for x in bad))
    with self.assertRaisesRegex(ValueError,"fingerprint mismatch"):m.validate(2,idx,self.patch,self.schema)
 def test_existing_master_corruption_blocks_merge(self):
    rows,idx=m.source_registry(self.src,self.reg)
    patch=m.validate(2,idx,self.patch,self.schema)
    out=self.dir/"final.json";wrong=json.loads(json.dumps(rows));wrong[0]["development_status"]="tampered";m.dump(out,wrong)
    a=type("args",(),{"output":out,"replace":False})()
    with self.assertRaisesRegex(ValueError,"Source fields changed"):m.merge(a,rows,idx,patch)
if __name__=="__main__":unittest.main()

