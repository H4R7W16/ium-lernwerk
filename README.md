# IuM-Lernwerk

Offenes, digitales Lernwerk für Informatik und Medienbildung am Gymnasium in Baden-Württemberg, Klassen 5 bis 7. Der Lernwerk-Kosmos verbindet verbindliche Kernpfade mit ausdrücklich erhaltenen Vertiefungs-, Transfer- und Projektmodulen.

## Phase 0: validierte Grundlage

Phase 0 umfasst Forschungsbasis, Curriculumdaten, Fachprofil, Modulverträge, Coverageaudit und das IUM10-Zeitmodell. Eine Lernendenanwendung und die Planung von Phase 1 gehören noch nicht zu diesem Stand.

Das IUM10-Zeitmodell hat den Status `working`. Die vollständigen Jahresvarianten und Bedarfsszenarien sind aus dem maschinenlesbaren Zeitmodell abgeleitet:

### Zeitmodell in Zahlen

| Klasse | Verfügbare Pfade (UE) | Bedarf ohne Angebot (UE) | Zeiturteil |
| --- | --- | --- | --- |
| 5 | 30/34/38 | — | green |
| 6 | 30/34/38/38/38 | — | green |
| 7 | — | 40/46/54 | red |

Die drei 38-UE-Pfade der Klasse 6 bilden unterschiedliche Erweiterungen ab. Für Klasse 7 ist keine der Bedarfsrechnungen ein verfügbares Jahresangebot; das Zeiturteil bleibt `red`.

Status: **Auftraggeber-Zeitfreigabe ausstehend**. `working` bedeutet reviewfähig und ungepilotiert, nicht freigegeben. Semantische Coverage, Zeitmachbarkeit, Sequenznachweis und Pilotstatus werden getrennt beurteilt:

- aktuelle IUM10-Coverage: 166 `covered` / 5 `partial`;
- historische IUM09-Projektion: 164 `covered` / 7 `partial`;
- 60/60 Zeitreviews und 4/4 Sequenznachweise sind dokumentiert;
- Pilotaufträge bleiben modulaggregiert und nichtpersonal, ohne persönliche Diagnostik oder Telemetrie.

In der historischen IUM09-Projektion gilt weiterhin: 164 sind auf Kandidatenebene `covered`, 7 bleiben `partial`. Von 60 Ausgangslücken wurden 53 geschlossen; 7 bleiben im Ledger offen. Trotz der verbesserten semantischen Coverage ist das Lernwerk weiterhin zeitlich nicht freigegeben.

Flexible Vertiefungs-, Transfer- und Projektmodule bleiben sichtbar und ersetzen keine fehlende Kernzeit. Digital ist das selbstverständliche Unterrichtsmedium; analoge Materialien werden nur eingesetzt, wenn die Lernhandlung ihre Verwendung didaktisch begründet. Eine zwanghafte Doppelstruktur ist nicht vorgesehen.

## Zentrale Einstiege

- [Validierte Modulroadmap](roadmap/module-roadmap.md)
- [Autoritatives IUM10-Zeitmodell](roadmap/time-model.json)
- [Recordgenauer Abdeckungsplan](roadmap/coverage-plan.json)
- [IUM10-Validator](scripts/validate_ium10.py)
- [IUM09-Validator](scripts/validate_ium09.py)
- [Gesamtvalidator Phase 0](scripts/validate_phase0.py)
- [Fachprofil Gymnasium 5–7](docs/fachprofil/ium-gymnasium-5-7.md)
- [Curriculum-Crosswalk](curriculum/crosswalk.json) und [begründete Progression](curriculum/progression.md)
- [Forschungsarchitektur](docs/research/phase-0/README.md) und [Forschungssynthese](docs/research/phase-0/synthesis.md)
- [Verbindliche Gesamtspezifikation](docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md)

IUM10 ist nach getrenntem Fach- und Engineeringreview reviewfähig. Die Zeitfreigabe und der Klasse-7-Entscheid bleiben Auftraggebergates; Phase 1 bleibt bis zu einem gesonderten Nutzerentscheid ungeplant.

## Validierung

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
```

## Lizenzen

Eigener Validierungscode steht unter der [MIT-Lizenz](LICENSE). Eigene inhaltliche Repository-Beiträge stehen unter [CC BY-SA 4.0](LICENSE-CONTENT.md), sofern eine Datei nicht ausdrücklich etwas anderes festlegt. Material Dritter behält seine jeweils ausgewiesene Lizenz.
