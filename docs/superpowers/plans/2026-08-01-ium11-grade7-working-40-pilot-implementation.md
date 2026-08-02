# IUM11 Grade 7 Working 40 Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das freigegebene IUM11-Pilotierungsdesign als vollständig lokales, datensparsames und fail-closed geprüftes Pilotinstrument umsetzen: vier Klasse-7-Clusterpakete, ein Jahrespaket, versionierte Evidenz- und Entscheidungspakete, ein zugängliches Offline-Cockpit und eine reine Status-Empfehlung ohne Mutation des autoritativen Zeitmodells.

**Architecture:** `roadmap/time-model.json` bleibt alleinige Quelle für Modul-, Integrations-, Pilot-, Privacy-, Rückfall- und Statusverträge. `pilot/pilot-protocol.json` ergänzt ausschließlich den operativen Ablauf und wird durch `scripts/validate_ium11.py` gegen einen kanonischen SHA-256-Fingerprint des vollständigen Zeitmodells gebunden. Dieselbe kompilierte Konfiguration speist Python-Validator, synthetische Beispiele und ein Vanilla-JavaScript-Cockpit; Cross-Runtime-Tests verhindern abweichende Schwellenlogik. Reale Evidenzpakete bleiben außerhalb des öffentlichen Repositorys.

**Tech Stack:** JSON, JSON Schema Draft 2020-12, Python 3.11+ Standardbibliothek, `unittest`, Vanilla HTML/CSS/JavaScript ohne Paketmanager oder Laufzeitabhängigkeit, Node.js 18+ ausschließlich für JavaScript-Vertragstests, Git und GitHub CLI.

**Ausführungsbilanz 2026-08-02:** Tasks 1–10 abgeschlossen; Fachreview und Engineering-/Privacy-/Accessibilityreview jeweils `APPROVED AFTER FIXES`; 636/636 Tests und alle vier Repositoryvalidatoren grün. Fixstand `dce092e`; der PR bleibt Draft. Reale Pilotierung, Statusmutation, Release und Phase 1 wurden nicht ausgeführt.

## Global Constraints

- Maßgebliche Spezifikation ist `docs/superpowers/specs/2026-08-01-ium11-grade7-working-40-pilot-design.md`, am 1. August 2026 schriftlich freigegeben.
- Der Implementierungsumfang endet bei Protokoll, Schemas, lokalem Offline-Cockpit, synthetischen Beispielen, Dokumentation, Validatoren und Reviews. Keine Lernmodule, Lernendenplattform, reale Pilotierung, Erhebung realer Daten, Produktstatusänderung, Niveaudifferenzierung oder Phase 1 werden umgesetzt.
- `roadmap/time-model.json` bleibt unverändert und autoritativ. Das operative Protokoll darf keine zweite Status-, Zeit-, Privacy- oder Curriculumswahrheit erzeugen.
- Der Ausgangszustand bleibt exakt `working / conditional / amber / covered / not-started / partial`.
- Vier Clusterbudgets bleiben hart und nicht verrechenbar: `8 / 11 / 11 / 10 UE`; ihre Summe beträgt exakt `40 UE`.
- Additive Rückfälle bleiben exakt `+3 / +2 / +3 / +6 UE`; der maximale Bedarf beträgt `54 UE`. Ein Rückfallwert ist nur eine Bedarfsableitung und niemals ein automatisch verfügbares Angebot.
- Die zehn Kernmodule erscheinen genau einmal in den vier Clustern. Flexible Vertiefungs-, Transfer- und Projektmodule bleiben erhalten, liegen außerhalb der 40 Kern-UE und dürfen nichts kompensieren.
- Die vier Clusterläufe erzeugen zehn Modul-Unterbefunde und vier Integrationsbefunde. Der nachgelagerte Jahreslauf erzeugt den fünften erforderlichen Pilotbefund.
- Ein positiver Minimalpilot trägt nur die dokumentierten Einsatzbedingungen und darf ausschließlich `eligible-for-working-availability-review` empfehlen.
- `reviewed` und `standard` sind gesperrt. `reviewed` erfordert später mindestens eine unabhängige zweite End-to-End-Jahresdurchführung sowie neue Review- und Auftraggebergates.
- Jedes Cluster ist nur `pass`, wenn sein Budget eingehalten ist, alle Pflichtphasen abgeschlossen sind, alle Muss-Kriterien `strong` sind, das Übergabeprodukt vorliegt und funktional weiterverwendet wird, Technik oder gleichwertiger Fallback funktioniert, Privacy positiv ist und keine Lernendenwarnung offen bleibt.
- Pflichtdaten-, Schema-, Versions-, Fingerprint- oder Interpretierbarkeitsfehler führen zu `not-evaluable`. Verletzte Muss-Bedingungen führen zu `fail`. Eine Privacyverletzung ist immer `fail` und blockiert den Export des betroffenen Pakets.
- Der Lernendenimpuls enthält exakt `clarity`, `cognitiveEngagement` und `supportUsefulness` mit den Kategorien `agree`, `partly`, `disagree`, `no-answer`.
- Unter zehn gültigen Antworten wird kein Lernendenaggregat exportiert; nur `suppressed-small-group` bleibt sichtbar. Mindestens ein Drittel `disagree` erzeugt eine offene Entwicklungswarnung und verhindert `pass`.
- Exportiert werden ausschließlich Klassenaggregate. Namen, Initialen, Schul-, Lehrkraft-, Klassen- oder Kursbezeichnungen, exakte Unterrichtsdaten, Freitext, Produkte, Produktlinks, Dateien, Screenshots, Medien, Einzelantworten, individuelle Verläufe, Kennungen, IP-Adressen, Telemetrie, Noten, Rankings, Kompetenzprofile und private Reflexion sind verboten.
- Das Cockpit arbeitet ohne Server, Backend, Konto, Netzwerkzugriff, CDN, externe Schrift, Cookie, `localStorage`, `sessionStorage`, `IndexedDB`, Service Worker oder Telemetrie. Zustand liegt nur im Arbeitsspeicher; Persistenz erfolgt ausschließlich durch bewussten JSON-Download.
- Reale Evidenz- und Entscheidungspakete werden nicht committed. Das Repository enthält ausschließlich Quellcode, Protokoll, Schemas, Anleitungen und offensichtlich synthetische Beispieldaten.
- Das Cockpit verwendet native Formularelemente, eine logische Überschriftenstruktur, sichtbaren Fokus, programmatisch verbundene Labels, ein fokussierbares Fehlerresümee, `aria-live`-Statusmeldungen, mindestens 44 × 44 CSS-Pixel große Bedienziele und WCAG 2.2 AA als technische Baseline.
- Python und JavaScript verwenden dieselben ganzzahligen Schwellen: Lernendenwarnung genau dann, wenn `disagree * 3 >= validResponses`; keine Fließkomma-Rundung.
- Der aktuelle kanonische SHA-256-Fingerprint von `roadmap/time-model.json` unter `json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` ist `873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1`.
- Protokoll-, Tool-, Evidenz- und Entscheidungsschemaversion starten jeweils bei `1` beziehungsweise semantisch bei `1.0.0`.
- Sichtbarer deutscher Text verwendet valides UTF-8 mit Umlauten und `ß`. Technische IDs, Enums, Dateinamen und JSON-Schlüssel bleiben ASCII-stabil.
- Es werden keine neuen Python- oder JavaScript-Abhängigkeiten eingeführt. Alle Repositoryprüfungen müssen mit Python-Standardbibliothek und vorhandenem Node.js laufen.
- Vor jedem Task `git status --short --branch` prüfen. Vor jedem Commit und Push `git fetch --prune` sowie `git pull --ff-only` ausführen. Bei Fehlern nicht committen oder pushen.
- Jeder Umsetzungstask folgt Red–Green–Refactor: zielgenauer fehlschlagender Test, bestätigter roter Lauf, minimale Implementierung, fokussierter grüner Lauf, vollständige Regression, kleiner Commit.
- Kein Force-Push, kein History-Rewrite und kein automatischer Merge des bestehenden Draft-PRs.

---

## File Map

| Pfad | Aktion | Verantwortung |
|---|---|---|
| `pilot/pilot-protocol.json` | Create | Operative IUM11-Version, Privacygrenzen, Schwellen, Lernendenimpuls, vier Clusterbindungen und Jahresbindung |
| `pilot/schemas/evidence-package.schema.json` | Create | Geschlossenes öffentliches Schema für Cluster- und Jahres-Evidenzpakete |
| `pilot/schemas/decision-package.schema.json` | Create | Geschlossenes öffentliches Schema für die validierte Zusammenführung und reine Statusempfehlung |
| `pilot/cockpit/index.html` | Create | Semantische Offline-Oberfläche, Eingabe-, Prüf-, Import- und Exportfluss |
| `pilot/cockpit/assets/styles.css` | Create | Zugängliches responsives Layout, Fokus, Kontrast und Touchziele |
| `pilot/cockpit/assets/app.js` | Create | Reine Ableitungsfunktionen plus Browsersteuerung ohne Persistenz oder Netzwerk |
| `pilot/cockpit/assets/protocol.js` | Create/generated | Deterministisch kompilierter, fingerprintgebundener Cockpitvertrag |
| `pilot/docs/teacher-guide.md` | Create | Bereitschaftsgate, Durchführung, lokale Aggregation, Export, Aufbewahrung und Wiederholung |
| `pilot/docs/review-guide.md` | Create | Fach-, Engineering-/Privacy- und Auftraggeberprüfung samt Aussagegrenzen |
| `pilot/examples/synthetic-cluster-pass.json` | Create | Positiver Daten-und-Codierungs-Cluster ohne Personenbezug |
| `pilot/examples/synthetic-cluster-programming-pass.json` | Create | Positiver Programmiercluster für vollständige Entscheidungstests |
| `pilot/examples/synthetic-cluster-net-security-pass.json` | Create | Positiver Netz-/Sicherheitscluster für vollständige Entscheidungstests |
| `pilot/examples/synthetic-cluster-data-media-society-pass.json` | Create | Positiver Daten-/Medien-/Gesellschaftscluster für vollständige Entscheidungstests |
| `pilot/examples/synthetic-cluster-fail.json` | Create | Negativer Cluster mit Budget- oder Muss-Kriterienfehler |
| `pilot/examples/synthetic-annual-pass.json` | Create | Positiver vollständiger 40-UE-Jahresbefund |
| `pilot/examples/synthetic-decision-eligible.json` | Create | Erwartetes Entscheidungspaket aus fünf positiven Stufen |
| `scripts/validate_ium11.py` | Create | Kanonische Fingerprints, Protokoll-, Paket-, Status-, Fallback- und Repositoryvalidierung |
| `scripts/build_ium11_cockpit.py` | Create | Deterministische Kompilierung des Protokolls in `protocol.js` |
| `tests/test_validate_ium11.py` | Create | Unit-, Schema-, Mutations-, Privacy-, Status- und Repositorytests |
| `tests/test_ium11_cockpit_contract.py` | Create | Build-, JavaScript-, Offline-, HTML-, Accessibility- und Cross-Runtime-Vertragstests |
| `scripts/validate_phase0.py` | Modify | IUM11 nach gültigem IUM10/IUM09-Stand genau einmal in die Gesamtkette aufnehmen |
| `tests/test_validate_phase0.py` | Modify | Aufrufreihenfolge und gemeinsame Eingaben der erweiterten Kette regressionssichern |
| `README.md` | Modify | Pilotinstrument, Statusgrenze, lokale Nutzung und Validierungsbefehle veröffentlichen |
| `docs/superpowers/plans/2026-08-01-ium11-grade7-working-40-pilot-implementation.md` | Track | Taskfortschritt über Checkboxen |
| `.superpowers/sdd/2026-08-01-ium11-grade7-working-40-pilot-implementation/` | Ignore/working | Taskbriefs, Diffs und getrennte Reviewberichte; keine Produktquelle |

Nicht verändern:

```text
roadmap/time-model.json
roadmap/module-candidates.json
roadmap/coverage-plan.json
roadmap/coverage-remediation.json
curriculum/
scripts/validate_ium09.py
tests/test_validate_ium09.py
scripts/validate_ium10.py
tests/test_validate_ium10.py
```

## Dependency Flow

```text
Task 1 Protokoll und Fingerprint
└── Task 2 Evidenzschema und fail-closed Paketgrenze
    └── Task 3 Clusterableitung, Schwellen und Rückfälle
        └── Task 4 Jahres- und Entscheidungspaket
            └── Task 5 synthetische Konformitätsbeispiele
                └── Task 6 kompilierter Cockpitvertrag und JavaScript-Domänenkern
                    └── Task 7 zugängliche Offline-Oberfläche
                        └── Task 8 Anleitungen, README und Gesamtvalidator
                            ├── Task 9 unabhängiges Fachreview
                            └── Task 10 Engineering-/Privacy-/Accessibilityreview und Handoff
```

## Spec Coverage Matrix

