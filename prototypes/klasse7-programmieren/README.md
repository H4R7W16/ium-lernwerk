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