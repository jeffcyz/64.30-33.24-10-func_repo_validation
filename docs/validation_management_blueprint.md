# Validation Management Blueprint

## What To Optimize For

- One source of truth for every validation script.
- Stable identifiers that work both in the host UI and in IronPython code.
- Clear severity, issue, explanation, impact, action, and context output.
- Reusable helpers so each validation function stays short.
- Consistent logging and easy filtering across many scripts.
- Easy onboarding for future additions and refactors.

## Recommended Model

Use three names for every validation:

- `script_name_display`: the exact name shown or referenced by the host system.
- `function_key`: a Python-safe internal identifier such as `periodic_validation_curr_sub_serv_fee_rate_versus_actual`.
- `issue_code`: a stable machine-friendly code such as `PERIODIC_FEE_RATE_MISMATCH`.

This split matters because some current script names appear to contain characters such as `:`, `%`, `/`, and `=`. Those are fine as display names but should not be your only internal identifier.

## Registry First

Do not spread metadata across individual scripts. Put the metadata in one registry file and let the functions stay focused on calculation logic.

Recommended registry columns:

- `script_name_display`
- `function_key`
- `focus`
- `asset`
- `type`
- `threshold`
- `severity`
- `issue_code`
- `description`
- `explanation`
- `impact`
- `action`
- `context_keys`
- `enabled`
- `owner`
- `notes`

Why this helps:

- You can audit all validations without opening every script.
- You can change message wording or severity without touching formula logic.
- You can report coverage by `focus`, `asset`, `type`, or severity.
- You can add dashboards, exports, or exception reports later with no major redesign.

## Severity And Logging

If the existing system already uses numeric thresholds, keep them. Add a matching logging severity so the rules are readable both to humans and to the runtime.

Suggested mapping:

| threshold | severity | logging level | meaning |
| --- | --- | --- | --- |
| 1 | DEBUG | `logging.DEBUG` | diagnostic only |
| 2 | INFO | `logging.INFO` | informational or low-risk setup issue |
| 3 | WARNING | `logging.WARNING` | important validation warning |
| 4 | ERROR | `logging.ERROR` | significant problem likely needing action |
| 5 | CRITICAL | `logging.CRITICAL` | blocking or release-critical issue |

Recommended result payload:

- `severity`
- `issue`
- `explanation`
- `impact`
- `action`
- `context`
- `script_name_display`
- `function_key`
- `focus`
- `asset`
- `type`
- `threshold`
- `issue_code`
- `status`
- `expected`
- `actual`

## Function Pattern

Each validation function should do only three things:

1. Read the needed inputs.
2. Evaluate one clear rule.
3. Return or emit one structured result.

Keep shared behavior in helpers:

- required field checks
- equality and tolerance checks
- balance roll-forward checks
- rate and percentage checks
- fee reconciliation checks
- structured log emission
- summary rollups

That gives you short business-rule functions and one shared output format.

## Suggested Folder Layout

```text
func_repo_validation/
  validation_inventory.md
  validation_management_blueprint.md
  validation_registry_template.csv
  ironpython_validation_helpers.py
  registry/
    validation_rules.csv
  setup/
  periodic/
```

Inside `setup/` and `periodic/`, group by `type` rather than by one huge flat list. That keeps related logic together and makes ownership clearer.

## Authoring Rules

- One function per rule.
- One rule per script name.
- No hardcoded severities inside business logic if they can live in the registry.
- No ad hoc free-text logging from every script. Route messages through the same helper.
- Default to passing rich `context` instead of concatenating long strings.
- Keep `issue`, `explanation`, `impact`, and `action` short and standardized.

## Message Design

Use these fields consistently:

- `issue`: one-line statement of what failed.
- `explanation`: why the rule exists or why the result is unexpected.
- `impact`: what could break downstream.
- `action`: what the operator or analyst should do next.
- `context`: the local facts needed to debug quickly.

Example:

```text
severity=ERROR
issue=Current bond balance does not reconcile to collateral balance
explanation=The current bond balance should roll from the prior period and reconcile to the linked collateral balance.
impact=Investor reporting, waterfall calculations, or exception sign-off may be unreliable.
action=Review remittance inputs, rollover logic, and collateral linkage for the current period.
context={"bond_id": "A1", "current_bond_balance": 102.50, "current_collateral_balance": 98.25, "difference": 4.25}
```

## Best Practice For Host-System Names

If the host system really calls validations by names such as `SetUpValidationDealContact:PrimaryAnalyst`, use a registry dispatcher:

- host system asks for `script_name_display`
- registry resolves it to `function_key`
- dispatcher calls the Python function object

That avoids forcing invalid characters into Python function names.

## Rollout Plan

1. Finalize the inventory and correct low-confidence OCR entries.
2. Populate a real registry CSV for all current validations.
3. Move common output behavior into shared helpers.
4. Refactor high-volume validations first, especially fee-versus-actual and rollover checks.
5. Add summary reporting by `focus`, `asset`, `type`, and `severity`.

## Anti-Patterns To Avoid

- Duplicating the same explanation text in dozens of scripts.
- Encoding business severity only in free text.
- Letting every script define its own output shape.
- Mixing setup validations and periodic validations in the same large file without a registry.
- Using the host display name as the only canonical identifier.
