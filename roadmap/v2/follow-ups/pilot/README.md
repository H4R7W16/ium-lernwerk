# FU-PILOT – Prüf- und Pilotinstrumente für R5-M06

**7. September 2026 · Instrumentenpaket zur Nutzerabnahme (`review`). Reale Prüfung und Pilot: nicht begonnen.**

Das Paket bindet technische Prüfung, Bedienbarkeit, Unterrichtsbeobachtung und Auswertung an **V2-G5-M06 „Präzise Abläufe entwickeln und prüfen“**. Maßgeblich sind das [angenommene Moduldesign](../../../../docs/superpowers/specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md), seine [additive Annahme](../reference-module/acceptance.json) und der [angenommene technische Audit](../technical/README.md). Die historischen Reviewstatus im unveränderten MOD-Snapshot sind keine erneut offenen Designentscheidungen.

## Review und Anwendung

| Datei | Zweck |
| --- | --- |
| [Prüfvertrag](design.md) | Gegenstand, Prüfpfade, Schwellen und zulässige Entscheidungen |
| [Technischer Leitfaden](technical-runbook.md) | Reproduzierbare Schritte für S0–S5, Datenhaltung, Recovery, Updates und reale Zugänge |
| [Beobachtungsinstrumente](observation-kit.md) | Leere Kontext-, Nutzungs- und Unterrichtsbögen; produktbezogene Kriterien und Diagnose-Fallback |
| [Daten- und Löschvertrag](data-and-rights.md) | Getrennte Datenwege, zuständige Rollen, Fristen und Löschkontrolle |
| [Auswertungsleitfaden](review-guide.md) | Getrennte Befundachsen, Widersprüche, Abbruch und menschlicher Entscheidungsbogen |
| [Strukturierter Vertrag](protocol.json) | Exakte Zeit-/Produktbindung, Gate- und Befundzuordnung, aktuelle Nichtdurchführung |
| [Synthetische Entscheidungsszenarien](decision-scenarios.synthetic.json) | Konstruierte Gegenbeispiele; keine Unterrichtsdaten |
| [Eingabebindung](input-bindings.json) | Geprüfte Eingaben und bytegenaue Hashes an MOD-Commit `9365045` |
| [Prüfbericht](validation-report.md) | Tatsächlich ausgeführte Dokumentenprüfung und offene Nachweise |
| [Arbeitsplan](work-plan.md) | Beauftragter Umfang und Erledigungsstand |

Die Formulare sind lesbare Markdown-Vorlagen, keine Erhebungsanwendung. Erst nach institutionell geklärtem Einsatz dürfen **Kopien außerhalb von Repo, OneDrive-Workspace und Vault** ausgefüllt werden. Im Projekt liegen ausschließlich leere Instrumente, Designparameter und ausdrücklich synthetische Beispiele. Die Lernendenmaterialien MAT-01–10 sind weiterhin nur spezifiziert.

## Übernahme aus IUM11, IUM19 und IUM20

| Historischer Eingang | Neue Entscheidung |
| --- | --- |
| `pilot/pilot-protocol.json`, `pilot/docs/publication-contract.json` (IUM11) | Evidenz, Entscheidung und Veröffentlichung getrennt halten. Working-40, Jahrescluster, Mindestzahl zehn und Drittelschwelle nicht übernehmen. Kein Jahresverfügbarkeitsnachweis durch M06. |
| `scripts/validate_ium11.py` (IUM11) | Referenz für abweisende Validierung; sein Zeitmodell/Fingerprint und seine Ergebnislogik gelten nicht für V2. |
| Gate-B-Design und Implementierungsplan vom 03.08.2026 (IUM19) | Technik → Exploration → Überarbeitung → Bestätigung als gestufte Prüfung nutzen. Neue Bindung an M06/P0–P6; beide vollständigen Unterrichtsläufe prüfen denselben 225-Minuten-Entwurf. Kein obligatorischer 270-Minuten-Lauf. |
| `pilot/ium5-gate-b/protocol.json` (IUM20) | Typisierte Nachweise und Abbruch erhalten; alte Modul-ID, starre Gerätematrix, neun alte Beobachtungskriterien und automatische positive Gesamtempfehlung ersetzen. |
| `pilot/ium5-gate-b/schemas/technical-evidence.schema.json`, `pilot-evidence.schema.json`, `scripts/validate_ium5_gate_b.py` (IUM20) | Nur Referenz: alte Schemaannahmen passen nicht zu neuer Produkt-/Zeit-/Datenbindung. Keine reale V2-Eingabe in diese Validatoren. Eine spätere Erhebungssoftware braucht einen eigenen Umsetzungsauftrag. |

Kein historisches Artefakt wird umgeschrieben oder als erledigter V2-Nachweis umetikettiert. Die zwölf LXF-Gates und acht TECH-Befunde werden im neuen Vertrag einzeln zu Prüfungen zugeordnet. Paketannahme erfüllt den Spezifikationsteil von MOD-PILOT; **MOD-PILOT als reales Eintrittsgate bleibt offen**.
