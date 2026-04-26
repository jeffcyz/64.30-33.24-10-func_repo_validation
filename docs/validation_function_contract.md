# Validation Function Contract

## Core Rule

Each validation function should:

1. Read the needed fields from `payload`.
2. Perform one business check.
3. Return one structured result `dict`.

Do not return bare `True` or `False`.
Do not print ad hoc messages from the validation function.
Do not depend on runtime class instances from another script.

## Preferred Runtime Shape

For this IronPython environment, the deployable pattern is:

- one validation script
- one first callable function in that script
- one call into `ValidationHelperApi(...)`
- one structured `dict` returned

## Result Shape

Each validation should return a `dict` with these fields:

- `script_name_display`
- `function_key`
- `status`
- `passed`
- `severity`
- `threshold`
- `issue_code`
- `issue`
- `explanation`
- `impact`
- `action`
- `context`
- `expected`
- `actual`

## Function Template

```python
from ironpython_validation_helpers import ValidationHelperApi

VALIDATION_METADATA = {
    "script_name_display": "PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance",
    "threshold": 3,
    "severity": "WARNING",
    "issue_code": "PERIODIC_BOND_VS_COLLATERAL_BALANCE",
    "explanation": "Current bond balance should reconcile to the linked collateral balance for the reporting period.",
    "impact": "Bond reporting and waterfall checks may be unreliable.",
    "action": "Review bond-collateral mapping, remittance inputs, and rollover logic.",
}


def PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance(payload, runtime_context=None, logger=None):
    return ValidationHelperApi(
        operation="within_tolerance",
        metadata=VALIDATION_METADATA,
        runtime_context=runtime_context,
        logger=logger,
        actual=payload.get("current_bond_balance"),
        expected=payload.get("current_collateral_balance"),
        tolerance=0.01,
        field_name="current bond balance vs collateral balance",
        context={"bond_id": payload.get("bond_id")},
        issue="Current bond balance does not reconcile to collateral balance",
    )
```

## Where To Put What

Put in `VALIDATION_METADATA`:

- script name
- function key
- threshold
- severity
- issue code
- stable explanation / impact / action

Put in the validation function body:

- payload field lookups
- derived expected values
- current-run context
- dynamic issue overrides when needed

## Pass And Fail Behavior

For `PASS`:

- default severity should be `INFO`
- issue text can stay empty
- keep `expected`, `actual`, and `context` when useful for audit

For `FAIL`:

- use metadata defaults unless the current rule needs more specific text
- make the output actionable without requiring the reader to inspect code

## Summary Pattern

If you need to aggregate many results, keep the validation functions simple and summarize later:

```python
summary = ValidationHelperApi(
    operation="summarize_results",
    results=result_list,
    minimum_severity="WARNING",
)
```

This keeps rule evaluation separate from reporting.
