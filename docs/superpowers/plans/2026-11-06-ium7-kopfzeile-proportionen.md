# IuM 7 – Kopfzeile angleichen: Umsetzungsplan

> Ausführung: inline mit gezieltem Review. Bestehende Prüfungen und gerenderte Ausgaben kontrollieren die Änderung.

**Ziel:** Reguläre Klasse-7-Köpfe übernehmen die Wortmarkengröße, Abstände und Navigationstypografie der veröffentlichten Klasse 5/6.
**Architektur:** Den vorhandenen Klasse-7-Adapter `prototypes/klasse7-jahrgang/kopfzeile.css` und den Logo-Breakpoint in `kopfzeile.cjs` anpassen. Die stärkeren Sonderregeln für eine kompakte Kopfzeile entfernen bzw. durch die Referenzstaffel ersetzen.
**Technik:** Statischer Pages-Build mit Node 22, CSS, Sichtprüfung im Browser.
**Freigegebene Vorgabe:** Nutzerauftrag vom 06.11.2026: Kopfzeile wie Klasse 5/6; Jahrgangszahl und Akzentfarbe erhalten. Entspricht dem Vorschlag aus der vorherigen Prüfung.

## Grenzen und Prüffokus

- Große und kompakte Wortmarke der 7 sowie Akzent #245743 erhalten.
- Standortlink, Klassenwahl, Themen, Wissen und Unterrichtsmaterial bleiben nutzbar.
- Keine neue Funktion „Deine Arbeit“ für Klasse 7 einführen.
- Klasse 5/6, Snap!-Editor, Projektionen und Lerninhalte bleiben unverändert.
- Besonders prüfen: Startseite versus Innenseite; 1280/834/390/320 Pixel; offene Menüs; lange Themenbezeichnung; horizontales Überlaufen.

## Schritte

- [x] Aktuelles origin/main abrufen, isolierten Branch im lokalen Work-Verzeichnis anlegen und bestehende Navigationsprüfungen ausführen.
- [x] Unveränderte Pages-Ausgabe als Vergleich erzeugen.
- [x] Kopfzeilenregeln in `prototypes/klasse7-jahrgang/kopfzeile.css` an die tatsächlich veröffentlichten Referenzmaße anpassen.
- [x] Neue Pages-Ausgabe erzeugen; Ausgabevergleich darf nur `klasse7/kopfzeile.css` sowie den regulären Logo-Breakpoint 760→1050 in Klasse-7-HTML betreffen; alle übrigen Bytes bleiben erhalten.
- [x] Bestehende Jahrgangs-/Klassenwahlprüfungen erneut ausführen; Headermaße und Menüs im Browser vergleichen.
- [x] Gezielten Qualitätsbericht an die Endfassung binden; Git-Diff prüfen und Umsetzung/Handoff im Vault dokumentieren.

## Entscheidungen

Die kleine, reversible CSS-Korrektur erhält keine neuen Tests, die lediglich CSS-Zahlen wiederholen. Vorhandene Navigations-/Inhaltstests, vollständiger Ausgabevergleich und echte Darstellung bei gleichen Breiten liefern die passenden Nachweise.

Integration: eigener Branch `fix/ium7-kopfzeile-proportionen-20261106` auf Basis `03fd12e9ef642148881360e19653318d18b68be3`. Die vorhandene Arbeitskopie bleibt auf ihrem bisherigen Branch. Veröffentlichung wird erst nach konkreter Prüfung behandelt.

Nach Quellprüfung präzisiert: Die Referenz zeigt das Kompaktlogo bereits bei 1050 px. Deshalb wird zusätzlich der reguläre Bild-Breakpoint in kopfzeile.cjs angeglichen. Projektionen behalten 700 px. Mobile Sichtung: white-space:nowrap der Referenz verhindert einen zusätzlichen Umbruch der Fachzeile.

Abschluss: Frischer Build 1373 Dateien; 16/16 Prüfungen bestanden; 91 reguläre HTML-Seiten nur mit Logo-Breakpoint geändert, ein Stylesheet geändert, 1281 Dateien bytegleich. Browserausgabe bytegleich zur Endfassung. Qualitätslauf READY_FOR_REVIEW, Prüffassung 7174e377e32639daa853a4b542df63c963a0716140e8d86e25dd8d325bbfb7be. Zusätzlicher Quellreview ohne wesentliche Befunde. Screenshots und Messungen unter Assets/IuM-Lernwerk/Design/2026-11-06-kopfzeile-harmonie im gemeinsamen Workspace.

## Folgeauftrag: aufgeklapptes Themenmenü

Freigegeben: Themenmenü wie Klasse 5/6 mit Nummern, kurzen Beschreibungen und Schließen-Bedienung; „Deine Arbeit“ bleibt vorerst weg.

- [x] `kopfzeile.cjs`: vorhandene Jahrgangstitel als Kurzbeschreibungen, nummerierte Themen und Schließen-Schaltfläche ausgeben.
- [x] `kopfzeile.css`: Zeilen, Schrift, Abstände, Trennlinien, Standortmarkierung, begrenzte Menühöhe und Schaltfläche nach Referenz.
- [x] `kopfzeile.js` und `build.cjs`: Schließen/Escape samt Fokusrückkehr nur auf regulären Klasse-7-Seiten einbinden. Kein Arbeitsstandskript laden.
- [x] Frisch bauen, 16 bestehende Prüfungen ausführen, Menü auf Desktop/Tablet/Handy einschließlich Scrollen und Tastatur sichten; Inhalts- und Ausnahmeerhalt vergleichen.
- [x] Qualitätsnachweis erneuern und bestehenden PR53 aktualisieren. Noch keine Veröffentlichung beauftragt.
Menü-Abschluss: 1374 Dateien; 16/16 Tests bestanden; 91 reguläre HTML nur im Themenmenü und bei der Menüskript-Einbindung geändert, ein Stylesheet geändert und ein Menüskript ergänzt; 1281 Dateien unverändert. Gesichtete Ausgabe bytegleich zum frischen Endbuild. Desktop/Tablet/Mobil und Schließen/Escape samt Fokusrückgabe geprüft. Qualitätslauf READY_FOR_REVIEW, Prüffassung d779de05e429ae6ff891c12a17d4c8714c10bf5d78dc3d218a98e90346dfc0e5. Nachweise: Assets/IuM-Lernwerk/Design/2026-11-06-themenmenue-harmonie. Keine Veröffentlichung.
