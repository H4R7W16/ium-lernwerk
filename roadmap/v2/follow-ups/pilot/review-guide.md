# Auswertung und menschliche Folgeentscheidung

**Noch keine Auswertung eines realen Laufs.** `decision-scenarios.synthetic.json` enthält frei konstruierte Prüffälle für die Entscheidungsgrenzen. Das lokale Prüfskript kontrolliert Dokumentenbindung und diese Beispiele; es ist kein freigegebener Evaluator für reale Pilotdaten.

## 1. Reihenfolge der Auswertung

1. **Identität und Umfang:** Modul, Protokoll, Materialien, Builddigest und tatsächlich durchgeführte Variante stimmen überein. Exploration und Bestätigung getrennt betrachten. Abweichende Fassung bedeutet neuen Nachweisumfang.
2. **Schutz und Abbruch:** Ein tatsächlicher kritischer Vorfall verlangt Nacharbeit am betroffenen Pfad, auch wenn andere Belege fehlen. Widersprüchliche Schwere-/Abbruchangaben zuerst klären. Keine synthetische „Bestanden“-Kategorie darf hier ein reales Ereignis verdecken.
3. **Belegvollständigkeit:** Nicht ausgeführte Tests, ungesichtete Produkte, unbekannte Zeit und ungeklärter Hilfekontext führen auf der betroffenen Achse zu `nicht-beurteilbar`. Kein Mittelwert ersetzt sie.
4. **Befunde je Achse:** TECH, USE und TEACH erhalten getrennte Ergebnisse. Wiederholtes Bedienhindernis, fehlende eigene Programmierung oder abgeschnittene Sicherung führen zu konkreter Nacharbeit, ohne betroffene Personen zu bewerten.
5. **Folgeentscheidung:** Eine vollständige, widerspruchsfreie Bestätigung ohne offenen kritischen oder fachlich wesentlichen Befund kann nur eine menschliche Prüfung des nächsten Schritts vorbereiten. Institutionelle Erlaubnisse und Veröffentlichung bleiben eigene Entscheidungen.

## 2. Ergebnisregeln

| Achse | Für einen positiven begrenzten Befund erforderlich | Andernfalls |
| --- | --- | --- |
| TECH | Jede für den vorgesehenen Betrieb erforderliche Prüfung im passenden Profil an der passenden Revision tatsächlich bestanden; Ausschlüsse begründet und mit realem Bedarf vereinbar | Fehlgeschlagen → Nacharbeit; fehlender Lauf/Profilbezug → nicht beurteilbar. Kein Gesamterfolg aus einer Teilmatrix. |
| USE | Alle fünf Kernaufträge im angebotenen Zugang beobachtbar; keine offene Zugangsblockade; wiederholte Hindernisse behoben und erneut geprüft | Einzelne offene Hindernisse bleiben Befunde; bei unklarem Einfluss keine positive Bedienbarkeitsaussage. Kein Effekturteil aus Gesprächsfeedback. |
| TEACH-Zeit | Fünf Termine jeweils höchstens 45 Minuten, alle Kernhandlungen/Revision/Sicherung tatsächlich enthalten, Segmentzeiten plausibel oder Gesamtzeit mit nachvollziehbarer Abdeckung belegt | Auslassung/Mehrzeit → Entwurf nacharbeiten. Unbekannte Zeit → nicht beurteilbar. Keine 270-Minuten-Ersatzbestätigung. |
| TEACH-Prozess | OBS-01–12 für die definierte Sichtung jeweils B, eigene digitale P3-Beiträge tatsächlich sichtbar, kein widersprechender Gegenbefund; Hilfesituation und Abrufabstand offengelegt | T/N → Nacharbeit/Nachsicherung mit erneuter eigener Anwendung; U → nicht beurteilbar. Alle B bedeuten nur begrenzte Prozessbeobachtung, keine klassenweite Kompetenzquote. |
| REVIEW | Nach Überarbeitung vollständiger Bestätigungslauf in anderer Klasse mit zugehöriger TECH-Prüfung; tatsächliche Rollen-/Datenentscheidungen dokumentiert; Grenzen aller Achsen ausdrücklich benannt | Exploration allein → Überarbeitung/Bestätigung vorbereiten. Fehlende Erlaubnisse schließen jeden realen nächsten Einsatz aus. |

Zusammenfassende Kategorien für die menschliche Arbeitsentscheidung: `revise-required`, `not-evaluable`, `ready-for-human-review`. Rangfolge für **reale** Unterlagen: beobachteter wesentlicher Fehler → Nacharbeit; sonst fehlende/inkonsistente Pflichtbelege → nicht beurteilbar; erst danach vollständig positive begrenzte Befunde → menschliches Review möglich. Für **synthetische** Unterlagen gilt ausschließlich `synthetic-only` für die reale Verwendbarkeit, unabhängig vom simulierten Ergebnis.

Auch `ready-for-human-review` hat stets `authorizesUse: false`, `authorizesPublication: false` und `effectClaimAllowed: false`. Es ändert weder Modulstatus noch Curriculumabdeckung, Gerätestatus oder aktive Baseline. Eine tatsächliche spätere Statusänderung benötigt eigene, sachlich passende Belege und eine explizite Entscheidung.

## 3. Widersprüche und fehlende Beobachtung

