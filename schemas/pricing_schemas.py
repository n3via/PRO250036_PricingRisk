from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


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
