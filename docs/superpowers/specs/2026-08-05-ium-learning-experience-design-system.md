# IuM-Lernwerk – Design-, Interaktions- und Produktionssystem

- **Task:** LXP04 Designsystem, Interaktionsmuster und Produktionsverträge ableiten
- **Status:** reviewbereit; schriftliche Nutzerfreigabe offen
- **Fassung:** 0.9
- **Datum:** 5. August 2026
- **Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E
- **Ausgangsstand:** lokaler `main` auf `38c68b6`; `origin/main` auf `3498838`
- **Arbeitsgrenze:** codefreie Spezifikation und detaillierter Implementierungsplan; kein Produktcode, keine IUM5-Neufassung, kein Preview, keine reale Erprobung

## 1. Entscheidung und Zweck

LXP04 wählt ein **vertragsorientiertes Learning-Experience-System**. Es beginnt nicht bei Farben, Karten oder einem Bestandsscreen, sondern bei der fachlichen Lernhandlung und ihrer überprüfbaren Beziehung zu Ziel, Denkobjekt, Evidenz, Rückmeldung, Revision, Orchestrierung und Resilienz.

Das System besitzt vier Ebenen:

1. **Experience-Vertrag:** normative Objekte, elf LXP02-Lernzustände, Guards, Fortschritts- und Datenbedeutung, Rollen und kontrollierter Wortschatz;
2. **Designgrundlage:** semantische Rollen für Typografie, Farbe, Fläche, Abstand, Bewegung, Fokus und Informationsdichte;
3. **Pattern- und Komponentenvertrag:** situationsübergreifend bestätigte Kompositionen und Interaktionen mit Zweck, Pflichtinhalt, Varianten, Zuständen, Semantik, Grenzen und Regression-Signalen;
4. **Produktionsvertrag:** versionierte Inhalts- und Patternschemas, Autor:innenworkflow, Qualitätsgates, Erweiterungsregeln und ein TDD-Implementierungsplan.

Die Architektur erhält die in LXP03 gewählte **stabile Fokuskomposition mit sichtbarer Lernzustandsbeziehung**. Pro Moment besitzt genau eine fachliche Lernhandlung Primat. Kontext, Überblick, Hilfe, Daten- und Recoveryhandlungen bleiben erreichbar, werden aber nur bei aktueller Funktion dominant.

Das System wird in LXP05 technisch als eigenes Paket `@ium/learning-experience` umgesetzt. Das bestehende `@ium/ui-components` bleibt für plattformweite technische Primitiven wie Verbindungs-, Speicher-, Update-, Fehler- und Datenkontrollen zuständig. Die Trennung verhindert, dass Infrastrukturstatus erneut die Lernhandlung dominiert oder der heutige IUM5-Workbench zum Designstandard wird.

## 2. Status, Geltungsbereich und Freigabegates

Der Nutzer hat LXP04 am 5. August 2026 ausdrücklich zur vollständigen Ausführung beauftragt, Codex operative Entscheidungen übertragen und nur dokumentierte Freigabegates als Stopppunkte bestimmt. Damit sind Taskanlage, Kontextprüfung, Ansatzvergleich, Designsystem-Spezifikation, Produktionsvertrag, Selbstprüfung, Implementierungsplan, lokale Dokumentationsintegration und gebündelte Reviewvorbereitung geöffnet.

LXP04 entscheidet verbindlich nach schriftlicher Freigabe:

- Systemgrenze und Paketverantwortung;
- semantische Designrollen und konkrete Grundwerte;
- Kompositions-, Komponenten-, Inhalts-, Interaktions-, Accessibility-, Resilienz- und Orchestrierungsverträge;
- Produktionsschema, Autor:innenworkflow, Governance und Qualitätsgates;
- Reihenfolge, Dateien, Schnittstellen, Tests und Commitgrenzen der späteren LXP05-Implementierung.

Geschlossen bleiben:

- schriftliche Annahme dieser Spezifikation und des Implementierungsplans;
- Ausführung von LXP05 oder des Implementierungsplans;
- Änderungen an Apps, Paketen, Modulen, Tests, Assets oder Buildkonfiguration;
- Neufassung von `IUM-5-CORE-05`;
- Auswahl oder Beschaffung externer Schrift-, Icon- oder Illustrationsassets;
- Preview, Deployment und reale Geräteprüfung;
- Pilotierung, LMS, Produktrelease und Statushochsetzung;
- Push oder Pull Request des lokalen Dokumentationsstands.

Die LXP04-Freigabe darf später ausschließlich LXP05 als neue Umsetzungsetappe öffnen. Sie ist keine Produkt-, Unterrichts-, Accessibility-, Pilot- oder Releasefreigabe.

## 3. Normative Eingaben und Vorrangregel

### 3.1 Quellen der Wahrheit

| Rang | Eingabe | Verbindliche Funktion in LXP04 |
|---:|---|---|
| 1 | neueste ausdrückliche Nutzerentscheidung | höchste Projektentscheidung |
| 2 | LXP01 Fassung 1.0 | Experience-Nordstern, Lernhandlungsloop, Q1–Q8, Motivation, Accessibility und globale Anti-Patterns |
| 3 | LXP02 Fassung 1.0 | Objekte, elf Lernzustände, Guards, Begriffe, Fortschritt, Daten, Rollen, Resilienz und Architekturgrenzen |
| 4 | LXP03 Fassung 1.0 | konkrete Vergleichsevidenz, Ansatz C, dreizehn Musterkandidaten, sieben Restrisiken und Nicht-Generalisierungen |
| 5 | Gesamtdesign und IUM5-Moduldesign | Projekt-, Fach- und technischer Belastungskontext; keine UI- oder Produktfreigabe |
| 6 | bestehender Plattformcode | belegte Mechanismen und Integrationsgrenzen; keine Designsystemnorm |
| 7 | diese Spezifikation | nach schriftlicher Freigabe normativer LXP04-Vertrag für LXP05 und LXP06 |

### 3.2 Konfliktregel

- LXP04 darf keine LXP01-Qualitätsdimension oder LXP02-Invariante still abschwächen.
- Ein LXP03-Musterkandidat wird nur generalisiert, wenn mindestens zwei Referenzsituationen ihn bestätigen und sein vollständiger Vertrag hier geschlossen wird.
- Eine einzelne IUM5-Repräsentation darf keine globale Komponente begründen.
- Visuelle Attraktivität darf nie gegen fachliche Klarheit, Bediengleichwertigkeit, Datenintegrität oder Lehrkraftorchestrierung priorisiert werden.
- Belegt ein späterer Prototyp einen Widerspruch, wird LXP04 ausdrücklich revidiert; LXP05 darf ihn nicht durch lokalen Sondercode verdecken.
- Wo technische Realisierung offenbleibt, muss der Experience-Vertrag trotzdem Ergebnis, Guard, Fail-Signal und zuständige Folgephase festlegen.

## 4. LXP04-Ergebnisvertrag

| ID | Ergebnis | normative Herkunft | Nachweis in dieser Spezifikation | Prüfung | Status |
|---|---|---|---|---|---|
| LXP04-01 | Systemisierungsansätze und Auswahl | LXP03 Auswahlentscheidung | § 5 | drei Ansätze, Kosten, Risiken, begründete Wahl | specified |
| LXP04-02 | geschlossene Traceability | LXP01–LXP03 | § 4 und § 22 | 12/12 Ergebnisse, Quellen und Gates | specified |
| LXP04-03 | semantische Designrollen | LXP01 Q1–Q3/Q7; LXP03 Nicht-Generalisierungen | §§ 7–8 | Rollen, Werte, Kontrast, Dichte und Motion | specified |
| LXP04-04 | Kompositionssystem | LXP03 Ansatz C | § 9 | Kosmos, Lernstudio, Fokusbühne, Kontextband, Aktionskante, Wide/Schmal | specified |
| LXP04-05 | Komponentenfamilien | LXP03 Musterkandidaten | § 10 | Zweck, Pflichtinhalt, Varianten, Zustände, Semantik, Nichtverwendung | specified |
| LXP04-06 | Interaktionsmuster | LXP02 Zustände/Guards; LXP03 Wireflows | § 11 | Orientierung bis Wiedereinstieg, Fokus und Status | specified |
| LXP04-07 | Inhaltsverträge | LXP01 Feedback/Revision; LXP02 Begriffs-/Belegvertrag | § 12 | Aufgaben, Copy, Hilfe, Feedback, Beleg, Lehrkraft | specified |
| LXP04-08 | Responsive- und Modalitätsvertrag | sieben LXP02-/LXP03-Risiken | §§ 9 und 13 | Wide/Schmal, Touch, Tastatur, Text/AT, Reduced Motion | specified |
| LXP04-09 | Accessibility- und Resilienzvertrag | LXP01 Q7/Q8; LXP02 Resilienz | §§ 13–14 | Fokus, Status, Reflow, Offline, Speicher, Recovery, Datenhandlung | specified |
| LXP04-10 | Produktions- und Governancevertrag | Initiative LXP04/LXP07-Grenze | §§ 16–18 | Schema, Autor:innenworkflow, Gates, Versionierung, Erweiterung | specified |
| LXP04-11 | Qualitäts- und Portabilitätsprüfung | LXP01 Q1–Q8/Anti-Patterns; LXP03 WU/Portabilität | §§ 15 und 19–21 | WU, 24 Systemurteile, drei Domänenproben, 12 Anti-Patterns | specified |
| LXP04-12 | detaillierter TDD-Implementierungsplan | Kontextpaket Chat 4 | separates Planartefakt, § 23 | exakte Dateien, Schnittstellen, RED/GREEN, Kommandos und Commits | specified |

## 5. Systemisierungsansätze

### 5.1 Ansatz A – visuelles Atomic-Design-System

**Kern:** Farben, Typografie, Abstände, Atome und Moleküle werden zuerst definiert; Lernseiten werden daraus zusammengesetzt.

**Stärken:** bekannte Designsystemlogik, schnelle visuelle Vereinheitlichung, kleine technische Bausteine.

**Kosten und Risiken:** Lernzustand, Evidenz und Orchestrierung werden zu nachträglicher Businesslogik; semantisch gleich aussehende Karten können fachlich völlig verschiedene Aufgaben tragen; der Bestand würde leicht nur neu dekoriert. LXP01 Q1–Q6 und die LXP03-Warnung vor fester Bildschirmtaxonomie wären gefährdet.

**Urteil:** als interne Komponentenzerlegung nützlich, aber als führende Systemlogik verworfen.

### 5.2 Ansatz B – IUM5-first Pattern Library

