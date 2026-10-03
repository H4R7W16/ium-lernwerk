# Algorithmus-Lernseite – Umsetzungsplan

> Ausführung: superpowers:executing-plans, inline gemäß Nutzerauftrag nach angenommenem Review. Keine erneute Freigabeschleife; keine Subagenten gemäß Workspace-Vorgabe.

**Goal:** Alle elf Algorithmusschritte und ihre Wissens-/Materialzugänge als zusammenhängende, übersichtliche Lernumgebung überarbeiten.
**Architecture:** Bestehendes Studio weiterverwenden; Fachmodell, StateEnvelope und IDs bleiben stabil. Eigenständiger Renderer für die Klasse-5-Begleitseiten verwendet dieselben Lerninhalte. Bereichsspezifisches CSS ergänzt den Mantel.
**Tech Stack:** Node 22, CommonJS-Generator, Browser-JavaScript/CSS; keine neuen Pakete.
**Spec:** Vault/40_Projekte/IuM-Lernwerk/2026-10-03 - UI und Designreview Klasse-5-Mantel.md, Folgeauftrag zur Umsetzung für Algorithmus/Wissen/Material.

## Global Constraints
- Freie Direktzugänge aller elf Schritte; Hilfen jederzeit erreichbar.
- Lernhandlung vor Verwaltungsfläche, keine künstliche Freischaltung.
- Alle bestehenden Programme, Fachinhalte, Lösungen und getrennten Antworten erhalten.
- Keine neue Speicherung oder Bewertungssemantik; keine Veröffentlichung.
- Lokale Arbeit und Build außerhalb OneDrive.

## Task 1: Lernansicht
Files: prototypes/m06-lernstudio/studio.js, studio-learning.js; prototypes/shared/algorithmus.css.
- [x] Aufgabenspezifische Hauptaktion definieren und testen: Vorhersage/Fehlersuche einzeln, Schleifenende pro Durchlauf, sonst Abspielen.
- [x] Kompakte Lernwegzeile, direkter Auftrag, große Fachfläche, Vorhersage/Ausschreiben vor Prüfung, sichtbare Erklärung und Kriterien, sekundäre Untersuchungswerkzeuge.
- [x] Sprachkorrekturen und Rückkehr zum primären Werkzeug.

## Task 2: Wissen und Material
Files: prototypes/shared/algorithmus-pages.cjs, mantel-render.cjs; Export vorhandener Hilfsrenderer aus studio-guides.cjs.
- [x] Generatorregression RED: elf einmalige Materiallinks, elf vollständige Einzelblätter, alle Wissensanker und früher Rückkehrweg.
- [x] Wissen nach fachlichen Fragen, Material nach Unterrichtsphasen; klare Zwecke und Arbeitsformen. Einzelblätter mit Ausgangsmaterial, Auftrag, Kriterien und optionalen Lösungen.
- [x] Gemeinsamen Quellenbestand verwenden, keine duplizierten Wissensseiten als Materialübersicht.

## Task 3: Prüfung und Übergabe
- [x] Gezielte Tests/Syntax und Link-validierender Build.
- [x] Browser: 1024/390 CSS-Pixel, Start/Schleife/eigener Plan/Transfer, Wissen und Materialrückkehr mit Probeantwort; keine ausführliche Funktionsabnahme.
- [x] Getrennter eigener Diffreview; Prüfstand und Handoff aktualisieren.
- [x] fetch/pull vor Commit, Branch/Hash dokumentieren; nicht pushen.

## Review Focus
- Kein Verlust einer eigenen Erklärung beim Wechseln oder Neuaufbau der Lernseite.
- Hauptaktion nach Direktlink oder Planwechsel korrekt; Pause weiterhin erreichbar.
- Lange Aufgabentitel und Code dürfen schmal nicht überlaufen.
- Material enthält alle benötigten Startzustände und modellbezogenen Grenzen.
- Lehrblatt und Wissen bleiben auch ohne JavaScript lesbar.

## Ledger
- Basis de6781e, neuer Branch feat/algorithmus-lernseite-design, Bestand 29/29 grün.
- Entscheidung: Gemeinsame Lerninhalte wiederverwenden; Klasse-5-Begleitseiten getrennt rendern. Kosten: ein zusätzlicher fokussierter Renderer.

- Prüfung: 41/41 gezielte Tests grün; Build mit 137 Dateien und validierten lokalen Links. Browser 1024×768 und 390×844, Start/Schleife/Schleifenende/eigener Plan/Transferblatt, Wissensrückkehr mit erhaltener Probeantwort. Keine Browserfehler. Probeantwort entfernt.
- Selbstreview: Direktlinks, Modelltexte, Einzelblätter, Hauptaktionen, State-IDs und CSS-Darstellung geprüft. Keine unabhängige Prüfung oder umfassende Funktionsabnahme behauptet. Reale Schulgeräte, Papierdruck und Lernendenerprobung offen.
- Handoff: Vorschau http://127.0.0.1:8774/klasse5/lernstudio/; lokale Sicherung auf feat/algorithmus-lernseite-design, kein Push/Deployment.
