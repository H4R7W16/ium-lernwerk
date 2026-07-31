# IUM10 Privacy-Vertrag Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Den heuristischen CORE-07-Freitextparser durch einen allgemeinen, fail-closed maschinenlesbaren Privacy-Vertrag ersetzen und `IUM-5-CORE-07` vollständig auf Schema 2 migrieren, ohne Coverage-, Zeit- oder Graphentscheidungen zu verändern.

**Architecture:** `roadmap/time-model.json` erhält einen Modul-Privacy-Vertrag und je Zeitreview eine recordgenaue Disposition. `scripts/validate_ium10.py` validiert Modulgrenze, IUM09-Handoff, Evidenzbasis und private Produkt-/Evidenz-/Zeitbeiträge strukturell; der parserabhängige Testcode entfällt erst nach nachgewiesenem RED/GREEN der neuen Verträge.

**Tech Stack:** Python 3 Standardbibliothek, `unittest`, JSON, bestehende IUM09-/IUM10-Validatoren, Git.

## Global Constraints

- Autoritative Spezifikation: `docs/superpowers/specs/2026-07-31-ium10-privacy-vertrag-design.md`.
- `roadmap/time-model.json` wechselt exakt von `schemaVersion: 1` auf `schemaVersion: 2`.
- Die erste Migration registriert genau einen Modulvertrag: `PC-IUM-5-CORE-07`.
- Der Modulvertrag besitzt ausschließlich `id`, `moduleId`, `scope`, `artifactOwner`, `artifactCustody`, `institutionalHandling`, `status`.
- `institutionalHandling` besitzt ausschließlich `access`, `observation`, `collection`, `transfer`, `storage`, `assessment`; jeder Wert ist exakt `prohibited`.
- `scope == "private-local-reflection"`, `artifactOwner == "learner"`, `artifactCustody == "learner-controlled"`.
- Jeder der sieben CORE-07-Zeitreviews besitzt genau eine `privacyDisposition`.
- `privacyDisposition` besitzt ausschließlich `contractId`, `observableBasis`, `evidenceContractId`, `privateArtifactContribution`, `privateActivityTimeTreatment`.
- `privateArtifactContribution` besitzt ausschließlich `product`, `evidence`, `additionalTimeClaim`; jeder Wert ist exakt `excluded`.
- `privateActivityTimeTreatment == "module-budget-only"`.
- CORE-07-Mapping: vier `nonpersonal-follow-up`, ein `nonpersonal-module-detail`, zwei `none`.
- Positive CORE-07-Record-Minuten bleiben exakt 65; nichtadditive Phasenclaims bleiben davon getrennt.
- `BMB16-GYM-PK-RK-003` und `LH26-E-DP-003` bleiben `unresolved`, ohne Evidenzvertrag, Phase, Pfad oder Zusatzminute.
- CORE-07 bleibt bei 4/5/6 UE; Klasse 5/6 bleiben bei 30/34/38 UE; Klasse 7 bleibt bei 40/46/54 UE.
- IUM09 bleibt bei 164 `covered` und 7 `partial`; Modul-, Coverage- und Handoff-Fingerprints bleiben unverändert.
- `roadmap/module-candidates.json`, `roadmap/coverage-plan.json`, `roadmap/coverage-remediation.json`, `curriculum/`, `scripts/validate_ium09.py` und `tests/test_validate_ium09.py` werden nicht geändert.
- Klasse-7-Daten werden nicht migriert.
- Der Freitextparser ist kein Fallback. Datenschutzfehler führen zu `IUM10ValidationError`.
- Vor jedem Commit: `git fetch --prune`, danach `git pull --ff-only`; bei Fehler stoppen.
- Kein Push in diesem Plan. Der übergeordnete IUM10-Plan pusht erst in Task 26.
- Jeder Task erhält einen frischen Implementer und anschließend einen unabhängigen Taskreview. Fixrunden folgen dem SDD-Ledger.

## File Structure

| Datei | Verantwortung |
|---|---|
| `roadmap/time-model.json` | Schema 2, Modul-Privacy-Vertrag und sieben CORE-07-Dispositionen |
| `scripts/validate_ium10.py` | Strukturelle Vertrags- und Dispositionsvalidierung |
| `tests/test_validate_ium10.py` | Unit-, Mutations-, Repository- und Bilanztests; Entfernung des Freitextparsers |
| `.superpowers/sdd/2026-07-30-ium10-zeitmodell-modulroadmap-implementation/task-14-report.md` | Git-ignorierter Nachweis für RED/GREEN, Migration und korrigierte Minutenbilanz |

## Execution Setup

Vor Task 1:

```powershell
git status --short --branch
$implementationBase = (git rev-parse HEAD).Trim()
```

Der Controller dokumentiert `$implementationBase` im neuen SDD-Ledger dieses Plans. Alle Scope- und Reviewranges dieses Plans beginnen an diesem gespeicherten Commit, nicht an `HEAD~1` und nicht am Designcommit.

---

### Task 1: Modul-Privacy-Verträge fail-closed validieren

**Files:**
- Modify: `scripts/validate_ium10.py:25-90`
- Modify: `scripts/validate_ium10.py:787-866`
- Test: `tests/test_validate_ium10.py:9-24`
- Test: `tests/test_validate_ium10.py:2052`

**Interfaces:**
- Consumes: validierte Modulverträge als `dict[str, dict]`, Schlüssel = `moduleId`.
- Produces:

```python
def validate_privacy_contracts(
    privacy_contracts,
    module_contracts,
):
    """Validate privacy contracts and return them keyed by contract id."""
```

- Produces bei Erfolg: `dict[str, dict]`, Schlüssel = `PC-<moduleId>`.
- Produces bei Fehler: `IUM10ValidationError` mit Modul-ID und verletztem Feld.

- [ ] **Step 1: Import und Testfixture für den neuen Validator vorbereiten**

Ergänze im bestehenden Importblock in `tests/test_validate_ium10.py`:

```python
validate_privacy_contracts,
```

Füge vor `IUM10TimeReviewTests` eine neue Klasse ein:

