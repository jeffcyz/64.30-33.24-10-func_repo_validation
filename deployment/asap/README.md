# ASAP deployment bundle builder

`python deployment/asap/build.py --verify` checks that every mapped legacy root entry is byte-identical to its canonical source in `src/`.

`python deployment/asap/build.py --build` writes the staging bundle under `dist/asap/`, plus a SHA-256 `artifact_manifest.json`.

This script **does not** communicate with ASAP, rewrite existing root scripts or publish a Release. The bundle preserves the existing per-script first-callable interface. It does **not** package the new development `ValidationEngine` as a global host function.

Review the mapping table in `docs/migration_map.md` and complete host UAT. The current bundle covers **only already implemented scripts**, not every validation described by `docs/validation_inventory.md`.
