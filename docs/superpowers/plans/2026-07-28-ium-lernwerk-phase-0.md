# IuM-Lernwerk Phase 0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ein quellenkritisch kuratiertes Forschungs- und Curriculumfundament erstellen, das ein belastbares Fachprofil, ein vollständiges Curriculum-Mapping und eine daraus abgeleitete Modulroadmap für Informatik und Medienbildung am Gymnasium in Baden-Württemberg, Klassen 5–7, bereitstellt.

**Architecture:** Die kanonischen Projektartefakte liegen im Git-Repository. Forschungsberichte werden als Rohberichte, kuratierte Synthesen, Quellenregister und Claim-Ledger getrennt; curriculare Vorgaben werden quellentreu in JSON-Datensätze überführt und durch einen Crosswalk zusammengeführt. Ein kleiner Python-Validator ohne externe Abhängigkeiten prüft Referenzen, Statuswerte, Abdeckung und Roadmap-Konsistenz; der Vault erhält nur Projektsteuerung und einen schlanken Routing-Adapter zum kanonischen Fachprofil.

**Tech Stack:** Markdown, JSON, Python 3.11+ Standardbibliothek, `unittest`, Git; Deep Research in ChatGPT Web oder eine gleichwertige quellenfähige Rechercheumgebung.

## Global Constraints

- Maßgebliche fachliche Spezifikation ist Commit `7801361` der Datei `docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md`.
- Das Hybridmodell ist ausdrücklich bestätigt: Der progressive Kernlernweg wird durch flexibel einsetzbare Vertiefungs-, Transfer- und Projektmodule ergänzt. Die zwischenzeitlich gelöschte Zeile in Abschnitt 2.2 wurde auf Nutzerauftrag am 28. Juli 2026 wiederhergestellt.
- Phase 0 erstellt keine Lernendenanwendung, kein Portal, keine PWA, keinen Local-First-Speicher und kein Pilotmodul.
- Geltungsbereich ist Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E.
- Die Lesehilfe 2026/2027 wird als Planungs- und Orientierungsgrundlage, nicht als bereits in Kraft gesetzter Bildungsplan behandelt.
- Normative Abdeckung berücksichtigt gemeinsam die Lesehilfe 2026/2027, den Bildungsplan 2016 Basiskurs Medienbildung, den Bildungsplan 2016 Aufbaukurs Informatik Klasse 7 sowie zugehörige Prozesskompetenzen und Operatoren.
- Rechercheergebnisse werden als `draft`, `working`, `reviewed` oder `standard` gekennzeichnet. Ein Deep-Research-Bericht ist niemals automatisch `reviewed`.
- Primärquellen, amtliche Quellen, systematische Reviews und peer-reviewte Forschung haben Vorrang. Sekundärdarstellungen dürfen Primärquellen erschließen, aber nicht verdecken.
- Jede kuratierte Behauptung verweist auf registrierte Quellen, nennt Reichweite und Einschränkungen und trennt Befund von Projektentscheidung.
- Quellen und Zitate werden nicht erfunden. Verbatim-Zitate bleiben kurz und werden mit Fundstelle dokumentiert.
- Eigene Inhalte tragen `CC BY-SA 4.0`; Validierungscode trägt `MIT`.
- Sichtbarer deutscher Text verwendet UTF-8-Umlaute und `ß`; technische IDs und Dateinamen bleiben ASCII-stabil.
- Es werden keine personenbezogenen Daten, Lernprofile oder diagnostischen Nutzungsdaten erhoben.
- Das zunächst vollständige Beurteilungsinstrumentarium bleibt `working` und darf die curriculare Architektur nicht dominieren.
- Der kanonische Projektbestand liegt im Repository. Der Vault enthält Steuerung, Handoff und einen Routing-Adapter, keine zweite vollständige Kopie des Forschungsbestands.
- Vor jedem Task: `git status --short --branch` prüfen. Wenn ein Remote vorhanden ist, vor dem Schreiben `git fetch --prune` und `git pull --ff-only` ausführen. Ohne Remote sind lokale Commits zulässig; Push bleibt gesperrt und wird dokumentiert.
- Jede Task endet mit einem prüfbaren Artefakt, erfolgreichen zielgerichteten Tests und einem kleinen, absichtlich zusammengestellten Commit.

## File Map

| Pfad | Verantwortung |
|---|---|
| `README.md` | Projektstatus, Phase-0-Einstieg, Lizenzen und Validierungsbefehle |
| `LICENSE` | MIT-Lizenz für eigenen Code |
| `LICENSE-CONTENT.md` | CC-BY-SA-4.0-Regel für eigene Inhalte und Kennzeichnung von Drittmaterial |
| `docs/research/phase-0/README.md` | Forschungsarchitektur, Paketstatus und Integrationsreihenfolge |
| `docs/research/phase-0/research-protocol.md` | Such-, Auswahl-, Prüf- und Kurationsprotokoll |
| `docs/research/phase-0/data-contract.md` | Verbindliche Felder und Statuswerte für Quellen, Claims und Designprinzipien |
| `docs/research/phase-0/source-register.json` | Zentrales Register aller amtlichen und wissenschaftlichen Quellen |
| `docs/research/phase-0/claim-ledger.json` | Kuratierte Aussagen mit Quellen, Reichweite, Evidenz und Designfolgen |
| `docs/research/phase-0/prompts/*.md` | Vollständige, reproduzierbare Deep-Research-Aufträge |
| `docs/research/phase-0/raw/*.md` | Unveränderte Rechercheeingänge mit Ausführungsmetadaten |
| `docs/research/phase-0/curated/*.md` | Quellenkritisch kuratierte Paketberichte |
| `docs/research/phase-0/synthesis.md` | Paketübergreifende Synthese und Konfliktanalyse |
| `docs/research/phase-0/design-principles.json` | Forschungsbasierte, maschinenprüfbare Designprinzipien |
| `docs/fachprofil/ium-gymnasium-5-7.md` | Kanonisches Fach-/Stufenprofil des Lernwerks |
| `curriculum/source-status.md` | Geltungsstatus, Version, Abrufdatum und Prüfnachweis jeder normativen Quelle |
| `curriculum/extraction-protocol.md` | Regeln für quellentreue Extraktion, IDs, Fundstellen und Änderungsnachverfolgung |
| `curriculum/lesehilfe-2026-27/competencies.json` | Niveau-E-Kompetenzen und Progressionshinweise der Lesehilfe |
| `curriculum/basiskurs-medienbildung/competencies.json` | Kompetenzen des Bildungsplans 2016 Basiskurs Medienbildung |
| `curriculum/aufbaukurs-informatik/competencies.json` | Kompetenzen des Bildungsplans 2016 Aufbaukurs Informatik Klasse 7 |
| `curriculum/operators.json` | Operatoren, Prozesskompetenzen und sichtbare Lernhandlungen |
| `curriculum/crosswalk.json` | Beziehungen, Überschneidungen, Erweiterungen und offene Differenzen zwischen den Quellen |
| `curriculum/progression.md` | Begründete Progression für Klassen 5, 6 und 7 |
| `roadmap/module-candidates.json` | Maschinenlesbare Kandidaten mit Kompetenzen, Voraussetzungen und Zeitkorridor |
| `roadmap/module-roadmap.md` | Lesbare Kernlernweg-, Vertiefungs- und Projektroadmap |
| `roadmap/coverage-plan.json` | Nachweis, welche Module welche verbindlichen Kompetenzen abdecken |
| `scripts/validate_phase0.py` | Standardbibliotheks-Validator und CLI |
| `tests/test_validate_phase0.py` | Unit-Tests für Datenvertrag und Abdeckungsregeln |
| `Vault/20_Wissen/Didaktik/Unterrichtsplanung/Fachprofile/Informatik und Medienbildung Gymnasium 5-7 - Planungsprofil.md` | Schlanker Workspace-Routing-Adapter zum kanonischen Profil |

