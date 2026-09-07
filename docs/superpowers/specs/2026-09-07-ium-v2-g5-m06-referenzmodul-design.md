# V2-G5-M06 – Referenzmodul „Präzise Abläufe entwickeln und prüfen“

**FU-MOD · 7. September 2026 · Design zur Nutzerabnahme (`review`).**

Dies ist die neue Spezifikation eines Referenzmoduls für Gymnasium Baden-Württemberg, Klasse 5, Niveau E. Der Lernkontext heißt **„Prüffahrt im Raster“**. Die Modulauswahl ändert weder die freigegebene R5-Unterrichtsreihenfolge noch deren Schwerpunkt Medienbildung. Das Modul bleibt dort M06 mit Voraussetzung M01. „Erstes Referenzmodul“ bezeichnet die Entwicklungsreihenfolge.

Auftrag: „Das ist angenommen. Führe jetzt IUM-V2-FU-MOD aus.“ FU-TECH wurde damit als Audit an Commit `69634c56d3d100d3bf33632f29a4f98eaf579276` angenommen. Seine acht technischen Befunde bleiben offen. V2 ist Planungs-/Entwicklungsbaseline; V1 bleibt Produktstand. Dieses Design enthält interne Prüffälle und Produktionsanforderungen, keine ausgearbeitete Lernumgebung, keine Lernmaterialproduktion und keinen Implementierungsplan. Pilot, LXP05-Integration und Veröffentlichung bleiben geschlossen.

Die ergänzende [Spezifikationsbindung](../../../roadmap/v2/follow-ups/reference-module/specification.json) hält Curriculum, Minuten, LXF-Ableitungen und Übergabegates maschinenlesbar fest. Sie ist kein Produktmanifest und wird von keiner Modulregistry geladen. [Prüfbericht](../../../roadmap/v2/follow-ups/reference-module/validation-report.md) und [Einstieg](../../../roadmap/v2/follow-ups/reference-module/README.md) führen den tatsächlichen Prüfstand.

## 1. Auswahl und Vorrang

| Kandidat aus R5 | Eignung als erste Referenz | Abwägung |
| --- | --- | --- |
| M01 – Schulischer Arbeitsraum, 180 Minuten | Grundlegender Einstieg; reale Geräte-, Datei- und Zugangshandlungen | Benötigt früh einen bestimmten schulischen Zugang und echte Ablagewege. Eine neutrale Simulation würde zentrale Nachweise verfehlen. Bleibt erstes Unterrichtsmodul. |
| M04 – Medienprodukt, 315 Minuten | Breite Verbindung aus Recherche, Gestaltung, Kooperation, Rechten und Revision | Hängt fachlich an M02/M03 und einem konkreten Werkzeug-/Quellenpaket. Für den ersten abgegrenzten Referenzentwurf zu viele gleichzeitig neue Voraussetzungen. |
| **M06 – Präzise Abläufe, 225 Minuten** | Klar prüfbare Beziehung zwischen Darstellung, Code, Zustand, Rückmeldung und eigener Revision | Gewählt, weil der LXF-Vertrag hier an kleinen Produkten und Störfällen konkret prüfbar wird. Die vorhandene Semantik reduziert technische Ungewissheit; sie bestimmt weder Kontext noch Aufgabenfolge. |

Auch innerhalb M06 wurden drei Wege abgewogen: Ein rein manueller Ablaufkurs trägt das Programmieren nicht vollständig. Eine externe freie Programmierumgebung wäre möglich, bringt aber zusätzliche Bedien-, Rechte- und Betriebsentscheidungen mit. Gewählt wird als **Designziel ein kleiner statischer Arbeitsraum mit einer blockartig dargestellten, ausführbaren Befehlssprache und gleichwertigen manuellen Spuren**. Seine tatsächliche Eignung als Programmiersprache und sein funktionaler Zugang müssen am späteren Produkt geprüft werden. Vor diesem Nachweis bleibt ALG-005 offen.

Vorrang: ausdrückliche Nutzerentscheidungen → aktive V2-Baseline → CUR/SRC und R5 → LXF03–07 und GOV → angenommener FU-TECH-Audit → dieses noch nicht angenommene Design. IUM16, IUM18 und LXP02 sind begrenzt geprüfte V1-Eingaben. Alte Coverage, elf Pflichtphasen, 270-Minuten-Erweiterung und alte Gate-A-Freigaben gelten hier nicht.

## 2. Planungsanker und reale Voraussetzungen

R5 weist M06 fünf Einheiten à 45 Minuten zu, aufgeteilt in 35 Minuten Orientierung/Erklärung, 55 angeleitete Übung, 60 eigene Anwendung, 40 Feedback/Revision und 35 Sicherung/Transfer. Diese Projektkalkulation wird unten neu auf Aufgaben verteilt; die gleiche Gesamtsumme wie bei IUM16 begründet keine Übernahme seines Zeitvertrags.

Planungsannahme ist eine Klasse 5 mit unterschiedlichen Lese-, Raumvorstellungs- und Bedienroutinen. Es liegen **keine reale Klasse, durchgeführten Vorgängerstunden, Schülerprodukte oder bestätigten Geräte vor**. M01 ist geplante Voraussetzung, kein beobachtetes Vorwissen. Ein eigenständiges IuM-Fachprofil liegt im allgemeinen Vault-Profilordner nicht vor; dort existiert nur das Geschichtsprofil. Fachliche Grundlage sind deshalb CUR/R5 und das geprüfte projektspezifische LXF-Profil. Das V1-Fachprofil wird nicht stillschweigend wieder zur Autorität.

Vor konkreter Produktion/Einsatz klärt die verantwortliche Lehrkraft mit Jan: tatsächliche Termine und 45-Minuten-Budgets, Fach-/Sprachzugänge, Geräte pro Person, Eingabehilfen, schulischer Kanal und Speicher-/Profilmodell. Für dieses Design gilt als Standard **ein Gerät pro Person**, vorübergehender Partnervergleich und eigenes Produkt. Bei einem Gerät pro Paar werden Bedienrollen gewechselt und beide programmieren einen eigenen Abschnitt; reicht die Zeit dafür nicht, bleibt der individuelle digitale Nachweis offen. Kein Loginsystem oder LMS ist zum fachlichen Kern nötig.

