# ASAP Validation Library

**Status: development migration; NOT approved for ASAP Production.**

This repo holds shared validation logic used by multiple securitization Deals / Portfolios. It is being reorganized into a modular **authoring** layout while preserving all existing ASAP host script entry points.

## Layout

| Path | Responsibility |
| --- | --- |
| `src/validation_library/runtime/` | Adapter for calls through the ASAP `gf` namespace |
| `src/validation_library/core/` | Engine, registry validation, context routing, severity and result contracts |
| `src/validation_library/rules/` | Shared and asset-class-specific rules (setup/periodic mapped to requested setup/payment folders) |
| `src/validation_library/helpers/` | Canonical copy of existing `ValidationHelperApi` helper |
| `configs/registry/` | Registry template and **illustrative only** rule mapping |
| `configs/deal_manifests/` | Example Deal config (**not** a deployed version pin) |
| `tests/` | Fast unit, registry, contract, integration, golden, and UAT guidance |
| `deployment/asap/` | Reproducible legacy-shaped bundle builder; never deploys itself |
| `docs/` | Architecture, API behavior, migration map, compatibility and release instructions |

## Quickstart (local CPython development)

```bash
python -m unittest discover -s tests -p "test_*.py"
python deployment/asap/build.py --verify
python deployment/asap/build.py --build
```

The resulting `dist/asap/` directory is a **staging artifact**, not a deployment. Before using it in ASAP, verify source mappings and actual host behavior in a non-production Deal. `src/validation_library/core/engine.py` is new and must not be assumed interchangeable with legacy production GF code.

## Compatibility commitment

All existing root-level ASAP entry points, `host_compatible/` scripts, historic docs and TODOs are retained **unchanged** in this branch. The source mirrors under `src/` are byte-identical to their originals, checked by tests. The root `validation_api.py` and `ironpython_validation_helpers.py` currently contain identical helper code, so a single source generates both.

This is a staged migration, **not** an upgrade or deployment of existing Deals.

See [Architecture](docs/architecture.md), [Migration Map](docs/migration_map.md), [Contract](docs/validation_contract.md), [Compatibility Matrix](docs/compatibility_matrix.md), and [Release Process](docs/release_process.md).

**Security:** Never commit real Deal datasets, PII, credentials or confidential issuer material to this public repository.
