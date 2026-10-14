from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from enum import Enum
from typing import List, Optional


class LoanProductType(str, Enum):
    CONSUMER = "CONSUMER"
    CORPORATE = "CORPORATE"
    LOAN = "LOAN"
    MERCHANDISING = "MERCHANDISING"
    MORTGAGE = "MORTGAGE"
    SYNDICATED = "SYNDICATED"


class MinimalLoanRepr(BaseModel):
    loanNumber: Optional[str] = None
    partyId: Optional[str] = None
    loanStatus: Optional[str] = None

    originationDate: Optional[date] = None
    risksAndCommitmentsDate: Optional[date] = None
    firstDisbursementDate: Optional[date] = None
    firstScheduledRepaymentDate: Optional[date] = None
    firstRepaymentDate: Optional[date] = None
    maturityDate: Optional[date] = None
    closingDate: Optional[date] = None

    repaymentType: Optional[str] = None
    interestPaymentType: Optional[int] = None

    loanProductType: Optional[LoanProductType] = None

    loanTypeCode: Optional[str] = None
    loanType: Optional[str] = None

    interestRateType: Optional[str] = None
    interestRate: Optional[float] = None

    riskStatus: Optional[bool] = None

    currency: Optional[str] = None

    grantedAmount: Optional[float] = None
    disbursedAmount: Optional[float] = None
    outstandingBalance: Optional[float] = None

    capAndFloorType: Optional[str] = None

    syndicatedLoanArranger: Optional[str] = None
    syndicatedLeadLenderOutstandingAmount: Optional[float] = None

    partyDescriptionId: Optional[str] = None