| Spezifikationsabschnitt | Umsetzungstasks |
|---|---|
| 1–2 Zweck und Grundentscheidungen | Global Constraints, Tasks 1, 4, 8 |
| 3 normative und didaktische Grundlage | Tasks 1, 8, 9 |
| 4 Scope und Nicht-Ziele | Global Constraints, File Map, Tasks 8–10 |
| 5 Systemarchitektur und Autoritätsgrenzen | Tasks 1, 4, 6, 8 |
| 6 Bereitschaft, vier Cluster, Wiederholung, Jahrespilot | Tasks 1, 3, 4, 7, 8 |
| 7 vier Evidenzspuren, Klassenbänder, Lernendenimpuls, Privacy | Tasks 2, 3, 5, 6, 7 |
| 8 Paketmodell, Offlinefluss, Fingerprints, Retention | Tasks 2, 4, 5, 6, 7, 8 |
| 9 Cluster-/Jahresstatus, Rückfälle und Empfehlung | Tasks 3, 4, 6 |
| 10 Rollen | Tasks 8–10 |
| 11 technische Artefakte | File Map, Tasks 1–8 |
| 12 Wiederverwendung für Klassen 5/6 | Tasks 1, 6, 9 |
| 13 Fehlerbehandlung | Tasks 2–4, 7, 10 |
| 14 Test- und Validierungsstrategie | sämtliche Tasks, insbesondere 5, 6, 8, 10 |
| 15 WU-Check | Tasks 8 und 9 |
| 16 Risiken und Gegenmaßnahmen | Global Constraints, Tasks 2, 7, 8, 10 |
| 17 Akzeptanzkriterien | Final Acceptance Checklist |
| 18 Freigabefolge | Task 10 und anschließendes Nutzerhandoff |

## Verbindliche öffentliche Python-Schnittstellen

`scripts/validate_ium11.py` stellt genau diese Funktionen bereit:

```python
class IUM11ValidationError(ValueError):
    pass


def canonical_sha256(payload: object) -> str:
    """Return lowercase SHA-256 for canonical UTF-8 JSON."""


def validate_pilot_protocol(protocol: dict, time_model: dict) -> dict:
    """Validate and return the compiled, fingerprint-bound pilot protocol."""


def evaluate_learner_pulse(payload: dict, protocol: dict) -> dict:
    """Return suppression state and deterministic development warnings."""


def validate_evidence_package(
    payload: dict,
    protocol: dict,
    time_model: dict,
) -> dict:
    """Validate one closed cluster or annual evidence package."""


def derive_cluster_result(payload: dict, cluster: dict, protocol: dict) -> dict:
    """Return result, module/integration sub-results, warnings and fallback units."""


def derive_annual_result(
    annual_payload: dict,
    cluster_packages: list[dict],
    protocol: dict,
) -> dict:
    """Return the fail-closed end-to-end result for the 40-unit path."""


def build_decision_package(
    evidence_packages: list[dict],
    protocol: dict,
    time_model: dict,
) -> dict:
    """Build a non-mutating decision package from exactly five current packages."""


def validate_decision_package(
    payload: dict,
    protocol: dict,
    time_model: dict,
) -> dict:
    """Validate a closed decision package and its derived recommendation."""


def validate_ium11(
    time_model: dict,
    ium10_result: dict,
    protocol: dict,
    evidence_schema: dict,
    decision_schema: dict,
    example_packages: list[dict],
    cockpit_root: Path,
) -> dict:
    """Validate the complete in-memory IUM11 contract."""


def validate_ium11_repository(root: Path) -> dict:
    """Load and validate the complete repository-level IUM11 contract."""
```

`scripts/build_ium11_cockpit.py` stellt bereit:

```python
def compile_cockpit_contract(protocol: dict, time_model: dict) -> dict:
    """Resolve contract references without creating a second status truth."""


def render_protocol_js(compiled_contract: dict) -> str:
    """Return deterministic window.IUM11_PROTOCOL JavaScript."""


def build_cockpit_contract(
    root: Path,
    output_path: Path | None = None,
) -> Path:
    """Write pilot/cockpit/assets/protocol.js and return its path."""
```

## Verbindliche JavaScript-Schnittstelle

`pilot/cockpit/assets/app.js` exportiert im Browser als `window.IUM11` und unter Node.js über `module.exports`:

```javascript
{
  evaluateLearnerPulse,
  deriveClusterResult,
  deriveAnnualResult,
  validateEvidencePackage,
  createPackageId,
  createEvidencePackage,
  serializePackage,
  parsePackage
}
```

Die reinen Funktionen akzeptieren und liefern ausschließlich JSON-kompatible Werte. Browserinitialisierung läuft nur, wenn `document` vorhanden ist.

Signaturen und Rückgaben sind verbindlich:

```javascript
evaluateLearnerPulse(payload, protocol) -> {status, warnings}
deriveClusterResult(payload, cluster, protocol) -> {result, moduleResults, integrationResult, developmentWarnings, fallbackDeltaUnits}
deriveAnnualResult(annualPayload, clusterPackages, protocol) -> {result, actualUnits, availabilityGateResults}
validateEvidencePackage(payload, protocol) -> validatedPayload
createPackageId() -> string matching `^PKG-[0-9a-f-]{36}$` with RFC-4122 version 4/variant bits
createEvidencePackage(scopeId, formValue, protocol) -> validatedPayload
serializePackage(payload) -> prettyPrintedJsonWithFinalNewline
parsePackage(sourceText, protocol) -> validatedPayload
```

## Verbindliche Paketformen

Ein Evidenzpaket besitzt ausschließlich diese Top-Level-Felder:

```text
schemaVersion, packageType, packageId, protocolVersion, protocolFingerprint,
toolVersion, timeModelFingerprint, scopeType, scopeId, context,
deliveryTimeEvidence, learningQualityEvidence, learnerPulseEvidence,
technicalPrivacyEvidence, result, developmentWarnings, retentionClass
```

Ein Entscheidungspaket besitzt ausschließlich:

```text
schemaVersion, packageType, packageId, protocolVersion, protocolFingerprint,
toolVersion, timeModelFingerprint, sourcePackageIds, pilotResults,
moduleResults, integrationResults, availabilityGateResults,
timeAndFallbackSummary,
technicalPrivacySummary, developmentWarnings, statementBoundary,
recommendation, reviewStatus, retentionClass
```

Erlaubte Kontextfelder sind genau:

```text
schoolYear, term, classSizeBand, deviceClass, browserFamily, networkMode
```

`schoolYear` folgt `^[0-9]{4}-[0-9]{2}$`; `term` ist `first-half`, `second-half` oder `full-year`; `classSizeBand` ist `under-10`, `10-19`, `20-29` oder `30-plus`. Geräte-, Browser- und Netzwerkwerte stammen ausschließlich aus Protokoll-Enums.

## Verbindliche verschachtelte Evidenzverträge

Für ein Cluster besitzt `deliveryTimeEvidence` genau:

```text
plannedUnits, actualUnits, completedPhaseIds, requiredLearningPhasesCompleted,
fallbackActivated, technicalStartupMinutes, supportDemandBand,
externalDisruptionCode
```

Für den Jahreslauf kommen genau `clusterOrder` und `clusterActualUnits` hinzu. `clusterActualUnits` enthält vier geordnete Objekte mit ausschließlich `clusterId` und `actualUnits`. `plannedUnits`, `actualUnits` und `technicalStartupMinutes` sind nichtnegative echte Integer; `fallbackActivated` und `requiredLearningPhasesCompleted` sind echte Booleans. `supportDemandBand` ist `low`, `medium` oder `high`; `externalDisruptionCode` ist `none` oder `interpretability-lost`.

`learningQualityEvidence` besitzt in beiden Scopes ausschließlich:

```text
moduleResults, integrationResults
```

Ein Modulresultat besitzt `pilotAssignmentId`, `moduleId`, `criteria`, `result`. Ein Integrationsresultat besitzt `pilotAssignmentId`, `integrationContractId`, `criteria`, `handoffProductPresent`, `handoffReused`, `result`. Ein Kriterium besitzt ausschließlich `criterionId` und `band`. Clusterpakete enthalten genau die zwei beziehungsweise drei eigenen Module und genau eine Integration; das Jahrespaket enthält erneut alle zehn Module und alle vier Integrationen in Protokollreihenfolge.

`technicalPrivacyEvidence` besitzt genau:

```text
technicalFunction, fallbackEquivalentLearningFunction, problemCode,
severity, privacyGate
```

`technicalFunction` und `privacyGate` sind `pass` oder `fail`; `fallbackEquivalentLearningFunction` ist Boolean; `problemCode` ist `none`, `startup`, `execution`, `import` oder `export`; `severity` ist `none`, `minor`, `major` oder `blocking`. Ein serialisiertes Paket mit `privacyGate: fail` wird zurückgewiesen, weil die Privacyverletzung den Export blockiert. Die reine Entwurfsableitung im Cockpit zeigt dafür `fail`, bevor ein Exportversuch möglich ist.

Ein Element von `developmentWarnings` besitzt ausschließlich `id`, `itemId`, `status`; `status` ist konstant `open`. Die Liste wird aus dem Lernendenimpuls abgeleitet und muss dem neu berechneten Wert bytegleich entsprechen.

## Verbindliche verschachtelte Entscheidungsverträge

- `pilotResults`: fünf geordnete Objekte mit `scopeId`, `packageId`, `result`.
- `moduleResults`: zehn geordnete Objekte mit `moduleId`, `pilotAssignmentId`, `result`.
- `integrationResults`: vier geordnete Objekte mit `integrationContractId`, `pilotAssignmentId`, `result`, `fallbackDeltaUnits`.
- `availabilityGateResults`: ausschließlich `capacity`, `integration`, `technical`, `privacy`, `pilot`; jeder Wert ist `passed` oder `failed`.
- `timeAndFallbackSummary`: ausschließlich `plannedUnits`, `actualUnits`, `fallbackUnits`, `requiredUnits`; dabei gilt `requiredUnits = 40 + fallbackUnits` und `fallbackUnits <= 14`.
- `technicalPrivacySummary`: ausschließlich `technical`, `privacy`; beide Werte sind `pass` oder `fail`.
- `developmentWarnings`: deduplizierte, nach `id` sortierte Warnungen in derselben geschlossenen Form wie im Evidenzpaket.

Die `packageId` eines Entscheidungspakets wird deterministisch als UUIDv5 aus der sortierten Folge seiner fünf zufälligen Quellpaket-IDs erzeugt. Dadurch bleibt der Build eines synthetischen Entscheidungspakets byteidentisch, ohne eine Personen- oder Institutionszuordnung einzuführen.

## Task 1: Protokoll, kanonischen Fingerprint und Repositorygrenze anlegen

**Files:**
- Create: `pilot/pilot-protocol.json`
- Create: `scripts/validate_ium11.py`
- Create: `tests/test_validate_ium11.py`

**Interfaces:**
- Consumes: `roadmap/time-model.json`, `scripts.validate_ium10.validate_ium10_repository`
- Produces: `canonical_sha256`, `validate_pilot_protocol`, `validate_ium11_repository`, kompilierter Protokollvertrag mit `protocolFingerprint`

- [x] **Step 1: Failing Tests für Fingerprint, Protokollform und vier Cluster schreiben**

```python
def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class IUM11ProtocolContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(cls.root / "roadmap/time-model.json")
        cls.protocol = load_json(cls.root / "pilot/pilot-protocol.json")

    def test_time_model_fingerprint_is_canonical_and_pinned(self):
        self.assertEqual(
            canonical_sha256(self.time_model),
            "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1",
        )
        self.assertEqual(
            self.protocol["timeModelFingerprint"],
            canonical_sha256(self.time_model),
        )

    def test_protocol_binds_exact_cluster_sequence(self):
        compiled = validate_pilot_protocol(self.protocol, self.time_model)
        self.assertEqual(
            [
                (cluster["id"], cluster["moduleIds"], cluster["budgetUnits"], cluster["fallbackDeltaUnits"])
                for cluster in compiled["clusters"]
            ],
            [
                ("CLUSTER-7-DATA-CODING", ["IUM-7-CORE-01", "IUM-7-CORE-02"], 8, 3),
                ("CLUSTER-7-PROGRAMMING", ["IUM-7-CORE-03", "IUM-7-CORE-04"], 11, 2),
                ("CLUSTER-7-NET-SECURITY", ["IUM-7-CORE-05", "IUM-7-CORE-06", "IUM-7-CORE-07"], 11, 3),
                ("CLUSTER-7-DATA-MEDIA-SOCIETY", ["IUM-7-CORE-08", "IUM-7-CORE-09", "IUM-7-CORE-10"], 10, 6),
            ],
        )

    def test_protocol_keeps_status_and_recommendation_boundaries(self):
        compiled = validate_pilot_protocol(self.protocol, self.time_model)
        self.assertEqual(compiled["status"], "working")
        self.assertEqual(
            compiled["allowedRecommendation"],
            "eligible-for-working-availability-review",
        )
        self.assertEqual(compiled["forbiddenRecommendations"], ["reviewed", "standard"])
```

