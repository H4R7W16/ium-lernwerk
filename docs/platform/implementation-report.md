# Implementierungsbericht Phase 1 – Plattformfundament

## Ergebnis und Aussagegrenze

Das freigegebene Plattformfundament ist mit Stand `6e05394b9f181db7ee1bc83cf1ac5de89be1af74` automatisiert verifiziert und erreicht den Status `implemented`. Es umfasst die contract-first Workspace-Architektur, einen production-empty Portalbuild, ein strikt isoliertes synthetisches Referenzmodul, Local-First-Zustand, Import/Export/Löschen, statische Root-/Subpath-Builds, kontrollierten Offline-/Updatebetrieb, Barrierefreiheitsverträge, Lizenz-/SBOM-Prüfung und GitHub-CI.

Diese Aussage ist technisch. Sie belegt weder reale Unterrichtswirksamkeit noch Safari auf einem verwalteten iPad, Schulnetz-, MDM-, Web-Clip-, Filter- oder LMS-Verhalten. `device-verified` bleibt deshalb ausdrücklich `not-run`; Phase 2 bleibt blockiert.

## Reproduktionsstand

- Ausgangscommit: `b00971e59992bae29eb20646fa9248c7f6e1d2b0`
- geprüfter Commit: `6e05394b9f181db7ee1bc83cf1ac5de89be1af74`
- Branch: `feat/ium-phase1-platform`
- Node.js: `22.20.0`
- npm: `10.9.3`
- Astro: `7.1.6`
- TypeScript: `6.0.3`
- Vitest: `4.1.10`
- Playwright: `1.62.1`
- axe Playwright: `4.12.1`
- vite-plugin-pwa: `1.3.0`
- Workbox: `7.4.1`
- tsx: `4.23.4`

Die abschließende Prüfung begann mit `npm ci`: 656 Pakete wurden installiert, 663 auditiert und 0 bekannte Schwachstellen gemeldet. Danach lief `npm run verify:phase1` ohne Fehler durch.

## Automatisierte Evidenz

| Gate | Ergebnis |
| --- | --- |
| Verifikationskette | 19/19 Schritte bestanden |
| Architekturgrenzen | 6/6 Workspaces bestanden |
| Plattformtests | 35/35 bestanden |
| Browser-Datenflüsse | 18/18 bestanden |
| Offline-/Update-Szenarien | 5/5 bestanden |
| Barrierefreiheitsszenarien | 11/11 bestanden |
| Python-/Bestandstests | 639/639 bestanden |
| Browsermatrix | Chromium `151.0.7922.34`, Firefox `153.0`, WebKit `26.5` |
| Abhängigkeitsprüfung | 646/646 Pakete im SBOM, 9 dokumentierte Ausnahmen, 0 ungültige Lizenzen |
| Security-Audit | 0 bekannte Schwachstellen |
| IUM-Bestand | IUM11, IUM10, IUM09 und Phase 0 bestanden |

Die Barrierefreiheitsprüfung umfasst axe auf vier Routen, Skip-Link und logische Tastaturfolge, Fokus auf Fehlersummary, 320-Pixel-Reflow, 200%-Zoomäquivalent, reduzierte Bewegung, 44×44-CSS-Pixel-Ziele und textuelle Statusunterscheidung. WebKit-Automation ist keine reale Safari-/VoiceOver-Evidenz.

## Builds und Budgets

Geprüft wurden:

1. Produktionsbuild für `/` ohne Module oder Fixture-Bezeichner.
2. Synthetischer Fixture-Build für `/`.
3. Synthetischer Fixture-Build für `/ium-lernwerk/`.

Messwerte des abschließenden Subpath-Builds:

| Messgröße | Ist | Budget |
| --- | ---: | ---: |
| Cold Transfer, gzip | 48.935 Byte | 256.000 Byte |
| initiales JavaScript, gzip | 45.998 Byte | 102.400 Byte |
| dekodierter Precache | 201.944 Byte | 2.097.152 Byte |
| gesamter Build | 219.431 Byte | Berichtswert |
| Drittanbieter-URLs | 0 | 0 |
| nicht base-aware Pfade | 0 | 0 |
| Qualitätsverletzungen | 0 | 0 |

`TEST-`-Bezeichner sind ausschließlich im synthetischen Fixture-Build zulässig und dort als zwei erwartete Ausgaben sichtbar. Der Produktionsbuild wurde separat auf vollständige Fixture-Isolation geprüft.

## Local-First-, Fehler- und Offline-Evidenz

