"""Static registry and portfolio contract; never dynamically import rule scripts."""

from .severity import normalize_severity


def validate_registry(rules, portfolios):
    if not isinstance(rules, dict) or not isinstance(portfolios, dict):
        raise ValueError("Rules and portfolios must be dictionaries")
    for key, rule in rules.items():
        if not isinstance(rule, dict):
            raise ValueError("Invalid registry rule %r" % key)
        if not rule.get("gf_function_name"):
            raise ValueError("Missing gf_function_name for %r" % key)
        if rule.get("call_style", "gf_v1") not in ("gf_v1", "payload_v1"):
            raise ValueError("Unsupported call_style for %r" % key)
        normalize_severity(rule.get("default_severity", "ERROR"))
    for key, portfolio in portfolios.items():
        if not isinstance(portfolio, dict) or not isinstance(portfolio.get("validation_keys", []), list):
            raise ValueError("Invalid portfolio %r" % key)
        missing = [rule_key for rule_key in portfolio["validation_keys"] if rule_key not in rules]
        if missing:
            raise ValueError("Unknown rules in portfolio %s: %s" % (key, ", ".join(missing)))
    return True


def registry_from_document(document):
    if not isinstance(document, dict):
        raise ValueError("Registry document must be a dictionary")
    rules = document.get("validations", {})
    portfolios = document.get("portfolios", {})
    validate_registry(rules, portfolios)
    return rules, portfolios
