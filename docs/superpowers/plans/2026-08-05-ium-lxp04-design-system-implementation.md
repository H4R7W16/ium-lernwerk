# IuM LXP04 Design System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das in LXP04 spezifizierte Learning-Experience-System als eigenständiges Paket implementieren, IUM5 über drei Referenzsituationen migrieren und die Qualitäts-, Accessibility-, Offline-, Datenschutz- und Produktionsverträge automatisiert absichern.

**Architecture:** `@ium/learning-experience` trägt semantische Experience-Verträge, Astro-Komponenten, CSS-Tokens und kleine progressive Controller. `@ium/ui-components` bleibt bei technischen Plattformzuständen; `@ium/ium-5-core-05` bleibt framework- und DOM-frei und liefert nur fachliche Zustände. Der Portal-Adapter verbindet diese drei Schichten, während Modulinhalt in `experience.json` versioniert und vor dem Build validiert wird.

**Tech Stack:** npm workspaces, TypeScript 6, Astro 7, CSS Custom Properties, Vitest 4, Playwright 1.62, axe-core, Python `unittest` und die bestehenden IuM-Verifikationsskripte.

## Global Constraints

- Dieser Plan ist der Implementierungshandoff von LXP04 an LXP05. Er wird erst nach der ausdrücklich dokumentierten Nutzerfreigabe von LXP04 ausgeführt.
- Für diesen Workspace ist `superpowers:executing-plans` in derselben Session der Standard. Subagenten werden nur eingesetzt, wenn der Nutzer das zusätzlich ausdrücklich autorisiert.
- Vor der ersten Änderung: `git status --short --branch`, `git fetch --prune` und `git pull --ff-only`. Bei einem Fehler von Fetch oder Pull nicht committen oder pushen.
- Produktimplementierung erfolgt in einem separaten Worktree und auf einem neuen Feature-Branch ab dem dann aktuellen lokalen `main`.
- Jeder Produktionsschritt beginnt mit einem fokussierten fehlschlagenden Test, anschließend minimaler Implementierung und erneutem Testlauf.
- Nicht in `Vault/`, `Vault/.obsidian/` oder `.git/` schreiben. Keine Build-Artefakte, Browserprofile, `node_modules` oder Secrets committen.
- Kein Push, Pull Request, Preview-Deployment, Realgeräte-, Pilot-, LMS- oder Release-Schritt ohne die dafür getrennt dokumentierten Freigaben.
- Keine Interaktions- oder Nutzungsmetriken ergänzen. Insbesondere bleiben `elapsedMs`, `attemptCount`, `clicks`, `hintUsage`, `playbackSpeed` und Namen aus dem persistierten Payload ausgeschlossen.
- Keine Nutzereingabe in `localStorage`, `sessionStorage` oder Cookies persistieren. Der bestehende IndexedDB-Pfad über `@ium/local-state` bleibt die einzige persistente Datenquelle.
- `@ium/ium-5-core-05` darf weder Astro-/DOM-Abhängigkeiten noch Importe aus `@ium/learning-experience` erhalten.
- Jede sichtbare Statusänderung muss auch programmatisch verfügbar sein; Farbe, Position oder Animation allein dürfen keine Bedeutung tragen.
- Motion ist optional, höchstens 180 ms lang und bei `prefers-reduced-motion: reduce` vollständig deaktiviert.

## Target State

~~~text
modules/IUM-5-CORE-05/lernumgebung/
└── experience.json
        │ validate + type
        ▼
@ium/learning-experience ── Astro patterns + tokens + controllers
        ▲                                  │
        │ semantic state                   │ progressive enhancement
@ium/ium-5-core-05                         ▼
        │                         apps/lernwerk-portal
        └──────── portal adapter ──────────┘
                        │
                        ▼
                 @ium/local-state
~~~

## Task 1: Freeze Package Boundaries and Workspace Wiring

**Files:**

- Create: `packages/learning-experience/package.json`
- Create: `packages/learning-experience/tsconfig.json`
- Create: `packages/learning-experience/src/index.ts`
- Modify: `package.json`
- Modify: `tsconfig.json`
- Modify: `apps/lernwerk-portal/package.json`
- Modify: `scripts/check-workspace-boundaries.ts`
- Test: `tests/platform/boundaries.test.ts`

- [ ] **Step 1: Add a failing architecture test**

Append a test that recognizes the new package, permits only its declared leaf dependencies, and rejects reverse imports from core:

~~~ts
test('recognizes learning-experience as a semantic leaf package', async () => {
  const report = await checkWorkspaceBoundaries({ rootDir: repoRoot });
  expect(report.workspaces).toContain('@ium/learning-experience');
  expect(report.violations).toEqual([]);
});

test('rejects learning-experience imports from framework-free core', async () => {
  const root = await createWorkspace(
    'packages/ium-5-core-05',
    {
      name: '@ium/ium-5-core-05',
      version: '0.1.0',
      private: true,
      dependencies: { '@ium/learning-experience': '0.1.0' },
    },
    "import '@ium/learning-experience';\n",
  );
  const report = await checkWorkspaceBoundaries({ rootDir: root });
  expect(report.violations.map((entry) => entry.code)).toContain(
    'UNAPPROVED_DEPENDENCY',
  );
});
~~~

- [ ] **Step 2: Verify the test fails for the missing workspace**

Run: `npx vitest run tests/platform/boundaries.test.ts`

Expected: FAIL because `@ium/learning-experience` is not present in the discovered workspaces.

- [ ] **Step 3: Create the package skeleton**

Use this package contract:

~~~json
{
  "name": "@ium/learning-experience",
  "version": "0.1.0",
  "private": true,
  "license": "MIT",
  "type": "module",
  "exports": {
    ".": "./src/index.ts",
    "./components/*": "./src/components/*.astro",
    "./controllers/*": "./src/controllers/*.ts",
    "./styles/*": "./src/styles/*"
  }
}
~~~

The package has no runtime dependency on `@ium/ium-5-core-05`, `@ium/local-state` or `@ium/ui-components`. Add it to the root TypeScript references and to portal dependencies. Update the boundary allowlist so the portal may import it while core packages may not.

- [ ] **Step 4: Verify boundary and type wiring**

Run:

~~~powershell
npm install --package-lock-only
npx vitest run tests/platform/boundaries.test.ts
npm run typecheck
~~~

Expected: all three commands PASS; the lockfile contains `@ium/learning-experience` as a workspace link.

- [ ] **Step 5: Commit the boundary**

~~~powershell
git add package.json package-lock.json tsconfig.json apps/lernwerk-portal/package.json packages/learning-experience scripts/check-workspace-boundaries.ts tests/platform/boundaries.test.ts
git commit -m "feat(experience): establish semantic package boundary"
~~~

## Task 2: Implement Versioned Content and Interaction Contracts

**Files:**

- Create: `packages/learning-experience/src/contracts.ts`
- Create: `packages/learning-experience/src/validation.ts`
- Modify: `packages/learning-experience/src/index.ts`
- Test: `tests/platform/learning-experience-contracts.test.ts`

