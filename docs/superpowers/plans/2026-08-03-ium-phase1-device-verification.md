# IuM Phase 1 Device Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to execute this plan task-by-task. The project rescue decision requires sequential inline execution without subagents.

**Goal:** Verify the implemented Phase-1 platform on a real managed school iPad and the named managed desktop/browser matrix, with dated configuration evidence and no learner data.

**Architecture:** A committed synthetic fixture build is served from an explicitly approved HTTPS origin. Each real target configuration gets its own immutable evidence record copied from `docs/platform/device-verification.md`; automated CI remains supporting evidence only. The final evaluator changes `device-verified` only after every mandatory target passes or an owner explicitly accepts a documented limitation.

**Tech Stack:** Astro 7.1.6 static build, vite-plugin-pwa 1.3.0, Workbox 7.4.1, GitHub Actions, managed iPadOS/Safari/VoiceOver, managed desktop Chromium/Firefox and the school LMS.

## Global Constraints

- Do not use real learner data, names, accounts, identifiers or free text from teaching.
- Do not infer Safari or iPad behavior from Playwright WebKit.
- Do not expose the fixture over plain LAN HTTP; service-worker evidence requires an approved trusted HTTPS origin.
- Do not enable GitHub Pages, a tunnel, a hosting provider or an MDM change without explicit owner approval.
- Keep `device-verified: not-run` until every mandatory target configuration has a complete evidence record.
- Keep Phase 2 and `IUM-5-CORE-05` blocked until the device gate is passed.
- Execute sequentially without subagents.

---

### Task 1: Seal the preflight and target matrix

**Files:**
- Read: `docs/platform/device-verification.md`
- Read: `docs/platform/implementation-report.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Tasks/2026-08-03 - IUM14 Phase 1 Realgerätegate durchführen.md`

**Interfaces:**
- Consumes: technical status `implemented`, final GitHub CI evidence, managed-device access and an approved HTTPS-origin decision.
- Produces: a dated target matrix with one row per mandatory configuration and an explicit execution owner.

- [ ] **Step 1: Confirm the repository baseline**

Run:

```powershell
git status --short --branch
git fetch --prune
git pull --ff-only origin main
git rev-parse HEAD
gh run view 30779774911 --json status,conclusion,headSha,url
```

Expected: clean `main`, local and remote head equal, and CI run `30779774911` completed with `success`.

- [ ] **Step 2: Record the real target configurations**

For each configuration, record exact device model, OS version, browser version, MDM profile, Web-Clip policy, storage/retention policy, content-filter or proxy policy, network and LMS. Mandatory configurations are:

1. managed school iPad with Safari and VoiceOver;
2. managed desktop with current school-supported Chromium;
3. managed desktop with current school-supported Firefox;
4. the school LMS iframe or external-tab path.

Expected: every value comes from the real target or its management console; no value is inferred from CI.

- [ ] **Step 3: Confirm an approved trusted HTTPS origin**

Accept exactly one written choice:

1. an existing institutionally approved HTTPS static host; or
2. GitHub Pages for the synthetic fixture, explicitly authorized as a temporary device-test publication.

Expected: the chosen origin is documented in IUM14. If neither is authorized, stop with status `blocked` and leave `device-verified: not-run`.

### Task 2: Publish a reproducible synthetic device-test build

**Files:**
- Read: `package.json`
- Read: `scripts/build-portal.ts`
- Read: `scripts/check-build-output.ts`
- Create only after hosting approval: hosting-specific workflow or deployment configuration named in the written approval
- Create during execution: one date-derived `managed-ipad-primary.md` record under `docs/platform/device-verification-runs/`, using the exact PowerShell derivation in Step 3

**Interfaces:**
- Consumes: approved HTTPS origin, clean `main`, fixture profile and exact commit SHA.
- Produces: immutable HTTPS test URL, build SHA and initial evidence record.

- [ ] **Step 1: Rebuild and verify the exact candidate**

Run:

```powershell
npm ci
npm run verify:phase1
npm run build:fixture:subpath
```

Expected: 19/19 verification steps pass and `apps/lernwerk-portal/dist/sw.js` contains no `self.__WB_MANIFEST` marker.

- [ ] **Step 2: Publish only through the approved path**

The publication must serve the committed fixture build at one stable HTTPS base path and must not add analytics, accounts, telemetry, third-party runtime assets or real data.

Expected: the iPad reports a secure page; the service worker scope equals the published base path; the tested URL and commit SHA are recorded.

- [ ] **Step 3: Create the configuration evidence record**

On the execution date, copy `docs/platform/device-verification.md` to a filename derived as follows:

```powershell
$runDate = Get-Date -Format 'yyyy-MM-dd'
$runPath = "docs/platform/device-verification-runs/$runDate-managed-ipad-primary.md"
```

Fill only facts observed on the real configuration. Store privacy-reviewed screenshots or exported network logs outside the repository if they contain local policy details; link them by an approved evidence path.

### Task 3: Execute managed iPad, Safari and VoiceOver checks

**Files:**
- Modify: the dated managed-iPad evidence record from Task 2

