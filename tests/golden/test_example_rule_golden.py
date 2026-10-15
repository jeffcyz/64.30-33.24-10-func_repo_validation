import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


class GoldenRuleTests(unittest.TestCase):
    def test_host_compatible_deal_name(self):
        source = ROOT / "host_compatible/setup/SetUpValidationDealName.py"
        spec = importlib.util.spec_from_file_location("legacy_deal_name_golden", str(source))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.SetUpValidationDealName({"deal_id": "TEST", "deal_name": ""})
        actual = {key: result[key] for key in ("passed", "status", "severity", "issue_code")}
        expected = {"passed": False, "status": "FAIL", "severity": "WARNING", "issue_code": "SETUP_DEAL_NAME_MISSING"}
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
