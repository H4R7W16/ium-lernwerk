# IuM-Lernwerk – kontrollierte Re-Baseline V2

- **Status:** schriftlich freigegeben
- **Fassung:** 1.0
- **Datum:** 3. September 2026
- **Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E
- **Repository-Ausgangsstand:** `main` bei `dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0`
- **Arbeitsbranch:** `feat/ium-v2-rebaseline`
- **Arbeitsgrenze:** Re-Baseline, Grundlagen, Audit und Planung; keine Inhaltsproduktion, kein LXP05-Neustart, kein Merge und keine Veröffentlichung

## 1. Entscheidung

Das IuM-Lernwerk erhält eine kontrollierte Re-Baseline V2. Die bisherige Roadmap wird nicht fortgeschrieben, als wären ihre fachlichen, didaktischen und organisatorischen Annahmen weiterhin unverändert gültig. Sie bleibt als historischer Stand erhalten und wird gegen ein neues V2-Anforderungsregister auditiert.

V2 umfasst die Klassen 5–7. Umsetzung und spätere Freigabe erfolgen jahrgangsweise in der Reihenfolge Klasse 5, Klasse 6, Klasse 7.

Die Inhaltsproduktion bleibt eingefroren. Insbesondere bleibt `origin/feat/lxp05-ium5-experience` ein ungemergter historischer Reviewstand. Er ist weder aktueller Produktstand noch Referenzdesign.

## 2. Anlass und Bestandsdiagnose

Die bisherige Basis ist substanziell, aber nicht in allen Teilen freigabefähig:

- Die offiziellen Curriculumdaten, der Curriculum-Crosswalk, das Plattformfundament sowie die Local-First-, Offline-, Datenschutz- und Accessibility-Grundentscheidungen sind wertvolle V1-Bestände.
- Die Modulroadmap, Zeitmodelle, Coverage-Entscheidungen und LXP-Artefakte sind prüfenswerte Kandidaten, nicht automatisch V2-Standards.
- Fünf Curriculumrecords stehen weiterhin auf `partial`; Querschnittskompetenzen dürfen nicht durch künstliche Zusatzaufgaben oder Zusatzzeit geschlossen werden.
- Die Quellenverwaltung trennt Phase-0-Register und spätere LXP01-Quellen. Die sechs ergänzenden LXP01-Quellen sind zwar in der Spezifikation dokumentiert, aber nicht in `source-register.json` und `claim-ledger.json` integriert.
- Das bestehende `design-principles.json` verknüpft Claims mit Designfolgen, bildet aber Wirkmechanismus, Geltungsbedingungen, Muster, Antimuster und Prüfmethode nicht als eigenständigen Vertrag ab.
- LXP01–LXP04 konnten formal freigegeben werden, obwohl LXP05 als konkrete Lernerfahrung nicht überzeugte. Technische und formale Vertragserfüllung war damit kein ausreichender Nachweis für Material- oder Lernqualität.
- Governance und öffentliche Aussagen müssen Curriculumzuordnung, evidenzorientierte Gestaltung, technische Verifikation, Nutzungsprüfung, Pilotierung und Lernwirksamkeit streng trennen.

## 3. Zielbild

V2 trennt historische Evidenz, aktuellen Aufbau und aktiven Produktstand:

```text
V1 – historischer, unveränderter Referenzstand
V2 – kontrollierter Aufbau mit offenen Gates
aktiv – erst nach ausdrücklichem Cutover
```

Die Zielstruktur im Repository lautet:

```text
roadmap/v2/
  status.json
  archive/
    v1-baseline.json
  requirements/
    requirements.json
  foundations/
    curriculum/
    sources/
    learning-experience/
    governance/
  audits/
    artifact-reuse.json
  grades/
    grade-5/
    grade-6/
    grade-7/
```

Bestehende V1-Dateien bleiben an ihren heutigen Pfaden unverändert. V2 verweist auf sie über Commit, Pfad und Prüfurteil. Eine Datei wird erst nach dem Cutover zur aktiven V2-Quelle.

## 4. Verbindliche Nicht-Ziele

Die Re-Baseline umfasst nicht:

- neue Lernmodule oder Lernendentexte;
- Weiterentwicklung, Integration oder Merge von LXP05;
- Hosting, Authentifizierung oder öffentliche Veröffentlichung;
- personenbezogene Diagnostik oder Learning Analytics;
- pauschale Fortschrittsprozente oder eine Gesamtampel;
- rückwirkendes Umschreiben historischer Baselines;
- das Erfinden fehlender historischer Task-Notizen;
- die Behauptung von Lernwirksamkeit aus Designreview, Usability oder technischen Tests.

