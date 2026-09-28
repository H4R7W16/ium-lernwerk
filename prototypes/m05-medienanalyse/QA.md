# Überarbeitung nach Lernwerkreview · 28.09.2026

## Gezielte Prüfung
- Zwei neue Logiktests zunächst rot, anschließend grün: Widerspruch versus fehlende Information; Transfer mit passender, widerlegter und offener Aussage.
- Bestehenden Materialtest an die eindeutige Bibliotheksüberschrift angepasst. Zusätzlich geprüft: Jeder der fünf Einzelbausteine enthält sein eigenes Bild, Situationskarte und Auftrag ohne JavaScript oder Verweis auf vorherige/nächste Seiten.
- Insgesamt 15 gezielte Modell-/Pages-Prüfungen bestanden. Keine umfassende Test-Suite.
- Pages-Build mit Syntax- und interner Linkprüfung: 54 öffentliche Dateien.
- Browser: Erklärung beim aufgedeckten Gesamtbild, kontrollierter Bild-/Textvergleich, verschiedene Rückmeldungen bei Widerspruch und fehlendem Wissen, A/B-Begründungsvergleich, eigener Beitrag mit Änderung und erneuter Kriterienprüfung, drei Transferurteile.
- Die Rückmeldung bewertet nur die geschlossenen Aufgaben; offene Beiträge werden ausdrücklich nicht automatisch beurteilt.
- Eigenständiger Gestaltungsbaustein mit Bild und Karte visuell bestätigt. Einstieg der Einzelmaterialien anschließend gestrafft.
- Desktop und gezielte Arbeitsflächenprüfung bei 1024 × 768: kein horizontaler Seitenüberlauf; aktive Überschrifteneingabe aktualisiert die Vorschau. Keine JavaScript-Fehler im erfassten Protokoll. Kein vollständiger Geräte-/Accessibility-Test.

## Didaktische Nacharbeit
F1: sichtbarer Arbeitsweg und Ergebnis, präzisierter Einstiegssatz nach Erklärung.
F2: schwache/starke Begründung vergleichen; Beleg–Wissensgrenze–Verbesserung modellieren; eigene Entscheidung ändern/beibehalten mit Grund.
F3: vier Kategorien statt Sammelkategorie; fachlich passende Rückmeldungsüberschriften.
F4: präzise Bibliotheksbehauptung, zulässiger enger Ausschnitt und Aussage zu täglichen Besuchszahlen ohne ausreichende Information.
F5: fünf einzeln aufrufbare Unterrichtsmaterialien; auch Wissensabschnitte mit eigenen Bildern/Karten; Hinweise für Übernahme und Wiedereinstieg.
F6: zwei getrennte Vergleichssätze, eine explizite Zuordnungsbegründung, weitere Impulse mündlich; keine doppelte Bearbeitungspflicht.
F7: konkrete Sprache, Begriffshilfen und Ausschnittbeschreibungen ohne vorweggenommene Auflösung.
Freie Navigation und die fünf Hauptschritte bleiben erhalten.

## Aussagegrenzen
Didaktisch überarbeitet und im genannten Umfang geprüft. Keine gemessene Lernwirkung, keine reale Klasse-5-/Schul-iPad-Erprobung, kein vollständiger Screenreader- oder physischer Drucktest. Gesamtbilder für den Ausdruck sind als eigene Druckansicht enthalten. Ausschluss von Speichern/Import/Export bleibt bestehen.

## Vorgehen bei Veröffentlichung
Wie im bestehenden Prototypstrang: begrenzter Prüfumfang, keine automatisch ausgelöste Gesamtsuite. Veröffentlichung über den vorhandenen Workflow mit check_scope=medienanalyse. Repository und Vault-Handoff dokumentieren Commit, PR und Veröffentlichungsnachweis.

---

# Historischer Nachweis vor dem Lernwerkreview

# Begrenzte Prüfung · 28.09.2026

Auftrag: keine umfassenden Tests. Geprüft wurde nur der neue Prototyp samt öffentlicher Dateizuordnung; keine Gesamtsuite und keine Prüfung der ausgeschlossenen Funktionsbereiche.

