# IuM-Lernwerk

Offenes, digitales Lernwerk für Informatik und Medienbildung am Gymnasium in Baden-Württemberg, Klassen 5 bis 7. Das Vorhaben verbindet einen verbindlichen Kernlernweg mit flexibel einsetzbaren Vertiefungs-, Transfer- und Projektmodulen.

## Phase 0: Forschungs- und Curriculumfundament

Phase 0 erstellt die überprüfbare Grundlage für spätere Lernmodule. Sie enthält Quellenregister, kuratierte Claims, quellentreue Curriculumdaten, ein Fachprofil sowie eine Modulroadmap. Eine Lernendenanwendung gehört nicht zu dieser Phase.

Der Phase-0-Abschlussreview vom 29. Juli 2026 weist den Bestand als **reviewfähig mit offenen Lücken** aus. Alle 171 curricularen Anforderungsrecords sind einem Kernkandidaten zugeordnet; 111 sind auf Kandidatenebene `covered`, 60 bleiben mit recordgenauer Begründung `partial`. Die Jahreskorridore von 31–44, 35–50 und 54–78 Einheiten sind für Klasse 5 `amber` und für die Klassen 6 und 7 `red`. Daraus folgt ausdrücklich weder eine Vollabdeckungs- noch eine Umsetzbarkeitsfreigabe.

Zentrale Einstiege:

- [Abschlussreview und Forschungsarchitektur](docs/research/phase-0/README.md)
- [Forschungssynthese](docs/research/phase-0/synthesis.md)
- [Fachprofil Gymnasium 5–7](docs/fachprofil/ium-gymnasium-5-7.md)
- [Curriculum-Crosswalk](curriculum/crosswalk.json) und [begründete Progression](curriculum/progression.md)
- [Modulroadmap](roadmap/module-roadmap.md) und [recordgenauer Abdeckungsplan](roadmap/coverage-plan.json)
- [verbindliche Gesamtspezifikation](docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md)
- [IUM09-Spezifikation zur curricularen Partial-Nacharbeit](docs/superpowers/specs/2026-07-29-ium09-curriculare-partial-nacharbeit-design.md), [Implementierungsplan](docs/superpowers/plans/2026-07-29-ium09-curriculare-partial-nacharbeit-implementation.md) und [Nacharbeitsledger](roadmap/coverage-remediation.json)

Die Ausgangsbilanz wird erst durch die dokumentierten modulweisen Audits verändert; der Ledger legt keine Endbilanz vorweg.

Vor jeder Phase-1-Spezifikation stehen vier getrennte Nutzerentscheidungen: Forschungsbasis, Fachprofil, curriculare Vollständigkeit und Modulroadmap. Die offenen `partial`- und Zeitlücken dürfen dabei angenommen, revidiert oder zur Nacharbeit zurückgegeben, aber nicht durch eine pauschale Freigabe unsichtbar gemacht werden.

## Validierung

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_phase0.py
```

## Lizenzen

Eigener Validierungscode steht unter der [MIT-Lizenz](LICENSE). Eigene inhaltliche Repository-Beiträge stehen unter [CC BY-SA 4.0](LICENSE-CONTENT.md), sofern eine Datei nicht ausdrücklich etwas anderes festlegt. Material Dritter behält seine jeweils ausgewiesene Lizenz.
