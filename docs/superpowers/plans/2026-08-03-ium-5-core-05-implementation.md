# IUM-5-CORE-05 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das vollständige, lokal speichernde und offline nutzbare Arbeitsmodul `IUM-5-CORE-05 – Präzise Abläufe ausführbar machen` einschließlich Lehrkräftehandbuch und interner Qualitätssicherung als eindeutig gekennzeichneten `working`-Stand umsetzen.

**Architecture:** Fachinhalte, Szenarien, Curriculum- und Lizenznachweise liegen unter `modules/IUM-5-CORE-05/`. Ein neues, ausdrücklich modulspezifisches und DOM-freies Paket `@ium/ium-5-core-05` enthält geschlossene Typen, Interpreter, Payloadvalidierung und reine Editoroperationen; es ist kein allgemeiner Plattformbaustein. Die Astro-App bindet diesen Kern über einen statisch zugeordneten Renderer `algorithm-workbench` an die bestehenden Local-First-, Import-/Export-, Offline- und Statusverträge an.

**Tech Stack:** Node 22.20.0, npm 10.9.3, Astro 7.1.6, TypeScript 6.0.3, Vitest 4.1.10, Playwright 1.62.1, axe-core 4.12.1, bestehende Phase-1-PWA und bestehender `ModuleRuntime`.

## Global Constraints

- Die freigegebene Spezifikation `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md` auf Commit `41102e1` steuert jeden Task.
- Die Ausführung beginnt in einem isolierten Worktree über `superpowers:using-git-worktrees`; nicht direkt auf `main` implementieren.
- Vor jedem Commit oder Push gelten die Repository-Regeln aus `AGENTS.md`; niemals Force-Push oder History-Rewrite.
- Modul-ID ist exakt `IUM-5-CORE-05`, Modulversion initial `0.1.0`, Payloadschema initial `1`, Status durchgehend `working`, `pilotRequired` bleibt wahr.
- Gate A erlaubt synthetische Implementierung, interne Vorschau und QA. Gate B für Unterrichtspilotierung, reale Lernendendaten, LMS, Produktkatalog, Pages-Produktdeployment und Statushochsetzung bleibt geschlossen.
- Der manuelle Pages-Workflow `.github/workflows/device-fixture-pages.yml` baut weiterhin ausschließlich `build:fixture:subpath`; er darf das Fachmodul nicht ausliefern.
- Zulässige Befehle sind ausschließlich `Gehe`, `Drehe links`, `Drehe rechts`, `Nimm auf`, `Lege ab` und `Wiederhole n-mal`.
- Wiederholungszahl ist ganzzahlig 2 bis 9; der Schleifenkörper enthält 1 bis 4 Grundbefehle; keine verschachtelten Schleifen, Bedingungen, Variablen oder freie Codeausführung.
- Szenarien verwenden höchstens 6 × 6 Felder. Eine Ausführung stoppt am ersten fachlichen Fehler oder vor Schritt 101.
- Gleicher Startzustand plus gleicher Algorithmus erzeugt bytegleich dieselbe fachliche Laufspur.
- Die Standardausführung ist schrittweise; Gesamtlauf ist zusätzlich möglich. Eine strukturierte unbewertete Vorhersage ist vor der ersten Ausführung und nach inhaltlicher Revision erforderlich.
- Persistiert werden nur `phaseId`, `scenarioId`, `initialAlgorithm`, `prediction`, `evidenceTrace`, `repairSource`, `repairHypothesis`, `revisedAlgorithm`, `loopDecision`, `systemClassifications` und `selfCheck`.
- Zeit, Klicks, Fokus, Navigation, Hilfenutzung, Wiedergabegeschwindigkeit, Versuchszahl und unbestätigte Zwischenläufe werden weder persistiert noch exportiert.
- Keine Namen, Konten, E-Mail-Adressen, Klassen- oder Gerätekennungen, Telemetrie, Drittanbieterrequests, automatische Punkte, Kompetenzstufen oder Personenprofile.
- Kurzbegründungen sind auf 500 Unicode-Codepunkte begrenzt.
- Der Kernpfad muss ohne Maus, Drag-and-drop, Farberkennung, Animation oder visuelles Raster möglich sein; Tastatur, Touch, Screenreader und Textdarstellung sind gleichwertige Anforderungen.
- Reflow bei 320 CSS-Pixeln und Bedienbarkeit bei 200 Prozent Zoom sind harte Browsergates.
- Es entstehen keine analogen Lernendenmaterialien und keine parallele Druckstruktur.
- Eigener Code steht unter MIT; eigene Texte, Aufgaben, Szenarien und Grafiken unter CC BY-SA 4.0.
- Kein React, Vue, Svelte, Preact, Lit oder globales Client-State-Framework; keine neuen Runtime-Abhängigkeiten.
- Fachliche Fixture und `TEST-PLATFORM-REFERENCE` bleiben strikt vom Produktionsmodul isoliert.
- Die Produktionsausgabe darf das Modul nur als „Arbeitsstand · nicht für Unterrichtseinsatz“ zeigen; sie wird nicht über den vorhandenen Pages-Workflow deployed.
- Alle Quellen sind UTF-8 ohne BOM und LF. Buildoutput, Reports, `node_modules`, Browserdateien und lokale Laufzeitdaten bleiben uncommitted.
- Jeder Verhaltenstask folgt TDD: roten Test schreiben, erwartetes Scheitern beobachten, minimale Implementierung, grünen Test beobachten, relevante Regressionen ausführen, committen.

---

## File Map

### Modulspezifischer Fachkern

- `packages/ium-5-core-05/package.json`: privates Workspacepaket ohne externe Abhängigkeit.
- `packages/ium-5-core-05/tsconfig.json`: striktes Composite-Projekt ohne DOM-Bibliothek.
- `packages/ium-5-core-05/src/model.ts`: geschlossene Befehls-, Szenario-, Zustands-, Trace- und Fehlertypen.
- `packages/ium-5-core-05/src/validation.ts`: fail-closed Parser für Algorithmen und Szenarien.
- `packages/ium-5-core-05/src/resources.ts`: geschlossener Vertrag für Lernpfad, Aufgaben, Hilfen, Transferfälle und Szenariobündel.
- `packages/ium-5-core-05/src/interpreter.ts`: unveränderliche Vorbereitung, Schritt- und Gesamtausführung.
- `packages/ium-5-core-05/src/payload.ts`: initialer Produktzustand, geschlossener Payloadparser und Persistenzprojektion.
- `packages/ium-5-core-05/src/editor.ts`: reine Einfüge-, Verschiebe-, Lösch- und Schleifenoperationen.
- `packages/ium-5-core-05/src/index.ts`: einzige öffentliche Exportfläche.

### Fachliche Modulquellen

- `modules/IUM-5-CORE-05/module.yaml`: Manifest mit Curriculum-, Zeit-, Daten-, Offline-, Accessibility- und Lizenzvertrag.
- `modules/IUM-5-CORE-05/lernumgebung/index.md`: OER-Einstieg, Status- und Scopegrenze.
- `modules/IUM-5-CORE-05/lernumgebung/content.json`: fünf UE, Erweiterungs-UE, Aufgabenfamilien, Rückmeldungen, Hilfen, Transfer und Selbstcheck.
- `modules/IUM-5-CORE-05/lernumgebung/scenarios.json`: zehn geschlossene Raster-, Start-, Ziel- und Fehlerfälle.
- `modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md`: vollständiges digitales Lehrkräftehandbuch.
- `modules/IUM-5-CORE-05/curriculum-mapping.json`: recordgenaue Zuordnung der fünf Kompetenzrecords und Zeitphasen.
- `modules/IUM-5-CORE-05/assets/delivery-robot.svg`: eigene sachliche Vektorgrafik ohne Text oder Marke.
- `modules/IUM-5-CORE-05/assets/licenses.json`: Provenienz, Rechte, Lizenz und Änderungen aller Modulassets.

### Registry, Build und statische Auslieferung

- `scripts/build-module-registry.ts`: geschlossene Rendererzuordnung und validiertes Workbench-Ressourcenbündel.
- `scripts/prepare-module-assets.ts`: statisch erlaubte Modulassets in den ignorierten Public-Buildbereich kopieren.
- `scripts/build-portal.ts`: Assets vor Astro/PWA vorbereiten.
- `apps/lernwerk-portal/public/asset-licenses.json`: öffentliche Evidenz für den generierten Modulassetpfad.
- `apps/lernwerk-portal/src/generated/module-registry.json`: weiterhin ignorierter Buildoutput mit Renderer und validierten Ressourcen.
- `.gitignore`: generierte Modulassets ausschließen.

### Lernendenoberfläche

- `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`: semantische Werkstatthülle, Aufgaben- und Datenkontrollen.
- `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`: Orchestrierung von View, Fachkern und Local-First-Runtime.
- `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`: DOM-Abbildung, Fokus, Live-Status und Ereignisse.
- `apps/lernwerk-portal/src/controllers/algorithm-workbench/browser-ports.ts`: ausschließlich modulspezifische Browserports für Export und Workspace-ID.
- `apps/lernwerk-portal/src/styles/algorithm-workbench.css`: Zweispaltenlayout, Stapelung, Trace, Fokus und reduzierte Bewegung.
- `apps/lernwerk-portal/src/pages/module/[id].astro`: statische Rendererwahl und ehrlicher `working`-Status.
- `apps/lernwerk-portal/src/pages/index.astro`: Entwicklungsmodul statt technischer Fixturetext im Produktionsprofil.
- `apps/lernwerk-portal/astro.config.ts`: symmetrische Profilisolation der beiden Rendererbundles.

### Tests und Qualitätsgates

- `tests/platform/ium5-model.test.ts`: geschlossene Modell- und Befehlsvalidierung.
- `tests/platform/ium5-resources.test.ts`: Modulmanifest, Inhalts-, Szenario-, Curriculum- und Lizenzvertrag.
- `tests/platform/ium5-interpreter.test.ts`: Semantik, Determinismus, Schleife und sechs Fehlerzustände.
- `tests/platform/ium5-payload.test.ts`: Datenminimierung, Grenzen, Kopien und Importvalidierung.
- `tests/platform/ium5-editor.test.ts`: unveränderliche Editoroperationen.
- `tests/platform/registry.test.ts`: statische Rendererbindung und Fixture-Isolation.
- `tests/platform/portal-build.test.ts`: Produktionsroute mit `working`-Kennzeichnung und Fixturetrennung.
- `tests/platform/build-quality.test.ts`: Produktionsbudgets, Assets, OER und keine Drittanbieter.
- `tests/browser/ium5-workbench.spec.ts`: vollständiger Lernzyklus in Chromium, Firefox und WebKit.
- `tests/browser/ium5-state.spec.ts`: Speichern, Neuladen, Export, Import, ungültiger Import und Löschen.
- `tests/browser/ium5-accessibility.spec.ts`: Tastatur, Screenreaderstruktur, axe, Reflow, Zoom und reduzierte Bewegung.
- `tests/browser/ium5-offline.spec.ts`: installierter Offlinepfad und zustandserhaltendes kontrolliertes Update.
- `playwright.ium5.config.mts`: isolierte Produktionsvorschau auf Port 4322.
- `scripts/verify-ium5.ts`: fail-fast Gesamtgate für Modul und unveränderte Phase-1-/Legacy-Verträge.
- `.github/workflows/ci.yml`: bestehende vier Jobs um IUM5-Prüfungen erweitern, ohne Deployjob.
- `docs/modules/ium-5-core-05.md`: lokale Entwicklung, Status, Daten, Offline, QA und Gate-B-Sperre.
- `docs/platform/README.md`: Phase-1-Ausgangsstand historisieren und den aktuellen nicht deployten `working`-Produktstand erklären.
- `docs/reviews/ium-5-core-05-fach-didaktik.md`: tatsächlicher interner Fach-/Didaktikreview.
- `docs/reviews/ium-5-core-05-engineering-accessibility-privacy.md`: tatsächlicher Technik-/Accessibility-/Privacy-/Lizenzreview.
- `README.md`: `working`-Einstieg und Verifikationsbefehl.

## Scope Check

Interpreter, Produktpayload, Modulressourcen, Lernendenoberfläche und QA bleiben in einem Plan, weil sie gemeinsam genau ein lauffähiges und prüfbares Modulprodukt bilden und durch denselben geschlossenen Modulvertrag gekoppelt sind. Keiner dieser Teile kann allein als nutzbare, Gate-A-prüfbare Software ausgeliefert werden. Die Grenzen bleiben trotzdem reviewbar: Fachkern, Inhalte/Registry, Interpreter, Payload, Renderer, Lernzyklus, Persistenz, vollständiger Lernpfad, Accessibility, Offline/CI und Reviews erhalten jeweils einen eigenen Task.

---

### Task 1: Modulspezifischen Fachkern und geschlossenen Befehlsvertrag anlegen

