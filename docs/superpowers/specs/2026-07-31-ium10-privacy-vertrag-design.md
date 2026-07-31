# IUM10 – Maschinenlesbarer Privacy-Vertrag

**Status:** `review-ready` – Gesamtdesign am 31. Juli 2026 abschnittsweise freigegeben; schriftliche Gesamtfreigabe steht aus  
**Stand:** 31. Juli 2026  
**Scope:** IuM-Lernwerk, IUM10 Task 14, allgemeines Schema für Klassen 5–7 mit erster vollständiger Migration von `IUM-5-CORE-07`  
**Voraussetzung:** IUM10-Zeitmodelldesign freigegeben; Tasks 1–13 umgesetzt und reviewt  
**Implementierungsgrenze:** Diese Spezifikation entwirft den Privacy-Vertrag. Sie verändert noch keine Daten, Validatoren oder Tests.

## 1. Zweck und Entscheidung

IUM10 muss sicherstellen, dass private lokale Lernaktivitäten nicht als beobachtbare Produkt-, Evidenz- oder zusätzliche Zeitspur verwendet werden. Der bisherige Task-14-Test versuchte, diese Invariante aus deutscher Freitextprosa in `rationale`, `risk`, `followUp` und Coverage-Evidenz abzuleiten.

Nach fünf regulären Reparaturrunden und einer ausdrücklich freigegebenen Ausnahmerunde blieb der Ansatz fail-open. Ein unabhängiger Review reproduzierte weiterhin einfache Gegenbeispiele aus:

- Negationsscope und doppelter beziehungsweise fokussierender Negation;
- invertierter Prohibitionswortstellung;
- nachgestelltem Privatkontext;
- klauselglobalen Risikoausnahmen.

Die Invariante wird deshalb nicht länger aus natürlicher Sprache abgeleitet. IUM10 erhält:

1. einen Modul-Privacy-Vertrag mit unveränderlichen institutionellen Datenschutzgrenzen;
2. eine recordgenaue Privacy-Disposition je Zeitreview;
3. einen fail-closed Validator für beide Ebenen.

Der Freitextparser wird als autoritatives Gate entfernt. Prosa bleibt eine menschenlesbare Erläuterung, ist aber nicht die Quelle der maschinenlesbaren Privacy-Garantie.

## 2. Geltungsbereich und Migration

Das Schema gilt allgemein für alle späteren `private-local`-Zeitreviews der Klassen 5–7. Die Migration erfolgt gestuft:

1. `IUM-5-CORE-07` wird in Task 14 vollständig migriert.
2. Klasse-7-Daten bleiben in diesem Architekturtask unverändert.
3. Sobald ein späterer Audittask einen `private-local`-Zeitreview für Klasse 7 registriert, muss er im selben Task den zugehörigen Modul-Privacy-Vertrag und die recordgenaue Disposition ergänzen.

Die Spezifikation verändert nicht:

- IUM09-Ursachenklassen;
- IUM09-Coverage-Entscheidungen;
- bestehende Evidenzvertrags-IDs;
- Modul-IDs, Modularten oder Graphkanten;
- Pfade, Phasen oder Zeitbudgets;
- den Status der sieben weiterhin `partial`-Records.

## 3. Verworfene Alternativen

### 3.1 Vollständiger Privacy-Vertrag in jedem Zeitreview

Diese Variante wäre lokal lesbar, würde dieselben institutionellen Grenzen aber in jedem Record wiederholen. Sie erzeugt Drift- und Wartungsrisiken und wird verworfen.

### 3.2 Eigenständige Datei `privacy-contracts.json`

Eine neue globale Registry könnte Coverage- und Zeitmodell gemeinsam bedienen. Für den aktuellen Scope würde sie jedoch einen zusätzlichen Artefakt-, Migrations- und Synchronisationspfad schaffen. Das bestehende Zeitmodell kann beide Vertragsebenen ohne neue Datei sauber aufnehmen. Die Variante wird nach YAGNI verworfen.

### 3.3 Gewählte Lösung: zweistufiger Vertrag in `time-model.json`

Ein Modulvertrag definiert die invariant gleiche institutionelle Grenze. Jede Zeitentscheidung ergänzt nur ihre recordgenaue Evidenz- und Zeitdisposition. Dadurch bleiben Verantwortlichkeiten getrennt und die späteren Klasse-7-Audits können dasselbe Schema wiederverwenden.

## 4. Schema-Version

`roadmap/time-model.json` wechselt von:

```json
{"schemaVersion": 1}
```

zu:

```json
{"schemaVersion": 2}
```

Schema 2 verlangt das top-level Feld `privacyContracts`. Es ist eine Liste eindeutiger Modul-Privacy-Verträge.

