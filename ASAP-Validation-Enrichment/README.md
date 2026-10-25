# ASAP Validation Enrichment — Paste-Only, Multi-Session Workflow

This folder is an **independent subproject** for generating documented ASAP Runtime-based `implementation_spec` entries for a pre-existing flat Validation Master JSON. It is designed for **19 separate Claude chat sessions (S00–S18)** with pasted-text attachments rather than file uploads or filesystem access.

> **SECURITY: The target GitHub repository is PUBLIC. This committed folder contains templates, prompts and local helper scripts only. Do NOT commit the actual ASAP manuals, original company JSON, generated patches, evidence catalogs, or project state unless company-approved for public disclosure. `.gitignore` protects common local filenames, but always check `git status` before pushing.**

## Quick start

1. Copy/clone this directory locally. Put your real `validation_master_flat.json`, `user_manual.txt`, `scripting_manual.txt` in `source/` **locally only**.
2. Run `python tools/build_registry.py` to create your stable row registry and source fingerprint (expected: 92 numbered + 16 continuation rows, but never fabricate rows to hit this target).
3. Run `python tools/prepare_session.py 00` to create `context_packs/SESSION_S00.txt`. It contains copy-paste source markers and the S00 task. Inspect sensitive content and use only an approved enterprise Claude environment.
4. Paste `prompts/INTAKE.md` into a new Claude conversation; then paste source blocks from the context pack. Send `START SESSION 00` after all blocks have been received.
5. Save Claude responses as LOCAL text artifacts. For structured outputs prefer JSONL, with one complete object per line. Run `python tools/validate_artifact.py <file>` (and optionally `--source source/validation_master_flat.json --batch 01` for a patch).
6. Repeat Sessions S01–S18. For each new conversation, paste fresh context. Do not assume Claude remembers previous chats.
7. After verified patches S08–S15 exist, use the final merge instructions (`prompts/S18.md`); an initial deterministic local merger is included as `tools/merge_specs.py`.

## Truth and continuity

- `source/validation_master_flat.json` is the immutable source of rules and statuses. A source hash controls identity.
- ASAP User Manual + Scripting Manual are the ONLY authority for ASAP-specific runtime objects/functions. Cite pasted SOURCE_ID/CHUNK_ID and direct excerpts; do not fabricate APIs.
- `record_id` is null for continuation rows; each gets a stable `row_key`, e.g. `C020-01`.
- Every new session consumes the latest locally saved `control/PROJECT_STATE.json` plus task-specific material and outputs a new handoff; local tools, not Claude, handle durable files.
- Unknown runtime mappings are `null` with explicit unresolved questions. Do not treat `THRESHOLD` as numeric tolerance or severity without evidence.
- `development_status` is preserved, and is independent of `spec_status` / implementation readiness.

## 19-session roadmap

| Stage | Sessions | Artifacts |
| --- | --- | --- |
| Bootstrap | S00 | CONTRACT, SPEC_SCHEMA, ROW_REGISTRY, PROJECT_STATE |
| Rule analysis | S01–S02 | RULES_PART1/2, BUSINESS_GAPS |
| Evidence routing | S03 | MANUAL_ROUTING, SOURCE_MANIFEST |
| Runtime evidence | S04–S06 | RUNTIME_CORE, RUNTIME_ACCESS, RUNTIME_CALCULATIONS |
| Canonical mapping | S07 | DATA_POINT_CATALOG, SHARED_PATTERNS |
| Specifications | S08–S15 | Eight `SPEC_PATCH_XX.jsonl` + QA |
| Integration | S16 | INTEGRATION_ISSUES/CORRECTIONS |
| Independent review | S17 | QA_FINDINGS/CORRECTIONS + unresolved |
| Merge | S18 | `validation_master_enriched.json`, report, deterministic merge |

Each session's complete prompt is in `prompts/SXX.md`; use `control/SESSION_MAP.json` for the expected inputs and outputs. Empty data folders are deliberately kept by `.gitkeep`. No actual manual or validation records are packaged.

## CLI examples

```powershell
python tools/build_registry.py
python tools/prepare_session.py 08
python tools/validate_artifact.py patches/SPEC_PATCH_01.jsonl --source source/validation_master_flat.json --batch 01
python tools/merge_specs.py --source source/validation_master_flat.json --patch-dir patches --out final/validation_master_enriched.json
```

`prepare_session.py` includes only locally present input files; it lists missing optional sources for you to append. Its auto-selection uses numbered records plus continuation rows by `parent_record_id`. Review generated context before posting to any external service.
