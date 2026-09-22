# Gezielte Qualitätssicherung · 23.09.2026

## Funktion und Fachlichkeit
- Neun neue Modelltests: ganzer Schleifenkörper und Folgeanweisung; 8 bereits gereinigte Kacheln beim Übergang; Reihen-/Spaltenlösung; Stationsbelegung; zwei offene innere Kacheln; neuer Abrufstart; Reparaturkriterium; vollständiger Musterweg; feste Beobachtungsfälle.
- Gezielter Regressionstest zur Reparatur zuerst rot: bloße Drehschleife plus ausgeschriebene Runde wurde fälschlich akzeptiert. Nach engerem Kriterium grün; alternative passende Gruppierung weiter gültig.
- Bisherige Material-/Journey-/Pages-Checks mit neuer Veröffentlichungsroute separat erhalten.

## Browsernachweise
- Chromium im Codex-Browser, explizite CSS-Viewports 1024×768, 768×1024, 390×844. Keine echte iPad-Hardware oder Safari-Emulation behauptet.
- Vorhersage auf (2,1), Blick oben für vor → links → vor; korrekt verglichen.
- Ein Schleifenkörper endet nach zwei Aktionen. Aktives links und Durchlauf 1/4 synchron sichtbar.
- Zwei Schleifenzahlen von 2 auf 3 geändert: acht Kacheln sauber, Auftrag erfüllt.
- Falscher linker Übergang liefert Ziel-/Blickrückmeldung; Änderung setzt den Raum auf acht vorausgehend saubere Kacheln zurück.
- Eigener Plan ausschließlich mit Touch-Bausteinen erstellt: drei Schleifen und beide Übergänge, zwölf Kacheln, 15 Aktionen.
- Letzte Schleifenzahl 3→2: elf Kacheln/14 Aktionen; Versuchsvergleich zeigt vorherigen und aktuellen Code samt richtigem Endstand.
- Randrunde endet am Start, meldet aber (2,2) und (3,2) offen. Letzte aktive Anweisung sichtbar, inneres Programm-scrollTop 281.
- Prüfstation A: nach dritter Aktion frei und ein Werkstück fertig; B: Stopp beim zweiten Aufnehmen. Code-Markierung und Live-Rückmeldung passen.
- Abruf: Folge vor/links dreimal plus rechts korrekt erkannt, Ende (2,1), Blick oben.
- Abspielen erreicht 8/8; Pause stoppt, Schaltfläche kehrt zu Abspielen zurück.
- Undo nach erstem Baustein ist aktiv und stellt leeren Plan wieder her.
- Tastatur-Enter auf Schleifenzahl hält Fokus am Plus; Escape kehrt zum bearbeiteten Baustein zurück.
- Keine Browser-Konsolenfehler in den geprüften Abläufen. Keine horizontale Seitenüberbreite in den geprüften Tablet-/schmalen Formaten.

## Unabhängiger Review
Vier gemeldete Ursachen behoben und nachgeprüft: Reparaturkriterium, falsches Koordinatensystem beim Scrollen zur aktiven Zeile, fehlende hörbare Stationszustände, Undo mit leerem Vorgänger. Nachprüfung der Ergänzungen Musterweg und Versuchsvergleich ohne weiteren relevanten Befund.

## Grenzen
Kein Import-/Exporttest, keine Gesamtsuite. Keine echte VoiceOver- oder Safari-Hardwareprüfung. Datenpersistenz ist kein Prüfungsschwerpunkt dieses Auftrags. Motivation, Lernzeit und Lerngewinn sind erst mit Lernenden beurteilbar.
