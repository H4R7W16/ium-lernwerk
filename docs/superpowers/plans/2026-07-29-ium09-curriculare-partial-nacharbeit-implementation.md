# IUM09 Curriculare Partial-Nacharbeit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die 60 in Gate 3 als Nacharbeitsauftrag angenommenen `partial`-Records recordgenau auditieren, fachlich tragfähige Evidenzverträge in den bestehenden Kernmodulen verankern und jede geschlossene oder verbleibende Lücke in einem unveränderlichen Nacharbeitsledger dokumentieren.

**Architecture:** IUM09 ergänzt die bestehenden Phase-0-Artefakte um recordgenaue `coverageEvidence`-Verträge und ein separates `coverage-remediation.json`. Ein fokussierter Python-Validator prüft Baseline, Modulstruktur, Evidenzmodi, Ledgerentscheidungen und die Synchronität mit dem Coverageplan; `validate_phase0.py` bleibt der gemeinsame Repository-Einstieg. Die 15 betroffenen Kernmodule werden nacheinander fachlich auditiert. Zeitmodell, Modulgraph und Hybridstruktur bleiben unverändert und werden nur als Übergabe an IUM10 dokumentiert.

**Tech Stack:** JSON, Markdown, Python 3.11+ Standardbibliothek, `unittest`, Git.

## Global Constraints

- Maßgebliche fachliche Spezifikation ist `docs/superpowers/specs/2026-07-29-ium09-curriculare-partial-nacharbeit-design.md` in Commit `a98a63e89b5be5311462c2aca09b97a11a7113ea`; sie wurde am 29. Juli 2026 schriftlich durch den Nutzer freigegeben.
- Maßgebliche Ausgangscoverage ist Commit `69c9d4f5504a297289615b4169fc4a9ea6d9b253`.
- Der Baseline-Fingerprint der 60 Ausgangsbefunde bleibt `b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892`.
- Der semantisch kanonisierte Fingerprint aus Modul-ID, Jahrgang, Typ, sortierten Voraussetzungen und Stundenkorridor bleibt `da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc`.
- Die Ursachenklassifikation bleibt exakt 39 `module-detail`, 9 `school-context`, 8 `private-local` und 4 `roadmap-level`.
- Es gibt keine Zielquote für geschlossene Records. `covered` ist ausschließlich das Ergebnis des manuellen Operator-Gegenstand-Lernhandlung-Produkt-Audits.
- Die 31 Kandidaten, ihre IDs, Jahrgänge, Typen, Voraussetzungen und Stundenkorridore bleiben unverändert.
- Der verbindliche Kernlernweg und die flexibel einsetzbaren Vertiefungs-, Transfer- und Projektmodule bleiben erhalten.
- IUM09 ändert weder Jahreszeitkorridore noch Abhängigkeiten. Erkannte Zeitfolgen werden an IUM10 übergeben; eine erforderliche Graphänderung erzwingt in IUM09 `remain-partial`.
- Die vier Records `LH26-E-PROG-001` bis `LH26-E-PROG-004` bleiben `partial`, erhalten keinen Einzelmodulvertrag und werden mit `timeImpact.level: roadmap-dependent` an IUM10 übergeben.
- `school-context` verlangt tatsächliche lokale Nutzung einer schulischen System-, Kanal- oder Regelumgebung. Eine Simulation oder bloße Beschreibung schließt den Record nicht.
- `private-local` bleibt ausschließlich lokal bei der lernenden Person. Private Inhalte werden nicht erhoben, übertragen, eingesammelt, gespeichert oder bewertet. Nur eine nichtpersonale fachliche Anschlussaufgabe darf geteilt oder beobachtet werden.
- Evidenzverträge dokumentieren eine fachlich tragfähige Lerngelegenheit, keine Leistungsbewertung und keinen tatsächlichen Kompetenzerwerb.
- Die 111 bereits `covered` eingestuften Records bleiben außerhalb des IUM09-Ledgers, behalten den Status `covered` und erhalten kein `evidenceContractId`.
- Die natürlichsprachliche Semantikentscheidung bleibt ein manueller Fachaudit. Der Validator prüft Struktur, Identität, Vollständigkeit und referenzielle Konsistenz, nicht die fachliche Bedeutung allein.
- Vor jedem Task: `git status --short --branch` prüfen. Vor jedem Commit oder Push: `git fetch --prune` und `git pull --ff-only` ausführen. Bei einem Fehler nicht pushen.
- Jeder Task endet mit einem kleinen, absichtlich zusammengestellten Commit. Coverage-Daten eines Moduls werden nie teilweise über mehrere Commits verteilt.
- Sichtbarer deutscher Text verwendet UTF-8-Umlaute und `ß`; technische IDs und Dateinamen bleiben ASCII-stabil.
- IUM09 umfasst keine Lernendenanwendung, keine Phase-1-Planung, keine Niveaudifferenzierung und keine personenbezogene Diagnostik.

## File Map

