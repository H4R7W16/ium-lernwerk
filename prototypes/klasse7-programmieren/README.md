# Klasse 7 · Programmierbogen ALG-1 bis ALG-6

Statische Inhaltsquellen für die ausdrücklich beauftragte Safari-Testfassung unter `/ium-lernwerk/klasse7/programmieren/`. Die Dateien unter `inhalt/` sind die versionierten Quellen dieses bereitgestellten Stands; der gemeinsame Build schreibt ausschließlich in einen frischen, ignorierten Ausgabeordner.

## Inhalt und Herkunft

Sechs Lernaufträge, sechs Startprojekte, vier Lehrbeispiele, Durchführung für ALG-1/3/4 und ALG-2/5/6, Sicherung, Hörbriefing als Text, Jahrgangsbrief und Safari-Prüfauftrag. Planungsbasis: bestätigtes didaktisches Inhaltsmapping vom 23.09.2026; 36 Jahres-UE, 405 ALG-Minuten (45/60/75/75/90/60). Vorbereitete Materialfassungen vom 22. und 24.10.2026 wurden zusammengeführt; Aufgabenbudgets und Lernhandlungen bleiben erhalten. Eigene Unterrichtskonstruktionen; keine realen Lernendendaten.

Snap!-Kernlaufzeit 12.3.6 aus dem offiziellen Release liegt zur reproduzierbaren HTTPS-Geräteprobe unter `inhalt/klasse7/programmieren/snap/`. Lizenz **AGPLv3**, unverändert enthalten in `snap/LICENSE`; Herkunft, Änderungen und Quelltextzugang stehen in `snap/AENDERUNGEN.md`, Dateihashes in `snap/provenienz.json`. Die Lizenz des Lernwerk-Repositories ersetzt diese Drittsoftwarelizenz nicht. Keine Quelländerungen in `src/`; Startdokument ohne Analyseinitialisierung, `noCloud: true`, Deutsch und auf den eigenen Ursprung begrenzte Verbindungsrichtlinie. Zusätzliche Medien-/Beispiel-/Erweiterungskataloge gehören nicht zum Testumfang.

Das Paket ist ein Teststand, keine abschließende Geräte-, Offline-, Datenschutz- oder Unterrichtsfreigabe. Vorangehende ungeprüfte Snap!-Dateiläufe werden nicht durch die Veröffentlichung als bestanden markiert. Der Safari-Prüfauftrag nennt alle offenen Beobachtungen. Ein Service Worker wird für den Editor nicht registriert.

## Bestand und Prüfungen

`bestand-sha256.json` bindet die 1066 Dateien von main `b2011088e0b0c5a77a422ee69ef1fca8c8c36c96`. `addClass7()` lehnt Änderungen am bisherigen Bestand, fremde Zusatzpfade und interne Dateien ab. Der gemeinsame Pages-Build prüft alle lokalen HTML-Verweise auch im neuen Bereich. `pages.test.cjs` prüft zusätzlich vollständige Materialien, Editor-Konfiguration, Herkunftshashes, Testauftrag und einen absichtlich veränderten Altbestand.

Reproduktion:

```text
node --test prototypes/klasse7-programmieren/pages.test.cjs
node prototypes/pages/build.cjs <frisches-ausgabeverzeichnis>
```

Der vollständige Pages-Testbefehl steht in `.github/workflows/klasse5-pages.yml`. Die bestehenden Klasse-5-, Recherche- und Klasse-6-Ausgaben bleiben bytegleich. Wurzeleinstieg bleibt unverändert; Klasse 7 hat einen eigenen Einstieg. Die veröffentlichten Lehrdateien sind kein geschützter Lösungsbereich.
## Gestaltung vom 25.10.2026