```python
class IUM10PrivacyContractTests(unittest.TestCase):
    MODULE_ID = "IUM-5-CORE-07"
    CONTRACT_ID = "PC-IUM-5-CORE-07"

    @classmethod
    def module_contracts(cls):
        return {
            cls.MODULE_ID: {
                "moduleId": cls.MODULE_ID,
                "status": "working",
            }
        }

    @classmethod
    def privacy_contract(cls):
        return {
            "id": cls.CONTRACT_ID,
            "moduleId": cls.MODULE_ID,
            "scope": "private-local-reflection",
            "artifactOwner": "learner",
            "artifactCustody": "learner-controlled",
            "institutionalHandling": {
                "access": "prohibited",
                "observation": "prohibited",
                "collection": "prohibited",
                "transfer": "prohibited",
                "storage": "prohibited",
                "assessment": "prohibited",
            },
            "status": "working",
        }
```

- [ ] **Step 2: RED für gültigen Vertrag und unbekannte Funktion ausführen**

Füge hinzu:

```python
def test_accepts_the_exact_module_privacy_contract(self):
    result = validate_privacy_contracts(
        [self.privacy_contract()],
        self.module_contracts(),
    )

    self.assertEqual(set(result), {self.CONTRACT_ID})
    self.assertEqual(result[self.CONTRACT_ID]["moduleId"], self.MODULE_ID)
```

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests.test_accepts_the_exact_module_privacy_contract
```

Expected: `ImportError` oder `NameError`, weil `validate_privacy_contracts` noch fehlt.

- [ ] **Step 3: Exakte Struktur- und Mutations-REDs schreiben**

Füge diese Tests mit wörtlichen Mutationen hinzu:

```python
def test_rejects_each_missing_or_extra_top_level_field(self):
    for field in tuple(self.privacy_contract()):
        with self.subTest(missing=field):
            contract = self.privacy_contract()
            del contract[field]
            with self.assertRaisesRegex(IUM10ValidationError, "fields"):
                validate_privacy_contracts(
                    [contract],
                    self.module_contracts(),
                )

    contract = self.privacy_contract()
    contract["note"] = "x"
    with self.assertRaisesRegex(IUM10ValidationError, "fields"):
        validate_privacy_contracts([contract], self.module_contracts())

def test_rejects_each_invalid_or_empty_top_level_value(self):
    mutations = (
        ("wrong id", lambda c: c.__setitem__("id", "PC-WRONG"), "id"),
        ("wrong scope", lambda c: c.__setitem__("scope", "shared"), "scope"),
        ("wrong owner", lambda c: c.__setitem__("artifactOwner", "teacher"), "artifactOwner"),
        ("wrong custody", lambda c: c.__setitem__("artifactCustody", "institution"), "artifactCustody"),
        ("boolean status", lambda c: c.__setitem__("status", True), "status"),
        ("wrong status", lambda c: c.__setitem__("status", "accepted"), "status"),
    )
    for label, mutate, message in mutations:
        with self.subTest(label=label):
            contract = self.privacy_contract()
            mutate(contract)
            with self.assertRaisesRegex(IUM10ValidationError, message):
                validate_privacy_contracts([contract], self.module_contracts())

    for field in (
        "id",
        "moduleId",
        "scope",
        "artifactOwner",
        "artifactCustody",
        "status",
    ):
        with self.subTest(empty=field):
            contract = self.privacy_contract()
            contract[field] = ""
            with self.assertRaises(IUM10ValidationError):
                validate_privacy_contracts(
                    [contract],
                    self.module_contracts(),
                )

def test_rejects_every_nonprohibited_institutional_handling_value(self):
    for field in (
        "access",
        "observation",
        "collection",
        "transfer",
        "storage",
        "assessment",
    ):
        with self.subTest(field=field):
            contract = self.privacy_contract()
            contract["institutionalHandling"][field] = "allowed"
            with self.assertRaisesRegex(
                IUM10ValidationError,
                f"{self.MODULE_ID}.*{field}",
            ):
                validate_privacy_contracts([contract], self.module_contracts())

def test_rejects_each_missing_or_extra_handling_field(self):
    extra = self.privacy_contract()
    extra["institutionalHandling"]["profiling"] = "prohibited"
    with self.assertRaisesRegex(IUM10ValidationError, "institutionalHandling"):
        validate_privacy_contracts([extra], self.module_contracts())

    for field in tuple(
        self.privacy_contract()["institutionalHandling"]
    ):
        with self.subTest(missing=field):
            contract = self.privacy_contract()
            del contract["institutionalHandling"][field]
            with self.assertRaisesRegex(
                IUM10ValidationError,
                "institutionalHandling",
            ):
                validate_privacy_contracts(
                    [contract],
                    self.module_contracts(),
                )

def test_rejects_duplicates_and_orphans(self):
    duplicate = copy.deepcopy(self.privacy_contract())
    orphan = self.privacy_contract()
    orphan["id"] = "PC-IUM-5-CORE-99"
    orphan["moduleId"] = "IUM-5-CORE-99"

    cases = (
        (
            "duplicate",
            [self.privacy_contract(), duplicate],
            self.module_contracts(),
            "unique",
        ),
        ("orphan", [orphan], self.module_contracts(), "unknown module"),
    )
    for label, contracts, modules, message in cases:
        with self.subTest(label=label):
            with self.assertRaisesRegex(IUM10ValidationError, message):
                validate_privacy_contracts(contracts, modules)
```

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
```

Expected: RED wegen fehlender Funktion.

- [ ] **Step 4: Minimalen Privacy-Vertragsvalidator implementieren**

Ergänze in `scripts/validate_ium10.py`:

```python
PRIVACY_CONTRACT_FIELDS = {
    "id",
    "moduleId",
    "scope",
    "artifactOwner",
    "artifactCustody",
    "institutionalHandling",
    "status",
}
INSTITUTIONAL_HANDLING_FIELDS = {
    "access",
    "observation",
    "collection",
    "transfer",
    "storage",
    "assessment",
}


def validate_privacy_contracts(privacy_contracts, module_contracts):
    """Validate privacy contracts and return them keyed by contract id."""
    _require(
        isinstance(privacy_contracts, list),
        "privacy contracts must be a list",
    )
    _require(
        isinstance(module_contracts, dict),
        "validated module contracts must be keyed by module id",
    )

    contracts_by_id = {}
    contracted_module_ids = set()
    for contract in privacy_contracts:
        _require(isinstance(contract, dict), "privacy contract must be an object")
        _require(
            set(contract) == PRIVACY_CONTRACT_FIELDS,
            "privacy contract fields differ from the IUM10 contract",
        )
        module_id = contract["moduleId"]
        contract_id = contract["id"]
        _require(
            isinstance(module_id, str) and module_id in module_contracts,
            f"privacy contract references unknown module: {module_id}",
        )
        _require(
            contract_id == f"PC-{module_id}",
            f"invalid privacy contract id: {module_id}",
        )
        _require(
            contract_id not in contracts_by_id
            and module_id not in contracted_module_ids,
            f"privacy contract ids and module ids must be unique: {module_id}",
        )
        _require(
            contract["scope"] == "private-local-reflection",
            f"invalid privacy scope: {module_id}",
        )
        _require(
            contract["artifactOwner"] == "learner",
            f"invalid artifactOwner: {module_id}",
        )
        _require(
            contract["artifactCustody"] == "learner-controlled",
            f"invalid artifactCustody: {module_id}",
        )
        handling = contract["institutionalHandling"]
        _require(
            isinstance(handling, dict)
            and set(handling) == INSTITUTIONAL_HANDLING_FIELDS,
            f"invalid institutionalHandling fields: {module_id}",
        )
        for field in sorted(INSTITUTIONAL_HANDLING_FIELDS):
            _require(
                handling[field] == "prohibited",
                f"{module_id} institutional handling {field} must be prohibited",
            )
        _require(
            isinstance(contract["status"], str)
            and contract["status"] in CONTRACT_STATUSES,
            f"invalid privacy status: {module_id}",
        )
        contracts_by_id[contract_id] = contract
        contracted_module_ids.add(module_id)
    return contracts_by_id
```

- [ ] **Step 5: GREEN und Mutationssensitivität ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests
```

Expected: alle Tests `OK`.

- [ ] **Step 6: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: validate IUM10 privacy contracts"
```

---

### Task 2: Recordgenaue Privacy-Dispositionen validieren

**Files:**
- Modify: `scripts/validate_ium10.py:1916-2450`
- Test: `tests/test_validate_ium10.py:2052-2248`

**Interfaces:**
- Consumes aus Task 1: validiertes Mapping von `validate_privacy_contracts()`.
- Erweitert kompatibel:

```python
def validate_time_reviews(
    time_reviews,
    remediation_payload,
    module_contracts,
    integration_contracts,
    annual_variants,
    require_complete=False,
    *,
    privacy_contracts=None,
):
    ...
```

- Produces: dieselbe Review-ID-Zuordnung wie bisher.
- `privacy_contracts=None` bedeutet leeres Mapping; bestehende nichtprivate Handtests bleiben kompatibel.

- [ ] **Step 1: Testhelper um Privacy-Vertrag und Disposition erweitern**

Erweitere `IUM10TimeReviewTests.validate_reviews()`:

```python
def validate_reviews(
    self,
    reviews,
    *,
    remediation_payload=None,
    module_contracts=None,
    integration_contracts=None,
    annual_variants=None,
    require_complete=False,
    privacy_contracts=None,
):
    return validate_time_reviews(
        reviews,
        self.remediation_payload
        if remediation_payload is None
        else remediation_payload,
        self.module_contracts() if module_contracts is None else module_contracts,
        self.integration_contracts()
        if integration_contracts is None
        else integration_contracts,
        self.annual_variants() if annual_variants is None else annual_variants,
        require_complete,
        privacy_contracts=privacy_contracts,
    )
```

Füge Helper hinzu:

```python
@classmethod
def core07_privacy_contracts(cls):
    return validate_privacy_contracts(
        [IUM10PrivacyContractTests.privacy_contract()],
        cls.module_contracts(),
    )

@staticmethod
def private_disposition(competency_id, observable_basis):
    return {
        "contractId": "PC-IUM-5-CORE-07",
        "observableBasis": observable_basis,
        "evidenceContractId": (
            None
            if observable_basis == "none"
            else f"CE-IUM-5-CORE-07-{competency_id}"
        ),
        "privateArtifactContribution": {
            "product": "excluded",
            "evidence": "excluded",
            "additionalTimeClaim": "excluded",
        },
        "privateActivityTimeTreatment": "module-budget-only",
    }
```

- [ ] **Step 2: RED für gültige private-local-Disposition schreiben**

```python
def test_accepts_private_local_review_with_nonpersonal_follow_up(self):
    competency_id = "BMB16-GYM-IK-MG-001"
    review = self.review(competency_id, "additional-time")
    review["privacyDisposition"] = self.private_disposition(
        competency_id,
        "nonpersonal-follow-up",
    )

    result = self.validate_reviews(
        [review],
        privacy_contracts=self.core07_privacy_contracts(),
    )

    self.assertEqual(set(result), {f"TR-{competency_id}"})
```

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests.test_accepts_private_local_review_with_nonpersonal_follow_up
```

Expected: RED, weil `validate_time_reviews()` das neue Schlüsselwort oder Feld noch nicht akzeptiert.

- [ ] **Step 3: RED-Matrix für Aktivierung, Evidenzbasis und Ausschlüsse schreiben**

Füge Tests mit diesen exakten Fällen hinzu:

```python
def test_rejects_private_local_review_without_module_contract(self):
    review = self.review("BMB16-GYM-IK-MG-001", "additional-time")
    with self.assertRaisesRegex(IUM10ValidationError, "private-local.*privacy"):
        self.validate_reviews([review], privacy_contracts={})

def test_rejects_protected_module_review_without_disposition(self):
    review = self.review("BMB16-GYM-IK-MG-001", "additional-time")
    with self.assertRaisesRegex(IUM10ValidationError, "privacyDisposition"):
        self.validate_reviews(
            [review],
            privacy_contracts=self.core07_privacy_contracts(),
        )

