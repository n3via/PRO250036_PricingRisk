import json

from CORE.api.base_services import BaseAPIService
from CORE.utils.helper import load_json
from schemas.pricing_schemas import LoanProposalCustomerOfferRepr, CreditPricingComputationSimulateRequest

class CreditPricingServices(BaseAPIService):

    ## Endpoint condiviso da tutti i metodi del service
    endpoint = "/credit-pricing-computations"
    
    
    def __init__(self, client, logger=None):
        
        super().__init__(client)
        self.logger = logger or client.logger
    
    # def get_loan_proposal_offers(self, customer_offer_id):
    #
    #     path = f"{self.endpoint}/loan-proposal-offers/{customer_offer_id}"
    #     #return self.APIGET(path_override=path, response_model=LoanProposalCustomerOfferRepr)
    #
    # def get_loan_proposal_offers_test(self):
    #     path = f"/header-summary"
    #     query_string = "?customerOfferId=123456789"
    #     return self.APIGET(path_override=path)

    def post_credit_pricing_computations_simulate(self):
        path = f"{self.endpoint}/simulate"
        request_body = load_json("tc0003_credit_pricing_computations_simulate_request.json")
        return self.APIPOST(path_override=path, response_model=CreditPricingComputationSimulateRequest, body=request_body)


    def get_credit_pricing_computations(self):
        query_string = "?customerOfferId=123&servicingOrderId=123&arrangementDossierId=123&computationPhase=S"
        path = f"{self.endpoint}{query_string}"
        request_body = load_json("tc0003_credit_pricing_computations_simulate_request.json")
        return self.APIGET(path_override=path, response_model=CreditPricingComputationSimulateRequest)

    def get_credit_pricing_computations_by_id(self, computation_id):
        path = f"{self.endpoint}/{computation_id}"
        request_body = load_json("tc0003_credit_pricing_computations_simulate_request.json")
        return self.APIGET(path_override=path, response_model=CreditPricingComputationSimulateRequest)