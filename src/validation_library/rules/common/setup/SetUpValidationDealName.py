from ironpython_validation_helpers import ValidationHelperApi


VALIDATION_METADATA = {
    "script_name_display": "SetUpValidationDealName",
    "function_key": "set_up_validation_deal_name",
    "focus": "SetUp",
    "asset": "All",
    "type": "Summary: Deal Details",
    "threshold": 3,
    "severity": "WARNING",
    "issue_code": "SETUP_DEAL_NAME_MISSING",
    "description": "Deal Name",
    "explanation": "Deal name must be populated during setup.",
    "impact": "Blank deal naming can break reporting, review workflows, and downstream identification.",
    "action": "Populate the deal name and rerun the validation.",
}


def SetUpValidationDealName(
    payload,
    runtime_context=None,
    logger=None,
    interrupt_after_scan=False,
):
    result = ValidationHelperApi(
        operation="required",
        script_name_display="SetUpValidationDealName",
        metadata=VALIDATION_METADATA,
        runtime_context=runtime_context,
        logger=logger,
        value=payload.get("deal_name"),
        field_name="deal_name",
        context={
            "deal_id": payload.get("deal_id"),
            "asset_type": payload.get("asset_type"),
        },
        issue="Deal name is missing",
    )

    if interrupt_after_scan and not result.get("passed"):
        raise ValueError(
            "SetUpValidationDealName failed after scan: severity=%s, deal_id=%s"
            % (
                result.get("severity"),
                result.get("context", {}).get("deal_id"),
            )
        )

    return result