**Files:**
- Create: `packages/ium-5-core-05/package.json`
- Create: `packages/ium-5-core-05/tsconfig.json`
- Create: `packages/ium-5-core-05/src/model.ts`
- Create: `packages/ium-5-core-05/src/validation.ts`
- Create: `packages/ium-5-core-05/src/index.ts`
- Modify: `package-lock.json`
- Modify: `tsconfig.json`
- Modify: `apps/lernwerk-portal/package.json`
- Modify: `scripts/check-workspace-boundaries.ts`
- Test: `tests/platform/ium5-model.test.ts`
- Test: `tests/platform/boundaries.test.ts`

**Interfaces:**
- Produces: `MODULE_ID`, `MODULE_VERSION`, `PAYLOAD_SCHEMA_VERSION`, `MAX_EXECUTED_STEPS`, `MAX_RATIONALE_CODEPOINTS`.
- Produces: `Position`, `Direction`, `BasicCommandKind`, `BasicCommand`, `RepeatCommand`, `Command`, `Algorithm`, `WorldState`, `Scenario`, `TraceEntry`, `InterpreterErrorCode`.
- Produces: `parseAlgorithm(value): ParseResult<Algorithm>` und `parseScenario(value): ParseResult<Scenario>`.
- Consumes: keine Fach- oder Browserabhängigkeit.

- [ ] **Step 1: Rote Modell- und Boundarytests schreiben**

```ts
import { describe, expect, test } from 'vitest';
import {
  MAX_EXECUTED_STEPS,
  MODULE_ID,
  parseAlgorithm,
  parseScenario,
} from '../../packages/ium-5-core-05/src/index.js';

describe('IUM-5-CORE-05 closed model', () => {
  test('exports the fixed module and execution limits', () => {
    expect(MODULE_ID).toBe('IUM-5-CORE-05');
    expect(MAX_EXECUTED_STEPS).toBe(100);
  });

  test('accepts basic commands and one fixed repeat', () => {
    expect(parseAlgorithm([
      { id: 'cmd-1', kind: 'pick-up' },
      { id: 'cmd-2', kind: 'repeat', count: 4, body: [{ id: 'cmd-3', kind: 'move' }] },
      { id: 'cmd-4', kind: 'drop' },
    ]).ok).toBe(true);
  });

  test.each([
    [{ id: 'cmd-1', kind: 'branch' }],
    [{ id: 'cmd-1', kind: 'repeat', count: 1, body: [{ id: 'cmd-2', kind: 'move' }] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 10, body: [{ id: 'cmd-2', kind: 'move' }] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      { id: 'cmd-2', kind: 'repeat', count: 2, body: [{ id: 'cmd-3', kind: 'move' }] },
    ] }],
  ])('rejects a forbidden command shape', (algorithm) => {
    expect(parseAlgorithm(algorithm).ok).toBe(false);
  });

  test('rejects duplicate command identifiers and unknown fields', () => {
    expect(parseAlgorithm([
      { id: 'cmd-1', kind: 'move' },
      { id: 'cmd-1', kind: 'turn-left' },
    ]).ok).toBe(false);
    expect(parseAlgorithm([{ id: 'cmd-1', kind: 'move', score: 10 }]).ok).toBe(false);
  });

  test('rejects a grid larger than six by six or positions outside it', () => {
    expect(parseScenario({
      id: 'oversized', title: 'Zu groß', width: 7, height: 6,
      start: { position: { column: 1, row: 1 }, direction: 'east', carrying: false },
      itemPosition: { column: 1, row: 1 }, targetPosition: { column: 6, row: 6 },
      obstacles: [],
    }).ok).toBe(false);
  });
});
```

Erweitere `tests/platform/boundaries.test.ts` um die Erwartung, dass `@ium/ium-5-core-05` bekannt, frameworkfrei und DOM-frei ist und jede nicht erlaubte Abhängigkeit als `UNAPPROVED_DEPENDENCY` meldet.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

Run:

```powershell
npm exec -- vitest run tests/platform/ium5-model.test.ts tests/platform/boundaries.test.ts
```

Expected: FAIL, weil Paket, Exporte und freigegebene Workspacegrenze noch fehlen.

- [ ] **Step 3: Workspace und geschlossene Fachtypen minimal implementieren**

`packages/ium-5-core-05/package.json`:

```json
{
  "name": "@ium/ium-5-core-05",
  "version": "0.1.0",
  "private": true,
  "license": "MIT",
  "type": "module",
  "exports": { ".": "./src/index.ts" }
}
```

`packages/ium-5-core-05/tsconfig.json` erweitert `../../tsconfig.base.json`, setzt `rootDir: "src"`, `outDir: "dist"`, `tsBuildInfoFile: "dist/tsconfig.tsbuildinfo"` und ausdrücklich `lib: ["ES2022"]`; damit stehen im Fachkern keine DOM-Typen zur Verfügung.

`model.ts` definiert exakt:

```ts
export const MODULE_ID = 'IUM-5-CORE-05' as const;
export const MODULE_VERSION = '0.1.0' as const;
export const PAYLOAD_SCHEMA_VERSION = 1 as const;
export const MAX_EXECUTED_STEPS = 100 as const;
export const MAX_RATIONALE_CODEPOINTS = 500 as const;

export type Direction = 'north' | 'east' | 'south' | 'west';
export type Position = Readonly<{ column: number; row: number }>;
export type BasicCommandKind =
  | 'move' | 'turn-left' | 'turn-right' | 'pick-up' | 'drop';
export type BasicCommand = Readonly<{ id: string; kind: BasicCommandKind }>;
export type RepeatCommand = Readonly<{
  id: string;
  kind: 'repeat';
  count: number;
  body: readonly BasicCommand[];
}>;
export type Command = BasicCommand | RepeatCommand;
export type Algorithm = readonly Command[];

export type WorldState = Readonly<{
  position: Position;
  direction: Direction;
  carrying: boolean;
  itemPosition: Position | null;
  delivered: boolean;
}>;

export type Scenario = Readonly<{
  id: string;
  title: string;
  width: number;
  height: number;
  start: Readonly<{ position: Position; direction: Direction; carrying: false }>;
  itemPosition: Position;
  targetPosition: Position;
  obstacles: readonly Position[];
}>;

export type InterpreterErrorCode =
  | 'OBSTACLE'
  | 'OUT_OF_BOUNDS'
  | 'INVALID_PICK_UP'
  | 'INVALID_DROP'
  | 'INVALID_REPEAT'
  | 'STEP_LIMIT';

export type TraceEntry = Readonly<{
  step: number;
  sourceCommandId: string;
  commandKind: BasicCommandKind | 'repeat';
  loop: Readonly<{ iteration: number; total: number }> | null;
  before: WorldState;
  after: WorldState;
  outcome: 'ok' | 'error';
  error: InterpreterErrorCode | null;
}>;
```

`validation.ts` verwendet ausschließlich geschlossene Schlüsselprüfungen. `parseAlgorithm` akzeptiert nur die fünf Grundbefehle, `repeat` mit 2–9 und 1–4 Grundbefehlen, IDs nach `^cmd-[1-9][0-9]*$`, eindeutige IDs über Hauptfolge und Schleifenkörper und keine zusätzlichen Felder. `parseScenario` akzeptiert Raster 1–6, Positionen innerhalb des Rasters, eindeutige Hindernisse sowie Gut, Start und Ziel außerhalb der Hindernisse.

Rückgabetyp:

```ts
export type ParseIssue = Readonly<{ path: string; message: string }>;
export type ParseResult<T> =
  | Readonly<{ ok: true; value: T }>
  | Readonly<{ ok: false; issues: readonly ParseIssue[] }>;
```

Ergänze das Paket als Root-TS-Referenz, exakte Portalabhängigkeit `"@ium/ium-5-core-05": "0.1.0"`, den geschlossenen Boundarygraph und `corePackages`. Führe anschließend `npm install --package-lock-only` aus.

- [ ] **Step 4: Modell-, Boundary- und Typprüfungen grün ausführen**

Run:

```powershell
npm exec -- vitest run tests/platform/ium5-model.test.ts tests/platform/boundaries.test.ts
npm run typecheck
npm run boundaries:check
```

Expected: alle Prüfungen PASS; der Boundarybericht enthält weiterhin genau die sieben nun freigegebenen Workspaces und keine Verletzung.

- [ ] **Step 5: Task 1 committen**

```powershell
git add package-lock.json tsconfig.json apps/lernwerk-portal/package.json scripts/check-workspace-boundaries.ts packages/ium-5-core-05 tests/platform/ium5-model.test.ts tests/platform/boundaries.test.ts
git commit -m "feat: add IUM5 algorithm model contract"
```

---

### Task 2: Modulquellen, Ressourcenvertrag, Registry und Assetpfad binden

**Files:**
- Create: `packages/ium-5-core-05/src/resources.ts`
- Modify: `packages/ium-5-core-05/src/index.ts`
- Create: `modules/IUM-5-CORE-05/module.yaml`
- Create: `modules/IUM-5-CORE-05/lernumgebung/index.md`
- Create: `modules/IUM-5-CORE-05/lernumgebung/content.json`
- Create: `modules/IUM-5-CORE-05/lernumgebung/scenarios.json`
- Create: `modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md`
- Create: `modules/IUM-5-CORE-05/curriculum-mapping.json`
- Create: `modules/IUM-5-CORE-05/assets/delivery-robot.svg`
- Create: `modules/IUM-5-CORE-05/assets/licenses.json`
- Create: `scripts/prepare-module-assets.ts`
- Modify: `scripts/build-module-registry.ts`
- Modify: `scripts/build-portal.ts`
- Modify: `apps/lernwerk-portal/public/asset-licenses.json`
- Modify: `.gitignore`
- Test: `tests/platform/ium5-resources.test.ts`
- Test: `tests/platform/registry.test.ts`

**Interfaces:**
- Consumes: `parseScenario`, `Scenario`, `ParseResult` aus Task 1.
- Produces: `WORKBENCH_SCENARIO_IDS`, `TRANSFER_CASE_IDS`, `WorkbenchScenarioId`, `TransferCaseId`, `LearningPhaseId`, `WorkbenchContent`, `WorkbenchResources`, `parseWorkbenchResources(content, scenarios)`.
- Produces: Registryfeld `renderer: 'fixture-workspace' | 'algorithm-workbench'`.
- Produces: Für `algorithm-workbench` genau `workbench: { content, scenarios, robotAssetPath }`.

- [ ] **Step 1: Rote Ressourcen-, Curriculum- und Registrytests schreiben**

```ts
import { readFile } from 'node:fs/promises';
import { parse } from 'yaml';
import { describe, expect, test } from 'vitest';
import { validateModuleManifest } from '../../packages/module-contract/src/index.js';
import { parseWorkbenchResources } from '../../packages/ium-5-core-05/src/index.js';
import { buildRegistry } from '../../scripts/build-module-registry.js';

const readJson = async (path: string) => JSON.parse(await readFile(path, 'utf8'));

describe('IUM-5-CORE-05 resources', () => {
  test('binds the approved manifest exactly', async () => {
    const manifest = parse(await readFile('modules/IUM-5-CORE-05/module.yaml', 'utf8'));
    expect(validateModuleManifest(manifest).ok).toBe(true);
    expect(manifest).toMatchObject({
      id: 'IUM-5-CORE-05', version: '0.1.0', status: 'working', grade: 5,
      kind: 'core', strands: ['STRAND-A'],
      time: { minLessons: 5, maxLessons: 6, contractId: 'TC-IUM-5-CORE-05' },
      prerequisites: ['IUM-5-CORE-01'],
      components: ['algorithm-workbench'],
      offline: { core: true, externalResources: [] },
    });
    expect(manifest.curriculum.competencyIds).toEqual([
      'LH26-E-PROG-002', 'LH26-E-ALG-001', 'LH26-E-ALG-002',
      'LH26-E-ALG-003', 'LH26-E-ALG-004',
    ]);
    expect(manifest.media.analogMaterials).toEqual([]);
    const timeModel = await readJson('roadmap/time-model.json');
    const timeContract = timeModel.moduleContracts.find(
      (contract: { moduleId: string }) => contract.moduleId === 'IUM-5-CORE-05',
    );
    expect(timeContract).toMatchObject({
      id: 'TC-IUM-5-CORE-05', pilotRequired: true, status: 'working',
    });
  });

  test('contains exact 225/270 minute paths and ten valid scenarios', async () => {
    const content = await readJson('modules/IUM-5-CORE-05/lernumgebung/content.json');
    const scenarios = await readJson('modules/IUM-5-CORE-05/lernumgebung/scenarios.json');
    const result = parseWorkbenchResources(content, scenarios);
    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.content.paths.regular.totalMinutes).toBe(225);
    expect(result.value.content.paths.extended.totalMinutes).toBe(270);
    expect(result.value.scenarios.map((entry) => entry.scenario.id)).toEqual([
      'worked-sequence', 'error-order', 'error-turn', 'error-missing-step',
      'error-repeat-count', 'product-a', 'product-b', 'product-c',
      'repair-standard', 'extended-inherited',
    ]);
  });

  test('maps every competency and records asset and handbook evidence', async () => {
    const mapping = await readJson('modules/IUM-5-CORE-05/curriculum-mapping.json');
    expect(mapping.records.map((record: { competencyId: string }) => record.competencyId))
      .toEqual([
        'LH26-E-PROG-002', 'LH26-E-ALG-001', 'LH26-E-ALG-002',
        'LH26-E-ALG-003', 'LH26-E-ALG-004',
      ]);
    for (const record of mapping.records) {
      expect(record.segmentIds.length).toBeGreaterThan(0);
      expect(record.productEvidence).toBeTruthy();
    }
    const licenses = await readJson('modules/IUM-5-CORE-05/assets/licenses.json');
    expect(licenses.assets).toEqual([expect.objectContaining({
      path: 'delivery-robot.svg', license: 'CC-BY-SA-4.0',
    })]);
    const handbook = await readFile(
      'modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md', 'utf8',
    );
    for (const heading of [
      'Fachlicher Hintergrund', 'Voraussetzungen', 'Fünf Unterrichtseinheiten',
      'Sechs Unterrichtseinheiten', 'Erwartbare Fehler', 'Accessibility',
      'Datenschutz und Export', 'Status- und Einsatzgrenze',
    ]) expect(handbook).toContain(heading);
  });

  test('keeps content free of gamification and diagnostic collection', async () => {
    const source = await readFile('modules/IUM-5-CORE-05/lernumgebung/content.json', 'utf8');
    expect(source).not.toMatch(/punkte|badge|rangliste|level|telemetrie|diagnoseprofil/i);
  });
});
```

