# ASAP host UAT

Do **not** treat Python CI as proof of compatibility with the real ASAP 2.0 GF host.

Required manual checks before release:
1. Confirm IronPython version, first-function behavior, import support and precise GF names.
2. Run setup and periodic scripts on approved non-production Deals.
3. Validate `raise_error` behavior, JSON contracts, severity/interrupt and result inclusion.
4. Compare with signed-off baseline; attach anonymized result diffs to PR.
5. Validate exact deployed bundle SHA-256 and approved rollback plan.

No production transaction data or credentials should be committed to this public repository.
