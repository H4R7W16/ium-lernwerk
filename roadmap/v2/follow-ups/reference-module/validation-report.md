# FU-MOD – Spezifikationsprüfung und Aussagegrenzen

Stand: 07.09.2026. **Design zur Nutzerabnahme, kein Produkt- oder Einsatznachweis.** Reviewart: KI-Dokumentenselbstprüfung. Kein unabhängiger Fachreview und keine menschliche Nutzungsprüfung werden behauptet.

## Gegenstand

Geprüft wird das [Moduldesign](../../../../docs/superpowers/specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md) für `V2-G5-M06`, seine [strukturierte Bindung](specification.json), die Übernahmegrenzen der Auditfamilien IUM16/IUM18/LXP02 und die Rechen-/Semantikbeispiele. Input ist `69634c56d3d100d3bf33632f29a4f98eaf579276`; die FU-TECH-Abnahme vom 07.09.2026 bleibt auf den Audit begrenzt.

## Formale und synthetische Verifikation

Die tatsächlich ausgeführten Ergebnisse stehen in [validation.json](validation.json) und [semantics-results.json](semantics-results.json). Reproduktion aus dem Repositoryroot, unter dem Repository-Node-22/npm-10-Vertrag:

```text
npx tsx roadmap/v2/follow-ups/reference-module/semantics-probe.mts
python -B roadmap/v2/follow-ups/reference-module/verify-spec.py
python -B scripts/validate_v2_rebaseline.py
python -B scripts/validate_v2_activation.py --vault "../../Vault"
npm run dashboard:update
git diff --check
```

`verify-spec.py` prüft acht Gruppen: unveränderte aktuelle/historische Inputhashes (Checkout und Git-Blob separat, CRLF/LF nur beim Inhaltsvergleich normalisiert), Abnahme-/Designgrenze, sieben exakte R5-Curriculumzuordnungen und Produkte, Minuten/Lernfunktionen, LXF-Claim-/Quellen-/Gatebezüge, vorhandenen Semantikbeleg, lokale Markdownlinks und unveränderte Produktpfade. Die Ausgabedatei bindet den konkreten Artefaktstand per SHA-256. Die Skripte sind Dokumenten-/Semantikprüfhilfen, keine Modulimplementierung; sie sind nicht an die Produktionsregistry oder CI angebunden.

| Ausgeführt am 07.09.2026 | Ergebnis |
| --- | --- |
| Semantikprobe, Node 22.23.2 / npm 10.9.8 | Vier Bewegungsfälle, eine erwartete V1-Parserablehnung und drei Vergleichsprüfungen bestätigt |
| Spezifikationsprüfung | Acht Gruppen bestanden; 32 Inputs, sieben Records, 22 Zeitsegmente/225 Minuten, 18 Prinzipien, 23 Claims mit 23 Quellen, zwölf Gates und 13 lokale Links |
| V2-Re-Baseline-Validator | Bestanden; historische Grundlagen unverändert |
| Aktivierungsvalidator mit tatsächlichem `../../Vault` | Bestanden; V2 Planungs-/Entwicklungsbaseline und V1-Produktgrenze erhalten |
| Dashboardprojektion aus aktuellem Statusregister | Snapshot und Obsidian-Cockpit erfolgreich aktualisiert; historische HTML-Follow-up-Projektion weiterhin separat nachzuarbeiten |

Die Probe führt vier neue Rastervektoren mit dem **vorhandenen V1-Interpreter** aus und vergleicht erwartete Zustände: S0 endet bei `(2,2)/Ost`, S1 nach acht Aktionen am Start/Ost, S2 scheitert technisch bei Aktion 3, und S3 durchläuft als entfaltete Folge in zehn Aktionen die vorgesehene Rechteckroute. Eine fünfte Probe bestätigt, dass seine kompakte Schleife mit fünf Körperanweisungen vom heutigen Parser abgelehnt wird (Limit vier). Diese Produktlücke ist als benötigte Anpassung ausdrücklich offengehalten. Drei zusätzliche Vergleiche prüfen: erste fachliche Abweichung bereits bei Aktion 2; die vollständige S3-Fahrspur; und den Gegenfall eines leeren Programms, das denselben Endzustand ohne Prüffahrt besitzt. Notwendige Transportfelder des heutigen Schemas sind nur intern gesetzte, ungenutzte Probeparameter. Ihre Entfernung/Entkopplung ist späterer Anpassungsbedarf, kein hier implementierter V2-Adapter.

