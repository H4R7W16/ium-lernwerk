# IuM-Lernwerk V2 Source Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Choose superpowers:subagent-driven-development only when the task graph passes the execution-mode check below; otherwise use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Den unveränderten Phase-0-Quellenbestand und die sechs bislang nur in LXP01 dokumentierten Zusatzquellen in einem gemeinsamen, prüfbaren V2-Quellenfundament zusammenführen, ohne daraus ungeprüfte V2-Claims oder Inhaltsfreigaben abzuleiten.

**Architecture:** Die Phase-0-Register bleiben unveränderte V1-Auditquellen und werden über Pfad, Hash und Zählung versiegelt. Neue V2-Verträge unter `roadmap/v2/foundations/sources/` ergänzen sechs Quellen, definieren Entitäts- und Claimgrenzen und speichern einen reproduzierbaren Linkaudit. Der bestehende V2-Validator prüft die statischen Verträge fail-closed; ein separates Standardbibliothek-Skript aktualisiert den datierten Online-Linkaudit atomar.

**Tech Stack:** Python 3 `unittest`, Python-Standardbibliothek `urllib`, JSON, JSON Schema, npm-Skripte, Git.

**Spec:** `docs/superpowers/specs/2026-09-03-ium-v2-controlled-rebaseline-design.md`

## Global Constraints

- Auf `feat/ium-v2-rebaseline` arbeiten; vor Commits `git fetch --prune` und `git pull --ff-only origin main` ausführen.
- `docs/research/phase-0/source-register.json`, `claim-ledger.json` und `design-principles.json` bleiben unveränderte V1-Auditinputs.
- Die sechs LXP01-Quellen werden registriert, ihre Aussagen aber erst in LXF02 als Claims bewertet.
- Keine Lerninhalte, keine Änderung an LXP05, kein Push, Merge, Hosting, Cutover oder Veröffentlichung.
- Quellen, Claims, Projektentscheidungen, Gestaltungsprinzipien, Materialmuster und Prüfnachweise bleiben getrennte Entitäten.
- Nicht auflösbare Pflichtquellen sind Fehler; eine optionale historische Lücke erzeugt eine Warnung mit Eigentümer und Akzeptanzkriterium.
- Online-Erreichbarkeit ist ein datierter Nachweis und keine Aussage über fachliche Qualität, Rechtslage oder Lernwirksamkeit.
- Deutschsprachiger sichtbarer Text verwendet UTF-8-Umlaute; technische IDs und Dateinamen bleiben ASCII.
- Absolute lokale Pfade und Build-Artefakte dürfen nicht in Verträge oder Git gelangen.

---

### Task 1: Freigegebenes Curriculumgate technisch schließen

**Files:**
- Modify: `tests/test_validate_v2_rebaseline.py`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `roadmap/v2/foundations/curriculum/status.json`

**Interfaces:**
- Consumes: dokumentierte Nutzerfreigabe von IUM-V2-CUR
- Produces: Curriculumstatus `done`, `foundationConcept: reviewed`, `subjectReview: passed`, `nextGate: IUM-V2-SRC`

- [x] **Step 1: Failing approval-transition test schreiben**

```python
def test_curriculum_foundation_accepts_documented_user_approval(self) -> None:
    status = load_real_curriculum_status()
    status["workStatus"] = "done"
    status["maturity"]["foundationConcept"] = "reviewed"
    status["maturity"]["subjectReview"] = "passed"
    status["nextGate"] = "IUM-V2-SRC"
    errors = validate_foundation_status(
        status,
        "curriculum",
        {"V2-REQ-CUR-001", "V2-REQ-CUR-002"},
        PROJECT_ROOT,
    )
    self.assertEqual([], errors)
```

- [x] **Step 2: Test rot ausführen**

Run: `python -B -m unittest discover -s tests -p "test_validate_v2_rebaseline.py"`

Expected: FAIL, weil der Validator weiterhin `review`, `in-review` und `IUM-V2-CUR-REVIEW` erzwingt.

- [x] **Step 3: Freigabestatus minimal implementieren**

