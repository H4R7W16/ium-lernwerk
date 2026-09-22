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
