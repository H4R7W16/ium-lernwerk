# LXF06 Reviewbogen für Lernenden- und Lehrkraftperspektive

**Vorlagenstatus:** `working`. **Ausfüllstatus:** nicht ausgefüllt; keine Prüfung oder Freigabe wird durch diese Vorlage behauptet.

Dieser Bogen dient dem fachlichen Vorproduktionsreview. Er kann nach Kopie an einem konkret benannten Artefakt ausgefüllt werden. Gatedefinitionen stehen in [experience-gates.json](experience-gates.json), Orchestrierungsanforderungen in [teacher-orchestration.md](teacher-orchestration.md).

## 1. Auftrag und prüfbarer Stand

| Feld | Eintrag bei Durchführung |
|---|---|
| Reviewdatum | Auszufüllen. |
| Reviewer und verantwortliche Rolle | Auszufüllen; Rolle aus `ownerRole` der betreffenden Gates zuordnen. |
| Art der Beteiligung | Menschlicher Review / KI-gestützter Dokumentenreview / technische Prüfung ausdrücklich unterscheiden. |
| Unabhängigkeit | Selbstreview oder unabhängige Gegenprüfung; keine Unabhängigkeit ohne entsprechenden Ablauf behaupten. |
| Artefakt und Pfad | Auszufüllen. |
| Vollständiger Git-Commit | Vollständiger 40-stelliger SHA des geprüften Standes. |
| Branch und lokale Abweichungen | Branch; bei uncommittetem Material zusätzlich exakten Diff oder Dateihashes sichern. Ein Basiscommit allein identifiziert Änderungen nicht. |
| Jahrgang, curricularer Scope, Lernfunktion | Auszufüllen; keine reale Lerngruppe oder Durchführung erfinden. |
| Prüfgegenstand | Vertrag / neutraler Walkthrough / späteres konkretes Material, jeweils ausdrücklich benennen. |
| Vorliegende Voraussetzungen | Freigegebene Quellen-, Claim-, Prinzipien- und Patternstände sowie offene Randbedingungen. |

## 2. Lernendenperspektive

An der konkreten Fundstelle festhalten, welche Information eine lernende Person benötigt, welche eigene Handlung sie ausführen soll und woran deren fachliche Qualität sichtbar wird. Eine Perspektivübernahme durch Reviewer ist keine Beobachtung realer Lernender.

| Prüffrage | Fundstelle, Beleg und Unsicherheit |
|---|---|
| Sind Ziel, Zweck und erste Handlung erkennbar? | Auszufüllen. |
| Bleiben zusammengehörige Repräsentationen und Zustände verständlich verbunden? | Auszufüllen. |
| Erhält Hilfe die eigene Kernhandlung und ist eine Rückkehr zur selbstständigen Bearbeitung möglich? | Auszufüllen. |
| Verbindet Rückmeldung Produktstelle, Kriterium und nutzbaren nächsten Schritt? | Auszufüllen. |
| Bleiben Arbeitsstand, offene Frage und Wiederaufnahmeweg unterscheidbar? | Auszufüllen. |
| Erhält ein Alternativpfad Kernhandlung und Anspruch? | Auszufüllen. |
| Besteht ein Weg ohne persönliche Offenlegung, Bloßstellung oder zeitkritische Bedienung? | Auszufüllen. |

## 3. Lehrkraftperspektive

| Prüffrage | Fundstelle, Beleg und Unsicherheit |
|---|---|
| Sind Voraussetzungen, Material, Geräte-/Bedienroutinen und Hilfewege vorab prüfbar? | Auszufüllen. |
| Welche Produktlagen steuern die Wahl zwischen Exploration, Modellierung und eigener Anwendung? | Auszufüllen. |
| Wo liegen Haltepunkte und welche Anschlussentscheidungen ermöglichen sie? | Auszufüllen. |
| Ist Kooperation begründet; sind individuelle Beiträge, Minimalprodukt, Zwischenkontrolle und Zusammenführung sichtbar? | Auszufüllen oder begründen, warum keine kooperative Variante vorgesehen ist. |
| Bleiben Übung, Feedbacknutzung, Sicherung und Puffer in den tatsächlichen Zeitvarianten erhalten? | Auszufüllen. |
| Was geschieht bei fehlendem Ergebnis, Partnerausfall, technischem Verlust oder ungleichwertigem Zugang? | Auszufüllen. |
| Welche reale Nutzungs- oder Unterrichtsprüfung steht noch aus und wer verantwortet sie? | Auszufüllen. |

## 4. Gateprotokoll

Für jedes Gate eine begründete Entscheidung treffen: `not-run`, `pass` oder `fail`. Die Ausgangswerte unten sind **nicht durchgeführt**. Alle zwölf Gates sind Pflichtgates des Vorproduktionsreviews; kein pauschales „nicht anwendbar“ darf ein Gate überspringen. Einzelne bedingte Anforderungen können mit fachlicher Begründung nicht zutreffen, beispielsweise Kooperation bei bewusst individueller Arbeit. Diese Begründung gehört in den Nachweis.

