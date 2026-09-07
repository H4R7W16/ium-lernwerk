# FU-PILOT – Prüfbericht

**7. September 2026 · Dokumenten-/Vertragsprüfung, keine reale Durchführung.** Die [maschinenlesbare Prüfung](validation.json) bindet 25 unveränderte Eingaben an MOD-Commit `9365045a2c2a50d2259d01ef172b7b292cd0ee24`. Das positive MOD-Feedback und der ausdrückliche FU-PILOT-Auftrag sind additiv dokumentiert; MOD-DESIGN ist angenommen, reale Eintrittsbedingungen bleiben offen.

## Tatsächlich geprüfter Umfang

`python -B roadmap/v2/follow-ups/pilot/verify-packet.py` prüft sieben Gruppen:

1. 25 aktuelle Checkout- und historische Git-Blob-Hashes; CRLF/LF nur für den Inhaltsvergleich zwischen den Ebenen normalisiert.
2. MOD- und TECH-Annahme mit unveränderten Folgegrenzen.
3. Exakte MOD-Zeit-/Produkt-/Curriculumsbindung: 22 Segmente, fünfmal 45 Minuten, 35/55/60/40/35; elf technische Prüfaufträge, fünf Nutzungsaufträge, zwölf Beobachtungskriterien, zwölf LXF-Gates und acht LXF03-Pilotfragen. Datenwege und reale Statusgrenzen geprüft.
4. Zwölf ausdrücklich synthetische Entscheidungsszenarien: vollständige hypothetische Bestätigung, kritischer Vorfall, fehlende Technik, falscher Build, wiederholtes Hindernis, entfallene Sicherung, Mehrzeit, Papier statt eigenem Code, fehlende Bestätigung, ungeklärter Schuleinsatz, Vorfall plus fehlende Belege und nicht interpretierbare Beobachtung.
5. Sechs bewusst fehlerhafte Änderungen nur im Arbeitsspeicher abgewiesen: Zeitdrift, fehlendes Gate, erfundener Realnachweis, vorgezogene Nutzungserlaubnis, gespeicherte Gesprächsantworten und Text statt Booleschem Wert.
6. Lokale Markdown-Verweise und Zeichensatz geprüft; aktuelle Anzahl in `validation.json`.
7. Repo-Schreibumfang auf neues FU-PILOT-Paket und additive MOD-Annahme begrenzt; Produktions-, CI-, Alt-Pilot- und versiegelte Baseline-Dateien unverändert.

**Sieben Prüfgruppen bestanden**, zwölf Szenarien und sechs Negativfälle bestätigt. Die nach dem Selbstreview abschließend geprüfte Fassung ist in `validation.json` gebunden. Der Prüfer validiert ausgewählte Vertragsinvarianten, keine vollständige JSON-Schema-Sicherheit für beliebige Eingaben. Er nimmt keine externen Evidenzdateien an und ist keine Erhebungssoftware.

Zusätzlich bestanden: `python -B scripts/validate_v2_rebaseline.py`, `python -B scripts/validate_v2_activation.py --vault '../../Vault'` und `npm run dashboard:update` mit Node 22.23.2 / npm 10.9.8. Das erzeugte Cockpit zeigt MOD angenommen und PILOT zur Instrumentenabnahme. Nach dem Commit wird die Ansicht nochmals mit dem sauberen Git-Stand erzeugt; der genaue Handoff liegt in der FU-PILOT-Session im Vault. Keine vollständige Produkt-/Browserregression für diese reine Spezifikationsänderung; bestehende FU-TECH-Lücken gelten fort.

## KI-Dokumentenselbstreview

Autorreview auf Fachlichkeit, Scope, Zeit, Datenfluss, Begriffe und Gegenbeispiele. Im Review präzisiert: Die technische Datenprüfung muss tatsächliche Dossier-/Exportinhalte auf P0/P4 und Telemetrie kontrollieren; bloße unsichtbare UI genügt nicht. Die Auswahl zweier Unterrichtskontexte und Rollenüberschneidungen sind ausdrücklich begrenzt. Die acht LXF03-Fragen wurden für Klasse 5 operationalisiert, nicht als beantwortet oder auf 6/7 übertragbar markiert.

Schwellen von zwei Sichtungen, zwei wiederkehrenden Hindernissen und fünf Minuten Abweichung sind begründete Projektregeln; keine empirischen Normen. Unterrichtsminuten und Erwachsenenzeit sind getrennt. Eine Beobachtungsperson kann nicht alle Prozesse garantiert erfassen; fehlende Sichtung ergibt U, keine geschätzte Erfüllung. Kein Klassenlernerfolg aus zwei guten Beiträgen. Optionales Rückmeldegespräch wird nicht als Datensatz gespeichert oder mit Lernwirkung verrechnet.

Datenfristen besitzen feste Endereignisse und Maximalgrenzen auch bei vertagter Entscheidung/Abbruch. Sie sind noch institutionell zu bestätigen. Reale Verantwortliche, Speicherorte und Termine bleiben als erforderliche Eingaben leer; das sind Eintrittsbedingungen, keine fehlenden Teile des Spezifikationsauftrags. Kein juristischer Freigabevermerk und kein behaupteter realer Löschtest.

## Offene Nachweise

V2-Modul/Editor/Materialien nicht implementiert; fünfteiliger S3-Körper und zielabhängiger Prüfer noch nicht ausgeführt. Acht TECH-Befunde offen. Echte Zielgeräte, Netz/LMS/Assistenz, Lernendennutzung, Unterrichtszeiten, eigene digitale Produkte, menschliche Fachprüfung, institutionelle Entscheidungen und Rechte konkreter Materialien nicht geprüft. `pilot: not-started`, `coverage: unassessed`, `publication: closed`.

Dieses Ergebnis wird zur eigenen FU-PILOT-Abnahme übergeben. Eine Annahme bestätigt das Instrumentendesign; sie startet weder eine Umsetzung noch einen realen Pilot. Kein unabhängiger Review, keine Wirkungsaussage.
