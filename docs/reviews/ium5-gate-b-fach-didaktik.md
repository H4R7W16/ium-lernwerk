---
review: IUM5-GATE-B-FACH-DIDAKTIK
reviewedCommit: 2b4353d5d1a786d4d1ceddba71e3a7b2bdfe28d9
verdict: APPROVED AFTER FIXES
reviewedAt: 2026-08-03
---

# IUM5 Gate B - Fachlich-didaktischer Review

## Aussagegrenze

Geprüft wurde die Implementierung des Gate-B-Pakets für `IUM-5-CORE-05`, nicht eine reale Pilotdurchführung und nicht die Wirksamkeit des Moduls. Der Review autorisiert weder Previewveröffentlichung noch Unterricht, LMS-Nutzung, Evidenzerhebung oder Statusänderung. Modulstatus bleibt `working`, Gerätestatus bleibt `not-run`.

## Prüfgegenstand

- Protokoll, Pilot- und Reviewleitfaden sowie analoger Beobachtungsbogen;
- Passung zum vorhandenen Lehrkräftehandbuch und zum regulären Fünf-UE-/erweiterten Sechs-UE-Pfad;
- Beobachtbarkeit der vollständigen Lernschleife von Vorhersage und Laufspur über erste Abweichung, Reparaturhypothese und minimale Revision bis Schleifenbegründung, Transfer und gemeinsamer Sicherung;
- Orchestrierung, Unterstützungsqualität, optionale Rückmeldung und Nichtwirksamkeitsgrenze;
- Trennung von explorativem Lauf `regular-225` und Bestätigung `extended-270` mit anderer Lerngruppe.

## Evidenz

| Evidenz | Ergebnis |
| --- | --- |
| Vergleich `modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md` mit Protokoll und Pilotleitfaden | fünf und sechs UE, Begriffe, Lernhandlungen und Unterstützungsgrenze stimmen überein |
| `npm run verify:ium5` | 24/24 Schritte erfolgreich |
| `npm run verify:ium5:gate-b` | 8/8 Schritte erfolgreich |
| `npm run test:platform` | 25 Testdateien, 132 Tests erfolgreich |
| `python -B -m unittest discover -s tests -p "test_*.py"` | 669 Tests erfolgreich |
| Chromium-Druckprüfung des Beobachtungsbogens | eine A4-Hochformatseite; bei 100 % und 200 % ohne Beschnitt, unlesbare Codes oder überlagerte Kontrollen |

## Stärken

- Die neun Kriterien bilden fachliche Handlungen statt bloßer Bedienereignisse ab. Die ersten sechs schließen die zentrale Diagnose- und Reparaturschleife; Transfer, denkförderliche Unterstützung und gemeinsame Sicherung bleiben eigenständig sichtbar.
- Die Pilotlehrkraft verantwortet Lernprozess und Fallback, während die Beobachtungsrolle nur geschlossene Klassenaggregate codiert. Technische Hilfe darf die kognitive Handlung nicht ersetzen.
- Der explorative Lauf erlaubt gezielte Reparatur, die Bestätigung verlangt eine andere Lerngruppe und die echte sechste UE. Dadurch wird Wiederholung derselben Lerngruppe nicht als unabhängige Bestätigung ausgegeben.
- Der optionale Drei-Fragen-Puls ist nicht leistungsbezogen, nicht diagnostisch und unter zehn gültigen Antworten vollständig unterdrückt.
- Der analoge Bogen ist medienbegründet: Aufmerksamkeit bleibt im Unterricht und der Nachweis bleibt unabhängig von der geprüften Anwendung.

## Befunde und verifizierte Korrekturen

### FD-01 - Mittel - Auswahl und Beschriftung konnten beim Druck getrennt umbrechen

- Vorbefund auf Commit `53f2dc7`: In einer engen geschlossenen Auswahlgruppe konnte die vierte Radiomarke am Zeilenende stehen, während ihre Beschriftung in die nächste Zeile wanderte. Das hätte Beobachtungscodes unnötig mehrdeutig machen können.
- Reproduzierender Test: `ium5-gate-b-observation-sheet.test.ts` verlangt zehn untrennbare `option-pair`-Gruppen.
- Korrektur: Commit `fd72620` gruppiert jede Kontrolle mit ihrer Beschriftung und verhindert den internen Umbruch.
- Verifikation: fokussierter Test grün; erneuter Chromium-PDF-Render exakt eine A4-Seite und visuell eindeutig bei 100 %/200 %; abschließende 24/24- und 8/8-Ketten grün.

## Offene Befunde

- Kritisch: keine.
- Wichtig: keine.
- Mittel: keine.
- Gering: keine blockierenden Hinweise.

## Urteil

`APPROVED AFTER FIXES`

Die Implementierung ist fachlich-didaktisch für den schriftlichen Gate-B-Handoff geeignet. Das Urteil bestätigt nur die Qualität und Geschlossenheit des Instrumentariums; reale technische Prüfung, zwei Pilotläufe, LMS-Entscheidung und mögliche Freigabeprüfung bleiben separate zukünftige Entscheidungen.
