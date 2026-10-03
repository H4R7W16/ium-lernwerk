# Klasse-5-Mantel – Umsetzungsplan

> Ausführung: superpowers:executing-plans, inline. Direkter Nutzerauftrag: Entwurf verbessern, dann Mantel erstellen. Der vorhandene Entwurf und Review mit Nutzerkorrektur bilden die Spezifikation.

**Goal:** Lauffähiger schulübergreifender Mantel für die drei vorhandenen Klasse-5-Angebote, mit vollständigen Begleitansichten und gemeinsamer Arbeitssicherung.
**Architecture:** Vorhandenen statischen Pages-Generator erweitern. Eigenständiger veröffentlichbarer Pfad klasse5/ mit kopierten Fachwerkzeugen aus denselben Quellen; historische Angebote unverändert. Gemeinsame Navigation, Tokens, Seitenrenderer, versionierte Zustandsverträge und gezielte Werkzeugadapter.
**Tech Stack:** Bestehendes Node-22-Projekt; CommonJS-Generatoren, klassische Browser-JavaScript-Dateien, Service Worker. Keine neue Framework-/Cloudabhängigkeit.
**Spec:** Vault-UI-Standard 1.2 und Funktionsvertrag; Nutzerkorrektur: lokale Hilfewege ausschließlich in schulischen Vorbereitungshinweisen.

## Global Constraints
- Klasse 5; drei echte Angebote, keine leeren Zukunftseinheiten.
- Vorhandene Lernhandlungen, Quellen, Bilder und Programme erhalten.
- Format der Arbeitsdatei: bestehendes ium-learning-state, formatVersion 1, moduleId/moduleVersion/stateSchemaVersion/workspaceId/savedAt/payload.
- Kein Login, Tracker, Kompetenzprofil oder automatische Freitextbewertung.
- Tabarbeit im sessionStorage, freiwillige Gerätesicherung; Einschränkungen offen erklären.
- Private Reflexion nicht im Standardprodukt; keine ungefragte Vorführung/Druckausgabe.
- Offline nur nach geprüfter Vorbereitung; eigener SW-Scope klasse5/, keine Überschreibung historischer Worker.
- Lokale Dateien/Tests/Builds außerhalb OneDrive. Keine Veröffentlichung oder Merge.

## Review Focus
- Beschädigte, fremde oder übergroße Arbeitsdatei: kein bestehender Stand verändert.
- Neu beginnen und importieren bei alter Arbeit: separater Stand bevorzugt, Ziel/Datum eindeutig.
- Werkzeugzustand nach Wissen-/Material-/Themenwechsel: keine Beleg-/Code-/Ausschnittverluste.
- Lange URLs und schmale Displays: Produkt bleibt vollständig lesbar.
- Speicher- und Offlinefehler: keine falsche Erfolgsmeldung; exportierbare Sitzung erhalten.

## Task 1: Inhalts-/Zustandsvertrag und statischer Mantel
Files: prototypes/shared/class5-catalog.cjs, mantel-model.js, mantel-render.cjs, mantel.css, mantel.test.cjs; Erweiterung build.cjs.
Interfaces: catalog() liefert drei Metadaten/Schritt-/Lernbogenrecords; augment(assets) erzeugt klasse5/ ohne Änderung alter Assets. Model validiert bestehende StateEnvelope plus familienbezogenen Mantelpayload.
- [x] Tests für fehlende Bogenfunktion, ungültige Datei, separate/ersetzende Importübernahme und vollständige neue Ansichten schreiben und RED beobachten.
- [x] Gemeinsamen Katalog, Wissen-/Material-/Lehrübersichten, Einzelmaterialzugänge, Wiederaufnahme und Arbeitsansicht erzeugen.
- [x] Inhaltseingaben und Zusatzblöcke external/cooperative/private an einem dokumentierten Autorenvertrag ausrichten.
- [x] Tests GREEN; alte 41 gezielte Prüfungen erneut ausführen.

## Task 2: Arbeitssicherung und Fachanschlüsse
Files: mantel-runtime.js, Werkzeugadapter in studio.js / Medien-app.js / Quellen-app.js; mantel-sw.js.
Interfaces: window.LernwerkMantel.register({capture,restore,validate,flush}) verbindet echte Fachzustände; Model hält versionierte Einzelstände und atomare Importübernahme.
- [x] Fachzustandsvalidierung und Fehler-/Privatheitsgrenzen mit RED-Testfällen prüfen.
- [x] Formulare und Werkzeugzustände vor Navigation sichern und beim Rückweg wiederherstellen. Eigene Stand-IDs, kein automatisches Mischen.
- [x] Gerätespeicherung, Abschalten versus Löschen, lesbares Produkt, versionierte Arbeitsdatei, Importvorschau und Reset umsetzen.
- [x] Service Worker mit vollständig geprüftem Paket, Offline-/Updatezuständen und separatem Scope.
- [x] Bedeutungsvolle Modell-/Importtests GREEN; Syntax prüfen.

## Task 3: Endprüfung und Übergabe
Files: QA-/Autorenhandbuch, Ausführungsledger; erforderliche Korrekturen.
- [x] Frischen Build in lokalem Work-Output erzeugen.
- [x] Drei Fachwege plus Wissen/Material/Rückkehr, Importvorschau/Abbruch, mehrere Stände, lange Quellenangabe, Offline und 320px im Browser prüfen.
- [x] Frische unabhängige Codeprüfung gemäß executing-plans/requesting-code-review. Wichtige Befunde mit reproduzierenden Tests beheben.
- [x] Plan, Ledger, Vault-Handoff und Session aktualisieren; überprüftes Produkt zur Sichtung öffnen.
- [x] Git-Abgleich vor Commit, Featurecommit dokumentieren; kein Push/Merge/Deployment ohne entsprechenden Auftrag.

Ausführungsgrenzen und tatsächliche Nachweise: siehe docs/klasse5-mantel-pruefstand.md. Exportdateiangebot bestätigt; externer Downloadabschluss und reale Geräteabnahme bleiben offen.