- [ ] **Step 1: Write the closed-contract tests**

Test a smallest valid document, every enum, duplicate IDs, unknown top-level and nested keys, missing German labels, invalid character limits, inaccessible action names and an unsupported `schemaVersion`:

~~~ts
import { describe, expect, test } from 'vitest';
import {
  parseExperienceContent,
  type ExperienceContentV1,
  type SupportSpec,
} from '../../packages/learning-experience/src/index.js';

const valid: ExperienceContentV1 = {
  schemaVersion: 1,
  moduleId: 'ium-informatik-5',
  terminologyVersion: 'lxp04-1',
  start: {
    heading: 'Algorithmen untersuchen',
    guidingQuestion: 'Wie wird aus einer Vermutung ein begründeter Algorithmus?',
    expectedCapability: 'Vermutung bilden, ausführen und mit Belegen überarbeiten.',
    timeWindowMinutes: [35, 50],
    socialForm: 'individual',
    primaryAction: {
      label: 'Mit der Vermutung beginnen',
      result: 'Die erste Vorhersage wird vorbereitet.',
    },
    resumeAction: null,
    resetAction: null,
  },
  actions: [],
  tasks: [],
  feedback: [],
  supports: [],
  checkpoints: [],
  evidenceCards: [],
  resilience: [],
};

describe('ExperienceContentV1', () => {
  test('accepts the smallest closed document', () => {
    expect(parseExperienceContent(valid)).toEqual({ ok: true, value: valid });
  });

  test('rejects unknown fields without coercion', () => {
    expect(parseExperienceContent({ ...valid, analytics: {} }).ok).toBe(false);
  });

  test('rejects duplicate IDs inside one contract collection', () => {
    const support: SupportSpec = {
      id: 'concept-algorithm',
      kind: 'concept',
      title: 'Begriff klären',
      trigger: 'Der Begriff Algorithmus ist noch unklar.',
      content: 'Ein Algorithmus beschreibt eindeutige ausführbare Schritte.',
      preservesAction: 'Die Vorhersage und Prüfung bleiben bei dir.',
      nextSupportId: null,
    };
    const duplicate = { ...valid, supports: [support, support] };
    const result = parseExperienceContent(duplicate);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.errors.map((error) => error.code)).toContain('duplicate_id');
    }
  });

  test('rejects unsupported future versions', () => {
    expect(parseExperienceContent({ ...valid, schemaVersion: 2 }).ok).toBe(false);
  });
});
~~~

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/learning-experience-contracts.test.ts`

Expected: FAIL because the package does not export the contract or parser.

- [ ] **Step 3: Implement exact TypeScript contracts**

Define the following closed, readonly contracts exactly from the LXP04 specification:

~~~ts
export interface ExperienceContentV1 {
  readonly schemaVersion: 1;
  readonly moduleId: string;
  readonly terminologyVersion: 'lxp04-1';
  readonly start: StartBoardSpec;
  readonly actions: readonly LearningActionSpec[];
  readonly tasks: readonly LearningTaskSpec[];
  readonly feedback: readonly FeedbackSpec[];
  readonly supports: readonly SupportSpec[];
  readonly checkpoints: readonly TeacherCheckpointSpec[];
  readonly evidenceCards: readonly EvidenceCardSpec[];
  readonly resilience: readonly ResilienceSpec[];
}

export interface LearningActionSpec {
  readonly id: string;
  readonly state: LearningStateId;
  readonly taskId: string;
  readonly purpose: string;
  readonly prompt: string;
  readonly product: string;
  readonly criteria: readonly string[];
  readonly primaryAction: {
    readonly label: string;
    readonly result: string;
  };
  readonly secondaryActions: readonly {
    readonly label: string;
    readonly purpose: string;
  }[];
  readonly requiredEvidence: readonly string[];
  readonly supportIds: readonly string[];
  readonly checkpointId: string | null;
  readonly persistence: 'none' | 'draft' | 'confirmed-product' | 'evidence';
  readonly next: readonly {
    readonly state: LearningStateId;
    readonly guard: string;
  }[];
}

export interface SupportSpec {
  readonly id: string;
  readonly kind: 'operation' | 'concept' | 'strategy' | 'example';
  readonly title: string;
  readonly trigger: string;
  readonly content: string;
  readonly preservesAction: string;
  readonly nextSupportId: string | null;
}
~~~

Add `StartBoardSpec`, `LearningTaskSpec`, `FeedbackSpec`, `EvidenceCardSpec`, `TeacherCheckpointSpec` and `ResilienceSpec` exactly as defined in the LXP04 spec. `LearningStateId` is the controlled eleven-state LXP02 vocabulary, not an open string. Validate every action → task, task → feedback/support/recovery, checkpoint, evidence-card and support-escalation reference. Do not expose module-specific command types in this package.

- [ ] **Step 4: Implement a strict parser**

The parser must return a discriminated result and collect path-specific errors:

~~~ts
export type ContractError = {
  readonly path: string;
  readonly code:
    | 'invalid_type'
    | 'missing_field'
    | 'unknown_field'
    | 'invalid_value'
    | 'duplicate_id'
    | 'limit_exceeded';
  readonly message: string;
};

export type ParseResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly errors: readonly ContractError[] };
~~~

Enforce the LXP04 content limits by Unicode code points: purpose/prompt 600, action label 72, criterion 240, support title 72, support content 1,200 and resilience message 600. Reject empty-trimmed strings, duplicate IDs in their scope, dangling task/feedback/support/checkpoint/evidence-card/resilience references, forbidden analytics fields and every unknown property. Return a fresh deep structure; never mutate or coerce input.

- [ ] **Step 5: Verify parser behavior**

Run:

~~~powershell
npx vitest run tests/platform/learning-experience-contracts.test.ts
npm run typecheck
~~~

Expected: both PASS.

- [ ] **Step 6: Commit the contracts**

~~~powershell
git add packages/learning-experience/src tests/platform/learning-experience-contracts.test.ts
git commit -m "feat(experience): add versioned content contracts"
~~~

## Task 3: Implement the Semantic Foundation and Automated Contrast Checks

**Files:**

- Create: `packages/learning-experience/src/styles/tokens.css`
- Create: `packages/learning-experience/src/styles/foundation.css`
- Create: `packages/learning-experience/src/styles/motion.css`
- Create: `packages/learning-experience/src/styles/patterns.css`
- Create: `packages/learning-experience/src/styles/index.css`
- Modify: `apps/lernwerk-portal/src/styles/global.css`
- Test: `tests/platform/learning-experience-styles.test.ts`

- [ ] **Step 1: Add static style-contract tests**

Read the CSS files in the test and assert the exact semantic tokens, system font stack, container breakpoints, focus treatment and reduced-motion override:

~~~ts
test('publishes the approved semantic palette', async () => {
  const css = await readFile(tokensPath, 'utf8');
  expect(css).toContain('--lx-color-canvas: #f7f5f0');
  expect(css).toContain('--lx-color-ink: #17212b');
  expect(css).toContain('--lx-color-action: #005a70');
  expect(css).toContain('--lx-color-focus: #d97706');
});

test('removes nonessential motion when requested', async () => {
  const css = await readFile(motionPath, 'utf8');
  expect(css).toMatch(/prefers-reduced-motion:\s*reduce/);
  expect(css).toContain('animation-duration: 0.01ms');
});
~~~

Add a local WCAG relative-luminance helper and assert every pair from the LXP04 table: canvas/ink ≥ 7, surface/ink ≥ 7, action/white ≥ 4.5, info ≥ 4.5, confirmed ≥ 4.5, warning ≥ 4.5, danger ≥ 4.5, focus/white ≥ 3 and focus/ink ≥ 3.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/learning-experience-styles.test.ts`

