"""Create stable registry and source checksum; never change original JSON."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
src=R/"source/validation_master_flat.json"
rows=json.loads(src.read_text(encoding="utf-8-sig"))
if not isinstance(rows,list): raise ValueError("Expected JSON array")
def h(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
counts={};output=[];ids=[]
for pos,row in enumerate(rows):
    rid=row.get("record_id");parent=row.get("parent_record_id")
    if rid is not None:
        num=int(float(rid));key=f"R{num:03d}";ids.append(num)
    else:
        if parent is None:raise ValueError(f"Continuation at {pos} has no parent")
        num=int(float(parent));counts[num]=counts.get(num,0)+1;key=f"C{num:03d}-{counts[num]:02d}"
    output.append({"row_key":key,"source_index":pos,"record_id":rid,"parent_record_id":parent,"row_type":row.get("row_type"),"script_name":row.get("SCRIPT NAME"),"source_row_sha256":h(row)})
if len(set(x["row_key"] for x in output))!=len(output):raise ValueError("Duplicate row keys")
if sorted(ids)!=list(range(1,93)) or len(output)!=108 or sum(x["record_id"] is None for x in output)!=16: raise ValueError("Unexpected source row counts; investigate, never pad")
out=R/"control/ROW_REGISTRY.jsonl"
out.write_text("".join(json.dumps(x,ensure_ascii=False)+"\n" for x in output),encoding="utf-8")
st=R/"control/PROJECT_STATE.json"
state=json.loads(st.read_text()) if st.exists() else json.loads((R/"templates/PROJECT_STATE.template.json").read_text())
state["source_dataset_sha256"]=hashlib.sha256(src.read_bytes()).hexdigest()
st.write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("Validated",len(output),"rows; wrote",out,st)