- [x] **Step 2: Fokussierten Test ausführen und roten Zustand bestätigen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11ProtocolContractTests -v
```

Expected: Import- oder Dateifehler, weil IUM11-Protokoll und Validator noch fehlen.

- [x] **Step 3: `pilot-protocol.json` mit exakt freigegebenen IDs und Schwellen anlegen**

Der Top-Level-Vertrag lautet:

```json
{
  "schemaVersion": 1,
  "id": "IUM11-GRADE-7-WORKING-40-PILOT",
  "status": "working",
  "protocolVersion": "1.0.0",
  "toolVersion": "1.0.0",
  "timeModelFingerprintAlgorithm": "sha256-canonical-json-v1",
  "timeModelFingerprint": "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1",
  "variantId": "GRADE-7-WORKING-40",
  "availabilityContractId": "AVAIL-GRADE-7-WORKING-40",
  "allowedRecommendation": "eligible-for-working-availability-review",
  "forbiddenRecommendations": ["reviewed", "standard"],
  "minimumLearnerResponses": 10,
  "learnerWarningRatio": {"numerator": 1, "denominator": 3},
  "bands": ["strong", "mixed", "weak"],
  "results": ["pass", "fail", "not-evaluable"],
  "prohibitedFieldNames": [
    "studentName", "studentInitials", "schoolName", "teacherName",
    "className", "courseName", "email", "accountId", "learnerId",
    "lessonDate", "timetable", "freeText", "studentProduct",
    "studentProductUrl", "filePath", "screenshot", "photo", "audio",
    "video", "individualResponse", "responseSequence", "deviceId",
    "networkId", "browserId", "ipAddress", "telemetry",
    "privateReflection", "grade", "ranking", "competenceProfile",
    "automatedPersonalAssessment"
  ],
  "evidenceTracks": [
    "deliveryTimeEvidence",
    "learningQualityEvidence",
    "learnerPulseEvidence",
    "technicalPrivacyEvidence"
  ],
  "learnerPulseItems": [
    {"id": "clarity", "prompt": "Ich wusste, was ich fachlich bearbeiten sollte."},
    {"id": "cognitiveEngagement", "prompt": "Ich musste erklären, prüfen, testen oder begründen – nicht nur klicken oder abschreiben."},
    {"id": "supportUsefulness", "prompt": "Die Hilfen halfen mir weiter, ohne die Lösung vorzugeben."}
  ],
  "contextEnums": {
    "term": ["first-half", "second-half", "full-year"],
    "classSizeBand": ["under-10", "10-19", "20-29", "30-plus"],
    "deviceClass": ["desktop", "laptop", "tablet", "mixed"],
    "browserFamily": ["chromium", "firefox", "safari", "mixed"],
    "networkMode": ["offline", "school-network", "local-fallback"]
  }
}
```

Ergänze vier `clusters` in der oben getesteten Reihenfolge. Jeder Cluster besitzt `id`, `order`, `pilotAssignmentId`, `integrationContractId`, `moduleIds`, `modulePilotAssignmentIds`, `budgetUnits`, `fallbackDeltaUnits` und `handoffCriterionId`. Die Bindungen lauten:

```python
CLUSTER_BINDINGS = [
    ("CLUSTER-7-DATA-CODING", "PILOT-INT-7-DATA-CODING", "INT-7-DATA-CODING", ["IUM-7-CORE-01", "IUM-7-CORE-02"], 8, 3),
    ("CLUSTER-7-PROGRAMMING", "PILOT-INT-7-PROGRAMMING", "INT-7-PROGRAMMING", ["IUM-7-CORE-03", "IUM-7-CORE-04"], 11, 2),
    ("CLUSTER-7-NET-SECURITY", "PILOT-INT-7-NET-SECURITY", "INT-7-NET-SECURITY", ["IUM-7-CORE-05", "IUM-7-CORE-06", "IUM-7-CORE-07"], 11, 3),
    ("CLUSTER-7-DATA-MEDIA-SOCIETY", "PILOT-INT-7-DATA-MEDIA-SOCIETY", "INT-7-DATA-MEDIA-SOCIETY", ["IUM-7-CORE-08", "IUM-7-CORE-09", "IUM-7-CORE-10"], 10, 6),
]
```

`annualPilot` bindet `ANNUAL-7-WORKING-40`, `PILOT-GRADE-7-WORKING-40`, `GRADE-7-WORKING-40`, alle vier Cluster-IDs und `budgetUnits: 40`.

Die exakte Top-Level-Feldmenge ist:

```python
PROTOCOL_FIELDS = {
    "schemaVersion", "id", "status", "protocolVersion", "toolVersion",
    "timeModelFingerprintAlgorithm", "timeModelFingerprint", "variantId",
    "availabilityContractId", "allowedRecommendation",
    "forbiddenRecommendations", "minimumLearnerResponses",
    "learnerWarningRatio", "bands", "results", "prohibitedFieldNames",
    "evidenceTracks", "learnerPulseItems", "contextEnums", "clusters",
    "annualPilot",
}
```

- [x] **Step 4: Kanonische Fingerprint- und geschlossene Protokollvalidierung implementieren**

```python
def canonical_sha256(payload: object) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IUM11ValidationError(message)


def _require_exact_fields(payload: dict, fields: set[str], label: str) -> None:
    _require(isinstance(payload, dict), f"{label} must be an object")
    _require(set(payload) == fields, f"{label} fields differ from contract")
```

`validate_pilot_protocol` prüft exakte Top-Level-Felder, Versionen, Status, vollständigen Zeitmodellfingerprint, die vier Cluster in Reihenfolge, zehn einmalige Kernmodule, 15 vorhandene Pilotaufträge, Budgets, Rückfälle, Lernendenfragen, Enums, Jahresbindung und Verbot von `reviewed`/`standard`. Es löst für jedes Modul ausschließlich referenziell `centralLearningAction`, `centralLearningProduct` und die sieben `working-40`-Phasen auf; für jede Integration löst es `preservedLearningActions` und `preservedProductAndCurriculumEvidence` auf.

Jeder kompilierte Cluster ergänzt genau diese abgeleiteten Strukturen:

```python
{
    "modules": [
        {
            "moduleId": "IUM-7-CORE-01",
            "pilotAssignmentId": "PILOT-IUM-7-CORE-01",
            "requiredPhaseIds": [
                "orientation-challenge", "activate-prior-knowledge",
                "build-concept", "guided-practice",
                "independent-action-product", "review-revise-transfer",
                "shared-consolidation",
            ],
            "criteria": [
                {"criterionId": "CRIT-IUM-7-CORE-01-ACTION", "sourceField": "centralLearningAction", "kind": "must"},
                {"criterionId": "CRIT-IUM-7-CORE-01-PRODUCT", "sourceField": "centralLearningProduct", "kind": "must"},
            ],
        }
    ],
    "integration": {
        "integrationContractId": "INT-7-DATA-CODING",
        "pilotAssignmentId": "PILOT-INT-7-DATA-CODING",
        "criteria": [
            {"criterionId": "CRIT-INT-7-DATA-CODING-HANDOFF-ACTIONS", "sourceField": "preservedLearningActions", "kind": "must"},
            {"criterionId": "CRIT-INT-7-DATA-CODING-HANDOFF-EVIDENCE", "sourceField": "preservedProductAndCurriculumEvidence", "kind": "must"},
        ],
    },
}
```

Die übrigen Module und Integrationen verwenden dieselbe algorithmische ID-Bildung mit ihren konkreten kanonischen IDs. Der kompilierte Rückgabewert ergänzt `protocolFingerprint = canonical_sha256(protocol)`, `clustersById = {cluster["id"]: cluster for cluster in clusters}` und `annualPilot`; er mutiert weder Eingaben noch Zeitmodell.

- [x] **Step 5: Repositoryeinstieg implementieren**

```python
def validate_ium11_repository(root: Path) -> dict:
    root = Path(root)
    time_model = _load_json(root / "roadmap/time-model.json")
    ium10_result = validate_ium10_repository(root)
    protocol = _load_json(root / "pilot/pilot-protocol.json")
    compiled = validate_pilot_protocol(protocol, time_model)
    return {"ium10": ium10_result, "protocol": compiled}
```

Die CLI akzeptiert `--root`, gibt Fehler als `IUM11 repository validation failed: ...` auf `stderr` aus und meldet im grünen Zustand Protokollversion, vier Cluster, zehn Module und einen Jahrespfad.

- [x] **Step 6: Fokussierte und vollständige Regression ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11ProtocolContractTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
```

Expected: alle neuen Protokolltests und alle bisherigen 482 Tests grün; CLI meldet `4 clusters, 10 module bindings, and 1 annual pilot`.

- [x] **Step 7: Task-Commit erstellen**

```powershell
git add pilot/pilot-protocol.json scripts/validate_ium11.py tests/test_validate_ium11.py
git commit -m "feat: add ium11 pilot protocol"
```

## Task 2: Geschlossenes Evidenzschema und fail-closed Paketgrenze implementieren

**Files:**
- Create: `pilot/schemas/evidence-package.schema.json`
- Modify: `scripts/validate_ium11.py`
- Modify: `tests/test_validate_ium11.py`

**Interfaces:**
- Consumes: kompilierter Protokollvertrag aus Task 1
- Produces: `evaluate_learner_pulse`, `validate_evidence_package`, geschlossenes Cluster-/Jahresschema

- [x] **Step 1: Failing Tests für Felder, Privacy, Unterdrückung und Warnung schreiben**

Lege oberhalb der Testklasse einen vollständig aus dem kompilierten Protokoll erzeugten Factorywert an:

```python
def reported_pulse(agree=8, partly=2, disagree=1, no_answer=1):
    count = agree + partly + disagree + no_answer
    return {
        "status": "reported",
        "classResponseCount": count,
        "items": [
            {"itemId": item_id, "agree": agree, "partly": partly, "disagree": disagree, "noAnswer": no_answer}
            for item_id in ("clarity", "cognitiveEngagement", "supportUsefulness")
        ],
    }


def valid_cluster_package(scope_id="CLUSTER-7-DATA-CODING"):
    root = Path(__file__).resolve().parents[1]
    time_model = load_json(root / "roadmap/time-model.json")
    protocol = validate_pilot_protocol(
        load_json(root / "pilot/pilot-protocol.json"),
        time_model,
    )
    cluster = protocol["clustersById"][scope_id]
    completed_phases = sorted({
        phase_id
        for module in cluster["modules"]
        for phase_id in module["requiredPhaseIds"]
    })
    return {
        "schemaVersion": 1,
        "packageType": "cluster-evidence",
        "packageId": f"PKG-{uuid.uuid4()}",
        "protocolVersion": protocol["protocolVersion"],
        "protocolFingerprint": protocol["protocolFingerprint"],
        "toolVersion": protocol["toolVersion"],
        "timeModelFingerprint": protocol["timeModelFingerprint"],
        "scopeType": "cluster",
        "scopeId": scope_id,
        "context": {"schoolYear": "2026-27", "term": "first-half", "classSizeBand": "20-29", "deviceClass": "mixed", "browserFamily": "chromium", "networkMode": "offline"},
        "deliveryTimeEvidence": {"plannedUnits": cluster["budgetUnits"], "actualUnits": cluster["budgetUnits"], "completedPhaseIds": completed_phases, "requiredLearningPhasesCompleted": True, "fallbackActivated": False, "technicalStartupMinutes": 3, "supportDemandBand": "low", "externalDisruptionCode": "none"},
        "learningQualityEvidence": {
            "moduleResults": [
                {"pilotAssignmentId": module["pilotAssignmentId"], "moduleId": module["moduleId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in module["criteria"]], "result": "pass"}
                for module in cluster["modules"]
            ],
            "integrationResults": [{"pilotAssignmentId": cluster["integration"]["pilotAssignmentId"], "integrationContractId": cluster["integration"]["integrationContractId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in cluster["integration"]["criteria"]], "handoffProductPresent": True, "handoffReused": True, "result": "pass"}],
        },
        "learnerPulseEvidence": reported_pulse(),
        "technicalPrivacyEvidence": {"technicalFunction": "pass", "fallbackEquivalentLearningFunction": False, "problemCode": "none", "severity": "none", "privacyGate": "pass"},
        "result": "pass",
        "developmentWarnings": [],
        "retentionClass": "until-decision",
    }
```

```python
class IUM11EvidencePackageTests(unittest.TestCase):
    def test_unknown_or_personal_fields_fail_closed(self):
        for field, value in [
            ("studentName", "Ada"),
            ("schoolName", "Beispielgymnasium"),
            ("freeText", "Beobachtung"),
            ("studentProductUrl", "file:///produkt.txt"),
            ("ipAddress", "192.0.2.1"),
        ]:
            payload = valid_cluster_package()
            payload[field] = value
            with self.subTest(field=field):
                with self.assertRaisesRegex(IUM11ValidationError, "fields|prohibited"):
                    validate_evidence_package(payload, self.protocol, self.time_model)

    def test_small_group_exports_no_counts(self):
        payload = valid_cluster_package()
        payload["learnerPulseEvidence"] = {"status": "suppressed-small-group"}
        validated = validate_evidence_package(payload, self.protocol, self.time_model)
        self.assertEqual(validated["learnerPulseEvidence"], {"status": "suppressed-small-group"})

    def test_one_third_disagree_creates_warning(self):
        pulse = reported_pulse(agree=6, partly=0, disagree=3, no_answer=1)
        result = evaluate_learner_pulse(pulse, self.protocol)
        self.assertEqual(result["warnings"][0]["itemId"], "clarity")
        self.assertEqual(result["warnings"][0]["status"], "open")
```

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11EvidencePackageTests -v
```

Expected: fehlendes Schema beziehungsweise fehlende Auswertungsfunktionen.

- [x] **Step 3: JSON Schema Draft 2020-12 als geschlossenen Vertrag anlegen**

Das Schema verwendet:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://h4r7w16.github.io/ium-lernwerk/pilot/schemas/evidence-package.schema.json",
  "title": "IUM11 evidence package",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion", "packageType", "packageId", "protocolVersion",
    "protocolFingerprint", "toolVersion", "timeModelFingerprint",
    "scopeType", "scopeId", "context", "deliveryTimeEvidence",
    "learningQualityEvidence", "learnerPulseEvidence",
    "technicalPrivacyEvidence", "result", "developmentWarnings",
    "retentionClass"
  ]
}
```