Bei uneiniger Bewertung die Anker am tatsächlich gesichteten Produkt erläutern, ohne neue Produktkopie anzulegen. Kann der Befund nicht nachvollzogen werden, `U` setzen und gezielt neu beobachten. Bei unbekannter Unterstützung keine Eigenständigkeit vermuten. Ein Musterlösungsbeitrag kann korrekt sein und dennoch den eigenen P3-Nachweis verfehlen. Wenn nur Papier verwendet wurde, bleiben andere fachliche Beobachtungen erhalten, ALG-005 aber offen.

Wiederaufnahme eines Dossiers belegt keinen erfolgreichen Abruf. P4 nach vorher geöffneter Lösung wird nicht als zeitversetztes Erinnern gewertet. Späterer Abruf allein zeigt zudem keinen langfristigen Lerngewinn. S4 trägt eine Transferbeobachtung im definierten Modell, keine generelle Transferfähigkeit. P6 zeigt begrenzte Systemeinordnung, kein Verständnis aller realen Systemalgorithmen.

Keine Vorher-nachher-Effektgröße aus P0/P4 bilden: Aufgaben, Zeitpunkte und Hilfekontexte sind dafür nicht standardisiert; die Antworten werden nicht gesammelt. Auch zwei Klassen ohne Vergleichsdesign, geeignete Lernmaße und entsprechende methodische Prüfung belegen keine kausale Wirkung. Ein solcher Forschungsauftrag wäre eine andere Aufgabe.

## 4. Entscheidungsbogen

| Feld | Auszufüllen in der privaten Reviewkopie |
| --- | --- |
| Identität | Modul/Protokoll/Materialien/Git-SHA/Builddigest und tatsächlich geprüfter Umfang |
| Evidenzart | synthetisch / reale Technik / reale Nutzung / realer Unterricht; niemals unmarkiert mischen |
| Rollen und Unabhängigkeit | Wer hat unterrichtet, beobachtet, technisch/fachlich geprüft und entschieden? Rollenüberschneidungen benennen. |
| TECH | Ergebnis, fehlende Profile, offene TECH-F01–F08 und Nachprüfung |
| USE | Beobachtete Zugänge, offene sachliche Hindernisse, Grenzen der Auswahl |
| TEACH | Zeit je Termin, ausgefallene Handlungen, OBS-Kategorien, eigener P3-Code, Hilfen, Abrufabstand, Rückfallgrenzen |
| Daten/Rechte | Freigabereferenzen, absolute Löschtermine, Löschkontrolle, offene externe Kopien/Logs |
| Gegenbefunde | Widersprüche und nicht erklärbare Abweichungen; keine Glättung zur Gesamtampel |
| Arbeitsentscheidung | Nacharbeit / nicht beurteilbar / bereit für menschliche Folgeprüfung |
| Nächster Schritt | Genau abgegrenzter Auftrag, zuständige Rolle, erforderlicher Nachweis; keine automatische Ausführung |
| Geltungsgrenze | Nur geprüfte Revision, Variante, Zugänge und Kontexte; keine Wirkung, Repräsentativität oder Vollabdeckung behaupten |

Ein bereinigter Entwicklungsvermerk für Repo/Vault enthält nur Versionen, sachliche Befunde, Maßnahmen, Grenzen und Entscheidungsreferenz. Die Schule prüft vor Weitergabe, ob auch diese Angaben im Kontext zuordenbar sind. Falls ja, bleibt der Vermerk privat. Reale Paketdateien gehören nicht in diesen Workspace.

## 5. WU- und LXF-Selbstreview dieses Entwurfs

| Prüfaspekt | Im Instrument enthalten | Noch praktisch zu prüfen |
| --- | --- | --- |
| Kognitive Aktivierung / Aufgabenqualität | Vorhersage, erste Abweichung, eigener Code, begründete Revision, neue Zustandsbedingung | Eigene Denkhandlung bei realen Lernenden |
| Konstruktive Unterstützung | Hürdenbezug, H1–H4, fachliche/Bedienhilfe getrennt, eigene Weiterhandlung | Verständlichkeit, Dosierung, Rücknahme |
| Klassenführung / Zeit | Fünf echte 45-Minuten-Budgets, vorhandene Fenster, separate Erwachsenenzeit | Beobachtungsaufwand und tatsächlicher Stundenverlauf |
| Formatives Feedback | Produktanker und unmittelbarer nächster Schritt; keine Personenurteile | Rückmeldung verstanden und genutzt |
| Kooperation | Beide erklären, Rollenwechsel, gemeinsames Kriterium, Kontrolle nach etwa 5 Minuten und eigene Revision | Tatsächliche Verantwortlichkeit, Ersatzweg offen markieren |
| Diagnose-Fallback | Ersatzdiagnose bei fehlendem P0/P2/P4; kein Rückschluss aus Dateiwiederherstellung | Passung zum realen M01-Stand |
| Sprache/Zugang | Mündliche oder zugängliche Erklärung, Text-/Printalternative, Bedienprobleme getrennt | Echte Eingabe-/Assistenzprofile und eigene Programmierung |
| Evidenz und Schutz | Vier Pfade, explizite Nichtdurchführung, begrenzte Sichtung, getrennte Datenwege | Institutionelle Entscheidungen und tatsächliche Löschung |

WU-Grundlage: gelesene lokale Exzerpte der IBBW-Bände **1, 4 und 5** (Angebot/Nutzung, Kooperation, formatives Feedback). Sie liefern eine Planungsfolie, keine Wirksamkeitsbestätigung dieses Pakets. Das projektspezifische LXF-Profil und die zwölf Experience-Gates werden in `protocol.json` einzeln gebunden. KI-Dokumentenselbstreview durch den Autor; kein unabhängiger Review und keine neue Quellenabnahme.