Expected: FAIL because the style files do not exist.

- [ ] **Step 3: Add the exact semantic token layer**

Implement lowercase token values and aliases:

~~~css
:root {
  color-scheme: light;
  --lx-color-canvas: #f7f5f0;
  --lx-color-surface: #ffffff;
  --lx-color-ink: #17212b;
  --lx-color-ink-muted: #4b5967;
  --lx-color-line: #a7b0b8;
  --lx-color-action: #005a70;
  --lx-color-focus: #d97706;
  --lx-color-info-text: #0b3a82;
  --lx-color-info-surface: #eaf2ff;
  --lx-color-confirmed-text: #246b47;
  --lx-color-confirmed-surface: #eaf6ee;
  --lx-color-warning-text: #7a4b00;
  --lx-color-warning-surface: #fff4d6;
  --lx-color-danger-text: #9b1c31;
  --lx-color-danger-surface: #fdecef;
  --lx-font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --lx-space-1: 0.25rem;
  --lx-space-2: 0.5rem;
  --lx-space-3: 0.75rem;
  --lx-space-4: 1rem;
  --lx-space-6: 1.5rem;
  --lx-space-8: 2rem;
  --lx-radius-s: 0.375rem;
  --lx-radius-m: 0.75rem;
  --lx-measure-reading: 70ch;
  --lx-motion-fast: 120ms;
  --lx-motion-standard: 180ms;
}
~~~

In `foundation.css` define body, readable measure, visible `:focus-visible` outline using both focus and ink contrast, minimum 44×44 px control targets, logical properties and container setup. In `patterns.css` use `@container experience (max-width: 39.999rem)`, `(min-width: 40rem) and (max-width: 69.999rem)`, and `(min-width: 70rem)`. No external font or image request.

- [ ] **Step 4: Import the package stylesheet once**

`apps/lernwerk-portal/src/styles/global.css` must import `@ium/learning-experience/styles/index.css` before portal-specific rules. Do not copy tokens into portal CSS.

- [ ] **Step 5: Verify styles and the existing build**

Run:

~~~powershell
npx vitest run tests/platform/learning-experience-styles.test.ts
npm run typecheck
npm run build
~~~

Expected: all PASS; built CSS contains the semantic custom properties exactly once.

- [ ] **Step 6: Commit the foundation**

~~~powershell
git add packages/learning-experience/src/styles apps/lernwerk-portal/src/styles/global.css tests/platform/learning-experience-styles.test.ts
git commit -m "feat(experience): implement calm semantic foundation"
~~~

## Task 4: Build the Shell, Focus, Action and Journey Primitives

**Files:**

- Create: `packages/learning-experience/src/components/ExperienceShell.astro`
- Create: `packages/learning-experience/src/components/ContextBand.astro`
- Create: `packages/learning-experience/src/components/LearningStateHeader.astro`
- Create: `packages/learning-experience/src/components/FocusStage.astro`
- Create: `packages/learning-experience/src/components/ActionEdge.astro`
- Create: `packages/learning-experience/src/components/JourneyMap.astro`
- Create: `packages/learning-experience/src/controllers/focus-stage.ts`
- Test: `tests/platform/learning-experience-components.test.ts`
- Test: `tests/browser/learning-experience-primitives.spec.ts`

- [ ] **Step 1: Write static component-contract tests**

Assert that every component exists and that:

- `ExperienceShell` renders one named context, journey, focus and action slot in that order.
- `FocusStage` has exactly one `main` landmark and programmatic heading reference.
- `ActionEdge` accepts one required primary action and no more than two secondary actions.
- `JourneyMap` uses an ordered list, sets `aria-current="step"` only on the active item and exposes text labels.
- no component uses `tabindex` above zero, inline click handlers, `role="button"` on non-buttons or autonomous focus on initial render.

Run: `npx vitest run tests/platform/learning-experience-components.test.ts`

Expected: FAIL for missing files.

- [ ] **Step 2: Implement typed Astro props and semantic markup**

The focus component contract is:

~~~astro
---
interface Props {
  id: string;
  heading: string;
  purpose?: string;
  focusOnActivation?: boolean;
}
const { id, heading, purpose, focusOnActivation = false } = Astro.props;
---
<main
  class="lx-focus-stage"
  data-lx-focus-stage
  data-focus-on-activation={String(focusOnActivation)}
  aria-labelledby={id + '-heading'}
  tabindex="-1"
>
  <header>
    <h1 id={id + '-heading'}>{heading}</h1>
    {purpose && <p>{purpose}</p>}
  </header>
  <slot />
</main>
~~~

`ActionEdge` uses actual `button type="button"` or `a` depending on an explicit `href`, never a generic clickable container. It renders the primary action first in DOM order and distinguishes secondary actions with text, not color alone.

- [ ] **Step 3: Add focus transfer only for user-triggered stage changes**

Export and test:

~~~ts
export function focusActivatedStage(root: ParentNode = document): void {
  const stage = root.querySelector<HTMLElement>(
    '[data-lx-focus-stage][data-focus-on-activation="true"]',
  );
  if (!stage) return;
  stage.focus({ preventScroll: true });
  stage.scrollIntoView({ block: 'start', behavior: reducedMotion() ? 'auto' : 'smooth' });
}
~~~

The controller must not run on first page load, must tolerate a missing stage, and must honor `prefers-reduced-motion`. The portal controller calls it only after an explicit action changes the active stage.

- [ ] **Step 4: Add browser acceptance tests**

Build a fixture page through the existing fixture mode and verify:

~~~ts
test('keeps one learning focus and moves focus after advance', async ({ page }) => {
  await page.goto('/fixtures/learning-experience');
  await expect(page.getByRole('main')).toHaveCount(1);
  await page.getByRole('button', { name: 'Weiter zur Vermutung' }).click();
  await expect(page.getByRole('main')).toBeFocused();
  await expect(page.getByRole('list', { name: 'Lernweg' })
    .locator('[aria-current="step"]')).toHaveText('Vermutung');
});
~~~

Also test 320 px width, 200% browser zoom, keyboard-only order, no horizontal page scroll and reduced motion.