def test_rejects_orphan_disposition_on_unprotected_module(self):
    review = self.review("BMB16-GYM-IK-GM-001", "additional-time")
    review["privacyDisposition"] = self.private_disposition(
        "BMB16-GYM-IK-GM-001",
        "nonpersonal-follow-up",
    )
    with self.assertRaisesRegex(IUM10ValidationError, "orphan"):
        self.validate_reviews([review], privacy_contracts={})

def test_rejects_private_disposition_reference_and_basis_drift(self):
    competency_id = "BMB16-GYM-IK-MG-001"
    mutations = (
        ("contract", ("contractId",), "PC-WRONG", "contractId"),
        (
            "basis",
            ("observableBasis",),
            "nonpersonal-module-detail",
            "observableBasis",
        ),
        (
            "unknown basis",
            ("observableBasis",),
            "personal-artifact",
            "observableBasis",
        ),
        (
            "evidence",
            ("evidenceContractId",),
            "CE-WRONG",
            "evidenceContractId",
        ),
        (
            "time treatment",
            ("privateActivityTimeTreatment",),
            "record-minutes",
            "module-budget-only",
        ),
        (
            "product",
            ("privateArtifactContribution", "product"),
            "included",
            "product",
        ),
        (
            "evidence contribution",
            ("privateArtifactContribution", "evidence"),
            "included",
            "evidence",
        ),
        (
            "time contribution",
            ("privateArtifactContribution", "additionalTimeClaim"),
            "included",
            "additionalTimeClaim",
        ),
    )
    for label, path, value, message in mutations:
        with self.subTest(label=label):
            review = self.review(competency_id, "additional-time")
            disposition = self.private_disposition(
                competency_id,
                "nonpersonal-follow-up",
            )
            target = disposition
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            review["privacyDisposition"] = disposition
            with self.assertRaisesRegex(IUM10ValidationError, message):
                self.validate_reviews(
                    [review],
                    privacy_contracts=self.core07_privacy_contracts(),
                )

def test_rejects_each_missing_or_extra_disposition_field(self):
    competency_id = "BMB16-GYM-IK-MG-001"
    disposition = self.private_disposition(
        competency_id,
        "nonpersonal-follow-up",
    )
    cases = []
    for field in tuple(disposition):
        mutated = copy.deepcopy(disposition)
        del mutated[field]
        cases.append((f"missing {field}", mutated, "privacyDisposition"))
    extra = copy.deepcopy(disposition)
    extra["note"] = "x"
    cases.append(("extra disposition", extra, "privacyDisposition"))

    for field in tuple(disposition["privateArtifactContribution"]):
        mutated = copy.deepcopy(disposition)
        del mutated["privateArtifactContribution"][field]
        cases.append((f"missing contribution {field}", mutated, "privateArtifactContribution"))
    extra_contribution = copy.deepcopy(disposition)
    extra_contribution["privateArtifactContribution"]["note"] = "x"
    cases.append(
        (
            "extra contribution",
            extra_contribution,
            "privateArtifactContribution",
        )
    )

    for label, mutated, message in cases:
        with self.subTest(label=label):
            review = self.review(competency_id, "additional-time")
            review["privacyDisposition"] = mutated
            with self.assertRaisesRegex(IUM10ValidationError, message):
                self.validate_reviews(
                    [review],
                    privacy_contracts=self.core07_privacy_contracts(),
                )

def test_rejects_cross_module_privacy_contract_reference(self):
    competency_id = "BMB16-GYM-IK-MG-001"
    core07 = IUM10PrivacyContractTests.privacy_contract()
    other = IUM10PrivacyContractTests.privacy_contract()
    other["id"] = "PC-IUM-5-CORE-01"
    other["moduleId"] = "IUM-5-CORE-01"
    privacy_contracts = validate_privacy_contracts(
        [core07, other],
        self.module_contracts(),
    )
    review = self.review(competency_id, "additional-time")
    review["privacyDisposition"] = self.private_disposition(
        competency_id,
        "nonpersonal-follow-up",
    )
    review["privacyDisposition"]["contractId"] = other["id"]

    with self.assertRaisesRegex(IUM10ValidationError, "contractId"):
        self.validate_reviews(
            [review],
            privacy_contracts=privacy_contracts,
        )
```

- [ ] **Step 4: RED für module-detail und unresolved `none` schreiben**

```python
def test_accepts_module_detail_and_unresolved_privacy_dispositions(self):
    module_detail_id = "BMB16-GYM-IK-MG-002"
    unresolved_id = "BMB16-GYM-PK-RK-003"
    module_detail = self.review(module_detail_id, "additional-time")
    module_detail["privacyDisposition"] = self.private_disposition(
        module_detail_id,
        "nonpersonal-module-detail",
    )
    unresolved = self.review(unresolved_id, "unresolved")
    unresolved["privacyDisposition"] = self.private_disposition(
        unresolved_id,
        "none",
    )

    result = self.validate_reviews(
        [module_detail, unresolved],
        privacy_contracts=self.core07_privacy_contracts(),
    )

    self.assertEqual(
        set(result),
        {f"TR-{module_detail_id}", f"TR-{unresolved_id}"},
    )

def test_rejects_none_with_evidence_phase_path_integration_sequence_or_minutes(self):
    competency_id = "BMB16-GYM-PK-RK-003"
    mutations = (
        ("evidence", ("privacyDisposition", "evidenceContractId"), "CE-WRONG"),
        ("phase", ("phaseIds",), ["guided-practice"]),
        ("path", ("pathAvailability",), [self.VARIANT_ID]),
        ("integration", ("integrationContractIds",), [self.INTEGRATION_ID]),
        ("sequence", ("sequenceEvidenceId",), "SE-WRONG"),
        ("minutes", ("additionalMinutes",), 15),
    )
    for label, path, value in mutations:
        with self.subTest(label=label):
            review = self.review(competency_id, "unresolved")
            review["privacyDisposition"] = self.private_disposition(
                competency_id,
                "none",
            )
            target = review
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            with self.assertRaises(IUM10ValidationError):
                self.validate_reviews(
                    [review],
                    privacy_contracts=self.core07_privacy_contracts(),
                )