## 5. Modul-Privacy-Vertrag

Die erste Migration registriert genau:

```json
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
```

### 5.1 Exakte Felder

Ein Modul-Privacy-Vertrag besitzt ausschließlich:

- `id`
- `moduleId`
- `scope`
- `artifactOwner`
- `artifactCustody`
- `institutionalHandling`
- `status`

`institutionalHandling` besitzt ausschließlich:

- `access`
- `observation`
- `collection`
- `transfer`
- `storage`
- `assessment`

### 5.2 Exakte Werte

Für Schema 2 gelten:

- `id == "PC-" + moduleId`;
- `scope == "private-local-reflection"`;
- `artifactOwner == "learner"`;
- `artifactCustody == "learner-controlled"`;
- alle sechs institutionellen Handlungen sind exakt `prohibited`;
- `status` entspricht den bestehenden IUM10-Vertragsstatuswerten.

`learner-controlled` erlaubt der lernenden Person, ein eigenes analoges oder lokales digitales Artefakt selbst zu verwahren. `storage: prohibited` verbietet institutionelle beziehungsweise lehrkraftseitige Speicherung; es verbietet nicht die lernendengesteuerte lokale Verwahrung.

## 6. Recordgenaue Privacy-Disposition

Jeder Zeitreview eines Moduls mit Privacy-Vertrag erhält das zusätzliche Feld `privacyDisposition`.

```json
{
  "privacyDisposition": {
    "contractId": "PC-IUM-5-CORE-07",
    "observableBasis": "nonpersonal-follow-up",
    "evidenceContractId": "CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-001",
    "privateArtifactContribution": {
      "product": "excluded",
      "evidence": "excluded",
      "additionalTimeClaim": "excluded"
    },
    "privateActivityTimeTreatment": "module-budget-only"
  }
}
```

### 6.1 Exakte Felder

`privacyDisposition` besitzt ausschließlich:

- `contractId`
- `observableBasis`
- `evidenceContractId`
- `privateArtifactContribution`
- `privateActivityTimeTreatment`

`privateArtifactContribution` besitzt ausschließlich:

- `product`
- `evidence`
- `additionalTimeClaim`

### 6.2 Exakte Werte

Für jede Disposition gelten:

- `contractId` referenziert den Privacy-Vertrag desselben Moduls;
- `observableBasis` ist genau einer der Werte:
  - `nonpersonal-follow-up`
  - `nonpersonal-module-detail`
  - `none`
- `evidenceContractId` ist die IUM09-Evidenzvertrags-ID oder exakt `null`;
- `product`, `evidence` und `additionalTimeClaim` sind jeweils exakt `excluded`;
- `privateActivityTimeTreatment == "module-budget-only"`.

`module-budget-only` bedeutet: Die private Aktivität darf reale Lernzeit innerhalb des Modulbudgets beanspruchen. Ihr Inhalt, Bearbeitungsstand oder individueller Zeitbedarf darf jedoch keine recordbezogene Zusatzzeit, Produktspur oder Evidenz begründen.

## 7. CORE-07-Migrationsmatrix

| Kompetenz-ID | Entscheidung | Zusatzminuten | `observableBasis` | `evidenceContractId` |
|---|---:|---:|---|---|
| `BMB16-GYM-IK-MG-001` | `additional-time` | 15 | `nonpersonal-follow-up` | `CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-001` |
| `BMB16-GYM-IK-MG-002` | `additional-time` | 20 | `nonpersonal-module-detail` | `CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-002` |
| `BMB16-GYM-IK-MG-003` | `absorbed` | 0 | `nonpersonal-follow-up` | `CE-IUM-5-CORE-07-BMB16-GYM-IK-MG-003` |
| `BMB16-GYM-PK-RK-001` | `additional-time` | 15 | `nonpersonal-follow-up` | `CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-001` |
| `BMB16-GYM-PK-RK-002` | `additional-time` | 15 | `nonpersonal-follow-up` | `CE-IUM-5-CORE-07-BMB16-GYM-PK-RK-002` |
| `BMB16-GYM-PK-RK-003` | `unresolved` | 0 | `none` | `null` |
| `LH26-E-DP-003` | `unresolved` | 0 | `none` | `null` |

Die positiven Record-Minuten bleiben:

```text
15 + 20 + 15 + 15 = 65 Minuten
```

`BMB16-GYM-IK-MG-003` nutzt eine bereits vorhandene nichtpersonale Produkt- und Revisionsspur und beansprucht keine zusätzlichen Minuten.

## 8. Validatorarchitektur

### 8.1 Neue Funktion

