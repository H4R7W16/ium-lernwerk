# IuM Learning Experience – Implementierungsnachweis LXP05

- **Datum:** 5. August 2026
- **Normative Grundlage:** `docs/superpowers/specs/2026-08-05-ium-learning-experience-design-system.md`, Fassung 1.0
- **Ausführungsplan:** `docs/superpowers/plans/2026-08-05-ium-lxp04-design-system-implementation.md`
- **Branch:** `feat/lxp05-ium5-experience`
- **Basis:** `main` auf `dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0`
- **Geprüfter Implementierungsstand:** `26890a1`
- **Gate:** lokales LXP05-Review; kein Merge, Push, Pull Request, Preview, Deployment, Realgerät, Pilot, LMS oder Release

## Urteil

Die 12 LXP04-Akzeptanzbereiche sind im vorgesehenen LXP05-Scope implementiert und durch die unten aufgeführten automatisierten Nachweise abgedeckt. Das generische Paket bleibt von IUM5-Fachsemantik getrennt; IUM5 bindet Fachrenderer und lokalen Zustand erst an der Portal-Kompositionsgrenze ein. Der Abschluss ist **reviewbereit**, aber keine Produkt-, Unterrichts-, Accessibility-, Pilot- oder Releasefreigabe.

## Traceability der Akzeptanzbereiche

| Akzeptanzbereich | Zentrale Implementierungsorte | Automatisierte Evidenz | Manuelle Beobachtung | Restunsicherheit |
|---|---|---|---|---|
| Architektur | `packages/learning-experience/`, `scripts/check-workspace-boundaries.ts`, `apps/lernwerk-portal/src/controllers/algorithm-workbench/experience-adapter.ts` | Boundarytests, `boundaries:check` mit 8 Workspaces, Portabilitätsfixture, `verify:experience` | Diff- und Abhängigkeitsreview: IUM5-Typen bleiben außerhalb des generischen Pakets | Keine zweite fachfremde Produktionsintegration; Portabilität ist synthetisch belegt |
| Visuelle Grundlage | `packages/learning-experience/src/styles/{tokens,foundation,patterns,motion}.css` | Style- und Kontrasttests; 9/9 semantische Kontrastpaare | Keine eigenständige visuelle Realgeräteprüfung | Altersangemessenheit und wahrgenommene visuelle Ruhe benötigen späteres Fach-/Nutzungsreview |
| Responsive Verhalten | `patterns.css`, `foundation.css`, `ium5-learning-experience-accessibility.spec.ts` | Reflow bei 320 CSS-Pixeln, 200-%-Zoom, 44×44-Ziele, drei Browser im Kernpfad | Browserausführung automatisiert; kein physisches Gerät | Gerätespezifische Browserchrome, Bildschirmtastaturen und echte Touchhardware ungeprüft |
| Interaktion | semantische Astro-Komponenten, `focus-stage.ts`, `workbench-controller.ts`, `workbench-view.ts` | Start-/Resume-, Kernzyklus-, Fokus-, Dialog-, Tastatur- und Touchtests | Kein zusätzlicher moderierter Walkthrough | Usability und kognitive Last sind nicht aus Automatisierung ableitbar |
| Inhalt | `modules/IUM-5-CORE-05/lernumgebung/experience.json`, `validation.ts`, `validate-experience-content.ts` | Strict-schema-, Referenz-, Textlängen- und Inhaltsintegrationstests | IDs, Begriffe und Handbuchbezüge im Diff geprüft | Fachliche Alters- und Unterrichtspassung bleibt einem separaten Review vorbehalten |
| Feedback und Revision | `EvidenceFeedback.astro`, `RevisionCompare.astro`, `SupportDisclosure.astro`, IUM5-Adapter/-Controller | Feedbackvertrag, Vorhersage–Beleg–Hypothese–Revision, korrekter Erstentwurf mit neutralem Reparaturfall | Keine Beobachtung mit Lernenden | Lernwirkung und tatsächliche Hilfeangemessenheit sind nicht belegt |
| Accessibility | semantische Komponenten, Fokus-/Statuscontroller, `ium5-accessibility.spec.ts`, `ium5-learning-experience-accessibility.spec.ts` | Axe, Tastaturkernweg, Textspur, Reflow, Zoom, Fokus, Touch, Forced Colors und Reduced Motion; 15/15 IUM5-A11Y-Tests | Kein manueller Screenreader- oder Realgerätecheck | Keine Behauptung vollständiger WCAG-2.2-AA-Konformität; manuelle AT-, Kontrast- und Kognitionschecks bleiben offen |
| Resilienz | `resilience-adapter.ts`, `ResilienceNotice.astro`, `RecoveryPanel.astro`, adaptierte `ui-components`, PWA-Registrierung | Resilienzvertrag, Plattform-Offline 5/5, IUM5-Offline 3/3, Fail-closed-Update | Keine reale Unterbrechungs-/Speicherstörung auf Endgerät | Betriebssystem-, Quota- und reale Cachefehler außerhalb der simulierten Fälle ungeprüft |
| Persistenz | `packages/ium-5-core-05/src/payload.ts`, `experience-state.ts`, `tests/fixtures/ium5-payload-v1.json` | Schema-2-Payload, Version-1-Migration, atomarer Import, Export/Löschen/Wiedereinstieg; 4/4 State-Tests | Persistierter Inhalt und Nichtpersistenz von Hilfen im Diff geprüft | Langzeitmigration über weitere zukünftige Versionen nicht vorweggenommen |
| Lehrkraftorchestrierung | `TeacherCheckpoint.astro`, `RoleExchange.astro`, `SharedHold.astro`, `lehrkraeftehandbuch.md` | Checkpoint-Vertrag sowie lokaler Browserablauf ohne Konto, Fernsperre oder Telemetrie | Kein realer Klassendurchlauf | Zeitfenster, Rollenwechsel und neutrale Evidenz benötigen Unterrichtserprobung |
| Portabilität | generisches Paket, `ium5-semantic-adapter.astro`, `learning-experience.astro` | Fachfremdes Fixture und injizierte IUM5-Renderer in Chromium, Firefox und WebKit; Boundary- und Negativscans | Architekturreview bestätigt Generalisierung von Beziehungen statt Raster/Laufspur | Quellenanalyse, Datenmodellierung und Medienproduktkritik sind noch keine vollständigen Produktionsmodule |
| Produktion | `verify-learning-experience.ts`, `verify-ium5.ts`, `docs/architecture/`, `docs/quality/ium5-acceptance-matrix.md` | 9/9 Experience-Prüfungen, 25/25 IUM5-Gesamtverifier, Build-/Lizenz-/Regressionstests | Scope-, History- und Artefaktreview: 101 LXP05-Dateien, keine Vault-Datei, sauberer Worktree | Fach-, Accessibility- und Engineeringreview durch Menschen sowie alle Einsatzgates bleiben getrennt |

