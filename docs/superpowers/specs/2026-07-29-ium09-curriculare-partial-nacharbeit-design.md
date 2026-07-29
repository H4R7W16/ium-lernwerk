# IUM09 – Curriculare Partial-Nacharbeit

**Status:** zur schriftlichen Nutzerreview
**Fassung:** 1.0
**Datum:** 29. Juli 2026
**Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E
**Ausgangsstand:** Commit `69c9d4f5504a297289615b4169fc4a9ea6d9b253`

## 1. Ziel

IUM09 bearbeitet die 60 in Phase 0 dokumentierten `partial`-Records fachlich und recordgenau. Die Nacharbeit darf weder eine formale Zuordnung als Abdeckung ausgeben noch die freigegebene Modulstruktur durch unkontrollierte Erweiterungen verändern.

Für jeden der 60 Ausgangsrecords muss nach der Umsetzung nachvollziehbar sein:

1. welcher exakte Quelltext geprüft wurde;
2. warum der Record zuvor `partial` war;
3. welcher Ursachenklasse er angehört;
4. welche fachliche Lernhandlung und welche Produktspur die Lücke schließen sollen;
5. ob der Status nach manuellem Fachaudit zu `covered` wechselt oder begründet `partial` bleibt;
6. welche Folgen für Zeitmodell und Modulgraph geprüft wurden;
7. welche nächste Entscheidung bei einer verbleibenden Lücke nötig ist.

Die Zahl der nach IUM09 verbleibenden `partial`-Records ist ein Ergebnis des Audits und keine vorab festgelegte Zielquote.

## 2. Verbindliche Grenzen

### 2.1 Semantische Grenze

`covered` bleibt eine Aussage auf Ebene des Modulkandidatendesigns. Der Status bedeutet:

- der vollständige Operator und Gegenstand des Records sind in einer fachlich passenden Lernhandlung enthalten;
- ein dazu passendes Lernprodukt oder eine andere ausdrücklich begründete Produktspur macht die Handlung überprüfbar;
- die Lernhandlung und Produktspur sind in einem Kernmodul verbindlich verankert;
- das `matchRationale` weist diesen Zusammenhang recordgenau nach.

`covered` bedeutet nicht:

- dass ein fertiges Modul implementiert ist;
- dass jede Schülerin und jeder Schüler die Kompetenz erworben hat;
- dass die Jahreszeit ausreicht;
- dass ein Unterrichtspilot bestanden wurde;
- dass aus einer formalen String-Übereinstimmung fachliche Abdeckung folgt.

### 2.2 Struktur- und Zeitgrenze

IUM09 verändert nicht:

- die 31 freigegebenen Modulkandidaten;
- Modul-IDs, Jahrgangszuordnungen oder Modultypen;
- `prerequisiteModuleIds`;
- `lessonRange`;
- die Trennung von Kernlernweg und flexiblen Vertiefungs-, Transfer- und Projektmodulen.

Wenn eine Lücke nur durch ein neues Modul, eine neue Abhängigkeit oder eine Änderung des Stundenkorridors geschlossen werden kann, bleibt der Record in IUM09 `partial`. Der Bedarf wird für IUM10 ausgewiesen.

IUM09 darf Zeitdruck sichtbar machen, aber keine zeitliche Tragfähigkeit behaupten. IUM10 übernimmt anschließend den recordgenauen Zeit- und Sequenzreview.

### 2.3 Datenschutz- und Diagnosegrenze

Es entstehen keine Konten, Namen, Profile, zentralen Kompetenzstände, Learning Analytics, Tracker, automatisierten Bewertungen oder personenbezogenen Telemetriedaten.

Private beziehungsweise sensible Selbstreflexion:

- findet ausschließlich in einem privaten lokalen Artefakt statt;
- wird nicht erhoben, übertragen, eingesammelt, gespeichert oder bewertet;
- wird nicht durch eine Offenlegungspflicht ersetzt;
- führt in eine nichtpersonale fachliche Anschlussaufgabe;
- ist kein integriertes Diagnoseinstrument.

### 2.4 Quellen- und Statusgrenze

Die normative Gewichtung bleibt erhalten:

- Basiskurs Medienbildung 2016 und Aufbaukurs Informatik 2016: `enacted`;
- Lesehilfe 2026/2027: `orientation`.

Die Lesehilfe wird nicht zur in Kraft gesetzten Norm aufgewertet. Das IuM-Fachprofil und alle aus Forschung abgeleiteten konkreten Planungsfolgen behalten ihren bisherigen Reifestatus.

## 3. Begründete Architekturentscheidung

### 3.1 Gewählter Ansatz: recordgenaue Evidenzverträge

Jeder fachlich geschlossene Ausgangsrecord erhält einen kleinen Evidenzvertrag im zuständigen Kernmodul. Ein Evidenzvertrag beschreibt nicht das ganze Modul, sondern genau die Teil-Lernhandlung und Produktspur, die für einen bestimmten Curriculumrecord verpflichtend sind.

Die zentrale Lernhandlung und das zentrale Lernprodukt eines Moduls bleiben lesbare Verdichtungen. Sie werden nicht zu langen Aufzählungen aller Einzelanforderungen erweitert.

Zusätzlich entsteht ein eigenständiges Nacharbeitsledger. Es hält den unveränderlichen Ausgangsbefund, die Entscheidung, den Evidenzvertrag sowie Zeit-, Graph- und Restrisikofolgen zusammen.

### 3.2 Verworfene Alternative: zentrale Modultexte verlängern

Eine bloße Erweiterung von `centralLearningAction` und `centralLearningProduct` würde bei Modulen mit sechs oder sieben Lücken unlesbare Sammelsätze erzeugen. Der einzelne Operator-Produkt-Match bliebe schwer prüfbar und eine kosmetische Statusanhebung wäre weiterhin möglich.

### 3.3 Verworfene Alternative: Module sofort teilen oder neu ordnen

Ein unmittelbarer Umbau des Modulgraphen würde die freigegebene Roadmapstruktur mit dem noch offenen Zeitmodell vermischen. Er würde IUM10 vorwegnehmen und die Wirkung einzelner Coverageentscheidungen auf Zeit und Progression verschleiern.

## 4. Ursachenklassen und Evidenzmodi

Alle 60 Ausgangsrecords gehören genau einer der folgenden Klassen an.

| Ursachenklasse / Evidenzmodus | Anzahl | Bedeutung | Nacharbeitsregel |
|---|---:|---|---|
| `module-detail` | 39 | Im bestehenden Modul fehlen ein expliziter fachlicher Teilschritt oder eine passende Produktspur. | Recordgenaue Lernhandlung und Produktspur im Kernmodul ergänzen und manuell auditieren. |
| `school-context` | 9 | Die Anforderung verlangt tatsächliches Handeln in einer schulischen System-, Kommunikations- oder Regelumgebung. | Plattformneutralen lokalen Konfigurationspunkt und realen Ausführungsnachweis festlegen; Simulation allein genügt nicht. |
| `private-local` | 8 | Die Anforderung berührt eigene Nutzung, Empfindung oder Selbstwahrnehmung. | Private lokale Reflexion ohne Erhebung mit einer nichtpersonalen fachlichen Anschlussaufgabe verbinden. |
| `roadmap-level` | 4 | Die Anforderung betrifft jahrgangsweite Balance, Progression oder Gewichtung und kann nicht durch ein Einzelmodulprodukt belegt werden. | In IUM09 `partial` belassen und als verpflichtenden Sequenznachweis an IUM10 übergeben. |

## 5. Datenartefakte

### 5.1 Erweiterung von `roadmap/module-candidates.json`

Betroffene Kernmodule erhalten ein optionales Feld `coverageEvidence`. Es enthält ausschließlich recordgenaue Evidenzverträge, die im manuellen Audit als fachlich tragfähig beurteilt wurden.

Ein Basisvertrag besitzt diese Felder:

```json
{
  "id": "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
  "competencyId": "BMB16-GYM-IK-GM-001",
  "mode": "module-detail",
  "learningAction": "Konkrete fachliche Lernhandlung.",
  "productEvidence": "Konkrete überprüfbare Produktspur.",
  "productVisibility": "shared"
}
```

Regeln:

