from ironpython_validation_helpers import ValidationHelperApi


VALIDATION_METADATA = {
    "script_name_display": "SetUpValidationInterestTypeExpectations",
    "function_key": "set_up_validation_interest_type_expectations",
    "focus": "SetUp",
    "asset": "All",
    "type": "Bond",
    "threshold": 5,
    "severity": "CRITICAL",
    "issue_code": "SETUP_INTEREST_TYPE_UNEXPECTED",
    "description": "Interest Type Expectations",
    "explanation": "Interest type should align with the selected coupon type code.",
    "impact": "Incorrect interest type can drive incorrect pricing, accrual, or downstream rule selection.",
    "action": "Review coupon type code and map the correct interest type.",
}


def SetUpValidationInterestTypeExpectations(payload, runtime_context=None, logger=None):
    coupon_type_code = payload.get("coupon_type_code")
    expected_interest_type = "Fixed"
    if coupon_type_code in ("FLT", "ARM", "FLOAT"):
        expected_interest_type = "Floating"

    return ValidationHelperApi(
        operation="equal",
        script_name_display="SetUpValidationInterestTypeExpectations",
        metadata=VALIDATION_METADATA,
        runtime_context=runtime_context,
        logger=logger,
        actual=payload.get("interest_type"),
        expected=expected_interest_type,
        field_name="interest_type",
        context={
            "deal_id": payload.get("deal_id"),
            "bond_id": payload.get("bond_id"),
            "coupon_type_code": coupon_type_code,
        },
        issue="Interest type does not match coupon type expectations",
        explanation="Coupon type code implies an expected interest type, and the configured value does not match.",
        impact="Interest calculations may use the wrong rule path.",
        action="Update interest type or coupon type code so they align.",
    )
