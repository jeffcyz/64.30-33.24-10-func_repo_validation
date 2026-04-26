import os
import runpy
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from ironpython_validation_helpers import ValidationHelperApi


def load_function(relative_path, function_name):
    script_path = os.path.abspath(relative_path)
    if os.name == "nt":
        script_path = "\\\\?\\" + script_path
    namespace = runpy.run_path(script_path)
    return namespace[function_name]


def build_sample_payloads():
    setup_payload = {
        "deal_id": "DEAL-001",
        "deal_name": "",
        "asset_type": "CMBS",
        "bond_id": "A1",
        "coupon_type_code": "FLT",
        "interest_type": "Fixed",
    }
    periodic_payload = {
        "deal_id": "DEAL-001",
        "bond_id": "A1",
        "asset_id": "ASSET-101",
        "period": "2026-03",
        "current_bond_balance": 102.50,
        "current_collateral_balance": 98.25,
        "scheduled_beginning_balance": 100.00,
        "scheduled_activity_delta": -8.00,
        "scheduled_ending_balance": 91.50,
    }
    return setup_payload, periodic_payload


def main():
    set_up_validation_deal_name = load_function(
        os.path.join("host_compatible", "setup", "SetUpValidationDealName.py"),
        "SetUpValidationDealName",
    )
    set_up_validation_interest_type_expectations = load_function(
        os.path.join("host_compatible", "setup", "SetUpValidationInterestTypeExpectations.py"),
        "SetUpValidationInterestTypeExpectations",
    )
    periodic_validation_current_bond_balance_vs_current_collateral_balance = load_function(
        os.path.join(
            "host_compatible",
            "periodic",
            "PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance.py",
        ),
        "PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance",
    )
    periodic_validation_asset_scheduled_balance_rollover = load_function(
        os.path.join(
            "host_compatible",
            "periodic",
            "PeriodicValidationAssetScheduledBalanceRollover.py",
        ),
        "PeriodicValidationAssetScheduledBalanceRollover",
    )

    runtime_context = {
        "run_id": "host-demo-001",
        "source_system": "asset securitization analysis pro",
    }
    setup_payload, periodic_payload = build_sample_payloads()

    results = [
        set_up_validation_deal_name(setup_payload, runtime_context=runtime_context),
        set_up_validation_interest_type_expectations(setup_payload, runtime_context=runtime_context),
        periodic_validation_current_bond_balance_vs_current_collateral_balance(
            periodic_payload,
            runtime_context=runtime_context,
        ),
        periodic_validation_asset_scheduled_balance_rollover(
            periodic_payload,
            runtime_context=runtime_context,
        ),
    ]

    print("INDIVIDUAL RESULTS")
    for result in results:
        print(result)

    print("")
    print("SUMMARY ONLY")
    print(ValidationHelperApi(operation="summarize_results", results=results))

    print("")
    print("SUMMARY WITH HIGH-SEVERITY FINDINGS")
    print(
        ValidationHelperApi(
            operation="summarize_results",
            results=results,
            minimum_severity="WARNING",
            include_results=False,
        )
    )


if __name__ == "__main__":
    main()
