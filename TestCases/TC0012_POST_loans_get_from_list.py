## Descrizione: Lanciare GET /customer-offers/loan-proposal-offers/{customerOfferId}
## Risultato atteso: 200 OK con response body LoanProposalCustomerOfferRepr

import logging

import allure

from CORE.assertions.common_assertions import assert_status_code
from service.loan_resource_controller import LoanResourceControllerServices
logger = logging.getLogger(__name__)


def test_TC0012_POST_loans_get_from_list(manual_token_client):
    # manual_token_client.headers["Accept"] = "application/json, text/plain, */*"
    with allure.step("STEP 1: --- Chiamata al servizio ---"):
        service = LoanResourceControllerServices(manual_token_client)
        with allure.step("/loans/get-from-list"):
            response, data = service.post_loans_get_from_list()

    with allure.step("STEP 2: --- Validazione della response ---"):
        assert_status_code(response, 200)