```

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests
```

Expected: neue Tests RED; bisherige Tests bleiben entweder grün oder scheitern nur an der bewusst erweiterten Feldlogik.

- [ ] **Step 5: Handoff-Grundvertrag erweitern**

Ergänze in `validate_time_reviews()` die bestehende Handoff-Prüfung:

```python
cause_class = handoff.get("causeClass")
evidence_contract_id = handoff.get("evidenceContractId")
_require(
    isinstance(cause_class, str) and cause_class.strip(),
    f"time handoff causeClass missing: {competency_id}",
)
_require(
    evidence_contract_id is None
    or (
        isinstance(evidence_contract_id, str)
        and evidence_contract_id.strip()
    ),
    f"invalid time handoff evidenceContractId: {competency_id}",
)
```

Die Baseline-Fingerprintfunktion bleibt unverändert.

- [ ] **Step 6: Dynamische Reviewfelder und Dispositionshelper implementieren**

Definiere:

```python
TIME_REVIEW_FIELDS = {
    "id",
    "competencyId",
    "moduleId",
    "sourceTimeImpactLevel",
    "decision",
    "rationale",
    "phaseIds",
    "additionalMinutes",
    "integrationContractIds",
    "sequenceEvidenceId",
    "pathAvailability",
    "coverageConsequence",
    "risk",
    "followUp",
    "status",
}
PRIVACY_DISPOSITION_FIELDS = {
    "contractId",
    "observableBasis",
    "evidenceContractId",
    "privateArtifactContribution",
    "privateActivityTimeTreatment",
}
PRIVATE_ARTIFACT_CONTRIBUTION_FIELDS = {
    "product",
    "evidence",
    "additionalTimeClaim",
}
OBSERVABLE_BASES = {
    "nonpersonal-follow-up",
    "nonpersonal-module-detail",
    "none",
}
```

Ergänze einen privaten Helper:

```python
def _validate_privacy_disposition(
    review,
    handoff,
    privacy_contracts_by_id,
    privacy_contract_by_module_id,
):
    competency_id = review["competencyId"]
    module_id = review["moduleId"]
    has_contract = module_id in privacy_contract_by_module_id
    cause_class = handoff["causeClass"]

    _require(
        cause_class != "private-local" or has_contract,
        f"private-local time review needs privacy contract: {competency_id}",
    )
    if not has_contract:
        _require(
            "privacyDisposition" not in review,
            f"orphan privacyDisposition: {competency_id}",
        )
        return

    _require(
        "privacyDisposition" in review,
        f"privacyDisposition missing: {competency_id}",
    )
    disposition = review["privacyDisposition"]
    _require(
        isinstance(disposition, dict)
        and set(disposition) == PRIVACY_DISPOSITION_FIELDS,
        f"privacyDisposition fields invalid: {competency_id}",
    )
    contract = privacy_contract_by_module_id[module_id]
    _require(
        disposition["contractId"] == contract["id"]
        and disposition["contractId"] in privacy_contracts_by_id,
        f"privacyDisposition contractId mismatch: {competency_id}",
    )
    basis = disposition["observableBasis"]
    _require(
        basis in OBSERVABLE_BASES,
        f"invalid observableBasis: {competency_id}",
    )
    expected_evidence_id = handoff["evidenceContractId"]
    _require(
        disposition["evidenceContractId"] == expected_evidence_id,
        f"privacyDisposition evidenceContractId mismatch: {competency_id}",
    )
    if basis == "nonpersonal-follow-up":
        _require(
            cause_class == "private-local" and expected_evidence_id is not None,
            f"invalid nonpersonal-follow-up observableBasis: {competency_id}",
        )
    elif basis == "nonpersonal-module-detail":
        _require(
            cause_class == "module-detail" and expected_evidence_id is not None,
            f"invalid nonpersonal-module-detail observableBasis: {competency_id}",
        )
    else:
        _require(
            expected_evidence_id is None
            and review["decision"] == "unresolved"
            and review["additionalMinutes"] == 0
            and review["phaseIds"] == []
            and review["pathAvailability"] == []
            and review["integrationContractIds"] == []
            and review["sequenceEvidenceId"] is None,
            f"none privacy basis must remain unresolved and unallocated: {competency_id}",
        )

    contribution = disposition["privateArtifactContribution"]
    _require(
        isinstance(contribution, dict)
        and set(contribution) == PRIVATE_ARTIFACT_CONTRIBUTION_FIELDS,
        f"privateArtifactContribution fields invalid: {competency_id}",
    )
    for field in sorted(PRIVATE_ARTIFACT_CONTRIBUTION_FIELDS):
        _require(
            contribution[field] == "excluded",
            f"{competency_id} private artifact {field} must be excluded",
        )
    _require(
        disposition["privateActivityTimeTreatment"] == "module-budget-only",
        f"privateActivityTimeTreatment must be module-budget-only: {competency_id}",
    )
```

Rufe den Helper nach der Grundvalidierung der Reviewfelder und der Entscheidung auf.

- [ ] **Step 7: Signatur und dynamischen Feldvertrag implementieren**

Ändere die Signatur exakt wie unter Interfaces. Normalisiere nur `None`:

```python
if privacy_contracts is None:
    privacy_contracts = {}
_require(
    isinstance(privacy_contracts, dict),
    "validated privacy contracts must be keyed by contract id",
)
privacy_contract_by_module_id = {
    contract["moduleId"]: contract
    for contract in privacy_contracts.values()
}
_require(
    len(privacy_contract_by_module_id) == len(privacy_contracts),
    "validated privacy contracts must use unique module ids",
)
```

Ersetze den statischen Reviewfeldvergleich. Zunächst sind ausschließlich der bisherige Feldsatz oder derselbe Feldsatz plus `privacyDisposition` strukturell zulässig; die moduleigene Pflicht beziehungsweise das Verbot entscheidet danach `_validate_privacy_disposition()`:

```python
_require(
    frozenset(review)
    in {
        frozenset(TIME_REVIEW_FIELDS),
        frozenset(TIME_REVIEW_FIELDS | {"privacyDisposition"}),
    },
    "time review fields differ from the IUM10 contract",
)
```

Rufe `_validate_privacy_disposition()` für jeden Review auf.

- [ ] **Step 8: GREEN und bestehende öffentliche Schnittstelle prüfen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
python -B -m unittest tests.test_validate_ium10
```

Expected: alle Tests `OK`; der bisherige sechste Positionsparameter `require_complete` funktioniert unverändert.

- [ ] **Step 9: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: validate IUM10 privacy dispositions"
```

---

### Task 3: CORE-07 auf Schema 2 und strukturierte Dispositionen migrieren

**Files:**
- Modify: `roadmap/time-model.json:1-20`
- Modify: `roadmap/time-model.json` – sieben Reviews mit `moduleId == "IUM-5-CORE-07"`
- Modify: `scripts/validate_ium10.py:787-866`
- Test: `tests/test_validate_ium10.py:1157-1215`
- Test: `tests/test_validate_ium10.py:2052-2248`

**Interfaces:**
- Consumes aus Task 1: `validate_privacy_contracts()`.
- Consumes aus Task 2: `validate_time_reviews(..., privacy_contracts=...)`.
- Produces: Repositoryartefakt Schema 2 mit einem Privacy-Vertrag und sieben Dispositionen.

- [ ] **Step 1: RED für Schema 2 und top-level Privacy-Vertrag schreiben**

Aktualisiere den Repositorytest:

```python
def test_repository_draft_has_schema_two_and_the_core07_privacy_contract(self):
    root = Path(__file__).resolve().parents[1]
    time_model = json.loads(
        (root / "roadmap/time-model.json").read_text(encoding="utf-8")
    )
    module_payload = json.loads(
        (root / "roadmap/module-candidates.json").read_text(encoding="utf-8")
    )

    validate_time_model_draft(time_model, module_payload)

    self.assertEqual(time_model["schemaVersion"], 2)
    self.assertIn("privacyContracts", time_model)
    self.assertEqual(
        [contract["id"] for contract in time_model["privacyContracts"]],
        ["PC-IUM-5-CORE-07"],
    )
```

Erweitere die erwartete top-level Feldmenge um `"privacyContracts"`.

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10CapacityModelTests.test_repository_draft_has_schema_two_and_the_core07_privacy_contract
```

Expected: RED, weil Repository und Validator noch Schema 1 verwenden.

- [ ] **Step 2: RED für die exakte 7er-Migrationsmatrix schreiben**

Füge in `IUM10TimeReviewTests` hinzu:

```python
def test_repository_core07_privacy_dispositions_match_the_audited_matrix(self):
    expected = {
        "BMB16-GYM-IK-MG-001": (
            "nonpersonal-follow-up",
            "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-001",
        ),
        "BMB16-GYM-IK-MG-002": (
            "nonpersonal-module-detail",
            "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-002",
        ),
        "BMB16-GYM-IK-MG-003": (
            "nonpersonal-follow-up",
            "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-003",
        ),
        "BMB16-GYM-PK-RK-001": (
            "nonpersonal-follow-up",
            "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-001",
        ),
        "BMB16-GYM-PK-RK-002": (
            "nonpersonal-follow-up",
            "CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-002",
        ),
        "BMB16-GYM-PK-RK-003": ("none", None),
        "LH26-E-DP-003": ("none", None),
    }
    reviews = [
        review
        for review in self.time_payload["timeReviews"]
        if review["moduleId"] == "IUM-5-CORE-07"
    ]
    self.assertEqual(len(reviews), 7)
    for review in reviews:
        with self.subTest(competency_id=review["competencyId"]):
            disposition = review["privacyDisposition"]
            self.assertEqual(disposition["contractId"], "PC-IUM-5-CORE-07")
            self.assertEqual(
                (
                    disposition["observableBasis"],
                    disposition["evidenceContractId"],
                ),
                expected[review["competencyId"]],
            )
            self.assertEqual(
                set(disposition["privateArtifactContribution"].values()),
                {"excluded"},
            )
            self.assertEqual(
                disposition["privateActivityTimeTreatment"],
                "module-budget-only",
            )
```

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests.test_repository_core07_privacy_dispositions_match_the_audited_matrix
```

Expected: RED mit fehlendem `privacyDisposition`.

- [ ] **Step 3: Repository-Validator auf Schema 2 umstellen**

Ändere:

```python
_require(
    isinstance(schema_version, int)
    and not isinstance(schema_version, bool)
    and schema_version == 2,
    "schema version must be the integer 2",
)
```

Nachdem `validated_module_contracts` erzeugt wurde:

```python
validate_privacy_contracts(
    time_model.get("privacyContracts"),
    validated_module_contracts,
)
```

Der bestehende Bool-Test bleibt erhalten und erwartet weiterhin `IUM10ValidationError`.

- [ ] **Step 4: `time-model.json` auf Schema 2 migrieren**

Setze:

```json
"schemaVersion": 2
```

Füge nach `annualVariants` und vor `timeReviews` ein:

```json
"privacyContracts": [
  {
    "id": "PC-IUM-5-CORE-07",
    "moduleId": "IUM-5-CORE-07",
    "scope": "private-local-reflection",
    "artifactOwner": "learner",
    "artifactCustody": "learner-controlled",
    "institutionalHandling": {
      "access": "prohibited",
      "observation": "prohibited",
      "collection": "prohibited",
      "transfer": "prohibited",
      "storage": "prohibited",
      "assessment": "prohibited"
    },
    "status": "working"
  }
]
```

- [ ] **Step 5: Sieben Dispositionen exakt nach Migrationsmatrix ergänzen**

Jeder CORE-07-Review erhält dieselbe Ausschlussstruktur:

```json
"privateArtifactContribution": {
  "product": "excluded",
  "evidence": "excluded",
  "additionalTimeClaim": "excluded"
},
"privateActivityTimeTreatment": "module-budget-only"
```

Setze `contractId`, `observableBasis` und `evidenceContractId` exakt nach Task-3-Step-2-Matrix. Ändere keine vorhandenen Reviewfelder.

