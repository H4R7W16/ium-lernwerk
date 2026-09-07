# V2-G5-M06 – Fachkern, Materialien und Oberfläche – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans`; keine Subagenten ohne Nutzerauftrag. Nur tatsächlich beauftragte Pakete ausführen, Checkboxes dokumentieren echte Arbeit.

**Goal:** Die angenommene „Prüffahrt im Raster“ als vollständigen lokalen Entwicklungskandidaten mit eigenen Darstellungen, ausführbarem Code, begrenztem Dossier und Lehrkraftmaterial herstellen.

**Architecture:** Ein neues reines Fachpaket enthält Bewegung, feste Wiederholung, nachvollziehbare Spur und Produktprojektion. Versionierte Materialien liefern Aufgaben, Hilfen, Transfer und Orchestrierung. Ein eigener Kandidatenbuild verbindet diese mit den geprüften Runtime-/Storage-/Updateports, ohne den V1-Lieferrobotermodus zu ersetzen.

**Tech Stack:** TypeScript 6.0.3, Astro 7.1.6, Vitest 4.1.10, Playwright 1.62.1; vorhandene Paket-/Schema-/Buildwerkzeuge. Node 22.23.2/npm 10.9.8; keine neue externe Laufzeitbibliothek.

**Spec:** [Hauptplan](2026-09-07-ium-v2-referenzmodul-implementation.md), [MOD-Design](../specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md), [strukturierte MOD-Bindung](../../../roadmap/v2/follow-ups/reference-module/specification.json), [PILOT](../../../roadmap/v2/follow-ups/pilot/README.md).

## Global Constraints

- Hauptplan und Runtimeplan gelesen; IMP01–04 erfüllen ihre jeweiligen Abschlusskriterien.
- `V2-G5-M06`, Modulversion `0.1.0`, Payloadschema1. Keine automatische Migration aus IUM-5-CORE-05.
- P1/P2/P3/P5/P6 bilden das begrenzte Dossier, P0/P4 nur flüchtig. Alle curricularen Nachweise bleiben `unassessed`.
- Fünfmal45 Minuten; O35/G55/I60/F40/S35. Keine universellen elf Seiten/Phasen, kein Tempo-/Punkte-/Badgekriterium.
- Befehle vor/links/rechts, feste Wiederholung 2–9, Körper1–5, keine Verschachtelung, höchstens100 ausgeführte Grundaktionen.
- S4 ist manueller Zustandstransfer; Papier erfüllt ALG-005 nicht. Tatsächliche Schule/Termin-/Zugangsentscheidungen werden nicht erfunden.
- Keine externe Medien-/Logoabhängigkeit, KI-Funktion, Accounts, Telemetrie, Veröffentlichung oder echte Pilotdaten.

## IMP05 – Neutraler Fachkern und begrenzte Produktdaten

**Files – Create:** `packages/v2-g5-m06/package.json`, `packages/v2-g5-m06/tsconfig.json`, `packages/v2-g5-m06/src/model.ts`, `validation.ts`, `interpreter.ts`, `goals.ts`, `editor.ts`, `dossier.ts`, `index.ts` im selben `src`-Verzeichnis; `tests/platform/v2-m06-model.test.ts`, `tests/platform/v2-m06-dossier.test.ts`.

**Files – Modify:** `tsconfig.json`, `scripts/check-workspace-boundaries.ts`, `apps/lernwerk-portal/package.json`, `package-lock.json` nur für das lokale Workspacepaket. Neues Paket hat keine externen Dependencies, Portal bekommt `@ium/v2-g5-m06` mit exakter lokaler Paketversion wie beim vorhandenen IUM5-Paket.

**Interfaces:** Neue exportierte Fachtypen und Funktionen, V1-Typen unverändert:

