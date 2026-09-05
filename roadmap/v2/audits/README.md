# IUM-V2-AUD – Übernahmeaudit

Stand: 2026-09-06. Das Audit bewertet **25 Artefaktfamilien** aus IUM00–IUM20 und LXP01–LXP04 anhand ihrer tatsächlichen Repositorydateien und der freigegebenen V2-Grundlagen. Die Familien sind historische Arbeitsergebnisse, keine Aussage über das Vorhandensein ihrer alten Vault-Task-Notizen. Die Bewertung ist zur fachlichen Nutzerabnahme bereit; sie führt keine der geplanten Anpassungen aus.

V1 ist unverändert an `dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0` gebunden. Das Inventar prüft 59 unterschiedliche V1-Dateien einschließlich ergänzender Belege. LXP05 wird separat am Kandidaten `645a1d4ea3c786b08e1320954b522edf86dc9f83` ausgewertet. Keiner dieser Befunde öffnet Inhaltsproduktion, Pilotierung, Veröffentlichung oder Cutover.

- [Maschinenlesbares Inventar mit Begründungen und Belegen](artifact-inventory.json)
- [Konkrete Nachfolgetasks](follow-up-tasks.json)
- [Separater LXP05-Erfahrungsbestand](lxp05-lessons.json)
- [Gegenprüfung und technische Nachweise](validation-report.md)
- [Auditstatus und weitergegebene Fragen](status.json)
- [GOV-Nutzerabnahme vom 6. September](../foundations/governance/acceptance.json)

## Bedeutung der Entscheidungen

| Entscheidung | Bedeutung |
| --- | --- |
| retain | Der exakt benannte Bestand bleibt innerhalb des angegebenen Geltungsbereichs unverändert verwendbarer Input. Keine Erweiterung seiner normativen Geltung und keine automatische V2-Aktivierung. |
| adapt | Bestimmte Substanz bleibt tragfähig, benötigt aber die dokumentierte Anpassung oder Einbettung in V2. Nachfolger und Akzeptanzkriterien sind zwingend. |
| replace | Die bisherige steuernde Fassung wird durch eine neue V2-Fassung ersetzt. Einzelne Quellen, Fachlogik oder Problembeispiele können weiterhin Belege sein. |
| reference-only | Historischer Vergleichs-/Erfahrungsbeleg ohne normative Steuerungs- oder Produktionsfunktion. |
| drop | Kein Bedarf in der neuen Grundlage; die Datei bliebe trotzdem im V1-Archiv. Im vorliegenden Audit für keine Familie gewählt. |

Ergebnis: **1 retain, 15 adapt, 5 replace, 4 reference-only, 0 drop**. Das sind Entscheidungen über Wiederverwendung, keine Reifegrade. Insbesondere bedeutet `adapt` nicht, dass die Anpassung schon umgesetzt wäre. Der Nachfolgestatus unterscheidet bereits abgenommene Grundlagenarbeit von geplanter Roadmaparbeit und gesperrter Produktarbeit.

## Entscheidungen je Artefaktfamilie

<!-- AUD-DECISIONS:START -->
| ID | Gegenstand | Entscheidung | Primärer Nachfolger |
| --- | --- | --- | --- |
| IUM00 | Forschungsvertrag und Quellenführung | `adapt` | IUM-V2-SRC |
| IUM01 | Informatikdidaktische Kuration | `adapt` | IUM-V2-R5 |
| IUM02 | Medienbildungsdidaktische Kuration | `adapt` | IUM-V2-R5 |
| IUM03 | Lernpsychologische Kuration | `adapt` | LXF02 |
| IUM04 | Digitale Lernumgebungen und OER | `adapt` | IUM-V2-FU-TECH |
| IUM05 | Quellentreue Curriculumextraktionen | `retain` | Keine Anpassungsarbeit |
| IUM06 | Synthese, Fachprofil und Crosswalk | `replace` | LXF03 |
| IUM07 | Modulkandidaten und Abdeckungsroadmap | `replace` | IUM-V2-R5 |
| IUM08 | Phase-0-Abschlussreview | `reference-only` | Keine Anpassungsarbeit |
| IUM09 | Recordgenaue Coverage-Nacharbeit | `adapt` | IUM-V2-R5 |
| IUM10 | Zeitmodell und Jahresvarianten | `replace` | IUM-V2-R5 |
| IUM11 | Working-40-Pilotinstrument | `adapt` | IUM-V2-FU-PILOT |
| IUM12 | Plattformfundament – Spezifikation | `adapt` | IUM-V2-FU-TECH |
| IUM13 | Implementiertes Plattformfundament | `adapt` | IUM-V2-FU-TECH |
| IUM14 | Reale Geräteprüfung – Teilbefunde | `reference-only` | Keine Anpassungsarbeit |
| IUM15 | Entwicklungs- und Einsatzgates | `adapt` | IUM-V2-GOV |
| IUM16 | IUM5-Modulspezifikation | `replace` | IUM-V2-FU-MOD |
| IUM17 | IUM5-Implementierungsplan | `reference-only` | Keine Anpassungsarbeit |
| IUM18 | IUM5-Implementierung | `adapt` | IUM-V2-FU-MOD |
| IUM19 | Gate-B-Spezifikation und Plan | `adapt` | IUM-V2-FU-PILOT |
| IUM20 | Implementiertes Gate-B-Paket | `adapt` | IUM-V2-FU-PILOT |
| LXP01 | Experience-Strategie | `adapt` | LXF02 |
| LXP02 | Produktarchitektur und Lernreise | `adapt` | LXF04 |
| LXP03 | Drei Referenzsituationen | `reference-only` | Keine Anpassungsarbeit |
| LXP04 | Designsystem und Produktionsverträge | `replace` | LXF05 |
<!-- AUD-DECISIONS:END -->