## Dependency Flow

```text
Task 1 Forschungsvertrag und Validator
├── Task 2 Normative Quellenbasis
│   ├── Task 9 Lesehilfe
│   ├── Task 10 Basiskurs Medienbildung
│   └── Task 11 Aufbaukurs Informatik
└── Tasks 3–6 Recherchepakete
    └── Task 7 Forschungssynthese
        └── Task 8 Fachprofil

Tasks 9–11
└── Task 12 Crosswalk und Progression

Task 8 + Task 12
└── Task 13 Modulkandidaten
    └── Task 14 Roadmap und Abdeckung
        └── Task 15 Phase-0-Abschlussreview
```

---

### Task 1: Forschungsvertrag, Lizenzen und Validierungskern

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `LICENSE-CONTENT.md`
- Create: `docs/research/phase-0/README.md`
- Create: `docs/research/phase-0/research-protocol.md`
- Create: `docs/research/phase-0/data-contract.md`
- Create: `docs/research/phase-0/source-register.json`
- Create: `docs/research/phase-0/claim-ledger.json`
- Create: `scripts/validate_phase0.py`
- Create: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: freigegebene Gesamtspezifikation auf Commit `7801361`
- Produces: `ValidationError`, `load_json(path)`, `validate_source_register(payload)`, `validate_claim_ledger(payload, source_ids)` und die verbindlichen Datenverträge für alle späteren Tasks

- [ ] **Step 1: Repo- und Spezifikationsintegrität prüfen**

Run:

```powershell
git status --short --branch
git diff -- docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md
git show HEAD:docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md
git remote -v
```

Expected:

- Die Arbeitskopie ist sauber und Abschnitt 2.2 enthält beide bestätigten Zugänge.
- Der Ausführungsbranch enthält Commit `63baa9e` sowie die wiederhergestellte Hybridmodell-Zeile.
- Spätere Änderungen am Verhältnis von Kern- und Ergänzungsmodulen benötigen eine eigene Spezifikationsrevision und Nutzerfreigabe.

- [ ] **Step 2: Failing tests für Quellen- und Claim-Verträge schreiben**

Add these tests to `tests/test_validate_phase0.py`:

```python
import unittest

from scripts.validate_phase0 import (
    ValidationError,
    validate_claim_ledger,
    validate_source_register,
)


class SourceRegisterTests(unittest.TestCase):
    def test_duplicate_source_id_is_rejected(self):
        payload = {
            "schemaVersion": 1,
            "sources": [
                {
                    "id": "SRC-001",
                    "package": "official",
                    "sourceKind": "official",
                    "title": "Quelle A",
                    "authors": ["Institution A"],
                    "year": 2026,
                    "url": "https://example.org/a",
                    "doi": None,
                    "license": "unknown",
                    "accessed": "2026-07-28",
                    "verificationStatus": "primary-checked",
                    "relevance": ["curriculum"],
                },
                {
                    "id": "SRC-001",
                    "package": "official",
                    "sourceKind": "official",
                    "title": "Quelle B",
                    "authors": ["Institution B"],
                    "year": 2026,
                    "url": "https://example.org/b",
                    "doi": None,
                    "license": "unknown",
                    "accessed": "2026-07-28",
                    "verificationStatus": "primary-checked",
                    "relevance": ["curriculum"],
                },
            ],
        }
        with self.assertRaises(ValidationError):
            validate_source_register(payload)


class ClaimLedgerTests(unittest.TestCase):
    def test_reviewed_claim_requires_registered_source_and_limitations(self):
        payload = {
            "schemaVersion": 1,
            "claims": [
                {
                    "id": "CLAIM-INF-001",
                    "package": "informatikdidaktik",
                    "statement": "Codeverständnis braucht gezielte Aufgaben.",
                    "scope": "Sekundarstufe I",
                    "status": "reviewed",
                    "evidenceLevel": "medium",
                    "sourceIds": ["SRC-NOT-REGISTERED"],
                    "limitations": "",
                    "designImplications": ["Codeerklärung als Lernhandlung vorsehen."],
                }
            ],
        }
        with self.assertRaises(ValidationError):
            validate_claim_ledger(payload, {"SRC-001"})
```

- [ ] **Step 3: Tests ausführen und erwartetes Scheitern prüfen**

Run:

```powershell
python -m unittest tests.test_validate_phase0 -v
```

Expected: `ERROR` mit `ModuleNotFoundError: No module named 'scripts.validate_phase0'`.

- [ ] **Step 4: Minimalen Validator implementieren**

Create `scripts/validate_phase0.py` with these public contracts:

```python
import json
from pathlib import Path


class ValidationError(ValueError):
    pass


SOURCE_KINDS = {
    "official",
    "systematic-review",
    "meta-analysis",
    "empirical-study",
    "research-synthesis",
    "handbook",
    "professional-standard",
    "secondary",
}
VERIFICATION_STATUSES = {
    "primary-checked",
    "metadata-checked",
    "secondary-only",
}
CLAIM_STATUSES = {"draft", "working", "reviewed", "standard"}
EVIDENCE_LEVELS = {"low", "medium", "high", "normative"}


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition, message):
    if not condition:
        raise ValidationError(message)


def validate_source_register(payload):
    _require(payload.get("schemaVersion") == 1, "source register schemaVersion must be 1")
    sources = payload.get("sources")
    _require(isinstance(sources, list), "sources must be a list")
    ids = [source.get("id") for source in sources]
    _require(all(isinstance(source_id, str) and source_id for source_id in ids), "every source needs an id")
    _require(len(ids) == len(set(ids)), "source ids must be unique")
    for source in sources:
        _require(source.get("sourceKind") in SOURCE_KINDS, f"invalid source kind: {source.get('id')}")
        _require(
            source.get("verificationStatus") in VERIFICATION_STATUSES,
            f"invalid verification status: {source.get('id')}",
        )
        _require(isinstance(source.get("title"), str) and source["title"].strip(), f"title missing: {source.get('id')}")
        _require(isinstance(source.get("relevance"), list) and source["relevance"], f"relevance missing: {source.get('id')}")
    return set(ids)


def validate_claim_ledger(payload, source_ids):
    _require(payload.get("schemaVersion") == 1, "claim ledger schemaVersion must be 1")
    claims = payload.get("claims")
    _require(isinstance(claims, list), "claims must be a list")
    ids = [claim.get("id") for claim in claims]
    _require(len(ids) == len(set(ids)), "claim ids must be unique")
    for claim in claims:
        _require(claim.get("status") in CLAIM_STATUSES, f"invalid claim status: {claim.get('id')}")
        _require(claim.get("evidenceLevel") in EVIDENCE_LEVELS, f"invalid evidence level: {claim.get('id')}")
        _require(set(claim.get("sourceIds", [])) <= source_ids, f"unknown source id: {claim.get('id')}")
        if claim.get("status") in {"reviewed", "standard"}:
            _require(claim.get("sourceIds"), f"reviewed claim has no source: {claim.get('id')}")
            _require(str(claim.get("limitations", "")).strip(), f"reviewed claim has no limitations: {claim.get('id')}")
    return set(ids)


def main():
    root = Path(__file__).resolve().parents[1]
    source_ids = validate_source_register(
        load_json(root / "docs/research/phase-0/source-register.json")
    )
    validate_claim_ledger(
        load_json(root / "docs/research/phase-0/claim-ledger.json"),
        source_ids,
    )
    print("phase 0 validation passed")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Leere, valide Register und den Datenvertrag anlegen**

Create:

```json
{
  "schemaVersion": 1,
  "sources": []
}
```

in `docs/research/phase-0/source-register.json`, and:

```json
{
  "schemaVersion": 1,
  "claims": []
}
```

in `docs/research/phase-0/claim-ledger.json`.

Document in `data-contract.md` every field shown in the tests, the allowed enum values from the validator, deterministic IDs (`SRC-`, `CLAIM-INF-`, `CLAIM-MED-`, `CLAIM-LP-`, `CLAIM-DLE-`) and the rule that `reviewed` requires a checked source plus explicit limitations.

- [ ] **Step 6: Forschungsprotokoll und Lizenzrahmen schreiben**

`research-protocol.md` must define:

1. search question;
2. inclusion and exclusion criteria;
3. priority of primary sources and systematic evidence;
4. source registration before claim creation;
5. claim-level verification against the cited original;
6. separation of evidence, interpretation and project decision;
7. quotation and copyright limits;
8. status transition `draft → working → reviewed → standard`;
9. update and correction procedure;
10. package-specific and integration review gates.

`LICENSE` contains the standard MIT text with `Copyright (c) 2026 IuM-Lernwerk contributors`. `LICENSE-CONTENT.md` states that own repository content is CC BY-SA 4.0 unless a file says otherwise and that third-party material retains its own license.

- [ ] **Step 7: Tests und Encoding-Gate ausführen**

Run:

```powershell
python -m unittest tests.test_validate_phase0 -v
python -c "from scripts.validate_phase0 import load_json, validate_claim_ledger, validate_source_register; s=load_json('docs/research/phase-0/source-register.json'); ids=validate_source_register(s); validate_claim_ledger(load_json('docs/research/phase-0/claim-ledger.json'), ids); print('phase0 contracts valid')"
rg -n "T[B]D|T[O]DO|F[I]XME|PLACEH[O]LDER" README.md LICENSE-CONTENT.md docs/research/phase-0 scripts tests
$encodingHits = Get-ChildItem README.md, LICENSE-CONTENT.md, docs/research/phase-0, scripts, tests -Recurse -File | Select-String -Pattern ([char]0x00C3), ([char]0x00C2), ([char]0xFFFD)
if ($encodingHits) { $encodingHits; throw "Möglicher Zeichensatzfehler" }
```

Expected: tests `OK`, message `phase0 contracts valid`, and `rg` returns no matches.

- [ ] **Step 8: Commit**

```powershell
git add README.md LICENSE LICENSE-CONTENT.md docs/research/phase-0 scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "chore: establish phase 0 research contract"
```

---

### Task 2: Amtliche Quellenbasis und Extraktionsprotokoll

**Files:**
- Create: `curriculum/source-status.md`
- Create: `curriculum/extraction-protocol.md`
- Modify: `docs/research/phase-0/source-register.json`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: `validate_source_register(payload)`
- Produces: registrierte normative Quellen `SRC-CUR-*`, einen dokumentierten Geltungsstatus und reproduzierbare Extraktionsregeln für Tasks 9–12

- [ ] **Step 1: Amtliche Quellen frisch prüfen**

Open and verify:

```text
https://km.baden-wuerttemberg.de/de/schule/schulartuebergreifend/mint/schule-und-unterricht/informatik-und-medienbildung
https://km.baden-wuerttemberg.de/de/schule/schulartuebergreifend/faq-bildungsreform
https://www.bildungsplaene-bw.de/%2CLde/LS/BP2016BW/ALLG/GYM/BMB
https://www.bildungsplaene-bw.de/%2CLde/LS/BP2016BW/ALLG/GYM/INF7
```

Also inspect:

```text
Assets/PDFs/Lesehilfe Informatik und Medienbildung Klassen 5 bis 7 2026-2027.pdf
SHA-256 1BC94255AD35D75782B819C1CA425D7C1F21CEDC6B2012378EC828BAC1451008
```

Expected: each source has title, issuing body, version/date, URL or asset path, access date, legal/administrative status and a precise note about its role.

- [ ] **Step 2: Failing test für normative Statusangaben schreiben**

Add a test that passes one `official` source without `normativeStatus` and expects `ValidationError`. Allowed values are:

```python
NORMATIVE_STATUSES = {
    "enacted",
    "orientation",
    "administrative-information",
    "superseded",
}
```

- [ ] **Step 3: Test ausführen und erwartetes Scheitern prüfen**

Run:

```powershell
python -m unittest tests.test_validate_phase0.SourceRegisterTests -v
```

Expected: FAIL because `validate_source_register` does not yet require `normativeStatus` for official sources.

- [ ] **Step 4: Normativstatus validieren**

Extend `validate_source_register` so every source with `sourceKind == "official"` requires one allowed `normativeStatus`. Non-official sources use `normativeStatus: null`.

- [ ] **Step 5: Quellen registrieren und Statusbericht schreiben**

Register at least:

- `SRC-CUR-LESEHILFE-2026-27`
- `SRC-CUR-KM-FACHSEITE`
- `SRC-CUR-KM-FAQ-REFORM`
- `SRC-CUR-BMB-2016`
- `SRC-CUR-INF7-2016`

Write `source-status.md` with one section per source and an explicit synthesis: which source is binding, which is orientation, where versions diverge, and which change monitor is needed for the future Fachplan.

- [ ] **Step 6: Extraktionsprotokoll schreiben**

`extraction-protocol.md` must require:

- verbatim competency wording with source locator;
- preservation of official numbering;
- deterministic fallback IDs when no official number exists;
- explicit grade, level and competency area;
- separation of competency text, examples, explanatory prose and local interpretation;
- dual review against rendered page and extracted text for the PDF;
- no silent merging of similar competencies;
- source-level change log;
- `verified`, `plausible` or `open` at record level.

- [ ] **Step 7: Validate and commit**

Run:

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
git diff --check
```

Expected: all tests pass and the validator reports a valid source register.

```powershell
git add curriculum/source-status.md curriculum/extraction-protocol.md docs/research/phase-0/source-register.json scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "docs: register authoritative curriculum sources"
```

---

### Task 3: Recherchepaket Informatikdidaktik Klassen 5–7

**Files:**
- Create: `docs/research/phase-0/prompts/01-informatikdidaktik.md`
- Create: `docs/research/phase-0/raw/01-informatikdidaktik.md`
- Create: `docs/research/phase-0/curated/01-informatikdidaktik.md`
- Modify: `docs/research/phase-0/source-register.json`
- Modify: `docs/research/phase-0/claim-ledger.json`

**Interfaces:**
- Consumes: `research-protocol.md`, Source/Claim contracts
- Produces: reviewed claims `CLAIM-INF-*` on progression, misconceptions, representations, programming practices and medium choice

- [ ] **Step 1: Vollständigen Deep-Research-Auftrag speichern**

Save this prompt in `prompts/01-informatikdidaktik.md`:

```text
Erstelle einen quellenkritischen Forschungsbericht zur Informatikdidaktik für Lernende im Alter von etwa 10 bis 13 Jahren, mit Blick auf einen gymnasialen Lernweg in den Klassen 5 bis 7. Untersuche: Progression von Algorithmen und Programmierung; Code lesen, erklären, vorhersagen, modifizieren, testen und selbst entwickeln; Daten und Codierung; Netze und Client-Server-Modelle; grundlegende Kryptografie; typische Fehlvorstellungen; geeignete externe Repräsentationen; worked examples, explizite Anleitung, Exploration und selbstständiges Problemlösen; blockbasierte und textbasierte Zugänge; fachlich begründete unplugged- und digitale Aktivitäten.

Priorisiere systematische Reviews, Meta-Analysen, peer-reviewte Primärstudien, etablierte Forschungsrahmen und offizielle professionelle Standards. Trenne robuste Befunde, plausible didaktische Heuristiken und offene Kontroversen. Gib für jede zentrale Aussage DOI oder direkte URL, Publikationsart, untersuchte Altersgruppe, Reichweite, methodische Einschränkungen und konkrete Konsequenzen für Lernziele, Aufgaben, Scaffolds, Fehlvorstellungsdiagnose und Lernprodukte an. Prüfe Originalquellen für die wichtigsten Claims. Vermeide lange Zitate und kennzeichne Übertragungen auf Baden-Württemberg als Projektinferenz.

Ausgabe: 1. Executive Summary; 2. Such- und Auswahlbeschreibung; 3. Evidenzmatrix; 4. Progression 5–7; 5. Fehlvorstellungen; 6. Aufgaben- und Repräsentationsdesign; 7. analog versus digital; 8. kontroverse oder schwache Evidenz; 9. priorisierte Designfolgen; 10. vollständiges Quellenverzeichnis mit stabilen Links.
```

- [ ] **Step 2: Deep Research ausführen und Rohbericht unverändert sichern**

Run the prompt in ChatGPT Web Deep Research or an equivalent source-capable environment. Determine the execution date with `Get-Date -Format 'yyyy-MM-dd'`. Add only YAML frontmatter with `package: informatikdidaktik`, the actual printed date as `executed`, `status: raw` and `prompt: ../prompts/01-informatikdidaktik.md` above the unchanged result.

- [ ] **Step 3: Quellen registrieren und Top-Claims gegen Originale prüfen**

For every source used in a retained claim:

1. open DOI or original publisher/institution page;
2. verify title, authors, year and study type;
3. register it as `SRC-INF-*`;
4. mark `primary-checked`, `metadata-checked` or `secondary-only`;
5. reject unverifiable citations.

- [ ] **Step 4: Kuratierten Bericht schreiben**

`curated/01-informatikdidaktik.md` must contain:

- scope and source quality;
- 8–15 retained claims;
- evidence and limitations per claim;
- age/stage transfer caveats;
- recommended progression 5–7;
- misconceptions and diagnostic opportunities without personal data storage;
- design consequences for module grammar;
- justified analog/digital choices;
- discarded or downgraded claims with reason;
- open research questions.

Add each retained claim to `claim-ledger.json` as `working` or `reviewed`; never `standard`.

- [ ] **Step 5: Validate and commit**

Run:

```powershell
python scripts/validate_phase0.py
rg -n "T[B]D|T[O]DO|F[I]XME|PLACEH[O]LDER" docs/research/phase-0
$encodingHits = Get-ChildItem docs/research/phase-0 -Recurse -File | Select-String -Pattern ([char]0x00C3), ([char]0x00C2), ([char]0xFFFD)
if ($encodingHits) { $encodingHits; throw "Möglicher Zeichensatzfehler" }
git diff --check
```

Expected: no unknown source IDs, no encoding hits and no red-flag matches.

```powershell
git add docs/research/phase-0
git commit -m "research: curate informatics didactics evidence"
```

---

### Task 4: Recherchepaket Didaktik der Medienbildung

**Files:**
- Create: `docs/research/phase-0/prompts/02-medienbildung.md`
- Create: `docs/research/phase-0/raw/02-medienbildung.md`
- Create: `docs/research/phase-0/curated/02-medienbildung.md`
- Modify: `docs/research/phase-0/source-register.json`
- Modify: `docs/research/phase-0/claim-ledger.json`

**Interfaces:**
- Consumes: research protocol and registers
- Produces: reviewed claims `CLAIM-MED-*` on digital agency, information quality, platform mechanisms, safety, media effects and production

- [ ] **Step 1: Vollständigen Deep-Research-Auftrag speichern**

Save:

```text
Erstelle einen quellenkritischen Forschungsbericht zur Didaktik der Medienbildung für Lernende im Alter von etwa 10 bis 13 Jahren. Im Zentrum stehen informationelle Selbstbestimmung, personenbezogene Daten und Metadaten, Quellenprüfung und Informationsqualität, KI-generierte Rechercheergebnisse, Plattform-, Werbe- und Personalisierungslogiken, digitale Kommunikation und Cybermobbing, Gaming und Monetarisierung, Desinformation und Deepfakes, Medienwirkung, Geschlechterrollen und Schönheitsideale, produktive Mediengestaltung, Urheberrecht, offene Lizenzen, digitale Mündigkeit und Partizipation.

Untersuche nicht nur Themen, sondern wirksame fachliche Lernhandlungen: technische Mechanismen erklären, Interessen und Wirkungen analysieren, Belege prüfen, Gestaltungsmittel gezielt einsetzen, Sicherheits- und Handlungsentscheidungen begründen und Medienprodukte revidieren. Priorisiere peer-reviewte Forschung, systematische Reviews, belastbare Jugendmedienstudien, offizielle Kompetenzrahmen und Primärquellen. Trenne empirische Befunde, normative Zielsetzungen und Projektentscheidungen. Gib DOI oder direkte URL, Altersgruppe, Kontext, Reichweite und Einschränkungen an. Vermeide reine Chancen-Risiken-Listen sowie lange Zitate.

Ausgabe: 1. Executive Summary; 2. Such- und Auswahlbeschreibung; 3. Evidenzmatrix; 4. Lernprogression 5–7; 5. typische Fehl- und Alltagsvorstellungen; 6. geeignete Analyse-, Urteils- und Produktionsaufgaben; 7. sichere und altersangemessene Unterrichtssettings; 8. kontroverse oder schwache Evidenz; 9. priorisierte Designfolgen; 10. vollständiges Quellenverzeichnis mit stabilen Links.
```

- [ ] **Step 2: Deep Research ausführen und Rohbericht sichern**

Determine the execution date with `Get-Date -Format 'yyyy-MM-dd'`. Use YAML frontmatter with `package: medienbildung`, the actual printed date as `executed`, `status: raw` and `prompt: ../prompts/02-medienbildung.md`.

- [ ] **Step 3: Quellen und Claims prüfen**

Register retained sources as `SRC-MED-*`. Verify high-impact claims against originals, especially claims about youth behavior, media effects, misinformation, cyberbullying and gaming.

- [ ] **Step 4: Kuratierten Bericht und Claim-Ledger aktualisieren**

Use the same ten-section curation structure as Task 3, but include an explicit matrix:

```text
technischer Mechanismus → gesellschaftliche Wirkung → fachliche Lernhandlung → mögliches Lernprodukt
```

Mark normative competence frameworks as `evidenceLevel: normative`, not as empirical proof.

- [ ] **Step 5: Validate and commit**

```powershell
python scripts/validate_phase0.py
git diff --check
git add docs/research/phase-0
git commit -m "research: curate media education evidence"
```

---

### Task 5: Recherchepaket Lernpsychologie und Unterrichtswissenschaft