S4 und S5 wurden fachlich als **Dokumenten-Walkthrough** geprüft. S4: Nach der ersten Aufnahme ist die Station belegt; eine zweite Aufnahme verletzt die definierte Voraussetzung. Dagegen stellt Aufnahme → Prüfung → Ablage jeweils den freien Zustand für den nächsten Durchlauf her. S5: Die Funktionsbeschreibung trägt die Systemzuordnung; ein Papieralgorithmus ist kein digitales System und ein isoliertes digitales Bild belegt den wesentlichen Verarbeitungsprozess nicht. Kein realer Prüfautomat oder externes System wurde getestet.

Der erste Lauf der Prüfhilfe verwendete ungültige technische Befehls-IDs; nach Kontrolle des Parsers wurden nur die Probe-IDs in dessen Format `cmd-N` gebracht. Ein zweiter Prüfaufbaufehler setzte Checkout-CRLF-Bytes mit Git-LF-Bytes gleich. Beide Prüfhilfen wurden korrigiert, ohne historische Eingaben zu ändern. Die zusätzlich gefundene Vierbefehlsgrenze wurde nicht wegkorrigiert, sondern als reale Übernahmegrenze dokumentiert.

Neue Produkt-/Browsertests sind für diesen Auftrag nicht angezeigt, da kein Produktcode geändert wurde. Die im angenommenen FU-TECH-Bericht offenen Firefox-/WebKit-/Gerätebefunde bleiben offen. Frühere umfangreiche Produktprüfungen werden nicht als neue FU-MOD-Verifikation ausgegeben.

## Selbstreview und eingearbeitete Korrekturen

| Gegenprobe | Befund und finale Auflösung |
| --- | --- |
| Wird M06 wegen der vorhandenen Technik automatisch gewählt? | M01/M04/M06 sowie manuell/externe Sprache/kleiner statischer Arbeitsraum verglichen. M06 ist Entwicklungsreferenz, Unterricht bleibt nach R5 geordnet. |
| Wird alter Kontext nur umbenannt? | Neue Bewegung mit mehrgliedrigem Körper und Zustandskontrast; Transport-/Liefermodell und alle alten Szenario-IDs ausgeschlossen. IUM18 muss für den neutralen Bewegungsteil angepasst werden. |
| Trägt ein Rasterweg schon ALG-003? | Nein. Spezifikation fordert erklärbare grafische Befehlsfolge samt Körper und eigene Durchführung; Ortslinie/Animation genügen nicht. |
| Ist ein erfolgreicher Lauf eine gelungene Lösung? | Nein. S3-Gegenfall mit leerem Code belegt die Lücke der reinen Endzustandsprüfung. Weg, Prüfpunkte und Erklärung müssen hinzukommen. |
| Wurde die erste Ursache mit der Fehlermeldung verwechselt? | S2 hat die erste fachliche Abweichung bei Schritt 2, den Laufabbruch erst bei Schritt 3. Rückmeldung ausdrücklich daran gebunden. |
| Stimmt die Minutenverteilung wirklich mit R5 überein? | Im ersten Entwurf waren fünf Minuten zu viel unter Sicherung und zu wenig unter angeleiteter Übung geführt. Der angeleitete Vergleich in Termin 1 wurde korrekt unter Übung eingeordnet. Final exakt O35/G55/I60/F40/S35 und fünfmal 45 Minuten. |
| Reicht „kleine positive Anzahl“ für den Interpretervertrag? | Präzisiert: Designfälle 2–4, aktueller Parser 2–9, technisches Limit 100 Aktionen. Keine unbelegte Fähigkeit des V1-Parsers und keine Altersnorm. |
| Passt der ganze neue Körper in den alten Parser? | Nein. S3 verlangt fünf Körperanweisungen, V1 erlaubt vier. Erwartete Ablehnung und entfaltete Bewegung separat geprüft; Limitanpassung bleibt offen. |
| Sind Rückkehr und Abruf dasselbe? | Nein. P4 vor Wiederanzeige; echter Abstand lokal festzulegen. Bei direkt anschließenden Terminen kein verzögerter Abruf behauptet. |
| Kann Partnerarbeit Eigenleistung verdecken? | Eigene Vorhersagen, Rollenwechsel, gemeinsamer Prüfpunkt, frühe Zwischenkontrolle, individuelle Revision und Ersatzprodukt festgelegt. |
| Ist Papier eine vollständige Erfüllung? | Nein. ALG-005 bleibt ohne tatsächliches selbstständiges Programmieren offen. Gleicher fachlicher Maßstab, getrennte Nachweisgrenze. |
| Wurden Mengen/Minuten als Forschungsergebnis dargestellt? | Sämtliche Mengen, Fälle und Zeitvorgaben sind lokale Designentscheidungen. Die freigegebenen 23 Claims behalten ihre Geltungsgrenzen. |
| Werden Einsatzfragen in die Designabnahme hineingelesen? | Nein. Sechs explizite Übergabebedingungen, acht TECH-Befunde und GOV-/R5-Gates bleiben offen; eigenes Designreview vor Implementierungsplan. |