| Pfad | Aktion | Verantwortung |
|---|---|---|
| `scripts/validate_ium09.py` | Create | Baseline-, Evidenz-, Ledger- und Synchronitätsvalidator für IUM09 |
| `tests/test_validate_ium09.py` | Create | Unit- und Repositorytests für den vollständigen IUM09-Vertrag |
| `scripts/validate_phase0.py` | Modify | IUM09-Validator in den bestehenden Repository-Einstieg einbinden |
| `tests/test_validate_phase0.py` | Modify | Feste 111/60-Annahmen durch ledgergestützte Bilanz ersetzen |
| `roadmap/coverage-remediation.json` | Create | Unveränderter Vorherbefund, Ursachenklasse, Entscheidung und Folgen aller 60 Records |
| `roadmap/module-candidates.json` | Modify | Nur fachlich bestandene recordgenaue `coverageEvidence`-Verträge ergänzen |
| `roadmap/coverage-plan.json` | Modify | Nur ledgergestützte Status- und Evidenzänderungen synchronisieren |
| `roadmap/module-roadmap.md` | Modify | Ergebnisbilanz, Verdichtungsrisiken und IUM10-Übergabe dokumentieren |
| `README.md` | Modify | IUM09-Artefakte, Statusgrenze und Validierungseinstieg verlinken |
| `docs/superpowers/plans/2026-07-29-ium09-curriculare-partial-nacharbeit-implementation.md` | Track | Ausführungsstand über Checkboxen nachvollziehbar halten |

## Dependency Flow

```text
Task 1 Evidenz- und Strukturvalidator
└── Task 2 Baseline-Ledger
    └── Task 3 Phase-0-Integration
        ├── Tasks 4–18 modulweise Fachaudits in fester Reihenfolge
        └── Task 19 Gesamtbilanz und Dokumentation
            └── Task 20 vollständige Prüfung und Reviews
```

## Verbindliche Validator-Schnittstellen

`scripts/validate_ium09.py` stellt genau diese öffentlichen Namen bereit:

```python
class IUM09ValidationError(ValueError):
    pass


def coverage_baseline_fingerprint(entries):
    """Return the canonical SHA-256 fingerprint of ledger before-records."""


def module_structure_fingerprint(module_payload):
    """Return the canonical SHA-256 fingerprint of immutable module fields."""


def validate_coverage_evidence(module_payload, curriculum_contracts):
    """Return evidence contracts keyed by contract id."""


def validate_remediation_ledger(
    remediation_payload,
    curriculum_contracts,
    evidence_contracts,
):
    """Return remediation entries keyed by competency id."""


def validate_remediated_coverage(
    coverage_payload,
    remediation_entries,
    evidence_contracts,
    curriculum_contracts,
):
    """Return the validated set of all coverage competency ids."""


def validate_ium09(
    module_payload,
    coverage_payload,
    remediation_payload,
    curriculum_contracts,
):
    """Validate the complete IUM09 chain and return both record maps."""
```

Die Rückgabe von `validate_ium09` lautet:

```python
{
    "evidenceContracts": evidence_contracts,
    "remediationEntries": remediation_entries,
}
```

## Standardzyklus für jeden Modul-Audit

Jeder der Tasks 4 bis 18 verwendet denselben atomaren Ablauf:

1. Den Quelltext und den bestehenden `reason` jedes genannten Records lesen.
2. Operator, Gegenstand, Kontext, Reichweite und Produktbedingung atomisieren.
3. Gegen zentrale Frage, Lernhandlung, Produkt und Voraussetzungen des Moduls prüfen.
4. Bei fachlicher Tragfähigkeit `covered`, sonst `remain-partial` entscheiden. Keine Quote berücksichtigen.
5. Die Entscheidung zuerst in `AUDITED_DECISIONS` in `tests/test_validate_ium09.py` eintragen und den Repositorytest rot ausführen.
6. Bei `covered` genau einen Evidenzvertrag ergänzen sowie Ledger und Coverageplan synchron ändern.
7. Bei `remain-partial` keinen Evidenzvertrag anlegen und `residualGap.reason`, `risk` und `followUp` mit dem Coverageplan identisch halten.
8. Zieltest, gesamte IUM09-Tests und bestehenden Phase-0-Validator grün ausführen.
9. Nur die vier zusammengehörigen Daten- und Teständerungen dieses Moduls committen.

Die wachsende Auditregistratur beginnt mit den vier zwingend verbleibenden Roadmap-Records:

```python
AUDITED_DECISIONS = {
    "LH26-E-PROG-001": ("IUM-5-CORE-01", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-002": ("IUM-5-CORE-05", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-003": ("IUM-7-CORE-08", "roadmap-level", "remain-partial"),
    "LH26-E-PROG-004": ("IUM-7-CORE-08", "roadmap-level", "remain-partial"),
}
```

Für jede fachlich geprüfte ID wird genau ein Eintrag ergänzt. Der Vollständigkeitstest `set(AUDITED_DECISIONS) == BASELINE_PARTIAL_IDS` wird erst in Task 19 aktiviert, damit jeder Zwischencommit grün bleiben kann.

Ein bestandener Basisvertrag folgt diesem Muster; die beiden natürlichsprachlichen Felder werden aus dem manuellen Audit formuliert und anschließend unverändert von Coverageplan und Ledger referenziert:

```json
{
  "id": "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
  "competencyId": "BMB16-GYM-IK-GM-001",
  "mode": "module-detail",
  "learningAction": "Die Verhaltensregeln der lokalen Medienordnung in einer Geräteerkundung einhalten sowie Eingabe-, Verarbeitungs- und Ausgabekomponenten benennen, ihre Funktion beschreiben und sachgerecht nutzen.",
  "productEvidence": "Kommentierte Gerätefunktionsmatrix mit Regelcheck und je einem beobachteten Eingabe-, Verarbeitungs- und Ausgabeschritt.",
  "productVisibility": "teacher-observable"
}
```