**Files:**
- Create: `docs/research/phase-0/prompts/03-lernpsychologie-unterricht.md`
- Create: `docs/research/phase-0/raw/03-lernpsychologie-unterricht.md`
- Create: `docs/research/phase-0/curated/03-lernpsychologie-unterricht.md`
- Modify: `docs/research/phase-0/source-register.json`
- Modify: `docs/research/phase-0/claim-ledger.json`

**Interfaces:**
- Consumes: research protocol, local IBBW WU corpus
- Produces: reviewed claims `CLAIM-LP-*` on prior knowledge, cognitive load, scaffolding, practice, retrieval, transfer, feedback, motivation and multimedia learning

- [ ] **Step 1: Lokale Ausgangsbasis inventarisieren**

Read at minimum:

```text
Vault/20_Wissen/Didaktik/Wirksamer Unterricht/IBBW WU Band 1 - Grundlagen wirksamer Unterricht.md
Vault/20_Wissen/Didaktik/Wirksamer Unterricht/IBBW WU Band 3 - Konstruktive Unterstuetzung.md
Vault/20_Wissen/Didaktik/Wirksamer Unterricht/IBBW WU Band 6 - Aufgaben im Fachunterricht.md
Vault/20_Wissen/Didaktik/Wirksamer Unterricht/IBBW WU Band 9 - Digitale Medien.md
```

Record which claims are already locally supported and which require fresh primary-source checks.

- [ ] **Step 2: Vollständigen Deep-Research-Auftrag speichern**

Save:

```text
Erstelle einen quellenkritischen Forschungsbericht zur Lernpsychologie und Unterrichtswissenschaft für ein digitales, lehrkraftorchestriertes Lernwerk in Informatik und Medienbildung, Klassen 5 bis 7. Untersuche Vorwissen und Fehlvorstellungen, kognitive Aktivierung, Cognitive Load, worked examples und Beispielvariation, Scaffolding und fading, Übungsfolgen, Abruf und langfristige Festigung, Transfer, Feedback, Motivation, Selbstregulation, multimediales Lernen, produktives Scheitern beziehungsweise angeleitete Exploration, konstruktive Unterstützung und Aufgabenqualität.

Priorisiere Meta-Analysen, systematische Reviews, belastbare Forschungsprogramme und Primärstudien. Prüfe, ob Befunde tatsächlich für 10- bis 13-Jährige, digitale Lernumgebungen oder Informatik-/Medienbildungsaufgaben gelten. Trenne robuste allgemeine Lernprinzipien von domänenspezifischen Übertragungen. Beziehe die IBBW-Reihe Wirksamer Unterricht als lokalen Syntheserahmen ein, führe zentrale Aussagen aber soweit möglich auf Originalquellen zurück. Gib DOI oder direkte URL, Kontext, Effektbereich, Moderatoren, Einschränkungen und konkrete Designfolgen an. Vermeide pauschale Effektstärken ohne Kontext und lange Zitate.

Ausgabe: 1. Executive Summary; 2. Such- und Auswahlbeschreibung; 3. Evidenzmatrix; 4. Prinzipien für die siebenstufige Modulgrammatik; 5. Übungs- und Festigungsarchitektur; 6. Scaffolding und fading; 7. Feedback und Selbstregulation ohne zentrale Diagnostik; 8. Multimedia- und Interaktivitätsregeln; 9. Konflikte und schwache Evidenz; 10. Quellenverzeichnis.
```

- [ ] **Step 3: Deep Research ausführen und Rohbericht sichern**

Determine the execution date with `Get-Date -Format 'yyyy-MM-dd'`. Use YAML frontmatter with `package: lernpsychologie-unterricht`, the actual printed date as `executed`, `status: raw` and `prompt: ../prompts/03-lernpsychologie-unterricht.md`.

- [ ] **Step 4: Kuratieren und gegen IBBW abgleichen**

For each retained claim:

- register source as `SRC-LP-*`;
- identify whether IBBW, original research or both support it;
- record moderators and transfer limits;
- state the exact affected module phase;
- reject claims that merely justify “more interactivity” without a learning mechanism.

- [ ] **Step 5: Validate and commit**

```powershell
python scripts/validate_phase0.py
git diff --check
git add docs/research/phase-0
git commit -m "research: curate learning science evidence"
```

---

### Task 6: Recherchepaket Digitale Lernumgebungen und OER

**Files:**
- Create: `docs/research/phase-0/prompts/04-digitale-lernumgebungen-oer.md`
- Create: `docs/research/phase-0/raw/04-digitale-lernumgebungen-oer.md`
- Create: `docs/research/phase-0/curated/04-digitale-lernumgebungen-oer.md`
- Modify: `docs/research/phase-0/source-register.json`
- Modify: `docs/research/phase-0/claim-ledger.json`

**Interfaces:**
- Consumes: research protocol and approved privacy/open design decisions
- Produces: reviewed claims `CLAIM-DLE-*` on accessibility, privacy, offline use, OER reuse and sustainable static delivery

- [ ] **Step 1: Vollständigen Deep-Research-Auftrag speichern**

Save:

```text
Erstelle einen quellenkritischen Forschungsbericht zu digitalen Lernumgebungen und Open Educational Resources für ein öffentliches, statisches, konto- und backendfreies Lernwerk für schulische iPads und Desktopbrowser. Untersuche barrierearme Lernnavigation, WCAG 2.2 AA im Bildungskontext, Touch- und Tastaturbedienung, Datenschutz durch Datenvermeidung, lokale Speicherung und nutzergesteuerten Export, Offlinefähigkeit und Progressive Web Apps, Update- und Fehlerverhalten, offene Lizenzen und Lizenzkompatibilität, OER-Nachnutzung, nachhaltige Webtechnologien, geringe Bandbreite, schulische Browserrestriktionen, Einbettung und langfristige Wartbarkeit.

Priorisiere normative Primärquellen wie W3C/WAI, Datenschutzbehörden, Creative Commons und technische Standards sowie belastbare Forschung zu digitalen Lernumgebungen. Trenne rechtliche beziehungsweise normative Anforderungen, technische Standards, empirische Befunde und Projektentscheidungen. Rechtsstände sind mit Datum und Zuständigkeit zu kennzeichnen; der Bericht ist keine Rechtsberatung. Gib direkte Original-URLs, Geltungsbereich, Einschränkungen und konkrete Design- oder Prüffolgen an. Vermeide Produktmarketing und lange Zitate.

Ausgabe: 1. Executive Summary; 2. Quellen- und Statusmatrix; 3. Accessibility; 4. Privacy und Local First; 5. Offline- und Updateverhalten; 6. OER und Lizenzkompatibilität; 7. schulische Geräte und Browser; 8. Nachhaltigkeit und Wartung; 9. offene Risiken; 10. priorisierte Anforderungen und Quellenverzeichnis.
```

- [ ] **Step 2: Deep Research ausführen und Rohbericht sichern**

Determine the execution date with `Get-Date -Format 'yyyy-MM-dd'`. Use YAML frontmatter with `package: digitale-lernumgebungen-oer`, the actual printed date as `executed`, `status: raw` and `prompt: ../prompts/04-digitale-lernumgebungen-oer.md`.

- [ ] **Step 3: Normative und empirische Aussagen getrennt kuratieren**

Register `SRC-DLE-*`. A retained accessibility, privacy or license claim must link to the original normative source. Empirical usability claims must name the studied population and context.

- [ ] **Step 4: Projektfolgen ohne Phase-1-Code formulieren**

The curated report may define requirements and QA criteria, but must not create portal code, PWA configuration or component implementation. Mark those consequences as inputs for the Phase-1 specification.

