# Agent Prompt: Generate Print-Friendly Card-Style ASAP2 Validation Function Inventory

You are working with an attached file or files that contain many already-written ASAP2 / Asset Securitization Analysis Pro validation functions.

These validation functions are intended to be registered later inside a `ValidationEngine` class and called through the ASAP2 `gf` global function namespace.

Your task is NOT to refactor code.

Your task is to inspect the attached validation functions and generate a readable Markdown inventory for further analysis, portfolio grouping, and future `ValidationEngine` registry design.

---

# Primary Goal

Read all validation functions in the attached file(s), then create a Markdown inventory that classifies each validation function by:

1. Validation focus:
   - setup
   - periodic
   - payment
   - deal-level
   - asset-level
   - bond-level
   - fee-level
   - account-level
   - unclear

2. Product scope:
   - general / all asset classes
   - RMBS
   - CMBS
   - ABS
   - CLO
   - NPL
   - unclear

3. Runtime context requirement:
   - assets
   - bonds
   - deal
   - fees
   - accounts
   - full context bundle
   - none / global fallback
   - unclear

4. What the function validates.

5. Whether the function appears ready to be added to `ValidationEngine`.

6. Any bugs, ambiguity, naming issues, duplicate keys, runtime-context concerns, or cleanup recommendations.

---

# Very Important Output Requirement

Do NOT generate a wide Markdown table as the main inventory.

The previous wide table format is not acceptable because it is too hard to read, too hard to print, and too wide for VS Code / GitHub Markdown / ChatGPT preview.

Avoid this style:

```markdown
| # | Function Name | Display Name | Function Key | Issue Code | Focus | Product Scope | Runtime Context Key | Suggested Portfolio | Default Severity | What It Validates | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
````

Instead, generate a **card-style Markdown document**.

Each function should get its own section with short fields arranged vertically.

The output should be readable in:

* VS Code Markdown preview
* GitHub Markdown
* ChatGPT
* printed PDF
* plain text review

---

# Output File

Create:

```text
validation_function_inventory.md
```

---

# Required Markdown Structure

Use this structure exactly.

````markdown
# ASAP2 Validation Function Inventory

## 1. Executive Summary

- Total validation functions reviewed:
- Setup-focused functions:
- Periodic-focused functions:
- Payment-focused functions:
- General / all-asset functions:
- RMBS-specific functions:
- CMBS-specific functions:
- ABS-specific functions:
- Functions ready for `ValidationEngine` registry:
- Functions needing manual review:
- Functions with likely bugs:
- Functions with duplicate or conflicting metadata:

---

## 2. Compact Matrix

This section should be a short, narrow table only for quick scanning.

Do not put long explanations in this table.

| # | Function | Focus | Scope | Context | Severity | Review Needed |
|---|---|---|---|---|---|---|
| 1 | `function_name` | setup | general | bonds | CRITICAL | No |
| 2 | `function_name` | periodic | general | bonds | ERROR | Yes |

Rules for this table:

- Keep it narrow.
- Keep each cell short.
- Do not include long `What It Validates` text.
- Do not include long notes.
- Detailed explanation must appear later in Function Inventory Cards.

---

## 3. Grouped Index

### 3.1 Setup Validations

#### General / All Asset Classes

- `function_name` — short purpose
- `function_name` — short purpose

#### RMBS

- `function_name` — short purpose

#### CMBS

- `function_name` — short purpose

#### ABS

- `function_name` — short purpose

---

### 3.2 Periodic / Payment Validations

#### General / All Asset Classes

- `function_name` — short purpose
- `function_name` — short purpose

#### RMBS

- `function_name` — short purpose

#### CMBS

- `function_name` — short purpose

#### ABS

- `function_name` — short purpose

---

### 3.3 Deal-Level Validations

- `function_name` — short purpose

### 3.4 Asset-Level Validations

- `function_name` — short purpose

### 3.5 Bond-Level Validations

- `function_name` — short purpose

### 3.6 Fee-Level Validations

- `function_name` — short purpose

### 3.7 Account-Level Validations

- `function_name` — short purpose

---

## 4. Function Inventory Cards

### 4.1 `function_name`

**Display Name:**  
Display name here.

**Function Key:**  
`FUNCTION_KEY`

**Issue Code:**  
`ISSUE_CODE`

**Focus:**  
setup / periodic / payment / deal-level / asset-level / bond-level / fee-level / account-level / unclear

**Product Scope:**  
general / RMBS / CMBS / ABS / CLO / NPL / unclear

**Runtime Context Key:**  
assets / bonds / deal / fees / accounts / context / none / unclear

**Suggested Portfolio:**  
setup / payment-periodic / both / unclear

**Default Severity:**  
INFO / LOW / WARNING / MEDIUM / HIGH / ERROR / CRITICAL / unclear

**What It Validates:**  
Write one concise paragraph explaining the business rule.

**Validation Logic Summary:**  

- Runtime object used:
- Loop target:
- Key fields checked:
- PASS condition:
- FAIL condition:
- Output shape:
- Host error behavior:

**ValidationEngine Draft Registry Entry:**

```python
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