Erweitere `tests/platform/registry.test.ts`: Produktionsregistry enthält genau `IUM-5-CORE-05`, `renderer === 'algorithm-workbench'`, `publishedStatus === 'working'`, `countsTowardCoverage === true`, validierte Workbenchressourcen und Assetpfad `generated-modules/ium-5-core-05/delivery-robot.svg`. Fixtureregistry enthält weiterhin ausschließlich `TEST-PLATFORM-REFERENCE`, `renderer === 'fixture-workspace'` und kein Workbenchbündel.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- vitest run tests/platform/ium5-resources.test.ts tests/platform/registry.test.ts
```

Expected: FAIL wegen fehlender Modulquellen, Ressourcenparser und Rendererfelder.

- [ ] **Step 3: Geschlossenen Ressourcenvertrag implementieren**

`resources.ts` definiert:

```ts
export type LearningPhaseId =
  | 'ue1-orientation' | 'ue1-prior-knowledge'
  | 'ue1-concept' | 'ue2-concept' | 'ue2-guided'
  | 'ue3-guided' | 'ue3-product' | 'ue4-product'
  | 'ue4-revision' | 'ue5-transfer' | 'ue5-consolidation'
  | 'ue6-extension';

export const WORKBENCH_SCENARIO_IDS = [
  'worked-sequence', 'error-order', 'error-turn', 'error-missing-step',
  'error-repeat-count', 'product-a', 'product-b', 'product-c',
  'repair-standard', 'extended-inherited',
] as const;
export type WorkbenchScenarioId = typeof WORKBENCH_SCENARIO_IDS[number];

export const TRANSFER_CASE_IDS = [
  'navigation', 'search-service', 'digital-timetable',
  'paper-map', 'mechanical-timer', 'controlled-vehicle',
] as const;
export type TransferCaseId = typeof TRANSFER_CASE_IDS[number];

export type LessonSegment = Readonly<{
  id: LearningPhaseId;
  lesson: 1 | 2 | 3 | 4 | 5 | 6;
  minutes: number;
  title: string;
  learningFunction: string;
  activityIds: readonly string[];
}>;

export type WorkbenchContent = Readonly<{
  schemaVersion: 1;
  moduleId: 'IUM-5-CORE-05';
  centralQuestion: string;
  paths: Readonly<{
    regular: Readonly<{ totalMinutes: 225; segmentIds: readonly LearningPhaseId[] }>;
    extended: Readonly<{ totalMinutes: 270; segmentIds: readonly LearningPhaseId[] }>;
  }>;
  segments: readonly LessonSegment[];
  activities: readonly Readonly<{
    id: string;
    family: 'precision' | 'worked-example' | 'error-case' | 'product' | 'transfer';
    title: string;
    instruction: string;
    scenarioIds: readonly WorkbenchScenarioId[];
  }>[];
  supports: readonly Readonly<{ id: string; title: string; text: string }>[];
  transferCases: readonly Readonly<{
    id: TransferCaseId;
    title: string;
    description: string;
  }>[];
  selfCheckQuestions: readonly Readonly<{ id: string; text: string }>[];
}>;

export type WorkbenchResources = Readonly<{
  content: WorkbenchContent;
  scenarios: readonly Readonly<{
    scenario: Scenario;
    starterAlgorithm: Algorithm | null;
    referenceAlgorithm: Algorithm;
  }>[];
}>;
```

`parseWorkbenchResources` prüft geschlossene Schlüssel, eindeutige IDs, alle Referenzen, genau 225/270 Minuten, genau fünf Aufgabenfamilien, vier Selbstcheckfragen, die sechs festen Transferfall-IDs sowie ausschließlich gültige Szenarien, Starter- und Referenzalgorithmen. Es lehnt zusätzliche Felder und unbekannte Szenario-/Aktivitätsreferenzen ab. Produktkarten besitzen `starterAlgorithm: null`; aktive Beispiele und Fehlerfälle besitzen einen vollständigen beziehungsweise gezielt fehlerhaften Starter. Jeder Fall besitzt einen strukturell gültigen Referenzalgorithmus, den die Oberfläche nur nach dem ausdrücklichen letzten Feedbackschritt zeigt. Die Lernendenressource enthält keine erwartete Transferklassifikation; fachliche Orientierung dazu steht ausschließlich im Lehrkräftehandbuch, damit die Oberfläche weder Lösung noch automatische Bewertung ableitet.

- [ ] **Step 4: Fachliche Quellen vollständig anlegen**

Das Manifest verwendet diese Datenfelder:

```yaml
data:
  stateSchemaVersion: 1
  fields:
    - phaseId
    - scenarioId
    - initialAlgorithm
    - prediction
    - evidenceTrace
    - repairSource
    - repairHypothesis
    - revisedAlgorithm
    - loopDecision
    - systemClassifications
    - selfCheck
  exportable: true
  deletable: true
```

`coverageEvidenceIds` enthält exakt:

```yaml
coverageEvidenceIds:
  - CE-IUM-5-CORE-05-LH26-E-ALG-001
  - TR-LH26-E-ALG-001
  - SE-LH26-E-PROG-002
```

`content.json` bildet die elf regulären Segmente aus der Spezifikation mit Minuten `15,20,10,25,20,25,20,35,10,25,20` und das erweiterte Segment mit 45 Minuten ab. Die vier Hilfekategorien sind konkrete Koordinaten-/Szenenbeschreibung, Drehhilfe, ausgeschriebene Schleife und Laufspurtabelle; zusätzliche Satzstarter und erster-Abweichung-Fragen werden ebenfalls explizit hinterlegt. Transferfälle sind Navigation, Suchdienst, digitale Stundenplananzeige, Papierkarte, mechanischer Kurzzeitwecker und das fern- oder programmsteuerbare Fahrzeug als Grenzfall.

`scenarios.json` verwendet diese geschlossenen Fälle:

| ID | Raster | Start/Blick | Gut | Ziel | Fachfunktion |
|---|---|---|---|---|---|
| `worked-sequence` | 5×4 | A4/north | A4 | D2 | vollständiges aktives Beispiel |
| `error-order` | 5×4 | A4/north | A4 | C2 | falsche Reihenfolge |
| `error-turn` | 5×4 | A4/north | A4 | C2 | falsche Drehung |
| `error-missing-step` | 5×4 | A4/north | A4 | C2 | fehlender Schritt |
| `error-repeat-count` | 6×3 | A2/east | A2 | F2 | falsche feste Anzahl |
| `product-a` | 6×6 | A6/north | A6 | D2 | eigener Lieferauftrag A |
| `product-b` | 6×6 | F6/north | F6 | B3 | eigener Lieferauftrag B |
| `product-c` | 6×6 | B1/south | B1 | F5 | eigener Lieferauftrag C |
| `repair-standard` | 5×3 | A2/east | A2 | E2 | standardisierte Revisionsspur |
| `extended-inherited` | 6×6 | F1/west | F1 | B5 | zusätzliche Ausführung und Reparatur |

Jeder Fall enthält nur synthetische Daten, gültige Hindernisse und eine bekannte Lösbarkeit. Das Handbuch enthält alle zwölf Punkte aus Spezifikationsabschnitt 25, beide Zeitpfade, Rollen für 1:1 und 1:2, erwartbare Fehler, frische Evidenzfälle, Modellgrenze, Voraussetzung und technische Fallbacks. `curriculum-mapping.json` bindet jeden der fünf Records an Segment, Tätigkeit, Produktspur und Grenze zu Klasse 7.

Die SVG-Datei verwendet nur projektintern gezeichnete geometrische Pfade, keine eingebettete Schrift, keine Rasterdaten, keine Marke. `assets/licenses.json` weist `delivery-robot.svg` als eigenes Werk unter CC BY-SA 4.0 aus.

- [ ] **Step 5: Registry und statische Assetvorbereitung implementieren**

Die Rendererzuordnung bleibt geschlossen:

```ts
function rendererFor(manifest: ModuleManifest, profile: BuildProfile) {
  if (
    profile === 'fixture'
    && manifest.id === 'TEST-PLATFORM-REFERENCE'
    && manifest.components.length === 1
    && manifest.components[0] === 'fixture-workspace'
  ) return 'fixture-workspace' as const;
  if (
    profile === 'production'
    && manifest.id === 'IUM-5-CORE-05'
    && manifest.components.length === 1
    && manifest.components[0] === 'algorithm-workbench'
  ) return 'algorithm-workbench' as const;
  throw new Error(`No static renderer contract for ${manifest.id}`);
}
```

Nur der Algorithmusrenderer lädt `content.json` und `scenarios.json`, validiert beide und schreibt das Bündel in die generierte Registry. `prepare-module-assets.ts` löscht ausschließlich `apps/lernwerk-portal/public/generated-modules`, legt es neu an und kopiert im Produktionsprofil genau die freigegebene SVG nach `generated-modules/ium-5-core-05/delivery-robot.svg`; das Fixtureprofil erzeugt keinen Modulassetpfad. `build-portal.ts` ruft dies vor dem Astrobuild auf. Ergänze denselben Zielpfad mit CC-BY-SA-4.0-Evidenz in der öffentlichen Assetliste und ignoriere den generierten Ordner.

- [ ] **Step 6: Ressourcen-, Registry-, Build- und Regressionstests grün ausführen**

```powershell
npm exec -- vitest run tests/platform/ium5-resources.test.ts tests/platform/registry.test.ts tests/platform/contracts.test.ts
npm run registry:production
npm run registry:fixture
npm run build
npm run build:fixture
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS; Registryprofile bleiben disjunkt; beide Builds finden ihre erforderlichen Quellen.

- [ ] **Step 7: Task 2 committen**

```powershell
git add .gitignore apps/lernwerk-portal/public/asset-licenses.json packages/ium-5-core-05/src modules/IUM-5-CORE-05 scripts/build-module-registry.ts scripts/prepare-module-assets.ts scripts/build-portal.ts tests/platform/ium5-resources.test.ts tests/platform/registry.test.ts
git commit -m "content: add IUM5 module resources"
```

---

### Task 3: Deterministischen Interpreter mit Schritt- und Gesamtlauf implementieren

**Files:**
- Create: `packages/ium-5-core-05/src/interpreter.ts`
- Modify: `packages/ium-5-core-05/src/index.ts`
- Test: `tests/platform/ium5-interpreter.test.ts`

**Interfaces:**
- Consumes: `Algorithm`, `Scenario`, `WorldState`, `TraceEntry`, `InterpreterErrorCode`, `MAX_EXECUTED_STEPS`.
- Produces: `ExecutionSession`, `beginExecution(scenario, algorithm)`, `stepExecution(session)`, `finishExecution(session)`, `missionSucceeded(scenario, state)`.
- Invariant: alle Rückgaben sind neue, tief kopierbare Werte; Eingaben werden nicht mutiert.

- [ ] **Step 1: Rote Semantik- und Fehlertests schreiben**

