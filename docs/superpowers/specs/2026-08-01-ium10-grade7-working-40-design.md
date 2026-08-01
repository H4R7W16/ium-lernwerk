# IUM10 – Klasse 7 als bedingt verfügbares 40-UE-Arbeitsziel

**Status:** Gesamtdesign freigegeben; schriftliches Spezifikationsreview ausstehend

**Stand:** 1. August 2026

**Scope:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klasse 7, Niveau E

**Voraussetzung:** IUM10 für die Klassen 5 und 6 ist als `working` freigegeben

**Implementierungsgrenze:** Diese Spezifikation entwirft den Klasse-7-Kapazitätsentscheid. Sie implementiert weder das Datenmodell noch Lernmodule, Pilotierungen oder Phase 1.

## 1. Zweck

IUM10 weist für Klasse 7 bisher drei vollständige, aber nicht verfügbare Bedarfsszenarien mit 40, 46 und 54 Unterrichtseinheiten aus. Diese Spezifikation macht die optimierte 40-UE-Untergrenze zu einem expliziten Arbeitsziel, ohne sie vor ihrer Erprobung als verfügbares oder zeitlich grünes Lehrwerksangebot auszugeben.

Das Ziel ist ein prüfbarer Jahrespfad, der:

- alle zehn Klasse-7-Kernmodule erhält;
- die notwendigen fachlichen Lernhandlungen, Produkte und Curriculumnachweise bewahrt;
- vier tragende Integrationen transparent macht;
- bei gebrochener Integration fail-closed auf einen höheren Zeitbedarf zurückfällt;
- ausschließlich nichtpersonale Pilotnachweise verwendet;
- flexible Vertiefungs-, Transfer- und Projektmodule als zusätzliches Angebot erhält;
- 38 UE nur als nichtnormative Vergleichsgrenze, nicht als verkürzten Klasse-7-Pfad behandelt.

## 2. Ausgangslage und Entscheid

### 2.1 Bestehendes IUM10-Modell

Das bestehende Schema 2 enthält:

- 31 Modulzeitverträge;
- acht Integrationsverträge;
- elf Jahresvarianten;
- 60 Zeitreviews;
- vier Sequenznachweise;
- fünf Risiken;
- 31 modulaggregierte Pilotaufträge.

Für Klasse 7 gelten derzeit:

| Szenario | Umfang | Verfügbarkeit | Funktion |
|---|---:|---|---|
| `GRADE-7-OPTIMIZED-DEMAND` | 40 UE | nicht verfügbar | optimierte Untergrenze |
| `GRADE-7-ROBUST-DEMAND` | 46 UE | nicht verfügbar | robustere Bedarfsrechnung |
| `GRADE-7-HISTORICAL-MINIMUM` | 54 UE | nicht verfügbar | historische Vergleichsgrenze ohne Clusteranrechnung |

Das Jahrgangsurteil ist `partial / red / partial / not-started` für semantische Coverage, Zeitmachbarkeit, Sequenznachweis und Pilotstatus.

### 2.2 Freigegebene Entscheidung

`GRADE-7-OPTIMIZED-DEMAND` wird durch `GRADE-7-WORKING-40` ersetzt. Der neue Pfad ist ein vollständiges, aber zunächst nur bedingt verfügbares Arbeitsziel.

Sein Ausgangszustand lautet:

| Achse | Ausgangswert | Bedeutung |
|---|---|---|
| Vertragsreife | `working` | als Entwicklungsgrundlage freigegeben, nicht abschließend geprüft |
| Verfügbarkeit | `conditional` | nur bei Erfüllung des eigenen Verfügbarkeitsvertrags nutzbar |
| Zeiturteil | `amber` | rechnerisch plausibel, praktisch noch nicht als Gesamtpfad bestätigt |
| Sequenznachweis | `covered` | Reihenfolge und Übergaben sind fachlich spezifiziert |
| Pilotstatus | `not-started` | weder Cluster- noch Gesamtpilot abgeschlossen |
| semantische Coverage | `partial` | die roadmapabhängigen Klasse-7-Nachweise dürfen ohne verfügbaren Pfad noch nicht geschlossen werden |

`working` ist kein Synonym für `available`, `green`, `completed`, `reviewed` oder eine Freigabe als Standard.

### 2.3 Verworfene Alternativen

Ein 38-UE-Pfad durch weitere Kompression wird nicht angelegt. Zwei zusätzliche Einheiten dürfen nicht durch stille Streichung, Hausaufgabenverlagerung, unbeaufsichtigte Selbstlernzeit oder flexible Module kompensiert werden.

