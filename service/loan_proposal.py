import json

from CORE.api.base_services import BaseAPIService
from CORE.utils.helper import load_json
from schemas.pricing_schemas import LoanProposalCustomerOfferRepr


class PricingServices(BaseAPIService):

    ## Endpoint condiviso da tutti i metodi del service
    endpoint = "/customer-offers"
    
    
    def __init__(self, client, logger=None):
        
        super().__init__(client)
        self.logger = logger or client.logger
    
    
    
    def get_loan_proposal_offers(self, customer_offer_id):
            
        path = f"{self.endpoint}/loan-proposal-offers/{customer_offer_id}"
        return self.APIGET(path_override=path, response_model=LoanProposalCustomerOfferRepr)

    def get_loan_proposal_offers_test(self):
        path = f"/header-summary"
        query_string = "?customerOfferId=123456789"
        return self.APIGET(path_override=path)

