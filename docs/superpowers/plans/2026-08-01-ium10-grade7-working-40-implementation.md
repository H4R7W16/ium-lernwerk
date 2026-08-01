# IUM10 Grade 7 Working 40 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das freigegebene Klasse-7-Design als Schema-3-Vertrag implementieren: `GRADE-7-WORKING-40` bleibt bis zu fünf bestandenen Gates und fünf abgeschlossenen nichtpersonalen Piloten `conditional / amber`, fällt bei jedem erforderlichen Gatefehler `unavailable / red` aus und bewahrt alle zehn Kernmodule in exakt 40 UE.

**Architecture:** `roadmap/time-model.json` bleibt die kanonische Quelle. `scripts/validate_ium10.py` erhält eine reine Zustandsableitung, einen jahrgangspfadbezogenen Verfügbarkeitsvalidator und typisierte Pilotaufträge. Jahresvarianten, Sequenzzeitbelege und Jahrgangsurteile verwenden dieselbe dreistufige Verfügbarkeitsachse. Das Modell trennt Vertragsreife, Verfügbarkeit, Zeitmachbarkeit, Sequenznachweis, Pilotstand und semantische Coverage; kein Status wird aus einem anderen stillschweigend abgeleitet. Markdown-Publikationen werden ausschließlich gegen das validierte JSON geprüft.

**Tech Stack:** JSON, Markdown, Python 3.11+ Standardbibliothek, `unittest`, Git und GitHub CLI.

## Global Constraints

- Maßgebliche Spezifikation ist `docs/superpowers/specs/2026-08-01-ium10-grade7-working-40-design.md`, am 1. August 2026 schriftlich freigegeben und in Commit `dd0e4c745e0ef34368d2c2ecc87bb06fceb9194b` veröffentlicht.
- Der Umfang endet beim Zeit-, Verfügbarkeits-, Pilot- und Publikationsvertrag. Keine Lernmodule, Plattform, Diagnostik, personenbezogene Datenerhebung, reale Pilotdaten, Niveaudifferenzierung oder Phase-1-Planung werden angelegt.
- Die zehn Klasse-7-Kernmodule und ihre Lernhandlungen, Produkte, Curriculumnachweise, Datenschutzgrenzen und historischen `lessonRange` bleiben erhalten.
- Die 40 UE verteilen sich exakt auf vier Cluster: `8 = 5 + 3`, `11 = 5 + 6`, `11 = 4 + 3 + 4` und `10 = 4 + 2 + 4`.
- Die 40 UE enthalten die fachlich erforderlichen Lern-, Übungs-, Rückmelde-, Revisions-, Sicherungs- und Transferhandlungen. Es gibt keinen zusätzlichen Jahrespuffer.
- Ein gescheiterter Cluster erhöht den Bedarf additiv um `+3`, `+2`, `+3` oder `+6` UE. Alle vier Fehlschläge ergeben 54 UE.
- `GRADE-7-ROBUST-DEMAND` mit 46 UE und `GRADE-7-HISTORICAL-MINIMUM` mit 54 UE bleiben `unavailable` und reine Referenzrechnungen.
- 38 UE werden ausschließlich als `comparisonBoundaryUnits` dokumentiert. Es entsteht weder eine 38-UE-Jahresvariante noch ein Modulbudgetpfad `38`.
- Flexible Vertiefungs-, Transfer- und Projektmodule bleiben erhalten, liegen außerhalb der 40 UE und dürfen weder Kernmodule noch gescheiterte Kernintegrationen ersetzen.
- Verboten bleiben Kernstreichung, Operatornennung statt Ausführung, Demonstration statt eigenständiger Anwendung, Hausaufgabenkompression, garantierte unbeaufsichtigte Selbstlernzeit und private Reflexion als Pilot-, Diagnose- oder Bewertungsdaten.
- `status`, `availabilityStatus`, `timeFeasibilityStatus`, `sequenceEvidenceStatus`, `pilotStatus` und `semanticCoverageStatus` bleiben unabhängige Achsen.
- Der Anfangszustand der Klasse 7 ist exakt `working / conditional / amber / covered / not-started / partial`.
- `available / green` ist nur bei fünf bestandenen Gates und fünf abgeschlossenen Klasse-7-Pilotaufträgen zulässig. Jeder erforderliche Gatefehler erzwingt `unavailable / red`.
- `reviewed` entsteht weder durch die Migration noch durch synthetische Tests. Es setzt später getrenntes Fach-, Engineering- und Auftraggebergate voraus.
- Die Klassen 5 und 6 werden inhaltlich nicht neu entschieden. Ihr bisheriges `available: true` wird nur zu `availabilityStatus: "available"` migriert; ihr `pilotStatus` bleibt `not-started`.
- Die 31 bestehenden Modul-Pilotaufträge bleiben erhalten. Hinzu kommen vier Integrationspiloten und ein Jahrespfadpilot; Gesamtzahl exakt 36.
- Pilotdaten bleiben aggregiert auf Modul-, Integrations- oder Jahrespfadebene. Namen, Kennungen, persönliche Telemetrie, individuelle Lernverläufe, Kompetenzprofile, private Reflexionsinhalte und Schülerprodukte als Zeitnachweis sind ausgeschlossen.
- Die `coverageDecision` der Sequenzrecords `LH26-E-PROG-003` und `LH26-E-PROG-004` bleibt `remain-partial`. Das Klasse-7-Sequenzurteil wird dennoch `covered`; die semantische Coverage bleibt bis zu einem späteren eigenen Audit `partial`.
- `roadmap/coverage-plan.json`, `roadmap/coverage-remediation.json` und `roadmap/module-candidates.json` werden nicht verändert.
- Die Baseline-Fingerprints bleiben unverändert:
  - Modulstruktur: `da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc`
  - IUM09-Coverageprojektion: `cb9e09fa755a15206054e87ad0d5a8784fead63ff59530da0088b34e11dd2974`
  - 60 Zeitübergaben: `423b94122b931f4585b75aa74074f71b2e80a2b8b02cc92b32bf74585128f9bd`
  - aktuelle Coverage: `f39df261d7fab3733deafe9c1f4da4d15ca2778440d6d38828a088614e835776`
- Sichtbarer deutscher Text verwendet valides UTF-8 mit Umlauten und `ß`. Technische IDs, Enums und Dateinamen bleiben ASCII-stabil.
- Vor jedem Task `git status --short --branch` prüfen. Vor jedem Commit und Push `git fetch --prune` sowie `git pull --ff-only` ausführen. Bei Fehlern nicht committen oder pushen.
- Jeder Task folgt Red–Green–Refactor: erst ein zielgenauer fehlschlagender Test, dann die minimale Code- beziehungsweise Datenänderung, dann fokussierte und vollständige Verifikation.
- Jeder Task endet in einem kleinen, absichtlich zusammengestellten Commit. Keine Force-Pushes und keine History-Rewrites.

---

## File Map

| Pfad | Aktion | Verantwortung |
|---|---|---|
| `scripts/validate_ium10.py` | Modify | Schema 3, Verfügbarkeitsvertrag, Zustandsableitung, typisierte Pilotaufträge, Referenz- und Publikationsgates |
| `tests/test_validate_ium10.py` | Modify | Unit-, Repository-, Mutations-, Privacy-, Publikations- und Regressionsprüfungen |
| `roadmap/time-model.json` | Modify | Kanonischer `GRADE-7-WORKING-40`-Pfad, Verfügbarkeitsvertrag, 36 Pilotaufträge und sechs Statusachsen |
| `roadmap/module-roadmap.md` | Modify | Menschenlesbare Schema-3-, Klasse-7-, Risiko-, Pilot- und Fallbackdarstellung |
| `README.md` | Modify | Projektstatus, Verfügbarkeitsgrenze und Validierungsbefehle |
| `docs/superpowers/plans/2026-08-01-ium10-grade7-working-40-implementation.md` | Track | Taskfortschritt über Checkboxen |
| `.superpowers/sdd/2026-08-01-ium10-grade7-working-40-implementation/` | Ignore/working | Ausführungsbriefs, Diffs und getrennte Reviewberichte; keine Produktquelle |

