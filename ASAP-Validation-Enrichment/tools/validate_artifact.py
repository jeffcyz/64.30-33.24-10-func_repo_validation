"""Validate pasted JSONL and exact batch row-key coverage."""
import argparse,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def jsonl(path):
    items=[]
    for i,line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(),1):
        if line.strip():
            try:items.append(json.loads(line))
            except Exception as e:raise ValueError(f"{path}:{i}: {e}") from e
    return items
p=argparse.ArgumentParser();p.add_argument("file");p.add_argument("--batch",type=int,choices=range(1,9));a=p.parse_args()
f=Path(a.file);data=jsonl(f) if f.suffix==".jsonl" else json.loads(f.read_text(encoding="utf-8-sig"))
print("Syntax OK; entries:",len(data) if isinstance(data,list) else "object")
if a.batch:
    intervals=[(1,12),(13,24),(25,36),(37,48),(49,60),(61,68),(69,80),(81,92)]
    lo,hi=intervals[a.batch-1]
    expected={r["row_key"] for r in jsonl(R/"control/ROW_REGISTRY.jsonl") if any(x is not None and lo<=int(float(x))<=hi for x in (r["record_id"],r["parent_record_id"]))}
    keys=[x["row_key"] for x in data]
    if len(set(keys))!=len(keys) or set(keys)!=expected:raise ValueError(f"Coverage error: missing={expected-set(keys)} extras={set(keys)-expected}")
    required=set(json.loads((R/"control/SPEC_SCHEMA.json").read_text())["required"])
    for row in data:
        spec=row.get("implementation_spec")
        if not isinstance(spec,dict) or required-set(spec):raise ValueError("Missing spec fields: "+row["row_key"])
    print("Batch coverage OK",lo,hi)
