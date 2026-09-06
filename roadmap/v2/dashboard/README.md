# IUM-V2-DASH – lokales Projektcockpit

Das Dashboard wurde aus dem freigegebenen Dashboardvertrag neu aufgebaut. Der historische Commit `07bc15e1e70d` ist nicht verfügbar und wird weder rekonstruiert noch als GitHub-Beleg ausgegeben. Maßgeblich sind die V2-Spezifikation vom 3. September 2026, der redaktionelle Statusblock im Vault und die 18 in `gates.json` benannten Task-Notizen.

## Lokal verwenden

Im Repository mit Node 22.12 oder neuer innerhalb der 22er-Linie und den bereits installierten Lockfile-Abhängigkeiten:

```powershell
npm run dashboard:check
npm run dashboard:update
npm run dashboard:preview
```

Die Präsentation läuft ausschließlich auf `http://127.0.0.1:4324/`. Die Vorschau erzeugt einen neuen Snapshot und einen eigenen statischen Build. `dashboard:update` aktualisiert zusätzlich das Obsidian-Cockpit. Nach Änderungen an Register, Task-Status oder Belegen neu ausführen; ein geöffneter statischer Build aktualisiert sich nicht selbst. Eine parallel laufende Vorschau vorher im zugehörigen Terminal beenden.

```powershell
npm run dashboard:preview -- --mode internal --port 4325
npm run dashboard:build
npm run test:dashboard
npm run test:dashboard:browser
```

`--vault-root` überschreibt `IUM_VAULT_ROOT`, das wiederum den Workspace-Standard überschreibt. `--register` kann eine andere Registerdatei auswählen; sämtliche Belegpfade bleiben an die erlaubten Repo-/Vault-Wurzeln gebunden. Unbekannte Optionen und Modi sind Fehler. `editorial-seed.json` dokumentiert den redaktionellen Migrationsstand für Tests und Wiederaufbau; Änderungen im Alltag erfolgen im Vault-Register, nicht in beiden Dateien. Für einen anderen Rechner werden der Registerblock und die in `gates.json` benannten Notizen benötigt. Es gibt keinen stillen Rückfall auf den Test-Seed.

## Acht Ansichten

Überblick, Baselines, Grundlagen, Lern-Experience, Übernahmeaudit, Jahrgänge, Gates und Evidenz. Belege öffnen auf zusätzlichen statischen Quellseiten. Der Quelltext wird unverändert als Text dargestellt, nicht als aktives HTML ausgeführt. Die Präsentation enthält nur ausdrücklich ausgewählte Präsentationsbelege. Ein interner Build ist eine eigene Ausgabe und keine per CSS versteckte Variante der Präsentation.

## Aussagegrenzen

- V1 bleibt aktiv und archivierte Referenz; V2 ist `building`. LXP05 bleibt eingefroren und ungemergt. Produktion, Cutover, Pilot und Veröffentlichung bleiben geschlossen.
- Fünf Stränge besitzen acht getrennte Reifeachsen; die Lern-Experience besitzt acht Unterachsen. Es gibt keine Gesamtprozentzahl und keine Gesamtampel.
- Nutzerabnahmen von R5/R6/R7 werden über eigene Acceptance-Belege und die aktuellen Task-Notizen sichtbar. Historische Prüfsnapshots werden dafür nicht umgeschrieben.
- R7-Pfade, Kapazitätschecks sowie sechs übernommene und drei neue offene Nachweisfragen stammen aus den unveränderten Jahrgangsdaten. Bedarf wird nicht als tatsächliche Verfügbarkeit ausgewiesen.
- Technische Nachweise bleiben an vollständige Commits gebunden. Ein anderer Checkout zeigt `stale`; ein veränderter Checkout erhält zusätzlich eine eigenständige Warnung. Beides ändert keine fachliche Reifeachse.
- GitHub-Beleglinks erfordern einen vollständigen lokalen Quellcommit, gleiche normalisierte Dateiinhalte und Erreichbarkeit über vorhandene `origin`-Referenzen. Nachweisstand ist der letzte Fetch; es gibt keine automatische Onlineprüfung. Nicht gepushte Belege bleiben lokal auflösbar und zeigen Commit sowie Inhaltsdigest.

## Fehler und Ausgaben

Ungültige Statuswerte, doppelte IDs, fehlende Pflichtstränge/Achsen/Gates, interne Belege in Präsentationsreferenzen, fehlende Pflichtquellen, Pfadüberschreitungen und veränderte akzeptierte Jahrgangspläne stoppen die Projektion. Optionale historische Quellenlücken bleiben Warnungen. UTF-8 wird für Belegtexte strikt geprüft; absolute lokale Pfade sind nicht zulässig.

Alle Quellen werden validiert und beide Projektionen vollständig vorbereitet, bevor `dashboard:update` eine Datei ersetzt. Jede Dateiersetzung erfolgt atomar über eine benachbarte temporäre Datei. Bei gescheiterter Snapshot-Ersetzung wird eine vorhandene Obsidian-Ausgabe zurückgesetzt. Die zwei Dateien bilden keine Dateisystemtransaktion bei Stromausfall; ein erneutes Update stellt die gemeinsame Projektion wieder her. Ungültige Quelldaten lassen beide bisherigen Ausgaben unverändert.

Snapshots, zeitlich getrennte Präsentations-/Arbeitsbuilds, Browserberichte und PDFs liegen unter ignoriertem `dist/` beziehungsweise `reports/`. Nur das Markdown-Cockpit wird in den Vault geschrieben. `latest-presentation.json` bzw. `latest-internal.json` wird erst nach erfolgreichem Build atomar aktualisiert. Fehlgeschlagene Builds ersetzen keinen letzten erfolgreichen Build. Alte Buildverzeichnisse werden nicht automatisch gelöscht.

## Prüfumfang

Siehe [Validierungsbericht](validation-report.md). Browsergates verwenden einen vom Test-Runner selbst gestarteten, lokal gebundenen Prozess und beenden genau diesen Prozess nach dem Lauf. Damit hängt die Windows-Ausführung nicht von der Prozessbaum-Bereinigung einer zusätzlichen Shell ab. Die Tests öffnen keine externe Seite. Ein manueller Klick auf einen ausgewiesenen GitHub-Beleg ist eine bewusst ausgelöste Navigation.

Nach DASH-Abnahme folgt ausschließlich die gesonderte Entscheidung IUM-V2-CUT. Die drei Audit-Folgeaufträge benötigen ihre eigenen Abhängigkeiten und Aufträge.
