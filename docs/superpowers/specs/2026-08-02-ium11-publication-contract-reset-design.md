# IUM11-Architekturreset für den Publikationsvertrag

**Status:** zur schriftlichen Freigabe  
**Datum:** 2026-08-02  
**Scope:** Abschluss von IUM11-Implementierungstask 8 nach ausgelöstem Fünf-Runden-Breaker

## 1. Ausgangslage

Task 8 veröffentlicht README-Einstieg, Lehrkräfteanleitung und Reviewanleitung für das lokale IUM11-Pilotinstrument. Der bisherige Validator versucht, Status-, Versions-, Zahlen- und Reifeaussagen in freier deutscher Prosa semantisch fail-closed zu klassifizieren.

Fünf testgetriebene Fixrunden haben gezeigt, dass dieser Ansatz strukturell ungeeignet ist. Negationen, koordinierte Aussagen, Nebensätze und Subjektwechsel erzeugen abwechselnd Unter- und Überblockierungen. Zuletzt blieben zwei reale Important-Befunde offen:

1. Eine Negation in einem abhängigen Nebensatz kann einen positiven Hauptclaim maskieren.
2. Ein ausdrücklicher Subjektwechsel nach `und` oder Komma kann den geerbten Pilotbezug nicht zuverlässig beenden.

Die Produktdokumente selbst enthalten am aktuellen Stand keine Statushochsetzung. Der Defekt betrifft die behauptete Vollständigkeit ihrer automatisierten natürlichsprachlichen Prüfung.

## 2. Ziel

IUM11 erhält einen deterministischen, maschinenlesbaren Publikationsvertrag. Alle veränderlichen Status-, Versions-, Kennzahlen- und Empfehlungswerte werden aus bestehenden kanonischen Datenquellen kompiliert und in den drei Veröffentlichungen als identischer, generierter Markdown-Faktenblock sichtbar gemacht. Unveränderliche Governancevorgaben wie Aussagegrenze, erlaubte spätere Auftraggeberänderungen und das Verbot einer automatischen Reifehochsetzung sind als geschlossene Konstanten dieser freigegebenen Spezifikation im Compiler gebunden.

Der Validator prüft ausschließlich klar definierte maschinenlesbare Grenzen. Er behauptet nicht mehr, beliebige deutsche Prosa semantisch vollständig auswerten zu können.

## 3. Nichtziele

Der Architekturreset:

- verändert weder `roadmap/time-model.json` noch `pilot/pilot-protocol.json`;
- verändert keine Produkt-, Verfügbarkeits-, Zeit-, Pilot- oder Coverageachse;
- startet keine reale Pilotierung und verarbeitet keine realen Evidenzpakete;
- verändert Cockpit, Evidenzschema, Entscheidungsschema und Ergebnisableitung nicht;
- ersetzt Fachreview und redaktionelle Prüfung nicht durch einen Textklassifikator;
- führt keine Fremdpakete, Netzwerkaufrufe, Telemetrie oder Persistenz ein;
- beginnt weder Release noch Phase 1.

## 4. Kanonische Quellen

Kanonische Datenquellen bleiben ausschließlich:

1. `pilot/pilot-protocol.json` für Protokollversion, Werkzeugversion, Zeitmodellfingerprint, Variante, Cluster, Rückfallwerte, Privacy-Schwelle, Aussagegrenze und Empfehlung;
2. `roadmap/time-model.json` für Kernpfad, Modulbelegung, Verfügbarkeitsvertrag und die sechs Klasse-7-Urteilachsen;
3. das bereits validierte IUM10-Ergebnis als Bindeglied zwischen Zeitmodell und abgeleiteten Klasse-7-Urteilen.

Die unveränderlichen Governancekonstanten werden in dieser Spezifikation vollständig und abschließend festgelegt. Sie werden nicht aus Dokumentprosa gelesen und nicht in einer weiteren handgepflegten Datendatei dupliziert.

`pilot/docs/publication-contract.json` ist ein generiertes Artefakt und keine dritte Primärquelle. Jede Abweichung von den Datenquellen oder den hier festgelegten Governancekonstanten ist ein Buildfehler.

## 5. Komponenten und Verantwortlichkeiten

### 5.1 Reiner Vertragscompiler

`scripts/ium11_publication.py` enthält ausschließlich reine, dependency-freie Funktionen:

- `compile_publication_contract(protocol, time_model, ium10_result) -> dict`
- `render_publication_contract_json(contract) -> bytes`
- `render_publication_markdown_block(contract) -> str`
- `replace_publication_block(text, block) -> str`
- `extract_publication_block(text) -> str`
- `validate_publication_text_boundary(relative_path, text) -> None`

Das Modul liest und schreibt keine Dateien. Es importiert weder den IUM11-Gesamtvalidator noch den Build-CLI und erzeugt deshalb keinen zyklischen Import.

