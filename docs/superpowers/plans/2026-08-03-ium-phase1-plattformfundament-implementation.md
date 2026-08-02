# IuM-Lernwerk Phase 1 Plattformfundament Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the contract-first, local-first, offline-capable Phase 1 platform foundation with a production-empty Astro portal and a strictly isolated synthetic reference fixture.

**Architecture:** A private npm-workspace monorepo keeps canonical JSON Schemas and framework-free TypeScript packages below a static Astro portal. Production and fixture registries have hard-separated source roots; the runtime reaches IndexedDB, files, the clock, and update state only through explicit ports. A custom `injectManifest` service worker provides controlled offline installation and prompt-based updates without starting Phase 2 or publishing a curricular module.

**Tech Stack:** Node 22.20.0, npm 10.9.3, Astro 7.1.6, TypeScript 6.0.3, JSON Schema 2020-12, Ajv 8.20.0, `idb` 8.0.3, `vite-plugin-pwa` 1.3.0, Workbox 7.4.1, Vitest 4.1.10, Playwright 1.62.1, axe-core 4.12.1, GitHub Actions.

## Global Constraints

- The approved specification is `docs/superpowers/specs/2026-08-03-ium-phase1-plattformfundament-design.md`, version 1.1, and governs every task.
- Begin execution in an isolated worktree created with `superpowers:using-git-worktrees`; do not implement on `main`.
- Preserve all 638 pre-existing Python tests and the Phase-0, IUM09, IUM10, and IUM11 validators.
- Do not change curriculum, coverage, time, pilot, availability, or product-status values.
- Do not create a curricular module, a teacher handbook, real pilot data, telemetry, accounts, central storage, or a hosting-provider commitment.
- `IUM-5-CORE-05` remains wholly outside Phase 1.
- Production reads only `modules/`; fixture builds read only `tests/fixtures/reference-module/` and synthetic curriculum fixtures.
- A `TEST-` ID in a production registry is a hard failure; fixture outputs never contribute coverage or maturity.
- Use npm Workspaces and exactly one committed `package-lock.json`; CI installs with `npm ci`.
- Pin Node to `22.20.0`, npm to `10.9.3`, TypeScript to `6.0.3`, and all dependencies to exact versions without `^` or `~`.
- Use `vite-plugin-pwa` directly in `astro.config.ts`; do not install `@vite-pwa/astro` because its current peer range excludes Astro 7.
- Use semantic HTML, CSS, Astro components, and small TypeScript controllers; do not add React, Preact, Vue, Svelte, Solid, Lit, or a global client-state framework.
- Own code is MIT; own visible learning/content text is CC BY-SA 4.0; fixture prose is synthetic and must not resemble finished instruction.
- No third-party scripts, fonts, trackers, CDN resources, or runtime requests in the core path.
- Maximum fixture import size is exactly 5 MiB.
- Portal plus fixture budgets are: 250 KiB gzip cold transfer, 100 KiB gzip initial JavaScript, 2 MiB decoded precache, and zero third-party requests.
- A first-ever uncached offline visit cannot be controlled and must not be claimed as an application-rendered error state.
- No automatic `skipWaiting()` or reload; updates activate only after a visible prompt, successful state flush, and explicit confirmation.
- Automated completion may reach `implemented`; `device-verified` remains open until a real managed school iPad and named desktop/screenreader matrix are documented.
- All source text is UTF-8 without BOM and LF. Generated directories, `node_modules`, Playwright browsers, reports, and build output remain uncommitted.
- Use TDD for every behavior: failing test, observed failure, minimal implementation, observed pass, relevant regression suite, commit.

---

## File Map

### Root configuration

- `.nvmrc`: exact Node version.
- `.npmrc`: reproducible npm behavior and engine enforcement.
- `package.json`: workspace graph, exact tool versions, and all root commands.
- `package-lock.json`: sole dependency lock.
- `tsconfig.base.json`: strict shared TypeScript rules.
- `vitest.config.ts`: contract and unit test projects.
- `playwright.config.ts`: fixture preview and Chromium/Firefox/WebKit projects.
- `tests/platform/helpers/build-portal.ts`: isolated production/fixture build harness with base-path readers.
- `.gitignore`: Node, generated registry, build, report, and browser artifacts.

### Canonical contracts

- `schemas/module-manifest.schema.json`: closed JSON Schema for production and synthetic module manifests.
- `schemas/learning-state-envelope.schema.json`: closed versioned local/export state envelope.
- `packages/module-contract/src/generated/module-manifest.d.ts`: generated, ignored TypeScript type.
- `packages/module-contract/src/generated/learning-state-envelope.d.ts`: generated, ignored TypeScript type.
- `packages/module-contract/src/errors.ts`: closed error codes and public error shape.
- `packages/module-contract/src/ports.ts`: storage, clock, download, copy, and update ports.
- `packages/module-contract/src/validators.ts`: Ajv validators and semantic manifest checks.
- `packages/module-contract/src/index.ts`: package exports.
- `scripts/generate-contract-types.ts`: deterministic JSON-Schema-to-TypeScript generation and `--check` drift mode.

### Registry and fixture isolation

- `scripts/build-module-registry.ts`: profile-bound YAML loading, structural and semantic validation, deterministic registry/build info.
- `scripts/check-workspace-boundaries.ts`: closed workspace dependency/import direction check.
- `apps/lernwerk-portal/src/generated/module-registry.json`: generated and ignored.
- `apps/lernwerk-portal/src/generated/build-info.json`: generated and ignored.
- `tests/fixtures/curriculum/competencies.json`: synthetic competency IDs only.
- `tests/fixtures/reference-module/module.yaml`: structurally complete `TEST-` manifest.
- `tests/fixtures/reference-module/lernumgebung/index.md`: noncurricular fixture entry marker.
- `tests/fixtures/reference-module/assets/licenses.json`: synthetic license evidence.

### Runtime packages

- `packages/local-state/src/memory-repository.ts`: selected and fallback volatile storage.
- `packages/local-state/src/indexeddb-repository.ts`: confirmed IndexedDB transactions and database migration.
- `packages/local-state/src/index.ts`: repository factory and exports.
- `packages/export-import/src/export-state.ts`: UTF-8 JSON, filename, download and copy fallback.
- `packages/export-import/src/import-state.ts`: 5 MiB guard, parsing, closed validation and preview.
- `packages/export-import/src/index.ts`: exports.
- `packages/module-runtime/src/migrations.ts`: sequential copied-state migration.
- `packages/module-runtime/src/runtime.ts`: one-active-state use cases and port coordination.
- `packages/module-runtime/src/index.ts`: exports.

### Portal and UI

