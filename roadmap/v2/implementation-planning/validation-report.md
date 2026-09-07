# IUM-V2-PLAN – Autorenreview und Planprüfung

Stand: 2026-09-07. Eingang `150deea22ba9bcf3170915bb4b24852d376f6a8b`. FU-PILOT ist als Instrumentenspezifikation angenommen. Der Implementierungsplan selbst steht in `review`; kein Umsetzungspaket wurde gestartet.

## Prüfumfang

Der [Hauptplan](../../../docs/superpowers/plans/2026-09-07-ium-v2-referenzmodul-implementation.md) und seine zwei Teilpläne beschreiben acht sequenzielle Pakete. [plan.json](plan.json) enthält sämtliche Dateioperationen, optionale Änderungen mit Grund, Taskpfade, Abhängigkeiten und Modellvorschläge. [input-bindings.json](input-bindings.json) bindet 94 unveränderte technische/Spezifikationseingaben und drei Plandokumente. Hashvergleich normalisiert ausschließlich CRLF zu LF.

Die sechs automatisierten Prüfgruppen in `verify-plan.py` prüfen:

1. Historische und aktuelle Eingabehashes sowie die drei Planhashes.
2. Planungsumfang, FU-PILOT-Annahme und unveränderte Einsatzgrenzen.
3. Acht Pakete, Reihenfolge und genaue Dateipfade: Änderungen nur an bestehenden bzw. vorher angelegten Dateien, keine doppelte Neuerstellung.
4. Lokale Links der drei Plandokumente.
5. Repoänderungen ausschließlich im neuen Planungspaket und der additiven PILOT-Annahme; kein vorhandener Produkt-/CI-/Foundationcode geändert.
6. Vault-Tasks, Codex-Zuordnung, Abhängigkeiten, Review-/Abnahmestatus und Kanbanplatzierung, wenn `--vault` angegeben ist.

Der tatsächliche letzte Lauf ist maschinenlesbar in [validation.json](validation.json) dokumentiert. Die im Plan enthaltenen künftigen Verhaltens-/Browserprüfungen sind **noch nicht ausgeführt**. Dieser Verifier prüft Dokumentbindung und Arbeitsumfang, nicht die Güte einer zukünftigen Implementierung.

## Inhaltlicher Selbstreview

| Reviewpunkt | Ergebnis der Planprüfung |
| --- | --- |
| TECH-F01–03 | Gemeinsame Datenannahme, Original-Recovery und einmaliger aktueller Importkandidat in IMP02; konkrete Gegenbeispiele. |
| TECH-F04–06 | Atomarer Revisions-/Löschschutz, Wahl vor Speicherung, bewusster Export und Updatekoordination in IMP03/04. Frühe synthetische Browserhülle verhindert eine Abhängigkeit vom fertigen M06-UI. |
| TECH-F07 | Neutraler neuer Fachkern, eigene Grafik und eigener Code, fünfteiliger Schleifenkörper, begrenzte Daten sowie eigener Renderer in IMP05–07. |
| TECH-F08 | Historische Aktivierung mit 108 Siegeln von aktueller Entwicklung trennen; IMP01 vor verändernden Paketen. Toolchain-/CI-/Browserbefunde in IMP08 mit realen Ergebnissen prüfen. |
| Zustandsschema | Vorhandene Regex lehnt M06 ab; gezielte Erweiterung in IMP02 einschließlich Negativfällen, keine allgemeine V2-Freigabe. |
| Buildprofil | Astro-Konfiguration und Ausgabeisolation explizit in IMP03/07; reale Routen/Bundles für Root und Unterpfad prüfen. |
| Lernprodukte | P0/P4 flüchtig; P1/P2/P3/P5/P6 begrenztes Dossier. Grafik und tatsächlicher Code getrennt; Beleg an zugehörigen Code gebunden. |
| Fachliche Fälle | S0–S5, erste Abweichung vs. Grenzfehler, vier Prüfpunkte und Randfahrt, manuelle Zustandsbindung und Grenze von Systemzuordnungen erhalten. |
| Materialien | MAT-01–10, H1–H4, vollständige Orchestrierung, vorlesbares Briefing, Lernendentext und Printfassung geplant. |
| Zeit | Genau 22 Segmente, fünfmal45 Minuten, O35/G55/I60/F40/S35; keine übernommene 270-Minuten- oder Elfseitenpflicht. |
| PILOT | Elf TECH-Aufträge synthetisch vorbereiten; fünf USE-Aufträge, zwölf Beobachtungskriterien und reale Laufbedingungen als spätere echte Nachweise führen. |
| Freigaben | Geplante neue Architekturentscheidungen stehen zur Annahme. Produktimplementierung, reale Nutzung, Pilot, Coverage und Veröffentlichung nicht als erledigt ausgeben. |

Die Abdeckung wurde durch Codex als Autoren-/Selbstreview geprüft; kein unabhängiger Reviewer eingesetzt. Die Dateiprüfung ersetzt diesen inhaltlichen Review nicht. Künftige Umsetzungen müssen die geplanten Prüfungen tatsächlich ausführen und jeden offenen Befund dokumentieren.

## Wiederholung und historische Grenzen

```powershell
python -B roadmap/v2/implementation-planning/verify-plan.py --vault ../../Vault
python -B scripts/validate_v2_rebaseline.py
python -B scripts/validate_v2_activation.py --vault ../../Vault
npm run dashboard:update
```

Für npm gilt die geprüfte Node22-Toolchain. Der Planverifier ist absichtlich auf den Plancheckpoint begrenzt. Nach tatsächlichem Implementierungsbeginn löst IMP01 ihn als aktuelle Entwicklungsprüfung ab; seine historischen Eingabebindungen bleiben nachvollziehbar. Die alten FU-MOD-/FU-PILOT-Verifier begrenzen Änderungen ebenfalls auf ihre damaligen Aufträge und werden nicht durch großzügigere Ausnahmen umgedeutet.

Planannahme ausstehend. Nächster konkreter Umsetzungsschritt nach Annahme: IUM-V2-IMP01, vorgeschlagen GPT-6 Astra · Hoch. Kein Push oder Merge durch diesen Planauftrag.