```ts
import { readFile } from 'node:fs/promises';
import { describe, expect, test } from 'vitest';
import {
  beginExecution,
  finishExecution,
  missionSucceeded,
  parseWorkbenchResources,
  stepExecution,
  type Algorithm,
  type Scenario,
} from '../../packages/ium-5-core-05/src/index.js';

const straight: Scenario = {
  id: 'straight', title: 'Gerade Lieferung', width: 6, height: 3,
  start: { position: { column: 1, row: 2 }, direction: 'east', carrying: false },
  itemPosition: { column: 1, row: 2 }, targetPosition: { column: 6, row: 2 },
  obstacles: [],
};

const algorithm: Algorithm = [
  { id: 'cmd-1', kind: 'pick-up' },
  { id: 'cmd-2', kind: 'repeat', count: 5, body: [{ id: 'cmd-3', kind: 'move' }] },
  { id: 'cmd-4', kind: 'drop' },
];

describe('deterministic interpreter', () => {
  test('step and full run produce the same trace and final state', () => {
    let stepped = beginExecution(straight, algorithm);
    while (stepped.status === 'ready' || stepped.status === 'running') {
      stepped = stepExecution(stepped);
    }
    const full = finishExecution(beginExecution(straight, algorithm));
    expect(stepped).toEqual(full);
    expect(missionSucceeded(straight, full.state)).toBe(true);
    expect(full.trace).toHaveLength(7);
    expect(full.trace[1]?.loop).toEqual({ iteration: 1, total: 5 });
  });

  test.each([
    ['OBSTACLE', [{ id: 'cmd-1', kind: 'move' }]],
    ['OUT_OF_BOUNDS', [{ id: 'cmd-1', kind: 'turn-left' }, { id: 'cmd-2', kind: 'move' }]],
    ['INVALID_PICK_UP', [{ id: 'cmd-1', kind: 'move' }, { id: 'cmd-2', kind: 'pick-up' }]],
    ['INVALID_DROP', [{ id: 'cmd-1', kind: 'drop' }]],
  ] as const)('stops with %s and leaves the failed state unchanged', (code, commands) => {
    const scenario = code === 'OBSTACLE'
      ? { ...straight, obstacles: [{ column: 2, row: 2 }] }
      : straight;
    const result = finishExecution(beginExecution(scenario, commands));
    expect(result.status).toBe('error');
    expect(result.error).toBe(code);
    expect(result.trace.at(-1)?.before).toEqual(result.trace.at(-1)?.after);
  });

  test('reports INVALID_REPEAT before moving', () => {
    const unsafe = [{ id: 'cmd-1', kind: 'repeat', count: 1, body: [{ id: 'cmd-2', kind: 'move' }] }];
    const result = beginExecution(straight, unsafe as Algorithm);
    expect(result.status).toBe('error');
    expect(result.error).toBe('INVALID_REPEAT');
    expect(result.trace).toHaveLength(1);
  });

  test('executes 100 basic steps and stops before step 101', () => {
    const many = Array.from({ length: 101 }, (_, index) => ({
      id: `cmd-${index + 1}`, kind: index % 2 === 0 ? 'turn-left' : 'turn-right',
    })) as Algorithm;
    const result = finishExecution(beginExecution(straight, many));
    expect(result.status).toBe('error');
    expect(result.error).toBe('STEP_LIMIT');
    expect(result.trace.at(-1)?.step).toBe(101);
  });

  test('does not mutate scenario or algorithm', () => {
    const scenarioBefore = structuredClone(straight);
    const algorithmBefore = structuredClone(algorithm);
    finishExecution(beginExecution(straight, algorithm));
    expect(straight).toEqual(scenarioBefore);
    expect(algorithm).toEqual(algorithmBefore);
  });

  test('every module reference algorithm completes its declared mission', async () => {
    const content = JSON.parse(await readFile(
      'modules/IUM-5-CORE-05/lernumgebung/content.json', 'utf8',
    ));
    const scenarios = JSON.parse(await readFile(
      'modules/IUM-5-CORE-05/lernumgebung/scenarios.json', 'utf8',
    ));
    const resources = parseWorkbenchResources(content, scenarios);
    expect(resources.ok).toBe(true);
    if (!resources.ok) return;
    for (const entry of resources.value.scenarios) {
      const result = finishExecution(beginExecution(
        entry.scenario, entry.referenceAlgorithm,
      ));
      expect(result.status, entry.scenario.id).toBe('complete');
      expect(missionSucceeded(entry.scenario, result.state), entry.scenario.id).toBe(true);
    }
  });
});
```

Ergänze separate Erwartungen für alle vier Startblickrichtungen, beide Drehungen, Aufnahme mit bereits getragenem Gut, Ablage außerhalb des Ziels und Ablage ohne Gut.

- [ ] **Step 2: Interpretertests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- vitest run tests/platform/ium5-interpreter.test.ts
```

Expected: FAIL wegen fehlender Interpreterexporte.

- [ ] **Step 3: Reinen unveränderlichen Interpreter implementieren**

`ExecutionSession`:

```ts
export type ExecutionStatus = 'ready' | 'running' | 'complete' | 'error';
export type ExecutionSession = Readonly<{
  scenarioId: string;
  status: ExecutionStatus;
  state: WorldState;
  program: readonly Readonly<{
    sourceCommandId: string;
    commandKind: BasicCommandKind;
    loop: Readonly<{ iteration: number; total: number }> | null;
  }>[];
  cursor: number;
  trace: readonly TraceEntry[];
  error: InterpreterErrorCode | null;
}>;
```

`beginExecution` validiert Algorithmus und Szenario erneut, expandiert feste Schleifen mit Iterationsmetadaten höchstens bis einschließlich des 101. Grundbefehls und erzeugt bei ungültigem Repeat einen unveränderten Fehlertrace. `stepExecution` führt genau einen expandierten Grundbefehl aus; Hindernis, Rastergrenze, Aufnahme und Ablage erzeugen einen Fehlertrace mit identischem Vorher-/Nachherzustand. `finishExecution` ruft `stepExecution` nur bis `complete` oder `error` auf. `missionSucceeded` ist nur wahr, wenn `delivered === true`, Gut und Roboter am Ziel sind und nichts mehr getragen wird.

- [ ] **Step 4: Interpreter und komplette Fachkernregression grün ausführen**

```powershell
npm exec -- vitest run tests/platform/ium5-interpreter.test.ts tests/platform/ium5-model.test.ts tests/platform/ium5-resources.test.ts
npm run typecheck
```

Expected: alle Prüfungen PASS.

- [ ] **Step 5: Task 3 committen**

```powershell
git add packages/ium-5-core-05/src/interpreter.ts packages/ium-5-core-05/src/index.ts tests/platform/ium5-interpreter.test.ts
git commit -m "feat: execute IUM5 algorithms deterministically"
```

---

### Task 4: Datensparsamen Produktpayload und geschlossene Importvalidierung implementieren

**Files:**
- Create: `packages/ium-5-core-05/src/payload.ts`
- Modify: `packages/ium-5-core-05/src/index.ts`
- Test: `tests/platform/ium5-payload.test.ts`
- Test: `tests/platform/runtime.test.ts`

**Interfaces:**
- Consumes: `Algorithm`, `Direction`, `Position`, `TraceEntry`, `LearningPhaseId`, Konstanten aus Task 1/2.
- Produces: `WorkbenchPayload`, `Prediction`, `EvidenceTrace`, `SystemClassification`, `SelfCheck`, `createInitialPayload()`, `parseWorkbenchPayload(value)`, `projectPersistentPayload(value)`.
- Invariant: Parser akzeptiert genau elf Top-Level-Felder und keinerlei Aktivitätsmetadaten.

- [ ] **Step 1: Rote Payload- und Datenminimierungstests schreiben**

```ts
import { describe, expect, test } from 'vitest';
import {
  createInitialPayload,
  parseWorkbenchPayload,
  projectPersistentPayload,
} from '../../packages/ium-5-core-05/src/index.js';

const allowed = [
  'phaseId', 'scenarioId', 'initialAlgorithm', 'prediction', 'evidenceTrace',
  'repairSource', 'repairHypothesis', 'revisedAlgorithm', 'loopDecision',
  'systemClassifications', 'selfCheck',
].sort();

describe('workbench payload', () => {
  test('starts with only the agreed product fields', () => {
    expect(Object.keys(createInitialPayload()).sort()).toEqual(allowed);
  });

  test.each(['elapsedMs', 'attemptCount', 'clicks', 'hintUsage', 'playbackSpeed', 'name'])
    ('rejects forbidden field %s', (field) => {
      const payload = { ...createInitialPayload(), [field]: 1 };
      expect(parseWorkbenchPayload(payload).ok).toBe(false);
    });

  test('limits explanations by Unicode code point instead of UTF-16 unit', () => {
    const valid = { ...createInitialPayload(), repairHypothesis: '🧭'.repeat(500) };
    const invalid = { ...createInitialPayload(), repairHypothesis: '🧭'.repeat(501) };
    expect(parseWorkbenchPayload(valid).ok).toBe(true);
    expect(parseWorkbenchPayload(invalid).ok).toBe(false);
  });

  test('returns a deep copy and never carries transient execution state', () => {
    const source = { ...createInitialPayload(), transientTrace: [{ step: 1 }] };
    const projected = projectPersistentPayload(source);
    expect(Object.keys(projected).sort()).toEqual(allowed);
    expect(projected).not.toBe(source);
  });

  test('rejects a future or malformed module payload without coercion', () => {
    expect(parseWorkbenchPayload({ ...createInitialPayload(), phaseId: 'future-phase' }).ok)
      .toBe(false);
    expect(parseWorkbenchPayload({ ...createInitialPayload(), initialAlgorithm: 'move' }).ok)
      .toBe(false);
  });

  test('rejects identifiers outside the closed content contract', () => {
    expect(parseWorkbenchPayload({ ...createInitialPayload(), scenarioId: 'unknown' }).ok)
      .toBe(false);
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      systemClassifications: [{
        caseId: 'unknown', classification: 'algorithmic', rationale: 'Begründung',
      }],
    }).ok).toBe(false);
  });

  test('rejects evidence beyond the hard execution limit', () => {
    const worldState = {
      position: { column: 1, row: 1 }, direction: 'east' as const, carrying: false,
      itemPosition: { column: 1, row: 1 }, delivered: false,
    };
    const evidenceTrace = {
      scenarioId: 'worked-sequence',
      entries: Array.from({ length: 102 }, (_, index) => ({
        step: index + 1,
        sourceCommandId: 'cmd-1',
        commandKind: 'turn-left',
        loop: null,
        before: worldState,
        after: worldState,
        outcome: 'ok',
        error: null,
      })),
      finalState: worldState,
      missionSucceeded: false,
    };
    expect(parseWorkbenchPayload({ ...createInitialPayload(), evidenceTrace }).ok)
      .toBe(false);
  });
});
```

Ergänze in `tests/platform/runtime.test.ts` den Modulfall: Eine Envelope mit `stateSchemaVersion: 2` wird bei Zielversion 1 fail-closed als `MIGRATION_FAILED` abgelehnt; `previewImport` verändert den aktiven Zustand bei Ablehnung nicht.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- vitest run tests/platform/ium5-payload.test.ts tests/platform/runtime.test.ts
```

Expected: FAIL wegen fehlender Payloadfunktionen.

- [ ] **Step 3: Exakten Payloadtyp und Parser implementieren**

```ts
export type Prediction = Readonly<{
  position: Position;
  direction: Direction;
  success: 'yes' | 'no' | 'unsure';
}>;

export type EvidenceTrace = Readonly<{
  scenarioId: WorkbenchScenarioId;
  entries: readonly TraceEntry[];
  finalState: WorldState;
  missionSucceeded: boolean;
}>;

export type SystemClassification = Readonly<{
  caseId: TransferCaseId;
  classification: 'algorithmic' | 'not-algorithmic' | 'needs-information';
  rationale: string;
}>;

export type SelfCheckValue = 'yes' | 'review' | 'not-applicable';
export type SelfCheck = Readonly<{
  unambiguous: SelfCheckValue;
  traceMatches: SelfCheckValue;
  repairJustified: SelfCheckValue;
  loopAppropriate: SelfCheckValue;
}>;

export type WorkbenchPayload = Readonly<{
  phaseId: LearningPhaseId;
  scenarioId: WorkbenchScenarioId;
  initialAlgorithm: Algorithm;
  prediction: Prediction | null;
  evidenceTrace: EvidenceTrace | null;
  repairSource: 'own-draft' | 'standard-error-case' | null;
  repairHypothesis: string;
  revisedAlgorithm: Algorithm | null;
  loopDecision: string;
  systemClassifications: readonly SystemClassification[];
  selfCheck: SelfCheck;
}>;
```

`createInitialPayload` startet mit `phaseId: 'ue1-orientation'`, `scenarioId: 'worked-sequence'`, leeren Algorithmen/Begründungen, `null` für noch nicht erzeugte Produktspuren, leerer Klassifikation und viermal `review`. `parseWorkbenchPayload` prüft geschlossene Schlüssel, alle verschachtelten Schlüssel, Algorithmen, höchstens 101 Traceeinträge, die zehn fest vereinbarten Szenario-IDs, die sechs fest vereinbarten Transferfall-IDs, Fall-ID- und Klassifikations-Eindeutigkeit sowie 500 Codepunkte je Freitext. `projectPersistentPayload` erstellt aus einem unbekannten Quellobjekt ausschließlich diese elf Felder und lässt den geschlossenen Parser über das Ergebnis laufen; bei ungültigem Produkt wirft es einen `TypeError` statt Daten zu raten.

- [ ] **Step 4: Payload-, Runtime- und Importregression grün ausführen**

```powershell
npm exec -- vitest run tests/platform/ium5-payload.test.ts tests/platform/runtime.test.ts tests/platform/export-import.test.ts
npm run typecheck
```

Expected: alle Prüfungen PASS; bestehende Fixturemigration auf Schema 2 bleibt unverändert.

- [ ] **Step 5: Task 4 committen**