- `packages/ui-components/src/components/*.astro`: accessible storage, connection, error, update and data controls.
- `packages/ui-components/src/controllers/*.ts`: framework-free progressive-enhancement controllers.
- `packages/ui-components/src/styles/components.css`: shared component presentation.
- `apps/lernwerk-portal/astro.config.ts`: static root/subpath config and direct Vite PWA integration.
- `apps/lernwerk-portal/src/layouts/BaseLayout.astro`: semantic shell and shared status regions.
- `apps/lernwerk-portal/src/pages/index.astro`: production-empty catalog and fixture catalog.
- `apps/lernwerk-portal/src/pages/daten.astro`: local data management.
- `apps/lernwerk-portal/src/pages/offline.astro`: cached offline explanation.
- `apps/lernwerk-portal/src/pages/module/[id].astro`: registry-derived static routes.
- `apps/lernwerk-portal/src/components/FixtureWorkspace.astro`: synthetic vertical-slice interaction only.
- `apps/lernwerk-portal/src/controllers/fixture-workspace.ts`: runtime wiring.
- `apps/lernwerk-portal/src/styles/global.css`: system-font responsive base.
- `apps/lernwerk-portal/src/sw.ts`: custom prompt-update service worker.
- `apps/lernwerk-portal/public/app-icon.svg`: source icon without branding claim.
- `apps/lernwerk-portal/public/icons/*.png`: mechanically generated PWA icons.

### Quality and delivery

- `tests/platform/*.test.ts`: schema, registry, state, import/export, migration, boundary and budget units.
- `tests/browser/platform.spec.ts`: persistence, reload, import/export/delete, keyboard and embedding paths.
- `tests/browser/offline.spec.ts`: offline, waiting update, failed install and scope paths.
- `tests/browser/accessibility.spec.ts`: axe, focus, reflow and reduced-motion paths.
- `scripts/check-build-output.ts`: budgets, base paths, cache inventory and third-party URL scan.
- `scripts/check-dependency-licenses.ts`: dependency license allowlist and SBOM check.
- `scripts/verify-phase1.ts`: sole cross-platform, fail-fast orchestration of all Phase-1 gates.
- `.github/workflows/ci.yml`: Python regression, Node contract/build, browser and artifact gates.
- `docs/platform/README.md`: local development, data, PWA, embedding and status boundaries.
- `docs/platform/device-verification.md`: unfilled real-device protocol with explicit open gate.
- `README.md`: current Phase-1 entry points and commands.

---

### Task 1: Workspace and canonical contracts

**Files:**
- Create: `.nvmrc`
- Create: `.npmrc`
- Create: `package.json`
- Create: `package-lock.json`
- Create: `tsconfig.base.json`
- Create: `vitest.config.ts`
- Modify: `.gitignore`
- Create: `schemas/module-manifest.schema.json`
- Create: `schemas/learning-state-envelope.schema.json`
- Create: `packages/module-contract/package.json`
- Create: `packages/module-contract/tsconfig.json`
- Create: `packages/module-contract/src/errors.ts`
- Create: `packages/module-contract/src/ports.ts`
- Create: `packages/module-contract/src/validators.ts`
- Create: `packages/module-contract/src/index.ts`
- Create: `scripts/generate-contract-types.ts`
- Test: `tests/platform/contracts.test.ts`

**Interfaces:**
- Produces: `validateModuleManifest(value): ValidationResult<ModuleManifest>`
- Produces: `validateLearningState(value): ValidationResult<LearningStateEnvelope>`
- Produces: `PlatformErrorCode`, `PlatformError`, `StateRepository`, `ClockPort`, `ExportPort`, `UpdatePort`
- Produces: root commands `contracts:generate`, `contracts:check`, `typecheck`, `test:platform`

- [ ] **Step 1: Add workspace/tool configuration without production behavior**

Create root `package.json` with private workspaces and exact dependencies:

```json
{
  "name": "ium-lernwerk",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "workspaces": ["apps/*", "packages/*"],
  "engines": { "node": ">=22.12.0 <23", "npm": ">=10.9.0 <11" },
  "scripts": {
    "contracts:generate": "tsx scripts/generate-contract-types.ts",
    "contracts:check": "tsx scripts/generate-contract-types.ts --check",
    "typecheck": "npm run contracts:generate && tsc -b --pretty false",
    "test:platform": "npm run contracts:generate && vitest run",
    "test:python": "python -B -m unittest discover -s tests -p \"test_*.py\""
  },
  "devDependencies": {
    "@astrojs/check": "0.9.10",
    "@axe-core/playwright": "4.12.1",
    "@playwright/test": "1.62.1",
    "@vite-pwa/assets-generator": "1.0.2",
    "astro": "7.1.6",
    "fake-indexeddb": "6.2.5",
    "json-schema-to-typescript": "15.0.4",
    "tsx": "4.23.4",
    "typescript": "6.0.3",
    "vite-plugin-pwa": "1.3.0",
    "vitest": "4.1.10",
    "workbox-core": "7.4.1",
    "workbox-precaching": "7.4.1",
    "workbox-routing": "7.4.1",
    "yaml": "2.9.0"
  }
}
```

Create `.nvmrc` as `22.20.0`, `.npmrc` with `engine-strict=true` and `save-exact=true`, and a strict `tsconfig.base.json` using `ES2022`, `Bundler`, `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `resolveJsonModule`, and `verbatimModuleSyntax`.

Every workspace package is `private`, versioned exactly `0.1.0`, and exports source entry points for the monorepo build. Internal workspace dependencies use the exact version `0.1.0`. `@ium/module-contract` depends on `ajv` `8.20.0` and `ajv-formats` `3.0.1`; `@ium/local-state` depends on `idb` `8.0.3`. No workspace may use `workspace:*`, ranges, or implicit transitive dependencies.

- [ ] **Step 2: Install exact dependencies and record the lock**

Run:

```powershell
npm install
```

Expected: `package-lock.json` is created, Node 22.20.0 satisfies engines, and `npm ls --depth=0` has no invalid peer dependency. Do not use `--force` or `--legacy-peer-deps`.

- [ ] **Step 3: Write failing closed-contract tests**

Create tests that import the currently absent validator exports:

```ts
import { describe, expect, test } from 'vitest';
import {
  validateLearningState,
  validateModuleManifest,
} from '../../packages/module-contract/src/index.js';

