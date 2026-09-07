# IUM-V2-FU-MOD – erstes V2-Referenzmodul

Stand: 7. September 2026. **Spezifikation zur Nutzerabnahme (`review`).**

Gewählt ist R5-M06 **„Präzise Abläufe entwickeln und prüfen“** für Klasse 5 am Gymnasium, Niveau E. Der neue Kontext „Prüffahrt im Raster“ führt von grafischen Anweisungen über ausführbaren Code und begründete Revision zum Transfer auf eine Prüfstation. Entwicklungsreihenfolge und Unterrichtsreihenfolge bleiben getrennt; M06 ersetzt nicht M01 als Unterrichtseinstieg.

- [Vollständiges Moduldesign mit Auswahl, Aufgaben, Materialien, Hilfen, Zeit, Rückkehr und technischen Übergaben](../../../../docs/superpowers/specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md)
- [Strukturierte Bindung an sieben Curriculumrecords, LXF und R5](specification.json)
- [Synthetische Prüfung der vorhandenen Bewegungssemantik](semantics-probe.mts) und [Ergebnis](semantics-results.json)
- [Prüfbericht, Selbstreview und offene reale Nachweise](validation-report.md)

Der ausdrückliche FU-MOD-Auftrag folgt auf die [FU-TECH-Abnahme](../technical/acceptance.json) an Commit `69634c56d3d100d3bf33632f29a4f98eaf579276`. Diese ist der Repositoryinput dieses Designs. IUM16 wird als Gesamtkomposition ersetzt; IUM18 liefert nur einen noch anzupassenden Bewegungsteil; LXP02 wird für Orientierung, Fokus und Rückkehr begrenzt genutzt. Alte Lieferszenarien, elf Pflichtphasen, Payload und V1-Materialien werden nicht übernommen.

Die 225 Minuten sind neu auf fünf Termine verteilt und entsprechen exakt den fünf R5-Zeitkomponenten. Es gibt sieben geplante Produktspuren P0–P6, einen begrenzten Materialvertrag und alle zwölf LXF-Gatebezüge. Die Materialmengen und Zeitannahmen sind noch nicht mit einer realen Klasse erprobt. Ein Daten-/Vertragscheck ist keine fachliche Nutzerabnahme.

V2 bleibt aktive Planungs-/Entwicklungsbaseline, V1 Produktstand. Das Paket ist kein Produktmanifest; Code, Registry und Lernmaterialproduktion wurden nicht begonnen. Acht TECH-Befunde, reale Zugänglichkeit, Schule/Betreiber/Rechte und Curriculumabdeckung bleiben offen. Pilot `not-started`, Nutzung/Geräteprüfung `not-run`, Veröffentlichung `closed`, LXP05 unintegriert. Historische AUD/R5/CUT-Siegel bleiben erhalten; aktueller Folgeauftrag wird additiv hier und in der Workspace-Task geführt.

Nächste Entscheidung: **Moduldesign annehmen oder konkret nacharbeiten lassen.** Erst aus einem angenommenen Design darf ein Implementierungsplan entstehen. FU-PILOT bleibt ein eigener Auftrag; weder Designabnahme noch Prüfskript erteilen eine Einsatzfreigabe.
