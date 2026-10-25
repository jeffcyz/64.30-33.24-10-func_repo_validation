"""Prepare paste-only session context; inspect before pasting into approved Claude."""
import argparse,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument("session",type=int,choices=range(19));p.add_argument("--include",action="append",default=[],help="Additional relative text file")
a=p.parse_args();s=a.session
meta=json.loads((R/"control/SESSION_MAP.json").read_text())[s]
def block(name,content,chunk="ALL"):
    return f"===== BEGIN SOURCE =====\nSOURCE_ID: {name}\nCHUNK_ID: {chunk}\nCONTENT_START\n{content.rstrip()}\nCONTENT_END\n===== END SOURCE ====="
parts=["# REVIEW CONFIDENTIAL CONTENT BEFORE PASTING INTO APPROVED CLAUDE"]
source=R/"source/validation_master_flat.json"
if (s in (0,1,2) or 8<=s<=15) and source.exists():
    rows=json.loads(source.read_text(encoding="utf-8-sig"))
    lo,hi=meta.get("start"),meta.get("end")
    if lo is not None:
        rows=[r for r in rows if any(v is not None and lo<=int(float(v))<=hi for v in [r.get("record_id"),r.get("parent_record_id")])]
    parts.append(block("VALIDATION_MASTER",json.dumps(rows,ensure_ascii=False,indent=2),f"S{s:02d}"))
for name,path in [("CONTRACT",R/"control/CONTRACT.md"),("SPEC_SCHEMA",R/"control/SPEC_SCHEMA.json"),("PROJECT_STATE",R/"control/PROJECT_STATE.json"),("ROW_REGISTRY",R/"control/ROW_REGISTRY.jsonl")]:
    if path.exists() and (s!=0 or name in ("CONTRACT","SPEC_SCHEMA")):parts.append(block(name,path.read_text(encoding="utf-8")))
for rel in a.include:
    path=(R/rel).resolve()
    if R not in path.parents or not path.is_file():raise ValueError("Invalid local input: "+rel)
    parts.append(block(path.stem.upper(),path.read_text(encoding="utf-8"),path.stem))
parts.append("# SEND AFTER ALL SOURCES\n"+(R/f"prompts/S{s:02d}.md").read_text(encoding="utf-8"))
out=R/f"context_packs/SESSION_S{s:02d}.txt";out.parent.mkdir(exist_ok=True)
out.write_text("\n\n".join(parts)+"\n",encoding="utf-8")
print(out,"bytes:",out.stat().st_size,"sha256:",hashlib.sha256(out.read_bytes()).hexdigest())
print("Append any other required manuals/catalogs as --include; this pack does not silently supply them.")
