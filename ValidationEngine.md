# Agent Prompt: Build ASAP2 `ValidationEngine` with Internal GF Registry and Explicit Runtime Inputs

ASAP2 exposes reusable global functions through the `gf` namespace. Existing validation functions can be called like:

```python
gf.validate_setup_bond_first_pay_date(...)
gf.validate_periodic_cls_pct(...)
gf.set_up_validation_state_code(...)
gf.validate_next_index_rate(...)
````

The goal is to build a class named exactly:

```python
class ValidationEngine(object):
    pass
```

This class should orchestrate existing `gf` validation functions into named validation portfolios.

---

# Core Design

`ValidationEngine` should be a portfolio orchestration layer.

It should not dynamically import validation files.

It should not require the caller to manually register validation functions.

It should not require the caller to manually create portfolios.

Instead, `ValidationEngine` internally manages:

1. Validation registry.
2. Portfolio registry.
3. Mapping from validation key to `gf_function_name`.
4. Mapping from portfolio key to validation keys.
5. Runtime object routing.
6. Output mode.
7. Whether passed records are included.
8. Return versus print behavior.
9. Severity-threshold interruption behavior.
10. Optional future email notification placeholder.

At runtime, each validation function should be resolved using:

```python
func = getattr(self.gf, gf_function_name)
```

Do not store every validation function as a direct instance attribute such as:

```python
self.validate_a = gf.validate_a
```

The preferred structure is metadata-driven:

```python
self.validations["validate_setup_bond_first_pay_date"] = {
    "key": "validate_setup_bond_first_pay_date",
    "name": "Bond Setup First Pay Date Validation",
    "validates": "Bond setup FirstPayDate must be populated.",
    "gf_function_name": "validate_setup_bond_first_pay_date",
    "category": "setup",
    "asset_class": "shared",
    "default_severity": "CRITICAL",
    "runtime_context_key": "bonds",
    "enabled": True,
    "default_params": {}
}
```

---

# Existing Validation Function Pattern

Many existing validation functions follow a pattern similar to:

```python
SCRIPT_NAME_DISPLAY = "Bond Setup First Pay Date Validation"
FUNCTION_KEY = "validate_setup_first_pay_date"
ISSUE_CODE = "BOND_SETUP_FIRST_PAY_DATE_NULL"

def validate_setup_bond_first_pay_date(
    runtime_context=None,
    params=None,
    include_results=False,
    include_pass=False,
):
    bds = bonds if runtime_context is None else runtime_context

    results = []

    for bd in bds:
        result = _check_first_pay_date(...)
        results.append(result)

    summary = gf.validation_main(
        operation="summarize_results",
        results=results,
    )

    payload = {
        "validation": FUNCTION_KEY,
        "success": summary.get("fail", 0) == 0,
        "summary": summary,
    }

    if include_results:
        payload["results"] = [
            {k: v for k, v in result.items() if v is not None}
            for result in results
            if include_pass or result.get("status") != "PASS"
        ]

    return gf.validation_main(
        operation="to_json",
        payload=payload,
    )
```

Therefore, `ValidationEngine` must support validation functions that return JSON strings, not only dictionaries.

Typical returned validation payload may look like:

```json
{
  "success": true,
  "summary": {
    "by_severity": {},
    "pass": 1,
    "highest_severity": null,
    "fail": 0,
    "total": 1
  },
  "results": [
    {
      "script_name_display": "Periodic Credit Support Percent Validation",
      "actual": "0.0000000000",
      "function_key": "validate_periodic_cls_pct",
      "issue_code": "CURR_CRED_SUPP_PCT_SUM_EXCEEDS_100",
      "explanation": "The sum of CurrCredSuppPct across all bonds for period '2' is 0.0000000000, which is strictly less than 100. Check passed.",
      "passed": true,
      "expected": "< 100",
      "context": {
        "raw_total": "0.0000000000",
        "period": 2
      },
      "status": "PASS",
      "severity": "INFO",
      "issue": "Total CurrCredSuppPct is within acceptable range (< 100%)"
    }
  ],
  "validation": "validate_periodic_cls_pct"
}
```

---

# Desired External Usage

The caller should only instantiate the engine with `gf`, then call a portfolio with explicit runtime objects and output settings.

Example for setup validation:

```python
engine = ValidationEngine(gf)