```ts
export type Direction = 'north'|'east'|'south'|'west';
export type Position = Readonly<{column:number; row:number}>;
export type State = Readonly<{position:Position; direction:Direction}>;
export type Basic = Readonly<{id:string; kind:'move'|'turn-left'|'turn-right'}>;
export type Repeat = Readonly<{id:string; kind:'repeat'; count:number; body:readonly Basic[]}>;
export type Program = readonly (Basic|Repeat)[];
export type Grid = Readonly<{width:number; height:number; start:State}>;
export type TraceStep = Readonly<{
  step:number; commandId:string; iteration:number|null;
  before:State; after:State; error:'OUT_OF_BOUNDS'|null;
}>;
export type Run = Readonly<{
  state:State; trace:readonly TraceStep[];
  status:'complete'|'OUT_OF_BOUNDS'|'STEP_LIMIT';
}>;
export type Goal = Readonly<{
  checkpoints:readonly Position[]; end:State;
  boundary:Readonly<{left:number;right:number;top:number;bottom:number}>;
}>;
export type ParseResult<T> = {ok:true;value:T}|{ok:false;issues:readonly string[]};
```

Geplante Exporte mit diesen Signaturen: `parseProgram(input:unknown): ParseResult<Program>`, `run(grid:Grid,program:Program): Run`, `checkGoal(run:Run,goal:Goal): {ok:boolean; reason:'complete'|'missing-checkpoint'|'wrong-end'|'off-boundary'|'execution-error'}`, `insert(program:Program,index:number,command:Basic|Repeat): Program`, `remove(program:Program,id:string): Program`, `move(program:Program,id:string,index:number): Program`. Editorfunktionen validieren das Ergebnis, nicht nur ihre Eingabe; keine automatisch erfundene fachliche Lösung. Fehlerhafte Indizes/IDs ergeben Parse-/Domänenfehler und keine stille Operation.

- [ ] **1. Neue Paketgrenze und roten Semantiktest anlegen.** Paketname `@ium/v2-g5-m06`, privat, Version0.1.0, ESM, Export `./src/index.ts`, TS-Konfiguration analog zum vorhandenen DOM-freien IUM5-Paket. Boundaryliste um das neue Kernpaket ohne Abhängigkeiten ergänzen. In `v2-m06-model.test.ts`:

```ts
import {test,expect} from 'vitest';
import {parseProgram,run,checkGoal} from '../../packages/v2-g5-m06/src/index.js';
test('five-command body executes the required rectangle; empty code does not',()=>{
  const parsed=parseProgram([{id:'cmd-1',kind:'repeat',count:2,body:[
    {id:'cmd-2',kind:'move'},{id:'cmd-3',kind:'move'},
    {id:'cmd-4',kind:'turn-left'},{id:'cmd-5',kind:'move'},
    {id:'cmd-6',kind:'turn-left'}
  ]}]);
  expect(parsed.ok).toBe(true);
  if(!parsed.ok) throw new Error('Reference must parse');
  const start={position:{column:1,row:3},direction:'east' as const};
  const grid={width:5,height:4,start};
  const goal={checkpoints:[{column:3,row:3},{column:3,row:2},
    {column:1,row:2},{column:1,row:3}],end:start,
    boundary:{left:1,right:3,top:2,bottom:3}};
  const result=run(grid,parsed.value);
  expect(result.trace).toHaveLength(10);
  expect(result.state).toEqual(start);
  expect(checkGoal(result,goal).ok).toBe(true);
  expect(checkGoal(run(grid,[]),goal).ok).toBe(false);
});
```

Run `npx vitest run tests/platform/v2-m06-model.test.ts`; erst fehlende Exporte, dann konkrete Semantik prüfen.
- [ ] **2. Parser und Interpreter implementieren.** `cmd-[1-9][0-9]*`, eindeutige IDs einschließlich Körper; geschlossene Objekte, keine `pick-up/drop`, keine unbekannten Felder, Wiederholungskörper1–5 und Anzahl2–9. Gridgrenzen positiv/ganzzahlig und Start innerhalb. Vor jeder Grundaktion Schrittlimit prüfen; kein stilles Abschneiden langer Programme. Drehung verändert nur Richtung. Fehlende Grenzenänderung bei unmöglicher Bewegung: `after===before`, Fehlertrace nennt ursprüngliche Command-ID/Iteration. Schleifenklammer zählt nicht als Aktion. Beispiel für Drehrichtung:

```ts
const directions: readonly Direction[]=['north','east','south','west'];
export function turn(direction:Direction,delta:-1|1):Direction {
  return directions[(directions.indexOf(direction)+delta+4)%4]!;
}
```