46 UE wird nicht zum primären Ziel, weil der bereits fachlich entworfene 40-UE-Pfad zunächst gezielt auf seine tragenden Integrationen geprüft werden soll. Das 46-UE-Modell bleibt als robuste Referenz sichtbar.

54 UE bleibt die historische Vergleichsgrenze für eine Durchführung ohne Clusteranrechnung. Es ist weder Empfehlung noch automatisch anzusetzendes Jahresangebot.

## 3. Verbindliche 40-UE-Sequenz

### 3.1 Jahresfolge

| Reihenfolge | Cluster | Module | Modulbudgets | Clusterbudget |
|---:|---|---|---|---:|
| 1 | Daten und Codierung | `IUM-7-CORE-01`, `IUM-7-CORE-02` | 5 + 3 | 8 UE |
| 2 | Programmieren | `IUM-7-CORE-03`, `IUM-7-CORE-04` | 5 + 6 | 11 UE |
| 3 | Netze und Sicherheit | `IUM-7-CORE-05`, `IUM-7-CORE-06`, `IUM-7-CORE-07` | 4 + 3 + 4 | 11 UE |
| 4 | Daten, Medien und Gesellschaft | `IUM-7-CORE-08`, `IUM-7-CORE-09`, `IUM-7-CORE-10` | 4 + 2 + 4 | 10 UE |
|  | **Gesamt** | **zehn Kernmodule** |  | **40 UE** |

Die Reihenfolge ist Bestandteil des Vertrags. Eine bloße Summengleichheit bei anderer Orchestrierung genügt nicht, weil die Zeitannahmen von konkreten Übergaben abhängen.

### 3.2 Enthaltene Lernzeit

Die 40 UE enthalten bereits die modulbezogen notwendigen Anteile für:

- Orientierung und Zielklarheit;
- Aktivierung relevanten Vorwissens;
- Begriffs-, Modell- und Verfahrensaufbau;
- angeleitete Übung;
- eigenständige fachliche Handlung und Produktarbeit;
- Rückmeldung oder Selbstkontrolle;
- Überarbeitung;
- Sicherung;
- Transfer oder aktiven Abruf.

Die 40 UE enthalten keinen zusätzlichen Jahres- oder Kalenderpuffer. Lokale Ausfälle, Vertretungsstunden, Wandertage und vergleichbare schulorganisatorische Verluste werden nicht durch fachliche Kürzungen absorbiert.

## 4. Die vier tragenden Integrationen

### 4.1 `INT-7-DATA-CODING`

**Module:** `IUM-7-CORE-01` und `IUM-7-CORE-02`

**Übergabeprodukt:** geprüfte Bit-, Code- und Datenmengenspur vom Bit-Codebuch zum Pixelraster, Bildcodec und Ressourcenvergleich.

Erhalten bleiben insbesondere:

- Binärdarstellung, ASCII-Codierung und Decodierung;
- Entwurf und Prüfung einer eindeutigen, umkehrbaren Vorschrift;
- Diskretisierung eines Bildes;
- Pixelcodierung und Decodiertest;
- Datenmengenvergleich und begründetes Ressourcenurteil.

Scheitert die gemeinsame Spur, steigt der 40-UE-Bedarf um 3 UE.

### 4.2 `INT-7-PROGRAMMING`

**Module:** `IUM-7-CORE-03` und `IUM-7-CORE-04`

**Übergabeprodukt:** gemeinsames Code-, Ablauf-, Zustands- und Testartefakt vom synchronen Trace bis zu Implementierung, Test und hypothesengeleitetem Debugging.

Erhalten bleiben insbesondere:

- Modellierung von Kontrollfluss, Werten und Zuständen;
- Ausführung und Korrektur eines vollständigen Traces;
- Implementierung desselben fachlichen Falls;
- Normal-, Grenz- und Gegenfälle;
- Debugginghypothese, Reparatur und Begründung.

Scheitert die gemeinsame Spur, steigt der 40-UE-Bedarf um 2 UE.

### 4.3 `INT-7-NET-SECURITY`

**Module:** `IUM-7-CORE-05`, `IUM-7-CORE-06` und `IUM-7-CORE-07`

**Übergabeprodukt:** durchgängiges System-, Bedrohungs-, Verschlüsselungs- und Angriffsmodell mit Datenweg, Schutzbedarf, Schlüsselmodell, Angriffsbefund und revidiertem Sicherheitsurteil.

