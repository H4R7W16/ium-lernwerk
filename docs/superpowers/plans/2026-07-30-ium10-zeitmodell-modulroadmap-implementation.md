# IUM10 Zeitmodell der Modulroadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das freigegebene IUM10-Design als maschinenprüfbares, fachlich begründetes Zeitmodell mit 31 Modulzeitverträgen, 60 recordgenauen Zeitreviews, expliziten Integrationsverträgen, konsistenten Jahresvarianten und vier Sequenznachweisen implementieren.

**Architecture:** `roadmap/time-model.json` wird die autoritative Quelle für Zeitannahmen, Modulbudgets, Integrationen und Jahresurteile. Ein neuer Standardbibliothek-Validator sichert die unveränderte IUM09-Baseline, prüft alle Zeit- und Referenzverträge und erzeugt bei zulässigen roadmapweiten Coverageänderungen eine historische IUM09-Projektion. `validate_phase0.py` bleibt der gemeinsame Einstieg und ruft Phase 0, IUM09 und IUM10 in einer fail-closed Kette auf. Semantische Coverage, zeitliche Durchführbarkeit, Sequenznachweis und Pilotstatus bleiben getrennte Statusdimensionen.

**Tech Stack:** JSON, Markdown, Python 3.11+ Standardbibliothek, `unittest`, Git.

## Global Constraints

- Maßgebliche Spezifikation ist `docs/superpowers/specs/2026-07-30-ium10-zeitmodell-modulroadmap-design.md`, erstmals als Commit `91915ebe474030deec10922f4fffbbc9a71f4052` veröffentlicht und am 30. Juli 2026 schriftlich durch den Nutzer freigegeben.
- Technische IUM10-Baseline ist Commit `e53bad7cffe1541fc910db948235908bebe89caa`.
- Der IUM09-Modulstrukturfingerprint bleibt `da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc`.
- Der rekonstruierte IUM09-Coveragefingerprint bleibt `cb9e09fa755a15206054e87ad0d5a8784fead63ff59530da0088b34e11dd2974`.
- Der Fingerprint der 60 IUM09-Zeitübergaben bleibt `423b94122b931f4585b75aa74074f71b2e80a2b8b02cc92b32bf74585128f9bd`.
- Die Baseline bleibt 31 Module, davon 24 `core` und 7 flexibel, 171 Curriculumrecords, 164 `covered`, 7 `partial`, 56 `review-required` und 4 `roadmap-dependent`.
- Modul-ID, Jahrgang, Modulart, Voraussetzungen, zentrale Lernhandlung, zentrales Lernprodukt, Datenschutzgrenze und historische `lessonRange` bleiben unverändert.
- Das Hybridmodell bleibt erhalten. Flexible Vertiefungs-, Transfer- und Projektmodule werden nicht zur verdeckten Voraussetzung der Kernabdeckung.
- Eine Unterrichtseinheit umfasst exakt 45 Minuten.
- `baseline`, `regular` und `extended` umfassen exakt 30, 34 und 38 UE. Sie sind `working`, keine amtliche Norm.
- Der Basispfad enthält bereits Aktivierung, Begriffs- oder Verfahrensaufbau, angeleitete Übung, eigenständige Handlung, Produktspur, Feedback oder Selbstkontrolle, Revision, Sicherung und Transfer beziehungsweise späteren Abruf.
- Kein erforderlicher Phasenbaustein eines Kernmoduls erhält null Minuten. Hausaufgaben, unbeaufsichtigte Selbstlernzeit oder idealisierte Technikzeit ersetzen keine Unterrichtszeit.
- Gemeinsam genutzte Zeit wird über genau einen `countedInModuleId` genau einmal gezählt. Scheitert eine Integration, gilt die eigenständige Zeit.
- Jeder der 60 Übergaberecords erhält genau einen Review. Es gibt keine Zielquote für `absorbed`, `integrated`, `additional-time` oder `unresolved`.
- Die vier Records `LH26-E-PROG-001` bis `LH26-E-PROG-004` erhalten zusätzlich genau einen Sequenznachweis und keinen fingierten Einzelmodulnachweis.
- Ein roadmapweiter Wechsel von `partial` zu `covered` setzt vollständigen Sequenznachweis, fachlich bestandenen Audit und mindestens eine tatsächlich verfügbare Jahresvariante voraus.
- `BMB16-GYM-IK-GM-003`, `BMB16-GYM-PK-RK-003` und `LH26-E-DP-003` bleiben ohne neuen semantischen Nachweis `partial`; Zeit allein schließt diese Lücken nicht.
- Klasse 5 muss rechnerisch 30/34/38 ergeben. Klasse 6 muss 30/34/38 ergeben. Klasse 7 bleibt mit 40/46/54 und `red` sichtbar.
- Ein rechnerisch grüner Pfad bleibt bis zur Pilotierung `working`. Pilotdaten werden nur aggregiert auf Modulebene und nie personenbezogen dokumentiert.
- Vor jedem Task `git status --short --branch` prüfen. Vor jedem Commit oder Push `git fetch --prune` und `git pull --ff-only` ausführen; bei Fehlern nicht committen oder pushen.
- Jeder Task endet mit einem kleinen, absichtlich zusammengestellten Commit. Daten eines Zeitreviews werden nicht auf mehrere Commits verteilt.
- Sichtbarer deutscher Text verwendet UTF-8-Umlaute und `ß`; technische IDs und Dateinamen bleiben ASCII-stabil.
- IUM10 umfasst keine Lernendenanwendung, keine Lernmodulimplementierung, keine Plattform, keine personenbezogene Diagnostik, keine Niveaudifferenzierung und keine Phase-1-Planung.

## File Map

| Pfad | Aktion | Verantwortung |
|---|---|---|
| `scripts/validate_ium10.py` | Create | Baseline-, Zeitvertrags-, Integrations-, Jahresvarianten-, Review-, Sequenz- und Referenzvalidator |
| `tests/test_validate_ium10.py` | Create | Unit-, Daten- und Repositorytests des vollständigen IUM10-Vertrags |
| `roadmap/time-model.json` | Create | Autoritatives Zeitmodell mit allen Verträgen, Varianten, Urteilen, Risiken und Pilotaufträgen |
| `roadmap/module-candidates.json` | Modify | 31 `timeContractId`-Referenzen und präzisierte Bedeutung von `lessonRange` |
| `roadmap/coverage-remediation.json` | Modify | 60 additive `timeReviewId`-Referenzen bei unveränderter IUM09-Begründung |
| `roadmap/coverage-plan.json` | Modify | 60 Zeitreview- und vier Sequenzreferenzen; Coverageänderung nur nach bestandenem Sequenzaudit |
| `roadmap/module-roadmap.md` | Modify | 30/34/38-Modell, Matrizen, Integrationen, 60/60-Bilanz und Klasse-7-Entscheidungsbedarf |
| `scripts/validate_ium09.py` | Modify | Additive IUM10-Referenz im historischen Ledger zulassen, ohne IUM09-Semantik zu ändern |
| `tests/test_validate_ium09.py` | Modify | Historische IUM09-Projektion bei zulässigen IUM10-Sequenzentscheidungen prüfen |
| `scripts/validate_phase0.py` | Modify | IUM10 in den gemeinsamen Repository-Einstieg integrieren |
| `tests/test_validate_phase0.py` | Modify | Dynamische Endbilanz und IUM10-Publikationskonsistenz prüfen |
| `README.md` | Modify | Autoritatives Zeitmodell, Validierung und Freigabegrenze dokumentieren |
| `docs/superpowers/plans/2026-07-30-ium10-zeitmodell-modulroadmap-implementation.md` | Track | Taskfortschritt über Checkboxen nachvollziehbar halten |

## Dependency Flow

```text
Task 1 Baseline- und Fingerprintvalidator
└── Task 2 Zeiteinheit und Kapazitätsmodell
    └── Task 3 Modulzeitvertragsschema
        ├── Task 4 Klasse-5-Verträge und Varianten
        ├── Tasks 5–6 Klasse-6-Verträge, Integrationen und Varianten
        └── Task 7 Klasse-7-Verträge, Cluster und Urteil
            └── Task 8 Zeitreviewschema
                └── Tasks 9–23 fünfzehn recordgenaue Modulaudits
                    └── Task 24 vier Sequenznachweise und Coverageentscheidungen
                        └── Task 25 Referenzen und Repository-Orchestrierung
                            └── Task 26 Publikation, Fachreview, Engineeringreview und Nutzerhandoff
```

## Verbindliche Validator-Schnittstellen

`scripts/validate_ium10.py` stellt genau diese öffentlichen Namen bereit:

```python
class IUM10ValidationError(ValueError):
    pass


def coverage_projection_fingerprint(coverage_payload, remediation_payload):
    """Return the canonical IUM09 semantic projection fingerprint."""


def time_handoff_fingerprint(remediation_payload):
    """Return the canonical SHA-256 fingerprint of all 60 IUM09 handoffs."""


def validate_ium10_baseline(
    module_payload,
    coverage_payload,
    remediation_payload,
):
    """Return immutable module, coverage and handoff baseline facts."""


def validate_capacity_model(capacity_model, unit_contract):
    """Return planning paths keyed by path id."""


def validate_module_contracts(module_contracts, module_payload):
    """Return module time contracts keyed by module id."""


def validate_integration_contracts(
    integration_contracts,
    module_contracts,
):
    """Return integration contracts keyed by contract id."""


def validate_annual_variants(
    annual_variants,
    module_contracts,
    integration_contracts,
):
    """Return annual variants keyed by variant id."""


def validate_time_reviews(
    time_reviews,
    remediation_payload,
    module_contracts,
    integration_contracts,
    annual_variants,
    *,
    require_complete,
):
    """Return time reviews keyed by competency id."""


def validate_sequence_evidence(
    sequence_evidence,
    time_reviews,
    annual_variants,
    coverage_payload,
):
    """Return sequence evidence keyed by competency id."""


def ium09_coverage_projection(
    coverage_payload,
    remediation_payload,
    sequence_evidence,
):
    """Return a deep-copied coverage payload restored to IUM09 after-status."""


def validate_time_references(
    module_payload,
    coverage_payload,
    remediation_payload,
    validated_time_model,
):
    """Validate all cross-artifact IUM10 references."""


def validate_ium10(
    time_payload,
    module_payload,
    coverage_payload,
    remediation_payload,
):
    """Validate the complete IUM10 chain and return indexed contracts."""
```

Die Rückgabe von `validate_ium10` lautet:

```python
{
    "moduleContracts": module_contracts,
    "integrationContracts": integration_contracts,
    "annualVariants": annual_variants,
    "timeReviews": time_reviews,
    "sequenceEvidence": sequence_evidence,
    "gradeJudgements": grade_judgements,
    "ium09CoverageProjection": ium09_projection,
}
```

Formbeispiele in diesem Abschnitt zeigen ausschließlich die exakte Feldstruktur. Leere Listen und Strings aus den Formbeispielen dürfen nicht in das produktive `time-model.json` übernommen werden; die Datentasks ersetzen sie durch die jeweils ausdrücklich geprüften Inhalte.

## Verbindliches Datenmodell

`roadmap/time-model.json` besitzt exakt diese Top-Level-Felder:

```json
{
  "schemaVersion": 1,
  "status": "working",
  "baseline": {},
  "unit": {},
  "capacityModel": {},
  "moduleContracts": [],
  "integrationContracts": [],
  "annualVariants": [],
  "timeReviews": [],
  "sequenceEvidence": [],
  "gradeJudgements": [],
  "risks": [],
  "pilotAssignments": []
}
```

Ein Modulzeitvertrag besitzt exakt:

```json
{
  "id": "TC-IUM-5-CORE-01",
  "moduleId": "IUM-5-CORE-01",
  "grade": 5,
  "kind": "core",
  "historicalLessonRange": {"min": 5, "max": 7},
  "competencyIds": [],
  "centralLearningAction": "",
  "centralLearningProduct": "",
  "prerequisiteModuleIds": [],
  "revisitModuleIds": [],
  "pathBudgets": [],
  "standaloneUnitRange": null,
  "timeReviewIds": [],
  "integrationContractIds": [],
  "schoolDependentSteps": [],
  "risk": "",
  "pilotRequired": true,
  "status": "working"
}
```

Jedes `pathBudgets`-Element besitzt exakt:

```json
{
  "pathId": "baseline",
  "units": 5,
  "minutes": 225,
  "directMinutes": 180,
  "countedSharedMinutes": 45,
  "phaseBudgets": [
    {
      "phaseId": "orientation-challenge",
      "minutes": 15,
      "learningFunction": "Ziel, Problem und erwartete Produktspur klären."
    }
  ],
  "sharedAllocations": [
    {
      "integrationContractId": "INT-5-RESEARCH-PRODUCTION",
      "minutes": 45
    }
  ]
}
```

Für Kernmodule enthält `phaseBudgets` alle sieben freigegebenen Phasen genau einmal und mit positiver Minutenzahl. Bei flexiblen Modulen entspricht die Phasenmenge exakt der vorhandenen `moduleGrammar`. Es gilt immer:

```text
minutes = units × 45
minutes = directMinutes + countedSharedMinutes
minutes = Summe phaseBudgets.minutes
countedSharedMinutes = Summe sharedAllocations.minutes
```

Ein Integrationsvertrag besitzt exakt:

```json
{
  "id": "INT-5-RESEARCH-PRODUCTION",
  "moduleIds": ["IUM-5-CORE-02", "IUM-5-CORE-06"],
  "pathIds": ["baseline", "regular", "extended"],
  "sharedPhaseOrProduct": "",
  "countedInModuleId": "IUM-5-CORE-06",
  "sharedMinutes": 45,
  "savingsMinutesByPath": {
    "baseline": 45,
    "regular": 0,
    "extended": 0
  },
  "preservedLearningActions": [],
  "preservedProductAndCurriculumEvidence": [],
  "prerequisites": [],
  "risk": "",
  "fallback": "",
  "status": "working"
}
```

Eine Jahresvariante besitzt exakt:

```json
{
  "id": "GRADE-5-BASELINE",
  "grade": 5,
  "kind": "planning-path",
  "pathId": "baseline",
  "targetUnits": 30,
  "allocations": [
    {
      "moduleId": "IUM-5-CORE-01",
      "budgetPathId": "baseline",
      "units": 5
    }
  ],
  "integrationContractIds": [],
  "available": true,
  "status": "working",
  "rationale": "",
  "risk": ""
}
```

Ein Zeitreview besitzt exakt:

```json
{
  "id": "TR-BMB16-GYM-IK-GM-001",
  "competencyId": "BMB16-GYM-IK-GM-001",
  "moduleId": "IUM-5-CORE-01",
  "sourceTimeImpactLevel": "review-required",
  "decision": "additional-time",
  "rationale": "",
  "phaseIds": ["guided-practice"],
  "additionalMinutes": 15,
  "integrationContractIds": [],
  "sequenceEvidenceId": null,
  "pathAvailability": ["GRADE-5-BASELINE", "GRADE-5-REGULAR", "GRADE-5-EXTENDED"],
  "coverageConsequence": "semantic-status-unchanged",
  "risk": "",
  "followUp": "",
  "status": "working"
}
```

Ein Sequenznachweis besitzt exakt:

```json
{
  "id": "SE-LH26-E-PROG-001",
  "competencyId": "LH26-E-PROG-001",
  "moduleIds": [],
  "grades": [],
  "progression": "",
  "operatorProductDepth": "",
  "perspectiveWeighting": "",
  "timeWeighting": "",
  "annualVariantIds": [],
  "remainingBoundary": "",
  "coverageDecision": "remain-partial",
  "fachAuditStatus": "passed",
  "status": "working"
}
```

Die vier Statusdimensionen eines Jahrgangsurteils heißen exakt `semanticCoverageStatus`, `timeFeasibilityStatus`, `sequenceEvidenceStatus` und `pilotStatus`. Ein `green`-Zeiturteil ist zulässig, obwohl die semantische Coverage noch `partial` ist; die Begründungen müssen diese Trennung ausdrücklich nennen.

Ein Jahrgangsurteil besitzt exakt:

```json
{
  "grade": 7,
  "semanticCoverageStatus": "partial",
  "timeFeasibilityStatus": "red",
  "sequenceEvidenceStatus": "partial",
  "pilotStatus": "not-started",
  "annualVariantIds": [
    "GRADE-7-OPTIMIZED-DEMAND",
    "GRADE-7-ROBUST-DEMAND",
    "GRADE-7-HISTORICAL-MINIMUM"
  ],
  "rationale": "Kein Bedarfsszenario liegt innerhalb des 38-UE-Erweiterungspfads.",
  "risk": "Eine rechnerische Verdichtung würde unverzichtbare Lernhandlungen verdrängen.",
  "decisionOptions": [
    "additional-school-time",
    "structural-integration-or-reclassification",
    "curricular-reprioritisation",
    "earlier-preparation",
    "explicitly-incomplete-path"
  ]
}
```

Ein Risiko besitzt exakt `id`, `scope`, `statement`, `mitigation`, `decisionNeed` und `status`. Ein Pilotauftrag besitzt exakt:

```json
{
  "id": "PILOT-TC-IUM-5-CORE-01",
  "moduleContractId": "TC-IUM-5-CORE-01",
  "metrics": [
    "actual-teaching-minutes",
    "technical-startup-minutes",
    "support-minutes",
    "practice-and-revision-minutes",
    "interruptions",
    "retrieval-needed",
    "product-reached"
  ],
  "dataBoundary": "aggregate-module-only-no-personal-data",
  "status": "not-started"
}
```

## Standardzyklus für die 15 Zeitreview-Audits

Jeder der Tasks 9 bis 23 verwendet diesen atomaren Ablauf:

1. Anforderungstext, IUM09-`timeImpact.rationale`, Evidenzvertrag, zentrale Modulhandlung, Produkt und alle relevanten Phasen lesen.
2. Prüfen, ob die Anforderung dieselbe positive Phase und dieselbe Produktspur nutzt (`absorbed`), gemeinsame Lernzeit benötigt (`integrated`), eigenständige positive Zeit benötigt (`additional-time`) oder noch nicht belastbar verortet ist (`unresolved`).
3. `absorbed` nur mit `additionalMinutes: 0`, positiver Phasenbindung und existierender Produktspur verwenden.
4. `integrated` nur mit positiver eigener Zeit oder mindestens einem gültigen Integrationsvertrag verwenden.
5. `additional-time` nur mit positiver Minutenzahl verwenden.
6. `unresolved` mit `additionalMinutes: 0`, leerer `pathAvailability` sowie konkret benanntem Risiko und Folgeauftrag verwenden.
7. Die Entscheidung zuerst in `TIME_AUDIT_DECISIONS` in `tests/test_validate_ium10.py` eintragen und den Repositorytest rot ausführen.
8. Genau einen vollständigen Zeitreview in `roadmap/time-model.json` ergänzen.
9. Prüfen, dass zusätzliche Minuten in den vorhandenen positiven Phasenbudgets enthalten sind und nicht zusätzlich auf die Jahressumme aufgeschlagen werden.
10. Zieltest, gesamte IUM10-Tests sowie bestehende Phase-0- und IUM09-Tests grün ausführen.
11. Nur Test und Zeitmodell dieses Modulaudits committen.

`TIME_AUDIT_DECISIONS` speichert keine fachliche Zielquote, sondern das tatsächlich auditierte Ergebnis:

```python
TIME_AUDIT_DECISIONS = {
}
```

Die Kommentierung steht nur im Plan; die produktive Testdatei beginnt mit einem leeren Dictionary und erhält ausschließlich geprüfte Einträge. Der Vollständigkeitstest gegen alle 60 IDs wird erst in Task 25 aktiviert.

---

### Task 1: IUM09-Baseline und Zeitübergaben testgetrieben versiegeln

**Files:**

- Create: `scripts/validate_ium10.py`
- Create: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: `module_payload: dict`, `coverage_payload: dict`, `remediation_payload: dict`
- Produces: `validate_ium10_baseline(...) -> {"moduleIds": set[str], "coverageIds": set[str], "handoffIds": set[str]}`

- [ ] `git status --short --branch` ausführen und bestätigen, dass nur Spezifikations-, Plan- und Workspaceänderungen vorliegen.
- [ ] In `tests/test_validate_ium10.py` Importe und einen Repositoryfixture für die drei Baselineartefakte anlegen.
- [ ] Diese positiven Baselineassertionen exakt schreiben:

```python
self.assertEqual(len(result["moduleIds"]), 31)
self.assertEqual(len(result["coverageIds"]), 171)
self.assertEqual(len(result["handoffIds"]), 60)
self.assertEqual(
    coverage_projection_fingerprint(
        self.coverage_payload,
        self.remediation_payload,
    ),
    BASELINE_COVERAGE_PROJECTION_SHA256,
)
self.assertEqual(
    time_handoff_fingerprint(self.remediation_payload),
    BASELINE_TIME_HANDOFF_SHA256,
)
```

- [ ] Rote Mutationstests schreiben: Modul-ID, Jahrgang, Art, Voraussetzung oder `lessonRange`; Coverage-ID, Modulzuordnung oder IUM09-Status; Übergabe-ID, Modul, Level oder Rationale müssen scheitern.
- [ ] Zieltest rot ausführen:

```powershell
python -B -m unittest tests.test_validate_ium10
```

Erwartet: `ModuleNotFoundError: No module named 'scripts.validate_ium10'`.

- [ ] In `scripts/validate_ium10.py` diese Konstanten und Fingerprintfunktionen implementieren:

```python
import copy
import hashlib
import json
from collections import Counter

from scripts.validate_ium09 import module_structure_fingerprint


IUM10_BASELINE_COMMIT = "e53bad7cffe1541fc910db948235908bebe89caa"
BASELINE_MODULE_STRUCTURE_SHA256 = (
    "da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc"
)
BASELINE_COVERAGE_PROJECTION_SHA256 = (
    "cb9e09fa755a15206054e87ad0d5a8784fead63ff59530da0088b34e11dd2974"
)
BASELINE_TIME_HANDOFF_SHA256 = (
    "423b94122b931f4585b75aa74074f71b2e80a2b8b02cc92b32bf74585128f9bd"
)
ROADMAP_DEPENDENT_IDS = frozenset(
    {
        "LH26-E-PROG-001",
        "LH26-E-PROG-002",
        "LH26-E-PROG-003",
        "LH26-E-PROG-004",
    }
)


class IUM10ValidationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM10ValidationError(message)


def _canonical_sha256(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def coverage_projection_fingerprint(coverage_payload, remediation_payload):
    remediation_by_id = {
        entry["competencyId"]: entry
        for entry in remediation_payload["entries"]
    }
    projection = []
    for entry in coverage_payload["entries"]:
        remediation = remediation_by_id.get(entry["competencyId"])
        after = remediation["after"] if remediation else entry
        projection.append(
            {
                "competencyId": entry["competencyId"],
                "moduleIds": sorted(entry["moduleIds"]),
                "coverageStatus": after["coverageStatus"],
                "semanticAudit": after["semanticAudit"],
                "evidenceModuleId": entry["evidenceModuleId"],
            }
        )
    return _canonical_sha256(
        sorted(projection, key=lambda record: record["competencyId"])
    )


def time_handoff_fingerprint(remediation_payload):
    handoffs = [
        {
            "competencyId": entry["competencyId"],
            "moduleId": entry["before"]["evidenceModuleId"],
            "sourceTimeImpactLevel": entry["timeImpact"]["level"],
            "sourceTimeImpactRationale": entry["timeImpact"]["rationale"],
        }
        for entry in remediation_payload["entries"]
    ]
    return _canonical_sha256(
        sorted(handoffs, key=lambda record: record["competencyId"])
    )
```

- [ ] `validate_ium10_baseline` ergänzen und zusätzlich exakt 24 `core`, 7 flexible, 164/7 rekonstruierte Coverage sowie 56/4 Übergabelevel prüfen.
- [ ] Zieltest grün ausführen; erwartet: `OK`.
- [ ] Vollständige bestehende Tests ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_phase0.py
```

Erwartet: 192 bestehende Tests plus neue IUM10-Tests grün; CLI endet mit `phase 0 validation passed`.

- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "test: seal IUM10 baseline"
```

### Task 2: Zeiteinheit, Kapazitätsbänder und Pufferregel implementieren

**Files:**

- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`
- Create: `roadmap/time-model.json`

**Interfaces:**

- Consumes: `capacity_model: dict`, `unit_contract: dict`
- Produces: `validate_capacity_model(...) -> dict[str, dict]`

- [ ] `git status --short --branch` prüfen.
- [ ] Rote Tests für exakt 45 Minuten, die Pfade `baseline: 30`, `regular: 34`, `extended: 38`, Status `working`, die fünf Kalenderwerte 40/40/39/36/37 und die Pufferformel schreiben.
- [ ] Rote Tests für 30+6 als fälschlich amtliche Norm, negative lokale Puffer, fehlende Kapazitätsebene und einen Basispfad ohne geschützte Lernfunktionen schreiben.
- [ ] In `roadmap/time-model.json` die Top-Level-Struktur mit `schemaVersion: 1`, `status: "draft"`, den drei Baselinefingerprints und leeren, ausdrücklich noch nicht in den gemeinsamen CLI-Einstieg eingebundenen Vertragslisten anlegen. `baseline` enthält `commit`, `moduleStructureSha256`, `coverageProjectionSha256` und `timeHandoffSha256` mit den Global-Constraint-Werten. Danach diesen Kapazitätskern eintragen:

```json
{
  "unit": {
    "label": "Unterrichtseinheit",
    "minutes": 45
  },
  "capacityModel": {
    "officialWeeklyUnits": 1,
    "officialStatus": "administrative-context",
    "calendarEstimate": {
      "schoolYear": "2026/2027",
      "status": "dated-project-calculation",
      "weekdayUnits": {
        "monday": 40,
        "tuesday": 40,
        "wednesday": 39,
        "thursday": 36,
        "friday": 37
      }
    },
    "capacityLevels": [
      "calendar-capacity",
      "local-capacity",
      "planning-capacity"
    ],
    "planningPaths": [
      {"id": "baseline", "units": 30, "status": "working"},
      {"id": "regular", "units": 34, "status": "working"},
      {"id": "extended", "units": 38, "status": "working"}
    ],
    "bufferRule": {
      "formula": "localCapacityUnits - selectedPathUnits",
      "minimumBufferUnits": 0,
      "protectedLearningFunctions": [
        "activation",
        "concept-building",
        "guided-practice",
        "independent-action",
        "product-evidence",
        "feedback-or-self-check",
        "revision",
        "consolidation",
        "transfer-or-retrieval"
      ]
    },
    "status": "working"
  }
}
```

- [ ] Zieltest rot ausführen; erwartet: fehlende Funktion `validate_capacity_model`.
- [ ] `validate_capacity_model` implementieren: exakte Felder, boolesche Werte nicht als Integer akzeptieren, drei eindeutige Pfade zurückgeben, 30+6 nur in erklärendem Risikotext zulassen.
- [ ] Zieltest grün ausführen:

```powershell
python -B -m unittest tests.test_validate_ium10
```

- [ ] JSON strikt laden und deterministisch serialisieren:

```powershell
python -c "import json,pathlib; p=pathlib.Path('roadmap/time-model.json'); d=json.loads(p.read_text(encoding='utf-8')); assert json.loads(json.dumps(d, ensure_ascii=False, sort_keys=True)) == d"
```

- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py roadmap/time-model.json
git commit -m "feat: define IUM10 capacity model"
```