- [ ] **Step 5: Verify primitives**

Run:

~~~powershell
npx vitest run tests/platform/learning-experience-components.test.ts
npm run build:fixture
npx playwright test tests/browser/learning-experience-primitives.spec.ts --project=chromium
npm run typecheck
~~~

Expected: all PASS.

- [ ] **Step 6: Commit the primitives**

~~~powershell
git add packages/learning-experience/src/components packages/learning-experience/src/controllers tests/platform/learning-experience-components.test.ts tests/browser/learning-experience-primitives.spec.ts
git commit -m "feat(experience): add focused journey primitives"
~~~

## Task 5: Separate Technical Resilience from Learning Feedback

**Files:**

- Create: `packages/learning-experience/src/components/SaveIndicator.astro`
- Create: `packages/learning-experience/src/components/ResilienceNotice.astro`
- Create: `packages/learning-experience/src/components/DataActionDialog.astro`
- Create: `packages/learning-experience/src/components/RecoveryPanel.astro`
- Create: `packages/learning-experience/src/controllers/resilience-adapter.ts`
- Create: `packages/learning-experience/src/controllers/data-action-dialog.ts`
- Modify: `packages/ui-components/src/components/StorageStatus.astro`
- Modify: `packages/ui-components/src/components/ConnectionStatus.astro`
- Modify: `packages/ui-components/src/components/UpdatePrompt.astro`
- Modify: `packages/ui-components/src/components/ErrorSummary.astro`
- Test: `tests/platform/learning-experience-resilience.test.ts`
- Test: `tests/browser/learning-experience-resilience.spec.ts`

- [ ] **Step 1: Define failing state-mapping tests**

Test only semantic platform state, never module content:

~~~ts
type SaveState = 'idle' | 'saving' | 'saved' | 'failed';
type ConnectivityState = 'online' | 'offline';
type RecoveryAction = 'retry' | 'export' | 'reset';

test.each([
  ['saving', 'Wird auf diesem Gerät gespeichert'],
  ['saved', 'Auf diesem Gerät gespeichert'],
  ['failed', 'Speichern nicht möglich'],
])('maps save state %s to durable text', (state, label) => {
  expect(getSaveMessage(state as SaveState)).toBe(label);
});
~~~

Assert that `adaptResilienceState` maps platform facts to exactly `info`, `limit` or `block` plus affected work, preserved state, consequence, safe action and return target. A learning answer must never appear in any live region; `saved` is a polite status while `failed` is an alert only after a user-triggered save.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/learning-experience-resilience.test.ts`

Expected: FAIL because the semantic resilience layer does not exist.

- [ ] **Step 3: Implement the four semantic resilience components**

- `SaveIndicator` accepts only `state` and `messageId`; it renders durable text and a restrained icon marked `aria-hidden="true"`.
- `ResilienceNotice` accepts `kind: 'offline' | 'update' | 'storage'`, a heading and body; it uses `role="status"` only when the transition follows a user action.
- `DataActionDialog` uses native `<dialog>` where available, has labelled title and description, initial focus on the non-destructive cancel button, returns focus to the invoker and requires confirmation for reset/import overwrite.
- `RecoveryPanel` preserves the current work by default and exposes retry, local export and reset as separately named actions.

Do not put technical connectivity notices inside `EvidenceFeedback` or any fachliche feedback component.

`resilience-adapter.ts` is a pure mapping from technical facts to `ResilienceSpec`. It imports neither DOM APIs nor IUM5 types; the portal supplies the affected-work label from validated content.

- [ ] **Step 4: Adapt existing technical components**

Keep `@ium/ui-components` as the source of browser/platform facts. Add neutral data attributes and typed state exports so the portal can inject those facts into the semantic components. Do not move IndexedDB access or service-worker control into `@ium/learning-experience`.

- [ ] **Step 5: Add browser behavior tests**

Cover:

- online → offline exposes one text status without moving focus;
- save failure becomes discoverable and work remains in the form;
- reset dialog starts on “Abbrechen”, Escape cancels, and focus returns to the reset trigger;
- export remains available offline;
- learning correctness is absent from all `[aria-live]` elements.

Run:

~~~powershell
npx vitest run tests/platform/learning-experience-resilience.test.ts
npm run build:fixture
npx playwright test tests/browser/learning-experience-resilience.spec.ts --project=chromium
~~~

Expected: all PASS.

- [ ] **Step 6: Commit resilience semantics**

~~~powershell
git add packages/learning-experience packages/ui-components tests/platform/learning-experience-resilience.test.ts tests/browser/learning-experience-resilience.spec.ts
git commit -m "feat(experience): separate resilience from learning feedback"
~~~

## Task 6: Add and Validate the IUM5 Experience Content Document

**Files:**

- Create: `modules/IUM-5-CORE-05/lernumgebung/experience.json`
- Create: `scripts/validate-experience-content.ts`
- Modify: `schemas/module-manifest.schema.json`
- Modify: `packages/module-contract/src/generated/module-manifest.d.ts`
- Modify: `modules/IUM-5-CORE-05/module.yaml`
- Modify: `scripts/build-module-registry.ts`
- Modify: `apps/lernwerk-portal/src/pages/module/[id].astro`
- Test: `tests/platform/ium5-experience-content.test.ts`
- Test: `tests/fixtures/reference-module/experience.json`

- [ ] **Step 1: Write content-validation tests**

Test that production IUM5 has exactly one `experience.json`, uses `schemaVersion: 1` and `terminologyVersion: 'lxp04-1'`, refers only to existing phase IDs, expresses the three reference situations through start/actions/checkpoints/evidence-card contracts, and has no HTML, scripts, tracking keys or URLs in learner-facing text.

Also create fixture failures for:

- missing file;
- malformed JSON;
- unsupported schema or terminology version;
- unknown phase ID;
- duplicate action ID;
- unknown property;
- body over the code-point limit.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/ium5-experience-content.test.ts`

Expected: FAIL because `experience.json` and validator are missing.

- [ ] **Step 3: Author the closed IUM5 document**

Encode the LXP03/LXP04 content for:

1. `start` with new/resume/reset copy;
2. `actions` for prediction → run → evidence → revision and evidence card → transfer → re-entry recall;
3. `tasks` with goal, thinking action, material, criteria, evidence, social form, persistence, offline and recovery requirements;
4. `feedback` bound to evidence, criterion, interpretation and next check;
5. `checkpoints` at comparison and transfer;
6. `supports` with operation/concept/strategy/example escalation;
7. `evidenceCards` with action-kind-specific required fields;
8. `resilience` wording and data-action confirmations.

Every action carries purpose, prompt, product, criteria, primary/secondary actions, evidence, task/support/checkpoint references, persistence and guarded next states. Tasks link to feedback and recovery. Keep commands, traces, scenario facts and algorithm semantics in `@ium/ium-5-core-05`; `experience.json` supplies labels, learning contracts and explanatory copy only.

