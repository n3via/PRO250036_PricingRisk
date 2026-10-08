"""
conftest.py (root)

Questo file centralizza la configurazione pytest dell'intero progetto.
Qui vengono definiti:
- fixture autouse che arricchiscono automaticamente il report Allure per ogni test;
- fixture di sessione condivise tra piu test (es. shared_vars);
- hook pytest di bootstrap e di chiusura sessione;
- fixture helper per costruire un client API con token bearer.

Flusso tipico durante un run:
1) pytest avvia i test e carica questo conftest globale;
2) per ogni test, le fixture autouse impostano titolo/attachment Allure;
3) i risultati raw Allure restano disponibili in allure-results.
"""

import pytest
import logging
import allure
import json
import os
from pathlib import Path
from CORE.config.config_loader import load_config
from CORE.utils.allure_shared_vars import attach_shared_vars_snapshot
from CORE.utils.variable_store import VariableStore
import tools.generate_allure_testcase_reports as per_testcase_reports


logging.getLogger("httpx").disabled = True
logging.getLogger("httpcore").disabled = True

pytest_plugins = ["CORE.fixtures.api_client_fixture"]


# ---------------------------------------------------------------------------
# Allure: titolo dinamico del testcase
# ---------------------------------------------------------------------------
# Questa fixture e autouse, quindi gira per ogni test senza doverla dichiarare
# nella firma della funzione test. Serve per evitare titoli statici e rendere
# il report piu leggibile con il nome reale del node pytest.
@pytest.fixture(autouse=True)
def allure_dynamic_title(request):
    """Imposta un titolo dinamico Allure per ogni test."""
    allure.dynamic.title(request.node.name)


# ---------------------------------------------------------------------------
# Allure: attachment traffico API direttamente sul testcase
# ---------------------------------------------------------------------------
# Usiamo un hook di reporting invece di una fixture teardown per assicurare che
# gli attachment vengano associati al testcase (non solo al container fixture).
def _resolve_api_client(funcargs: dict) -> object | None:
    return funcargs.get("api_client") or funcargs.get("manual_token_client")


def _attach_api_calls(calls: list[dict]) -> None:
    if not calls:
        return

    summary = []
    for idx, call in enumerate(calls, start=1):
        request_info = call.get("request", {}) or {}
        response_info = call.get("response", {}) or {}
        status = response_info.get("status", "")
        method = request_info.get("method", "")
        url = request_info.get("url", "")
        error_message = response_info.get("error")

        summary.append({
            "index": idx,
            "method": method,
            "url": url,
            "status": status,
            "error": error_message,
        })

        curl_command = request_info.get("curl")
        if curl_command:
            allure.attach(
                str(curl_command),
                name=f"API call #{idx} - curl",
                attachment_type=allure.attachment_type.TEXT,
            )

        allure.attach(
            json.dumps(request_info, ensure_ascii=False, indent=2, default=str),
            name=f"API call #{idx} - request",
            attachment_type=allure.attachment_type.JSON,
        )

        request_body = request_info.get("body")
        if request_body is not None:
            body_attachment = request_body
            body_type = allure.attachment_type.JSON if isinstance(request_body, (dict, list)) else allure.attachment_type.TEXT
            if isinstance(request_body, (dict, list)):
                body_attachment = json.dumps(request_body, ensure_ascii=False, indent=2, default=str)
            allure.attach(
                str(body_attachment),
                name=f"API call #{idx} - request body",
                attachment_type=body_type,
            )

        allure.attach(
            str(status),
            name=f"API call #{idx} - status code",
            attachment_type=allure.attachment_type.TEXT,
        )

        body = response_info.get("body", "")
        body_text = "" if body is None else str(body)
        body_type = allure.attachment_type.HTML if "<" in body_text and ">" in body_text else allure.attachment_type.TEXT

        response_payload = {
            "status": status,
            "headers": response_info.get("headers", {}),
        }
        allure.attach(
            json.dumps(response_payload, ensure_ascii=False, indent=2, default=str),
            name=f"API call #{idx} - response meta",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            body_text,
            name=f"API call #{idx} - response body",
            attachment_type=body_type,
        )

        validation_errors = response_info.get("validation_errors")
        if error_message:
            allure.attach(
                str(error_message),
                name=f"API call #{idx} - error",
                attachment_type=allure.attachment_type.TEXT,
            )
        if validation_errors:
            allure.attach(
                json.dumps(validation_errors, ensure_ascii=False, indent=2, default=str),
                name=f"API call #{idx} - validation errors",
                attachment_type=allure.attachment_type.JSON,
            )

    allure.attach(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str),
        name="API calls summary",
        attachment_type=allure.attachment_type.JSON,
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    if report.failed:
        longrepr = getattr(report, "longreprtext", None) or str(getattr(report, "longrepr", ""))
        if longrepr:
            allure.attach(
                longrepr,
                name="Test failure details",
                attachment_type=allure.attachment_type.TEXT,
            )

    #funcargs = getattr(item, "funcargs", {}) or {}
    #api_client = _resolve_api_client(funcargs)
    #if not api_client:
    #    return

    #calls = getattr(api_client, "_calls", None) or []
    #_attach_api_calls(calls)


