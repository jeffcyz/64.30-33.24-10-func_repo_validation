from ironpython_validation_helpers import ValidationHelperApi


VALIDATION_METADATA = {
    "script_name_display": "PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance",
    "function_key": "periodic_validation_current_bond_balance_vs_current_collateral_balance",
    "focus": "Periodic",
    "asset": "CMBS",
    "type": "Deal Level",
    "threshold": 3,
    "severity": "WARNING",
    "issue_code": "PERIODIC_BOND_VS_COLLATERAL_BALANCE",
    "description": "Current Bond Balance Vs Current Collateral Balance",
    "explanation": "Current bond balance should reconcile to the linked collateral balance for the reporting period.",
    "impact": "Bond reporting and waterfall checks may be unreliable.",
    "action": "Review bond-collateral mapping, remittance inputs, and rollover logic.",
}


def PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance(payload, runtime_context=None, logger=None):
    return ValidationHelperApi(
        operation="within_tolerance",
        script_name_display="PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance",
        metadata=VALIDATION_METADATA,
        runtime_context=runtime_context,
        logger=logger,
        actual=payload.get("current_bond_balance"),
        expected=payload.get("current_collateral_balance"),
        tolerance=0.01,
        field_name="current bond balance vs collateral balance",
        context={
            "deal_id": payload.get("deal_id"),
            "bond_id": payload.get("bond_id"),
            "period": payload.get("period"),
        },
        issue="Current bond balance does not reconcile to collateral balance",
    )
