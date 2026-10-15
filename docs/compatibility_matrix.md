# Compatibility Matrix

| Interface | Legacy baseline | New branch | Validation required |
| --- | --- | --- | --- |
| Root Python GF helper entry | `ValidationHelperApi` | byte-identical mirrored source | SHA/bytes equality in CI |
| Host-compatible setup and periodic scripts | first callable host function | byte-identical mirrored source | CI parity + host UAT |
| `SetUpValidationStateCode` and `validate_next_index_rate` | script-global asap2_obj inputs | same source mirrored, legacy path retained | CI parity + host UAT |
| Registry template | CSV | byte-identical source under configs | CI parity |
| ValidationEngine | design prompts (Markdown) | newly implemented development orchestration | fake-GF integration only; **NOT production certified** |
| Severity / result contract | existing helper behavior | local normalization for Engine | unit/contract tests; validate native GF behavior in UAT |
| RMBS and ABS modules | no deployable modules confirmed in this repo snapshot | empty package paths | future implementation; not marked complete |
| CMBS periodic rules | two documented host-compatible examples | copies under `rules/cmbs/payment` | category mapping / deploy UAT |
| Deal-specific version selection | host capability unverified | sample manifest only | investigate host loading/version switching |

## Compatibility gates

- **CI:** `python -m unittest discover -s tests -p "test_*.py"`, mirror parity and bundle creation.
- **Pre-release UAT:** real IronPython import checks, GF resolution, runtime object routing, interruption and host `raise_error`.
- **Business regression:** sanitized fixtures representing Setup and Periodic by actual asset-class applicability; record pass/fail, numeric tolerances, severity and summary.
- **Audit:** record code SHA, artifact digest, rule set, enabled rules and Deal-level deployment approvals.

Do not automatically promote anything from the development branch to production.
