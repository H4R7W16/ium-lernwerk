# Sauber geplant · Reinigungsroboter

[Vorschau öffnen](./reinigungsfall.html#einstieg)

Interaktiver Konzeptstand vom 13. September 2026 für IuM, Klasse 5. Drei Grundrisse verbinden einzelne Befehle, Wiederholungen, Fehlerdiagnose und einen eigenen Reinigungsplan. Zurück am Start bedeutet noch nicht, dass die gesamte Fläche gereinigt ist.

## Umfang und Grenzen

Freie Programme bestehen aus `vor`, `links`, `rechts` und `wiederhole 2–9 [1–5 Grundbefehle]`. Keine Verschachtelung, höchstens 100 Aktionen. Die Startkachel zählt als gereinigt. Vorhersagen, Codefassungen und ausgewählte Ergebnisse lassen sich vergleichen. Ablaufgrafiken werden auf Papier erstellt.

Eingaben bleiben ausschließlich bis zum Neuladen erhalten. Keine dauerhafte Speicherung, Offlinezusage, automatische Benotung oder nachgewiesene Lernwirkung. Diese veröffentlichte Vorschau ist ein Konzept für das fachliche Review.

[Aufgaben, Lösungen und fünf Unterrichtseinheiten](https://github.com/H4R7W16/ium-lernwerk/blob/4abbe6c2225e608f9bc10c9ae9a4028477235864/docs/planning/ium-5-7/m06-reinigungsfall.md)

[Früherer Prüffahrt-Entwurf](./prueffahrt.html)

## Veröffentlichung und Prüfung

Die statischen Quelldateien stammen aus dem geprüften Workspace-Prototyp `Shared/Prototypes/ium-v2-ux01`. Die Reinigungsansicht ist zusätzlich der Start unter `index.html`. Ihr Rückverweis führt zum erhaltenen Prüffahrt-Entwurf. Ein `noindex`-Hinweis ist keine Zugriffskontrolle; GitHub Pages ist öffentlich.

Prüfung vom Repo-Stamm:

```sh
node --test prototypes/m06-reinigungsfall/reinigungsfall.test.cjs
node prototypes/m06-reinigungsfall/build.cjs
```

Der Build benötigt einen frischen Ausgabeordner und prüft Syntax, lokale HTML-Verweise sowie die explizite Liste öffentlicher Dateien. Er kopiert zehn Dateien in `dist/reinigungsfall-pages`; dieser erzeugte Ordner wird nicht versioniert.

Der Workflow `Reinigungsfall Pages` prüft Pull Requests. Ausschließlich ein manueller Start auf `main` veröffentlicht unter der bestehenden Pages-Adresse. Die beiden historischen Veröffentlichungsworkflows bleiben unverändert. Der gesamte V2-Entwicklungsbranch wird für diese Vorschau nicht integriert.

`sw.js` beendet die Registrierung des vorherigen technischen Offline-Fixtures. Es löscht weder Caches noch Lernstände und lädt keine offene Seite neu. Bei einem bereits geöffneten alten Stand einmal neu laden; der direkte Link `reinigungsfall.html` vermeidet die alte Startseite.
