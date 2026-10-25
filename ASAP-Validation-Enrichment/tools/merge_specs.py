"""Merge exactly 8 patches into immutable original dataset; do not apply unreviewed corrections."""
import argparse,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read_jsonl(path):
    result=[]
    for lineno,line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(),1):
        if line.strip():
            try:result.append(json.loads(line))
            except Exception as e:raise ValueError(f"{path}:{lineno}: {e}") from e
    return result
def fingerprint(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
p=argparse.ArgumentParser();p.add_argument("--source",default=str(R/"source/validation_master_flat.json"));p.add_argument("--patch-dir",default=str(R/"patches"));p.add_argument("--out",default=str(R/"final/validation_master_enriched.json"));a=p.parse_args()
source=Path(a.source);original=json.loads(source.read_text(encoding="utf-8-sig"))
state=R/"control/PROJECT_STATE.json"
if state.exists():
    hash_saved=json.loads(state.read_text()).get("source_dataset_sha256")
    if hash_saved and hash_saved!=hashlib.sha256(source.read_bytes()).hexdigest():raise ValueError("Source file hash mismatch")
specs={}
for n in range(1,9):
    file=Path(a.patch_dir)/f"SPEC_PATCH_{n:02d}.jsonl"
    if not file.exists():raise FileNotFoundError(file)
    for obj in read_jsonl(file):
        key=obj["row_key"]
        if key in specs:raise ValueError("Duplicate patch key "+key)
        specs[key]=obj["implementation_spec"]
registry={r["row_key"]:r for r in read_jsonl(R/"control/ROW_REGISTRY.jsonl")}
required=set(json.loads((R/"control/SPEC_SCHEMA.json").read_text())["required"])
out=[];seen=set();continuations={}
for pos,row in enumerate(original):
    rid=row.get("record_id")
    if rid is not None:key=f"R{int(float(rid)):03d}"
    else:
        parent=int(float(row["parent_record_id"]))
        continuations[parent]=continuations.get(parent,0)+1
        key=f"C{parent:03d}-{continuations[parent]:02d}"
    if key not in registry or registry[key]["source_index"]!=pos or registry[key]["source_row_sha256"]!=fingerprint(row):raise ValueError("Source identity mismatch "+key)
    if key not in specs or not isinstance(specs[key],dict) or required-set(specs[key]):raise ValueError("Invalid/missing spec "+key)
    if "implementation_spec" in row:raise ValueError("Already enriched source "+key)
    out.append({**row,"implementation_spec":specs[key]});seen.add(key)
if set(specs)!=seen:raise ValueError("Unknown patch keys "+str(set(specs)-seen))
if [{k:v for k,v in row.items() if k!="implementation_spec"} for row in out]!=original:raise ValueError("Original data mutated")
dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
temp=dest.with_suffix(".tmp");temp.write_text(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
if json.loads(temp.read_text())!=out:raise ValueError("Roundtrip mismatch")
temp.replace(dest)
(dest.parent/"enrichment_report.json").write_text(json.dumps({"rows":len(out),"status":"STRUCTURAL_ONLY_NOT_RUNTIME_CERTIFIED"},indent=2)+"\n",encoding="utf-8")
print("Wrote",dest,len(out),"rows")
