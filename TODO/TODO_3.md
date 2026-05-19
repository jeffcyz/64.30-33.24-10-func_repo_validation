下面是一份可以直接给 Codex 的 **English prompt**。目标是：让 Codex 读取你 attachment 里已经写好的 validation functions，先不改代码，只做 **inventory / classification / documentation**，生成一份 Markdown list，供后续决定如何放进 `ValidationEngine` 的 registry 和 portfolio。

````markdown
# Agent Prompt: Build Validation Function Inventory from Attached ASAP2 Validation Functions

You are working with an attached file or files that contain many already-written ASAP2 / Asset Securitization Analysis Pro validation functions.

These validation functions are intended to be called later by a `ValidationEngine` class through the ASAP2 `gf` global function namespace.

Your task in this step is NOT to refactor the functions and NOT to modify the validation logic.

Your task is to inspect the attached validation functions and create an initial Markdown inventory that classifies each function for future portfolio design.

---

# Primary Goal

Read all validation functions in the attached file(s), then generate a Markdown inventory list that identifies:

1. The function name.
2. The display name, if available.
3. The `FUNCTION_KEY`, if available.
4. The `ISSUE_CODE`, if available.
5. The validation focus:
   - setup
   - periodic
   - payment
   - deal-level
   - asset-level
   - bond-level
   - fee-level
   - account-level
   - other / unclear
6. The applicable product scope:
   - general / all asset classes
   - RMBS
   - CMBS
   - ABS
   - CLO
   - NPL
   - other / unclear
7. The primary runtime object required:
   - assets
   - bonds
   - deal
   - fees
   - accounts
   - context bundle
   - none / global fallback
   - unclear
8. What the function validates, summarized in plain English.
9. Whether it appears suitable for:
   - setup portfolio
   - payment / periodic portfolio
   - both
   - not sure
10. Suggested `ValidationEngine` registry entry fields:
    - `key`
    - `name`
    - `validates`
    - `gf_function_name`
    - `category`
    - `asset_class`
    - `default_severity`
    - `runtime_context_key`
11. Any concerns, ambiguities, or cleanup recommendations.

---

# Important Context

The future `ValidationEngine` will call validation functions through `gf` using function names.

Example future registry entry:

```python
self._add_validation(
    key="validate_setup_bond_first_pay_date",
    name="Bond Setup First Pay Date Validation",
    validates="Bond setup FirstPayDate must be populated.",
    gf_function_name="validate_setup_bond_first_pay_date",
    category="setup",
    asset_class="general",
    default_severity="CRITICAL",
    runtime_context_key="bonds"
)
````

The current step should help create these registry entries later.

---

# Existing Validation Function Pattern

Many functions may look like this:

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
    ...
```

Some functions may return JSON strings by calling:

```python
return gf.validation_main(
    operation="to_json",
    payload=payload,
)
```

Some functions may use:

```python
gf.validation_main(operation="pass_result", ...)
gf.validation_main(operation="fail_result", ...)
gf.validation_main(operation="summarize_results", ...)
```

Use these clues to infer what each function validates.

---

# Classification Rules

## Focus Category

Classify each function into one main focus:

### `setup`

Use this if the function checks static setup fields such as:

* asset setup fields
* bond setup fields
* deal setup fields
* state code
* first pay date
* accrual type
* primary analyst
* deal name
* issue date
* maturity date
* setup parameters

### `periodic`

Use this if the function checks recurring period-level data, such as:

* current period fields
* ending balance fields
* rollover fields
* scheduled balance
* current credit support percent
* payment period values
* periodic parameters

### `payment`

Use this if the function checks payment waterfall, payment allocation, paid amounts, fee actuals, interest/principal paid, or distribution results.

### `deal-level`

Use this if it validates deal-level metadata or deal-wide parameters.

### `asset-level`

Use this if it validates asset-level fields or iterates over assets.

### `bond-level`

Use this if it validates bond/class/note-level fields or iterates over bonds.

### `fee-level`

Use this if it validates fees, expenses, servicing fees, trustee fees, or fee actual vs expected.

### `account-level`

Use this if it validates reserve accounts, collection accounts, payment accounts, or account balances.

If unclear, mark as:

```text
unclear
```

and explain why.

---

## Product Scope

Classify product scope as:

```text
general
RMBS
CMBS
ABS
CLO
NPL
other
unclear
```

Use `general` when the function appears reusable across all asset classes.

Use specific product types only when the function clearly references product-specific logic, naming, fields, or business rules.

Examples:

* If it checks a generic bond field like `FirstPayDate`, likely `general`.
* If it checks mortgage collateral fields, likely `RMBS`.
* If it checks commercial mortgage fields, likely `CMBS`.
* If it checks auto/student/consumer receivable fields, likely `ABS`.
* If it checks collateralized loan obligation concepts, likely `CLO`.

If there is not enough evidence, mark as `general` or `unclear`, and explain.

---

## Runtime Context Key

Infer the likely `runtime_context_key` for each function.