```powershell
git add packages/ium-5-core-05/src/payload.ts packages/ium-5-core-05/src/index.ts tests/platform/ium5-payload.test.ts tests/platform/runtime.test.ts
git commit -m "feat: validate IUM5 learning products"
```

---

### Task 5: Produktionsroute und semantische Fokuswerkstatt statisch ausliefern

**Files:**
- Create: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Create: `apps/lernwerk-portal/src/styles/algorithm-workbench.css`
- Modify: `apps/lernwerk-portal/src/pages/module/[id].astro`
- Modify: `apps/lernwerk-portal/src/pages/index.astro`
- Modify: `apps/lernwerk-portal/astro.config.ts`
- Modify: `package.json`
- Create: `playwright.ium5.config.mts`
- Test: `tests/platform/portal-build.test.ts`
- Test: `tests/platform/build-quality.test.ts`

**Interfaces:**
- Consumes: Registryfelder `profile`, `renderer`, `publishedStatus`, `workbench` und `robotAssetPath`.
- Produces: DOM-Wurzel `[data-algorithm-workbench]` mit eingebettetem validierten Ressourcen-JSON.
- Produces: Rootbefehle `preview:ium5` und später `test:ium5:*` auf Port 4322.

- [ ] **Step 1: Rote Produktions-, Kennzeichnungs- und Isolierungstests schreiben**

Ersetze den alten Production-empty-Test durch:

```ts
test('production build exposes only the working IUM5 module route', async () => {
  const output = await buildPortal('production', '/');
  builds.push(output);
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/ium-5-core-05/index.html',
  ]);
  expect(await output.text('index.html')).toContain('Arbeitsstand · nicht für Unterrichtseinsatz');
  const moduleHtml = await output.text('module/ium-5-core-05/index.html');
  expect(moduleHtml).toContain('Präzise Abläufe ausführbar machen');
  expect(moduleHtml).toContain('Status working');
  expect(moduleHtml).toContain('data-algorithm-workbench');
  expect(moduleHtml).not.toContain('Synthetische technische Referenz');
});

test('fixture build contains no IUM5 renderer or identifier', async () => {
  const output = await buildPortal('fixture', '/');
  builds.push(output);
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/test-platform-reference/index.html',
  ]);
  const combined = `${await output.text('index.html')}\n${await output.text('module/test-platform-reference/index.html')}`;
  expect(combined).not.toContain('IUM-5-CORE-05');
  expect(combined).not.toContain('algorithm-workbench');
});
```

Ergänze `build-quality.test.ts` um einen Productionbuild, der Budgets, Null-Drittanbieter, Null-`TEST-`, OER-Kennzeichnung und vorhandene SVG-Lizenz prüft.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- vitest run tests/platform/portal-build.test.ts tests/platform/build-quality.test.ts
```

Expected: FAIL, weil Route noch immer die Fixturekomponente und -texte rendert.

- [ ] **Step 3: Geschlossene statische Rendererwahl und ehrliche Statusanzeige implementieren**

`[id].astro` verwendet keine dynamischen Imports und keinen Manifest-Komponentennamen als Pfad. Die Auswahl ist ein expliziter Zweig:

```astro
{module.renderer === 'fixture-workspace' ? (
  <FixtureWorkspace moduleId={module.id} moduleVersion={module.version} />
) : module.renderer === 'algorithm-workbench' && module.workbench ? (
  <AlgorithmWorkbench
    moduleId={module.id}
    moduleVersion={module.version}
    resources={module.workbench}
  />
) : (
  <p role="alert">Für dieses Modul fehlt ein freigegebener Renderer.</p>
)}
```

Für `publishedStatus === 'working'` stehen unmittelbar vor `h1` und in der Werkstatt sichtbar:

```html
<p class="working-banner" role="status">
  Arbeitsstand · Status working · nicht für Unterrichtseinsatz
</p>
```

Der Index nennt im Produktionsprofil „Arbeitsmodule“, nicht „veröffentlicht“ oder „Technische Referenz“, und der Link heißt „Arbeitsstand öffnen“. Das Fixtureprofil behält seinen bisherigen Wortlaut.

- [ ] **Step 4: Semantische Werkstatthülle und eingebettete Ressourcen anlegen**

`AlgorithmWorkbench.astro` enthält:

- Auftrag und Lernziel;
- Phasennavigation;
- Ausführungsraum mit `aria-labelledby` und textlicher Zustandsbeschreibung;
- Algorithmuseditor als geordnete Liste;
- Vorhersageformular;
- Ausführungssteuerung;
- Laufspurtabelle;
- Reparatur- und Begründungsfelder;
- Hilfenbereich;
- Algorithmus-Lupe;
- vierteiligen Selbstcheck;
- lokale Speicher-, Export-, Import- und Löschkontrollen mit Sensibilitätshinweis;
- dieselben Import-/Löschdialoge wie der Plattformvertrag, aber mit modulbezogenen IDs.

Das validierte Ressourcenbündel wird als sicher serialisiertes JSON eingebettet. Vor `set:html` werden `<`, `>`, `&`, U+2028 und U+2029 in Unicode-Escapes umgewandelt; der Controller liest ausschließlich `textContent` des `application/json`-Elements.

Die erste CSS-Fassung setzt `.workbench-focus` als zwei Spalten `minmax(0, 1fr)` und stapelt sie unter 48rem. Der Ausführungsraum steht in DOM-Reihenfolge vor dem Editor; Laufspur und Revision folgen direkt danach.

- [ ] **Step 5: Profilebundles symmetrisch isolieren und IUM5-Preview konfigurieren**

Der bestehende Vite-Pluginzweig entfernt im Produktionsprofil nur `FixtureWorkspace`-Bundles und im Fixtureprofil nur `AlgorithmWorkbench`-/`algorithm-workbench`-Bundles. `playwright.ium5.config.mts` nutzt `tests/browser/ium5-*.spec.ts`, Base-URL `http://127.0.0.1:4322`, denselben Browserstand und Webserverkommando `npm run preview:ium5`. Rootscript:

```json
"preview:ium5": "tsx scripts/preview-portal.ts production / 4322"
```

- [ ] **Step 6: Route, Buildqualität, Typen und bestehende Fixturetests grün ausführen**

```powershell
npm exec -- vitest run tests/platform/portal-build.test.ts tests/platform/build-quality.test.ts tests/platform/registry.test.ts
npm run build
npm run build:fixture
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS; Production und Fixture enthalten jeweils nur ihren erlaubten Renderer.

- [ ] **Step 7: Task 5 committen**

```powershell
git add package.json playwright.ium5.config.mts apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/styles/algorithm-workbench.css apps/lernwerk-portal/src/pages/module/[id].astro apps/lernwerk-portal/src/pages/index.astro apps/lernwerk-portal/astro.config.ts tests/platform/portal-build.test.ts tests/platform/build-quality.test.ts
git commit -m "feat: render the IUM5 working module"
```

---

### Task 6: Schaltflächeneditor und verpflichtende Vorhersage umsetzen

**Files:**
- Create: `packages/ium-5-core-05/src/editor.ts`
- Modify: `packages/ium-5-core-05/src/index.ts`
- Create: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Create: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Test: `tests/platform/ium5-editor.test.ts`
- Create: `tests/browser/ium5-workbench.spec.ts`

**Interfaces:**
- Produces: `insertCommand`, `moveCommand`, `removeCommand`, `replaceRepeat`, `nextCommandId` als unveränderliche beziehungsweise reine Funktionen.
- Produces: `connectAlgorithmWorkbench(root?: ParentNode): Promise<void>`.
- Viewereignisse: `ium5:algorithm-change`, `ium5:prediction-confirm`, `ium5:run-step`, `ium5:run-all`, `ium5:revision-confirm`.

- [ ] **Step 1: Rote Editor- und Browsertests schreiben**

```ts
import { describe, expect, test } from 'vitest';
import {
  insertCommand, moveCommand, nextCommandId, removeCommand, replaceRepeat,
} from '../../packages/ium-5-core-05/src/index.js';

describe('immutable command editor', () => {
  test('inserts, moves and removes without mutating the source', () => {
    const source = [{ id: 'cmd-1', kind: 'move' }] as const;
    const inserted = insertCommand(source, 1, { id: 'cmd-2', kind: 'turn-right' });
    expect(inserted.map((command) => command.id)).toEqual(['cmd-1', 'cmd-2']);
    expect(moveCommand(inserted, 1, -1).map((command) => command.id))
      .toEqual(['cmd-2', 'cmd-1']);
    expect(removeCommand(inserted, 0).map((command) => command.id)).toEqual(['cmd-2']);
    expect(source).toEqual([{ id: 'cmd-1', kind: 'move' }]);
  });

  test('rejects an invalid repeat edit instead of normalizing it', () => {
    const source = [{
      id: 'cmd-1', kind: 'repeat', count: 2,
      body: [{ id: 'cmd-2', kind: 'move' }],
    }] as const;
    expect(() => replaceRepeat(source, 0, {
      id: 'cmd-1', kind: 'repeat', count: 1, body: [{ id: 'cmd-2', kind: 'move' }],
    })).toThrow();
  });

  test('continues identifiers after imported top-level and loop commands', () => {
    expect(nextCommandId([
      { id: 'cmd-2', kind: 'move' },
      { id: 'cmd-4', kind: 'repeat', count: 2, body: [{ id: 'cmd-7', kind: 'move' }] },
    ])).toBe('cmd-8');
  });
});
```

Browsertest:

```ts
test('builds an algorithm by buttons and requires a prediction before execution', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Nimm auf einfügen' }).click();
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(2);
  await page.getByRole('button', { name: 'Befehl 2 nach oben' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeDisabled();
  await page.getByLabel('Erwartete Endposition').selectOption('A3');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('north');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('unsure');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeEnabled();
});
```

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- vitest run tests/platform/ium5-editor.test.ts
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts --project=chromium
```

Expected: Unit- und Browsertest FAIL wegen fehlender Funktionen und Controller.

- [ ] **Step 3: Reine Editoroperationen implementieren**

Alle Funktionen kopieren vor der Änderung, validieren das Ergebnis mit `parseAlgorithm` und werfen bei ungültigem Index, Delta oder Befehl einen `RangeError` beziehungsweise `TypeError`. `moveCommand` akzeptiert nur `-1` oder `1`; Bewegung über Listenanfang/-ende ist ein No-op mit neuer Kopie. `nextCommandId` durchsucht Hauptfolge und Schleifenkörper und liefert eins größer als die höchste vorhandene Nummer, mindestens `cmd-1`; dadurch bleiben IDs nach Reload und Import eindeutig. Schleifenkörper werden über eigene beschriftete Schaltflächen bearbeitet, niemals über Drag.

- [ ] **Step 4: View und Vorhersagegating minimal verbinden**

`workbench-view.ts` rendert Befehle ausschließlich mit `textContent`, nummeriert sie fachlich sichtbar und liefert pro Block `nach oben`, `nach unten`, `löschen`. Der Controller hält zunächst `createInitialPayload()` im Speicher, erzeugt IDs monoton als `cmd-1`, `cmd-2` und verwirft eine bestätigte Vorhersage bei jeder inhaltlichen Algorithmusänderung. Ausführungsschaltflächen sind genau dann aktiv, wenn `prediction !== null` und der aktuelle Algorithmus seit der Bestätigung unverändert ist.

Die Vorhersagefelder sind strukturiert und unbewertet. Es erscheint ausschließlich „Vorhersage gespeichert – jetzt prüfen“, niemals richtig/falsch vor der Ausführung.

- [ ] **Step 5: Unit- und Browsertests grün ausführen**

```powershell
npm exec -- vitest run tests/platform/ium5-editor.test.ts tests/platform/ium5-model.test.ts
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts --project=chromium
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS.

- [ ] **Step 6: Task 6 committen**

```powershell
git add packages/ium-5-core-05/src/editor.ts packages/ium-5-core-05/src/index.ts apps/lernwerk-portal/src/controllers/algorithm-workbench apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro tests/platform/ium5-editor.test.ts tests/browser/ium5-workbench.spec.ts
git commit -m "feat: add IUM5 editor and prediction gate"
```

---

### Task 7: Ausführung, Laufspur, Fehlerfeedback und Revisionsvertrag verbinden

**Files:**
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `apps/lernwerk-portal/src/styles/algorithm-workbench.css`
- Modify: `tests/browser/ium5-workbench.spec.ts`

**Interfaces:**
- Consumes: Interpreter aus Task 3 und Payload aus Task 4.
- Produces: transiente `ExecutionSession`, bestätigte `EvidenceTrace`, `repairSource`, `repairHypothesis`, `revisedAlgorithm`, `loopDecision`.
- Invariant: nur bestätigte Belegspur gelangt in den Payload; Fehlversuchshistorie bleibt im Controller und wird beim Neuladen verworfen.

- [ ] **Step 1: Rote vollständige Lernzyklus- und Fehlerfeedbacktests ergänzen**

```ts
test('predicts, steps, traces, hypothesizes and confirms a repaired algorithm', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  const trace = page.getByRole('table', { name: 'Laufspur' });
  await expect(trace).toContainText('Iteration');
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
    .toContainText('Auftrag noch nicht erfüllt');
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().check();
  await page.getByLabel('Reparaturhypothese').fill(
    'Die Wiederholungszahl ist zu klein. Mit vier Schritten erreicht der Roboter das Ziel.',
  );
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await page.getByLabel('Wiederholungszahl').fill('4');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeDisabled();
});