## 3. Ziel, Sinn und Produkt

Leitfrage: **Wie lässt sich eine wiederholte Prüffahrt so beschreiben, dass wir ihren Ablauf vorhersagen, ausführen und begründet verbessern können?**

Lernende sollen eine präzise Anweisung von einer unbestimmten Absicht unterscheiden, einen grafischen Ablauf mit ausführbarem Code verbinden, eine feste Wiederholung als Wiederholung des **gesamten Körpers** erklären und einen Fehler an der frühesten relevanten Abweichung prüfen. Eine begründete Lösung benennt Startzustand, Wirkung der Anweisungen, Schleifenkörper/-anzahl und Grenzen des Modells.

Die eigene Denkhandlung ist nötig, weil der sichtbare Endzustand mehrere Ursachen haben kann. Ein Wagen kann zum Start zurückkehren und trotzdem die falschen Prüfpunkte besucht haben. Das Produkt muss die beabsichtigte Fahrt **mit einer Spur begründen**. KI-generierter Code oder eine automatisch abgespielte Lösung ersetzt weder eigene Vorhersage noch Erklärung; das Design enthält keine generative KI-Funktion.

Das zentrale Lernprodukt ist ein kleines **Prüfdossier**, kein unbeschränktes Portfolio. Es enthält folgende verbundene Spuren; kurze mündliche Erläuterungen am sachlichen Produkt sind zulässig, ohne Audioaufzeichnungspflicht:

| ID | Erzeugte Spur | Erwartung und Weiterverwendung |
| --- | --- | --- |
| P0 | Ausgangsvorhersage zu S0, mit einem Begründungsschritt | Diagnose für die nächste Erklärung. Ein unklarer Beitrag wird nachgefragt; er ist kein Personenurteil. Wird nicht dauerhaft für die Auswertung gesammelt. |
| P1 | Kommentierte grafische Befehlsfolge zum Beispiel S1 und eine selbst ergänzte Folge | Pfeile zeigen Ausführungsreihenfolge, ein Rahmen den ganzen Wiederholungskörper. Die Person erläutert und vollzieht mindestens einen selbst ergänzten Abschnitt. Ein bloßer Weg auf dem Raster reicht für ALG-003 nicht. |
| P2 | Begrenzter Vergleichs-/Revisionsbeleg zu S2 | Ausgangsprogramm, Vorhersage, erste Abweichung, begründete Änderung und erneute Spur. Gleicher Prüffall vor/nach Revision; Fehlermeldung und Ursache werden getrennt. |
| P3 | Eigener grafischer Entwurf und ausführbarer Code zu S3, Vorhersage, ausgewählte Laufspur, Begründung | Alle verlangten Prüfpunkte in Reihenfolge, Rückkehr und Blickrichtung stimmen; Code und Grafik bedeuten dasselbe. Feste Wiederholung wird tatsächlich verwendet und erklärt. Fachliche Qualität ist nicht identisch mit „Programm beendet“. |
| P4 | Aktiver Abruf einer gesicherten Schleifenbeziehung bei einem späteren Termin | Vor Anzeige der alten Lösung einen kurzen Körper entfalten und einen Zustand begründen. Sofort anschließende Nachklärung bei Lücke; kein dauerhaftes Kompetenzlabel. |
| P5 | Transferentscheidung zur Prüfstation S4 mit kurzer Zustandsspur | Neue Zustandsbedingung wird geprüft; eine ungeeignete Blockgruppierung wird erklärt und revidiert. Kein zusätzlicher praktischer Programmiernachweis. |
| P6 | Zwei begründete Systemzuordnungen plus eine benannte Erkenntnisgrenze aus S5 | Aus gegebenen Funktionsbeschreibungen einen wesentlichen algorithmischen Prozess identifizieren. Nicht aus einem Icon auf das ganze System schließen. In der Schlusssicherung verwenden. |

P1, P2, P3, P5 und P6 bilden das begrenzte Dossier. P0/P4 dienen der aktuellen Diagnose; nur die nötige nächste Handlung wird in der Rückkehrnotiz festgehalten. In einer gemeinsamen Gerätevariante bleiben eigene P1/P3-Beiträge getrennt zuordenbar, lokal ohne Namen oder Klassenkennung.

Qualitätsmaßstab: **präzise**, **zwischen Darstellungen konsistent**, **an der Spur geprüft**, **begründet revidiert** und **auf neue Bedingungen übertragen**. Kein Tempo-, Punkt-, Badge- oder Kürzestwegkriterium. Alle Aufgaben sind formative `learning-task`; P4/P5 beginnen ohne fachliche Lösungshilfe, bleiben jedoch Lernaufgaben. Hilfenutzung wird am Produktkontext geklärt, nicht benotet. Eine spätere Leistungsaufgabe bräuchte einen eigenen transparenten Vertrag.

## 4. Curriculum und Nachweisgrenzen

Die sieben ausgewählten Records sind genau die R5-M06-Zuordnungen. Alle bleiben `coverage: unassessed` und `evidenceStatus: planned-only`.

| Record | Bindung / Erfüllungsform | Konkret geplanter Nachweis | Nicht ausreichend |
| --- | --- | --- | --- |
| BMB16-GYM-PK-SK-001 | amtlich, querschnittlich | Fachbegriffe in P1/P2/P3/P5 sachlich richtig verwenden | Wortliste oder Abschluss allein; M06 erfüllt die querschnittliche Erwartung nicht für das ganze Jahr |
| LH26-E-ALG-001 | Orientierung 5/6, direktes Modul | P6: Prozess aus Funktionsbeschreibung erkennen und begründen | „Jedes digitale Bild ist ein Algorithmus“ oder bloße Namen von Apps |
| LH26-E-ALG-002 | Orientierung 5/6, direktes Modul | P1/P3: eindeutige Vorschriften samt Start und Reihenfolge erklären | Nur das Fahrziel nennen |
| LH26-E-ALG-003 | Orientierung 5/6, direktes Modul | P1/P3: grafische Befehlsdarstellung erläutern und ausführen | Unkommentierte Ortslinie, fertige Animation oder nur kopierte Blöcke |
| LH26-E-ALG-004 | Orientierung 5/6, direktes Modul | P2/P3/P5: Einzelanweisung, ganzer Körper und konstante Anzahl beschreiben | Nur eine Zahl am Wiederholungsblock ändern |
| LH26-E-ALG-005 | Orientierung 5/6, direktes Modul | P3: selbst editierte, tatsächlich ausführbare Anweisungen und feste Schleife in einer geeigneten Sprache | Papierausführung, Codebild oder Lehrkraftlauf; Sprache und zugänglicher Editor müssen praktisch geprüft werden |
| LH26-E-ALG-006 | Orientierung 5/6, direktes Modul | P2/P3: relevante Codeabschnitte schrittweise analysieren, Wirkung und erste Abweichung erklären | Nur Endposition oder rotes Fehlersymbol |