describe('closed Phase-1 contracts', () => {
  test('rejects unknown manifest fields', () => {
    const result = validateModuleManifest({
      schemaVersion: 1,
      id: 'TEST-PLATFORM-REFERENCE',
      version: '1.0.0',
      title: 'Technische Referenz',
      status: 'draft',
      grade: 5,
      kind: 'core',
      strands: ['TEST-STRAND'],
      time: { minLessons: 1, maxLessons: 1, contractId: 'TEST-TIME-001' },
      prerequisites: [],
      curriculum: { competencyIds: ['TEST-COMP-001'], coverageEvidenceIds: ['TEST-COV-001'] },
      learningDesign: {
        centralQuestion: 'Technische Frage',
        goals: ['Technischen Zustand prüfen'],
        actions: ['Synthetische Eingabe ändern'],
        product: 'Synthetischer Zustand',
        misconceptions: [],
        scaffolds: []
      },
      components: ['fixture-workspace'],
      media: { digitalFunction: 'Technischen Zustandsfluss prüfen', analogMaterials: [] },
      data: { stateSchemaVersion: 1, fields: ['text', 'choice'], exportable: true, deletable: true },
      offline: { core: true, externalResources: [] },
      accessibility: { alternatives: [], manualChecks: ['keyboard', 'screenreader'] },
      licenses: { content: 'CC-BY-SA-4.0', code: 'MIT', assetEvidencePath: 'assets/licenses.json' },
      quality: { evidenceRefs: [] },
      unexpected: true
    });
    expect(result.ok).toBe(false);
  });

  test('rejects a state with identity fields', () => {
    const result = validateLearningState({
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'TEST-PLATFORM-REFERENCE',
      moduleVersion: '1.0.0',
      stateSchemaVersion: 1,
      workspaceId: '123e4567-e89b-42d3-a456-426614174000',
      savedAt: '2026-08-03T12:00:00.000Z',
      payload: {},
      learnerName: 'Nicht erlaubt'
    });
    expect(result.ok).toBe(false);
  });
});
```

- [ ] **Step 4: Run the tests and observe the expected failure**

Run:

```powershell
npm run test:platform -- --run tests/platform/contracts.test.ts
```

Expected: FAIL because `packages/module-contract/src/index.ts` or its exports do not exist.

- [ ] **Step 5: Implement the two canonical schemas and validator API**

Use JSON Schema 2020-12, `additionalProperties: false` at every contract object boundary, the four existing status values, production IDs `^IUM-[567]-(CORE|EXT|TRANSFER|PROJECT)-[0-9]{2}$`, reserved fixture IDs `^TEST-[A-Z0-9-]+$`, and a free JSON-object `payload` only inside the state envelope. Export this exact result contract:

```ts
export type ValidationIssue = Readonly<{
  path: string;
  keyword: string;
  message: string;
}>;

export type ValidationResult<T> =
  | Readonly<{ ok: true; value: T }>
  | Readonly<{ ok: false; issues: readonly ValidationIssue[] }>;
```

Create the closed error union:

```ts
export type PlatformErrorCode =
  | 'STORAGE_UNAVAILABLE'
  | 'STORAGE_QUOTA'
  | 'STORAGE_WRITE_FAILED'
  | 'IMPORT_TOO_LARGE'
  | 'IMPORT_INVALID'
  | 'IMPORT_WRONG_MODULE'
  | 'IMPORT_UNSUPPORTED_VERSION'
  | 'MIGRATION_FAILED'
  | 'OFFLINE_NOT_READY'
  | 'UPDATE_INSTALL_FAILED';
```

Generate TypeScript types with `json-schema-to-typescript`, stable banner text, alphabetical property order disabled, and a `--check` mode that compares bytes without writing.

- [ ] **Step 6: Run contract, type and legacy regression gates**

Run:

```powershell
npm run contracts:generate
npm run contracts:check
npm run typecheck
npm run test:platform -- --run tests/platform/contracts.test.ts
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: contract tests PASS, generated check PASS, TypeScript PASS, and 638 Python tests PASS.

- [ ] **Step 7: Commit Task 1**

```powershell
git add .nvmrc .npmrc .gitignore package.json package-lock.json tsconfig.base.json vitest.config.ts schemas packages/module-contract scripts/generate-contract-types.ts tests/platform/contracts.test.ts
git commit -m "feat: establish phase1 platform contracts"
```

---

### Task 2: Deterministic registry and fixture isolation

**Files:**
- Create: `scripts/build-module-registry.ts`
- Create: `scripts/check-workspace-boundaries.ts`
- Create: `tests/fixtures/curriculum/competencies.json`
- Create: `tests/fixtures/reference-module/module.yaml`
- Create: `tests/fixtures/reference-module/lernumgebung/index.md`
- Create: `tests/fixtures/reference-module/assets/licenses.json`
- Create: `tests/platform/registry.test.ts`
- Modify: `package.json`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `validateModuleManifest`
- Produces: `buildRegistry({ profile, rootDir, outputDir }): Promise<ModuleRegistry>`
- Produces: `renderRegistry(registry): Uint8Array`
- Produces: `computeReleaseId(paths): Promise<string>`
- Produces: CLI profiles exactly `production` and `fixture`
- Produces: commands `registry:production`, `registry:fixture`, `boundaries:check`

- [ ] **Step 1: Write failing profile-isolation and determinism tests**

```ts
test('production ignores every fixture source', async () => {
  const registry = await buildRegistry({
    profile: 'production',
    rootDir: repoRoot,
    outputDir: temporaryOutput
  });
  expect(registry.modules).toEqual([]);
});

test('fixture profile yields exactly the reserved synthetic entry', async () => {
  const registry = await buildRegistry({
    profile: 'fixture',
    rootDir: repoRoot,
    outputDir: temporaryOutput
  });
  expect(registry.modules.map((entry) => entry.id)).toEqual([
    'TEST-PLATFORM-REFERENCE'
  ]);
  expect(registry.modules[0]?.countsTowardCoverage).toBe(false);
  expect(registry.modules[0]?.publishedStatus).toBeNull();
});

test('equal inputs produce byte-identical registry bytes', async () => {
  const first = renderRegistry(await buildRegistry(fixtureOptions));
  const second = renderRegistry(await buildRegistry(fixtureOptions));
  expect(second).toEqual(first);
});
```

Define `fixtureOptions` once in the test as the fixed `fixture` profile with the repository root and a test-owned temporary output directory.

- [ ] **Step 2: Run the tests and observe the missing builder failure**

Run:

```powershell
npm run test:platform -- --run tests/platform/registry.test.ts
```

Expected: FAIL because `build-module-registry.ts` does not exist.

- [ ] **Step 3: Add the complete synthetic fixture**

The fixture manifest must fill every required manifest field, use only `TEST-` references, point to the checked-in entry and license evidence, set the synthetic input status to `draft`, and include `countsTowardCoverage: false` only in the generated registry—not as an author-controlled manifest override.

Synthetic curriculum data contains exactly:

```json
{
  "schemaVersion": 1,
  "sourceId": "TEST-CURRICULUM",
  "records": [
    {
      "id": "TEST-COMP-001",
      "text": "Technische Referenzkompetenz ohne Unterrichtsgeltung",
      "recordType": "test-fixture"
    }
  ]
}
```