**Kern:** Die vorhandene Algorithmus-Werkstatt wird in wiederverwendbare Karten, Tabellen, Editoren und Statusbausteine zerlegt.

**Stärken:** geringe anfängliche Implementierungskosten, direkter Anschluss an vorhandenen Code und Tests.

**Kosten und Risiken:** Raster, Blockeditor, deterministische Laufspur und eindeutige erste Abweichung würden fälschlich zum globalen Lernwerkmodell. Quellenurteil, Medienproduktrevision und mehrdeutige Systemmodelle wären strukturell benachteiligt. Die heutige Mega-Seite bliebe trotz Komponentenzerlegung die implizite Informationsarchitektur.

**Urteil:** als Migrationsquelle für Mechanismen zulässig, als Systemursprung verworfen.

### 5.3 Ansatz C – Contract-first Experience System

**Kern:** Zustands-, Inhalts-, Evidenz-, Orchestrierungs-, Accessibility- und Recoveryverträge führen. Designrollen und Komponenten realisieren diese Verträge; fachspezifische Repräsentationen bleiben austauschbar.

**Stärken:** vollständige Passung zu LXP01–LXP03; klare Portabilität; fachliche Eigenleistung und Datenminimierung bleiben prüfbar; technische Komponenten erhalten eindeutige Verantwortungen; Varianten können ohne Paralleltaxonomie entstehen.

**Kosten:** höherer anfänglicher Vertrags- und Testaufwand; bestehender IUM5-Code muss in LXP05 gezielt zerlegt statt kosmetisch umgebaut werden; Autor:innen benötigen validierte Inhaltsschemas.

**Entscheidung:** Ansatz C wird gewählt. Atomic-Design-Prinzipien dienen nur der technischen Zerlegung innerhalb eines bereits geschlossenen Experience-Vertrags. Bestandscode dient nur als Mechanismen- und Regressionsevidenz.

## 6. Systemarchitektur und Paketgrenzen

### 6.1 Zielpakete

| Paket/Ort | Verantwortung | darf enthalten | darf nicht enthalten |
|---|---|---|---|
| `@ium/module-contract` | plattformweite Manifest-, Zustandshüllen- und Portverträge | generische technische Schnittstellen | Lernzustands- oder UI-Details eines Moduls |
| `@ium/ui-components` | technische Plattformprimitiven | Verbindung, Speicher, Update, Fehler, Datenhandlungen | Lernweg-, Aufgaben-, Feedback- oder Belegkartentaxonomie |
| `@ium/learning-experience` | wiederverwendbares LXP-System | Designrollen, Experience-Verträge, Astro-Patterns, Fokus-/Statuscontroller, Inhaltsvalidator | IUM5-Szenarien, Interpreter, Curriculumdetails oder personenbezogene Analyse |
| `@ium/ium-5-core-05` | IUM5-Fachlogik und lokale Produktzustände | Algorithmus-, Szenario-, Beleg- und Modulpayload | globale Designrollen oder generische Orchestrierungsregeln |
| Portal-App | Routen, Registry, Shell und produktweite Komposition | Kosmos, Modulroute, Paketverdrahtung | duplizierte Fachvalidatoren oder zweite Designsystemquelle |
| Modulordner | validierter Inhalt und Assets | Inhalt, Szenarien, Modulhandbuch, Lizenzevidenz | CSS-Sonderdesign ohne Patternvertrag |

### 6.2 Abhängigkeitsrichtung

```text
module-contract
  ↑
ui-components     learning-experience
  ↑                    ↑
portal-app ← module renderer ← module package/content
```

`@ium/learning-experience` darf `@ium/ui-components` verwenden, aber nicht umgekehrt. Das Experience-Paket kennt keine IUM5-Typen. Ein Modulrenderer injiziert fachliche Repräsentation, Inhalt und Aktionen in die generischen Patterns.

### 6.3 Einheiten mit klarer Verantwortung

- **Contract:** beschreibt Bedeutung, Eingaben, Ausgaben, Guard und Fail-Signal ohne Darstellung.
- **Pattern:** verbindet mehrere Komponenten zu einer vollständigen Lernhandlung.
- **Component:** realisiert genau eine semantische Verantwortung innerhalb eines Patterns.
- **Renderer:** bindet fachliche Daten und Aktionen an Patterns; er erfindet keine neue globale Semantik.
- **Content bundle:** liefert validierte Texte, Kriterien, Hilfen, Haltepunkte und Lizenz-/Quellenangaben.
- **State adapter:** übersetzt modulspezifischen Payload in LXP02-Zustände und Fortschrittssignale; er speichert keine Verhaltensdaten.

## 7. Kontrollierter Wortschatz und Entscheidungsledger

### 7.1 Produktbegriffe

LXP02-Begriffe bleiben unverändert: `Lernwerk-Kosmos`, `Lernstudio`, `Sicherungsraum`, `Lehrkraftspur`, `Modul`, `Lernpfad`, `Unterrichtseinheit`, `Lernphase`, `Lernhandlung`, `Sicherungsartefakt` und `Belegkarte`.

Die LXP03-Analysebegriffe werden in LXP04 als Patternfunktionen präzisiert:

| Patternbegriff | Bedeutung | kein Synonym für |
|---|---|---|
| Fokusbühne | Bereich, in dem aktuelle Lernhandlung, Denkobjekt, Kriterium und unmittelbares Ergebnis Primat besitzen | gesamte Seite, beliebige Card, modales Fenster |
| Kontextband | nachrangiger, stabiler Kontext aus Ziel, Herkunft, Position, Modus und handlungsrelevantem Status | Breadcrumb allein, technische Statusleiste |
| Aktionskante | Ende eines fachlich vollständigen Zusammenhangs mit genau einer Primärhandlung und sicheren Geschwisterhandlungen | Sticky-Footer ohne Kontext, generisches `weiter` |
| Lernwegkarte | orientierend erreichbare Gesamtbeziehung von Lernphasen und Zuständen ohne Zustandsmutation | Fortschrittsbalken, Sitemap, freie Sprungnavigation |
| Evidenzbezug | explizite Relation zwischen Erwartung, Handlung, Wirkung, Quelle, Kriterium und Deutung | dekorative Hervorhebung oder Dateianhang |

### 7.2 Neue technische Namen

Die späteren APIs verwenden englische technische Kennungen, sichtbare Copy bleibt deutsch. Verbindliche Namen sind:

- `LearningStateId` für die elf LXP02-Zustände;
- `ExperienceContractV1` für den systemweiten Patternvertrag;
- `LearningActionSpec` für eine fachlich vollständige Lernhandlung;
- `ExperienceContentV1` für modulbezogenen LXP-Inhalt;
- `FeedbackSpec`, `SupportSpec`, `TeacherCheckpointSpec`, `EvidenceCardSpec` und `ResilienceSpec` für Teilverträge;
- `ExperienceShell`, `ContextBand`, `LearningStateHeader`, `FocusStage`, `ActionEdge` und `JourneyMap` für Grundkomponenten.

Lokale Prüfbezeichnungen wie `SEC-WRITE` oder `REENTRY-COMPARE` werden nicht zu globalen Zustands-IDs.

## 8. Visuelle Sprache und semantische Designrollen

### 8.1 Gestalterische Richtung

Die visuelle Richtung heißt **ruhige Präzision**:

- sachlich und wertig statt steril;
- altersangemessen statt kindlich verniedlicht;
- klare Hierarchie statt dekorativer Kartensammlung;
- sichtbare Beziehungen statt flächiger Farbcodierung;
- fokussierte Akzente statt Belohnungsästhetik;
- robuste Systemschriften und lokale SVG-Assets statt netzabhängiger Markenmittel.

Kosmos und Lernstudio sind verwandt, aber nicht identisch. Der Kosmos darf mehr Überblick und modulare Vielfalt zeigen. Das Lernstudio reduziert die visuelle Varianz und priorisiert die aktuelle fachliche Beziehung. Sicherungsraum und Recovery verwenden dieselben Rollen; sie erhalten keine Portfolio- oder Alarmästhetik als eigenes Produkt.

### 8.2 Farbrollen Fassung 1

| Rolle | Wert | Zweck | Kontrastbeispiel | Verbot |
|---|---|---|---|---|
| `--lx-color-canvas` | `#F7F5F0` | ruhiger Seitenhintergrund | `#17212B` darauf 14,95:1 | Statusbedeutung |
| `--lx-color-surface` | `#FFFFFF` | Arbeitsfläche | `#17212B` darauf 16,29:1 | alleinige Fokusmarkierung |
| `--lx-color-ink` | `#17212B` | Primärtext | auf Canvas 14,95:1 | deaktivierter Text |
| `--lx-color-ink-muted` | `#4B5967` | Sekundärtext | muss in Implementierung mindestens 4,5:1 halten | Pflichtkriterium verstecken |
| `--lx-color-line` | `#A7B0B8` | strukturelle Grenzen | zusätzlich durch Fläche/Abstand gestützt | einziger Bedeutungsunterschied |
| `--lx-color-action` | `#005A70` | Primäraktion und aktive Beziehung | Weiß darauf 7,79:1 | Fortschritt/Kompetenz codieren |
| `--lx-color-action-strong` | `#003F52` | Hover/Pressed | Weiß darauf wird vor Merge maschinell geprüft | Gefahr oder Erfolg codieren |
| `--lx-color-focus` | `#D97706` | 3-Pixel-Fokusoutline | gegen Weiß 3,19:1; gegen Ink 5,11:1 | Fließtext auf Weiß |
| `--lx-color-info-*` | Text `#0B3A82`, Fläche `#EAF2FF` | RES-INFO, Kontextinformation | 9,60:1 | Erfolg oder Freigabe |
| `--lx-color-confirmed-*` | Text `#246B47`, Fläche `#EAF6EE` | technisch/fachlich bestätigter Stand | 5,79:1 | Kompetenzurteil oder Belohnung |
| `--lx-color-warning-*` | Text `#7A4B00`, Fläche `#FFF4D6` | RES-LIMIT, Entscheidung nötig | 6,76:1 | Fehlversuch der Person |
| `--lx-color-danger-*` | Text `#9B1C31`, Fläche `#FDECEF` | RES-BLOCK, irreversible Datenhandlung | 7,07:1 | fachliche Abweichung allein |

Farbe ist nie alleiniger Bedeutungsträger. Jede Rolle besitzt Text, Icon oder strukturelle Kennzeichnung. Fachliche Ausgangs- und Revisionsstände werden durch Labels, Überschriften und Beziehungslinien unterschieden, nicht durch Rot/Grün.