### Task 3: Schema und Rechenregeln der 31 Modulzeitverträge implementieren

**Files:**

- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: `module_contracts: list[dict]`, `module_payload: dict`
- Produces: `validate_module_contracts(...) -> dict[str, dict]`

- [ ] `git status --short --branch` prüfen.
- [ ] Testfabriken für einen Kern- und einen flexiblen Zeitvertrag mit den im Datenmodell festgelegten exakten Feldern schreiben.
- [ ] Rote Tests für unbekanntes Modul, doppelte Vertrags-ID, falsche ID-Bildung, abweichenden Jahrgang/Typ/`lessonRange`, abweichende Kompetenz-/Voraussetzungsliste sowie veränderte zentrale Handlung oder Produkt schreiben.
- [ ] Rote Rechentests schreiben: `minutes != units * 45`, Phasensumme ungleich Gesamtzeit, `directMinutes + countedSharedMinutes` ungleich Gesamtzeit, Shared-Summe ungleich `countedSharedMinutes`.
- [ ] Rote Didaktiktests schreiben: fehlende Kernphase, Nullzeit in einer Kernphase, Phase außerhalb der `moduleGrammar`, fehlende Lernfunktion, flexible Kernabdeckung oder `pilotRequired: false`.
- [ ] Zieltest rot ausführen; erwartet: fehlende Funktion `validate_module_contracts`.
- [ ] Diese Konstanten und den Validierungskern implementieren:

```python
PHASE_IDS = (
    "orientation-challenge",
    "activate-prior-knowledge",
    "build-concept",
    "guided-practice",
    "independent-action-product",
    "review-revise-transfer",
    "shared-consolidation",
)
CONTRACT_STATUSES = {"working", "reviewed"}
CORE_PATH_IDS = {
    5: {"baseline", "regular", "extended"},
    6: {"baseline", "regular"},
    7: {"optimized", "robust", "historical-minimum"},
}


def _positive_int(value):
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value > 0
    )
```

- [ ] Pro Modul genau einen `TC-{moduleId}`-Vertrag erzwingen. `standaloneUnitRange` ist für Kernmodule `null`, für flexible Module exakt `{min, recommended, max}` mit `0 < min <= recommended <= max`.
- [ ] Für Kernmodule exakt die vorgesehene Pfadmenge verlangen; `IUM-6-CORE-04` darf zusätzlich `targeted-extension` besitzen. Flexible Module besitzen genau `standalone`.
- [ ] Zieltest grün ausführen und vollständige Tests/CLI regressionsfrei bestätigen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: validate IUM10 module contracts"
```

### Task 4: Klasse-5-Zeitverträge, Integration und 30/34/38-Varianten anlegen

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `tests/test_validate_ium10.py`
- Modify: `scripts/validate_ium10.py`

**Interfaces:**

- Consumes: sieben Klasse-5-Module und deren Strukturverträge
- Produces: sieben Zeitverträge, `INT-5-RESEARCH-PRODUCTION`, drei Klasse-5-Jahresvarianten

- [ ] `git status --short --branch` prüfen.
- [ ] Diese Sollmatrix als Testkonstante anlegen:

```python
EXPECTED_GRADE_5_UNITS = {
    "IUM-5-CORE-01": {"baseline": 5, "regular": 6, "extended": 6},
    "IUM-5-CORE-02": {"baseline": 4, "regular": 5, "extended": 5},
    "IUM-5-CORE-03": {"baseline": 4, "regular": 5, "extended": 5},
    "IUM-5-CORE-04": {"baseline": 3, "regular": 3, "extended": 3},
    "IUM-5-CORE-05": {"baseline": 5, "regular": 5, "extended": 6},
    "IUM-5-CORE-06": {"baseline": 5, "regular": 5, "extended": 7},
    "IUM-5-CORE-07": {"baseline": 4, "regular": 5, "extended": 6},
}
```

- [ ] Rote Repositorytests schreiben, die sieben vollständige Verträge, exakt 30/34/38, ausschließlich Kernmodule und `available: true` verlangen.
- [ ] Unit-Tests für Integrationsverträge und Jahresvarianten schreiben: unbekannte Module/Pfade, fehlendes `countedInModuleId`, doppelt gezählte Shared Minutes, abweichende Allokation und falsche Zielsumme müssen scheitern.
- [ ] `validate_integration_contracts` und `validate_annual_variants` implementieren; boolesche Werte dürfen nicht als Minuten oder Einheiten gelten.
- [ ] Für jeden Modulpfad positive Minutenbudgets aller sieben Phasen aus der zentralen Lernhandlung und dem zentralen Produkt ableiten. Zusätzliche Regel-/Erweiterungszeit muss mindestens `guided-practice`, `independent-action-product` oder `review-revise-transfer` erhöhen.
- [ ] `INT-5-RESEARCH-PRODUCTION` anlegen: `IUM-5-CORE-02` und `IUM-5-CORE-06`, gemeinsame Quellen- und Belegspur, 45 gemeinsame Minuten gezählt in `IUM-5-CORE-06`, Einsparung 45/0/0 Minuten für baseline/regular/extended, Rückfall auf eigenständige Recherche- und Produktionszeit.
- [ ] In `IUM-5-CORE-06` die eine Shared Allocation eintragen; `IUM-5-CORE-02` referenziert die Integration ohne zweite Zählung.
- [ ] `GRADE-5-BASELINE`, `GRADE-5-REGULAR` und `GRADE-5-EXTENDED` mit den exakten Modulpfaden und Summen anlegen.
- [ ] Ein Klasse-5-Jahrgangsurteil mit getrenntem semantischem Status, `timeFeasibilityStatus: "green"`, noch nicht gestartetem Pilotstatus und den drei verfügbaren Varianten anlegen.
- [ ] Zieltest ausführen; erwartet vor Datenänderung fehlende Verträge, danach `OK`.
- [ ] Vollständige IUM10-Tests und bestehende Tests/CLI grün ausführen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py scripts/validate_ium10.py
git commit -m "data: add grade 5 time model"
```

### Task 5: Klasse-6-Kern- und Flexzeitverträge anlegen

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: sieben Klasse-6-Kernmodule und vier flexible Klasse-6-Module
- Produces: elf vollständige Zeitverträge

- [ ] `git status --short --branch` prüfen.
- [ ] Diese Kernmatrix als rote Testkonstante anlegen:

```python
EXPECTED_GRADE_6_CORE_UNITS = {
    "IUM-6-CORE-01": {"baseline": 5, "regular": 6},
    "IUM-6-CORE-02": {"baseline": 4, "regular": 5},
    "IUM-6-CORE-03": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-04": {
        "baseline": 4,
        "regular": 5,
        "targeted-extension": 6,
    },
    "IUM-6-CORE-05": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-06": {"baseline": 4, "regular": 4},
    "IUM-6-CORE-07": {"baseline": 5, "regular": 6},
}
```