## Automatisierte Nachweise
- Vier neue Modelltests zuerst rot wegen fehlender Funktionen, dann grün: begrenzte Ausschnitte, Vergleich mit nur einer veränderten Eigenschaft, offene/passende/unpassende Belegzuordnung, Ausgabe von HTML-Zeichen als Text.
- Zwei neue Buildverträge zuerst rot wegen fehlender Medienanalyse-Dateien, dann grün: vollständige öffentliche Dateien einschließlich unveränderter Bilder; Material ohne JavaScript mit getrennten Lehrlösungen.
- Mit den sechs bestehenden Prüfungen des Pages-Dateivertrags: insgesamt zwölf gezielte Tests bestanden.
- Statischer Build: 49 öffentliche Dateien; Syntaxprüfung der ausgelieferten JavaScript-Dateien und Prüfung statischer interner Links. Keine zusätzlichen Laufzeitabhängigkeiten.

## Begrenzter Browserdurchgang
- Einstieg: beide Ausschnitte sichtbar, eigene Beobachtung eingegeben; bei späterer Rückkehr innerhalb der laufenden Seite weiterhin vorhanden.
- Untersuchung: Ausschnitt „Mitmachstände“ verändert das Bild bei gleicher Überschrift. Umschalten auf Überschriftenvergleich setzt beide Bilder gleich; Auswahl einer anderen Überschrift aktualisiert nur diese.
- Belege: vier Zuordnungen mit konkreten materialbezogenen Rückmeldungen.
- Editor: eigene Überschrift, Bildunterschrift und Begründung eingegeben; Bildausschnitt geändert, direkte Vorschau, Selbstprüfung geöffnet.
- Überarbeitung nach angehaktem Kriterium: Hinweis zur erneuten Prüfung erscheint; Kriterien werden zurückgesetzt.
- Transfer: Bibliotheksausschnitt, vollständiges Bild und Situationskarte aufrufbar.
- Materialbogen und Lehrbriefing unabhängig erreichbar und inhaltlich im Browser geprüft. Keine Scripts in den statischen Seiten.
- Ansichten: 1024 × 768 (Einstieg/Vergleich), 768 × 1024 (Editor) und 390 × 844 (Einstieg). Kein horizontaler Seitenüberlauf in den geprüften Ansichten. Keine doppelten IDs im Editor.
- Keine JavaScript-Fehler im erfassten Browserprotokoll.
- Tastatur-Sprunglink erhält den aktuell geöffneten Lernschritt.

## Befunde und Korrekturen
- Beim eigenen Gegenlesen doppelte IDs zwischen Eingabe und Vorschau beseitigt.
- Der Sprunglink #main löste ursprünglich die allgemeine Hash-Navigation aus. Die Ursache wurde getrennt behandelt; Browsernachprüfung auf dem Transfer bestätigt, dass der Schritt erhalten bleibt.
- Tablet-Einstieg gestrafft und Überschriften vor den Bildern angeordnet, damit die zu untersuchenden Aussagen früh sichtbar sind.
- Ein fehlerhaft quotiertes temporäres Integrationsskript stoppte vor jeder Mutation; korrigiert, anschließend alle geplanten Prüfungen grün. Kein Produktfehler.

## Fachlicher Gegencheck
- Sichtbares, zusätzliche Situationsangaben und weiterreichende Behauptungen sind getrennt.
- Positiv wertende Überschrift wird nicht automatisch als wahr behandelt.
- Vollständiges Bild bleibt eine begrenzte Darstellung; keine vollständige Ereigniskenntnis behauptet.
- Mehrere sinnvolle Gestaltungen möglich. Ausschnitt nicht pauschal als Täuschung eingeordnet.
- Eigene Antwort/Produkt/Begründung erforderlich; Muster erst auf Wunsch sichtbar.
- Lehrweg ohne vorherigen digitalen Pflichtdurchlauf; analoges Gestalten wird nicht als Nachweis digitaler Werkzeugbedienung ausgegeben.

## Nicht nachgewiesen
Keine gemessene Lernwirkung, keine tatsächliche Klasse-5-Erprobung, kein realer iPad-/Screenreader-Test und keine vollständige Barrierefreiheitsprüfung. Druck-CSS vorhanden, kein physischer Drucktest. Reale Bildquellenkritik würde weitere Herkunftsprüfung benötigen; die bewusst erfundenen Materialien bilden diesen Teil nicht ab.