### 5.2 Build-CLI

`scripts/build_ium11_publication_contract.py`:

- lädt Zeitmodell und Pilotprotokoll aus dem Repository;
- führt zuerst IUM10- und IUM11-Protokollvalidierung aus;
- kompiliert Vertrag, JSON und Markdownblock;
- ersetzt JSON und jeden der drei markierten Dokumentbereiche jeweils atomar;
- unterstützt `--check`, ohne Dateien zu verändern;
- meldet fehlende oder doppelte Marker, ungültige Quellen und Drift mit Exitcode ungleich null.

### 5.3 IUM11-Gesamtvalidator

`scripts/validate_ium11.py`:

- entfernt den bisherigen Natural-Language-Claimparser vollständig;
- kompiliert den erwarteten Vertrag aus den bereits validierten In-Memory-Quellen;
- verlangt byteidentisches JSON und byteidentische Faktenblöcke;
- prüft die strukturelle Textgrenze außerhalb der Blöcke;
- nimmt `pilot/docs/publication-contract.json` in die geschlossene Pilot-Dateikarte auf.

## 6. Geschlossenes Vertragsobjekt

Das JSON-Objekt besitzt exakt diese Top-Level-Felder:

```json
{
  "schemaVersion": 1,
  "id": "IUM11-PUBLICATION-CONTRACT",
  "contractVersion": "1.0.0",
  "sourceBindings": {},
  "corePath": {},
  "privacyBoundary": {},
  "currentAxes": {},
  "statementBoundary": "documented-conditions-only",
  "allowedRecommendation": "eligible-for-working-availability-review",
  "forbiddenMaturityValues": [],
  "futureDecisionBoundary": {},
  "preservationBoundary": {},
  "realPilotCompleted": false,
  "syntheticValidationOnly": true
}
```

### 6.1 `sourceBindings`

Exakte Felder:

```json
{
  "protocolPath": "pilot/pilot-protocol.json",
  "timeModelPath": "roadmap/time-model.json",
  "protocolVersion": "1.0.0",
  "toolVersion": "1.0.0",
  "timeModelFingerprintAlgorithm": "sha256-canonical-json-v1",
  "timeModelFingerprint": "<64 lowercase hex characters>"
}
```

Der Fingerprint muss sowohl zum kanonisch serialisierten Zeitmodell als auch zum Fingerprint im Pilotprotokoll passen.

### 6.2 `corePath`

Exakte Felder:

```json
{
  "variantId": "GRADE-7-WORKING-40",
  "targetUnits": 40,
  "clusterCount": 4,
  "moduleCount": 10,
  "pilotStageCount": 5,
  "clusters": [
    {
      "id": "CLUSTER-7-DATA-CODING",
      "order": 1,
      "budgetUnits": 8,
      "fallbackDeltaUnits": 3
    }
  ]
}
```

`clusters` enthält alle vier Cluster in Protokollreihenfolge. Die übrigen Budgets sind `11 / 11 / 10`, die übrigen Rückfallwerte `2 / 3 / 6`. `moduleCount` wird aus der eindeutigen Vereinigungsmenge aller Cluster-Module abgeleitet. `pilotStageCount` ist die Zahl der Cluster plus genau ein Jahreslauf.

### 6.3 `privacyBoundary`

Exakte Felder:

```json
{
  "minimumLearnerResponses": 10,
  "personalDataAllowed": false,
  "realPackagesInRepositoryAllowed": false
}
```

### 6.4 `currentAxes`

Exakte Felder und Werte:

```json
{
  "status": "working",
  "availabilityStatus": "conditional",
  "timeFeasibilityStatus": "amber",
  "sequenceEvidenceStatus": "covered",
  "pilotStatus": "not-started",
  "semanticCoverageStatus": "partial"
}
```

`status` und `availabilityStatus` werden gegen die Klasse-7-Variante geprüft. Die übrigen Achsen stammen aus dem Klasse-7-Eintrag von `gradeJudgements` und müssen zum validierten IUM10-Ergebnis passen.

### 6.5 Reife- und Entscheidungsgrenze

`forbiddenMaturityValues` ist exakt:

```json
["reviewed", "standard"]
```

`futureDecisionBoundary` besitzt exakt:

```json
{
  "requiresCommissionerDecision": true,
  "allowedChanges": [
    {"field": "availabilityStatus", "value": "available"},
    {"field": "timeFeasibilityStatus", "value": "green"},
    {"field": "pilotStatus", "value": "completed"}
  ],
  "unchangedAxes": [
    {"field": "status", "value": "working"},
    {"field": "semanticCoverageStatus", "value": "partial"}
  ],
  "secondIndependentAnnualRunRequiredForMaturity": true
}
```

Die Reihenfolge der Arrays ist Vertragsbestandteil.

