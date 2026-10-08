# PRO230109_Anagrafe

Suite di test API per il progetto Anagrafe basata sul framework condiviso `PYTEST_FRAMEWORK`.

---

# Prerequisiti

Clonare entrambe le repository nella stessa cartella:

```text
Allitude

├── PYTEST_FRAMEWORK
└── PRO230109_Anagrafe
```

---

# Setup

## 1. Creazione Virtual Environment

Posizionarsi nella root del progetto:

```bash
cd PRO230109_Anagrafe
```

Creare la virtual environment:

```bash
python -m venv .venv
```

Attivarla:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 2. Installazione dipendenze e aggiornamento dipendenze

Installare il framework e le relative dipendenze:

```bash install
pip install -e {percorso_alla_cartella}\PYTEST_FRAMEWORK
```
```bash update
pip install -U -e ../PYTEST_FRAMEWORK

##oppure

pip install --upgrade -e ../PYTEST_FRAMEWORK
```

```

---

## Verifica installazione

Aprire Python:

```bash
python
```

Esempio di import dal framework:

```python
from CORE.api.base_services import BaseAPIService
```

Se non vengono restituiti errori, il framework è correttamente collegato.

Uscire da Python:

```python
exit()
```

---

# Struttura

```text
PRO230109_Anagrafe

├── config
├── schemas
├── service
├── TestCases
├── TestData
├── run_test_plan.py
├── requirements.txt
└── README.md
```

---

# Configurazione

## test_plan.yaml

Definisce:

- progetto
- testcase da eseguire
- configurazioni di esecuzione

Percorso:

```text
config/test_plan.yaml
```

---

## environments.yaml

Definisce:

- ambiente attivo
- base_url
- timeout
- header
- token di autenticazione

Percorso:

```text
config/environments.yaml
```

Esempio:

```yaml
default_environment: local

environments:
  local:
    auth:
      token: ${LOCAL_BEARER_TOKEN}
```

---

# Esecuzione Test

## Eseguire l'intera suite

```bash
pytest
```

---

## Eseguire raccolta test

```bash
pytest --collect-only -q
```

---

## Eseguire un testcase

```bash
pytest -k "TC0001_GET_Employees" -v
```

---

## Eseguire tramite test plan

```bash
python run_test_plan.py
```

---

## Generare report separati

```bash
python run_test_plan.py --split-reports
```

---

## Eseguire testcase specifici

```bash
python run_test_plan.py --case-ids TC0001_GET_Employees
```

---

## Eseguire più testcase

```bash
python run_test_plan.py --split-reports --case-ids TC0001_GET_Employees TC0002_POST_Employees
```

---

# Reportistica

Risultati raw:

```text
allure-results/
```

Report HTML:

```text
reports/PRO230109_Anagrafe/allure_html/
```

Report separati:

```text
reports/PRO230109_Anagrafe/mail_ready/
```

---

# Struttura funzionale

## schemas

Contiene i modelli Pydantic:

```text
schemas/
```

---

## service

Contiene i service API:

```text
service/
```

---

## TestCases

Contiene tutti i testcase:

```text
TestCases/
```

---

## TestData

Contiene file e dataset utilizzati dai test.

---

# Workflow di sviluppo

Il codice specifico del progetto deve rimanere all'interno di questa repository.

Le modifiche comuni devono essere implementate nel repository:

```text
PYTEST_FRAMEWORK
```

---

# Gestione GITHUB e Branch
Per evitare conflitti e mantenere stabile il branch principale, ogni sviluppatore deve lavorare sul proprio branch personale.

## Branch disponibili

```text
main
elena
federico
benedetto
giorgia
giulia
```

## Regole

- Non lavorare direttamente sul branch `main`.
- Ogni sviluppatore deve utilizzare esclusivamente il proprio branch personale.
- Il branch `main` deve contenere solo codice stabile e condiviso.
- Le modifiche devono essere testate prima del merge su `main`.

---

## Prima di iniziare a lavorare

Aggiornare il branch principale:

```bash
git checkout main
git pull
```

Passare al proprio branch:

```bash
git checkout giulia
```

Aggiornare il proprio branch con le ultime modifiche presenti su `main`:

```bash
git merge main
```

---

## Durante lo sviluppo

Effettuare commit sul proprio branch:

```bash
git add .
git commit -m "Descrizione modifica"
git push origin giulia
```

---

## Conclusione dello sviluppo

Quando una funzionalità è completata:

1. Verificare che tutti i test siano verdi.
2. Effettuare il push sul proprio branch.
3. Creare una Pull Request verso `main`.
4. Effettuare il merge solo dopo la verifica delle modifiche.

Flusso:

```text
giulia
   ↓
Pull Request
   ↓
main
```

---

## Esempio completo

```bash
git checkout main
git pull

git checkout giulia
git merge main

# sviluppo

git add .
git commit -m "Aggiunta reportistica dipendenti"
git push origin giulia
```

# Note

- Non copiare componenti del framework all'interno del progetto.
- Utilizzare sempre classi e utility tramite import da `CORE`.
- Le nuove funzionalità condivise devono essere sviluppate nel framework.
- Le personalizzazioni Anagrafe devono rimanere all'interno del progetto.