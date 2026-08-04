# IUM5 Gate B – Pilotleitfaden

```yaml
class-relation: different-class-required
retention: 30-days-after-decision
```

## Zweck und Grenze der Aussagekraft

Die Pilotierung prüft Durchführbarkeit, Passung des Zeitmodells und beobachtbare Lernhandlungen im Modul IUM-5-CORE-05. Sie ist weder Wirksamkeitsstudie noch Unterrichts- oder Produktfreigabe. Beobachtet werden ausschließlich geschlossene Klassenaggregate; individuelle Lernprodukte und personenbezogene Aufzeichnungen gehören nicht zur Pilot-Evidenz.

## Rollen

- Die Pilotlehrkraft verantwortet Unterricht, Fallback und Schutz der Lernenden.
- Eine beobachtende Rolle codiert nur die neun vereinbarten Kriterien auf dem analogen Bogen.
- Engineering ist für Buildidentität, technische Abbruchcodes und Wiederherstellung zuständig, greift aber nicht in fachliche Lernhandlungen ein.
- Koordination prüft Eintritt, Trennung der beiden Lerngruppen, Aggregation, Löschung und Übergabe.
- Die beauftragende Stelle entscheidet über eine begrenzte technische Ausnahme und später über die weitere Reviewroute.

Mindestens Unterricht und Beobachtung liegen bei verschiedenen Personen. Technische Hilfe darf Denken nicht durch Vormachen ersetzen.

## Eintrittscheckliste

- [ ] Auftrag, Nichtfreigabegrenze und öffentliche Zugänglichkeit der Link-URL wurden den beteiligten Erwachsenen erklärt.
- [ ] SHA, Preview-ID, Status `working` und `deviceVerified: not-run` stimmen mit dem technischen Paket überein.
- [ ] Die Sechs-Zeilen-Matrix ist `pass` oder für den ersten Lauf liegt genau eine schriftlich akzeptierte Ausnahme vor.
- [ ] Geräte, Netz, LMS-Route, Offlinepfad und eigener-Tab-Fallback wurden vorbereitet.
- [ ] Der analoge Beobachtungsbogen trägt nur Kontextbänder und geschlossene Codes.
- [ ] Abbruchsignal, Ersatzmedium und Rollenkommunikation wurden vor Beginn geprobt.
- [ ] Für die Bestätigung ist eine andere Lerngruppe verbindlich eingeplant.

Fehlt ein Punkt, beginnt keine Pilotstunde.

## Explorative Durchführung: regular-225

Der erste Lauf umfasst fünf Einheiten zu je 45 Minuten. Die Pilotlehrkraft führt den regulären Lernpfad aus: präzisieren, Algorithmus aufbauen und vorhersagen, ausführen und Laufspur erklären, erste Abweichung lokalisieren und minimal reparieren, erneut testen sowie Strategien und Systembezug gemeinsam sichern.

Die beobachtende Rolle markiert je Kriterium nur `met`, `partly`, `not-met` oder `not-observable`. Sie notiert keine Äußerungen einzelner Personen. Nach jeder Einheit werden Zeitband, Abweichungscode, Fallbackfunktion und Störungscode gemeinsam plausibilisiert; die Pilotlehrkraft sieht keine Auswertung auf Personenebene.

## Reparatur-Checkpoint

Nach dem explorativen Lauf trennen die Rollen drei Fragen:

1. Ist eine technische Störung reproduzierbar und vor der Bestätigung zu schließen?
2. Muss eine Instruktion, Orchestrierung oder Unterstützung minimal angepasst werden?
3. Bleibt dabei der fachliche Kern der Lernschleife unverändert?

Jede Änderung erhält eine neue Buildidentität und macht technische Evidenz des alten Builds unbrauchbar. Eine inhaltliche Änderung wird vor der Bestätigung fachlich geprüft. Ein Datenschutzbefund beendet die Route statt einen Reparaturversuch mit zusätzlichen Daten auszulösen.

