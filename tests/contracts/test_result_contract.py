import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from validation_library.core.result_contract import normalize_validation_result


class ContractTests(unittest.TestCase):
    def test_boolean_legacy(self):
        item = normalize_validation_result(False, "rule_a", "A", "WARNING")
        self.assertFalse(item["success"])
        self.assertEqual(item["highest_severity"], "WARNING")

    def test_record_level(self):
        item = normalize_validation_result([
            {"passed": True, "severity": "INFO"},
            {"passed": False, "severity": "CRITICAL"},
        ], "rule_a", "A")
        self.assertEqual(item["summary"]["fail"], 1)
        self.assertEqual(item["highest_severity"], "CRITICAL")

    def test_fail_closed_for_ambiguous(self):
        with self.assertRaises(ValueError):
            normalize_validation_result({"summary": {}}, "rule_a", "A")


if __name__ == "__main__":
    unittest.main()