- `id` ist repositoryweit eindeutig.
- `competencyId` muss im selben Modul in `competencyIds` stehen.
- Der Vertrag darf nur in einem Kernmodul liegen.
- `learningAction` nennt den vollständigen fachlichen Operator und Gegenstand.
- `productEvidence` nennt, woran die Lernhandlung im Kandidatendesign erkennbar wird.
- `productVisibility` ist genau einer der Werte `shared`, `teacher-observable` oder `private-local`.
- `module-detail` erlaubt ausschließlich `shared` oder `teacher-observable`.
- Ein Vertrag ist keine Leistungsbewertung und keine Aussage über tatsächlichen Kompetenzerwerb.

Für `school-context` kommen verpflichtend hinzu:

```json
{
  "executionType": "actual-local-use",
  "localConfigurationRequirement": "Welche schulische System-, Kanal- oder Regelumgebung vor Ort einzusetzen ist."
}
```

Dabei gilt:

- `executionType` muss exakt `actual-local-use` sein;
- `productVisibility` muss `shared` oder `teacher-observable` sein;
- keine bestimmte Plattform wird als allgemeine Voraussetzung festgeschrieben;
- die Lernhandlung muss eine tatsächliche lokale Ausführung verlangen;
- ein rein fiktiver oder nur beschriebener Ablauf schließt den Record nicht;
- der Ausführungsnachweis darf keine Zugangsdaten oder privaten Kommunikationsinhalte speichern.

Für `private-local` kommen verpflichtend hinzu:

```json
{
  "privacyBoundary": "Das private lokale Artefakt wird nicht erhoben, übertragen, eingesammelt, gespeichert oder bewertet.",
  "nonPersonalFollowUp": "Nichtpersonale fachliche Anschlussaufgabe."
}
```

Dabei gilt:

- `productVisibility` muss `private-local` sein;
- `productEvidence` beschreibt ein privates lokales Artefakt;
- `nonPersonalFollowUp` überführt die Reflexion in Fallanalyse, Kriterienarbeit, Modellbildung, Handlungsoption oder fachliches Urteil ohne persönliche Offenlegung;
- Lehrkraftbeobachtung, Gespräch oder Abgabe dürfen nicht zur verdeckten Erhebung des privaten Inhalts werden.

Für `roadmap-level` wird kein Evidenzvertrag im Einzelmodul angelegt.

### 5.2 Neues Artefakt `roadmap/coverage-remediation.json`

Das Nacharbeitsledger besitzt `schemaVersion: 1`, den Status `working`, den Ausgangscommit, die Ausgangszahlen, einen Baseline-Fingerprint und genau 60 Einträge.

Der Baseline-Fingerprint verhindert, dass der Ausgangsbefund während der Nacharbeit unbemerkt umgeschrieben wird. Er ist der SHA-256-Wert einer kanonischen UTF-8-JSON-Darstellung. Dafür werden die 60 Objekte nach `competencyId` sortiert und jeweils genau diese Felder verwendet:

```text
competencyId
requirementText
before.coverageStatus
before.semanticAudit
before.evidenceModuleId
before.reason
```

Die Serialisierung nutzt sortierte Objektschlüssel, keine ASCII-Ersetzung und die kompakten JSON-Trennzeichen `,` und `:`. Der erwartete Fingerprint wird als IUM09-Baselinekonstante im Validator festgeschrieben und in einem Unit-Test gesichert. Der Validator benötigt dadurch keinen Git-Zugriff.

```json
{
  "baseline": {
    "coverageCommit": "69c9d4f5504a297289615b4169fc4a9ea6d9b253",
    "partialCount": 60,
    "recordFingerprintSha256": "b7602352c67f61cdf075a65df167e12f7283b8f62867386545fea758b6e08892"
  }
}
```

Jeder Eintrag folgt diesem Vertrag:

```json
{
  "competencyId": "BMB16-GYM-IK-GM-001",
  "requirementText": "Exakter Text aus der registrierten Curriculumquelle.",
  "causeClass": "module-detail",
  "before": {
    "coverageStatus": "partial",
    "semanticAudit": "documented-gap",
    "evidenceModuleId": "IUM-5-CORE-01",
    "reason": "Exakter Ausgangsgrund aus coverage-plan.json."
  },
  "decision": "covered",
  "evidenceContractId": "CE-IUM-5-CORE-01-BMB16-GYM-IK-GM-001",
  "after": {
    "coverageStatus": "covered",
    "semanticAudit": "operator-product-match"
  },
  "changeRationale": "Recordgenaue fachliche Begründung der Entscheidung.",
  "timeImpact": {
    "level": "review-required",
    "rationale": "Warum IUM10 diese Lernhandlung zeitlich prüfen muss."
  },
  "graphImpact": {
    "level": "none",
    "rationale": "Warum keine neue Modulabhängigkeit nötig ist."
  },
  "residualGap": null
}
```

Zulässige Entscheidungen:

- `covered`: Der Evidenzvertrag besteht den manuellen Operator-Gegenstand-Lernhandlung-Produkt-Audit.
- `remain-partial`: Die Lücke bleibt sichtbar.

Bei `covered` gilt:

- `evidenceContractId` ist gesetzt und verweist auf genau einen gültigen Vertrag;
- `after.coverageStatus` ist `covered`;
- `after.semanticAudit` ist `operator-product-match`;
- `residualGap` ist `null`.

Bei `remain-partial` gilt:

- `evidenceContractId` ist `null`;
- `after.coverageStatus` ist `partial`;
- `after.semanticAudit` ist `documented-gap`;
- `residualGap` enthält die drei nichtleeren Felder `reason`, `risk` und `followUp`.

Zulässige Zeitfolgen:

- `none-detected`: Der Vertrag präzisiert eine bereits im Modul angelegte Lernhandlung; daraus folgt noch keine Freigabe des Jahreszeitmodells.
- `review-required`: Der Vertrag ergänzt oder konkretisiert eine Lernhandlung, deren Zeitbedarf IUM10 prüfen muss.
- `roadmap-dependent`: Die Anforderung kann nur jahrgangs- oder roadmapweit beurteilt werden.

Zulässige Graphfolgen:

- `none`: Der Record bleibt im bestehenden Modul und benötigt keine neue Voraussetzung.
- `review-required`: Eine belastbare Schließung würde eine Strukturänderung verlangen. In diesem Fall muss die Entscheidung `remain-partial` sein.

### 5.3 Änderung von `roadmap/coverage-plan.json`

Für einen der 60 Ausgangsrecords darf sich `coverageStatus` nur ändern, wenn:

1. ein Ledger-Eintrag mit unverändertem Ausgangsbefund existiert;
2. der Ledger-Eintrag `decision: covered` besitzt;
3. ein gültiger Evidenzvertrag existiert;
4. `evidence` und `matchRationale` den exakten Quelltext sowie die unveränderte `learningAction` und `productEvidence` des Vertrags enthalten;
5. der manuelle Fachaudit die Semantik bestätigt.

Geänderte Records erhalten das Feld `evidenceContractId`.

Die 111 zuvor `covered` eingestuften Records bleiben außerhalb des IUM09-Ledgers und verwenden weiterhin ihren bestehenden zentralen Modulnachweis.

Ein verbleibender `partial`-Record behält eine konkrete Lücke. Sein `reason`, `risk` und `followUp` müssen mit `residualGap` im Ledger übereinstimmen.

### 5.4 Änderung von `roadmap/module-roadmap.md`

Die Roadmap dokumentiert nach IUM09:

- die neue Coveragebilanz nach Quellengewicht;
- die Zahl der geschlossenen und verbleibenden Ausgangslücken;
- die vier Ursachenklassen;
- Module mit besonderem Verdichtungs- oder Zeitdruck;
- alle `timeImpact`-Einträge mit `review-required` oder `roadmap-dependent` als Übergabe an IUM10;
- die weiterhin unveränderten Modulabhängigkeiten und Stundenkorridore;
- die Trennung von semantischer Abdeckung und zeitlicher Umsetzbarkeit.

Die Roadmap darf aus IUM09 keine verbesserte Jahresfreigabe ableiten.

## 6. Datenfluss und Prüfkette

