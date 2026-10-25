# Project Contract (bootstrap baseline)

Status: TEMPLATE / S00 SHOULD CONFIRM, NOT SILENTLY REDEFINE.

1. Source of business truth: original validation_master_flat.json, unchanged.
2. Source of ASAP Runtime truth: explicitly supplied chunks of User Manual / Scripting Manual; every verified ASAP API symbol needs traceable evidence.
3. Never fabricate an API, tolerance, conversion, formula, default numeric zero, or inaccessible source.
4. Preserve all original data fields, original `NaN` and `NaT` strings, order, continuation rows, and `development_status`.
5. Use `R001` for numbered record 1; use `C020-01` for the first continuation of record 20. Row identity based on source order + parent association; validate immutable fingerprint.
6. Each spec patch adds ONLY `implementation_spec` to the identified row; do not rewrite business fields.
7. `documented` / `partially_documented` / `unresolved` must reflect actual evidence, not mere completeness of JSON keys.
8. Always maintain source IDs, chunk IDs, and separate observations from assumptions.
9. All Claude interactions use pasted sources. Claude cannot assume local filesystem access or promise actual files.
10. Each session outputs complete, copyable artifact blocks and HANDOFF_SXX.md; local scripts validate and persist.
11. Sensitive source/evidence is local-only. Target GitHub repository is public.
12. Every session starts fresh; latest PROJECT_STATE and required artifacts are explicitly pasted.