## Frische Qualitätsleiter am Reviewgate

Alle Befehle liefen am 5. August 2026 sequenziell vom sauberen Commit `26890a1`; jeder Befehl endete mit Exitcode `0`.

| Nr. | Befehl | Ergebnis |
|---:|---|---|
| 1 | `npm run contracts:check` | generierte Verträge bytegleich |
| 2 | `npm run boundaries:check` | 8/8 Workspace-Grenzen bestanden |
| 3 | `npm run typecheck` | TypeScript-Projektverbund fehlerfrei |
| 4 | `npm run test:platform` | 34 Dateien, 213/213 Tests bestanden |
| 5 | `npm run test:python` | 669/669 Tests bestanden |
| 6 | `npm run build` | Produktionsbuild bestanden |
| 7 | `npm run test:browser` | 18/18 Tests in Chromium, Firefox und WebKit bestanden |
| 8 | `npm run test:accessibility` | 12/12 Tests bestanden |
| 9 | `npm run test:offline` | 5/5 Tests bestanden |
| 10 | `npm run test:ium5:browser` | 45/45 Tests in Chromium, Firefox und WebKit bestanden |
| 11 | `npm run test:ium5:state` | 4/4 Tests bestanden |
| 12 | `npm run test:ium5:accessibility` | 15/15 Tests bestanden |
| 13 | `npm run test:ium5:offline` | 3/3 Tests bestanden |
| 14 | `npm run verify:experience` | 9/9 Experience-Prüfungen bestanden |
| 15 | `npm run verify:ium5` | 25/25 fail-fast-Schritte bestanden; darin Astro 0 Fehler/0 Warnungen/0 Hinweise, 648 Lizenzkomponenten ohne ungültigen Befund |

Die absichtlich erzeugten negativen IUM11-Testmeldungen innerhalb der Python-Suite gehören zu erwarteten Fail-closed-Testfällen; die Suite endet mit `OK` und 669/669 bestandenen Tests.

## Implementierungsentscheidungen und Grenzen

- `BaseLayout` besitzt weiterhin den einzigen `<main>`-Landmark der Seite. Deshalb ist `FocusStage` eine eindeutig beschriftete und fokussierbare `<section>` und `ExperienceShell` erzeugt keinen verschachtelten zweiten `<main>`. Das erfüllt die normative Ein-Main- und Fokusanforderung, auch wenn ein isoliertes Planbeispiel `FocusStage` als `<main>` skizziert hatte.
- Start- und Wiedereinstiegskomponenten akzeptieren eine kontextabhängige Überschriftenebene. In der IUM5-Modulroute bleibt genau eine Seitenüberschrift Ebene 1; die Experience-Abschnitte folgen auf Ebene 2.
- Die Belegkarte persistiert genau sechs fachliche Felder. Quellen- und Belegreferenzen verweisen auf autoritative Spuren; Klicks, Zeiten, Versuche, Hilfe-, Scroll-, Fokus- und Playbackdaten werden nicht gespeichert.
- Lehrkraftorchestrierung bleibt lokal und transparent. Es gibt keine Accounts, Gerätefernansicht, Fernsperre, Telemetrie oder geteilte Echtzeitsitzung.

## Reviewgate

Der Ausführungsplan enthält 82/82 abgeschlossene Arbeitsschritte und keinen offenen Schritt. Offen ist ausschließlich die ausdrückliche schriftliche Annahme dieses LXP05-Implementierungsergebnisses oder die Benennung konkreter Änderungen. Integration und jede Einsatzphase erfordern einen neuen, ausdrücklich autorisierten Schritt.
