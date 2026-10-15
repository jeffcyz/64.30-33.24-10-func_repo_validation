# Source and Host Migration Map

Every mapped source below is currently byte-identical to the legacy file. `deployment/asap/build.py --verify` checks this invariant.

| Existing host entry point | New authoring source |
| --- | --- |
| `ironpython_validation_helpers.py` | `src/validation_library/helpers/validation_helper_api.py` |
| `validation_api.py` | `src/validation_library/helpers/validation_helper_api.py` |
| `SetUpValidationStateCode.py` | `src/validation_library/rules/common/setup/SetUpValidationStateCode.py` |
| `validate_next_index_rate.py` | `src/validation_library/rules/common/payment/validate_next_index_rate.py` |
| `host_compatible/setup/SetUpValidationDealName.py` | `src/validation_library/rules/common/setup/SetUpValidationDealName.py` |
| `host_compatible/setup/SetUpValidationInterestTypeExpectations.py` | `src/validation_library/rules/common/setup/SetUpValidationInterestTypeExpectations.py` |
| `host_compatible/periodic/PeriodicValidationAssetScheduledBalanceRollover.py` | `src/validation_library/rules/cmbs/payment/PeriodicValidationAssetScheduledBalanceRollover.py` |
| `host_compatible/periodic/PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance.py` | `src/validation_library/rules/cmbs/payment/PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance.py` |
| `validation_registry_template.csv` | `configs/registry/validation_registry_template.csv` |

### Retained historic material

`ValidationEngine01.md`, `ValidationEngine02.md`, `setup/`, `periodic/`, `TODO/`, `example_validation_runner.py`, `host_compatible/` and existing `docs/` are unchanged. The `.txt` example snippets remain documentation; they have not been silently rewritten into importable modules.

### Safe follow-on migration

1. Validate first-function binding rules, GF names and import behavior in ASAP UAT.
2. Classify each existing rule's true asset-class applicability, setup/periodic stage and parameter contract.
3. Migrate only one proven rule group at a time into deployable artifacts.
4. Gate each group on golden output parity, UAT, business sign-off and controlled version bump.
5. Only after all consumers move off legacy paths should duplicate runtime entry points be removed.

Neither a new Git directory nor a Deal Manifest by itself changes what the host runs.
