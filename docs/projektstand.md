# IuM-Lernwerk – Projektstand

Dokumentationsstand: **06.11.2026**, abgeglichen mit `main` an [d57db00](https://github.com/H4R7W16/ium-lernwerk/commit/d57db00). Spätere Änderungen stehen in der [Commit-Historie](https://github.com/H4R7W16/ium-lernwerk/commits/main/).

## Aktuell veröffentlicht

Die gemeinsame Pages-Ausgabe enthält die Jahrgänge [5](https://h4r7w16.github.io/ium-lernwerk/klasse5/), [6](https://h4r7w16.github.io/ium-lernwerk/klasse6/) und [7](https://h4r7w16.github.io/ium-lernwerk/klasse7/). Klasse 7 hat einen gemeinsamen Einstieg für Daten, Medien, Programmieren und Gaming, 22 Kernaufgaben und 29 zugeordnete Lernziele.

Das [Gesamtkonzept](../prototypes/shared/gesamtkonzept.json) verbindet die Jahrgänge durch Progression, Nachweise, Wiederaufnahme und Übergänge. Seine derzeitigen Zeitkonten betragen 1710 Minuten für Klasse 5, 1710 Minuten für Klasse 6 und 1620 Minuten für Klasse 7, jeweils einschließlich der dort ausgewiesenen Diagnose-, Organisations-, Unterstützungs- und Pufferanteile. Diese aktuellen Planungsdaten sind vom früheren IUM10-/Working-40-Modell zu unterscheiden.

Die Lernseiten bieten Aufgaben und Materialien für die Lernenden; Jahresleitfäden, Durchführungshinweise, Briefings und Sicherungen unterstützen die Lehrpersonen. Der [Repo-Einstieg](../README.md) verlinkt die passenden Jahrgangsseiten.

## Jüngste integrierte Änderungen

| Datum | Änderung | Nachweis |
| --- | --- | --- |
| 03.11.2026 | Gesamtkonzept 5–7 in die Lernwerk-Ausgabe integriert | [Konzeptdaten und Ausgabestufe](../prototypes/shared/gesamtkonzept.cjs) |
| 05.11.2026 | Themen-, Aufgaben-, Material- und Briefingwege verbessert | [PR 50](https://github.com/H4R7W16/ium-lernwerk/pull/50) |
| 05.11.2026 | Gerätebezogene Arbeitswege für iPad und Windows ergänzt | [PR 51](https://github.com/H4R7W16/ium-lernwerk/pull/51) |
| 05.11.2026 | Fizz-Spot V4 und Hörvergleich in MED-1 eingebunden | [PR 52](https://github.com/H4R7W16/ium-lernwerk/pull/52) |
| 06.11.2026 | Kopfzeile und Themenmenü von Klasse 7 an Klasse 5/6 angeglichen | [PR 53](https://github.com/H4R7W16/ium-lernwerk/pull/53) |
| 06.11.2026 | Veröffentlichungsprüfungen an das neue Menü angepasst und drei Klasse-7-Vertragstests in die PR-CI aufgenommen | [PR 54](https://github.com/H4R7W16/ium-lernwerk/pull/54) |

Die aktuellen Änderungen werden im [Pages-Workflow](https://github.com/H4R7W16/ium-lernwerk/actions/workflows/klasse5-pages.yml) gebaut. Der Workflowverlauf zeigt den jeweiligen Veröffentlichungsstand; ein PR oder erfolgreicher Plattformtest allein belegt noch kein Pages-Deployment.

## Offene Grenzen und nächste Arbeit

- **Erprobung:** Reale Lernwirkungen, Bearbeitungszeiten sowie der vollständige Ablauf auf Schulgeräten und in Schulnetzen sind noch zu prüfen. Bestehende automatisierte Prüfungen und einzelne Browser-Sichtungen ersetzen diese Erprobung nicht.
- **Zeit in Klasse 6:** Die im Gesamtkonzept vorgesehenen 38 tatsächlich verfügbaren Unterrichtseinheiten sind als schulische Voraussetzung noch zu bestätigen.
- **Arbeitsübersicht in Klasse 7:** „Deine Arbeit“ ist dort noch nicht implementiert. Dokumente, Heftprodukte, Bilder und Snap!-XML werden bislang über die jeweiligen Aufgabenwege gesichert. Ein Konzept für eine gemeinsame Übersicht ist eine eigene Weiterentwicklung.
- **Medienproduktion:** Weitere Bild- und Filmfassungen können sich in separaten Arbeitsständen befinden. Erst die Integration ihrer geprüften Quellen macht sie zum Bestandteil dieser Website.
- **Speicherung und Offlinebetrieb:** Klasse 5/6 und die Klasse-7-Werkzeuge haben unterschiedliche Funktionen. Kein pauschales Versprechen geräteübergreifender Synchronisierung oder vollständiger Offline-Verfügbarkeit.

## Aktuelle Website und historische Grundlagen

Der [Pages-Generator](../prototypes/pages/README.md) veröffentlicht die aktuelle Website aus `prototypes/`. Die älteren Stränge unter `apps/`, `packages/`, `modules/`, `pilot/`, `curriculum/` und `roadmap/` bleiben als Entwicklungsgrundlagen und geprüfte Vertragsstände erhalten. Sie besitzen eigene Tests und Statusgrenzen.

Insbesondere werden das historische Working-40-Zeitmodell, Pilotgates oder Gerätestatus durch eine neue Lernseite nicht automatisch freigegeben. Die dazugehörigen gebundenen Abschnitte sind im aufklappbaren historischen Teil der [README](../README.md) erhalten.
