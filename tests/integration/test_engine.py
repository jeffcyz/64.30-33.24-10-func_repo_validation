import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from validation_library.core.engine import ValidationEngine


class MockGF(object):
    def __init__(self):
        self.received = None

    def check_a(self, runtime_context=None, params=None, include_results=False, include_pass=False):
        self.received = (runtime_context, params, include_results, include_pass)
        return {"success": False, "severity": "CRITICAL", "results": [
            {"passed": True, "severity": "INFO"},
            {"passed": False, "severity": "CRITICAL"},
        ]}

    def check_b(self, runtime_context=None, params=None, include_results=False, include_pass=False):
        return True

    def check_payload(self, payload, runtime_context=None):
        return {"passed": bool(payload.get("deal_name")), "severity": "WARNING"}


class EngineTests(unittest.TestCase):
    def make_engine(self, gf):
        rules = {
            "a": {"gf_function_name": "check_a", "default_severity": "ERROR", "runtime_context_key": "bonds"},
            "b": {"gf_function_name": "check_b"},
        }
        portfolios = {"rmbs": {"name": "RMBS test", "validation_keys": ["a", "b"]}}
        return ValidationEngine(gf, rules, portfolios)

    def test_dispatch_and_separate_output_flags(self):
        gf = MockGF()
        payload = self.make_engine(gf).run_portfolio(
            "rmbs", bonds=[1], function_include_results=True,
            function_include_passed=True, portfolio_include_passed=False,
            portfolio_include_results=True, interrupt_enabled=True,
        )
        self.assertEqual(gf.received, ([1], {}, True, True))
        self.assertEqual(payload["portfolio_summary"]["total_validations"], 2)
        self.assertEqual(len(payload["validations"]), 1)
        self.assertEqual(len(payload["validations"][0]["results"]), 1)
        self.assertTrue(payload["should_interrupt"])

    def test_summary_only(self):
        payload = self.make_engine(MockGF()).run_portfolio("rmbs", portfolio_include_results=False)
        self.assertNotIn("results", payload["validations"][0])

    def test_raise_on_interrupt(self):
        with self.assertRaises(RuntimeError):
            self.make_engine(MockGF()).run_portfolio(
                "rmbs", interrupt_enabled=True, raise_on_interrupt=True
            )

    def test_payload_style(self):
        engine = ValidationEngine(
            MockGF(),
            {"x": {"gf_function_name": "check_payload", "call_style": "payload_v1"}},
            {"setup": {"validation_keys": ["x"]}},
        )
        out = engine.run_portfolio("setup", runtime_context={"deal_name": "Example"}, portfolio_include_passed=True)
        self.assertTrue(out["success"])

    def test_missing_gf_rejected(self):
        engine = ValidationEngine(MockGF(), {"x": {"gf_function_name": "not_here"}}, {"x": {"validation_keys": ["x"]}})
        with self.assertRaises(ValueError):
            engine.run_portfolio("x")


if __name__ == "__main__":
    unittest.main()