- [ ] **Step 4: Wire validation into registry construction**

Add the optional closed manifest property `"experienceContract": { "const": 1 }`, set `experienceContract: 1` only in `modules/IUM-5-CORE-05/module.yaml` for this slice, and run `npm run contracts:generate` so `module-manifest.d.ts` is regenerated from the schema. Modules without that declaration keep their current build path and do not need an empty experience document.

Export:

~~~ts
export async function readExperienceContent(
  moduleDirectory: string,
): Promise<ExperienceContentV1>;
~~~

Call it during registry generation for every production module that declares `experienceContract: 1`. On failure, print every contract error with module-relative file path and JSON path, then exit non-zero. Pass the parsed content as Astro props from `[id].astro`; do not re-read files in client JavaScript.

- [ ] **Step 5: Verify content and builds**

Run:

~~~powershell
npx vitest run tests/platform/ium5-experience-content.test.ts
npm run registry:production
npm run registry:fixture
npm run contracts:check
npm run build
npm run typecheck
~~~

Expected: all PASS; invalid fixtures fail only inside their explicit test assertions.

- [ ] **Step 6: Commit the production contract**

~~~powershell
git add modules/IUM-5-CORE-05/lernumgebung/experience.json modules/IUM-5-CORE-05/module.yaml tests/fixtures/reference-module/experience.json schemas/module-manifest.schema.json packages/module-contract/src/generated/module-manifest.d.ts scripts/validate-experience-content.ts scripts/build-module-registry.ts apps/lernwerk-portal/src/pages/module/[id].astro tests/platform/ium5-experience-content.test.ts
git commit -m "feat(ium5): add validated experience content"
~~~

## Task 7: Introduce an IUM5 Experience Adapter without Changing Core Semantics

**Files:**

- Create: `apps/lernwerk-portal/src/controllers/algorithm-workbench/experience-adapter.ts`
- Create: `apps/lernwerk-portal/src/controllers/algorithm-workbench/experience-state.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Test: `tests/platform/ium5-experience-adapter.test.ts`

- [ ] **Step 1: Write adapter truth-table tests**

Map existing core payload facts to presentation state:

| Core fact | Experience stage |
|---|---|
| no initial algorithm | `start` |
| algorithm, no prediction | `prediction` |
| prediction, no trace | `run` |
| trace, no repair hypothesis | `evidence` |
| repair hypothesis, no revised algorithm | `revision` |
| revised algorithm, incomplete transfer | `transfer` |
| transfer complete | `reentry` |

Add separate cases for stored resume data, unavailable persistence, validation failure and import recovery. Assert the adapter does not mutate the payload.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/ium5-experience-adapter.test.ts`

Expected: FAIL for missing adapter exports.

- [ ] **Step 3: Implement a closed presentation state**

~~~ts
export type ExperienceStage =
  | 'start'
  | 'prediction'
  | 'run'
  | 'evidence'
  | 'revision'
  | 'transfer'
  | 'reentry';

export interface Ium5ExperienceState {
  readonly stage: ExperienceStage;
  readonly canResume: boolean;
  readonly saveState: 'idle' | 'saving' | 'saved' | 'failed';
  readonly connectivity: 'online' | 'offline';
  readonly recovery: 'none' | 'validation' | 'storage' | 'import';
}
~~~

`deriveIum5ExperienceState` is pure. Browser facts enter through parameters, not global reads. Persisted fields stay owned by `projectPersistentPayload`. Do not add a duplicated stage field to the payload; derive it from existing work.

- [ ] **Step 4: Reduce the mega-component by composition**

Keep `AlgorithmWorkbench.astro` as the IUM5 composition root, but replace hand-built shell, state banners and navigation with `ExperienceShell`, `JourneyMap`, `FocusStage` and `ActionEdge`. Move no domain calculation into Astro markup. Retain stable `data-*` hooks required by the controller until the matching browser tests migrate.

- [ ] **Step 5: Connect stage activation**

The controller:

1. reads action intent from an actual button;
2. invokes the existing core transition;
3. re-derives `Ium5ExperienceState`;
4. renders via `workbench-view.ts`;
5. calls `focusActivatedStage` only if the user action changed `stage`;
6. announces only save/connectivity/error state, never the learning result.

- [ ] **Step 6: Verify no payload or boundary regression**

Run:

~~~powershell
npx vitest run tests/platform/ium5-experience-adapter.test.ts tests/platform/ium5-payload.test.ts tests/platform/boundaries.test.ts
npm run typecheck
npm run test:ium5:state
~~~

Expected: all PASS; the allowed persistent payload key set is unchanged.

- [ ] **Step 7: Commit the adapter seam**

~~~powershell
git add apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/controllers/algorithm-workbench tests/platform/ium5-experience-adapter.test.ts
git commit -m "refactor(ium5): add semantic experience adapter"
~~~

## Task 8: Implement Reference Situation 1 — Start and Resume

**Files:**

