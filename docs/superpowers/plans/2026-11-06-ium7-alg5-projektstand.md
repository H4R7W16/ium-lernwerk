# ALG-5 Projektstand Implementation Plan

> For agentic workers: Use superpowers:subagent-driven-development / executing-plans. Dieser Plan wird im bestehenden isolierten Worktree ausgeführt; keine Löschung von Plan-/Prüfdateien.

**Goal:** Eigene ALG-5-Snap-Projekte bewusst in einer Arbeitskarte übernehmen, genau diesen Stand wiederöffnen und zusammen mit der Übersicht mitnehmen.
**Architecture:** Versionierte optionale Projektkopie nur an ALG-5-Karten. Parent-Übersicht besitzt Speicher/Import/Export; ein eigener same-origin iframe nutzt einen eng abgeleiteten Lernwerk-Snap-Editor. Originale gebundene Snap-/Fachquellen bleiben unverändert; der Adapter erhält Zugriff auf die vorhandene korrekte Serialisierung und kontrollierte Öffnung.
**Tech Stack:** Node22, CommonJS/UMD, native Browser-APIs, vorhandenes Snap; keine neue Laufzeitabhängigkeit.
**Spec:** Angenommener Vorschlag im Chat und ausdrücklicher Umsetzungsauftrag; Konzept1.1 unter Vault/40_Projekte/IuM-Lernwerk/2026-11-06 - Konzept Deine Arbeit Klasse 7.md (Stufe2). Entscheidungen unten sind Umsetzungskonkretisierungen innerhalb dieses Auftrags.

## Global Constraints

- Ausschließlich ALG-5 enthält Projektstände; alle anderen Karten und Jahrgänge funktionieren weiterhin.
- Projekt bewusst übernehmen; Zeitpunkt anzeigen; echte eigene Datei/Editorstand von Startprojekt unterscheiden.
- Ein Stand je Karte, erneute Übernahme ersetzt bewusst diesen Stand; kein Hintergrundabgleich externer Dateien.
- V1-Übersichten lesen; V2 trägt optional project {format:snap-project,version:1,xml,filename,savedAt}; alte Daten erhalten, Import vollständig/atomar prüfen.
- Snap-XML höchstens10MiB wie vorhandener Editor; Übersichtspaket höchstens32MiB; Speicherquota kann früher greifen und führt zu ehrlicher RAM-/Exportführung.
- Herkunftsmanifeste nicht unabhängig von Quellen verändern. Neue Editor-Hülle/Runtime durch exakt geprüfte Ableitung; originale Snap-Dateien bleiben bytegleich.
- Kein automatisches Ausführen importierter Projekte. Prüfung der XML-Struktur und tatsächliche Snap-Ladeprobe; gespeicherter Stand ist kein fachlicher Erfolgsnachweis.
- Nutzerauftrag umfasst Umsetzung/Prüfung; Veröffentlichung dieser Erweiterung ist nicht beauftragt.

## Review Focus

1. Native XML-Dateiöffnung setzt Snap-dirty zurück: andere Scene muss trotzdem als noch nicht in Arbeitskarte übernommen erkannt werden.
2. Editoränderung während Übernahme: nur passende erfasste Revision als übernommen markieren.
3. Große Projekte/Quota/anderer Tab: keine unbemerkte Verdrängung; RAM-Stand exportierbar und bestehende Kopien geschützt.
4. Falsche/beschädigte Datei oder Ladefehler: alter Stand und Übersicht bleiben erhalten; keine falsche Erfolgsmeldung.
5. Rückkehr mit Starter statt eigenem Projekt: eindeutige Dateiauswahl/Startaktion, Dateiname/Zeit und echte Wiederöffnungsprobe mit verändertem Projekt.

## Task1 – Modell und Speicher (alg5_projekt_modell)

Files: prototypes/shared/work-overview-model.js, work-overview-storage.js, zugehörigeTests; ggf.snap-project-model.js/.test.cjs.
Interfaces: validateProject(project), setProject(store,cardId,project,catalog), removeProject(store,cardId,catalog,now); Result {ok,store,card,error}; MAX_BYTES, MAX_PROJECT_BYTES. save erhält bestehendes Projekt bei Hinweisänderung.
- [ ] Tests zuerst rot: V1→V2, Projekt nurALG5, Erhalt bei Edit/Import, invalid/overlimit atomar.
- [ ] Modell implementieren und Tests grün.
- [ ] Quota-/Konflikt-/beschädigteCopy-Tests mit Projektständen.