- [ ] **Step 4: Implement fixed-root profile loading and semantic checks**

The builder must select roots with a closed switch:

```ts
const profileRoots = {
  production: {
    modules: 'modules',
    curriculum: [
      'curriculum/lesehilfe-2026-27/competencies.json',
      'curriculum/basiskurs-medienbildung/competencies.json',
      'curriculum/aufbaukurs-informatik/competencies.json'
    ]
  },
  fixture: {
    modules: 'tests/fixtures/reference-module',
    curriculum: ['tests/fixtures/curriculum/competencies.json']
  }
} as const;
```

Reject unknown profiles, path escapes, duplicate IDs, missing files, unresolved competencies, real IDs in fixture mode, `TEST-` IDs in production mode, and any author-provided coverage-count or published-status override. Sort module IDs and JSON keys before writing. Compute release IDs as `ium-<first 16 hex characters>` from SHA-256 over profile, normalized relative paths, and source bytes; exclude generated/build/ignored paths.

- [ ] **Step 5: Add package/import boundary checking**

Encode the allowed workspace dependency graph from the specification. Scan each workspace `package.json` and TypeScript import specifier. Fail on a cycle, a dependency outside the allowlist, a direct `idb` import outside `local-state`, or direct Astro/DOM imports inside `module-contract`, `local-state`, `export-import`, and `module-runtime`.

- [ ] **Step 6: Verify production, fixture and boundary gates**

```powershell
npm run registry:production
npm run registry:fixture
npm run boundaries:check
npm run test:platform -- --run tests/platform/registry.test.ts
npm run typecheck
```

Expected: production registry has zero modules; fixture registry has exactly `TEST-PLATFORM-REFERENCE`; all tests PASS.

- [ ] **Step 7: Commit Task 2**

```powershell
git add package.json .gitignore scripts/build-module-registry.ts scripts/check-workspace-boundaries.ts tests/fixtures tests/platform/registry.test.ts
git commit -m "feat: isolate deterministic module fixtures"
```

---

### Task 3: Local-state repositories and storage modes

**Files:**
- Create: `packages/local-state/package.json`
- Create: `packages/local-state/tsconfig.json`
- Create: `packages/local-state/src/memory-repository.ts`
- Create: `packages/local-state/src/indexeddb-repository.ts`
- Create: `packages/local-state/src/index.ts`
- Create: `tests/platform/local-state.test.ts`

**Interfaces:**
- Consumes: `LearningStateEnvelope`, `StateRepository`, `PlatformError`
- Produces: `MemoryStateRepository`
- Produces: `IndexedDbStateRepository`
- Produces: `createStateRepository(options): Promise<StateRepositorySelection>`

- [ ] **Step 1: Write failing one-active-state and confirmed-transaction tests**

```ts
test('stores exactly one active state per module', async () => {
  const repository = new MemoryStateRepository();
  await repository.save(state({ workspaceId: firstId, payload: { text: 'eins' } }));
  await repository.save(state({ workspaceId: secondId, payload: { text: 'zwei' } }));
  expect(await repository.load('TEST-PLATFORM-REFERENCE')).toMatchObject({
    workspaceId: secondId,
    payload: { text: 'zwei' }
  });
});

test('reports saved only after the IndexedDB transaction completes', async () => {
  const repository = await createIndexedDbTestRepository();
  const result = await repository.save(state());
  expect(result).toEqual({ ok: true, mode: 'persistent' });
  expect(await repository.load('TEST-PLATFORM-REFERENCE')).toEqual(state());
});

test('falls back visibly when IndexedDB opening fails', async () => {
  const selection = await createStateRepository({
    indexedDbFactory: rejectingIndexedDbFactory,
    preferredMode: 'persistent'
  });
  expect(selection.mode).toBe('volatile-fallback');
  expect(selection.warning?.code).toBe('STORAGE_UNAVAILABLE');
});
```

- [ ] **Step 2: Run and observe missing repository failures**

```powershell
npm run test:platform -- --run tests/platform/local-state.test.ts
```

Expected: FAIL because repositories do not exist.

- [ ] **Step 3: Implement memory and IndexedDB repositories**

Use database `ium-lernwerk`, schema version 1, object store `activeStates`, key path `moduleId`, and no indexes containing user-entered content. Await both the individual request and `transaction.done` before success. On `QuotaExceededError`, return `STORAGE_QUOTA`; on open failure return `STORAGE_UNAVAILABLE`; on other write failure return `STORAGE_WRITE_FAILED`.

Repository methods are exactly:

```ts
export interface StateRepository {
  readonly mode: 'persistent' | 'volatile-selected' | 'volatile-fallback';
  load(moduleId: string): Promise<LearningStateEnvelope | null>;
  save(state: LearningStateEnvelope): Promise<SaveResult>;
  deleteModule(moduleId: string): Promise<DeleteResult>;
  deleteAll(): Promise<DeleteResult>;
}
```

- [ ] **Step 4: Add database upgrade and deletion-negative tests**

Test opening version 0 to 1, blocked deletion, missing state deletion, module isolation, and a failed write that leaves the previous committed state unchanged.

- [ ] **Step 5: Run repository, contract and type gates**

```powershell
npm run test:platform -- --run tests/platform/local-state.test.ts tests/platform/contracts.test.ts
npm run typecheck
```

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```powershell
git add packages/local-state tests/platform/local-state.test.ts package.json package-lock.json
git commit -m "feat: add confirmed local state repositories"
```

---

### Task 4: Import, export and module runtime

**Files:**
- Create: `packages/export-import/package.json`
- Create: `packages/export-import/tsconfig.json`
- Create: `packages/export-import/src/export-state.ts`
- Create: `packages/export-import/src/import-state.ts`
- Create: `packages/export-import/src/index.ts`
- Create: `packages/module-runtime/package.json`
- Create: `packages/module-runtime/tsconfig.json`
- Create: `packages/module-runtime/src/migrations.ts`
- Create: `packages/module-runtime/src/runtime.ts`
- Create: `packages/module-runtime/src/index.ts`
- Create: `tests/platform/export-import.test.ts`
- Create: `tests/platform/runtime.test.ts`

**Interfaces:**
- Produces: `serializeState(state): Uint8Array`
- Produces: `stateExportFilename(state): string`
- Produces: `parseImport(bytes, expectedModuleId): ImportParseResult`
- Produces: `migrateStateCopy(state, targetVersion, migrations): MigrationResult`
- Produces: `createModuleRuntime(dependencies): ModuleRuntime`

- [ ] **Step 1: Write failing fail-closed import and migration tests**