Erhalten bleiben insbesondere:

- Netz- und Client-Server-Modellierung;
- Speicherort, Bedrohung und Schutzentscheidung;
- Trennung von Codierung und Verschlüsselung;
- Vergleich von Transport- und Ende-zu-Ende-Schutz;
- Ausführung von Caesar- und monoalphabetischer Substitution;
- Brute Force, Häufigkeitsanalyse, Hypothese, Befund und begrenztes Sicherheitsurteil.

Scheitert das gemeinsame Modell, steigt der 40-UE-Bedarf um 3 UE.

### 4.4 `INT-7-DATA-MEDIA-SOCIETY`

**Module:** `IUM-7-CORE-08`, `IUM-7-CORE-09` und `IUM-7-CORE-10`

**Übergabeprodukt:** gemeinsames kuratiertes Evidenz-, Mechanismus- und Medienrevisionsdossier mit Akteurskarte, Beleg und Gegenbeleg, Wirkungs- und Rechteprüfung sowie unterscheidbaren Produktspuren.

Erhalten bleiben insbesondere:

- Analyse von Akteuren und Interessen;
- Prüfung von Behauptung, Primärbeleg und Gegenbeleg;
- Daten- und Rechtsfolgen sowie revidierter Standpunkt;
- Trennung psychologischer, sozialer und ökonomischer Gamingmechanismen;
- Prüfung einer Redesign-Alternative;
- Bearbeitung eines Medienbildes;
- Rechteprüfung, Gegenperspektive, Feedback und Revision.

Private Reflexionen bleiben privat. Sie werden weder erhoben noch bewertet oder als Ersatz für die fachliche Mechanismuskarte verwendet.

Scheitert das gemeinsame Dossier, steigt der 40-UE-Bedarf um 6 UE.

### 4.5 Allgemeine Übergaberegeln

Jeder Cluster benötigt ein überprüfbares fachliches Transferprodukt. Dasselbe Thema, Fallbeispiel oder digitale Werkzeug allein begründet keine Integration.

Ein Übergabeprodukt muss:

- die fachliche Vorleistung des früheren Moduls tatsächlich enthalten;
- im Folgemodul funktional weiterverwendet werden;
- die unterschiedlichen Modulhandlungen und Curriculumnachweise erkennbar lassen;
- lokal oder nichtpersonal einsetzbar sein;
- ohne persönliches Profil, zentrale Diagnostik oder Telemetrie auskommen.

Vorwissen wird im jeweiligen Modul reaktiviert. Der Jahrespfad darf nicht davon abhängen, dass persönliche Lernprodukte zentral gespeichert oder über das Schuljahr hinweg personenbezogen verfolgt werden.

## 5. Verfügbarkeit und Zustandsmodell

### 5.1 Getrennte Statusachsen

Das Modell führt mindestens folgende voneinander unabhängige Achsen:

- `status`: Vertragsreife mit `working` oder `reviewed`;
- `availabilityStatus`: `conditional`, `available` oder `unavailable`;
- `timeFeasibilityStatus`: `green`, `amber` oder `red`;
- `sequenceEvidenceStatus`: `covered` oder `partial`;
- `pilotStatus`: `not-started`, `in-progress` oder `completed`;
- `semanticCoverageStatus`: `covered` oder `partial`.

Kein Einzelstatus darf einen anderen implizit überschreiben.

### 5.2 Verfügbarkeitsgates für `GRADE-7-WORKING-40`

Der Pfad darf nur dann von `conditional` zu `available` und von `amber` zu `green` wechseln, wenn alle folgenden Gates bestanden sind:

1. **Kapazitätsgate:** 40 Unterrichtseinheiten à 45 Minuten sind real im schulischen Angebot einplanbar. Erforderliche Lernzeit wird nicht in Hausaufgaben oder private Lernzeit verschoben.
2. **Integrationsgate:** Alle vier Cluster besitzen ihr vollständiges Übergabeprodukt und bewahren die getrennten fachlichen Lernhandlungen.
3. **Technikgate:** Die notwendigen Werkzeuge funktionieren im schulischen Zielsystem. Der Pflichtpfad benötigt weder persönliche Konten noch eine zentrale Speicherung von Lernendendaten; kritische Schritte besitzen eine lokale, datenschutzkonforme Rückfallebene.
4. **Privacy-Gate:** Pilot- und Verfügbarkeitsnachweise enthalten keine personenbezogenen Lernverlaufsdaten, Profile, Inhalte privater Reflexionen oder persönliche Telemetrie.
5. **Pilotgate:** Alle vier Cluster und danach der vollständige 40-UE-Jahrespfad wurden gemäß den nichtpersonalen Pilotverträgen erprobt.

