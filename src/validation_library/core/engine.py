"""Portfolio orchestration with explicit ASAP GF dependency and stable output controls."""

import json

from .context import merge_runtime_context, select_runtime_context
from .registry import validate_registry
from .result_contract import normalize_validation_result
from .severity import meets_threshold, normalize_severity
from ..runtime.asap_adapter import ASAPAdapter


class ValidationEngine(object):
    def __init__(self, gf, validations=None, portfolios=None):
        self.validations = dict(validations or {})
        self.portfolios = dict(portfolios or {})
        validate_registry(self.validations, self.portfolios)
        self.adapter = ASAPAdapter(gf)

    def run_portfolio(
        self,
        portfolio_key,
        runtime_context=None,
        function_include_results=False,
        function_include_passed=False,
        portfolio_include_results=True,
        portfolio_include_passed=False,
        return_results=True,
        print_results=False,
        interrupt_enabled=False,
        interrupt_severity="CRITICAL",
        raise_on_interrupt=False,
        **runtime_inputs
    ):
        if portfolio_key not in self.portfolios:
            raise ValueError("Unknown portfolio: %s" % portfolio_key)
        threshold = normalize_severity(interrupt_severity)
        bundle = merge_runtime_context(runtime_context, **runtime_inputs)
        portfolio = self.portfolios[portfolio_key]
        output = []
        count_failed, count_passed = 0, 0
        severities = {}
        should_interrupt = False

        for key in portfolio["validation_keys"]:
            rule = self.validations[key]
            if not rule.get("enabled", True):
                continue
            selected_context = select_runtime_context(rule, bundle)
            params = dict(rule.get("default_params") or {})
            raw = self.adapter.invoke(
                rule, selected_context, params,
                function_include_results, function_include_passed,
            )
            item = normalize_validation_result(
                raw, key, rule.get("name", key), rule.get("default_severity", "ERROR")
            )
            if item["success"]:
                count_passed += 1
            else:
                count_failed += 1
                severity = item["highest_severity"]
                severities[severity] = severities.get(severity, 0) + 1
                if interrupt_enabled and meets_threshold(severity, threshold):
                    should_interrupt = True
            if not portfolio_include_passed and item["success"]:
                continue
            if not portfolio_include_results:
                item.pop("results", None)
            elif (not portfolio_include_passed or not function_include_passed) and isinstance(item.get("results"), list):
                from .result_contract import _record_passed
                item["results"] = [r for r in item["results"] if not _record_passed(r)]
            output.append(item)

        summary = {
            "total_validations": count_failed + count_passed,
            "passed_validations": count_passed,
            "failed_validations": count_failed,
            "by_severity": severities,
        }
        payload = {
            "portfolio_key": portfolio_key,
            "portfolio_name": portfolio.get("name", portfolio_key),
            "success": count_failed == 0,
            "should_interrupt": should_interrupt,
            "portfolio_summary": summary,
            "validations": output,
        }
        if print_results:
            print(json.dumps(payload, sort_keys=True, default=str))
        if should_interrupt and raise_on_interrupt:
            raise RuntimeError("ASAP validation interrupted: %s (%s)" % (portfolio_key, threshold))
        return payload if return_results else None