| Gate-ID | Entscheidung | Nachweis und Fundstelle | Tatsächlich angewandte Methode / Rolle | Offene Frage oder Nacharbeit |
|---|---|---|---|---|
| evidence-integrity | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| goal-action-evidence-alignment | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| cognitive-economy | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| disciplinary-learning-action | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| representation-coherence | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| support-without-task-removal | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| feedback-and-next-action | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| orientation-and-recovery | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| accessibility-and-equivalence | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| teacher-orchestration | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| privacy-and-emotional-safety | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |
| pilot-boundary | not-run | Auszufüllen. | Auszufüllen. | Auszufüllen. |

Jeder `pass` muss die konkrete `passCondition` der Gatedefinition belegen. Jede `fail`-Entscheidung benennt erforderliche Änderung, verantwortliche Rolle, Wiederprüfung und die entsprechende `failAction`. Ein leerer Beleg oder reines automatisches Testergebnis schließt kein didaktisches Gate. Aussagen wie „wirkt verständlich“ oder „alle Tests grün“ ersetzen keine fachliche Fundstelle.

## 5. Neutrale Walkthroughs und offene reale Prüfungen

| Walkthrough-ID | Dokumentenprüfung und Gegenfall | Beobachteter Beleg | Ergebnis / erforderliche Änderung |
|---|---|---|---|
| entry | Ausgangsprodukt vorhanden versus fehlend/mehrdeutig. | Auszufüllen. | Auszufüllen. |
| central-learning-action | Hilfe führt zu Eigenleistung versus übernimmt sie; Kooperation macht Beiträge sichtbar versus verdeckt sie. | Auszufüllen. | Auszufüllen. |
| securing-and-reentry | Gesicherter Stand versus verlorenes Ergebnis; aktiver Abruf versus Wiederlesen. | Auszufüllen. | Auszufüllen. |

Den Gegenfall am Entwurf durchspielen: Führt er zu einer eindeutigen Umsteuerung oder bleibt der nächste Schritt unklar? Das Vorhandensein einer Tabelle allein reicht nicht.

| Späterer Nachweis | Warum hier noch nicht ausführbar? | Auslöser und verantwortliche Rolle | Aktuelle Aussagegrenze |
|---|---|---|---|
| Tatsächliche technische Funktion / Accessibility am Produkt | Auszufüllen. | Auszufüllen. | Keine technische Konformitätsaussage aus dem neutralen Entwurf. |
| Reale Nutzungsprüfung | Auszufüllen. | Auszufüllen. | Kein Nachweis beobachteter Lernendenreaktionen. |
| Unterrichtspilot | Auszufüllen. | Auszufüllen. | Pilot bleibt `not-started`. |
| Wiederholte Bewährung / Lernwirkung | Auszufüllen. | Auszufüllen. | Kein Standard- oder Wirkungsnachweis. |

Eine fehlende Pflichtfunktion des aktuellen Entwurfs darf nicht als bloß „späterer Nachweis“ ausgelagert werden. Beispiel: Eine Alternative mit entfernter Kernhandlung fällt bereits im Dokumentenreview durch. Eine funktional schlüssig geplante Alternative besitzt dagegen noch keinen technischen Implementierungsnachweis.

## 6. Gesamtentscheidung und Freigabegrenze

- **Ergebnis des durchgeführten Reviews:** Auszufüllen; bei jedem offenen oder fehlgeschlagenen Pflichtgate bleibt die fachliche Weitergabe blockiert.
- **Begründung mit entscheidenden Belegen:** Auszufüllen.
- **Verbleibende Unsicherheiten:** Auszufüllen, einschließlich Reichweite und zuständiger Rolle.
- **Erforderliche Änderungen und Wiederprüfung:** Auszufüllen; andernfalls ausdrücklich „keine im geprüften Umfang“ mit Begründung.
- **Prüfbare Folgeaktion:** Auszufüllen. Ein vollständig belegter Vorproduktionsreview wird LXF07 vorgelegt; er vergibt dessen Freigabe nicht selbst.
- **Nutzerentscheidung zu LXF06:** Auszufüllen, mit Datum und dokumentierter Entscheidung. Ohne diese Entscheidung bleibt LXF07 geschlossen.

**Verbindliche Aussagegrenze:** Aus diesem Review folgt keine Aussage über Lernwirksamkeit. Ein Dokumentenreview, technischer Test oder Usabilitybefund ersetzt weder einen Unterrichtspilot noch einen belastbaren Wirkungsnachweis. Pilot bleibt `not-started`, Standardisierung unzulässig und Inhaltsproduktion `frozen`, bis die jeweiligen gesonderten Gates geöffnet werden.

## 7. Schutz der Beobachtungsdaten

Der Bogen erfasst Reviewerrollen, Artefakte und Aufgabenmerkmale. Keine Namen, Kennungen, privaten Medienerfahrungen, Klickverläufe oder individuellen Hilfenutzungs-/Zeitprofile von Lernenden eintragen. Für später tatsächlich erhobene Nutzungs- oder Pilotdaten gelten die gesonderten Governance- und Pilotierungsentscheidungen; diese Vorlage schafft keine Datenerhebungsfreigabe.
