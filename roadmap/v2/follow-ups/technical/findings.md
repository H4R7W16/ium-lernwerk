# FU-TECH – Befunde und Nacharbeitskriterien

Geprüfter Stand: `32b523a657a3e6717a83fd9aaa755c8deed9adbf`. Alle acht Befunde sind offen. „Hoch“ bedeutet Sperre der betroffenen technischen Wiederverwendung; es ist keine Behauptung eines bereits eingetretenen realen Schadens. Synthetische Probes, Codeinspektion und Umgebungsausfälle werden getrennt geführt.

## TECH-F01 – lokaler Start umgeht die Importprüfung (hoch)

`packages/module-runtime/src/runtime.ts`, `start()` und `previewImport()`; `packages/module-runtime/src/migrations.ts`, `migrateStateCopy()`.

**Beobachtung:** Ein lokal gespeicherter Stand mit Modulversion 1.0.0 wird von einer Runtime 2.0.0 bei gleichem Payloadschema geöffnet. Dieselbe exportierte Datei wird als nicht unterstützte Modulversion abgelehnt. Ein lokal gespeicherter Stand mit ungültigem `savedAt` wird bei unverändertem Schema ebenfalls akzeptiert. Der Migrationshelfer validiert nur nach tatsächlichen Migrationsschritten. Beides im Befundlauf reproduziert.

**Folge:** Gleiche Daten haben je nach Eingangsweg unterschiedliche Gültigkeit. Ein V2-Adapter darf lokale Altstände nicht ungeprüft interpretieren. Der IUM5-Controller prüft zwar seine Payload, ersetzt damit aber keine vollständige Hüllen-/Versionsprüfung.

**Nacharbeit M02:** Vor jeder Aktivierung Hülle, Modulidentität, unterstützte Modulversion, Zustandsschema und modulbezogene Payload prüfen. Supportmatrix explizit festlegen; nicht durch Gleichsetzen von Modulversion und Schema ersetzen. Prüfungen für ältere/neuere/falsche Modulversion, identisches Schema, ungültige Hülle sowie erfolgreiche und fehlende Migrationspfade. Ablehnung muss den gespeicherten Originalstand erhalten.

## TECH-F02 – Original bleibt bei Migrationsfehler nicht über die Runtime exportierbar (hoch)

`runtime.ts`, `start()`/`exportState()`; V1-Spezifikation Abschnitt 15.

**Beobachtung:** Fehlt der Schritt Schema 1 → 2, bleibt das gespeicherte Original unverändert. `start()` liefert Fehler, setzt aber keinen exportierbaren Recoveryzustand; `exportState()` benötigt `#active` und schlägt anschließend fehl. Die Fehlermeldung empfiehlt dennoch den Originalexport. Synthetisch reproduziert; keine reale Datei verloren.

**Nacharbeit M02:** Unveränderliches Original gesondert als Recoverydaten halten und bewusst ausgeben, ohne den aktiven Zielzustand als gültig zu setzen. Auch bei Loadfehlern einen verständlichen, nicht destruktiven Weg vorsehen. Test: Migration wirft/fehlt/liefert ungültige Payload; Originalexport gelingt byte- bzw. inhaltsgetreu, kein vorzeitiges Überschreiben, Wiederholung und Abbruch funktionieren.

## TECH-F03 – ungültiger Folgeimport entwertet alten Preview nicht (mittel)

`runtime.ts`, `previewImport()`/`confirmImport()` und Pending-Lebenszyklus.

**Beobachtung:** Gültigen Import vorprüfen, anschließend ungültiges JSON vorprüfen, dann `confirmImport()` aufrufen: Die Runtime bestätigt den alten Preview. Synthetisch reproduziert. `deleteActive()` leert Pending ebenfalls nicht. Es gibt keine explizite Runtime-Abbruchoperation.

**Begrenzung:** Der heutige IUM5-Controller setzt bei Fehler/Abbruch `pendingPayload = null` und schützt den normalen Bestätigungsweg. Der Probe belegt einen Mangel des generischen Runtimevertrags, keinen nachgewiesenen UI-Importfehler dieser Werkstatt.

**Nacharbeit M02:** Jede neue Vorprüfung beginnt mit Entwertung des bisherigen Kandidaten. Expliziter Abbruch; bei Löschen und Sitzungswechsel ebenfalls entwerten. Bestätigung an den aktuell validierten Kandidaten binden. Negative Sequenztests für Fehler, Abbruch, Löschen und erneutes Bestätigen ergänzen.

## TECH-F04 – ein Modulslot ohne Konflikt- und Mehrtab-Löschschutz (hoch)

`packages/local-state/src/indexeddb-repository.ts`, Store `activeStates`, `keyPath: 'moduleId'`; `runtime.ts`, `flush()`.