### 5.3 Zustandsübergänge

| Bedingung | Verfügbarkeit | Zeit | Sequenz | Pilot |
|---|---|---|---|---|
| Designspezifikation umgesetzt, noch kein Pilot | `conditional` | `amber` | `covered` | `not-started` |
| Pilot begonnen, mindestens ein Gate noch offen | `conditional` | `amber` | `covered` | `in-progress` |
| alle Clusterpiloten bestanden, Gesamtpilot offen | `conditional` | `amber` | `covered` | `in-progress` |
| Gesamtpilot und alle Gates bestanden | `available` | `green` | `covered` | `completed` |
| notwendiges Gate gescheitert | `unavailable` | `red` | Ergebnis bleibt separat | tatsächlicher Pilotstand |

Nach bestandenem Gesamtpilot darf die semantische Coverage nur dann von `partial` zu `covered` wechseln, wenn zusätzlich:

- die betroffenen Sequenznachweise den verfügbaren Jahrespfad referenzieren;
- der Coveragevalidator den Statuswechsel trägt;
- ein eigenständiger Fachaudit den Nachweis bestätigt;
- keine private oder personenbezogene Evidenz verwendet wird.

`reviewed` entsteht nicht automatisch. Die Hochstufung benötigt getrenntes Fach- und Engineeringreview sowie ein erneutes Auftraggebergate.

### 5.4 Klassen 5 und 6

Die bereits als `working` freigegebenen Zeitmodelle der Klassen 5 und 6 werden inhaltlich nicht neu entschieden. Ihre bisherigen Wahrheitswerte zur Verfügbarkeit werden lediglich in das neue Feld `availabilityStatus` übertragen. Pilotstatus und Vertragsreife bleiben davon getrennt.

Der strengere Verfügbarkeitsvertrag dieser Spezifikation gilt für den neu eingeführten Klasse-7-Arbeitspfad. Er führt keine rückwirkende Neubewertung der Klassen 5 und 6 ein.

## 6. Fail-closed-Rückfallmodell

### 6.1 Additive Berechnung

Für den 40-UE-Pfad gilt:

```text
fallbackUnits = 40 + Summe der Zuschläge aller gescheiterten Cluster
```

| Cluster | Zuschlag |
|---|---:|
| Daten und Codierung | +3 UE |
| Programmieren | +2 UE |
| Netze und Sicherheit | +3 UE |
| Daten, Medien und Gesellschaft | +6 UE |

Die Zuschläge sind additiv. Dadurch entstehen je nach Befund auch Zwischenwerte wie 42, 43, 45, 46, 48 oder 51 UE. Es werden dafür nicht automatisch neue angebotene Jahresvarianten angelegt.

Scheitern alle vier Cluster, ergibt sich die historische Obergrenze von 54 UE.

### 6.2 Rolle der 46- und 54-UE-Modelle

`GRADE-7-ROBUST-DEMAND` mit 46 UE bleibt eine robuste Referenzrechnung. Sie ist nicht gleichbedeutend mit jedem denkbaren einzelnen oder kombinierten Clusterfehler.

`GRADE-7-HISTORICAL-MINIMUM` mit 54 UE bleibt die nachvollziehbare Vergleichsrechnung ohne Clusteranrechnung.

Beide bleiben zunächst `unavailable`. Ein berechneter Rückfallbedarf ist eine Kapazitätswarnung, kein automatisch freigegebenes Angebot.

### 6.3 Verbotene Kompensationen

Ein Zeitdefizit darf nicht kompensiert werden durch:

- stille Streichung eines Kernmoduls oder einer erforderlichen Lernhandlung;
- bloße Erwähnung statt Ausführung eines Operators;
- Demonstration statt eigenständiger Anwendung;
- Verlagerung von Übung, Feedback, Revision, Sicherung oder Transfer in Hausaufgaben;
- Nutzung unbeaufsichtigter digitaler Selbstlernzeit als garantierte Unterrichtszeit;
- Nutzung privater Reflexionen als Pilot-, Diagnose- oder Bewertungsdaten;
- Ersatz eines Kernmoduls durch ein flexibles Modul;
- Umdeklaration des 38-UE-Vergleichsrahmens zum Klasse-7-Pfad.