engine.run_portfolio(
    portfolio_key="rmbs_setup",
    assets=assets,
    bonds=bonds,
    deal=deal,
    output_mode="summary",
    include_passed=False,
    return_results=False,
    print_results=True,
    interrupt_enabled=True,
    interrupt_severity="CRITICAL",
    raise_on_interrupt=True
)
```

Example for payment validation:

```python
engine = ValidationEngine(gf)

payload = engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    deal=deal,
    period=period,
    payment_date=payment_date,
    output_mode="full",
    include_passed=False,
    return_results=True,
    print_results=False,
    interrupt_enabled=True,
    interrupt_severity="HIGH",
    raise_on_interrupt=False
)
```

The caller should not need to know which individual `gf` functions are inside the selected portfolio.

---

# File to Create

Create:

```text
validation_engine.py
```

The class inside the file must be:

```python
class ValidationEngine(object):
    pass
```

Keep the file self-contained if practical.

---

# Class Initialization

Implement:

```python
def __init__(self, gf,
             default_output_mode="summary",
             default_include_passed=False,
             default_interrupt_enabled=True,
             default_interrupt_severity="CRITICAL"):
    self.gf = gf

    self.default_output_mode = default_output_mode
    self.default_include_passed = default_include_passed
    self.default_interrupt_enabled = default_interrupt_enabled
    self.default_interrupt_severity = default_interrupt_severity

    self.validations = {}
    self.portfolios = {}

    self._register_default_validations()
    self._register_default_portfolios()
```

`ValidationEngine` should be usable immediately after instantiation.

No external registration step should be required.

---

# Public API

Expose these public methods:

```python
class ValidationEngine(object):

    def __init__(self, gf,
                 default_output_mode="summary",
                 default_include_passed=False,
                 default_interrupt_enabled=True,
                 default_interrupt_severity="CRITICAL"):
        pass

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
                      output_mode=None,
                      include_passed=None,
                      return_results=True,
                      print_results=False,
                      interrupt_enabled=None,
                      interrupt_severity=None,
                      raise_on_interrupt=False):
        pass

    def list_portfolios(self):
        pass

    def list_validations(self):
        pass

    def get_portfolio_definition(self, portfolio_key):
        pass

    def get_validation_definition(self, validation_key):
        pass

    def send_email_notification(self, payload, email_options=None):
        pass
```

Do not require external users to call:

```python
engine.register_validation(...)
engine.create_portfolio(...)
```

Registration should be internal only.

---

# Explicit Runtime Object Inputs

`run_portfolio()` must support explicit runtime object inputs:

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
```

It should also support an optional `runtime_context` dictionary.

Inside `run_portfolio()`, build a context bundle.

Suggested helper:

```python
def _build_context_bundle(self, runtime_context=None,
                          assets=None, bonds=None, deal=None,
                          fees=None, accounts=None,
                          period=None, payment_date=None,
                          distribution_date=None, model=None):
    bundle = {}

    if isinstance(runtime_context, dict):
        bundle.update(runtime_context)

    if assets is not None:
        bundle["assets"] = assets

    if bonds is not None:
        bundle["bonds"] = bonds

    if deal is not None:
        bundle["deal"] = deal

    if fees is not None:
        bundle["fees"] = fees

    if accounts is not None:
        bundle["accounts"] = accounts

    if period is not None:
        bundle["period"] = period

    if payment_date is not None:
        bundle["payment_date"] = payment_date

    if distribution_date is not None:
        bundle["distribution_date"] = distribution_date

    if model is not None:
        bundle["model"] = model

    return bundle
```

Explicit inputs must override same-named values from `runtime_context`.

For example:

```python
runtime_context = {"bonds": old_bonds}

engine.run_portfolio(
    portfolio_key="rmbs_setup",
    runtime_context=runtime_context,
    bonds=new_bonds
)
```

The engine should use `new_bonds`.

---

# Runtime Context Routing

Each validation registry item must define which runtime object it needs.

Use a field named:

```python
runtime_context_key
```

Examples:

```python
runtime_context_key="assets"
runtime_context_key="bonds"
runtime_context_key="deal"
runtime_context_key="fees"
runtime_context_key="accounts"
runtime_context_key="context"
runtime_context_key=None
```

Meaning:

```text
runtime_context_key="assets"  -> pass assets as runtime_context
runtime_context_key="bonds"   -> pass bonds as runtime_context
runtime_context_key="deal"    -> pass deal as runtime_context
runtime_context_key="context" -> pass the full context bundle as runtime_context
runtime_context_key=None      -> pass None as runtime_context
```

This is required because existing ASAP2 validation functions usually expect `runtime_context` to be the direct object they iterate over, such as `assets` or `bonds`, not the full dictionary.

Example:

```python
def validate_setup_bond_first_pay_date(
    runtime_context=None,
    params=None,
    include_results=False,
    include_pass=False,
):
    bds = bonds if runtime_context is None else runtime_context
```

This function should receive:

```python
runtime_context=bonds
```

not:

```python
runtime_context={
    "assets": assets,
    "bonds": bonds,
    "deal": deal
}
```

---

# Runtime Context Resolver

Implement:

```python
def _resolve_runtime_context(self, validation_meta, context_bundle):
    runtime_context_key = validation_meta.get("runtime_context_key")

    if runtime_context_key == "context":
        return context_bundle

    if runtime_context_key:
        return context_bundle.get(runtime_context_key)

    return None
```

Optional enhancement:

Each validation may also include:

```python
runtime_context_required=True
allow_global_context_fallback=True
```

If `runtime_context_required=True` and the selected object is missing, return a standardized CRITICAL validation output instead of crashing.

If `allow_global_context_fallback=True`, missing selected context may return `None`, allowing the validation function to use ASAP2 global objects such as global `bonds` or `assets`.

---

# Internal Validation Registry

Implement:

```python
def _register_default_validations(self):
    pass
```

Use an internal helper:

```python
def _add_validation(self, key, name, validates, gf_function_name,
                    category=None,
                    asset_class=None,
                    default_severity="HIGH",
                    enabled=True,
                    default_params=None,
                    description=None,
                    metadata=None,
                    runtime_context_key=None,
                    runtime_context_required=False,
                    allow_global_context_fallback=True):
    pass
```

Each validation record should contain:

```python
{
    "key": "...",
    "name": "...",
    "validates": "...",
    "gf_function_name": "...",
    "category": "...",
    "asset_class": "...",
    "default_severity": "...",
    "enabled": True,
    "default_params": {},
    "description": "...",
    "metadata": {},
    "runtime_context_key": "...",
    "runtime_context_required": False,
    "allow_global_context_fallback": True
}
```

Use real existing validation function names where available.

Include at least these examples or placeholders:

```python
self._add_validation(
    key="validate_setup_bond_first_pay_date",
    name="Bond Setup First Pay Date Validation",
    validates="Bond setup FirstPayDate must be populated.",
    gf_function_name="validate_setup_bond_first_pay_date",
    category="setup",
    asset_class="shared",
    default_severity="CRITICAL",
    runtime_context_key="bonds"
)

self._add_validation(
    key="validate_periodic_cls_pct",
    name="Periodic Credit Support Percent Validation",
    validates="Total current credit support percent should be within the acceptable threshold.",
    gf_function_name="validate_periodic_cls_pct",
    category="pmt",
    asset_class="shared",
    default_severity="HIGH",
    runtime_context_key="bonds"
)

self._add_validation(
    key="setup_state_code",
    name="State Code Validation",
    validates="Asset setup State field must contain a valid US state or territory code.",
    gf_function_name="set_up_validation_state_code",
    category="setup",
    asset_class="shared",
    default_severity="CRITICAL",
    runtime_context_key="assets"
)

self._add_validation(
    key="next_index_rate",
    name="Next Index Rate Validation",
    validates="Floating-rate bonds must have populated and non-zero NextIndexRate.",
    gf_function_name="validate_next_index_rate",
    category="pmt",
    asset_class="shared",
    default_severity="HIGH",
    runtime_context_key="bonds"
)

self._add_validation(
    key="deal_name",
    name="Deal Name Validation",
    validates="Deal name must be populated and valid.",
    gf_function_name="validate_deal_name",
    category="setup",
    asset_class="shared",
    default_severity="HIGH",
    runtime_context_key="deal"
)
```

Adjust exact function names after inspecting the repository.

---

# Internal Portfolio Registry

Implement:

```python
def _register_default_portfolios(self):
    pass
```

Use an internal helper:

```python
def _add_portfolio(self, portfolio_key, name, validation_keys,
                   description=None,
                   default_output_mode="summary",
                   default_include_passed=False,
                   default_interrupt_enabled=True,
                   default_interrupt_severity="CRITICAL"):
    pass
```

Required portfolio keys:

```text
rmbs_setup
rmbs_pmt
cmbs_setup
cmbs_pmt
abs_setup
abs_pmt
```

Example:

```python
self._add_portfolio(
    portfolio_key="rmbs_setup",
    name="RMBS Setup Validation Portfolio",
    description="Standard RMBS setup validation checks.",
    validation_keys=[
        "validate_setup_bond_first_pay_date",
        "setup_state_code",
        "deal_name"
    ],
    default_output_mode="summary",
    default_include_passed=False,
    default_interrupt_enabled=True,
    default_interrupt_severity="CRITICAL"
)

self._add_portfolio(
    portfolio_key="rmbs_pmt",
    name="RMBS Payment Validation Portfolio",
    description="Standard RMBS payment and periodic validation checks.",
    validation_keys=[
        "validate_periodic_cls_pct",
        "next_index_rate"
    ],
    default_output_mode="summary",
    default_include_passed=False,
    default_interrupt_enabled=True,
    default_interrupt_severity="CRITICAL"
)
```

A validation can appear in multiple portfolios.

---

# Calling Existing GF Validation Functions

Each validation should be executed by resolving the gf function at runtime:

```python
gf_function_name = validation_meta["gf_function_name"]
func = getattr(self.gf, gf_function_name)
```

Then call it using the selected runtime object:

```python
selected_runtime_context = self._resolve_runtime_context(
    validation_meta,
    context_bundle
)
```

Most current functions appear to accept:

```python
runtime_context=None,
params=None,
include_results=False,
include_pass=False
```

The engine should call validation functions like this when possible:

```python
raw_result = func(
    runtime_context=selected_runtime_context,
    params=params,
    include_results=include_results,
    include_pass=include_passed
)
```

Where:

```python
include_results = output_mode == "full"
include_pass = include_passed
```

Call rules:

* In `summary` mode, call each validation with `include_results=False`.
* In `full` mode, call each validation with `include_results=True`.
* If `include_passed=False`, call with `include_pass=False`.
* If `include_passed=True`, call with `include_pass=True`.

Support fallback call signatures because not all existing gf functions may accept all arguments:

1. Try keyword call:

```python
func(
    runtime_context=selected_runtime_context,
    params=params,
    include_results=include_results,
    include_pass=include_passed
)
```

2. If argument mismatch occurs, try:

```python
func(selected_runtime_context, params, include_results, include_passed)
```

3. If argument mismatch occurs, try:

```python
func(selected_runtime_context, params)
```

4. If argument mismatch occurs, try:

```python
func(selected_runtime_context)
```

5. If argument mismatch occurs, try:

```python
func()
```

6. If still failing, convert the exception into a standardized CRITICAL engine result.

Be careful not to hide business-logic `TypeError` too aggressively. If accurate signature inspection is not IronPython-safe, keep fallback simple and document the limitation.

---

# Validation Function Return Shapes

Current validation functions may return a JSON string because they often use:

```python
return gf.validation_main(
    operation="to_json",
    payload=payload
)
```

Therefore, the engine must support these return shapes:

```text
JSON string
dict
list of dict
dict containing "results"
None
```

Implement a robust parser/normalizer.

Rules:

1. If raw result is a string, try to parse it as JSON.
2. If parsed JSON is a dict with fields like `success`, `summary`, `results`, and `validation`, treat it as a validation payload.
3. If raw result is a dict with `summary` and optional `results`, treat it as a validation payload.
4. If raw result is a dict that looks like one result record, wrap it into a list.
5. If raw result is a list, treat it as result records.
6. If raw result is `None`, treat it as an empty result list with a zero summary.
7. If shape is unexpected, convert it into a standardized CRITICAL failure result.

---

# Preserve Per-Validation Summary

Existing validation functions may already return:

```python
{
    "validation": "...",
    "success": True,
    "summary": {
        "pass": 1,
        "fail": 0,
        "total": 1,
        "highest_severity": None,
        "by_severity": {}
    },
    "results": [...]
}
```

The engine must preserve this summary.

