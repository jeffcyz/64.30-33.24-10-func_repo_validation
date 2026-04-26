# Host-Compatible Design For Asset Securitization Analysis Pro

## Runtime Constraint

This host environment has two important limits:

- cross-script calls can only target the other script's first function
- validation scripts should not depend on class instances created in another script

Because of that, the deployable design should stay simple and function-based.

## Recommended Shape

Use this pattern:

- one validation script
- one first callable validation function in that script
- one helper script
- one first callable helper entry in that script

That means:

```text
Validation Script
  -> ValidationHelperApi(...)
    -> internal pure functions
      -> structured result dict
```

## What To Avoid

Avoid these runtime patterns in the host system:

- `registry.helper(...).require(...)`
- decorator-driven registration that must happen before execution
- cross-script object construction
- helper scripts that require multiple callable entry points

## What To Use Instead

Each validation script should define:

- local metadata
- one public validation function
- one call to `ValidationHelperApi(...)`

Example:

```python
from ironpython_validation_helpers import ValidationHelperApi

VALIDATION_METADATA = {...}

def SetUpValidationDealName(payload, runtime_context=None, logger=None):
    return ValidationHelperApi(
        operation="required",
        metadata=VALIDATION_METADATA,
        runtime_context=runtime_context,
        logger=logger,
        value=payload.get("deal_name"),
        field_name="deal_name",
        context={"deal_id": payload.get("deal_id")},
        issue="Deal name is missing",
    )
```

## Why This Is Better Here

This pattern works well in the host because:

- every script can run independently
- no global runtime registration is required
- results stay structured and consistent
- warning level, issue text, explanation, impact, and action still stay standardized

## Files In This Folder

- `host_compatible/setup/SetUpValidationDealName.py`
- `host_compatible/setup/SetUpValidationInterestTypeExpectations.py`
- `host_compatible/periodic/PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance.py`
- `host_compatible/periodic/PeriodicValidationAssetScheduledBalanceRollover.py`
- `host_compatible/example_host_compatible_runner.py`

These examples are the closest match to the real host deployment model.