**Notes / Concerns:**

* If clean, write: `Clean and consistent.`
* If there are concerns, list them as bullets.

---

## 5. Suggested ValidationEngine Registry Draft

Group the draft registry entries by category.

### 5.1 Setup Validations

```python
# setup validations

self._add_validation(
    key="...",
    name="...",
    validates="...",
    gf_function_name="...",
    category="setup",
    asset_class="general",
    default_severity="...",
    runtime_context_key="..."
)
```

### 5.2 Periodic / Payment Validations

```python
# periodic / payment validations

self._add_validation(
    key="...",
    name="...",
    validates="...",
    gf_function_name="...",
    category="periodic",
    asset_class="general",
    default_severity="...",
    runtime_context_key="..."
)
```

### 5.3 Deal-Level Validations

```python
# deal-level validations
```

### 5.4 Asset-Level Validations

```python
# asset-level validations
```

### 5.5 Bond-Level Validations

```python
# bond-level validations
```

### 5.6 Fee-Level Validations

```python
# fee-level validations
```

### 5.7 Account-Level Validations

```python
# account-level validations
```

---

## 6. Suggested Portfolio Grouping

### 6.1 General Setup Portfolio

* `function_name`
* `function_name`

### 6.2 General Payment / Periodic Portfolio

* `function_name`
* `function_name`

### 6.3 RMBS Setup Portfolio

* `function_name`

### 6.4 RMBS Payment / Periodic Portfolio

* `function_name`

### 6.5 CMBS Setup Portfolio

* `function_name`

### 6.6 CMBS Payment / Periodic Portfolio

* `function_name`

### 6.7 ABS Setup Portfolio

* `function_name`

### 6.8 ABS Payment / Periodic Portfolio

* `function_name`

---

## 7. Manual Review Required

For each function needing review, use this format.

### `function_name`

**Reason for Review:**
Explain the issue.

**Potential Impact:**
Explain why it matters.

**Suggested Fix or Decision Needed:**
Explain what should be checked, fixed, renamed, or decided.

---

## 8. Cleanup Recommendations

### 8.1 Naming Issues

* ...

### 8.2 Duplicate Function Keys

* ...

### 8.3 Duplicate Issue Codes

* ...

### 8.4 Runtime Context Issues

* ...

### 8.5 Output Shape Issues

* ...

### 8.6 Severity / Issue Code Issues

* ...

### 8.7 Possible Logic Bugs

* ...

### 8.8 Host Error / Interruption Concerns

* ...

### 8.9 ValidationEngine Registry Readiness

* ...

````

---

# What to Extract from Each Function

For each validation function, inspect:

1. Function name.
2. Constants above or near the function:
   - `SCRIPT_NAME_DISPLAY`
   - `FUNCTION_KEY`
   - `ISSUE_CODE`
3. Function signature:
   - `runtime_context`
   - `params`
   - `include_results`
   - `include_pass`
4. Runtime object used:
   - `assets`
   - `bonds`
   - `deal`
   - `fees`
   - `accounts`
   - full context bundle
5. Whether it loops over:
   - assets
   - bonds
   - fees
   - accounts
   - one deal object
6. Fields being checked.
7. PASS condition.
8. FAIL condition.
9. Severity used in fail results.
10. Output shape:
    - JSON string
    - dict
    - list
    - dict with `summary`
    - dict with `results`
11. Whether it calls:
    - `gf.validation_main(operation="pass_result")`
    - `gf.validation_main(operation="fail_result")`
    - `gf.validation_main(operation="summarize_results")`
    - `gf.validation_main(operation="to_json")`
    - `gf.validation_main(operation="emit_host_error")`
12. Whether results are appended correctly.
13. Whether `include_results` and `include_pass` are implemented correctly.
14. Whether function naming and `FUNCTION_KEY` are consistent.
15. Whether multiple functions have duplicated `FUNCTION_KEY` or `ISSUE_CODE`.

---

# Classification Rules

## Focus

Classify each function into one main focus:

```text
setup
periodic
payment
deal-level
asset-level
bond-level
fee-level
account-level
unclear
````

Use `setup` when the function checks static configuration, setup fields, or deal/bond/asset metadata.

Examples:

* deal name
* primary analyst
* state code
* first pay date
* accrual end date type
* bond type
* denomination
* setup parameters
* record date type

Use `periodic` when the function checks current period data, roll-forward data, ending balances, current period percentages, current fields, or period-level parameters.

Use `payment` when the function checks payment waterfall results, paid amounts, principal paid, interest paid, actual fees, expected fees, distribution logic, or payment allocations.

If a function is both periodic and payment-related, classify as:

```text
periodic/payment
```

or choose the stronger category and note the overlap.

---

## Product Scope

Classify each function as:

```text
general
RMBS
CMBS
ABS
CLO
NPL
unclear
```

Use `general` when the function appears reusable across asset classes.

Use specific product scope only if there is clear product-specific evidence.

Examples:

* Generic bond field check -> `general`
* Mortgage collateral rule -> `RMBS`
* Commercial mortgage / property-level rule -> `CMBS`
* Consumer/auto/student/credit-card receivable rule -> `ABS`
* CLO collateral or tranche-specific rule -> `CLO`
* NPL-specific bond or loss logic -> `NPL`

Do not over-classify.

If evidence is weak, use `general` or `unclear`, and explain.

---

## Runtime Context Key

Infer the correct `ValidationEngine.runtime_context_key`.

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

Examples:

```python
bds = bonds if runtime_context is None else runtime_context
for bd in bds:
    ...
```

means:

```text
runtime_context_key = bonds
```

```python
assets_obj = assets if runtime_context is None else runtime_context
for asset in assets_obj:
    ...
```

means:

```text
runtime_context_key = assets
```

If the function needs both `deal` and `bonds`, suggest:

```text
runtime_context_key = context
```

and explain that this function may need to be updated to read from a context bundle.

If the function uses global objects directly despite accepting `runtime_context`, flag it.

---

# Default Severity Inference

If severity is explicitly used in the function, use it.

If severity is not explicit, infer conservatively:

* Missing required setup field: `CRITICAL`
* Invalid setup field: `CRITICAL`
* Payment calculation error: `ERROR`
* Balance mismatch: `ERROR`
* Warning-level threshold breach: `WARNING`
* Informational check: `INFO`
* Unclear: `ERROR` and mark as manual review

Support these severity labels:

```text
INFO
LOW
WARNING
MEDIUM
HIGH
ERROR
CRITICAL
```

---

# ValidationEngine Draft Registry Rules

For each function, draft a registry entry.

Use this format:

```python
self._add_validation(
    key="function_or_function_key",
    name="Display Name",
    validates="Concise business rule.",
    gf_function_name="actual_function_name",
    category="setup_or_periodic_or_payment",
    asset_class="general_or_RMBS_or_CMBS_or_ABS_or_CLO_or_NPL_or_unclear",
    default_severity="ERROR",
    runtime_context_key="bonds"
)
```

Rules:

1. `key` should preferably be stable and unique.
2. `gf_function_name` must be the actual callable function name.
3. If `FUNCTION_KEY` is duplicated, do not reuse it blindly as `key`.
4. If function name and `FUNCTION_KEY` conflict, flag it.
5. If the best registry key is unclear, propose one and mark manual review.
6. `validates` should be short and precise.
7. Do not invent product scope if evidence is weak.
8. Do not invent runtime context if unclear; mark `unclear`.

---

# Important Issues to Flag

When you find a possible problem, document it clearly under the function card and under Cleanup Recommendations.

Examples of issues to flag:

* `results.append(result)` appears inside an `if host_target is not None` block, causing results to be silently dropped.
* Function accepts `runtime_context` but still reads module-level global `assets`, `bonds`, or `deal`.
* Function needs both `bonds` and `deal`, but `runtime_context_key` is only `bonds`.
* Function has duplicate `FUNCTION_KEY` with another validation.
* Function has duplicate `ISSUE_CODE` where uniqueness is expected.
* Function name and `FUNCTION_KEY` do not match.
* Function returns JSON string but does not include `summary`.
* Function supports `include_results` but not `include_pass`.
* Function emits host errors internally, which may conflict with `ValidationEngine` portfolio-level interruption.
* Function has inconsistent severity naming such as `ERROR` vs `CRITICAL`.
* Usage example calls the function with incorrect syntax.
* Function result says pass but issue code sounds like failure.
* Function has wrong `actual` field.
* Function has typo in function name, such as `valiate` instead of `validate`.
* Function appears to use a wrong object index, such as enumerating `assets_obj` but accessing global `assets[i]`.

Do not silently fix these issues. Document them.

---

# Do Not Modify Code

For this task:

* Do not refactor validation functions.
* Do not rewrite validation logic.
* Do not change function signatures.
* Do not create or modify `ValidationEngine`.
* Only create the Markdown inventory file.
* Do not invent missing business rules.
* If classification is uncertain, mark it as uncertain and explain why.

---

# Final Response Required

After generating `validation_function_inventory.md`, report:

1. File created.
2. Total number of functions reviewed.
3. Count by focus.
4. Count by product scope.
5. Count by runtime context key.
6. Functions ready for `ValidationEngine`.
7. Functions needing manual review.
8. Top cleanup recommendations.
9. Duplicate `FUNCTION_KEY` findings, if any.
10. Duplicate `ISSUE_CODE` findings, if any.
11. Any likely bugs found.

Do not stop after planning. Inspect the attached validation function file(s) and generate the readable card-style Markdown inventory.

```
```