Ein `school-context`-Vertrag ergänzt:

```json
{
  "executionType": "actual-local-use",
  "localConfigurationRequirement": "Die vor Ort freigegebene schulische Anmeldung, Verzeichnisstruktur und Betriebssystemumgebung werden tatsächlich verwendet; Zugangsdaten werden nicht dokumentiert."
}
```

Ein `private-local`-Vertrag ergänzt:

```json
{
  "privacyBoundary": "Das private lokale Artefakt wird nicht erhoben, übertragen, eingesammelt, gespeichert oder bewertet.",
  "nonPersonalFollowUp": "Die Lernenden prüfen einen fiktiven Fall mit denselben fachlichen Kriterien und teilen ausschließlich das nichtpersonale Fallurteil."
}
```

---

### Task 1: Evidenzverträge und unveränderliche Modulstruktur testgetrieben validieren

**Files:**

- Create: `scripts/validate_ium09.py`
- Create: `tests/test_validate_ium09.py`

- [ ] `git status --short --branch` ausführen und bestätigen, dass nur der Plan geändert ist.
- [ ] In `tests/test_validate_ium09.py` minimale Fabriken für einen Kernmodulkandidaten, Curriculumvertrag sowie je einen gültigen `module-detail`-, `school-context`- und `private-local`-Vertrag anlegen.
- [ ] Rote Tests für unbekannte Kompetenz, flexibles Modul, doppelte Vertrags-ID, falsche ID-Bildung, ungültigen Modus und ungültige Sichtbarkeit schreiben.
- [ ] Rote Tests schreiben, die bei `school-context` `executionType: actual-local-use` und `localConfigurationRequirement` erzwingen.
- [ ] Rote Tests schreiben, die bei `private-local` `private-local`-Sichtbarkeit, die exakte Datenschutzgrenze und `nonPersonalFollowUp` erzwingen.
- [ ] Rote Tests für den Modulstrukturfingerprint schreiben: geänderte ID, Jahrgang, Art, Voraussetzung oder `lessonRange` müssen scheitern; reine JSON-Schlüsselreihenfolge darf den Fingerprint nicht ändern.
- [ ] Zieltest rot ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_validate_ium09.py"
```

- [ ] In `scripts/validate_ium09.py` Konstanten und kanonische Fingerprintfunktionen implementieren:

```python
import hashlib
import json
from collections import Counter


BASELINE_COVERAGE_COMMIT = (
    "69c9d4f5504a297289615b4169fc4a9ea6d9b253"
)
BASELINE_PARTIAL_COUNT = 60
BASELINE_RECORD_FINGERPRINT_SHA256 = (
    "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892"
)
BASELINE_MODULE_STRUCTURE_FINGERPRINT_SHA256 = (
    "da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc"
)
CAUSE_CLASS_COUNTS = Counter(
    {
        "module-detail": 39,
        "school-context": 9,
        "private-local": 8,
        "roadmap-level": 4,
    }
)
EVIDENCE_MODES = {"module-detail", "school-context", "private-local"}
PRODUCT_VISIBILITIES = {"shared", "teacher-observable", "private-local"}
TIME_IMPACT_LEVELS = {
    "none-detected",
    "review-required",
    "roadmap-dependent",
}
GRAPH_IMPACT_LEVELS = {"none", "review-required"}
PRIVATE_BOUNDARY_TEXT = (
    "Das private lokale Artefakt wird nicht erhoben, übertragen, "
    "eingesammelt, gespeichert oder bewertet."
)