### 6.6 Erhaltungsgrenze

`preservationBoundary` besitzt exakt:

```json
{
  "flexibleModulesOutsideCorePreserved": true,
  "flexibleModuleSubstitution": "forbidden"
}
```

Die Erhaltung ist eine Governancekonstante dieser Spezifikation; die Substitutionssperre wird zusätzlich gegen `forbiddenCompensations` des Verfügbarkeitsvertrags geprüft. Der sichtbare Satzstamm „Flexible Vertiefungs-, Transfer- und Projektmodule bleiben“ steht innerhalb des generierten Faktenblocks und bleibt dadurch mindestens in README und Reviewanleitung erhalten.

## 7. Deterministische Serialisierung

JSON wird als UTF-8 ohne BOM, mit sortierten Schlüsseln, zwei Leerzeichen Einrückung, LF-Zeilenenden und genau einem finalen Zeilenumbruch gerendert.

Der Markdownblock besitzt exakt diese Marker:

```markdown
<!-- IUM11-PUBLICATION-CONTRACT:START -->
<!-- Generiert aus Pilotprotokoll und Zeitmodell; nicht manuell bearbeiten. -->
...
<!-- IUM11-PUBLICATION-CONTRACT:END -->
```

Zwischen den Markern steht eine GitHub-kompatible Markdown-Tabelle. Sie enthält alle Vertragsfelder in fester Reihenfolge, einschließlich Clusterbudgets, Rückfallwerte, aktueller Achsen und künftig ausschließlich durch Auftraggebergate erlaubter Änderungen. Derselbe Block wird byteidentisch in folgende Dateien eingebettet:

- `README.md`
- `pilot/docs/teacher-guide.md`
- `pilot/docs/review-guide.md`

Die sichtbare Tabelle ist zugleich menschenlesbare Statusquelle und maschinengeprüfte Projektion des JSON-Vertrags.

## 8. Strukturelle Textgrenze außerhalb des Faktenblocks

Die Textgrenze interpretiert keine Grammatik und keine Negation. Sie arbeitet nur auf klar reservierten maschinenlesbaren Formen.

### 8.1 Prüfbereich

- In den beiden Guides: gesamter Text außerhalb des generierten Blocks.
- In README: nur der Abschnitt `## IUM11-Pilotinstrument` außerhalb des Blocks; andere Klassen- und IUM10-Abschnitte bleiben unberührt.

### 8.2 Außerhalb des Blocks verbotene Formen

- jede SemVer-Zeichenfolge nach dem Muster `[0-9]+\.[0-9]+\.[0-9]+`;
- jeder Empfehlungscode mit Präfix `eligible-for-`;
- Zuweisungen zu `status`, `availabilityStatus`, `timeFeasibilityStatus`, `sequenceEvidenceStatus`, `pilotStatus` oder `semanticCoverageStatus`;
- die reservierten englischen Vertragswerte `working`, `available`, `unavailable`, `reviewed`, `standard`, `conditional`, `green`, `amber`, `red`, `covered`, `not-started`, `partial`, `completed` und `documented-conditions-only`;
- die technische Variantenkennung `GRADE-7-WORKING-40`;
- numerische Kerndeklarationen nach den Formen `Zahl + UE`, `Zahl + Cluster`, `Zahl + Modul`, `Zahl + Pilotstufe` oder `Privacy-Schwelle + Zahl`.

Diese Literale werden in den drei Veröffentlichungen in den Faktenblock verlagert. Erklärende Prosa verweist auf den Block oder formuliert ohne konkurrierende maschinenlesbare Deklaration. Deutsche Verben wie „abgeschlossen“ werden nicht semantisch bewertet; Aussagen darüber bleiben Gegenstand von Fach- und Redaktionsreview.

Die Textgrenze garantiert damit, dass außerhalb des Faktenblocks keine zweite maschinenlesbare Statusquelle entsteht. Sie garantiert ausdrücklich nicht die semantische Widerspruchsfreiheit beliebiger natürlicher Sprache.

## 9. Fehlerverhalten

Alle folgenden Fälle scheitern fail-closed:

- ungültiges Pilotprotokoll oder Zeitmodell;
- Fingerprintabweichung zwischen Protokoll und Zeitmodell;
- fehlende oder mehrdeutige Klasse-7-Variante, Urteilachsen oder Verfügbarkeitsverträge;
- abweichende Modul-, Cluster-, Budget-, Rückfall- oder Pilotstufenzahl;
- unbekannte oder zusätzliche Vertragsfelder;
- fehlendes, zusätzliches oder byteabweichendes JSON-Artefakt;
- fehlende, doppelte, verschachtelte, vertauschte oder byteabweichende Markdownmarker;
- reservierte maschinenlesbare Deklarationen außerhalb des Faktenblocks;
- eine beschädigte Einzeldatei oder ein nach unterbrochenem Mehrdatei-Schreibvorgang verbliebener Driftstand.