Validator und realen Status gemeinsam auf die vier freigegebenen Werte umstellen. `contentImplementation: not-started`, `classroomPilot: not-started` und `release: closed` bleiben unverändert.

- [x] **Step 4: Test grün ausführen**

Run: `python -B -m unittest discover -s tests -p "test_validate_v2_rebaseline.py"`

Expected: alle V2-Tests grün.

### Task 2: Quelleninventar und sechs LXP01-Migrationspfade definieren

**Files:**
- Create: `schemas/v2/source-inventory.schema.json`
- Create: `roadmap/v2/foundations/sources/inventory.json`
- Modify: `tests/test_validate_v2_rebaseline.py`
- Modify: `scripts/validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: 63 Phase-0-Quellen, 51 Claims, 15 Designprinzipien und LXP01 §§ 6.1–6.6
- Produces: `SourceInventoryV1` mit 63 versiegelten Basisquellen, sechs Zusatzquellen und 69 Quellen insgesamt

- [x] **Step 1: Fehlende und unvollständige Inventare rot testen**

Tests müssen mindestens diese Fehler auslösen:

```text
roadmap/v2/foundations/sources/inventory.json fehlt
V2-Quelleninventar muss sechs LXP01-Zusatzquellen enthalten
V2-Quelleninventar muss insgesamt 69 Quellen ausweisen
LXP01-Quelle LXP-SRC-SDT-2024 benötigt einen eindeutigen V2-Migrationspfad
```

- [x] **Step 2: SourceInventoryV1-Schema erstellen**

Das Schema erlaubt ausschließlich:

```json
{
  "schemaVersion": 1,
  "projectId": "ium-lernwerk",
  "asOf": "YYYY-MM-DD",
  "phase0Baseline": {},
  "locatorOverrides": [],
  "lxp01Additions": [],
  "totals": {}
}
```

Jede Zusatzquelle benötigt `legacyId`, `sourceId`, `title`, `authors`, `year`, `sourceKind`, `url`, `doi`, `verificationStatus`, `licenseStatus`, `usageStatus`, `accessed`, `liveCheck`, `migrationState`, `claimMigration` und `recheckTriggers`.

- [x] **Step 3: Phase-0-Baseline versiegeln**

Diese geprüften Werte eintragen:

```json
{
  "sourceRegister": {"path": "docs/research/phase-0/source-register.json", "sha256": "F4B52FB6B8B5C7E31FF3BA73DA63B9D4E46F47B55FC51DFEDAE3F809100D6AB1", "count": 63},
  "claimLedger": {"path": "docs/research/phase-0/claim-ledger.json", "sha256": "5D6D5518FD9896FF052F51E06C52B0758EC031AF7B27E0919498BA5D9982728C", "count": 51},
  "principleLedger": {"path": "docs/research/phase-0/design-principles.json", "sha256": "4F577237E1CC9386DB87D37F7291D1E0C08ACF87C7ED5C85A48E2A6162C87B7B", "count": 15},
  "role": "v1-audit-input"
}
```

- [x] **Step 4: Sechs LXP01-Quellen registrieren**

Exakte Legacy-IDs:

```text
LXP-SRC-SDT-2024
LXP-SRC-SEGMENT-2019
LXP-SRC-SIGNAL-2016
LXP-SRC-W3C-COGA-2021
LXP-SRC-UDL30-2024
LXP-SRC-COS-2023
```

Vier DOI-Quellen erhalten `verificationStatus: metadata-checked` und `usageStatus: citation-only`. W3C erhält `primary-checked` und `reuse-with-notice`; CAST erhält `primary-checked` und `citation-and-link-only`. Alle sechs erhalten `claimMigration: pending-lxf02-claim-review`.

- [x] **Step 5: Lesehilfe-Locator nur in V2 ergänzen**

Für `SRC-CUR-LESEHILFE-2026-27` wird die in IUM-V2-CUR bestätigte Direkt-URL als `locatorOverride` eingetragen. Die V1-Datei bleibt unverändert.

- [x] **Step 6: Inventarvalidierung grün umsetzen**

`validate_source_inventory(data, root)` prüft Hashes, Counts, Legacy-/Source-ID-Mengen, eindeutige IDs, HTTPS/DOI-Formate, Datumsformate, Lizenz-/Nutzungsstatus, Linkcheckdaten, Migrationsstatus und Recheck-Trigger.

### Task 3: Claim- und Entitätsgrenzen fail-closed absichern

**Files:**
- Create: `schemas/v2/source-traceability.schema.json`
- Create: `roadmap/v2/foundations/sources/traceability.json`
- Modify: `tests/test_validate_v2_rebaseline.py`
- Modify: `scripts/validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: kombinierte Menge aus 63 Phase-0- und sechs V2-Zusatzquellen
- Produces: `SourceTraceabilityV1`, Warnungs-/Fehlertrennung und geschlossene Claim-Quelle-Referenzen