### 8.3 Typografierollen

- Grundschrift: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
- Code, Befehle und Zustandsdaten: `ui-monospace, "Cascadia Mono", Consolas, monospace`;
- Fließtext: `1rem` bei `1.6` Zeilenhöhe, maximal `68ch`;
- Kontexttext: mindestens `0.9375rem` bei `1.45`;
- Haupttitel: `clamp(2rem, 5vw, 3.5rem)`;
- Zustandsüberschrift: `clamp(1.5rem, 3vw, 2.25rem)`;
- Abschnittsüberschrift: `clamp(1.25rem, 2vw, 1.625rem)`;
- Mindestgröße sichtbarer Pflichtcopy: `0.9375rem`; keine 12-Pixel-Hilfstexte;
- Versalien nur für kurze Eyebrow-/Statuslabels, niemals für Aufträge oder Rückmeldung.

Eigene Webfonts werden in Fassung 1 nicht benötigt. Eine spätere Fontänderung ist ein LXP04-Change, weil Metrik, Reflow, Dichte und Offlinebundle erneut geprüft werden müssen.

### 8.4 Raum-, Form- und Tiefenrollen

- Basiseinheit: `0.25rem`;
- Abstände: `0.25`, `0.5`, `0.75`, `1`, `1.5`, `2`, `3`, `4rem`;
- enge semantische Gruppe: `0.5–0.75rem`;
- Patternabschnitt: `1–1.5rem`;
- Trennung fachlicher Zusammenhänge: `2–3rem`;
- Aktionsziel: mindestens `2.75rem × 2.75rem` beziehungsweise 44 × 44 CSS-Pixel;
- Radius klein `0.375rem`, mittel `0.75rem`, groß `1.25rem`;
- Schatten nur für modale Überlagerung oder echte Ebenentrennung; normale Arbeitsflächen nutzen Linie, Fläche und Abstand;
- höchstens drei gleichzeitige Flächenebenen: Canvas, Surface, hervorgehobene fachliche Beziehung.

### 8.5 Bewegung

- Zustandswechsel standardmäßig ohne räumliche Metapher;
- optionale Mikrotransition `120ms` für Fokus-/Disclosure-Rückmeldung;
- optionale Bereichstransition `180ms` für nichtfachliche Offenlegung;
- keine automatische Weganimation, kein Parallax, kein Konfetti und kein animierter Fortschritt;
- `prefers-reduced-motion: reduce` setzt Animation und Transition auf `0s` und erhält identische Reihenfolge, Copy, Status- und Fokusfolge;
- Bewegung darf nie die erste oder einzige Erklärung einer Zustandsänderung sein.

## 9. Kompositions- und Responsivevertrag

### 9.1 Gemeinsame Anatomie

Jeder Lernstudio-Moment besitzt dieselbe funktionale Reihenfolge:

```text
Skip-Link und globaler Produktkontext
→ Kontextband
→ Lernzustandsüberschrift mit Ziel, Handlung und Kriterium
→ Fokusbühne mit fachlicher Beziehung
→ kontextnahe Rückmeldung oder Hilfe, wenn aktuell
→ Aktionskante
→ nachrangige Lernweg-, Daten- und Lehrkraftzugänge
```

Die Reihenfolge gilt im DOM und in der Text-/AT-Ausgabe. Wide darf zusammengehörige Teile nebeneinander anordnen, aber die semantische und Tastaturreihenfolge bleibt erhalten.

### 9.2 Kompositionsbudgets

| Funktion | verbindliches Budget | Fail-Signal |
|---|---|---|
| Primärhandlung | genau eine sichtbare Primäraktion pro fachlich vollständigem Moment | zwei gleichgewichtige Calls-to-action oder generisches `weiter` |
| sichere Geschwisterhandlungen | höchstens zwei direkt sichtbar; weitere bedarfsgerecht | Aktionskante wird zur Toolbar |
| aktuelle fachliche Frage | genau eine; kurze Kontextzeile möglich | Leitfrage konkurriert mit Modulbeschreibung |
| Qualitätskriterium | mindestens eines vor Handlung sichtbar; höchstens drei gleichzeitig | Kriterium erscheint erst nach Entscheidung |
| Fokusbühne | ein dominanter Beziehungszusammenhang | mehrere unverbundene Arbeitskarten mit gleichem Gewicht |
| kontextnahe Hilfe | eine geöffnete Hilfeschicht; weitere geschlossen erreichbar | alle Hilfen gleichzeitig oder Lösung vor Strategie |
| technische Normalinformation | eine nachrangige Textzeile oder Statuszugang | Speicher/Verbindung steht vor Ziel und Handlung |
| Fließtext | maximal 68 Zeichenbreiten; längere Erklärungen in eigenem Kontext | Vollbreitentext oder Scrollwand in Fokusbühne |

### 9.3 Größenklassen

Komponenten reagieren auf die verfügbare Containerbreite, nicht auf Gerätetypen:

- **compact:** unter `40rem`; eine Spalte, Quellkontext vor Eingabe, Aktionskante im Fluss;
- **standard:** `40rem` bis unter `70rem`; eine oder zwei Spalten nur bei erhaltener Ursache-Wirkung-Beziehung;
- **wide:** ab `70rem`; maximal drei funktionale Regionen, davon genau eine Fokusbühne;
- globale Inhaltsbreite maximal `76rem`, Lesespalte maximal `68ch`.

Der Basispfad ist compact. `@container`-Regeln dürfen Standard/Wide ergänzen; ohne Container-Query-Unterstützung bleibt die einspaltige Folge vollständig nutzbar.

### 9.4 Wide-Regeln

Nebeneinander ist nur zulässig für fachlich zu vergleichende oder kausal verbundene Darstellungen:

- Erwartung ↔ beobachtete Wirkung;
- Ausgang ↔ Revision;
- Quelle/Beleg ↔ Deutung;
- Modell ↔ Daten/Fall;
- Arbeitsprodukt ↔ Qualitätskriterium.

Navigation, Hilfe, Technikstatus oder Lehrkraftinformation dürfen keine gleichrangige dritte Spalte neben einer bereits komplexen Fachbeziehung bilden.

### 9.5 Compact- und Reflow-Regeln

- Quell- und Ausgangskontext steht vor der darauf bezogenen Eingabe.
- Befehl, Vorzustand und Nachzustand bleiben als vollständige Schrittgruppe zusammen.
- Nach einer Eingabe bleibt ein benannter Rücksprung zur Quelle verfügbar.
- Keine horizontale Seitennavigation; fachliche Tabellen werden in semantische Gruppen umgebrochen oder erhalten einen beschrifteten lokalen Scrollbereich.
- Sticky-Aktionen sind nur zulässig, wenn sie keinen Inhalt verdecken, bei 200 Prozent Zoom funktionieren und im DOM an ihrer logischen Position verbleiben.
- Gesamtkarte, Hilfen und Datenhandlungen dürfen den kritischen Pfad nicht vorlesen oder fokussieren, solange sie geschlossen sind.

## 10. Komponenten- und Patternkatalog

### 10.1 Grundkomponenten

| Komponente | Zweck und Pflichtinhalt | Varianten/Zustände | Semantik und Fokus | nicht verwenden für |
|---|---|---|---|---|
| `ExperienceShell` | Produktkontext, Skip-Link, Hauptinhalt, nachrangiger globaler Zugang | `cosmos`, `studio`, `secure` | `main` besitzt Fokusziel; Landmarknamen eindeutig | Lernzustand oder technische Alarmmeldung |
| `ContextBand` | Ziel, Herkunft, Position, Modus, handlungsrelevanter Status | `normal`, `resume`, `teacher-led`, `recovery` | kurze Liste; kein `role=status` im Normalmodus | vollständige Breadcrumb-, Fortschritts- oder Statuswand |
| `LearningStateHeader` | kontrolliertes Zustandslabel, fachliche Frage, aktuelle Handlung, Kriterium | elf LXP02-Zustände | `h1`/`h2` nach Seitenkontext; Fokus nach Zustandswechsel | lange Aufgabenbeschreibung |
| `FocusStage` | aktuelle fachliche Beziehung und Lernprodukt | `single`, `compare`, `cause-effect`, `source-interpretation` | `section` mit eindeutiger Überschrift; DOM-Reihenfolge stabil | beliebige Kartenansammlung |
| `ActionEdge` | Primäraktion, bis zu zwei sichere Geschwister, Guard-/Folgenhinweis | `ready`, `guarded`, `busy`, `blocked` | Aktion nennt Ergebnis/Objekt; Guardcopy programmatisch zugeordnet | generisches `weiter`, globale Toolbar |

### 10.2 Orientierung und Navigation

| Komponente | Vertrag | erlaubte Varianten | Fail-Signal |
|---|---|---|---|
| `StartBoard` | Leitfrage, erwartbare Handlungsfähigkeit, Zeitkorridor, Sozialform, lokale Startoption und genau eine nächste Aktion | `new`, `resume`, `teacher-led`, `recover` | mehrere gleichgewichtige Starts, Technikstatus vor Lernziel |
| `JourneyMap` | Unterrichtseinheiten, Lernphasen, aktuelle Funktion, erlaubte Rückkehr und Anschluss | `overview`, `current-context`, `blocked-link` | Prozent-/Seitenfortschritt oder unguarded free navigation |
| `ResumePrompt` | Zielrekonstruktion, letzter bestätigter Stand, offene Handlung, nächste Aktion | `short`, `active-recall`, `version-conflict` | alte Vollarbeit vor aktivem Abruf oder versteckter Konflikt |

### 10.3 Fachliche Lernhandlung

| Komponente/Pattern | Pflichtvertrag | Portabilitätsgrenze |
|---|---|---|
| `PredictionForm` | Erwartung vor Wirkung; strukturierte oder knappe Eingabe; unbewertet; fachlich notwendige Felder | Feldtypen werden pro Domäne spezifiziert; nicht jede Handlung braucht Position/Richtung |
| `SemanticModelView` | visuelle und textliche Darstellung aus derselben semantischen Quelle; Kontrolle-Wirkung-Bezug | IUM5-Raster, Quelle, Datensatz oder Medienprodukt sind Renderer-Slots |
| `EvidenceView` | auswählbarer Beleg mit Herkunft, Zustand, Kriterium und unverändertem Snapshot | lineare Laufspur ist nur eine Variante |
| `EvidenceFeedback` | Ergebnis, relevante Stelle/Quelle, Kriterium, nächster Prüfschritt; keine Personenwertung | Mehrdeutigkeit und konkurrierende Belege müssen möglich sein |
| `RevisionCompare` | autoritativer Ausgang, ausgewählter Beleg, gezielte Änderung, Revision und erneute Prüfbedingung | nichtlineare/mediale Produkte benötigen passende Vergleichsrenderer |
| `EvidenceCardComposer` | Quelle–Beleg–Deutung–Revision–Kernaussage–Modellgrenze; keine zweite Vollerzählung | Pflichtfelder folgen Lernhandlungsart, nicht universellem Kartenlayout |
| `TransferPrompt` | neuer Fall zuerst, eigene Entscheidung, Bezug zum gesicherten Konzept und Grenze | darf keine Oberflächenvariation des Ausgangsfalls sein |
| `ReentryRecall` | kurze eigene Abrufantwort vor alter Vollanzeige; neue Antwort bleibt getrennt | Zeitgrenze und Aufgabenformat kommen aus Modulvertrag |

