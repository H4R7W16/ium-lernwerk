# IUM-V2-DASH – Validierungsbericht

Stichtag: 6. September 2026. Prüfer: Codex, KI-gestützter Implementierungs- und Dokumentenselbstreview. Keine unabhängige externe Prüfung oder Nutzerabnahme des Dashboards behauptet. R7 wurde ausdrücklich vom Nutzer freigegeben; sein akzeptierter Stand ist `60c7d0a195bc6f3e6803bdc2a97e4a7479e28a24`.

## Ergebnis und Prüfumfang

Die neu aufgebaute Astro-Ansicht und das generierte Obsidian-Cockpit verwenden denselben validierten Snapshot. Acht Hauptansichten zeigen 18 Re-Baseline-Gates, fünf Stränge mit acht Reifeachsen und acht Experience-Unterachsen. Präsentation und interne Arbeitsansicht werden in getrennte Verzeichnisse gebaut. Pflichtbelege sind lokal auflösbar; nicht gepushte Commits erhalten keine erfundenen GitHub-Links.

25 Node-Vertrags-/Integrationstests prüfen unter anderem falsche Statuswerte, doppelte IDs, fehlende Pflichtstränge und Reifeachsen, Sichtbarkeit, lokale Pfade, fehlende Pflichtbelege, offene Vorgängergates, reale Quellprojektion, vollständige Git-SHAs, Commitfrische und unveränderte atomare Ausgabe bei ungültigen Daten.

Sechs Chromium-Prüfungen umfassen achtseitige Navigation und lokale Links, automatische WCAG-2.2-AA-Prüfung aller Hauptansichten, Tastatur/Skip-Link, 390-/768-Pixel-Ansichten ohne Seitenüberlauf, Druck mit allen Gates/Reifeachsen sowie Prüfung sämtlicher Präsentationsdateien auf interne Belege, absolute lokale Pfade und aktive externe Ressourcen. Es entstehen keine externen Hintergrundanfragen. Sichtprüfung ergänzt die automatisierten Prüfungen für Desktop, responsive Ansicht und gerenderte Druckseiten. Automatisierte Accessibility-Prüfungen ersetzen keine spätere manuelle Assistenztechnik- oder Realgeräteprüfung.

Die 966 bestehenden Python-Regressionstests und das V2-Gate bestanden. Der vollständige Python-Lauf benötigte 130,961 Sekunden. 132 Plattformtests und die Workspace-Grenzprüfung bestanden ebenfalls. 25 Dashboardtests und sechs Browserprüfungen wurden zusätzlich unter Node 22.23.2 / npm 10.9.8 erfolgreich ausgeführt; damit ist die deklarierte Runtime-Linie geprüft. Die genaue abschließende Runtime- und Git-Zuordnung wird im zugehörigen Session-Handoff dokumentiert; dieser Bericht behauptet keinen selbstreferenziellen eigenen Commit.

## Geschlossene Befunde

- Eine zu breite lokale Pfadprüfung erkannte fälschlich das Ende von HTTPS als Laufwerkspräfix. Eine explizite Wortgrenze und ein realer URL-Regressionstest schließen den Fehler.
- Die installierte Astro-Version erwartet einen String für das Ausgabeverzeichnis; die Buildkonfiguration wurde entsprechend korrigiert.
- Teiltransparente Navigationsnummern führten zu einem Kontrastbefund. Die Darstellung wurde ohne Transparenz umgesetzt; erneuter Accessibility-Lauf bestanden.
- Der Tastaturtest verwendete zunächst eine dekorative, für Assistenztechnik verborgene Nummer im Linknamen. Er adressiert jetzt den tatsächlichen Navigationslink.
- Die Druckansicht verwendet eine eigene transponierte Reifetabelle, enthält den vollständigen Checkout-Commit am Seitenanfang und unterdrückt die alleinstehende Fußzeilen-Seite.
- Der Browser-Test-Runner verwaltet seinen lokalen Vorschauprozess direkt und beendet ihn nach dem Lauf; keine Wiederverwendung eines unbekannten bereits laufenden Servers.

## Bewusst offene Grenzen

Der frühere Dashboard-Commit bleibt eine historische Quellenlücke. Zwei optionale historische Task-Belege (IUM14 und LXP05) fehlen; die Präsentation fasst diese Lücken ohne interne Quelldetails zusammen. Das Dashboard enthält historische, unveränderte Quelltexte: spätere Abnahmen stehen in der aktuellen Gatefolge und in Acceptance-Belegen. Ein abgeschlossener Planungsreview ist kein beobachteter Lernnachweis.

Für R7 bleiben die reale Kapazität und Eingangslage ungeprüft. 36/40/43 UE sind Bedarf; acht/drei/keine zusätzlichen Orientierungsziele sind je Pfad zeitbedingt offen. Drei neue Reflexionsnachweise bleiben in jedem Pfad offen, zusätzlich zu sechs Vorgängerfragen. Es werden weder vollständige Curriculumabdeckung noch reale Lernwirkung, Nutzungsprüfung, Pilotierung oder Einsatzfreigabe behauptet.

V1 bleibt aktiv. V2 ist im Aufbau, LXP05 eingefroren und ungemergt. Inhaltsproduktion, Veröffentlichung und Cutover wurden nicht geöffnet. DASH wird als überprüfbares Paket zur Nutzerabnahme übergeben.
