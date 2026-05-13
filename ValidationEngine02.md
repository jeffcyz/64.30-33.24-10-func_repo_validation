# Agent Prompt: Refactor ASAP2 `ValidationEngine` to Use Boolean Result Controls Instead of Summary/Full Output Mode

The project already has a class named:

```python
class ValidationEngine(object):
    pass
````

The current `ValidationEngine` can run validation portfolios and print JSON output similar to:

```json
{
  "include_passed": false,
  "interrupt_enabled": false,
  "interrupt_severity": "CRITICAL",
  "output_mode": "summary",
  "portfolio_key": "rmbs_pmt",
  "portfolio_name": "RMBS Payment Validation Portfolio",
  "portfolio_summary": {
    "by_severity": {
      "ERROR": 1,
      "WARNING": 1
    },
    "failed_validations": 2,
    "highest_severity": null,
    "passed_validations": 5,
    "total_failed_records": 2,
    "total_passed_records": 2345,
    "total_records_checked": 2347,
    "total_validations": 7
  },
  "should_interrupt": false,
  "success": false,
  "validations": [
    {
      "success": false,
      "summary": {
        "by_severity": {
          "ERROR": 1
        },
        "fail": 1,
        "highest_severity": "ERROR",
        "pass": 0,
        "total": 1
      },
      "validates": "Total current credit support percent must be within the acceptable threshold.",
      "validation_key": "validate_periodic_cls_pct",
      "validation_name": "Periodic Credit Support Percent Validation"
    }
  ]
}
```

The current engine is close to the desired design, but the result-control interface needs to be refactored.

---

# Main Refactor Goal

Remove this parameter:

```python
output_mode="summary" or "full"
```

Do not use `"summary"` or `"full"` as commands anymore.

Instead, use explicit boolean parameters.

The engine must separately control two different levels of result inclusion:

1. Individual validation function execution level.
2. Final portfolio output level.

---

# Why This Refactor Is Needed

Existing ASAP2 validation functions often accept:

```python
runtime_context=None,
params=None,
include_results=False,
include_pass=False
```

Example:

```python
def validate_periodic_cls_pct(
    runtime_context=None,
    params=None,
    include_results=False,
    include_pass=False,
):
    ...
```

Here:

```python
include_results
```

controls whether the individual validation function returns detailed record-level results.

And:

```python
include_pass
```

controls whether that individual validation function includes passed records in its detailed result list.

However, the `ValidationEngine` also needs a separate portfolio-level display policy:

* show only the portfolio-level summary
* show failed validation summaries/details only
* show both failed and passed validation summaries/details

Therefore, the engine needs two layers of controls.

---

# Required New Parameters

Replace `output_mode` with these boolean controls.

## Layer 1: Individual Validation Function Controls

These parameters are passed down into each `gf` validation function.

```python
function_include_results=False
function_include_passed=False
```

Meaning:

### `function_include_results`

Controls whether each individual `gf` validation function is asked to return detailed record-level results.

It maps to the validation function argument:

```python
include_results=function_include_results
```

### `function_include_passed`

Controls whether each individual `gf` validation function includes passed records in its detailed result list.

It maps to the validation function argument:

```python
include_pass=function_include_passed
```

Important:

* If `function_include_results=False`, the individual validation function may return only `summary`.
* If `function_include_results=True` and `function_include_passed=False`, the individual validation function should return failed records only.
* If `function_include_results=True` and `function_include_passed=True`, the individual validation function should return both failed and passed records.

---

## Layer 2: Portfolio Final Output Controls

These parameters control what the final `ValidationEngine` payload shows.

```python
portfolio_include_results=True
portfolio_include_passed=False
```

Meaning:

### `portfolio_include_results`

Controls whether the final portfolio payload includes the `validations` list.

If:

```python
portfolio_include_results=False
```

then the final payload should only show portfolio-level fields:

```python
{
    "portfolio_key": "...",
    "portfolio_name": "...",
    "success": true or false,
    "should_interrupt": true or false,
    "interrupt_enabled": true or false,
    "interrupt_severity": "...",
    "function_include_results": false,
    "function_include_passed": false,
    "portfolio_include_results": false,
    "portfolio_include_passed": false,
    "portfolio_summary": {...}
}
```

No validation-level output should appear.

If:

```python
portfolio_include_results=True
```

then the final payload should include:

```python
"validations": [...]
```

### `portfolio_include_passed`

Controls whether passed validations are included in the final `validations` list.

If:

```python
portfolio_include_passed=False
```

then the final `validations` list should include only failed validations.

If:

```python
portfolio_include_passed=True
```

then the final `validations` list should include both failed and passed validations.

Important:

This is validation-level filtering, not record-level filtering.

Record-level passed filtering is controlled by:

```python
function_include_passed
```

---

# New `run_portfolio` Signature

Refactor `run_portfolio()` to use this signature:

```python
def run_portfolio(self, portfolio_key,
                  assets=None,
                  bonds=None,
                  deal=None,
                  fees=None,
                  accounts=None,
                  period=None,
                  payment_date=None,
                  distribution_date=None,
                  model=None,
                  runtime_context=None,

                  function_include_results=False,
                  function_include_passed=False,
                  portfolio_include_results=True,
                  portfolio_include_passed=False,

                  return_results=True,
                  print_results=False,
                  interrupt_enabled=None,
                  interrupt_severity=None,
                  raise_on_interrupt=False):
    pass
