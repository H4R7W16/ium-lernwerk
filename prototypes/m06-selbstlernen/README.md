# Mit Schleifen planen – eigenständig lernen

Zusätzliche Prüffassung vom 21.09.2026 für Informatik ab Klasse 5. Die Lernstrecke verbindet Grundbewegungen, Schleifen, Vorhersage, Schrittuntersuchung, eigene Flächenprogramme, gestufte Hilfen und vollständige Lösungen.

- [Interaktive Fassung](https://h4r7w16.github.io/ium-lernwerk/selbstlernen/)
- [Lesefassung](https://h4r7w16.github.io/ium-lernwerk/selbstlernen/read.html)
- [Bisherige Lernfassung 2](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall-v2/)
- [Erste Reinigungsfassung](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall.html)

Die vorherigen Adressen und die Startweiterleitung bleiben erhalten. Die Veröffentlichung dient der Rückmeldung. Fachlicher KI-Gegencheck und technische Prüfung ersetzen keine Schülererprobung; eine Unterrichtsfreigabe wird nicht behauptet. Echter 200-%-Browserzoom und abschließende Abnahme sind noch offen.

## Lokal öffnen

Im Repositoryordner:

```sh
python -m http.server 43866 --bind 127.0.0.1 --directory prototypes/m06-selbstlernen
```

Anschließend http://127.0.0.1:43866/index.html oder read.html öffnen. Neue Antwortfelder bleiben im geöffneten Tab und gehören nicht zum bestehenden Sicherungsvertrag. Die Oberfläche erläutert diese Grenze. Import-/Exportfunktionen wurden in dieser Revision nicht geprüft.

## Quellen und gezielte Prüfung

content.cjs enthält die gemeinsamen Inhalte; render.cjs erzeugt index.html und read.html. model.js liefert die fachliche Auswertung, cleaning-core.js die Bewegungsregeln. app.js und app.css verbinden Darstellung und Bedienung. material.test.cjs prüft gezielt die Materialrevision ohne Import-/Exportfälle.

```sh
node --test prototypes/m06-selbstlernen/material.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs
node prototypes/m06-reinigungsfall/build.cjs
```

Der Build erwartet einen noch nicht vorhandenen Ausgabeordner; alternativ einen neuen Zielpfad als Argument angeben. Er erhält die bisherigen Pages-Dateien und ergänzt selbstlernen/ mit sechs Laufzeitdateien. Interne Reviewberichte, lokale Pfade und Arbeitsprotokolle sind nicht Teil dieser Veröffentlichung.

Der manuelle Workflow `.github/workflows/selbstlernen-pages.yml` veröffentlicht von main. Er führt ausschließlich die beiden oben benannten Prüfdateien und den statischen Build aus; keine Import-/Exporttests oder Gesamtsuiten.
