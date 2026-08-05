# Lokale Datenhaltung und Resilienz

## Zustandsweg

IUM5 schreibt ausschließlich über `@ium/local-state` in die lokale IndexedDB-Datenbank. Komponenten speichern nicht selbst. Der Browsercontroller projiziert vor jedem Speichern durch den geschlossenen Payloadparser; Export und Import verwenden denselben validierten Modulzustand. Es gibt kein Konto, Backend, Analyticsziel oder automatische Übertragung.

Der aktuelle IUM5-Vertrag ist `stateSchemaVersion 2`. Ein valider älterer Stand durchläuft am Runtime-Adapter die einzige zulässige Migration `stateSchemaVersion 1 → 2`; dabei wird das neue Feld deterministisch als `evidenceCard: null` ergänzt. Unbekannte zukünftige Schemaversionen und zusätzliche Felder werden nicht still angepasst.

Die Belegkarte persistiert genau sechs Werte: Quellenreferenz, Belegreferenz, Deutung, Überarbeitung, Kernaussage und Modellgrenze. Freier Wiedereinstiegsabruf, Rollenwechsel, gemeinsame Halteentscheidung, Hilfenutzung, Klicks, Zeiten, Versuche, Scores und Identitäten werden nicht gespeichert.

## Lernrückmeldung und technische Resilienz

Fachliche Rückmeldung benennt Ergebnis, sichtbaren Beleg, Kriterium, Deutungsfrage und nächsten Prüfschritt. Technische Resilienz benennt dagegen Speicher-, Offline-, Validierungs- oder Importzustand samt Erhaltungs- und Rückfallweg. Technische Statusregionen geben keine Lernantwort und kein Leistungsurteil aus.

## Wiederherstellung

- Offline: der installierte Kernpfad arbeitet mit demselben lokalen Zustand weiter.
- Speicherfehler: Eingaben bleiben sichtbar; Wiederholen, Export und bestätigtes Zurücksetzen bleiben explizit.
- Ungültiger Import: der aktive Stand bleibt unverändert.
- Löschen: betrifft nach Bestätigung nur den gewählten Modulstand.

## Nicht-Generalisierungen

IUM5-Raster, Editor, Befehlskatalog, Laufspursemantik, Szenario-IDs, fachliche Sprache und Checkpoint-Platzierung bleiben außerhalb der generischen Persistenzschicht. Die lokale Belegkarte ist kein Portfolio, keine Versuchschronik und kein Diagnoseprofil.
