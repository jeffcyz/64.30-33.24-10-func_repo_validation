# Validation Example Patterns

These examples cover the four most common rule shapes:

- required field
- expected value equality
- tolerance comparison
- roll-forward reconciliation

## Files

- `setup/setup_validation_examples.py`
- `periodic/periodic_validation_examples.py`
- `example_validation_runner.py`

## Reuse Pattern

When you add a new validation, copy the closest example and change:

- `script_name_display`
- metadata values
- payload field names
- comparison logic
- issue / explanation / impact / action
- context keys

## Authoring Checklist

- one validation function per rule
- one rule per script name
- return one structured `dict`
- keep field reads and business logic short
- route shared formatting through `ValidationHelperApi(...)`
- pass `expected` and `actual` whenever possible

## What To Keep Out Of The Function

Avoid these inside an individual validation function:

- long custom log formatting
- global warning counters
- cross-rule aggregation
- final reporting
- runtime class construction from another script

Keep those concerns in the shared helper and summary step.