`checkGoal` betrachtet erfolgreiche **Bewegungsschritte**, nicht wiederholte Drehzustände als neue Besuche. Alle Prüfpunkte in Reihenfolge; keine Bewegung im Rechteckinneren oder außerhalb des Randes; korrekter Endzustand. Codeende/kurzer Code alleine erfüllt nichts. Zusätzliche korrekte Randfahrten nicht wegen mangelnder Kürze abwerten; Pflichtschleife separat als Aufgabenanforderung prüfen.
- [ ] **3. Weitere interne Fälle und Fehler testen.** S0 drei Aktionen→`(2,2)/O`; S1 acht→Start/O; S2 erste fachliche Abweichung2, Grenzfehler3; Wiederholung0/1/10, Körper0/6, verschachtelt, doppelte IDs, Import von Transportbefehlen ablehnen. Genau100 Aktionen zulässig, 101. Aktion stoppt mit `STEP_LIMIT`. Grafik-/Code-Semantik kann gleich sein, obwohl IDs anders sind; ID-Abgleich allein ist keine fachliche Konsistenzprüfung. S4-Referenz manuell fachlich prüfen, keinen Pick-up-Befehl in diesen Interpreter zurückführen.
- [ ] **4. Produkt-/Sitzungstypen implementieren.** In `dossier.ts` geschlossene Datentypen: `Diagram = {program:Program; explanation:string}` als **eigener** editierbarer Grafikentwurf; UI stellt Reihenfolge/Körperrahmen aus diesen Daten dar. `Evidence = {program:Program; predicted:State|null; steps:readonly number[]; rationale:string}`; Spur wird aus exakt diesem Programm rekonstruierbar berechnet. `Dossier = {schemaVersion:1; p1:{diagram:Diagram}; p2:{before:Evidence; after:Evidence; firstDeviation:number|null}; p3:{diagram:Diagram; draftProgram:Program; evidence:Evidence}; p5:{sequence:readonly ('aufnehmen'|'prüfen'|'ablegen')[]; rationale:string}; p6:{timeControl:string; routeCalculation:string; boundary:string}; returnNote:{area:'auftrag'|'dossier'|'sicherung'; openPoint:string; nextAction:string}}`. Kein Volltrace-/Trialarchiv: ausgewählte Schrittnummern nur im Umfang der aktuellen Programmlänge, maximal100; ein P2-Vorher/Nachher-Vergleich ist das Lernprodukt.

`SessionState = {dossier:Dossier; p0:string; p4:string; selectedHelp:'H1'|'H2'|'H3'|'H4'|null; currentRun:Run|null}`. `createInitialDossier(): Dossier`, `parseDossier(input:unknown): ParseResult<Dossier>`, `projectDossier(session:SessionState): Dossier`. Leere Felder sind unvollständige Arbeit, kein ungültiger Zwang zum Fertigsein. Technische Eingabegrenzen: jedes kurze Erklärfeld maximal500 Unicode-Codepoints, Rückkehrfelder je200; sichtbar anzeigen, nie still kürzen. Diese Werte sind Daten-/Bediengrenzen, keine didaktischen Sollwortzahlen. Technische Grenzfälle mit langen Eingaben prüfen.
- [ ] **5. Minimierung und Codebindung prüfen.** `projectDossier` baut erlaubte Felder explizit neu auf, kein Restoperator der Sitzung. Test mit `p0:'PRIVATE-P0'`, `p4:'PRIVATE-P4'` und ausgewählter Hilfe darf keine dieser Diagnosen/Hilfehistorien serialisieren. Nach Codeänderung in P3 bleiben frühere Belege entweder klar als zugehöriger alter Programmbeleg markiert oder werden explizit als nicht aktuell angezeigt; nie eine erfolgreiche alte Spur an neuen Code hängen. Für die erste Umsetzung: `Evidence.program` ist der ausgewählte Beleg; Der eigene Grafikentwurf liegt in `p3.diagram.program`, der tatsächliche Code in `p3.draftProgram`. Stimmen Codeinhalte nicht überein, Anzeige `Beleg gehört zum vorherigen Code`; `p3.draftProgram` ist ein verpflichtendes Dossierfeld und wird in Initialwert/Parser/Projektion berücksichtigt. Erst bewusste Auswahl eines neuen Laufs ersetzt den Beleg. Eigene Grafik bleibt separat; keine automatische Gleichsetzung mit Entwurfscode.
- [ ] **6. Abschluss.** `npx vitest run tests/platform/v2-m06-model.test.ts tests/platform/v2-m06-dossier.test.ts tests/platform/ium5-interpreter.test.ts tests/platform/ium5-payload.test.ts`, `npm run typecheck`, `npm run boundaries:check`. Alter V1-Körper bleibt maximal4, sein Verhalten unverändert. Fetch/Pull, Commit `feat: add neutral V2 M06 model and dossier`.

