# Klasse 7 – Deine Arbeit, Stufe 1: Umsetzungsplan

> Ausführung fortlaufend im bestehenden isolierten Worktree. Arbeitsbereiche werden nach Dateien getrennt; Integration und tatsächliche Browserprüfung liegen beim Hauptagenten. Der Nutzer hat Konzept1.1 und Umsetzung ausdrücklich freigegeben.

**Ziel:** Lernende merken eine Aufgabe, finden Ergebnisablage und nächsten Schritt wieder und können ihre Übersicht verlässlich mitnehmen – ohne ein zusätzliches Pflichtportfolio.
**Architektur:** Ein kleiner wiederverwendbarer Modell-/Speicherkern mit explizitem Jahrgang, eine Klasse7-Aufgabenregistrierung und eine eigenständige Arbeitsübersicht. Reguläre Aufgaben erhalten einen einfachen Merken-Link; persönliche Speicherlogik läuft ausschließlich auf der Arbeitsübersicht. Bestehende 5/6-Runtimes, Snap und fachliche Aufgaben bleiben unverändert.
**Technik:** Bestehender statischer Node22-Pages-Build, Vanilla JavaScript, native HTML-Formulare/Dialoge, Node-Tests; keine neuen Abhängigkeiten.
**Spec:** Freigegebenes Konzept1.1 „2026-11-06 – Konzept Deine Arbeit Klasse7“ im Projekt-Vault. Schwerpunkt des Nutzerfolgeauftrags: selbstständig verständliche Bedienung und realer Nutzen, überprüft an DAT-1 und ALG-5.

## Globale Vorgaben und Entscheidungen

- Keine Veröffentlichung der neuen Funktion in diesem Auftrag; fertig prüfen und als konkreten Entwurfs-PR bereitstellen. Veröffentlichung der vorigen Kopfzeile war ein separater Auftrag.
- 22 reguläre Aufgaben der vier Reihen erhalten „Für später merken“. Die Formulierung verdeutlicht die Handlung besser als ein sofortiges Weiterarbeiten-Versprechen. Eingabe öffnet auf arbeit.html; dort vorgewählte Aufgabe, sichtbare Arbeitsstelle und freiwillige Ablage-/Nächster-Schritt-Angaben.
- Kein Aufruf-/Lernfortschritts-Tracking, keine Bewertungs-/Fertiganzeigen, keine Produktdateien im Übersichtexport. Private Seiten und private Arbeitsabschnitte nicht registrieren. Keine automatische Erkennung privater Freitexte behaupten.
- Rücksprungziele ausschließlich aus dem Build-Katalog; importierte Dateien enthalten keine ausführbaren URLs. Veraltete Ziele behalten ihre Hinweise und führen mit Erklärung zur Aufgabe/Reihe zurück.
- Interne Navigation/Reload im selben Tab bei funktionierender Tabsicherung erhalten. Gerätespeicherung optional, nur nach bestätigtem Schreiben als aktiv anzeigen. Abschalten löscht vorhandene Kopie nicht. Entfernen gezielt und bestätigt; andere Jahrgänge unberührt.
- Import: Vorschau, Karten auswählen, standardmäßig zusätzlich übernehmen. Ersetzen nur eine ausdrücklich gewählte Karte derselben Aufgabe. Wirksame Reihenhinweise beim Export pro Karte auflösen; importierte Hinweise bleiben eigene Kartenhinweise.
- Snap bleibt unverändert: Anleitung zum Öffnen der eigenen XML und eigene Testnotizen, keine vorgetäuschte automatische Projektwiederaufnahme.

## Schnittstellen

`arbeit-katalog.cjs`: `createCatalog(pages)` liefert `{grade:7,version:1,areas:[{id,name,path,notesPath}],tasks:[{id,code,title,area,path,places:[{id,title}],notesPath,snapPath?}]}`. Pfade relativ zur Klasse7-Wurzel, erste Arbeitsstelle id="" = Ganze Aufgabe. Öffentliche vorhandene H2-IDs; private Abschnitte ausgeschlossen.

`arbeit-seite.cjs`: `renderWorkPage(catalog)` liefert komplette arbeit.html inklusive regulärer Kopfzeile, gemeinsamer Reihenstile, eigener work-overview.css, Inline-JSON `#work-catalog` und drei defer-Skripten work-overview-model.js, work-overview-storage.js, work-overview.js. Appwurzel `#work-app`.

`arbeit-adapter.cjs`: `addWorkOverview(pages)` liefert neue Map, ergänzt Seite/Assets, und setzt auf 22 Aufgaben einen unterpfadfähigen Link `arbeit.html?aufgabe=dat-1`. Markierung `data-work-overview="bookmark"` isoliert den neuen Navigationszusatz für den Inhaltsvergleich. Keine Antwortfelder/Speicherlogik auf Aufgaben oder privaten Seiten.

Modell/Speicher werden durch eigene gemeinsame Module geliefert; genaue exportierte API wird vor Runtime-Anschluss verbindlich dokumentiert. Alle Modelle sind in Node ohne Browser testbar. Katalog ist die einzige Quelle für URLs.

## Aufgaben