Alle zwölf LXF-Gates besitzen im Design eine konkrete Fundstelle, verantwortliche Rolle und reale Nachweisgrenze. Status ist `specified-for-user-review`; es wird kein neues `passed` für fachliche Nutzerabnahme, Zugänglichkeit oder Pilot erzeugt. Der knappe WU-/Unterrichtsplanungscheck steht im Design § 12.

## Offene spätere Nachweise und Verantwortlichkeit

- **Designabnahme – Jan:** Auswahl, Produktvertrag, neuer Kontext/Transfer und 225-Minuten-Variante annehmen oder konkret nacharbeiten lassen. Bis dahin kein Implementierungsplan.
- **Technische Anpassung – technische Prüfende:** TECH-F01–F08, neutraler Bewegungsadapter, Manifest/Registry, Datenversionen, Recovery, Speicher-/Mehrtab-/Updatevertrag, Browsermatrix und Statusprojektion. Kein Befund durch dieses Dokument geschlossen.
- **Programmiersprache/Zugang – Fach-/Zugangsprüfung:** Tatsächliche eigene Codebearbeitung und Ausführung, Darstellungsverknüpfung, Tastatur/Touch/Hilfsmittel und Ausdruckswege. Keine WCAG- oder reale Gerätefreigabe aus der Probe.
- **Konkrete Klasse/Zeit – planende Lehrkraft:** Tatsächliches M01-Anschlusswissen, Termine/Abstand, Geräteverteilung, Materialverständnis, Führbarkeit und zusätzliche Hilfen. Fünf Einheiten bleiben Hypothese.
- **Betrieb/Rechte – Jan koordiniert zuständige Stellen:** GOV-Q-OPERATOR/SCHOOL/REVIEWERS/RIGHTS, konkrete Datenflüsse und Fristen. CUR-Q-002 und weitere R5-Eigenbezüge unverändert offen.
- **Prüf-/Pilotinstrumente – FU-PILOT in eigenem Auftrag:** An dieses konkrete Design, seine Produkte und Zeiten binden; vor realer Durchführung erneut gesonderte Einsatzentscheidung. Zufriedenheit, grüner Test oder vorhandenes Dossier belegen keine Lernwirkung.

Empfehlung der Selbstprüfung: Das schriftliche Design ist als abgegrenztes FU-MOD-Ergebnis zur eigenen Nutzerabnahme bereit. Die genannten realen Prüfungen sind bewusst noch nicht möglich und deshalb keine bestandenen Nachweise. Dieses Ergebnis legitimiert weder eine neue Implementierung noch Produktion, Pilot oder Veröffentlichung.
