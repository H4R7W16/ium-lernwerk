---
review: IUM-5-CORE-05-engineering-accessibility-privacy
reviewedCommit: 4c26698590869b51e8d272cb4ddaf4920455d180
reviewedAt: 2026-08-03
verdict: APPROVED
device-verified: not-run
gateB: closed
---

# Engineering-, Accessibility-, Privacy- und Lizenzreview: IUM-5-CORE-05

## Auftrag und Aussagegrenze

Geprüft wurde Commit `4c26698590869b51e8d272cb4ddaf4920455d180` gegen den technischen Vertrag der freigegebenen Modulspezifikation. Der Review bewertet Code, Builds und automatisierte Evidenz. Er erklärt weder ein reales Gerät noch VoiceOver, Schulnetz, MDM, Filter oder LMS für bestanden und verändert den Status `device-verified: not-run` nicht.

## Gelesene und ausgeführte Evidenz

- `packages/ium-5-core-05/src/` und zugehörige Modell-, Interpreter-, Editor-, Payload- und Ressourcentests;
- `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`, Controller, Browserports und Styles;
- Registry-, Build-, Runtime-, Import-/Export-, PWA-, Lizenz- und Dokumentationstests unter `tests/platform/`;
- IUM5-Browsersuiten für Kernpfad, Zustand, Offline und Accessibility;
- `.github/workflows/ci.yml` und `.github/workflows/device-fixture-pages.yml`;
- vollständiger Lauf `npm run verify:ium5` am 2026-08-03: 24/24 Schritte erfolgreich.

## Einzelbefunde

| Prüfbereich | Befund und Evidenz |
| --- | --- |
| Renderer- und Profilgrenze | `build-module-registry.ts` akzeptiert `algorithm-workbench` ausschließlich für exakt `IUM-5-CORE-05`; Produktion und Fixture besitzen disjunkte Registries, Assets, Routen und Bundles. `registry.test.ts` und `portal-build.test.ts` prüfen beide Richtungen. |
| Fachkern und Determinismus | Das DOM-freie Paket besitzt eine geschlossene Befehlssprache, unveränderliche Editoroperationen und deterministische Schritt-/Gesamtausführung. `ium5-interpreter.test.ts` deckt `OBSTACLE`, `OUT_OF_BOUNDS`, `INVALID_PICK_UP`, `INVALID_DROP`, `INVALID_REPEAT` und `STEP_LIMIT` sowie alle zehn Referenzlösungen ab. |
| Datenminimierung | `payload.ts` akzeptiert exakt elf Produktfelder. Bearbeitungszeit, Versuche, Klicks, Hilfenutzung, Playback, Fokus und Navigation fehlen; Browserexporte werden dagegen geprüft. Es gibt kein Konto, Backend und keine Telemetrie. |
| Import, Migration und lokale Kontrolle | Malformed Payloads, falsche Modulversion und zukünftiges Schema ändern den aktiven Zustand nicht. Export, Vorschau/Bestätigung, Import, modulspezifisches Löschen und globales Löschen sind testgedeckt; der volatile Modus und das Kopierfallback bleiben sichtbar. |
| Accessibility und Eingabe | Axe, vollständiger Tastaturzyklus, Touchzyklus, semantische Textszene, beschriftete Laufspur, Fokus nach Fehlern/Phasen/Editoraktionen, 320/360/640 CSS-Pixel, 200-Prozent-Zoom, reduzierte Bewegung und 44-Pixel-Ziele sind automatisiert geprüft. Drag-and-drop, Farbe und Animation sind für die Kernhandlung nicht erforderlich. |
| Offline und kontrolliertes Update | Nach Installation ist der gesamte Kernpfad offline nutzbar. Ein gültiger Kandidat aktiviert erst nach bewusstem Speichern/Flush; ein geändertes, fehlendes Asset macht den Kandidaten `redundant`. Precache-Einträge tragen SHA-384-Integrität. Die aktive Version bleibt beim Fehler erhalten. |
| Build, Basispfad und Laufzeitgrenzen | Produktionsbuild und Rootpfad sowie Fixture-Root-/Subpathvertrag sind geprüft. Der Qualitätsinspektor meldet für Produktion keine Drittanbieter-URLs, Testkennungen oder dynamische Codeausführung. Budgets bleiben deutlich unter 250 KiB Cold-Transfer, 100 KiB initialem JavaScript und 2 MiB Precache. |
| Lizenzen | Das projektintern aus geometrischen SVG-Primitiven erzeugte Roboterasset enthält keine Raster-/Remoteeinbettung und ist in Modul- und Buildnachweisen als CC BY-SA 4.0 ausgewiesen. Code bleibt MIT; Dependency-SBOM und Ausnahmen sind ohne ungültigen Befund. |
| Publikations- und Statusgrenze | CI behält exakt die vier Jobs `legacy`, `contracts-build`, `browser` und `offline-quality`. Der Pages-Workflow baut ausschließlich `build:fixture:subpath` und enthält weder IUM5-ID noch Renderer. Das Modul zeigt `working` und „nicht für Unterrichtseinsatz“; Gate B bleibt geschlossen. |

## Offene Risiken und Nacharbeit außerhalb Gate A

- Reale Safari-/VoiceOver-/iPad-, MDM-, Filter-, Schulnetz-, Web-Clip- und LMS-Prüfung ist nicht erfolgt.
- Browserautomation belegt programmatische Struktur und Bedienpfade, aber keine praktische Screenreaderqualität mit realen Nutzenden.
- Offlinebeständigkeit unter schulischen Speicherlöschrichtlinien und knappen Gerätespeichern benötigt Realgeräte-Evidenz.
- Öffentliche Produktbereitstellung ist absichtlich nicht eingerichtet; der vorhandene Pages-Pfad bleibt eine synthetische Systemprobe.

## Urteil

`APPROVED`

Der geprüfte Commit erfüllt die Engineering-, Accessibility-, Privacy- und Lizenzanforderungen für den internen Gate-A-Handoff ohne blockierenden Befund. `device-verified: not-run`, `working` und das geschlossene Gate B bleiben unverändert.
