# Erster Klasse-5-Lernbogen – Implementierungsplan
> Ausführung: superpowers:executing-plans, inline. Keine Subagenten gemäß Workspace-Regel ohne ausdrückliche Erlaubnis.
**Ziel:** Produktionsübersicht und vollständig eingebundener Dateien-Lernbogen mit gleichwertigem iPad-/Windows-Weg.
**Grundlage:** Nutzerauftrag „Fahre damit fort“ zum Produktionsplan vom 03.10.2026; Präzisierung beide Geräte gleichwertig.
**Architektur:** Bestehender JSON-Aufnahmeweg wird abwärtskompatibel erweitert. Fachinhalte bleiben im Paket, generische Ausgabe in einem Renderer; keine neue App oder Speichersemantik.
**Technik:** CommonJS, Node 22, statisches HTML/CSS, bestehender Mantel.
## Grenzen
- Ausgangsstand b2f1614, separater Folgebranch; keine Abhängigkeiten, kein Push/Deployment.
- Jahresplanung aus dee82ec: G5-M01 bis M06, 38 UE Bedarf unbestätigt.
- Bestehende Prototypen und Antwortenformat bleiben erhalten.
- Keine automatische Bewertung realer Gerätehandlungen; kein erfundener Erprobungsnachweis.
- Keine direkten HTML-Eingaben im Autorenformat; Dateipfade auf Paketassets begrenzt.
## Prüfschwerpunkte
- Wissen und Material wirklich verschieden; direkte Rückkehr hält die aktuelle Aufgabe.
- Fehlende Medien, Quellen oder Rechteangaben und unzulässige Pfade werden abgewiesen.
- Materialien enthalten tatsächlich benötigte Daten, Kriterien und getrennte Hilfen/Lösungen.
- Alte Prototypen und bestehende einfache Inhaltsfixtures weiterhin lauffähig.
- Papierdarstellung enthält keine eigenen Arbeitsdaten oder ungefragt Lösungen.
## Aufgaben
- [x] Ausgangsstand/Branch/16 grüne Basistests.
- [x] 1. Produktionsübersicht und Unterrichtsbrief: docs/produktion/klasse5.md, docs/produktion/g5-m01-dateien.md.
- [x] 2. RED: class5-content.test.cjs für Autorenversion 2, echte Assets, unzulässige Referenzen/Pfade und unterschiedliche Ausgaben.
- [x] 3. GREEN: class5-content.cjs erweitern, class5-author-render.cjs ergänzen und in mantel-render.cjs anbinden; kleine CSS-Ergänzungen.
- [x] 4. Inhaltspaket dateien.json + kleine eigene Assets; sieben fachlich begründete Schritte, vier Wissensartikel, Material-/Hilfs-/Lösungsdruck, Lehrerbrief.
- [x] 5. Fachlicher Review, gezielte Regressionen, frischer Build, Browser 1024/390, Rückkehr und Drucklogik; reale Druckdarstellung als offener Erprobungspunkt.
- [x] 6. Plan/Nachweise/Vault aktualisieren, sauber lokal committen und Vorschau übergeben.
## Protokoll
- Bounded follow-up: vorhandener Autorenweg und angenommener UI-Vertrag. Nutzer hat den konkreten Produktionsvorschlag freigegeben; Routineausführung ohne erneute Zwischenfreigaben.
- Initiale Baseline: 16 Tests bestanden; keine Abhängigkeiten installiert.
- Review inline als Selbstreview, nicht als unabhängiges Gutachten.

## Abschlussnachweise · 03.10.2026
- Autorenversion 2 implementiert, ein realer Dateien-Bogen mit sieben Schritten, vier Wissensartikeln und drei eigenen Assets aufgenommen.
- Baseline 16/16; erste Autoren-RED-Runde 1/4 grün (Legacy-Gerätevalidierung, fehlender Renderer und fehlendes Paket scheiterten wie erwartet). Fehlerhafte Mutationsprüfung danach um eine gültige Baseline ergänzt.
- Rückkehrproblem im Browser reproduziert: Planen → Wissen ohne Eingabe führte zum Einstieg. Regression vor Fix 5/6, danach grün. Lesen erzeugt weiterhin keinen Lernnachweis.
- Finale gezielte Suite: 48/48 bestanden; Mantel, Autorenpaket, gemeinsame UI, Algorithmusmaterial/Lernprozess sowie Quellenquest-/Medienmodelle. Keine neuen Abhängigkeiten.
- Finaler Build: 161 Dateien, einschließlich Linkprüfung; Quelle und Drucktext beider Downloads stimmen überein. Syntaxprüfung der geänderten Browserruntime bestanden.
- Sichtprüfung auf TIER im Codex-Browser bei 1024 und 390 CSS-Pixeln: kein horizontaler Überlauf in den geprüften Ansichten; vier Angebote und Grafiken im Einstieg vorhanden; beide Gerätehilfen jeweils vier Schritte; Wissensrückkehr mit/ohne Antwort, Antworterhalt und Einzelmaterial geprüft; keine aufgezeichneten JS-Fehler.
- Druckauswahl und Vorher-/Nachher-Drucklogik automatisiert geprüft. Tatsächliche Druckemulation/Paginierung nicht über die verfügbare Browser-API geprüft; Papierausdruck bleibt Erprobungspunkt. Keine Behauptung realer iPad-/Schulprofiltests.
- Fachlicher Selbstreview im Unterrichtsbrief: selbst gelöste Fälle, falsche Begriffe, offene Ziele, Diagnosegrenzen, Hilfen/Revision, Transfer und späterer Abruf. Kein unabhängiger Review.
- Vorschau: http://127.0.0.1:8776/klasse5/dateien/ ; Gesamteinstieg /klasse5/. Buildordner C:/Users/Jan/AI-Workspace-Local/Work/ium-klasse5-dateien-20261003-03, eigener Server PID 18768.
- Screenshot: C:/Users/Jan/.codex/visualizations/2026/10/03/01a100d9-525a-73b1-86a6-e75d679d8507/dateien-lernbogen-tablet.jpg.
- Lokale Übergabe als review. Nutzer-Sichtung, tatsächlicher Geräte-/Drucktest und Unterrichtserprobung stehen aus; 38 UE Jahresverfügbarkeit weiterhin unbestätigt. Kein Push/Deployment oder Zeitplan eingerichtet.

- Stagingprüfung fand zwei zusätzliche Leerzeilen am Ende eigener TXT-Assets; bereinigt. Anschließend Autorenprüfung 7/7 und frischer Build erneut bestanden.