- [ ] **Step 5: Validate and commit**

```powershell
python scripts/validate_phase0.py
git diff --check
git add docs/research/phase-0
git commit -m "research: curate digital learning and OER evidence"
```

---

### Task 7: Paketübergreifende Forschungssynthese

**Files:**
- Create: `docs/research/phase-0/synthesis.md`
- Create: `docs/research/phase-0/design-principles.json`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: four curated reports and `claim-ledger.json`
- Produces: design principles `PRIN-*` with exact `claimIds`, conflicts and Phase-1 implications

- [ ] **Step 1: Failing tests für Designprinzipien schreiben**

Add tests for `validate_design_principles(payload, claim_ids)`:

```python
def test_design_principle_rejects_unknown_claim(self):
    payload = {
        "schemaVersion": 1,
        "principles": [
            {
                "id": "PRIN-001",
                "title": "Beispiele gezielt ausblenden",
                "statement": "Hilfen werden nach erfolgreicher Anwendung schrittweise reduziert.",
                "claimIds": ["CLAIM-MISSING"],
                "appliesTo": ["scaffolding"],
                "status": "working",
                "phase1Implications": ["Hilfestufen im Modulmanifest beschreibbar machen."],
                "risks": ["Zu frühes Fading kann überfordern."],
            }
        ],
    }
    with self.assertRaises(ValidationError):
        validate_design_principles(payload, {"CLAIM-LP-001"})
```

- [ ] **Step 2: Test ausführen und erwartetes Scheitern prüfen**

Expected: import error for the not-yet-defined function.

- [ ] **Step 3: Validator erweitern**

`validate_design_principles` must enforce unique `PRIN-*` IDs, registered claim references, nonempty `appliesTo`, `phase1Implications`, `risks` and status in the common status model. Extend `main()` to validate `design-principles.json`.

- [ ] **Step 4: Synthese schreiben**

`synthesis.md` must include:

1. evidence base and confidence;
2. converging principles across packages;
3. tensions, such as exploration versus explicit guidance;
4. age- and domain-specific limits;
5. consequences for the seven module phases;
6. consequences for teacher orchestration;
7. consequences for analog/digital choice;
8. consequences for non-personal diagnostic opportunities;
9. consequences for later assessment review;
10. unresolved questions and explicit Phase-1 inputs.

- [ ] **Step 5: Designprinzipien erfassen**

Create only principles that can cite at least one retained claim. A principle may be `working` when transfer to IuM 5–7 remains inferential; it may be `reviewed` only when evidence and applicability were both checked.

- [ ] **Step 6: Validate and commit**

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
git diff --check
git add docs/research/phase-0 scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "research: synthesize phase 0 design principles"
```

---

### Task 8: Fachprofil Informatik und Medienbildung Gymnasium 5–7

**Files:**
- Create: `docs/fachprofil/ium-gymnasium-5-7.md`
- Create: `Vault/20_Wissen/Didaktik/Unterrichtsplanung/Fachprofile/Informatik und Medienbildung Gymnasium 5-7 - Planungsprofil.md`
- Modify: `docs/research/phase-0/design-principles.json`

**Interfaces:**
- Consumes: research synthesis, design principles, Manifest, pedagogical profile and curriculum source status
- Produces: canonical Fachprofil plus Vault routing adapter; inputs to Tasks 13–14

- [ ] **Step 1: Profilstruktur gegen Pilotprofil prüfen**

Read:

```text
Vault/20_Wissen/Didaktik/Unterrichtsplanung/Fachprofile/Geschichte Kursstufe - Planungsprofil.md
Vault/20_Wissen/Didaktik/Unterrichtsplanung/Unterrichtsplanung - Manifest.md
Vault/20_Wissen/Didaktik/Unterrichtsplanung/50_Qualitätssicherung/Unterrichtsplanung - Prüf-Gates.md
```

Extract structure, but do not copy history-specific rules.

- [ ] **Step 2: Kanonisches Profil schreiben**

`docs/fachprofil/ium-gymnasium-5-7.md` must contain:

- scope, status and source basis;
- relationship of personal principles, research findings, curriculum requirements and project decisions;
- subject core and central ways of thinking;
- separate informatics and media-education learning strands plus their justified integration;
- age-specific progression 5–7;
- material and representation standards;
- programming-task standards;
- media-analysis and production-task standards;
- typical misconceptions and learning barriers;
- scaffolding, practice, feedback and securing;
- teacher orchestration;
- analog/digital decision rules;
- non-personal diagnostic opportunities;
- source, license and accessibility requirements;
- assessment toolkit as reducible `working` section;
- no-gos;
- open questions and review status.

Every research-based profile rule cites `CLAIM-*`; every normative rule cites a curriculum source; every project decision cites the design specification.

- [ ] **Step 3: Vault-Routing-Adapter schreiben**

The Vault note contains:

- normal Vault frontmatter;
- `status: working`;
- purpose and scope;
- absolute repository path to the canonical profile;
- compact routing rules for `unterricht-planen`;
- statement that the repository file is canonical and the Vault note is not a duplicate;
- links to `[[IuM-Lernwerk]]`, `[[Unterrichtsplanung - Manifest]]`, `[[Bildungsplan - Mapping Konzept]]` and UP01.

- [ ] **Step 4: Profil-Gate prüfen**

Run:

```powershell
rg -n "^## " docs/fachprofil/ium-gymnasium-5-7.md
rg -n "CLAIM-|SRC-CUR-|working|reviewed|No-Gos|Diagnose|analog|digital" docs/fachprofil/ium-gymnasium-5-7.md
rg -n "T[B]D|T[O]DO|F[I]XME|PLACEH[O]LDER" docs/fachprofil/ium-gymnasium-5-7.md
$encodingHits = Select-String -LiteralPath docs/fachprofil/ium-gymnasium-5-7.md -Pattern ([char]0x00C3), ([char]0x00C2), ([char]0xFFFD)
if ($encodingHits) { $encodingHits; throw "Möglicher Zeichensatzfehler" }
```

Expected: all required sections and source types are present, with no red-flag or encoding hit.

- [ ] **Step 5: Commit repository file only**

```powershell
git add docs/fachprofil/ium-gymnasium-5-7.md docs/research/phase-0/design-principles.json
git commit -m "docs: define IuM 5-7 teaching profile"
```

The Vault adapter is documented in the Task-8 Session Summary; it is not added to the repository commit.

---

### Task 9: Lesehilfe 2026/2027 quellentreu extrahieren

**Files:**
- Create: `curriculum/lesehilfe-2026-27/competencies.json`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: PDF and `extraction-protocol.md`
- Produces: `validate_curriculum_dataset(payload)` and verified `LH26-*` records for Niveau E

- [ ] **Step 1: Failing tests für Curriculum-Datensätze schreiben**

Add tests requiring:

- `schemaVersion == 1`;
- `sourceId` references the source register;
- unique record IDs;
- nonempty `text`;
- `grades`, `level`, `area`, `recordType`, `sourceLocator` and `status`;
- `sourceLocator.page` as positive integer for PDF records;
- allowed status `verified`, `plausible`, `open`.

Test that duplicate IDs and a page number `0` are rejected.

- [ ] **Step 2: Tests ausführen und erwartetes Scheitern prüfen**

Expected: import error for `validate_curriculum_dataset`.

- [ ] **Step 3: Curriculum-Validator implementieren**

Public signature: `validate_curriculum_dataset(payload, source_ids)`.

It returns the set of record IDs and validates `recordType` in:

```python
{"competency", "progression-note", "example", "operator", "process-competency"}
```

Extend `main()` to validate every `curriculum/**/competencies.json` file that exists.

- [ ] **Step 4: PDF vollständig extrahieren**

Use both text extraction and rendered page inspection. Record:

- all five competency areas;
- all Niveau-E competencies;
- grade or grade band;
- official wording;
- examples as separate `recordType: example`;
- progression notes;
- page and section;
- record status.

Generate deterministic IDs in document order:

```text
LH26-E-DP-001
LH26-E-ID-001
LH26-E-ALG-001
LH26-E-KS-001
LH26-E-DA-001
```

where `DP`, `ID`, `ALG`, `KS`, `DA` correspond to the five official areas.

- [ ] **Step 5: Doppelte und fehlende Einträge prüfen**

Run:

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
```