Definiere `oneOf` für `cluster-evidence`/`cluster` und `annual-evidence`/`annual`. Jedes verschachtelte Objekt trägt `additionalProperties: false`. `packageId` folgt `^PKG-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`. Fingerprints folgen `^[0-9a-f]{64}$`; Versionen sind konstant `1` beziehungsweise `1.0.0`; `retentionClass` ist konstant `until-decision`.

`learnerPulseEvidence` verwendet genau eine der Formen:

```json
{"status": "suppressed-small-group"}
```

oder:

```json
{
  "status": "reported",
  "classResponseCount": 24,
  "items": [
    {"itemId": "clarity", "agree": 16, "partly": 5, "disagree": 2, "noAnswer": 1},
    {"itemId": "cognitiveEngagement", "agree": 15, "partly": 6, "disagree": 2, "noAnswer": 1},
    {"itemId": "supportUsefulness", "agree": 14, "partly": 7, "disagree": 2, "noAnswer": 1}
  ]
}
```

- [x] **Step 4: Manuelle fail-closed Validierung ohne Fremdabhängigkeit implementieren**

Verwende feste Feldmengen für Top-Level, Kontext und alle vier Evidenzspuren. Prüfe Typen mit `type(value) is int` beziehungsweise `type(value) is bool`, damit Python-Bools nicht als Integer akzeptiert werden. Prüfe:

```python
def evaluate_learner_pulse(payload: dict, protocol: dict) -> dict:
    if payload == {"status": "suppressed-small-group"}:
        return {"status": "suppressed-small-group", "warnings": []}
    _require_exact_fields(payload, {"status", "classResponseCount", "items"}, "learner pulse")
    _require(payload["status"] == "reported", "learner pulse status is invalid")
    _require(type(payload["classResponseCount"]) is int, "classResponseCount must be int")
    _require(payload["classResponseCount"] >= 10, "reported learner pulse requires at least 10 responses")
    warnings = []
    for expected_id, item in zip(("clarity", "cognitiveEngagement", "supportUsefulness"), payload["items"], strict=True):
        _require(item["itemId"] == expected_id, "learner pulse item order differs")
        total = item["agree"] + item["partly"] + item["disagree"] + item["noAnswer"]
        valid = item["agree"] + item["partly"] + item["disagree"]
        _require(total == payload["classResponseCount"], "learner pulse sums differ")
        _require(valid >= 10, "reported learner pulse item has fewer than 10 valid responses")
        if item["disagree"] * 3 >= valid:
            warnings.append({"id": f"WARN-{expected_id}", "itemId": expected_id, "status": "open"})
    return {"status": "reported", "warnings": warnings}
```

`validate_evidence_package` prüft Paket-/Protokoll-/Tool-/Zeitmodellversion, Scopebindung, ausschließlich erlaubte Kontextwerte, Pflichtphasen, Kriterien-IDs, Bands, Technik-/Privacy-Enums, widerspruchsfreie Summen und exakt die aus den Eingaben neu abgeleiteten Warnungen. Das übergebene `result` wird niemals vertraut, sondern in Task 3/4 neu berechnet und verglichen.

- [x] **Step 5: Privacy- und Schemamutationen vollständig parametrisieren**

Mutiere nacheinander jedes verbotene Feld in Top-Level, `context`, allen Evidenzspuren und Warnungen. Mutiere außerdem bool/int, negative Summen, gemischte Versionen, falsche Fingerprints, freie Texte, Produktpfade, vierte Lernendenfrage, falsche Antwortreihenfolge, unter zehn reportete Antworten und `suppressed-small-group` mit zusätzlichen Zählwerten. Jede Mutation muss an `validate_evidence_package` scheitern.

- [x] **Step 6: Tests und CLI ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11EvidencePackageTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
```

Expected: alle Evidenz-, Privacy- und Regressionstests grün.

- [x] **Step 7: Task-Commit erstellen**

```powershell
git add pilot/schemas/evidence-package.schema.json scripts/validate_ium11.py tests/test_validate_ium11.py
git commit -m "feat: validate ium11 evidence packages"
```

## Task 3: Clusterergebnisse, Modul-Unterbefunde und additive Rückfälle ableiten

**Files:**
- Modify: `scripts/validate_ium11.py`
- Modify: `tests/test_validate_ium11.py`

**Interfaces:**
- Consumes: validiertes Cluster-Evidenzpaket und kompilierte Clusterkonfiguration
- Produces: `derive_cluster_result` mit Ergebnis, zehn möglichen Modul-Unterbefunden, Integrationsbefund, Warnungen und Rückfallwert

- [x] **Step 1: Failing Tests für sämtliche harte Clustergates schreiben**

```python
class IUM11ClusterResultTests(unittest.TestCase):
    def test_positive_cluster_requires_every_gate(self):
        result = derive_cluster_result(
            valid_cluster_package(scope_id="CLUSTER-7-DATA-CODING"),
            self.protocol["clustersById"]["CLUSTER-7-DATA-CODING"],
            self.protocol,
        )
        self.assertEqual(result["result"], "pass")
        self.assertEqual([item["result"] for item in result["moduleResults"]], ["pass", "pass"])
        self.assertEqual(result["integrationResult"]["result"], "pass")
        self.assertEqual(result["fallbackDeltaUnits"], 0)

    def test_mixed_or_weak_must_criterion_fails(self):
        for band in ("mixed", "weak"):
            payload = valid_cluster_package()
            payload["learningQualityEvidence"]["moduleResults"][0]["criteria"][0]["band"] = band
            with self.subTest(band=band):
                self.assertEqual(self.derive(payload)["result"], "fail")

    def test_budget_overrun_is_not_compensated(self):
        payload = valid_cluster_package(scope_id="CLUSTER-7-DATA-CODING")
        payload["deliveryTimeEvidence"]["actualUnits"] = 9
        result = self.derive(payload)
        self.assertEqual(result["result"], "fail")
        self.assertEqual(result["fallbackDeltaUnits"], 3)

    def test_missing_interpretability_is_not_evaluable(self):
        payload = valid_cluster_package()
        payload["deliveryTimeEvidence"]["externalDisruptionCode"] = "interpretability-lost"
        self.assertEqual(self.derive(payload)["result"], "not-evaluable")
```

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11ClusterResultTests -v
```

Expected: `derive_cluster_result` fehlt oder liefert noch keine vollständige Ableitung.

- [x] **Step 3: Muss-Kriterien und Modul-Unterbefunde rein ableiten**

Jedes Modul erhält genau die Kriterien:

```text
f"CRIT-{module_id}-ACTION"   → centralLearningAction
f"CRIT-{module_id}-PRODUCT"  → centralLearningProduct
```

Jede Integration erhält:

```text
f"CRIT-{integration_id}-HANDOFF-ACTIONS"   → preservedLearningActions
f"CRIT-{integration_id}-HANDOFF-EVIDENCE"  → preservedProductAndCurriculumEvidence
```

Die IDs werden durch Ersetzen von `IUM-` beziehungsweise `INT-` nicht verkürzt; Beispiele sind `CRIT-IUM-7-CORE-01-ACTION` und `CRIT-INT-7-DATA-CODING-HANDOFF-EVIDENCE`. `validate_pilot_protocol` kompiliert diese Kriterien deterministisch, `validate_evidence_package` verlangt jedes genau einmal.

- [x] **Step 4: Ergebnispriorität und Rückfalllogik implementieren**

```python
def derive_cluster_result(payload: dict, cluster: dict, protocol: dict) -> dict:
    not_evaluable = (
        payload["deliveryTimeEvidence"]["externalDisruptionCode"] == "interpretability-lost"
    )
    module_results = _derive_module_results(payload, cluster)
    integration_result = _derive_integration_result(payload, cluster)
    pulse = evaluate_learner_pulse(payload["learnerPulseEvidence"], protocol)
    failed = any(
        [
            payload["deliveryTimeEvidence"]["actualUnits"] > cluster["budgetUnits"],
            not payload["deliveryTimeEvidence"]["requiredLearningPhasesCompleted"],
            any(item["result"] != "pass" for item in module_results),
            integration_result["result"] != "pass",
            payload["technicalPrivacyEvidence"]["technicalFunction"] != "pass",
            payload["technicalPrivacyEvidence"]["privacyGate"] != "pass",
            bool(pulse["warnings"]),
        ]
    )
    result = "not-evaluable" if not_evaluable else "fail" if failed else "pass"
    return {
        "result": result,
        "moduleResults": module_results,
        "integrationResult": integration_result,
        "developmentWarnings": pulse["warnings"],
        "fallbackDeltaUnits": cluster["fallbackDeltaUnits"] if result == "fail" else 0,
    }
```

Privacyverletzung wird vor dieser Ableitung abgefangen, als `fail` klassifiziert und blockiert Export/Weiterverarbeitung. Ein technischer Fallback ist nur positiv, wenn `fallbackActivated` wahr, `fallbackEquivalentLearningFunction` wahr und das Budget eingehalten ist. `requiredLearningPhasesCompleted` ist nur dann wahr, wenn die exportierte, sortierte Phasenmenge exakt der kompilierten Pflichtphasenmenge aller Clustermodule entspricht.

- [x] **Step 5: Alle vier Cluster und Grenzwerte parametrisiert testen**

Prüfe pro Cluster positiven Lauf, `budget + 1`, jede fehlende Phase, jedes `mixed`/`weak`, fehlendes oder nicht weiterverwendetes Übergabeprodukt, Technikfehler, nichtgleichwertigen Fallback, Privacyfehler und Lernendenwarnung. Prüfe Warnungsgrenzen `2/7` ohne Warnung, `3/9` mit Warnung und `4/12` mit Warnung. Prüfe Rückfälle exakt `3/2/3/6` und dass `not-evaluable` keinen positiven Pilotbefund erzeugt.