Nicht verändern:

```text
roadmap/module-candidates.json
roadmap/coverage-plan.json
roadmap/coverage-remediation.json
scripts/validate_ium09.py
tests/test_validate_ium09.py
scripts/validate_phase0.py
tests/test_validate_phase0.py
```

## Dependency Flow

```text
Task 1 reine Zustandsmaschine
└── Task 2 atomare Schema-3- und Working-40-Migration
    └── Task 3 Verfügbarkeitsvertrag und Cross-Object-Orchestrierung
        └── Task 4 typisierte 36 Pilotaufträge
            └── Task 5 Sequenz-/Coverage-Entkopplung und Referenzschluss
                └── Task 6 Privacy-, Fallback-, Flex- und Mutationsgates
                    └── Task 7 JSON-synchrone Publikation
                        ├── Task 8 unabhängiges Fachreview
                        └── Task 9 unabhängiges Engineeringreview, Gesamtverifikation und Handoff
```

## Verbindliche öffentliche Validator-Schnittstellen

`scripts/validate_ium10.py` ergänzt genau diese Funktionen:

```python
def derive_grade_7_operational_state(
    availability_contract,
    pilot_assignments,
):
    """Return availability, time-feasibility and pilot state for Grade 7."""


def validate_availability_contracts(
    availability_contracts,
    annual_variants,
    integration_contracts,
):
    """Return the exact Grade-7 availability contract keyed by id."""


def validate_pilot_assignments(
    pilot_assignments,
    module_contracts,
    integration_contracts,
    availability_contracts,
):
    """Return all typed, privacy-safe pilot assignments keyed by id."""
```

`validate_ium10(...)` gibt danach zusätzlich `availabilityContracts` und die typisierten `pilotAssignments` zurück. Alle bisherigen Rückgabeschlüssel bleiben erhalten.

## Verbindliches Schema 3

`roadmap/time-model.json` besitzt exakt diese Top-Level-Felder:

```json
{
  "schemaVersion": 3,
  "status": "working",
  "baseline": {},
  "unit": {},
  "capacityModel": {},
  "moduleContracts": [],
  "integrationContracts": [],
  "annualVariants": [],
  "availabilityContracts": [],
  "privacyContracts": [],
  "timeReviews": [],
  "sequenceEvidence": [],
  "gradeJudgements": [],
  "risks": [],
  "pilotAssignments": []
}
```

Jede Jahresvariante besitzt exakt:

```json
{
  "id": "GRADE-7-WORKING-40",
  "grade": 7,
  "kind": "working-target",
  "pathId": "working-40",
  "targetUnits": 40,
  "allocations": [],
  "integrationContractIds": [],
  "availabilityStatus": "conditional",
  "availabilityContractId": "AVAIL-GRADE-7-WORKING-40",
  "status": "working",
  "rationale": "Alle zehn Kernmodule bilden in vier fachlich gebundenen Clustern ein vollständiges 40-UE-Arbeitsziel.",
  "risk": "Die Verfügbarkeit hängt von vier unpilotierten Integrationen und dem vollständigen End-to-End-Pilot ab."
}
```

Die Listen im Formbeispiel werden im Produktmodell nicht leer gelassen. `allocations` enthält die zehn Kernmodule in verbindlicher Reihenfolge und `integrationContractIds` die vier Klasse-7-Cluster. Alle übrigen Jahresvarianten führen `availabilityContractId: null`.

Der einzige Verfügbarkeitsvertrag besitzt exakt:

```json
{
  "id": "AVAIL-GRADE-7-WORKING-40",
  "variantId": "GRADE-7-WORKING-40",
  "requiredCapacityUnits": 40,
  "comparisonBoundaryUnits": 38,
  "gates": {
    "capacity": {"status": "not-started", "requirement": "40 Unterrichtseinheiten à 45 Minuten sind real im schulischen Angebot einplanbar; erforderliche Lernzeit wird nicht in Hausaufgaben oder private Lernzeit verschoben."},
    "integration": {"status": "not-started", "requirement": "Alle vier Cluster besitzen ihr vollständiges Übergabeprodukt und bewahren die getrennten fachlichen Lernhandlungen."},
    "technical": {"status": "not-started", "requirement": "Der Pflichtpfad funktioniert ohne persönliche Konten oder zentrale Lernendendatenspeicherung und besitzt für kritische Schritte eine lokale datenschutzkonforme Rückfallebene."},
    "privacy": {"status": "not-started", "requirement": "Pilot- und Verfügbarkeitsnachweise enthalten keine personenbezogenen Lernverlaufsdaten, Profile, privaten Reflexionsinhalte oder persönliche Telemetrie."},
    "pilot": {"status": "not-started", "requirement": "Vier getrennte Clusterpiloten und danach der vollständige 40-UE-Jahrespfad sind mit nichtpersonalen Pilotaufträgen abgeschlossen."}
  },
  "fallbackDeltaUnitsByIntegrationContractId": {
    "INT-7-DATA-CODING": 3,
    "INT-7-PROGRAMMING": 2,
    "INT-7-NET-SECURITY": 3,
    "INT-7-DATA-MEDIA-SOCIETY": 6
  },
  "maximumFallbackUnits": 54,
  "forbiddenCompensations": [
    "core-module-removal",
    "required-learning-action-removal",
    "operator-mention-only",
    "demonstration-instead-of-independent-application",
    "homework-shift",
    "unsupervised-self-study-as-guaranteed-time",
    "private-reflection-as-evidence",
    "flexible-module-substitution",
    "comparison-boundary-as-grade-7-path"
  ],
  "failureMode": "fail-closed",
  "status": "working",
  "risk": "Fehlende, widersprüchliche oder gescheiterte Evidenz darf keinen positiven Verfügbarkeits- oder Zeitstatus erzeugen."
}
```

Jeder Pilotauftrag besitzt exakt:

```json
{
  "id": "PILOT-INT-7-DATA-CODING",
  "scopeType": "integration",
  "scopeIds": ["INT-7-DATA-CODING"],
  "contractIds": ["INT-7-DATA-CODING"],
  "aggregationLevel": "integration",
  "measures": [
    "plannedTeachingUnits",
    "actualTeachingUnits",
    "handoffProductPresent",
    "fallbackActivated",
    "aggregatedTechnicalStartupMinutes",
    "aggregatedSupportDemand",
    "requiredLearningPhasesCompleted",
    "gateOutcome"
  ],
  "personalData": "prohibited",
  "personalTelemetry": "prohibited",
  "privateReflectionEvidence": "prohibited",
  "excludedUses": [
    "grades",
    "competence-profiles",
    "individual-diagnostics",
    "learner-identifiers",
    "personal-learning-paths",
    "private-reflection-content",
    "student-products-as-time-evidence",
    "automated-personal-assessment"
  ],
  "status": "not-started",
  "fallback": "standalone-module-time"
}
```

Für `scopeType: "module"` gilt `aggregationLevel: "module"` und `fallback: "nonpersonal-module-replanning"`. Für `scopeType: "annual-variant"` gilt `scopeIds: ["GRADE-7-WORKING-40"]`, `contractIds: ["AVAIL-GRADE-7-WORKING-40"]`, `aggregationLevel: "annual-variant"` und `fallback: "nonpersonal-annual-replanning"`.

---

### Task 1: Reine Klasse-7-Zustandsmaschine testgetrieben ergänzen

**Files:**

- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

- [ ] **Step 1: Import und vier fehlschlagende Unit-Tests schreiben**