- [x] 1. Baseline: Ausgang d57db001, reine Dokumentationsfortschreibung auf main fba0660, sauberer isolierter Branch; vorhandene 18 Pages-Verträge plus Jahrgang/Klassenwahl ausführen und unveränderten Build als Vergleich ablegen.
- [x] 2. Modell und Speicher: zuerst fehlschlagende Fälle für Export/Import, Jahrgangstrennung, Reihenhinweise, Ersetzen, veraltete Ziele, ungültige Eingaben und Speicherfehler; danach pure Implementierung. Bewahrt inkompatible gespeicherte Daten und bietet Notexport an; kein stilles Überschreiben.
- [x] 3. Katalog/Integration: 22 Aufgaben und vorhandene sichere Arbeitsstellen erfassen, regulären Kopf um Deine Arbeit ergänzen, Merken-Links und Hilfe für Lehrpersonen integrieren. Bestehende Inhalts-/Skripttests für den ausdrücklich erlaubten Zusatz präzise ergänzen, Schutz nicht entfernen.
- [x] 4. Oberfläche/Runtime: Leerzustand mit kurzer verständlicher Einführung; vier Themen, Merkkarten, Bearbeiten, Entfernen, Reihenhinweis, Datum und tatsächliche Rückkehr. Export-/Importvorschau, Speicherstatus/Fehlerhilfe und Druckansicht. Native Tastaturführung und 48px-Ziele, 320px-Reflow; lange fremde Texte ausschließlich als Text anzeigen.
- [x] 5. Durchläufe: DAT-1 (Heft, Arbeitsstelle, nächster Schritt, Neuaufruf), ALG-5 (XML und Testnotiz getrennt, klare Startergrenze). Tatsächlichen Export herunterladen und in unabhängigem Browser-Speicher importieren; Auswahl/Ersetzen/Abbruch und mobile Darstellung prüfen. Speicherausfälle in fokussierten Runtime-Tests, keine erfundene Geräteprobe.
- [x] 6. Abschluss: frischer Gesamtbuild, vollständige Pages-Verträge, vollständiger Ausgabeabgleich (5/6/Snap/Projektionen bytegleich, Fachinhalte außerhalb genehmigter Navigation gleich), frischer Code-/UX-Review und notwendige Nacharbeit. Versionsgebundener Lernwerk-Qualitätsbericht, Session/Task/Handoff, Commit/Push und Entwurfs-PR; CI bis Abschluss verfolgen.

## Reviewfokus

1. Speicherverweigerung und inkompatible Altdatei dürfen keine bestehende Kopie überschreiben; RAM-Änderungen vor Navigation schützen und Export ermöglichen.
2. Import darf fremde Jahrgänge/private Routenziele nicht aktivieren; Abbruch und Fehler verändern nichts; zielgenaues Ersetzen und gemeinsame Reihenhinweise getrennt prüfen.
3. Ein eingetragener Dateiname ist keine gesicherte Datei. Erstnutzung und Gerätewechsel müssen das in handlungsfähiger Sprache erklären, ohne eine Einstellungsrunde zu erzwingen.
4. ALG-5 darf nicht behaupten, den eigenen Code automatisch zu öffnen. Bestehende XML-Wiederöffnung und Testhandeln bleiben sichtbar.
5. Lange Dateinamen/Freitexte, Tastatur und schmale Ansicht; keine stille Textkürzung eigener Inhalte und keine XSS/HTML-Ausführung.

## Ausführungsnotizen

Konzept bereits freigegeben; keine erneute Planfreigabe erforderlich. Die zusätzliche Verständlichkeitsprüfung ist ein hypothetischer Lernendendurchlauf, kein Nachweis mit echten Kindern. Scope/Dateigrenzen werden bei Delegation dokumentiert. Build und Testdateien bleiben unter AI-Workspace-Local/Work, ausgewählte Ergebnisse unter Assets.
## Ergebnis der Ausführung

- Modell/Speicher: 22 Tests; Runtime: 7 Ereignis-Regressionsfälle mit echten Modulen in Node-VM. Renderer 3 und Integration 6 Tests ergänzen die Bestandsverträge. Vollständige Pages-Liste: 228/228 grün.
- Review-Nacharbeit: Downloadangebot hebt die Verlustwarnung bei flüchtigem Speicher nicht auf; gemeinsame Hinweise werden bewusst genutzt; reguläres erneutes Merken aktualisiert eine bestehende Karte; Import/Druck führen sichtbar zur Übersicht; Gerätedatenkonflikte bieten Export der vorhandenen Kopie; Importdatum sichtbar; asynchroner Import schützt zwischenzeitliche Eingaben.
- Neuer Eintrag übernimmt vorhandene Reihenhinweise als eigene Kopie. Erst ausdrücklich aktivierte gemeinsame Nutzung bindet ihn an den Reihenhinweis. Bestehende gebundene Karten zeigen eine sichtbare Änderungswarnung.
- Tatsächlicher Browser: DAT-1 mit Abschnitt/Heft/nächstem Schritt und Reload; ALG-5 mit XML und Testnotizen; Exportdatei zwischen getrennten Origins geladen, Auswahl/Ersetzen/Abbruch/Fremddatei geprüft. Optionale Gerätekopie in neuem Tab wiedergefunden. 320-Pixel-Ansicht, Tastatur, langer Dateiname und Desktop ohne horizontalen Überlauf.
- Snap-Datei tatsächlich heruntergeladen und wieder geöffnet. Dies prüft den XML-Rundlauf des Startprojekts, nicht eine gelöste Programmieraufgabe.
- Frischer Build 1379 Dateien. Vollvergleich: 1282 bytegleich, 91 reguläre HTML-Seiten mit genau erlaubten Navigationszusätzen (22 Merken-Links), eine Kopf-CSS-Datei, fünf neue Dateien. Klasse5/6, Snap und Projektionen bytegleich.
- Nachweise außerhalb des Repos: AI-Workspace-Local/Work/ium7-deine-arbeit-20261106-qa. Abschlussstatus, Commit/PR/CI und Qualitätsbericht werden im Vault-Handoff erfasst. Keine Veröffentlichung im Rahmen dieses Folgeauftrags.