test('shows cause and state before an optional strategy hint', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Drehung öffnen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('C2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
    .toContainText(/Schritt .*Blickrichtung/);
  await expect(page.getByRole('button', { name: 'Strategiehinweis öffnen' })).toBeVisible();
  await expect(page.getByText('Vollständiges Beispiel')).toBeHidden();
});
```

Ergänze Tests für Hindernis, Rastergrenze, ungültige Aufnahme, ungültige Ablage, ungültige Wiederholungszahl und Schrittgrenze sowie für Schritt-/Gesamtlauf mit identischer sichtbarer Endspur. Der Wiederholungstest setzt im sichtbaren Schleifenzahlfeld `1`, erwartet einen deaktivierten Ausführungsstart und die Meldung „Wiederholungszahl muss zwischen 2 und 9 liegen“ mit Verweis auf den fehlerhaften Block; damit sind alle sechs Interpreterfehler auch an ihrer Oberflächengrenze geprüft.

- [ ] **Step 2: Browsertests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts --project=chromium
```

Expected: neue Lernzyklus- und Fehlerfälle FAIL.

- [ ] **Step 3: Interpreterzustand und sichtbare Laufspur verbinden**

Der Controller beginnt jede Ausführung neu aus Szenario plus aktuell bestätigtem Algorithmus. `Schritt ausführen` ruft genau einmal `stepExecution`, `Vollständig ausführen` genau einmal `finishExecution`. Die View rendert für jeden Traceeintrag Nummer, Quellbefehl, Iteration, Vorherposition/-blick/-tragezustand, Nachherzustand und Ergebnis. Aktueller Befehl, Position, Blickrichtung, Tragezustand und Schleifeniteration stehen zugleich als sichtbarer Text und in einer höflichen Live-Region.

Ergebnisstaffelung:

1. Auftrag erfüllt oder noch nicht erfüllt;
2. verursachender Schritt und Zustand;
3. expliziter Vergleich mit Vorhersage;
4. Strategiehinweis erst nach Klick;
5. vollständiges Beispiel erst nach zweitem ausdrücklichem Klick.

- [ ] **Step 4: Reparaturquelle und Sonderfall „sofort korrekt“ implementieren**

Bei eigener Abweichung setzt der Controller `repairSource: 'own-draft'`, speichert erst nach Bestätigung die ausgewählte Belegspur und verlangt Hypothese vor Revision. Ist der erste eigene Lauf fachlich vollständig korrekt, bleibt das Produkt unverändert und der Controller lädt deterministisch `repair-standard`; erst dessen Revisionsspur setzt `repairSource: 'standard-error-case'`. Es wird kein Fehler in den eigenen Algorithmus eingefügt und kein personenbezogenes Merkmal gespeichert.

Nach jeder inhaltlichen Revision werden Vorhersage und transiente Ausführung verworfen. Eine neue Vorhersage ist erforderlich. Die bestätigte Schleifenbegründung akzeptiert maximal 500 Codepunkte und wird nicht automatisch bewertet.

- [ ] **Step 5: Lernzyklus, Interpreterregression und Typen grün ausführen**

```powershell
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts --project=chromium
npm exec -- vitest run tests/platform/ium5-interpreter.test.ts tests/platform/ium5-payload.test.ts
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS.

- [ ] **Step 6: Task 7 committen**

```powershell
git add apps/lernwerk-portal/src/controllers/algorithm-workbench apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/styles/algorithm-workbench.css tests/browser/ium5-workbench.spec.ts
git commit -m "feat: add IUM5 trace and revision cycle"
```

---

### Task 8: Local-First-Speicherung, Export, Import und Löschung anbinden

**Files:**
- Create: `apps/lernwerk-portal/src/controllers/algorithm-workbench/browser-ports.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Create: `tests/browser/ium5-state.spec.ts`

**Interfaces:**
- Consumes: `createStateRepository`, `createModuleRuntime`, `parseWorkbenchPayload`, `projectPersistentPayload`.
- Produces: bestätigte Speicherung mit 250-ms-Debounce, Export-/Kopierfallback, fail-closed Importvorschau und bestätigte Löschung.
- Invariant: `targetStateSchemaVersion: 1`, `migrations: []`; unbekannte zukünftige Schemafassung bleibt abgelehnt.

- [ ] **Step 1: Rote Verlustfreiheits- und Datenminimierungstests schreiben**

```ts
test('reload, export, delete and import preserve only the learning product', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await page.reload();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);

  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand exportieren' }).click();
  const path = await (await download).path();
  const exported = JSON.parse(await readFile(path!, 'utf8'));
  expect(Object.keys(exported.payload).sort()).toEqual([
    'evidenceTrace', 'initialAlgorithm', 'loopDecision', 'phaseId', 'prediction',
    'repairHypothesis', 'repairSource', 'revisedAlgorithm', 'scenarioId',
    'selfCheck', 'systemClassifications',
  ]);
  expect(JSON.stringify(exported.payload)).not.toMatch(
    /elapsed|attempt|click|hint|playback|focus|navigation/i,
  );

  await page.getByRole('button', { name: 'Arbeitsstand löschen' }).click();
  await page.getByRole('button', { name: 'Löschen bestätigen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(0);
  await page.setInputFiles('input[type=file]', path!);
  await page.getByRole('button', { name: 'Import übernehmen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);
});

test('rejects a malformed module payload without changing active work', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await page.setInputFiles('input[type=file]', {
    name: 'invalid.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      format: 'ium-learning-state', formatVersion: 1,
      moduleId: 'IUM-5-CORE-05', moduleVersion: '0.1.0', stateSchemaVersion: 1,
      workspaceId: '11111111-1111-4111-8111-111111111111',
      savedAt: '2026-08-03T00:00:00.000Z', payload: { name: 'Person' },
    })),
  });
  await expect(page.getByRole('heading', { name: 'Import prüfen' })).toBeHidden();
  await expect(page.getByRole('alert')).toContainText('nicht übernommen');
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);
});
```

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- playwright test tests/browser/ium5-state.spec.ts --config playwright.ium5.config.mts --project=chromium
```

Expected: FAIL, weil der Controller noch flüchtig arbeitet.

- [ ] **Step 3: Bestehende Runtime ohne Plattformänderung anbinden**

`browser-ports.ts` enthält nur den modulspezifischen `ExportPort` und kryptografisch erzeugte UUID wie die Fixture, importiert aber keinen Fixturecode. Der Controller wählt über `?storage=volatile` bewusst flüchtigen Modus, sonst persistent mit vorhandenem Fallback. Er startet `ModuleRuntime` mit Modul-ID/-version, Schema 1 und leerer Migrationsliste.

Bei leerem Runtimepayload wird `createInitialPayload()` geschrieben und bestätigt gespeichert. Bei vorhandenem Payload muss `parseWorkbenchPayload` erfolgreich sein; andernfalls zeigt die Oberfläche einen fail-closed Fehler, verändert oder überschreibt den gespeicherten Stand nicht und deaktiviert Fachinteraktionen bis Löschen oder gültigem Import.

Jede fachliche Produktänderung projiziert zuerst `projectPersistentPayload`, aktualisiert Runtime und speichert nach 250 ms. Vor Export, Sichtbarkeitswechsel und `ium:flush-request` wird sofort bestätigt gespeichert.

- [ ] **Step 4: Import- und Löschvertrag fail-closed verbinden**

Nach `runtime.previewImport` prüft der Controller zusätzlich `parseWorkbenchPayload(preview.state.payload)`. Nur dann wird der bestehende Bestätigungsdialog gezeigt. Ablehnung leert die Dateiauswahl und lässt den aktiven Zustand unverändert. Nach bestätigtem Import wird ausschließlich der validierte Payload gerendert. Löschung startet Runtime neu, erzeugt den Initialpayload, speichert ihn bestätigt und fokussiert die Werkstattüberschrift.

Export behält den vorhandenen Sensibilitätshinweis; das Fallbacktextfeld enthält exakt dieselben validierten Bytes wie der Download.

- [ ] **Step 5: Zustands-, Runtime-, Browser- und Typprüfungen grün ausführen**

```powershell
npm exec -- playwright test tests/browser/ium5-state.spec.ts --config playwright.ium5.config.mts --project=chromium
npm exec -- vitest run tests/platform/ium5-payload.test.ts tests/platform/runtime.test.ts tests/platform/export-import.test.ts tests/platform/local-state.test.ts
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS.

- [ ] **Step 6: Task 8 committen**

```powershell
git add apps/lernwerk-portal/src/controllers/algorithm-workbench apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro tests/browser/ium5-state.spec.ts
git commit -m "feat: persist IUM5 products locally"
```

---

### Task 9: Vollständigen Fünf-/Sechs-UE-Lernpfad, Hilfen, Transfer und Selbstcheck umsetzen

**Files:**
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `apps/lernwerk-portal/src/styles/algorithm-workbench.css`
- Modify: `tests/browser/ium5-workbench.spec.ts`
- Modify: `tests/browser/ium5-state.spec.ts`
- Test: `tests/platform/ium5-resources.test.ts`

**Interfaces:**
- Consumes: validierte Segmente, Aktivitäten, Hilfen, Szenarien, Transferfälle und Selbstcheckfragen.
- Produces: regulärer Pfad über fünf UE; bei explizitem `?path=extended` zusätzliche sechste UE.
- Invariant: Pfadwahl und Hilfenutzung bleiben flüchtig; sie erscheinen nicht im Payload.

- [ ] **Step 1: Rote Pfad-, Hilfen-, Transfer- und Exporttests ergänzen**

```ts
test('exposes all five task families and the regular five-lesson path', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  for (const [button, heading] of [
    ['Präzisionskontrast öffnen', 'Präzisionskontrast'],
    ['Aktives Beispiel öffnen', 'Aktives Beispiel'],
    ['Gezielte Fehlerfälle öffnen', 'Gezielte Fehlerfälle'],
    ['Eigenen Lieferauftrag öffnen', 'Eigener Lieferauftrag'],
    ['Algorithmus-Lupe öffnen', 'Algorithmus-Lupe'],
  ]) {
    await page.getByRole('button', { name: button }).click();
    await expect(page.getByRole('heading', { name: heading })).toBeVisible();
  }
  await expect(page.getByText('225 Minuten · 5 Unterrichtseinheiten')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Zusätzliche Fehlerwerkstatt' }))
    .toBeHidden();
});

test('shows the sixth lesson only through the explicit extended path', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/?path=extended');
  await expect(page.getByText('270 Minuten · 6 Unterrichtseinheiten')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Zusätzliche Fehlerwerkstatt' }))
    .toBeVisible();
  await expect(page.getByText('extended-inherited')).not.toBeVisible();
});

test('stores classifications and self-check but never support usage', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Drehhilfe öffnen' }).click();
  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill(
    'Die Route wird durch eine präzise Folge algorithmischer Schritte bestimmt.',
  );
  await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand exportieren' }).click();
  const path = await (await download).path();
  const exported = JSON.parse(await readFile(path!, 'utf8'));
  expect(exported.payload.systemClassifications).toHaveLength(1);
  expect(exported.payload.selfCheck.unambiguous).toBe('yes');
  expect(JSON.stringify(exported)).not.toMatch(/Drehhilfe|support|hint/i);
});
```

Ergänze Ressourcentests, die die exakten Phasensummen `15/20/35/45/55/35/20` und erweitert `15/20/35/60/75/40/25` berechnen sowie sicherstellen, dass die Erweiterung `extended-inherited` tatsächlich Vorhersage, Ausführung, Fehlerlokalisierung, Hypothese, Revision und Vergleich verlangt.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- vitest run tests/platform/ium5-resources.test.ts
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts tests/browser/ium5-state.spec.ts --config playwright.ium5.config.mts --project=chromium
```

Expected: neue Pfad- und Transfererwartungen FAIL.

- [ ] **Step 3: Phasennavigation und drei gleichwertige Produktkarten verbinden**

Die Navigation zeigt UE und Lernfunktion, nicht Punktestand oder Fortschrittsprozent. Lernende oder Lehrkraft wechseln bewusst; der Controller persistiert nur `phaseId`. Im Produktsegment kann Karte A, B oder C gewählt werden; alle drei verwenden denselben Qualitätsvertrag. Karte wird als `scenarioId` gespeichert. Wechsel nach bestätigter Vorhersage verlangt eine ausdrückliche Bestätigung, weil er Produktspuren verwirft.

Der erweiterte Pfad wird ausschließlich aus `new URLSearchParams(location.search).get('path') === 'extended'` abgeleitet. Er wird nicht gespeichert und nicht automatisch empfohlen. Ohne Parameter bleibt UE6 vollständig ausgeblendet.

- [ ] **Step 4: Hilfen flüchtig und nichtadaptiv implementieren**

Jede Hilfe öffnet nur nach Schaltflächenklick einen benannten Bereich. Der Controller führt keine Zähler, Zeitstempel oder Auswahlhistorie. Hilfen schließen automatisch keine andere Hilfe und verschwinden nicht aufgrund vermeintlicher Leistung. Die vollständige Lösung ist ausschließlich im aktiven Beispiel und nach ausdrücklicher Feedbackstaffelung erreichbar.

- [ ] **Step 5: Algorithmus-Lupe und Selbstcheck speichern**

Jeder Transferfall besitzt eine Auswahl `algorithmic`, `not-algorithmic`, `needs-information` sowie bis 500 Codepunkte Begründung. Keine Auswahl wird automatisch bepunktet. Der Fahrzeuggrenzfall fordert sichtbar die fehlende Information „direkt ferngesteuert oder gespeicherter Ablauf“. Der Selbstcheck besitzt genau vier Felder mit `yes`, `review`, `not-applicable`; daraus folgt keine automatische Empfehlung.

- [ ] **Step 6: Lernpfad-, Zustands- und Inhaltsprüfungen grün ausführen**

```powershell
npm exec -- vitest run tests/platform/ium5-resources.test.ts tests/platform/ium5-payload.test.ts
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts tests/browser/ium5-state.spec.ts --config playwright.ium5.config.mts --project=chromium
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS.

