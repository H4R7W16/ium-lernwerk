# Wiederaufnahme · Durchführung und Erwartungen

**20 + 20 + 30 + 20 = 90 Minuten · eigenes Jahreskonto**

Die vier Lernendenseiten sind vollständig. Nach 1–2 Wochen Abstand zum jeweiligen Bogen, die gemischte Seite vor Klasse 8 einsetzen. Keine Vorbereitungs-Hausaufgabe. Zuerst ohne Sicherung abrufen, danach Belege vergleichen und eine Stelle gezielt verbessern. Lösungen erst im Vergleichsfenster gemeinsam öffnen; diese öffentlich zugänglichen Seiten sind kein gesicherter Testbereich.

Die 20-Minuten-Seiten verwenden **8 selbst lösen + 5 vergleichen/klären + 5 verbessern/erneut prüfen + 2 Anschluss**. Die Codeseite verwendet **12 + 7 + 8 + 3 = 30**. Vorlesen und gleichwertige mündliche Antworten ermöglichen. Wer Hilfe braucht, markiert die fragliche Angabe; erst einen Hinweis geben, dann eine eigene Erklärung verlangen. Kein vollständiges Muster abschreiben lassen.

## Medien · Beleg und Reichweite

[Lernendenseite](wiederaufnahme-medien.html)

B belegt 16 von 20 freiwillig teilnehmenden AG-Mitgliedern mit Wunsch nach einer **zusätzlichen AG-Ausgabe**. Weder ganze Schule noch ausschließlich digitale Bücher sind belegt. C übernimmt A und ist kein unabhängiger Beleg. D bestätigt unabhängig den Gegenstand der Frage, aber weder die Stimmenzahl noch eine Schulmehrheit. Likes ersetzen diese Belege nicht. Absichtliche Täuschung ist aus den Angaben nicht nachweisbar.

Mögliche Überschrift: „16 befragte Mitglieder der Bücher-AG wünschen zusätzliche digitale Lektüre“. A nicht in der irreführenden Form weitergeben; wenn weitergegeben, mit Korrektur und Beleg. Neuer Fall: „9 von 12 befragten Robotik-AG-Mitgliedern wünschen einen zweiten Termin“. Für ein Urteil über die gesamte Schule braucht es eine geeignete Befragung dieser Zielgruppe mit klarer Frage; eine neue Prozentrechnung allein repariert die Reichweite nicht.

**Anschluss:** Bei Verwechslung Gruppe und Frage jeweils im Original unterstreichen lassen, dann den neuen Fall ohne Muster lösen. Bei Quellenverwechslung den Herkunftspfeil C→A zeichnen. Nur die offene Teilfrage nachprüfen.

## Daten · Eindeutigkeit und Modellgrenze

[Lernendenseite](wiederaufnahme-daten.html) · übernimmt den bereits geplanten Datenabruf und ergänzt seine Rückmeldewege.

`0|10` bedeutet XY, `01|0` bedeutet ZX. Eine mögliche Reparatur: X→00, Y→01, Z→10, fester Beginn und Zweiergruppen. Gleich lange, verschiedene Wörter funktionieren bei vereinbartem Anfang. YZX wäre mit dieser Tabelle `011000`; andere eindeutige Tabellen gelten ebenso.

12×8 = 96 Bit = 12 Byte; mit 12 Text-Byte insgesamt 24 Byte, also 6 Byte frei. Gegenfall: 8×8 = 64 Bit = 8 Byte; plus 10 = 18 Byte, also 2 Byte frei. Einheiten mitführen. Nur Nutzdaten unter den genannten Regeln, keine reale Dateigrößenprognose.

Datenreduktion muss die benötigten Informationen erhalten: Erkennbarkeit im Plan, feine Schadensdetails in der Dokumentation. Verwechselbare Zeichen verfehlen den Zweck. Exakte Strommengen lassen sich ohne weitere Angaben zu Technik und Betrieb nicht aus Dateigrößen ableiten.

**Anschluss:** Bei Codefehlern zwei Segmentierungen zeigen lassen. Bei Einheitenfehlern zuerst Pixel→Bit, dann Bit→Byte. Bei pauschalem „kleiner ist besser“ den konkreten Nutzungszweck benennen lassen und den neuen Symbolfall prüfen.