def _canonical_sha256(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def module_structure_fingerprint(module_payload):
    structure = sorted(
        (
            {
                "id": module["id"],
                "grade": module["grade"],
                "kind": module["kind"],
                "prerequisiteModuleIds": sorted(
                    module["prerequisiteModuleIds"]
                ),
                "lessonRange": module["lessonRange"],
            }
            for module in module_payload["modules"]
        ),
        key=lambda record: record["id"],
    )
    return _canonical_sha256(structure)
```

- [ ] `validate_coverage_evidence` fail-closed implementieren. Eine Vertrags-ID muss exakt `CE-{module_id}-{competency_id}` lauten; nur Kernmodule und im selben Modul registrierte Kompetenzen sind erlaubt.
- [ ] `coverageEvidence` nur als nichtleere Liste akzeptieren, falls das optionale Feld vorhanden ist.
- [ ] `module-detail` auf `shared` oder `teacher-observable`, `school-context` zusätzlich auf reale lokale Ausführung und `private-local` auf die feste Datenschutzgrenze begrenzen.
- [ ] Zieltest grün ausführen.
- [ ] `git diff --check` ausführen.
- [ ] `git fetch --prune` und `git pull --ff-only` ausführen.
- [ ] Commit erstellen:

```powershell
git add scripts/validate_ium09.py tests/test_validate_ium09.py
git commit -m "test: add IUM09 evidence contract validator"
```

### Task 2: Das 60er-Baseline-Ledger testgetrieben anlegen

**Files:**

- Modify: `scripts/validate_ium09.py`
- Modify: `tests/test_validate_ium09.py`
- Create: `roadmap/coverage-remediation.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Die vier Klassifikationsmengen aus Abschnitt 12 der Spezifikation als `frozenset` in `scripts/validate_ium09.py` festschreiben und als `BASELINE_PARTIAL_IDS` vereinigen.
- [ ] Rote Tests für Top-Level-Felder, Baselinecommit, `partialCount`, Fingerprint, exakt 60 eindeutige IDs und die exakte ID-zu-Ursachenklasse-Zuordnung schreiben.
- [ ] Rote Tests für `decision`/`after`, `evidenceContractId`, `residualGap`, Zeit- und Graphfolgen schreiben.
- [ ] Rote Tests erzwingen, dass `roadmap-level` immer `remain-partial`, ohne Vertrag, mit `roadmap-dependent` und ohne Graphänderung bleibt.
- [ ] `coverage_baseline_fingerprint` implementieren:

```python
def coverage_baseline_fingerprint(entries):
    baseline_records = sorted(
        (
            {
                "competencyId": entry["competencyId"],
                "requirementText": entry["requirementText"],
                "before": {
                    "coverageStatus": entry["before"]["coverageStatus"],
                    "semanticAudit": entry["before"]["semanticAudit"],
                    "evidenceModuleId": entry["before"]["evidenceModuleId"],
                    "reason": entry["before"]["reason"],
                },
            }
            for entry in entries
        ),
        key=lambda record: record["competencyId"],
    )
    return _canonical_sha256(baseline_records)
```

- [ ] `roadmap/coverage-remediation.json` mit genau den 60 aktuellen `partial`-Einträgen anlegen. `requirementText` und `before` werden mechanisch und unverändert aus `coverage-plan.json` übernommen.
- [ ] Jeden Eintrag zunächst konsistent als `remain-partial` anlegen; `residualGap` übernimmt `reason`, `risk` und `followUp` unverändert aus dem Coverageplan.
- [ ] Für die vier `roadmap-level`-Records `timeImpact.level: roadmap-dependent` setzen. Für alle übrigen Einträge bis zum manuellen Modulaudit konservativ `review-required` setzen.
- [ ] `graphImpact.level: none` setzen, solange der spätere Fachaudit keine notwendige Strukturänderung erkennt.
- [ ] `changeRationale` beschreibt als Ausgangszustand, dass die Lücke bis zum modulweisen Fachaudit sichtbar bleibt; keine Schließung vorwegnehmen.
- [ ] `validate_remediation_ledger` implementieren und dabei exakten Quelltext, exakten Baseline-Fingerprint, exakte Klassifikationsmenge und referenzielle Konsistenz mit vorhandenen Evidenzverträgen prüfen.
- [ ] Zieltest grün ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_validate_ium09.py"
```

- [ ] Den Fingerprint zusätzlich direkt aus dem neuen Ledger ausgeben und mit der freigegebenen Konstante vergleichen.
- [ ] `git diff --check`, `git fetch --prune` und `git pull --ff-only` ausführen.
- [ ] Commit erstellen:

```powershell
git add scripts/validate_ium09.py tests/test_validate_ium09.py roadmap/coverage-remediation.json
git commit -m "data: establish IUM09 remediation baseline"
```

### Task 3: IUM09 fail-closed in den Phase-0-Einstieg integrieren

**Files:**

- Modify: `scripts/validate_ium09.py`
- Modify: `tests/test_validate_ium09.py`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`
- Modify: `README.md`

- [ ] `git status --short --branch` prüfen.
- [ ] Rote Integrationstests für die Kette Curriculum ↔ Modul ↔ Evidenzvertrag ↔ Ledger ↔ Coverageplan schreiben.
- [ ] Rote Tests schreiben, die Statusänderungen ohne Ledger, Verträge ohne `covered`-Entscheidung, abweichende Restrisiken und neue `evidenceContractId`-Felder in den bisherigen 111 Records ablehnen.
- [ ] Rote Tests schreiben, die jede Änderung am semantisch kanonisierten Modulstrukturfingerprint ablehnen.
- [ ] `validate_remediated_coverage` implementieren. Für `covered` müssen `requirementText`, `learningAction` und `productEvidence` sowohl in `evidence` als auch in `matchRationale` unverändert vorkommen. Für `remain-partial` müssen `reason`, `risk` und `followUp` exakt `residualGap` entsprechen.
- [ ] `validate_ium09` als Orchestrator implementieren und unreferenzierte oder mehrfach referenzierte Evidenzverträge ablehnen.
- [ ] In `scripts/validate_phase0.py` den Import sowohl für Paket- als auch Direktausführung stabil einbinden:

```python
if __package__:
    from .validate_ium09 import validate_ium09
else:
    from validate_ium09 import validate_ium09
```

- [ ] In `main()` die bereits geladenen Payloads wiederverwenden und nach `validate_coverage(...)` ergänzen:

```python
coverage_payload = load_json(root / "roadmap/coverage-plan.json")
validate_coverage(
    coverage_payload,
    required_curriculum_contracts,
    module_contracts,
)
validate_ium09(
    module_candidates,
    coverage_payload,
    load_json(root / "roadmap/coverage-remediation.json"),
    required_curriculum_contracts,
)
```

- [ ] Den vorherigen direkten `load_json(...)`-Aufruf innerhalb von `validate_coverage` durch `coverage_payload` ersetzen; keine doppelte Dateiladung stehen lassen.
- [ ] In `tests/test_validate_phase0.py` die feste `Counter({"covered": 111, "partial": 60})`-Erwartung durch eine aus 111 Altbeständen plus Ledger-`after` berechnete Erwartung ersetzen.
- [ ] Die festen Teilmengen unter `expected_partial_ids` durch alle Ledger-Einträge mit `decision: remain-partial` ersetzen; die vier Progressionsprüfungen bleiben explizit.
- [ ] Roadmap-Textprüfungen für `covered` und `partial` dynamisch aus der Coverage-Datei ableiten, damit Task 19 die tatsächlich auditierte Bilanz dokumentieren kann.
- [ ] In `README.md` Spezifikation, Implementierungsplan und Nacharbeitsledger verlinken; weiterhin klarstellen, dass die Ausgangsbilanz erst durch die modulweisen Audits verändert wird.
- [ ] Zieltests grün ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_validate_ium09.py"
python -B -m unittest discover -s tests -p "test_validate_phase0.py"
python -B scripts/validate_phase0.py
```

- [ ] `git diff --check`, `git fetch --prune` und `git pull --ff-only` ausführen.
- [ ] Commit erstellen:

```powershell
git add scripts/validate_ium09.py tests/test_validate_ium09.py scripts/validate_phase0.py tests/test_validate_phase0.py README.md
git commit -m "feat: integrate IUM09 remediation validation"
```

### Task 4: `IUM-5-CORE-01` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `BMB16-GYM-IK-GM-001`, `BMB16-GYM-IK-GM-003`, `LH26-E-DA-004` |
| `school-context` | `BMB16-GYM-IK-GM-002`, `BMB16-GYM-PK-SK-003`, `LH26-E-DP-001` |
| `roadmap-level` | `LH26-E-PROG-001` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Alle sechs nicht-roadmapweiten Records einzeln nach dem Standardzyklus auditieren; insbesondere tatsächliche lokale Anmeldung, Betriebssystemnutzung und Medienregeln nicht durch Beschreibungen ersetzen.
- [ ] Den roadmapweiten Progressionsrecord ohne Einzelvertrag als `remain-partial` bestätigen.
- [ ] Alle sieben Ergebnisse in `AUDITED_DECISIONS` eintragen.
- [ ] Repositorytest rot ausführen.
- [ ] Ausschließlich für bestandene Records Evidenzverträge unter `IUM-5-CORE-01.coverageEvidence` ergänzen.
- [ ] Ledger und Coverageplan atomar synchronisieren; Zeitfolgen für Betriebssystem-, Geräte- und Regelhandlungen konservativ an IUM10 übergeben.
- [ ] IUM09-Tests und Phase-0-Validator grün ausführen.
- [ ] Diff auf unveränderte Modulstruktur prüfen und committen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-5-CORE-01 coverage gaps"
```

### Task 5: `IUM-5-CORE-07` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `BMB16-GYM-IK-MG-002` |
| `private-local` | `BMB16-GYM-IK-MG-001`, `BMB16-GYM-IK-MG-003`, `BMB16-GYM-PK-RK-001`, `BMB16-GYM-PK-RK-002`, `BMB16-GYM-PK-RK-003`, `LH26-E-DP-003` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Alle sieben Records einzeln auditieren. Für jeden `private-local`-Record prüfen, ob die nichtpersonale Anschlussaufgabe ohne Kenntnis der privaten Notiz funktioniert.
- [ ] Records `remain-partial` lassen, wenn Beschreibung, Vergleich, Bewertung oder Diskussion nur durch Offenlegung eigener Nutzung sichtbar würde.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge mit der exakten Datenschutzgrenze und jeweils einer fachlich passenden nichtpersonalen Anschlussaufgabe ergänzen.
- [ ] Ledger und Coverageplan synchron aktualisieren; keine persönliche Handlungsoption als abzugebendes Produkt formulieren.
- [ ] IUM09-Tests, Phase-0-Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-5-CORE-07 coverage gaps"
```

### Task 6: `IUM-7-CORE-08` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `INF7-16-GYM-IK-IGD-006`, `INF7-16-GYM-PK-AB-005`, `INF7-16-GYM-PK-AB-006`, `INF7-16-GYM-PK-KK-006` |
| `private-local` | `LH26-E-DP-013` |
| `roadmap-level` | `LH26-E-PROG-003`, `LH26-E-PROG-004` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Die vier sichtbaren fachlichen Records auf vollständige Perspektivenbreite, ethische Argumentation, Vielfalt sowie Nutzen-Risiko-Erklärung prüfen.
- [ ] Den privaten Reflexionsrecord nur schließen, wenn eine private Reflexion des eigenen Umgangs möglich ist und ausschließlich ein nichtpersonaler Falschmeldungsfall geteilt wird.
- [ ] Beide Progressionsrecords ohne Einzelvertrag als `remain-partial` bestätigen.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen und alle vier Artefakte synchronisieren.
- [ ] Zeitverdichtung wegen der bereits breiten zentralen Modulhandlung ausdrücklich als `review-required` markieren, ohne `lessonRange` zu ändern.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-7-CORE-08 coverage gaps"
```

### Task 7: `IUM-5-CORE-03` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `BMB16-GYM-PK-RK-004`, `LH26-E-KS-002` |
| `school-context` | `BMB16-GYM-IK-KK-002`, `BMB16-GYM-IK-KK-003`, `BMB16-GYM-PK-HK-003`, `LH26-E-KS-001` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Die vier schulkontextbezogenen Records nur bei tatsächlicher Nutzung eines vor Ort freigegebenen Kanals beziehungsweise Kollaborationswerkzeugs schließen.
- [ ] Sicherstellen, dass keine Zugangsdaten oder privaten Nachrichteninhalte Teil des Produktnachweises werden.
- [ ] Rechtliche und moralische Grenzen sowie gemeinsame Reflexion/Diskussion als getrennte Teilanforderungen auditieren.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-5-CORE-03 coverage gaps"
```

### Task 8: `IUM-7-CORE-03` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `INF7-16-GYM-IK-ALG-003`, `INF7-16-GYM-PK-MI-005`, `INF7-16-GYM-PK-SV-003`, `LH26-E-ALG-007`, `LH26-E-ALG-008`, `LH26-E-ALG-009` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Jeden Record gegen das synchrone Code-, Ablauf- und Zustandstrace auditieren; Variable, Ausdruck, Rückgabe, Datentyp und Daten-/Objektbeziehung nicht ineinander auflösen.
- [ ] Den Einsatz eines grafischen Modellierungswerkzeugs nur schließen, wenn er als tatsächliche Lernhandlung und Produktspur orchestrierbar ist.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Für jede zusätzliche Trace-Komponente den Zeitbedarf als `none-detected` oder `review-required` begründen.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-7-CORE-03 coverage gaps"
```

### Task 9: `IUM-5-CORE-02` auditieren

**Records:** `LH26-E-ID-009` (`module-detail`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Prüfen, ob das Quellendossier Vorwissen sichtbar aktiviert, mit neuen Informationen verknüpft und für die Suchfrage weiterverarbeitet, ohne ein unverbundenes Zusatzprodukt zu erzeugen.
- [ ] Entscheidung in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Je nach Audit exakt einen Vertrag ergänzen oder die Restrisiken präzisieren; Ledger und Coverageplan synchronisieren.
- [ ] Tests und Validator grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-5-CORE-02 coverage gap"
```

### Task 10: `IUM-5-CORE-05` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `LH26-E-ALG-001` |
| `roadmap-level` | `LH26-E-PROG-002` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Prüfen, ob das Identifizieren algorithmisch bestimmter digitaler Systeme die zentrale Algorithmusarbeit trägt und im Produkt nachweisbar ist.
- [ ] Den roadmapweiten Progressionsrecord ohne Einzelvertrag als `remain-partial` bestätigen.
- [ ] Beide Entscheidungen in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Datenartefakte synchron aktualisieren; `roadmap-dependent` für den Progressionsrecord beibehalten.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-5-CORE-05 coverage gaps"
```

### Task 11: `IUM-5-CORE-06` auditieren

**Records:** `BMB16-GYM-IK-PP-002`, `LH26-E-DA-005`, `LH26-E-DA-006`, `LH26-E-DA-008` (alle `module-detail`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Datenschutz neben Urheberrecht, konkrete Textbausteine/Formatierungsoptionen, eine benannte visuelle Objektart und die Analyse einer vorgegebenen Gestaltung einzeln auditieren.
- [ ] Kein generisches Medienprodukt als Beleg für alle vier Records akzeptieren; jede Produktspur muss den jeweiligen Operator sichtbar machen.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Zeitverdichtung für zusätzliche Analyse- oder Produktionsschritte an IUM10 übergeben.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-5-CORE-06 coverage gaps"
```

### Task 12: `IUM-6-CORE-02` auditieren

**Records:** `LH26-E-DP-004`, `LH26-E-DP-006` (beide `module-detail`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Nutzungs-/Rahmenbedingungen exemplarisch sowie spezifische Werbeauswahl als getrennte Mechanismen und Produktspuren auditieren.
- [ ] Keine realen Nutzungsprofile, Konten oder personenbezogenen Werbedaten als Nachweis verlangen.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-6-CORE-02 coverage gaps"
```

### Task 13: `IUM-6-CORE-06` auditieren

**Records:** `LH26-E-KS-014`, `LH26-E-KS-015` (beide `module-detail`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Merkmale, Ursachen/begünstigende Faktoren, Prävention, Hilfsangebote und Meldemöglichkeiten als unterscheidbare Teilanforderungen auditieren.
- [ ] Ausschließlich fiktive Fälle verwenden und keine persönliche Konfliktoffenlegung verlangen.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-6-CORE-06 coverage gaps"
```

### Task 14: `IUM-6-CORE-07` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `LH26-E-DA-009`, `LH26-E-DA-010`, `LH26-E-DA-012` |
| `school-context` | `LH26-E-DA-015` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Kreatives Textprodukt, Analyse einer vorhandenen Wirkungsabsicht und Anwendung von Bedienkonzepten als getrennte Nachweise auditieren.
- [ ] Den schulkontextbezogenen Teilen-Record nur schließen, wenn mindestens zwei tatsächlich genutzte, vor Ort verfügbare und datenschutzkonforme Teilwege dokumentiert werden.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Zeit- und Rechtefolgen an IUM10 beziehungsweise Releaseprüfung übergeben, ohne Modulzeit zu ändern.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-6-CORE-07 coverage gaps"
```

### Task 15: `IUM-7-CORE-01` auditieren

**Records:** `INF7-16-GYM-IK-DC-001`, `INF7-16-GYM-IK-DC-004`, `INF7-16-GYM-IK-DC-005`, `LH26-E-ID-020`, `LH26-E-ID-021` (alle `module-detail`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Alltagsbeispiele, Datenmenge als Bitfolgenlänge, Bit/Byte, Dezimalpräfixe sowie Binärumwandlung 0–255 samt Prinzip einzeln auditieren.
- [ ] Überlappende Bildungsplan- und Lesehilfe-Records getrennt beibehalten und jeweils quellentreu nachweisen.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Verdichtung des bestehenden 6–9-Korridors ausdrücklich an IUM10 übergeben.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-7-CORE-01 coverage gaps"
```

### Task 16: `IUM-7-CORE-04` auditieren

**Records:** `INF7-16-GYM-PK-KK-002`, `INF7-16-GYM-PK-MI-003`, `INF7-16-GYM-PK-SV-002` (alle `module-detail`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Zielgruppenorientierte Fachkommunikation, Abstraktion und aussagekräftige Datei-/Bezeichnernamen als getrennte Entwicklungs- und Produktspuren auditieren.
- [ ] Prüfen, ob die Ergänzungen in Teamplan und kommentiertem Programm integriert bleiben und kein unverbundenes Zusatzprodukt erzeugen.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-7-CORE-04 coverage gaps"
```

### Task 17: `IUM-7-CORE-05` auditieren

**Records:**

| Ursache | Kompetenz-ID |
|---|---|
| `module-detail` | `INF7-16-GYM-IK-IGD-004`, `INF7-16-GYM-PK-AB-002` |
| `school-context` | `INF7-16-GYM-PK-SV-001` |

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Mobile Geräte/Datenträger samt Schutzmaßnahmen und Modell-Realsituations-Vergleich getrennt auditieren.
- [ ] Zielorientiertes Arbeiten im Schulnetz nur bei tatsächlicher lokaler Nutzung schließen; keine Zugangsdaten protokollieren.
- [ ] Ergebnisse in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Bestandene Verträge ergänzen; Ledger und Coverageplan synchron aktualisieren.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-7-CORE-05 coverage gaps"
```

### Task 18: `IUM-7-CORE-10` auditieren

**Records:** `LH26-E-DP-014` (`private-local`)

**Files:** `tests/test_validate_ium09.py`, `roadmap/module-candidates.json`, `roadmap/coverage-remediation.json`, `roadmap/coverage-plan.json`

- [ ] `git status --short --branch` prüfen.
- [ ] Prüfen, ob der Einfluss von Geschlechterrollen und Schönheitsidealen auf die eigene Selbstwahrnehmung privat reflektiert werden kann, während ausschließlich eine nichtpersonale Analyse oder Gegenperspektive sichtbar wird.
- [ ] Bei jeder impliziten Offenlegungs- oder Bewertungsanforderung `remain-partial` wählen.
- [ ] Entscheidung in `AUDITED_DECISIONS` eintragen und Repositorytest rot ausführen.
- [ ] Je nach Audit einen privaten Vertrag ergänzen oder die Restrisiken präzisieren; Ledger und Coverageplan synchronisieren.
- [ ] Tests, Validator und Strukturfingerprint grün ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py roadmap/module-candidates.json roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "data: audit IUM-7-CORE-10 coverage gap"
```

### Task 19: Vollständigkeitstest, Ergebnisbilanz und IUM10-Übergabe

**Files:**

- Modify: `tests/test_validate_ium09.py`
- Modify: `tests/test_validate_phase0.py`
- Modify: `roadmap/module-roadmap.md`
- Modify: `README.md`
- Modify: `roadmap/coverage-remediation.json` only if a cross-artifact inconsistency is found
- Modify: `roadmap/coverage-plan.json` only if a cross-artifact inconsistency is found

- [ ] `git status --short --branch` prüfen.
- [ ] In `tests/test_validate_ium09.py` den finalen Vollständigkeitstest aktivieren:

```python
self.assertEqual(set(AUDITED_DECISIONS), BASELINE_PARTIAL_IDS)
```

- [ ] Zusätzlich prüfen, dass `AUDITED_DECISIONS` Modul, Ursache und Entscheidung jedes Ledgereintrags exakt spiegelt.
- [ ] Finale Summen aus `coverage-plan.json` maschinell berechnen: Gesamtstatus, `enacted`/`orientation`, geschlossene Ausgangslücken und verbleibende Ausgangslücken.
- [ ] Alle `timeImpact`-Einträge mit `review-required` oder `roadmap-dependent` nach Modul gruppieren und auf Vollständigkeit prüfen.
- [ ] In `roadmap/module-roadmap.md` die Ausgangsbilanz 111/60 klar von der auditieren Endbilanz trennen.
- [ ] Eine Tabelle der Ursachenklassen mit Ausgangszahl, geschlossen und verbleibend ergänzen.
- [ ] Eine IUM10-Übergabetabelle mit betroffenen Modulen/Records, `timeImpact.level` und Begründung ergänzen.
- [ ] Modulgraph, Stundenkorridore und Urteile `amber`/`red` unverändert lassen und ausdrücklich keine bessere Jahresfreigabe ableiten.
- [ ] Die vier Roadmap-Progressionsrecords namentlich als verbleibende IUM10-Prüfaufträge aufführen.
- [ ] In `README.md` die tatsächliche Endbilanz, das Ledger und die weiterhin fehlende Zeitfreigabe dokumentieren.
- [ ] Die dynamischen Repositorytests in `tests/test_validate_phase0.py` gegen die neue Roadmapbilanz grün ausführen.
- [ ] Zieltests ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_validate_ium09.py"
python -B -m unittest discover -s tests -p "test_validate_phase0.py"
python -B scripts/validate_phase0.py
```

- [ ] `git diff --check`, `git fetch --prune` und `git pull --ff-only` ausführen.
- [ ] Commit erstellen:

```powershell
git add tests/test_validate_ium09.py tests/test_validate_phase0.py roadmap/module-roadmap.md README.md
git add roadmap/coverage-remediation.json roadmap/coverage-plan.json
git commit -m "docs: publish IUM09 remediation balance"
```

Vor dem Commit mit `git diff --cached --name-only` bestätigen, dass die beiden JSON-Dateien nur dann gestaged sind, wenn tatsächlich eine inhaltlich begründete Konsistenzkorrektur nötig war.

### Task 20: Repository-Gates, Selbstreview, Fachreview und Engineeringreview

**Files:**

- Modify: nur Dateien mit konkret festgestellten Reviewmängeln

- [ ] `git status --short --branch` prüfen.
- [ ] Vollständige Tests ausführen:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_phase0.py
git diff --check
```

- [ ] Alle veränderten `.md`, `.json` und `.py` als UTF-8 strikt decodieren und nach Ersatzzeichen `�` prüfen.
- [ ] Den Baseline-Fingerprint der 60 `before`-Records erneut berechnen und exakt mit `b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892` vergleichen.
- [ ] Den Modulstrukturfingerprint erneut berechnen und exakt mit `da02be74104d88dd9adb0d7927feeab4eea5f65dcc616c5645b0f2145ca4d4fc` vergleichen.
- [ ] Prüfen, dass exakt 171 Coverageeinträge, 60 Ledgereinträge und 31 Modulkandidaten existieren.
- [ ] Prüfen, dass die vier `roadmap-level`-Records weiterhin `partial` sind und keinen Vertrag besitzen.
- [ ] Prüfen, dass alle vorherigen 111 `covered`-Records weiterhin `covered`, ledgerfrei und ohne `evidenceContractId` sind.
- [ ] Prüfen, dass jeder geschlossene Ausgangsrecord genau einen Vertrag und jeder verbleibende Record ein vollständiges Restrisiko besitzt.
- [ ] Prüfen, dass jeder `school-context`-Vertrag tatsächliche lokale Ausführung verlangt und keine Plattform als allgemeine Voraussetzung festschreibt.
- [ ] Prüfen, dass jeder `private-local`-Vertrag die feste Datenschutzgrenze und eine nichtpersonale Anschlussaufgabe besitzt.
- [ ] Fachreview anhand der vier Gates Operator/Gegenstand, Aufgabe/Produkt, Überfrachtung und Datenschutz durchführen und jeden Mangel recordgenau notieren.
- [ ] Engineeringreview anhand der 15 Fehlerfälle aus Abschnitt 8 der Spezifikation durchführen; für jeden gefundenen Validatorblindfleck zuerst einen roten Regressionstest schreiben.
- [ ] Reviewkorrekturen in kleinen separaten Commits umsetzen und die vollständigen Gates erneut ausführen.
- [ ] `git fetch --prune` und `git pull --ff-only` ausführen.
- [ ] Den Branch pushen:

```powershell
git push origin feat/ium-phase0
```

- [ ] Draft-PR #1 um Endbilanz, Testnachweis, verbleibende Lücken und IUM10-Übergabe ergänzen.
- [ ] Erst nach bestandenem Fach- und Engineeringreview IUM09 im Vault als reviewfähig dokumentieren; IUM10 bleibt bis zur gesonderten Nutzerannahme der Endbilanz blockiert.

## Selbstreview des Plans vor Ausführung

- [ ] Jede verbindliche Regel der freigegebenen Spezifikation ist mindestens einem Task oder Global Constraint zugeordnet.
- [ ] Alle 60 IDs erscheinen genau einmal in den 15 Modultasks.
- [ ] Die Taskverteilung ergibt 39/9/8/4.
- [ ] Die vier `roadmap-level`-Records werden nirgends als schließbar beschrieben.
- [ ] Kein Task ändert Modulgraph, Stundenkorridor oder Zahl der Kandidaten.
- [ ] Jeder Datentask beginnt mit einem roten Test und endet mit zielgerichteter sowie integrierter Prüfung.
- [ ] Die Testregistratur bildet fachliche Entscheidungen ab, setzt aber keine Schließungsquote.
- [ ] Keine Codepassage enthält Marker für offene Implementierung, Platzhalterwerte oder eine nur scheinbar implementierte Funktion.
- [ ] Imports, Funktionsnamen und Rückgabeverträge sind in Plan und File Map konsistent.
- [ ] Der Abschluss trennt semantische Coverage ausdrücklich von zeitlicher Umsetzbarkeit.

## Ausführungshandoff

Nach Freigabe dieses Plans gibt es zwei Ausführungsmodi:

1. **Subagent-driven (empfohlen):** Taskweise Umsetzung mit getrenntem Fach- und Engineeringreview. Dieser Modus erfordert eine ausdrückliche Nutzerfreigabe für Subagenten.
2. **Inline mit `superpowers:executing-plans`:** Sequentielle Umsetzung im aktuellen Task mit Checkpoints nach Validator/Ledger, nach den ersten fünf Modulaudits, nach allen Modulaudits und vor dem Push.

Ohne ausdrückliche Delegationsfreigabe wird Modus 2 verwendet.