## Task2 – Echter Snap-Adapter (alg5_snap_anbindung)

Files: neue prototypes/klasse7-jahrgang/snap-projekt-adapter.cjs, snap-projekt-bridge.js, snap-projekt-adapter.test.cjs.
Interfaces: addSnapProjectEditor(pages)->Map; neue URL klasse7/programmieren/snap/arbeit.html; window.LernwerkProjectBridge ready,getSnapshot()->{xml,name,revision},openProject(xml,options)->Promise,isDirty(),markSaved(revision)->boolean.
- [ ] Tests zuerst rot: Ausgangsquellen unverändert, Hook exakt einmal, readiness/dirty/scenechange/revisionguard/rollback.
- [ ] Abgeleitete Hülle und Adapter implementieren, nurALG5; JS im Projekt deaktiviert.
- [ ] Tests grün, fachliche Serialisierung samt ursprünglichen Blockfiltern erhalten.

## Task3 – Verständliche Bedienung (Root)

Files: neue work-overview-projects.js samtTests; work-overview.js/.css; arbeit-seite.cjs/arbeit-adapter.cjs undjeweiligeTests.
- [ ] Verhaltenstests zuerst rot: keine Übernahme vor erfolgreichem Laden; bestehendeKarte erhältHinweise; unsavedclose/cancel; klarePaketinhalte.
- [ ] Karte zeigt Projektname/Übernahmezeit, Projekt hinzufügen/weiterbearbeiten/XMLexport/gezieltesEntfernen.
- [ ] Dialog mit eigenerDateiauswahl oder ausdrücklichStartprojekt, echtemEditor, Übernehmen undÜbersichtmitProjektmitnehmen.
- [ ] Speicherstatus, Hilfe, Importvorschau undDrucktexte entsprechen tatsächlichenInhalten.

## Task4 – Integration, echte Wege und Abschluss

- [ ] Frischer Vollbuild und komplettePagesTests; vollständig gegenBaseline vergleichen, erlaubteÄnderungsliste.
- [ ] EigenesverändertesALG5Projekt importieren, übernehmen, neuöffnen, ändern, erneutübernehmen, Paketexport, andererBrowserSpeicherimport, Projekt+Testfall wiederfinden.
- [ ] Fehl-/Abbruchwege, NativeDateiöffnen, Quota/Größenfälle, alteV1Datei, DAT1Erhalt; schmaleAnsicht undTastatur; Druckmetadatenprüfung.
- [ ] Unabhängiger Code-/UXReview, Nacharbeit, fassungsgebundener Qualitätszyklus.
- [ ] Commit/Push/Entwurfs-PR nachFetch/Pull; Task/Initiative/Kanban/Session aktualisieren; keinMerge/Deploy.


## Abschlussentscheidung · 07.11.2026

Die Implementierung der Aufgaben 1–3 ist erfolgt. Der statische Gegenreview mit gezielten Regressionen ist abgeschlossen; sechs Befunde (R1, R1a, R2–R5) wurden korrigiert und 27 gezielte Tests bestanden. Der tatsächliche Browserdurchlauf wurde nach einem entdeckten und korrigierten iframe-Layoutfehler durch Grenzen der Computersteuerung unterbrochen. Die vollständige reale XML-/Paket-Rücksicherung sowie die schmale Tastaturansicht dieser Erweiterung sind dadurch nicht nachgewiesen.

Jan entschied am 07.11.2026 ausdrücklich: „wir gehen davon aus, dass es funktoniert.“ Die noch offene praktische Endprüfung wird damit als akzeptierte Annahme dokumentiert und nicht weiter blockierend verfolgt. Die vorstehenden offenen Browser-Prüfpunkte werden nicht rückwirkend als bestanden markiert. Es gibt weder einen vollständigen grünen Browsernachweis noch eine empirische Lernendenerprobung. Ein formaler Inhalts-Qualitätspass wird daraus nicht abgeleitet; fachliche Aufgaben und Zeitplanung wurden nicht geändert.

Abschlussumfang: frischer integrierter Pages-Testlauf/Build, Vergleich gegen aktuellen main, versionierter Quellstand und Entwurfs-PR. Kein Merge oder Deployment dieser Stufe. Der spätere Publikationsauftrag muss diese benannte Prüfgrenze mitführen.
