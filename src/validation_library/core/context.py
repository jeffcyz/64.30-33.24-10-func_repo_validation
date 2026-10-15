"""Explicit context routing; no implicit ASAP global-object dependency."""


def merge_runtime_context(runtime_context=None, **runtime_inputs):
    result = dict(runtime_context or {})
    for key, value in runtime_inputs.items():
        if value is not None:
            result[key] = value
    return result


def select_runtime_context(rule, bundle):
    key = rule.get("runtime_context_key", "context")
    if key == "context":
        return bundle
    if key is None:
        return None
    if key not in bundle and rule.get("runtime_context_required", False):
        raise ValueError("Missing required runtime context %r for %r" % (key, rule.get("key")))
    return bundle.get(key)
