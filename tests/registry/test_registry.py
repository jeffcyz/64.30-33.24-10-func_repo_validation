import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from validation_library.core.registry import registry_from_document, validate_registry


class RegistryTests(unittest.TestCase):
    def test_example_registry(self):
        document = json.loads((ROOT / "configs/registry/example_rules.json").read_text(encoding="utf-8"))
        rules, portfolios = registry_from_document(document)
        self.assertIn("example_cmbs_periodic", portfolios)
        self.assertTrue(validate_registry(rules, portfolios))

    def test_unknown_rule_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_registry({"x": {"gf_function_name": "check"}}, {"bad": {"validation_keys": ["missing"]}})


if __name__ == "__main__":
    unittest.main()
