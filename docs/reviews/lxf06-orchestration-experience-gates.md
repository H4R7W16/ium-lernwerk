# LXF06 Implementierungsreview

Stand: 2026-09-05. Prüfart: KI-gestützter Selbstreview durch Codex, keine unabhängige Gegenprüfung und keine fachliche Nutzerfreigabe. Der geprüfte Stand ist der Commit, der diesen Bericht erstmals hinzufügt; Basis ist `22e9978e86fe5a0fc61e1d5de8072c7a94e18eeb` auf `feat/ium-v2-rebaseline`.

## Gegenstand und Ergebnis

Task 6 des freigegebenen LXF-Plans ist umgesetzt. Der Lehrkraftleitfaden beschreibt Vorbereitung, Auftakt, Modellierung, Kooperation, Haltepunkte, Feedbacknutzung, Sicherung, Zeitvarianten und Fallbacks. Zwölf methodenspezifische Gatedefinitionen und ein ausdrücklich leerer Reviewbogen ergänzen den Vertrag. Die bereits vom Nutzer freigegebenen LXF05-Patternstatus sind als Voraussetzung im selben Änderungsstand enthalten.

Im Selbstreview wurde kein verbleibender blockierender Befund festgestellt. Dieses Ergebnis empfiehlt die Vorlage zum Nutzerreview; es ersetzt dessen Entscheidung nicht.

## Fachliche Gegenfälle

| Prüffall | Beleg und Konsequenz im Entwurf |
|---|---|
| Fehlendes oder mehrdeutiges Ausgangsprodukt | `teacher-orchestration.md`, Walkthrough `entry`: Diagnose und Wahl zwischen Modellierung, Erkundung und eigener Anwendung bleiben begründet; fehlende Evidenz gilt nicht als Kompetenznachweis. |
| Hilfe übernimmt die Kernhandlung | Walkthrough `central-learning-action` und Gate `support-without-task-removal`: Hilfe muss reduziert oder umgebaut werden; eine eigene Anwendung bleibt erforderlich. |
| Kooperation verdeckt individuelle Leistung oder ein Partner fällt aus | Kooperationsabschnitt: eigener Beitrag, Minimalprodukt, Zwischenkontrolle und Zusammenführung sind festgelegt. Ein Einzelpfad weist ein ausdrücklich kooperatives Lernziel nicht gleichwertig nach. |
| Arbeitsstand geht verloren | Walkthrough `securing-and-reentry`: Wiederherstellung oder begrenzte Neuerstellung sowie eine offene Frage und der nächste Arbeitsschritt ermöglichen den Wiedereinstieg. |
| Papieralternative entfernt einen digitalen Lerngegenstand | Fallbacktabelle und Gate `accessibility-and-equivalence`: Zugang und fachliche Äquivalenz werden getrennt geprüft; eine entfernte Kernhandlung blockiert bereits den Entwurfsreview. |
| Automatisierte Tests werden als didaktische Freigabe ausgelegt | Vertrag, Validator und Reviewbogen: Methodenpflicht, konkrete Fundstellen und zuständige Rolle sind erforderlich; `executionStatus` bleibt `not-run`. |
| Dokumentenreview wird zu Pilot-, Standard- oder Wirkungsaussage | `reviewBoundary`, `statusEffect` und Reviewbogen schließen diese Promotion aus; tatsächliche Nutzungs- und Unterrichtsnachweise bleiben offen. |

Alle zwölf Gates verweisen auf bekannte, freigegebene LXF04-Prinzipien und LXF05-Muster. Zusammen decken die Referenzen alle 18 Prinzipien und zehn Muster ab. Die drei neutralen Walkthrough-Zuordnungen umfassen sämtliche Pflichtgates. Diese Referenzabdeckung allein ist kein Wirksamkeitsnachweis.

## Technische Nachweise

- TDD: Die neuen Vertragstests scheiterten vor der Implementierung an fehlendem Validator beziehungsweise fehlenden Pflichtartefakten; anschließend bestanden alle 15 neuen Tests.
- `python -B -m unittest discover -s tests -p test_validate_v2_rebaseline.py`: 149 Tests bestanden.
- `python -B -m unittest discover -s tests`: 824 Tests bestanden.
- `npm run verify:v2`: bestanden.
- Unabhängige Schema-Instanzprüfung mit vorhandenem AJV Draft 2020-12 und `ajv-formats`: Original akzeptiert, zwölf unzulässige Mutationen abgewiesen. Geprüft wurden Methodenpflicht, Statuspromotion, boolescher Typ, Leertext, Rolle, doppelte IDs, Schema-Version und ungültiges Kalenderdatum.
- `git diff --check`: bestanden.

JSON-Schema prüft Struktur und lokale Methodenbedingungen; der Python-Validator prüft zusätzlich Referenzen, Freigabestatus und vollständige Walkthrough-Abdeckung. Beide Verfahren bewerten keine fachliche Qualität von Freitexten. Die Schema-Instanzprüfung ist technisch unabhängig vom Python-Validator, der fachliche Review ist ein Selbstreview.

## Übergabe und Grenzen

Die Nutzerentscheidung betrifft [Lehrkraftorchestrierung](../../roadmap/v2/foundations/learning-experience/teacher-orchestration.md), [zwölf Gatedefinitionen](../../roadmap/v2/foundations/learning-experience/experience-gates.json) und [Reviewbogen](../../roadmap/v2/foundations/learning-experience/review-form.md). LXF06 steht zur fachlichen Freigabe; LXF07 wurde nicht begonnen. Das Gesamtfundament bleibt `working`, Pilot `not-started` und Inhaltsproduktion `frozen`. Kein Push, Merge, Produktrelease oder Cutover gehört zu diesem Abschluss.
