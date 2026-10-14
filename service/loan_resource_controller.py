import json

from CORE.api.base_services import BaseAPIService
from CORE.utils.helper import load_json
from schemas.loans_schemas import MinimalLoanRepr

class LoanResourceControllerServices(BaseAPIService):

    ## Endpoint condiviso da tutti i metodi del service
    endpoint = "/loans"
    
    
    def __init__(self, client, logger=None):
        
        super().__init__(client)
        self.logger = logger or client.logger
    

    def get_loan_proposal_offers(self):
            
        path = f"{self.endpoint}/loans"
        query_params = load_json("tc0006_get_loans.json")
        return self.APIGET(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)

    def get_loan_with_loan_number(self,loan_number):
        query_params = load_json("tc0007_get_loans_loannumber.json")
        path = f"{self.endpoint}/loans/{loan_number}"
        return self.APIGET(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)

    def get_loan_with_loan_number_repayments(self,loan_number):
        query_params = load_json("tc0008_get_loans_loannumber_repayments.json")
        path = f"{self.endpoint}/loans/{loan_number}/repayments"
        return self.APIGET(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)

    def get_loans_repayment_simulation(self):
        query_params = load_json("tc0009_get_loans_repayment_simulation.json")
        path = f"{self.endpoint}/loans/repayment-simulation"
        return self.APIGET(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)


    def get_loans_products(self):
        query_params = load_json("tc0010_get_loans_products.json")
        path = f"{self.endpoint}/loans/products"
        return self.APIGET(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)

    def get_loans_demostrative_plan(self):
        query_params = load_json("tc0011_get_loans_demostrative_plan.json")
        path = f"{self.endpoint}/loans/demonstrative-plan"
        return self.APIGET(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)


    def post_loans_get_from_list(self):
        query_params = load_json("tc0012_get_loans_demostrative_plan_by_id.json")
        path = f"{self.endpoint}/loans/get-from-list"
        return self.APIPOST(path_override=path, response_model=MinimalLoanRepr, queryString=query_params)
