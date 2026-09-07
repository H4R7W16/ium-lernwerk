# Technischer Prüfleitfaden – R5-M06

**Leeres Instrument, Ausführung noch nicht erfolgt.** Jede Prüfung verwendet ausschließlich synthetische Arbeitsstände. Sie bindet den späteren V2-Build; vorhandene V1-Ergebnisse sind Referenzen. Das aktuelle Design hat noch keinen ausführbaren V2-Build.

## Prüfkopf und Ergebniscodes

Vor Ausführung in einer zugriffsbeschränkten Kopie außerhalb des Workspace dokumentieren: Protokollversion/-hash, Modul-ID/-version, Git-SHA, Builddigest, Materialrevision, Betriebssystem-/Browserfamilie und Version, Eingabe-/Assistenzweg, verwaltetes Profil ja/nein, Netzmodus und Erlaubnisreferenz. Keine Seriennummer, IP, Kontokennung oder Schulnetzkennung. Die bereinigte technische Reproduktion darf nur synthetische Inhalte enthalten.

Jeder Schritt erhält `pass`, `fail`, `not-run` oder `not-applicable` mit konkreter Begründung. `not-applicable` ist nur zulässig, wenn die geprüfte Variante diese Funktion nachweislich nicht anbietet und der Betrieb sie nicht voraussetzt. Eine nicht verfügbare, im Zielbetrieb benötigte Funktion ist `not-run` oder `fail`. Protokollzeilen dürfen diese Unterscheidung nicht durch eine globale Ausnahme überdecken.

## Zielmatrix festlegen

| Profil | Pflicht, sobald … | Prüfungen |
| --- | --- | --- |
| Z-DESKTOP | Desktop/Notebook zum vorgesehenen Einsatz gehört | Alle TECH-Prüfungen; Tastatur ohne Drag-and-drop; jeweiliger verwalteter Browser. Chromium-Ergebnis gilt nicht für Firefox. |
| Z-TABLET | Tablet zum vorgesehenen Einsatz gehört | Alle TECH-Prüfungen; Touch, Bildschirmtastatur, Dateidialoge und Export-/Importziel im verwalteten Profil. |
| Z-ASSISTIVE | Assistiver Zugang für die geplante Nutzung gebraucht oder als geeignet angeboten wird | Vollständige eigene Codeeingabe, Grafik-/Textalternative, Zustand, Spur, Fehlermeldung und Fokus mit genau benanntem Hilfsmittel; zum Beispiel VoiceOver/Safari. Automatisierte Accessibility-Checks genügen dafür nicht. |
| Z-NETWORK | Jeder reale Einsatz | Erstaufruf und Wiederaufruf über den tatsächlichen freigegebenen Zugangsweg; Netzunterbrechung und zuständige Policy. Offline-Eignung nur behaupten, wenn diese Variante geprüft ist. |
| Z-LMS | Tatsächlich ein LMS-Link oder iframe genutzt werden soll | Echte Weiterleitung/Einbettung, Speicherpartitionierung, Downloadberechtigung, eigener Tab und Rückkehr. Ein Direktaufruf ersetzt keine LMS-Prüfung. |

Vor Erprobung legt die verantwortliche Stelle die tatsächlich angebotenen Profile fest. Eine reine Desktoperprobung darf auf diesen Bereich begrenzt werden; sie bestätigt keine Tablet-/Assistenz-/LMS-Eignung. Ein Ausschluss darf keine für teilnehmende Lernende benötigte Zugänglichkeit entfernen. Dafür muss ein gleichwertiger Kernzugang geprüft werden, sonst beginnt diese Nutzung nicht.

## Reproduzierbare Prüfaufträge

