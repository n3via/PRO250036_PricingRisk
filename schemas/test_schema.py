from datetime import date

from pydantic import BaseModel

class LoginPageSchema(BaseModel):
    kycExpiryDate: date
    kycUpdateNeeded: bool
    kycUpdateNeededNew: int
    partyId: str
    amlRiskRating: str
    juridicalSpecies: str