### 10.4 Unterstützung und Orchestrierung

| Komponente/Pattern | Pflichtvertrag | Grenze |
|---|---|---|
| `SupportDisclosure` | getrennte Bedien-, Begriffs- und Strategiehilfe; bewusste Öffnung; Fokus zurück; keine Nutzungsprotokollierung | vollständiges Beispiel ist eigene letzte Eskalationsstufe |
| `TeacherCheckpoint` | Anlass, erwartbare gewöhnliche Evidenz, Frage/Intervention, neutraler Fallback, Rückkehrzustand und Ausstiegskriterium | keine privaten Gerätestände oder personenbezogene Daten |
| `RoleExchange` | zwei fachlich aktive Rollen, Wechsel nach benanntem Teilschritt, gemeinsames Produkt/Beleg | nicht global für individuelle Sicherung erzwingen |
| `SharedHold` | transparente Pause für Austausch/Sicherung, lokaler Stand bleibt, Rückkehrhandlung eindeutig | keine Fernsteuerung oder automatische Projektion privater Arbeit |

### 10.5 Resilienz und Datenhoheit

| Komponente | Pflichtvertrag | Varianten | Fail-Signal |
|---|---|---|---|
| `SaveIndicator` | letzter bestätigter Stand und aktuelle Speicherfähigkeit | `saved`, `saving`, `volatile`, `failed` | behaupteter Erfolg oder Dominanz im Ruhemodus |
| `ResilienceNotice` | betroffene Arbeit, Erhalt, Konsequenz, sichere Primärhandlung, Rückweg | `info`, `limit`, `block` | Farbe allein, tote Aktion oder unklare Datenfolge |
| `DataActionDialog` | Gegenstand, Reichweite, Sensitivität, Eigentümerschaft, sichere Standardaktion | `export`, `import`, `delete-card`, `delete-module` | voreingestelltes Teilen, Teilimport, ungenaue Löschung |
| `RecoveryPanel` | Originalerhalt, Versions-/Integritätsbefund, zulässige Optionen und unveränderte Rückkehr | `read-export`, `validated-copy`, `retry`, `pause` | stille Migration, Merge oder Überschreibung |

### 10.6 Verschachtelungsregeln

- `ExperienceShell` enthält genau einen aktuellen `LearningStateHeader` und höchstens eine primäre `FocusStage`.
- `FocusStage` darf `SemanticModelView`, `EvidenceView`, `PredictionForm` oder `RevisionCompare` kombinieren, aber nicht gleichzeitig alle Patternfamilien.
- `ActionEdge` gehört semantisch zum aktuellen Lernmoment und liegt außerhalb modaler Dialoge.
- `SupportDisclosure` darf keinen neuen Lernzustand erzeugen.
- `TeacherCheckpoint` erscheint lernendenseitig nur als Haltepunkt/Arbeitsform, nicht mit Lehrkraftinternas.
- `ResilienceNotice` darf `ActionEdge` nur bei `limit` oder `block` ersetzen; `info` bleibt nachrangig.
- Datenhandlungen liegen in einem stabilen Datenbereich oder bewussten Dialog, nie als Abschlussbelohnung.

## 11. Interaktions- und Zustandsmuster

### 11.1 Zustandskomposition

| LXP02-Zustand | dominante Beziehung | Primärhandlung | Fokus nach Eintritt | Guard/Fallthrough |
|---|---|---|---|---|
| `LS-ORIENT` | Ziel ↔ Position ↔ nächster Schritt | Kontext klären oder Abrufantwort beginnen | Zustandsüberschrift | Voraussetzungen/Stand verständlich, sonst Recovery |
| `LS-READY` | Bedingungen ↔ Startfolge | Lernhandlung beginnen | erste fachliche Überschrift | Kern lokal und Ziel/Sozialform geklärt |
| `LS-DECIDE` | Denkobjekt ↔ Erwartung/Entscheidung | Erwartung festhalten | erste Eingabe | notwendige Felder vollständig, unbewertet |
| `LS-ACT` | Handlung ↔ veränderbares Modell/Produkt | gezielt handeln | aktive Kontrolle oder Arbeitsregion | Entscheidung liegt vor, Fachsystem validiert |
| `LS-OBSERVE` | Handlung ↔ beobachtete Wirkung/Beleg | relevanten Beleg wählen | Wirkung/Statusüberschrift | Wirkung vollständig und gleichwertig verfügbar |
| `LS-INTERPRET` | Erwartung ↔ Beleg ↔ Kriterium | Bedeutung/erste Abweichung prüfen | Feedbacküberschrift | Beleg ist Handlung zugeordnet, Lösung bleibt offen |
| `LS-REVISE` | Ausgang ↔ Beleg ↔ Änderung | Revision begründen und bestätigen | editierbare Revision | Änderung bezieht sich auf Beleg; Undo vorhanden |
| `LS-SECURE` | Produkt ↔ Beleg ↔ Kernaussage/Grenze | Sicherungsartefakt bestätigen | erste offene Sicherungsanforderung | reale Produktspur, kein Systemstatus als Beleg |
| `LS-TRANSFER` | gesichertes Konzept ↔ neuer Fall | auf veränderten Fall übertragen | neuer Fall | eigene Entscheidung vor alter Lösung |
| `LS-PAUSE` | bestätigter Stand ↔ offene Handlung | sicher pausieren/fortsetzen | Pausenüberschrift bzw. Rückkehranker | Speicherehrlichkeit, kein unbestätigter Erfolg |
| `LS-RECOVER` | Original ↔ Konflikt ↔ sichere Option | Recovery wählen | Problemüberschrift | keine Mutation vor vollständiger Validierung |

### 11.2 Guardbasierter Übergang

Jeder Übergang besitzt:

1. Ausgangszustand und fachlichen Anlass;
2. sichtbare Guardbedingung;
3. genau eine autoritative Aktion;
4. atomare Mutation oder ausdrücklich keine Mutation;
5. Statusmeldung mit Ergebnis und nächstem Kontext;
6. Fokusziel im neuen oder erhaltenen Zustand;
7. sicheren Abbruch-/Rückweg;
8. Persistenzentscheidung ohne Verhaltensprotokoll.

Deaktivierte rätselhafte Buttons sind kein Ersatz für Guardcopy. Wenn eine spätere Aktion noch nicht verfügbar ist, erklärt der aktuelle Zusammenhang, welche fachliche Vorbedingung sie öffnet.

### 11.3 Evidenzgebundene Rückmeldung

Rückmeldung folgt einer geschlossenen Grammatik:

```text
Ergebnis oder Zustand
→ relevante Stelle, Quelle oder Beziehung
→ Bezug zu Erwartung und Kriterium
→ nächste fachliche Prüffrage
→ optionale strategische Hilfe
→ vollständiges Beispiel nur nach bewusster Eskalation
```

`richtig/falsch`, Ampel, Punkte, Personlob oder ein grüner Lauf ohne fachliche Information bestehen den Vertrag nicht. Erfolgreiche erste Fassungen erhalten einen neutralen Kontrast- oder Grenzfall, wenn Revision zur Lernhandlung gehört.

### 11.4 Ausgang-/Revisionsvergleich

- Ausgang bleibt lesbar und autoritativ.
- Revision ist editierbar und visuell wie semantisch benannt.
- Der ausgewählte Beleg verweist auf konkrete Quelle/Stelle.
- Änderung und Begründung sind verbunden.
- erneute Ausführung oder Prüfung erfordert eine neue Erwartung, wenn die inhaltliche Revision die Wirkung ändert.
- Vollhistorien und Versuchszähler sind ausgeschlossen.

### 11.5 Hilfe mit Fokus-Rückkehr

Hilfestufen:

1. **Bedienhilfe:** Wie wird die vorhandene fachliche Handlung ausgeführt?
2. **Begriffshilfe:** Welcher Begriff oder welche Darstellung muss verstanden werden?
3. **Strategiehilfe:** Welcher Vergleich oder Prüfschritt ist sinnvoll?
4. **Beispiel:** vollständiger, fachlich anderer Fall nach bewusster Eskalation.

Beim Schließen kehrt der Fokus zum auslösenden Element zurück. Öffnung, Stufe und Nutzungsdauer werden nicht gespeichert.

### 11.6 Lehrkraft-Haltepunkt und Rollenwechsel

Ein Haltepunkt enthält im Inhaltsvertrag:

- fachlichen Anlass;
- erwartbaren Zeitkorridor;
- sichtbares Signal für Lernende;
- gewöhnliche Evidenz aus Produkt, Erklärung, Handzeichen oder neutralem Fall;
- mögliche Lehrkraftfrage/Intervention;
- Fallback ohne private Geräteeinsicht;
- erlaubten Rückkehrzustand;
- klares Ausstiegskriterium.

Bei 1:2-Arbeit benennt `RoleExchange` die fachliche Verantwortung beider Rollen und den Wechselmoment. Keine Person bleibt dauerhaft Bedienerin oder Zuschauer.

### 11.7 Aktive Wiederaufnahme

- kurze Unterbrechung: letzter bestätigter Zustand, offene Handlung und nächster Schritt;
- längere Unterbrechung: kurze Abruffrage und eigene Antwort vor alter Vollanzeige;
- Versionkonflikt: Original lesen/exportieren oder vollständig validierte Kopie; keine Teilmigration;
- neue Abrufantwort bleibt von der alten Belegkarte getrennt und ist kein automatisches Update der Karte.

## 12. Inhalts- und Copyverträge

### 12.1 `ExperienceContentV1`

Jedes Modul stellt einen validierten LXP-Inhaltsvertrag bereit:

```ts
type ExperienceContentV1 = Readonly<{
  schemaVersion: 1;
  moduleId: string;
  terminologyVersion: 'lxp04-1';
  start: StartBoardSpec;
  actions: readonly LearningActionSpec[];
  tasks: readonly LearningTaskSpec[];
  feedback: readonly FeedbackSpec[];
  supports: readonly SupportSpec[];
  checkpoints: readonly TeacherCheckpointSpec[];
  evidenceCards: readonly EvidenceCardSpec[];
  resilience: readonly ResilienceSpec[];
}>;
```

Der Vertrag ergänzt, aber dupliziert nicht Modulmanifest, Fachressourcen oder persistenten Lernpayload.

`StartBoardSpec` ist ebenfalls geschlossen:

~~~ts
type StartBoardSpec = Readonly<{
  heading: string;
  guidingQuestion: string;
  expectedCapability: string;
  timeWindowMinutes: readonly [number, number];
  socialForm: 'individual' | 'pair' | 'group' | 'plenary';
  primaryAction: Readonly<{ label: string; result: string }>;
  resumeAction: Readonly<{ label: string; purpose: string }> | null;
  resetAction: Readonly<{ label: string; consequence: string }> | null;
}>;
~~~

### 12.2 `LearningActionSpec`

```ts
type LearningActionSpec = Readonly<{
  id: string;
  state: LearningStateId;
  taskId: string;
  purpose: string;
  prompt: string;
  product: string;
  criteria: readonly string[];
  primaryAction: Readonly<{ label: string; result: string }>;
  secondaryActions: readonly Readonly<{ label: string; purpose: string }>[];
  requiredEvidence: readonly string[];
  supportIds: readonly string[];
  checkpointId: string | null;
  persistence: 'none' | 'draft' | 'confirmed-product' | 'evidence';
  next: readonly Readonly<{ state: LearningStateId; guard: string }>[];
}>;
```

`prompt` fordert eine fachliche Handlung, keine bloße Bedienaktion. `primaryAction.label` nennt Ergebnis oder Objekt, zum Beispiel `Vorhersage festhalten`, `erste Abweichung prüfen` oder `Belegkarte sichern`.

### 12.3 Aufgabenvertrag

Jede zentrale Aufgabe folgt diesem geschlossenen Teilvertrag:

~~~ts
type LearningTaskSpec = Readonly<{
  id: string;
  learningGoal: string;
  purpose: string;
  thinkingAction: string;
  product: string;
  materialRefs: readonly string[];
  criteria: readonly string[];
  requiredEvidence: readonly string[];
  supportIds: readonly string[];
  feedbackId: string;
  socialForm: 'individual' | 'pair' | 'group' | 'plenary';
  roleIds: readonly string[];
  persistence: 'none' | 'draft' | 'confirmed-product' | 'evidence';
  offlineRequirement: 'core' | 'enhancement';
  recoverySpecId: string;
}>;
~~~

Damit benennt jede zentrale Aufgabe:

- fachliches Ziel und beobachtbares Produkt;
- Sinn oder Funktion im Lernweg;
- aktuelle Denkhandlung;
- Material/Quelle/Repräsentation;
- Qualitätskriterium vor der Handlung;
- Belegpflicht;
- Hilfe ohne Übernahme der Kernhandlung;
- Diagnose-/Feedbackpunkt;
- Sozialform und Rollen, falls relevant;
- Persistenz-, Offline- und Recoveryfolge.

Eine Aufgabe fällt durch, wenn sie nur Inhalt anzeigt, Klicks sequenziert, generischen Freitext sammelt oder ein digitales Tool ohne Lernfunktion verwendet.

### 12.4 Feedbackvertrag

```ts
type FeedbackSpec = Readonly<{
  id: string;
  result: string;
  evidenceRef: string;
  criterion: string;
  interpretationPrompt: string;
  nextCheck: string;
  strategySupportId: string | null;
  exampleSupportId: string | null;
}>;
```

Feedbacktext ist auf Aufgabe, Prozess, Kriterium oder Selbstregulation bezogen, nie auf die Person. Er ermöglicht unmittelbare Weiterarbeit. Sozialer Vergleich, Notensprache und pauschales Lob sind ausgeschlossen.

### 12.5 Hilfevertrag

```ts
type SupportSpec = Readonly<{
  id: string;
  kind: 'operation' | 'concept' | 'strategy' | 'example';
  title: string;
  trigger: string;
  content: string;
  preservesAction: string;
  nextSupportId: string | null;
}>;
```

`preservesAction` erklärt, welche fachliche Eigenleistung bei Lernenden bleibt. Ein Beispiel verwendet einen anderen Fall und darf den aktuellen Beleg oder die aktuelle Lösung nicht eintragen.

### 12.6 Belegkartenvertrag

```ts
type EvidenceCardSpec = Readonly<{
  id: string;
  actionKind: 'predict-test' | 'create-revise' | 'analyze-judge' | 'secure-transfer';
  requiredFields: readonly EvidenceFieldId[];
  modelBoundaryPrompt: string;
  transferPromptId: string | null;
  reentryPromptId: string | null;
}>;
```

Die stabilen Beziehungen sind Kontext, eigene Entscheidung/Modell, Handlung/Test, beobachteter Effekt/Beleg, Interpretation, Revision, Kernaussage/Modellgrenze und Transfer. Eine visuelle Universalkarte und dieselben Pflichtfelder für alle Lernhandlungen sind ausdrücklich nicht Teil des Vertrags.

### 12.7 Lehrkraftvertrag

```ts
type TeacherCheckpointSpec = Readonly<{
  id: string;
  state: LearningStateId;
  purpose: string;
  timeWindowMinutes: readonly [number, number];
  socialForm: 'individual' | 'pair' | 'group' | 'plenary';
  learnerSignal: string;
  ordinaryEvidence: readonly string[];
  teacherPrompt: string;
  neutralFallback: string;
  returnState: LearningStateId;
  exitCriterion: string;
}>;
```

### 12.8 Copyregeln

- sichtbare Labels verwenden den kontrollierten LXP02-Wortschatz;
- Verben benennen fachliche Wirkung: `vergleichen`, `vorhersagen`, `prüfen`, `begründen`, `revidieren`, `sichern`, `übertragen`;
- `weiter`, `fertig`, `abschließen`, `Erfolg`, `Fehler` oder `richtig` benötigen ein fachliches Objekt oder Kriterium;
- Sätze sind direkt, respektvoll und nicht infantilisierend;
- technische Meldungen nennen betroffene Arbeit, Erhalt, Folge, sichere Handlung und Rückweg;
- keine Pflichtcopy setzt Farbwahrnehmung, räumliche Position oder Animation voraus;
- Fachbegriffe werden kontextsensitiv erklärt, nicht durch dauerhafte Vereinfachung ersetzt.

Die Inhaltsvalidatoren zählen Unicode-Codepoints und erzwingen folgende Obergrenzen:

| Feldfamilie | Maximum |
|---|---:|
| Überschrift, Hilfe- oder Aktionslabel | 72 |
| Kriterium, Ergebnis, Folge oder Rücksprung | 240 |
| fachlicher Zweck, Prompt, Produkt, Beleganforderung oder Recoverymeldung | 600 |
| Hilfeinhalt | 1.200 |

Leer getrimmte Pflichttexte, unbekannte Felder, doppelte IDs und nicht auflösbare Referenzen werden fail-closed abgelehnt.

## 13. Accessibility- und Gleichwertigkeitsvertrag

### 13.1 Technische Baseline

- WCAG 2.2 AA bleibt Zielstandard, aber Konformität wird erst in LXP06 behauptet;
- zentrale Pfade funktionieren mit Tastatur, Touch und Text-/Assistive-Technology;
- keine Kernhandlung verlangt Drag-and-drop, Hover, Farbe, Bewegung oder feinmotorische Geste;
- Reflow bei 320 CSS-Pixeln und Nutzung bei 200 Prozent Zoom ohne horizontalen Seitenüberlauf;
- sichtbare Aktionen mindestens 44 × 44 CSS-Pixel;
- Fokusindikator mindestens 3 CSS-Pixel und gegen angrenzende Fläche mindestens 3:1;
- Reduced Motion deaktiviert alle nicht notwendigen Übergänge vollständig;
- automatisch erkennbare Prüfungen werden durch manuelle Tastatur-, Screenreader-, Reflow-, Zoom-, Kontrast- und Kognitionschecks ergänzt.

### 13.2 Funktionsgleichwertigkeit

Ein alternativer Pfad ist nur gleichwertig, wenn er:

- dasselbe Ziel und dieselbe zentrale Entscheidung verlangt;
- dieselben Guards und Konsequenzen besitzt;
- dieselbe Quelle, Evidenz und Modellgrenze verfügbar macht;
- vergleichbare Rückmeldung und Revision ermöglicht;
- denselben persistenten Produktvertrag erzeugt;
- keine Lösung früher offenlegt oder fachliche Schwierigkeit senkt.

### 13.3 Fokusvertrag

- Zustandswechsel fokussiert die neue Zustandsüberschrift, nicht den Dokumentanfang.
- Inline-Aktionen behalten Fokus, wenn nur Status oder Inhalt aktualisiert wird.
- Fehlerfokus geht zur ersten reparierbaren Stelle oder zu einer Zusammenfassung mit Rücklinks.
- Disclosure-Schließen kehrt zum Auslöser zurück.
- Dialoge erhalten initial Fokus auf Titel oder sichere Standardaktion; `Esc` bricht nichtdestruktiv ab.
- Nach Dialogschluss kehrt Fokus zum Auslöser oder zum benannten Folgeziel zurück.
- Gesamtkarte kehrt exakt zum Öffnungspunkt zurück und verändert keinen Lernstand.
- Statusmeldungen dürfen Fokus nicht für jede Speicheraktualisierung verschieben.

### 13.4 Status- und Live-Regionen

- `polite`: Speichern, bestätigte lokale Aktion, nachrangiger Zustandswechsel;
- fokussierte Überschrift statt Live-Region: neuer fachlicher Lernzustand;
- `alert`: Datenverlustgefahr, blockierte Kernhandlung, abgewiesener Import oder fehlgeschlagene irreversible Aktion;
- visuelle Szene, Textdarstellung und Statusmeldung stammen aus derselben semantischen Quelle;
- keine parallelen Live-Regionen melden denselben Vorgang mehrfach.

### 13.5 Kognitive Accessibility