- [ ] **Step 7: Task 9 committen**

```powershell
git add apps/lernwerk-portal/src/controllers/algorithm-workbench apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/styles/algorithm-workbench.css tests/browser/ium5-workbench.spec.ts tests/browser/ium5-state.spec.ts tests/platform/ium5-resources.test.ts
git commit -m "feat: complete the IUM5 learning path"
```

---

### Task 10: Gleichwertige Tastatur-, Touch-, Screenreader- und Reflowpfade sichern

**Files:**
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/styles/algorithm-workbench.css`
- Create: `tests/browser/ium5-accessibility.spec.ts`

**Interfaces:**
- Consumes: vollständige Werkstatt aus Tasks 5–9.
- Produces: semantische Bereiche, zugängliche Zustands- und Laufspurtexte, Fokusregeln, reduzierte Bewegung und Reflow.
- Invariant: Keine Information oder Aktion hängt ausschließlich von Farbe, Position, Bewegung, Canvas oder Drag ab.

- [ ] **Step 1: Rote Accessibility-, Tastatur- und Reflowtests schreiben**

```ts
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test('has no automatically detectable accessibility violations', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  const result = await new AxeBuilder({ page }).analyze();
  expect(result.violations).toEqual([]);
});

test('completes the core learning cycle by keyboard', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).focus();
  await page.keyboard.press('Enter');
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).press('Enter');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).press('Enter');
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().press('Space');
  await page.getByLabel('Reparaturhypothese').fill(
    'Die Wiederholungszahl ist zu klein; ein weiterer Schritt führt zum Ziel.',
  );
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).press('Enter');
  await page.getByLabel('Wiederholungszahl').fill('4');
  await page.getByRole('button', { name: 'Revision übernehmen' }).press('Enter');
  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeDisabled();
  await page.getByRole('button', { name: 'UE 5 · Transfer' }).press('Enter');
  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill(
    'Eine präzise Folge von Anweisungen bestimmt die Route.',
  );
  await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
});

test('provides a complete textual scene and trace without the visual grid', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await expect(page.getByRole('region', { name: 'Szenenbeschreibung' }))
    .toContainText(/Position|Blickrichtung|Gut|Ziel|Hindernisse/);
  await expect(page.getByRole('table', { name: 'Laufspur' })).toBeVisible();
});

test('reflows at 320 CSS pixels without horizontal page scroll', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto('/module/ium-5-core-05/');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth))
    .toBe(true);
});

test('remains usable at 200 percent zoom', async ({ page }) => {
  await page.setViewportSize({ width: 640, height: 900 });
  await page.goto('/module/ium-5-core-05/');
  await page.evaluate(() => document.documentElement.style.setProperty('zoom', '2'));
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth))
    .toBe(true);
  await expect(page.getByRole('button', { name: 'Gehe einfügen' })).toBeVisible();
});

test.use({ reducedMotion: 'reduce' });
test('uses step execution without motion under reduced motion', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await expect(page.locator('[data-robot]')).toHaveCSS('transition-duration', '0s');
});
```

Ergänze den gleichwertigen Touchpfad ohne Drag:

```ts
test.describe('touch-only core path', () => {
  test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });

  test('edits, predicts, executes, repairs and transfers by touch controls', async ({ page }) => {
    await page.goto('/module/ium-5-core-05/');
    await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).tap();
    await page.getByLabel('Erwartete Endposition').selectOption('E2');
    await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
    await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
    await page.getByRole('button', { name: 'Vorhersage bestätigen' }).tap();
    await page.getByRole('button', { name: 'Vollständig ausführen' }).tap();
    await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().tap();
    await page.getByLabel('Reparaturhypothese').fill(
      'Die Wiederholungszahl ist zu klein; ein weiterer Schritt führt zum Ziel.',
    );
    await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).tap();
    await page.getByLabel('Wiederholungszahl').fill('4');
    await page.getByRole('button', { name: 'Revision übernehmen' }).tap();
    await page.getByRole('button', { name: 'UE 5 · Transfer' }).tap();
    await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
    await page.getByLabel('Begründung zu Navigation').fill(
      'Eine präzise Folge von Anweisungen bestimmt die Route.',
    );
    await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
    await expect(page.locator('[draggable="true"]')).toHaveCount(0);
  });
});
```

Fokusprüfungen erwarten nach Import die Werkstattüberschrift, nach Löschen die Werkstattüberschrift, nach einem echten Fachfehler die fokussierte Fehlerzusammenfassung und nach Phasenwechsel die neue Phasenüberschrift. Eine tabellarische Reflowprüfung verwendet zusätzlich `{ width: 360, height: 640 }` und `{ width: 640, height: 360 }` und erwartet in Hoch- und Querformat keinen horizontalen Seitenscroll.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- playwright test tests/browser/ium5-accessibility.spec.ts --config playwright.ium5.config.mts --project=chromium
```

Expected: mindestens Reflow-, Fokus- oder reduzierte-Bewegung-Prüfungen FAIL.

- [ ] **Step 3: Semantik, Live-Regionen und Textäquivalent vervollständigen**

Verwende Landmarks und beschriftete `section`, echte `button`, `label`, `fieldset`, `legend`, `ol` und `table`. Aktueller Schritt ist `aria-live="polite"`; Fehlerzusammenfassung bleibt fokussierbar und verwendet den bestehenden Errorannouncer. Das visuelle Raster ist `aria-hidden="true"`; direkt daneben beschreibt dieselbe Controllerzustandsquelle Position, Blickrichtung, Gut, Ziel und Hindernisse in Text. Laufspur besitzt eine Caption und ausgeschriebene Zustandszellen.

Nach Einfügen bleibt Fokus am ausgelösten Befehlstyp, nach Verschieben am verschobenen Block, nach Löschen am logisch nächsten Block oder Einfügebereich. Kein Fokus wird in Live-Regionen gezwungen; nur echte Fehlerzusammenfassung erhält Fokus.

- [ ] **Step 4: Responsive und reduzierte CSS-Regeln implementieren**

Kein Element setzt eine feste Mindestbreite über 0 innerhalb der Fokusspalten. Editorzeilen und Aktionen umbrechen, Tabellen liegen in einem beschrifteten Scrollcontainer, die Seite selbst scrollt nicht horizontal. Unter 48rem steht Ausführungsraum vor Editor. Bei `prefers-reduced-motion: reduce` sind alle Transitionen und Laufanimationen deaktiviert; Schrittzustände wechseln unmittelbar.

- [ ] **Step 5: Accessibility und Browsermatrix grün ausführen**

```powershell
npm exec -- playwright test tests/browser/ium5-accessibility.spec.ts --config playwright.ium5.config.mts --project=chromium
npm exec -- playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts
npm run typecheck
npm run check:astro
```

Expected: Accessibilitytests PASS; Kernlernzyklus PASS in Chromium, Firefox und WebKit.

- [ ] **Step 6: Task 10 committen**

```powershell
git add apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts apps/lernwerk-portal/src/styles/algorithm-workbench.css tests/browser/ium5-accessibility.spec.ts
git commit -m "feat: make IUM5 workbench accessible"
```

---

### Task 11: Offline-, Lizenz-, Dokumentations- und CI-Gates schließen

**Files:**
- Create: `tests/browser/ium5-offline.spec.ts`
- Create: `scripts/verify-ium5.ts`
- Create: `docs/modules/ium-5-core-05.md`
- Modify: `package.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `docs/platform/README.md`
- Modify: `tests/platform/documentation.test.ts`
- Modify: `tests/platform/pages-workflow.test.ts`
- Modify: `tests/platform/license-policy.test.ts`
- Modify: `tests/platform/build-quality.test.ts`

**Interfaces:**
- Produces: `npm run test:ium5:browser`, `test:ium5:state`, `test:ium5:accessibility`, `test:ium5:offline`, `verify:ium5`.
- Produces: dieselben vier CI-Jobs mit zusätzlichen Modulschritten, kein fünfter Deployjob.
- Invariant: Pages-Workflow bleibt Fixture-only; `verify:ium5` setzt `device-verified` nicht.

- [ ] **Step 1: Rote Offline-, Dokumentations- und Workflowtests schreiben**

`ium5-offline.spec.ts` baut Produktionskandidaten mit diesem lokalen Helfer; er kopiert zuerst alle Assets und zuletzt `sw.js` in das vom Previewserver ausgelieferte Verzeichnis:

```ts
const repoRoot = process.cwd();
const productionOutput = resolve(repoRoot, 'apps/lernwerk-portal/dist');