## 5. V2-Anforderungsvertrag

Jede V2-Anforderung besitzt eine stabile ID und wird unabhängig von vorhandenen Artefakten formuliert.

```ts
type RequirementDomain =
  | 'curriculum'
  | 'didactics'
  | 'sources'
  | 'platform'
  | 'privacy'
  | 'governance'
  | 'public-perception'
  | 'experience';

type RequirementBinding =
  | 'official'
  | 'project'
  | 'orientation'
  | 'candidate'
  | 'optional';

type RequirementScope =
  | 'module'
  | 'cross-cutting'
  | 'year'
  | 'cross-grade'
  | 'system';

type RequirementCoverage =
  | 'unassessed'
  | 'uncovered'
  | 'partial'
  | 'covered'
  | 'not-applicable';

interface V2Requirement {
  id: string;
  title: string;
  statement: string;
  domain: RequirementDomain;
  origin: EvidencePointer[];
  binding: RequirementBinding;
  scope: RequirementScope;
  grades: Array<5 | 6 | 7>;
  fulfillmentModes: Array<'direct-module' | 'integrated' | 'cross-cutting'>;
  coverage: RequirementCoverage;
  evidence: EvidencePointer[];
  dependencies: string[];
  risks: string[];
  gate: string;
}

interface EvidencePointer {
  kind: 'repo' | 'git' | 'vault' | 'url' | 'doi';
  target: string;
  label: string;
  required: boolean;
}
```

Unbekannte Enums, doppelte IDs, fehlende Pflichtfelder, unauflösbare Pflichtreferenzen und zirkuläre Abhängigkeiten sind Validierungsfehler.

## 6. Getrennte Reifeachsen

V2 führt keine Gesamtbewertung. Mindestens diese Achsen bleiben getrennt:

```text
Curriculumabdeckung
Konzept
Implementierung
technische Verifikation
fachlich-didaktischer Review
Nutzungsprüfung
Unterrichtspilot
Publikations-/Releasefreigabe
```

Ein grüner technischer Test darf keine andere Achse hochstufen. Ein Dirty Checkout erzeugt eine Warnung, verändert aber keinen Reifegrad. Ein Nachweis zu einem anderen Commit ist `stale`.

## 7. V1-Archiv und Cutover

Das V1-Archiv besteht aus:

1. einem unveränderlichen Git-Commit oder Remote-Ref;
2. `roadmap/v2/archive/v1-baseline.json` mit Commit, Remote-Refs, Artefaktliste und Aussagegrenzen;
3. einer menschenlesbaren Archivnotiz im Vault;
4. einer Kennzeichnung historischer, ungemergter Kandidatenbranches.

Bekannte Remote-Baselines zum Spezifikationszeitpunkt:

- `main`: `dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0`
- `origin/feat/lxp05-ium5-experience`: `645a1d4ea3c786b08e1320954b522edf86dc9f83`

Der im Vault dokumentierte lokale Dashboard-Commit `07bc15e1e70d` ist nicht als Remote-Branch auffindbar. Er darf erst als Git-Evidenz verwendet werden, wenn das Objekt lokal wiedergefunden oder veröffentlicht wurde. Bis dahin gilt die Dashboard-Implementierung als nicht reproduzierbarer lokaler Stand.

V2 wird erst aktiv, wenn alle Pflichtgates bestanden sind und der Nutzer den Cutover ausdrücklich freigibt. Davor bleibt `main` der Produktstand und `roadmap/v2/status.json` führt V2 als `building`.

## 8. Curriculumfundament

Die drei Curriculumquellen und Rohrecords bleiben erhalten. Ihre Geltung wird nicht aus der alten Roadmap abgeleitet:

- amtliche Bildungspläne: `official` beziehungsweise normativ geltender Stand;
- Lesehilfe 2026/2027: `orientation`;
- Projektentscheidungen: nicht normativ.

Curriculumabdeckung kann auf drei Arten nachgewiesen werden:

1. direkt in einem Modul;
2. integriert über mehrere Module;
3. als querschnittliche, fortlaufende Lernhandlung.

`BMB16-GYM-IK-GM-003` wird als Kandidat für den dritten Modus geführt. Daraus entsteht keine zusätzliche Unterrichtszeit. Die übrigen vier `partial`-Records bleiben offen, bis sie einzeln fachlich entschieden wurden.

## 9. Quellenfundament

V2 konsolidiert Quellen, Claims, Designentscheidungen und Assets, ohne sie zu vermischen:

```text
Quelle
→ prüfbarer Claim
→ Projektentscheidung
→ Gestaltungsprinzip
→ Materialmuster
→ Prüfmethode
```

Jede Quelle besitzt eine direkte Fundstelle, Prüfstatus, Quellentyp, Abrufdatum, Lizenz- oder Nutzungsstatus und Aktualitätsrisiko. Jede freigaberelevante Aussage verweist auf Claims; Claims verweisen ausschließlich auf registrierte Quellen.

Nicht auflösbare optionale historische Links bleiben Warnungen. Nicht auflösbare Pflichtquellen blockieren den jeweiligen Gateabschluss.

## 10. Lern- und Experience-Fundament

### 10.1 Grundentscheidung

Das Fundament umfasst die vollständige Lernarchitektur:

- Lernendenmaterial;
- Aufgaben und fachliche Lernhandlungen;
- Erklärung, Beispiele und Repräsentationen;
- Unterstützung, Feedback, Übung und Transfer;
- digitale Darstellung, Navigation und Interaktion;
- Accessibility und vorhersehbare Lernbarrieren;
- Lehrkraftorchestrierung, Zeit und Fallbacks.

Es ist kein visueller Styleguide und keine Sammlung pauschaler Lernpsychologie-Regeln.

### 10.2 Evidenz-zu-Design-Vertrag

```ts
type ContentStatus = 'draft' | 'working' | 'reviewed' | 'standard';
type EvidenceLevel = 'low' | 'medium' | 'high' | 'normative';
type DesignObligation = 'required' | 'conditional' | 'recommended' | 'avoid';
type VerificationMethod =
  | 'source-review'
  | 'expert-review'
  | 'content-walkthrough'
  | 'automated-check'
  | 'accessibility-audit'
  | 'usability-test'
  | 'classroom-pilot';

interface LearningEvidenceClaimV2 {
  id: string;
  statement: string;
  mechanism: string;
  scope: string;
  learnerContext: string;
  boundaryConditions: string[];
  sourceIds: string[];
  evidenceLevel: EvidenceLevel;
  status: ContentStatus;
}

interface LearningDesignPrincipleV2 {
  id: string;
  title: string;
  decision: string;
  claimIds: string[];
  decisionBasis: string;
  obligation: DesignObligation;
  appliesTo: string[];
  positivePatterns: string[];
  antiPatterns: string[];
  observableCriteria: string[];
  verificationMethods: VerificationMethod[];
  status: ContentStatus;
}
```

`standard` setzt eine belastbare Grundlage und wiederholte Anwendung oder Pilotbewährung voraus. Vor Inhaltsproduktion kann das Fundament höchstens `reviewed` erreichen.

### 10.3 Quellenfamilien

Mindestens folgende Felder werden auditiert:

- IBBW: Tiefenstrukturen, kognitive Aktivierung, Aufgabenqualität, digitale Medien;
- Cognitive Load und Cognitive Theory of Multimedia Learning;
- ICAP und generative Lernhandlungen;
- Worked Examples, Selbsterklärung, Scaffolding und explizite Erklärung;
- Abruf, Verteilung, Sicherung und Transfer;
- Feedback, Metakognition und Selbstregulation;
- Motivation, Sinn, Kompetenzerfahrung und begrenzte Autonomie;
- UDL 3.0, Sprache, Accessibility und WCAG 2.2;
- Classroom Orchestration ohne personenbezogene Telemetrie;
- Informatik- und Medienbildungsdidaktik für 10- bis 13-Jährige.

Die vorhandenen IUM03-Claims und die LXP01-Ergänzungen sind Auditinput. Sie werden weder pauschal verworfen noch automatisch übernommen.

### 10.4 Lernendenprofil Klasse 5–7

Das V2-Profil beschreibt vorhersehbare Varianz statt einer fiktiven Durchschnittsperson:

- Vorwissen und fachliche Vorstellungen;
- Lese- und Fachsprachenniveau;
- Aufmerksamkeits- und Arbeitsgedächtnisbelastung;
- digitale Bedienroutinen;
- Selbststeuerung und Hilfenutzung;
- Motivation und wahrgenommener Sinn;
- Barrieren und Ausdrucksmöglichkeiten.

Alters- oder entwicklungsbezogene Aussagen benötigen Quellen und Geltungsgrenzen. Defizitlabels, stabile Personenprofile und Ableitungen aus Klickdauer sind ausgeschlossen.

### 10.5 Acht Qualitätsdimensionen