- Create: `packages/learning-experience/src/components/StartBoard.astro`
- Create: `packages/learning-experience/src/components/ResumePrompt.astro`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/styles/algorithm-workbench.css`
- Test: `tests/browser/ium5-start-resume.spec.ts`

- [ ] **Step 1: Add failing learner-flow tests**

Cover both clean and stored starts:

~~~ts
test('starts with purpose and one primary action', async ({ page }) => {
  await page.goto('/module/ium-informatik-5');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText(
    'Algorithmen untersuchen',
  );
  await expect(page.getByRole('button', {
    name: 'Mit der Vermutung beginnen',
  })).toHaveCount(1);
  await expect(page.getByRole('main').getByRole('button')).toHaveCount(1);
});

test('offers resume before reset without exposing stored answers', async ({ page }) => {
  await seedIum5State(page);
  await page.goto('/module/ium-informatik-5');
  await expect(page.getByRole('button', { name: 'Weiterarbeiten' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Neu beginnen' })).toBeVisible();
  await expect(page.getByText('3 Versuche')).toHaveCount(0);
});
~~~

Also test that “Neu beginnen” opens the confirmation dialog, cancel preserves data, confirmation clears only the selected module record, and keyboard focus returns predictably.

- [ ] **Step 2: Confirm red**

Run: `npx playwright test tests/browser/ium5-start-resume.spec.ts --config playwright.ium5.config.mts --project=chromium`

Expected: FAIL because current IUM5 renders the old full workbench immediately.

- [ ] **Step 3: Implement start and resume patterns**

`StartBoard` displays context, purpose and exactly one primary action. `ResumePrompt` displays the last meaningful learning stage in words, not a percentage, timestamp, attempt count or score. Its primary action is “Weiterarbeiten”; “Neu beginnen” is secondary and routes through `DataActionDialog`.

At compact width, place actions in one vertical reading order; at wide width, keep content measure ≤ 70ch and do not turn the start into a dashboard.

- [ ] **Step 4: Preserve local-first behavior**

Read existing module state only via the current `@ium/local-state` port. A missing database, denied storage or invalid record must lead to start plus `RecoveryPanel`, never a blank page. No network is required for either path.

- [ ] **Step 5: Verify the reference situation**

Run:

~~~powershell
npx playwright test tests/browser/ium5-start-resume.spec.ts --config playwright.ium5.config.mts --project=chromium
npm run test:ium5:state
npm run test:ium5:offline
~~~

Expected: all PASS.

- [ ] **Step 6: Commit start and resume**

~~~powershell
git add packages/learning-experience/src/components/StartBoard.astro packages/learning-experience/src/components/ResumePrompt.astro apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/controllers/algorithm-workbench apps/lernwerk-portal/src/styles/algorithm-workbench.css tests/browser/ium5-start-resume.spec.ts
git commit -m "feat(ium5): implement focused start and resume"
~~~

## Task 9: Implement Reference Situation 2 — Prediction, Evidence and Revision

**Files:**

- Create: `packages/learning-experience/src/components/PredictionForm.astro`
- Create: `packages/learning-experience/src/components/SemanticModelView.astro`
- Create: `packages/learning-experience/src/components/EvidenceView.astro`
- Create: `packages/learning-experience/src/components/EvidenceFeedback.astro`
- Create: `packages/learning-experience/src/components/RevisionCompare.astro`
- Create: `packages/learning-experience/src/components/SupportDisclosure.astro`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `apps/lernwerk-portal/src/styles/algorithm-workbench.css`
- Test: `tests/browser/ium5-evidence-revision.spec.ts`
- Test: `tests/platform/learning-feedback-contract.test.ts`

- [ ] **Step 1: Add a failing learning-feedback contract test**

Assert that feedback always contains:

~~~ts
export interface FeedbackSpec {
  readonly id: string;
  readonly result: string;
  readonly evidenceRef: string;
  readonly criterion: string;
  readonly interpretationPrompt: string;
  readonly nextCheck: string;
  readonly strategySupportId: string | null;
  readonly exampleSupportId: string | null;
}
~~~

Reject labels such as “Richtig”, “Falsch” or a bare score when the result lacks criterion, evidence reference, interpretation prompt or next check. Enforce unique IDs linking feedback to visible trace evidence and existing support IDs.

- [ ] **Step 2: Add failing browser tests for the complete cycle**

The tests must show that a keyboard-only learner can:

1. construct an initial algorithm;
2. state a prediction before execution;
3. run the model;
4. inspect trace evidence;
5. receive descriptive evidence feedback;
6. formulate a repair hypothesis;
7. compare original and revision;
8. execute the revision.

Verify that execution is blocked until a prediction exists, focus moves once per stage, the current evidence row has text plus `aria-current`, and the revision comparison has explicit “Vorher”/“Nachher” headings rather than relying on columns.

- [ ] **Step 3: Confirm red**

Run:

~~~powershell
npx vitest run tests/platform/learning-feedback-contract.test.ts
npx playwright test tests/browser/ium5-evidence-revision.spec.ts --config playwright.ium5.config.mts --project=chromium
~~~

Expected: both FAIL on missing semantic components/behavior.

- [ ] **Step 4: Implement the six patterns**

- `PredictionForm` uses a `fieldset` and `legend`, visible labels, inline validation connected by `aria-describedby`, and preserves invalid input.
- `SemanticModelView` exposes the model state as a structured text summary in addition to the visual grid; decorative direction glyphs are hidden from assistive tech.
- `EvidenceView` renders the trace as an ordered list or table according to semantic data; each entry names step, command, before, after and outcome.
- `EvidenceFeedback` explains what was observed, points to evidence and presents one next action. It has no technical save/connectivity status.
- `RevisionCompare` serializes original and revised algorithms as two labelled regions in source order, with a concise change summary before the regions.
- `SupportDisclosure` renders operation, concept, strategy and example as explicit escalation levels. Opening is user-controlled, closing returns focus to the trigger, and `preservesAction` remains visible so help never silently takes over the core task.

Keep the existing core interpreter and trace types authoritative. Components receive already-computed domain facts and never recalculate movement, loop behavior or mission success.

- [ ] **Step 5: Make the action graph explicit**

In the controller, reject impossible action order even if a crafted DOM event tries to skip stages. Use the current core validation result as the authority. Show a durable error summary linked to the invalid field; do not silently coerce.

- [ ] **Step 6: Verify the core learning cycle**

Run:

~~~powershell
npx vitest run tests/platform/learning-feedback-contract.test.ts tests/platform/ium5-interpreter.test.ts tests/platform/ium5-editor.test.ts
npx playwright test tests/browser/ium5-evidence-revision.spec.ts --config playwright.ium5.config.mts --project=chromium
npm run test:ium5:accessibility
npm run typecheck
~~~

Expected: all PASS and no existing interpreter/editor expectation changes.

- [ ] **Step 7: Commit evidence-led feedback**

~~~powershell
git add packages/learning-experience/src/components apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/controllers/algorithm-workbench apps/lernwerk-portal/src/styles/algorithm-workbench.css tests/platform/learning-feedback-contract.test.ts tests/browser/ium5-evidence-revision.spec.ts
git commit -m "feat(ium5): implement evidence-led revision cycle"
~~~

## Task 10: Implement Reference Situation 3 — Evidence Card, Transfer and Re-entry

**Files:**

- Create: `packages/learning-experience/src/components/EvidenceCardComposer.astro`
- Create: `packages/learning-experience/src/components/TransferPrompt.astro`
- Create: `packages/learning-experience/src/components/ReentryRecall.astro`
- Modify: `packages/learning-experience/src/contracts.ts`
- Modify: `packages/learning-experience/src/validation.ts`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-controller.ts`
- Modify: `apps/lernwerk-portal/src/controllers/algorithm-workbench/workbench-view.ts`
- Modify: `packages/ium-5-core-05/src/payload.ts`
- Modify: `packages/ium-5-core-05/src/index.ts`
- Test: `tests/platform/ium5-payload.test.ts`
- Test: `tests/browser/ium5-transfer-reentry.spec.ts`

- [ ] **Step 1: Add a failing minimal-evidence-card payload test**

Extend the closed payload with one field only:

~~~ts
export interface EvidenceCardPayload {
  readonly sourceRef: string;
  readonly evidenceRef: string;
  readonly interpretation: string;
  readonly revision: string;
  readonly keyStatement: string;
  readonly modelBoundary: string;
}
~~~

Test:

- all six values required after card submission;
- 500 Unicode code points per value;
- unknown nested keys rejected;
- raw execution trace, timestamps, user identity and interaction metrics excluded;
- `projectPersistentPayload` returns a deep copy;
- payload without `evidenceCard` migrates to `null` deterministically.