Algorithm:

1. Normalize raw output into this internal structure:

```python
{
    "validation_key": "...",
    "validation_name": "...",
    "validates": "...",
    "success": True,
    "summary": {...},
    "results": [...]
}
```

2. If raw payload contains `summary`, use it as the primary per-validation summary.
3. If no summary exists, calculate summary from result records.
4. If raw payload contains `success`, preserve it unless the summary clearly contradicts it.
5. If `results` are absent because `include_results=False`, still use returned `summary` to build the portfolio summary.

This is critical because summary mode may not return detailed results.

---

# Standard Result Contract

When detailed result records are present, normalize them toward this schema:

```python
{
    "status": "PASS" or "FAIL",
    "passed": True or False,
    "severity": "INFO" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "threshold": optional,
    "issue_code": optional,
    "issue": optional,
    "explanation": optional,
    "impact": optional,
    "action": optional,
    "context": {},
    "expected": optional,
    "actual": optional,
    "script_name_display": optional,
    "function_key": optional
}
```

Normalization rules:

* If `passed` is missing but `status == "PASS"`, set `passed=True`.
* If `passed` is missing but `status == "FAIL"`, set `passed=False`.
* If `status` is missing but `passed=True`, set `status="PASS"`.
* If `status` is missing but `passed=False`, set `status="FAIL"`.
* If `severity` is missing:

  * Use `"INFO"` for passed records.
  * Use the validation’s `default_severity` for failed records.
* If `context` is missing or `None`, set it to `{}`.
* Add metadata into `context` where useful:

  * `validation_key`
  * `validation_name`
  * `gf_function_name`

---

# Portfolio-Level Summary

The engine should build a portfolio summary from per-validation summaries.

Portfolio summary must include:

```python
{
    "total_validations": 0,
    "passed_validations": 0,
    "failed_validations": 0,
    "total_records_checked": 0,
    "total_passed_records": 0,
    "total_failed_records": 0,
    "highest_severity": None,
    "by_severity": {}
}
```

Use each validation’s summary:

```python
summary["pass"]
summary["fail"]
summary["total"]
summary["highest_severity"]
summary["by_severity"]
```

Do not require detailed results to calculate portfolio summary.

---

# Output Modes

Support exactly two output modes:

```text
summary
full
```

Default:

```text
summary
```

No compact mode is required.

---

## Summary Mode Output

Summary mode should not include detailed result records.

Output should include:

```python
{
    "portfolio_key": "...",
    "portfolio_name": "...",
    "success": True or False,
    "should_interrupt": True or False,
    "output_mode": "summary",
    "include_passed": False,
    "interrupt_enabled": True,
    "interrupt_severity": "CRITICAL",
    "portfolio_summary": {...},
    "validations": [
        {
            "validation_key": "...",
            "validation_name": "...",
            "validates": "...",
            "success": True or False,
            "summary": {...}
        }
    ]
}
```

No `results` field should appear in summary mode.

---

## Full Mode Output

Full mode should include detailed result records when available.

Output should include everything in summary mode plus:

```python
"results": [...]
```

for each validation.

Rules:

* If `include_passed=False`, include only failed records in `results`.
* If `include_passed=True`, include both pass and fail records in `results`.
* If a validation function does not return results even in full mode, keep `results` as an empty list and preserve summary.

---

# Return and Print Control

Support:

```python
return_results=True
print_results=False
```

Rules:

* If `return_results=True`, return the final payload dict.
* If `print_results=True`, print the final payload as JSON.
* If both are true, print and return.
* If both are false, run silently unless interruption is raised.

Use JSON-safe printing:

```python
def _print_json(self, payload):
    import json
    try:
        print(json.dumps(payload, indent=2, sort_keys=True))
    except Exception:
        print(json.dumps(payload))
```

---

# Interruption Control

Only severity-threshold interruption is required.

Do not implement `any_fail`.

Support:

```python
interrupt_enabled=True
interrupt_severity="CRITICAL"
raise_on_interrupt=True
```

Severity order:

```python
["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
```

Rules:

* `should_interrupt=True` only if:

  * `interrupt_enabled=True`
  * the portfolio summary highest severity is equal to or above `interrupt_severity`
