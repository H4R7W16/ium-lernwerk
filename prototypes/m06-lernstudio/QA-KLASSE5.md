# Klasse-5-Prototyp: gezielte Prüfung am 27.09.2026

## Gegenstand

Konsolidierung des bestehenden Lernstudios nach dem Vierfassungenreview. Ziel: selbstständiges Lernen und frei auswählbare Unterrichtsbausteine für Klasse 5. Keine umfassende Testkampagne, keine Lernwirkungsmessung und keine Realgeräteabnahme.

## Automatisch geprüft

- Sechs neue Verhaltenstests: kein Aufgabenerfolg durch einen Auswahlcheck bei leerem/ungeprüftem Plan; Wandstopp; Vorhersage und Befehlsfolge; beide Transferpläne; gemeinsamer Vergleichsschritt mit unterschiedlich langen Versuchen; zwei vollständige Lösungswege mit 15 bzw. 18 Aktionen. Alle bestanden.
- Begrenzter Bestandslauf zusammen mit den neuen Tests: 16 bestanden. Der verwendete negative Namensfilter schloss entgegen der Absicht einen bestehenden Wiederherstellungstest nicht aus; dieser lief einmal mit. Keine Funktionsänderung oder weitere Prüfung dieses ausgeschlossenen Bereichs.
- Statischer Build mit Syntax- und Linkprüfung: 39 Dateien. Neue Wissen-/Lehrseiten sind enthalten und benötigen keine Skripte.
- `git diff --check` ohne Fehler nach Entfernen einer nachlaufenden Leerstelle.

## Gezielte Browserhandlungen

Tatsächlicher In-App-Browser, hauptsächlich 1024 × 768. Zusätzlich 768 × 1024 für Lehrübersicht und direkt geöffnete Station 9. In den gemessenen Ansichten keine horizontale Seitenüberbreite. Dies ist keine Safari-/iPad-Prüfung.

- Optionaler Grundbefehlsversuch: links ändert den Blick bei gleichbleibender Kachel.
- Erste Aufgabe: Endkachel und Blick gewählt, bis zum Ende untersucht; passende Rückmeldung.
- Richtige Zusatzfrage bei leerem eigenen Plan: weiterhin „Plan noch prüfen“.
- vor/links/rechts direkt hinzugefügt; Schleife eingebettet bearbeitet und übernommen. Simulation während offener Bearbeitung gesperrt, nach Übernehmen wieder bedienbar.
- Unvollständigen Plan beobachtet und anschließend durch einen vollständigen Reihenplan ersetzt: zwölf Kacheln, kein Wandstopp und Schleife anerkannt.
- Vorher/Jetzt auf gemeinsamem Handlungsschritt angesehen. Kürzerer Versuch bleibt klar als beendet markiert; eigener Regler und Schrittzahl.
- Spur eingeschaltet und visuell sichtbar; Zeitleiste bis zum Ende und rückwärts bedienbar.
- Schleifenfolge vor–links–vor–links eingegeben: passende Folge und aufgabenbezogene Rückmeldung.
- Transfer A/B: Stopp beim zweiten Aufnehmen in B, drei Werkstücke in A; „Beide Pläne untersucht“.
- Erklärung geöffnet: Modell und Steuerung bleiben daneben erreichbar, auch im geprüften Hochformat.
- Lehrübersicht: Startbilder, Programme, Erklärideen und Antworten gelesen; Station 9 direkt ohne vorangehende digitale Aufgaben geöffnet. Im frischen Tab keine Browserfehler.

## Gefundene und behobene Punkte

- Ein Quelltext-Ersetzungsschritt hatte beim Schließen des Editors aus dem Mehrfachselektor einen Einzelselektor gemacht. Dadurch brach Übernehmen ab. Ursache korrigiert, konkreten Ablauf erneut erfolgreich bedient.
- Das `hidden`-Attribut der SVG-Spur musste ausdrücklich umgeschaltet werden. Korrigiert und sichtbare Spur im Browser bestätigt.
- Die statische Lösung zu Station 9 verwies zunächst auf eine nur in den Hilfen enthaltene Ergänzung. Der vollständige Ergänzungscode steht nun auch in der Lesefassung.

## Grenzen / nächster sinnvoller Schritt

Die sprachliche und didaktische Passung ist redaktionell umgesetzt; ihre Wirkung ist noch nicht mit Fünftklässlern geprüft. Als nächster Schritt reicht eine kleine Unterrichtserprobung: Einstieg ohne Hilfe, eine Schleife erklären, eigenen Plan entwickeln; zusätzlich eine Station durch die Lehrperson erklären und direkt in die Anschlussübung wechseln. Reale Schul-iPads und vollständige Barrierefreiheit sind weiterhin offen.

Nur lokale Umsetzung und Vorschau; keine neue öffentliche Veröffentlichung in diesem Auftrag.