@pytest.fixture(autouse=True)
def allure_attach_shared_vars(shared_vars):
    """Allega automaticamente le variabili condivise (se presenti) a fine test."""
    yield
    # Lo snapshot viene allegato solo se ci sono valori nel VariableStore.
    attach_shared_vars_snapshot(allure, shared_vars)


# ---------------------------------------------------------------------------
# Logging globale
# ---------------------------------------------------------------------------
# Configurazione base valida per tutto il processo pytest.
# Fornisce timestamp + logger name + livello per facilitare debug nei log.
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------------------------------
# Fixture di sessione: path root progetto
# ---------------------------------------------------------------------------
# Scope session: creato una sola volta per l'intero run.
@pytest.fixture(scope="session")
def project_root():
    """Ritorna il path del progetto root"""
    return Path(__file__).parent


# ---------------------------------------------------------------------------
# Fixture di sessione: store condiviso tra testcase
# ---------------------------------------------------------------------------
# VariableStore consente di passare dati tra test (quando necessario),
# mantenendo API esplicite (set/get/require) e attachment Allure dedicato.
@pytest.fixture(scope="session")
def shared_vars():
    """Store condiviso per salvare e riusare variabili estratte nei vari test.

    Esempio:
    - test A: shared_vars.set("party_id", "00020245")
    - test B: party_id = shared_vars.require("party_id")
    """
    return VariableStore()


@pytest.fixture(scope="session", autouse=True)
def seed_shared_vars_from_config(shared_vars):
    """Precarica docid/revid/action in shared_vars da config.test_data se disponibili."""
    cfg = load_config() or {}
    test_data = cfg.get("test_data", {}) if isinstance(cfg, dict) else {}

    for key in ("docid", "revid", "action", "correlationid", "ackid"):
        if key in test_data:
            shared_vars.set(key, test_data[key])


# ---------------------------------------------------------------------------
# Hook pytest: registrazione marker custom
# ---------------------------------------------------------------------------
# Questo evita warning sui marker non registrati e documenta i tipi di test.
def pytest_configure(config):
    """Hook per configurazioni iniziali di pytest"""
    # Aggiungi marker personalizzati
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "api: mark test as an API test")
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "slow: mark test as slow")


def pytest_sessionfinish(session, exitstatus):
    if session.config.option.collectonly:
        return

    # In split-run mode, report generation is handled explicitly by run_test_plan.py
    if os.getenv("PYTEST_SKIP_PER_TESTCASE_AUTOGEN") == "1":
        return

    try:
        per_testcase_reports.main(["--allure-results", "allure-results"])
    except Exception as exc:
        logging.getLogger(__name__).warning(
            "[pytest] Warning: errore generazione report per testcase: %s",
            exc,
        )


# ---------------------------------------------------------------------------
# Fixture helper: client API autenticato con bearer token da config ambiente
# ---------------------------------------------------------------------------
# Legge il token dall'ambiente attivo (config/environments.yaml), lo normalizza
# e lo applica sia sugli header custom del wrapper sia sul client httpx interno.
@pytest.fixture
def manual_token_client(api_client):
    config_loader = load_config()
    token = config_loader['auth']['token']
    if isinstance(token, str):
        # Riduce errori dovuti a token incollati con spazi/newline finali.
        token = token.strip()
    if not token:
        raise ValueError(
            "Token bearer mancante: configura environments.<env>.auth.token in environments.yaml "
            "(supporta anche placeholder ${NOME_VARIABILE})."
        )

    bearer_value = f"Bearer {token}"
    # ApiClient usa api_client.headers come sorgente per ogni request.
    api_client.headers["Authorization"] = bearer_value
    # Manteniamo coerente anche il client httpx sottostante.
    api_client.client.headers["Authorization"] = bearer_value

    return api_client
 