Then manually compare record counts per competency area against the PDF tables and record the counts in the dataset metadata.

- [ ] **Step 6: Commit**

```powershell
git add curriculum/lesehilfe-2026-27/competencies.json scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "data: extract 2026 IuM guidance competencies"
```

---

### Task 10: Bildungsplan 2016 Basiskurs Medienbildung extrahieren

**Files:**
- Create: `curriculum/basiskurs-medienbildung/competencies.json`
- Modify: `docs/research/phase-0/source-register.json`

**Interfaces:**
- Consumes: official BMB source and curriculum validator
- Produces: verified `BMB16-*` records including process competencies, operators and content standards

- [ ] **Step 1: Offizielle Abschnittsstruktur erfassen**

Record source sections, official identifiers, grades, process competencies, content standards, operators, terms and examples separately. Do not infer Lesehilfe mappings in this task.

- [ ] **Step 2: Quellentreuen Datensatz erstellen**

Use official IDs when present. Otherwise use deterministic document-order IDs:

```text
BMB16-GYM-[A-Z0-9]+-[0-9]{3}
```

Every record includes direct URL and section locator. `level` is `E` only when the source explicitly supports that assignment; otherwise store the source’s own level terminology.

- [ ] **Step 3: Validate and manually spot-check**

Run:

```powershell
python scripts/validate_phase0.py
```

Manually compare at least the first, middle and last record of each source section against the official page.

- [ ] **Step 4: Commit**

```powershell
git add curriculum/basiskurs-medienbildung/competencies.json docs/research/phase-0/source-register.json
git commit -m "data: extract media education curriculum"
```

---

### Task 11: Bildungsplan 2016 Aufbaukurs Informatik Klasse 7 extrahieren

**Files:**
- Create: `curriculum/aufbaukurs-informatik/competencies.json`
- Modify: `docs/research/phase-0/source-register.json`

**Interfaces:**
- Consumes: official INF7 source and curriculum validator
- Produces: verified `INF7-16-*` records including process competencies, operators and content standards

- [ ] **Step 1: Offizielle Abschnittsstruktur erfassen**

Separate:

- process-related competencies;
- content-related competencies;
- algorithms and programming;
- data and coding;
- computer systems and networks;
- information society and security;
- official examples and explanatory notes.

- [ ] **Step 2: Quellentreuen Datensatz erstellen**

Preserve official IDs; otherwise use:

```text
INF7-16-GYM-[A-Z0-9]+-[0-9]{3}
```

Do not merge similar records and do not import examples as binding competencies.

- [ ] **Step 3: Validate and manually spot-check**

Run:

```powershell
python scripts/validate_phase0.py
```

Compare first, middle and last record of every official section with the original page.

- [ ] **Step 4: Commit**

```powershell
git add curriculum/aufbaukurs-informatik/competencies.json docs/research/phase-0/source-register.json
git commit -m "data: extract grade 7 informatics curriculum"
```

---

### Task 12: Curriculum-Crosswalk, Operatoren und Progression

**Files:**
- Create: `curriculum/operators.json`
- Create: `curriculum/crosswalk.json`
- Create: `curriculum/progression.md`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: all three curriculum datasets and Fachprofil
- Produces: `validate_crosswalk(payload, curriculum_ids)`, a resolved union of requirements and a justified grade progression

- [ ] **Step 1: Failing Crosswalk-Tests schreiben**

Tests must reject:

- unknown source or target record IDs;
- invalid relationship;
- missing rationale;
- an `open` difference without an explicit follow-up action.

Allowed relationships:

```python
{"equivalent", "overlaps", "extends", "reframes", "new", "not-comparable"}
```

- [ ] **Step 2: Test ausführen und erwartetes Scheitern prüfen**

Expected: import error for `validate_crosswalk`.

- [ ] **Step 3: Crosswalk-Validator implementieren**

Public signature: `validate_crosswalk(payload, curriculum_ids)`. Extend `main()` to validate `operators.json`, `crosswalk.json` and the union of all curriculum IDs.

Every relation contains `fromIds`, `toIds`, `relationship`, `rationale`, `status` and `followUp`.

- [ ] **Step 4: Operatoren und Prozesskompetenzen zusammenführen**

`operators.json` distinguishes:

- exact official term;
- source record;
- expected observable action;
- likely complexity band;
- applicable grades;
- notes on ambiguity.

Do not invent a universal operator hierarchy when sources use different semantics.

- [ ] **Step 5: Crosswalk erstellen**

Map:

1. Lesehilfe to BMB;
2. Lesehilfe to INF7;
3. BMB and INF7 overlaps;
4. genuinely new or reframed Lesehilfe requirements;
5. requirements from enacted plans not explicit in the Lesehilfe.

Every normative record must appear in at least one crosswalk relation or in an explicit `unmappedRecords` list with reason and follow-up.

- [ ] **Step 6: Progression 5–7 begründen**

`progression.md` must define:

- five recurring strands;
- prerequisite concepts;
- expected transitions 5→6 and 6→7;
- repeated concepts at increasing complexity;
- technical, application and societal perspectives;
- unresolved allocations for combined 5/6 requirements;
- explicit difference between normative requirement and didactic sequencing decision.

- [ ] **Step 7: Validate and commit**

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
git diff --check
git add curriculum scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "data: crosswalk curricula and define progression"
```

---

### Task 13: Modulkandidaten und Abhängigkeitsgraph

**Files:**
- Create: `roadmap/module-candidates.json`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: Fachprofil, design principles, curriculum crosswalk and progression
- Produces: `validate_module_candidates(payload, curriculum_ids)` and a cycle-free candidate graph

- [ ] **Step 1: Failing Modulkandidaten-Tests schreiben**

Tests must reject:

- duplicate module IDs;
- unknown competency IDs;
- unknown prerequisite module IDs;
- dependency cycles;
- invalid module kind;
- missing learning product or medium rationale;
- analog material without a didactic rationale;
- `core` module without grade and lesson range.

Allowed kinds:

```python
{"core", "extension", "transfer", "project"}
```

- [ ] **Step 2: Tests ausführen und erwartetes Scheitern prüfen**

Expected: import error for `validate_module_candidates`.

- [ ] **Step 3: Validator und Zyklusprüfung implementieren**

Public signature: `validate_module_candidates(payload, curriculum_ids)`.

Return module IDs after depth-first cycle detection. Extend `main()` to validate `module-candidates.json`.

- [ ] **Step 4: Kandidaten aus Lernhandlungen statt Themenlisten ableiten**

Every module record includes:

- `id` in format `IUM-5-CORE-01`;
- `title`;
- `grade`;
- `kind`;
- `strandIds`;
- `competencyIds`;
- `prerequisiteModuleIds`;
- `lessonRange` with integer `min` and `max`;
- `centralQuestion`;
- `centralLearningAction`;
- `centralLearningProduct`;
- `moduleGrammar`;
- `mediumRationale`;
- `analogMaterials`;
- `assessmentWorkingNotes`;
- `status`.

Core candidates jointly cover the union of binding and orientation requirements. Flexible candidates may depend on defined core prerequisites.

- [ ] **Step 5: Hybridmodell-Integrität prüfen**

Before finalizing this task, verify that section 2.2 still contains both approved sentences and that `module-candidates.json` includes the kinds `core`, `extension`, `transfer` and `project` without forcing every flexible kind into every grade.

- [ ] **Step 6: Validate and commit**

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
git diff --check
git add roadmap/module-candidates.json scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "plan: define IuM module candidates"
```

