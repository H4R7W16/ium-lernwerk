# Sauber geplant · Reinigungsroboter

[Vorschau im Browser öffnen](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall.html#einstieg) – ohne Installation oder Anmeldung.

Interaktiver Konzeptstand vom 13. September 2026 für IuM, Klasse 5. Drei Grundrisse verbinden einzelne Befehle, Wiederholungen, Fehlerdiagnose und einen eigenen Reinigungsplan. Zurück am Start bedeutet noch nicht, dass die gesamte Fläche gereinigt ist.

Diese Beschreibung macht den aktuellen Stand für einen kleinen Kreis nachvollziehbar. Eindrücke und Probleme bitte direkt an Jan zurückmelden. Es gibt keinen vorgegebenen Prüfauftrag und keinen zusätzlichen Rückmeldekanal.

## Ausprobieren und nachvollziehen

Der Lernweg links führt von den ersten Befehlen zum eigenen Plan. Du kannst zwischen den Aufgaben wechseln, einzelne Aktionen oder den ganzen Code ausführen und deine Eingaben innerhalb der Sitzung wieder aufrufen. Für die eigene Ablaufgrafik werden Papier und Stift benötigt.

[Aufgaben, Musterlösungen und Ablauf für fünf Unterrichtseinheiten](https://github.com/H4R7W16/ium-lernwerk/blob/4abbe6c2225e608f9bc10c9ae9a4028477235864/docs/planning/ium-5-7/m06-reinigungsfall.md) erklären die didaktische Planung. Die Vorschau selbst zeigt nur diesen M06-Lernfall, nicht das gesamte Lehrwerk. [Planung für die Klassen 5–7](https://github.com/H4R7W16/ium-lernwerk/blob/4abbe6c2225e608f9bc10c9ae9a4028477235864/docs/planning/ium-5-7/README.md).

## Umfang und Grenzen

Freie Programme bestehen aus `vor`, `links`, `rechts` und `wiederhole 2–9 [1–5 Grundbefehle]`. Keine Verschachtelung, höchstens 100 Aktionen. Die Startkachel zählt als gereinigt. Vorhersagen, Codefassungen und ausgewählte Ergebnisse lassen sich vergleichen. Ablaufgrafiken werden auf Papier erstellt.

**Eingaben bleiben ausschließlich bis zum Neuladen oder Schließen erhalten.** Dauerhaftes Speichern und verlässlicher Offlinebetrieb fehlen noch. Eine erfolgreiche Fahrt bewertet keine Erklärung; automatisierte Tests belegen keine Lernwirkung. Der Modellroboter reagiert nicht auf Sensoren oder neu auftauchende Hindernisse.

[Früheren Prüffahrt-Entwurf im Browser öffnen](https://h4r7w16.github.io/ium-lernwerk/prueffahrt.html) – nur als Vergleich zum aktuellen Reinigungsfall.

## Lokal öffnen und technisch prüfen

Nach dem Herunterladen oder Klonen des Repositories lässt sich `prototypes/m06-reinigungsfall/reinigungsfall.html` direkt im Browser öffnen. Für die Vorschau werden keine zusätzlichen Pakete benötigt. Alternativ vom Repo-Stamm mit vorhandenem Python starten:

```sh
python -m http.server 43862 --bind 127.0.0.1 --directory prototypes/m06-reinigungsfall
```

Anschließend `http://127.0.0.1:43862/reinigungsfall.html` öffnen. Der Server ist nur auf dem eigenen Rechner erreichbar.

Die Modelltests benötigen Node.js; der Veröffentlichungsworkflow verwendet Version 22.20.0. Vom Repo-Stamm:

```sh
node --test prototypes/m06-reinigungsfall/reinigungsfall.test.cjs
```

Die acht Tests prüfen unter anderem Drehungen, Wiederholungen, Randfehler, die ausgelassene Mitte und zwei unterschiedliche vollständige Reinigungspläne. Sie ersetzen keine Erprobung mit Lernenden.

Die zugehörigen Dateien lassen sich auch [direkt auf GitHub lesen](https://github.com/H4R7W16/ium-lernwerk/tree/main/prototypes/m06-reinigungsfall): `reinigungsfall-core.js` enthält Modell und Ausführung, `reinigungsfall.js` die Aufgaben und Bedienung, `reinigungsfall.test.cjs` die Modelltests.

## Veröffentlichung und Prüfung

Die statischen Quelldateien stammen aus dem geprüften Workspace-Prototyp `Shared/Prototypes/ium-v2-ux01`. Die Reinigungsansicht ist zusätzlich der Start unter `index.html`. Ihr Rückverweis führt zum erhaltenen Prüffahrt-Entwurf. Ein `noindex`-Hinweis ist keine Zugriffskontrolle; GitHub Pages ist öffentlich.

Veröffentlichungsbuild vom Repo-Stamm:

```sh
node prototypes/m06-reinigungsfall/build.cjs
```

Der Build benötigt einen frischen Ausgabeordner und prüft Syntax, lokale HTML-Verweise sowie die explizite Liste öffentlicher Dateien. Er kopiert zehn Dateien in `dist/reinigungsfall-pages`; dieser erzeugte Ordner wird nicht versioniert.

Der Workflow `Reinigungsfall Pages` prüft Pull Requests. Ausschließlich ein manueller Start auf `main` veröffentlicht unter der bestehenden Pages-Adresse. Die beiden historischen Veröffentlichungsworkflows bleiben unverändert. Der gesamte V2-Entwicklungsbranch wird für diese Vorschau nicht integriert.

`sw.js` beendet die Registrierung des vorherigen technischen Offline-Fixtures. Es löscht weder Caches noch Lernstände und lädt keine offene Seite neu. Bei einem bereits geöffneten alten Stand einmal neu laden; der direkte Link `reinigungsfall.html` vermeidet die alte Startseite.