```python
class IUM10Grade7OperationalStateTests(unittest.TestCase):
    required_pilot_ids = {
        "PILOT-INT-7-DATA-CODING",
        "PILOT-INT-7-PROGRAMMING",
        "PILOT-INT-7-NET-SECURITY",
        "PILOT-INT-7-DATA-MEDIA-SOCIETY",
        "PILOT-GRADE-7-WORKING-40",
    }

    def contract(self, gate_status="not-started"):
        return {
            "gates": {
                gate_id: {"status": gate_status}
                for gate_id in (
                    "capacity", "integration", "technical", "privacy", "pilot"
                )
            }
        }

    def pilots(self, status="not-started"):
        return {
            pilot_id: {"id": pilot_id, "status": status}
            for pilot_id in self.required_pilot_ids
        }

    def test_initial_contract_is_conditional_amber_and_not_started(self):
        self.assertEqual(
            derive_grade_7_operational_state(self.contract(), self.pilots()),
            {
                "availabilityStatus": "conditional",
                "timeFeasibilityStatus": "amber",
                "pilotStatus": "not-started",
            },
        )

    def test_started_or_partly_completed_pilots_are_in_progress(self):
        pilots = self.pilots()
        pilots["PILOT-INT-7-DATA-CODING"]["status"] = "completed"
        self.assertEqual(
            derive_grade_7_operational_state(self.contract(), pilots)["pilotStatus"],
            "in-progress",
        )

    def test_all_passed_gates_and_pilots_are_available_and_green(self):
        self.assertEqual(
            derive_grade_7_operational_state(
                self.contract("passed"), self.pilots("completed")
            ),
            {
                "availabilityStatus": "available",
                "timeFeasibilityStatus": "green",
                "pilotStatus": "completed",
            },
        )

    def test_any_failed_gate_is_fail_closed_after_completed_pilots(self):
        contract = self.contract("passed")
        contract["gates"]["technical"]["status"] = "failed"
        self.assertEqual(
            derive_grade_7_operational_state(
                contract, self.pilots("completed")
            ),
            {
                "availabilityStatus": "unavailable",
                "timeFeasibilityStatus": "red",
                "pilotStatus": "completed",
            },
        )
```

- [ ] **Step 2: Den Red-Zustand nachweisen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7OperationalStateTests -v
```

Expected: ImportError oder vier Fehler, weil die Funktion noch nicht existiert.

- [ ] **Step 3: Minimale reine Ableitung implementieren**

```python
GRADE_7_REQUIRED_PILOT_IDS = frozenset(
    {
        "PILOT-INT-7-DATA-CODING",
        "PILOT-INT-7-PROGRAMMING",
        "PILOT-INT-7-NET-SECURITY",
        "PILOT-INT-7-DATA-MEDIA-SOCIETY",
        "PILOT-GRADE-7-WORKING-40",
    }
)


def derive_grade_7_operational_state(availability_contract, pilot_assignments):
    gate_statuses = {
        gate["status"] for gate in availability_contract["gates"].values()
    }
    required_pilots = [
        pilot_assignments[pilot_id]
        for pilot_id in GRADE_7_REQUIRED_PILOT_IDS
    ]
    pilot_statuses = {pilot["status"] for pilot in required_pilots}
    if pilot_statuses == {"not-started"}:
        pilot_status = "not-started"
    elif pilot_statuses == {"completed"}:
        pilot_status = "completed"
    else:
        pilot_status = "in-progress"

    if "failed" in gate_statuses:
        availability_status, time_status = "unavailable", "red"
    elif gate_statuses == {"passed"} and pilot_status == "completed":
        availability_status, time_status = "available", "green"
    else:
        availability_status, time_status = "conditional", "amber"

    return {
        "availabilityStatus": availability_status,
        "timeFeasibilityStatus": time_status,
        "pilotStatus": pilot_status,
    }
```

- [ ] **Step 4: Fokussierte und vollständige Tests ausführen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7OperationalStateTests -v
python -B -m unittest discover -s tests -p "test_*.py"
```

- [ ] **Step 5: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: derive grade 7 operational state"
```

---

### Task 2: Schema 3 und `GRADE-7-WORKING-40` atomar migrieren

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

- [ ] **Step 1: Repositorytests auf den freigegebenen Schema-3-Zustand umstellen**

Die bisherigen Tests für Schema 2, Boolean-Verfügbarkeit, `GRADE-7-OPTIMIZED-DEMAND` und das rote Klasse-7-Urteil nicht ersatzlos löschen, sondern in positive Schema-3- und negative Altformatprüfungen überführen:

```python
def test_repository_uses_schema_three_and_no_boolean_availability(self):
    self.assertEqual(self.time_model["schemaVersion"], 3)
    self.assertIn("availabilityContracts", self.time_model)
    self.assertTrue(
        all(
            variant["availabilityStatus"]
            in {"conditional", "available", "unavailable"}
            and "available" not in variant
            for variant in self.time_model["annualVariants"]
        )
    )
    self.assertTrue(
        all(
            "availabilityStatus" in item and "available" not in item
            for evidence in self.time_model["sequenceEvidence"]
            for item in evidence["timeEvidence"]
        )
    )


def test_repository_has_working_40_and_two_unavailable_references(self):
    variants = {
        variant["id"]: variant
        for variant in self.time_model["annualVariants"]
        if variant["grade"] == 7
    }
    self.assertEqual(
        set(variants),
        {
            "GRADE-7-WORKING-40",
            "GRADE-7-ROBUST-DEMAND",
            "GRADE-7-HISTORICAL-MINIMUM",
        },
    )
    self.assertEqual(
        (
            variants["GRADE-7-WORKING-40"]["kind"],
            variants["GRADE-7-WORKING-40"]["pathId"],
            variants["GRADE-7-WORKING-40"]["targetUnits"],
            variants["GRADE-7-WORKING-40"]["availabilityStatus"],
        ),
        ("working-target", "working-40", 40, "conditional"),
    )
    self.assertEqual(
        {
            variants["GRADE-7-ROBUST-DEMAND"]["availabilityStatus"],
            variants["GRADE-7-HISTORICAL-MINIMUM"]["availabilityStatus"],
        },
        {"unavailable"},
    )


def test_rejects_legacy_boolean_availability(self):
    payload = copy.deepcopy(self.time_model)
    variant = payload["annualVariants"][0]
    variant["available"] = True
    del variant["availabilityStatus"]
    with self.assertRaisesRegex(
        IUM10ValidationError,
        "annual variant fields differ",
    ):
        validate_ium10(
            payload,
            self.module_payload,
            self.coverage_payload,
            self.remediation_payload,
        )
```

Außerdem exakt testen:

```python
self.assertEqual(
    [
        allocation["units"]
        for allocation in variants["GRADE-7-WORKING-40"]["allocations"]
    ],
    [5, 3, 5, 6, 4, 3, 4, 4, 2, 4],
)
self.assertEqual(
    sum(
        allocation["units"]
        for allocation in variants["GRADE-7-WORKING-40"]["allocations"]
    ),
    40,
)
```

- [ ] **Step 2: Den Red-Zustand nachweisen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7RepositoryTests -v
python -B -m unittest tests.test_validate_ium10.IUM10AnnualVariantTests -v
```

Expected: Fehlschläge zu Schema 2, Alt-ID, `optimized` und `available`.

- [ ] **Step 3: Validator-Konstanten und Schemafelder migrieren**

```python
AVAILABILITY_STATUSES = {"conditional", "available", "unavailable"}
ANNUAL_PATH_IDS_BY_KIND = {
    "planning-path": {"baseline", "regular", "extended"},
    "working-target": {"working-40"},
    "demand-scenario": {"robust", "historical-minimum"},
}
CORE_PATH_ORDER = {
    5: ("baseline", "regular", "extended"),
    6: ("baseline", "regular", "targeted-extension"),
    7: ("working-40", "robust", "historical-minimum"),
}
GRADE_7_VARIANT_TARGETS = {
    "GRADE-7-WORKING-40": ("working-40", 40),
    "GRADE-7-ROBUST-DEMAND": ("robust", 46),
    "GRADE-7-HISTORICAL-MINIMUM": ("historical-minimum", 54),
}
```

`TIME_MODEL_FIELDS` erhält `availabilityContracts`. Die Schema-Prüfungen in `validate_time_model_draft` und `validate_ium10` verlangen den echten Integer `3`. `validate_annual_variants` ersetzt `available` durch `availabilityStatus` und ergänzt `availabilityContractId`:

```python
variant_fields = {
    "id",
    "grade",
    "kind",
    "pathId",
    "targetUnits",
    "allocations",
    "integrationContractIds",
    "availabilityStatus",
    "availabilityContractId",
    "status",
    "rationale",
    "risk",
}
```

`SEQUENCE_TIME_EVIDENCE_FIELDS` ersetzt ebenfalls `available` durch `availabilityStatus`. `_validate_grade_7_judgement` und `_validate_final_grade_judgements` ergänzen `availabilityStatus` als eigene Urteilsachse. Gleichzeitig wird der Klasse-7-Sequenzstatus auf `covered` gesetzt und nicht länger aus `coverageDecision == "remain-partial"` abgeleitet; nur `semanticCoverageStatus` folgt weiterhin dem Coverage-Ledger.

- [ ] **Step 4: Kanonisches JSON atomar migrieren**

In `roadmap/time-model.json`:

1. `schemaVersion` auf `3` setzen und `availabilityContracts` ergänzen.
2. In allen elf Jahresvarianten `available` entfernen, `availabilityStatus` und `availabilityContractId` ergänzen.
3. Klassen 5/6: `availabilityStatus: "available"` und `availabilityContractId: null`.
4. `GRADE-7-OPTIMIZED-DEMAND` vollständig in `GRADE-7-WORKING-40` umbenennen.
5. Den Klasse-7-Pfadschlüssel `optimized` in Modulbudgets, Integrationsverträgen, Allokationen, `timeReviews.pathAvailability`, Sequenzzeitbelegen und erklärenden JSON-Texten zu `working-40` migrieren.
6. `GRADE-7-WORKING-40` erhält `kind: "working-target"`, `availabilityStatus: "conditional"` und `availabilityContractId: "AVAIL-GRADE-7-WORKING-40"`.
7. Robust und historisch bleiben `kind: "demand-scenario"`, `availabilityStatus: "unavailable"` und `availabilityContractId: null`.
8. Alle `sequenceEvidence.timeEvidence` verwenden `availabilityStatus` statt `available`.
9. Jahrgangsurteile ergänzen `availabilityStatus`: Klasse 5/6 `available`, Klasse 7 `conditional`.
10. Klasse 7 erhält `timeFeasibilityStatus: "amber"` und `sequenceEvidenceStatus: "covered"`; `semanticCoverageStatus: "partial"` und `pilotStatus: "not-started"` bleiben.
11. Den oben vollständig definierten Verfügbarkeitsvertrag als einziges Listenelement eintragen.

Die Klasse-7-Entscheidungsoptionen werden exakt:

```python
GRADE_7_DECISION_OPTIONS = [
    "pilot-grade-7-clusters",
    "pilot-grade-7-end-to-end",
    "fall-back-on-failed-required-gate",
]
```

Das Risikorecord `RISK-IUM10-GRADE7-CAPACITY` erhält exakt:

```json
{
  "id": "RISK-IUM10-GRADE7-CAPACITY",
  "scope": "grade-7",
  "risk": "Das 40-UE-Arbeitsziel der Klasse 7 hängt von vier unpilotierten Integrationen, fünf verpflichtenden Verfügbarkeitsgates und einem End-to-End-Pilot ab.",
  "impact": "Vor vollständiger Pilotierung bleibt GRADE-7-WORKING-40 conditional und amber; ein gescheitertes erforderliches Gate macht den Pfad unavailable und red und aktiviert den ausgewiesenen Rückfallbedarf.",
  "mitigation": "Vier Clusterpiloten und den 40-UE-Jahrespfad ausschließlich nichtpersonal prüfen; bei Gatefehlern fail-closed auf 40 UE plus additive Clusterzuschläge zurückfallen, ohne Kernmodule, Lernhandlungen oder flexible Module umzudeuten.",
  "status": "working"
}
```

`APPROVED_RISK_REGISTER_SHA256` wird auf den für diese fünf sortierten Records kanonisch berechneten Wert gesetzt:

```python
APPROVED_RISK_REGISTER_SHA256 = (
    "cee9ab121ccde252b243a930bb76a07209909145b77d12864de60dd790846492"
)
```

- [ ] **Step 5: Altformat und verbotene 38-UE-Variante ausschließen**

```powershell
rg -n '"available"\s*:|GRADE-7-OPTIMIZED-DEMAND|"optimized"' roadmap/time-model.json scripts/validate_ium10.py
```

Expected: kein Treffer in Produktmodell oder Validator. Negative Regressionstests dürfen die Alt-ID und das Altformat ausschließlich als Mutationsinput enthalten. Danach einen Mutationstest ergänzen, der eine `GRADE-7-WORKING-38`-Variante anhängt und mit `IUM10ValidationError` abgewiesen wird.

- [ ] **Step 6: Fokussierte und vollständige Validierung**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10AnnualVariantTests -v
python -B -m unittest tests.test_validate_ium10.IUM10Grade7RepositoryTests -v
python -B -m unittest tests.test_validate_ium10.IUM10SequenceEvidenceTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
```

Expected: alle Prüfungen grün; elf Jahresvarianten bleiben elf.

- [ ] **Step 7: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: migrate grade 7 working 40 to schema 3"
```

---

### Task 3: Verfügbarkeitsvertrag exakt validieren und mit dem Zustandsmodell verdrahten

**Files:**

- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

- [ ] **Step 1: Positive und mutierte Vertragsfälle schreiben**

```python
def test_repository_has_exact_grade_7_availability_contract(self):
    contract = self.time_model["availabilityContracts"][0]
    self.assertEqual(contract["variantId"], "GRADE-7-WORKING-40")
    self.assertEqual(contract["requiredCapacityUnits"], 40)
    self.assertEqual(contract["comparisonBoundaryUnits"], 38)
    self.assertEqual(
        set(contract["gates"]),
        {"capacity", "integration", "technical", "privacy", "pilot"},
    )
    self.assertEqual(
        contract["fallbackDeltaUnitsByIntegrationContractId"],
        {
            "INT-7-DATA-CODING": 3,
            "INT-7-PROGRAMMING": 2,
            "INT-7-NET-SECURITY": 3,
            "INT-7-DATA-MEDIA-SOCIETY": 6,
        },
    )
    self.assertEqual(
        contract["requiredCapacityUnits"]
        + sum(contract["fallbackDeltaUnitsByIntegrationContractId"].values()),
        contract["maximumFallbackUnits"],
    )
```

Mutationen müssen mindestens abweisen:

- fehlendes oder zusätzliches Gate;
- Gate-Status außerhalb `not-started|passed|failed`;
- Boolean statt Integer für 40, 38, Zuschläge oder 54;
- `comparisonBoundaryUnits != 38`;
- falsche Cluster-ID oder falscher Zuschlag;
- `maximumFallbackUnits != 54`;
- fehlende verbotene Kompensation;
- `failureMode != "fail-closed"`;
- zweiter Verfügbarkeitsvertrag;
- Vertragsreferenz auf Robust, Historisch oder eine unbekannte Variante.