* If detailed results are available, the engine may also check detailed failed records.
* If `interrupt_enabled=False`, `should_interrupt=False`.
* If `interrupt_severity="CRITICAL"`, only CRITICAL failures interrupt.
* If `interrupt_severity="HIGH"`, HIGH and CRITICAL failures interrupt.
* If `interrupt_severity="MEDIUM"`, MEDIUM, HIGH, and CRITICAL failures interrupt.

Important sequencing:

1. Run all validations in the selected portfolio.
2. Build context bundle from explicit inputs.
3. Resolve selected runtime context per validation.
4. Call each `gf` validation function.
5. Parse and normalize each validation output.
6. Preserve or build each validation summary.
7. Build portfolio summary.
8. Determine `should_interrupt`.
9. Build final payload.
10. Print payload if `print_results=True`.
11. Raise interruption only after payload is built and printed.
12. Return payload only if `return_results=True` and no exception prevents normal return.

Host-facing message:

```python
def _build_host_message(self, portfolio_summary):
    failed = portfolio_summary.get("total_failed_records", 0)
    return "{} validation errors raised, test failed, download log to view detail".format(failed)
```

Suggested raised exception message:

```text
2 validation errors raised, test failed, download log to view detail
```

---

# Existing Per-Validation Host Error Behavior

Some existing validation functions may currently call host error logic internally, for example:

```python
gf.validation_main(
    operation="emit_host_error",
    result=result,
    host_target=host_target,
    host_raise_method="raise_error",
    attribute_name="FirstPayDate",
)
```

The preferred architecture is:

* Individual validation functions return results.
* `ValidationEngine` controls portfolio-level interruption.

Do not break existing ASAP2 behavior.

If practical, pass a parameter through `params` to suppress per-validation host error emission when called from `ValidationEngine`.

Suggested default params may include:

```python
params = {
    "emit_host_error": False,
    "suppress_host_error": True
}
```

But do not force this if existing functions do not support it.

Document the limitation if some existing validation functions still emit host errors internally.

---

# Missing GF Function Handling

If a registered `gf_function_name` does not exist on `self.gf`, do not crash directly.

Return a standardized CRITICAL validation output:

```python
{
    "validation_key": "...",
    "validation_name": "...",
    "validates": "...",
    "success": False,
    "summary": {
        "pass": 0,
        "fail": 1,
        "total": 1,
        "highest_severity": "CRITICAL",
        "by_severity": {
            "CRITICAL": 1
        }
    },
    "results": [
        {
            "status": "FAIL",
            "passed": False,
            "severity": "CRITICAL",
            "issue_code": "VALIDATION_GF_FUNCTION_NOT_FOUND",
            "issue": "Validation global function was not found.",
            "explanation": "The ValidationEngine could not find the expected function on gf.",
            "impact": "This validation could not be executed.",
            "action": "Check the gf function name registered inside ValidationEngine.",
            "context": {
                "validation_key": "...",
                "validation_name": "...",
                "gf_function_name": "..."
            },
            "expected": "gf contains the registered validation function.",
            "actual": "Function not found on gf."
        }
    ]
}
```

---

# Missing Runtime Context Handling

If a validation has:

```python
runtime_context_required=True
```

and the required object is missing from the context bundle, return a standardized CRITICAL validation output:

```python
{
    "validation_key": "...",
    "validation_name": "...",
    "validates": "...",
    "success": False,
    "summary": {
        "pass": 0,
        "fail": 1,
        "total": 1,
        "highest_severity": "CRITICAL",
        "by_severity": {
            "CRITICAL": 1
        }
    },
    "results": [
        {
            "status": "FAIL",
            "passed": False,
            "severity": "CRITICAL",
            "issue_code": "VALIDATION_RUNTIME_CONTEXT_MISSING",
            "issue": "Required runtime context object is missing.",
            "explanation": "The ValidationEngine could not resolve the runtime object required by this validation.",
            "impact": "This validation could not be executed.",
            "action": "Pass the required object into run_portfolio, such as assets=assets, bonds=bonds, or deal=deal.",
            "context": {
                "validation_key": "...",
                "validation_name": "...",
                "gf_function_name": "...",
                "runtime_context_key": "bonds"
            },
            "expected": "Required runtime context object is available.",
            "actual": "Runtime context object is missing."
        }
    ]
}
```

---

# Runtime Error Handling

If a `gf` validation function raises an exception, convert it into a standardized CRITICAL validation output:

```python
{
    "validation_key": "...",
    "validation_name": "...",
    "validates": "...",
    "success": False,
    "summary": {
        "pass": 0,
        "fail": 1,
        "total": 1,
        "highest_severity": "CRITICAL",
        "by_severity": {
            "CRITICAL": 1
        }
    },
    "results": [
        {
            "status": "FAIL",
            "passed": False,
            "severity": "CRITICAL",
            "issue_code": "VALIDATION_FUNCTION_RUNTIME_ERROR",
            "issue": "Validation function failed during execution.",
            "explanation": "The ValidationEngine could not complete this validation function.",
            "impact": "This validation result may be incomplete.",
            "action": "Review the global function name, function signature, runtime context routing, and validation logic.",
            "context": {
                "validation_key": "...",
                "validation_name": "...",
                "gf_function_name": "...",
                "runtime_context_key": "...",
                "error_type": "...",
                "error_message": "..."
            },
            "expected": "Validation function executes successfully.",
            "actual": "Validation function raised an exception."
        }
    ]
}
```

---

# Required Internal Helper Methods

Implement internal helper methods similar to:

```python
def _register_default_validations(self):
    pass

def _register_default_portfolios(self):
    pass

def _add_validation(self, key, name, validates, gf_function_name,
                    category=None,
                    asset_class=None,
                    default_severity="HIGH",
                    enabled=True,
                    default_params=None,
                    description=None,
                    metadata=None,
                    runtime_context_key=None,
                    runtime_context_required=False,
                    allow_global_context_fallback=True):
    pass

def _add_portfolio(self, portfolio_key, name, validation_keys,
                   description=None,
                   default_output_mode="summary",
                   default_include_passed=False,
                   default_interrupt_enabled=True,
                   default_interrupt_severity="CRITICAL"):
    pass

def _build_context_bundle(self, runtime_context=None,
                          assets=None, bonds=None, deal=None,
                          fees=None, accounts=None,
                          period=None, payment_date=None,
                          distribution_date=None, model=None):
    pass

def _resolve_runtime_context(self, validation_meta, context_bundle):
    pass

def _run_validation(self, validation_key, context_bundle,
                    output_mode="summary", include_passed=False):
    pass

def _call_gf_validation(self, validation_meta, selected_runtime_context,
                        output_mode="summary", include_passed=False):
    pass

def _parse_raw_validation_output(self, raw_result, validation_meta):
    pass

def _normalize_validation_output(self, parsed_payload, validation_meta):
    pass

def _normalize_result_record(self, record, validation_meta):
    pass

def _summarize_results(self, results):
    pass

def _summarize_portfolio(self, validation_outputs):
    pass

def _determine_should_interrupt(self, portfolio_summary, validation_outputs,
                                interrupt_enabled, interrupt_severity):
    pass

def _build_output_payload(self, portfolio_key, portfolio_meta,
                          validation_outputs, portfolio_summary,
                          output_mode, include_passed,
                          interrupt_enabled, interrupt_severity,
                          should_interrupt):
    pass

def _make_missing_gf_function_output(self, validation_meta):
    pass

def _make_missing_runtime_context_output(self, validation_meta):
    pass

def _make_runtime_error_output(self, validation_meta, error):
    pass

def _make_unexpected_result_shape_output(self, validation_meta, raw_result):
    pass

def _build_host_message(self, portfolio_summary):
    pass

def _print_json(self, payload):
    pass
```

---

# Email Placeholder

Do not implement real email functionality now.

Add only:

```python
def send_email_notification(self, payload, email_options=None):
    """
    Placeholder for future email integration.
    Do not hard-code credentials.
    Do not add dependencies.
    """
    return None
```

Email should not affect validation execution.

---

# ASAP2 / IronPython Compatibility

This may run inside ASAP2 / IronPython.

Follow these constraints:

* Avoid third-party packages.
* Avoid dataclasses.
* Avoid pydantic.
* Avoid async code.
* Avoid f-strings if IronPython 2.7 compatibility is required.
* Use `.format()` string formatting.
* Use plain dict/list/string/bool/int structures.
* Use standard library `json`.
* Keep exception handling simple.
* Avoid advanced introspection.
* Do not rely on external file imports unless needed.
* Keep the class file self-contained if possible.

---