## 7. Flexible Module

Flexible Vertiefungs-, Transfer- und Projektmodule bleiben ausdrücklich Bestandteil des Lernwerk-Kosmos. Sie werden nicht gestrichen oder abgewertet.

Für `GRADE-7-WORKING-40` gilt jedoch:

- Sie sind nicht in den 40 UE enthalten.
- Sie sind keine Voraussetzung der Kernabdeckung.
- Sie dürfen keine gescheiterte Kernintegration kompensieren.
- Sie können bei zusätzlicher lokaler Zeit als Vertiefung, Transfer oder Projekt angeboten werden.
- Ihr Einsatz benötigt eine eigene transparente Zeitangabe.

Damit bleibt die modulare Erweiterbarkeit erhalten, ohne eine zweite Zwangsstruktur oder verdeckte Pflichtzeit zu erzeugen.

## 8. Nichtpersonale Pilotarchitektur

### 8.1 Pilotstufen

Die Pilotierung erfolgt in zwei Stufen:

1. vier getrennte Clusterpiloten;
2. ein vollständiger End-to-End-Pilot der 40-UE-Sequenz.

Ein End-to-End-Pilot darf die Clusterprüfung nicht durch eine bloße Jahressumme ersetzen.

### 8.2 Zulässige Pilotdaten

Gespeichert werden ausschließlich Angaben auf Modul-, Cluster- oder Pfadebene:

- geplante Unterrichtseinheiten;
- tatsächlich benötigte Unterrichtseinheiten;
- Vorliegen des vereinbarten Übergabeprodukts;
- Aktivierung einer Rückfallebene;
- aggregierter technischer Start- und Unterstützungsaufwand;
- Durchführung der vorgesehenen Übungs-, Rückmelde-, Überarbeitungs-, Sicherungs- und Transferphasen;
- nichtpersonaler Befund, ob ein Gate bestanden wurde.

### 8.3 Ausgeschlossene Daten und Nutzungen

Nicht erhoben oder zentral gespeichert werden:

- Namen, Kennungen oder Kontodaten von Lernenden;
- individuelle Lernverläufe oder Kompetenzprofile;
- personenbezogene Zeit-, Fehler- oder Unterstützungsdaten;
- Inhalte privater Reflexionen;
- persönliche Telemetrie oder Interaktionsprotokolle;
- Schülerprodukte als Beleg der zeitlichen Machbarkeit;
- automatische personenbezogene Bewertung oder Diagnose.

Lehrkräfte dürfen die für Unterricht üblichen unmittelbaren Beobachtungen nutzen. Diese Spezifikation erzeugt daraus jedoch keine neue zentrale Datensammlung oder technische Diagnostik.

### 8.4 Fehlerbehandlung

Ein nicht auswertbarer oder datenschutzwidriger Pilotnachweis gilt nicht als bestanden. Fehlende Evidenz erzeugt keinen positiven Status.

Wenn eine technische Rückfallebene mehr Zeit benötigt, wird diese Zeit sichtbar dokumentiert. Das Modell darf keine idealisierte Technikzeit als tatsächliche Unterrichtskapazität ausgeben.

## 9. Schema 3

### 9.1 Kanonisches Artefakt

`roadmap/time-model.json` bleibt die einzige kanonische Quelle für Zeitverträge, Jahresvarianten, Status, Risiken und Pilotaufträge.

Die `schemaVersion` wird wegen der veränderten Verfügbarkeits- und Pilotrepräsentation von 2 auf 3 erhöht.

### 9.2 Jahresvarianten

Das boolesche Feld `available` wird durch das explizite Feld `availabilityStatus` ersetzt:

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

Die vorhandenen Modulallokationen und vier Integrations-IDs werden vollständig übernommen. Das Beispiel kürzt diese Listen nur zur Lesbarkeit.

Zulässige Verfügbarkeitswerte sind exakt:

- `conditional`;
- `available`;
- `unavailable`.

### 9.3 Verfügbarkeitsvertrag

Schema 3 ergänzt einen jahrgangspfadbezogenen Verfügbarkeitsvertrag mit mindestens:

- eindeutiger ID;
- Jahresvarianten-ID;
- erforderlicher Kapazität von 40 UE;
- nichtnormativer Vergleichsgrenze von 38 UE;
- den fünf verpflichtenden Gates;
- den vier Cluster-IDs;
- den vier additiven Rückfallzuschlägen;
- maximalem Rückfallbedarf von 54 UE;
- verbotenen Kompensationen;
- Fail-closed-Regel;
- Status und Risiko.

