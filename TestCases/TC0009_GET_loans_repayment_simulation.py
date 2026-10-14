## Descrizione: Lanciare GET /customer-offers/loan-proposal-offers/{customerOfferId}
## Risultato atteso: 200 OK con response body LoanProposalCustomerOfferRepr

import logging

import allure

from CORE.assertions.common_assertions import assert_status_code
from service.loan_resource_controller import LoanResourceControllerServices
logger = logging.getLogger(__name__)


def test_TC0009_GET_loans_repayment_simulation(manual_token_client):
    # manual_token_client.headers["Accept"] = "application/json, text/plain, */*"
    with allure.step("STEP 1: --- Chiamata al servizio ---"):
        service = LoanResourceControllerServices(manual_token_client)
        with allure.step("/loans/repayment-simulation"):
            response, data = service.get_loans_repayment_simulation()

    with allure.step("STEP 2: --- Validazione della response ---"):
        assert_status_code(response, 200)