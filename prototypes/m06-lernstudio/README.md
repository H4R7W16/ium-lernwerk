# Lernstudio · Sauber geplant

Zusätzliche eigenständige Prüffassung des M06-Beispielinhalts. Öffentlich unter /lernstudio/. Die bisherigen Fassungen bleiben erhalten; die Lernwerkstatt verlinkt das Lernstudio im Versionsmenü.

## Gestaltungsentscheidungen

- **Zusammengehöriges gemeinsam zeigen:** Programm und Raum stehen auf Tablets nebeneinander. Jede ausgeführte Anweisung wird am zugehörigen Baustein markiert. Ort, Blick, Schleifendurchlauf und erreichte Kacheln bleiben sichtbar.
- **Lernhandlungen statt bloßer Klickaktivität:** Endzustand vorhersagen, Schleifenkörper ausschreiben, Fehler reparieren, Teilpläne verändern, eigene Flächenlösung begründen, eine Behauptung widerlegen und auf eine andere Maschine übertragen.
- **Hilfen schrittweise reduzieren:** Erst untersuchen, dann ein vollständiges Beispiel, anschließend anpassen und selbst planen. Zwei Hinweise und die ausführliche Erklärung stehen am jeweiligen Auftrag bereit.
- **Gezieltes Feedback:** Fahrtergebnis und begründeter Selbstcheck sind getrennt. „Check gelöst“ bescheinigt nur diese einzelne Antwort, keine allgemeine Kompetenz. Wiederholte oder unterstützte Antworten bleiben unterscheidbar.
- **Gesteuerte Bewegung:** Start/Pause, einzelner Schritt, ein Schleifendurchlauf, Rückschritt, Neustart und drei Tempi. Auch ein Durchlauf zeigt seine einzelnen Aktionen. Pausieren bei Tabwechsel; CSS respektiert reduzierte Bewegung.
- **Bedienbare Tablet-Oberfläche:** mindestens 44 CSS-Pixel große Schaltflächen, kein zwingendes Ziehen, zugängliche Dialoge und Tastaturfokus, eine Spalte auf schmalen Geräten. Ausführliche Erklärung und Auflösung werden gezielt geöffnet.
- **Lernstand bewusst speichern:** Sitzung standardmäßig im Arbeitsspeicher. Gerätespeicherung erst nach Opt-in; separater Schlüssel ium-lernstudio-v1. Keine Telemetrie und keine Übermittlung von Antworten.

Die Entscheidungen beziehen sich auf das Forschungsdossier vom 23.09.2026: Cognitive Load Theory / Multimedia Learning (Sweller; Fiorella & Mayer), ICAP (Chi & Wylie), angeleitetes Entdecken (Lazonder & Harmsen), Selbsterklärung und Feedback (Bisra; Wisniewski), Abrufübungen (Agarwal) sowie WCAG/COGA als Gestaltungsstandards. Dies ist eine begründete Designübertragung, kein Nachweis einer bereits gemessenen Lernwirkung.

## Technische Grenzen

Die fachlichen Inhalte und der Simulator werden aus den vorhandenen Selbstlern- und Lernwerkstatt-Modellen eingebunden. Das Lernstudio besitzt eine eigene Darstellung, Checkfragen und ein eigenes Zustandsmodell. Es unterstützt dieselbe Sprache: vor, links, rechts sowie nicht verschachtelte Schleifen mit 2–9 Durchläufen und 1–5 Anweisungen im Körper. Maximal 30 Bausteine im Editor; die Simulation stoppt spätestens nach 100 Aktionen.

## Gezielt prüfen

Node 22:

    node --test prototypes/m06-selbstlernen/material.test.cjs prototypes/m06-reinigungsfall/pages-build.test.cjs prototypes/m06-lernfassung3/journey.test.cjs prototypes/m06-lernwerkstatt/workshop.test.cjs prototypes/m06-lernstudio/studio.test.cjs
    node prototypes/m06-reinigungsfall/build.cjs <frisches-ausgabeverzeichnis>

Keine Import-/Exporttests oder Gesamtsuite erforderlich. Die Veröffentlichung übernimmt ausschließlich die vier Laufzeitdateien dieses Ordners. Tests und dieser interne Hinweis werden nicht ausgeliefert.

Reale Schul-iPads, assistive Technik, Zoom und die Lernwirkung müssen im Unterricht separat erprobt werden. Browser-Viewports ersetzen diesen Nachweis nicht.

## Konsolidierter Klasse-5-Prototyp · 27.09.2026

Das bestehende Lernstudio ist die ausgewählte Ausbau-Basis. Alle elf Stationen bleiben frei anwählbar und als Hash-Links erreichbar. Die Klasse-5-Inhalte in `studio-learning.js` ergänzen die gemeinsame fachliche Simulation, ohne andere Fassungen umzuschreiben.

- Kurze Voraussetzungen, sichtbare Merksätze, freiwilliger Befehlsversuch, Satzanfänge und Erklärungskriterien.
- Direkte Tasten für vor/links/rechts; Bausteine und Schleifen werden neben dem Modell bearbeitet. Vor dem Ausführen Änderungen übernehmen oder abbrechen.
- Optionale Spur, schrittweise Zeitleiste und Vergleich zweier Versuche am gleichen Schritt.
- Aufgabenrückmeldung folgt dem tatsächlichen Plan bzw. der Vorhersage. Eine Zusatzfrage bestätigt keinen ungeprüften eigenen Plan; freie Erklärungen werden nicht automatisch bewertet.
- `wissen.html`: alle Erklärungen, Startbilder, Lösungen und ein ausgearbeiteter Spaltenweg als Alternative zum Reihenweg.
- `lehrkraft.html`: selbstständig lesbare Lehrübersicht mit Startbildern, Programmen, Erklärideen, Gesprächsimpulsen, Antworten und direkten Übungslinks. Unterrichtsgespräch und Vortrag können einzelne Inhalte übernehmen, ohne digitalen Pflichtdurchlauf.

Beide Leseseiten werden aus `studio-guides.cjs` und derselben Inhaltsschicht beim vorhandenen Pages-Build erzeugt. Sie benötigen kein JavaScript. Für die vollständige Vorschau den Build nutzen, nicht nur die Quell-index.html öffnen:

```text
node prototypes/m06-reinigungsfall/build.cjs <frisches-lokales-Ausgabeverzeichnis>
```

Danach das Ausgabeverzeichnis mit einem lokalen statischen Server bereitstellen und `/lernstudio/` öffnen. Die Ausgabe enthält 39 Dateien. Der öffentliche Einstieg wird erst bei einer gesonderten Veröffentlichung aktualisiert.

Gezielte neue Verhaltenstests: `node --test prototypes/m06-lernstudio/studio-learning.test.cjs`. Prüfumfang und Grenzen: `QA-KLASSE5.md`.
