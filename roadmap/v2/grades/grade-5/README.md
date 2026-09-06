# IUM-V2-R5 – Roadmap Klasse 5

Stand: 6. September 2026. **Zur fachlichen Nutzerabnahme bereit.** Diese neue Modul- und Jahresplanung ist ein Konzept für lehrkraftorchestrierten Unterricht am Gymnasium, Niveau E. Sie enthält geplante Lernhandlungen und Nachweise, keine fertigen Lernmodule oder Lernendentexte. Autor und Prüfer: Codex, KI-Dokumentenselbstreview.

- [Modulverträge, Zeitvarianten und Werkzeugmatrix](roadmap.json)
- [Vollständige Curriculumdisposition](curriculum-map.json)
- [Review, Gegenfälle und technische Prüfungen](validation-report.md)
- [Getrennte Reifeachsen und gebundene Prüfeingänge](status.json)
- [Ausdrückliche AUD-Nutzerabnahme](../../audits/acceptance.json)

## Grundlage und Geltung

Das [Kultusministerium](https://km.baden-wuerttemberg.de/de/schule/schulartuebergreifend/mint/schule-und-unterricht/informatik-und-medienbildung) führt die bestehenden Bildungspläne weiterhin als Grundlage; die [Lesehilfe 2026/2027](https://km.baden-wuerttemberg.de/fileadmin/redaktion/m-km/intern/PDF/Dateien/Schulart%C3%BCbergreifend/MINT/2026_Lesehilfe_IuM_Gym_und_Sek_I_bf.pdf) dient als Übergangsorientierung. Beide wurden am 6. September gelesen. Die Lesehilfe weist gemeinsame Inhalte für 5/6 aus und setzt für das Gymnasium Niveau E an. Die Aufteilung zwischen den beiden Jahrgängen ist hier eine Projektentscheidung. Eine neue Byteidentitätsprüfung oder inhaltliche Neuprüfung der vollständigen BMB-Remotefassung wird nicht behauptet; deren Rohrecords bleiben an die geprüfte Curriculumgrundlage gebunden.

Grundlage sind alle **59 BMB-Records** sowie **85 für Klasse 5/6 einschlägige Lesehilfe-Records**. Davon sind 85 Kompetenzen: 25 amtliche BMB-Kompetenzen und 60 orientierende Kompetenzen. Die weiteren 59 Records sind Beispiele, Operatoren und Progressionshinweise. Sie helfen bei der Auslegung und zählen weder als zusätzliche Kompetenzen noch als zusätzliche Unterrichtszeit.

| Disposition | Amtlich | Orientierung | Bedeutung |
| --- | ---: | ---: | --- |
| Für Klasse 5 geplant | 23 | 39 | Konkrete Zuordnung zu regulären Lernhandlungen und geplanten Produkten |
| Für R6 vorgesehen | 0 | 17 | Begründeter, noch nicht abgenommener Auftrag an die folgende Jahrgangsplanung |
| Eigenbezugsnachweis offen | 2 | 4 | Keine Erfüllungsbehauptung ohne tragfähige Curriculum-/Datenschutzentscheidung |

**Keine dieser Zahlen ist ein Abdeckungs- oder Lernerfolgsnachweis.** Alle Kompetenz-Coveragewerte bleiben `unassessed`. Das zentrale Anforderungsregister und die versiegelten CUR-/LXF-/GOV-/AUD-Snapshots werden nicht umgeschrieben. Die AUD-Abnahme am Commit `dc059cffcb2866c6e0d7df3c83dbc0410d14d680` wird additiv dokumentiert.

## Neuer Kernpfad

| Modul | Fachlicher Kern und geplanter Nachweis | Minuten / UE |
| --- | --- | ---: |
| M01 – Im schulischen Arbeitsraum sicher handeln | Gerät, Programm, Eingabe/Verarbeitung/Ausgabe und Speicherort unterscheiden; Zugang schützen und Arbeitsdatei wiederfinden | 180 / 4 |
| M02 – Informationen finden, prüfen und ordnen | Eingegrenzte Sachfrage recherchieren; Quellen anhand von Kriterien auswählen; strukturierte Informationssammlung begründen | 225 / 5 |
| M03 – Digital zusammenarbeiten und verständlich kommunizieren | Tatsächlichen schulischen Kommunikationsweg nutzen; individuelle Beiträge in eine gemeinsame Gliederung einarbeiten | 135 / 3 |
| M04 – Ein Medienprodukt gestalten, prüfen und vorstellen | Überschaubares Text-/Bildprodukt mit Präsentationsansicht, Quellenhinweisen und begründeter Revision erstellen | 315 / 7 |
| M05 – Medienwirkungen und Selbstdarstellung beurteilen | Neutrale Darstellungen vergleichen; Wirkungen und Folgen abschätzen und ein kriteriengestütztes Urteil formulieren | 180 / 4 |
| M06 – Präzise Abläufe entwickeln und prüfen | Anweisungen und feste Wiederholung grafisch und in Code darstellen; Spur erklären und Fehler gezielt korrigieren | 225 / 5 |
| **Kern gesamt** | **Sechs neue Lernbögen** | **1260 / 28** |

Die Folge entsteht aus Voraussetzungen: sicherer Arbeitsraum → begründete Information → gemeinsamer Entwurf → Produkt und Revision → Medienurteil. M06 benötigt die grundlegenden Bedienroutinen, aber nicht die gesamte Medienproduktionskette; der spätere Platz ist eine organisatorische Jahresentscheidung. Medienbildung hat den Schwerpunkt, einfache algorithmische Begriffe bilden einen ersten informatischen Zugang. Der Aufbaukurs Klasse 7 wird nicht vorgezogen.

M02/M03 liefern Grundlage und Planung für M04. M05 greift Gestaltungsentscheidungen aus M04 erneut auf. Jeder Lernbogen enthält Orientierung/Erklärung, angeleitete Übung, selbstständige Anwendung, nutzbare Rückmeldung und Sicherung/Transfer. Das sind budgetierte Funktionen, keine vorgeschriebene Seitenfolge. Die detaillierten Minutenanteile sind im Modulvertrag ausgewiesen.

Die vorhandene V1-Modulfolge und das frühere Zeitmodell wurden im Audit als `replace` bewertet. Die neuen Kennungen `V2-G5-M01` bis `M06` sind reine Planungskennungen und keine Produktionsregistrierung. Weder das alte IUM5-Modul noch LXP05 wird damit wieder aufgenommen.

## Jahresvarianten und Zeitgrenzen

Einheiten von 45 Minuten sind Rechengrößen; die Schule bestimmt den tatsächlichen Takt und das verfügbare Kontingent. Die Budgets sind **ungeprüfte Projektannahmen**, keine amtliche Vorgabe oder gemessene Bearbeitungsdauer.

| Variante | Kern | Verteilte Wiederaufnahme | Organisation | Puffer | Flex | Summe |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 32 UE, knapp | 1260 | 45 | 45 | 90 | 0 | 1440 Minuten |
| 36 UE, Arbeitsannahme | 1260 | 135 | 45 | 180 | 0 | 1620 Minuten |
| 40 UE, mit Vertiefung | 1260 | 135 | 45 | 180 | 180 | 1800 Minuten |

Die Kernzeiten enthalten bereits die modulinterne Übung, Rückmeldung und Sicherung. Jahresweite Wiederaufnahme und organisatorische Wechsel sind zusätzliche Zeiten und werden nicht doppelt gebucht. Nach M02 werden Ablageroutinen aus M01, nach M04 Quellenkriterien aus M02 und nach M06 ein neuer Medienfall mit Kriterien aus M05 wieder aufgenommen. Die knappe Variante reserviert dafür je 15 Minuten, die übrigen je 45 Minuten. Diese Fenster sind zeitlich versetzte Lerngelegenheiten, kein Beweis nachhaltigen Lernens.

36 UE bilden die bevorzugte Arbeitsannahme mit Reserve für Hürden und Nachsicherung. 32 UE sind nur bei tragfähigen Zugängen und begrenztem zusätzlichem Hilfebedarf plausibel. Unterhalb dieses Budgets braucht es eine neue Teilplanung mit sichtbaren Auslassungen; kein stilles Streichen von Feedback, Übung oder Kompetenznachweisen. Die sechs offenen Eigenbezugsnachweise sind in keiner Variante durch versteckte Minuten oder einen Scheinauftrag „abgedeckt“.

Die beiden **Flexmodule** vertiefen Gestaltungsvarianten (90 Minuten nach M04/M05) und algorithmische Varianten (90 Minuten nach M06). Sie ersetzen keine Kernmodule und tragen keine nur dort erreichbare Pflichtkompetenz. Bei höherem Hilfebedarf hat zusätzliche Übung Vorrang vor Flex.

## Lernarchitektur, Unterstützung und Orchestrierung

Die Verträge wenden das freigegebene LXF03-Profil und die LXF04-Prinzipien an: aufgabenbezogenes Vorwissen, explizites Modellieren, verbundene Darstellungen, begrenzte Auswahl, abnehmende Hilfen und konkrete Revision. Prinzipien-IDs lösen auf registrierte Claims und Quellen auf. Es werden keine neuen pauschalen Alters- oder Wirksamkeitsclaims eingeführt.

Die jahrgangsweite Wiederaufnahme konkretisiert zusätzlich `LXF04-PR-014` (verzögerter Abruf), der neue Anwendungsfall `LXF04-PR-015` (relationaler Transfer) aus dem [Lernarchitektur-Vertrag](../../foundations/learning-experience/learning-architecture.json). Diese Bezüge begründen die Planung, keine gemessene Wirkung der hier geschätzten Minuten.

Für M03 ist ein individueller Beitrag mit gemeinsamer Revision verpflichtender Planungsbestandteil. Nach spätestens zehn Arbeitsminuten prüft die Lehrkraft ein Minimalprodukt. Eine Rückmeldung muss das Produkt ändern oder eine begründete Beibehaltung auslösen. Bei ausgefallener Diagnose beginnt die nächste Sitzung mit kurzer Nachsicherung; sie baut nicht auf einem nur angenommenen Lernstand auf. Der Jahrespuffer muss dafür verfügbar bleiben.

Digital ist das Primärmedium: tatsächliche Recherche, Dateiverwaltung, Überarbeitung, Austausch und Codeausführung haben jeweils eine fachliche Funktion. Sprache, Eingabeform und Hilfen werden an die konkreten Hürden angepasst. Ein analoger Fallback kann ein Urteil oder eine Ablaufanalyse erhalten, ersetzt aber weder schulischen Login noch digitalen Austausch oder tatsächliches Programmieren. Ausgefallene digitale oder kooperative Teilnachweise bleiben sichtbar und werden erst nach realem Nachholen gewertet.

Ein ausgearbeitetes Materialpaket, Hörbriefing oder eine LearningView-Anlage gehört erst zur späteren konkreten Modulspezifikation/Produktion. Die Roadmap legt keine zusätzliche Ausspielplattform fest.

## Werkzeugkompetenz ohne Zusatzauftrag

`BMB16-GYM-IK-GM-003` erhält eine querschnittliche Evidenzmatrix mit **null zusätzlichen Minuten**: M01 zeigt Gerät und Ablage, M02 Browser/Suche, M04 Text-, Bild- und Präsentationswerkzeuge. Unterstützung nimmt aufgabenbezogen ab; zunehmend selbstständige Anwendung wird später an Sachprodukten beurteilt. Eine abgehakte Bedienliste oder Klickdauer genügt nicht. Die Werkzeughandlungen sind Bestandteile der ohnehin geplanten Arbeit.

## Offene Eigenbezüge

Der vollständige R5-Abgleich erweitert die bisher auf `LH26-E-DP-003` fokussierte Problemlage. Offen bleiben:

- Amtlich: `BMB16-GYM-PK-RK-001` und `BMB16-GYM-IK-MG-001`.
- Orientierung: `LH26-E-DP-002`, `LH26-E-DP-003`, `LH26-E-DP-009`, `LH26-E-KS-011`.

Ihre eigenen Erfahrungs-/Nutzungsbezüge dürfen nicht durch fiktive Fälle ersetzt oder durch private Abgaben, Nutzungsprotokolle, Lehrkraftbeobachtung privater Inhalte oder Telemetrie erzwungen werden. Ein verantwortlicher Curriculum-/Governancereview muss die tragfähige Nachweisform entscheiden. **Die Roadmap behauptet daher ausdrücklich keine vollständige Erfüllung des Basiskurses.** Der Befund erweitert den Anwendungsbereich von CUR-Q-002, ohne dessen versiegelte Fassung zu verändern.

Davon zu unterscheiden ist `BMB16-GYM-PK-RK-003`: Folgen fremder Selbstdarstellung können in M05 anhand eines nicht personenbezogenen Falles abgeschätzt und bewertet werden. Der Plan verlangt beide Denkhandlungen; der tatsächlich durchgeführte Nachweis steht noch aus.

## Übergabe an R6 und spätere Gates

Die 17 orientierenden R6-Aufträge betreffen Werbeauswahl und Dateninteressen (`DP-006` bis `008`), indexbasierte Suche, Motive/Interessenkonflikte, automatisierten Content, anspruchsvolleren Quellenvergleich/KI-Recherche und Codierung (`ID-004`, `006` bis `008`, `011` bis `015`) sowie Netzmodelle, Speichervergleich, soziale Medien und begünstigende Konfliktstrukturen (`KS-008` bis `010`, `012`, `015`). Vollständige IDs und Einzelbegründungen stehen in der Matrix. R6 muss diese Übergabe gegen seine eigene Zeitplanung prüfen; sie ist noch keine fertige R6-Roadmap.

16 offene Grundlagenfragen bleiben unverändert an ihren ursprünglichen Quellen verknüpft. Vier konkrete R5-Eintrittsgates benennen zusätzlich Verantwortlichkeit und Trigger: reale Zugänge/Werkzeuge, lokales Stundenbudget, die sechs Eigenbezüge und die spätere Erprobung. Jede Modulplanung nennt eine eigene Pilotfrage. Vor einer Erprobung müssen insbesondere schulischer Kanal, Datenschutz, Rechte, funktionaler Zugang und Gerätepfade unter der konkreten Konfiguration geklärt sein.

Nächster Schritt ist die fachliche R5-Abnahme oder konkrete Nacharbeit; danach folgt IUM-V2-R6. Inhaltsproduktion bleibt eingefroren, V1 aktiv und Cutover unentschieden. Die späteren TECH-/MOD-/PILOT-Aufträge bleiben separat gesperrt.