Die jeweils genaue Begründung, der untersuchte Geltungsbereich, ein tatsächlich im V1-Artefakt vorhandener Textanker und die V2-Nachweise stehen im Inventar. Die Tabellen sind Einstiegspunkte; frühere Taskstatus werden nicht als Entscheidungsgrundlage verwendet.

## Wesentliche fachliche Entscheidungen

**Curriculumdaten:** IUM05 bleibt als quellentreuer Extraktionsbestand erhalten. Amtliche Bildungspläne, orientierende Lesehilfe, Beispiele, Operatoren und Projektzuordnungen bleiben getrennt. Die geprüften 278 Records liefern noch keine V2-Modulabdeckung. R5/R6/R7 müssen neue Zuordnungen, tatsächliche Lernhandlungen, Produkte und Rückgriffe ausweisen und Quellenänderungen bei Verwendung beachten.

**Gesamtsteuerung und Jahresplanung:** IUM06 wird als alter Steuerungsverbund ersetzt. Das widerspricht nicht den feineren LXF01-Entscheidungen, die einzelne Claims, Prinzipien und das Fachprofil adaptieren: Ihre Substanz fließt in getrennte V2-Verträge ein, der alte Gesamtverbund steuert V2 nicht weiter. IUM07 und IUM10 werden durch neue Jahresroadmaps ersetzt. Historische 30/34/38- oder Working-40-Werte sind Vergleichsrechnungen, keine automatisch gültigen V2-Zeitbudgets.

**Restlücken:** IUM09 liefert Ursachen und Evidenzideen. Die bereits freigegebenen CUR-Entscheidungen bleiben vorrangig: Werkzeugnutzung wird in regulären Lernhandlungen querschnittlich nachgewiesen; es entsteht kein künstlicher Zusatzauftrag. Privater Eigenbezug bleibt unter CUR-Q-002 offen. CUR-Q-003 bleibt der Klasse-7-Progression und Fachbalance zugeordnet. Ein fiktiver Fall erfüllt keinen geforderten Eigenbezug; ein Einzel-/Papierfallback fingiert keine ausgefallene kooperative oder digitale Kompetenz.

**Technik und Modul:** Local-First, geschlossener Import, kontrollierte Updates und deterministische Algorithmussemantik sind wertvoller technischer Bestand. Konkrete Wiederverwendung benötigt aber die Anpassung an V2-Verträge, aktuelle Umgebungen und ein neues Moduldesign. IUM16 wird als Gesamtspezifikation ersetzt; IUM18 bleibt selektiv anzupassender Code-/Szenarienbestand. Der alte Implementierungsplan IUM17 wird nicht erneut ausgeführt. Kein Build, keine Oberfläche und kein Paket wird durch das Audit in V2 integriert.

**Geräte und Pilot:** IUM14 enthält echte Teilbeobachtungen, die erhalten bleiben. Fehlende Geräte-, Versions-, Policy-, Desktop- und LMS-Angaben verhindern einen vollständigen Gerätepass. IUM11 und IUM19/20 liefern anpassbare Prüfverfahren und synthetische Instrumente. Ihre Zeitbindung, Gruppenschwellen, Aufbewahrungsregeln und Kennzahlen sind keine allgemeinen V2-Vorgaben. Die Anpassung der Instrumente ist keine Durchführung eines Piloten.