- [ ] Flexible Sollverträge testen: `IUM-6-EXT-01` empfohlen 4 UE, `IUM-6-EXT-02` empfohlen 3 UE, `IUM-6-TRANSFER-01` empfohlen 4 UE, `IUM-6-PROJECT-01` mit Korridor 8/10/12 UE.
- [ ] Für alle elf Module positive, zur jeweiligen `moduleGrammar` vollständige Phasenbudgets anlegen.
- [ ] Bei den Kernmodulen zusätzliche Zeit ausschließlich als zusätzliche Erklärung, Übung, Handlung, Revision, Sicherung oder Abruf ausweisen.
- [ ] Bei den flexiblen Modulen `standaloneUnitRange` und Andockvoraussetzungen aus dem bestehenden Graph unverändert übernehmen.
- [ ] Projektzeit nicht in 30/34/38 einplanen und im Risiko die notwendige zusätzliche Schwerpunktzeit ausdrücklich nennen.
- [ ] Zieltest rot und nach Datenänderung grün ausführen; anschließend Gesamttests und CLI.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: add grade 6 time contracts"
```

### Task 6: Klasse-6-Integrationen und drei belastbare 38er-Varianten implementieren

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: elf Klasse-6-Zeitverträge
- Produces: drei Integrationsverträge, 30er-/34er-Pfad und drei 38er-Varianten

- [ ] `git status --short --branch` prüfen.
- [ ] Rote Tests für `INT-6-ACTORS-SELECTION`, `INT-6-CONFLICT-PRODUCTION` und `INT-6-ALGORITHM-REVISIT` schreiben.
- [ ] Integrationsverträge mit diesen Grenzen anlegen:

| ID | Module | gezählt in | Einsparung baseline/regular |
|---|---|---|---:|
| `INT-6-ACTORS-SELECTION` | `IUM-6-CORE-01`, `IUM-6-CORE-02` | `IUM-6-CORE-01` | 90/45 Minuten |
| `INT-6-CONFLICT-PRODUCTION` | `IUM-6-CORE-06`, `IUM-6-CORE-07` | `IUM-6-CORE-07` | 90/0 Minuten |
| `INT-6-ALGORITHM-REVISIT` | `IUM-5-CORE-05`, `IUM-6-CORE-04` | `IUM-6-CORE-04` | 45/0 Minuten |

- [ ] Für jeden Vertrag gemeinsame Lernhandlung, Produkt-/Curriculumnachweise, Voraussetzungen, Risiko und eigenständige Rückfallzeit konkret benennen.
- [ ] Shared Allocations nur bei den drei `countedInModuleId`-Verträgen eintragen und Doppelzählungstests schreiben.
- [ ] `GRADE-6-BASELINE` mit 30 und `GRADE-6-REGULAR` mit 34 Kern-UE anlegen.
- [ ] Drei exakt 38 UE große Erweiterungsvarianten anlegen:

```text
GRADE-6-EXTENDED-REFERENCE = Regelkern 34 + IUM-6-EXT-01 4
GRADE-6-EXTENDED-TRANSFER  = Regelkern 34 + IUM-6-TRANSFER-01 4
GRADE-6-EXTENDED-CODING    = Regelkern mit IUM-6-CORE-04 targeted-extension 35 + IUM-6-EXT-02 3
```

- [ ] Validatorisch erzwingen, dass flexible Module keine Kernmodule ersetzen und `IUM-6-PROJECT-01` in keiner normalen Variante vorkommt.
- [ ] Ein Klasse-6-Jahrgangsurteil anlegen: `green` nur wenn 30/34/38, alle Verträge und alle Integrationen bestehen; andernfalls `amber` mit konkret benanntem Restbefund. Semantischen Status und Pilotstatus getrennt halten.
- [ ] Zieltest rot und nach Implementierung grün ausführen; anschließend Gesamttests/CLI.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "data: add grade 6 annual variants"
```

### Task 7: Klasse-7-Bedarfsverträge, Orchestrierungscluster und rotes Urteil implementieren

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: zehn Klasse-7-Kernmodule und drei flexible Klasse-7-Module
- Produces: 13 Verträge, vier Integrationscluster, drei Bedarfsszenarien und ein `red`-Urteil

- [ ] `git status --short --branch` prüfen.
- [ ] Diese Matrix als rote Testkonstante anlegen:

```python
EXPECTED_GRADE_7_UNITS = {
    "IUM-7-CORE-01": {"optimized": 5, "robust": 5, "historical-minimum": 6},
    "IUM-7-CORE-02": {"optimized": 3, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-03": {"optimized": 5, "robust": 5, "historical-minimum": 6},
    "IUM-7-CORE-04": {"optimized": 6, "robust": 6, "historical-minimum": 7},
    "IUM-7-CORE-05": {"optimized": 4, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-06": {"optimized": 3, "robust": 3, "historical-minimum": 4},
    "IUM-7-CORE-07": {"optimized": 4, "robust": 4, "historical-minimum": 5},
    "IUM-7-CORE-08": {"optimized": 4, "robust": 6, "historical-minimum": 6},
    "IUM-7-CORE-09": {"optimized": 2, "robust": 3, "historical-minimum": 4},
    "IUM-7-CORE-10": {"optimized": 4, "robust": 6, "historical-minimum": 6},
}
```

- [ ] Zehn Kernverträge mit positiven Phasenbudgets anlegen. Die optimierte Untergrenze darf keine Kernphase auf null setzen.
- [ ] Flexible Verträge anlegen: `IUM-7-EXT-01` und `IUM-7-TRANSFER-01` mit 3/4/5 UE, `IUM-7-PROJECT-01` mit 8/10/12 UE. Keines wird in Klasse 7 eingeplant.
- [ ] Vier Clusterintegrationen anlegen:

| ID | Module | gezählt in | Einsparung optimized/robust |
|---|---|---|---:|
| `INT-7-DATA-CODING` | `IUM-7-CORE-01`, `IUM-7-CORE-02` | `IUM-7-CORE-02` | 135/90 Minuten |
| `INT-7-PROGRAMMING` | `IUM-7-CORE-03`, `IUM-7-CORE-04` | `IUM-7-CORE-04` | 90/90 Minuten |
| `INT-7-NET-SECURITY` | `IUM-7-CORE-05`, `IUM-7-CORE-06`, `IUM-7-CORE-07` | `IUM-7-CORE-07` | 135/135 Minuten |
| `INT-7-DATA-MEDIA-SOCIETY` | `IUM-7-CORE-08`, `IUM-7-CORE-09`, `IUM-7-CORE-10` | `IUM-7-CORE-10` | 270/45 Minuten |

- [ ] `GRADE-7-OPTIMIZED-DEMAND`, `GRADE-7-ROBUST-DEMAND` und `GRADE-7-HISTORICAL-MINIMUM` mit 40/46/54 UE, `kind: "demand-scenario"` und `available: false` anlegen.
- [ ] Rote Tests schreiben, die ein 30er-, 34er- oder 38er-Klasse-7-Angebot, flexible Ersatzmodule oder ein anderes Urteil als `red` ablehnen.
- [ ] Im Klasse-7-Urteil fünf Folgeoptionen dokumentieren: zusätzliche schulische Zeit, strukturelle Integration/Reklassifikation, curriculare Neupriorisierung, vorbereitende Verschiebung und ausdrücklich unvollständiger Pfad. Keine Option als umgesetzt markieren.
- [ ] Zieltests, Gesamttests und CLI grün ausführen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "data: model grade 7 time demand"
```

### Task 8: Zeitreviewschema und inkrementelle Auditregistratur implementieren

**Files:**

- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: `time_reviews`, `remediation_payload`, validierte Modul-, Integrations- und Jahresvariantenverträge
- Produces: `validate_time_reviews(..., require_complete=False|True) -> dict[str, dict]`

- [ ] `git status --short --branch` prüfen.
- [ ] `TIME_AUDIT_DECISIONS = {}` in der Testdatei anlegen.
- [ ] Fabriken und positive Tests für `absorbed`, `integrated`, `additional-time` und `unresolved` schreiben.
- [ ] Rote Tests schreiben: doppelte ID, falsches Modul/Level, unbekannte Phase/Integration/Variante, `absorbed` mit Zusatzzeit, `integrated` ohne Zeit und Integration, `additional-time` mit null, `unresolved` mit verfügbarem Pfad oder leerem Risiko.
- [ ] Rote Tests für `roadmap-dependent` schreiben: leere Phasen, `sequenceEvidenceId` verpflichtend, kein Einzelphasennachweis.
- [ ] Zieltest rot ausführen; erwartet: fehlende Funktion `validate_time_reviews`.
- [ ] Entscheidungsregeln und exakte Feldmengen implementieren. `require_complete=False` validiert eine eindeutige Teilmenge der 60 Baseline-IDs; `True` verlangt exakt alle 60. Die Funktion erhält `annual_variants` als fünftes Positionsargument.
- [ ] Sicherstellen, dass `pathAvailability` nur vorhandene Jahresvarianten nennt und `additionalMinutes` bereits in den Modulbudgets enthalten ist.
- [ ] Zieltest grün und Gesamttests regressionsfrei ausführen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "feat: validate IUM10 time reviews"
```

### Task 9: `IUM-5-CORE-01` mit sieben Zeitübergaben auditieren

