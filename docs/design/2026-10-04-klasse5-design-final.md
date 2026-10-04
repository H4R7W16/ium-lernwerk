# Klasse 5 – übernommenes Design, 04.10.2026

Jan beauftragt die Umsetzung des Designs für Klasse 5 und schließt weitere inhaltliche Anpassungen aus. Die Fortsetzung betrifft ausschließlich prototypes/shared/identity.css. Bereits vorhandene Wortmarke 02, Klassenfarbe #2D52EE, Segoe UI, Bilder und sämtliche Inhalte bleiben Grundlage.

## Umsetzung

Gemeinsame Akzentrollen zentral definiert und mit den vorhandenen Farbvariablen verbunden. Navigation mit 16 px und mindestens 48 px Trefferhöhe; auf sehr schmalen Displays zwei Zeilen. Lern- und Ergebnistext mit 18 px, Ergebnislabel als lesbare Zwischenüberschrift. Eingabefelder mit klarerer Kontur und 18 px Text. Zugangskarten auf der Startseite neutral und zurückhaltend; mobil kompakte Anordnung der vollständigen vorhandenen Texte. Keine Kürzung, Themengruppierung oder Änderung des Wiedereinstiegsverhaltens.

## Nachweise und Selbstreview

Selbstreview im bestehenden Chat gemäß Repository-AGENTS. Geprüft: gemeinsame Variablen, CSS-Kaskade, vollständige sichtbare Texte, Tastaturfokus-Regeln, mobile Anordnung, Seitenbreite, erreichbares Themenmenü und Eingabefelder. Keine zusätzlichen Tests für feste CSS-Werte.

- Build: node prototypes/m06-reinigungsfall/build.cjs dist/design-04, erfolgreich; 388 öffentliche Dateien.
- Node-Prüfungen: node --test prototypes/shared/*.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs; 57 bestanden, 0 fehlgeschlagen.
- Inhaltserhaltung: frische SHA-256-Manifeste vor/nach der Umsetzung. Von 158 Prototyp-Quellfiles änderte sich ausschließlich shared/identity.css. Alle 284 generierten HTML-Dateien sind bytegleich. Im Build wechseln nur klasse5/identity.css und die daraus abgeleitete klasse5/mantel-sw.js; alle übrigen 386 öffentlichen Dateien bleiben bytegleich.
- Bericht: reports/design-class5-final/content-preservation.json; Ausgangshashes before.json; Node-Ausgabe node-tests.log.
- Browser: 320, 390, 540, 768, 1024 und 1280 CSS-Pixel. Dokumentbreite überschreitet in keiner geprüften Ansicht die verfügbare Breite. Themenmenü geöffnet und geschlossen, bei 320 und 1024 innerhalb der Seitenbreite.
- Geräte-Lerneinheit, erster Auftrag, optionales Eingabefeld und Wissen über die echte Navigation geöffnet. Feldtext 18 px, Kontur rgb(118,130,145), mobiler Logo-Assetpfad korrekt. Keine Lernantwort eingegeben oder gelöscht.
- git diff --check: erfolgreich; vorhandene Hinweise zur Zeilenendenkonvertierung betreffen die früheren Änderungen.
- Desktop- und Mobilvorschau unter Assets/IuM-Lernwerk/Design/2026-10-04-klasse5-final/ im gemeinsamen AI-Workspace.

Browser-Sichtprüfung und automatisierte Prüfungen ersetzen keine vollständige WCAG-Abnahme oder Prüfung auf realen Schulgeräten.

## Vorschau und Git-Stand

http://127.0.0.1:8791/klasse5/index.html

Der bestehende Server verwendet dist/design-02. Nach Inhaltserhaltungsprüfung wurden nur die beiden geänderten Dateien übernommen; das gesamte Verzeichnis ist anschließend bytegleich mit dist/design-04. Neuer Start bei Bedarf: python -m http.server 8791 --bind 127.0.0.1 --directory dist/design-04.

Worktree: C:/Users/Jan/AI-Workspace-Local/Work/ium-identitaet-02-20261004. Branch feat/ium-identitaet-02, Basis 6cfd63e. Änderungen weiterhin lokal uncommitted, einschließlich der vorangegangenen Markenintegration. Kein Merge, Push oder Deployment; gleichzeitig genutzte Produktarbeitskopie nicht verändert.
