# Daten, Zuständigkeiten und Löschung

**Vorgeschlagener betrieblicher Vertrag für FU-PILOT, noch keine institutionelle Entscheidung.** Grundlage ist der [angenommene GOV-Vertrag](../../foundations/governance/governance-contract.json). Die folgenden Fristen sind konkrete datensparsame **Projektvorgaben für diesen Prüfzweck**, keine behaupteten gesetzlichen Aufbewahrungsfristen. Vor tatsächlichem Einsatz muss die zuständige Stelle sie mit dem konkreten Datenweg bestätigen; Abweichungen erfordern einen begründeten eigenen Vertrag und ändern keine vorhandenen Daten stillschweigend.

## 1. Datenwege bleiben getrennt

| Datenklasse | Zweck / Inhalt | Speicherort und Zugriff | Höchstfrist dieses Entwurfs |
| --- | --- | --- | --- |
| DATA-SYNTH | Leere Vorlagen, frei erfundene technische Teststände, synthetische Entscheidungsszenarien | Repo/Vault gemäß Dateirolle; keine realen Inhalte hinein kopieren | Git-versionierte Entwicklungsartefakte, keine personenbezogene Erhebung |
| DATA-DOSSIER | Eigene P1/P2/P3/P5/P6 und knappe Rückkehrnotiz für das Weiterlernen; keine zusätzlichen Versuchslogs | Vorher freigegebener schulischer Geräte-/Profilbereich oder persönliche Papierfassung; Lernende und zuständige Lehrkraft. Kein Pilotexport. | Nach letzter benötigter Rückmeldung/Rückgabe, spätestens 14 Kalendertage nach T5; Termin vor Start festlegen. Andere schulische Dokumentationszwecke brauchen einen getrennten Vertrag. |
| DATA-DIAG | P0/P4 als aktuelle Diagnose, keine Antwortsammlung | Nur im Unterricht einsehen/erläutern; Rückkehrnotiz enthält bei Bedarf nächste Handlung, nicht Abrufantwort | Antwortanzeige/Arbeitsblatt für diesen Diagnosezweck am Ende des betreffenden Termins bereinigen; keine dauerhafte Sammlung |
| DATA-OBS | OBS-Kategorie, Hilfekontext, Unterrichtsminuten, sachliche Störungs-/Maßnahmencodes; keine Einzelbeiträge | Papier unter Aufsicht; danach zugriffsbeschränkte schulische Ablage außerhalb von Repo, Vault und diesem OneDrive-Workspace. Lehrkraft/Beobachtung und benannte Reviewrolle | Papier nach geprüftem Übertrag, spätestens 7 Tage nach Termin; digitale Arbeitsaggregate bis Entscheidung + 14 Tage, spätestens 60 Tage nach T5 |
| DATA-USE | Zusammengefasste sachliche Bedienprobleme je angebotenem Zugangsprofil, ohne Personen-/Sitzungsnummer | Zugelassene schulische Ablage; benannte Nutzungs-/Zugangsprüfende | Rohnotizen nach geprüftem Übertrag, spätestens 7 Tage nach Sitzung; Problemliste bis Entscheidung + 14 Tage, spätestens 60 Tage nach letzter Nutzungssitzung |
| DATA-TECH | Bereinigte technische Reproduktion mit synthetischen Daten, Build-/Browser-/Policykategorien | Bereinigte reine Softwarebefunde dürfen nach Prüfung ins Repo; reale Umgebungsprotokolle bleiben bei zuständiger Technikstelle | Reales Umgebungsprotokoll bis Entscheidung + 14 Tage, spätestens 60 Tage nach Abschluss der technischen Prüfserie; reine synthetische Bugreproduktion regulär versionierbar |
| DATA-OPS | Namen/Zuständigkeiten, konkrete Termine, Erlaubnis- und Ablaufregister; getrennt von Beobachtung | Zuständige Schule/Betreiber, vor Start bestimmter Ort; Zugang nur für verantwortliche Rollen | Pilotbezogenes Arbeitsregister bis Entscheidung + 30 Tage, spätestens 90 Tage nach letztem zugehörigem Lauf. Institutionell anderweitig erforderliche Aktenführung ist getrennt zu entscheiden. |
| DATA-EXTERNAL | Bewusst angelegte Exporte, Downloads, Clipboard, Backups, Profilsynchronisierung, Hosting-/LMS-Logs | Jeweiliger realer Speicherverantwortlicher; Wege vor Start inventarisieren | App-Exporte spätestens mit DATA-DOSSIER löschen; Clipboard nach bewusster Übertragung bereinigen. Für Logs/Backups vor Start konkrete Dauer und Ablaufdatum bestimmen; ohne nachvollziehbare Regel bleibt betroffener Betriebsweg geschlossen. |

Fristende ist jeweils der **frühere** der genannten Termine. Eine vertagte Entscheidung verlängert die Höchstfrist nicht. Ein später Bestätigungslauf verlängert die Frist der Exploration nicht. Innerhalb des zulässigen Zeitfensters muss daher die bereinigte Entwicklungsentscheidung gesichert werden; nach Löschung fehlende Vergleichsdaten nicht rekonstruieren oder behaupten. Bei Abbruch tritt dessen Datum für die betreffende Serie an die Stelle des geplanten Enddatums; offene Arbeitsdaten nicht bis zu einem nie stattfindenden T5 behalten.