**LXP-Kette:** LXP01 `adapt → LXF02`, LXP02 `adapt → LXF04`, LXP03 `reference-only` und LXP04 `replace → LXF05` bestätigen das freigegebene LXF01-Audit exakt. Die entsprechenden Grundlagen wurden inzwischen bearbeitet und abgenommen. Das bedeutet weder eine implementierte V2-Produktarchitektur noch eine Rücknahme der LXP05-Sperre.

## Nachfolgearbeit und Gatefolge

Das Register enthält zwölf konkrete Nachfolgetasks: sechs bereits abgeschlossene Grundlagenaufträge, R5/R6/R7 und drei neu aus diesem Audit abgeleitete, gesperrte Folgeaufträge. Jeder besitzt Zweck, Artefaktzuordnung, Akzeptanzkriterien, Abhängigkeiten und eine Vault-Task-Notiz.

1. **Jetzt:** Dieses Audit fachlich abnehmen oder konkrete Nacharbeit benennen.
2. **Danach:** R5 → R6 → R7 → DASH → CUT in der bestehenden Reihenfolge. Die Nachfolgehinweise ergänzen die jeweiligen Aufgaben, ohne die Jahresroadmaps vorwegzunehmen.
3. **Nach gesondertem Cutover-/Folgeauftrag:** `IUM-V2-FU-TECH` prüft technische V1-Bausteine gegen V2; `IUM-V2-FU-MOD` spezifiziert ein erstes passendes Referenzmodul. Beide bleiben gesperrt und benötigen einen eigenen Nutzerauftrag. FU-MOD autorisiert noch keine Implementierung.
4. **Nach diesen Grundlagen und eigenem Auftrag:** `IUM-V2-FU-PILOT` bindet Prüf- und Pilotinstrumente an das konkrete V2-Modul. Reale Erhebungen und Einsätze bleiben gesonderte Entscheidungen.

Die drei Folgeaufträge sind keine zusätzlichen Voraussetzungen vor R5 und verändern die laufende Re-Baseline-Gatefolge nicht. Für die spätere Produktarbeit wird kein bereits erledigter LXF-Task wieder auf „in Arbeit“ gesetzt.

## GOV-Abnahme und offene Fragen

Der datierte GOV-Snapshot vom 5. September dokumentiert den damaligen Review mit ausstehender Abnahme. Die neuere [Abnahmenotiz](../foundations/governance/acceptance.json) hält die ausdrückliche Nutzerentscheidung vom 6. September für Commit `9f52cdc6f5e36b72b7a3fd9e64501ccfc4af2135` fest. Diese additive Dokumentation bewahrt die ursprünglichen 25 GOV- und 35 LXF07-Prüfeingänge unverändert.

16 unterschiedliche offene Fragen aus LXF07 und GOV werden mit Verweis auf ihre ursprünglichen Eigentümer, Risiken und Trigger weitergetragen. CUR-Q-002 steht in beiden Grundlagen und wird einmal mit beiden Quellen aufgeführt. Keine Frage wird durch Audit oder GOV-Abnahme geschlossen. Betreiber, konkrete schulische Stelle, menschliche Prüfrollen und Rechte bleiben vor ihren jeweiligen Einsatzgates zu klären. Die Alters-, Technik- und Pilotfragen bleiben sichtbar.

## Prüfmethode und Grenzen

Autor und Prüfer: Codex; KI-gestützter Dokumentenselbstreview. Zuerst wurden Artefaktfamilien geprüft, danach Konflikte zwischen Familien und V2-Grundlagen. Für ergänzende Dateien wurden Herkunft, Rolle und Bindung geprüft; das ist keine erneute vollständige Code- oder Quellenbegutachtung jeder Datei. Fehlende historische Vault-Notizen werden nicht rekonstruiert oder als vorhanden ausgegeben. Die Projektseite diente der Zuordnung; die Entscheidungen stützen sich auf die versionierten Artefakte.

`npm run verify:v2` prüft zuerst die bisherigen Grundlagen, dann das Audit. Der Auditvalidator prüft die genaue 25er-Menge, erlaubte Entscheidungen, feste Artefaktzuordnung, Git-Dateiinhalte und Hashes, V2-Anforderungsbezüge, konkrete Nachfolger, Abhängigkeiten, Fragenübergabe und LXP05-Trennung. Die Prüfdateien sind mit SHA-256 über UTF-8/LF gebunden. Der Validator beweist keine fachliche Wahrheit von Freitext und keine tatsächliche Lernwirkung; Begründungen und Gegenfälle bleiben redaktionell zu prüfen.