Die Vergleichsgrenze von 38 UE wird nicht als `annualVariant` modelliert.

### 9.4 Pilotaufträge

Die bisher nur modulbezogene Struktur `pilotAssignments` wird in Schema 3 typisiert. Zulässige Scopes sind:

- `module`;
- `integration`;
- `annual-variant`.

Die bestehenden 31 Modulaufträge bleiben erhalten und werden ohne Verlust ihrer Privacy-Verträge migriert. Hinzu kommen:

- ein Pilotauftrag je Klasse-7-Integration;
- ein Pilotauftrag für `GRADE-7-WORKING-40`.

Jeder Auftrag nennt Scope, Bezugsverträge, Aggregationsebene, zulässige Messgrößen, ausgeschlossene Nutzungen, Privacy-Status, Pilotstatus und Rückfallebene.

### 9.5 Jahrgangsurteil

Das Klasse-7-Jahrgangsurteil referenziert:

- `GRADE-7-WORKING-40`;
- `GRADE-7-ROBUST-DEMAND`;
- `GRADE-7-HISTORICAL-MINIMUM`.

Es ergänzt `availabilityStatus` als eigene Achse und startet mit:

```text
semanticCoverageStatus: partial
availabilityStatus: conditional
timeFeasibilityStatus: amber
sequenceEvidenceStatus: covered
pilotStatus: not-started
```

## 10. Menschlich lesbare Publikation

Aus dem kanonischen Modell werden synchron aktualisiert:

- `roadmap/module-roadmap.md`;
- `README.md`;
- Risikodarstellung;
- Pilotdarstellung;
- Klasse-7-Sequenz- und Coverageerläuterung.

Die Publikation muss klar unterscheiden zwischen:

- freigegebenem Arbeitsziel;
- bedingter Verfügbarkeit;
- rechnerischem Zeiturteil;
- Pilotstand;
- robustem Bedarf;
- historischer Vergleichsgrenze.

Unzulässig sind Formulierungen wie „Klasse 7 ist verfügbar“, „40 UE sind erprobt“ oder „vollständige Abdeckung ist erreicht“, solange die zugehörigen Gates nicht bestanden sind.

## 11. Validatorarchitektur

`scripts/validate_ium10.py` bleibt der autoritative IUM10-Validator. Er wird für Schema 3 erweitert und prüft fail-closed.

### 11.1 Strukturinvarianten

Der Validator prüft mindestens:

1. `schemaVersion` ist exakt 3.
2. Es gibt genau eine Variante `GRADE-7-WORKING-40`.
3. Der alte Bezeichner `GRADE-7-OPTIMIZED-DEMAND` kommt nicht mehr als Jahresvariante vor.
4. Der Pfad enthält genau zehn Klasse-7-Kernmodule.
5. Jedes Kernmodul kommt genau einmal vor.
6. Die Modulbudgets ergeben exakt 40 UE.
7. Die Clusterbudgets ergeben exakt `8 + 11 + 11 + 10`.
8. Die Modul- und Clusterreihenfolge ist verbindlich abgebildet.
9. Genau die vier freigegebenen Integrationsverträge tragen den Pfad.
10. 46 und 54 UE bleiben als nicht verfügbare Referenzszenarien erhalten.
11. 38 UE erscheint nicht als Klasse-7-Jahresvariante.

### 11.2 Statusinvarianten

Der Validator prüft mindestens:

1. Der initiale 40-UE-Pfad ist `working`, `conditional` und `amber`.
2. Sequenzstatus und Pilotstatus sind davon getrennt.
3. `available/green` ist nur bei fünf bestandenen Gates und abgeschlossenem Gesamtpilot zulässig.
4. `reviewed` ist ohne dokumentierte Review- und Auftraggeberfreigabe unzulässig.
5. Gescheiterte notwendige Gates führen zu `unavailable/red`.
6. Ein Coveragewechsel zu `covered` benötigt verfügbaren Pfad, bestandenen Sequenznachweis und positiven Fachaudit.

### 11.3 Zeit- und Rückfallinvarianten

Der Validator prüft mindestens:

1. Die Zuschläge lauten exakt `3 / 2 / 3 / 6` UE.
2. Mehrere Zuschläge werden addiert, nicht überschrieben oder gedeckelt.
3. Der maximale Rückfall ergibt exakt 54 UE.
4. 46 UE bleibt Referenz und wird nicht fälschlich als universeller Rückfall jedes Fehlers behandelt.
5. Ein berechneter Rückfallbedarf erzeugt keine automatische verfügbare Jahresvariante.

