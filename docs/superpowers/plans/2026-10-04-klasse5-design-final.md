# Klasse 5 – freigegebenes Design abschließen

Auftrag vom 04.10.2026: Design übernehmen, keine weiteren inhaltlichen Änderungen.
Bestehender isolierter Worktree: feat/ium-identitaet-02, Basis 6cfd63e.

## Umfang

Nur prototypes/shared/identity.css ändern. Die bereits integrierte Wortmarke 02 und das bestätigte Klasse-5-Blau #2D52EE bleiben die Grundlage. Gemeinsame Akzentrollen zentral definieren; Typografie, Konturen, Abstände und mobile Zugangskarten verbessern. Alle Texte, Inhaltsdateien, HTML-Generatoren, Lernwege, Funktionen und fachlichen Medien bleiben unverändert. Keine neue Jahrgangsnavigation. Keine Veröffentlichung.

## Schritte

- [x] Arbeitsbereich und Git-Status prüfen; Quell- und Ausgabehashes vor Änderungen sichern.
- [x] Gemeinsame CSS-Gestaltung für Klasse 5 abschließen.
- [x] Statischen Mantel bauen, vorhandene Funktionsprüfungen ausführen, Inhaltserhaltung durch Hashvergleich nachweisen.
- [x] Desktop, Tablet und Mobilansicht bis 320 CSS-Pixel sowie Fachseite und Navigation im Browser prüfen.
- [x] Laufende Vorschau aktualisieren; Selbstreview, Nachweise und Session Summary dokumentieren.

## Prüfentscheidungen

Keine Tests für feste CSS-Werte ergänzen; sie würden die Umsetzung lediglich nachbilden. Vorhandene Produktprüfungen und Browserprüfung verwenden. Für Inhaltserhaltung unveränderte HTML-, JavaScript-, Inhalts- und Medienhashes prüfen. Im öffentlichen Build dürfen nur identity.css und der automatisch daraus abgeleitete Serviceworker wechseln. Im bestehenden Chat selbst reviewen, gemäß Repository-AGENTS; keine Subagenten. Keine neuen Abhängigkeiten, keine Löschungen, kein Commit/Push/Deployment in diesem Schritt.
