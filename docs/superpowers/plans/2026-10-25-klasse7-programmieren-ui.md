# Klasse 7 · Gestaltungsüberarbeitung – Implementation Plan

> Agenten: inline ausführen, entsprechend dem Lernwerk-Qualitätszyklus ohne Subagenten. Die bereits beauftragte gemeinsame Lernwerk-UI wird auf den vorhandenen Programmierbogen angewandt.

## Ziel und Grundlage

Jans Auftrag vom 25.10.: Die funktionierende Testfassung ansprechender gestalten. Bestehende 36-UE-Planung, Aufgaben, Zeiten, Projektdateien und Snap!-Laufzeit bleiben erhalten. Gestaltungsgrundlage: UI-Standard Fassung 1.2 vom 03.10. mit dokumentiertem Umsetzungsauftrag; keine neue Plattform oder neue didaktische Konzeption.

Richtung: heller warmer Hintergrund, Waldgrün, weiße Leseflächen, Systemschrift, großzügige Gliederung. Die Übersicht zeigt einen zusammenhängenden Lernweg und eine eigene, rein illustrative SVG-Ablaufgrafik ohne Lösungen. Lernseiten erhalten eine seitliche Aufgabennavigation, erkennbare aktuelle Aufgabe, Inhaltsanker, klare Editor-/Dateiaktionen und Vor-/Zurückwege. Lehrpersonenmaterial bleibt separat erreichbar. Kernaufträge und Warnungen bleiben sichtbar; kein Fortschritt wird vorgetäuscht.

Alternativen: reine Farbkorrektur würde die fehlende Orientierung kaum verbessern; eine Umgestaltung der Snap!-Oberfläche wäre ein eigener technischer Eingriff. Anwendung des vorhandenen Lernwerk-Rahmens ist die passende begrenzte Umsetzung. Detailentscheidungen zu SVG und Raster stammen von Codex; sie werden nicht als neue Nutzerfreigabe ausgegeben.

## Architektur und Dateien

Statische HTML-/CSS-Quellen unter prototypes/klasse7-programmieren/inhalt/. Kein neuer Laufzeitcode, kein Speicher, keine externen Schriften. HTML-Transformation lokal mit vorhandenem parse5, keine neue Projektabhängigkeit. Renderer-/Prüfarbeitsdateien unter AI-Workspace-Local/Work/ium7-ui-20261025. Ausgabeverzeichnis und Vorschau außerhalb OneDrive. Die lokale Vorschau dient ausschließlich der Gestaltung, keiner Umgehung der früher blockierten lokalen Snap!-Offlineprobe; Snap! wird dort nicht ausgeführt.

## Prüfschwerpunkte

- Kein verlorener Auftrag, Zahlwert, Code oder Tabelleninhalt; Text-/Code-Fingerprints vor Umbau erfassen.
- Alle Snap!-/XML-/Bilddateien bytegleich; bestehende 1066 Pages-Dateien bleiben geschützt.
- Aktuelle Aufgabe und echte Navigationsziele mit Tastatur und in schmalen Ansichten verständlich.
- Keine übergroßen Statushinweise vor der Lernhandlung; Erprobungsstatus trotzdem sichtbar.
- Lange Überschriften, Code und Tabellen passen auf Desktop und in die tatsächliche schmale Vorschau; Safari bleibt eigene Geräteprobe.

## Schritte

- [x] Baseline erfassen und gezielte Tests schreiben; neuen Navigationsvertrag zunächst rot nachweisen.
- [x] Übersicht, Leseseiten und Lehrpersonenrahmen im vorhandenen Stil überarbeiten; Aufgabenblöcke unverändert erhalten.
- [x] Tests, Build und tatsächliche Desktop-/schmale HTML-Ansichten prüfen; bei Befunden nacharbeiten.
- [x] Versionsgebundenen Selbstreview mit verbliebenen Safari-Grenzen dokumentieren.
- [ ] Geprüften Stand über den vorhandenen PR-/Pages-Weg veröffentlichen und öffentliche Ausgabe kontrollieren.
- [ ] Handoff, Projektstatus und Session Summary aktualisieren.
Vor dem Quellcommit: 121 Pages-Tests bestanden; nach den letzten CSS-Korrekturen alle 13 Klasse-7-Tests und frischer Build (1138 Dateien) bestanden. Eng begrenzter Gestaltungs-Selbstreview READY_FOR_REVIEW, Fassung f51ed4eaf6f74073ea6fdb85eebfca5e38e2ae5f8612912322348287bbe7049c. Öffentlicher Integrations-/Deploymentabschluss und Session-Handoff werden nach diesem Quellcommit im Workspace dokumentiert.
