import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "deployment" / "asap"))
from build import TARGETS, verify_legacy_mirrors, build


class DeploymentParityTests(unittest.TestCase):
    def test_preserve_every_existing_script(self):
        self.assertEqual(verify_legacy_mirrors(), [])

    def test_at_least_seven_files(self):
        self.assertGreaterEqual(len(TARGETS), 7)


if __name__ == "__main__":
    unittest.main()