### 11.4 Privacy- und Scopeinvarianten

Der Validator prüft mindestens:

1. Pilotdaten bleiben modul-, cluster- oder pfadaggregiert.
2. Persönliche Daten und persönliche Telemetrie sind ausgeschlossen.
3. Private Reflexionen werden weder beobachtet noch bewertet oder als Evidenz genutzt.
4. Flexible Module stehen nicht in den 40-UE-Allokationen.
5. Flexible Module werden nicht als Voraussetzung oder Rückfallkompensation verwendet.
6. Klassen 5 und 6 behalten ihre freigegebenen Zeit- und Inhaltsverträge.

### 11.5 Dokumentationssynchronität

README, Modulroadmap und maschinenlesbares Modell müssen dieselben Werte und Status ausweisen. Der Validator erkennt insbesondere:

- veraltete 40/46/54-Texte;
- falsche Verfügbarkeitsaussagen;
- fehlende Nichtnormativität der 38-UE-Grenze;
- fehlende flexible Erweiterungsmodule;
- widersprüchliche Pilot- oder Coverageaussagen.

## 12. Teststrategie

### 12.1 Positive Tests

Die Tests belegen mindestens:

- gültige Migration auf Schema 3;
- exakte 40-UE-Sequenz;
- vollständige Cluster- und Übergabeverträge;
- korrekten Initialstatus;
- korrekte additive Rückfallberechnung;
- Erhalt der Klassen 5 und 6;
- Erhalt der 31 Modul-Pilotaufträge plus fünf neuen Pilotaufträgen;
- Synchronität von JSON, README und Modulroadmap.

### 12.2 Mutationstests

Mindestens folgende Mutationen müssen scheitern:

- Kernmodul fehlt oder ist doppelt;
- Cluster- oder Modulreihenfolge verändert;
- Summe ist nicht 40 UE;
- Übergabeprodukt fehlt;
- fachliche Lernhandlung wird aus einem Integrationsvertrag entfernt;
- falscher oder nichtadditiver Rückfallzuschlag;
- `available` ohne bestandene Gates;
- `green` ohne Gesamtpilot;
- `covered` ohne verfügbaren Pfad oder Fachaudit;
- 38 UE wird als Klasse-7-Pfad angelegt;
- flexibles Modul ersetzt Kernzeit;
- persönliche Daten oder Telemetrie werden als Pilotmaß genannt;
- private Reflexion wird beobachtbar oder bewertbar gemacht;
- Klasse 5 oder 6 wird unbeabsichtigt inhaltlich verändert;
- README oder Modulroadmap behaupten einen weitergehenden Status als das JSON-Modell.

### 12.3 Repositorygates

Vor einer Implementierungsabnahme müssen frisch bestanden sein:

- vollständige Python-Testsuite;
- IUM10-Validator;
- IUM09-Validator;
- Phase-0-Validator;
- JSON- und UTF-8-Prüfung;
- Baseline- und Dokumentationsgates.

## 13. Fachliche und technische Reviews

Nach der Umsetzung erfolgen zwei voneinander unabhängige Reviews.

### 13.1 Fachreview

Das Fachreview prüft:

- Erhalt aller curricularen Anforderungen;
- Operator- und Produkttiefe;
- tatsächliche Kontinuität der vier Übergabeprodukte;
- Übungs-, Feedback-, Revisions-, Sicherungs- und Transferzeit;
- fachliche Angemessenheit der Rückfalllogik;
- Grenzen der Coverageaussage;
- didaktische Funktion digitaler und gegebenenfalls analoger Medien.

### 13.2 Engineeringreview

Das Engineeringreview prüft:

- Schema-3-Konsistenz;
- fail-closed Statusübergänge;
- additive Rückfallberechnung;
- Privacy-Invarianten;
- Baselineerhalt;
- Validator- und Testabdeckung;
- Synchronität der öffentlichen Dokumentation.

Ein Review darf fehlende Pilotdaten nicht durch Plausibilitätsannahmen ersetzen.

## 14. Unterrichtsqualitative Begründung

Das Design folgt den bereits freigegebenen IuM-Fachprofil- und WU-Grundsätzen:

- **Kognitive Aktivierung:** Modellieren, codieren, testen, angreifen, prüfen, beurteilen und revidieren bleiben ausgeführte Lernhandlungen.
- **Konstruktive Unterstützung:** Aktivierung, angeleitete Übung und technische Unterstützung werden nicht aus der Unterrichtszeit herausgerechnet.
- **Klarheit und Struktur:** Vier fachlich begründete Cluster machen die Jahresfolge nachvollziehbar.
- **Aufgabenqualität:** Zeitgewinne entstehen nur durch ein tatsächlich weiterverwendetes fachliches Produkt.
- **Feedback und Revision:** Rückmeldung ohne anschließende Weiterarbeit gilt nicht als vollständige Lernfunktion.
- **Transfer:** Jeder Cluster endet in einem überprüfbaren Übergabe- oder Transferprodukt.
- **Datensparsamkeit:** Unterrichtsverbesserung beruht auf aggregierten Prozessdaten, nicht auf personenbezogenen Profilen.
- **Medienwahl:** Digitale Werkzeuge sind selbstverständliches Unterrichtsmedium, benötigen aber eine fachliche Funktion und eine schulisch tragfähige Rückfallebene. Analoge Phasen bleiben möglich, wenn ihre Lernfunktion dies begründet.

## 15. Abgrenzung

Diese Spezifikation umfasst ausschließlich den Klasse-7-Kapazitätsentscheid und die dafür nötige Weiterentwicklung des IUM10-Zeitmodells.

Nicht enthalten sind:

- Entwicklung der zehn Lernmodule;
- Umsetzung einer Lernendenanwendung;
- Lehrkräftehandbuch oder konkrete Unterrichtsmaterialien;
- Durchführung oder Auswertung realer Pilotierungen;
- personenbezogene Diagnostik;
- Lernprofile oder Telemetrie;
- neue curriculare Priorisierung;
- Streichung oder Reklassifikation von Kernmodulen;
- Planung von Phase 1;
- Veröffentlichung des 40-UE-Pfads als erprobter Standard.

## 16. Akzeptanzkriterien der späteren Implementierung

- [ ] `roadmap/time-model.json` verwendet Schema 3.
- [ ] `GRADE-7-WORKING-40` ersetzt den bisherigen optimierten Bedarfsbezeichner.
- [ ] Alle zehn Kernmodule stehen in der freigegebenen Reihenfolge und ergeben 40 UE.
- [ ] Alle vier Clusterverträge bewahren ihre Lernhandlungen, Produkte und Curriculumnachweise.
- [ ] Der Ausgangszustand ist `working / conditional / amber / covered / not-started / partial` auf den getrennten Statusachsen.
- [ ] Die fünf Verfügbarkeitsgates sind maschinenlesbar und fail-closed.
- [ ] Die Zuschläge `+3 / +2 / +3 / +6` sind additiv und ergeben maximal 54 UE.
- [ ] 46 und 54 UE bleiben als nicht verfügbare Referenzmodelle erhalten.
- [ ] 38 UE ist nur eine nichtnormative Vergleichsgrenze und keine Jahresvariante.
- [ ] Flexible Vertiefungs-, Transfer- und Projektmodule bleiben sichtbar und zusätzlich.
- [ ] Die 31 Modul-Pilotaufträge bleiben erhalten; vier Cluster- und ein Gesamtpilotauftrag kommen hinzu.
- [ ] Pilotverträge schließen personenbezogene Daten, Telemetrie und private Reflexionsinhalte aus.
- [ ] Klassen 5 und 6 bleiben inhaltlich unverändert.
- [ ] JSON, README und Modulroadmap sind synchron.
- [ ] Positive Tests, Mutationstests und alle Repositorygates bestehen.
- [ ] Fachreview und Engineeringreview sind getrennt dokumentiert.
- [ ] Kein Status behauptet eine durchgeführte Pilotierung oder Standardfreigabe.

## 17. Freigabefolge

1. Das abschnittsweise Gesamtdesign wurde am 1. August 2026 freigegeben.
2. Diese schriftliche Spezifikation benötigt ein eigenes Nutzerreview.
3. Erst nach der ausdrücklichen schriftlichen Spezifikationsfreigabe wird mit `superpowers:writing-plans` ein testgetriebener Implementierungsplan erstellt.
4. Die Planfreigabe, Implementierung, Reviews, Pilotierung und spätere Statushochstufung bleiben jeweils eigene Gates.

Die Freigabe dieser Spezifikation erlaubt die Planung. Sie erlaubt weder die automatische Implementierung noch die Ausweisung von `GRADE-7-WORKING-40` als verfügbares oder erprobtes Lehrwerksangebot.
