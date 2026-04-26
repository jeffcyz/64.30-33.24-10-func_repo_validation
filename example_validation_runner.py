import logging

from ironpython_validation_helpers import ValidationHelperApi
from periodic.periodic_validation_examples import run_periodic_validation_examples
from setup.setup_validation_examples import run_setup_validation_examples


def configure_logger():
    logger = logging.getLogger("validation")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    return logger


def build_sample_payloads():
    setup_payload = {
        "deal_id": "DEAL-001",
        "deal_name": "",
        "asset_type": "CMBS",
        "primary_analyst": None,
        "team": "CMBS Surveillance",
        "bond_id": "A1",
        "coupon_type_code": "FLT",
        "interest_type": "Fixed",
    }

    periodic_payload = {
        "deal_id": "DEAL-001",
        "bond_id": "A1",
        "asset_id": "ASSET-101",
        "loan_id": "LOAN-77",
        "period": "2026-03",
        "current_bond_balance": 102.50,
        "current_collateral_balance": 98.25,
        "scheduled_beginning_balance": 100.00,
        "scheduled_activity_delta": -8.00,
        "scheduled_ending_balance": 91.50,
        "special_serv_fee_expected": 2.35,
        "special_serv_fee_actual": 2.35,
    }
    return setup_payload, periodic_payload


def print_results(title, results):
    print("")
    print(title)
    print(ValidationHelperApi(operation="summarize_results", results=results))
    findings = ValidationHelperApi(
        operation="summarize_results",
        results=results,
        minimum_severity="WARNING",
        include_results=False,
    ).get("findings_at_or_above", [])
    for result in findings:
        print(result)


def main():
    logger = configure_logger()
    setup_payload, periodic_payload = build_sample_payloads()

    runtime_context = {
        "run_id": "demo-run-001",
        "source_system": "asset securitization analysis pro",
    }

    setup_results = run_setup_validation_examples(
        setup_payload,
        runtime_context=runtime_context,
        logger=logger,
    )
    periodic_results = run_periodic_validation_examples(
        periodic_payload,
        runtime_context=runtime_context,
        logger=logger,
    )
    overall_results = setup_results + periodic_results

    print_results("SETUP RESULTS", setup_results)
    print_results("PERIODIC RESULTS", periodic_results)
    print("")
    print("OVERALL SUMMARY")
    print(ValidationHelperApi(operation="summarize_results", results=overall_results))


if __name__ == "__main__":
    main()