**Interfaces:**
- Consumes: approved HTTPS fixture URL and the configured managed iPad.
- Produces: real Safari, PWA, storage, offline, update, touch and VoiceOver evidence.

- [ ] **Step 1: Verify first online use and network locality**

Open portal, fixture module and data page in Safari. Inspect the available network log or filter log for unexpected third-party runtime requests.

Expected: all runtime requests stay on the approved origin; portal and fixture load without silent policy failures.

- [ ] **Step 2: Verify Local First and transfer controls**

Enter the synthetic text `IUM Geräteprobe`, reload, export, delete, import the same export, then perform global deletion. Repeat with explicitly selected volatile mode.

Expected: confirmed persistent state survives reload; valid import is lossless; deletion requires confirmation; volatile state is absent after a fresh session; no real personal data is used.

- [ ] **Step 3: Verify offline and controlled update behavior**

After a confirmed online installation, disconnect network access and reload portal, module and an uncached route. Reconnect, publish or select the approved candidate update, enter synthetic state and confirm the update.

Expected: cached routes and offline fallback work; first uncached offline behavior is documented; update prompt appears; state survives the confirmed update; a broken candidate leaves the previous active version usable.

- [ ] **Step 4: Verify Web Clip or PWA installation**

Install using the target Web-Clip/PWA policy and launch from the managed home-screen entry.

Expected: start URL and scope match the approved base path; no navigation escapes or policy block is silent.

- [ ] **Step 5: Verify VoiceOver and touch**

With VoiceOver active, traverse landmarks, headings, save status, error summary, fields, dialogs and buttons. Complete save, rejected import, import confirmation and delete confirmation using touch exploration and VoiceOver gestures.

Expected: labels and states are understandable, focus moves to errors and returns predictably, and every visible action is operable without relying on color.

### Task 4: Execute managed desktop and LMS checks

**Files:**
- Create: one dated evidence record per managed Chromium, Firefox and LMS configuration

**Interfaces:**
- Consumes: same approved HTTPS build and named managed target configurations.
- Produces: desktop, keyboard, download, policy and LMS evidence.

- [ ] **Step 1: Run the core state flow in managed Chromium and Firefox**

Repeat persistent save/reload, volatile mode, valid and invalid import, export, single deletion and global deletion in each managed browser.

Expected: results match the contract; any policy-dependent download or storage restriction is visible and recorded.

- [ ] **Step 2: Run the keyboard and desktop screenreader path**

Use keyboard only for skip link, navigation, fields, dialogs, import and deletion. Use the institutionally available desktop screenreader and record its exact version.

Expected: logical order, visible focus, usable status announcements and no keyboard trap.

- [ ] **Step 3: Verify LMS integration**

Embed the approved fixture URL using the actual LMS policy. If iframe storage or sandbox policy prevents reliable operation, verify that the external-tab path is visible and understandable.

Expected: either the embedded flow works without silent state loss, or the documented external-tab fallback works and is accepted by the owner.

### Task 5: Evaluate and close or retain the gate

**Files:**
- Modify: all dated evidence records
- Modify only on full pass: `docs/platform/device-verification.md`
- Modify: `docs/platform/implementation-report.md`
- Modify: IUM14 task, Phase-1 initiative, Kanban, Roadmap, project page and session summary

**Interfaces:**
- Consumes: complete dated evidence records for every mandatory configuration.
- Produces: `passed`, `fail` or `blocked` gate decision with reproducible evidence.

- [ ] **Step 1: Audit evidence completeness**

Every required checkbox must have a real observation, exact configuration and evidence path. Automated CI is supporting context, never the device observation.

Expected: no blank mandatory field and no inferred iPad result.

- [ ] **Step 2: Apply the fail-closed decision rule**

- Set `passed` only when every mandatory configuration passes or an owner explicitly accepts each documented limitation.
- Set `fail` when a reproducible platform defect remains.
- Keep `blocked` when device, policy, network, LMS or HTTPS access is unavailable.

- [ ] **Step 3: Update status without overstating scope**

Only on `passed`, change the template front matter to `device-verified: passed`, update the implementation report and unblock the Phase-2 decision gate. A device pass does not establish teaching effectiveness, release readiness or curriculum-module quality.

- [ ] **Step 4: Re-run repository verification and publish the evidence metadata**

Run:

```powershell
npm run verify:phase1
git diff --check
git fetch --prune
git pull --ff-only origin main
```

Commit only privacy-reviewed metadata and repository-safe evidence links. Never commit local MDM secrets, learner data or sensitive network details.

## Self-Review

- Spec coverage: real iPad/Safari, VoiceOver, managed desktop browsers, keyboard, HTTPS, offline/update, storage, Web Clip, filters and LMS are each assigned to an explicit task.
- Scope boundary: CI remains `implemented` evidence; no step permits emulation to set `device-verified`.
- Privacy boundary: synthetic data only; policy evidence is reviewed before repository publication.
- Execution status: the owner approved temporary GitHub Pages and confirmed an available managed target iPad. HTTPS publication is being implemented; real configuration and interaction evidence remain open until the guided device run.