Quellvalidierung und Rendering aller vier Ziele werden abgeschlossen, bevor der erste Schreibvorgang beginnt. Jede Zieldatei wird über eine temporäre Datei im selben Verzeichnis und `os.replace` atomar ersetzt; dadurch kann keine einzelne Datei teilweise geschrieben werden. Ein unerwarteter Betriebssystemfehler zwischen mehreren erfolgreichen Ersetzungen kann einen gemischten, aber nicht beschädigten Dateistand hinterlassen. Der anschließende `--check` erkennt diesen Stand vollständig, und ein erneuter Build stellt alle vier Projektionen wieder her. `--check` ist immer read-only.

## 10. Migration

1. Reinen Compiler und geschlossene Vertragsstruktur testgetrieben einführen.
2. Build-CLI und atomaren Schreib-/Checkpfad ergänzen.
3. JSON-Artefakt und drei identische Markdownblöcke generieren.
4. Vertragstragende freie Prosa in den drei Dokumenten entfernen oder auf den Faktenblock verweisen lassen.
5. Den bisherigen Natural-Language-Claimparser sowie seine Grammatikmatrizen vollständig entfernen.
6. IUM11-Gesamtvalidator und geschlossene Pilot-Dateikarte auf den neuen Vertrag umstellen.
7. README-Befehle um den neuen Buildcheck ergänzen.
8. Task 8 erneut unabhängig reviewen; erst nach Freigabe Tasks 9 und 10 fortsetzen.

Die fünf bisherigen Parser-Fixcommits bleiben als nachvollziehbare Entwicklungsgeschichte erhalten. Es findet kein History-Rewrite statt.

## 11. Teststrategie

### 11.1 Compiler

- exakte Top-Level- und Nested-Feldmengen;
- Ableitung aller Werte aus realen kanonischen Fixtures;
- unsortierte, doppelte oder fehlende Cluster/Module werden abgewiesen;
- Fingerprint, Urteilachsen und Statusquellen müssen übereinstimmen;
- Eingaben werden nicht mutiert.

### 11.2 Renderer und Build

- byteidentisches JSON mit UTF-8, LF und finalem Zeilenumbruch;
- byteidentischer Markdownblock in allen drei Veröffentlichungen;
- zweimaliges Bauen ist idempotent;
- `--check` ist read-only;
- fehlende, doppelte, vertauschte und manipulierte Marker scheitern;
- atomarer Schreibweg verhindert beschädigte Einzeldateien; ein simulierter Fehler zwischen Zielersetzungen wird vom anschließenden `--check` als Drift erkannt.

### 11.3 Textgrenze

- jede reservierte maschinenlesbare Form außerhalb des Blocks scheitert in jedem Prüfbereich;
- dieselben Formen innerhalb des exakten Blocks sind zulässig;
- deutsche Nebensätze, Negationen und Subjektwechsel werden nicht klassifiziert und erzeugen weder Unter- noch Überblockierung;
- README-Bereiche außerhalb von IUM11 bleiben von der lokalen Textgrenze unberührt;
- der sichtbare Satz zu flexiblen Vertiefungs-, Transfer- und Projektmodulen bleibt erhalten.

### 11.4 Regression

- alle IUM11-Publikations- und Orchestrierungstests;
- Cockpitbuild und Node-Syntax;
- vollständige Python-Testsuite;
- IUM11-, IUM10-, IUM09- und Phase-0-CLI;
- `git diff --check` und Repositoryscan auf ausschließlich synthetische Pilotpakete.

## 12. Akzeptanzkriterien

Der Architekturreset ist abgeschlossen, wenn:

1. alle veränderlichen Vertragswerte ausschließlich aus den bestehenden kanonischen Datenquellen kompiliert und alle unveränderlichen Governancewerte exakt an diese Spezifikation gebunden werden;
2. JSON und drei Markdownblöcke reproduzierbar und byteidentisch sind;
3. keine konkurrierende handgepflegte Publikationsquelle entsteht;
4. der Natural-Language-Claimparser vollständig entfernt ist;
5. die neue strukturelle Textgrenze keine grammatische oder semantische Vollständigkeit behauptet;
6. alle reservierten maschinenlesbaren Deklarationen ausschließlich im Faktenblock stehen;
7. flexible Vertiefungs-, Transfer- und Projektmodule sichtbar erhalten bleiben;
8. alle fokussierten und vollständigen Prüfungen grün sind;
9. ein frischer unabhängiger Task-8-Review keine offenen Critical-, Important- oder Minor-Befunde meldet;
10. reale Pilotierung, Statushochsetzung, Release und Phase 1 unverändert ausgeschlossen bleiben.