- [x] **Step 1: Trennung und Referenzfehler rot testen**

```python
self.assertIn("V2-Quellenmodell benötigt exakt sechs getrennte Entitätstypen", errors)
self.assertIn("Freigaberelevanter Claim CLAIM-LP-001 referenziert unbekannte Quelle SRC-UNKNOWN", errors)
self.assertIn("Nicht auflösbare Pflichtquelle SRC-REQUIRED blockiert das Quellenfundament", errors)
```

Ein optionaler Eintrag mit `resolutionStatus: unresolved` muss dagegen als Warnung zurückgegeben werden.

- [x] **Step 2: SourceTraceabilityV1 erstellen**

Die sechs Entitätstypen sind exakt:

```text
source
claim
project-decision
design-principle
material-pattern
verification-evidence
```

Jeder Typ erhält eine eindeutige Definition und erlaubte Referenzrichtungen. Keine Entität darf still als andere Entität gelten.

- [x] **Step 3: Bestehende Claimbezüge prüfen**

Der Validator liest `claim-ledger.json`, verlangt 51 eindeutige Claims und prüft jede `sourceId` gegen die kombinierte Quellenmenge. Für alle 51 `reviewed` Claims muss mindestens eine `primary-checked` Phase-0-Quelle vorhanden sein.

- [x] **Step 4: Quellenlücken explizit führen**

`SRC-LP-SIGNALING-2018` wird als optionale, derzeit nicht claimtragende Quelle mit `resolutionStatus: needs-primary-recheck`, Eigentümer `LXF02` und Akzeptanzkriterium geführt. Unaufgelöste Pflichtquellen bleiben im realen Vertrag leer und werden vom Validator blockiert.

- [x] **Step 5: Tests und `verify:v2` grün ausführen**

Run: `python -B -m unittest discover -s tests -p "test_validate_v2_rebaseline.py"`

Run: `npm run verify:v2`

Expected: grün mit genau der dokumentierten optionalen Warnung.

### Task 4: Datierbaren Online-Linkaudit implementieren