## Bestätigung: extended-270

Der zweite Lauf verwendet eine andere Lerngruppe und den erweiterten Pfad mit sechs Einheiten zu je 45 Minuten. Die sechste Einheit vertieft feste Wiederholung und Modellgrenzen; sie ersetzt keinen Kernbestandteil. Matrix, SHA, Preview-ID, Beobachtungscodes und Unterstützungsregeln bleiben identisch zur reparierten Prüffassung.

Eine Wiederholung mit derselben Lerngruppe, ein Mischbuild oder eine fehlende sechste Einheit wird `not-evaluable`. Eine begrenzte technische Ausnahme aus dem ersten Lauf gilt hier nicht.

## Neun Beobachtungen

| ID | Beobachtbarer Klassenbefund |
| --- | --- |
| `prediction-used` | Vorhersagen werden vor dem Ausführen fachlich genutzt. |
| `trace-explained` | Laufspuren erklären Zustandsänderungen. |
| `first-deviation-localized` | Die erste Abweichung wird im Ablauf lokalisiert. |
| `repair-hypothesis` | Die Reparatur folgt einer benannten Hypothese. |
| `minimal-revision-retested` | Eine minimale Änderung wird erneut ausgeführt. |
| `loop-decision-justified` | Die Entscheidung für oder gegen feste Wiederholung wird begründet. |
| `systems-transfer` | Algorithmische und nichtalgorithmische Systeme werden unterschieden. |
| `support-preserves-thinking` | Unterstützung erhält die kognitive Lernhandlung. |
| `shared-consolidation` | Die gemeinsame Sicherung expliziert Begriffe und Strategien. |

Für eine positive Laufbewertung dürfen die ersten sechs Kriterien weder `not-met` noch `not-observable` enthalten; höchstens eines steht auf `partly`. Gemeinsame Sicherung und Zeitpassung müssen abgeschlossen sein.

## Optionale Drei-Fragen-Rückmeldung

Die freiwillige anonyme Rückmeldung verwendet genau diese drei geschlossenen Prompts:

- `clarity`: „Ich wusste, was ich als Nächstes tun sollte.“
- `cognitive-engagement`: „Vorhersage und Laufspur haben mich zum Nachdenken über den Ablauf gebracht.“
- `support-usefulness`: „Die Hilfen haben mir weitergeholfen, ohne mir die Lösung abzunehmen.“

Je Prompt werden nur `agree`, `partly`, `disagree` und `noAnswer` gezählt. Unter zehn gültigen Antworten lautet die einzige digitale Ausgabe `suppressed`; Kategorien und Summen werden nicht gespeichert. Die Rückmeldung ist optional, nicht leistungsbezogen und keine Diagnostik.

## Abbruch und Fallback

Die Pilotlehrkraft stoppt bei Datenschutzrisiko, Barrierefreiheitsblocker, falschem Build, Zustandsverlust, nicht beherrschbarer technischer Unterbrechung oder wenn die fachliche Lernzeit zusammenbricht. Der Unterricht wechselt dann auf das vorbereitete funktionsgleiche analoge oder lehrkraftgesteuerte Medium. Ein Fallback zählt nur als `equivalent`, `partial` oder `not-equivalent`; er wird nicht durch zusätzliche Beobachtungsdaten kompensiert.

## Aggregation, Vernichtung und Löschung

Nach jeder Runde übertragen Beobachtung und Pilotlehrkraft nur geschlossene Klassenaggregate in das private Pilotpaket. Der Papierbogen wird unmittelbar nach kontrollierter Übertragung vernichtet; bei Nichtnutzung wird `not-used` gesetzt. Reale digitale Pakete bleiben außerhalb des Repositories, werden nur den benannten Reviewrollen zugänglich gemacht und spätestens 30 Tage nach der Entscheidung einschließlich temporärer Kopien gelöscht. Ohne bestätigte Vernichtung und Löschung ist die Gesamtempfehlung nicht positiv.