Keine zusätzlichen Klasse-7-Anforderungen, Beispiele oder Progressionsbeschreibungen werden als Kompetenzpflicht gezählt. Keine amtliche Aufteilung der Lesehilfe auf Klasse 5 und 6 wird behauptet. M06 löst keine der offenen Eigenbezugsfragen aus R5/CUR-Q-002; diese bleiben in anderen Modulen unverändert offen. M06 hat keinen eigenen fächerintegrativen Erfüllungsnachweis. Kooperation unterstützt hier die fachliche Arbeit und wird nicht als Erfüllung des digitalen Kommunikationsmoduls M03 verbucht.

Am 07.09.2026 wurde die [amtliche Fachseite](https://km.baden-wuerttemberg.de/de/schule/schulartuebergreifend/mint/schule-und-unterricht/informatik-und-medienbildung) erneut gelesen. Sie führt die bestehende Bildungsplangrundlage und die Lesehilfe als Übergangsorientierung fort. Die [Lesehilfe 2026/2027](https://km.baden-wuerttemberg.de/fileadmin/redaktion/m-km/intern/PDF/Dateien/Schulart%C3%BCbergreifend/MINT/2026_Lesehilfe_IuM_Gym_und_Sek_I_bf.pdf), S. 2–3 und 8–9, wurde inhaltlich für diesen Ausschnitt gegengeprüft, nicht erneut byteidentisch bestätigt. BMB-Sachkompetenz wurde anhand des versiegelten lokalen Records geprüft; der direkte Onlineabruf scheiterte. Das ist keine neue vollständige Quellenabnahme. Unveränderte Originaltexte, Fundstellen und Bindungsgrade stehen in den verknüpften Curriculumdatensätzen.

## 5. Fachlicher Modellvertrag und interne Prüffälle

Das Rastermodell kennt Ort und Blickrichtung. Spalten zählen von links, Zeilen von oben; `(2,3)` heißt Spalte 2, Zeile 3. `vor` verschiebt genau ein Feld in Blickrichtung, `links`/`rechts` drehen um 90 Grad am Ort. `wiederhole n [Körper]` führt den vollständigen nicht verschachtelten Körper genau n-mal aus. Die Entwurfsfälle nutzen Anzahlen 2–4. Der geprüfte V1-Parser erlaubt 2–9; dieser begrenzte Editorbereich und das technische Ausführungslimit von 100 Aktionen sind der Ausgangspunkt der späteren Anpassung, keine Altersregel. Der neue Modulvertrag benötigt Körper mit bis zu fünf Grundanweisungen; der V1-Parser erlaubt bislang nur vier. S3 ist in seiner kompakten Referenzform deshalb dort noch nicht ausführbar. Die Erweiterung auf fünf ist ein ausdrücklicher Anpassungsbedarf. Bedingungen, Variablen, Sensoren und verschachtelte Schleifen sind ausgeschlossen. Grenzen/Hindernisse stoppen mit unverändertem Zustand des fehlerhaften Schritts. Eine Schleifenklammer ist Kontrollstruktur, kein zusätzlicher Fahr- oder Drehschritt.

Eine Ablaufgrafik zeigt Start, geordnete beschriftete Anweisungen, zusammengehörigen Körper mit konstanter Anzahl und Ende. Eine lineare sprachliche Darstellung erhält Reihenfolge und Gruppierung. Diese Grafik wird vom Lernenden erklärt/ergänzt; eine automatisch aus Code erzeugte Grafik allein wäre kein Darstellungsnachweis. Die Laufspur führt Schritt, zugehörige Anweisung, gegebenenfalls Wiederholungsdurchlauf sowie Vorher-/Nachherzustand zusammen.

Die folgenden **neu entworfenen internen Testvektoren** machen Fachlichkeit prüfbar. Sie sind kein publiziertes Schülerpaket. Die Zahlen sind bewusst klein gewählte Designparameter, keine empirischen Altersgrenzen.

| Fall | Gegenstand / erwartete Beziehung | Prüfanker |
| --- | --- | --- |
| S0 – Richtung und Schritt | Raster 3×3, Start `(1,3)`, Nord. `vor; rechts; vor` | Zustände `(1,2)/N`, `(1,2)/O`, `(2,2)/O`. Drehung verändert den Ort nicht. Frühe Modellierung bei unsicherer Richtungsdeutung. |
| S1 – Ganzer Wiederholungskörper | Raster 4×4, Start `(2,3)`, Ost. `wiederhole 4 [vor; links]` | 8 Aktionen: `(3,3)` → `(3,2)` → `(2,2)` → `(2,3)` nach den Fahrten; am Ende wieder Ost. An einer neuen, angefangenen Grafik erklären/ergänzen, welche Anweisung als Nächstes kommt. |
| S2 – Gültiger Code, falsche Gruppierung | Gleicher Start wie S1. Fehlfassung `wiederhole 4 [vor]; links`; Bezug ist die beabsichtigte S1-Prüffahrt | Erste fachliche Abweichung bei Aktion 2: erneute Fahrt statt Drehung. Erst Aktion 3 würde die Grenze überschreiten. Körpergrenze begründet auf `[vor; links]` ändern, nicht bloß Zahl reduzieren. Erneut vom gleichen Start prüfen. |
| S3 – Eigene rechteckige Prüffahrt | Raster 5×4, Start `(1,3)`, Ost. Prüfpunkte in Reihenfolge `(3,3)`, `(3,2)`, `(1,2)`, `(1,3)`; Abschluss Ost, nur Randfahrt des Rechtecks | Ein Referenzweg: `wiederhole 2 [vor; vor; links; vor; links]`, 10 Aktionen. Eigener Entwurf ohne kompletten Lösungscode; gleichwertige korrekte Programme zulässig, feste Schleife obligatorisch. Nicht der kürzeste Code entscheidet. |
| S4 – Transfer zur Prüfstation | Ein ausdrücklich vereinfachtes neues Modell verarbeitet drei Werkstücke nacheinander: `aufnehmen` braucht freie Station, `prüfen` ein aufgenommenes Werkstück, `ablegen` ein geprüftes Werkstück und macht die Station frei | `wiederhole 3 [aufnehmen; prüfen; ablegen]` ist ausführbar. `wiederhole 3 [aufnehmen]; wiederhole 3 [prüfen]; wiederhole 3 [ablegen]` scheitert bei der zweiten Aufnahme. Körper, Reihenfolge und Anfangsbedingung begründen. |
| S5 – Systeme anhand ihrer Funktion einordnen | Neutrale Funktionsbriefe zu digitaler Zeitsteuerung und Wegberechnung; Vergleich mit einer auf Papier beschriebenen Vorschrift und einem isolierten digitalen Standbild | Bei Zeitsteuerung/Wegberechnung einen notwendigen Verarbeitungsablauf benennen. Papier kann eine algorithmische Vorschrift tragen, ist aber kein digitales System. Aus dem Standbild allein lässt sich die wesentliche Funktionsweise des Gesamtsystems nicht bestimmen. |

S4 ist Transfer, weil eine neue Zustandsabhängigkeit (frei → belegt → geprüft → frei) statt räumlicher Orientierung die Ausführbarkeit bestimmt. Die Person muss das Körperprinzip auf andere Aktionen und deren Voraussetzungen übertragen. Kein bloßer Farb-, Zahlen- oder Oberflächenwechsel. Das manuelle Transferprodukt belegt keinen neu programmierten Prüfautomaten. S5 ist begrenzte Modell-/Systemeinordnung, kein detaillierter Nachweis realer Such-, Navigations- oder KI-Algorithmen.

Die V1-Lieferszenarien `worked-sequence`, `error-*`, `product-a/b/c`, `repair-standard` und `extended-inherited` werden **nicht** als V2-Material übernommen. Ihr technischer Wert liegt in Prüfmustern für Zustände, Befehlsreferenzen und Fehler. S0–S5 wurden unabhängig für die neue Körper-/Zustandsbeziehung entworfen; es werden keine alten Szenario-IDs umetikettiert.

## 6. Materialumfang und Ausdruckswege

Die Materialliste begrenzt den späteren Produktionsauftrag. Alle Positionen sind `specified-not-produced`; nur die internen Vektoren oben sind vorhanden. Eigenentwürfe sind als solche zu kennzeichnen, Curriculumszitate bleiben Lehrkraftreferenz. Fremde Illustrationen, Markenfiguren, Accounts, Video- oder Linkrecherchen sind für den Kern nicht nötig.

| Material-ID | Erforderlicher Umfang | Lernfunktion, Verwendung und Grenze |
| --- | --- | --- |
| MAT-01 | Eine kurze Auftaktkarte mit S0 und erster Handlung | Ziel/Diagnose, gemeinsam gesprochen oder gelesen. Ein Arbeitsauftrag statt mehrerer Vorspannseiten. |
| MAT-02 | Eine wiederverwendbare Befehls-/Zustandslegende | Fachbegriffe direkt am Beispiel. Zunächst Schritt/Drehung/Zustand, danach Schleife/Körper/Anzahl/Spur; keine vorausgesetzte Glossarlektüre. |
| MAT-03 | Ein segmentiertes S1-Beispiel mit zwei Verarbeitungsstopps | Vorhersagen/Zuordnen vor vollständiger Lösung, danach eigener Ergänzungsschritt. Lehrkraft hat vollständige Lösung und typische Fehlwege. |
| MAT-04 | Eine S2-Fehlfassung und ein Vergleichs-/Revisionsfeld | Ein verpflichtender Fehlerfall genügt; Fehlervarianten nur bei diagnostiziertem Bedarf innerhalb derselben Zeit. |
| MAT-05 | Eine S3-Auftragskarte und ein kleines Dossiergerüst | Eigene Grafik/Code, eine Vorhersage, eine ausgewählte Spur und eine kurze Begründung. Kein Protokoll aller Versuche. |
| MAT-06 | Drei punktuelle Hilfen H1–H3 plus Eingabe-/Sprachhilfe H4 | Auf Wunsch oder produktbezogen empfohlen; nicht als verpflichtende Hilfenseitenfolge. |
| MAT-07 | Eine Rückkehrkarte mit Stand/offenem Punkt/nächster Handlung; eine verdeckt gehaltene Abrufaufgabe | Arbeitswiederaufnahme und Abruf trennen; alte Lösung erst nach Abruf anzeigen. |
| MAT-08 | Ein S4-Kontrast mit Zustandslegende; vier kurze S5-Funktionsbriefe | Transfer und Systemeinordnung. S5-Briefe als zusammen betrachtbarer Kontrast, keine vier Rechercheaufträge. |
| MAT-09 | Lehrkrafthandbuch mit Kurzstart, Ablaufvarianten, erwarteten Spuren, Hilfe-/Störfallentscheidungen und Quellen-/Rechteverzeichnis | Vollständige Referenzlösungen sind klar von Lernendenansichten getrennt; kein Sicherheitsversprechen durch bloßes Verstecken im statischen Bundle. Vorlesbares Kurzbriefing; Audio wäre nur eine spätere alternative Ausspielung mit gleichem Text. |
| MAT-10 | Zugängliche Print-/Textfassungen der nötigen Grafiken, Karten und Dossierfelder | Gleiche Körper-/Zustandsbeziehung und Kriterien. Algorithmische Handlungen bleiben möglich; echtes Programmieren wird bei Ausfall später nachgeholt. |

Schreiblast: kurze Markierung, kleine Zustandstabelle und in der Regel ein bis zwei Begründungssätze pro Entscheidung; dies ist eine korrigierbare Umfangsannahme, keine zulässige Höchstlänge oder starre Jahrgangsnorm. Mündliches Erklären am selben Produkt und sachliche Lehrkraftnotiz ersetzen längere Texte, ohne die Begründung wegzulassen. Keine Foto-/Tonpflicht.

Die spätere Oberfläche priorisiert jeweils Auftrag und relevantes Produkt. Raster/Code werden fachlich gekoppelt, Spur und Hilfen bei Bedarf erreicht; auf schmalen Ansichten bleibt der markierte Befehl mit seinem Zustand rekonstruierbar. Farben unterstützen Bezeichner, ersetzen sie nicht. Klick, Tastatur und Touch erhalten gleichwertige Befehle für Einfügen, Umordnen, Gruppieren und Entfernen; Drag-and-drop ist optional. Textliche Raster-/Spurbeschreibung, nachvollziehbare Lesereihenfolge und manuelles Schrittmaß sind Pflicht. Fachliche Wahrnehmung darf weder von Animation noch von zeitkritischer Reaktion abhängen.

## 7. Verlauf und nachgerechnetes Budget

Die fünf Termine sind eine **konkrete Planungsvariante**, keine unveränderliche Phasenmaschine. Materialeinheiten können mehrere LXF-Funktionen tragen. Die Lehrkraft kann zu Erklärung oder Revision zurückkehren. Fehlende Voraussetzungen und Produkte werden nicht durch einen Weiter-Button ersetzt.

Abkürzungen für die exakte R5-Bindung: O = Orientierung/Erklärung, G = angeleitete Übung, I = eigene Anwendung, F = Feedback/Revision, S = Sicherung/Transfer.

| Termin | Minutenfolge (je 45) | Produkt / fachlicher Haltepunkt |
| --- | --- | --- |
| 1 | 10 O Ziel, S0 und begrenzte Sichtung; 10 O frühe Modellierung oder kurze Problemöffnung mit anschließendem Erklären; 15 G Grafik/Anweisung an S1; 5 I eigener Ergänzungsschritt; 5 G angeleiteter Vergleich und Sicherung | P0/P1. Nach S0 Fach-/Sprach-/Bedienhürde trennen. Nach Beispiel einen eigenen Zustandsübergang erklären lassen. |
| 2 | 5 O Rückkehrkontext; 10 O Körper und Anzahl an S1 mit Verarbeitungsstopp; 20 G S2 vorhersagen/prüfen; 5 F gezielte Revision; 5 S Körperregel sichern | P2. Erste fachliche Abweichung kann vor der technischen Fehlermeldung liegen. |
| 3 | 5 S P4-Abruf vor alter Lösung; 10 G Rückkehrklärung und Auftragsverständnis; 20 I S3 individuell entwerfen/programmieren; 10 F Partnerprüfung und erste Revision | P3-Entwurf. Eigene Vorhersage beider Personen vor dem Vergleich; Zwischenkontrolle nach der ersten Partnererklärung. |
| 4 | 5 G Rückkehr und nötige Modellierung; 25 I S3 mit Spur fertigstellen; 10 F erklärungsbezogene Revision; 5 S Körper-/Zustandsbeziehung gemeinsam bündeln | P3. Ein fehlerfreier Lauf benötigt dennoch Begründung. Wer S3 sofort löst, prüft P2 erneut an seiner Erklärung, ohne künstlich einen Fehler einzubauen. |
| 5 | 10 I S4 zunächst eigenständig; 15 F Transferbegründung vergleichen, Missverständnis korrigieren; 15 S S5-Systemzuordnung und gemeinsame Einordnung; 5 S Dossier/Rückkehrstand sichern | P5/P6. Veränderte Ausführungsbedingung ausdrücklich erklären; offene digitale Nachweise und nächste Handlung benennen. |
| **Summe** | **35 O + 55 G + 60 I + 40 F + 35 S = 225 Minuten** | **5 × 45 Minuten**, keine zusätzliche sechste Pflicht-UE |

Diese Minuten enthalten Lesen, kleine Wechsel, Rückkehr und Sicherung innerhalb des Moduls. Sie sind nicht 225 Minuten reine Bildschirmarbeit. Die getrennten R5-Jahresbudgets für organisatorische Wechsel/Wiederaufnahme bleiben erhalten und werden nicht zusätzlich als hier schon erbrachte Lernzeit gezählt. Die R5-Wiederaufnahme von M05 nach M06 wird nicht in diese 225 Minuten hineingerechnet.

P4 liegt im Standard am Beginn des dritten Unterrichtstermins vor Wiederanzeige der am zweiten Termin gesicherten Körperregel. Der **tatsächliche Abstand** wird vor Einsatz benannt. Bei unmittelbar aneinanderhängenden Einheiten ist dies nur unmittelbare Anwendung, kein verzögerter Abruf; ein späterer Abruf bleibt offen und wird in einer ausdrücklich geplanten Folgezeit nachgeholt. Wiederhergestellte Dateien allein belegen keinen Abruf. R6 nimmt Algorithmusarbeit nach seiner eigenen Roadmap auf; keine V1-Anschluss-ID und kein automatisch verfügbares Vorwissen.

**Zeitvarianten:** Bei geringem Vorwissen ersetzt in Termin 1 die Erklärung die optionale Problemöffnung innerhalb der 20 O-Minuten. In Termin 3/4 kann der geplante Partnervergleich als Lehrkraftvergleich stattfinden; die frei werdende Organisationszeit bleibt bei eigener Anwendung/Revision. Sichere Lernende prüfen innerhalb ihrer I-Zeit eine alternative Körperzerlegung anhand gleicher Kriterien, ohne neue Pflichtinhalte. Reicht das Budget trotzdem nicht, stoppt die Lehrkraft an einem gesicherten Teilprodukt, benennt offene Nachweise und plant mit Jan zusätzliche Zeit oder einen reduzierten Teilauftrag. Vier ausgefallene/verkürzte Termine dürfen nicht stillschweigend als vollständiges M06 gelten. R5-F02 ist eine gesonderte Flexplanung, keine automatisch erteilte 270-Minuten-Erweiterung.

## 8. Hilfen, Feedback und Orchestrierung

| Hilfe | Beobachtbarer Auslöser | Begrenzte Hilfe / nächste eigene Handlung / Rücknahme |
| --- | --- | --- |
| H1 – Richtung und Zustand | Person verändert beim Drehen auch den Ort oder kann den Start nicht deuten | Einen einzelnen Drehschritt mit Richtungsmarker modellieren; Person erklärt den nächsten anderen Schritt. Marker bei sicherer Erklärung reduzieren. |
| H2 – Körpergrenze | Nur `vor` wird wiederholt, Zahl wird als Zahl aller Aktionen gelesen | Körper sichtbar umrahmen und einen Durchlauf entfalten; zweiten Durchlauf und erwarteten Zustand selbst erzeugen. Rahmenhilfe in S3 nicht vorab vollständig ausfüllen. |
| H3 – Erste Abweichung | Es wird nur auf die rote Meldung reagiert oder wahllos geändert | Erwartete und beobachtete Schritte bis zur ersten Differenz nebeneinanderstellen; Person markiert Ursache, formuliert Änderung und prüft erneut. Keine automatische Reparatur. |
| H4 – Sprache oder Bedienung | Mündliche Erklärung ist sachlich tragfähig, Text-/Eingabeweg stockt | Begriffs-/Satzhilfe beziehungsweise Bedienvorführung an einem anderen Beispiel. Die Zielentscheidung selbst bleibt bei der Person; anderer zugänglicher Eingabe-/Ausdrucksweg. Kein Defizitlabel. |

Wenn die Hilfe die Kernhandlung übernehmen müsste, wechselt die Lehrkraft ausdrücklich zur Modellierung. Erst eine neue eigene Anwendung danach trägt einen Eigenleistungsbeleg. H1–H4 sind erreichbare Möglichkeiten, keine stufenweise Pflichtabfrage.

Rückmeldung nennt **Kriterium, Produktstelle und nächste Handlung**. Beispiel für S2: „Deine Spur zeigt bei Schritt 2 eine weitere Fahrt. Prüfe, welche Anweisungen zu einem Durchlauf gehören, und teste die geänderte Gruppe vom gleichen Start.“ Der erste technische Fehler an Schritt 3 ist nur ein Befund; die fachliche Ursachenaussage bleibt zu begründen. Automatik darf Zustand/Regelverletzung melden, jedoch keine freie Erklärung automatisch als verstanden einstufen. Ein erreichbarer Lehrkraft-/Textvergleichspfad klärt unverständliche Rückmeldungen.

Partnervergleich in Termin 3: Jede Person bringt ihre eigene Vorhersage und einen erklärten Körperentwurf mit. A erklärt; B prüft einen benannten Zustandsübergang; danach Rollenwechsel. Gemeinsames Minimalprodukt ist **eine begründete Übereinstimmung oder strittige Stelle mit konkretem Prüfschritt**. Die Lehrkraft kontrolliert nach der ersten Erklärung beide Beiträge und unterbricht passive Übernahme. Unterschiede werden anschließend an der Spur gemeinsam geklärt. Jede Person überarbeitet ihren eigenen Code und begründet eine Entscheidung. Bei Partnerausfall liefert MAT-09 eine vorbereitete sachliche Gegenposition; der fachliche Auftrag bleibt, tatsächliche Kooperation wird nicht fingiert.

## 9. Orientierung, Übergänge und Wiedereinstieg

Der Arbeitsraum bietet drei fachliche Zugänge: **Auftrag und Beispiel**, **eigenes Prüfdossier**, **Sicherung und Rückkehr**. Dies sind Informationsbereiche, keine drei Pflichtbildschirme. Ein Lernender sieht den Zweck, das vorhandene Produkt, eine offene Entscheidung und eine nächste Handlung. Eine Gesamtprozentzahl oder elf zwangsweise abzuarbeitende Zustände sind ausgeschlossen.

| Lage / Übergang | Bedingung und Lehrkraftentscheidung | Rückkehr-/Fallbackfolge |
| --- | --- | --- |
| Start → Modellierung oder begrenzte Problemöffnung | S0 liefert erklärbare fachliche Spur; bei Mehrdeutigkeit kurz nachfragen | Fehlende Voraussetzung aufbauen, keine Vorerfahrung aus M01-Abhakung ableiten. |
| Beispiel → eigene Anwendung | Ein selbst ergänzter Kernschritt ist erklärbar | Sonst anderes Teilbeispiel modellieren; kein unbegleitetes Weiterklicken. |
| Vorhersage → Ausführen | Erwartung ist schriftlich, markiert oder mündlich am Produkt rekonstruierbar | Freie technische Erkundung bleibt möglich, wird aber nicht als vorhersagegebundener Beleg gespeichert. Keine Texteingabe als starre Ausführungssperre. |
| Ausführen → Vergleichen/Revision | Code-, Szenario- und Vorhersagestand gehören zusammen | Bei Codeänderung alte Spur als früheren Stand behalten und neuen Lauf erzeugen; niemals alte Spur stillschweigend neuem Code zuordnen. |
| Revision → Sicherung | Gleiches Kriterium ist am Vorher-/Nachherstand geprüft | Offene Begründung sichtbar lassen, statt automatisch Kompetenz zu setzen. |
| Unterbrechung → Weiterarbeit | Stand, Szenariofassung und letzte offene Entscheidung sind lesbar | Lernende bestätigen nächsten Schritt; kein Zwang, alle vorigen Bereiche erneut abzuhaken. |
| Unterbrechung → Abruf | Früher gesicherte Beziehung, tatsächlicher Abstand, alte Lösung zunächst verdeckt | Aktiver Abruf → Feedback → alte Lösung/Nachklärung; Recovery und Behalten sind verschiedene Nachweise. |
| Produkt fehlt / Import unbrauchbar | Verlust sachlich benennen, vorhandenes Original schützen | Kurzer Ersatzfall und Rekonstruktion, kein erfundener Lernerfolg und kein Rückschluss auf fehlendes Verständnis. |

Die Rückkehrkarte nennt: zuletzt bearbeiteter fachlicher Gegenstand, vorhandener Produktstand, offen gebliebene Prüfung und nächste Handlung. Sie unterscheidet `bearbeitet`, `geprüft`, `offen` und begründet `nicht anwendbar`. „Geprüft“ bezeichnet ein genanntes Kriterium an einem Produkt mit benannter Prüfart, keine Freigabe oder globale Kompetenz. Letzter Seitenbesuch und fachliche Sicherung sind getrennt.

## 10. Technischer Übergabevertrag

Die folgenden Entscheidungen machen den späteren Auftrag konkret. Sie implementieren keine neue Schnittstelle und vergeben noch keine Software-/Payloadversion.

| Bereich | Designentscheidung | Vor Implementierung/Einbindung zu belegender Vertrag |
| --- | --- | --- |
| Modulidentität | `V2-G5-M06` bleibt Planungs-ID; später eigenes V2-Modul mit dieser Zuordnung | Neue eindeutige Produktidentität und Versionsmatrix festlegen; keine automatische Migration von `IUM-5-CORE-05` 0.1.0/schema 1. TECH-F01/F07, M02/M07. |
| Fachlogik | Aus IUM18 Bewegung, Drehung, konstante nicht verschachtelte Wiederholung und explizite Vorher-/Nachherspur selektiv nutzen | V1-`Scenario`/`WorldState` enthalten Transportfelder. Diese nicht ins neue Lernmodell zwingen. Neutrales Raster-/Zustandsmodell ableiten, Körperlimit von vier auf fünf anpassen und Bewegungsteil samt Parser/Editor gegen neue Fälle erneut prüfen. Unveränderte Direktübernahme des alten Moduls ist ausgeschlossen. |
| Prüfergebnis | `Programm beendet`, `Regel verletzt` und `Auftragskriterium erfüllt` unterscheiden | S3-Zielprüfung berücksichtigt Route/Prüfpunktreihenfolge und Blickrichtung; freie Begründung bleibt menschlich. Die V1-Eigenschaft `delivered` ist hier kein Erfolgskriterium. |
| Produktdaten | Begrenzte P1/P2/P3/P5/P6-Spuren; jeweilige Szenario-/Codefassung, Vorhersage und ausgewählter Lauf nachvollziehbar verbinden | Keine vollständige Versuchschronik, Personen-ID, Zeit-/Klick-/Hilfenprofil. Änderungen entwerten Zuordnung aktueller Nachweise, ohne Originale still zu überschreiben. Belegauswahl und Arbeitsfassung trennen. |
| Speicherung | Vor erstem persistentem Schreiben verständliche Wahl; flüchtige Arbeit möglich und ehrlich benannt | Modul-/Schema-/Payloadprüfung bei Laden/Import gleich; Speicherwahl und tatsächliche Datenflüsse stimmen überein. Ein aktiver Schreibstand pro Modul/Profil mit überprüftem Konflikt-/Löschschutz, weitere Tabs nicht still parallel schreiben lassen. TECH-F01/F04/F05. |
| Import/Export/Verlust | Vor Ersetzen Vorschau und bestätigte Entscheidung; Original bei Fehler erhalten und wieder exportierbar | Fehlgeschlagene/abgebrochene Vorschau entwertet Pending-Import; V1-Dateien verständlich ablehnen, nicht passend machen. Exportkopien separat behandeln. Clipboard nur als bewusst gewählte Aktion, kein versteckter Fallback. TECH-F02/F03/F05. |
| Updates | Arbeit vor Reload sichern oder Update verschieben; flüchtiges Flush ist keine Sicherung | Ungesicherter oder konfliktbehafteter Stand verhindert automatischen Reload; mehrere Clients und Fehlerpfade müssen geprüft sein. TECH-F06. |
| Lieferung und Zugang | Statischer Arbeitsraum, eigener Print-/Textpfad, kein benötigtes Login/Backend | Browser-/Geräte-/Netz-/LMS-Zielmatrix am tatsächlichen Kandidaten; Firefox- und WebKitbefunde aus FU-TECH bleiben offen. Neues Manifest/Registry/CI/Baselineprüfung und korrekte Follow-up-Projektion erforderlich. TECH-F07/F08. |

Die synthetische Semantikprobe verwendet den heutigen V1-Interpreter mit intern notwendigen, ungenutzten Transportfeldern nur zur Prüfung des Bewegungsteils. S3 wird als entfaltete Folge geprüft; die kompakte Fünfbefehlsschleife wird vom heutigen Parser erwartungsgemäß abgelehnt. Sie ist **kein V2-Adapter und kein Nachweis der neuen Oberfläche**. Wenn sich die Extraktion nicht begrenzt und verständlich realisieren lässt, ist vor dem neuen Implementierungsplan die Werkzeugentscheidung erneut zu prüfen; der fachliche Produktvertrag bleibt maßgeblich.

## 11. Kanal, GOV und offene Einsatzbedingungen

Der statische Arbeitsraum ist gewählt, weil editierbarer Code, schrittweise deterministische Ausführung und vergleichbare Zustände die Zielhandlung tragen. HTML/WordPress als reine Quellenumgebung und LearningView als Abgabe-/Kurssteuerung wurden erwogen; beides ist für den hier begrenzten Kern nicht erforderlich. Ein späteres LMS kann einen freigegebenen Einstieg bereitstellen, ersetzt jedoch keine Einbettungsprüfung. Keine neue Plattform wird eingerichtet.

Die Spezifikation verwendet ausschließlich sachliche Eigenentwürfe. Das ist kein pauschaler Rechte-/Datenschutznachweis für spätere Assets oder den Betrieb. GOV-Q-OPERATOR (Betreiber/Hosting/Logs), GOV-Q-SCHOOL (konkrete Schule, Profile, Datenflüsse/Fristen), GOV-Q-REVIEWERS (zuständige fachliche/technische Prüfende) und GOV-Q-RIGHTS (konkrete Inhalte, Bearbeitungen, Lizenzen und Auslieferungsort) bleiben offen. Jan koordiniert die zuständigen Rollen; eine Rolle ist noch keine eingesetzte oder unabhängige Person.

Keine private Medienbiografie, reale Accounts, Aufzeichnungen oder institutionell eingesammelten Reflexionen. Das Dossier kann dennoch freie Texte enthalten: spätere Umsetzung soll zur sachbezogenen Eingabe anleiten und schützt den lokalen Zugriff. App-Löschen entfernt keine Downloads, Clipboardkopien, LMS-/Hostlogs oder Gerätesynchronisation. Realbelege bleiben außerhalb des öffentlichen Repos. FU-PILOT muss den konkreten Beobachtungs-/Speicher-/Löschvertrag vor seinem eigenen Ergebnis festlegen; hier werden keine Fristen oder anonymen Datenbestände erfunden.

Offene Bedingungen blockieren den **jeweils betroffenen späteren Schritt**, nicht die schriftliche Abnahme dieser Spezifikation. Aktuell vorgeschlagenes Design: `review`; Curriculum: `unassessed`; Produktimplementierung: `not-started`; reale Technik/Zugänglichkeit/Nutzung: `not-run`; Pilot: `not-started`; Wirkung: nicht belegt; Veröffentlichung: `closed`.

## 12. LXF-Ableitung, Prüfbarkeit und Abnahme

Die vollständige Quellen-/Claim-/Prinzipienbindung steht in `specification.json`: R5-Prinzipien werden übernommen; PR-004/005/010/014/016/017 ergänzen begründet Materialökonomie, digitale Handlung, formative Aufgaben, verzögerten Abruf, Recovery und Zugang. PR-002 trägt die begrenzte Wahl des Ausdruckswegs. Es gibt keinen neuen empirischen Claim. Die abgeleiteten Minuten, Fälle und Materialmengen sind **Designentscheidungen unter offenen Alters-/Nutzungsannahmen**. Die LXF02-Geltungsgrenzen einschließlich begrenzter Übertragbarkeit auf Klasse 5 bleiben bestehen.

| LXF-Gate | Konkreter Designbeleg | Grenze des aktuellen Selbstreviews |
| --- | --- | --- |
| evidence-integrity | §§ 1–4, 12; Eingabehashes und Claimketten | Quellen-/Dokumentenprüfung; keine neue Wirkungsevidenz |
| goal-action-evidence-alignment | §§ 3–5; P0–P6 und sieben Records | Nachweise geplant, keine Coverage gesetzt |
| cognitive-economy | §§ 6–8; Materialgrenzen, fünf Termine, optionale Hilfen | Keine empirischen Lese-/Zeitgrenzen bestätigt |
| disciplinary-learning-action | §§ 3, 5, 8; Vorhersage, Körperentscheidung, Revision | Eigene Handlung muss später beobachtet werden |
| representation-coherence | §§ 5–6; Grafik/Code/Spur, textliche Entsprechung | Kein fertiges UI und kein Accessibilitypass |
| support-without-task-removal | § 8; H1–H4 mit Rücknahme und eigener Anwendung | Keine reale Hilfenutzung geprüft |
| feedback-and-next-action | §§ 7–9; P2/P4/P5 und Revisionszeiten | Abrufabstand noch lokal zu bestimmen |
| orientation-and-recovery | §§ 9–10; drei Informationszugänge und Verlustfälle | TECH-F01–F06 nicht repariert |
| accessibility-and-equivalence | §§ 6, 9–10; alternative Eingabe/Ausdruck/Print, offenes ALG-005 | Tatsächlicher Geräte-/Hilfsmittelzugang offen |
| teacher-orchestration | §§ 7–9; konkrete Haltepunkte, Kooperation und Ersatzsichtung | Führbarkeit und Zeit nicht pilotiert |
| privacy-and-emotional-safety | §§ 3, 8, 11; sachliche Produkte und Speichergrenzen | GOV-Einsatzfreigaben offen |
| pilot-boundary | §§ 10–12; getrennte Reifeachsen/Übergaben | FU-PILOT braucht eigene Abnahme-/Auftragslage; keine Durchführung |

WU-Check: Kognitive Aktivierung liegt in der begründeten Körper-/Zustandsentscheidung; Unterstützung adressiert konkrete Hürden; Führung erfolgt an Produkten und Haltepunkten; Feedback hat reservierte Revisionszeit. Kooperation erfordert beide Beiträge und individuelle Anschlussarbeit. Fehlender Exit führt zu Ersatzsichtung. Sprach- und Eingabewege erhalten die fachliche Erklärung. Wichtigster verbleibender Prüfpunkt ist, ob fünf Einheiten bei tatsächlichem Vorwissen für **eigenständiges Programmieren plus begründeten Transfer** reichen. Quellenbasis: gelesene lokale WU-Exzerpte 1, 4 und 5 als Reflexionsrahmen; LXF02 bleibt die registrierte Evidenzbasis.

Pflicht-Gates der Unterrichtsplanung: Planungsanker **gesichert als R5-Projektplan, reale Klasse als Annahme markiert**; Lernprozess und Sinn **im Design begründet**; Fachlichkeit **an internen Spuren prüfbar**, Material **spezifiziert, noch nicht produziert**; Passung **nachgerechnet, real ungeprüft**; Lernsteuerung/Diagnose **konkret geplant**; Digitalitäts-, Kooperations- und Fallbackvertiefung **dokumentiert**. Das ist keine Einsatzbewertung fertiger Materialien.

Zur Nutzerabnahme steht dieses vollständige Design: Auswahl M06, neuer Prüffahrtkontext und Transfer, Produkt-/Nachweisvertrag, 225-Minuten-Variante, Unterstützung/Orchestrierung und technische Übergabegrenzen. **Erst nach dieser Designabnahme darf ein neuer Implementierungsplan daraus abgeleitet werden.** Ein eigener Folgeauftrag muss seinen Umfang benennen; die Abnahme allein repariert keine TECH-Befunde und startet keine Produktion. FU-PILOT bleibt ein separater Spezifikationsauftrag; eine reale Durchführung wäre wiederum gesondert freizugeben.
