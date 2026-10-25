# Lernwerk-Editor Klasse 7 Implementation Plan

> Inline ausführen entsprechend Repo-AGENTS und Lernwerk-Qualitätszyklus; keine Subagenten. Bestehende getrennte Veröffentlichungskopie, eigener Branch.

**Goal:** Größere, ruhigere und klar geführte Snap!-Ansicht für ALG-1 bis ALG-6.
**Architecture:** Zusätzlicher Einstieg lernwerk.html, lokale Modell-/Oberflächenskripte und CSS; unveränderte Snap!-Engine und originale index.html. Keine Frameworkabhängigkeit.
**Spec:** docs/superpowers/specs/2026-10-25-klasse7-lernwerk-editor-design.md

## Dateien und Grenzen

Neu unter prototypes/klasse7-programmieren/inhalt/klasse7/programmieren/snap/: lernwerk.html, lernwerk-modell.js, lernwerk-editor.js, lernwerk.css, LERNWERK.md und lernwerk-herkunft.json. Tests außerhalb inhalt/. Materiallinks werden nach erfolgreicher Integration auf die neue Ansicht geführt; Artikeltexte, alle zehn XML und sämtliche Original-Snap-Dateien bleiben geschützt. Technische Prüfung unter AI-Workspace-Local/Work/ium7-editor-20261025, kleine Nachweise später Assets/.

## Review Focus

ALG-1 hat absichtlich lose Stapel: grüne Flagge darf nicht als Start jedes Stapels versprochen werden. ALG-6 benötigt den falschen Vergleich und den Reparaturblock nicht gleichzeitig. Schrittmodus muss native Pausen verwenden. Import/Moduswechsel darf keine Arbeit still verwerfen. Download ist keine beobachtete Dateispeicherung; originaler XML-/Sichtbarkeitszustand muss erhalten bleiben.

## Aufgaben

- [ ] Verhaltensprüfungen für sichere Aufgabenwahl, notwendige Palettenblöcke, Wiederherstellung beim Export, Dateiannahme und Schrittkontrollen schreiben; rot nachweisen.
- [ ] Zusätzliches Konfigurationsmodell und klare HTML-/CSS-Bedienung implementieren. Enginezustand lesen und native Aktionen verwenden; Schutz vor Arbeitsverlust und sichtbare Bedienhilfe.
- [ ] Alle bestehenden Schutzprüfungen und neuen Tests ausführen; frische vollständige Pages-Ausgabe bauen. Herkunft eigener Dateien dokumentieren.
- [ ] Testansicht über bestehenden PR-/Pages-Weg bereitstellen; öffentliche echte Engine prüfen, noch offene Geräteprobe klar kennzeichnen. Bei Befunden nacharbeiten.
- [ ] Materiallinks/Lehrhinweise konsistent nachführen, tatsächliche Ausgaben kritisch selbst prüfen; versionsgebundener Abschluss mit vorhandenen Safari-Grenzen.
- [ ] Öffentliche Ausgabe bestätigen, Projekt-Handoff und Session Summary erstellen.