## IMP06 – Vollständige Materialien und Orchestrierung

**Files – Create:** unter `modules-v2/V2-G5-M06/`: `content.json`, `cases.json`, `materials/start.md`, `legend.md`, `worked-example.md`, `revision.md`, `own-program.md`, `helps.md`, `return-and-retrieval.md`, `transfer-and-systems.md`, `teacher/handbook.md`, `teacher/briefing.md`, `print/learner.html`, `rights.json`; außerdem `scripts/check-v2-m06-materials.ts`, `tests/platform/v2-m06-materials.test.ts`.

**Interfaces:** `cases.json` enthält S0–S3-Grid-/Referenzdaten passend zu IMP05 und getrennte manuelle S4/S5-Daten. `content.json` bindet `{schemaVersion:1,moduleId:'V2-G5-M06',materialRevision:'0.1.0',segments,materials,helps}`. `segments` übernimmt die 22 IDs/Minuten/Hauptfunktionen exakt; `materials` Einträge `{id,path,productIds,audience:'learner'|'teacher'}`; `helps` Einträge `{id,trigger,learnerText,ownFollowUp,fade}`. Das Format dient der Produktion und Quellenbindung, nicht einer starren Seitennavigation.

- [ ] **1. Materialbindung als roten Vertragstest anlegen.** `checkMaterialPacket(rootDir:string): Promise<{issues:readonly string[]}>` neu exportieren. Test liest den realen neuen Materialbestand; erwartet exakt MAT-01–10, H1–H4, P0–P6-Bindungen und die MOD-Minuten. Mutierte Fixture mit fehlender MAT-08 oder 270-Minuten-Verlauf muss scheitern. Kein Wortlauttest für die Qualität von Lerntexten. Beispiel:

```ts
import {test,expect} from 'vitest';
import {checkMaterialPacket} from '../../scripts/check-v2-m06-materials.js';
test('production materials preserve all 22 approved time segments',async()=>{
  const result=await checkMaterialPacket(process.cwd());
  expect(result.issues).toEqual([]);
});
```

Run `npx vitest run tests/platform/v2-m06-materials.test.ts`; der erste Lauf scheitert an fehlendem Materialbestand. Anschließend Parser mit geschlossenen IDs, Dateiexistenz innerhalb Modulroot und exakten Sollsummen implementieren.
- [ ] **2. MAT-01–05 ausarbeiten.** Auftakt/Ziel und S0-Vorhersage; schrittweise Legende; S1 segmentiertes Beispiel mit zwei Verarbeitungsstopps und eigenem Ergänzungsschritt; genau ein S2-Körperfehler mit erwarteter erster Abweichung und erneuter Prüfung; S3 eigener Auftrag mit Reihenfolge der vier Prüfpunkte, geforderter fester Schleife, eigenem Grafik-/Codeentwurf, Vorhersage, Spur und Erklärung. Schülertext benennt das Fahrziel, zeigt nicht den vollständigen S3-Referenzcode. Lehrkraftteil erhält vollständige Lösungen und plausible Fehlwege. Arbeitsauftrag als konkreter Starttext:

```text
Entwirf eine Prüffahrt. Sie beginnt bei (1,3) mit Blick nach rechts.
Besuche nacheinander (3,3), (3,2), (1,2) und (1,3).
Fahre nur am Rand dieses Rechtecks und blicke am Ende wieder nach rechts.
Nutze eine feste Wiederholung. Zeichne zuerst deine Anweisungen mit dem
ganzen Wiederholungskörper. Schreibe dann deinen Code. Sage einen Zustand
voraus und prüfe ihn an der Laufspur. Erkläre, warum deine Fahrt passt.
```

