---
review: IUM-5-CORE-05-fach-didaktik
reviewedCommit: 4c26698590869b51e8d272cb4ddaf4920455d180
reviewedAt: 2026-08-03
verdict: APPROVED
gateB: closed
---

# Fachlich-didaktischer Review: IUM-5-CORE-05

## Auftrag und Aussagegrenze

Geprüft wurde der interne `working`-Stand von `IUM-5-CORE-05 – Präzise Abläufe ausführbar machen` am Commit `4c26698590869b51e8d272cb4ddaf4920455d180` gegen die freigegebene Modulspezifikation und den TDD-Implementierungsplan. Der Review beurteilt fachliche Kohärenz, didaktische Umsetzbarkeit und die interne Gate-A-Prüfbarkeit. Er ist keine Unterrichtspilotierung, keine Wirksamkeitsaussage und keine Öffnung von Gate B.

## Gelesene und ausgeführte Evidenz

- `modules/IUM-5-CORE-05/module.yaml`, `curriculum-mapping.json`, `lernumgebung/content.json` und `lernumgebung/scenarios.json`;
- `modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md` und `lernumgebung/index.md`;
- `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md`;
- `tests/platform/ium5-resources.test.ts`, `ium5-interpreter.test.ts` und `ium5-payload.test.ts`;
- `tests/browser/ium5-workbench.spec.ts`, `ium5-state.spec.ts`, `ium5-offline.spec.ts` und `ium5-accessibility.spec.ts`;
- vollständiger Lauf `npm run verify:ium5` am 2026-08-03: 24/24 Schritte erfolgreich.

## Einzelbefunde

| Prüfbereich | Befund und Evidenz |
| --- | --- |
| Curriculum und Progression | Die fünf Records `LH26-E-PROG-002` sowie `LH26-E-ALG-001` bis `004` besitzen jeweils Lernhandlung, Produktbeleg, Segmentbindung und Scopegrenze in `curriculum-mapping.json`. Feste Wiederholung bleibt auf 2–9 Durchläufe begrenzt; Verzweigung, bedingte Schleife, Variable und vertiefte Kontrollflussanalyse bleiben ausdrücklich Klasse 7 vorbehalten. Manifest- und Mappingvertrag werden in `ium5-resources.test.ts` geprüft. |
| Zeit und Zusatzleistung | `content.json` summiert den regulären Pfad auf 225 Minuten und den erweiterten Pfad auf 270 Minuten. UE6 nutzt `extended-inherited` für neue Vorhersage, reale Ausführung, erste Abweichung, Hypothese, Revision, erneute Prüfung und Produktvergleich; sie wiederholt nicht nur die Einführung. Ressourcen- und Browsertests prüfen beide Pfade. |
| Aufgabenarchitektur | Präzisionskontrast, aktives Beispiel, gezielte Fehlerfälle, eigenes Produkt und Algorithmus-Lupe sind als fünf unterscheidbare Aufgabenfamilien vorhanden und in `ium5-workbench.spec.ts` sichtbar geprüft. Drei gleichwertige Produktkarten verhindern die Bindung des Lernprodukts an nur eine Route. |
| Erkenntniszyklus | Oberfläche, Inhalte und Tests erzwingen die Folge präzisieren, vorhersagen, ausführen, Laufspur lesen, erste Abweichung lokalisieren, Hypothese formulieren, gezielt revidieren und Schleifenentscheidung begründen. Die Ausführung bleibt deterministisch und die Belegspur wird bewusst bestätigt. |
| Sofort korrekter Entwurf | Ein bereits korrekter Erstentwurf wird nicht künstlich verändert, sondern nachvollziehbar in den standardisierten Fall `repair-standard` überführt. Der Browsertest „moves a correct first draft … without changing it“ sichert diese didaktische Ausnahme. |
| Transfer und Sicherung | Die Algorithmus-Lupe enthält Positivfälle, Nichtbeispiele und den betriebsartabhängigen Grenzfall. Vier unbewertete Selbstcheckfragen und die im Handbuch festgelegten Erklärungspunkte führen zur gemeinsamen fachsprachlichen Sicherung. |
| Unterrichtsorganisation | Das Handbuch beschreibt Einzelverantwortung, Partnererklärung und einen 1:2-Rollenwechsel nach jedem bestätigten Spurabschnitt. Voraussetzungen aus `IUM-5-CORE-01`, Dateidialog-Fallback und frische, nichtpersistierte Evidenzfälle sind konkret benannt. |
| Medien- und Bewertungsgrenze | `analogMaterials` ist leer, weil Interpreter, Zustandswechsel und reproduzierbare Laufspur die eigenständige digitale Lernfunktion bilden. Es gibt keine analoge Doppelstruktur, Gamification, Punkte, adaptive Personalisierung, automatische Diagnose oder Benotung. |

## Offene Risiken und Nacharbeit außerhalb Gate A

- Zeitpassung, Verständlichkeit und Orchestrierung müssen mit realen Lerngruppen pilotiert werden; `pilotRequired` bleibt wahr.
- Die 1:2-Rollenorganisation und die Qualität gemeinsamer Sicherungen sind Lehrkräftehandlungen und nicht durch Browserautomation belegbar.
- Die curriculare Zuordnung ist intern konsistent; ihre Bewährung in heterogenen Lerngruppen und eine spätere Niveaudifferenzierung sind noch offen.
- Reale Geräte-, VoiceOver-, Schulnetz-, Filter-, MDM- und LMS-Evidenz fehlt weiterhin; `device-verified: not-run` bleibt korrekt.

## Urteil

`APPROVED`

Der geprüfte Commit erfüllt die fachlich-didaktischen Anforderungen für den internen Gate-A-Handoff ohne blockierenden Befund. Der Status bleibt `working`; Gate B bleibt geschlossen.
