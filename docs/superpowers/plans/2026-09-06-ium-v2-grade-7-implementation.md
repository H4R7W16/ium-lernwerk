# IUM-V2-R7 – Umsetzungsplan

> Ausführung mit `superpowers:executing-plans` sequenziell im vorhandenen Feature-Branch. Gemeinsame Vertragsdateien und verpflichtende Gatefolge erlauben keine parallele Agentenarbeit.

**Ziel:** Eigenständige Klasse-7-Roadmap mit vollständiger Anforderungsdisposition, geprüfter Progression 5–7 und ehrlicher Kapazitätsentscheidung.

**Architektur:** Neue Jahrgangsverträge neben unveränderten R5-/R6-Snapshots. 134 einschlägige Rohrecords (51 amtliche und 31 orientierende Kompetenzen, 52 Kontexte) werden recordgenau disponiert. Fünf Kernmodule tragen die amtlichen Anforderungen; zwei curriculare Erweiterungen tragen zusätzliche orientierende Ziele. Optionale Flexmodule bleiben davon getrennt.

**Technik:** JSON, Draft-2020-12-Schema, Python-Vertragsvalidator und unittest; keine Produktabhängigkeit ändern.

**Spezifikation:** [Freigegebene kontrollierte Re-Baseline](../specs/2026-09-03-ium-v2-controlled-rebaseline-design.md). R6 ausdrücklich abgenommen bei `c38ff9b0b037539b37d6964091c38dc3c323344a`.

## Verbindliche Grenzen

- V1 aktiv; V2 building; Inhaltsproduktion frozen. Kein LXP05, Push, Merge, Pilot oder Cutover.
- Amtliche Aufbaukursrecords bleiben official, Lesehilfe bleibt orientation. Planung ist keine tatsächliche Coverage.
- Historische 40-/46-/54-UE-Modelle sind Auditinput; kein verfügbarer V2-Pfad wird daraus abgeleitet.
- Tatsächliches Anschlusswissen unbekannt. Sieben geplante Einstiegsklärungen mit eigenem Budget, Hilfereaktion und Neuplanung bei breiten Lücken.
- Sechs offene Eigenbezugsrecords aus R6 und 16 Grundlagenfragen erhalten. Drei neue Reflexionsrecords (LH26-E-DP-013/014/018) bis zur konkreten datensparsamen Nachweisentscheidung offen führen; fachliche Teilhandlungen bleiben möglich.
- R7 endet im eigenen Nutzerreview. DASH und CUT bleiben getrennte Folgegates.

## 1. Eingang und fachliche Planung

- [x] R6-Abnahme dokumentieren, R7 vor Arbeit auf in_progress setzen; Board und Initiative nachführen.
- [x] Alle 94 Aufbaukurs- und 40 Klasse-7-Lesehilfe-Records lesen, Quellenrollen unterscheiden und amtliche Fachseite prüfen.
- [x] `roadmap/v2/grades/grade-7/roadmap.json` und `curriculum-map.json`: sieben neue Lernbögen mit Erklärung, Übung, eigenem Produkt, Feedback, Revision und Sicherung; 79 geplante Kompetenzzuordnungen und drei offene Reflexionsentscheidungen.
- [x] `progression.json`: sieben Stränge verbinden konkrete R5-/R6-Module und geplante Produkte mit R7-Zielen, Eingangsklärung und Grenzen. Nicht beobachtetes Wissen bleibt unbekannt.
- [x] Jahrespfade separat rechnen: Kern 1260 Minuten plus 105 Einstieg, 45 Überbrückung, 90 Wiederaufnahme, 30 Organisation, 90 Puffer = 1620 Minuten/36 UE. Medienanalyse erweitert um 180 Minuten auf 40 UE; Gaming um weitere 135 auf 43 UE. 43 UE ist Bedarfsrechnung, kein verfügbares Jahresangebot. Für jeden Pfad eingeschlossene und aus Kapazitätsgründen offene Records explizit projizieren. Kapazitätschecks gegen 32/36/40 reale Netto-UE-Szenarien; tatsächliche lokale Verfügbarkeit überall unbestätigt.

## 2. Verträge und Regression

Dateien: neuer `scripts/validate_v2_grade7.py`, `tests/test_validate_v2_grade7.py`, `schemas/v2/grade-7.schema.json`; additive R6-`acceptance.json`; Jahrgangs-`status.json`, `README.md`, `validation-report.md`. Nur Import/Aufruf und Missing-File-Erwartungen in den bestehenden V2-Prüfdateien erweitern.

- [x] Zuerst Negativtests anlegen: fehlender amtlicher Record, zum Kontext heruntergestufte Kompetenz, künstliche Reflexionserfüllung, fehlender R5/R6-Anschluss, als bekannt gesetztes Vorwissen, Modul-/Jahresdoppelzählung, versteckte ausgelassene Orientierung, alter Zeitpfad als verfügbar, Flex als Pflichtträger, vorgezogener DASH/Cutover, veraltete Hashbindung und falscher Abnahmecommit.
- [x] Fehlenden Validator zunächst nachweisen: `python -m unittest tests.test_validate_v2_grade7` muss scheitern.
- [x] `validate_planning(roadmap, matrix, progression, root) -> list[str]`, `validate_status(data, root) -> list[str]`, `validate_acceptance(data) -> list[str]` und `validate_repository(root) -> list[str]` implementieren. Typ-/ID-/Quellen-/Referenz-/Zeit-/Projektions-/Gatefehler zurückweisen; Eingänge über normalisierten UTF-8-Text mit SHA-256 binden.
- [x] Gezielte Tests, `python -m unittest discover -s tests`, `npm run verify:v2`, fünf Schema-Instanzen und lokale Markdownziele prüfen. Während der vollständigen Suite Eingänge nicht verändern.

## 3. Review und Handoff

- [x] Fachlicher KI-Dokumentenselbstreview: amtlicher Kern einschließlich Prozesse, orientierende Mehranforderungen, ehrliche Reflexionslücken, Progression 5–7, mehrere Kompetenzen ohne Zeitrabatt, Grenzen von Digitalfallbacks und Kapazität prüfen.
- [ ] Nach erfolgreichem `git fetch --prune` und `git pull --ff-only` ausschließlich R7-Dateien lokal committen; Hash und Push-Status dokumentieren.
- [ ] R6 done, R7 review und DASH planned in Task, Initiative, Board, Roadmap und Statusregister herstellen; Entscheidungsvorlage und Session gemäß Vault-Template erstellen. UTF-8, Frontmatter, neue Links, Folgegates und tatsächlichen Commit abgleichen.

Der vorhandene Ausführungsauftrag autorisiert die gesamte Vorbereitung bis zu diesem konkreten Reviewpaket. Eine offene Kapazitäts- oder Reflexionsentscheidung wird sichtbar vorgelegt und nicht stillschweigend gelöst.

Die letzten beiden Schritte betreffen den Commit und die anschließende Vault-Übergabe. Ihr endgültiger Ausführungsstatus steht in der R7-Session Summary mit dem tatsächlichen Commit-Hash.