- [ ] **3. MAT-06–08 ausarbeiten.** H1 Ort/Richtung, H2 vollständiger Körper, H3 erste Abweichung, H4 Eingabe/Sprache; je Trigger, kurzer Text, eigene Folgehandlung und Rücknahme. Rückkehrkarte Stand/offener Punkt/nächste Handlung getrennt von verdecktem P4-Impuls aus PILOT. S4 Werkstücke mit freier/belegter/geprüfter Station; zwei Gruppierungen prüfen, zweite Aufnahme scheitert. S5 vier neutrale Funktionsbriefe (digitale Zeitsteuerung, Wegberechnung, Papieralgorithmus, isoliertes Standbild), zwei Zuordnungen plus Erkenntnisgrenze. Keine erfundenen Details realer Apps, keine private Mediennutzung erfragen.
- [ ] **4. MAT-09 ausarbeiten.** Handbuch mit Kurzstart, M01-Ersatzdiagnose, fünf Terminen, genauen Segmenten, Beobachtungspunkten, eigener/Partnerverantwortung, Rollewechsel, Minimalprodukt, Zwischenkontrolle nach etwa5 Minuten, gemeinsamer Sicherung und individueller Revision. Bei einem Gerät pro Paar beide eigene Programmierung; fehlender individueller digitaler Nachweis offen. Kein bloßes „Partnerarbeit“. Abruf nur vor alter Lösung; fehlender/kurzer Abstand begrenzt Behauptung. Speicher-/Recovery-/Verlust-/Ausfallhinweise entsprechen IMP02–04. Pflichtmaterial, optionale Hilfen und reine Lehrerreferenzen klar unterscheidbar. `briefing.md` als vorlesbarer Fließtext ohne Tabellen, Code oder dichte Links; Quellen/Technik in getrenntem Anhang. Kein Audio erzeugen.
- [ ] **5. MAT-10 erstellen und visuell prüfen.** `print/learner.html` enthält druckfreundliche text-/rasterbasierte Lernendenseiten aus demselben Materialinhalt; lesbare Schwarzweiß-Körperrahmen, geordnete Textalternative und ausreichend eigene Felder. Keine separaten ungebundenen Materialkopien mit widersprechenden Zahlen. Druckansicht im Browser prüfen: A4, keine abgeschnittenen Aufgaben, handschriftliche/mündliche Erklärung möglich. Vollständige Programmierleistung bleibt digital. Rechteverzeichnis für eigene Texte/Grafiken und tatsächliche Quellen; keine Logos/Fremdassets hinzufügen, die der Kern nicht braucht. Quelldatensätze bleiben unverändert.
- [ ] **6. Didaktischen Autorenreview und Abschluss durchführen.** P0–P6, zehn Materialien, H1–H4 und zwölf LXF-Gates einzeln gegen Qualitätsanker prüfen; Fachbegriffe, Start-/Endzustände, Prompt/Solution-Trennung und Zeitverbrauch kontrollieren. Reale Lerngruppe/Termine sind weiterhin unbekannt: Material als anpassbarer Entwicklungskandidat kennzeichnen, kein durchgeführter Unterricht. `npx tsx scripts/check-v2-m06-materials.ts`, Materialtests und lokale Printprüfung; Fetch/Pull, Commit `feat: author V2 M06 learner and teacher materials`.

## IMP07 – Kandidatenregistry und zugänglicher Arbeitsraum

**Files – Create:** `schemas/v2/module-candidate.schema.json`, `scripts/build-v2-module-registry.ts`, `modules-v2/V2-G5-M06/module.json`, `apps/lernwerk-portal/src/components/M06Workspace.astro`, `apps/lernwerk-portal/src/controllers/m06/controller.ts`, `view.ts`, `diagram-editor.ts`, `code-editor.ts`, `apps/lernwerk-portal/src/styles/m06.css`, `tests/platform/v2-registry.test.ts`, `tests/platform/v2-m06-controller.test.ts`.