async function publishIum5Candidate(options: {
  buildRevision: string;
  removeBeforeWorker?: readonly string[];
}): Promise<void> {
  const candidate = await mkdtemp(join(tmpdir(), 'ium5-update-candidate-'));
  try {
    await buildPortalToDirectory({
      profile: 'production', base: '/', rootDir: repoRoot,
      outputDir: candidate, buildRevision: options.buildRevision,
    });
    for (const entry of await readdir(candidate, { withFileTypes: true })) {
      if (entry.name === 'sw.js' || entry.name === '.vite-cache') continue;
      await cp(resolve(candidate, entry.name), resolve(productionOutput, entry.name), {
        recursive: entry.isDirectory(), force: true,
      });
    }
    for (const relativePath of options.removeBeforeWorker ?? []) {
      await rm(resolve(productionOutput, relativePath), { force: true });
    }
    await copyFile(resolve(candidate, 'sw.js'), resolve(productionOutput, 'sw.js'));
  } finally {
    await rm(candidate, { recursive: true, force: true });
  }
}
```

```ts
test('completes the installed IUM5 core path offline with local state', async ({ context, page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await page.evaluate(async () => navigator.serviceWorker.ready);
  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Präzise Abläufe ausführbar machen' }))
    .toBeVisible();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('table', { name: 'Laufspur' })).toBeVisible();
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().check();
  await page.getByLabel('Reparaturhypothese').fill(
    'Die Wiederholungszahl ist zu klein; ein weiterer Schritt führt zum Ziel.',
  );
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await page.getByLabel('Wiederholungszahl').fill('4');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  await page.getByRole('button', { name: 'UE 5 · Transfer' }).click();
  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill(
    'Eine präzise Folge von Anweisungen bestimmt die Route.',
  );
  await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await context.setOffline(false);
});
```

Der kontrollierte Updatetest ruft `publishIum5Candidate({ buildRevision: 'ium5-candidate-2' })` auf, wartet auf sichtbaren Updateprompt, ändert davor einen Algorithmus, aktiviert erst über „Speichern und aktualisieren“ und erwartet danach denselben Algorithmus. Der Fail-closed-Test ruft `publishIum5Candidate({ buildRevision: 'ium5-broken', removeBeforeWorker: ['generated-modules/ium-5-core-05/delivery-robot.svg'] })` auf; der Kandidat wird redundant und der aktive Stand bleibt offline nutzbar.

Dokumentationstests erwarten für das Root-README:

```ts
for (const required of [
  'docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md',
  'docs/superpowers/plans/2026-08-03-ium-5-core-05-implementation.md',
  'docs/modules/ium-5-core-05.md',
  'npm run verify:ium5',
  'working', 'nicht für Unterrichtseinsatz', 'Gate B', 'device-verified: not-run',
]) expect(await readFile('README.md', 'utf8')).toContain(required);
```

Für `docs/platform/README.md` erwarten sie `Phase-1-Ausgangsstand`, `production-empty`, `IUM-5-CORE-05`, `working` und `nicht deployt`. Damit bleibt der frühere Produktionszustand nachvollziehbar, wird aber nicht länger als aktueller Stand behauptet.

Workflowtest bestätigt weiterhin exakt `build:fixture:subpath` in `device-fixture-pages.yml` und verbietet `build`, `build:ium5`, `IUM-5-CORE-05` sowie `algorithm-workbench` in diesem Workflow.

- [ ] **Step 2: Tests ausführen und das erwartete Scheitern bestätigen**

```powershell
npm exec -- playwright test tests/browser/ium5-offline.spec.ts --config playwright.ium5.config.mts --project=chromium
npm exec -- vitest run tests/platform/documentation.test.ts tests/platform/pages-workflow.test.ts tests/platform/license-policy.test.ts tests/platform/build-quality.test.ts
```

Expected: neue Offline-, Dokumentations- und Skripterwartungen FAIL.

- [ ] **Step 3: Rootbefehle und fail-fast IUM5-Verifikation implementieren**

Rootscripts:

```json
"test:ium5:browser": "playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts",
"test:ium5:state": "playwright test tests/browser/ium5-state.spec.ts --config playwright.ium5.config.mts --project=chromium",
"test:ium5:accessibility": "playwright test tests/browser/ium5-accessibility.spec.ts --config playwright.ium5.config.mts --project=chromium",
"test:ium5:offline": "playwright test tests/browser/ium5-offline.spec.ts --config playwright.ium5.config.mts --project=chromium",
"verify:ium5": "tsx scripts/verify-ium5.ts"
```

`verify-ium5.ts` verwendet wie Phase 1 `spawnSync`, `shell: false`, `stdio: 'inherit'` und stoppt beim ersten Fehler. Reihenfolge:

1. `contracts:check`
2. `boundaries:check`
3. `typecheck`
4. `check:astro`
5. `test:platform`
6. `build`
7. `build:fixture`
8. `build:fixture:subpath`
9. `quality:build`
10. `quality:licenses`
11. `test:browser`
12. `test:offline`
13. `test:accessibility`
14. `test:ium5:browser`
15. `test:ium5:state`
16. `test:ium5:offline`
17. `test:ium5:accessibility`
18. `test:python`
19. `python -B scripts/build_ium11_cockpit.py --check`
20. `python -B scripts/build_ium11_publication_contract.py --check`
21. `python -B scripts/validate_ium11.py`
22. `python -B scripts/validate_ium10.py`
23. `python -B scripts/validate_ium09.py`
24. `python -B scripts/validate_phase0.py`

- [ ] **Step 4: Dokumentation und CI ehrlich erweitern**

`docs/modules/ium-5-core-05.md` dokumentiert lokale Starts, regulären und erweiterten Pfad, Arbeitsstand, Datenfelder, flüchtige Nichtdaten, Import-/Export-/Löschpfad, Offlinegrenze, Accessibilitybedienung, Lizenzen, Verifikationskommando und geschlossene Gate-B-Grenze. README verlinkt Spezifikation, Plan, Modulbetrieb und Handbuch, nennt aber keine Veröffentlichung. `docs/platform/README.md` bezeichnet `production-empty` ausdrücklich als Phase-1-Ausgangsstand und beschreibt den aktuellen Unterschied: Das `working`-Modul ist im lokalen Produktionsbuild sichtbar, aber weder freigegeben noch durch den Fixture-only-Pagesworkflow deployt. Der historische `docs/platform/implementation-report.md` bleibt unverändert.

CI behält genau `legacy`, `contracts-build`, `browser`, `offline-quality`. `contracts-build` führt zusätzlich `npm run check:astro`, `npm run build` und die erweiterten Plattformtests aus. `browser` ergänzt `npm run test:ium5:browser` und `npm run test:ium5:state`. `offline-quality` ergänzt die beiden IUM5-Offline-/Accessibilitybefehle. Es entsteht kein Deployment, Secret oder Lernendendatenartefakt.

- [ ] **Step 5: Offline-, Lizenz-, Dokumentations- und CI-Prüfungen grün ausführen**

```powershell
npm exec -- playwright test tests/browser/ium5-offline.spec.ts --config playwright.ium5.config.mts --project=chromium
npm exec -- vitest run tests/platform/documentation.test.ts tests/platform/pages-workflow.test.ts tests/platform/license-policy.test.ts tests/platform/build-quality.test.ts
npm run quality:licenses
npm run quality:build
npm run typecheck
npm run check:astro
```

Expected: alle Prüfungen PASS; Pages-Vertrag bleibt unverändert Fixture-only.

- [ ] **Step 6: Task 11 committen**

```powershell
git add package.json README.md .github/workflows/ci.yml scripts/verify-ium5.ts docs/modules/ium-5-core-05.md docs/platform/README.md tests/browser/ium5-offline.spec.ts tests/platform/documentation.test.ts tests/platform/pages-workflow.test.ts tests/platform/license-policy.test.ts tests/platform/build-quality.test.ts
git commit -m "test: gate the IUM5 working module"
```

---

### Task 12: Vollverifikation, getrennte interne Reviews und Gate-A-Handoff

**Files:**
- Create: `docs/reviews/ium-5-core-05-fach-didaktik.md`
- Create: `docs/reviews/ium-5-core-05-engineering-accessibility-privacy.md`
- Modify: `docs/modules/ium-5-core-05.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: vollständige Implementierung und alle automatisierten Gates.
- Produces: zwei tatsächliche, getrennte Reviewbefunde und einen ehrlichen Gate-A-Handoff.
- Invariant: automatisierter oder interner Abschluss hebt weder `working` noch `device-verified: not-run` an und öffnet Gate B nicht.

- [ ] **Step 1: Sauberen Arbeitsbaum und vollständige lokale Ausgangslage prüfen**

```powershell
git status --short --branch
git diff --check
npm run verify:ium5
```

Expected: Arbeitsbaum enthält nur die beiden noch anzulegenden Reviewdokumente beziehungsweise deren Handoffänderungen; `git diff --check` ohne Ausgabe; alle Verifikationsschritte PASS. Bei einem Fehler wird gestoppt und derselbe Task mit TDD korrigiert, bevor ein Reviewurteil entsteht.

- [ ] **Step 2: Fachlich-didaktischen Review gegen reale Artefakte durchführen**

Prüfe und dokumentiere mit konkreten Datei-/Testbelegen:

- fünf Kompetenzrecords und Grenze zu Klasse 7;
- 225-/270-Minutenvertrag und echte zusätzliche Ausführung in UE6;
- alle fünf Aufgabenfamilien;
- Präzision, Vorhersage, Ausführung, Laufspur, erste Abweichung, Hypothese, Revision und Schleifenentscheidung;
- standardisierten Reparaturfall bei sofort korrektem Erstentwurf;
- Algorithmus-Lupe mit Positiv-, Nicht- und Grenzfällen;
- explizite Erklärung und gemeinsame Sicherung;
- 1:1-/1:2-Orchestrierung, Voraussetzungen und frischer Evidenzfall;
- keine Gamification, automatische Bewertung, Diagnose oder analoge Doppelstruktur.

`docs/reviews/ium-5-core-05-fach-didaktik.md` enthält tatsächlichen geprüften Commit, gelesene Artefakte, Einzelbefunde mit Evidenzpfad, offene Risiken und genau eines der Urteile `APPROVED`, `APPROVED AFTER FIXES` oder `CHANGES REQUIRED`. Bei `CHANGES REQUIRED` endet der Task ohne Abschlusscommit; Befunde werden zuerst testgetrieben behoben und erneut vollständig geprüft.

- [ ] **Step 3: Engineering-, Accessibility-, Privacy- und Lizenzreview durchführen**

Prüfe und dokumentiere getrennt:

- statische Rendererbindung und Fixture-Isolation;
- Interpreterdeterminismus und alle Fehler;
- geschlossene Payloadfelder und flüchtige Nichtdaten;
- fail-closed Import, Migration/Future-Schema, Export, Löschen und Speicherfallback;
- Tastatur, Touch, Screenreaderstruktur, Textäquivalent, 320px, 200 Prozent und reduzierte Bewegung;
- Root-/Subpath-, Offline- und kontrollierten Updatepfad;
- Null Drittanbieter, Null dynamische Codeausführung, Budgets und Assetlizenzen;
- Fixture-only-Pagesworkflow, `working`-Kennzeichnung und geschlossenes Gate B.

`docs/reviews/ium-5-core-05-engineering-accessibility-privacy.md` verwendet denselben realen Commit- und Urteilsvertrag. Kein Review darf `device-verified` als bestanden bezeichnen.

- [ ] **Step 4: Reviewbefunde maschinenlesbar im Betriebsdokument referenzieren**

Ergänze in `docs/modules/ium-5-core-05.md` die beiden Reviewpfade, tatsächliche Urteile und den letzten grünen `verify:ium5`-Lauf. README nennt weiterhin ausschließlich „interner Arbeitsstand“. Wenn ein Review Nacharbeit erforderte, dokumentiere die Fixcommits und den erneuten vollständigen Lauf.

- [ ] **Step 5: Finales lokales Gate erneut ausführen**

```powershell
npm run verify:ium5
git diff --check
git status --short --branch
```

Expected: vollständige Verifikation PASS, Diffcheck leer; ausschließlich Review- und Handoffdokumentation uncommitted.

- [ ] **Step 6: Task 12 committen**

```powershell
git add docs/reviews/ium-5-core-05-fach-didaktik.md docs/reviews/ium-5-core-05-engineering-accessibility-privacy.md docs/modules/ium-5-core-05.md README.md
git commit -m "docs: hand off IUM5 for gate A review"
```

- [ ] **Step 7: Branch nach Repositoryregeln veröffentlichen und CI beobachten**

```powershell
git fetch --prune
git pull --ff-only origin main
git push -u origin HEAD
```

Expected: regulärer Push ohne Force. Der passende GitHub-Actions-Lauf beendet alle vier Jobs grün. Commit, Branch, Remote, Run-ID und offene Gate-B-/Realgeräteanforderungen werden im Workspace-Handoff dokumentiert.

---

## Spec Coverage Self-Review Map

| Spezifikationsabschnitt | Umsetzungstask |
|---|---|
| 1 Entscheidung und Ziel | 2, 5, 9 |
| 2 Status- und Gategrenze | 5, 11, 12 |
| 3 Grundlagen und Hierarchie | 2, 12 |
| 4 Curricularer Vertrag | 2, 11, 12 |
| 5 Leitfrage, Lernziele, Kriterien | 2, 5, 9 |
| 6 Zentrales Lernprodukt | 4, 7, 8, 9 |
| 7 Designansätze | 5, 6, 9 |
| 8 Kontext und Modellgrenze | 2, 9, 12 |
| 9 Befehlssprache und Zustand | 1, 3 |
| 10 Fehlersemantik | 3, 7 |
| 11 Interaktionszyklus | 6, 7, 8 |
| 12 Oberflächenarchitektur | 5, 10 |
| 13 Aufgabenfamilien | 2, 9 |
| 14 Reguläre Sequenz | 2, 9 |
| 15 Erweiterungspfad | 2, 9 |
| 16 Unterstützung und Differenzierung | 2, 9 |
| 17 Rückmeldung | 7 |
| 18 Lehrkraft und Sozialform | 2, 12 |
| 19 Voraussetzung und Fallback | 2, 8, 11 |
| 20 Lokaler Daten- und Exportvertrag | 4, 8 |
| 21 Lernnachweis ohne Diagnostik | 4, 9 |
| 22 Barrierefreiheit und responsive Nutzung | 5, 10 |
| 23 Digital-analog-Entscheidung | 2, 12 |
| 24 Technische Architekturgrenze | 1, 2, 5, 11 |
| 25 Lehrkräftehandbuch | 2, 12 |
| 26 OER-, Asset- und Quellenvertrag | 2, 11 |
| 27 Qualitätssicherung | 3, 4, 8, 10, 11, 12 |
| 28 Definition of Done Gate A | 11, 12 |
| 29 Nicht-Ziele | Global Constraints, 12 |
| 30 Implementierungsreihenfolge | Tasks 1–12 |
| 31 Risiken und Gegenmaßnahmen | 2, 6, 7, 9, 10, 11, 12 |
| 32 Akzeptanzkriterien | 11, 12 |
| 33 Schriftliches Freigabegate | vorliegender Plan und späterer Ausführungsauftrag |

## Plan Self-Review Checklist

- [x] Jede der elf persistenten Payloadeigenschaften ist in Task 4 definiert und in Task 8 getestet.
- [x] Alle sechs Interpreterfehler sind in Task 3 und ihre sichtbare Behandlung in Task 7 getestet.
- [x] Reguläre und erweiterte Minutensummen werden aus Quelldaten berechnet, nicht nur als Text gesucht.
- [x] `algorithm-workbench` ist statisch an genau `IUM-5-CORE-05` gebunden.
- [x] Fixture- und Produktionsbundles sind in beide Richtungen isoliert.
- [x] Der Pages-Workflow bleibt Fixture-only und enthält keinen Produktbuild.
- [x] Keine Aufgabe erhebt Zeit, Klicks, Versuche, Hilfenutzung oder personenbezogene Daten.
- [x] Alle später verwendeten Typen und Funktionen werden in einem früheren Task produziert.
- [x] Jeder Task endet mit eigenständig prüfbarem Ergebnis und Commit.
- [x] Kein Schritt enthält eine offene Implementierungsentscheidung oder einen inhaltlichen Platzhalter.
- [x] Interne Reviews und grüne CI öffnen Gate B nicht.