```text
registrierter Curriculumrecord
→ Ausgangseintrag in coverage-plan.json
→ Ursachenklasse im Nacharbeitsledger
→ gegebenenfalls Evidenzvertrag im zuständigen Kernmodul
→ manueller Operator-Gegenstand-Lernhandlung-Produkt-Audit
→ After-Entscheidung im Ledger
→ synchroner Status in coverage-plan.json
→ Zeit- und Graphübergabe in module-roadmap.md
→ maschinelle Konsistenzprüfung
→ Fachreview und Engineeringreview
→ Nutzerreview der verbleibenden Lücken
```

Die maschinelle Prüfung validiert Struktur, Identität, Vollständigkeit und referenzielle Konsistenz. Sie ersetzt keine natürlichsprachliche Semantikentscheidung.

## 7. Manuelle Entscheidungsregeln

### 7.1 Operator- und Gegenstandsprüfung

Vor `covered` wird der Record in atomare Anforderungen zerlegt:

- Operator oder Operatorfolge;
- fachlicher Gegenstand;
- verlangter Kontext;
- Reichweite wie „mehrere“, „gemeinsam“, „selbstständig“ oder „aus verschiedenen Perspektiven“;
- gegebenenfalls Produkt-, Reflexions- oder Handlungsbedingung.

Jede Teilanforderung muss in `learningAction` und `productEvidence` nachweisbar sein. Ein ähnliches Thema oder ein schwächerer Operator genügt nicht.

### 7.2 Aufgaben- und Produktprüfung

Die Produktspur muss zur verlangten Lernhandlung passen:

- Benennen oder Beschreiben verlangt identifizierbare Fachbegriffe beziehungsweise Merkmale.
- Anwenden oder Nutzen verlangt tatsächliche Ausführung, nicht nur Beschreibung.
- Erklären verlangt nachvollziehbare Beziehungen oder Mechanismen.
- Vergleichen verlangt Kriterien und mindestens zwei Bezugsgrößen.
- Bewerten verlangt Kriterien, Belege und ein begründetes Urteil.
- Entwerfen, Implementieren, Testen und Debuggen bleiben unterscheidbare informatische Handlungen.
- Reflektieren verlangt eine revidierbare Beziehung zwischen Erfahrung, Kriterium und Handlungsoption, ohne eine persönliche Offenlegung zu erzwingen.

### 7.3 Überfrachtungsprüfung

Ein Evidenzvertrag darf nicht nur deshalb akzeptiert werden, weil sein Text formal in ein Modul passt.

Der Record bleibt `partial`, wenn:

- die neue Lernhandlung die zentrale Modulfrage nicht trägt;
- die Produktspur ein unverbundenes Zusatzprodukt erzeugt;
- eine neue Voraussetzung nötig wäre;
- die Anforderungen innerhalb des bestehenden Kandidaten fachlich nicht orchestrierbar erscheinen;
- die Schließung nur durch eine Zeit- oder Strukturannahme möglich wird, die IUM09 nicht freigeben darf.

### 7.4 Datenschutzprüfung

Für `private-local` wird fachlich geprüft:

- Ist die private Reflexion für den Curriculumoperator tatsächlich nötig?
- Bleibt das Artefakt ausschließlich bei der lernenden Person?
- Funktioniert die fachliche Anschlussaufgabe ohne Kenntnis des privaten Inhalts?
- Entsteht keine Benotungs-, Vergleichs- oder Offenlegungserwartung?
- Wird kein Profil aus Einzelantworten oder Nutzungsdaten abgeleitet?

Wenn eine dieser Bedingungen nicht erfüllt ist, bleibt der Record `partial`.

## 8. Fehlerbehandlung und Validatorregeln

Der Phase-0-Validator wird um folgende Fehlerfälle erweitert:

1. Das Ledger enthält nicht exakt die 60 Ausgangs-IDs oder enthält Duplikate.
2. Die Ursachenklassen ergeben nicht exakt 39 `module-detail`, 9 `school-context`, 8 `private-local` und 4 `roadmap-level`.
3. `requirementText` oder `before` weicht vom festgeschriebenen Baseline-Fingerprint des Ausgangscommits ab.
4. Ein Evidenzvertrag verweist auf eine unbekannte Kompetenz, ein anderes Modul oder ein flexibles Modul.
5. Eine Vertrags-ID ist doppelt.
6. `mode`, `productVisibility` oder bedingte Felder sind ungültig.
7. `school-context` besitzt keinen lokalen Konfigurationspunkt oder verlangt keine tatsächliche Ausführung.
8. `private-local` ist nicht privat sichtbar oder besitzt keine Datenschutzgrenze und keine nichtpersonale Anschlussaufgabe.
9. `roadmap-level` besitzt einen Einzelmodulvertrag oder wechselt in IUM09 zu `covered`.
10. `decision`, After-Status und `semanticAudit` widersprechen sich.
11. Ein geschlossener Record besitzt keinen gültigen `evidenceContractId`.
12. `evidence` oder `matchRationale` weicht von Quelle oder Evidenzvertrag ab.
13. Ein verbleibender `partial`-Record besitzt kein vollständiges `residualGap`.
14. `graphImpact: review-required` wird dennoch als `covered` entschieden.
15. Modul-IDs, Jahrgänge, Typen, Voraussetzungen oder Stundenkorridore unterscheiden sich vom Baselinecommit.
16. Die 171 Pflichtrecords sind nicht mehr vollständig und eindeutig im Coverageplan enthalten.

Fehlermeldungen nennen die betroffene `competencyId` oder Vertrags-ID.

## 9. Teststrategie

Die Umsetzung erfolgt testgetrieben.

### 9.1 Unit-Tests für Evidenzverträge

Tests prüfen:

- gültige Basisverträge;
- unbekannte oder doppelte Kompetenz- und Vertrags-IDs;
- Kernmodulbindung;
- zulässige Modi und Sichtbarkeiten;
- modeabhängige Pflichtfelder;
- die Datenschutzregeln für `private-local`;
- den lokalen Konfigurationspunkt für `school-context`.

### 9.2 Unit-Tests für das Nacharbeitsledger

Tests prüfen:

- exakt 60 eindeutige Baseline-Records;
- die Verteilung 39/9/8/4;
- exakten Quelltext und unveränderten Ausgangsgrund;
- konsistente Decision-/After-Kombinationen;
- gültige Zeit- und Graphfolgen;
- vollständige Restrisiken bei `remain-partial`;
- die verpflichtende `remain-partial`-Entscheidung für die vier `roadmap-level`-Records.

### 9.3 Integrationstests

Tests prüfen die Kette:

```text
Curriculumquelle
↔ Modulzuordnung
↔ Evidenzvertrag
↔ Nacharbeitsledger
↔ Coverageplan
↔ Roadmapbilanz
```

Insbesondere gilt:

- Jede Statusänderung der Ausgangs-60 ist ledgergestützt.
- Kein anderer Record wird durch IUM09 unbeabsichtigt umklassifiziert.
- Die 111 zuvor `covered` eingestuften Records bleiben erhalten.
- Die Baselineverträge von Modulgraph und Zeitkorridoren bleiben unverändert.
- Summen nach `enacted` und `orientation` stimmen mit den Daten überein.

### 9.4 Repository-Gates

