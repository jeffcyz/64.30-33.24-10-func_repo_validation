# Validation Script Inventory

Source: OCR from `Screenshot 2026-04-16 131318.png`.

Working assumptions:
- `focus` is inferred from the `SetUp` or `Periodic` prefix in the script name.
- Thresholds and descriptions are OCR-derived and should be human-verified before final production use.
- A few names contain punctuation that would not be valid as a Python identifier. Treat those as display names from the host system, not as a recommended internal function key.

## SetUp

- `SetUpValidationDealName` | threshold=`3` | Deal Name
- `SetUpValidationDealDescription` | threshold=`5` | Deal Description
- `SetUpValidationAssetType` | threshold=`5` | Asset Type
- `SetUpValidationCollateralPurpose` | threshold=`5` | Collateral Purpose
- `SetUpValidationCurrencyType` | threshold=`3` | Currency Type
- `SetUpValidationHolidaySchedule` | threshold=`5` | Holiday Schedule
- `SetUpValidationPaymentFrequency` | threshold=`3` | Payment Frequency
- `SetUpValidationCutoffDate` | threshold=`3` | Cutoff Date
- `SetUpValidationFirstPayDate` | threshold=`5` | First Pay Date
- `SetUpValidationRecordDate` | threshold=`5` | Record Date
- `SetUpValidationTerminationDate` | threshold=`5` | Termination Date
- `SetUpValidationTeamMember` | threshold=`5` | Team Member
- `SetUpValidationDealContact:PrimaryAnalyst` | threshold=`5` | Deal Contact: Primary Analyst
- `SetUpValidationDealContact:SecondaryAnalyst` | threshold=`3` | Deal Contact: Secondary Analyst
- `SetUpValidationDealContact:PrimaryAdministrator` | threshold=`5` | Deal Contact: Primary Administrator
- `SetUpValidationDealContact:PrimaryOperations` | threshold=`3` | Deal Contact: Primary Operations
- `SetUpValidationDealContact:ValidationAnalyst` | threshold=`3` | Deal Contact: Validation Analyst
- `SetUpValidationCounterparty` | threshold=`5` | Counterparty
- `SetUpValidationIncorrectStateClassification` | threshold=`2` | Incorrect State Classification
- `SetUpValidationStateCode` | threshold=`2` | State value is a valid state code
- `SetUpValidationIncorrectPropertyTypeClassification` | threshold=`2` | Incorrect Property Type Classification
- `SetUpValidationBondAliasPopulation` | threshold=`4` | Bond Alias Population
- `SetUpValidationCurrencyTypeSelected` | threshold=`5` | Currency Type Selected
- `SetUpValidationTierNumberNotSelected` | threshold=`3` | Tier Number Not Selected
- `SetUpValidationDenominationAndType` | threshold=`5` | Denomination and Type
- `SetUpValidationInterestTypeExpectations` | threshold=`5` | Interest Type Expectations
- `SetUpValidationAccrualTypeSelected` | threshold=`5` | Accrual Type Selected
- `SetUpValidationFirstPayDatePopulated` | threshold=`5` | First Pay Date Populated
- `SetUpValidationRecordDatePopulated` | threshold=`5` | Record Date Populated
- `SetUpValidationIndexNamePopulationExpectations` | threshold=`5` | Index Name Population Expectations
- `SetUpValidationGroupNumberPopulated` | threshold=`5` | Group Number Populated
- `SetUpValidationSubpoolPopulation` | threshold=`5` | Subpool Population
- `SetUpValidationAccrualTypeChosen` | threshold=`5` | Accrual Type Chosen
- `SetUpValidationCouponTypeCodeChosen` | threshold=`5` | Coupon Type Code Chosen
- `SetUpValidationBondRatingPopulation` | threshold=`2` | Bond Rating Population

## Periodic

