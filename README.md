# IuM-Lernwerk

Offenes, digitales Lernwerk für Informatik und Medienbildung am Gymnasium in Baden-Württemberg, Klassen 5 bis 7. Das Vorhaben verbindet einen verbindlichen Kernlernweg mit flexibel einsetzbaren Vertiefungs-, Transfer- und Projektmodulen.

## Phase 0: Forschungs- und Curriculumfundament

Phase 0 erstellt die überprüfbare Grundlage für spätere Lernmodule. Sie enthält Quellenregister, kuratierte Claims, quellentreue Curriculumdaten, ein Fachprofil sowie eine Modulroadmap. Eine Lernendenanwendung gehört nicht zu dieser Phase.

Der Forschungsrahmen liegt unter [docs/research/phase-0](docs/research/phase-0/README.md). Die verbindliche Gesamtspezifikation ist unter [docs/superpowers/specs](docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md) dokumentiert.

## Validierung

```powershell
python -m unittest tests.test_validate_phase0 -v
python scripts/validate_phase0.py
```

## Lizenzen

Eigener Validierungscode steht unter der [MIT-Lizenz](LICENSE). Eigene inhaltliche Repository-Beiträge stehen unter [CC BY-SA 4.0](LICENSE-CONTENT.md), sofern eine Datei nicht ausdrücklich etwas anderes festlegt. Material Dritter behält seine jeweils ausgewiesene Lizenz.