Vor Übergabe müssen grün sein:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_phase0.py
git diff --check
```

Zusätzlich erfolgen:

- UTF-8- und Sonderzeichenprüfung der veränderten Textdateien;
- manueller Fachaudit aller 60 Entscheidungen;
- Engineeringreview von Schema, Validator und Tests;
- Review der Zeit- und Graphübergabe;
- Nutzerreview der verbleibenden `partial`-Records.

## 10. Umsetzungsreihenfolge

1. Tests für den Evidenzvertrag schreiben und rot ausführen.
2. Validatorunterstützung für `coverageEvidence` implementieren.
3. Tests für das 60er-Nacharbeitsledger schreiben und rot ausführen.
4. `coverage-remediation.json` mit unveränderten Ausgangsbefunden und Ursachenklassen anlegen.
5. Die Records modulweise manuell auditieren.
6. Nur bestandene Entscheidungen als Evidenzverträge in Kernmodule eintragen.
7. Coverageplan und Ledger synchron aktualisieren.
8. Integrationstests für die vollständige Nachweiskette ergänzen.
9. Roadmapbilanz und IUM10-Übergabe aktualisieren.
10. Vollständige Tests, Validator, Diff- und Encoding-Gates ausführen.
11. Fach- und Engineeringreview durchführen.
12. Verbleibende Lücken zur Nutzerentscheidung vorlegen.

Die modulweise Reihenfolge beginnt bei den höchsten Lückenkonzentrationen:

1. `IUM-5-CORE-01`
2. `IUM-5-CORE-07`
3. `IUM-7-CORE-08`
4. `IUM-5-CORE-03`
5. `IUM-7-CORE-03`
6. übrige betroffene Kernmodule

## 11. Didaktische Qualitätsprüfung

### Prüf-Gates

- **Planungsanker:** gesichert; Curriculumquellen, IuM-Fachprofil, Phase-0-Coverageplan und freigegebene Roadmapstruktur sind maßgeblich.
- **Lernprozess:** tragfähig, wenn jeder geschlossene Record eine fachliche Denk- oder Handlungsspur statt bloßer Themennennung besitzt.
- **Sinn und Eigenleistung:** begründet, wenn das Produkt Erklären, Anwenden, Prüfen, Gestalten, Bewerten oder Reflektieren tatsächlich benötigt.
- **Fachlichkeit und Material:** exact source first; amtliche Begriffe, Operatoren und Geltungsstatus bleiben erhalten.
- **Passung und Anspruch:** noch nicht zeitlich freigegeben; Überfrachtungsbefunde gehen sichtbar an IUM10.
- **Lernsteuerung und Diagnose:** Produktspuren dienen lernbezogener Rückmeldung; private Reflexion bleibt außerhalb von Erhebung und Bewertung.
- **Ausspielkanal:** nicht Gegenstand von IUM09; digital bleibt Primärmedium, ohne funktionslose analoge Doppelstruktur.

### WU-Check

- **Kognitive Aktivierung:** Der Evidenzvertrag verlangt eine konkrete fachliche Handlung und nicht nur Bedienung oder Aktivität.
- **Konstruktive Unterstützung:** IUM09 schreibt keine vollständigen Hilfen aus; es verhindert aber Produktanforderungen, die die zentrale Denkhandlung ersetzen.
- **Klassenführung / Struktur:** Schulkontext-Verträge benennen einen lokalen Konfigurationspunkt, damit reale Systembedingungen vor Durchführung geklärt werden.
- **Aufgabenqualität:** Operator, Gegenstand, Lernhandlung und Produktspur müssen valide zusammenpassen.
- **Feedback / Diagnose:** Sichtbare Produkte ermöglichen Rückmeldung; private Artefakte werden nicht zur Diagnosequelle.
- **Kooperation / Verantwortlichkeit:** Kooperationsrecords verlangen tatsächliche gemeinsame Nutzung und eine identifizierbare gemeinsame Produktspur.
- **Diagnose-Fallback:** Ein fehlender oder privater Nachweis wird nicht durch personenbezogene Datenerhebung kompensiert; der Record bleibt gegebenenfalls `partial`.
- **Sprachsensibilität / Zugänglichkeit:** Fachbegriffe und Operatoren bleiben quellentreu; konkrete sprachliche Scaffolds gehören in die spätere Modulspezifikation.
- **Wichtigste Verbesserung:** Die Coverageentscheidung wird von langen zentralen Modultexten entkoppelt und als eigenständiger fachlicher Vertrag prüfbar.
- **WU-Quellenbasis:** IBBW „Wirksamer Unterricht“, Band 1 als Grundrahmen, Band 6 für Aufgabenqualität und Band 9 für lernfunktionale Digitalität; die lokalen Exzerpte sind Orientierungsrahmen und kein Wirksamkeitsnachweis für die konkrete Umsetzung.

## 12. Vollständige Ausgangsklassifikation

### 12.1 `module-detail` – 39 Records

- `BMB16-GYM-IK-GM-001`
- `BMB16-GYM-IK-GM-003`
- `BMB16-GYM-IK-MG-002`
- `BMB16-GYM-IK-PP-002`
- `BMB16-GYM-PK-RK-004`
- `INF7-16-GYM-IK-ALG-003`
- `INF7-16-GYM-IK-DC-001`
- `INF7-16-GYM-IK-DC-004`
- `INF7-16-GYM-IK-DC-005`
- `INF7-16-GYM-IK-IGD-004`
- `INF7-16-GYM-IK-IGD-006`
- `INF7-16-GYM-PK-AB-002`
- `INF7-16-GYM-PK-AB-005`
- `INF7-16-GYM-PK-AB-006`
- `INF7-16-GYM-PK-KK-002`
- `INF7-16-GYM-PK-KK-006`
- `INF7-16-GYM-PK-MI-003`
- `INF7-16-GYM-PK-MI-005`
- `INF7-16-GYM-PK-SV-002`
- `INF7-16-GYM-PK-SV-003`
- `LH26-E-ALG-001`
- `LH26-E-ALG-007`
- `LH26-E-ALG-008`
- `LH26-E-ALG-009`
- `LH26-E-DA-004`
- `LH26-E-DA-005`
- `LH26-E-DA-006`
- `LH26-E-DA-008`
- `LH26-E-DA-009`
- `LH26-E-DA-010`
- `LH26-E-DA-012`
- `LH26-E-DP-004`
- `LH26-E-DP-006`
- `LH26-E-ID-009`
- `LH26-E-ID-020`
- `LH26-E-ID-021`
- `LH26-E-KS-002`
- `LH26-E-KS-014`
- `LH26-E-KS-015`

### 12.2 `school-context` – 9 Records

- `BMB16-GYM-IK-GM-002`
- `BMB16-GYM-IK-KK-002`
- `BMB16-GYM-IK-KK-003`
- `BMB16-GYM-PK-HK-003`
- `BMB16-GYM-PK-SK-003`
- `INF7-16-GYM-PK-SV-001`
- `LH26-E-DA-015`
- `LH26-E-DP-001`
- `LH26-E-KS-001`

### 12.3 `private-local` – 8 Records

- `BMB16-GYM-IK-MG-001`
- `BMB16-GYM-IK-MG-003`
- `BMB16-GYM-PK-RK-001`
- `BMB16-GYM-PK-RK-002`
- `BMB16-GYM-PK-RK-003`
- `LH26-E-DP-003`
- `LH26-E-DP-013`
- `LH26-E-DP-014`

### 12.4 `roadmap-level` – 4 Records

- `LH26-E-PROG-001`
- `LH26-E-PROG-002`
- `LH26-E-PROG-003`
- `LH26-E-PROG-004`

## 13. Abnahmekriterien

IUM09 ist erst abnahmefähig, wenn:

- alle 60 Ausgangsrecords genau einmal im Ledger stehen;
- die Klassifikation 39/9/8/4 maschinell bestätigt ist;
- jeder Statuswechsel quellen-, operator-, lernhandlungs- und produktgenau begründet ist;
- jeder geschlossene Record einen gültigen Evidenzvertrag besitzt;
- jeder verbleibende `partial`-Record Grund, Risiko und Folgeaktion besitzt;
- die vier Roadmap-Progressionsrecords bis IUM10 sichtbar `partial` bleiben;
- private Reflexion weder erhoben noch gespeichert oder bewertet wird;
- Modulgraph und Zeitkorridore unverändert bleiben;
- Zeit- und Verdichtungsfolgen vollständig an IUM10 übergeben sind;
- Unit-Tests, Validator, Diff- und Encoding-Gates grün sind;
- Fach- und Engineeringreview bestanden sind;
- der Nutzer die verbleibenden Lücken gesondert prüfen kann.

## 14. Nicht Bestandteil von IUM09

- Überarbeitung der Jahreszeitkorridore;
- neue Module, Modulteilungen oder neue Abhängigkeiten;
- Fertigstellung einzelner Lernmodule;
- Plattform-, PWA-, Hosting- oder Speicherimplementierung;
- personenbezogene Diagnostik oder Bewertung;
- Niveaudifferenzierung;
- Klassen 8–11;
- eine Vollabdeckungs-, Jahreszeit- oder Implementierungsfreigabe;
- Phase-1-Planung.

## 15. Nächster Freigabeschritt

Nach schriftlicher Nutzerfreigabe dieser Spezifikation wird ein testgetriebener Implementierungsplan erstellt. Erst danach beginnen Änderungen an Validator, Tests, Coverageplan und Modulkandidaten.
