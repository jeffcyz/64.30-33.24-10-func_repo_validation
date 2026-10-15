# Registry configuration

`example_rules.json` demonstrates the new engine's `gf_v1` and `payload_v1` dispatch metadata; it is **not an approved production registry**. These are names from existing example scripts; actual ASAP GF availability, host execution signatures, rule ownership, and input routing require UAT.

`validation_registry_template.csv` is a byte-identical copy of the original registry template. Maintain stable `function_key`, `issue_code`, severity, and host script names. Avoid replacing a production registry with sample rows.