**Files:**
- Create: `schemas/v2/source-link-audit.schema.json`
- Create: `scripts/check_v2_source_links.py`
- Create: `tests/test_check_v2_source_links.py`
- Create: `roadmap/v2/foundations/sources/link-audit.json`
- Modify: `package.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: `load_targets(root) -> list[SourceTarget]` aus Phase-0-Register und V2-Inventar
- Produces: atomaren Snapshot `SourceLinkAuditV1` und CLI `npm run verify:v2:sources:online`

- [x] **Step 1: Lokalen HTTP-Vertrag rot testen**

Ein Testserver stellt `200`, `302 → 200`, `403`, `404` und `405 HEAD → 200 GET` bereit. Tests beweisen:

```text
200/302 => resolved
403 => restricted, aber auflösbar
404 Pflichtquelle => Fehler und bestehender Snapshot bleibt bytegleich
404 optionale Quelle => Warnung
405 HEAD mit erfolgreichem GET-Fallback => resolved
```

- [x] **Step 2: Linkchecker minimal implementieren**

`probe_target(target)` prüft DOI-Locators am DOI-Resolver ohne Publisher-Download und normale HTTPS-URLs mit Redirects. Es speichert nur Source-ID, geprüften Locator, Ergebnis, HTTP-Code und normalisierte Ziel-URL; keine Seiteninhalte und keine lokalen Pfade.

- [x] **Step 3: Atomisches Schreiben implementieren**

`write_snapshot_atomic(path, payload)` schreibt zuerst eine Nachbardatei und ersetzt das Ziel erst, wenn keine Pflichtquelle `missing` oder `unresolved` ist. Bei Fehlern bleibt der letzte gültige Snapshot unverändert.

- [x] **Step 4: Npm-Skript ergänzen**

```json
"verify:v2:sources:online": "python -B scripts/check_v2_source_links.py --write"
```

- [x] **Step 5: Reales Online-Audit ausführen**

Run: `npm run verify:v2:sources:online`

Expected: 69 Quellen geprüft; keine nicht auflösbare Pflichtquelle. Erreichbarkeitsbeschränkungen werden getrennt von fehlenden Links ausgewiesen.

- [x] **Step 6: Statischen Snapshot validieren**

`validate_source_link_audit(data, inventory, root)` prüft exakte Quellenmenge, Eindeutigkeit, Stichtag, Locatorbindung, Ergebnissenums und die Nullmenge blockierender Pflichtquellen.

### Task 5: Quellenstatus, Reviewpaket und Regressionen abschließen

**Files:**
- Create: `roadmap/v2/foundations/sources/status.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`
- Modify: Workspace-Task, Initiative, Kanban, Roadmap und Entwicklungshistorie
- Create: Session Summary unter `Vault/50_Codex/Sessions/`

**Interfaces:**
- Consumes: Inventar, Traceability und Linkaudit
- Produces: Quellenfundament höchstens im Status `review`

- [x] **Step 1: Statusvertrag rot testen**

Der Quellenstatus muss `V2-REQ-SRC-001`, alle drei V2-Quellenverträge und das Test-/Validatorpaar referenzieren. Er darf keine Inhaltsimplementierung, Pilotierung oder Releasefreigabe beanspruchen.

- [x] **Step 2: Realen Status erstellen**

Setzen:

```text
workStatus: review
foundationConcept: draft
dataVerification: passed
contentImplementation: not-started
technicalVerification: passed
subjectReview: in-review
release: closed
nextGate: IUM-V2-SRC-REVIEW
```

- [x] **Step 3: Proportionale Verifikation ausführen**

Run: `npm run verify:v2`

Run: `python -B -m unittest discover -s tests -p "test_*.py"`

Run unter Node 22.22.0/npm 10.9.4: `npm run typecheck`, `npm run test:platform`, `npm run verify:phase1` und `npm run verify:ium5`.

Zusätzlich: V1-Diff gegen `dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0` für `docs/research/phase-0`, `curriculum`, `modules`, `pilot` und bestehende `roadmap/*`-Verträge muss leer sein.

- [x] **Step 4: Unabhängigen Read-only-Code-Review durchführen**

Reviewer prüft Contract-Schema-Parität, Crashfreiheit bei syntaktisch gültigem Fehlinput, Pflicht-/Optionaltrennung, atomische Snapshotlogik und fehlende Claim-Automatik. Findings werden vor dem Nutzerreview testgetrieben geschlossen.

- [x] **Step 5: Remote-Abgleich und lokalen Commit erstellen**

Run: `git fetch --prune`

Run: `git pull --ff-only origin main`

Commit: `feat(v2): consolidate source foundation`

- [x] **Step 6: Workspace-Handoff auf Review aktualisieren**

IUM-V2-SRC bleibt bis zur ausdrücklichen Nutzerfreigabe `review`. LXF01 wird nicht automatisch gestartet. Push, Merge, Inhaltsproduktion und Cutover bleiben geschlossen.

## Execution-mode check

Use **Inline Execution** with `superpowers:executing-plans`. Alle Tasks ändern denselben V2-Validator, denselben Testbestand, denselben Quellenvertragsbaum und denselben Feature-Branch; sichere unabhängige Schreibbereiche fehlen.
