## Descrizione: Lanciare GET /customer-offers/loan-proposal-offers/{customerOfferId}
## Risultato atteso: 200 OK con response body LoanProposalCustomerOfferRepr

import logging

import allure

from CORE.assertions.common_assertions import assert_status_code
from service.loan_proposal import PricingServices
from service.credit_pricing import CreditPricingServices
logger = logging.getLogger(__name__)


def test_TC0003_POST_CreditPricingComputationsSimulate(manual_token_client):
    # manual_token_client.headers["Accept"] = "application/json, text/plain, */*"

    with allure.step("STEP 1: --- Chiamata al servizio ---"):
        service = CreditPricingServices(manual_token_client)
        with allure.step("POST /customer-offers/loan-proposal-offers/customerOfferId"):
            response, data = service.post_credit_pricing_computations_simulate()

    with allure.step("STEP 2: --- Validazione della response ---"):
        assert_status_code(response, 200)