Update the exact allowed-key assertion in `ium5-payload.test.ts`. Do not add a separate progress percentage or re-entry score.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/ium5-payload.test.ts`

Expected: FAIL because `evidenceCard` is not part of the current closed contract.

- [ ] **Step 3: Implement the narrow payload migration**

Add `evidenceCard: EvidenceCardPayload | null` to the initial payload, parser and projection. References identify the authoritative source/trace rather than copying it; interpretation, revision, key statement and model boundary retain the learner’s minimal evidence product. The parser accepts the previous stored schema only through an explicit version-aware migration at the local-state adapter boundary; it must still reject arbitrary future fields. Increment the module payload schema version through the existing module contract mechanism and add a fixture for the prior version.

- [ ] **Step 4: Implement the three semantic patterns**

- `EvidenceCardComposer` exposes source and evidence selection first, then four visible labelled textareas: Deutung, Überarbeitung, Kernaussage und Modellgrenze. It displays character limits before overflow and preserves entries after validation.
- `TransferPrompt` presents the existing closed transfer cases one at a time, requires a classification and rationale, and connects the result to the evidence card.
- `ReentryRecall` begins with a free recall prompt derived from the previous card’s key statement, followed by self-comparison. It does not reveal the stored answer until the learner chooses “Mit meiner Belegkarte vergleichen”.

No component stores data itself. The controller submits through the IUM5 payload and local-state port.

- [ ] **Step 5: Add the end-to-end browser test**

Test an offline-capable flow from completed revision through card, one transfer classification, simulated reload and re-entry recall. Assert:

- only the minimal card persists;
- recall appears before the stored answer;
- export/import preserves the card;
- reset removes the card;
- no personal data or interaction metric enters IndexedDB/export;
- 320 px and 200% zoom remain operable.

- [ ] **Step 6: Verify persistence and transfer**

Run:

~~~powershell
npx vitest run tests/platform/ium5-payload.test.ts tests/platform/export-import.test.ts tests/platform/local-state.test.ts
npx playwright test tests/browser/ium5-transfer-reentry.spec.ts --config playwright.ium5.config.mts --project=chromium
npm run test:ium5:offline
npm run typecheck
~~~

Expected: all PASS.

- [ ] **Step 7: Commit minimal evidence persistence**

~~~powershell
git add packages/learning-experience/src packages/ium-5-core-05/src apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro apps/lernwerk-portal/src/controllers/algorithm-workbench tests/platform/ium5-payload.test.ts tests/browser/ium5-transfer-reentry.spec.ts
git commit -m "feat(ium5): persist minimal evidence card and reentry"
~~~

## Task 11: Implement Teacher Orchestration and Shared Holds

**Files:**

- Create: `packages/learning-experience/src/components/TeacherCheckpoint.astro`
- Create: `packages/learning-experience/src/components/RoleExchange.astro`
- Create: `packages/learning-experience/src/components/SharedHold.astro`
- Modify: `apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro`
- Modify: `modules/IUM-5-CORE-05/lernumgebung/experience.json`
- Modify: `modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md`
- Test: `tests/platform/ium5-teacher-orchestration.test.ts`
- Test: `tests/browser/ium5-teacher-orchestration.spec.ts`

- [ ] **Step 1: Write checkpoint contract tests**

For each checkpoint, require:

~~~ts
export interface TeacherCheckpointSpec {
  readonly id: string;
  readonly state: LearningStateId;
  readonly purpose: string;
  readonly timeWindowMinutes: readonly [number, number];
  readonly socialForm: 'individual' | 'pair' | 'group' | 'plenary';
  readonly learnerSignal: string;
  readonly ordinaryEvidence: readonly string[];
  readonly teacherPrompt: string;
  readonly neutralFallback: string;
  readonly returnState: LearningStateId;
  readonly exitCriterion: string;
}
~~~

Assert that a checkpoint has no remote lock, teacher account, hidden dashboard, countdown or automatic data transmission. `neutralFallback` must explain how instruction proceeds without private device state or a shared stop, and `returnState` must be an allowed LXP02 state.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/ium5-teacher-orchestration.test.ts`

Expected: FAIL because teacher patterns are missing.

- [ ] **Step 3: Implement local orchestration patterns**

`TeacherCheckpoint` is a locally rendered pause card, not an authorization system. `RoleExchange` names two roles (“Erklären” and “Prüfen”), the exchange prompt and a visible swap action. `SharedHold` allows “Gemeinsam besprechen” and “Ohne gemeinsame Besprechung fortfahren”; neither path loses work.

Store no checkpoint telemetry. If a learner continues independently, derive the stage from their learning payload and do not add a persisted “teacher bypass” field.

- [ ] **Step 4: Align the teacher handbook**

Add a section that names:

- the two checkpoint triggers;
- the purpose and suggested 2–4 minute exchange;
- a screen-reader/keyboard-compatible facilitation option;
- the independent continuation path;
- the boundary that no learner monitoring or remote control exists;
- how to use the evidence card for formative dialogue without collecting identities.

- [ ] **Step 5: Add browser tests**

Verify checkpoint text and choices, role swap keyboard behavior, no request to an analytics/network endpoint, continued offline operation and unchanged persistence after either release path.

Run:

~~~powershell
npx vitest run tests/platform/ium5-teacher-orchestration.test.ts
npx playwright test tests/browser/ium5-teacher-orchestration.spec.ts --config playwright.ium5.config.mts --project=chromium
npm run test:ium5:offline
~~~

Expected: all PASS.

- [ ] **Step 6: Commit teacher orchestration**

~~~powershell
git add packages/learning-experience/src/components modules/IUM-5-CORE-05/lernumgebung/experience.json modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro tests/platform/ium5-teacher-orchestration.test.ts tests/browser/ium5-teacher-orchestration.spec.ts
git commit -m "feat(ium5): add local teacher orchestration"
~~~

## Task 12: Enforce Accessibility, Portability and Production Gates

**Files:**

- Create: `scripts/verify-learning-experience.ts`
- Create: `tests/platform/learning-experience-production.test.ts`
- Create: `tests/browser/ium5-learning-experience-accessibility.spec.ts`
- Create: `tests/browser/ium5-learning-experience-portability.spec.ts`
- Modify: `package.json`
- Modify: `scripts/verify-ium5.ts`
- Modify: `docs/quality/ium5-acceptance-matrix.md`
- Modify: `docs/architecture/systemgrenzen.md`
- Modify: `docs/architecture/lokale-datenhaltung-und-resilienz.md`
- Modify: `README.md`

- [ ] **Step 1: Add failing production-gate tests**

The production test must fail unless:

- every `experience.json` validates;
- all referenced component contracts exist;
- every semantic color pair meets its required ratio;
- package boundaries remain directed;
- no external font/image URL appears in the experience package;
- no forbidden analytics/personal-data key appears in content, payload or export;
- every reference situation has a Playwright test;
- the documentation records contract version, migration rule and non-generalizations.

- [ ] **Step 2: Confirm red**

Run: `npx vitest run tests/platform/learning-experience-production.test.ts`

Expected: FAIL because the verifier and documentation entries are missing.

- [ ] **Step 3: Implement the verifier and npm script**