- [ ] **Step 2: Den Red-Zustand nachweisen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7AvailabilityContractTests -v
```

Expected: Fehler, weil `validate_availability_contracts` noch nicht existiert oder die Mutationen noch akzeptiert werden.

- [ ] **Step 3: Exakten Validator implementieren**

```python
AVAILABILITY_CONTRACT_FIELDS = {
    "id",
    "variantId",
    "requiredCapacityUnits",
    "comparisonBoundaryUnits",
    "gates",
    "fallbackDeltaUnitsByIntegrationContractId",
    "maximumFallbackUnits",
    "forbiddenCompensations",
    "failureMode",
    "status",
    "risk",
}
AVAILABILITY_GATE_FIELDS = {"status", "requirement"}
AVAILABILITY_GATE_STATUSES = {"not-started", "passed", "failed"}
GRADE_7_AVAILABILITY_GATE_IDS = {
    "capacity", "integration", "technical", "privacy", "pilot"
}
GRADE_7_FALLBACK_DELTAS = {
    "INT-7-DATA-CODING": 3,
    "INT-7-PROGRAMMING": 2,
    "INT-7-NET-SECURITY": 3,
    "INT-7-DATA-MEDIA-SOCIETY": 6,
}
```

`validate_availability_contracts(...)` verlangt genau einen Vertrag, prüft alle Feld- und Typgrenzen fail-closed, bindet die vier Integrations-IDs an `integration_contracts`, bindet `variantId` an `GRADE-7-WORKING-40` und bestätigt:

```python
contract["maximumFallbackUnits"] == (
    contract["requiredCapacityUnits"]
    + sum(contract["fallbackDeltaUnitsByIntegrationContractId"].values())
)
```

- [ ] **Step 4: Orchestrator-Reihenfolge verdrahten**

In `validate_ium10` gilt:

```python
annual_variants = validate_annual_variants(...)
availability_contracts = validate_availability_contracts(
    time_payload["availabilityContracts"],
    annual_variants,
    integration_contracts,
)
```

`_validate_grade_7_judgement` erhält `availability_contracts` als Argument. Es prüft, dass nur `GRADE-7-WORKING-40` den Vertrag referenziert und Robust/Historisch keine implizite Freigabe erhalten.

- [ ] **Step 5: Tests und CLI ausführen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7AvailabilityContractTests -v
python -B -m unittest tests.test_validate_ium10.IUM10Grade7RepositoryTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
```

- [ ] **Step 6: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: validate grade 7 availability contract"
```

---

### Task 4: 31 Modul-, vier Integrations- und einen Jahrespilot typisieren

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

- [ ] **Step 1: Failing Tests für 36 typisierte Privacy-safe-Aufträge schreiben**

```python
def test_repository_has_exactly_thirty_six_typed_pilot_assignments(self):
    pilots = self.time_model["pilotAssignments"]
    self.assertEqual(len(pilots), 36)
    self.assertEqual(
        Counter(pilot["scopeType"] for pilot in pilots),
        {"module": 31, "integration": 4, "annual-variant": 1},
    )
    self.assertEqual(
        Counter(pilot["aggregationLevel"] for pilot in pilots),
        {"module": 31, "integration": 4, "annual-variant": 1},
    )


def test_every_pilot_prohibits_personal_and_private_evidence(self):
    for pilot in self.time_model["pilotAssignments"]:
        self.assertEqual(pilot["personalData"], "prohibited")
        self.assertEqual(pilot["personalTelemetry"], "prohibited")
        self.assertEqual(pilot["privateReflectionEvidence"], "prohibited")
        self.assertIn(
            "student-products-as-time-evidence",
            pilot["excludedUses"],
        )
        self.assertEqual(pilot["status"], "not-started")
```

Mutationstests ersetzen nacheinander `personalData`, `personalTelemetry` oder `privateReflectionEvidence` durch `allowed`, entfernen einen Ausschluss, duplizieren einen Scope, vertauschen `scopeType`/`aggregationLevel` oder referenzieren einen falschen Vertrag. Jede Mutation muss an der öffentlichen `validate_ium10`-Grenze scheitern.

- [ ] **Step 2: Den Red-Zustand nachweisen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10FinalIntegrationTests.test_pilot_assignments_are_typed_aggregated_and_nonpersonal -v
```

Expected: Fehlschlag bei 31 statt 36 beziehungsweise altem Feldschema.

- [ ] **Step 3: Pilotvalidator auf das einheitliche Schema umstellen**

```python
PILOT_ASSIGNMENT_FIELDS = {
    "id",
    "scopeType",
    "scopeIds",
    "contractIds",
    "aggregationLevel",
    "measures",
    "personalData",
    "personalTelemetry",
    "privateReflectionEvidence",
    "excludedUses",
    "status",
    "fallback",
}
PILOT_SCOPE_TYPES = {"module", "integration", "annual-variant"}
PILOT_STATUSES = {"not-started", "in-progress", "completed"}
PILOT_MEASURES = [
    "plannedTeachingUnits",
    "actualTeachingUnits",
    "handoffProductPresent",
    "fallbackActivated",
    "aggregatedTechnicalStartupMinutes",
    "aggregatedSupportDemand",
    "requiredLearningPhasesCompleted",
    "gateOutcome",
]
PILOT_EXCLUDED_USES = [
    "grades",
    "competence-profiles",
    "individual-diagnostics",
    "learner-identifiers",
    "personal-learning-paths",
    "private-reflection-content",
    "student-products-as-time-evidence",
    "automated-personal-assessment",
]
```

`validate_pilot_assignments(...)` prüft:

- genau 36 eindeutige IDs;
- genau einen Auftrag für jeden der 31 Modulverträge;
- genau einen Auftrag für jede der vier Klasse-7-Integrationen;
- genau einen Auftrag für `GRADE-7-WORKING-40`;
- exakte Scope-/Contract-/Aggregation-/Fallback-Zuordnung;
- ausschließlich die acht zugelassenen Messgrößen in dieser Reihenfolge;
- drei `prohibited`-Privacyfelder;
- exakt die acht ausgeschlossenen Nutzungen;
- Status nur aus `PILOT_STATUSES`.

- [ ] **Step 4: JSON verlustfrei migrieren und fünf Aufträge ergänzen**

Die 31 bisherigen Modulaufträge behalten ID und Modulzuordnung:

```json
{
  "id": "PILOT-IUM-5-CORE-01",
  "scopeType": "module",
  "scopeIds": ["IUM-5-CORE-01"],
  "contractIds": ["TC-IUM-5-CORE-01"],
  "aggregationLevel": "module",
  "measures": [
    "plannedTeachingUnits",
    "actualTeachingUnits",
    "handoffProductPresent",
    "fallbackActivated",
    "aggregatedTechnicalStartupMinutes",
    "aggregatedSupportDemand",
    "requiredLearningPhasesCompleted",
    "gateOutcome"
  ],
  "personalData": "prohibited",
  "personalTelemetry": "prohibited",
  "privateReflectionEvidence": "prohibited",
  "excludedUses": [
    "grades",
    "competence-profiles",
    "individual-diagnostics",
    "learner-identifiers",
    "personal-learning-paths",
    "private-reflection-content",
    "student-products-as-time-evidence",
    "automated-personal-assessment"
  ],
  "status": "not-started",
  "fallback": "nonpersonal-module-replanning"
}
```

Zusätzlich exakt `PILOT-INT-7-DATA-CODING`, `PILOT-INT-7-PROGRAMMING`, `PILOT-INT-7-NET-SECURITY`, `PILOT-INT-7-DATA-MEDIA-SOCIETY` und `PILOT-GRADE-7-WORKING-40` anlegen.

`handoffProductPresent` speichert ausschließlich den aggregierten Ja/Nein-Befund zum vereinbarten Übergabeprodukt. Weder das Produkt selbst noch eine Zuordnung zu Lernenden wird gespeichert; der Befund darf allein keine positive Zeitmachbarkeit begründen.

- [ ] **Step 5: Zustandsableitung gegen validierte Piloten verdrahten**

```python
operational_state = derive_grade_7_operational_state(
    availability_contracts["AVAIL-GRADE-7-WORKING-40"],
    pilot_assignments,
)
```

`_validate_final_grade_judgements` verlangt für Klasse 7, dass `availabilityStatus`, `timeFeasibilityStatus` und `pilotStatus` exakt diesem Ergebnis entsprechen. Der `pilot`-Gate-Status `passed` ist nur zulässig, wenn alle fünf erforderlichen Aufträge `completed` sind.

- [ ] **Step 6: Tests und vollständige Suite ausführen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10FinalIntegrationTests -v
python -B -m unittest tests.test_validate_ium10.IUM10Grade7OperationalStateTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
```

- [ ] **Step 7: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: type privacy-safe pilot assignments"
```

---

### Task 5: Sequenznachweis und semantische Coverage sauber entkoppeln

**Files:**

- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

- [ ] **Step 1: Failing Tests für die sechs unabhängigen Achsen schreiben**

