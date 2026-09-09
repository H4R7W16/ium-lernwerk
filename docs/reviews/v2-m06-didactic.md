# V2-M06 – didaktischer Integrationsreview

Stand: 9. September 2026. Dies ist ein strukturierter Autorenreview des Entwicklungskandidaten, kein Schlussreview und keine Erprobung mit Lernenden.

## Curriculumrecords

| Record | Umsetzung im Kandidaten | Grenze |
| --- | --- | --- |
| BMB16-GYM-PK-SK-001 | P1/P2/P3/P5 verlangen sachlich richtige Fachbegriffe bei Darstellung, Revision, Code und Transfer. | Querschnittliche Erwartung; M06 belegt keine Erfüllung für das ganze Jahr. |
| LH26-E-ALG-001 | P6: algorithmischen Prozess aus Funktions-/Systembeschreibung erkennen und begründen. | Bloße Appnamen oder digitale Bilder reichen nicht. |
| LH26-E-ALG-002 | P1/P3: eindeutige Vorschrift mit Start und Reihenfolge erläutern. | Das Fahrziel allein reicht nicht. |
| LH26-E-ALG-003 | P1/P3: grafische Befehlsdarstellung erklären und ausführen. | Ortslinie, fertige Animation oder kopierte Blöcke allein reichen nicht. |
| LH26-E-ALG-004 | P2/P3/P5: Einzelanweisung, ganzen Körper und konstante Anzahl beschreiben. | Nur eine Anzahl zu ändern reicht nicht. |
| LH26-E-ALG-005 | P3: persönlich editierte ausführbare Anweisungen und feste Schleife in geeigneter Sprache. | Papierausführung, Codebild oder Lehrkraftlauf reichen nicht. |
| LH26-E-ALG-006 | P2/P3: relevante Codeabschnitte schrittweise analysieren, Wirkung und erste Abweichung erklären. | Endposition oder Fehlersymbol allein reichen nicht. |

Korrektur F04 vom 09.09.2026: Die Recordzuordnung folgt Abschnitt 4 des angenommenen [M06-Designs](../superpowers/specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md). Alle sieben Records bleiben `unassessed`; dies ist eine Zuordnung vorgesehener Lernnachweise, keine beobachtete Curriculumabdeckung. Die frühere falsche Zuordnung bleibt in der Git-Historie und im datierten NA07-Review nachvollziehbar.

## Produkte P0–P6

| Produkt | Verbindung | Status |
| --- | --- | --- |
| P0 frühe Vorhersage | Feld vor Ausführung; flüchtig und nicht exportiert | synthetisch geprüft |
| P1 eigene Grafik | unabhängiger Grafikeditor mit Erklärung | synthetisch geprüft |
| P2 Revision | Vorher/Nachher, Spurstellen und erste Abweichung | synthetisch geprüft |
| P3 eigener Code und Beleg | fünfteiliger Körper, zehnteilige Spur und laufgebundene Begründung | Ausführung, Übernahme, Export, Import, Reload und Offlinewiedereinstieg synthetisch geprüft |
| P4 Abruf | eigener Abruf vor alter Lösung; flüchtig | synthetisch geprüft |
| P5 Transfer | aufnehmen–prüfen–ablegen plus Zustandsbegründung | Material-/UI-Anker geprüft |
| P6 Systeme | Zeit, Route und Grenze von Papier/Standbild getrennt | Material-/UI-Anker geprüft |

## Materialien MAT-01–10

Materialgenaue Zuordnung nach `modules-v2/V2-G5-M06/content.json` (F04-Korrektur vom 09.09.2026):

| Material | Auftrag / Produkt |
| --- | --- |
| MAT-01 `start` | Einstieg und frühe Vorhersage P0 |
| MAT-02 `legend` | Befehlslegende |
| MAT-03 `worked-example` | S1 und eigene Grafik P1 |
| MAT-04 `revision` | S2 und Revision P2 |
| MAT-05 `own-program` | S3 und eigener Code P3 |
| MAT-06 `helps` | Hilfen H1–H4 |
| MAT-07 `return-and-retrieval` | Rückkehr und Abruf P4 |
| MAT-08 `transfer-and-systems` | Transfer P5 und Systeme P6 |
| MAT-09 `handbook` | Lehrkrafthandbuch |
| MAT-10 `learner` | Druckfassung |

Zehn Materialien plus Briefing bilden elf Materialrouten im 225-Minuten-Entwurf. Die A4-Fassung unterstützt Planung und Dokumentation; ALG-005 benötigt zusätzlich selbst eingegebenen ausführbaren Code.

## Zwölf LXF-Gates

| Gate | Kandidatenbeleg | Reale Grenze |
| --- | --- | --- |
| evidence-integrity | Registry-SHA, Materialrevision, getrennte synthetische Evidenz | unabhängiges Review offen |
| goal-action-evidence-alignment | Auftrag, Code, Trace und Zielprüfung greifen ineinander | Lernwirksamkeit offen |
| cognitive-economy | drei Arbeitsbereiche, kompakte Befehlslegende, situative Hilfen | Belastung nicht beobachtet |
| disciplinary-learning-action | Vorhersagen, ausführen, prüfen, revidieren, begründen | reale Lernhandlungen offen |
| representation-coherence | Grafik und Code teilen Semantik, bleiben als Produkte getrennt | Missverständnisse offen |
| support-without-task-removal | H1–H4 geben Hinweise ohne Lösungsvorgabe | Hilfenutzung offen |
| feedback-and-next-action | Zielmeldung, erste Abweichung und Rückkehrnotiz | Qualität der Anschlussaktion offen |
| orientation-and-recovery | Navigation, Speicherstatus, offener Punkt, nächste Handlung, Importvorschau und beschädigte lokale Stände | reale Recoveryablage offen |
| accessibility-and-equivalence | Tastatur, Touch, Text, Reflow, Axe und 44-px-Inventar in drei Browsern synthetisch geprüft | assistive Realprüfung offen |
| teacher-orchestration | Handbuch und Briefing binden fünf Termine und Entscheidungspunkte | Lehrkraftnutzung offen |
| privacy-and-emotional-safety | P0/P4 flüchtig, keine Telemetrie, bewusster Export | schulischer Datenbetrieb offen |
| pilot-boundary | Kandidatenhinweis und geschlossene Reifeachsen sichtbar | Pilot nicht begonnen |

## Drei Informationsbereiche

1. **Auftrag und Beispiel** hält Auftrag, Hilfen und Abruf vor der alten Lösung zusammen.
2. **Mein Prüfdossier** verbindet eigene Grafik, eigenen Code, Vorhersage/Spur, Revision, Transfer und Systeme.
3. **Sicherung und Rückkehr** macht Speicherstatus, offenen Punkt, nächste Handlung und Datenverwaltung sichtbar.

## Reviewurteil

Die geplante didaktische Struktur ist im Kandidaten vollständig auffindbar und synthetisch bedienbar. P0–P6, S0–S5, MAT-01–10 plus Briefing, Import/Recovery, Offlinewiedereinstieg und die zugänglichen Bedienpfade sind technisch belegt. NA07 dokumentiert die fünf anschließend mit NA08 beauftragten Korrekturen; reale Nutzungsbeobachtung, Curriculumfreigabe, assistive Zielgeräte, Schulnetz/LMS und Pilotierung wurden nicht durchgeführt.