```ts
test('rejects input over exactly 5 MiB without parsing', () => {
  const bytes = new Uint8Array(5 * 1024 * 1024 + 1);
  expect(parseImport(bytes, 'TEST-PLATFORM-REFERENCE')).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_TOO_LARGE' })
  });
});

test('wrong-module import leaves repository unchanged', async () => {
  const repository = seededRepository(existingState);
  const runtime = createRuntime(repository);
  const result = await runtime.importState(serializeState(otherModuleState));
  expect(result.ok).toBe(false);
  expect(await repository.load(existingState.moduleId)).toEqual(existingState);
});

test('failed migration preserves the original state byte-for-byte', async () => {
  const original = state({ stateSchemaVersion: 1, payload: { text: 'alt' } });
  const repository = seededRepository(original);
  const result = await createRuntime(repository, failingMigration).start();
  expect(result.error?.code).toBe('MIGRATION_FAILED');
  expect(await repository.load(original.moduleId)).toEqual(original);
});
```

- [ ] **Step 2: Run and observe missing service failures**

```powershell
npm run test:platform -- --run tests/platform/export-import.test.ts tests/platform/runtime.test.ts
```

Expected: FAIL because import/export/runtime exports do not exist.

- [ ] **Step 3: Implement deterministic export and defensive parsing**

Encode with `TextEncoder`, two-space JSON indentation, LF, and exactly one final newline. Use filename `ium-<lowercase-safe-module-id>-<UTC-YYYY-MM-DD>.json`; never include workspace ID. Parse only UTF-8 JSON, validate the closed envelope, reject wrong modules and unsupported future versions, and return a preview containing module ID, module version, saved time, and payload field names—but not rendered HTML.

- [ ] **Step 4: Implement copied sequential migrations and runtime use cases**

Migration functions have this signature:

```ts
export type StateMigration = Readonly<{
  from: number;
  to: number;
  migrate: (payload: Readonly<Record<string, unknown>>) => Record<string, unknown>;
}>;
```

Deep-copy the envelope before each `n → n+1` step, validate after every step, and save only the final validated target. Runtime methods are `start`, `updatePayload`, `flush`, `exportState`, `previewImport`, `confirmImport`, `deleteActive`, and `deleteAll`.

- [ ] **Step 5: Add download and copy fallback tests**

Verify successful explicit download, rejected browser download followed by copy text, export while offline, delete reread confirmation, and selected volatile mode.

- [ ] **Step 6: Run package and legacy gates**

```powershell
npm run test:platform -- --run tests/platform/export-import.test.ts tests/platform/runtime.test.ts
npm run typecheck
python -B scripts/validate_phase0.py
```

Expected: PASS.

- [ ] **Step 7: Commit Task 4**

```powershell
git add packages/export-import packages/module-runtime tests/platform/export-import.test.ts tests/platform/runtime.test.ts package.json package-lock.json
git commit -m "feat: add safe state transfer runtime"
```

---

### Task 5: Static portal shell and accessible UI primitives

**Files:**
- Create: `apps/lernwerk-portal/package.json`
- Create: `apps/lernwerk-portal/tsconfig.json`
- Create: `apps/lernwerk-portal/astro.config.ts`
- Create: `apps/lernwerk-portal/src/env.d.ts`
- Create: `apps/lernwerk-portal/src/layouts/BaseLayout.astro`
- Create: `apps/lernwerk-portal/src/pages/index.astro`
- Create: `apps/lernwerk-portal/src/pages/daten.astro`
- Create: `apps/lernwerk-portal/src/pages/offline.astro`
- Create: `apps/lernwerk-portal/src/pages/module/[id].astro`
- Create: `apps/lernwerk-portal/src/styles/global.css`
- Create: `packages/ui-components/package.json`
- Create: `packages/ui-components/tsconfig.json`
- Create: `packages/ui-components/src/components/StorageStatus.astro`
- Create: `packages/ui-components/src/components/ConnectionStatus.astro`
- Create: `packages/ui-components/src/components/ErrorSummary.astro`
- Create: `packages/ui-components/src/components/UpdatePrompt.astro`
- Create: `packages/ui-components/src/components/DataControls.astro`
- Create: `packages/ui-components/src/styles/components.css`
- Create: `tests/platform/helpers/build-portal.ts`
- Create: `tests/platform/portal-build.test.ts`
- Modify: `package.json`

**Interfaces:**
- Consumes: generated registry and build info.
- Produces: root/subpath-safe static routes, production-empty state, shared status component DOM contracts.
- Produces: `buildPortal(profile, base): Promise<BuiltPortal>` with `text(path)`, `glob(pattern)`, `manifest`, `serviceWorkerText`, and `externalUrls` readers over an isolated temporary build.
- Produces: commands `build`, `build:fixture`, `build:fixture:subpath`, `check:astro`, `preview:fixture`.

- [ ] **Step 1: Write failing production-empty and fixture-route build tests**

```ts
test('production build is honest and has no module route', async () => {
  const output = await buildPortal('production', '/');
  expect(await output.text('index.html')).toContain('Noch keine Lernmodule veröffentlicht');
  expect(await output.glob('module/**/index.html')).toEqual([]);
});

test('fixture build exposes only the synthetic route', async () => {
  const output = await buildPortal('fixture', '/');
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/test-platform-reference/index.html'
  ]);
  expect(await output.text('index.html')).toContain('Technische Systemprobe');
});
```

- [ ] **Step 2: Run and observe the missing app failure**

```powershell
npm run test:platform -- --run tests/platform/portal-build.test.ts
```

Expected: FAIL because the Astro app and build helper do not exist.

- [ ] **Step 3: Implement the static app and strict profile orchestration**

Astro output is `static`. Read only `IUM_BUILD_PROFILE` values `production|fixture` and base paths normalized to leading/trailing `/`; reject any other profile or path containing `..`, query, fragment, or URL scheme. Run the corresponding fixed registry command before Astro. `getStaticPaths()` returns only registry entries.

- [ ] **Step 4: Implement accessible shell components**

Use a skip link, one `main`, consistent landmarks, visible focus, system fonts, 320 CSS-pixel reflow, no color-only state, minimum 44×44 CSS-pixel action targets, and `aria-live="polite"` only for concise storage/connection updates. `ErrorSummary` uses `role="alert"`, an actual heading, links to invalid controls, a closed error-code mapping, and a collapsed technical `<details>` block.

- [ ] **Step 5: Verify root and subpath static output**

```powershell
npm run build
npm run build:fixture
npm run build:fixture:subpath
npm run check:astro
npm run test:platform -- --run tests/platform/portal-build.test.ts
```

Expected: all PASS; subpath HTML contains `/ium-lernwerk/` asset and route prefixes and no hardcoded root navigation.

- [ ] **Step 6: Commit Task 5**

```powershell
git add apps/lernwerk-portal packages/ui-components tests/platform/portal-build.test.ts package.json package-lock.json
git commit -m "feat: add accessible static portal shell"
```

---

### Task 6: Fixture workspace and browser data flows