```

Remove or deprecate:

```python
output_mode
include_passed
```

If backward compatibility is needed, `output_mode` and old `include_passed` may be accepted temporarily, but the new design should be based on the four explicit boolean controls.

---

# Result Control Matrix

The engine should support these common modes.

## 1. Portfolio Summary Only

Use this when the user only wants portfolio-level summary.

```python
engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=False,
    function_include_passed=False,
    portfolio_include_results=False,
    portfolio_include_passed=False,
    print_results=True,
    return_results=False
)
```

Expected output:

```json
{
  "portfolio_key": "rmbs_pmt",
  "portfolio_name": "RMBS Payment Validation Portfolio",
  "success": false,
  "should_interrupt": false,
  "interrupt_enabled": false,
  "interrupt_severity": "CRITICAL",
  "function_include_results": false,
  "function_include_passed": false,
  "portfolio_include_results": false,
  "portfolio_include_passed": false,
  "portfolio_summary": {
    "total_validations": 7,
    "passed_validations": 5,
    "failed_validations": 2,
    "total_records_checked": 2347,
    "total_passed_records": 2345,
    "total_failed_records": 2,
    "highest_severity": "ERROR",
    "by_severity": {
      "ERROR": 1,
      "WARNING": 1
    }
  }
}
```

No `validations` list should appear.

---

## 2. Portfolio Summary + Failed Validation Summaries

Use this as the recommended default.

```python
engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=False,
    function_include_passed=False,
    portfolio_include_results=True,
    portfolio_include_passed=False,
    print_results=True,
    return_results=False
)
```

Expected behavior:

* Individual validation functions return summary only.
* Final payload includes only failed validations.
* Since `function_include_results=False`, validation-level records are not available.
* Each failed validation still shows metadata and summary.

Expected structure:

```json
{
  "portfolio_key": "rmbs_pmt",
  "portfolio_name": "RMBS Payment Validation Portfolio",
  "success": false,
  "should_interrupt": false,
  "function_include_results": false,
  "function_include_passed": false,
  "portfolio_include_results": true,
  "portfolio_include_passed": false,
  "portfolio_summary": {...},
  "validations": [
    {
      "validation_key": "validate_periodic_cls_pct",
      "validation_name": "Periodic Credit Support Percent Validation",
      "validates": "Total current credit support percent must be within the acceptable threshold.",
      "success": false,
      "summary": {
        "pass": 0,
        "fail": 1,
        "total": 1,
        "highest_severity": "ERROR",
        "by_severity": {
          "ERROR": 1
        }
      }
    }
  ]
}
```

---

## 3. Portfolio Summary + Failed Validation Details

Use this when the user wants failed detailed records.

```python
engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=True,
    function_include_passed=False,
    portfolio_include_results=True,
    portfolio_include_passed=False,
    print_results=True,
    return_results=False
)
```

Expected behavior:

* Individual validation functions are called with:

  ```python
  include_results=True
  include_pass=False
  ```
* Final output includes only failed validations.
* Each failed validation includes failed detailed records if returned by the validation function.

Expected structure:

```json
{
  "portfolio_key": "rmbs_pmt",
  "portfolio_name": "RMBS Payment Validation Portfolio",
  "success": false,
  "should_interrupt": false,
  "function_include_results": true,
  "function_include_passed": false,
  "portfolio_include_results": true,
  "portfolio_include_passed": false,
  "portfolio_summary": {...},
  "validations": [
    {
      "validation_key": "validate_periodic_cls_pct",
      "validation_name": "Periodic Credit Support Percent Validation",
      "validates": "Total current credit support percent must be within the acceptable threshold.",
      "success": false,
      "summary": {...},
      "results": [
        {
          "status": "FAIL",
          "passed": false,
          "severity": "ERROR",
          "issue_code": "...",
          "issue": "...",
          "expected": "...",
          "actual": "..."
        }
      ]
    }
  ]
}
```

---

## 4. Full Audit Output Including Passed Validations and Passed Records

Use this when the user wants everything.

```python
engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=True,
    function_include_passed=True,
    portfolio_include_results=True,
    portfolio_include_passed=True,
    print_results=True,
    return_results=True
)
```

Expected behavior:

* Individual validation functions are called with:

  ```python
  include_results=True
  include_pass=True
  ```
* Final payload includes both failed and passed validations.
* Detailed results may include both failed and passed records.

---

# Function-Level Call Behavior

When running each validation, call the gf function with the new explicit function-level controls.

Preferred call:

```python
raw_result = func(
    runtime_context=selected_runtime_context,
    params=params,
    include_results=function_include_results,
    include_pass=function_include_passed
)
```

Fallback calls should preserve the same order as the existing engine:

```python
func(selected_runtime_context, params, function_include_results, function_include_passed)
func(selected_runtime_context, params)
func(selected_runtime_context)
func()
```

If all calls fail, convert the exception into a standardized CRITICAL validation output.

---

# Portfolio-Level Filtering Behavior

The engine should always run all validations in the selected portfolio.

It should always use all validation summaries to build `portfolio_summary`.

Then it should apply portfolio-level filtering only when building the final output payload.

Rules:

1. `portfolio_summary` must include all validations, both passed and failed.
2. `passed_validations` and `failed_validations` must count all validations.
3. `total_records_checked`, `total_passed_records`, and `total_failed_records` must count all validations.
4. If `portfolio_include_results=False`, do not include the `validations` list at all.
5. If `portfolio_include_results=True` and `portfolio_include_passed=False`, include only failed validations in the final `validations` list.
6. If `portfolio_include_results=True` and `portfolio_include_passed=True`, include both failed and passed validations in the final `validations` list.
7. If detailed records exist, include them inside each validation output.
8. If detailed records do not exist because `function_include_results=False`, do not fabricate them.

---

# Naming Rules

Remove these old keys from the final output:

```json
"output_mode": "summary"
"include_passed": false
```

Replace them with:

```json
"function_include_results": false,
"function_include_passed": false,
"portfolio_include_results": true,
"portfolio_include_passed": false
```

This makes it clear which layer each setting controls.

---

# Runtime Context Handling

Keep the current explicit runtime object design.

`run_portfolio()` should support:

```python
assets=assets
bonds=bonds
deal=deal
fees=fees
accounts=accounts
period=period
payment_date=payment_date
distribution_date=distribution_date
model=model
runtime_context=runtime_context
```

Build a context bundle internally.

Explicit inputs should override same-named values from `runtime_context`.

Each validation registry item should still define:

```python
runtime_context_key
```

Examples:

```python
runtime_context_key="assets"
runtime_context_key="bonds"
runtime_context_key="deal"
runtime_context_key="context"
runtime_context_key=None
```

Routing rules:

```text
runtime_context_key="assets"  -> pass assets as runtime_context
runtime_context_key="bonds"   -> pass bonds as runtime_context
runtime_context_key="deal"    -> pass deal as runtime_context
runtime_context_key="context" -> pass the full context bundle as runtime_context
runtime_context_key=None      -> pass None as runtime_context
```

---

# GF Function Registry Design

Keep the existing internal registry design.

Each validation should store `gf_function_name` as a string.

Example:

```python
self.validations["validate_periodic_cls_pct"] = {
    "key": "validate_periodic_cls_pct",
    "name": "Periodic Credit Support Percent Validation",
    "validates": "Total current credit support percent must be within the acceptable threshold.",
    "gf_function_name": "validate_periodic_cls_pct",
    "category": "pmt",
    "asset_class": "rmbs",
    "default_severity": "ERROR",
    "runtime_context_key": "bonds",
    "enabled": True,
    "default_params": {}
}
```

At runtime:

```python
func = getattr(self.gf, gf_function_name)
```

Do not switch to direct function attributes.

---

# JSON String Output Support

Keep support for validation functions returning JSON strings.

Many validation functions return:

```python
return gf.validation_main(
    operation="to_json",
    payload=payload
)
```

The engine must continue to parse:

```text
JSON string
dict
list of dict
dict with summary/results
None
```

The engine must preserve per-validation summaries if returned.

This is especially important when:

```python
function_include_results=False
```

because the validation may return summary but no detailed results.

---

# Severity and Interruption Behavior

Keep severity-threshold interruption only.

Do not implement `any_fail`.

Support:

```python
interrupt_enabled=True
interrupt_severity="CRITICAL"
raise_on_interrupt=True
```

The engine should determine interruption from portfolio-level summary and/or detailed results.

Rules:

1. `should_interrupt=True` only if `interrupt_enabled=True`.
2. `should_interrupt=True` only if highest failed severity is equal to or above `interrupt_severity`.
3. The engine must build the final payload before raising interruption.
4. If `print_results=True`, the engine must print the payload before raising interruption.
5. Interruption should not depend on whether `portfolio_include_results` is true or false.
6. Interruption should not depend on whether detailed records were included.
7. Interruption must use the full portfolio summary, not only displayed validations.

Suggested host message:

```python
def _build_host_message(self, portfolio_summary):
    failed = portfolio_summary.get("total_failed_records", 0)
    return "{} validation errors raised, test failed, download log to view detail".format(failed)
