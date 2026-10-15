import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from validation_library.core.severity import normalize_severity, meets_threshold


class SeverityTests(unittest.TestCase):
    def test_order(self):
        self.assertTrue(meets_threshold("CRITICAL", "ERROR"))
        self.assertFalse(meets_threshold("WARNING", "ERROR"))

    def test_unknown_is_error(self):
        with self.assertRaises(ValueError):
            normalize_severity("BYPASS")


if __name__ == "__main__":
    unittest.main()