**Files – Modify:** `apps/lernwerk-portal/astro.config.ts`, `scripts/build-module-registry.ts`, `scripts/build-portal.ts`, `scripts/preview-portal.ts`, `scripts/publication-mode.ts`, `scripts/prepare-module-assets.ts`, `scripts/check-build-output.ts`, `apps/lernwerk-portal/src/pages/module/[id].astro`, `apps/lernwerk-portal/src/pages/index.astro`, `apps/lernwerk-portal/src/layouts/BaseLayout.astro`, `package.json`, `tests/platform/registry.test.ts`, `tests/platform/publication-mode.test.ts`, `tests/platform/portal-build.test.ts`. Astro-Profilprüfung und Ausgabeisolation schließen RuntimeProbe/Fixture/V1-Bundles aus dem V2-Build und M06-Bundles aus production/fixture aus. Buildtests prüfen echte Ausgabedateien und Routen einschließlich Unterpfad; nicht nur ein TypeScript-Union-Label ändern.

**Interfaces:**

```ts
export type BuildProfile = 'production'|'fixture'|'v2-development';
export type M06Candidate = Readonly<{
  schemaVersion:2; baseline:'v2'; id:'V2-G5-M06'; version:'0.1.0';
  renderer:'v2-m06'; payloadSchemaVersion:1; status:'draft';
  curriculumCoverage:'unassessed'; pilot:'not-started'; publication:'closed';
  specPath:string; materialRevision:string;
  curriculumRecordIds:readonly string[]; lxfGateIds:readonly string[];
  minutes:225;
}>;
```

`parseV2Candidate(input:unknown): ParseResult<M06Candidate>`, `buildV2Registry(options:BuildRegistryOptions): Promise<void>` schreibt einen als V2 getaggten Registrydatensatz mit `countsTowardCoverage:false` und `publishedStatus:null`. `connectM06(root:HTMLElement, resources:M06Resources, dependencies:M06Dependencies): Promise<M06Controller>`. `M06Resources` ist geparster Inhalt aus IMP06 plus Cases; `M06Dependencies` enthält Runtimefabrik, Storagewahl, Exportport, Reloadregistrierung. `M06Controller` hat `flush()`, `prepareForReload()`, `dispose()`; `flush` projiziert zuerst ausschließlich `Dossier` aus IMP05, niemals gesamte Sitzung.