## Programmieren · Bedingung vor Bewegung

[Lernendenseite](wiederaufnahme-programmieren.html)

`3+3` liefert die Zahl 6; `x=36` einen Wahrheitswert. `sage` ist hier ein Befehl zur Ausgabe des Texts und kein Reporter für einen rückgegebenen Rechenwert. Nach der festen Wiederholung ist x=12. Es folgen 22, 32, 42, 52. Danach immer weitere Zehnerschritte: Die letzte Ziffer bleibt 2; 36 wird nicht erreicht. Die nachfolgende Meldung läuft im idealisierten Modell deshalb nicht an.

Passende Reparatur: `nicht (x < 36)` beziehungsweise mathematisch `x ≥ 36`. Die vereinfachte Ablaufzeichnung prüft zuerst: wahr→Stopp, falsch→10 Schritte→erneute Prüfung. Der Vergleich muss sich auf die vereinbarte Zielregel beziehen; „genau 36“ wäre eine andere Aufgabe.

| Start der reparierten bedingten Schleife | Endposition | Bewegungen | Prüfungen |
|---:|---:|---:|---:|
| 12 | 42 | 3 | 4 |
| 36 | 36 | 0 | 1 |
| 40 | 40 | 0 | 1 |

Bei Start 12 unterscheiden sich die Regeln zuerst an Position 42: Gleichheit falsch, „mindestens 36“ wahr. Neuer Fall 31 mit Schrittweite 8 endet bei 39 nach einer Bewegung und zwei Prüfungen. „Ziel erreicht oder überschritten“ passt; „genau am Ziel“ wäre falsch. Die Startwerte beziehen sich ausdrücklich nur auf die bedingte Schleife, damit die feste Wiederholung sie nicht zuvor verändert.

**Anschluss:** Bei Verwechslung der Prüfungen mit Bewegungen zuerst die Entscheidung an x=36 erklären lassen. Bei fehlender Grenze den Fall x=40 erneut prüfen. Bei Datenartfehlern einen Reporterwert von einer ausgeführten Handlung unterscheiden lassen. Erst anschließend eine kurze eigene Codeerprobung im Unterstützungskonto, wenn ein praktischer Nachweis noch offen ist.

## Gemischt · Neue Situation, bekannte Kriterien

[Lernendenseite](wiederaufnahme-gemischt.html)

1. Belegt ist die Antwort von 6/8 freiwillig befragten AG-Mitgliedern zu einem weiteren Termin. Ganze Schule und wöchentlicher Termin sind nicht belegt; auch 2.000 Likes ändern das nicht.
2. 8×8 Bit = 8 Byte; 16×16 Bit = 32 Byte. Die kleinere Variante genügt, wenn das Symbol für den Zweck eindeutig erkennbar bleibt. Ohne sichtbare Bilder keine konkrete Qualitätsbehauptung. Größer ist dann nicht automatisch zweckmäßiger; Stromverbrauch nicht exakt daraus ableiten.
3. 28→35→42→49…; 40 wird bei diesen Siebenerschritten nicht getroffen. `nicht (x < 40)` stoppt bei 42 nach zwei Bewegungen. Start 42: keine Bewegung, eine Prüfung.
4. Passwort nicht weitergeben, Druck benennen und eine erreichbare Lehr-/Vertrauensperson hinzuziehen. Bei bereits erfolgter Weitergabe mit Unterstützung das Konto absichern. Freundschaft macht die Forderung nicht zu einer sicheren Zusammenarbeit. Keine realen Passwörter oder eigenen Erfahrungen abfragen.

**Sicherung und Übergabe:** Pro Person eine aussagekräftige Begründung oder offene Stelle erfassen, keine pauschale Rangliste. Eine Begründung aus der Vergleichsphase durch den neuen Fall individuell gegenprüfen. Die kurze Mischung zeigt einzelne fachliche Anschlüsse; praktische Eigenleistungen und private Reflexion bleiben eigene Nachweise beziehungsweise geschützte Bereiche. Größerer Nachholbedarf zählt zum Unterstützungskonto und wird mit tatsächlichen Minuten dokumentiert.