```python
def validate_privacy_contracts(
    privacy_contracts,
    module_contracts,
):
    """Validate privacy contracts and return them keyed by contract id."""
```

Die Funktion:

- verlangt eine Liste;
- validiert exakte Felder und Werte;
- lehnt boolesche oder leere Ersatzwerte ab;
- erzwingt eindeutige Vertrags- und Modul-IDs;
- prüft, dass das Modul im validierten Zeitmodell existiert;
- gibt ein Mapping nach Vertrags-ID zurück.

### 8.2 Erweiterte Zeitreview-Funktion

Die bestehende öffentliche Reihenfolge bleibt kompatibel:

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

`privacy_contracts` ist das bereits durch `validate_privacy_contracts()` validierte Mapping.

### 8.3 Aktivierungsregeln

Der Validator arbeitet fail-closed:

1. Hat ein Modul einen Privacy-Vertrag, benötigt jeder registrierte Zeitreview dieses Moduls eine `privacyDisposition`.
2. Hat ein Zeitreview laut IUM09-Handoff `causeClass == "private-local"`, benötigt sein Modul spätestens mit Aufnahme des Reviews einen Privacy-Vertrag.
3. Reviews anderer Module dürfen keine verwaiste `privacyDisposition` führen.
4. Vertrags-, Modul- und Kompetenzbezüge müssen eindeutig sein.

### 8.4 Evidenzbasis

`observableBasis` wird gegen den IUM09-Handoff geprüft:

- `nonpersonal-follow-up`
  - nur bei `causeClass == "private-local"`;
  - `evidenceContractId` muss der nichtleeren Handoff-ID entsprechen;
  - die private Aktivität bleibt von Produkt, Evidenz und Zusatzzeit ausgeschlossen.
- `nonpersonal-module-detail`
  - nur bei `causeClass == "module-detail"`;
  - `evidenceContractId` muss der nichtleeren Handoff-ID entsprechen.
- `none`
  - nur bei Handoff-`evidenceContractId == null`;
  - Reviewentscheidung muss `unresolved` sein;
  - `additionalMinutes == 0`;
  - `phaseIds`, `pathAvailability` und `integrationContractIds` sind leer;
  - `sequenceEvidenceId == null`.

Positive Zusatzminuten sind nur zulässig, wenn `observableBasis != "none"`. Ihre fachliche Begründung stammt ausschließlich aus dem nichtpersonalen Evidenzpfad.

### 8.5 Fehler

Fehler werden als `IUM10ValidationError` ausgegeben. Die Meldung nennt mindestens:

- Modul-ID bei einem Modulvertragsfehler;
- Kompetenz-ID bei einer fehlerhaften Disposition;
- betroffenes Feld beziehungsweise verletzte Beziehung.

Datenschutzfehler sind harte Validierungsfehler. Es gibt keinen Warn- oder Fallbackmodus.

## 9. Verhältnis zu IUM09

IUM09 bleibt fachlich und technisch unverändert:

- `causeClass` bleibt autoritativ für die Herkunft der Lücke;
- `evidenceContractId` bleibt autoritativ für die Coverage-Evidenz;
- `privacyBoundary` und `nonPersonalFollowUp` bleiben als lesbare Bestandteile der IUM09-Evidenzverträge erhalten;
- Coverage-Fingerprints und Modulstruktur-Fingerprints bleiben unverändert;
- IUM10 präemptiert keinen semantischen Coverage-Status.

Der Privacy-Vertrag bewertet die IUM09-Entscheidung nicht neu. Er legt ausschließlich fest, welche Anteile eine IUM10-Zeitentscheidung tragen dürfen.

## 10. Entfernung der Freitextheuristik

Nach nachgewiesenem RED und GREEN der strukturierten Tests werden entfernt:

- `_assert_core07_no_affirmative_private_handling`;
- die zugehörigen Token-, Klausel-, Negations-, Prohibitions- und Aktionsparser-Helfer;
- die Grammatikfamilien-Tests, deren Aussage ausschließlich vom Freitextparser abhängt.

Erhalten bleiben fachliche Repositorytests für:

- Medienwirkung und Kriterienurteil;
- private lokale Lernaktivität;
- unabhängigen nichtpersonalen Anschlussnachweis;
- Produkt- und Phasengrenzen;
- die beiden unresolved Records;
- unveränderte Minuten, Pfade und Jahresbilanzen.

Eine Prose-Rephrase darf die strukturierte Privacy-Garantie nicht verändern. Widerspruchsfreie und klare Prosa bleibt Gegenstand des menschlichen Fachreviews, nicht eines selbstgebauten Sprachparsers.

## 11. TDD- und Mutationsstrategie