Ein Arbeitsdossier ohne Namen ist auf einem bekannten Schulgerät nicht automatisch anonym. Auch kleine Beobachtungsaggregate können im Kontext zuordenbar sein. Deshalb gelten geschützte Ablage und beschränkter Zugriff, obwohl das Paket keine Identifikatoren fordert. Die Entscheidungskopie fürs Projekt enthält lediglich bereinigte Modul-/Protokoll-/Buildbezüge, fachliche Befunde, Maßnahmen und Nachweisgrenzen. Keine Klassenkennungen, exakten Unterrichtstermine, Teilnehmendenzahlen, Produktkopien oder Zitate übernehmen. Bei verbleibender Zuordenbarkeit bleibt auch die Entscheidung außerhalb des Workspace.

## 2. Rollen und Eintritt

- **Jan / project-decision:** nimmt Design und Folgeaufträge an, koordiniert die Benennung der zuständigen Stellen. Keine automatische Schul- oder Betreiberrolle.
- **school-controller:** entscheidet vor Lernendennutzung über Zweck, Rechtsgrundlage, erforderliche Information, Schutz, Zugang und konkrete Löschtermine. Die tatsächliche Stelle ist noch nicht benannt.
- **operator:** klärt den tatsächlich angebotenen Hosting-/Betriebsweg vor Veröffentlichung. Öffentliche statische Seiten können Serverlogs verursachen; `noindex` ist kein Zugangsschutz.
- **teacher-reviewer / durchführende Lehrkraft:** bestätigt reale Vorarbeit, Zeit und sichere Alternativen, verantwortet formative Rückmeldung, Unterbrechung und Dossier-Rückgabe.
- **Beobachtung / Nutzungsmoderation:** erfasst nur die vereinbarten Kategorien, schützt Papier, prüft Übertrag und löscht fristgerecht. Bei Rollenidentität mit Lehrkraft werden eingeschränkte Beobachtungsmöglichkeiten offengelegt.
- **technical-, accessibility-, subject-didactics-, privacy- und rights-reviewer:** prüfen jeweils ihren benannten Bereich. Datenschutzberatung ersetzt keine Entscheidung der verantwortlichen Stelle. Ein KI-Selbstreview ist keine externe Fachprüfung.

Die noch unbesetzten Rollen werden vor Einsatz im privaten Freigaberegister mit tatsächlicher Person/Stelle, Umfang, Datum und Erreichbarkeit zugeordnet. Eine Person darf mehrere fachlich passende Rollen übernehmen, sofern Interessenkonflikt/fehlende Unabhängigkeit offengelegt werden; dadurch entsteht kein unabhängiger Doppelreview.

## 3. Verbindlicher Löschablauf

Vor Start: Enddatum, Entscheidungszieltermin und jeden absoluten Löschtermin in der privaten Kopie eintragen. Speicherstellen inventarisieren: App-Stand, Papier, Exportordner, automatische Downloadkopien, Clipboard/Cloud-Clipboard, Schulprofil-/Dateisync, Backup und gegebenenfalls Server-/LMS-Logs. Lernmodul-Persistenz muss zu diesem Vertrag passen; die offenen F04–F06 verhindern aktuell eine pauschale Zusage.

Nach jeder Sitzung: Papier unter Aufsicht halten, keine Handyfotos. Geschlossene Kategorien übertragen, durch zweite benannte Person oder dokumentierten Gegencheck mit der Originalvorlage auf Übertragungsfehler prüfen. Originale danach vernichten. Freitext über Lernende wird nicht übertragen. Optionales Gesprächsfeedback wird nicht gesammelt.

Am Fristende: Zuständige Person entfernt Pilotarbeitsdaten am vereinbarten Ort, leert anwendbare Papierkörbe/Exportablagen und bestätigt den Umfang. Externe Löschungen durch jeweilige Zuständige gesondert bestätigen lassen. Backups/technisch nicht sofort löschbare Kopien müssen vor Start mit Zugriffssperre und konkretem Ablauf geklärt sein; „App gelöscht“ genügt nicht. Dieser Ablauf ist eine noch zu realisierende Anforderung und keine zugesicherte Fähigkeit der aktuellen V1-App.

| Datenklasse | Start-/Endereignis | Absoluter Löschtermin | Zuständige Rolle | Speicherstellen geprüft | Tatsächlich erledigt / Restbestand |
| --- | --- | --- | --- | --- | --- |
| DATA-DOSSIER / DIAG / OBS / USE / TECH / OPS / EXTERNAL | — | — | — | nein | nicht durchgeführt |

Ungeplanter Personenbezug, fremder Stand oder unerwartete Übertragung: betroffenen Pfad anhalten, keine Weitergabe ins Projekt/Chat, zuständige Schule/Betreiber informieren und nach deren Verfahren behandeln. Vor Wiederaufnahme den konkreten Fehler beheben und prüfen. Das Paket schreibt keine pauschale Meldepflicht oder Rechtsbewertung vor.

## 4. Rechte und Ausspielung

MAT-01–10 liegen noch nicht als Produktionsmaterial vor. Für eigene neue Texte/Grafiken Autorenschaft und Fassung dokumentieren. Für jede spätere Übernahme Quelle, Rechteinhaber, Lizenz/Erlaubnis, erlaubte Bearbeitung, Kennzeichnung und Ausspielkanal belegen. Die bloße Quelle im SRC-Register ist keine Nutzungsfreigabe für ein Asset. Keine Logos oder institutionelle Unterstützung aus dem Projektkontext ableiten.

Lernprodukte verbleiben beim Unterrichtszweck. Ihre Veröffentlichung, Weitergabe an KI-Dienste oder Nutzung als öffentliches Beispiel ist nicht Bestandteil dieses Prüfvertrags. Ein hypothetischer separater Auftrag müsste eigenständig Rechte und Datenverarbeitung klären. Für FU-PILOT werden keine realen Daten eingeholt und keine externen Dienste eingerichtet.
