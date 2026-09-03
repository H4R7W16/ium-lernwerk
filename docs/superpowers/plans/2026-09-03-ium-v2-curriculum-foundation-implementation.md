# IuM-Lernwerk V2 Curriculum Foundation Implementation Plan

> **Execution:** Inline mit `superpowers:executing-plans`; Validator, Testdaten und reale Verträge bauen sequenziell aufeinander auf.

**Ziel:** Den geprüften V1-Curriculumbestand als unveränderte Auditbasis für V2 versiegeln, amtliche und orientierende Quellen sauber trennen und die fünf offenen V1-Abdeckungsfälle einzeln für die spätere V2-Planung entscheiden, ohne V1-Abdeckung als V2-Nachweis zu übernehmen.

**Architektur:** Neue Verträge liegen ausschließlich unter `roadmap/v2/foundations/curriculum/`. Ein generischer Fundamentstatus trennt Konzept, Datenprüfung, Inhaltsumsetzung, Fachreview, Pilot und Freigabe. Die Quellenbasis bindet Datensätze, Hashes, Recordzahlen und aktuelle amtliche Fundstellen. Die Lückenbewertung trennt historischen V1-Befund, vorgesehenen V2-Erfüllungsmodus, Zeitfolge und späteren Designbedarf. Der vorhandene V2-Validator prüft die Verträge fail-closed und gleicht sie mit den unveränderten V1-Dateien ab.

**Grenzen:** Keine Änderung unter `curriculum/`, `modules/`, `pilot/` oder an bestehenden `roadmap/*.json`/`roadmap/*.md`; keine Lerninhalte, kein LXP05-Neustart, kein Cutover, kein Push oder Merge.

## Task 1: Curriculumverträge testgetrieben abgrenzen

**Dateien:**

- Ändern: `tests/test_validate_v2_rebaseline.py`
- Ändern: `scripts/validate_v2_rebaseline.py`

- [x] Fehlende Curriculumverträge als harte Fehler testen.
- [x] Tests für exakt drei Quellen und 278 eindeutige Records ergänzen.
- [x] Tests für die Bindungsgrenze `enacted` versus `orientation` ergänzen.
- [x] Tests für exakt die fünf aktuell partiellen V1-Records ergänzen.
- [x] Tests ergänzen, dass kein V1-Befund automatisch V2-Abdeckung erzeugt.
- [x] Den BMB-Werkzeugfall auf `cross-cutting`, null Zusatzminuten und keine künstliche Zusatzaufgabe festlegen.
- [x] Tests zunächst rot ausführen.

## Task 2: Schemas und reale V2-Datensätze erstellen

**Dateien:**

- Erstellen: `schemas/v2/foundation-status.schema.json`
- Erstellen: `schemas/v2/curriculum-source-basis.schema.json`
- Erstellen: `schemas/v2/curriculum-gap-assessments.schema.json`
- Erstellen: `roadmap/v2/foundations/curriculum/status.json`
- Erstellen: `roadmap/v2/foundations/curriculum/source-basis.json`
- Erstellen: `roadmap/v2/foundations/curriculum/gap-assessments.json`

- [x] Einen statusachsenscharfen Fundamentvertrag ohne Gesamtampel anlegen.
- [x] V1-Baseline, drei Quellregister, Datei-Hashes, Counts, Crosswalk und Coverage-Audit erfassen.
- [x] Die aktuelle amtliche Direktfundstelle der Lesehilfe mit Prüfdatum erfassen und ihre Bytegleichheit per SHA-256 bestätigen.
- [x] Alle fünf Lücken mit V1-Befund, V2-Modus, Zeitstatus, Datenschutz-/Roadmapbedarf und nächstem Review erfassen.
- [x] Alle fünf V2-Abdeckungsstände auf `unassessed` belassen.

## Task 3: Reale und temporäre Verträge validieren

**Dateien:**

- Ändern: `scripts/validate_v2_rebaseline.py`
- Ändern: `tests/test_validate_v2_rebaseline.py`

- [x] Neue Dateien in die fail-closed Kontrollgrenze aufnehmen.
- [x] Repository-relative Pfade, tatsächliche Hashes, Source-IDs, Recordzahlen und eindeutige IDs prüfen.
- [x] Crosswalk- und Coverage-Zählungen gegen den unveränderten V1-Bestand prüfen.
- [x] Exakte Restlückenmenge und Bindungsgrade gegen `coverage-plan.json` prüfen.
- [x] Erfüllungsmodus und Zeitentscheidung des Werkzeugfalls unveränderlich prüfen.
- [x] Abdeckungsbehauptungen ohne neue V2-Evidenz ablehnen.
- [x] Fokussierte Tests und `npm run verify:v2` grün ausführen.

## Task 4: Reviewpaket und Workspace-Handoff

**Dateien:**

- Aktualisieren: Task, Initiative, Kanban und Roadmap im Vault
- Erstellen: Session Summary unter `Vault/50_Codex/Sessions/`

- [x] Diff gegen V1-Pfade prüfen und deren Unverändertheit bestätigen.
- [x] Python-Gesamttests und proportionale Repositoryregressionen ausführen.
- [x] Vor einem Commit `git fetch --prune` und `git pull --ff-only` ausführen.
- [ ] Lokalen Feature-Commit erstellen.
- [ ] IUM-V2-CUR auf `review` setzen und dem Nutzer die fünf Entscheidungen mit offenen Punkten vorlegen.

## Abnahmegrenze dieses Schritts

Das Curriculumfundament erreicht höchstens `review`: Datenbestand und Quellenbindung können verifiziert sein, aber V2-Inhaltsumsetzung, fachlicher Detailreview, Pilotierung und Freigabe bleiben getrennt und offen. Die nächste Grundlagenarbeit beginnt erst nach Nutzerreview dieses Pakets.
