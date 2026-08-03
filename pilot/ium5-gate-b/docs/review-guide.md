# IUM5 Gate B – Reviewleitfaden

## Evidenzklassen

Das Entscheidungspaket führt drei getrennte Klassen zusammen: technische Matrix, explorativer Pilotlauf und Bestätigungslauf. Hinzu kommen ausschließlich Rollenurteile und Löschstatus. Automatisierte Tests sind unterstützende Reproduzierbarkeitsevidenz, ersetzen aber weder reale Zielgeräte noch Pilotbefunde. Öffentliche synthetische Beispiele dürfen nicht als reale Evidenz gewertet werden.

## Buildkonsistenz

Technisches Paket, beide Pilotpakete und Entscheidungspaket müssen denselben vollständigen SHA und dieselbe Preview-ID tragen. Modul bleibt IUM-5-CORE-05 Version 0.1.0 mit Produktstatus `working` und Gerätestatus `not-run`. Fehlende, verkürzte oder widersprüchliche Identitäten ergeben `not-evaluable`; Reviewrollen dürfen sie nicht durch Interpretation heilen.

## Datenschutzvorrang

Ein Datenschutzbruch, eine verbotene Datenspur oder nicht bestätigte Evidenzhygiene hat Vorrang vor sonst positiven Befunden und führt zu `revise-required`. Es werden keine Rohdaten nachgefordert. Das Review hält nur den geschlossenen Befund fest, beendet den Zugriff und veranlasst Löschung beziehungsweise Klärung außerhalb des Repositories.

## Regeln für pass, revise und not-evaluable

| Lage | Technischer oder Pilotbefund | Gesamtroute |
| --- | --- | --- |
| sechs technische Zeilen positiv, beide Läufe vollständig, Kriteriengrenzen eingehalten | `pass` | Reviewfolge fortsetzen |
| Datenschutzbruch, technischer Fehler, Kriterium nicht erfüllt, mehr als ein teilweise erfülltes Kernkriterium oder abgelehntes Review | `revise-required` | Ursache schließen und neuen, konsistenten Evidenzsatz erzeugen |
| Evidenz fehlt, widerspricht sich, verwendet dieselbe Lerngruppe oder ein Urteil steht aus | `not-evaluable` | keine positive oder negative Wirksamkeitsaussage ableiten |
| eine technische Zeile im ersten Lauf formal akzeptiert, mit Kompensation und Abbruchcodes | `limited-accepted` | nur explorativer Eintritt; niemals positive Gesamtempfehlung |

Die Reihenfolge ist fest: Datenschutz, Vollständigkeit und Konsistenz, Negativkriterien, positive Eignung.

## Vier-Augen-Reviewfolge

1. Pilotlehrkraft bestätigt Durchführung, Fallback und Aggregation.
2. Fachlich-didaktischer Review prüft Lernschleife, Zeitmodell, Beobachtbarkeit und Unterstützungsqualität.
3. Engineering-, Accessibility- und Privacy-Review prüft Build, technische Matrix, Barrierefreiheit, Datenvertrag und Löschfähigkeit.
4. Koordination prüft Paketkonsistenz, getrennte Lerngruppen und Reviewvollständigkeit.
5. Die beauftragende Stelle akzeptiert oder verwirft ausschließlich die daraus abgeleitete Route.

Mindestens zwei unabhängige Rollen sehen jeden entscheidenden Befund. Eine Rolle darf den eigenen offenen Befund nicht allein schließen.

## Getrennte Pilot-, LMS- und Freigabeentscheidungen

- `pilot-decision` beantwortet nur, ob die zwei geplanten Pilotstufen nach Vertrag auswertbar durchgeführt wurden.
- `lms-decision` beantwortet nur, ob die reale schulische Route technisch und organisatorisch verwendet werden kann.
- `working-release-review` beantwortet erst danach, ob der vorhandene Arbeitsstand einer gesonderten Freigabeprüfung zugeführt werden darf.

Keine der drei Entscheidungen setzt automatisch Modulstatus, Gerätestatus, Deployment oder Unterrichtsfreigabe. Ein positives LMS-Ergebnis kompensiert keinen Pilot- oder Datenschutzbefund.

## Zulässige abschließende Empfehlung

Die einzige positive Ausgabe lautet `eligible-for-working-release-review`. Sie bedeutet ausschließlich: Der konsistente Gate-B-Evidenzsatz darf einer neuen menschlichen Entscheidung über den weiterhin als `working` markierten Stand vorgelegt werden. Alternativen sind `revise-required` und `not-evaluable`. Eine automatische Statusänderung oder Produktfreigabe ist ausgeschlossen; reale Pakete müssen gelöscht und die Löschung bestätigt sein.