---

### Task 14: Modulroadmap und vollständiger Abdeckungsplan

**Files:**
- Create: `roadmap/coverage-plan.json`
- Create: `roadmap/module-roadmap.md`
- Modify: `scripts/validate_phase0.py`
- Modify: `tests/test_validate_phase0.py`

**Interfaces:**
- Consumes: curriculum union and module candidate graph
- Produces: `validate_coverage(payload, required_ids, module_ids)` and the reviewable first roadmap

- [ ] **Step 1: Failing Coverage-Tests schreiben**

Tests must prove:

- every required normative record is `covered`, `partial` or `deferred`;
- `covered` references at least one valid core module;
- `partial` and `deferred` include reason, risk and follow-up;
- every module competency reference is represented in coverage;
- orientation-only Lesehilfe records are visibly distinguished from enacted requirements.

- [ ] **Step 2: Test ausführen und erwartetes Scheitern prüfen**

Expected: import error for `validate_coverage`.

- [ ] **Step 3: Coverage-Validator implementieren**

Public signature: `validate_coverage(payload, required_ids, module_ids)`.

The CLI exits nonzero when an enacted requirement is absent from the coverage plan. Extend `main()` to validate `coverage-plan.json`.

- [ ] **Step 4: Abdeckungsplan erzeugen**

For every required record store:

- `competencyId`;
- `normativeWeight`: `enacted` or `orientation`;
- `moduleIds`;
- `coverageStatus`;
- `evidence`;
- `risk`;
- `followUp`.

Duplicates across sources remain traceable through the crosswalk rather than being silently counted twice.

- [ ] **Step 5: Lesbare Roadmap schreiben**

`module-roadmap.md` must include:

- design assumptions and time model;
- core sequence for grades 5, 6 and 7;
- flexible extension, transfer and project candidates;
- dependency rationale;
- curriculum coverage summary;
- year-level time corridor and buffer;
- modules requiring analog materials and why;
- modules with heightened safety, rights or currency review needs;
- first Goldstandard-Pilot recommendation with selection criteria, but no Phase-2 implementation plan;
- unresolved decisions and risks.

- [ ] **Step 6: Validate and commit**

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
git diff --check
git add roadmap scripts/validate_phase0.py tests/test_validate_phase0.py
git commit -m "plan: map curriculum coverage to module roadmap"
```

---

### Task 15: Phase-0-Abschlussreview und Handoff

**Files:**
- Modify: `docs/research/phase-0/README.md`
- Modify: `README.md`
- Modify: `Vault/40_Projekte/IuM-Lernwerk/IuM-Lernwerk.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Tasks/2026-05-13 - UP01 Fachprofile Unterricht ausbauen.md`
- Modify: Phase-0-Tasknotizen under `Vault/60_Organisation/Workspace-Entwicklung/Tasks/`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Workspace Kanban.md`
- Modify: Phase-0 initiative under `Vault/60_Organisation/Workspace-Entwicklung/Initiativen/`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Entwicklungshistorie.md`
- Create: dated Session Summary under `Vault/50_Codex/Sessions/`

**Interfaces:**
- Consumes: all Phase-0 deliverables and validation results
- Produces: review package and explicit gate before any Phase-1 specification

- [ ] **Step 1: Vollständige automatisierte Prüfung ausführen**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_phase0.py
git diff --check
rg -n "T[B]D|T[O]DO|F[I]XME|PLACEH[O]LDER" README.md docs curriculum roadmap scripts tests
$encodingHits = Get-ChildItem README.md, docs, curriculum, roadmap, scripts, tests -Recurse -File | Select-String -Pattern ([char]0x00C3), ([char]0x00C2), ([char]0xFFFD)
if ($encodingHits) { $encodingHits; throw "Möglicher Zeichensatzfehler" }
git status --short --branch
```

Expected: tests `OK`, validator exit `0`, no diff-check errors, no red-flag or encoding matches, only expected documentation changes.

- [ ] **Step 2: Manuelles Quellen- und Coverage-Audit durchführen**

Sample:

- three claims per research package;
- first, middle and last record per curriculum source section;
- every `partial` or `deferred` coverage entry;
- every dependency edge in the proposed core path;
- every source marked `secondary-only`;
- every `reviewed` design principle.

Record findings and corrections in `docs/research/phase-0/README.md`.

- [ ] **Step 3: Spezifikationsabdeckung prüfen**

Map each relevant requirement from sections 3, 4, 5, 8, 9, 13 and Phase 0 of the Gesamtdesign to:

- a research artifact;
- a profile rule;
- a curriculum record;
- a roadmap or coverage entry.

Document genuine gaps; do not close them by assertion.

- [ ] **Step 4: Repository-Status dokumentieren und final committen**

If a remote exists, run:

```powershell
git fetch --prune
git pull --ff-only
```

Then:

```powershell
git add README.md docs/research/phase-0
git commit -m "docs: complete phase 0 research foundation"
git status --short --branch
git log --oneline --decorate -15
```

Do not push without a configured, successfully synchronized remote.

- [ ] **Step 5: Workspace-Handoff aktualisieren**

Set:

- completed Phase-0 tasks to `review`;
- UP01 to `review` only if its Fachprofil acceptance criteria are met;
- Phase-0 initiative to `review`;
- Kanban cards to `Review`;
- next action to user review of research basis, Fachprofil, curriculum coverage and roadmap;
- no Phase-1 task to `in_progress`.

Create the Session Summary from `Vault/00_System/Templates/Template - Codex Session.md` with the actual completion date returned by `Get-Date -Format 'yyyy-MM-dd'`, commit hashes, branch, remote and push status.

- [ ] **Step 6: Nutzerreview anbieten**

The handoff must ask the user to review four separate gates:

1. research synthesis;
2. Fachprofil;
3. curriculum completeness;
4. module roadmap.

Phase 1 may be specified only after these gates are accepted or consciously revised.

## Plan-Level Acceptance Criteria

- [ ] All four research packages exist as prompt, raw input and curated report.
- [ ] Every retained claim references registered sources and explicit limitations.
- [ ] The canonical Fachprofil distinguishes personal principles, evidence, curriculum and project decisions.
- [ ] All three normative/orienting curriculum sources are extracted with locators and record status.
- [ ] The crosswalk accounts for every record or explicitly marks it unresolved.
- [ ] The progression distinguishes normative requirements from didactic sequencing decisions.
- [ ] Module candidates form an acyclic dependency graph.
- [ ] Every enacted requirement is covered, partial or deferred with a reviewable rationale.
- [ ] The roadmap preserves the approved progressive core plus flexible module architecture.
- [ ] No Phase-1 platform implementation has entered Phase 0.
- [ ] Automated tests, manual source spot-checks and spec-coverage review pass.
- [ ] Repository and Workspace handoff make the next review step unambiguous.