**Records:** `BMB16-GYM-IK-GM-001`, `BMB16-GYM-IK-GM-002`, `BMB16-GYM-IK-GM-003`, `BMB16-GYM-PK-SK-003`, `LH26-E-DA-004`, `LH26-E-DP-001`, `LH26-E-PROG-001`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Geräteerkundung, lokale Medienordnung, Dateiorganisation, Datenbezug, Datenschutz und schulische Anmelde-/Speicherhandlungen jeweils getrennt gegen positive Phasen und Produktspuren prüfen.
- [ ] `BMB16-GYM-IK-GM-003` ohne neuen semantischen Nachweis trotz Zeitzuweisung als semantisch unverändert `partial` markieren.
- [ ] `LH26-E-PROG-001` nur an `SE-LH26-E-PROG-001` binden; keine Einzelphase fingieren.
- [ ] Sieben Ergebnisse in `TIME_AUDIT_DECISIONS` eintragen und den Zieltest rot ausführen.
- [ ] Sieben vollständige Reviews ergänzen; schulabhängige Technikzeit sichtbar halten.
- [ ] IUM10-Zieltests, gesamte Tests und CLI grün ausführen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-5-CORE-01 time impacts"
```

### Task 10: `IUM-5-CORE-02` mit einer Zeitübergabe auditieren

**Records:** `LH26-E-ID-009`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Informationsbewertung als ausgeführte Recherche-, Beleg- und Urteilsarbeit prüfen, nicht als bloße Kriterienliste.
- [ ] Gemeinsame Quellen- und Belegspur mit `INT-5-RESEARCH-PRODUCTION` nur bei tatsächlich identischer Produktspur verwenden.
- [ ] Entscheidung registrieren, Zieltest rot ausführen, genau einen Review ergänzen.
- [ ] IUM10-Tests, Gesamttests und CLI grün ausführen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-5-CORE-02 time impact"
```

### Task 11: `IUM-5-CORE-03` mit sechs Zeitübergaben auditieren

**Records:** `BMB16-GYM-IK-KK-002`, `BMB16-GYM-IK-KK-003`, `BMB16-GYM-PK-HK-003`, `BMB16-GYM-PK-RK-004`, `LH26-E-KS-001`, `LH26-E-KS-002`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Kommunikationsregeln, respektvolle Reaktion, Hilfeweg, schulischer Kanal und kooperative Produktspuren einzeln zeitlich auditieren.
- [ ] Schulkontextzeit nur bei tatsächlicher lokaler Ausführung anrechnen; Simulation bleibt unzureichend.
- [ ] Sechs Ergebnisse registrieren, Zieltest rot ausführen und sechs Reviews ergänzen.
- [ ] Prüfen, dass Regelpfadmehrzeit reale Übung, Revision oder Sicherung trägt.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-5-CORE-03 time impacts"
```

### Task 12: `IUM-5-CORE-05` mit zwei Zeitübergaben auditieren

**Records:** `LH26-E-ALG-001`, `LH26-E-PROG-002`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Algorithmusentwicklung als Erklärung, Erprobung, Fehlerkorrektur und Produkt sichern; reine Demonstration zählt nicht.
- [ ] `LH26-E-PROG-002` ausschließlich an `SE-LH26-E-PROG-002` binden.
- [ ] Zwei Ergebnisse registrieren, roten Test ausführen und zwei Reviews ergänzen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-5-CORE-05 time impacts"
```

### Task 13: `IUM-5-CORE-06` mit vier Zeitübergaben auditieren

**Records:** `BMB16-GYM-IK-PP-002`, `LH26-E-DA-005`, `LH26-E-DA-006`, `LH26-E-DA-008`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Planung, Produktion, Quellen-/Rechtebeleg, Zielgruppenpassung und Revision als reale Zeitbestandteile prüfen.
- [ ] `INT-5-RESEARCH-PRODUCTION` nur dort referenzieren, wo dieselbe Quellen- und Belegspur beide Anforderungen trägt.
- [ ] Vier Ergebnisse registrieren, roten Test ausführen und vier Reviews ergänzen.
- [ ] Prüfen, dass die Erweiterungszeit von 5 auf 7 UE Produktvertiefung und Revision erhöht.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-5-CORE-06 time impacts"
```

### Task 14: `IUM-5-CORE-07` mit sieben Zeitübergaben auditieren

**Records:** `BMB16-GYM-IK-MG-001`, `BMB16-GYM-IK-MG-002`, `BMB16-GYM-IK-MG-003`, `BMB16-GYM-PK-RK-001`, `BMB16-GYM-PK-RK-002`, `BMB16-GYM-PK-RK-003`, `LH26-E-DP-003`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Medienwirkung, private Selbstreflexion, Kriterienurteil und nichtpersonale Anschlussprodukte getrennt auditieren.
- [ ] Private Inhalte weder als Produktzeit noch als beobachtbare Nachweisspur modellieren.
- [ ] `BMB16-GYM-PK-RK-003` und `LH26-E-DP-003` ohne neuen semantischen Nachweis unverändert `partial` lassen.
- [ ] Sieben Ergebnisse registrieren, roten Test ausführen und sieben Reviews ergänzen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-5-CORE-07 time impacts"
```

### Task 15: `IUM-6-CORE-02` mit zwei Zeitübergaben auditieren

**Records:** `LH26-E-DP-004`, `LH26-E-DP-006`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Personalisierte Auswahl und Datenfluss als nachvollziehbare Modell- und Urteilsarbeit auditieren.
- [ ] Gemeinsame Akteurs-/Interessen-/Evidenzmodelle nur über `INT-6-ACTORS-SELECTION` zählen.
- [ ] Zwei Ergebnisse registrieren, roten Test ausführen und zwei Reviews ergänzen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-6-CORE-02 time impacts"
```

### Task 16: `IUM-6-CORE-06` mit zwei Zeitübergaben auditieren

**Records:** `LH26-E-KS-014`, `LH26-E-KS-015`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Konfliktanalyse, Handlungsoptionen und Hilfesysteme als ausgeführte Fallarbeit auditieren.
- [ ] Gemeinsame Zielgruppen-/Wirkungsarbeit mit Medienrevision ausschließlich über `INT-6-CONFLICT-PRODUCTION` referenzieren.
- [ ] Zwei Ergebnisse registrieren, roten Test ausführen und zwei Reviews ergänzen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-6-CORE-06 time impacts"
```

### Task 17: `IUM-6-CORE-07` mit vier Zeitübergaben auditieren

**Records:** `LH26-E-DA-009`, `LH26-E-DA-010`, `LH26-E-DA-012`, `LH26-E-DA-015`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Wirkung, Rechte, Zielgruppenbezug und Revision jeweils als sichtbare Produktarbeit auditieren.
- [ ] Schulabhängige Veröffentlichung oder Freigabe nur als lokale Ausführung, nicht als allgemeine Plattformvoraussetzung modellieren.
- [ ] Vier Ergebnisse registrieren, roten Test ausführen und vier Reviews ergänzen.
- [ ] Prüfen, dass der Regelpfad die zusätzliche Revision und Sicherung tatsächlich budgetiert.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-6-CORE-07 time impacts"
```

### Task 18: `IUM-7-CORE-01` mit fünf Zeitübergaben auditieren

**Records:** `INF7-16-GYM-IK-DC-001`, `INF7-16-GYM-IK-DC-004`, `INF7-16-GYM-IK-DC-005`, `LH26-E-ID-020`, `LH26-E-ID-021`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Zeichen, Zahlen, Bitfolgenlänge, Bit/Byte, Präfixe und Binärumwandlung als getrennte Begriffs-, Übungs- und Produktspuren auditieren.
- [ ] Überlappende Bildungsplan- und Lesehilferecords quellentreu getrennt lassen; keine Zeit doppelt zählen, wenn dieselbe Handlung beide trägt.
- [ ] Fünf Ergebnisse registrieren, roten Test ausführen und fünf Reviews ergänzen.
- [ ] Pfadverfügbarkeit auf Klasse-7-Bedarfsszenarien beziehen, nicht als grünen Jahrespfad ausgeben.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-7-CORE-01 time impacts"
```

### Task 19: `IUM-7-CORE-03` mit sechs Zeitübergaben auditieren

**Records:** `INF7-16-GYM-IK-ALG-003`, `INF7-16-GYM-PK-MI-005`, `INF7-16-GYM-PK-SV-003`, `LH26-E-ALG-007`, `LH26-E-ALG-008`, `LH26-E-ALG-009`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Kontrollfluss, Zustände, Modellierung, Testfälle und Fehlersuche einzeln zeitlich auditieren.
- [ ] Demonstration nicht als selbstständige Implementierungs-, Test- oder Debugginghandlung zählen.
- [ ] Sechs Ergebnisse registrieren, roten Test ausführen und sechs Reviews ergänzen.
- [ ] Optimierten Bedarf nicht als freigegebenen 38er-Pfad darstellen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-7-CORE-03 time impacts"
```

### Task 20: `IUM-7-CORE-04` mit drei Zeitübergaben auditieren

**Records:** `INF7-16-GYM-PK-KK-002`, `INF7-16-GYM-PK-MI-003`, `INF7-16-GYM-PK-SV-002`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Zielgruppenorientierte Fachkommunikation, Abstraktion und aussagekräftige Bezeichner als getrennte Entwicklungs- und Produktspuren auditieren.
- [ ] Gemeinsame Programmierzeit mit `INT-7-PROGRAMMING` nur einmal zählen; Teamarbeit ersetzt keine individuelle Fachhandlung.
- [ ] Drei Ergebnisse registrieren, roten Test ausführen und drei Reviews ergänzen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-7-CORE-04 time impacts"
```

### Task 21: `IUM-7-CORE-05` mit drei Zeitübergaben auditieren

