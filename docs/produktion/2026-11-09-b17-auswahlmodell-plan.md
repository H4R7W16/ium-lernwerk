# B17 Auswahlmodell · Plan und Inhaltsbrief

09.11.2026 · Ausgang df78c190b974e046537a7b7618c57bdc3c594a8f · feat/ium-lernbogen-pilot-20261107.
Inline-Produktion und Selbstreview nach projektspezifischem Lernwerk-Qualitätszyklus. Nutzer beauftragt MP-B17-01; keine neue Unterrichtskonzeption oder Veröffentlichung.

## Zweck und Lernbewegung vor Eingriff

Klasse 6, etwa 11–12 Jahre. Räumlich sichtbare Trennung von Kennung/aktueller Seite im Browser und früherer Besuchsliste beim Anbieter; darauf zwei offene Regeln. Zettel-/Listenweg bleibt gleichwertig. Eine optionale native aufklappbare Bildschirmhilfe ersetzt bei Wahl das Zettelauslegen, keine doppelte Pflichtausführung.

M03: Erkennen15 → Wirkung15 → Daten20 → Modell20 → B42-Fluss25 → eigene Werbekarte25 → Revision30 → Eigenbezug30 (neutral10/privat15/privatsichern5) → Transfer/Sicherung30. 210 Kernminuten. Vorab8 M02-Minuten, später6 vorM06 und6 vorM07 separat. B42 und Datenfluss bleiben eigener neuer Fall, kein automatisches Diagramm. Echte Gestaltung/Revision und private Wege bewahren.

## Konkretes Modell

Ein vorhandener eigener Fall, keine neue Fallauswahl: frühere Besuche Lesen/Zeichnen/Zeichnen, aktuelle Seite Lesen, Kennung B17. Regel K nur aktuelle Seite; V zählt nur frühere Besuche; Gleichstand verwendet K. Aktuelle Seite zählt nie in Verlauf. Bestehendes vorgemachtes Zweibesuch-Beispiel zeigt Gleichstand; eigener Dreibesuch-Fall kann mathematisch keinen Gleichstand bilden. Allgemeine Kernfunktion wird auch für Gleichstände geprüft.

Zustände: predict-start → choose → predict-change → compare. Startprüfung erst nach eigener Vorhersage, dann genau einen Besuch wählen; andere Wahl vor zweiter Prüfung ersetzt die Auswahl statt weitere Daten zu ändern. Neue Ergebnisse bis „Änderung prüfen“ verborgen. Vergleich zeigt Zählung/benutzte Daten, keinen Richtig-/Falsch-Score. Nach abgeschlossener Prüfung nur Reset; keine wiederholte Klicksuche ohne neue Vorhersage. Reset verändert die fachliche Versuchsspur nicht.

UI: Browser mit Kennung B17 und fester aktueller Seite; Anbieter mit zugeordneter Dreierliste und nativer Radiowahl; getrennte K/V-Auswertung. Vorhersage/Erklärung bleiben in vorhandener Antwortspur oder mündlich/auf Papier. Keine neuen Antwortfelder, kein neuer Tooladapter oder Erfolgsstatus. Zustand nur im Arbeitstab, beim Wiederöffnen Start. Bedienereignisse bleiben im Modell, um keinen falschen Speicherstatus für die allgemeine Arbeit zu erzeugen. Keine Cookies, echte Verlaufserfassung, Netzaufrufe oder Speicherung durch das Modell.

## Technische Einbindung und Schnittstellen

- Neu: prototypes/shared/b17-model.js (UMD, Browser und Node), b17-model.css, b17-render.cjs und b17-model.test.cjs.
- Exporte Modell: evaluate(current, visits) → {context,history,counts,tie}; createState(); transition(state, action, index); historyFor(state). Aktionen CHECK_START, CHOOSE_VISIT, CHECK_CHANGE, RESET.
- Renderer render(paper=false) mit nativen Details/Buttons/Radios; assets(pack) nur für explizit aktiviertes Modell.
- Bestehenden Autorenvertrag gezielt um selectionModel:true erweitern, nur grade6/area werbung/step modell/task versuch. Klasse5 und andere Inhalte bleiben unberührt.
- class5-content.cjs validiert Flag und ergänzt Widget am bestehenden Aufgabenblock; Papierausgabe rendert unveränderten Kartenweg ohne Widget.
- class6-render.cjs lädt CSS/JS nur bei data-b17-model und stellt zwei kleine Laufzeitdateien bereit.
- werbung.json: Flag und alternative Arbeitsanweisung, Lehrhinweise/Briefing/Medienentscheidung gleichzeitig; class6-teacher-pages.cjs Reihenkommentar anpassen. Keine neuen Quellen-/Rechtsbehauptungen.
- Paket-ID/Version 2.0.0 und bestehende Felder bleiben für vorhandene Arbeitsdateien kompatibel. Git/QA binden die Inhaltsrevision; kein geändertes Antwortschema.

## Schritte und Prüfung

- [x] Tests zuerst: K/V getrennt, Beispielgleichstand, alle drei Eingriffe inkl. unverändertem Ergebnis, Zustand/Einzeleingriff/Reset, Fehlerfälle, Integration/Autorenvertrag/Papierweg/Feldbestand. Erwartetes Scheitern dokumentieren.
- [x] Kleine reine Regel-/Zustandsfunktionen, zugängliche UI/Renderer und eng begrenzte Einbindung implementieren; vorhandene Texte/Lehrhinweise nachführen.
- [x] Gezielt und vollständig testen, frischer Build und Vergleich zum Ausgang: alle fremden Lernwege/Medien schützen, Offlinepakete mit neuem JS/CSS prüfen.
- [x] Tatsächliche Desktop-/390px-/Tastaturprobe, beide Ergebniszweige und Reset; vorhandene Antwortspur bleibt erhalten. Text-/Bedienlast gegen Papieralternative abwägen, ganzen M03-Weg bearbeiten/prüfen.
- [x] Endfassung erfassen, kritischer Selbstreview mit Hürde/Umgehungsweg und Gewinnen/Verlusten; check/report, Fetch/Pull und lokaler Commit, Vorschau/Handoff.

## Reviewfokus

Vorhersage nicht automatisch bestätigen; aktuelle Seite nicht heimlich mitzählen; Kennung nicht als Liste zeigen; genau einen Eingriff zulassen; gleiche Ausgabe als gültigen Gegenfall erklären; keine falsche Speicherung oder Haken als Lernnachweis. B42 und späterer unbekannter gemeinsamer Browser bleiben Transfer mit Grenze. Neue räumliche Hilfe kostet Auswahl/Bedienung; echte Entlastung und 20-Minuten-Zeitbudget bleiben Unterrichtserprobung.