# Acceptance Criteria

The implementation is complete only if:

1. A class named `ValidationEngine` is created.
2. The class accepts `gf` in `__init__`.
3. The caller does not manually register validations.
4. The caller does not manually create portfolios.
5. The engine internally manages `self.validations`.
6. The engine internally manages `self.portfolios`.
7. Each validation stores `gf_function_name` as a string.
8. Each validation may define `runtime_context_key`.
9. The engine resolves `gf` functions using `getattr(self.gf, gf_function_name)`.
10. The engine supports explicit runtime inputs such as `assets=assets`, `bonds=bonds`, and `deal=deal`.
11. The engine builds a context bundle from explicit inputs.
12. Explicit inputs override same-named values in `runtime_context`.
13. The engine passes the selected object, not the whole context dict, to validations with `runtime_context_key="assets"`, `"bonds"`, or `"deal"`.
14. The engine can pass the entire context bundle when `runtime_context_key="context"`.
15. The engine can run selected portfolios by `portfolio_key`.
16. Required portfolios include:

    * `rmbs_setup`
    * `rmbs_pmt`
    * `cmbs_setup`
    * `cmbs_pmt`
    * `abs_setup`
    * `abs_pmt`
17. The engine supports validation functions returning JSON strings.
18. The engine supports validation functions returning dictionaries.
19. The engine supports validation functions returning dictionaries with `summary` and optional `results`.
20. The engine preserves per-validation summaries when returned.
21. The engine can build portfolio summary from per-validation summaries without requiring detailed records.
22. Output mode supports `summary` and `full`.
23. Default output mode is `summary`.
24. Summary mode does not show detailed result records.
25. Full mode shows detailed result records when available.
26. Passed detailed records are hidden by default.
27. Passed detailed records can be included with `include_passed=True`.
28. Return and print behavior are controlled separately.
29. Missing `gf` function becomes a standardized CRITICAL validation output.
30. Missing required runtime context becomes a standardized CRITICAL validation output.
31. Runtime error inside a `gf` validation function becomes a standardized CRITICAL validation output.
32. Interruption is based only on severity threshold.
33. No `any_fail` mode is required.
34. Final payload is built before interruption is raised.
35. If `print_results=True`, the payload is printed before interruption is raised.
36. Email functionality is only a placeholder.
37. Code remains simple and ASAP2-compatible.

---

# Example Final ASAP2 Usage

Setup portfolio:

```python
engine = ValidationEngine(gf)

engine.run_portfolio(
    portfolio_key="rmbs_setup",
    assets=assets,
    bonds=bonds,
    deal=deal,
    output_mode="summary",
    include_passed=False,
    return_results=False,
    print_results=True,
    interrupt_enabled=True,
    interrupt_severity="CRITICAL",
    raise_on_interrupt=True
)
```

Payment portfolio:

```python
engine = ValidationEngine(gf)

payload = engine.run_portfolio(
    portfolio_key="rmbs_pmt",
    bonds=bonds,
    deal=deal,
    period=period,
    payment_date=payment_date,
    output_mode="full",
    include_passed=False,
    return_results=True,
    print_results=False,
    interrupt_enabled=True,
    interrupt_severity="HIGH",
    raise_on_interrupt=False
)
```

---

# Final Response Required After Implementation

After implementation, report:

1. File created or modified.
2. Final public API of `ValidationEngine`.
3. Internal validation registry structure.
4. Internal portfolio registry structure.
5. How explicit inputs such as `assets=assets`, `bonds=bonds`, and `deal=deal` are handled.
6. How `runtime_context_key` routes each validation to the correct runtime object.
7. How JSON-string validation outputs are parsed.
8. How per-validation summaries are preserved.
9. How portfolio summaries are built.
10. Example ASAP2 setup portfolio usage.
11. Example ASAP2 payment portfolio usage.
12. Example summary output.
13. Example full output.
14. How `getattr(self.gf, gf_function_name)` is used.
15. How interruption threshold is controlled.
16. How output is preserved before interruption.
17. Any ASAP2 / IronPython compatibility notes.

Do not only plan. Implement `ValidationEngine` directly.

```

这个版本已经把你现在的真实架构固定下来了：**外部显式传 `assets/bonds/deal`，engine 内部按 `runtime_context_key` 分配给不同 validation function。**
```