Übersicht und alle dreizehn Materialseiten verwenden den bereits beauftragten Lernwerk-UI-Rahmen 1.2: warmes Canvas, Waldgrün, Systemschrift, getrennte Lern-/Lehrnavigation, Standortmarkierung, Abschnittsanker sowie eindeutige Editor- und XML-Aktionen. Die Übersicht bündelt die sechs Aufgaben in drei Abschnitten. Keine neue Speicherung, keine Laufzeitskripte und keine externen Schriften. CSS/HTML passen sich schmalen Ansichten an; Tabellen bleiben in einem eigenen Scrollbereich, der mit der Tastatur erreichbar ist.

`ui-inhalt-sha256.json` bindet alle ursprünglichen Absatz-, Überschriften-, Listen-, Tabellen- und Codeblöcke der dreizehn Materialseiten an main `5d997232537893239e847eb3a1f0fb3031b9403a`; zusätzlich alle Projekt-, Bild- und Snap!-Dateien bytegenau. Ergänzte Abschnittsnavigation wird beim Inhaltsvergleich separat behandelt. `ui.test.cjs` prüft Inhaltswahrung, Navigationsziele und den Schutz des Laufzeitpakets. Die Inhalte werden für den Vergleich in Textblöcke zerlegt; dies ersetzt keine Sicht- oder Geräteprüfung.

```text
node --test prototypes/klasse7-programmieren/*.test.cjs
```

Sichtprüfung der tatsächlichen HTML-Ausgabe auf Desktop und in eingebetteten Ansichten mit 320, 390 und 834 Pixeln; direkte Navigation, Abschnittssprung und Tastatureinstieg tatsächlich bedient. Das ist eine redaktionelle Gestaltungsprüfung im verfügbaren Browser. Der umfassendere Materialreview vom 24.10. sowie Safari, Schrittmodus, Export/Wiederimport, Netzwerk und Offline bleiben getrennte offene Prüfungen. Snap! und die zehn XML-Projekte sind bei dieser Überarbeitung unverändert.

## Zusätzliche Lernwerk-Ansicht für den Editor

Der anschließende Nutzerauftrag umfasst jetzt ausdrücklich auch die Programmieroberfläche: Funktionsfülle, kleine Bedienung und Gestaltung. `snap/lernwerk.html` verwendet dieselbe originale Snap!-Engine und dieselben XML-Dateien. Zusätzliche eigene HTML-/CSS-/JS-Dateien stellen klare Datei-/Ausführungsaktionen, native Schritte und tatsächliche Zustandswerte bereit. Die früheren Aussagen ohne zusätzliche Laufzeitskripte beziehen sich auf die vorangehende Materialseitengestaltung. Das Original `snap/index.html` und sämtliche Originaldateien bleiben bytegleich; `snap/LERNWERK.md` beschreibt den zusätzlichen Umfang und die Grenzen, `snap/lernwerk-herkunft.json` bindet die neuen Dateien.

Die Nacharbeit berücksichtigt tatsächliche Blockmigrationen und verwendet binär exakte Bühnenmaßstäbe, damit die ganzzahligen Grenzwerte dieser Aufgaben nicht durch die Ansicht verfälscht werden. `editor.test.cjs` prüft Verhaltensgrenzen, native Migrationsdaten, Layoutgeometrie und die aufgabenrichtigen Editoreinstiege. Materiallinks führen auf die zugehörige neue Ansicht; die vollständige Palette ist ohne Projektverlust erreichbar. Die bisherige Ansicht bleibt als Rückweg mit Startdatei in einem neuen Tab erhalten. Echte Safari-/Touch-/Netzwerk-/Offlineprobe bleibt gesondert offen.

## Inhaltsfassung 2.0 vom 25.10.2026
Der beauftragte Aufgabenreview wird als Rover-Werkstatt umgesetzt. Die Quellen unter material/ erzeugen mit python render_material.py zwölf Materialartikel; --check prüft die Synchronität. projects_v2.py ergänzt zehn eigenständige XML-Dateien ausschließlich um eingebettete SVG-Bühnen. projektlogik-v1.json schützt die vorherigen Befehlsgraphen. Der Zeit-/Quellenvertrag steht öffentlich in fassung.json. Die ursprüngliche Textbindung bleibt historisch erhalten; inhalt-v2-sha256.json bindet die beauftragte neue Textfassung und die bewusst geänderten eigenen XML. Die unveränderte Engine bleibt weiterhin gegen die ursprüngliche Provenienz geschützt. Neue Codekarte: bilder/alg6-codekarte.svg, eigene Darstellung, CC BY-SA 4.0. Keine neue Bibliothek, Cloud oder Speicherfunktion.

