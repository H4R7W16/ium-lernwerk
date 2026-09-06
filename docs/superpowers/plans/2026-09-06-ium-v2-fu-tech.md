# IUM-V2-FU-TECH – technischer Prüfplan

**Ziel:** Dateigenaue Übernahmeentscheidungen für IUM04, IUM12, IUM13 und IUM18 gegen die aktive V2-Baseline zur Nutzerabnahme vorbereiten.

**Architektur:** Additiver Audit unter `roadmap/v2/follow-ups/technical/`; versiegelte AUD-/CUT-/Aktivierungsinputs bleiben unverändert. Der Auftrag prüft und spezifiziert Migrationen, implementiert aber kein neues Lernmodul und keinen Produktwechsel.

**Technik:** Bestehende Python-, Vitest-, Playwright-, Build- und Lizenzprüfungen; Markdown-Lesefassung und JSON-Dateiinventar mit SHA-256. Keine neue Abhängigkeit.

**Spezifikation:** Workspace-Task IUM-V2-FU-TECH und historischer Eintrag in `roadmap/v2/audits/follow-up-tasks.json`; V2-Anforderungen, GOV und LXF04–06.

## Grenzen

- Ausgangscommit `32b523a657a3e6717a83fd9aaa755c8deed9adbf`, bestehender sauberer Feature-Branch `feat/ium-v2-rebaseline`. Nur additive Auditdateien; kein Bedarf an einem weiteren Checkout für Produktänderungen.
- Reale Geräte-/Netzprüfung und institutionelle Rollen bleiben unbestätigt; keine Nachweise erfinden.
- Keine automatische LXP05-Übernahme, Modulproduktion, Pilotierung, Veröffentlichung, Push oder Merge.
- Historische Nachfolgestatus bleiben historische Snapshots. Aktueller Auftrag und Review werden separat geführt.

## Schritte

- [x] Auftrag, CUT-Abhängigkeit und Git-Ausgangsstand prüfen; Task und Kanban übernehmen.
- [x] Technische Primärdateien lesen: Verträge, Laufzeit, Speicher, Import/Export, Updatefluss, Build/Workflows, Interpreter und Moduladapter. V2- und GOV-Bezüge notieren.
- [x] Aktuelle Primärdokumentation zu Browserpersistenz, Service Worker, Laufzeitversion und Accessibility anlassbezogen prüfen; Quellen und Aussagegrenzen dokumentieren.
- [x] Bestehendes vollständiges `npm run verify:ium5` unter der projektspezifizierten Node-22-/npm-10-Laufzeit ausführen und Ausgabe außerhalb des Vaults sichern. Enthält Plattform-, Browser-, Offline-, Accessibility- und Pythonprüfungen. Anschließend V2-/Aktivierungsvalidator mit tatsächlichem Vault prüfen.
- [x] `roadmap/v2/follow-ups/technical/README.md`, `inventory.json` und `validation-report.md` erstellen: dateigenaue Entscheidungen, Migrationsreihenfolge, technische Findings und gesperrte Betriebsfragen.
- [x] Inventar auf Dateiexistenz, eindeutige Pfade, SHA-256, vollständige Familien-/Primärbelege und auflösbare Referenzen prüfen; Audit gegen alle Akzeptanzkriterien selbstreviewen.
- [x] Task in `review`; Initiative, Kanban, Projektstatus, generiertes Dashboard und Session Summary aktualisieren. Historische 18 Gates bleiben abgeschlossen.
- [x] Vor lokalem Commit `git fetch --prune` und `git pull --ff-only`; nur Audit-/Statusänderungen aufnehmen. Commit und nicht erfolgten Push dokumentieren.

## Übergabe

Prüfurteil als KI-Selbstreview mit konkreten Befunden und verifizierten Grenzen; fachliche Nutzerabnahme bleibt eigener letzter Schritt. FU-MOD und FU-PILOT erhalten durch dieses Audit keinen Ausführungsauftrag.

## Ausführungsergebnis

Audit in review. 52 Dateien, acht offene Befunde, sechs synthetische Beobachtungen. Die vollständige IUM5-Kette blieb bei Firefox unvollständig; Teilnachweise, gezielte Nachläufe und WebKitunsicherheiten stehen im Validierungsbericht. Keine Produktmigration. Lokaler Commit und finales Git-Ergebnis stehen im Session-Handoff.