```

Update portfolio `highest_severity` correctly.

Do not leave `highest_severity` as `null` if `by_severity` contains failures.

For example:

```json
"by_severity": {
  "ERROR": 1,
  "WARNING": 1
}
```

should produce:

```json
"highest_severity": "ERROR"
```

---

# Missing GF Function Handling

If a registered `gf_function_name` does not exist on `self.gf`, return a standardized failed validation output.

This output must be included in portfolio summary even if `portfolio_include_results=False`.

Use severity:

```python
"CRITICAL"
```

Issue code:

```python
"VALIDATION_GF_FUNCTION_NOT_FOUND"
```

---

# Runtime Error Handling

If a `gf` validation function raises an exception, return a standardized failed validation output.

This output must be included in portfolio summary even if `portfolio_include_results=False`.

Use severity:

```python
"CRITICAL"
```

Issue code:

```python
"VALIDATION_FUNCTION_RUNTIME_ERROR"
```

---

# Missing Runtime Context Handling

If a validation has:

```python
runtime_context_required=True
```

and its required context object is missing, return a standardized failed validation output.

This output must be included in portfolio summary even if `portfolio_include_results=False`.

Use severity:

```python
"CRITICAL"
```

Issue code:

```python
"VALIDATION_RUNTIME_CONTEXT_MISSING"
```

---

# Required Code Changes

Update `ValidationEngine` so that:

1. `output_mode` is removed from the main logic.
2. `include_passed` is removed from the main logic.
3. `function_include_results` controls the validation function call argument `include_results`.
4. `function_include_passed` controls the validation function call argument `include_pass`.
5. `portfolio_include_results` controls whether final payload includes the `validations` list.
6. `portfolio_include_passed` controls whether passed validations appear in the final `validations` list.
7. Portfolio summary always includes all validations.
8. Interruption always uses all validations, not just displayed validations.
9. Output payload prints the new boolean settings.
10. Backward compatibility for old `output_mode` is optional, but the preferred API should use booleans only.

---

Default values should resolve as:

```python
if function_include_results is None:
    function_include_results = self.default_function_include_results