**Records:** `INF7-16-GYM-IK-IGD-004`, `INF7-16-GYM-PK-AB-002`, `INF7-16-GYM-PK-SV-001`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Mobile Geräte/Datenträger, Schutzmaßnahmen, Modell-Realsituations-Vergleich und Schulnetznutzung getrennt auditieren.
- [ ] Tatsächliche lokale Schulnetznutzung einschließlich technischer Anlaufzeit sichtbar budgetieren; keine Zugangsdaten dokumentieren.
- [ ] Drei Ergebnisse registrieren, roten Test ausführen und drei Reviews ergänzen.
- [ ] Clusterintegration `INT-7-NET-SECURITY` darf keine Schutz- oder Modellhandlung entfernen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-7-CORE-05 time impacts"
```

### Task 22: `IUM-7-CORE-08` mit sieben Zeitübergaben auditieren

**Records:** `INF7-16-GYM-IK-IGD-006`, `INF7-16-GYM-PK-AB-005`, `INF7-16-GYM-PK-AB-006`, `INF7-16-GYM-PK-KK-006`, `LH26-E-DP-013`, `LH26-E-PROG-003`, `LH26-E-PROG-004`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Datenakteure, Desinformation, Quellenprüfung, Interessen, Perspektiven und private Reflexionsgrenzen getrennt auditieren.
- [ ] Private Inhalte ausschließlich lokal belassen; gemeinsame Nachweise müssen nichtpersonal sein.
- [ ] `LH26-E-PROG-003` und `LH26-E-PROG-004` nur an ihre Sequenznachweise binden und wegen fehlendem verfügbarem Klasse-7-Jahrespfad nicht vorschnell schließen.
- [ ] Sieben Ergebnisse registrieren, roten Test ausführen und sieben Reviews ergänzen.
- [ ] Clusterintegration `INT-7-DATA-MEDIA-SOCIETY` gegen Überfrachtung prüfen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-7-CORE-08 time impacts"
```

### Task 23: `IUM-7-CORE-10` mit einer Zeitübergabe auditieren

**Records:** `LH26-E-DP-014`

**Files:** `roadmap/time-model.json`, `tests/test_validate_ium10.py`

- [ ] `git status --short --branch` prüfen.
- [ ] Selbstwahrnehmung privat reflektieren lassen; nur nichtpersonale Analyse oder Gegenperspektive als sichtbare Produktspur verwenden.
- [ ] Keine implizite Offenlegungs-, Erhebungs- oder Bewertungszeit modellieren.
- [ ] Ergebnis registrieren, roten Test ausführen und einen Review ergänzen.
- [ ] Tests/CLI grün ausführen, synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json tests/test_validate_ium10.py
git commit -m "data: audit IUM-7-CORE-10 time impact"
```

### Task 24: Vier Sequenznachweise und ihre Coveragefolgen auditieren

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `roadmap/coverage-plan.json` only for fachlich bestandene roadmapweite Statuswechsel
- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: vier roadmapabhängige Zeitreviews, Jahresvarianten und aktueller Coverageplan
- Produces: vier Sequenznachweise und recordgenaue `coverageDecision`

- [ ] `git status --short --branch` prüfen.
- [ ] Rote Tests für exakt die IDs `LH26-E-PROG-001` bis `LH26-E-PROG-004` schreiben.
- [ ] Rote Tests schreiben, die bei `covered` vollständige Module/Jahrgänge, Progression, Operator-/Produkttiefe, Perspektiv- und Zeitgewichtung, `fachAuditStatus: passed` sowie mindestens eine `available: true`-Jahresvariante verlangen.
- [ ] Rote Tests schreiben, die `LH26-E-PROG-003` oder `004` bei ausschließlich nicht verfügbaren Klasse-7-Bedarfsszenarien nicht als `covered` akzeptieren.
- [ ] `SE-LH26-E-PROG-001` über Arbeitsfähigkeit, Datenhandhabung und zunehmende Selbstständigkeit in Klassen 5/6 auditieren.
- [ ] `SE-LH26-E-PROG-002` über Algorithmenprodukt Klasse 5, Wiederaufnahme Klasse 6 und Implementierungs-/Debuggingtiefe Klasse 7 auditieren.
- [ ] `SE-LH26-E-PROG-003` und `004` über Perspektiven-, Daten- und Medienprogression auditieren; Klasse-7-Zeitgrenze ausdrücklich benennen.
- [ ] Für jeden Record ohne Schließungsquote `covered` oder `remain-partial` entscheiden. Die Spezifikation nimmt das Ergebnis nicht vorweg.
- [ ] Nur bei bestandenem `covered`-Entscheid Coverageplan auf `covered`/`operator-product-match` umstellen; bestehende Anforderung, Modulhandlung und Produktstrings in `evidence` und `matchRationale` erhalten.
- [ ] Zieltests, alle IUM10-/IUM09-/Phase-0-Tests und CLI grün ausführen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json roadmap/coverage-plan.json scripts/validate_ium10.py tests/test_validate_ium10.py
git commit -m "data: audit IUM10 sequence evidence"
```

### Task 25: Alle Referenzen schließen und IUM10 fail-closed in den Repository-Einstieg integrieren

**Files:**

- Modify: `roadmap/time-model.json`
- Modify: `roadmap/module-candidates.json`
- Modify: `roadmap/coverage-remediation.json`
- Modify: `roadmap/coverage-plan.json`
- Modify: `scripts/validate_ium09.py`
- Modify: `tests/test_validate_ium09.py`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`
- Modify: `scripts/validate_ium10.py`
- Modify: `tests/test_validate_ium10.py`

**Interfaces:**

- Consumes: vollständiges IUM10-Modell und alle drei referenzierenden Roadmapartefakte
- Produces: `validate_ium10(...)` und gemeinsamer grüner CLI-Einstieg

- [ ] `git status --short --branch` prüfen.
- [ ] Den finalen Vollständigkeitstest aktivieren:

```python
self.assertEqual(set(TIME_AUDIT_DECISIONS), set(BASELINE_TIME_HANDOFF_IDS))
self.assertEqual(len(TIME_AUDIT_DECISIONS), 60)
```

- [ ] Zusätzlich registrierte Modul-ID, Quelllevel, Entscheidung und Minuten exakt gegen jeden Zeitreview prüfen.
- [ ] `roadmap/time-model.json` auf `status: "working"` setzen und exakt 31 Modulverträge, 60 Zeitreviews, vier Sequenznachweise, drei Jahrgangsurteile sowie einen Pilotauftrag pro Modulvertrag verlangen.
- [ ] In jedem Modulkandidaten `timeContractId: "TC-{moduleId}"` ergänzen und `modelNotes.timeBoundary` so präzisieren, dass `lessonRange` historische eigenständige Kandidatenschätzung und `time-model.json` autoritative Jahreszuweisung ist.
- [ ] In allen 60 Remediationeinträgen `timeReviewId: "TR-{competencyId}"` ergänzen; keine IUM09-Begründung, Entscheidung oder `timeImpact` ändern.
- [ ] In allen 60 Coverageeinträgen des Ledgers dieselbe `timeReviewId` ergänzen; bei den vier Roadmaprecords zusätzlich `sequenceEvidenceId: "SE-{competencyId}"`.
- [ ] `scripts/validate_ium09.py` so erweitern, dass `timeReviewId` optional für historische Unitfixtures, aber bei vorhandener Referenz nichtleer ist. IUM09-Entscheidungen bleiben unverändert.
- [ ] `ium09_coverage_projection` mit `copy.deepcopy` implementieren: nur fachlich durch IUM10 geschlossene Roadmaprecords werden für den historischen IUM09-Lauf auf Ledger-`after`, `residualGap.reason`, `risk` und `followUp` zurückprojiziert.
- [ ] Rote Tests schreiben, die andere Coverageänderungen, fehlende oder falsche Referenzen, doppelte IDs und Änderungen am historischen `lessonRange` blockieren.
- [ ] `validate_ium10` implementieren und exakte Top-Level-Felder, alle Komponenten, drei Jahrgangsurteile, Risiken und nichtpersonale Pilotaufträge orchestrieren.
- [ ] `scripts/validate_phase0.py` nach dem bisherigen Phase-0-Coveragecheck wie folgt orchestrieren:

```python
time_model = load_json(root / "roadmap/time-model.json")
ium10_result = validate_ium10(
    time_model,
    module_candidates,
    coverage_payload,
    remediation_payload,
)
validate_ium09(
    module_candidates,
    ium10_result["ium09CoverageProjection"],
    remediation_payload,
    required_curriculum_contracts,
)
```

- [ ] Den bisherigen direkten IUM09-Aufruf ersetzen, nicht zusätzlich doppelt ausführen.
- [ ] `validate_phase0.py` am Ende `phase 0, IUM09 and IUM10 validation passed` ausgeben lassen und Tests darauf aktualisieren.
- [ ] Zieltests rot und nach Implementierung grün ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_validate_ium10.py"
python -B -m unittest discover -s tests -p "test_validate_ium09.py"
python -B -m unittest discover -s tests -p "test_validate_phase0.py"
python -B scripts/validate_phase0.py
```