- [ ] **Step 6: Repository-Reviewvalidation an den Privacy-Vertrag binden**

Im Test, der die tatsächlichen Repositoryreviews über `validate_time_reviews()` validiert, erzeuge:

```python
privacy_contracts = validate_privacy_contracts(
    self.time_payload["privacyContracts"],
    self.repository_module_contracts,
)
```

Übergib:

```python
privacy_contracts=privacy_contracts
```

Alle direkten Repositoryaufrufe von `validate_time_reviews()` erhalten dasselbe validierte Mapping. Handgebaute Nichtprivacy-Tests bleiben bei `None`.

- [ ] **Step 7: GREEN für Schema, Matrix und Repositoryvalidator**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10CapacityModelTests
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests
python -B -m unittest tests.test_validate_ium10
```

Expected: alle Tests `OK`.

- [ ] **Step 8: Dateninvarianz vor Commit prüfen**

Run:

```powershell
python -B -m scripts.validate_ium09
python -B scripts/validate_phase0.py
git diff -- roadmap/module-candidates.json roadmap/coverage-plan.json roadmap/coverage-remediation.json curriculum
```

Expected:

- beide Validatoren Exitcode 0;
- der Diff der ausgeschlossenen Datenpfade ist leer.

- [ ] **Step 9: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "data: migrate CORE07 privacy contracts"
```

---

### Task 4: Freitextparser durch strukturierte CORE-07-Repositorytests ersetzen

**Files:**
- Modify: `tests/test_validate_ium10.py:3164-3905`
- Modify: `tests/test_validate_ium10.py:4447-4794`
- Test: `tests/test_validate_ium10.py`

**Interfaces:**
- Consumes aus Task 3: Schema-2-Daten und validierte Dispositionen.
- Produces: fachlicher CORE-07-Audit ohne Privacy-Semantik aus Freitext.

- [ ] **Step 1: Bestehenden strukturierten Gate-Erfolg vor Parserentfernung dokumentieren**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests.test_repository_core07_privacy_dispositions_match_the_audited_matrix
```

Expected: beide Läufe `OK`. Notiere Befehle und Zählung im Task-14-Report.

- [ ] **Step 2: RED-Mutation zeigt strukturierte Ausschlusswirkung**

Füge einen Repositorymutationstest hinzu:

```python
def test_repository_core07_rejects_each_private_contribution_mutation(self):
    fields = ("product", "evidence", "additionalTimeClaim")
    for field in fields:
        with self.subTest(field=field):
            time_payload = copy.deepcopy(self.time_payload)
            review = next(
                review
                for review in time_payload["timeReviews"]
                if review["competencyId"] == "BMB16-GYM-IK-MG-001"
            )
            review["privacyDisposition"]["privateArtifactContribution"][field] = (
                "included"
            )
            privacy_contracts = validate_privacy_contracts(
                time_payload["privacyContracts"],
                self.repository_module_contracts,
            )
            with self.assertRaisesRegex(IUM10ValidationError, field):
                validate_time_reviews(
                    time_payload["timeReviews"],
                    self.remediation_payload,
                    self.repository_module_contracts,
                    self.repository_integration_contracts,
                    self.repository_annual_variants,
                    privacy_contracts=privacy_contracts,
                )
```

Führe den Test zunächst mit einer temporären lokalen Rückmutation aus, bei der der entsprechende Validatorcheck auskommentiert ist. Expected: drei Subtests FAIL. Stelle den Validatorcheck wieder her; der Test muss GREEN werden. Committe keine Rückmutation.

- [ ] **Step 3: Parserabhängige Aufrufe aus fachlichen CORE-07-Helpern entfernen**

Entferne ausschließlich Aufrufe von:

```python
self._assert_core07_no_affirmative_private_handling(...)
```

Erhalte:

- `mode == "private-local"`;
- `productVisibility == "private-local"`;
- exakte IUM09-`privacyBoundary`;
- vorhandenen `nonPersonalFollowUp`;
- semantische Traces für private Aktivität, Fallprodukt, Medienwirkung, Kriterienurteil und Unabhängigkeit;
- `nonpersonal`-Anforderung im Review;
- Produktphasengrenze;
- unresolved-Prüfungen.

- [ ] **Step 4: Parser und parserabhängige Tests vollständig entfernen**

Entferne:

```text
_assert_core07_no_affirmative_private_handling
_core07_*privacy*
_core07_*prohibit*
_core07_*forbidden*
_core07_*handling*
```

Entferne die Tests:

```text
test_core07_rejects_contradictory_private_handling
test_core07_repository_audit_rejects_positive_action_masked_by_later_negation
test_core07_repository_audit_rejects_action_under_negated_prohibition
test_core07_repository_audit_rejects_action_masked_by_ohne_unrelated_object
test_core07_rejects_affirmative_private_grammar_families
test_core07_accepts_explicitly_negated_private_handling
```

Entferne außerdem den ausschließlich von diesen Prose-Regressionen verwendeten Helper:

```text
_assert_core07_repository_rejects_follow_up_mutation
```

Erhalte Tests, die echte Repositorydaten, strukturierte Verträge oder fachliche Tracegruppen prüfen.

- [ ] **Step 5: Keine verwaisten Parsernamen nachweisen**

Run:

```powershell
rg -n "_core07_.*(privacy|prohibit|forbidden|handling)|_assert_core07_no_affirmative_private_handling|affirmative_private_grammar|negative_private_grammar" tests/test_validate_ium10.py
```

Expected: keine Treffer.

- [ ] **Step 6: Fachliche und strukturierte CORE-07-Suite ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests
python -B -m unittest tests.test_validate_ium10
```

Expected: alle Tests `OK`.

