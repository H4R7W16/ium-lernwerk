# Lehrkräfteanleitung zum IUM11-Pilotinstrument

<!-- IUM11-PUBLICATION-CONTRACT:START -->
<!-- Generiert aus Pilotprotokoll und Zeitmodell; nicht manuell bearbeiten. -->
| Bereich | Verbindliche Fakten |
| --- | --- |
| Vertragsbindung | schemaVersion: 1; id: IUM11-PUBLICATION-CONTRACT; contractVersion: 1.0.0; protocolPath: pilot/pilot-protocol.json; timeModelPath: roadmap/time-model.json; protocolVersion: 1.0.0; toolVersion: 1.0.0; timeModelFingerprintAlgorithm: sha256-canonical-json-v1; timeModelFingerprint: 873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1 |
| Kernpfad | variantId: GRADE-7-WORKING-40; targetUnits: 40; clusterCount: 4; moduleCount: 10; pilotStageCount: 5 |
| Clusterbudgets und Rückfälle | id: CLUSTER-7-DATA-CODING; order: 1; budgetUnits: 8; fallbackDeltaUnits: 3; id: CLUSTER-7-PROGRAMMING; order: 2; budgetUnits: 11; fallbackDeltaUnits: 2; id: CLUSTER-7-NET-SECURITY; order: 3; budgetUnits: 11; fallbackDeltaUnits: 3; id: CLUSTER-7-DATA-MEDIA-SOCIETY; order: 4; budgetUnits: 10; fallbackDeltaUnits: 6 |
| Privacygrenze | minimumLearnerResponses: 10; personalDataAllowed: false; realPackagesInRepositoryAllowed: false |
| Aktuelle Urteilachsen | status: working; availabilityStatus: conditional; timeFeasibilityStatus: amber; sequenceEvidenceStatus: covered; pilotStatus: not-started; semanticCoverageStatus: partial |
| Aussagegrenze | statementBoundary: documented-conditions-only |
| Zulässige Empfehlung | allowedRecommendation: eligible-for-working-availability-review |
| Gesperrte Reifegrade | forbiddenMaturityValues: reviewed; forbiddenMaturityValues: standard |
| Spätere Auftraggeberentscheidung | requiresCommissionerDecision: true; secondIndependentAnnualRunRequiredForMaturity: true; allowedChanges: availabilityStatus: available; allowedChanges: timeFeasibilityStatus: green; allowedChanges: pilotStatus: completed; unchangedAxes: status: working; unchangedAxes: semanticCoverageStatus: partial |
| Reale Pilotierung | realPilotCompleted: false; syntheticValidationOnly: true |
| Flexible Module | flexibleModulesOutsideCorePreserved: true; flexibleModuleSubstitution: forbidden; Flexible Vertiefungs-, Transfer- und Projektmodule bleiben sichtbar erhalten. |
<!-- IUM11-PUBLICATION-CONTRACT:END -->

## 1. Zweck und Aussagegrenze

Das IUM11-Pilotinstrument prüft den Klasse-7-Kernpfad unter dokumentierten Einsatzbedingungen. Die verbindlichen Fakten, Aussagegrenzen und späteren Entscheidungsvorbehalte stehen im automatisch erzeugten Faktenblock. Ein positiver Minimalpilot ist weder eine Statusfreigabe noch ein Wirksamkeitsnachweis.

## 2. Bereitschaftsgate vor jedem Lauf

Beginnen Sie einen Clusterlauf erst, wenn alle sieben Punkte nachweislich erfüllt sind:

1. Fachlich reviewfähige Lernmaterialien liegen für alle Module des Scopes vor.
2. Das zugehörige Lehrkräftehandbuch liegt vor.
3. Ankeraufgaben und Kriterien sind vollständig.
4. Digitale Werkzeuge und gleichwertige lokale Fallbacks funktionieren.
5. Die Privacygrenzen wurden geprüft.
6. Die reale Kapazität für den gewählten Pilotpfad ist gesichert.
7. Vertrags- und Protokollfingerprint sind aktuell.

Ist ein Punkt offen, beginnt der Lauf nicht. Dokumentieren Sie die Klärung außerhalb personenbezogener Systeme und prüfen Sie das Gate danach erneut.

## 3. Reihenfolge und Jahresvoraussetzung

Führen Sie die vorgesehenen Cluster in Protokollreihenfolge mit ihren harten, nicht verrechenbaren Budgets durch. Die konkrete Reihenfolge und die Budgets stehen im Faktenblock.

Zeiten zwischen Clustern werden nicht verrechnet. Additive Fallbackbedarfe sind nur Bedarfsableitungen und kein automatisch verfügbares Angebot. Der Jahreslauf wird erst freigeschaltet, wenn die erforderlichen versionsgleichen Clusterpakete in dieser Reihenfolge lokal importiert wurden.

## 4. Lernprodukte lokal prüfen

Prüfen Sie Ankerprodukte, Revisionen und Übergabeprodukte ausschließlich lokal in der vorgesehenen Lernumgebung. Übernehmen Sie weder Produkt noch Ausschnitt in das Cockpit. Erstellen Sie keine Kopie, keinen Upload, keinen Screenshot und keinen Link. Im Paket steht nur der aggregierte Befund, ob das Übergabeprodukt vorlag und funktional weiterverwendet wurde.

## 5. Klassenbänder vergeben

Bewerten Sie jedes protokollierte Muss-Kriterium für die Klasse als `strong`, `mixed` oder `weak`:

- `strong`: Die geforderte Lernhandlung und das Lernprodukt sind im Klassenbefund tragfähig belegt.
- `mixed`: Der Klassenbefund ist uneinheitlich oder nur teilweise tragfähig.
- `weak`: Die geforderte Qualität ist im Klassenbefund nicht belegt.

Nur durchgängig `strong` kann einen positiven Modul-, Integrations- oder Jahresbefund tragen. Die Bänder sind Projekt-Akzeptanzgrenzen, keine Noten und keine individuellen Kompetenzprofile.

## 6. Dreiteiligen Lernendenimpuls aggregieren

Erheben Sie ausschließlich die drei Protokollitems `clarity`, `cognitiveEngagement` und `supportUsefulness` mit den Kategorien `agree`, `partly`, `disagree` und `no-answer`. Es gibt keine Freitexte. Zählen Sie die Antworten außerhalb des Cockpits und geben Sie dort je Item nur die vier Klassensummen ein. Einzelantworten, Reihenfolgen und Zuordnungen werden nicht übertragen.

Bei unter zehn gültigen Antworten wählen Sie `suppressed-small-group`; alle Zählwerte bleiben unterdrückt. Die Schwellenregel für offene Entwicklungswarnungen steht im Faktenblock. Verwenden Sie dafür ausschließlich die im Cockpit neu berechnete ganzzahlige Schwelle.

Eine optionale analoge Zählhilfe dient nur temporär der Durchführung. Vernichten Sie sie unmittelbar nach der Übertragung der Summen. Sie begründet keine parallele analoge Vollstruktur.

## 7. Technik, Fallback und Privacy prüfen

Erfassen Sie technische Funktion, Problemcode, Schweregrad und den Einsatz eines Fallbacks. Ein technischer Ausfall kann nur dann als gleichwertiger Pfad gelten, wenn der tatsächlich aktivierte Fallback dieselbe Lernfunktion erhält. Markieren Sie dies nicht vorsorglich.

Das Privacygate muss positiv sein. Bei einer Privacyverletzung lautet die Ableitung `fail`; der Export bleibt gesperrt. Entfernen Sie nicht nur ein problematisches Feld, sondern verwerfen Sie den Entwurf, klären Sie die Ursache und beginnen Sie mit einem neuen, ausschließlich aggregierten Datensatz.

## 8. Im Cockpit prüfen, importieren und herunterladen

1. Öffnen Sie `pilot/cockpit/index.html` lokal in einer aktuellen Browserengine.
2. Bestätigen Sie alle sieben Bereitschaftspunkte und wählen Sie den Scope.
3. Erfassen Sie ausschließlich die aggregierten Pflichtfelder.
4. Wählen Sie „Neu ableiten und prüfen“. Das Cockpit zeigt ein fokussierbares Fehlerresümee und einen verständlichen Korrekturhinweis.
5. Korrigieren Sie Fehler in der Quelle. Beschädigte, veraltete oder widersprüchliche Dateien werden nicht übernommen.
6. Laden Sie erst das frisch validierte JSON bewusst herunter. Ohne Download geht der flüchtige Zustand beim Schließen oder Neuladen verloren.
7. Für den Jahreslauf importieren Sie die vier positiven Clusterpakete erneut und in Protokollreihenfolge. Ein fehlender, nicht positiver oder versionsfremder Import sperrt den Jahresmodus.

## 9. Fünf aktuelle Pakete lokal zusammenführen

Halten Sie die vier positiven Clusterpakete und das positive Jahrespaket in einem nichtöffentlichen Ordner außerhalb des Repositorys bereit. Erzeugen Sie dort das Entscheidungspaket; wiederholen Sie `--evidence` genau fünfmal:

```powershell
python -B scripts/validate_ium11.py `
  --evidence C:\privat\cluster-1.json `
  --evidence C:\privat\cluster-2.json `
  --evidence C:\privat\cluster-3.json `
  --evidence C:\privat\cluster-4.json `
  --evidence C:\privat\jahreslauf.json `
  --decision-output C:\privat\ium11-entscheidung.json
```

Alle Eingaben und `--decision-output` müssen außerhalb des Repositorys liegen. Vorhandene Ausgabedateien werden nicht überschrieben. Nur fünf aktuelle, versions- und fingerprintgleiche Pakete werden zusammengeführt.

## 10. Nach `fail` oder `not-evaluable` wiederholen

Nach `fail` beheben Sie die verletzte Muss-Bedingung, planen den betroffenen Scope neu und wiederholen ihn vollständig. Nach `not-evaluable` stellen Sie Pflichtdaten, Interpretierbarkeit, Versionen und Fingerprints wieder her und wiederholen den Scope ebenfalls vollständig. Alte und neue Pakete werden nicht gemischt; der Jahreslauf verwendet nur die vier aktuellen positiven Clusterpakete.

## 11. Aufbewahren und löschen

Bewahren Sie reale Evidenz- und Entscheidungspakete nichtöffentlich und zugriffsbeschränkt nur bis zur Auftraggeberentscheidung auf. Danach sind Pakete, lokale Dateinamen-Zuordnungen und temporäre Zählhilfen zu löschen, sofern keine abweichende institutionelle Aufbewahrungspflicht gilt. Dokumentieren Sie eine solche Pflicht außerhalb des öffentlichen Repositorys.

Speichern Sie niemals reale Pakete, Rohprodukte, Dateinamen-Zuordnungen oder Verknüpfungen in Git, GitHub, Tickets oder öffentlichen Reviewartefakten. Im öffentlichen Repository verbleiben ausschließlich die ausdrücklich synthetischen Beispiele.