Use:

```text
assets
bonds
deal
fees
accounts
context
none
unclear
```

Rules:

* If the function iterates over `assets` or asset-like objects, use `assets`.
* If the function iterates over `bonds`, `classes`, `notes`, or bond-like objects, use `bonds`.
* If the function validates one deal object, use `deal`.
* If it needs multiple objects, use `context`.
* If it uses ASAP2 global variables and does not clearly accept a runtime object, use `none` or `unclear`.

For example:

```python
bds = bonds if runtime_context is None else runtime_context
for bd in bds:
    ...
```

means:

```text
runtime_context_key = bonds
```

---

# Output Format

Create a Markdown file named:

```text
validation_function_inventory.md
```

Use this structure:

````markdown
# ASAP2 Validation Function Inventory

## Summary

- Total functions reviewed:
- Setup-focused:
- Periodic-focused:
- Payment-focused:
- General / all asset classes:
- RMBS-specific:
- CMBS-specific:
- ABS-specific:
- Functions with unclear classification:
- Functions with missing metadata:
- Functions with potential cleanup needs:

## Inventory Table

| # | Function Name | Display Name | Function Key | Issue Code | Focus | Product Scope | Runtime Context Key | Suggested Portfolio | Default Severity | What It Validates | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | setup | general | bonds | setup | CRITICAL | ... | ... |

## Suggested ValidationEngine Registry Draft

```python
# Draft only. Review before using in production.

self._add_validation(
    key="...",
    name="...",
    validates="...",
    gf_function_name="...",
    category="...",
    asset_class="...",
    default_severity="...",
    runtime_context_key="..."
)
````

## Suggested Portfolio Grouping

### General Setup Portfolio

* ...

### General Payment / Periodic Portfolio

* ...

### RMBS Setup Portfolio

* ...

### RMBS Payment / Periodic Portfolio

* ...

### CMBS Setup Portfolio

* ...

### CMBS Payment / Periodic Portfolio

* ...

### ABS Setup Portfolio

* ...

### ABS Payment / Periodic Portfolio

* ...

## Ambiguous or Needs Review

List functions where classification is uncertain.

For each one, explain:

* why it is ambiguous
* what information is missing
* what should be reviewed manually

## Cleanup Recommendations

List any recommendations such as:

* inconsistent function naming
* missing `SCRIPT_NAME_DISPLAY`
* missing `FUNCTION_KEY`
* missing `ISSUE_CODE`
* unclear severity
* unclear runtime context
* functions that emit host errors internally
* functions that may need `params={"suppress_host_error": True}` support
* functions that return non-standard payload shapes

````

---

# Required Analysis Details

For each function, inspect:

1. Function name.
2. Constants above the function:
   - `SCRIPT_NAME_DISPLAY`
   - `FUNCTION_KEY`
   - `ISSUE_CODE`
3. Parameters:
   - `runtime_context`
   - `params`
   - `include_results`
   - `include_pass`
4. What global object it appears to use:
   - `assets`
   - `bonds`
   - `deal`
   - `fees`
   - `accounts`
5. Loop target:
   - `for asset in assets`
   - `for bd in bonds`
   - `for fee in fees`
6. Field names being checked.
7. Issue text, explanation, impact, and action.
8. Severity used in fail results.
9. Whether pass/fail records follow the standard validation result contract.
10. Whether the function returns JSON through `gf.validation_main(operation="to_json")`.

---

# Default Severity Inference

If severity is explicit in the function, use that severity.

If severity is not explicit, infer conservatively:

- Missing required setup field -> `CRITICAL`
- Invalid setup field -> `CRITICAL`
- Payment calculation mismatch -> `ERROR` or `CRITICAL`, depending on impact
- Balance mismatch -> `ERROR`
- Tolerance breach -> `WARNING` or `ERROR`
- Informational check -> `INFO`
- Unclear -> `ERROR` and mark as review needed

Support both normalized and legacy severities:

```python
INFO
LOW
WARNING
MEDIUM
HIGH
ERROR
CRITICAL
````

---

# Do Not Modify Code

For this task:

* Do not refactor validation functions.
* Do not rewrite validation logic.
* Do not change function signatures.
* Do not create `ValidationEngine` code.
* Do not change any existing files except creating the Markdown inventory file.
* Do not assume product scope if evidence is weak.
* Do not invent missing business meaning.

This is an inventory and classification task only.

---

# Final Response Required

After completing the inventory, report:

1. The Markdown file created.
2. Total number of validation functions reviewed.
3. Number of functions by focus:

   * setup
   * periodic
   * payment
   * other / unclear
4. Number of functions by product scope:

   * general
   * RMBS
   * CMBS
   * ABS
   * unclear
5. Functions that need manual review.
6. Functions that appear ready to be added to `ValidationEngine`.
7. Any naming or metadata cleanup recommendations.

Do not stop after planning. Inspect the attached validation function file(s) and generate `validation_function_inventory.md`.

```
```