```python
def test_grade_7_initial_axes_match_the_approved_contract(self):
    judgement = next(
        item
        for item in self.time_model["gradeJudgements"]
        if item["grade"] == 7
    )
    variant = next(
        item
        for item in self.time_model["annualVariants"]
        if item["id"] == "GRADE-7-WORKING-40"
    )
    self.assertEqual(
        {
            "status": variant["status"],
            "availabilityStatus": judgement["availabilityStatus"],
            "timeFeasibilityStatus": judgement["timeFeasibilityStatus"],
            "sequenceEvidenceStatus": judgement["sequenceEvidenceStatus"],
            "pilotStatus": judgement["pilotStatus"],
            "semanticCoverageStatus": judgement["semanticCoverageStatus"],
        },
        {
            "status": "working",
            "availabilityStatus": "conditional",
            "timeFeasibilityStatus": "amber",
            "sequenceEvidenceStatus": "covered",
            "pilotStatus": "not-started",
            "semanticCoverageStatus": "partial",
        },
    )


def test_grade_7_sequence_is_covered_while_coverage_stays_partial(self):
    evidence = {
        item["competencyId"]: item
        for item in self.time_model["sequenceEvidence"]
    }
    for competency_id in {"LH26-E-PROG-003", "LH26-E-PROG-004"}:
        self.assertEqual(
            evidence[competency_id]["coverageDecision"],
            "remain-partial",
        )
        self.assertEqual(
            evidence[competency_id]["coverageConsequence"]["coverageStatus"],
            "partial",
        )
```

Mutationstests belegen zusätzlich:

- `semanticCoverageStatus: "covered"` scheitert, solange `GRADE-7-WORKING-40` nicht `available` ist und kein neuer Fachaudit vorliegt;
- `sequenceEvidenceStatus: "partial"` scheitert trotz vier vollständiger Sequenzverträge;
- ein Sequenzzeitbeleg mit von seiner Jahresvariante abweichendem `availabilityStatus` scheitert;
- ein Resttext, der `GRADE-7-WORKING-40` als verfügbar oder erprobt bezeichnet, scheitert.

- [ ] **Step 2: Red-Zustand nachweisen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10SequenceEvidenceTests -v
python -B -m unittest tests.test_validate_ium10.IUM10PublishedRoadmapTests.test_grade_judgements_match_current_coverage_and_sequence_evidence -v
```

- [ ] **Step 3: Sequenzstatus aus Vertragsvollständigkeit ableiten**

Der atomare Schema-3-Schritt muss bereits folgenden Vertrag hergestellt haben; dieser Task sichert ihn mit Mutationen gegen spätere Rückkopplung ab:

```python
expected_statuses = {5: "covered", 6: "covered", 7: "covered"}
```

In `_validate_final_grade_judgements` bleibt die Kopplung von `coverageDecision == "remain-partial"` an den Sequenzstatus entfernt. Der Code lautet:

```python
derived_sequence = {5: "covered", 6: "covered", 7: "covered"}
for evidence in sequence_evidence.values():
    for grade in evidence["grades"]:
        _require(
            evidence["fachAuditStatus"] == "passed",
            f"grade {grade} sequence evidence is not fach-audited",
        )
```

Die semantische Ableitung aus `coverage_payload` bleibt unverändert und ergibt für Klasse 7 weiterhin `partial`.

- [ ] **Step 4: Referenzvalidator auf `availabilityStatus` synchronisieren**

`validate_sequence_evidence` prüft jeden `timeEvidence`-Eintrag gegen die referenzierte Jahresvariante:

```python
_require(
    time_item["availabilityStatus"]
    == annual_variants[time_item["variantId"]]["availabilityStatus"],
    f"sequence time evidence availability differs: {competency_id}",
)
```

`validate_time_references` bindet `AVAIL-GRADE-7-WORKING-40`, die fünf neuen Pilot-IDs, die neue Jahresvarianten-ID und alle umbenannten `pathAvailability`-Referenzen. Es darf keine Referenz auf `GRADE-7-OPTIMIZED-DEMAND` geben.

- [ ] **Step 5: Regression für unveränderte Quellartefakte ergänzen**

```python
def test_schema_three_keeps_module_coverage_and_handoff_fingerprints(self):
    result = validate_ium10(
        self.time_model,
        self.module_payload,
        self.coverage_payload,
        self.remediation_payload,
    )
    self.assertEqual(
        result["baseline"]["moduleStructureSha256"],
        BASELINE_MODULE_STRUCTURE_SHA256,
    )
    self.assertEqual(
        result["baseline"]["coverageProjectionSha256"],
        BASELINE_COVERAGE_PROJECTION_SHA256,
    )
    self.assertEqual(
        result["baseline"]["timeHandoffSha256"],
        BASELINE_TIME_HANDOFF_SHA256,
    )
```

- [ ] **Step 6: Tests und Validatoren ausführen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10SequenceEvidenceTests -v
python -B -m unittest tests.test_validate_ium10.IUM10FinalIntegrationTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
```

- [ ] **Step 7: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "fix: separate grade 7 sequence and semantic status"
```

---

### Task 6: Privacy-, Fallback-, Flex- und Fail-closed-Grenzen mit Mutationen härten

**Files:**

- Modify: `tests/test_validate_ium10.py`
- Modify: `scripts/validate_ium10.py`

- [ ] **Step 1: Eine tabellengetriebene Mutationssuite schreiben**

Die Suite mutiert eine tiefe Kopie des vollständigen Repositorymodells und ruft die öffentliche `validate_ium10`-Grenze auf:

```python
def assert_public_validation_rejects(self, mutator, message):
    payload = copy.deepcopy(self.time_model)
    mutator(payload)
    with self.assertRaisesRegex(IUM10ValidationError, message):
        validate_ium10(
            payload,
            self.module_payload,
            self.coverage_payload,
            self.remediation_payload,
        )
```

Mindestens diese Mutationen sind einzeln verpflichtend:

| Mutation | Erwartete Ablehnung |
|---|---|
| eines der zehn Kernmodule aus `GRADE-7-WORKING-40.allocations` entfernen | vollständige Kernfolge |
| ein flexibles Modul in die 40 UE aufnehmen | Flex außerhalb Pflichtpfad |
| `targetUnits` auf 38 setzen | 38 ist keine Variante |
| `comparisonBoundaryUnits` auf 40 setzen | Vergleichsgrenze exakt 38 |
| einen Fallbackzuschlag auf 0 oder Boolean setzen | positive exakte Integer |
| `maximumFallbackUnits` auf 53 setzen | additive Summe 54 |
| eine Cluster-ID aus der Fallbacktabelle entfernen | vier exakte Cluster |
| `failureMode` auf `best-effort` setzen | fail-closed |
| `privateReflectionEvidence` auf `allowed` setzen | Privacy fail-closed |
| `student-products-as-time-evidence` entfernen | verbotene Nutzung |
| `personalTelemetry` auf `optional` setzen | persönliche Telemetrie verboten |
| Pilotgate `passed`, Piloten aber `not-started` | Pilotgate ohne Evidenz |
| alle Piloten `completed`, ein Gate `failed` und Urteil grün | Gatefehler bleibt red |
| robustes 46-UE-Modell auf `conditional` oder `available` setzen | Referenz bleibt unavailable |
| Working-40-`status` auf `reviewed` setzen | kein automatisches Review |

- [ ] **Step 2: Red-Zustand jeder Mutation einzeln beobachten**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7FailClosedMutationTests -v
```

Expected: neue Tests schlagen zunächst an mindestens einer noch offenen Validatorgrenze fehl.

- [ ] **Step 3: Nur nachgewiesene Lücken im Validator schließen**

Keine Freitextheuristik einführen. Strukturierte IDs, Enums, Mengen-, Summen-, Typ- und Referenzverträge tragen die Gates. Für verbotene Kompensationen wird die exakte Liste verglichen; für Privacy werden nur strukturierte Felder geprüft.

Die `available / green`-Grenze lautet:

```python
_require(
    (
        operational_state["availabilityStatus"],
        operational_state["timeFeasibilityStatus"],
    )
    == (
        grade_7_variant["availabilityStatus"],
        grade_7_judgement["timeFeasibilityStatus"],
    ),
    "grade 7 operational state differs from gates and pilots",
)
```

