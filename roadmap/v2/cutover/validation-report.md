# IUM-V2-CUT – Technischer Prüfbericht

Stand: 6. September 2026 · **Technische Prüfung bestanden; konkrete Nutzerentscheidung ausstehend.**

Geprüft wurde der CUT-Arbeitsbaum auf `feat/ium-v2-rebaseline` auf Grundlage des angenommenen DASH-Commits `85ccc94b1dc9c5cc60fc48470bd6346cac3b3e50`. Der nachfolgende lokale Abschlusscommit steht im Session-Handoff; kein Selbstbezug auf einen erfundenen zukünftigen Hash. Runtime: Node **22.23.2**, npm **10.9.8**, vorhandenes Workspace-Python. Keine neuen Abhängigkeiten installiert.

## Tatsächlich ausgeführte Prüfungen

| Prüfung | Ergebnis |
|---|---|
| `npm run verify:v2:cutover` | Bestehendes V2-Gate bestanden; historische Grundlagen und Jahrgangssiegel unverändert. |
| `python -B scripts/validate_v2_cutover.py --vault ../../Vault; python -B -m unittest discover -s tests -p test_validate_v2_cutover.py` | 17 tatsächliche Nutzerfreigaben, 33 historische Artefakte, 104 aktuelle Inputs, acht Anforderungen und 46 Bedingungen gültig; 30 fokussierte Tests bestanden, zuletzt 4,916 Sekunden. |
| `npm run test:dashboard` | 30 Vertrags-/Projektionstests bestanden, einschließlich CRLF-Register, abgelehnter fehlender DASH-Freigabe, CUT-Review und verfrühter Aktivierung; final 30,970 Sekunden. |
| `IUM_DASHBOARD_TEST_PORT=4327 npm run test:dashboard:browser (PowerShell-Umgebungsvariable entsprechend gesetzt)` | Sechs Chromium-Gates bestanden (15,4 Sekunden): acht Ansichten und lokale Links, drei CUT-Optionen, WCAG 2.2 AA, Tastatur, 390/768-Pixel-Reflow, Ressourcenfilter und Druck. Desktop/Tablet sowie drei Gate- und zwei Reife-PDF-Seiten visuell geprüft. |
| `npm run verify:ium5 (außerhalb der Sandbox nach reproduziertem Firefox-Leerseitenfehler)` | 24/24 Schritte bestanden; enthält alle 19 Phase-1-Prüfschritte. 996 Python-Tests (128,333 Sekunden), 132 Plattformtests sowie 18 Plattform-Browser-, 5 Offline-, 12 Accessibility-, 39 IUM5-Browser-, 4 Zustands-, 3 IUM5-Offline- und 12 IUM5-Accessibilityprüfungen bestanden. Nach späterer isolierter CRLF-Parserkorrektur Dashboard-, CUT- und V2-Prüfungen gezielt erneut bestanden; keine Lernplattformänderung. |

## Befunde und Nachprüfung

1. **Firefox/Sandbox:** Der erste vollständige Repositorylauf bestand die ersten zehn Schritte und zwölf Chromium-/WebKit-Browserfälle. Sechs Firefox-Fälle scheiterten beim `browserContext.newPage` mit einem internen `_page`-Fehler, bevor Anwendungscode lief. Ein isolierter Firefox-Leerseitentest reproduzierte den Fehler innerhalb der Sandbox und bestand außerhalb. Der festhängende eigene Testprozessbaum wurde anhand der Prozesszuordnung eindeutig identifiziert und mit `taskkill /PID … /T /F` beendet; PowerShell `Stop-Process` hatte einen internen Fehler geliefert. Anschließend wurde das **gesamte** 24-Schritte-Gate außerhalb der Sandbox erfolgreich ausgeführt. Kein Test ausgelassen und keine Anwendungskorrektur für dieses Umgebungsproblem.
2. **Windows-Register:** Der erste reale Dashboard-Browseraufbau scheiterte am CRLF-Zeilenumbruch des Vault-Registers. Ein fokussierter Test reproduzierte die bisherige reine LF-Annahme. Der Parser normalisiert jetzt CRLF; alle 30 Dashboardtests, sechs Browsergates sowie CUT-/V2-Prüfungen bestanden danach. Der nach dieser kleinen Parseränderung nicht betroffene Lernplattformcode blieb unverändert; das komplette IUM5-Gate wurde nicht unnötig ein drittes Mal gestartet.
3. **Portabilität der Belege:** Aktuelle UTF-8-Textdigests normalisieren CRLF zu LF entsprechend den bisherigen V2-Siegeln. Historische Artefaktbelege verwenden weiterhin exakte Git-Blob-Bytes. Zwei gezielte Tests unterscheiden diese Fälle.
4. **Vorgängerbindung:** SRC-Nachweise wurden aus tatsächlich vorhandenen `inventory.json`/`traceability.json` des SRC-Commits gelesen, R6 aus seiner `curriculum-map.json`. Spätere Artefakte werden früheren Freigaben nicht rückwirkend zugeschrieben. R5-Risikozusammenfassungen ohne eigenes Risikofeld sind ausdrücklich redaktionell gekennzeichnet.

