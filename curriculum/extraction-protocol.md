# Extraktionsprotokoll für Curriculumdaten

Dieses Protokoll ist für die Curriculum-Tasks 9 bis 12 verbindlich. Es schützt die Nachvollziehbarkeit zwischen amtlicher Vorlage, extrahiertem Datensatz und lokaler didaktischer Entscheidung.

## 1. Eingabe, Version und Freigabe

1. Ausschließlich eine im [Quellenregister](../docs/research/phase-0/source-register.json) registrierte Quelle verwenden.
2. Vor jeder Extraktion `source-status.md` auf Status, Fassung, Geltungsbereich und offene Monitoringfragen prüfen.
3. Bei PDF-Quellen Hash, Seitenzahl und Dokumentmetadaten erfassen. Die betreffende Seite wird zusätzlich gerendert und visuell gegen den extrahierten Text geprüft.
4. Bei Webseiten Abrufdatum, URL, Seitentitel und Abschnittsanker dokumentieren. Dynamische Webseiten erhalten kein erfundenes Jahr.
5. Nur `enacted`-Quellen können einen verbindlichen Kompetenzdatensatz begründen. `orientation`- und `administrative-information`-Quellen werden als Kontext oder Zuordnung, nie als Ersatz einer Kompetenznorm gespeichert.

## 2. Ein Datensatz pro Kompetenz

Jeder Kompetenzdatensatz enthält mindestens:

- `sourceId` und eine unveränderte Quellfassung bzw. den geprüften Hash;
- den Wortlaut der Kompetenz **wortgetreu**;
- einen präzisen Locator: bei PDF Seitenzahl plus Überschrift/Unterabschnitt, bei Webseite URL plus Abschnittsüberschrift und vorhandene Anker- oder Nummernangabe;
- die amtliche Nummer unverändert, sofern sie vorhanden ist;
- sonst eine deterministische, quellenspezifische ID in Dokumentreihenfolge nach dem für den Datensatz festgelegten Schema, derzeit `LH26-E-<Bereich>-<laufnummer>`, `BMB16-GYM-<Bereich>-<laufnummer>` beziehungsweise `INF7-16-GYM-<Bereich>-<laufnummer>`; nur für eine neue Quelle ohne bereits festgelegtes Schema gilt als generischer Fallback `<sourceId>--p<Seite-oder-Abschnitt>--<normalisierte-Überschrift>--<laufnummer>`, wobei die Normalisierung nur ASCII-Kleinbuchstaben, Ziffern und Bindestriche nutzt;
- Klassenstufe, Niveau und Kompetenzbereich als getrennte Felder;
- `status` mit genau einem Wert `verified`, `plausible` oder `open`.

`verified` bedeutet: Wortlaut und Locator wurden gegen die gerenderte Vorlage bzw. die Primärseite geprüft. `plausible` bedeutet: eine maschinelle oder manuelle Vorstrukturierung liegt vor, aber die Gegenprüfung steht noch aus. `open` bedeutet: die Information ist unvollständig, widersprüchlich oder vom Monitoring abhängig; sie darf nicht als Norm weiterverwendet werden.

## 3. Trennung der Aussageebenen

Kompetenztext, Beispiele, erläuternder Prosa-Text und lokale Interpretation werden in getrennten Feldern oder Datensätzen geführt. Lokale Interpretation erhält eine eigene Kennzeichnung und darf weder den Wortlaut verändern noch eine amtliche Nummer übernehmen. Beispiele sind keine Kompetenzen. Ähnliche Kompetenzen aus verschiedenen Quellen oder Klassenstufen werden nicht stillschweigend zusammengeführt; Beziehungen werden als explizite Verweise mit beiden Quell-IDs erfasst.

## 4. Prüfung und Umgang mit Unklarheiten

1. PDF: Text extrahieren, betreffende Seite rendern, Wortlaut, Nummerierung, Zeilenumbruch und Tabellen-/Listenstruktur vergleichen.
2. Webseite: sichtbaren Primärinhalt und verlinkte amtliche Downloads prüfen; Unterstützungsmaterialien nicht als Bestandteil des Bildungsplans behandeln.
3. Bei fehlender offizieller Nummer die Fallback-ID bilden, aber keinen Nummerncharakter vortäuschen.
4. Bei widersprüchlichen Fassungen beide Fassungen mit Quelle und Datum dokumentieren, `status: open` setzen und nicht zusammenführen.
5. Erst nach Vier-Augen-Prüfung oder dokumentierter Eigenprüfung kann ein Datensatz `verified` werden.

## 5. Quellenänderungslog

Für jede extrahierte Quelle wird ein fortlaufendes Log mit Datum, `sourceId`, alter und neuer Fassung (URL bzw. Hash), betroffenen Locators, Art der Änderung, Prüfperson und Auswirkung auf Datensätze geführt. Geänderte Quellen erzeugen neue oder revidierte Datensätze; bestehende Datensätze bleiben mit ihrer früheren Quellenfassung nachvollziehbar. Die offene Publikationsfrage zur Lesehilfe 2026/2027 wird bis zur verifizierten amtlichen Direkt-URL mindestens vor jedem Curriculum-Task erneut geprüft.