Die Startdaten bleiben `conditional / amber`; synthetische Mutationen dürfen die produktiven JSON-Statuswerte nicht hochstufen.

- [ ] **Step 4: Vollständige Regression und statische Scans**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10Grade7FailClosedMutationTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
rg -n "TODO|TBD|FIXME|PLACEHOLDER" scripts/validate_ium10.py tests/test_validate_ium10.py roadmap/time-model.json
rg -n '"available"\s*:|GRADE-7-OPTIMIZED-DEMAND|"optimized"' roadmap/time-model.json scripts/validate_ium10.py
git diff --check
```

Expected: alle Tests/Validatoren grün; beide `rg`-Scans ohne Treffer; Diff-Gate grün.

- [ ] **Step 5: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "test: harden grade 7 fail closed boundaries"
```

---

### Task 7: Roadmap und README synchron aus Schema 3 publizieren

**Files:**

- Modify: `roadmap/module-roadmap.md`
- Modify: `README.md`
- Modify: `tests/test_validate_ium10.py`

- [ ] **Step 1: Failing Publikationstests schreiben**

Die bisherigen elf Varianten bleiben elf. Der veröffentlichte Klasse-7-Ausschnitt muss getrennte Zeilen enthalten:

```text
GRADE-7-WORKING-40 | working-target | working-40 | 40 | conditional
GRADE-7-ROBUST-DEMAND | demand-scenario | robust | 46 | unavailable
GRADE-7-HISTORICAL-MINIMUM | demand-scenario | historical-minimum | 54 | unavailable
```

Tests prüfen zusätzlich:

```python
self.assertIn(
    "working / conditional / amber / covered / not-started / partial",
    roadmap,
)
self.assertIn("38 UE", roadmap)
self.assertIn("nichtnormative Vergleichsgrenze", roadmap)
self.assertIn("31 Modulaufträge", roadmap)
self.assertIn("vier Integrationsaufträge", roadmap)
self.assertIn("ein Jahrespfadauftrag", roadmap)
self.assertIn(
    "Flexible Vertiefungs-, Transfer- und Projektmodule",
    roadmap,
)
self.assertNotIn("Klasse 7 ist verfügbar", roadmap)
self.assertNotIn("40 UE sind erprobt", roadmap)
```

README-Tests verlangen `conditional` und `amber` für Klasse 7 und verbieten eine Aussage, die `working` mit `available` gleichsetzt.

- [ ] **Step 2: Red-Zustand nachweisen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PublishedRoadmapTests -v
```

Expected: alte 40/46/54-unavailable-/red-Texte, 31er-Pilottabelle und Alt-ID führen zu Fehlern.

- [ ] **Step 3: `roadmap/module-roadmap.md` aktualisieren**

Mindestens diese Abschnitte synchronisieren:

- Modellstatus und Schema-Version;
- Jahresvariantentabelle mit `availabilityStatus`;
- Klasse-7-Kernfolge und vier Cluster;
- Verfügbarkeitsvertrag mit fünf Gates;
- additives Fallbackmodell `40 + 3 + 2 + 3 + 6 = 54`;
- 38 UE als nichtnormative Vergleichsgrenze ohne Variante;
- flexible Module ausdrücklich zusätzlich außerhalb der 40 UE;
- getrennte sechs Statusachsen;
- Risiko `RISK-IUM10-GRADE7-CAPACITY`;
- Pilotstatus mit 31/4/1 und drei Aggregationsebenen;
- Datenschutzgrenze ohne private Reflexion, Telemetrie oder Schülerprodukte als Zeitnachweis;
- Reviewgrenze: kein `reviewed` und keine Zeitfreigabe.

Alte Formulierungen, wonach alle drei Klasse-7-Szenarien unavailable/red seien, werden durch die genaue Dreiteilung conditional/amber versus unavailable ersetzt. Robust und Historisch dürfen nicht als Ersatzangebot erscheinen.

- [ ] **Step 4: `README.md` aktualisieren**

Der Kurzstatus nennt:

```text
Klasse 5: available / green / covered / not-started / partial
Klasse 6: available / green / covered / not-started / covered
Klasse 7: conditional / amber / covered / not-started / partial
```

Dabei die Achsen im Text ausschreiben, damit die Reihenfolge nicht missverständlich wird. Auf `roadmap/time-model.json` als kanonische Quelle und `roadmap/module-roadmap.md` als abgeleitete Lesefassung verweisen.

- [ ] **Step 5: Altbezeichnungen und Behauptungen scannen**

```powershell
rg -n 'GRADE-7-OPTIMIZED-DEMAND|"optimized"|Klasse 7 ist verfügbar|40 UE sind erprobt' roadmap/module-roadmap.md README.md
```

Expected: kein Treffer.

- [ ] **Step 6: Publikations- und Gesamttests ausführen**

```powershell
python -B -m unittest tests.test_validate_ium10.IUM10PublishedRoadmapTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
python -B scripts/validate_phase0.py
git diff --check
```

- [ ] **Step 7: Synchronisieren und committen**

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/module-roadmap.md README.md tests/test_validate_ium10.py
git commit -m "docs: publish grade 7 conditional working path"
```

---

### Task 8: Unabhängiges Fachreview gegen die freigegebene Spezifikation

**Files:**

- Review: `docs/superpowers/specs/2026-08-01-ium10-grade7-working-40-design.md`
- Review: `roadmap/time-model.json`
- Review: `roadmap/module-roadmap.md`
- Review: `README.md`
- Modify bei Befund: `tests/test_validate_ium10.py` und kleinster betroffener Produktpfad

- [ ] **Step 1: Reviewbasis unveränderlich festhalten**

```powershell
git status --short --branch
git rev-parse HEAD
git diff dd0e4c745e0ef34368d2c2ecc87bb06fceb9194b...HEAD -- roadmap/time-model.json roadmap/module-roadmap.md README.md
```

Base- und Head-Commit im Fachreviewbericht unter `.superpowers/sdd/2026-08-01-ium10-grade7-working-40-implementation/fachreview.md` notieren.

- [ ] **Step 2: Fachliche Prüffragen einzeln beantworten**

Der Review bestätigt oder beanstandet ausdrücklich:

1. alle zehn Kernmodule vorhanden und in der freigegebenen Reihenfolge;
2. Clustersummen 8/11/11/10 und Jahressumme 40;
3. alle notwendigen Lernhandlungen, Produkte und Curriculumnachweise erhalten;
4. vier Übergabeprodukte fachlich belastbar und nicht bloß thematisch gekoppelt;
5. Fallbackzuschläge +3/+2/+3/+6 fachlich korrekt und additiv;
6. 46/54 nur Referenz, 38 nur nichtnormativer Vergleich;
7. flexible Module vollständig erhalten und außerhalb der Pflichtzeit;
8. semantische Coverage `partial` und Sequenzvertrag `covered` widerspruchsfrei erklärt;
9. kein privater Inhalt, keine persönliche Diagnostik und kein Schülerprodukt als Zeitnachweis;
10. keine Publikationsaussage behauptet Pilotierung, Verfügbarkeit oder `reviewed`.

- [ ] **Step 3: Jeden Befund testgetrieben bearbeiten**

Bei jedem Befund zuerst einen fehlschlagenden Test ergänzen, dann die kleinste Korrektur vornehmen und den fokussierten Test erneut ausführen. Keine Änderung ohne reproduzierbaren Vertragstest.

- [ ] **Step 4: Fachreview abschließen**

Akzeptiert wird nur `APPROVED` oder `APPROVED AFTER FIXES` ohne offenen Critical-, Important- oder Minor-Befund. Bei verbleibendem fachlichem Dissens stoppt die Umsetzung vor Task 9.