Die drei gezielten Test-first-Zyklen (neuer CUT-Vertrag, CUT-Dashboardstatus, CRLF-Parser) zeigten zuerst den erwarteten fehlenden/fehlerhaften Zustand und bestanden nach der Umsetzung. Die 30 CUT-Tests enthalten Positivprüfungen und Ablehnungen bei verlorenen Gates, fehlenden Freigabeauszügen, falschen Commits/Digests, Drift, verschwundenen Bedingungen, erfundener Coverage oder vorweggenommenen Auswahl-/Einsatzfreigaben.

## Sichtprüfung

Desktopansicht und responsive Tabletaufnahme geprüft. Der Browser prüft zusätzlich alle acht Ansichten bei 390 und 768 Pixeln sowie Tastaturnavigation. Die drei A4-Seiten der Gate-/Optionsansicht und die zwei Seiten der Grundlagen-/Reifeansicht wurden mit Poppler gerendert und einzeln visuell geprüft: alle 18 Gates, alle drei Auswahloptionen, acht Reifeachsen, verständliche Grenzen und keine abgeschnittenen Inhalte. Die Test-PDFs sind QA-Artefakte mit damaligem Arbeitskopienstand, kein abschließend publizierter Bericht.

Automatisierte WCAG-2.2-AA-Prüfungen sind technische Indikatoren; eine vollständige manuelle Barrierefreiheitsprüfung oder tatsächliche Nutzungsbewährung wird nicht behauptet. Review durch Codex, keine unabhängige externe Review oder neue fachliche Abnahme.

## Prüfartefakte und verbleibende Grenzen

Lokale Logs liegen außerhalb des Repositories unter `_Transfer/ium-cut-ium5.log` (abgebrochener Sandboxlauf), `_Transfer/ium-cut-ium5-unsandboxed.log` (24/24), `_Transfer/ium-cut-dashboard-unit-final.log` und `_Transfer/ium-cut-dashboard-browser-final.log`. Isolierter Firefox-Reproduktionstest: `_Transfer/ium-cut-firefox-smoke.cjs`. Screenshots und PDFs liegen unter ignoriertem `reports/`; gerenderte PDF-Seiten unter `_Transfer/ium-cut-gates-*.png` und `ium-cut-maturity-*.png`. Keine Build-, Runtime- oder großen QA-Dateien im Git/Vault.

[review.json](review.json) enthält die maschinenlesbare Prüflaufzusammenfassung. `python -B scripts/validate_v2_cutover.py --vault <Vault-Verzeichnis> --require-verified` prüft die tatsächlichen Freigabeauszüge und diese vollständige Prüflaufdokumentation zusätzlich zu den Inputbindungen. Die Prüfung selbst kann keine Nutzerentscheidung erzeugen.

V1 bleibt aktiv; V2 `building`. Produktion, LXP05, Pilot, Schul-/Betreiberfreigabe, Hosting, Veröffentlichung, Push und Merge werden nicht aus grünen Tests abgeleitet. Die neun Nachweisfragen, tatsächliche Kapazität und reale Eingangslage bleiben offen. Der [Entscheidungsbericht](README.md) empfiehlt die ausdrücklich begrenzte Annahme als Planungs-/Entwicklungsbaseline.