- [ ] Fingerprints, 31/60/4/171-Vollständigkeit und 30/34/38/40/46/54 erneut maschinell prüfen.
- [ ] Synchronisieren und committen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/time-model.json roadmap/module-candidates.json
git add roadmap/coverage-remediation.json roadmap/coverage-plan.json
git add scripts/validate_ium09.py tests/test_validate_ium09.py
git add scripts/validate_ium10.py tests/test_validate_ium10.py
git add scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "feat: integrate IUM10 time validation"
```

### Task 26: Zeitmodell publizieren, getrennt reviewen und als Nutzer-Gate übergeben

**Files:**

- Modify: `roadmap/module-roadmap.md`
- Modify: `README.md`
- Modify: nur Dateien mit konkret festgestellten Reviewmängeln

- [ ] `git status --short --branch` prüfen.
- [ ] In `roadmap/module-roadmap.md` Projektannahme, datierte Kalenderrechnung, 30/34/38-Arbeitsmodell und Freigabeurteil klar trennen.
- [ ] Klasse-5- und Klasse-6-Modulmatrix einschließlich aller 38er-Varianten publizieren.
- [ ] Klasse-7-Matrix 40/46/54, vier Cluster, `red`-Urteil und fünf nicht umgesetzte Folgeoptionen publizieren.
- [ ] Integrationsverträge mit gezähltem Modul, erhaltener Lernhandlung/Produktspur, Einsparung und Rückfalloption lesbar dokumentieren.
- [ ] Die 60/60-Zeitbilanz nach Modul gruppiert mit Kompetenz-ID, Quelllevel, Entscheidung, Zusatzminuten, Pfadverfügbarkeit und Coveragefolge publizieren.
- [ ] Vier Sequenznachweise und tatsächliche Coveragefolgen publizieren; semantische Coverage und Zeitstatus getrennt ausweisen.
- [ ] `README.md` auf `roadmap/time-model.json`, drei Validatoren und die weiterhin ausstehende Auftraggeber-Zeitfreigabe aktualisieren.
- [ ] Repositorytests schreiben, welche alle publizierten Summen und 60 Tabellenzeilen aus den JSON-Artefakten ableiten; keine Zahlen nur als statischen Text testen.
- [ ] Vollständige Gates ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_phase0.py
git diff --check
```

- [ ] Alle veränderten `.md`, `.json` und `.py` strikt als UTF-8 decodieren, auf das Unicode-Ersatzzeichen U+FFFD prüfen und alle JSON-Dateien deterministisch roundtrippen.
- [ ] Fachreview durchführen: Lernhandlungs-/Produktrealismus, Nullzeit, Überfrachtung, schulabhängige Technik, private Grenzen, 60 Einzelentscheidungen, vier Sequenzen und Klasse-7-Konflikt. Jeden Befund record- oder vertragsgenau dokumentieren.
- [ ] Engineeringreview durchführen: exakte Felder, bool-vs-int, Dubletten, unbekannte Referenzen, Fingerprints, Doppelzählung, Summen, historische Projektion, Coverageupgrade, UTF-8 und Markdown/JSON-Synchronität.
- [ ] Für jeden Reviewbefund zuerst einen roten Regressionstest schreiben, dann den kleinsten Fix umsetzen und alle Gates erneut ausführen.
- [ ] Zielbilanz maschinell ausgeben und gegen 31 Verträge, 60 Reviews, vier Sequenzen, 30/34/38 für Klassen 5/6 und 40/46/54 `red` für Klasse 7 prüfen.
- [ ] Synchronisieren, den Publikationscommit erstellen und pushen:

```powershell
git fetch --prune
git pull --ff-only
git add roadmap/module-roadmap.md README.md
git commit -m "docs: publish IUM10 time model"
git push origin feat/ium-phase0
```

Reviewkorrekturen werden vor diesem Publikationscommit jeweils mit den konkret betroffenen Pfaden in eigenen kleinen Commits gestaged; kein Sammel-`git add` auf ganze Verzeichnisse ist zulässig.

- [ ] Mit `git status --short --branch`, `git rev-parse HEAD` und `git rev-parse origin/feat/ium-phase0` sauberen, synchronen Abschluss nachweisen.
- [ ] Draft-PR #1 um Zeitmodell, Testbilanz, fachlichen/technischen Reviewstatus, verbleibende Risiken und Klasse-7-Entscheidungsbedarf ergänzen.
- [ ] Workspace-Task, Initiative, Kanban, Projektseite, Entwicklungshistorie und Session Summary mit Commit, Branch, Testzahl, Coveragefolge und Pushstatus aktualisieren.
- [ ] IUM10 als reviewfähig, nicht als freigegeben dokumentieren. Phase 1 bleibt bis zum gesonderten Nutzerentscheid ungeplant.

## Selbstreview des Plans vor Ausführung

### Spezifikationsabdeckung

| Spezifikationsabschnitt | Umsetzungsort im Plan |
|---|---|
| §§ 1–3 Zweck, Baseline, Kapazität und Puffer | Global Constraints, Tasks 1–2 |
| § 4 Zeitverträge und positive Phasenbudgets | Tasks 3–7 |
| § 5 vollständiger Review der 60 Übergaben | Task 8 und Tasks 9–23 |
| § 6 Integrationsverträge und Rückfall | Tasks 4, 6 und 7 |
| § 7 Jahrgangsmodelle 30/34/38 und 40/46/54 | Tasks 4, 6 und 7 |
| § 8 getrennte Coverage- und Progressionsfolgen | Tasks 24–25 |
| § 9 Artefaktarchitektur | File Map und Tasks 1–8, 25–26 |
| § 10 zwanzig Validierungsregeln | Tasks 1–8 und 25–26 |
| § 11 sechs Review- und Freigabegates | Dependency Flow und Task 26 |
| §§ 12–13 Pilot-, Status-, Abbruch- und Rückfalllogik | Global Constraints, Tasks 4–7 und 25–26 |
| § 14 WU-Check | positive Lernfunktionsbudgets in Tasks 3–7 und Fachreview in Task 26 |
| § 15 Akzeptanzkriterien | nachfolgende Selbstreview-Checkliste und Task 26 |
| § 16 Nichtziele | Global Constraints und Ausführungshandoff |

- [x] Jede verbindliche Regel der freigegebenen Spezifikation ist mindestens einem Task oder Global Constraint zugeordnet.
- [x] Alle 31 Modul-IDs erhalten genau einen Vertrag; 24 Kern- und 7 flexible Module bleiben sichtbar.
- [x] Alle 60 Übergabe-IDs erscheinen genau einmal in den 15 Modulaudits.
- [x] Die Verteilung der Audittasks ergibt 27 Klasse-5-, 8 Klasse-6- und 25 Klasse-7-Records.
- [x] Alle vier `roadmap-dependent`-IDs besitzen zusätzlich genau einen Sequenznachweis.
- [x] 30/34/38 für Klasse 5 und Klasse 6 sowie 40/46/54 für Klasse 7 sind in Tests und Datentasks verankert.
- [x] Kein Task verändert Modul-ID, Jahrgang, Art, Voraussetzung, zentrale Handlung, Produkt oder historische `lessonRange`.
- [x] Flexible Vertiefungs-, Transfer- und Projektmodule bleiben erhalten und ersetzen keine Kernabdeckung.
- [x] Jeder Datentask beginnt mit einem roten Test und endet mit zielgerichteter sowie integrierter Prüfung.
- [x] Zeitreviewentscheidungen werden ohne Zielquote fachlich getroffen.
- [x] Semantische Coverage, Zeitdurchführbarkeit, Sequenznachweis und Pilotstatus bleiben getrennt.
- [x] Roadmap-Coverage kann nur über vollständigen Sequenznachweis, verfügbaren Jahrespfad und Fachaudit steigen.
- [x] Private Inhalte werden weder beobachtet, gesammelt, gespeichert noch bewertet.
- [x] Kein Code- oder Datenabschnitt enthält Marker für offene Implementierung, unbefüllte Scheinwerte oder nur scheinbar erfüllte Funktionen.
- [x] Imports, Funktionsnamen, Feldnamen und Rückgabeverträge sind in Plan, File Map und Orchestrierung konsistent.
- [x] Der Abschluss enthält getrenntes Fach- und Engineeringreview, gesondertes Nutzer-Gate und keine Phase-1-Planung.

## Ausführungshandoff

Nach Freigabe dieses Plans gibt es zwei Ausführungsmodi:

1. **Subagent-driven (empfohlen):** Taskweise Umsetzung mit getrennten Implementierungs- und Reviewrollen. Dieser Modus erfordert eine ausdrückliche Nutzerfreigabe für Subagenten.
2. **Inline mit `superpowers:executing-plans`:** Sequentielle Umsetzung im aktuellen Task mit Checkpoints nach Task 3, Task 8, Task 14, Task 23, Task 25 und vor dem Push.

Ohne ausdrückliche Delegationsfreigabe wird Modus 2 verwendet.
