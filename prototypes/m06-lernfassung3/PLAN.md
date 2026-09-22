# Lernfassung 3 – interaktive Planungssequenz
Stand: 22.09.2026. Auftrag und Entwurf sind durch „führe das jetzt aus“ freigegeben.
Basis: origin/main f8aabde, isolierter bestehender Worktree, neuer Branch feat/m06-lernfassung3.

## Ziel und Grenzen
Dritte auswählbare Fassung unter /lernfassung-3/. Die vollständigen Inhalte der Selbstlernstrecke bleiben verfügbar. Nur der Planungsabschnitt bekommt vier verbundene Etappen. Alte Fassungen behalten ihre Inhalte; Navigation erhält einen dritten Link. Keine Gesamtsuite, keine Import-/Exporttests, keine Lernwirksamkeitsbehauptung.

## Schritte
1. Neue Planungslogik zuerst mit gezielten Tests: 4×2-Lücken, Wandstopp, unvollständige Fläche, linker Wechsel mit vorhandenem Besuchsstand und korrekter Zielrichtung.
2. Vorhandene Inhalte in vier frei wählbare Etappen gliedern. Zahlen/Drehungen unmittelbar ausführbar machen, Rückmeldungen an Fahrt koppeln, bei Änderung alte Rückmeldung entfernen. Freier 4×3-Plan bleibt kriterial bewertet; alternative gültige Wege zulassen.
3. Dritte Fassung, eigene Browsersicherung und Lesefassung anbinden. Inhalte/Simulationskern gemeinsam verwenden. Zwei kleine optionale Hooks im bestehenden Renderer/App statt Kopien der gesamten Strecke.
4. Gezielt Modell, Material und Pages-Dateikarte prüfen; Browser: Fehler/Korrektur, Etappen, Wissen-Rückkehr, Alternativplan, Tastatur, schmaler Bildschirm und Lesefassung.
5. Frisches Branch-Review, nötige Korrekturen, GitHub/Pages bereitstellen und Workspace-Handoff aktualisieren.

## Schnittstellen und Entscheidungen
- Gemeinsamer Renderer erhält optionale Seitenliste; Standardausgabe bleibt bis auf Versionsnavigation gleich.
- Neue UI erhält renderSim über optionalen Mount-Hook. Der Basiskern bleibt unverändert.
- Neue Etappeneingaben bleiben wie freie Antwortfelder im offenen Tab. Eigener Raumplan nutzt bestehende Sicherungsfunktion mit eigenem Browser-Schlüssel. Kein Umbau des Dateiformats.
- Lesen/Drucken zeigt alle Etappen und vollständigen Hilfen/Lösungen.
- Reviewfokus: versteckte Sprungziele, alte Erfolgsrückmeldung nach Änderung, Startzustand linker Wechsel, falsche Zielrichtung, Versionstrennung und veröffentlichte Pfade.

## Fortschritt
- Ausgangslage: sauber, fetch/pull erfolgreich, 49/49 gezielte Basistests bestanden.
- Schritte 1–3 umgesetzt: sieben neue Fachprüfungen erst rot, dann grün; Pages-Verfügbarkeit ebenfalls erst rot, dann grün. Insgesamt 57/57 gezielte Tests.
- Schritt 4 lokal geprüft: Beispiel, 4×2-Wandstopp/Korrektur, falsche Reihe/falscher Blick/Korrektur beim linken Wechsel, neun erreichte Kacheln nach richtigem Wechsel, alternativer spaltenweiser 4×3-Plan, Wissen-Rückkehr, verstecktes Sprungziel, Tastatur, 320/1280 Pixel, vollständige Lesefassung, Versionswechsel, getrennte Browsersicherung. Keine Browserfehler.
- Schritt 5: unabhängiger Review ohne P1/P2-Befund; zusätzliche Leerzeile bereinigt. Veröffentlichung und öffentlicher Nachweis folgen.
- Ruling: bestehendes isoliertes Arbeitsverzeichnis wiederverwenden, neuer Branch von origin/main; kein zweiter Worktree nötig. Nutzerausführung umfasst die dritte auswählbare Fassung im bestehenden Pages-Angebot.