- Zweck, aktuelle Handlung, Kriterium und nächster Schritt sind benennbar;
- kritische Pfade sind kurz und rückkehrbar;
- notwendige Quelle bleibt erreichbar, ohne Erinnerung an verborgene Zustände zu verlangen;
- Begriffe und Komponentenpositionen bleiben konsistent;
- progressive Offenlegung verbirgt keine Voraussetzung, Folge oder irreversible Handlung;
- Hilfen sind kontextnah, abgestuft und übernehmen nicht die fachliche Entscheidung;
- Wiedereinstieg rekonstruiert Ziel und offenen Schritt, keine Lernendenbiografie.

## 14. Local-First-, Offline-, Fehler- und Datenvertrag

### 14.1 Schweregrade

| Schwere | Bedeutung | Darstellung | Aktion |
|---|---|---|---|
| `RES-INFO` | normale Information; aktuelle Fachhandlung bleibt vollständig | nachrangiger Status im Kontextband oder Datenbereich | keine Unterbrechung |
| `RES-LIMIT` | eine konkrete Option fehlt; gleichwertiger Kern bleibt | kontextnahes `ResilienceNotice` mit betroffener Handlung | sichere Alternative, Retry oder Pause |
| `RES-BLOCK` | Kernfunktion, Integrität oder Datenhoheit nicht sicher | fokussierter Recoverybereich, aktuelle Aktion gesperrt | Original erhalten, Export/Recovery/Abbruch |

### 14.2 Pflichtfelder von `ResilienceSpec`

```ts
type ResilienceSpec = Readonly<{
  code: string;
  severity: 'info' | 'limit' | 'block';
  affectedWork: string;
  preservedState: string;
  consequence: string;
  primaryAction: string;
  secondaryAction: string | null;
  returnTarget: string;
}>;
```

### 14.3 Experience-Invarianten

- Der letzte bestätigte Stand ist autoritativ.
- Flüchtige Eingabe wird als flüchtig benannt und darf nicht als gespeichert gelten.
- Offlinebereitschaft wird nur für tatsächlich vorhandenen Kern und Assets behauptet.
- Eine nicht verfügbare Aktion bleibt nicht scheinbar funktionsfähig.
- Import wird vollständig vor Mutation validiert; Übernahme ist atomar.
- Inkompatible Versionen bleiben unverändert les-/exportierbar oder werden vollständig migriert; keine Teilverschmelzung.
- Löschung nennt Reichweite, Abhängigkeiten und Irreversibilität; Standard ist Abbrechen.
- Export nennt Umfang, Freitextsensitivität, lokale Eigentümerschaft und Zielhandlung; kein automatisches Teilen.
- Konto, Backend, Telemetrie, Klick-, Zeit-, Versuch-, Hilfe-, Scroll- oder Fokushistorie bleiben ausgeschlossen.

### 14.4 Verhältnis zu `@ium/ui-components`

`ConnectionStatus`, `StorageStatus`, `UpdatePrompt`, `ErrorSummary` und `DataControls` werden nicht unverändert in den primären Lernraum gestellt. LXP05 adaptiert sie über das Experience-System:

- Normalstatus fließt nachrangig in `ContextBand`/`SaveIndicator`;
- handlungsbegrenzender Status wird `ResilienceNotice`;
- blockierender Status wird `RecoveryPanel` oder `ErrorSummary` mit fachlichem Rückweg;
- Datenhandlungen bleiben im stabilen Datenbereich oder `DataActionDialog`;
- technische Events werden in Experience-Schwere, Copy und Fokusfolge übersetzt.

## 15. Lernwirksamkeit, Lehrkraftorchestrierung und WU-Check

### 15.1 Quellenstatus

Der WU-Check nutzt das geprüfte lokale Planungsmanifest sowie die IBBW-Exzerpte:

- Band 1: Angebots-Nutzungs-Modell, Sicht-/Tiefenstrukturen und Orchestrierung;
- Band 5: formatives Feedback als Lernstand–Ziel–nächster Schritt;
- Band 6: Aufgaben als fachliche Handlungsaufforderung mit Validität, Sinn, Aktivierung und Adaptivität;
- Band 9: digitaler Mehrwert nur über Aktivierung, Unterstützung oder Struktur.

Die Exzerpte sind Orientierungsrahmen. LXP04 behauptet weder empirische Wirksamkeit des Produkts noch reale Passung zur Lerngruppe. Fachprofil und Curriculum bleiben im dokumentierten Reifegrad; LXP05 und LXP06 müssen konkrete Inhalte und Unterrichtsabläufe erneut prüfen.

### 15.2 Systemweiter WU-Check

| Prüffeld | LXP04-Vertrag | Gate für LXP05/LXP06 |
|---|---|---|
| Kognitive Aktivierung | `LearningActionSpec` verlangt fachliche Entscheidung, Handlung, Beleg und gegebenenfalls Revision | kein Slice besteht nur aus Lesen, Klicken oder Formularerfüllung |
| Konstruktive Unterstützung | Hilfen sind hürdenspezifisch, abgestuft und bewahren die Kernhandlung | Strategie-/Beispielhilfe wird fachlich auf Lösungsoffenlegung geprüft |
| Klassenführung/Struktur | Kontextband, Zustand, Haltepunkte, Zeitkorridore, Rollen und sichere Pause bilden einen Unterrichtsrhythmus | Lehrkraft kann Start, Halt, Austausch und Sicherung ohne Dashboard durchführen |
| Aufgabenqualität | Ziel, Sinn, Denkhandlung, Produkt, Kriterium, Beleg und Adaptivität sind Pflichtfelder | jede IUM5-Aufgabe trifft das intendierte Lernziel und hält Anspruch im Reflow-/Alternativpfad |
| Feedback/Diagnose | Evidenzfeedback verbindet Lernstand, Ziel/Kriterium und nächsten Prüfschritt | Feedback ermöglicht direkte Revision; kein richtig/falsch, Personlob oder soziale Norm |
| Kooperation/Verantwortlichkeit | Rollen benennen fachliche Teilhandlungen und Wechselmomente | 1:2-Pfad verhindert dauerhafte Bedien-/Zuschauerrolle |
| Diagnose-Fallback | `TeacherCheckpointSpec` enthält neutralen Fall und gewöhnliche Evidenz | fehlende private Evidenz wird nie durch erfundene Systemdiagnostik ersetzt |
| Sprachliche/kognitive Zugänglichkeit | kontrollierter Wortschatz, Copyregeln, Fokus, Reflow, Hilfen und Quellenbezug | Fachsprache bleibt präzise und wird kontextuell gestützt |
| Digitaler Mehrwert | deterministische/semantische Rückkopplung, Revision, Local First, Wiederaufnahme und gleichwertige Pfade | jeder digitale Mechanismus benennt die verbesserte Tiefenstruktur |
| Wichtigste Verbesserung | heutige Mega-Seite wird durch guardbasierte Fokuskomposition ersetzt | Browserwalkthrough zeigt Ursache–Wirkung ohne Scrollsuche oder Erinnerungsbruch |

### 15.3 Eigenleistungsvertrag

Das System schützt fachliche Eigenleistung durch:

- Erwartung oder Entscheidung vor Wirkung;
- Bezug auf den eigenen bestätigten Ausgangsstand;
- Auswahl und Deutung eines realen Belegs;
- begründete Revision mit erneuter Prüfung;
- Modellgrenze und Transferentscheidung;
- aktiven Abruf vor alter Vollanzeige.

Sprachlich glatte, kopierte oder KI-generierte Texte ersetzen diese situierten Beziehungen nicht. Das System erfasst jedoch keine Autorschafts- oder KI-Nutzungsprofile. Lehrkraftreview richtet sich auf Produkt, Beleg und Begründung.

## 16. Produktionsvertrag

### 16.1 Produktionsobjekte

Ein vollständiger Modul-Slice enthält:

1. validiertes Modulmanifest;
2. `ExperienceContentV1` mit Start, Lernhandlungen, Hilfen, Haltepunkten, Beleg- und Resilienzverträgen;
3. fachspezifische Ressourcen und Validatoren;
4. modulspezifischen State-Adapter ohne Verhaltensdaten;
5. Renderer, der ausschließlich freigegebene Experience-Patterns zusammensetzt;
6. Inhalts-, Accessibility-, Offline-, Daten-, Lizenz- und Browsertests;
7. Lehrkraftspur/Modulhandbuch mit denselben IDs und Begriffen;
8. Traceability von Curriculum/Fachziel über Lernhandlung bis Test.

### 16.2 Dateivertrag für LXP05

```text
packages/learning-experience/
  package.json
  src/contracts.ts
  src/validation.ts
  src/components/*.astro
  src/controllers/focus-stage.ts
  src/controllers/resilience-adapter.ts
  src/styles/tokens.css
  src/styles/foundation.css
  src/styles/patterns.css

modules/IUM-5-CORE-05/
  module.yaml
  lernumgebung/experience.json
  lernumgebung/content.json
  lernumgebung/scenarios.json

apps/lernwerk-portal/src/components/
  LearningStudio.astro
  ium5/*.astro

tests/platform/
  learning-experience-contracts.test.ts
  learning-experience-boundaries.test.ts
  learning-experience-content.test.ts

tests/browser/
  lxp-reference-entry.spec.ts
  lxp-reference-core.spec.ts
  lxp-reference-securing.spec.ts
  lxp-accessibility.spec.ts
  lxp-offline.spec.ts
```

Das bestehende `AlgorithmWorkbench.astro` wird in LXP05 schrittweise ersetzt, nicht parallel als zweite Produktoberfläche dauerhaft weitergeführt. Die Fachlogikpakete bleiben erhalten; Migrationen des persistenten Payloads benötigen eigenen Schema- und Originalerhaltvertrag.

### 16.3 Autor:innenworkflow

```text
fachliches Ziel und Lernprodukt
→ zentrale Lernhandlung und Beleg
→ Zustands-/Guardfolge
→ Aufgabe, Kriterien, Hilfe und Feedback
→ Lehrkraft-Haltepunkt und Fallback
→ Accessibility-/Reflow-/Offlinevarianten
→ Contentvalidator
→ Referenz-Slice im Browser
→ Fach-, WU-, Accessibility- und Engineeringreview
→ erst danach Aufnahme als Produktionsmuster
```

Autor:innen wählen keine beliebigen Komponenten. Sie wählen einen freigegebenen Lernhandlungsvertrag; der Vertrag erlaubt nur passende Patternkombinationen.

### 16.4 Qualitätsgates pro Slice

