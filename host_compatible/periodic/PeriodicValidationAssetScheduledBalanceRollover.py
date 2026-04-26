from ironpython_validation_helpers import ValidationHelperApi


VALIDATION_METADATA = {
    "script_name_display": "PeriodicValidationAssetScheduledBalanceRollover",
    "function_key": "periodic_validation_asset_scheduled_balance_rollover",
    "focus": "Periodic",
    "asset": "CMBS",
    "type": "Asset",
    "threshold": 3,
    "severity": "WARNING",
    "issue_code": "PERIODIC_ASSET_SCHEDULED_BALANCE_ROLLOVER",
    "description": "Asset Scheduled Balance Rollover",
    "explanation": "Ending scheduled balance should equal beginning scheduled balance plus current-period scheduled balance activity.",
    "impact": "Asset movement reporting and reconciliation may be unreliable.",
    "action": "Review beginning balance, scheduled principal activity, and ending balance inputs.",
}


def PeriodicValidationAssetScheduledBalanceRollover(payload, runtime_context=None, logger=None):
    return ValidationHelperApi(
        operation="roll_forward",
        script_name_display="PeriodicValidationAssetScheduledBalanceRollover",
        metadata=VALIDATION_METADATA,
        runtime_context=runtime_context,
        logger=logger,
        beginning_balance=payload.get("scheduled_beginning_balance"),
        activity_delta=payload.get("scheduled_activity_delta"),
        ending_balance=payload.get("scheduled_ending_balance"),
        tolerance=0.01,
        field_name="scheduled balance",
        context={
            "deal_id": payload.get("deal_id"),
            "asset_id": payload.get("asset_id"),
            "period": payload.get("period"),
        },
        issue="Scheduled balance roll-forward does not reconcile",
        explanation="Scheduled ending balance should reconcile from beginning balance plus scheduled activity for the period.",
        impact="Scheduled activity trends and exception reporting may be misleading.",
        action="Check prior-period carry-forward and current-period scheduled activity inputs.",
    )