1. Ziel und Sinn.
2. Vorwissen und kognitive Belastung.
3. Fachliche Lernhandlung.
4. Erklärung und Repräsentation.
5. Aufgabe und Unterstützung.
6. Feedback, Übung und Transfer.
7. Orientierung und Zugänglichkeit.
8. Lehrkraftorchestrierung.

### 10.6 Material- und Experience-Grammatik

Verbindlich sind Lernfunktionen, keine feste Seitenschablone:

```text
orientieren
→ Vorwissen sichtbar machen
→ fachliches Problem eröffnen
→ erklären oder modellieren
→ angeleitet handeln
→ selbstständig anwenden
→ Rückmeldung nutzen
→ sichern und übertragen
```

Die Reihenfolge darf fachlich begründet verändert werden. Jede Interaktion benennt ihre Lernfunktion. Dekoration, Interaktivität, Punkte oder Fortschrittsanzeigen gelten nicht als Lernnachweis.

### 10.7 Experience-Gates

Ein neutrales Gerüst oder späteres Referenzmaterial besteht das Gate nur, wenn:

- Ziel, Lernhandlung und Lernnachweis zusammenpassen;
- die Oberfläche keine vermeidbare kognitive Nebenlast erzeugt;
- zusammengehörige Repräsentationen auffindbar verbunden sind;
- Unterstützung die Kernhandlung erhält;
- Feedback eine nächste fachliche Handlung ermöglicht;
- Orientierung, Fokus, Status und Fehlerbehebung verständlich sind;
- gleichwertige Tastatur-, Touch- und Textpfade bestehen;
- die Lehrkraft den Ablauf realistisch orchestrieren kann;
- Geltungsgrenzen und offene Pilotfragen sichtbar bleiben.

Automatisierte Tests können Vertrags-, Link-, Struktur- und Accessibilityfehler finden. Sie können didaktische Qualität oder Lernwirkung nicht allein freigeben.

## 11. Governance und öffentliche Wahrnehmung

Öffentliche Aussagen werden an Mindestnachweise gebunden:

| Aussage | Mindestnachweis |
| --- | --- |
| curricular zugeordnet | überprüftes Curriculum-Mapping |
| evidenzorientiert gestaltet | `reviewed` Evidenz- und Designvertrag |
| barrierearm entwickelt | Accessibility-Review mit dokumentierten Grenzen |
| technisch verifiziert | Tests am angegebenen Commit |
| mit Nutzenden geprüft | dokumentierter Walkthrough oder Usability-Test |
| unterrichtlich pilotiert | dokumentierter Unterrichtspilot |
| lernwirksam | belastbarer Wirkungsnachweis, nicht nur Designreview oder Zufriedenheit |

Pauschale Aussagen wie „wissenschaftlich bewiesen“, „für alle geeignet“, „vollständig barrierefrei“ oder „garantiert lernwirksam“ sind unzulässig.

## 12. Übernahmeaudit

Jedes Artefakt IUM00–IUM20 und LXP01–LXP04 erhält genau eine Entscheidung:

```ts
type ReuseDecision =
  | 'retain'
  | 'adapt'
  | 'replace'
  | 'reference-only'
  | 'drop';

interface ArtifactReuseDecision {
  artifactId: string;
  artifactRef: EvidencePointer;
  decision: ReuseDecision;
  rationale: string;
  requirementIds: string[];
  evidence: EvidencePointer[];
  successorTaskId: string | null;
}
```

Eine Entscheidung ohne Begründung, V2-Anforderungsbezug oder überprüfbaren Artefaktverweis ist ungültig. LXP05 wird außerhalb dieser Übernahmemenge ausschließlich als historische Fehler-, Risiko- und Erfahrungsquelle geführt.

## 13. Sequenz der Re-Baseline

```text
IUM-V2-00  V1 einfrieren und Archivmanifest erstellen
IUM-V2-01  V2-Anforderungsregister aufbauen
IUM-V2-CUR Curriculumfundament konsolidieren
IUM-V2-SRC Quellenfundament konsolidieren
LXF01  vorhandene Lernpsychologie- und Experience-Basis auditieren
LXF02  Evidenzlücken schließen
LXF03  Fach- und Stufenprofil IuM 5–7 entwickeln
LXF04  Lernarchitektur-Vertrag ableiten
LXF05  Material- und Experience-Grammatik entwickeln
LXF06  Orchestrierungsstandard und Experience-Gates entwickeln
LXF07  Fundament prüfen und als reviewed freigeben
IUM-V2-GOV Governance und öffentliche Wahrnehmung konsolidieren
IUM-V2-AUD IUM-/LXP-Übernahmeaudit durchführen
IUM-V2-R5  Roadmap Klasse 5 neu aufbauen
IUM-V2-R6  Roadmap Klasse 6 neu aufbauen
IUM-V2-R7  Roadmap Klasse 7 neu aufbauen
IUM-V2-DASH Dashboard auf V1/V2-Steuerung migrieren
IUM-V2-CUT V2-Cutover gesondert entscheiden
```