- [ ] **1. Registry-Negativtests schreiben.** Bestehende Produktions-/Fixturetests bleiben erhalten. Neu: fehlende Baseline, Version1-Manifest, fremder Renderer, unbekannter Payload, fehlendes LXF-Gate, falsche sieben Curriculum-IDs, Coverage=true und M06 im V1-Produktionsprofil ablehnen. Die Liste der sieben IDs exakt aus MOD lesen, keine alte komplette Curriculumdatei zum M06-Nachweis machen. `parseV2Candidate` benutzt neues geschlossenes Schema und semantische Bindungsprüfung.
- [ ] **2. Neuen Buildzweig implementieren.** `v2-development` liest ausschließlich `modules-v2` und bindet aktuelle angenommene V2-Quellen/Designs. Release-ID umfasst Profil, tatsächliche Materialdateien, Schema und Kandidatenmanifest. `assertPublicationCombination` erlaubt genau `v2-development:development`, verbietet `v2-development:gate-b-preview` und `device-fixture`. V2-Build braucht vollständigen Git-SHA statt `stable`; Ausgabe Root und `/ium-lernwerk/` testen. Scripts: `build:v2`, `build:v2:subpath`, `preview:v2` auf4324. Kein Deploymentworkflow ergänzen. V2-Seiten zeigen „V2-Entwicklungskandidat – noch nicht für Unterrichtseinsatz freigegeben“; das ist kein Sicherheits-/Zugangsschutz.
- [ ] **3. Drei Informationsbereiche umsetzen.** „Auftrag und Beispiel“, „Mein Prüfdossier“, „Sicherung und Rückkehr“. Keine feste Zahl von Screens oder Prozentfortschritt. Fachliche Bedeutung trägt die Navigation; Datensatz `returnNote.area` merkt nur den Arbeitsbereich. Lehrkraft kann segmentiert anleiten, Lernende eigenen Stand wiederfinden. P0/P4 zunächst ohne alte Lösung; bewusste Freigabe der Lösung erst nach eigener Antwort/Ersatzdiagnose. Keine versteckte Sicherheitsannahme: statische Lehrerdateien sind technisch lesbar, nur didaktisch getrennt.
- [ ] **4. Eigene Grafik und Code ermöglichen.** Zwei unterscheidbare Editoren: Grafik mit Start, geordneten beschrifteten Anweisungen, Körperrahmen/Anzahl und Ende; eigene Ergänzung/Erklärung. Codeeditor bietet move/left/right/repeat und ganze Körperbearbeitung bis5 Befehle. Beide per Buttons/Tastatur, ohne Drag-and-drop-Zwang; Touch und Textalternativen gleichwertig. Eigene Grafik wird nicht ungefragt aus Code überschrieben. Ein optionaler Vergleich zeigt Unterschiede an, verändert keinen Schülerentwurf. Jeder Editor erzeugt dieselbe definierte `Program`-Struktur, bleibt aber im Dossier getrennt.
- [ ] **5. Vorhersage, Spur und Revision verbinden.** Eigene Vorhersage vor Ausführen verfügbar; Zustandsänderung mit Command-ID, Iteration und Vorher/Nachher lesbar. S2 benennt den ersten fachlichen Unterschied getrennt von Grenzfehlermeldung. Zielprüfung an Prüfpunkten und Randfahrt; kein „alles richtig“ aus `complete`. Hilfen H1–H4 nahe der Hürde, nicht verpflichtend nacheinander. Bewusste Auswahl einer relevanten Spur ersetzt nur den passenden Produktbeleg; alte Codebindung klar anzeigen. Feedback führt zu nächster eigener Handlung, keine Punkte/Belohnungsleiste.
- [ ] **6. Persistenz/Import/Update anbinden.** Vor Runtimebeginn `chooseStorage`; Runtimepolicy mit `createInitialDossier` und `parseDossier`, Version0.1.0/Schema1. Initiale P0/P4 leer, nach Reload wieder leer. P1/P2/P3/P5/P6 editierbar; unvollständige Dossiers gültig, keine fiktive Fertigstellung. Pending-Import wird bei jedem Fehler/Abbruch/Löschen entwertet. Recovery als gesonderter Originalexport. Konflikt zeigt erhaltenen eigenen Entwurf und nächsten sicheren Schritt. Kontrolliertes Update nutzt `prepareForReload`, `dispose` entfernt Listener, keine doppelten Autosaves. Fehler beim Autosave zeigt ungesichert; kein stilles Weiterlaufen mit „gespeichert“.
- [ ] **7. Zugängliche Labels und Prüfanker bereitstellen.** Verbindliche Namen für Browser-/Assistenzprüfung: „Auf diesem Gerät speichern“, „Nur in dieser Sitzung arbeiten“, „Abruf öffnen“, „Deine Abrufbegründung“, „Zum eigenen Entwurf“, „Begründung der Prüffahrt“, „Arbeitsstand speichern“. Sichtbare fachlich passende Überschriften, Feldlabels und Fehlerbezug; Fokus nach Tastatureinfügen an sinnvoller nächster Aktion, Pointerfokus separat begründen. Statusansagen gezielt, kein Vorlesen jeder Bewegung ohne Wunsch. 200/400%-Reflow, Tastatur und Textspur prüfen; keine zeitkritische Animation voraussetzen.
- [ ] **8. Controller-Verhaltensprüfung und Abschluss.** State-machine-Tests mit realer Fachlogik und gefälschten Ports: eigene Änderung→flush genau Dossier, Importfehler→keinConfirm, Savefehler→ungesichert, Codeänderung→alteSpur, Löschen→P0/P4/Pending/Belege weg. Keine Tests nur auf private Methodennamen. `npx vitest run tests/platform/v2-registry.test.ts tests/platform/v2-m06-controller.test.ts tests/platform/publication-mode.test.ts`, `npm run typecheck`, `npm run check:astro`, `npm run build:v2`, `npm run build:v2:subpath`, `npm run build`, `npm run build:fixture`, lokale vollständige S0–S5-Durchsicht einschließlich Print. Fetch/Pull, Commit `feat: integrate V2 M06 development workspace`.

## Übergabe an IMP08

Ein sichtbarer Kandidat ist noch keine abgeprüfte Umsetzung. IMP08 führt die vollständige synthetische Matrix und V1-Regression aus; echte Zielgeräte, Lernendennutzung und die zwei Unterrichtsläufe aus PILOT bleiben eigene Aufgaben. Materialrechte und fehlende institutionelle Entscheidungen werden nicht durch Quellenlinks oder erfolgreiche Builds ersetzt.