- [ ] **Step 5: Gegebenenfalls Fixcommit erstellen**

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json roadmap/module-roadmap.md README.md tests/test_validate_ium10.py
git commit -m "fix: address grade 7 fachreview"
```

Wenn keine Änderungen nötig waren, keinen leeren Commit erzeugen.

---

### Task 9: Unabhängiges Engineeringreview, Gesamtverifikation und Nutzerhandoff

**Files:**

- Review: `scripts/validate_ium10.py`
- Review: `tests/test_validate_ium10.py`
- Review: `roadmap/time-model.json`
- Review: `roadmap/module-roadmap.md`
- Review: `README.md`
- Modify bei Befund: kleinster betroffener Test- und Produktpfad
- Track: `docs/superpowers/plans/2026-08-01-ium10-grade7-working-40-implementation.md`

- [ ] **Step 1: Engineeringreview auf dem Fachreview-Head starten**

Der Bericht unter `.superpowers/sdd/2026-08-01-ium10-grade7-working-40-implementation/engineeringreview.md` prüft:

- exakte Feldmengen und strikte Integer-vs-Boolean-Typen;
- eindeutige IDs und geschlossene Referenzen;
- keine Alt-ID und kein `optimized`-Pfad in Produkt-, Validator- oder Publikationsdateien; Testliterale sind nur in ausdrücklich negativen Regressionstests zulässig;
- reine deterministische Zustandsableitung;
- Gatefehler dominiert jeden positiven Pilotzustand;
- Pilotgate kann ohne fünf abgeschlossene Pilotaufträge nicht bestehen;
- keine Freitextheuristik als Privacy- oder Verfügbarkeitsgate;
- keine Schwächung der 31 Modul-, 60 Review-, vier Sequenz-, fünf Risiko- oder Baseline-Invarianten;
- Mutationstests erreichen die öffentliche `validate_ium10`-Grenze;
- Dokumentation wird aus JSON-Fakten geprüft und nicht über selbstreferenzielle Konstanten;
- keine Änderungen außerhalb der File Map.

- [ ] **Step 2: Befunde testgetrieben schließen**

Für jeden Befund zuerst den kleinsten fehlschlagenden Test schreiben, den Fehler reproduzieren, minimal beheben und fokussiert erneut testen. Nach Fixes ein unabhängiges Re-Review desselben Diffs verlangen.

- [ ] **Step 3: Vollständige maschinelle Verifikation ausführen**

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
rg -n "TODO|TBD|FIXME|PLACEHOLDER" scripts/validate_ium10.py tests/test_validate_ium10.py roadmap/time-model.json roadmap/module-roadmap.md README.md
rg -n '"available"\s*:|GRADE-7-OPTIMIZED-DEMAND|"optimized"' roadmap/time-model.json scripts/validate_ium10.py roadmap/module-roadmap.md README.md
git diff --check
git status --short --branch
```

Expected:

- vollständige Testsuite grün;
- drei Validatoren grün;
- beide `rg`-Scans ohne Treffer;
- `git diff --check` ohne Ausgabe;
- nur beabsichtigte Dateien geändert.

- [ ] **Step 4: UTF-8, JSON und Python-Syntax prüfen**

```powershell
python -B -c "import ast,json,pathlib; files=['scripts/validate_ium10.py','tests/test_validate_ium10.py']; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8')) for f in files]; json.loads(pathlib.Path('roadmap/time-model.json').read_text(encoding='utf-8')); print('UTF8_JSON_AST=PASS')"
```

Zusätzlich alle fünf geänderten Produktdateien auf `U+FFFD` prüfen. Expected: kein Ersatzzeichen.

- [ ] **Step 5: Plan abhaken und finalen Fixcommit erstellen**

Nur tatsächlich erledigte Checkboxen auf `[x]` setzen. Falls Task 9 Änderungen enthält:

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py roadmap/time-model.json roadmap/module-roadmap.md README.md docs/superpowers/plans/2026-08-01-ium10-grade7-working-40-implementation.md
git commit -m "test: finalize grade 7 working 40 contract"
```

Wenn nur der Planstatus geändert wurde:

```powershell
git fetch --prune
git pull --ff-only
git add docs/superpowers/plans/2026-08-01-ium10-grade7-working-40-implementation.md
git commit -m "docs: complete grade 7 working 40 plan"
```

- [ ] **Step 6: Push und Draft-PR aktualisieren**

```powershell
git push origin feat/ium-phase0
gh pr edit 1 --repo H4R7W16/ium-lernwerk --body-file .superpowers/sdd/2026-08-01-ium10-grade7-working-40-implementation/pr-body.md
gh pr view 1 --repo H4R7W16/ium-lernwerk --json url,isDraft,headRefName,headRefOid
```

Der PR-Text nennt Schema 3, `GRADE-7-WORKING-40`, `conditional / amber / covered / not-started / partial`, 36 nichtpersonale Pilotaufträge, fail-closed-Fallback, unveränderte Baseline-Fingerprints, tatsächliche Testzahl und beide Reviewurteile.

- [ ] **Step 7: Remote-Synchronität beweisen**

```powershell
git fetch --prune
git rev-parse HEAD
git rev-parse origin/feat/ium-phase0
gh pr view 1 --repo H4R7W16/ium-lernwerk --json headRefOid,url,isDraft
git status --short --branch
```

Expected: lokaler Head, Remote-Head und PR-Head identisch; Branch sauber; PR bleibt Draft.

- [ ] **Step 8: Nutzerhandoff**

Berichten:

- Ergebnis und bewusst nicht implementierten Scope;
- finalen Commit-Hash, Branch, Push-Status und PR-Link;
- tatsächliche Testzahl und Validatorstatus;
- Fach- und Engineeringreview;
- exakten Anfangszustand der sechs Klasse-7-Achsen;
- dass `available / green` und `reviewed` weiterhin nicht freigegeben sind;
- dass reale Cluster- und Jahrespiloten noch ausstehen;
- dass Phase 1 weiterhin ungeplant bleibt.

Danach ein neues schriftliches Auftraggebergate einholen. Keine Pilotdaten oder Statushochsetzung antizipieren.

---

## Final Acceptance Checklist

- [ ] `schemaVersion == 3` und exakt ein `availabilityContract`.
- [ ] `GRADE-7-WORKING-40` umfasst alle zehn Kernmodule in 40 UE.
- [ ] Clustersummen `8/11/11/10` und Fallbackzuschläge `3/2/3/6` sind maschinengeprüft.
- [ ] 38 UE existieren nur als nichtnormative `comparisonBoundaryUnits`.
- [ ] Robust 46 und Historisch 54 bleiben `unavailable`.
- [ ] Flexible Vertiefungs-, Transfer- und Projektmodule bleiben zusätzlich erhalten.
- [ ] Anfangszustand Klasse 7 ist `working / conditional / amber / covered / not-started / partial`.
- [ ] Jedes erforderliche gescheiterte Gate erzeugt `unavailable / red`.
- [ ] `available / green` benötigt fünf bestandene Gates und fünf abgeschlossene Klasse-7-Pilotaufträge.
- [ ] Genau 36 typisierte Pilotaufträge liegen vor: 31 Modul, 4 Integration, 1 Jahrespfad.
- [ ] Pilotaufträge verbieten personenbezogene Daten, Telemetrie, private Reflexionsinhalte und Schülerprodukte als Zeitnachweis.
- [ ] `LH26-E-PROG-003` und `LH26-E-PROG-004` bleiben semantisch `remain-partial`.
- [ ] Klassen 5/6 sind nur von Boolean zu `availabilityStatus: available` migriert.
- [ ] Modulstruktur-, Coverage- und Zeitübergabe-Fingerprints bleiben unverändert.
- [ ] JSON, Validator, Tests, Roadmap und README sind referenziell synchron.
- [ ] Alt-ID, Altpfad und Boolean-Verfügbarkeitsfeld fehlen in allen Produktdateien.
- [ ] Getrenntes Fach- und Engineeringreview ohne offenen Befund.
- [ ] Vollständige Testsuite, IUM10, IUM09, Phase 0, UTF-8, JSON, AST und Diff-Gate grün.
- [ ] Branch, Remote und Draft-PR zeigen denselben finalen Commit.
- [ ] Kein reales Pilotdatum, keine Plattform, keine Diagnostik und keine Phase 1 implementiert.
