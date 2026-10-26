EXECUTE SINGLE VALIDATION

Use only the pasted sources in THIS conversation, and use the TARGET_RECORD_ID from the session header.

Perform one complete analysis and return TWO artifacts:

ARTIFACT 1 — SPEC_R###.jsonl
One JSON object per source row (target numbered row and all associated continuation rows), with keys:
- row_key: exact stable key from ROW_REGISTRY.
- source_row_sha256: exact corresponding source hash copied from ROW_REGISTRY.
- implementation_spec: conforms exactly to supplied SPEC_SCHEMA.

ARTIFACT 2 — QA_R###.json
A single JSON object with:
- target_record_id, expected_row_keys, emitted_row_keys, source_chunks_reviewed;
- original_conditions_covered (identify each WARNING/continuation rule);
- required_data_point_count, documented_runtime_mappings, unresolved_runtime_mappings;
- missing_business_decisions, unresolved_questions, implementation_readiness;
- source_evidence_summary, schema_validation_status, known_limitations.

ANALYSIS REQUIREMENTS:

1. Identify original FOCUS, TYPE, ASSET, SCRIPT NAME, DESCRIPTION, WARNING, THRESHOLD, NOTES and continuation rows. Each original condition must have a distinct representation in validation_logic. Preserve original failure messages.
2. List EVERY business input and intermediate output required to evaluate each condition. For each: data origin, deal/bond/asset/loan scope, setup/current/previous/historical period, units/type if available, dependencies and manual evidence.
3. Verify access pathways using actually supplied Scripting and User Manual sections. An exact documented Runtime API needs symbol/signature, arguments, return type, lifecycle and citation; if unavailable, use null.
4. Include ordered calculation_steps, runtime_access_plan and validation_logic with explicit Pass/Fail conditions. Never default an unknown amount to zero or invent comparison tolerance.
5. Use Release Notes to qualify version-specific behavior. Treat SQL Catalog as database metadata, NOT a direct Runtime API.
6. Distinguish documented, partially_documented and unresolved; implementation_readiness must not be ready while a necessary mapping, calculation or business decision remains unresolved.
7. Keep shared_pattern_references an array; do not fabricate global catalog IDs if no catalog was pasted.
8. Do not generate actual ASAP validation code or analyze other records. Do not alter development_status.

QUALITY GATE:
- Expected and emitted row keys match exactly, no duplicates.
- JSONL contains no code fences, markdown commentary, ellipses or invalid JSON.
- All required SPEC_SCHEMA properties are present with the correct types.
- Every documented Runtime claim has a real pasted source reference and corroborating excerpt.
- All original business conditions accounted for.
- If a source chunk is incomplete or an API is unavailable, say so and leave unknown values null.

Output the full content of SPEC_R###.jsonl in one fenced jsonl code block, followed by QA_R###.json in a separate fenced json code block. Replace ### with the zero-padded target ID. No other artifacts. Do not say you modified local files. Stop after these two artifacts.