- Dauerhafte Speicherung wird erst nach abgeschlossener IndexedDB-Transaktion gemeldet; ein fehlgeschlagener Schreibvorgang erhält den zuvor bestätigten Stand.
- Gewählte flüchtige Nutzung und sichtbarer Fallback bei gesperrter IndexedDB bleiben unterscheidbar.
- Importdateien über 5 MiB, fremde Module, zukünftige Modulversionen, Identitätsfelder und fehlgeschlagene Migrationen werden ohne Zustandsmutation abgewiesen.
- Import verändert den aktiven Zustand erst nach Bestätigung; Export fällt bei blockiertem Download auf denselben kopierbaren JSON-Inhalt zurück.
- Einzelnes und globales Löschen verlangen eine Bestätigung und lesen den Repositoryzustand anschließend neu.
- Ein installierter Build bleibt nach Online-Erstaufruf offline arbeits- und exportfähig; Schema 1 wird kontrolliert nach Schema 2 migriert.
- Ein wartendes Update aktiviert sich erst nach erfolgreichem Runtime-Flush. Eine Kandidatenversion mit fehlendem Precache-Asset scheitert geschlossen, während die alte aktive Version erhalten bleibt.
- Root- und Subpath-Scope wurden einschließlich Offline-Neuladen geprüft. Ein allererster Offline-Aufruf ohne vorhandenen Cache bleibt prinzipbedingt außerhalb der App-Kontrolle.

## Fail-closed-Mutationsaudit

Die Negativgrenzen wurden einzeln kontrolliert. Abgewiesen wurden unbekannte Manifestfelder, Identitätsfelder im Lernzustand, Fixture-Verweise auf reale Curriculum-/Coverage-IDs, Fixture-Kennungen im Produktionsbuild, Importgröße `5 MiB + 1 Byte`, falsches Modul, nicht unterstützte Version, fehlgeschlagene Migration, fehlgeschriebene IndexedDB-Transaktion, unbedingtes `skipWaiting()`, externe Laufzeit-URL, künstlich unterschrittenes Buildbudget und eine künstlich verbotene MIT-Lizenz.

Der Audit fand einen Testdefekt: Ein fälschlich auf `passed` gesetztes Geräte-Frontmatter blieb zunächst grün, weil `not-run` im Erläuterungstext vorkam. Commit `6e05394` liest nun gezielt das YAML-Frontmatter; die falsche Mutation wird rot, der echte Status `not-run` grün. Außerdem beseitigte `0d4f963` einen durch `git diff --check` gefundenen Whitespace-Befund. Weitere Produktbefunde entstanden nicht.

## Lokaler Chromium-Sicht- und Bediencheck

Ein zusätzlich gerenderter localhost-Lauf bestätigte:

- Layout ohne horizontales Elementüberlaufen bei 320, 768 und 1280 CSS-Pixeln sowie beim 640-Pixel-Zoomäquivalent;
- Bearbeiten, lokale Speicherung, Neuladen, synthetische Importvorschau, bestätigten Import und bestätigtes Löschen;
- Fokuswiederherstellung zum Lösch-Auslöser nach Abbruch sowie Reorientierung zur Modulüberschrift nach Import oder Löschen;
- ausschließlich lokale Ressourcenziele im beobachtbaren Lauf.

Die In-App-Browseroberfläche meldete keine bestätigte Service-Worker-Offlinebereitschaft und blieb deshalb korrekt im Zustand „Online – Offlinebereitschaft wird geprüft“. Offline-Neuladen und kontrollierter Updateprompt wurden nicht aus dieser Oberfläche abgeleitet, sondern durch die fünf isolierten Chromium-Service-Worker-Szenarien belegt. Die Tastatur- und Reduced-Motion-Evidenz stammt ergänzend aus den automatisierten Real-Browser-Tests, weil die In-App-Steuerung globale Tab-/Zoom-/Medienemulationssignale nicht zuverlässig weitergab.

## CI und offene Schritte

`.github/workflows/ci.yml` definiert ausschließlich die Jobs `legacy`, `contracts-build`, `browser` und `offline-quality` mit Node `22.20.0`, `npm ci`, lokal installierten Playwright-Browsern und ignorierten Berichten als Artefakten. Es gibt weder Deployment noch Secrets, reale Daten oder Release-Status. Der Workflow ist syntaktisch und vertraglich lokal geprüft; der erste Remote-Lauf startet erst nach dem Push.

Nächster verbindlicher Schritt ist die reale Durchführung von [device-verification.md](device-verification.md) auf einem verwalteten Ziel-iPad mit Safari, VoiceOver, MDM/Web-Clip, Speicher- und Filterrichtlinie, Schulnetz, Offline-/Updatefall sowie LMS-Einbettung. Bis zu belastbarer Evidenz bleibt `device-verified: not-run` und Phase 2 gesperrt.