## ALG-1 · Erster Unterrichtseinsatz vom 27.10.2026

Zusätzlich veröffentlichte Durchführungshilfe mit konkreten Lehrerimpulsen, 45-Minuten-Verlauf, Hilfen, Diagnose und Datei-Rückkehr unter `lehrpersonen/alg-1-durchfuehrung.html`; separates Vorlesebriefing unter `lehrpersonen/alg-1-briefing.html`. Die Quellen `material/einsatz-alg-1.md` und `material/briefing-alg-1.md` stammen aus der maßgeblichen Vault-Durchführungsfassung 1.0 vom 27.10.2026; nur Links, Titel und Webkontext sind angepasst. Der Materialrenderer erzeugt und prüft nun 14 Artikel. Übersicht und Lehrpersonennavigation verlinken beide Ergänzungen. Bestehende Artikel, sechs Lernaufgaben, Zeitkonto, Projekte und Snap!-Laufzeit bleiben erhalten. Das Briefing ist ein lesbarer Vorlesetext, keine Audiodatei. Reale Schulgeräte-/Safari- und Unterrichtserprobung bleiben offen.

## Klassenstufen-Auswahl vom 27.10.2026

Die gemeinsame letzte Pages-Ausgabestufe ergänzt die Klassenstufen-Auswahl im Titel, auch in der eigenen Lernwerk-Editorhülle. Die Quellen und bisherigen Inhaltsbindungen dieses Pakets bleiben als Ausgang erhalten. Der veröffentlichte Hüllenhash und die zusätzlichen Navigationsdateien werden im eigenen Herkunftsmanifest neu gebunden; Original-Engine, Projekte und Laufzeit bleiben unverändert. Details und enger Bestandsschutz: `../pages/README.md`.

## ALG-2 · Erster Unterrichtseinsatz vom 27.10.2026

Zusätzlicher 60-Minuten-Durchführungsplan unter `lehrpersonen/alg-2-durchfuehrung.html` und separates Vorlesebriefing unter `lehrpersonen/alg-2-briefing.html`. Die Quellen `material/einsatz-alg-2.md` und `material/briefing-alg-2.md` übertragen die maßgeblichen Vault-Fassungen 1.0 mit angepassten Links. Der Renderer erzeugt und prüft nun 16 Artikel. Zeitfenster 15 + 15 + 20 + 10, Variante 45 + 15 mit Zwischenspeicherung, vier vorhandene Tabellenzeilen und individuelle Anschlussdiagnose bleiben im bestehenden 405-Minuten-Konto. Keine Änderung von Aufgabenfassung 2.0, XML-Projekten oder Snap!-Laufzeit. Tatsächliche Schulgeräte-/Safari-Dateiroutine und Unterrichtserprobung bleiben getrennt offen.

## ALG-3 · Erster Unterrichtseinsatz vom 27.10.2026

Ergänzte 75-Minuten-Durchführung unter `lehrpersonen/alg-3-durchfuehrung.html` und separates Vorlesebriefing unter `lehrpersonen/alg-3-briefing.html`. Die Markdownquellen `material/einsatz-alg-3.md` und `briefing-alg-3.md` übertragen die maßgeblichen Vault-Fassungen1.0 mit Weblinks; der Renderer prüft jetzt18Artikel. Zeitfenster15+15+30+15, Variante45+30, eigene Entscheidungsfrage, Grenztests und Fragenwechsel bleiben im vorhandenen405-Minuten-Konto. Übersicht und13Lehrnavigationen verlinken beide Seiten. Aufgabenfassung2.0, XML und Original-Engine unverändert. Reale Safari-Dateiroutine und Unterrichtserprobung bleiben offen.