- [x] **Step 6: Fokussierte und vollständige Tests ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11ClusterResultTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
```

Expected: alle vier Clusterverträge und sämtliche Regressionen grün.

- [x] **Step 7: Task-Commit erstellen**

```powershell
git add scripts/validate_ium11.py tests/test_validate_ium11.py
git commit -m "feat: derive ium11 cluster outcomes"
```

## Task 4: Jahresbefund und nichtmutierendes Entscheidungspaket implementieren

**Files:**
- Create: `pilot/schemas/decision-package.schema.json`
- Modify: `scripts/validate_ium11.py`
- Modify: `tests/test_validate_ium11.py`

**Interfaces:**
- Consumes: genau vier aktuelle Clusterpakete, genau ein Jahrespaket, kompilierter Protokollvertrag
- Produces: `derive_annual_result`, `build_decision_package`, `validate_decision_package`

- [x] **Step 1: Failing Tests für Jahresvoraussetzungen und Empfehlung schreiben**

Ergänze diese exakten Hilfen:

```python
def valid_annual_package():
    root = Path(__file__).resolve().parents[1]
    time_model = load_json(root / "roadmap/time-model.json")
    protocol = validate_pilot_protocol(
        load_json(root / "pilot/pilot-protocol.json"),
        time_model,
    )
    clusters = protocol["clusters"]
    modules = [module for cluster in clusters for module in cluster["modules"]]
    completed_phases = sorted({
        phase_id
        for module in modules
        for phase_id in module["requiredPhaseIds"]
    })
    return {
        "schemaVersion": 1,
        "packageType": "annual-evidence",
        "packageId": f"PKG-{uuid.uuid4()}",
        "protocolVersion": protocol["protocolVersion"],
        "protocolFingerprint": protocol["protocolFingerprint"],
        "toolVersion": protocol["toolVersion"],
        "timeModelFingerprint": protocol["timeModelFingerprint"],
        "scopeType": "annual",
        "scopeId": "ANNUAL-7-WORKING-40",
        "context": {"schoolYear": "2026-27", "term": "full-year", "classSizeBand": "20-29", "deviceClass": "mixed", "browserFamily": "chromium", "networkMode": "offline"},
        "deliveryTimeEvidence": {
            "plannedUnits": 40,
            "actualUnits": 40,
            "completedPhaseIds": completed_phases,
            "requiredLearningPhasesCompleted": True,
            "fallbackActivated": False,
            "technicalStartupMinutes": 12,
            "supportDemandBand": "low",
            "externalDisruptionCode": "none",
            "clusterOrder": [cluster["id"] for cluster in clusters],
            "clusterActualUnits": [{"clusterId": cluster["id"], "actualUnits": cluster["budgetUnits"]} for cluster in clusters],
        },
        "learningQualityEvidence": {
            "moduleResults": [
                {"pilotAssignmentId": module["pilotAssignmentId"], "moduleId": module["moduleId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in module["criteria"]], "result": "pass"}
                for module in modules
            ],
            "integrationResults": [
                {"pilotAssignmentId": cluster["integration"]["pilotAssignmentId"], "integrationContractId": cluster["integration"]["integrationContractId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in cluster["integration"]["criteria"]], "handoffProductPresent": True, "handoffReused": True, "result": "pass"}
                for cluster in clusters
            ],
        },
        "learnerPulseEvidence": reported_pulse(),
        "technicalPrivacyEvidence": {"technicalFunction": "pass", "fallbackEquivalentLearningFunction": False, "problemCode": "none", "severity": "none", "privacyGate": "pass"},
        "result": "pass",
        "developmentWarnings": [],
        "retentionClass": "until-decision",
    }


def five_positive_packages():
    return [
        valid_cluster_package("CLUSTER-7-DATA-CODING"),
        valid_cluster_package("CLUSTER-7-PROGRAMMING"),
        valid_cluster_package("CLUSTER-7-NET-SECURITY"),
        valid_cluster_package("CLUSTER-7-DATA-MEDIA-SOCIETY"),
        valid_annual_package(),
    ]


def packages_by_scope(packages):
    return {package["scopeId"]: package for package in packages}
```

```python
class IUM11DecisionPackageTests(unittest.TestCase):
    def test_positive_minimal_pilot_only_recommends_working_review(self):
        package = build_decision_package(
            five_positive_packages(),
            self.protocol,
            self.time_model,
        )
        self.assertEqual(package["recommendation"], "eligible-for-working-availability-review")
        self.assertEqual(package["statementBoundary"], "documented-conditions-only")
        self.assertEqual(package["reviewStatus"], {
            "fach": "not-started",
            "engineeringPrivacy": "not-started",
            "commissioner": "not-started",
        })
        self.assertEqual(package["availabilityGateResults"], {
            "capacity": "passed",
            "integration": "passed",
            "technical": "passed",
            "privacy": "passed",
            "pilot": "passed",
        })
        self.assertNotIn("timeModelMutation", package)

    def test_annual_requires_four_positive_same_version_clusters(self):
        mutations = [
            lambda packages: packages.pop(0),
            lambda packages: packages[0].__setitem__("result", "fail"),
            lambda packages: packages[0].__setitem__("protocolVersion", "2.0.0"),
            lambda packages: packages[0].__setitem__("timeModelFingerprint", "0" * 64),
        ]
        for mutate in mutations:
            packages = five_positive_packages()
            mutate(packages)
            with self.subTest(mutation=mutate):
                with self.assertRaises(IUM11ValidationError):
                    build_decision_package(packages, self.protocol, self.time_model)

    def test_no_cluster_time_compensation(self):
        packages = five_positive_packages()
        packages_by_scope(packages)["CLUSTER-7-DATA-CODING"]["deliveryTimeEvidence"]["actualUnits"] = 9
        packages_by_scope(packages)["CLUSTER-7-PROGRAMMING"]["deliveryTimeEvidence"]["actualUnits"] = 10
        with self.assertRaisesRegex(IUM11ValidationError, "cluster budget"):
            build_decision_package(packages, self.protocol, self.time_model)
```

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11DecisionPackageTests -v
```

Expected: Entscheidungsschema und Ableitungsfunktionen fehlen.

- [x] **Step 3: Geschlossenes Entscheidungsschema anlegen**

Verwende Draft 2020-12, `additionalProperties: false` auf jeder Objektebene und die im Abschnitt „Verbindliche Paketformen“ festgelegten Top-Level-Felder. Zentrale Konstanten:

```json
{
  "schemaVersion": 1,
  "packageType": "pilot-decision",
  "statementBoundary": "documented-conditions-only",
  "retentionClass": "until-decision"
}
```

`recommendation` ist genau eines von:

```text
eligible-for-working-availability-review
repeat-required
not-evaluable
```

`reviewStatus` besitzt ausschließlich `fach`, `engineeringPrivacy`, `commissioner`; jeder Wert ist `not-started`, `passed` oder `failed`. Ein vom Validator erzeugtes Paket beginnt immer dreimal mit `not-started`.

- [x] **Step 4: Jahresableitung ohne Querkompensation implementieren**

```python
def derive_annual_result(
    annual_payload: dict,
    cluster_packages: list[dict],
    protocol: dict,
) -> dict:
    ordered = sorted(cluster_packages, key=lambda item: protocol["clustersById"][item["scopeId"]]["order"])
    _require(len(ordered) == 4, "annual result requires four cluster packages")
    _require(all(item["result"] == "pass" for item in ordered), "annual result requires positive clusters")
    _require(
        [item["scopeId"] for item in ordered] == protocol["annualPilot"]["clusterIds"],
        "annual cluster sequence differs",
    )
    for item in ordered:
        cluster = protocol["clustersById"][item["scopeId"]]
        _require(
            item["deliveryTimeEvidence"]["actualUnits"] <= cluster["budgetUnits"],
            f"cluster budget exceeded: {item['scopeId']}",
        )
    _require(annual_payload["deliveryTimeEvidence"]["actualUnits"] <= 40, "annual budget exceeded")
    _require(annual_payload["deliveryTimeEvidence"]["clusterOrder"] == protocol["annualPilot"]["clusterIds"], "annual sequence differs")
    return {"result": "pass", "actualUnits": annual_payload["deliveryTimeEvidence"]["actualUnits"]}
```

Der Jahresbefund verlangt im Jahrespaket erneut alle vier Clusterbudgets, Übergaben, Pflichtphasen, Technik-/Privacybefunde und die fünf Gates `capacity`, `integration`, `technical`, `privacy`, `pilot` als `passed`. Frühere Clusterpakete ersetzen keine Jahresbeobachtung.

- [x] **Step 5: Entscheidungspaket deterministisch bauen und erneut validieren**

`build_decision_package`:

1. validiert jedes Eingabepaket erneut;
2. verlangt fünf verschiedene `packageId` und exakt die vier Cluster- plus eine Jahres-Scope-ID;
3. verlangt identische Protokoll-, Tool- und Fingerprintwerte;
4. leitet zehn Modul- und vier Integrationsresultate aus den Clusterpaketen ab;
5. berechnet Rückfälle als Summe ausschließlich fehlgeschlagener Integrationen;
6. leitet die fünf `availabilityGateResults` ausschließlich aus Kapazität, Integrationen, Technik, Privacy und fünf Pilotresultaten ab;
7. setzt `recommendation` auf `eligible-for-working-availability-review` nur bei fünf positiven Ergebnissen und fünf bestandenen Gates, sonst `repeat-required` oder `not-evaluable`;
8. setzt die Aussagegrenze und drei ungestartete Reviews;
9. prüft mit `validate_decision_package` den gerade erzeugten Wert erneut.

Vor und nach dem Aufruf wird `canonical_sha256(time_model)` verglichen. Jede Mutation des Eingabezeitmodells ist ein Testfehler.

Ergänze den lokalen CLI-Pfad für nichtöffentliche Pakete:

```powershell
python -B scripts/validate_ium11.py `
  --evidence C:\private-pilot\cluster-1.json `
  --evidence C:\private-pilot\cluster-2.json `
  --evidence C:\private-pilot\cluster-3.json `
  --evidence C:\private-pilot\cluster-4.json `
  --evidence C:\private-pilot\annual.json `
  --decision-output C:\private-pilot\decision.json
```

`--evidence` muss genau fünfmal erscheinen, `--decision-output` darf noch nicht existieren, und Ein- sowie Ausgabepfade werden vor dem Schreiben vollständig validiert. Liegt ein Pfad innerhalb des öffentlichen Repositorys, wird der Vorgang abgelehnt; einzige Ausnahme ist der in Task 5 getrennt getestete synthetische Schreibpfad. Fehler hinterlassen keine Teildatei.

- [x] **Step 6: Mutationstests für unzulässige Reifeaussagen ergänzen**

Mutiere `recommendation` zu `reviewed`, `standard`, `available` und `green`; setze Reviews ohne positives Minimalpilotpaket auf `passed`; entferne eine Quelle; dupliziere eine Scope-ID; mische Fingerprints; ändere Gesamtzeit auf 41; verrechne einen Überlauf quer; markiere `semanticCoverageStatus` als `covered`; füge eine Statusmutation hinzu. Jede Mutation muss an der öffentlichen Entscheidungsgrenze scheitern.

- [x] **Step 7: Fokussierte und vollständige Tests ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11DecisionPackageTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
```

Expected: Jahres-, Entscheidungs- und alle bisherigen Tests grün; `roadmap/time-model.json` bleibt byteidentisch zum Taskbeginn.

- [x] **Step 8: Task-Commit erstellen**

```powershell
git add pilot/schemas/decision-package.schema.json scripts/validate_ium11.py tests/test_validate_ium11.py
git commit -m "feat: build ium11 pilot decisions"
```

## Task 5: Synthetische Konformitätsbeispiele und Repositoryvalidierung vervollständigen

**Files:**
- Create: `pilot/examples/synthetic-cluster-pass.json`
- Create: `pilot/examples/synthetic-cluster-programming-pass.json`
- Create: `pilot/examples/synthetic-cluster-net-security-pass.json`
- Create: `pilot/examples/synthetic-cluster-data-media-society-pass.json`
- Create: `pilot/examples/synthetic-cluster-fail.json`
- Create: `pilot/examples/synthetic-annual-pass.json`
- Create: `pilot/examples/synthetic-decision-eligible.json`
- Modify: `scripts/validate_ium11.py`
- Modify: `tests/test_validate_ium11.py`

**Interfaces:**
- Consumes: Paketvalidatoren und Ableitungsfunktionen aus Tasks 2–4
- Produces: öffentliche, offensichtlich synthetische Referenzpakete und vollständigen Repositorybefund

- [x] **Step 1: Failing Repositorytests für alle Beispiele schreiben**

Die Testhilfen sind exakt:

```python
def load_positive_example_packages(root):
    names = [
        "synthetic-cluster-pass.json",
        "synthetic-cluster-programming-pass.json",
        "synthetic-cluster-net-security-pass.json",
        "synthetic-cluster-data-media-society-pass.json",
        "synthetic-annual-pass.json",
    ]
    return [load_json(root / "pilot/examples" / name) for name in names]


def collect_keys(value):
    if isinstance(value, dict):
        return set(value) | set().union(*(collect_keys(item) for item in value.values()), set())
    if isinstance(value, list):
        return set().union(*(collect_keys(item) for item in value), set())
    return set()
```

```python
class IUM11SyntheticExampleTests(unittest.TestCase):
    def test_all_examples_are_closed_nonpersonal_and_derivable(self):
        result = validate_ium11_repository(self.root)
        self.assertEqual(result["exampleCounts"], {
            "clusterPass": 4,
            "clusterFail": 1,
            "annualPass": 1,
            "decisionEligible": 1,
        })

    def test_positive_examples_rebuild_committed_decision_byte_for_byte(self):
        positive = load_positive_example_packages(self.root)
        rebuilt = build_decision_package(positive, self.protocol, self.time_model)
        committed = load_json(self.root / "pilot/examples/synthetic-decision-eligible.json")
        self.assertEqual(rebuilt, committed)

    def test_examples_contain_no_identifying_or_free_text_keys(self):
        for path in sorted((self.root / "pilot/examples").glob("*.json")):
            flattened_keys = collect_keys(load_json(path))
            self.assertTrue(flattened_keys.isdisjoint(PROHIBITED_FIELD_NAMES), path)
```

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11SyntheticExampleTests -v
```

Expected: Beispieldateien fehlen.

- [x] **Step 3: Vier positive Clusterbeispiele mit neutralen Kontextwerten anlegen**

Alle positiven Cluster verwenden:

```json
{
  "schemaVersion": 1,
  "packageType": "cluster-evidence",
  "protocolVersion": "1.0.0",
  "toolVersion": "1.0.0",
  "timeModelFingerprint": "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1",
  "context": {
    "schoolYear": "2026-27",
    "term": "first-half",
    "classSizeBand": "20-29",
    "deviceClass": "mixed",
    "browserFamily": "chromium",
    "networkMode": "offline"
  },
  "result": "pass",
  "developmentWarnings": [],
  "retentionClass": "until-decision"
}
```

Jede Datei erhält eine feste RFC-4122-v4-konforme synthetische `packageId` mit `PKG-`-Präfix, den aktuellen `protocolFingerprint`, ihre richtige Scope-ID, das exakte Clusterbudget, alle kompilierten Pflichtphasen und Muss-Kriterien `strong`, ein vorhandenes und weiterverwendetes Übergabeprodukt, positiven Technik-/Privacybefund und einen Lernendenimpuls mit mindestens zehn gültigen Antworten unter der Warnungsgrenze.

- [x] **Step 4: Negatives Cluster- und positives Jahresbeispiel anlegen**

`synthetic-cluster-fail.json` verwendet `CLUSTER-7-PROGRAMMING`, `actualUnits: 12`, Ergebnis `fail` und Rückfall `2`; alle anderen Felder bleiben gültig, damit genau das Budgetgate den negativen Befund erklärt.

`synthetic-annual-pass.json` verwendet Scope `ANNUAL-7-WORKING-40`, `term: full-year`, exakt 40 UE, die Reihenfolge der vier Cluster-IDs, erneute positive Cluster-/Übergabe-/Phasenbefunde und alle fünf Gates `passed`.

- [x] **Step 5: Entscheidungspaket ausschließlich durch Produktionsfunktion erzeugen**

Verwende einmalig die Python-Produktionsfunktion und prüfe den erzeugten Wert vor dem Commit:

```powershell
python -B scripts/validate_ium11.py --write-synthetic-decision pilot/examples/synthetic-decision-eligible.json
python -B scripts/validate_ium11.py
```

Der CLI-Schreibmodus akzeptiert ausschließlich den exakten Pfad unter `pilot/examples/`, überschreibt keine andere Datei und verwendet nur die fünf committed positiven Evidenzbeispiele. Er ist kein Schreibweg für reale Daten.

- [x] **Step 6: Repositoryvalidator auf Schemas, Beispiele und Statusinvariante erweitern**

`validate_ium11_repository` lädt beide Schemas, alle sieben Beispiele und verifiziert zusätzlich:

- keine reale Evidenzdatei außerhalb `pilot/examples/`;
- alle Beispieldateinamen beginnen mit `synthetic-`;
- kein Zeitmodellstatus ändert sich;
- Protokoll- und Beispiel-Fingerprints stimmen;
- genau vier positive Clusterscopes und ein positiver Jahres-Scope;
- negative Beispieldatei bleibt von der positiven Entscheidung ausgeschlossen;
- Entscheidung lässt `status: working` und `semanticCoverageStatus: partial` unangetastet.

- [x] **Step 7: Fokussierte und vollständige Tests ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11SyntheticExampleTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
```

Expected: Beispiele sind schema-, privacy- und ableitungskonform; vollständige Suite grün.

- [x] **Step 8: Task-Commit erstellen**

```powershell
git add pilot/examples scripts/validate_ium11.py tests/test_validate_ium11.py
git commit -m "test: add ium11 synthetic evidence set"
```

## Task 6: Cockpitvertrag deterministisch kompilieren und JavaScript-Domänenkern bauen

**Files:**
- Create: `scripts/build_ium11_cockpit.py`
- Create: `pilot/cockpit/assets/protocol.js`
- Create: `pilot/cockpit/assets/app.js`
- Create: `tests/test_ium11_cockpit_contract.py`

**Interfaces:**
- Consumes: `pilot-protocol.json`, `time-model.json`, Python-Ableitungsregeln und synthetische Beispiele
- Produces: deterministisches `window.IUM11_PROTOCOL`, reine JavaScript-Vertragsfunktionen und Cross-Runtime-Parität

- [x] **Step 1: Failing Build- und Node-Vertragstests schreiben**

```python
def run_node(source):
    return subprocess.run(
        ["node", "-e", source],
        cwd=Path(__file__).resolve().parents[1],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class IUM11CockpitBuildTests(unittest.TestCase):
    def test_protocol_asset_is_reproducible(self):
        committed = (self.root / "pilot/cockpit/assets/protocol.js").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary_directory:
            generated = Path(temporary_directory) / "protocol.js"
            build_cockpit_contract(self.root, output_path=generated)
            self.assertEqual(generated.read_text(encoding="utf-8"), committed)

    def test_javascript_exports_exact_public_api(self):
        result = run_node("""
          const api = require('./pilot/cockpit/assets/app.js');
          process.stdout.write(JSON.stringify(Object.keys(api).sort()));
        """)
        self.assertEqual(json.loads(result.stdout), sorted([
            "evaluateLearnerPulse", "deriveClusterResult", "deriveAnnualResult",
            "validateEvidencePackage", "createPackageId", "createEvidencePackage",
            "serializePackage", "parsePackage"
        ]))
```

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_ium11_cockpit_contract.IUM11CockpitBuildTests -v
```

Expected: Buildskript und JavaScript-Dateien fehlen.

- [x] **Step 3: Kompilierung ohne Statusduplikation implementieren**

`compile_cockpit_contract` ruft `validate_pilot_protocol` auf und erzeugt ausschließlich:

```python
{
    "schemaVersion": 1,
    "protocolVersion": compiled["protocolVersion"],
    "protocolFingerprint": compiled["protocolFingerprint"],
    "toolVersion": compiled["toolVersion"],
    "timeModelFingerprint": compiled["timeModelFingerprint"],
    "minimumLearnerResponses": 10,
    "learnerWarningRatio": {"numerator": 1, "denominator": 3},
    "learnerPulseItems": compiled["learnerPulseItems"],
    "contextEnums": compiled["contextEnums"],
    "clusters": compiled["clusters"],
    "annualPilot": compiled["annualPilot"],
}
```

`render_protocol_js` schreibt UTF-8 ohne BOM, sortierte JSON-Schlüssel und genau:

```python
def render_protocol_js(compiled_contract: dict) -> str:
    payload = json.dumps(
        compiled_contract,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (
        "/* Generated by scripts/build_ium11_cockpit.py; do not edit manually. */\n"
        f"window.IUM11_PROTOCOL = Object.freeze({payload});\n"
    )
```

Der Build ist byteidentisch und schreibt atomar über eine temporäre Datei im Zielverzeichnis.

- [x] **Step 4: Reine JavaScript-Schwellen- und Paketfunktionen implementieren**

```javascript
function evaluateLearnerPulse(payload, protocol) {
  if (payload.status === 'suppressed-small-group') {
    assertExactKeys(payload, ['status'], 'learnerPulseEvidence');
    return {status: 'suppressed-small-group', warnings: []};
  }
  assertExactKeys(payload, ['status', 'classResponseCount', 'items'], 'learnerPulseEvidence');
  if (payload.status !== 'reported' || !Number.isInteger(payload.classResponseCount) || payload.classResponseCount < protocol.minimumLearnerResponses) {
    throw new Error('reported learner pulse requires at least 10 responses');
  }
  const warnings = [];
  protocol.learnerPulseItems.forEach((definition, index) => {
    const item = payload.items[index];
    const valid = item.agree + item.partly + item.disagree;
    const total = valid + item.noAnswer;
    if (item.itemId !== definition.id || total !== payload.classResponseCount || valid < protocol.minimumLearnerResponses) {
      throw new Error('learner pulse sums or ids differ');
    }
    if (item.disagree * protocol.learnerWarningRatio.denominator >= valid * protocol.learnerWarningRatio.numerator) {
      warnings.push({id: `WARN-${definition.id}`, itemId: definition.id, status: 'open'});
    }
  });
  return {status: 'reported', warnings};
}
```

`deriveClusterResult` und `deriveAnnualResult` folgen exakt den Python-Prädikaten aus Tasks 3/4. `validateEvidencePackage` lehnt zusätzliche Schlüssel rekursiv ab. `serializePackage` gibt `JSON.stringify(payload, null, 2) + '\n'` zurück; `parsePackage` akzeptiert nur JSON-Objekte und validiert sofort. `createPackageId` verwendet `crypto.randomUUID()` und erzeugt `` `PKG-${uuid}` ``; unter Node wird `require('node:crypto').randomUUID` verwendet.

- [x] **Step 5: Cross-Runtime-Tests gegen alle Beispiele ergänzen**

Für jede synthetische Evidenzdatei ruft der Test Python und Node auf und vergleicht `result`, Warnungs-IDs, Modul-/Integrationsresultate und Rückfallwerte. Zusätzliche Grenzfälle sind `2/7`, `3/9`, `4/12`, `9` reportete Antworten, `suppressed-small-group` mit Zusatzfeld, Budget+1, fehlende Phase, `mixed`, Privacyfehler und falscher Fingerprint.

- [x] **Step 6: Build-, Node- und vollständige Tests ausführen**

Run:

```powershell
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/app.js
python -B -m unittest tests.test_ium11_cockpit_contract -v
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: Build byteidentisch, Node-Syntax grün, Python/JavaScript-Parität für alle Fälle.

- [x] **Step 7: Task-Commit erstellen**

```powershell
git add scripts/build_ium11_cockpit.py pilot/cockpit/assets/protocol.js pilot/cockpit/assets/app.js tests/test_ium11_cockpit_contract.py
git commit -m "feat: add ium11 cockpit contract core"
```

## Task 7: Zugängliche speicherfreie Offline-Oberfläche implementieren

**Files:**
- Create: `pilot/cockpit/index.html`
- Create: `pilot/cockpit/assets/styles.css`
- Modify: `pilot/cockpit/assets/app.js`
- Modify: `tests/test_ium11_cockpit_contract.py`

**Interfaces:**
- Consumes: `window.IUM11_PROTOCOL` und reine JavaScript-Funktionen aus Task 6
- Produces: lokaler Formularfluss für Bereitschaft, Kontext, vier Evidenzspuren, Prüfung, JSON-Download und Dateiimport

- [x] **Step 1: Failing HTML-, Offline- und Accessibility-Vertragstests schreiben**

Implementiere in derselben Testdatei `CockpitHTMLParser(HTMLParser)`. Der Parser sammelt Starttags, Attribute, `label[for]`, Control-IDs, Landmarks und positive `tabindex`-Werte. `parse_html(path)` liest UTF-8 und gibt den gefütterten Parser zurück; `read_cockpit_sources(root)` konkateniert ausschließlich `index.html`, `styles.css`, `protocol.js` und `app.js`.

```python
class IUM11CockpitMarkupTests(unittest.TestCase):
    def test_cockpit_has_required_landmarks_and_status_regions(self):
        document = parse_html(self.root / "pilot/cockpit/index.html")
        self.assertEqual(document.count("main"), 1)
        self.assertTrue(document.has_element(id="error-summary", attributes={"tabindex": "-1"}))
        self.assertTrue(document.has_element(id="status-message", attributes={"aria-live": "polite"}))
        self.assertTrue(document.labels_cover_all_controls())

    def test_cockpit_contains_no_network_or_persistence_capability(self):
        combined = read_cockpit_sources(self.root)
        for token in [
            "fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon",
            "localStorage", "sessionStorage", "indexedDB", "document.cookie",
            "serviceWorker", "http://", "https://", "@import", "url(//"
        ]:
            with self.subTest(token=token):
                self.assertNotIn(token, combined)

    def test_controls_use_native_keyboard_semantics(self):
        document = parse_html(self.root / "pilot/cockpit/index.html")
        self.assertFalse(document.has_positive_tabindex())
        self.assertFalse(document.has_click_only_noninteractive_elements())
```

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_ium11_cockpit_contract.IUM11CockpitMarkupTests -v
```

Expected: HTML und CSS fehlen.

- [x] **Step 3: Semantische Oberfläche mit vier klaren Schritten anlegen**

`index.html` besitzt genau einen `<main>` und vier nummerierte Abschnitte:

1. **Bereitschaft prüfen** – Material, Lehrkräftehandbuch, Ankeraufgaben, Werkzeug/Fallback, Privacy, Kapazität und Fingerprint als sieben Pflichtcheckboxen; ohne vollständiges Gate bleiben Form und Export deaktiviert.
2. **Pilotstufe und Kontext** – Scopeauswahl aus Protokoll, ausschließlich sechs erlaubte Kontextfelder.
3. **Aggregierte Evidenz erfassen** – Zeit/Phasen, Modul-/Integrationskriterien, Lernendenimpuls und Technik/Privacy in getrennten `<fieldset>`-Gruppen.
4. **Prüfen und exportieren** – abgeleitetes Ergebnis, Warnungen, Aussagegrenze, `error-summary`, `status-message`, Import- und Downloadbutton.

Kein Element fordert Namen, Schule, Klasse, Kurs, Datum, Freitext oder Produktupload an. `accept="application/json,.json"` begrenzt die lokale Dateiauswahl.

Jeder Validierungsfehler wird intern als `{code, scopeId, nextStep}` repräsentiert. Sichtbare Meldungen nennen dadurch immer Ursache, betroffenen Scope und genau einen zulässigen nächsten Schritt; es gibt keinen „trotzdem exportieren“-Pfad.

- [x] **Step 4: Zustandsmaschine und sicheren Export/Import verdrahten**

```javascript
const state = {
  readiness: new Set(),
  scopeId: null,
  importedClusters: new Map(),
  draft: null,
  validatedPackage: null
};

function downloadPackage(payload) {
  const blob = new Blob([serializePackage(payload)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `ium11-${payload.scopeId.toLowerCase()}-${payload.packageId}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
}

function clearState() {
  state.readiness.clear();
  state.scopeId = null;
  state.importedClusters.clear();
  state.draft = null;
  state.validatedPackage = null;
  document.querySelector('form').reset();
}
```

Export ist deaktiviert, solange Validierung fehlschlägt, Privacy `fail` ist oder Ergebnis nicht neu abgeleitet wurde. Bei Auswahl des Jahres-Scope verlangt die Oberfläche vor der Eingabe vier lokale Clusterdateien. Sie akzeptiert nur vier verschiedene, positive und versionsgleiche Pakete in Protokollreihenfolge und hält sie ausschließlich in `state.importedClusters`; erst dann wird die Jahreserfassung freigeschaltet. Schließen/Neuladen verwirft den Zustand. Import liest ausschließlich mit `FileReader.readAsText`, ruft `parsePackage` auf, zeigt Fehler im fokussierten Fehlerresümee und übernimmt nie ungeprüfte Werte in den Zustand.

- [x] **Step 5: CSS-Baseline für Fokus, Kontrast, Reflow und Touch anlegen**

Nutze Systemschriften, relative Einheiten, `max-width: 72rem`, sichtbares `:focus-visible` mit mindestens 3 px Kontur, Textkontrast mindestens 4.5:1, Status zusätzlich zu Farbe als Text/Icon, `min-block-size: 44px` und `min-inline-size: 44px` für Buttons/Inputs. Bei `prefers-reduced-motion: reduce` werden Übergänge deaktiviert. Bei 320 CSS-Pixel Breite entsteht kein horizontaler Seiten-Scroll.

- [x] **Step 6: Node-Flowtests für Bereitschaft, Exportblockade und Import schreiben**

Teste mit einer kleinen DOM-Adaptergrenze statt Browserglobalen in den reinen Funktionen:

- sieben Bereitschaftsgates erforderlich;
- Privacyfehler blockiert Downloadfunktion;
- unbekanntes Feld beim Import wird abgewiesen;
- `suppressed-small-group` zeigt keine Zählfelder im exportierten JSON;
- Warnung fokussiert Fehlerresümee und verhindert `pass`;
- `clearState` entfernt sämtliche In-Memory-Werte;
- Jahresmodus bleibt ohne vier positive versionsgleiche Clusterimporte gesperrt;
- Dateiname enthält nur Scope und zufällige Paket-ID.

- [x] **Step 7: Fokussierte und vollständige Verifikation ausführen**

Run:

```powershell
node --check pilot/cockpit/assets/app.js
python -B scripts/build_ium11_cockpit.py --check
python -B -m unittest tests.test_ium11_cockpit_contract -v
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: Markup-, Offline-, Accessibility-, Node- und Regressionstests grün.

- [x] **Step 8: Task-Commit erstellen**

```powershell
git add pilot/cockpit/index.html pilot/cockpit/assets/styles.css pilot/cockpit/assets/app.js tests/test_ium11_cockpit_contract.py
git commit -m "feat: add offline ium11 pilot cockpit"
```

## Task 8: Lehrkräfte-/Reviewanleitungen, README und Gesamtvalidator integrieren

**Files:**
- Create: `pilot/docs/teacher-guide.md`
- Create: `pilot/docs/review-guide.md`
- Modify: `README.md`
- Modify: `scripts/validate_ium11.py`
- Modify: `scripts/validate_phase0.py:1-12,1429-1534`
- Modify: `tests/test_validate_ium11.py`
- Modify: `tests/test_validate_phase0.py:1839-1905`

**Interfaces:**
- Consumes: vollständiges IUM11-Instrument aus Tasks 1–7
- Produces: ausführbare Lehrkräfte-/Reviewprozesse, öffentliche Einstiege und erweiterte Phase-0-Kette

- [x] **Step 1: Failing Publikations- und Orchestrierungstests schreiben**

```python
class IUM11PublicationTests(unittest.TestCase):
    def test_readme_states_exact_pilot_boundary(self):
        text = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn("IUM11-Pilotinstrument", text)
        self.assertIn("keine reale Pilotierung", text)
        self.assertIn("eligible-for-working-availability-review", text)
        self.assertIn("Flexible Vertiefungs-, Transfer- und Projektmodule bleiben", text)
        for forbidden in [
            "GRADE-7-WORKING-40 ist available",
            "GRADE-7-WORKING-40 ist reviewed",
            "Pilotierung abgeschlossen",
        ]:
            self.assertNotIn(forbidden, text)

    def test_guides_name_privacy_retention_and_repeat_rules(self):
        teacher = (self.root / "pilot/docs/teacher-guide.md").read_text(encoding="utf-8")
        review = (self.root / "pilot/docs/review-guide.md").read_text(encoding="utf-8")
        for anchor in ["unter zehn", "keine Freitexte", "bis zur Auftraggeberentscheidung", "löschen", "fail", "not-evaluable", "wiederholen"]:
            self.assertIn(anchor, teacher)
        for anchor in ["Fachreview", "Engineering-/Privacyreview", "Auftraggebergate", "zweite unabhängige", "documented-conditions-only"]:
            self.assertIn(anchor, review)
```

Erweitere den bestehenden Phase-0-Test auf Aufrufreihenfolge `ium10`, `ium09`, `ium11` und die Ausgabe `phase 0, IUM09, IUM10 and IUM11 validation passed\n`.

- [x] **Step 2: Roten Lauf bestätigen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11PublicationTests -v
python -B -m unittest tests.test_validate_phase0.CoverageRepositoryTests.test_phase0_entrypoint_runs_ium10_then_ium09_once_on_projection -v
```

Expected: Anleitungen/README-Einstiege fehlen und Phase 0 ruft IUM11 noch nicht auf.

- [x] **Step 3: Lehrkräfteanleitung mit ausführbarem Ablauf schreiben**

`teacher-guide.md` enthält in dieser Reihenfolge:

1. Zweck und Aussagegrenze der Entwicklungsprüfung;
2. sieben Punkte des Bereitschaftsgates;
3. Clusterreihenfolge `8 / 11 / 11 / 10` und Jahresvoraussetzung;
4. lokale Prüfung von Produkten ohne Kopie, Upload oder Link;
5. Klassenbandwahl `strong/mixed/weak`;
6. Zählen des dreiteiligen Lernendenimpulses außerhalb des Cockpits und Eingabe ausschließlich der Summen;
7. Unterdrückung unter zehn gültigen Antworten;
8. Technik-/Fallback- und Privacyprüfung;
9. Import, Validierung, bewusster Download und verständliche Fehlerwege;
10. lokales Zusammenführen der fünf aktuellen Pakete mit `--evidence` und `--decision-output` außerhalb des Repositorys;
11. Wiederholung nach `fail`/`not-evaluable`;
12. nichtöffentliche Ablage bis zur Auftraggeberentscheidung und anschließende Löschung ohne abweichende institutionelle Pflicht;
13. Verbot, reale Pakete, Dateinamen-Zuordnungen oder Rohprodukte in GitHub zu speichern.

Eine optionale analoge Zählhilfe wird nur als temporäre, nach Übertragung zu vernichtende Durchführungshilfe beschrieben; es entsteht keine parallele Vollstruktur.

- [x] **Step 4: Reviewanleitung mit drei getrennten Gates schreiben**

`review-guide.md` enthält:

- Fachreviewfragen zu Curriculumstatus, Operatorentiefe, Ankerhandlung, Lernprodukt, Übung, Feedback, Revision, Sicherung, Transfer und Übergabekontinuität;
- Engineering-/Privacyfragen zu Schema, Fingerprints, Offline/No-Persistence, verbotenen Feldern, ganzzahligen Schwellen, additiven Rückfällen, Accessibility, Browserbaseline und Dokumentationssynchronität;
- Auftraggebergate mit exakt zulässigen Statusänderungen `availabilityStatus: available`, `timeFeasibilityStatus: green`, `pilotStatus: completed`;
- unveränderte Achsen `status: working` und `semanticCoverageStatus: partial`;
- Minimalpilotaussage `documented-conditions-only`;
- Sperre für `reviewed`/`standard` und Erfordernis einer zweiten unabhängigen Jahresdurchführung;
- Retentions- und Veröffentlichungsschritt nach der Entscheidung.

- [x] **Step 5: README auf das Instrument und unveränderten Produktstatus synchronisieren**

Ergänze unter Phase 0 einen Abschnitt „IUM11-Pilotinstrument“ mit Links auf Protokoll, Cockpit, Lehrkräfteanleitung, Reviewanleitung und IUM11-Validator. Erkläre, dass das Instrument synthetisch geprüft, aber nicht real pilotiert ist. Aktualisiere die Validierungsbefehle um:

```powershell
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/app.js
python -B scripts/validate_ium11.py
```

Die Klasse-7-Zeile und sechs Anfangsachsen bleiben unverändert; flexible Module bleiben sichtbar.

- [x] **Step 6: IUM11 in die Phase-0-Kette aufnehmen**

```python
if __package__:
    from .validate_ium11 import validate_ium11
else:
    from validate_ium11 import validate_ium11

# in main(), nach validate_ium09(...)
validate_ium11(
    time_model,
    ium10_result,
    load_json(root / "pilot/pilot-protocol.json"),
    load_json(root / "pilot/schemas/evidence-package.schema.json"),
    load_json(root / "pilot/schemas/decision-package.schema.json"),
    [load_json(path) for path in sorted((root / "pilot/examples").glob("*.json"))],
    root / "pilot/cockpit",
)
print("phase 0, IUM09, IUM10 and IUM11 validation passed")
```

Der Test mockt alle drei Validatoren und verlangt jeden genau einmal. IUM11 erhält dasselbe `time_model`-Objekt und dasselbe `ium10_result`; IUM10 wird nicht doppelt ausgeführt.

- [x] **Step 7: Repositoryscan für reale Daten und Dokumentationsdrift ergänzen**

`validate_ium11` verlangt:

- alle im File Map genannten Produktdateien vorhanden;
- ausschließlich `synthetic-*.json` unter `pilot/examples/`;
- keine weiteren `.json`-Pakete unter `pilot/` außer Protokoll, Schemas, Beispiele und generiertes `protocol.js`;
- README und Guides nennen Protokoll-/Toolversion `1.0.0`, 40 UE, 4 Cluster, 10 Module, 5 Stufen, Privacyschwelle 10 und erlaubte Empfehlung;
- keine Publikation behauptet `available`, `reviewed`, `standard` oder abgeschlossene reale Pilotierung;
- Protokollbuild byteidentisch.

- [x] **Step 8: Fokussierte und vollständige Verifikation ausführen**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11PublicationTests -v
python -B -m unittest tests.test_validate_phase0.CoverageRepositoryTests -v
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
```

Expected: Publikation, Orchestrierung, vollständige Suite und alle vier CLI-Wege grün.

- [x] **Step 9: Task-Commit erstellen**

```powershell
git add pilot/docs/teacher-guide.md pilot/docs/review-guide.md README.md scripts/validate_ium11.py scripts/validate_phase0.py tests/test_validate_ium11.py tests/test_validate_phase0.py
git commit -m "docs: publish ium11 pilot instrument"
```

## Task 9: Unabhängiges Fachreview gegen Spezifikation und Fachprofil durchführen

**Files:**
- Review: `docs/superpowers/specs/2026-08-01-ium11-grade7-working-40-pilot-design.md`
- Review: `pilot/pilot-protocol.json`
- Review: `pilot/docs/teacher-guide.md`
- Review: `pilot/docs/review-guide.md`
- Review: `roadmap/time-model.json` ausschließlich lesend
- Review: `docs/fachprofil/ium-gymnasium-5-7.md` ausschließlich lesend
- Modify bei Befund: kleinster betroffener Produkt- und Testpfad
- Working report: `.superpowers/sdd/2026-08-01-ium11-grade7-working-40-pilot-implementation/fachreview.md`

**Interfaces:**
- Consumes: vollständig grüne Tasks 1–8
- Produces: unabhängiges Fachurteil `APPROVED`, `APPROVED AFTER FIXES` oder `CHANGES REQUIRED`

- [x] **Step 1: Reviewpaket mit exaktem Scope erstellen**

Das Review beantwortet jede Frage einzeln mit `PASS` oder einem Befund nach Schweregrad:

1. Sind Aufbaukurs Informatik 2016 als `enacted` und Lesehilfe 2026/2027 als `orientation` korrekt getrennt?
2. Bleiben PROG-003/004 und `semanticCoverageStatus: partial` unverändert?
3. Operationalisieren die zehn Modul-Unterbefunde tatsächliche zentrale Lernhandlungen und Produkte statt bloßer Aktivität?
4. Bewahren die vier Integrationsbefunde alle `preservedLearningActions` und `preservedProductAndCurriculumEvidence`?
5. Sind Übung, Feedback, Revision, Sicherung und Transfer durch Pflichtphasen geschützt?
6. Sind `strong/mixed/weak` ausdrücklich Projekt-Akzeptanzgrenzen statt Noten oder empirischer Normen?
7. Bleibt der Lernendenimpuls ergänzend und frei von Kompetenz- oder Wirkungsaussagen?
8. Sind Fallbacks nur bei gleicher Lernfunktion positiv?
9. Bleiben flexible Vertiefungs-, Transfer- und Projektmodule erhalten und außerhalb der Kernzeit?
10. Begrenzen Guides und Entscheidungspaket den Minimalpilot auf dokumentierte Einsatzbedingungen?

- [x] **Step 2: Fachreview auf aktuellem Gesamtdiff durchführen**

Der Reviewer liest Spezifikation, Protokoll, Guides, relevante Zeitmodellverträge und Fachprofil. Er prüft keine bloßen Suchtreffer, sondern verfolgt jede Modul-/Integrationsbindung bis zu ihrem kanonischen Vertrag.

- [x] **Step 3: Jeden Befund testgetrieben schließen**

Für jeden Critical-, Important- oder Minor-Befund zuerst einen fokussierten fehlschlagenden Test ergänzen, den Fehler reproduzieren, die kleinste Produktkorrektur implementieren und fokussiert sowie vollständig erneut testen. Keine Spezifikationsabschwächung zur Testbehebung.

- [x] **Step 4: Unabhängiges Re-Review ausführen**

Das Re-Review verwendet den neuen Gesamtdiff und bestätigt für jede der zehn Fragen `PASS`. `APPROVED AFTER FIXES` ist zulässig; offene Befunde sind nicht zulässig.

- [x] **Step 5: Gegebenenfalls Fix-Commit erstellen**

Explizit nur tatsächlich geänderte Produkt- und Testdateien stagen:

```powershell
git status --short
git diff --check
git diff --name-only -- pilot scripts tests README.md
git add -u -- pilot scripts tests README.md
git commit -m "fix: address ium11 fachreview"
```

Bei befundleerem Review entsteht kein leerer Commit.

## Task 10: Engineering-, Privacy- und Accessibilityreview, Gesamtverifikation und Handoff

**Files:**
- Review: gesamter Diff vom IUM11-Planbasiscommit bis `HEAD`
- Modify bei Befund: kleinster betroffener Produkt- und Testpfad
- Working report: `.superpowers/sdd/2026-08-01-ium11-grade7-working-40-pilot-implementation/engineering-review.md`
- Modify: `docs/superpowers/plans/2026-08-01-ium11-grade7-working-40-pilot-implementation.md` nur Checkboxen/Verifikationsbilanz
- Modify: Draft-PR-Beschreibung nach finaler Verifikation

**Interfaces:**
- Consumes: fachlich freigegebene Tasks 1–9
- Produces: technisch, datenschutzbezogen und zugänglich geprüfter Implementierungsstand ohne reale Daten und ohne Statusmutation

- [x] **Step 1: Whole-branch Reviewpaket erzeugen**

Basis ist der Commit unmittelbar vor Task 1. Prüfe den vollständigen Diff und mindestens diese Bereiche einzeln:

1. exakte Feldmengen und rekursives fail-closed Verhalten;
2. Python-Bool-/Int-/Float-Typgrenzen;
3. kanonische Protokoll- und Zeitmodellfingerprints;
4. Scope-, Versions- und Paket-ID-Konsistenz;
5. Privacyfeldsperren und Small-Group-Unterdrückung;
6. ganzzahlige Lernendenwarnung an den Grenzen;
7. Clusterbudgets, Nichtverrechnung und additive Rückfälle;
8. Jahresvoraussetzungen und fünf Verfügbarkeitsgates;
9. Unmöglichkeit von `reviewed`/`standard` und Zeitmodellmutation;
10. Python-/JavaScript-Parität;
11. deterministischer Protokollbuild;
12. keine Netzwerk-/Persistenzfähigkeit;
13. Import-/Exportfehler und beschädigte Dateien;
14. Tastatur, Fokus, Labels, Statusmeldungen, Kontrast, Reflow und Touchziele;
15. keine realen Evidenzdaten im Repository;
16. Phase-0-Aufrufreihenfolge und Fehlerpropagation;
17. README-/Guide-/Schema-/Code-Synchronität;
18. UTF-8, JSON, Python-AST, JavaScript-Syntax und Diffhygiene.

- [x] **Step 2: Cockpit visuell und interaktiv in einer aktuellen Browserengine prüfen**

Öffne `pilot/cockpit/index.html` direkt als lokale Datei. Falls die Prüfumgebung `file://` nicht darstellt, starte ausschließlich als Reviewharness:

```powershell
python -B -m http.server 8765 --bind 127.0.0.1 --directory pilot/cockpit
```

Prüfe bei 320, 768 und 1280 CSS-Pixel Breite: vollständige Tastaturbedienung, sichtbare Fokusreihenfolge, Error-Summary-Fokus, `aria-live`-Meldung, 200-%-Zoom, Reflow ohne horizontalen Seitenscroll, Kontrast, Touchziele, Import eines gültigen und beschädigten Pakets, Privacy-Exportblockade, JSON-Download und Zustandsverlust nach Reload. Die Netzwerkansicht darf außer lokalen Dokument-/Assetabrufen keine Requests zeigen.

- [x] **Step 3: Befunde testgetrieben schließen und re-reviewen**

Jeder Befund erhält zuerst eine reproduzierende Unit-, Node-, Markup- oder Repositoryprüfung. Danach kleinste Korrektur, fokussierter grüner Lauf, vollständiger Lauf und unabhängiges Re-Review. Offene Critical-/Important-/Minor-Befunde verhindern Handoff.

- [x] **Step 4: Frische Gesamtverifikation ausführen**

Run:

```powershell
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/protocol.js
node --check pilot/cockpit/assets/app.js
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
git diff --check
```

Zusätzliche statische Gates:

```powershell
$markers = @('TO' + 'DO', 'T' + 'BD', 'FIX' + 'ME', 'PLACE' + 'HOLDER', 'X' + 'XX')
Get-ChildItem pilot, scripts/validate_ium11.py, scripts/build_ium11_cockpit.py, tests/test_validate_ium11.py, tests/test_ium11_cockpit_contract.py, README.md -File -Recurse | Select-String -Pattern ($markers -join '|')
rg -n "fetch\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|localStorage|sessionStorage|indexedDB|document\.cookie|serviceWorker|https?://" pilot/cockpit
rg -n "studentName|schoolName|teacherName|className|courseName|freeText|studentProduct|ipAddress|telemetry" pilot
```

Expected: vollständige Suite ohne Fehler oder Skips; alle Validatoren grün; Build byteidentisch; Syntax-/Diffgates grün; die drei `rg`-Scans ohne unzulässige Treffer. Schema-URLs in `$id` und lizenzbezogene Dokumentationslinks werden beim Netzwerk-Scan als ausdrücklich geprüfte, nicht ausführbare Metadaten ausgenommen.

- [x] **Step 5: UTF-8-, JSON- und AST-Gate ausführen**

```powershell
python -B -c "import ast,json,pathlib; py=['scripts/validate_ium11.py','scripts/build_ium11_cockpit.py','tests/test_validate_ium11.py','tests/test_ium11_cockpit_contract.py']; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8')) for p in py]; js=['pilot/pilot-protocol.json','pilot/schemas/evidence-package.schema.json','pilot/schemas/decision-package.schema.json',*map(str,pathlib.Path('pilot/examples').glob('*.json'))]; [json.loads(pathlib.Path(p).read_text(encoding='utf-8')) for p in js]; print('IUM11_UTF8_JSON_AST=PASS')"
```

Expected: `IUM11_UTF8_JSON_AST=PASS`.

- [x] **Step 6: Finalen Fix- oder Verifikationscommit erstellen**

Nur bei tatsächlichen Änderungen:

```powershell
git status --short
git diff --check
git diff --name-only -- pilot scripts tests README.md
git add -u -- pilot scripts tests README.md
git commit -m "fix: complete ium11 pilot verification"
```

Danach Plancheckboxen und tatsächliche Testzahl in einem eigenen Dokumentationscommit aktualisieren:

```powershell
git add docs/superpowers/plans/2026-08-01-ium11-grade7-working-40-pilot-implementation.md
git commit -m "docs: record ium11 pilot verification"
```

- [x] **Step 7: Remote synchronisieren, pushen und Draft-PR aktualisieren**

```powershell
git fetch --prune
git pull --ff-only
git push origin feat/ium-phase0
```

Der PR-Text nennt Protokollversion, Zeitmodellfingerprint, vier Cluster, zehn Modul-Unterbefunde, fünf Stufen, Small-Group-Unterdrückung, Offline/No-Persistence, tatsächliche Testzahl, vier Validatoren und beide Reviewurteile. Er behauptet keine reale Pilotierung oder Statushochsetzung. Der PR bleibt Draft.

- [x] **Step 8: Remote- und Statusnachweis prüfen**

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse origin/feat/ium-phase0
gh pr view 1 --json isDraft,headRefOid,url,body
```

Expected: Worktree sauber; lokaler, Remote- und PR-Head identisch; PR bleibt Draft und enthält die IUM11-Verifikationsbilanz.

- [x] **Step 9: Nutzerhandoff mit harten Grenzen erstellen**

Der Handoff nennt:

- implementierte Artefakte und lokale Cockpitnutzung;
- tatsächliche Testzahl und Validatorstatus;
- Fach- und Engineering-/Privacy-/Accessibilityurteil;
- Commit, Branch, Push und Draft-PR;
- unveränderte Achsen `working / conditional / amber / covered / not-started / partial`;
- keine realen Daten, keine Pilotfreigabe und keine Statusmutation;
- nächstes getrenntes Gate: Bereitschaft der Lernmaterialien und reale Pilotdurchführung.

## Final Acceptance Checklist

- [x] `pilot/pilot-protocol.json` bindet exakt Schema/Protokoll/Tool `1 / 1.0.0 / 1.0.0` und den kanonischen Zeitmodellfingerprint.
- [x] Vier Cluster enthalten alle zehn Kernmodule genau einmal in `8 / 11 / 11 / 10 UE`.
- [x] Rückfälle sind exakt `3 / 2 / 3 / 6` und addieren höchstens auf 54 UE.
- [x] Zehn Modul- und vier Integrations-Unterbefunde binden an die kanonischen Lernhandlungen, Produkte, Phasen und Integrationsnachweise.
- [x] Evidenz- und Entscheidungsschema sind rekursiv geschlossen und lehnen unbekannte Felder ab.
- [x] Nur sechs grobe Kontextfelder sind zulässig; exakte Unterrichtsdaten und institutionelle Bezeichnungen fehlen.
- [x] Lernendenimpuls besitzt exakt drei Items und vier Kategorien.
- [x] Unter zehn gültigen Antworten werden alle Zählwerte unterdrückt.
- [x] `disagree * 3 >= validResponses` erzeugt deterministisch eine offene Warnung.
- [x] Cluster-`pass` verlangt Budget, Phasen, `strong`, Übergabe, Technik/Fallback, Privacy und warnungsfreien Zustand.
- [x] Privacyverletzung ist `fail` und blockiert Export; Pflicht-/Versions-/Fingerprintfehler sind `not-evaluable`.
- [x] Keine Clusterzeit wird mit einem anderen Cluster verrechnet.
- [x] Jahrespilot verlangt vier positive versionsgleiche Cluster und beobachtet 40 UE sowie Übergänge erneut.
- [x] Entscheidungspaket mutiert weder `time-model.json` noch einen Produktstatus.
- [x] Ein positiver Minimalpilot empfiehlt ausschließlich `eligible-for-working-availability-review`.
- [x] `reviewed` und `standard` können weder Python noch JavaScript erzeugen.
- [x] Offline-Cockpit besitzt keinen Netzwerk-, Konto-, Backend-, Cookie-, Telemetrie- oder Persistenzweg.
- [x] Import, Fehlerdarstellung, bewusster Download und Zustandsverlust nach Reload funktionieren.
- [x] Native Tastaturbedienung, Labels, sichtbarer Fokus, Error Summary, Live-Status, Reflow, Kontrast und Touchziele sind geprüft.
- [x] Kompilierter Cockpitvertrag ist byteidentisch reproduzierbar.
- [x] Python und JavaScript liefern für alle synthetischen und mutierten Grenzfälle dieselben Resultate.
- [x] Öffentliche Beispiele sind ausschließlich synthetisch; reale Pakete sind im Repository verboten.
- [x] Lehrkräfte- und Reviewanleitung decken Bereitschaft, Aggregation, Wiederholung, Retention, Löschung und drei menschliche Gates ab.
- [x] README nennt Instrument und Aussagegrenze, ohne reale Pilotierung oder Statushochsetzung zu behaupten.
- [x] Phase 0 ruft IUM10, IUM09 und IUM11 genau einmal in dokumentierter Reihenfolge auf.
- [x] `roadmap/time-model.json`, Curriculum, Modulroadmap und bestehende IUM09/IUM10-Validatoren bleiben unverändert.
- [x] Flexible Vertiefungs-, Transfer- und Projektmodule bleiben explizit erhalten.
- [x] Fachreview ist ohne offene Befunde freigegeben.
- [x] Engineering-/Privacy-/Accessibilityreview ist ohne offene Befunde freigegeben.
- [x] Vollständige Testsuite, IUM11-, IUM10-, IUM09- und Phase-0-Validator, Build-, UTF-8-, JSON-, AST-, JavaScript- und Diffgates sind frisch grün.
- [x] Branch, Remote und Draft-PR sind synchron; keine reale Pilotierung, Statusmutation, Releasefreigabe oder Phase 1 wurde ausgeführt.
