# Medienanalyse Klasse 5 – Umsetzungsplan

> Ausführung: superpowers:executing-plans, durch Codex in dieser Sitzung. Keine Subagenten.
> Die fachliche Spezifikation wurde mit „mach das“ angenommen. Keine erneute Freigabeschleife.

**Ziel:** Ein eigenständig verständlicher zweiter Lernstudio-Prototyp „Ein Bild – zwei Geschichten“.
**Architektur:** Eigenständige statische Anwendung unter /medienanalyse/ mit fünf freien Hash-Zielen. Inhalte und Erklärungen in content.js; reine Bild-/Evidenzlogik in model.js; UI in app.js. Statische Lehr-, Wissens- und Materialseiten aus denselben Inhalten. Integration in vorhandenen Pages-Build.
**Stack:** HTML, CSS, Vanilla JavaScript (Node-22-kompatibles UMD), keine neue Abhängigkeit.
**Spezifikation:** Nutzerentscheidung dieser Sitzung; Vault-Task „2026-09-28 - IUM Medienanalyse als zweiten Klasse-5-Prototyp umsetzen“.

## Bedingungen
- Klasse 5, Schul-iPad, alle Schritte frei erreichbar, keine Pflichtfreischaltungen.
- Hauptfall Schulfest; Transfer Bibliothek. KI-Illustrationen und erfundene Situationskarten ausdrücklich kennzeichnen.
- Beobachtung, Deutung und zusätzliche Materialangaben unterscheiden. Originalbild nicht als vollständige Wahrheit ausgeben.
- Bildausschnitt und Überschrift zunächst einzeln verändern; eigener Beitrag und eigene Begründung mit Revision.
- Nur geschlossene materialgebundene Aussagen automatisch rückmelden. Freie Antworten mit Kriterien/Beispielen, ohne automatische Benotung.
- Vollständige Erklärungen und Hilfen sowie unabhängig verwendbarer Materialbogen und Lehrpersonenbriefing.
- Speichern/Import/Export außerhalb des Umfangs, keine umfassenden Tests.
- Bestehende Anwendungen erhalten; isolierter Branch feat/medienanalyse-klasse5; Integration über PR auf main.

## Reviewfokus
- Ausschnitte außerhalb der Bildgrenzen: Zahlen begrenzen, feste Bildproportion.
- Freier Text mit HTML-Zeichen: als Text darstellen.
- Unbeantwortete Evidenzfragen: konkret als offen ausweisen; keine Erfolgsbehauptung.
- Wechsel zwischen Schritten: Entwurf/Notizen in der laufenden Seite erhalten; keine automatischen Musterlösungen im Entwurf.
- Lehrweg ohne JavaScript: Bilder, Aufgaben, fachliche Antworten und Direktlinks vollständig.

## Task 1: Material und Modell
Dateien: prototypes/m05-medienanalyse/{content.js,model.js,model.test.cjs,assets/schulfest.png,assets/bibliothek.png,ASSETS.md}
- [x] Vier kleine Verhaltenstests für Cropgrenzen, Ein-Faktor-Vergleich, Evidenzrückmeldung und Text-Escaping schreiben und rot ausführen.
- [x] crop({x,width}), experiment(mode,crop,headline), assess(answers), escapeHtml(value) implementieren; Inhalte mit fünf Schritten und getrennten Belegarten erstellen.
- [x] Bilddateien übernehmen, verwendete Prompts und Herkunft dokumentieren. Keine nachträglichen Fakten aus Bilddetails erfinden.
- [x] Dieselben Tests grün ausführen.
Erwartung: vier bestandene Tests, keine Prüfung ausgeschlossener Funktionen.

## Task 2: Lernumgebung und eigenständiges Material
Dateien: prototypes/m05-medienanalyse/{index.html,app.js,style.css,guides.cjs,README.md}
- [x] Fünf frei anwählbare Schritte mit Hilfen, eigener Beobachtung, kontrolliertem Vergleich, Aussagenprüfung, Beitragseditor und Transfer umsetzen.
- [x] Direkte DOM-Updates für Editor und Slider; Fokus erhalten. Muster erst auf Wunsch öffnen.
- [x] Statische Wissen-/Lehr-/Materialseiten rendern; Materialbogen ohne Lösungen, Lehrseite mit Musterantworten, Zeitannahmen und Fehlvorstellungen.
- [x] Browser: Hauptweg, Schrittwechsel, Bearbeitung nach Selbstcheck, Transfer und 1024/768/390-Breite prüfen.
Erwartung: sichtbare Bild-/Textänderungen, keine Pflichtreihenfolge, keine horizontale Überbreite.

## Task 3: Integration, begrenzte Prüfung, Übergabe
Dateien: prototypes/m06-reinigungsfall/build.cjs, pages-build.test.cjs; .github/workflows/selbstlernen-pages.yml; Lernstudio-index.html
- [x] Neue öffentliche Dateiliste einschließlich Binärbilder und /medienanalyse/ integrieren; statische Links prüfen.
- [x] Gezielter neuer Buildvertrag; anschließend ausschließlich neue Modelltests und Pages-Dateiprüfung sowie Syntax/Build.
- [x] Kleiner Browserreview und fachlicher Gegencheck; Grenzen in QA.md dokumentieren.
- [ ] Fetch/FF-Pull, Commit, Push und PR; bestehendes öffentliches Projekt um das angenommene Modul ergänzen.
- [ ] Task, Projekt, Initiative, Kanban und Session aktualisieren.

## Fortschritt
- Plan geprüft: alle fünf fachlichen Schritte, eigener Beitrag und Lehrweg abgedeckt.
- Ausgangspunkt: cf82254; Git-Status sauber und Fetch/FF-Pull erfolgreich.
- Bildgenerierung: beide gewünschten Szenen vorhanden und visuell passend.
