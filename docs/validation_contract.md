# Validation Contract (migration stage)

There are **two separate existing interfaces**:

- The standalone `ValidationHelperApi(operation, ...)` helper and host-compatible sample functions yield a result dictionary with keys such as `script_name_display`, `function_key`, `passed`, `status`, `severity`, `threshold`, `issue_code`, `context`, `expected` and `actual`.
- Some older host functions return a boolean or list and expose `return_results` and `interrupt_after_scan` instead. Existing instances such as `SetUpValidationStateCode` remain untouched.

The *new development orchestration* uses `ValidationEngine(gf, validations, portfolios)`, with explicit `gf_function_name`, `runtime_context_key`, `call_style`, and optionally `default_params`. It supports two-layer flags:

- `function_include_results`, `function_include_passed` affect parameters passed to GF functions using `gf_v1`.
- `portfolio_include_results`, `portfolio_include_passed` control returned validation details and passed records/validations.

Do not equate `payload_v1` with `gf_v1` parameter conventions. Existing host scripts cannot be assumed to support result flags. The adapter must be configured explicitly.

## Invariants to test

1. Stable host script names, `gf_function_name`, input bindings, case and calling style.
2. No silent reinterpretation of `success` vs `passed` or failed records.
3. Canonical severity precedence and threshold comparison.
4. Summary is constructed before optional interruption.
5. Whether `raise_error` is invoked in the host is preserved separately from a Python exception.
6. Same input and approved rules produce the same expected result; behavior changes require sign-off.

`docs/validation_function_contract.md` remains the original source contract for host-compatible functions. The development Engine still requires UAT before replacing any existing orchestration.
