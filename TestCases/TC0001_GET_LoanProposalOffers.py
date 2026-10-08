## Descrizione: Lanciare GET /customer-offers/loan-proposal-offers/{customerOfferId}
## Risultato atteso: 200 OK con response body LoanProposalCustomerOfferRepr

import logging

import allure

from CORE.assertions.common_assertions import assert_status_code
from service.loan_proposal import PricingServices


logger = logging.getLogger(__name__)


def test_TC0001_GET_LoanProposalOffers(manual_token_client):
    
    #manual_token_client.headers["Accept"] = "application/json, text/plain, */*"
    
    with allure.step("STEP 1: --- Chiamata al servizio ---"):
        service = PricingServices(manual_token_client)
        with allure.step("GET /customer-offers/loan-proposal-offers/customerOfferId"):
            customer_offer_id = ""
            response, data = service.get_loan_proposal_offers(customer_offer_id)
    
    with allure.step("STEP 2: --- Validazione della response ---"):
        assert_status_code(response, 200)