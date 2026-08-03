# IuM Export Sensitivity Notice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the approved visible, screenreader-associated export sensitivity notice without changing the direct local export flow.

**Architecture:** The existing static `FixtureWorkspace.astro` receives one visible paragraph with a stable ID, and the existing export button references it through `aria-describedby`. No controller, storage, serialization, network or dialog behavior changes. A real-browser accessibility test protects the user-visible and programmatic relationship.

**Tech Stack:** Astro 7.1.6, TypeScript, Playwright, Vitest, GitHub Actions, GitHub Pages

## Global Constraints

- Use the exact approved text: `Exportdateien können Freitext oder Lernprodukte enthalten. Prüfe sie vor dem Teilen und veröffentliche sie nicht ungeprüft.`
- Keep the export a direct action without a confirmation dialog.
- Do not change serialization, file naming, download, copy fallback, storage, import, telemetry, network or privacy behavior.
- Keep `device-verified: not-run` until the real iPad retest and every other mandatory target configuration are complete.
- Execute sequentially without subagents.

---

### Task 1: Visible and programmatically associated export notice

**Files:**
- Modify: `tests/browser/accessibility.spec.ts`
- Modify: `apps/lernwerk-portal/src/components/FixtureWorkspace.astro`

**Interfaces:**
- Consumes: existing `Exportieren` button selected by accessible role and name.
- Produces: visible paragraph `#export-sensitivity-hint` and `aria-describedby="export-sensitivity-hint"` on the export button.

- [ ] **Step 1: Write the failing browser test**

Append this test to `tests/browser/accessibility.spec.ts`:

```ts
test('export notice is visible and programmatically describes the direct action', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  const notice = page.locator('#export-sensitivity-hint');
  await expect(notice).toHaveText(
    'Exportdateien können Freitext oder Lernprodukte enthalten. Prüfe sie vor dem Teilen und veröffentliche sie nicht ungeprüft.',
  );
  await expect(notice).toBeVisible();
  await expect(page.getByRole('button', { name: 'Exportieren' })).toHaveAttribute(
    'aria-describedby',
    'export-sensitivity-hint',
  );
});
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```powershell
npx playwright test tests/browser/accessibility.spec.ts --project=chromium --grep "export notice"
```

Expected: FAIL because `#export-sensitivity-hint` does not exist.

- [ ] **Step 3: Add the minimal static markup**

In `FixtureWorkspace.astro`, place this paragraph immediately before the actions and associate only the export button:

```astro
<p id="export-sensitivity-hint">
  Exportdateien können Freitext oder Lernprodukte enthalten. Prüfe sie vor dem Teilen und
  veröffentliche sie nicht ungeprüft.
</p>
<div class="actions">
  <button type="button" aria-describedby="export-sensitivity-hint" data-fixture-export>
    Exportieren
  </button>
```

Leave the remaining actions and closing markup unchanged.

- [ ] **Step 4: Verify GREEN and existing direct export**

Run:

```powershell
npx playwright test tests/browser/accessibility.spec.ts --project=chromium --grep "export notice"
npx playwright test tests/browser/platform.spec.ts --grep "edit, reload, export"
```

Expected: the new test passes; the existing Chromium, Firefox and WebKit export flow still downloads directly and remains lossless.

- [ ] **Step 5: Run the complete Phase-1 verification**

Run:

```powershell
npm run verify:phase1
```

Expected: all 19 verification steps pass, including platform, browser, offline, accessibility and Python suites.

- [ ] **Step 6: Commit and publish**

Before commit and push, run `git fetch --prune` and `git pull --ff-only`. Commit the plan, test and component change, push `main`, and require all four GitHub-CI jobs to pass. Then dispatch the manual Pages workflow with:

```powershell
gh workflow run device-fixture-pages.yml --repo H4R7W16/ium-lernwerk --ref main `
  -f build_revision=device-export-notice-2026-08-03-1 `
  -f candidate_mode=valid
```

Expected: Pages build and deploy pass; the published module HTML contains the exact notice and association.

- [ ] **Step 7: Close only after the real-device retest**

On the managed iPad, activate the valid update, confirm that the notice is visible and announced with the export button in VoiceOver, and confirm that export still downloads directly. Record only the observed result; close the export checkbox only after this succeeds.