- [ ] **Step 7: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add tests/test_validate_ium10.py
git commit -m "test: replace CORE07 privacy prose parser"
```

---

### Task 5: Migration, Minutenbilanz und Parent-Task-14-Gates schließen

**Files:**
- Modify: `tests/test_validate_ium10.py`
- Modify: `.superpowers/sdd/2026-07-30-ium10-zeitmodell-modulroadmap-implementation/task-14-report.md`

**Interfaces:**
- Consumes: alle strukturierten Validatoren und Schema-2-Daten aus Tasks 1–4.
- Produces: unveränderte fachliche und zeitliche Endbilanz sowie vollständigen Handoff an den übergeordneten IUM10-Plan.

- [ ] **Step 1: RED für unveränderte Privacy- und Zeitbilanz schreiben**

Füge einen literal abgeleiteten Repositorytest hinzu:

```python
def test_repository_core07_privacy_migration_preserves_time_and_coverage_balance(self):
    reviews = [
        review
        for review in self.time_payload["timeReviews"]
        if review["moduleId"] == "IUM-5-CORE-07"
    ]
    self.assertEqual(len(reviews), 7)
    self.assertEqual(
        sum(
            review["additionalMinutes"]
            for review in reviews
            if review["additionalMinutes"] > 0
        ),
        65,
    )
    self.assertEqual(
        {
            review["competencyId"]
            for review in reviews
            if review["decision"] == "unresolved"
        },
        {"BMB16-GYM-PK-RK-003", "LH26-E-DP-003"},
    )
    self.assertEqual(
        {
            review["privacyDisposition"]["observableBasis"]
            for review in reviews
        },
        {
            "nonpersonal-follow-up",
            "nonpersonal-module-detail",
            "none",
        },
    )
    self.assertEqual(
        sum(
            review["privacyDisposition"]["observableBasis"]
            == "nonpersonal-follow-up"
            for review in reviews
        ),
        4,
    )
    self.assertEqual(
        sum(
            review["privacyDisposition"]["observableBasis"]
            == "nonpersonal-module-detail"
            for review in reviews
        ),
        1,
    )
    self.assertEqual(
        sum(
            review["privacyDisposition"]["observableBasis"] == "none"
            for review in reviews
        ),
        2,
    )
```

Vor Task-3-Datenmigration wäre dieser Test RED; auf dem aktuellen Task-4-Stand muss er GREEN sein. Dokumentiere beide historischen Belege aus den Taskreports, statt die Daten zurückzusetzen.

- [ ] **Step 2: Parent-Task-14-Report korrigieren**

Ersetze die missverständliche Summendarstellung durch zwei getrennte Zeilen:

```text
Nichtadditive Phasenclaims: 85 Minuten.
Positive Record-Minuten: 65 Minuten.
```

Dokumentiere:

- Modulvertrag `PC-IUM-5-CORE-07`;
- Dispositionsbilanz 4/1/2;
- parserfreie strukturierte Privacy-Garantie;
- unveränderte 4/5/6 UE;
- unveränderte unresolved Records;
- Commits aus Tasks 1–4.

- [ ] **Step 3: Vollständige frische Verifikation ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PrivacyContractTests
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests
python -B -m unittest tests.test_validate_ium10
python -B -m unittest discover -s tests -p "test_*.py"
python -B -m scripts.validate_ium10
python -B -m scripts.validate_ium09
python -B scripts/validate_phase0.py
git diff --check
```

Expected:

- alle Testläufe `OK`;
- alle drei Validatoren Exitcode 0;
- `git diff --check` ohne Ausgabe.

- [ ] **Step 4: Fingerprints, prior20, Scope und UTF-8 prüfen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10BaselineTests.test_repository_baseline_has_immutable_module_coverage_and_handoff_contracts
python -B -m unittest tests.test_validate_ium10.IUM10TimeReviewTests.test_repository_time_reviews_match_the_audited_decisions
git diff --name-only $implementationBase..HEAD
```

Expected tracked scope:

```text
roadmap/time-model.json
scripts/validate_ium10.py
tests/test_validate_ium10.py
```

Prüfe alle drei Dateien strikt als UTF-8 ohne BOM und ohne U+FFFD:

```powershell
$trackedText = @(
  'roadmap/time-model.json',
  'scripts/validate_ium10.py',
  'tests/test_validate_ium10.py'
)
foreach ($path in $trackedText) {
  $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $path))
  if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    throw "UTF-8 BOM found: $path"
  }
  $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
  $text = $utf8.GetString($bytes)
  if ($text.Contains([char]0xFFFD)) {
    throw "U+FFFD found: $path"
  }
}
```

Bestätige den prior20-Strukturhash:

```text
f4bc3b75f2d575ce24faf3dd6bc16ea9823eb7b44c37391744c0f14a47563908
```

- [ ] **Step 5: Testbilanz committen**

Wenn Step 1 einen neuen getrackten Test ergänzt hat:

```powershell
git fetch --prune
git pull --ff-only
git add tests/test_validate_ium10.py
git commit -m "test: lock CORE07 privacy migration balance"
```

Wenn der Test bereits unverändert in Task 3 integriert wurde, entfällt dieser Commit; dokumentiere im Report ausdrücklich `no tracked change`.

- [ ] **Step 6: Unabhängigen Gesamt-Review dieses Plans ausführen**

Der Controller:

1. erzeugt ein Reviewpaket vom im SDD-Ledger gespeicherten `$implementationBase` bis `HEAD`;
2. übergibt Spezifikation, diesen Plan, Taskreports und Reviewpaket an einen frischen Reviewer;
3. verlangt getrennte Urteile zu Spec-Compliance und Engineeringqualität;
4. behandelt offene Critical-/Important-Befunde nach dem SDD-Fixloop;
5. markiert den Parent-Task 14 erst nach sauberem Review als abgeschlossen.

## Finaler Handoff

Nach sauberem Gesamt-Review:

1. Parent-SDD-Ledger ergänzt:

```text
Task 14: architecture replacement authorized and complete (privacy contract schema 2; prose parser removed; review clean)
Task 14: complete (commits 2a9c80b..<head7>, review clean)
```

2. Parent-Plan markiert Task 14 `completed` und Task 15 `in_progress`.
3. Workspace-Task, Initiative, Kanban, Entwicklungshistorie und Session Summary werden aktualisiert.
4. Kein Push; Ausführung des ursprünglichen IUM10-Plans wird unmittelbar mit Task 15 fortgesetzt.