| ID / Bezug | Schritte mit synthetischen Daten | Erwartung / Gegenprüfung |
| --- | --- | --- |
| TECH-01 Build und Bindung / F07,F08 | Revision/Builddigest und Materialversion notieren. M06 öffnen. S3-Auftrag, Start, Raster, Prüfpunkte, Sprache und Produktfelder gegen MOD prüfen. | Kein alter IUM-5-CORE-05-Lernweg, keine elf Pflichtphasen, keine alte Coverage oder 270-Minuten-Variante. Abweichende Revision stoppt die Zusammenführung von Evidenz. |
| TECH-02 Fachsemantik / F07 | S0: `(1,3)/N`, vor/rechts/vor. S1: `(2,3)/O`, 4×[vor,links]. S2: 4×[vor],links. S3: `(1,3)/O`, 2×[vor,vor,links,vor,links]. Im V2-Editor eingeben und schrittweise ausführen. | S0 `(2,2)/O`, 3 Aktionen. S1 Rückkehr/O, 8 Aktionen. S2 erste fachliche Abweichung Aktion 2, Grenzfehler Aktion 3 bei vorher `(4,3)/O`. S3 fünfteiliger Körper akzeptiert, 10 Aktionen, Prüfpunkte `(3,3),(3,2),(1,2),(1,3)`, Abschluss O. Der bisherige V1-Parser lehnt den Körper ab; dies muss erst behoben werden. |
| TECH-03 Spur und fachliches Ziel / F07 | Bei S3 leeres Programm und Referenzprogramm vergleichen. Anfangs-/Endposition, durchlaufene Prüfpunkte, Anweisungsreferenz und Iteration einzeln prüfen. Danach Code ändern und eine alte Spur aufrufen. | Programmende allein meldet kein erfülltes Fahrziel. Leeres Programm besucht die Prüfpunkte nicht. Alte Spur ist dem alten Code zugeordnet/als veraltet erkennbar; keine falsche Bestätigung nach Revision. |
| TECH-04 Versionen und Recovery / F01,F02 | Gültigen synthetischen Stand speichern. Direktladen und Import mit falscher Modulversion, unbekannter Payloadversion und beschädigtem Envelope versuchen. Fehlerzustand verlassen, Originalsicherung anfordern. | Direktladen und Import verwenden denselben erklärten Supportvertrag. Ungültiger Stand wird nicht aktiviert. Originaldaten bleiben als gekennzeichnete Recoverydatei erreichbar, ohne als kompatibler Lernstand zu gelten; gültiger vorhandener Stand bleibt geschützt. |
| TECH-05 Importtransaktion / F03 | Gültigen Import A vorprüfen, dann ungültigen B vorprüfen, danach Bestätigung versuchen. Wiederholen mit A-Vorschau und anschließend Löschen des aktiven Stands. | Kein altes A bleibt unbemerkt bestätigbar. Abbruch/Fehler/Löschen räumt ausstehende Importaktion auf. UI und öffentliche Laufzeitschnittstelle beide prüfen. |
| TECH-06 Speicherung, Tabs und Löschen / F04 | Synthetisches P3 in zwei Tabs öffnen, unterschiedlich ändern, speichern; einen Tab löschen lassen und im anderen weiterschreiben. Profilwechsel auf gemeinsamem Gerät prüfen. | Dokumentierter Konfliktpfad statt stiller Überschreibung. Gelöschter Stand lebt nicht unbemerkt wieder auf. Keine fremden Dossiers im nächsten Profil. Ein Origin-/Modulschlüssel allein ist kein persönlicher Arbeitsraum. |
| TECH-07 Speicherwahl und Datenwege / F05 | Frisches Profil: vor und nach Speicherwahl IndexDB/Netz/Clipboard prüfen; Export, Rückimport und Löschen durchführen. Speicherfehler provozieren. | Keine behauptete Einwilligungswahl bei tatsächlichem automatischem Schreiben. Klar erkennbar, was lokal gespeichert/temporär ist. Kein automatischer Clipboard-Export bei Fehler. Export nur bewusst, Zielort bekannt. App-Löschen entfernt nicht behauptetermaßen externe Kopien. |
| TECH-08 Volatil, Offline und Update / F06 | Temporären Modus mit P3 verwenden, Reload/Update auslösen. Persistentes Profil offline wiederöffnen. Speicherfehler und abgebrochenes Update, dann Update bei zweitem Tab testen. | Erfolgreiches Memory-flush wird nicht als Reloadsicherheit behandelt. Kein Reload vor echter Sicherung oder bewusster Verlustentscheidung. Fehlerpfad bleibt bedienbar; andere Tabs werden koordiniert. Kein Offlineversprechen aus einem bloßen Erstaufruf. |
| TECH-09 Eingabe und Gleichwertigkeit / F07,F08 | S3 allein per Tastatur, anschließend je angebotener Touch-/Assistenzvariante selbst bearbeiten. Zoom/Reflow prüfen; Fehler, Hilfe, Grafik, Trace und Wiedereinstieg lesen. | Alle Kernhandlungen erreichbar, Fokus nachvollziehbar, Texte nicht abgeschnitten, Gruppierung nicht nur farblich. Text-/Printweg erhält fachliche Beziehung. Ein Papierweg erfüllt ALG-005 nicht. |
| TECH-10 Netz, Betrieb und Rechte / F05,F08 | Tatsächlichen Route-/Profilvertrag mit synthetischem Stand prüfen, Requests und Hostinglog-Kategorien sichten; ausgelieferte Assets mit Rechteverzeichnis vergleichen. | Keine unerwarteten Drittressourcen/Telemetrie. Hosting-/LMS-Logs getrennt vom App-Speicher bewertet. Betreiber und Schulstelle haben den konkreten Betrieb entschieden. Prüfung eines synthetischen Builds ist keine solche Entscheidung. |
| TECH-11 Wiederaufnahme und Verlust / F02,F04,F06 | Mit vorhandenem, fehlendem, altem und nicht lesbarem Stand jeweils erneut starten; P4 vor alter Lösung und danach bewusste Arbeitswiederaufnahme testen. | Stand/offener Punkt/nächste Handlung sichtbar. Fehlender Stand führt zu Ersatzdiagnose/Nachsicherung. Abruf bleibt von Dateiwiederherstellung getrennt. Kein Fortschritt durch bloßes Wiederöffnen. |

