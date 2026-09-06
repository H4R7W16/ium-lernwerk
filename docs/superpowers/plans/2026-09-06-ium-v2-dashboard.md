# IUM-V2-DASH – Umsetzung der freigegebenen Dashboardverträge

Grundlage: V2-Spezifikation vom 3. September, Abschnitt 14/15, sowie DASH02/DASH04 mit freigegebenem Statusmodell und acht statischen Astro-Ansichten. R7 ist ausdrücklich angenommen. Historischer Dashboard-Commit nicht vorhanden; Neuaufbau auf feat/ium-v2-rebaseline. Keine zusätzliche Architekturfreigabe erforderlich. Keine parallelen Agenten.

- [x] R7-Freigabe dokumentieren, DASH übernehmen und Bestand prüfen.
- [x] Redaktionelles Register auf V2 migrieren; 18 Gates, fünf Stränge, acht Reifeachsen und acht Experience-Unterachsen mit Evidenz binden.
- [x] Fail-closed Vertrag testgetrieben entwickeln: Pflichtstränge, Statuswerte, IDs, Links, Sichtbarkeit, vollständige Git-SHAs, stale und dirty getrennt.
- [x] Atomaren Snapshot und Obsidian-Cockpit erzeugen; fehlerhafte Updates erhalten letzte gültige Dateien.
- [x] Eigenständige Astro-App mit acht Seiten, lokalen Belegseiten, Präsentationsfilter und Drucklayout aufbauen. Präsentationsbuild enthält keine internen Quellen. Keine externen Ressourcen.
- [x] Build, Navigation/Links, Accessibility, Mobil/Tablet, Tastatur, No-Network und Druck prüfen; visueller Selbstreview.
- [x] V2- und Python-Regression ausführen, Befunde schließen; keine Änderungen an versiegelten Vorgängerdateien.
- [ ] Fetch/Pull, lokaler Commit und überprüfbare Git-Provenienz; kein Push/Merge/Hosting.
- [ ] Dashboard auf sauberem Commit regenerieren; Task, Initiative, Board, Projekt, Entscheidung und Session auf DASH-Review übergeben. CUT wartet auf eigene Freigabe.

## Daten- und Aktualisierungsentscheidung

Das Statusregister bleibt redaktionelle Quelle. Ein enges Manifest benennt die 18 bestehenden Task-Dateien; deren Frontmatter ist der operative Gate-Stand. Versiegelte Statusdateien bleiben historische Prüfsnapshots, Akzeptanzbelege dokumentieren spätere Nutzerfreigaben. Repository-Evidenz wird mit Inhaltsdigest und dem tatsächlichen dateibezogenen Commit gebunden; GitHub-Links nur bei Erreichbarkeit über vorhandene origin-Refs und identischem Dateistand. Technische Commit-Frische ist eine eigene Angabe und verändert keine fachliche Reife.

App und Obsidian-Ausgabe werden aus demselben validierten Modell erzeugt. Statische Belegseiten liefern nur ausdrücklich als presentation markierte Quelltexte; interne Quellen werden vor dem Rendern entfernt, nicht per CSS versteckt. Alle Quellen bleiben lokal. Rohartefakte werden vor Aufnahme auf absolute lokale Pfade geprüft. Laufzeit- und Builddateien liegen unter ignoriertem dist/reports, keine Builddateien im Vault. Atomare Dateiersetzung erfolgt erst nach vollständiger Validierung; Snapshot ist die atomare Veröffentlichungseinheit, abgeleitete Ansichten sind reproduzierbar.

Der endgültige Git-Commit und die anschließende Vault-Übergabe werden nach dem Commit in der Session Summary dokumentiert; diese beiden Nachschritte erzeugen keinen selbstreferenziellen Commit.
