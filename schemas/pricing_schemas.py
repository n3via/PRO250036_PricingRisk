from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from enum import Enum
from typing import List, Optional



class LoanProposalMortgageMediationData(BaseModel):
	model_config = ConfigDict(extra="forbid")

	mortgageMediationType: str
	clientMediationExpense: int
	bankMediationExpense: int


class LoanProposalPublicGuaranteeData(BaseModel):
	model_config = ConfigDict(extra="forbid")

	publicGuaranteeType: str
	publicGuaranteeExpense: int
	publicGuaranteePercentage: int


class LoanProposalCustomerOfferRepr(BaseModel):
	model_config = ConfigDict(extra="forbid")

	id: int
	creationDate: date
	serviceCode: str
	marketingProductId: str
	productTermsId: str
	dossierId: str
	offerStatus: str
	partyId: str
	partyType: str
	branchId: str
	targetMarketId: str
	preAmortizationDuration: int
	preAmortizationPeriodicity: str
	amortizationDuration: int
	amortizationPeriodicity: str
	marketingCampaignCode: str
	mortgageMediationData: LoanProposalMortgageMediationData
	publicGuaranteeData: LoanProposalPublicGuaranteeData


class CreditPricingComputationSimulateRequest(BaseModel):

	# ============================================================
	# ENUMS
	# ============================================================

	class ServiceCodeType(str, Enum):
		M01 = "M01"
		C01 = "C01"
		F90 = "F90"
		P01 = "P01"

	class PeriodicityType(str, Enum):
		BULLET = "00"
		YEARLY = "01"
		SEMIANNUALLY = "02"
		TRIANNUAL = "03"
		QUARTERLY = "04"
		BIMONTHLY = "06"
		MONTHLY = "12"

	class DriverCode(str, Enum):
		PARTNER = "01"
		LOAN_TO_VALUE = "03"
		INSTALMENT_INCOME_RATIO = "04"
		CUSTOMER_TENURE = "05"
		NACE_CODE = "06"
		COMPETENCE_ZONE = "07"
		AGE = "08"
		COMMERCIAL_CAMPAIGN = "Campagna"

	class PricingOutcome(str, Enum):
		GREATER_THAN_USURY = "GREATER_THAN_USURY"
		BETWEEN_STANDARD_AND_USURY = "BETWEEN_STANDARD_AND_USURY"
		BETWEEN_BREAK_EVEN_AND_STANDARD = "BETWEEN_BREAK_EVEN_AND_STANDARD"
		LOWER_THAN_BREAK_EVEN_AND_BIGGER_THAN_RECOMMENDED = (
			"LOWER_THAN_BREAK_EVEN_AND_BIGGER_THAN_RECOMMENDED"
		)
		LOWER_THAN_BREAK_EVEN_AND_RECOMMENDED = (
			"LOWER_THAN_BREAK_EVEN_AND_RECOMMENDED"
		)

	class CurrentAccountType(str, Enum):
		SINGLE = "S"
		ORDINARY = "O"
		ADVANCE = "A"

	# ============================================================
	# FINANCIAL STATEMENT
	# ============================================================

	class FinancialStatementRepr(BaseModel):
		financialStatementNumber: int

		interestIncome: float
		interestExpense: float
		netInterestMargin: float

		feeMargin: float
		intermediationMargin: float

		valueAdjustments: float
		netOperatingResult: float

		operatingCosts: float

		grossProfit: float
		taxes: float

		netProfit: float

		eva: float
		rorwa: float

	# ============================================================
	# MARKUP
	# ============================================================

	class MarkupRepr(BaseModel):
		driver: CreditPricingComputationSimulateRequest.DriverCode
		markup: float

	# ============================================================
	# PRICING COMPONENT
	# ============================================================

	class PricingComponentRepr(BaseModel):
		# opzionale (non marcato con *)
		id: Optional[int] = None

		serviceCode: CreditPricingComputationSimulateRequest.ServiceCodeType

		tanBreakEven: float
		tanEffectiveRecommended: float
		tanEffectiveStandard: float
		tanEffectiveProposed: float

		signatureCreditPeriodicity: Optional[CreditPricingComputationSimulateRequest.PeriodicityType] = None

		commissionBreakEven: float
		commissionEffectiveRecommended: float
		commissionStandard: float
		commissionEffectiveProposed: float

		instalmentCommissionBreakEven: float
		instalmentCommissionEffectiveRecommended: float
		instalmentCommissionEffectiveProposed: float
		instalmentCommissionStandard: float

		tegBreakEven: float
		tegProposed: float
		tegRecommended: float
		tegStandard: float
		tegUsury: float

		baseRate: float

		breakEvenSpread: float
		creditRiskSpread: float
		fundingCostSpread: float
		operatingCostSpread: float
		capitalCostSpread: float
		commissionCostSpread: float

		recommendedFinancialStatements: List[CreditPricingComputationSimulateRequest.FinancialStatementRepr]
		proposedFinancialStatements: List[CreditPricingComputationSimulateRequest.FinancialStatementRepr]

		stateSecurity100Flag: bool

		productMarkup: float
		crossProductMarkup: float
		extraMarginMarkup: float
		totalMarkup: float

		crossProductMarkups: List[CreditPricingComputationSimulateRequest.MarkupRepr]

		outcome: CreditPricingComputationSimulateRequest.PricingOutcome

		obscureTeg: bool

		currentAccountType: Optional[CreditPricingComputationSimulateRequest.CurrentAccountType] = None
		singleAccountFlag: Optional[bool] = None

	# ============================================================
	# ROOT RESPONSE
	# ============================================================

	class CreditPricingRepr(BaseModel):
		evaRecommended: Optional[float] = None
		evaProposed: Optional[float] = None

		rorwaRecommended: Optional[float] = None
		rorwaProposed: Optional[float] = None

		pricingComponents: List[CreditPricingComputationSimulateRequest.PricingComponentRepr]