| Gate | Muss bestehen | blockiert bei |
|---|---|---|
| G1 Fachziel/Aufgabe | Ziel, Produkt, Denkhandlung, Kriterium, Beleg, Transfergrenze | reine Bedienung, unklare Eigenleistung, unbelegte Fachrelation |
| G2 Zustände/Guards | kontrollierte IDs, erlaubte Folge, verbotene Übergänge | Direktlauf ohne Erwartung, Sicherung ohne Deutung, Transfer ohne Beleg |
| G3 Inhalt/Copy | Schema, kontrollierter Wortschatz, konkrete Fehl-/Hilfecopy | `weiter`-/Ampel-/Personlob-Copy, Lösungsoffenlegung |
| G4 Komposition | Compact zuerst, Wide-Beziehungen, Budgets | Mega-Seite, parallele Vollnavigation, Kontextverlust |
| G5 Accessibility | Axe plus Tastatur, Touch, Text/AT, Fokus, Reflow, Zoom, Kontrast, Reduced Motion | ungleichwertiger Pfad oder verlorener Guard/Beleg |
| G6 Local First/Offline | bestätigter Stand, Offlinekern, RES-Mapping, atomare Datenhandlungen | Schein-Erfolg, tote Aktion, Datenverlust, Teilmigration |
| G7 Orchestrierung/WU | Haltepunkte, Rollen, gewöhnliche Evidenz, Fallback, digitaler Mehrwert | Dashboardbedarf, Zuschauerrolle, Tool ohne Lernfunktion |
| G8 Grenzen/Lizenzen | Paketgrenzen, keine externe Netzabhängigkeit, Asset-/Lizenznachweis | Modul-CSS als Systemfork, unklare Rechte, Telemetrie |
| G9 Regression | Plattform-, Python-, IUM5- und neue LXP-Tests | Bestandsvertrag oder Gate fällt |
| G10 Review | getrennt Fach/Lernen, Accessibility und Engineering | ungelöstes `fail` oder nicht belegtes `pass` |

## 17. Governance, Versionierung und Erweiterung

### 17.1 Versionsarten

- `ExperienceContractV1`: semantischer Systemvertrag;
- `terminologyVersion: lxp04-1`: sichtbarer Wortschatz;
- `styleVersion: calm-precision-1`: Designrollen und Grundwerte;
- `content.schemaVersion`: Struktur eines Modul-Inhaltsvertrags;
- `stateSchemaVersion`: persistenter modulspezifischer Zustand;
- Modul-/Inhaltsversion bleibt fachliche Quelle für Migration und Beleggültigkeit.

Eine Stiländerung, die Hierarchie, Dichte, Fokus, Reflow oder Bedeutung verändert, ist keine kosmetische Patchversion und benötigt erneute LXP04-/LXP06-Prüfung.

### 17.2 Aufnahme eines neuen Patterns

Ein neues Pattern wird nur aufgenommen, wenn:

1. mindestens zwei fachlich verschiedene Situationen es benötigen;
2. eine bestehende Komponente oder Komposition die Aufgabe nicht ohne Bedeutungsverbiegung erfüllt;
3. Zweck, Pflichtinhalt, Varianten, Zustände, Semantik, Fokus, Content, Resilienz und Nichtverwendung dokumentiert sind;
4. Compact, Wide, Tastatur, Touch, Text/AT und Reduced Motion geprüft sind;
5. Q1–Q8, WU- und Anti-Pattern-Gates bestehen;
6. Paketgrenze und Autor:innenworkflow aktualisiert sind;
7. Migration oder Abwärtskompatibilität für bestehende Module benannt ist.

### 17.3 Änderungsklassen

| Klasse | Beispiel | erforderliche Prüfung |
|---|---|---|
| Patch | Tippfehler ohne Bedeutungsänderung | Contenttest und Diffreview |
| Minor | neue zulässige Variante innerhalb eines Patternvertrags | Vertrags-, Browser-, A11Y- und Portabilitätstest |
| Major | neuer Zustand, veränderte Guardbedeutung, anderes Progressions- oder Datenmodell | dokumentierte Revision von LXP02/LXP04 und schriftliche Nutzerfreigabe |

### 17.4 Keine lokalen Systemforks

Modulspezifische CSS-, Copy- oder Komponentenabweichungen dürfen globale Patternverträge nicht umgehen. Fachrenderer dürfen neue Repräsentationen liefern; sie müssen Designrollen, Fokus-, Status-, Responsive- und Accessibilityverträge verwenden. Wiederkehrende Abweichungen werden als Patternantrag geprüft, nicht kopiert.

## 18. Review- und Teststandard

### 18.1 Automatisiert

- TypeScript-/Schema-Validatoren lehnen unbekannte Felder fail-closed ab.
- Vertragstests prüfen kontrollierte Zustands-IDs, Primäraktionszahl, Guardziele, persistente Felder und verbotene Verhaltensdaten.
- CSS-/Buildtests prüfen Tokenvollständigkeit, keine externen Font-/Assetrequests und dokumentierte Paketgrenzen.
- Playwright prüft drei Referenzsituationen, Fokusfolge, Tastatur, Touch, 320-Pixel-Reflow, 200-Prozent-Zoom, Reduced Motion und Offline.
- Axe bleibt notwendiges, aber nicht hinreichendes Gate.
- Kontrastrollen werden maschinell gegen 4,5:1 für normalen Text, 3:1 für große Schrift/UI-Grenzen und 3:1 für Fokus angrenzend geprüft.

### 18.2 Manuell

- kognitiver Walkthrough: Ziel, Handlung, Kriterium, Beleg und nächster Schritt;
- Screenreaderpfad mit ausgeschalteter visueller Szene;
- Touchpfad ohne Hover/Drag;
- Quellen-/Revisionsbezug im Compact-Reflow;
- technische Normal-, Limit- und Blockzustände;
- Lehrkraftdurchlauf ohne private Geräteeinsicht;
- Fachreview der Aufgabe, Rückmeldung, Hilfe, Belegkarte und Modellgrenze;
- visuelles Review auf Ruhe, Hierarchie, Altersangemessenheit und fehlende Belohnungsästhetik.

### 18.3 Evidenzregel

Ein automatischer Test darf nur technische und vertragliche Eigenschaften belegen. Er beweist keine Lernwirkung, Altersangemessenheit, Unterrichtspassung oder vollständige WCAG-Konformität. Diese Aussagen bleiben LXP06 und realer Erprobung vorbehalten.

## 19. Qualitätsprüfung Q1–Q8

| Situation | Dimension | Urteil | Systemnachweis | verbleibendes Folgegate |
|---:|---|---|---|---|
| 1 | Q1 Lernhandlungs-Klarheit | pass | StartBoard, LearningStateHeader und ActionEdge schließen Ziel, Handlung, Kriterium und nächste Aktion | reale Copy/Usability LXP06 |
| 1 | Q2 kognitive Ökonomie | pass-with-explicit-risk | Kompositionsbudgets, Compact-first und nachrangiger Normalstatus | reale Typografie/Inhaltslänge LXP05/06 |
| 1 | Q3 Agency/Motivation | pass | neue, fortgesetzte und lehrkraftgeleitete Starts erhalten lokalen Stand und begrenzte Wahl | Unterrichtscopy LXP05 |
| 1 | Q4 Feedback/Revision | pass | Bereitschaftsfeedback bewertet keine Person; Vorhersageguard bleibt | Produktwalkthrough LXP06 |
| 1 | Q5 Kontinuität | pass | ResumePrompt, active recall, Versions-Recovery | echte Migration LXP05/06 |
| 1 | Q6 Orchestrierung | pass | TeacherCheckpoint, Rollen, Fallback und gemeinsame Haltepunkte | reale Zeit/Geräte LXP06/Pilot |
| 1 | Q7 Gleichwertigkeit | pass-with-explicit-risk | Funktionsgleichwertigkeit, Fokus, Reflow, Touch/Tastatur/Text-AT | implementierte Semantik/Screenreader LXP05/06 |
| 1 | Q8 Resilienz | pass | RES-Mapping, Originalerhalt, keine Telemetrie | Asset-/Cachetechnik LXP05/06 |
| 2 | Q1 Lernhandlungs-Klarheit | pass | elf kontrollierte Zustände und fachliche Aktionslabels | Zustandswechsel im Browser LXP06 |
| 2 | Q2 kognitive Ökonomie | pass-with-explicit-risk | FocusStage-Varianten verbinden Erwartung, Modell, Wirkung und Beleg zustandsbezogen | Split-Attention im realen Slice LXP06 |
| 2 | Q3 Agency/Motivation | pass | Vorhersage, Belegwahl, Hypothese, Revision ohne Punkte/Rang | Fachvalidität der Fälle LXP05/06 |
| 2 | Q4 Feedback/Revision | pass | FeedbackSpec und RevisionCompare schließen Revisionsloop | konkrete Feedbackcopy LXP05 |
| 2 | Q5 Kontinuität | pass | bestätigter Produkt-/Belegstand statt Versuchshistorie | Payloadmigration LXP05 |
| 2 | Q6 Orchestrierung | pass | SharedHold, RoleExchange, neutraler Fall | Unterrichtswalkthrough LXP06 |
| 2 | Q7 Gleichwertigkeit | pass-with-explicit-risk | SemanticModelView, EvidenceView, Fokus-/Livevertrag | AT-Pfad darf Lösung nicht verraten LXP05/06 |
| 2 | Q8 Resilienz | pass-with-explicit-risk | Offlinekern, RES-LIMIT/BLOCK und sichere Pause | Interpreter-/Assetausfall LXP05/06 |
| 3 | Q1 Lernhandlungs-Klarheit | pass | Sicherung, Transfer, Export, Pause und Abruf getrennte Patterns | reale Copy LXP05/06 |
| 3 | Q2 kognitive Ökonomie | pass-with-explicit-risk | EvidenceCardComposer referenziert Spuren, Aktionskante begrenzt Abschlussoptionen | reale Kartendichte LXP06 |
| 3 | Q3 Agency/Motivation | pass | Belegwahl, Modellgrenze, bewusster Export und Anschluss | kein sozialer Zeigezwang LXP06 |
| 3 | Q4 Feedback/Revision | pass | reale Quelle, Deutung und Revision bleiben verbunden | Fachreview LXP05/06 |
| 3 | Q5 Kontinuität | pass | aktive Wiederaufnahme und getrennte Abrufantwort | langfristige Versionspraxis LXP06 |
| 3 | Q6 Orchestrierung | pass | gemeinsame Sicherung mit neutraler/freiwilliger Evidenz | Unterrichtswalkthrough LXP06 |
| 3 | Q7 Gleichwertigkeit | pass-with-explicit-risk | Quelle vor Eingabe, Schrittgruppen im Reflow, Dialog-/Exportfokus | echtes Exportformat/Screenreader LXP05/06 |
| 3 | Q8 Resilienz | pass | eigentumsbewusste Datenhandlung, atomare Migration/Löschung | technische Implementierung LXP05 |

