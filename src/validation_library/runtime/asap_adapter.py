"""ASAP GF dispatcher supporting explicitly configured calling conventions."""


class ASAPAdapter(object):
    def __init__(self, gf):
        self.gf = gf

    def invoke(self, rule, runtime_context, params, include_results, include_passed):
        name = rule["gf_function_name"]
        func = getattr(self.gf, name, None)
        if func is None or not callable(func):
            raise ValueError("ASAP GF is unavailable or not callable: %s" % name)
        style = rule.get("call_style", "gf_v1")
        if style == "gf_v1":
            return func(
                runtime_context=runtime_context,
                params=params,
                include_results=include_results,
                include_pass=include_passed,
            )
        if style == "payload_v1":
            payload = params.get("payload", runtime_context)
            if not isinstance(payload, dict):
                raise ValueError("payload_v1 requires a dictionary payload")
            return func(payload, runtime_context=runtime_context)
        raise ValueError("Unsupported GF calling convention: %s" % style)