**Beobachtung:** Die Datenbank `ium-lernwerk` Version 1 hält pro Modulkennung einen Stand; `workspaceId` ist kein Speicherschlüssel. Zwei Runtimeinstanzen können nacheinander denselben Stand laden. Nach einer neuen Speicherung A überschreibt die veraltete Instanz B ihn erfolgreich, ohne Konflikthinweis. Am gemeinsamen Memory-Speicherport reproduziert; IndexedDB verwendet denselben modulbezogenen Ersetzungsvertrag.

**Folge:** Mehrtabbetrieb, Versionen auf derselben Origin und geteilte Browserprofile sind nicht gegeneinander isoliert. Nach globalem Löschen kann ein anderer noch aktiver Client seinen alten Stand erneut schreiben. Diese Löschfolge wurde per Code abgeleitet, nicht als reale Mehrtabprüfung ausgegeben.

**Nacharbeit M03:** Explizites Eininstanz-/Mehrinstanzmodell wählen. Bei gemeinsamer Nutzung Revision/Lease oder gleichwertige Konfliktprüfung und Löschinvalidierung vorsehen; Namespace-/Profilentscheidung dokumentieren. Tests mit zwei echten Browserkontextseiten, konkurrierendem Schreiben, globalem Löschen, Reopen, Modulversionswechsel und gemeinsamem Profil; keine stille Datenüberschreibung.

## TECH-F05 – dokumentierte Speicherwahl und wirklicher Datenfluss weichen ab (hoch)

`docs/platform/README.md` beschreibt Schreiben erst nach bewusster Zustimmung. `workbench-controller.ts` wählt ohne `?storage=volatile` unmittelbar `persistent`, ruft `start()` auf und speichert die Initialpayload. Der Kataloglink und die Modulroute enthalten davor keine Speicherentscheidung. Das ist ein Code-/Dokumentwiderspruch; keine Behauptung eines bestimmten Rechtsverstoßes.

Der Repositorymodus `persistent` bezeichnet einen erfolgreichen IndexedDB-Pfad, keine erteilte `navigator.storage.persist()`-Garantie. `browser-ports.ts` versucht im Kopierfallback außerdem `navigator.clipboard.writeText(value)`. Download und Clipboard sind zusätzliche Ablagen außerhalb der globalen App-Löschung.

**Nacharbeit M01/M03:** Vor erstem Schreibvorgang einen nachvollziehbaren Speicherwahlvertrag umsetzen und Texte daran ausrichten. Eviction, Fremdzugriff im Profil, Export, Clipboard und Gerätesync transparent behandeln. Test: Erstaufruf im frischen Profil erzeugt vor der vorgesehenen Wahl keinen Lernstand; flüchtiger Pfad bleibt flüchtig; Fehler-/Quota-/Downloadblockaden zeigen korrekte Optionen. Zuständige Stelle klärt den konkreten Betrieb gemäß GOV.

## TECH-F06 – erfolgreicher Flush ist bei flüchtigem Modus keine Updatesicherung (hoch)

`apps/lernwerk-portal/src/controllers/pwa-registration.ts`, `flushActiveRuntimes()`/`activateAfterFlush()`; `workbench-controller.ts`, `flush()`; Memory-Adapter.

**Beobachtung:** Ein Memory-Flush liefert erfolgreich, der Stand fehlt jedoch in einer neuen Sitzung. Die Updateorchestrierung wertet nur die Boolean-Flushantworten des aktuellen Dokuments aus und ruft anschließend den Service-Worker-Updater mit Reload auf. Diese zusammengesetzte Verlustgefahr ist aus Code und synthetischem Memory-Neustart belegt; kein behaupteter realer iPad-Updatelauf.

Zusätzlich liegt `Promise.all(pending)` vor dem try/catch für die Aktivierung; eine abgelehnte Flush-Promise wird nicht in die vorgesehene Speicherfehlermeldung übersetzt. Offene andere Tabs werden hier nicht koordiniert.

**Nacharbeit M04:** Wiederherstellbarkeit ausdrücklich prüfen. Bei flüchtigem Zustand Export/fortgesetzte Sitzung/Abbruch anbieten und Verlust nicht als gesichertes Update darstellen. Tests: volatile-selected, volatile-fallback, Quota, Promise-Rejection, zwei offene Clients, vollständiger und defekter Kandidat; fachliches Lernprodukt nach Update erhalten oder Update nachvollziehbar abgebrochen.

## TECH-F07 – Manifest, Registry und Moduladapter bilden noch V1 ab (hoch)

`schemas/module-manifest.schema.json`, `scripts/build-module-registry.ts`, Modulroute und IUM5-Adapter.