Export a callable function for Vitest and a CLI entry:

~~~ts
export interface ExperienceVerificationReport {
  readonly ok: boolean;
  readonly checks: readonly {
    readonly id: string;
    readonly ok: boolean;
    readonly detail: string;
  }[];
}

export async function verifyLearningExperience(
  rootDir: string,
): Promise<ExperienceVerificationReport>;
~~~

Add `"verify:experience": "tsx scripts/verify-learning-experience.ts"`. Make `verify-ium5.ts` call the verifier and surface its failed check IDs, while keeping the new script independently runnable.

- [ ] **Step 4: Add comprehensive accessibility tests**

Use axe plus behavioral assertions across clean start, resume, prediction, evidence, revision, transfer, re-entry, offline, validation error and recovery. Test Chromium keyboard behavior and the existing configured browser matrix where stable. Required assertions:

- one main landmark and ordered headings;
- all controls have accessible names;
- errors link to fields and focus the error summary only after submit;
- dialogs trap and restore focus;
- `aria-current` occurs exactly once in an active journey;
- no positive `tabindex`;
- no keyboard trap;
- 320 CSS px width and 200% zoom without loss of action;
- forced-colors retains visible focus and state;
- reduced motion removes scroll animation;
- visual model has equivalent structured text;
- status regions exclude learning answers.

- [ ] **Step 5: Add portability tests**

Render the package fixture without `@ium/ium-5-core-05` and render an IUM5 page with a fake semantic component adapter. Assert that:

- generic package code contains no IUM5 phase, command or scenario IDs;
- the IUM5 core imports no Astro/DOM/experience package;
- `experience.json` can be parsed independently;
- StartBoard, FocusStage, ActionEdge, EvidenceFeedback and RecoveryPanel render with non-IUM5 fixture content;
- module-specific trace and editor views remain injected by the portal composition root.

- [ ] **Step 6: Update architectural and acceptance documentation**

Record:

- `@ium/learning-experience` ownership and dependency direction;
- version 1 content and component contracts;
- IndexedDB-only persistence and the evidence-card migration;
- distinction between learning feedback and technical resilience;
- all three reference situations;
- explicit non-generalizations: IUM5 grid/editor, command catalog, trace semantics, scenario IDs, fachliche language, teacher checkpoint placement;
- acceptance evidence with exact test/command names.

- [ ] **Step 7: Run the full quality ladder**

Run in this order and stop on the first failure:

~~~powershell
npm run contracts:check
npm run boundaries:check
npm run typecheck
npm run test:platform
npm run test:python
npm run build
npm run test:browser
npm run test:accessibility
npm run test:offline
npm run test:ium5:browser
npm run test:ium5:state
npm run test:ium5:accessibility
npm run test:ium5:offline
npm run verify:experience
npm run verify:ium5
~~~

Expected:

- TypeScript/Astro/build commands exit 0.
- Platform and Python suites report 0 failed.
- All browser suites report 0 failed.
- `verify:experience` and `verify:ium5` end with an explicit PASS summary.

- [ ] **Step 8: Inspect generated output without committing it**

Run:

~~~powershell
git status --short
git diff --check
rg -n "https?://|analytics|attemptCount|elapsedMs|clicks|hintUsage|playbackSpeed" packages/learning-experience modules/IUM-5-CORE-05/lernumgebung/experience.json
~~~

Expected: no build artifact is tracked; `git diff --check` is silent; the final search finds no external asset/analytics/metric violation. Legitimate prohibition tests may contain the forbidden test strings and must be reviewed rather than deleted.

- [ ] **Step 9: Commit production gates**

~~~powershell
git add package.json package-lock.json scripts/verify-learning-experience.ts scripts/verify-ium5.ts tests/platform/learning-experience-production.test.ts tests/browser/ium5-learning-experience-accessibility.spec.ts tests/browser/ium5-learning-experience-portability.spec.ts docs README.md
git commit -m "test(experience): enforce production quality gates"
~~~

## Task 13: Review the Completed Implementation and Prepare the Approval Handoff

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-design-system.md`
- Modify: `docs/superpowers/plans/2026-08-05-ium-lxp04-design-system-implementation.md`
- Create: `docs/quality/ium-learning-experience-implementation-report.md`

- [ ] **Step 1: Re-read LXP04 and trace every normative contract**

Create a report table with one row for every LXP04 acceptance area: architecture, visual foundation, responsive behavior, interaction, content, feedback, accessibility, resilience, persistence, teacher orchestration, portability and production. Each row names implementation files, automated evidence, manual observation if any and residual uncertainty.

- [ ] **Step 2: Run focused diff and history review**

~~~powershell
git diff main...HEAD --stat
git diff main...HEAD -- packages/learning-experience apps/lernwerk-portal packages/ium-5-core-05 modules/IUM-5-CORE-05
git log --oneline main..HEAD
git status --short --branch
~~~

Expected: only LXP05-scoped product, content, tests and documentation changes; clean worktree after the report commit; no merge, generated artifact or unrelated Vault file.

- [ ] **Step 3: Run the full quality ladder once more**

Repeat Task 12 Step 7 from a clean checkout. Record exact counts and command exits in the implementation report. A stale earlier run is not sufficient for completion.

- [ ] **Step 4: Commit the implementation report**

~~~powershell
git add docs/quality/ium-learning-experience-implementation-report.md docs/superpowers/specs/2026-08-05-ium-learning-experience-design-system.md docs/superpowers/plans/2026-08-05-ium-lxp04-design-system-implementation.md
git commit -m "docs(experience): record implementation evidence"
~~~

- [ ] **Step 5: Stop at the LXP05 review gate**

Do not merge, push, open a pull request, deploy a preview or begin device/pilot work. Present:

- branch and commit hash;
- changed-file summary;
- complete verification results;
- LXP04 traceability report;
- remaining risks and manual observations;
- exact approval choices for the next gate.

## Completion Definition

The implementation represented by this plan is complete only when:

1. all 13 tasks and every checkbox are complete;
2. `@ium/learning-experience` remains independent of IUM5 core semantics;
3. the three reference situations pass keyboard, accessibility, state and offline tests;
4. minimal evidence-card persistence is versioned and migration-tested;
5. teacher orchestration works locally without accounts, remote locks or telemetry;
6. every production verifier and existing regression suite passes from a clean worktree;
7. documentation contains exact evidence and non-generalizations;
8. the implementation is presented at its explicit review gate without unauthorized merge, push, preview, device, pilot, LMS or release work.

## Explicit Non-Goals

- No generalized visual page builder or arbitrary schema renderer.
- No learning analytics, attempt tracking, scoring dashboard or personal profile.
- No remote teacher control, shared real-time session or account system.
- No replacement of `@ium/ium-5-core-05` domain rules with component logic.
- No migration of the IUM5 grid/editor, command catalog, trace model, scenario IDs or fachliche content into the generic package.
- No preview deployment, real-device evidence, pilot, LMS integration or release decision inside this plan.