**Bilanz:** 24/24 Systemurteile, davon 17 `pass`, 7 `pass-with-explicit-risk`, kein ungelöstes `fail`. Die sieben Risiken entsprechen den geerbten LXP02-/LXP03-Risiken und besitzen konkrete LXP05-/LXP06-Gates.

## 20. Portabilitätsprüfung

| Probe | verwendete Systempatterns | austauschbare Fachrenderer | System-Fail-Signal |
|---|---|---|---|
| Quellen-/Evidenzanalyse | Prediction/Decision, EvidenceView, EvidenceFeedback, RevisionCompare, EvidenceCardComposer, TransferPrompt | Quelle, Provenienz, Text-/Bildstelle, Perspektive, Gegenbeleg | System verlangt deterministischen Lauf oder eindeutige Fehlerursache |
| Daten-/Systemmodellierung | PredictionForm, SemanticModelView, EvidenceView, RevisionCompare, Modellgrenze | Datensatz, Variablen, Beziehungen, Diagramm, konkurrierende Modelle | System erzwingt eine lineare Spur oder genau eine richtige Modellfassung |
| Medienproduktkritik | Kriterium, Wirkungserwartung, Produktausschnitt, Feedback, Variantenvergleich, Revision, Transfer | Medienprodukt, Zielgruppe, Gestaltungsmittel, Rezeptionsbeleg | technische Korrektheit oder Statusfarbe ersetzt Wirkung/Kriterium |

**Urteil:** Zustands-, Evidenz-, Feedback-, Revisions-, Orchestrierungs- und Resilienzpatterns tragen alle drei Proben. Fachrepräsentation, Belegform und Antwortformat bleiben neu zu entwerfen. Das System generalisiert Beziehungen, nicht IUM5-Bildschirme.

## 21. Globaler Anti-Pattern-Scan

| Anti-Pattern | LXP04-Schutz | Regression-Signal |
|---|---|---|
| Mega-Seite | eine FocusStage, Kompositionsbudgets, Zustandswechsel | mehrere Phasen/Werkzeuge/Hilfen/Datenhandlungen gleichzeitig primär |
| Infrastruktur-First | Technik im Ruhemodus nachrangig, RES nur handlungsbezogen | Speicher/Verbindung vor Ziel/Primäraktion |
| Pseudo-Fortschritt | fachliche Zustände/Produkte/Belege | Prozent, Seite, Klick, Zeit oder Versuch als Lernen |
| dekorative Gamification | ruhige Präzision, keine Belohnungsrollen | Badge, Streak, Rang, Timer, Konfetti |
| offene Wahl ohne Struktur | eine Primäraktion, Guards, begrenzte Geschwister | gleichgewichtige Optionen ohne Folge/Kriterium |
| Wizard ohne Überblick | JourneyMap und Rückkehranker | irreversible Folge ohne Kontext/Rückweg |
| Feedback als Urteil | FeedbackSpec | richtig/falsch, Ampel oder Lob ohne Beleg/nächsten Schritt |
| adaptive Blackbox | bewusste Hilfen, keine Verhaltensdaten | Pfad/Hilfe aus Klicks, Zeit, Fehlern, Hilfeprofil |
| Lehrkraft als Nachtrag | TeacherCheckpoint und SharedHold | Unterricht nur mit externem Handbuch koordinierbar |
| Accessibility als Parallelprodukt | Funktionsgleichwertigkeit und eine semantische Quelle | Alternativpfad trägt andere Aufgabe oder Lösung |
| Narration als Lernersatz | Aufgaben-/Eigenleistungsvertrag | Kontext/Animation ohne Denkprodukt |
| Export als Abschluss | getrennte Sicherungs-, Transfer-, Export- und Pausenpatterns | Dateierzeugung gilt als Sicherung oder Lernerfolg |

Alle zwölf Anti-Patterns sind auf Systemebene ausgeschlossen. Ihr Auftreten in einem LXP05-Slice ist ein blockierender Regression-Befund.

## 22. Nicht generalisieren und bekannte Risiken

### 22.1 Nicht generalisieren

- IUM5-Raster, Roboter, Befehle, Blockeditor, Laufspurtabelle und Lieferfall;
- genau vier Kernansichten, sieben Sicherungsmomente oder drei Spalten;
- Belegkarte als universelles festes Layout;
- eindeutige erste Abweichung, Determinismus oder eine korrekte Endfassung;
- konkrete Szenariozahl, Befehlslänge oder Freitextlänge aus IUM5;
- aktuelle technische Events, CSS-Klassen oder DOM-Selektoren als öffentliche Experience-API;
- heutige `phaseId`-Navigation als LXP02-Lernzustandsmodell;
- PDF oder JSON als einziges Exportformat;
- globaler Rollenwechsel in jeder Aufgabe;
- Wirksamkeit, Altersangemessenheit, WCAG-Konformität, Pilotierbarkeit oder Produktreife.

### 22.2 Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme | Fail-Gate |
|---|---|---|
| Designsystem wird zur Kartenästhetik | Contract-first-Abhängigkeit und Aufgaben-/Zustandsvalidator | Komponente ohne Lernfunktion/Guard |
| IUM5 überprägt System | drei Portabilitätsproben und getrennte Fachrenderer | globaler Vertrag enthält Raster-/Laufspurannahme |
| Content-Schema wird Autor:innenbürokratie | kleine verantwortliche Teilverträge, konkrete Fehlermeldungen, Referenzinhalte | notwendige Lernhandlung nur durch Freitextschema ausdrückbar |
| Fokuskomposition wird starrer Wizard | JourneyMap, Rückkehr, fachlich vollständige Momente | Kontext/Quelle/Undo verloren |
| visuelle Ruhe wird langweilig oder unklar | präzise Hierarchie, fachliche Signalrollen, echte Produktvergleiche | Dekoration muss Motivation ersetzen |
| Accessibility senkt Anspruch | Funktionsgleichwertigkeit und dieselbe Evidenz | Alternativpfad vereinfacht Fachhandlung |
| Status- und Recoverycopy überlädt | RES-Schwere und Normalstatus nachrangig | Technik dominiert ohne Handlungsbedarf |
| System/Modul-Paketgrenze verwischt | Boundarytests und keine IUM5-Typen im LXP-Paket | zyklische oder modulspezifische Abhängigkeit |
| lokale Zustandsmigration verliert Arbeit | Originalerhalt, atomare Migration, exportierbarer Altstand | Teilmigration/Überschreibung |
| Lehrkraftspur wird Dashboard | gewöhnliche Evidenz, neutrale Fälle, keine Fernansicht | Personen-/Gerätedaten erforderlich |

## 23. Implementierungshandoff

Der vollständige TDD-Plan liegt unter:

```text
docs/superpowers/plans/2026-08-05-ium-lxp04-design-system-implementation.md
```

Er ist bewusst in eigenständig prüfbare Tranches geschnitten:

1. Verträge und Paketgrenzen;
2. Designrollen und Grundkomposition;
3. Accessibility-, Fokus- und Resilienzprimitiven;
4. validierter IUM5-Experience-Inhalt und State-Adapter;
5. Referenzsituation 1;
6. Referenzsituation 2;
7. Referenzsituation 3;
8. Lehrkraftorchestrierung und Modulhandbuch;
9. integrierte Accessibility-/Offline-/Portabilitäts- und Produktionsgates;
10. Review und Handoff an LXP06.

Der Plan ist eine Ausführungsgrundlage, keine Ausführungsfreigabe. LXP05 darf erst nach schriftlicher Annahme von Spezifikation und Plan als neuer Task geöffnet werden.

## 24. Akzeptanz- und Scopebilanz

- drei Systemisierungsansätze verglichen, Ansatz C begründet gewählt;
- 12/12 LXP04-Ergebnisse `specified`;
- vier Systemebenen und sechs Paket-/Artefaktverantwortungen geschlossen;
- konkrete Designrollen für Farbe, Typografie, Raum, Form, Tiefe und Motion;
- Compact-, Standard- und Wide-Vertrag mit Informationsbudgets;
- 24 Komponenten/Patterns mit Zweck, Varianten, Semantik, Grenzen und Fail-Signalen;
- elf LXP02-Zustände in wiederverwendbare Kompositionen überführt;
- Aufgaben-, Feedback-, Hilfe-, Belegkarten-, Lehrkraft- und Resilienzverträge geschlossen;
- Tastatur, Touch, Text/AT, Fokus, Reflow, Zoom, Kontrast und Reduced Motion normiert;
- Local First, Offline, Import, Export, Löschung und Recovery erhalten Datenhoheit;
- Produktionsworkflow, zehn Qualitätsgates, Versionierung und Patternaufnahme definiert;
- WU-Check, 24/24 Q1–Q8-Urteile, drei Portabilitätsproben und 12/12 Anti-Patterns geschlossen;
- Nicht-Generalisierungen und zehn bekannte Risiken mit Gates dokumentiert;
- detaillierter TDD-Implementierungsplan separat erstellt;
- Repository-Scope bleibt dokumentarisch; kein Produktcode und keine Folgephase begonnen.

Offen bleibt ausschließlich die ausdrücklich dokumentierte schriftliche Nutzerfreigabe.

## 25. Schriftliches Freigabegate

Die LXP04-Spezifikation und der Implementierungsplan werden als gebündeltes Reviewpaket vorgelegt. Eine Freigabe muss ausdrücklich schriftlich erfolgen, zum Beispiel mit `LXP04 freigegeben`.

Die Freigabe würde bewirken:

- Fassung 1.0 wird normativer Design-, Interaktions-, Inhalts-, Accessibility-, Produktions- und Governancevertrag;
- der detaillierte TDD-Plan wird verbindliche Planungsgrundlage;
- LXP05 darf als eigene Umsetzungsetappe und neuer Task geplant beziehungsweise gestartet werden.

Die Freigabe bewirkt nicht:

- automatische Ausführung des Plans;
- Freigabe einer IUM5-Neufassung oder eines visuellen Produkts;
- Aussage über Lernwirkung, Usability, WCAG-Konformität oder reale Unterrichtspassung;
- Preview, Deployment, Realgerätegate, Pilotierung, LMS, Release oder Statushochsetzung;
- Push oder Pull Request des lokalen Dokumentationsstands.

Bis zur schriftlichen Antwort bleibt diese Fassung `0.9`, der Task `review` und LXP05 geschlossen.