Jeder Schritt erhält ein eigenes Review. Ungeklärte Punkte werden gelöst oder mit Eigentümer, Risiko und Akzeptanzentscheidung sichtbar offen geführt.

## 14. Dashboardvertrag

Das Dashboard zeigt mindestens:

- V1 als archivierten Referenzstand;
- V2 als Aufbauzustand;
- LXP05 als eingefrorenen ungemergten Kandidaten;
- Inhaltsproduktion als geschlossen;
- Curriculum, Quellen, Lern-/Experience-Fundament und Governance als getrennte Gates;
- Evidenzbasis, Lernendenprofil, Lernarchitektur, Materialgestaltung, Interaktion, Orchestrierung, Review und Pilotstatus getrennt;
- Stichtag, Commit und auflösbare Evidenzlinks;
- keine absoluten lokalen Pfade;
- keine pauschale Gesamtampel und keinen Gesamtfortschritt in Prozent.

Der Präsentationsmodus zeigt nur freigegebene Präsentationsevidenz. Interne Unsicherheiten werden nicht verborgen, sondern angemessen zusammengefasst.

## 15. Fehler- und Aktualisierungsverhalten

- Validatoren arbeiten fail-closed.
- V2-Dateien werden atomar geschrieben.
- Ein fehlgeschlagenes Update lässt den letzten gültigen Snapshot unverändert.
- Unbekannte Statuswerte, doppelte IDs, fehlende Pflichtstränge und ungültige Pflichtlinks sind Fehler.
- Optional fehlende historische Quellen werden als Warnung ausgewiesen.
- Git-Nachweise werden an vollständige Commit-SHAs gebunden.
- Ein nicht verfügbarer lokaler Commit wird nicht in einen GitHub-Link umgewandelt.

## 16. Validierung und Abnahme

Die Re-Baseline ist erst für den Cutover entscheidungsreif, wenn:

- V1 unveränderlich referenziert und V2 davon getrennt ist;
- das V2-Anforderungsregister vollständig und widerspruchsfrei ist;
- Curriculum-, Quellen-, Lern-/Experience- und Governancefundament ihre jeweiligen Reviews bestanden haben;
- alle IUM00–IUM20- und LXP01–LXP04-Artefakte auditiert sind;
- Jahrgangsroadmaps 5, 6 und 7 getrennt vorliegen;
- Dashboard und Präsentationsansicht den V2-Status korrekt darstellen;
- automatisierte Validatoren und Repositoryregressionen grün sind;
- fehlende Pilotbewährung sichtbar bleibt;
- der Nutzer den Cutover ausdrücklich freigibt.

Das Lern- und Experience-Fundament kann vor Produktion `reviewed` werden. `standard` wird erst nach mehreren tragfähigen Anwendungen oder Pilotnachweisen zulässig.

## 17. Festgelegte Annahmen

- Sprache ist Deutsch mit echten UTF-8-Umlauten.
- Zielgruppe des Cockpits sind fachlich Beteiligte.
- V2 ist zunächst lokal; Hosting und Veröffentlichung bleiben separat.
- Digital bleibt Primärmedium, Analoges benötigt fachlichen oder lernpsychologischen Mehrwert.
- Das Lernwerk unterstützt lehrkraftorchestrierten Unterricht und ist kein vollständig selbstgesteuerter Onlinekurs.
- Inhalte werden erst nach Abschluss der Grundlagen- und Auditgates wieder geöffnet.
- Build-Artefakte und reale Statussnapshots gelangen weder in den Vault noch in Git.

## 18. Freigabevermerk

Die Architektur wurde im Dialog abschnittsweise freigegeben:

1. V1/V2-Zielarchitektur und Cutover;
2. V2-Anforderungs- und Statusmodell;
3. sequenzielle Re-Baseline und Jahrgangsreihenfolge;
4. umfassendes Lern- und Experience-Fundament;
5. Evidenz-zu-Design-Vertrag und zweistufige Validierung;
6. Taskstruktur, Dashboard- und Governancegrenzen.

Die Freigabe autorisiert Spezifikation und Planung. Sie ist keine Inhalts-, Pilot-, Push-, Merge- oder Veröffentlichungsfreigabe.
