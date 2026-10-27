# IuM 7 an die Reihenidentität anpassen

Auftrag vom 27.10.2026: Design/Layout von IuM 7 an die bestehende Reihe anpassen und den aktuellen Stand auf GitHub Pages veröffentlichen. Die bereits geprüfte Inhaltsfassung 2.2 gehört zum aktuellen Stand.

## Umsetzung und Plan

Die sichtbare Referenz ist die bereits veröffentlichte Identität 02 von Klasse 5/6. Klasse 7 übernimmt dieselbe Wortmarke mit großer 7, Segoe UI, Papierfläche und neutrale Textfarben, gemeinsame Kopfzeilenproportionen und Navigation. Der vorhandene Jahrgangsakzent #245743 bleibt. Desktop- und kompakte PNG-Wortmarke sind aus den vorhandenen editierbaren SVGs abgeleitet; SVG-Master liegen daneben.

1. `prototypes/klasse7-programmieren/layout.cjs` ergänzt die gemeinsame Hülle ausschließlich im Pages-Ausgabeschritt. Es übernimmt die tatsächlichen Mantel-/Identitätsdateien aus der vorhandenen Klasse-5-Ausgabe, ergänzt die Klasse-7-Marke und bindet den geänderten Editor-Kopf im Herkunftsmanifest.
2. `reihenlayout.css` gleicht vorhandene Aufgaben-, Übersichts- und Lehrpersonenelemente ab: Schrift und Farben, lesbare Navigation, weiße Arbeitsabschnitte, Hilfe, Tabellen und kompakter Editor-Kopf.
3. `prototypes/pages/build.cjs` wendet den Layoutschritt vor der bestehenden Klassenstufennavigation an. Der Navigationstest vergleicht deshalb deren Ausgabe mit der bereits angepassten Hülle.
4. `layout.test.cjs` prüft die tatsächlich veröffentlichten Seiten, Inhaltserhaltung, unveränderte Klassen 5/6, erreichbare responsive Bilder und korrekte Editor-Herkunftsbindung. Keine Tests für einzelne feste CSS-Werte.
5. Frischer Pages-Build, tatsächliche Browseransichten und schmale Rahmen; gezielter Layout-Selbstreview. Danach bestehender PR 38, CI und autorisierte Veröffentlichung auf Pages.

Artikel, Zeitbudgets und Programme werden in diesem Schritt nicht neu verfasst. Die Rohquellen und ursprüngliche Snap-Bindung bleiben als Vergleich erhalten. Die ergänzende `layout`-Bindung beschreibt den veröffentlichten Editor-Kopf; die bestehende `navigation`-Bindung erfasst die danach ergänzte Klassenstufenauswahl.

Nachweise und technische Arbeitsdateien liegen lokal unter `AI-Workspace-Local/Work/ium7-layout-qa-20261027`. Fertige Sichtprüfungen und Berichte werden gezielt im vorgesehenen Assets-Bereich archiviert. Der Produktionsbrief im Vault hält die Nutzerbindung und den endgültigen Git-/Deploy-Stand fest.

## Abschlussprüfung

Gezielter Selbstreview, Prüffassung 2: `READY_FOR_REVIEW`, Hash `cd680831d665f62918ad39dff6ed7381bcaf831d23a70589ce0bc0d81d1caa78`. Zwei wesentliche Darstellungsbefunde behoben: übergroßes Symbol im Snap-Zugang bei 320 Pixeln und lange Lehrmaterialnavigation vor dem angeforderten Artikel. Die Materialwahl ist jetzt nativ einklappbar; alle 17 Links bleiben erhalten.

149 Pages-Prüfungen vor der letzten Materialmenü-Nacharbeit bestanden, danach 11 betroffene Layout-/Navigationsprüfungen erfolgreich. Vollständiger Endbuild: 1170 Dateien, davon 100 unter Klasse 7; 25 Seiten mit gemeinsamer Identität. Lokale Vorschau bytegleich mit der finalen Klasse-7-Ausgabe. 22 Artikelrenderer synchron. Lern-/Lehrtexte und Programme erhalten; veröffentlichte Klassen 5/6 bytegleich.

Browser: tatsächlicher Desktop sowie lokale CSS-Rahmen mit 320, 390 und 834 Pixeln; Klassenwahl geöffnet und mit Escape geschlossen, Hilfe und Materialwahl geöffnet, Durchführung über die Materialwahl erreicht. Echter Roverlauf 0 → 40; Dateidialog geöffnet und abgebrochen. Keine neue vollständige Datei-Rückkehr- oder Safari-/Touchprüfung; Unterrichtsgrenzen aus Inhaltsreview 2.2 bestehen fort.