**Files:**
- Create: `apps/lernwerk-portal/src/components/FixtureWorkspace.astro`
- Create: `apps/lernwerk-portal/src/controllers/fixture-workspace.ts`
- Create: `packages/ui-components/src/controllers/data-controls.ts`
- Create: `packages/ui-components/src/controllers/status-announcer.ts`
- Create: `playwright.config.ts`
- Create: `tests/browser/platform.spec.ts`
- Modify: `apps/lernwerk-portal/src/pages/module/[id].astro`
- Modify: `apps/lernwerk-portal/src/pages/daten.astro`
- Modify: `package.json`

**Interfaces:**
- Consumes: module runtime, local-state factory, import/export services.
- Produces: DOM events `ium:state-status`, `ium:error`, and `ium:data-changed` with closed detail shapes.
- Produces: command `test:browser`.

- [ ] **Step 1: Write failing end-to-end persistence and transfer tests**

```ts
test('edit, reload, export, delete and import is lossless', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await page.getByLabel('Synthetischer Text').fill('Zustand A');
  await page.getByLabel('Synthetische Auswahl').selectOption('beta');
  await expect(page.getByRole('status')).toContainText('Lokal gespeichert');
  await page.reload();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Zustand A');
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Exportieren' }).click();
  const exportFile = await download;
  await page.getByRole('button', { name: 'Arbeitsstand löschen' }).click();
  await page.getByRole('button', { name: 'Löschen bestätigen' }).click();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('');
  await page.setInputFiles('input[type=file]', await exportFile.path());
  await page.getByRole('button', { name: 'Import übernehmen' }).click();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Zustand A');
});
```

Also write tests for keyboard-only use, one active state, selected volatile mode, wrong-module rejection, copy fallback when download is blocked, delete-all reread, and a sandboxed iframe with blocked storage/download.

- [ ] **Step 2: Run Chromium and observe missing workspace behavior**

```powershell
npm run build:fixture
npx playwright test tests/browser/platform.spec.ts --project=chromium
```

Expected: FAIL at missing fixture controls or runtime behavior.

- [ ] **Step 3: Wire the fixture to runtime ports**

Use only the two synthetic fields `text` and `choice`. Debounce input by 250 ms, flush on `change`, `visibilitychange` when hidden, and explicit export/update actions. Do not save before the repository transaction confirms. Render imported text with form `.value` only, never `innerHTML`.

- [ ] **Step 4: Implement import preview, confirmation and deletion UX**

Preview module ID, version, saved time, and field names. Require an explicit confirmation for replace, module delete, and global delete. Restore focus to the initiating control after cancel and to the primary workspace heading after a successful import/delete.

- [ ] **Step 5: Run all three browser engines and unit regressions**

```powershell
npx playwright install chromium firefox webkit
npm run test:browser
npm run test:platform
npm run typecheck
```

Expected: Chromium, Firefox, and WebKit data-flow tests PASS.

- [ ] **Step 6: Commit Task 6**

```powershell
git add apps/lernwerk-portal packages/ui-components playwright.config.ts tests/browser/platform.spec.ts package.json package-lock.json
git commit -m "feat: complete fixture local-first data flow"
```

---

### Task 7: Controlled PWA, offline and update lifecycle

**Files:**
- Create: `apps/lernwerk-portal/src/sw.ts`
- Create: `apps/lernwerk-portal/src/controllers/pwa-registration.ts`
- Create: `apps/lernwerk-portal/public/app-icon.svg`
- Create: `apps/lernwerk-portal/public/icons/pwa-192x192.png`
- Create: `apps/lernwerk-portal/public/icons/pwa-512x512.png`
- Create: `apps/lernwerk-portal/public/icons/maskable-512x512.png`
- Create: `tests/browser/offline.spec.ts`
- Create: `tests/platform/pwa-contract.test.ts`
- Modify: `apps/lernwerk-portal/astro.config.ts`
- Modify: `apps/lernwerk-portal/src/layouts/BaseLayout.astro`
- Modify: `packages/ui-components/src/components/UpdatePrompt.astro`
- Modify: `packages/ui-components/src/components/ConnectionStatus.astro`
- Modify: `package.json`

**Interfaces:**
- Produces: PWA states `not-ready|ready|offline|degraded`.
- Produces: update controller methods `check`, `activateAfterFlush`, `dismiss`.
- Produces: message `SKIP_WAITING` only after explicit activation.

- [ ] **Step 1: Write failing static PWA contract tests**

```ts
import { readFile } from 'node:fs/promises';

test('custom worker has no unconditional skipWaiting', async () => {
  const source = await readFile('apps/lernwerk-portal/src/sw.ts', 'utf8');
  expect(source.match(/self\.skipWaiting\(/g)).toHaveLength(1);
  expect(source).toMatch(
    /if \(event\.data\?\.type === 'SKIP_WAITING'\)[\s\S]*self\.skipWaiting\(\)/
  );
});

test('fixture precache stays inside the configured base and contains offline route', async () => {
  const build = await buildPortal('fixture', '/ium-lernwerk/');
  expect(build.manifest.start_url).toBe('/ium-lernwerk/');
  expect(build.serviceWorkerText).toContain('/ium-lernwerk/offline/');
  expect(build.externalUrls).toEqual([]);
});
```

- [ ] **Step 2: Run and observe missing worker/config failures**

```powershell
npm run test:platform -- --run tests/platform/pwa-contract.test.ts
```

Expected: FAIL because the service worker and manifest are absent.

- [ ] **Step 3: Configure direct Vite PWA `injectManifest`**

In `astro.config.ts`, add `VitePWA` under `vite.plugins`, `strategies: 'injectManifest'`, `srcDir: 'src'`, `filename: 'sw.ts'`, `registerType: 'prompt'`, exact base-aware `scope` and `start_url`, and local icon entries. Do not enable auto-update.

- [ ] **Step 4: Implement the custom worker and registration controller**

Use `precacheAndRoute(self.__WB_MANIFEST)`, a navigation catch handler that returns the base-aware precached offline page, and this only activation path:

```ts
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    void self.skipWaiting();
  }
});
```

The page registration exposes `ready` only from `onOfflineReady`, shows a prompt from `onNeedRefresh`, calls `runtime.flush()` before `updateSW(true)`, and keeps the old page active if flush fails.

- [ ] **Step 5: Generate deterministic local PWA assets**

Create a simple geometric source SVG containing no text and no third-party mark. Generate 192, 512, and maskable 512 PNG files using the pinned assets generator. Record the exact command in `package.json` as `assets:pwa`; rerunning it must produce the same dimensions and no network requests.

- [ ] **Step 6: Write and run Chromium offline/update scenarios**

Cover:

- successful first online fixture load, confirmed ready, then offline reload;
- network loss during input with local save and export;
- unknown cached-shell path yielding the offline page;
- second build installing as waiting worker and showing a prompt;
- explicit update after a successful flush;
- missing asset in a candidate build causing install failure while the old worker remains active;
- state schema 1 to 2 migration on copied data;
- return online;
- root and `/ium-lernwerk/` scopes.

Run:

```powershell
npm run test:offline
```

Expected: PASS in Chromium. Firefox/WebKit retain data-flow tests; do not claim their service-worker behavior from this automation.

- [ ] **Step 7: Run PWA, portal, browser and type gates**

```powershell
npm run test:platform -- --run tests/platform/pwa-contract.test.ts tests/platform/portal-build.test.ts
npm run test:offline
npm run typecheck
```

Expected: PASS.

- [ ] **Step 8: Commit Task 7**

```powershell
git add apps/lernwerk-portal packages/ui-components tests/browser/offline.spec.ts tests/platform/pwa-contract.test.ts package.json package-lock.json
git commit -m "feat: add controlled offline update lifecycle"
```

---

### Task 8: Accessibility, budgets, licenses and no-network gates

**Files:**
- Create: `scripts/check-build-output.ts`
- Create: `scripts/check-dependency-licenses.ts`
- Create: `tests/platform/build-quality.test.ts`
- Create: `tests/browser/accessibility.spec.ts`
- Modify: `playwright.config.ts`
- Modify: `package.json`
- Modify: `apps/lernwerk-portal/src/styles/global.css`
- Modify when a failing test demonstrates a defect: `packages/ui-components/src/components/StorageStatus.astro`
- Modify when a failing test demonstrates a defect: `packages/ui-components/src/components/ConnectionStatus.astro`
- Modify when a failing test demonstrates a defect: `packages/ui-components/src/components/ErrorSummary.astro`
- Modify when a failing test demonstrates a defect: `packages/ui-components/src/components/UpdatePrompt.astro`
- Modify when a failing test demonstrates a defect: `packages/ui-components/src/components/DataControls.astro`

**Interfaces:**
- Produces: command `quality:build`.
- Produces: command `quality:licenses`.
- Produces: command `test:accessibility`.
- Produces: `inspectBuild(distDir): Promise<BuildQualityReport>`.
- Produces: machine-readable reports under ignored `reports/phase1/`.

- [ ] **Step 1: Write failing build-quality budget tests**

```ts
test('fixture build remains inside approved budgets', async () => {
  const report = await inspectBuild(fixtureDist);
  expect(report.coldTransferGzipBytes).toBeLessThanOrEqual(250 * 1024);
  expect(report.initialJavaScriptGzipBytes).toBeLessThanOrEqual(100 * 1024);
  expect(report.precacheDecodedBytes).toBeLessThanOrEqual(2 * 1024 * 1024);
  expect(report.thirdPartyUrls).toEqual([]);
});
```

Also fail on `http://`, `https://`, protocol-relative URLs, `eval`, `new Function`, non-base-aware absolute local paths, missing license evidence, and a `TEST-` ID in production output.

- [ ] **Step 2: Write failing real accessibility tasks**

Run axe on every Phase-1 route, then test skip-link focus, logical tab order, error-summary focus links, live status, 320×640 reflow, 200% zoom-equivalent viewport, reduced motion, and 44×44 action targets. Assert no horizontal page scroll and no essential state conveyed by color-only classes.

- [ ] **Step 3: Run and observe missing quality-script failures**

```powershell
npm run test:platform -- --run tests/platform/build-quality.test.ts
npx playwright test tests/browser/accessibility.spec.ts --project=chromium
```

Expected: FAIL because quality inspectors and/or required accessibility behavior are absent.

- [ ] **Step 4: Implement deterministic build inspection**

Measure gzip with Node `zlib.gzipSync` at level 9, decoded cache bytes from the generated precache list, and cold entry resources parsed from built HTML. Normalize paths and JSON report ordering. Do not count source maps or the ignored report itself.

- [ ] **Step 5: Implement dependency-license and SBOM gate**

Use `npm query . --json` and allow only exact SPDX expressions from this reviewed set: `MIT`, `ISC`, `BSD-2-Clause`, `BSD-3-Clause`, `Apache-2.0`, `CC0-1.0`, `0BSD`, and `BlueOak-1.0.0`. Fail on missing, unknown, GPL/AGPL/SSPL, or non-SPDX values until explicitly reviewed. Run `npm sbom --sbom-format cyclonedx` and validate that root plus every installed package appears; write the SBOM only to ignored `reports/phase1/`.

- [ ] **Step 6: Fix only demonstrated accessibility or budget defects**

Keep system fonts, framework-free controls, and the approved budgets. If a dependency alone causes a budget breach, prefer lazy loading or removal over raising the budget.

- [ ] **Step 7: Run all quality gates**

```powershell
npm run build:fixture
npm run quality:build
npm run quality:licenses
npm run test:accessibility
npm run boundaries:check
npm run typecheck
```

Expected: PASS with zero third-party requests and all four budgets green.

- [ ] **Step 8: Commit Task 8**

```powershell
git add scripts/check-build-output.ts scripts/check-dependency-licenses.ts tests/platform/build-quality.test.ts tests/browser/accessibility.spec.ts apps/lernwerk-portal packages/ui-components package.json package-lock.json playwright.config.ts
git commit -m "test: enforce phase1 platform quality gates"
```

---

### Task 9: CI, documentation and explicit device gate

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `scripts/verify-phase1.ts`
- Create: `docs/platform/README.md`
- Create: `docs/platform/device-verification.md`
- Modify: `README.md`
- Modify: `package.json`
- Test: `tests/platform/documentation.test.ts`

**Interfaces:**
- Produces: root command `verify:phase1`.
- Produces: GitHub CI jobs `legacy`, `contracts-build`, `browser`, and `offline-quality`.
- Produces: explicit status boundary `implemented` versus `device-verified`.

- [ ] **Step 1: Write failing documentation/status tests**

Require README links to the approved spec, implementation plan, portal commands, Local-First data documentation, and device protocol. Require device protocol fields for date, operator, device, OS/browser versions, MDM/Web-Clip/storage/filter policy, VoiceOver, Chromium, Firefox, online/offline, import/export, update, result, finding, and evidence path. Require its status to remain `not-run` until real evidence exists.

- [ ] **Step 2: Run and observe missing docs/CI failures**

```powershell
npm run test:platform -- --run tests/platform/documentation.test.ts
```

Expected: FAIL because files and command do not exist.

- [ ] **Step 3: Add the complete root verification command**

`verify:phase1` runs, in this order:

```text
contracts:check
boundaries:check
typecheck
test:platform
build
build:fixture
build:fixture:subpath
quality:build
quality:licenses
test:browser
test:offline
test:accessibility
test:python
build_ium11_cockpit --check
build_ium11_publication_contract --check
validate_ium11
validate_ium10
validate_ium09
validate_phase0
```

Implement `scripts/verify-phase1.ts` as the sole cross-platform fail-fast orchestrator. It runs the listed commands through `spawnSync` with inherited stdio, stops at the first nonzero or missing-process result, and returns that exit code. Define `verify:phase1` exactly as `tsx scripts/verify-phase1.ts`; do not duplicate the command chain in a shell-specific npm script.

- [ ] **Step 4: Add GitHub Actions**

Use `actions/checkout@v5`, `actions/setup-node@v5`, and `actions/upload-artifact@v4`. Use Node 22.20.0, `npm ci`, cache npm only, install Playwright browsers with dependencies in the browser job, and upload ignored reports only as CI artifacts. No deployment job, secrets, real data, or release status is added.

- [ ] **Step 5: Document operation and honest status**

Explain production-empty versus fixture builds, data modes, export sensitivity, global delete, first-ever offline limitation, controlled updates, embedding fallbacks, root/subpath deployment, licenses, exact QA commands, and the fact that CI can establish only `implemented`. Keep the real device checklist `not-run`.

- [ ] **Step 6: Run docs, workflow syntax and full automated verification**

```powershell
npm run test:platform -- --run tests/platform/documentation.test.ts
npm run verify:phase1
```

Expected: all automated gates PASS. Device protocol remains visibly `not-run`.

- [ ] **Step 7: Commit Task 9**

```powershell
git add .github/workflows/ci.yml scripts/verify-phase1.ts docs/platform README.md package.json tests/platform/documentation.test.ts
git commit -m "docs: operationalize phase1 platform verification"
```

---

### Task 10: Final review, integration and handoff

**Files:**
- Modify: only files implicated by verified review findings.
- Create: `docs/platform/implementation-report.md`
- Modify: Workspace task, initiative, Kanban, project page, development history, and Codex session summary outside the repository.

**Interfaces:**
- Produces: final status `implemented` only if every automated gate is green.
- Leaves: `device-verified: not-run` and Phase 2 blocked.

- [ ] **Step 1: Inspect the complete branch diff against the plan baseline**

Run:

```powershell
git diff --check b00971e..HEAD
git diff --stat b00971e..HEAD
git status --short --branch
```

Review contract ownership, schema/type identity, fixture isolation, import rendering, storage transaction confirmation, update activation, cache/base paths, accessibility semantics, licenses, generated-file hygiene, and every Global Constraint.

- [ ] **Step 2: Run a mutation audit for fail-closed boundaries**

Temporarily mutate one case at a time in tests or temporary copies and confirm rejection for unknown manifest fields, `TEST-` production ID, real fixture curriculum ID, identity field in state, 5 MiB + 1 import, wrong module, unsupported version, failed migration, failed IndexedDB write, unconditional `skipWaiting`, external URL, over-budget asset, forbidden license, and missing device evidence. Revert only temporary mutations; do not weaken gates.

- [ ] **Step 3: Perform a local real-Chromium visual and keyboard check**

Serve the committed fixture build on localhost. Inspect at 320, 768, and 1280 CSS pixels; 200% zoom; keyboard-only navigation; focus restoration; reduced motion; offline reload; update prompt; import/export/delete; and network log. Capture findings in `implementation-report.md`. This is a local browser check, not the managed-iPad device gate.

- [ ] **Step 4: Fix verified findings test-first and commit each coherent fix**

For each finding: add a failing regression test, observe failure, implement the smallest fix, run focused plus affected suites, and commit with `fix: ...`. If no finding exists, record `no additional finding` without creating an empty commit.

- [ ] **Step 5: Run the final clean verification from committed sources**

```powershell
npm ci
npm run verify:phase1
git diff --check b00971e..HEAD
git status --short --branch
```

Expected: all gates PASS; only the intended implementation report or final handoff edit may be uncommitted before its final commit.

- [ ] **Step 6: Write and commit the implementation report**

Report exact Node/npm/dependency versions, commit range, test counts, builds, budgets, browser versions, accessibility results, Local-First/error/offline/update evidence, fixture isolation, known limitations, and the explicit open `device-verified` gate.

```powershell
git add docs/platform/implementation-report.md
git commit -m "docs: hand off phase1 platform implementation"
```

- [ ] **Step 7: Synchronize safely and integrate**

Before any push:

```powershell
git fetch --prune
git pull --ff-only origin main
```

Run this only after confirming `origin/main` is an ancestor of the feature branch; otherwise stop and reconcile the moved base without rewriting history. Push the feature branch with its upstream, integrate only after all checks, rerun the full verification on the integrated `main`, and push `main` without force.

- [ ] **Step 8: Update Workspace handoff**

Mark the implementation task `done` only for status `implemented`. Keep the initiative `in_progress` or `review` with `device-verified: not-run`; keep Phase 2 blocked. Record final commits, branch, remote, test totals, budgets, browser matrix, and the exact next real-device action in Task, Initiative, Kanban, Project, History, and Session Summary.

---

## Plan Self-Review

### Specification coverage

| Specification area | Implemented by |
|---|---|
| Scope and Phase-2 boundary | Global Constraints, Tasks 2, 9, 10 |
| Contract-first workspace | Tasks 1–2 |
| Manifest and deterministic registry | Tasks 1–2 |
| Local state and visible modes | Task 3 |
| Import, export, delete and migrations | Task 4 |
| Static portal and framework-free UI | Tasks 5–6 |
| Root/subpath and embedding | Tasks 5–8 |
| Offline and controlled updates | Task 7 |
| Accessibility and real tasks | Tasks 5–8, 10 |
| Budgets, licenses, OER and no network | Task 8 |
| CI and reproducibility | Task 9 |
| `implemented` versus `device-verified` | Tasks 9–10 |
| Existing Python/IUM regression preservation | Tasks 1, 4, 9, 10 |

### Self-review result

- All 26 specification sections map to at least one task.
- Production and fixture roots, ID namespaces, curriculum inputs, status effects and output profiles are explicit.
- Database migration belongs to `local-state`; module-state migration belongs to `module-runtime`.
- Import parsing never mutates storage; only a confirmed runtime action commits a fully migrated copy.
- The service worker cannot activate automatically and the old release survives an incomplete new install.
- Automated browser evidence does not claim Safari service-worker verification.
- The implementation can honestly finish as `implemented` while leaving the managed-iPad `device-verified` gate open.
- No placeholder instructions, floating versions, unowned interfaces or implicit follow-up implementation remain.

## Execution Decision

The user already selected inline execution by asking: “Erstelle den Plan und setze ihn dann um.” Execute with `superpowers:executing-plans`; do not dispatch implementation subagents.