**Beobachtung:** Manifestschema 1 enthält alte Status-, Zeit- und Lernmaterialfelder. Der Build akzeptiert als Produkt nur den fest codierten IUM5-Renderer und lädt die historischen Curriculumdateien. Für `production` wird `countsTowardCoverage` auf true gesetzt, ohne V2-Nachweisprüfung. Dieses interne V1-Flag ist keine tatsächlich erfüllte V2-Coverage. Die Modulroute unterscheidet nur `working` von der sonstigen synthetischen Referenzanzeige.

Die Payload/Resources verwenden elf Kernphasen plus `ue6-extension`, feste Szenario-/Transferkennungen und die V1-Zeit-/Materialkomposition. Der Controller setzt Schema 1 und `migrations: []`. Demgegenüber verlangen LXF04–06 flexible Lernfunktionen und explizite Produkt-/Hilfs-/Feedback-/Wiedereinstiegsbindungen.

**Nacharbeit M07/M05:** Aus freigegebenem FU-MOD-Design einen V2-Manifest-/Adaptervertrag ableiten. V1-Module und Auslieferung separat erhalten; keine pauschale Anhebung alter Status- oder Coveragewerte. Tests für fremde/alte Manifestversion, falsche Baseline, ungeprüfte Coveragebelege, fehlende LXF-Verweise und falsche Renderer-/Payloadversion. Interpreter, Parser und Editor sind nur unter ihrer tatsächlichen Semantik selektiv übernehmbar.

## TECH-F08 – aktuelle technische Zielmatrix bleibt unvollständig (mittel)

Lokaler Prüfstand Node 22.23.2/npm 10.9.8 entspricht dem `engines`-Bereich; die Workflowdateien pinnen weiterhin 22.20.0. Der vorhandene CI-Vertrag enthält keinen expliziten V2-/Aktivierungs-CLI-Aufruf (Pythonregression ist vorhanden). Ein neuer V2-Auslieferungsstand braucht seine eigene vollständige Gatebindung.

Im aktuellen Prüflauf scheitert Firefox bereits bei `browserContext.newPage` mit `Cannot read properties of undefined (reading '_page')`. Derselbe Fehler ist mit leerem Browserkontext ohne Projektseite reproduziert. Das ist ein reproduzierbarer Fehler des lokalen Firefox-/Playwright-Prüfpfads; genaue Umgebungsursache ungeklärt, weder Produktfehler noch bestandener Firefox-Nachweis behauptet. Der hängen gebliebene vollständige Lauf wurde nach allen sechs Firefoxfehlern beendet; übrige Prüfbereiche wurden getrennt weitergeprüft.

**Nacharbeit M05/M06:** Toolchain und Firefoxprüfpfad reparieren/angleichen, dann vollständige Zielmatrix erneut ausführen. Verwaltetes iPad, Safari, MDM, Schulnetz, tatsächliches LMS und VoiceOver bleiben eigenständige reale Prüfungen. Historische iPad-Teilbefunde vom 03.08.2026 betreffen andere Kandidaten und schließen das V2-Gate nicht.

**Erweiterte WebKit-Prüfung:** Die IUM5-Werkstatt-, Zustands- und Accessibilityfälle wurden zusätzlich gemeinsam auf Chromium und WebKit ausgeführt: 53 bestanden, fünf WebKitfälle fehlgeschlagen. Die fünf Fälle wurden anschließend mit einem WebKitworker einzeln nachgeprüft: vier bestanden, die Fokusprüfung nach Klick auf „Gehe einfügen“ schlug erneut fehl. Die vier schwankenden Fälle betreffen zwei Importwarnungen, Tastaturablauf und Zielgrößenprüfung; ihre Ursache bleibt offen. Beim Fokusfall erwartet der Test Fokus nach einem Pointerklick, während der Insert-Handler keinen expliziten Fokus setzt. Diese Abweichung zur Testerwartung ist reproduziert; sie wird ohne getrennte Tastatur-/Browseranalyse nicht pauschal zum WCAG-Verstoß erklärt. Auch der zweite Lauf macht den ersten nicht rückwirkend grün.

**Statusprojektion:** `packages/project-status/index.mjs` bildet `followUps` aus dem versiegelten AUD-Plan weiterhin pauschal als `blocked` ab. FU-TECH wird deshalb in aktueller Task, Registerfokus, nächster Entscheidung und Obsidian-Cockpit korrekt als `review` geführt. Der globale technische Dashboardnachweis bleibt der frühere Aktivierungsnachweis. Eine aktuelle HTML-Nachfolgerprojektion braucht eine separate, testgestützte Migration des Statuslesers mit Erhaltung der historischen Siegel; sie ist keine V2-Produktfreigabe.
