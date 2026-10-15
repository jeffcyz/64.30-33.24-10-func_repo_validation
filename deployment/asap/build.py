"""Build a deployable legacy-shaped artifact from modular authoring sources.

Run on the development workstation (CPython 3), not inside ASAP IronPython.
It never updates Git root files or the live ASAP environment.
"""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src" / "validation_library"
TARGETS = {
    "ironpython_validation_helpers.py": "helpers/validation_helper_api.py",
    "validation_api.py": "helpers/validation_helper_api.py",
    "SetUpValidationStateCode.py": "rules/common/setup/SetUpValidationStateCode.py",
    "validate_next_index_rate.py": "rules/common/payment/validate_next_index_rate.py",
    "host_compatible/setup/SetUpValidationDealName.py": "rules/common/setup/SetUpValidationDealName.py",
    "host_compatible/setup/SetUpValidationInterestTypeExpectations.py": "rules/common/setup/SetUpValidationInterestTypeExpectations.py",
    "host_compatible/periodic/PeriodicValidationAssetScheduledBalanceRollover.py": "rules/cmbs/payment/PeriodicValidationAssetScheduledBalanceRollover.py",
    "host_compatible/periodic/PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance.py": "rules/cmbs/payment/PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance.py",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def verify_legacy_mirrors():
    errors = []
    for destination, source in sorted(TARGETS.items()):
        current = ROOT / destination
        canonical = SRC / source
        if not current.is_file() or not canonical.is_file():
            errors.append("Missing: %s or %s" % (destination, source))
        elif current.read_bytes() != canonical.read_bytes():
            errors.append("Different: %s vs %s" % (destination, source))
    return errors


def build(output_dir):
    output_dir = Path(output_dir)
    manifest = {"format": "asap-legacy-script-bundle", "files": {}}
    for destination, source in sorted(TARGETS.items()):
        origin = SRC / source
        target = output_dir / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(origin), str(target))
        manifest["files"][destination] = sha256(target.read_bytes())
    (output_dir / "artifact_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Ensure root legacy scripts mirror the modular sources")
    parser.add_argument("--build", action="store_true", help="Build an isolated artifact in dist/asap")
    parser.add_argument("--output", default=str(ROOT / "dist" / "asap"))
    arguments = parser.parse_args()
    if not arguments.verify and not arguments.build:
        parser.error("Choose --verify, --build, or both")
    if arguments.verify:
        errors = verify_legacy_mirrors()
        if errors:
            for error in errors:
                print(error)
            raise SystemExit(1)
        print("All legacy sources match their new modular counterparts.")
    if arguments.build:
        manifest = build(arguments.output)
        print("Built %d ASAP-compatible source files in %s" % (len(manifest["files"]), arguments.output))


if __name__ == "__main__":
    main()