TECH-07 umfasst zusätzlich die Prüfung, dass P0/P4 nicht dauerhaft im Dossier/Export landen und keine Versuchshistorie, Hilfezählung oder Pilottelemetrie gespeichert wird. Nach einem vollständigen synthetischen Durchlauf App-Stand und bewusst erzeugten Export direkt auf diese Daten prüfen; eine fehlende sichtbare Anzeige ist kein Beleg fehlender Speicherung.

S4/S5 sind fachliche Materialprüfungen: S4 wiederholt den vollständigen Körper aufnehmen/prüfen/ablegen dreimal; die getrennt gruppierte Fassung scheitert an zweiter Aufnahme. S5 unterscheidet digitale Zeitsteuerung und Wegberechnung von Papierbeschreibung und unzureichendem Standbild. Diese Fälle verlangen im Entwurf keinen zusätzlichen Interpreter für Werkstücke oder reale Navigationsalgorithmen.

## Ergebniszeile zum Kopieren

| Profil | TECH-ID | Geprüfte Revision | Ergebnis | Bereinigter Reproduktionsbezug | Schwere | Nacharbeit / Wiederprüfung |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | — | not-run | — | nicht bewertet | — |

Bei kritischem Fehler den betroffenen Pfad stoppen und den Fehlerzustand mit synthetischen Daten nachvollziehbar machen. Reale Arbeitsstände nicht in Bugreports kopieren. Für F08 bleiben die dokumentierten Firefox-Runner-/WebKit-Fokusbefunde offene Eingaben; grüne andere Browser ersetzen ihre Prüfung nicht. Die spätere Umsetzung muss auch Node-/CI-Vertrag und explizite V2-Aktivierungsprüfung zusammenführen. Dieses Paket ändert weder CI noch Runtime.