if function_include_passed is None:
    function_include_passed = self.default_function_include_passed

if portfolio_include_results is None:
    portfolio_include_results = self.default_portfolio_include_results

if portfolio_include_passed is None:
    portfolio_include_passed = self.default_portfolio_include_passed
```

---

# Updated Internal Helper Methods

Update or create helpers similar to:

```python
def _run_validation(self, validation_key, context_bundle,
                    function_include_results=False,
                    function_include_passed=False):
    pass

def _call_gf_validation(self, validation_meta, selected_runtime_context,
                        function_include_results=False,
                        function_include_passed=False):
    pass

def _build_output_payload(self, portfolio_key, portfolio_meta,
                          validation_outputs, portfolio_summary,
                          function_include_results,
                          function_include_passed,
                          portfolio_include_results,
                          portfolio_include_passed,
                          interrupt_enabled,
                          interrupt_severity,
                          should_interrupt):
    pass
```

The old helper arguments using `output_mode` should be removed or adapted.

---

# Acceptance Criteria

The refactor is complete only if:

1. `ValidationEngine` no longer depends on `output_mode="summary"` or `output_mode="full"` as the primary interface.
2. `function_include_results` is passed to each gf validation as `include_results`.
3. `function_include_passed` is passed to each gf validation as `include_pass`.
4. `portfolio_include_results=False` produces portfolio-level summary only.
5. `portfolio_include_results=True` includes validation-level output.
6. `portfolio_include_passed=False` includes only failed validations in the final displayed validation list.
7. `portfolio_include_passed=True` includes both failed and passed validations in the final displayed validation list.
8. Portfolio summary always includes all validations, regardless of portfolio display filtering.
9. Interruption uses all validation results/summaries, not only displayed validations.
10. Interruption works even when `portfolio_include_results=False`.
11. Summary output can be printed before interruption.
12. JSON-string validation outputs are still parsed correctly.
13. Per-validation summaries are still preserved.
14. Detailed records are included only when `function_include_results=True` and the validation function returns them.
15. Passed detailed records are included only when `function_include_passed=True`.
16. Final payload includes the four new boolean settings:

    * `function_include_results`
    * `function_include_passed`
    * `portfolio_include_results`
    * `portfolio_include_passed`
17. Old output keys `output_mode` and `include_passed` are removed from new payloads.
18. Severity order supports `ERROR` and `WARNING`.
19. `highest_severity` is correctly calculated from `by_severity`.
20. Missing gf function, runtime errors, and missing runtime context still produce standardized CRITICAL validation outputs.
21. Code remains compatible with ASAP2 / IronPython as much as practical.

---

# Example Final Usage

## Portfolio summary only

```python
engine = ValidationEngine(gf)

engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=False,
    function_include_passed=False,
    portfolio_include_results=False,
    portfolio_include_passed=False,
    return_results=False,
    print_results=True,
    interrupt_enabled=False,
    interrupt_severity="CRITICAL",
    raise_on_interrupt=False
)
```

## Failed validation summaries only

```python
engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=False,
    function_include_passed=False,
    portfolio_include_results=True,
    portfolio_include_passed=False,
    return_results=False,
    print_results=True
)
```

## Failed validation details only

```python
engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=True,
    function_include_passed=False,
    portfolio_include_results=True,
    portfolio_include_passed=False,
    return_results=False,
    print_results=True
)
```

## Full audit output

```python
payload = engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    function_include_results=True,
    function_include_passed=True,
    portfolio_include_results=True,
    portfolio_include_passed=True,
    return_results=True,
    print_results=True
)
```

---

# Final Response Required After Implementation

After implementing the refactor, report:

1. Files modified.
2. Updated `ValidationEngine.__init__` signature.
3. Updated `run_portfolio` signature.
4. Explanation of the two-level result-control design.
5. Example output for portfolio summary only.
6. Example output for failed validation summaries only.
7. Example output for failed validation details only.
8. Example output for full audit output.
9. How `function_include_results` maps to validation function `include_results`.
10. How `function_include_passed` maps to validation function `include_pass`.
11. How `portfolio_include_results` controls the final `validations` list.
12. How `portfolio_include_passed` filters passed validations.
13. How interruption still uses all validations.
14. Any backward compatibility notes for old `output_mode` and `include_passed`.

Do not only plan. Implement the refactor directly.

```

这版 prompt 已经把你现在的核心问题拆清楚了：**function 层负责“要不要让每个 validation function 产生 detailed records”；portfolio 层负责“最终展示 portfolio summary、failed validations、还是 passed validations 也展示”。**
```