### 11.1 RED vor Datenmigration

Tests müssen zunächst nachweisen, dass Schema 1 beziehungsweise fehlende strukturierte Verträge folgende Fälle nicht erfüllt:

- fehlendes `privacyContracts`;
- fehlender CORE-07-Vertrag;
- fehlende Dispositionen;
- fehlende strukturierte Ausschlüsse.

### 11.2 Vertragstests

Die Tests mutieren einzeln:

- jedes top-level Feld;
- jedes Feld von `institutionalHandling`;
- jede institutionelle Handlung von `prohibited` auf einen anderen Wert;
- Vertrags-ID, Modul-ID und Dubletten;
- `scope`, `artifactOwner`, `artifactCustody` und `status`;
- unbekannte Zusatzfelder.

### 11.3 Dispositionstests

Die Tests mutieren einzeln:

- fehlende oder zusätzliche Felder;
- falsche Vertrags- oder Modulreferenz;
- jede Variante von `observableBasis`;
- abweichende oder unzulässige `evidenceContractId`;
- jeden der drei Ausschlüsse;
- `privateActivityTimeTreatment`;
- `none` zusammen mit Evidenz, Phase, Pfad, Integration oder positiven Minuten;
- positive Minuten ohne nichtpersonale Evidenzbasis.

### 11.4 Repositorybilanz

Ein Repositorytest weist exakt nach:

- ein CORE-07-Modulvertrag;
- sieben CORE-07-Dispositionen;
- vier `nonpersonal-follow-up`;
- ein `nonpersonal-module-detail`;
- zwei `none`;
- 65 positive Record-Minuten;
- zwei unveränderte `unresolved`-Reviews.

## 12. Unveränderte fachliche und zeitliche Bilanz

Die Migration verändert nicht:

- CORE-07 mit 4/5/6 Unterrichtseinheiten;
- Klasse 5 mit 30/34/38 Unterrichtseinheiten;
- Klasse 6 mit 30/34/38 Unterrichtseinheiten;
- Klasse 7 mit 40/46/54 Unterrichtseinheiten;
- 31 Modulverträge;
- 60 IUM09-Zeitübergaben;
- IUM09-Endbilanz 164 `covered` / 7 `partial`;
- prior20-Strukturhash;
- Modul-, Coverage- und Handoff-Fingerprints.

Die Task-14-Berichtstabelle wird präzisiert:

- 85 Minuten sind nichtadditive Phasenclaims;
- 65 Minuten sind positive Record-Minuten;
- beide Größen werden getrennt ausgewiesen und nicht summengleich dargestellt.

## 13. Dateien im Implementierungsscope

Voraussichtlich geändert:

```text
roadmap/time-model.json
scripts/validate_ium10.py
tests/test_validate_ium10.py
.superpowers/sdd/2026-07-30-ium10-zeitmodell-modulroadmap-implementation/task-14-report.md
```

Die `.superpowers`-Artefakte bleiben git-ignorierte Ausführungsnachweise.

Nicht geändert:

```text
roadmap/module-candidates.json
roadmap/coverage-plan.json
roadmap/coverage-remediation.json
curriculum/
scripts/validate_ium09.py
tests/test_validate_ium09.py
```

## 14. Abnahmekriterien

Der Architekturtask ist implementiert, wenn:

1. `time-model.json` Schema 2 nutzt.
2. `PC-IUM-5-CORE-07` exakt dem Modulvertrag entspricht.
3. alle sieben CORE-07-Reviews die festgelegte Disposition besitzen.
4. sämtliche Struktur-, Referenz-, Enum- und Mutationsfehler fail-closed mit recordgenauer Meldung scheitern.
5. der Freitextparser und seine parserabhängigen Grammatiktests entfernt sind.
6. die fachlichen CORE-07-Nachweise weiterhin vollständig bestehen.
7. Zeitentscheidungen, Phasen, Pfade, Minuten und Jahresbilanzen unverändert sind.
8. RK-003 und DP-003 `unresolved` bleiben.
9. IUM09-, IUM10-, Phase-0- und vollständige Repositorytests grün sind.
10. UTF-8-, Diff-, Fingerprint- und prior20-Gates grün sind.
11. ein unabhängiger Review keine offenen Critical- oder Important-Befunde meldet.

## 15. Nicht Bestandteil

Dieser Architekturtask:

- migriert noch keine Klasse-7-Zeitreviews;
- schließt keine verbleibende curriculare Lücke;
- ändert keine private Lernaufgabe;
- führt keine Diagnostik oder personenbezogene Speicherung ein;
- verändert keine Phase-1-Plattformentscheidung;
- veröffentlicht oder pusht noch keinen Zwischenstand.

