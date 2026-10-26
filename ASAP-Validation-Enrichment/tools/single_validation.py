"""One-record Claude workflow: prepare, validate, merge. No third-party dependencies."""
import argparse, json, hashlib, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def dump(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    assert load(p)==x
def lines(p):
    result=[]
    for n,s in enumerate(Path(p).read_text(encoding="utf-8-sig").splitlines(),1):
        if s.strip():
            try: result.append(json.loads(s))
            except ValueError as e:raise ValueError(f"{p}:{n}: {e}") from e
    return result
def fingerprint(r):return hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def source_registry(source,reg):
    rows=load(source); entries=lines(reg); index={};counts={}
    if not isinstance(rows,list) or len(rows)!=len(entries):raise ValueError("Source/registry count mismatch")
    for i,(r,e) in enumerate(zip(rows,entries)):
        rid=r.get("record_id")
        if rid is None:
            parent=r.get("parent_record_id")
            if parent is None:raise ValueError("Continuation missing parent")
            parent=int(parent);counts[parent]=counts.get(parent,0)+1
            key=f"C{parent:03d}-{counts[parent]:02d}"
        else:key=f"R{int(rid):03d}"
        if e["row_key"]!=key or e["source_index"]!=i or e["source_row_sha256"]!=fingerprint(r):
            raise ValueError(f"Source identity mismatch: {key}")
        if key in index:raise ValueError(f"Duplicate row_key: {key}")
        index[key]=(i,r,e["source_row_sha256"])
    return rows,index
def target(index,rid):
    key=f"R{rid:03d}"
    if key not in index:raise ValueError(f"Unknown record ID {rid}")
    return [k for k,(_,r,_) in index.items() if r.get("record_id")==rid or (r.get("record_id") is None and r.get("parent_record_id")==rid)]
def check(v,s,loc="$"):
    if "enum" in s and v not in s["enum"]:raise ValueError(f"{loc}: invalid enum")
    typ=s.get("type")
    if typ:
        ts=[typ] if isinstance(typ,str) else typ
        d={"null":type(None),"string":str,"array":list,"object":dict,"integer":int,"number":(int,float),"boolean":bool}
        if not any(isinstance(v,d[t]) and not(t in ("number","integer") and isinstance(v,bool)) for t in ts):
            raise ValueError(f"{loc}: wrong type")
    if isinstance(v,dict):
        if set(s.get("required",[]))-set(v):raise ValueError(f"{loc}: missing required fields")
        for k,p in s.get("properties",{}).items():
            if k in v:check(v[k],p,loc+"."+k)
    if isinstance(v,list) and "items" in s:
        for i,x in enumerate(v):check(x,s["items"],f"{loc}[{i}]")
def validate(rid,index,patch,schema):
    objects=lines(patch); expected=target(index,rid); keys=[x.get("row_key") for x in objects]
    if len(keys)!=len(set(keys)) or set(keys)!=set(expected):raise ValueError(f"Row coverage mismatch: expected {expected}, got {keys}")
    for o in objects:
        if set(o)!={"row_key","source_row_sha256","implementation_spec"}:raise ValueError("Unexpected patch fields")
        if o["source_row_sha256"]!=index[o["row_key"]][2]:raise ValueError("Patch row fingerprint mismatch")
        check(o["implementation_spec"],load(schema),"implementation_spec")
    return objects
def block(name,chunk,text,scope="FULL_DOCUMENT"):
    return f"===== BEGIN SOURCE =====\nSOURCE_ID: {name}\nCHUNK_ID: {chunk}\nSOURCE_SCOPE: {scope}\nCONTENT_START\n{text.rstrip()}\nCONTENT_END\n===== END SOURCE =====\n"
def prepare(args,index):
    names={"ASAP_SCRIPTING_MANUAL":"merged_scripting_manual.md","ASAP_USER_MANUAL":"merged_user_manual.md","ASAP_RELEASE_NOTES":"Releases-be4181818e.md","ASAP_SCHEMA_CATALOG":"schema_catalog.md"}
    keys=target(index,args.id)
    content=[block("VALIDATION_RECORD",f"R{args.id:03d}",json.dumps([index[k][1] for k in keys],ensure_ascii=False,indent=2),"TARGET_AND_CONTINUATIONS")]
    reg=[{"row_key":k,"source_row_sha256":index[k][2],"source_index":index[k][0]} for k in keys]
    content.append(block("ROW_REGISTRY",f"R{args.id:03d}","\n".join(json.dumps(x) for x in reg),"TARGET_AND_CONTINUATIONS"))
    content.append(block("SPEC_SCHEMA","CANONICAL",Path(args.schema).read_text(encoding="utf-8")))
    if args.manual_mode=="full":
        for name,filename in names.items():
            path=ROOT/"source"/filename
            if not path.is_file():raise FileNotFoundError(path)
            content.append(block(name,filename,path.read_text(encoding="utf-8")))
    if args.manual_mode=="selected" and not args.include:raise ValueError("Selected mode requires --include SOURCE_ID:relative_path")
    for item in args.include:
        name,sep,relative=item.partition(":")
        if not sep or name not in names:raise ValueError("--include requires SOURCE_ID:relative/path")
        p=(ROOT/relative).resolve()
        if not p.is_file() or ROOT not in p.parents:raise ValueError("Unsafe or missing source chunk")
        content.append(block(name,p.stem,p.read_text(encoding="utf-8"),"SELECTED_SECTIONS"))
    folder=ROOT/"context_packs/by_record";folder.mkdir(parents=True,exist_ok=True)
    (folder/f"R{args.id:03d}_CONTEXT.txt").write_text("\n\n".join(content),encoding="utf-8")
    prompt=(ROOT/"prompts/SINGLE_VALIDATION_EXECUTE.md").read_text(encoding="utf-8")
    (folder/f"R{args.id:03d}_EXECUTE.txt").write_text(f"TARGET_RECORD_ID: {args.id}\nTARGET_ROW_KEY: R{args.id:03d}\n\n"+prompt,encoding="utf-8")
    print(f"Prepared R{args.id:03d}: {len(keys)} source rows")
def merge(args,original,index,patch):
    path=args.output;existing=load(path) if path.exists() else [dict(x) for x in original]
    if len(existing)!=len(original):raise ValueError("Wrong output row count")
    for n,(old,new) in enumerate(zip(original,existing)):
        if {k:v for k,v in new.items() if k!="implementation_spec"}!=old:raise ValueError(f"Source fields changed at row {n}")
    for item in patch:
        n=index[item["row_key"]][0]
        if "implementation_spec" in existing[n] and not args.replace:raise ValueError("Already enriched; use --replace")
        existing[n]["implementation_spec"]=item["implementation_spec"]
    if path.exists():
        backup=path.with_suffix(path.suffix+".bak");shutil.copy2(path,backup)
        print("Backup:",backup)
    dump(path,existing)
    print(f"PASS: merged {len(patch)} source rows into {path}, preserved {len(original)} records and original fields")
def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest="action",required=True)
    for name in ("prepare","validate","merge"):
        q=sub.add_parser(name);q.add_argument("--id",type=int,required=True)
        q.add_argument("--source",type=Path,default=ROOT/"source/validation_master_flat.json")
        q.add_argument("--registry",type=Path,default=ROOT/"control/ROW_REGISTRY.jsonl")
        q.add_argument("--schema",type=Path,default=ROOT/"control/SPEC_SCHEMA.json")
        if name=="prepare":
            q.add_argument("--manual-mode",choices=("full","selected"),default="full")
            q.add_argument("--include",action="append",default=[])
        else:q.add_argument("--patch",type=Path,default=None)
        if name=="merge":
            q.add_argument("--output",type=Path,default=ROOT/"final/validation_master_enriched.json")
            q.add_argument("--replace",action="store_true")
    a=p.parse_args()
    original,index=source_registry(a.source,a.registry)
    if a.action=="prepare":prepare(a,index);return
    patch=a.patch or ROOT/f"patches/by_record/SPEC_R{a.id:03d}.jsonl"
    objects=validate(a.id,index,patch,a.schema)
    print("PASS: patch JSONL, source hashes, schema required/types and row-key coverage")
    if a.action=="merge":merge(a,original,index,objects)
if __name__=="__main__":main()