- `PeriodicValidationInterestAccruedParameters` | threshold=`5` | Interest Accrued Parameters
- `PeriodicValidationInterestPaidParameters` | threshold=`5` | Interest Paid Parameters
- `PeriodicValidationCurrIntPaidParameters` | threshold=`5?` | CurrIntPaid Parameters
- `PeriodicValidationTotalInterestPaidParameters` | threshold=`5` | Total Interest Paid Parameters
- `PeriodicValidationOTCCIntParameters` | threshold=`5?` | OTCCInt Parameters
- `PeriodicValidationCurrentClass%` | threshold=`3` | Current Class %
- `PeriodicValidationOrigCredSupport%` | threshold=`3` | Orig Cred Support %
- `PeriodicValidationNextIndexRate` | threshold=`3` | Next Index Rate
- `PeriodicValidationFeeRate/StripRates` | threshold=`5` | Fee Rate/Strip Rates
- `PeriodicValidationBondIntendedPaydown` | threshold=`3` | Bond Intended Paydown
- `PeriodicValidationBondBalanceLimitations` | threshold=`5` | Bond Balance Limitations
- `PeriodicValidationRemittance=CashIn` | threshold=`5` | Remittance=CashIn
- `PeriodicValidationCurrentBondBalanceVsCurrentCollateralBalance` | threshold=`3` | Current Bond Balance Vs Current Collateral Balance
- `PeriodicValidationCurrentNoteRateToReachCurrentNetRate` | threshold=`5` | Current Note Rate to Reach Current Net Rate
- `PeriodicValidationNoteRateAtContributionToReachNetRateAtContribution` | threshold=`5` | Note Rate at Contribution to Reach Net Rate at Contribution
- `PeriodicValidationNotionalBondCurrentBalanceCheck` | threshold=`5` | Notional Bond Current Balance Check
- `PeriodicValidationNotionalClassesShouldNotPayPrincipal` | threshold=`4` | Notional Classes Should Not Pay Principal
- `PeriodicValidationResidualClassBeingPaid` | threshold=`3` | Residual Class Being Paid
- `PeriodicValidationAssetHasANegativeEndingBalance` | threshold=`5` | Asset has a Negative Ending Balance
- `PeriodicValidationAssetPrincipalAndLossComponentsAreTooLarge` | threshold=`5` | Asset Principal and Loss Components Are Too Large
- `PeriodicValidationAssetsHaveYMAmount;BondsShouldAsWell` | threshold=`5` | Assets Have YM Amount; Bonds Should as Well
- `PeriodicValidationAssetScheduledBalanceRollover` | threshold=`3` | Asset Scheduled Balance Rollover
- `PeriodicValidationAssetActualBalanceRollover` | threshold=`2` | Asset Actual Balance Rollover
- `PeriodicValidationFixedRateRollover` | threshold=`3?` | Fixed Rate Rollover
- `PeriodicValidationPeriod1BeginningScheduledBalance` | threshold=`3` | Period 1 Beginning Scheduled Balance
- `PeriodicValidationCurrentNoteRateDetermination` | threshold=`3` | Current Note Rate Determination
- `PeriodicValidationInterestOnlyLoansOnlyPayingInterest` | threshold=`3` | Interest Only Loans Only Paying Interest
- `PeriodicValidationEndingScheduledBalanceDetermination` | threshold=`5` | Ending Scheduled Balance Determination
- `PeriodicValidationDeferredInterestRollover` | threshold=`5` | Deferred Interest Rollover
- `PeriodicValidationTotalDeferredInterestCalculated` | threshold=`5` | Total Deferred Interest Calculated
- `PeriodicValidationBeginningLoanCount` | threshold=`3` | Beginning Loan Count
- `PeriodicValidationInterestReserveAccount` | threshold=`5` | Interest Reserve Account
- `PeriodicValidationDrasticAssetStatusChange` | threshold=`3` | Drastic Asset Status Change
- `PeriodicValidationFixedRateNextReporting` | threshold=`3` | Fixed Rate Next Reporting
- `PeriodicValidationSpecialServFeeCalcVersusActual` | threshold=`3` | SpecialServFee Calc Versus Actual
- `PeriodicValidationOtherFee1VersusActual` | threshold=`3` | OtherFee1 Versus Actual
- `PeriodicValidationOtherFee2VersusActual` | threshold=`3` | OtherFee2 Versus Actual
- `PeriodicValidationOtherFee3VersusActual` | threshold=`3` | OtherFee3 Versus Actual
- `PeriodicValidationOtherFee4VersusActual` | threshold=`3` | OtherFee4 Versus Actual
- `PeriodicValidationOtherFee5VersusActual` | threshold=`3` | OtherFee5 Versus Actual
- `PeriodicValidationLiquidFeeAmtVersusActual` | threshold=`3` | LiquidFeeAmt Versus Actual
- `PeriodicValidationCurrMasterServFeeVersusActual` | threshold=`3` | CurrMasterServFee Versus Actual
- `PeriodicValidationCurrSubServFeeVersusActual` | threshold=`3` | CurrSubServFee Versus Actual
- `PeriodicValidationCurrTrustFeeVersusActual` | threshold=`3` | CurrTrustFee Versus Actual
- `PeriodicValidationCurrInsurFeeVersusActual` | threshold=`3` | CurrInsurFee Versus Actual
- `PeriodicValidationServFeeVersusActual` | threshold=`3` | ServFee Versus Actual
- `PeriodicValidationExcessServFeeVersusActual` | threshold=`3` | ExcessServFee Versus Actual
- `PeriodicValidationMSSurveillanceFeeVersusActual` | threshold=`3` | MSSurveillanceFee Versus Actual
- `PeriodicValidationSSSurveillanceFeeVersusActual` | threshold=`3` | SSSurveillanceFee Versus Actual
- `PeriodicValidationCollatAdminFeeVersusActual` | threshold=`3` | CollatAdminFee Versus Actual
- `PeriodicValidationCertAdminFeeVersusActual` | threshold=`3` | CertAdminFee Versus Actual
- `PeriodicValidationCustodianFeeVersusActual` | threshold=`3` | CustodianFee Versus Actual
- `PeriodicValidationOwnerTrustFeeVersusActual` | threshold=`3` | OwnerTrustFee Versus Actual
- `PeriodicValidationTotalFeesExpensesVersusActual` | threshold=`3` | TotalFeesExpenses Versus Actual
- `PeriodicValidationWorkoutFeeAmtVersusActual` | threshold=`3` | WorkoutFeeAmt Versus Actual
- `PeriodicValidationServAndTrustFeeRateVersusActual` | threshold=`3` | ServAndTrustFeeRate Versus Actual
- `PeriodicValidationCurrSubServFeeRateVersusActual` | threshold=`3` | CurrSubServFeeRate Versus Actual
- `PeriodicValidationDisclSpecialServicerFeeVersusActual` | threshold=`3?` | DisclSpecialServicerFee Versus Actual

## Low-Confidence OCR Follow-Up

- Confirm whether `PeriodicValidationOTCCIntParameters` should be `OTCC` or `DTCC`.
- Confirm whether `%`, `/`, `=`, `;`, and `:` are literal host-system script names or only display labels.
- Confirm the exact threshold for `PeriodicValidationCurrIntPaidParameters`.
- Confirm the exact threshold for `PeriodicValidationFixedRateRollover`.
- Confirm the exact threshold for `PeriodicValidationDisclSpecialServicerFeeVersusActual`.
- If these names need to become callable IronPython identifiers, create a registry alias from display name to a safe internal `function_key`.
