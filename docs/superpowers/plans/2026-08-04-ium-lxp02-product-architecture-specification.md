# IuM LXP02 Product Architecture Specification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a review-ready, code-free LXP02 specification for the IuM-Lernwerk product architecture, navigation and coherent learning journey.

**Architecture:** One normative Markdown specification defines the complementary spaces of Lernwerk-Kosmos and Lernstudio, their information hierarchy, learner and teacher states, navigation transitions, re-entry, evidence spaces and resilient local-first behavior. Every contract is checked through the three LXP01 vertical reference situations before it can pass the written user gate. The plan creates no product code, wireframe or visual design system.

**Tech Stack:** Markdown, Mermaid state/flow diagrams, PowerShell, ripgrep and Git; no application runtime, framework or new dependency.

## Global Constraints

- LXP01 at `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md` is the normative input and may not be weakened silently.
- Keep the two-level architecture: an open modular Lernwerk-Kosmos outside modules and a teacher-orchestrated Lernstudio inside a module.
- Preserve the full experience loop: orient, activate prior knowledge and expectations, think and decide, act, observe effects, interpret feedback, check and revise, secure and transfer, re-enter.
- Motivation comes from relevant goals, meaningful bounded choice, visible competence growth, useful feedback and aesthetic care; do not add points, streaks, rankings, artificial scarcity or reward loops.
- Progress is subject-matter progress, not click completion, time-on-task or person-level analytics.
- Keep learner data local; do not add accounts, central diagnostics, telemetry, class management or automatic personalization.
- Design offline, recovery and update states as visible experience states rather than hidden technical exceptions.
- Preserve accessibility, cognitive accessibility, keyboard and touch equivalence, reduced-motion compatibility and non-color-only meaning.
- Keep the teacher lane tied to the same learning actions and vocabulary as the learner lane; do not create a second product.
- Do not create product code, wireframes, moodboards, brand decisions, CSS, component APIs, router libraries, state libraries, a full design-system taxonomy, new curriculum mapping, pilot instruments, deployments or release actions.
- LXP03 owns concrete visual/interaction realizations of the three vertical reference situations; LXP04 owns the reusable design and interaction system.
- Execute the plan sequentially because all tasks modify one normative architecture specification.

## File Map

- Create: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md` — the single normative LXP02 product-architecture specification.
- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md` — approved LXP01 evidence, experience and quality contract.
- Read: `docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md` — project-wide product, licensing and platform constraints.
- Read: `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md` — concrete module semantics used only as a stress test, not as an experience approval.
- Read: `docs/platform/implementation-report.md` — current platform status and technical boundary.
- Modify at handoff: `Vault/60_Organisation/Workspace-Entwicklung/Tasks/2026-08-04 - LXP02 Produktarchitektur Navigation und Lernreise spezifizieren.md` — execution status, decisions and review gate.
- Modify at handoff: the initiative, Kanban, roadmap, context package, project page and one session summary named in the active workspace task.

---

### Task 1: Seal the specification boundary and traceability scaffold

**Files:**

- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md`
- Read: `docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md`
- Read: `docs/platform/implementation-report.md`
- Create: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`

**Interfaces:**

- Consumes: the written LXP01 approval, the eight quality dimensions, the three reference situations and current platform boundaries.
- Produces: an explicit LXP02 scope, a decision ledger, a source-of-truth order and a 12-item traceability matrix for every required LXP02 result.

- [ ] **Step 1: Confirm the clean documentation baseline**

Run:

```powershell
git status --short --branch
git fetch --prune
git pull --ff-only
git rev-parse HEAD
```

Expected: the repository is clean, `main` is based on the current remote, and the approved LXP01 commit is in history. Stop if pull cannot fast-forward.

- [ ] **Step 2: Open the workspace task before specification work**

Set LXP02 from `planned` to `in_progress` and record Codex takeover in its result log without adding `owner_agent`. Confirm that LXP01 is `done` and is the only direct dependency.

Expected: task status and handoff comply with the agent-neutral lock rule; no LXP03 or LXP04 task is activated.

- [ ] **Step 3: Create the normative document header and status boundary**

Create the specification with these opening sections in this order:

1. `Entscheidung und Zweck`
2. `Status, Geltungsbereich und Nicht-Ziele`
3. `Normative Eingaben und Vorrangregel`
4. `LXP02-Ergebnisvertrag`
5. `Begriffs- und Entscheidungsledger`

The status section must state that this is product-architecture specification work only. It must explicitly exclude product code, concrete wireframes, visual styling, IUM5 rewriting, pilot, deployment, LMS and release.

- [ ] **Step 4: Add the 12-item traceability matrix**

Create one row for each approved LXP02 consequence:

1. Cosmos information architecture;
2. module start and startboard;
3. Lernstudio state model;
4. navigation between learning phases and lessons;
5. whole-map and progressive disclosure;
6. new, continuation and re-entry paths;
7. securing space and evidence card;
8. teacher lane;
9. local-first, offline and error states;
10. role and social-form changes;
11. terminology and labelling contract;
12. boundary to LXP03 and LXP04.

Use these columns: `LXP02-ID`, `required result`, `normative input`, `specification section`, `reference-situation check`, `review evidence`, `status`. The only allowed status values during drafting are `specified`, `open-decision` and `not-applicable-with-rationale`.

- [ ] **Step 5: Validate the scaffold**

Run:

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n '^## ' $specPath
rg -n 'Produktcode|Wireframe|Pilot|LMS|Release|LXP02-ID' $specPath
(Select-String -Path $specPath -Pattern '^\| LXP02-' -Encoding UTF8).Count
```

Expected: all five opening sections exist; every exclusion is visible; the matrix contains exactly 12 requirement rows.

- [ ] **Step 6: Commit the sealed scaffold**

```powershell
git add docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md
git diff --cached --check
git commit -m "docs(lxp02): scaffold product architecture contract"
```

Expected: a documentation-only commit; no application, package, fixture or test file is staged.

### Task 2: Specify the Lernwerk-Kosmos information architecture

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`
- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md`
- Read: `docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md`

**Interfaces:**

- Consumes: the LXP01 distinction between overview/selection and focused learning.
- Produces: a stable content-object hierarchy, global orientation model and transition contract from Cosmos to Lernstudio.

- [ ] **Step 1: Define the architecture objects and ownership rule**

Specify a hierarchy that distinguishes at least:

- Lernwerk-Kosmos;
- curriculum or topic region;
- module family;
- module;
- learning path;
- lesson or teaching unit;
- learning phase;
- learning action;
- securing artifact.

For every object record: purpose, learner-visible identity, teacher-visible orchestration data, parent, permitted children, entry action and whether local progress may be attached. Resolve synonymous legacy terms in the terminology ledger instead of preserving two labels for one object.

- [ ] **Step 2: Specify global Cosmos views without designing screens**

Define the information responsibilities of:

1. overview and orientation;
2. search or filtering if retained;
3. module comparison;
4. current and recent work;
5. teacher-prepared starting point;
6. help, accessibility and local-data controls.

For each view specify question answered, minimum information, primary action, permissible secondary actions, empty state, offline state and route back. Do not define layout, component shape, color or typography.

- [ ] **Step 3: Define the Cosmos-to-Lernstudio handoff**

Record the transition payload conceptually: selected module, intended learning path, lesson or phase target, launch mode, social form, estimated teaching-time corridor, locally available continuation state and offline readiness. Mark each field as learner-visible, teacher-visible, local-persisted or session-only.

Expected: learners can explain where they are going and how to return; teachers can launch the same learning object without a parallel content taxonomy.

- [ ] **Step 4: Define global navigation invariants**

The specification must make these invariants normative:

- changing global space never silently discards local work;
- returning to Cosmos preserves module and phase context;
- global navigation does not compete visually with the current learning action;
- every deep entry has a recoverable parent context;
- browser back, explicit back and home actions have distinct, documented meaning;
- offline navigation never implies unavailable content is ready.

- [ ] **Step 5: Run the Cosmos contract check**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n 'Lernwerk-Kosmos|Modulfamilie|Lernpfad|Lernphase|Sicherungsartefakt' $specPath
rg -n 'verwirft|Elternkontext|offline|Rückkehr|Browser-Zurück' $specPath
```

Expected: every object and navigation invariant has a normative statement and a reviewable failure condition.

- [ ] **Step 6: Commit the Cosmos architecture**

```powershell
git add docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md
git diff --cached --check
git commit -m "docs(lxp02): specify cosmos information architecture"
```

### Task 3: Specify module entry, startboard and re-entry

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`
- Read: `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md`

**Interfaces:**

- Consumes: Cosmos launch context, local continuation state and the LXP01 entry/orientation reference situation.
- Produces: one coherent entry contract for new start, teacher-directed start, continuation, recovery and later re-entry.

- [ ] **Step 1: Define the five entry modes**

Specify separately:

1. new self-initiated module entry;
2. teacher-directed lesson entry;
3. continuation on the same device;
4. re-entry after a longer interruption;
5. recovery after offline, update or local-data disruption.

For each mode identify trigger, trusted context, information that must be confirmed, primary action, cancel/return path and the condition under which work may resume.

- [ ] **Step 2: Define the startboard information contract**

The startboard must answer, in learner language:

- What is this about?
- What will I be able to do or explain?
- Where am I now?
- What is the next meaningful action?
- How much classroom time is this segment expected to need?
- What material, partner or group arrangement is required?
- Is the required content available offline?
- What local work will be used or restored?
- How can I return without losing work?

Specify which answers are always visible, progressively available or teacher-controlled. Keep learning goal and current action dominant.

- [ ] **Step 3: Specify stale, conflicting and absent continuation states**

Define visible behavior for:

- no local state;
- one valid continuation state;
- a completed phase with an unfinished securing action;
- a state from an older compatible content version;
- an incompatible or corrupted local state;
- a teacher-directed target that differs from the local continuation point.

No case may silently overwrite, reset or merge learner work. The teacher-directed target may guide the next action but must not erase local evidence.

- [ ] **Step 4: Specify re-entry orientation**

Re-entry must show last meaningful action, last secured result, current goal, next decision and available recovery path. It must not use a generic percentage, streak or time-based urgency. Define the maximum information needed before the learner can resume and which details remain expandable.

- [ ] **Step 5: Walk through reference situation 1**

Use the approved entry/orientation situation and write a two-lane walkthrough with columns:

`moment`, `learner sees`, `learner decides/does`, `system response`, `teacher sees/can do`, `local state`, `failure recovery`, `quality dimensions`.

Expected: the learner can name goal, position, next action and return path; the teacher can start or redirect without inspecting personal telemetry.

- [ ] **Step 6: Validate and commit entry architecture**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n 'Neueinstieg|Fortsetzung|Wiedereinstieg|Wiederherstellung|Startboard' $specPath
rg -n 'überschreib|inkompatibel|beschädigt|Lehrkraftziel|offline verfügbar' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp02): define entry and re-entry architecture"
```

Expected: all five entry modes and six continuation cases are explicit; the commit remains documentation-only.

### Task 4: Specify the Lernstudio state and navigation model

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`
- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md`
- Read: `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md`

**Interfaces:**

- Consumes: startboard launch context and the approved experience grammar.
- Produces: normative learning states, permitted transitions, phase navigation and progressive-disclosure rules.

- [ ] **Step 1: Define the canonical learning-state vocabulary**

Evaluate the minimum state set needed to distinguish orientation, readiness, active thinking/decision, action, observable effect, feedback interpretation, revision, securing, transfer, pause and recoverable error. Record the selected German labels and stable technical-neutral IDs in the terminology ledger.

The state model must describe learning meaning, not UI pages. Avoid a state for every click or component event.

- [ ] **Step 2: Create the state transition table**

For every permitted transition include:

`from state`, `event or learner action`, `guard`, `visible dominant region`, `feedback`, `local persistence`, `teacher cue`, `offline behavior`, `recovery`, `to state`.

Explicitly document prohibited transitions such as action before required prediction, securing before feedback interpretation, transfer without a secured result and silent advance on timer expiry.

- [ ] **Step 3: Add one Mermaid state diagram**

The diagram must represent the canonical happy path plus pause, revision loop and recoverable error. It must not encode visual layout or a JavaScript implementation. Every diagram node and edge must have a matching transition-table entry.

- [ ] **Step 4: Specify lesson and phase navigation**

Define the distinct meaning of:

- next learning action;
- previous context;
- phase overview;
- whole-module map;
- lesson boundary;
- pause and exit;
- resume;
- teacher-directed phase jump.

For each action state when it is available, what context remains visible, what requires confirmation and how unsaved or unsecured work is protected.

- [ ] **Step 5: Specify progressive disclosure as a content contract**

For each learning state classify information as:

- dominant now;
- context kept visible;
- expandable support;
- intentionally unavailable until meaningful;
- never hidden because it is safety-, privacy- or decision-critical.

Normatively prohibit hiding the current goal, relevant input, affected representation, feedback meaning, error recovery or save status.

- [ ] **Step 6: Stress-test with the IUM5 core interaction**

Walk prediction, deterministic execution, trace observation, feedback interpretation, hypothesis-led repair, rerun and securing through the state model. Record every mismatch as either a LXP02 architecture correction or an explicit IUM5 legacy issue; do not edit IUM5 product files.

- [ ] **Step 7: Validate and commit the Lernstudio model**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n 'from state|Ausgangszustand|Revision|Sicherung|Transfer|Wiederherstellung' $specPath
rg -n 'stateDiagram|Mermaid|Gesamtkarte|Phasenübersicht|progressive Offenlegung' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp02): specify learning studio state model"
```

Expected: the table, diagram and IUM5 walkthrough agree; no UI or runtime state-library decision appears.

### Task 5: Specify progress, securing space and evidence card

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`

**Interfaces:**

- Consumes: Lernstudio states and locally persisted learning results.
- Produces: a subject-matter progress model, a securing-space contract and one portable evidence-card grammar.

- [ ] **Step 1: Define subject-matter progress signals**

Allow progress signals only when they represent a meaningful capability or secured learning result, for example orientation completed, hypothesis articulated, model tested, error cause revised, explanation secured or transfer justified. Explicitly reject click count, page count, time-on-task, rank and inferred ability scores.

For every signal specify evidence source, learner meaning, teacher use, local persistence, expiry/version behavior and whether the signal may be manually revised.

- [ ] **Step 2: Define the securing-space responsibilities**

The securing space must support reviewing, comparing, revising, exporting and reusing learner-selected artifacts without becoming a portfolio platform or central assessment store. Specify empty, partial, complete, incompatible-version and offline states.

- [ ] **Step 3: Define the evidence-card grammar**

Each card must distinguish:

- context and learning question;
- learner decision, hypothesis or model;
- action or test performed;
- observed effect;
- interpreted feedback;
- revision and rationale;
- secured conclusion;
- transfer connection;
- local timestamp/version only where needed for recovery, not behavioral analytics.

Specify which fields are required by learning-action type, which are learner-editable and which are system-derived. Do not require personal reflection or sensitive free text.

- [ ] **Step 4: Define export, deletion and re-import experience**

Specify confirmation, sensitivity notice, file ownership language, compatible-version check, failure explanation and recovery path. Export must be explicitly learner- or teacher-initiated; no background synchronization or central upload may be implied.

- [ ] **Step 5: Walk through reference situation 3**

Use the securing/transfer/re-entry situation to show how a learner secures an artifact, connects it to a transfer problem, exits and later resumes. Include the teacher close-out and next-lesson launch without person-level monitoring.

- [ ] **Step 6: Validate and commit the evidence architecture**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n 'fachlicher Fortschritt|Sicherungsraum|Belegkarte|Export|Löschung|Re-Import' $specPath
rg -n 'Klick|Bearbeitungszeit|Rang|Hintergrundsynchron' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp02): define securing and evidence architecture"
```

### Task 6: Specify teacher orchestration, roles and social-form transitions

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`

**Interfaces:**

- Consumes: the same content objects, learning states and evidence grammar used by learners.
- Produces: a non-telemetric teacher lane and explicit transitions between individual, partner, group and whole-class work.

- [ ] **Step 1: Define the teacher lane by teaching phase**

Specify responsibilities for preparation, launch, observation, intervention, transition, securing and follow-up. For each phase state what is visible before class, during the current learning action and only on demand.

The lane may expose curriculum connection, intended learning action, expected misconceptions, discussion prompts, timing corridor, social form, material needs, offline readiness and intervention options. It may not expose central learner histories, inferred profiles or hidden monitoring.

- [ ] **Step 2: Define intervention contracts**

For each intervention type record trigger observable in ordinary teaching, teacher action, learner-facing consequence, preserved local state and exit condition. Cover at least:

- clarify the current goal;
- pause for whole-class comparison;
- reveal or point to a scaffold;
- redirect to revision;
- change social form;
- defer transfer or expansion;
- recover from technical disruption.

No intervention may silently complete, grade or rewrite learner work.

- [ ] **Step 3: Define role and social-form transitions**

Specify the handoff for individual-to-pair, pair-to-group, group-to-plenary and return-to-individual work. For each transition identify shared object, private local artifact, speaking/listening role if needed, confirmation step, device arrangement and recovery if a partner or device is unavailable.

- [ ] **Step 4: Define shared-display and privacy boundaries**

State which information may be projected or shared to a whole class, which requires learner selection, which must remain local and how neutral examples replace personal disclosure. Teacher prompts and projected states must use the same labels as the learner experience.

- [ ] **Step 5: Walk through all three reference situations from the teacher lane**

Add one row per orchestration moment: `prepare`, `launch`, `observe`, `intervene`, `transition`, `secure`, `re-enter`. Mark whether the teacher acts at class, group or individual level and what evidence is available without telemetry.

- [ ] **Step 6: Validate and commit teacher orchestration**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n 'Vorbereitung|Start|Beobachtung|Intervention|Übergang|Sicherung|Wiedereinstieg' $specPath
rg -n 'Einzelarbeit|Partnerarbeit|Gruppenarbeit|Plenum|Telemetrie|personenbezogen' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp02): specify teacher orchestration architecture"
```

### Task 7: Specify resilience, accessibility and terminology contracts

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`
- Read: `docs/platform/implementation-report.md`

**Interfaces:**

- Consumes: all navigation, state, evidence and teacher-lane decisions.
- Produces: visible local-first/offline/error states, cross-input accessibility rules and one controlled German label set.

- [ ] **Step 1: Define the experience severity model**

Use three severities with distinct behavior:

1. informational state — learning can continue unchanged;
2. action-limiting state — one action is unavailable but a safe alternative exists;
3. blocking or safety/privacy-critical state — learning must pause until the user understands and chooses a recovery action.

For each severity define prominence, focus behavior, announcement, persistence, dismissibility and teacher cue. Do not encode color as the only differentiator.

- [ ] **Step 2: Specify the required resilience cases**

Cover at least:

- first use while offline;
- previously cached content offline;
- required module asset unavailable;
- local save unavailable or quota exhausted;
- corrupted or incompatible import;
- export interrupted;
- update available;
- update failed while the old version remains usable;
- content version changed during a paused learning path;
- browser or policy blocks a needed capability.

For every case state visible message purpose, preserved work, primary recovery action, alternative route, teacher information and forbidden silent behavior.

- [ ] **Step 3: Specify interaction and cognitive-accessibility invariants**

Bind every navigation and state transition to:

- keyboard, touch and assistive-technology operability;
- predictable focus movement and return;
- programmatic name, role, value and state;
- status announcements that do not steal focus unnecessarily;
- reduced-motion equivalence;
- zoom/reflow and narrow-screen equivalence;
- plain, age-appropriate action language;
- stable placement and stable naming across phases;
- no forced memorization of hidden prior context;
- no information loss through progressive disclosure.

- [ ] **Step 4: Finalize the terminology and labelling contract**

Create a controlled table with `concept ID`, `preferred German label`, `learner meaning`, `teacher meaning`, `allowed short label`, `rejected synonyms`, `state-dependent wording`, `accessibility note`. Include all global spaces, navigation actions, learning states, progress signals, securing objects, offline states and teacher interventions.

Label actions by outcome rather than icon or location. Distinguish `zurück`, `zur Übersicht`, `pausieren`, `sichern`, `verwerfen`, `wiederherstellen` and `fortsetzen` explicitly.

- [ ] **Step 5: Run resilience and label checks**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
rg -n 'informativ|handlungseinschränkend|blockierend|sicherheitskritisch|datenschutzkritisch' $specPath
rg -n 'Tastatur|Touch|Fokus|Statusmeldung|Bewegungsreduktion|Reflow|kognitive' $specPath
rg -n 'zurück|Übersicht|pausieren|sichern|verwerfen|wiederherstellen|fortsetzen' $specPath
```

Expected: every required resilience case and every action label has explicit behavior and a failure condition.

- [ ] **Step 6: Commit resilience and terminology**

```powershell
git add docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md
git diff --cached --check
git commit -m "docs(lxp02): define resilient accessible navigation"
```

### Task 8: Validate the integrated architecture through the three reference situations

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`
- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md`
- Read: `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md`

**Interfaces:**

- Consumes: the integrated Cosmos, entry, Lernstudio, evidence, teacher, resilience and terminology contracts.
- Produces: three end-to-end architecture walkthroughs, an eight-dimension scorecard, resolved contradictions and a hard boundary for LXP03/LXP04.

- [ ] **Step 1: Normalize the three walkthrough tables**

Use the same columns for all three situations:

`moment`, `space`, `learning state`, `learner goal`, `visible dominant information`, `learner action`, `system response`, `teacher option`, `local state`, `offline/recovery`, `navigation out/back`, `quality evidence`.

Each walkthrough begins in Cosmos or a documented deep-entry context and ends with a recoverable next position.

- [ ] **Step 2: Complete situation 1 — entry and orientation**

Exercise new start, teacher-directed start and re-entry variants. Include narrow-screen and keyboard-only considerations. Fail the architecture if goal, position, next action, offline readiness or return path becomes ambiguous.

- [ ] **Step 3: Complete situation 2 — interactive core action with feedback and revision**

Exercise prediction/decision, action, effect, feedback interpretation, at least one revision loop and securing. Include action-limiting offline behavior and a teacher whole-class pause. Fail if feedback becomes answer revelation, revision can be skipped silently or global navigation overwhelms the current action.

- [ ] **Step 4: Complete situation 3 — securing, transfer and re-entry**

Exercise evidence-card creation, learner-selected export, transfer prompt, pause, later re-entry and teacher follow-up. Fail if progress is represented only as completion, personal disclosure is required or a version/error state can silently discard work.

- [ ] **Step 5: Score all eight LXP01 quality dimensions**

For every situation record `pass`, `pass-with-explicit-risk` or `fail` for:

1. learning-action clarity;
2. cognitive economy;
3. agency and motivation;
4. feedback and revision;
5. progress and continuity;
6. teacher orchestration;
7. accessibility and equivalence;
8. resilience, privacy and openness.

Every `pass-with-explicit-risk` requires owner, follow-up phase and failure signal. Any `fail` blocks written review.

- [ ] **Step 6: Resolve cross-contract contradictions**

Check at least:

- whole-map visibility versus progressive disclosure;
- teacher direction versus learner agency;
- local continuity versus version changes;
- module freedom versus global terminology;
- accessible redundancy versus cognitive economy;
- offline truthfulness versus uninterrupted flow.

For each contradiction record chosen priority, mechanism, cost and validation path. Do not defer an architecture decision to component styling.

- [ ] **Step 7: Seal the LXP03/LXP04 boundary**

LXP03 receives the architecture walkthroughs and creates concrete comparable experience designs for the three situations. LXP04 receives only patterns proven across those designs and turns them into reusable visual, interaction, accessibility and production contracts. Explicitly list decisions LXP02 has made and decisions it intentionally leaves to each later phase.

- [ ] **Step 8: Validate and commit the integrated walkthroughs**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
(Select-String -Path $specPath -Pattern '^### Referenzsituation ' -Encoding UTF8).Count
rg -n 'Lernhandlungs-Klarheit|kognitive Ökonomie|Agency|Feedback|Kontinuität|Lehrkraftorchestrierung|Gleichwertigkeit|Resilienz' $specPath
rg -n 'LXP03|LXP04|pass-with-explicit-risk|fail' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp02): validate product architecture scenarios"
```

Expected: exactly three normalized walkthroughs, 24 quality-dimension judgments and no unresolved `fail` result.

### Task 9: Complete the written LXP02 review package

**Files:**

- Modify: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Tasks/2026-08-04 - LXP02 Produktarchitektur Navigation und Lernreise spezifizieren.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Initiativen/2026-08-04 - IuM-Lernwerk Learning Experience und Produktionssystem.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Workspace Kanban.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Workspace Roadmap.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Kontextpakete/Kontextpaket - IuM-Lernwerk Learning Experience.md`
- Modify: `Vault/40_Projekte/IuM-Lernwerk/IuM-Lernwerk.md`
- Create: one dated LXP02 session summary under `Vault/50_Codex/Sessions/`

**Interfaces:**

- Consumes: all LXP02 sections and validation evidence.
- Produces: a self-reviewed specification at `review`, a clean documentation history and one explicit written user gate before LXP03.

- [ ] **Step 1: Close the 12-item traceability matrix**

Every row must be `specified` and point to a concrete section plus at least one reference-situation check. Resolve every `open-decision`. A `not-applicable-with-rationale` result is allowed only when the LXP01 consequence is demonstrably owned by LXP03 or LXP04 and the boundary is explicit.

- [ ] **Step 2: Run the full specification coverage check**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
$specText = Get-Content -Raw -Encoding UTF8 -LiteralPath $specPath
$required = @(
  'Informationsarchitektur des Kosmos',
  'Startboard',
  'Zustandsmodell des Lernstudios',
  'Navigation zwischen Lernphasen',
  'progressive Offenlegung',
  'Wiedereinstieg',
  'Sicherungsraum',
  'Belegkarte',
  'Lehrkraftspur',
  'Offline',
  'Sozialformwechsel',
  'Beschriftungsvertrag',
  'LXP03',
  'LXP04'
)
$missing = @($required | Where-Object { -not $specText.Contains($_) })
if ($missing.Count -gt 0) { $missing; exit 1 }
Write-Output "PASS: $($required.Count)/$($required.Count) Architekturmarker vorhanden"
```

Expected: exit 0 and `14/14` architecture markers.

- [ ] **Step 3: Run document hygiene and scope checks**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md'
git diff --check
rg -n 'Produktcode|Wireframe|Moodboard|CSS|Router|Pilot|Deployment|Release' $specPath
git diff --name-only $(git merge-base HEAD origin/main)..HEAD
```

Expected: no whitespace errors; explicit exclusions remain; all LXP02 commits touch documentation only. Inspect the file list and stop if application or package files appear.

- [ ] **Step 4: Perform the writing-plan self-review against LXP01**

Read LXP01 sections 9–34 and map each normative architecture consequence to LXP02. Confirm:

- all 12 LXP02 results are specified;
- terms and state IDs are consistent across tables and diagrams;
- every diagram edge exists in the transition table;
- the three walkthroughs use the same state and label vocabulary;
- no architecture choice depends on an unspecified UI layout;
- no product implementation or later-phase decision slipped into scope.

Fix any discrepancy in the specification before proceeding.

- [ ] **Step 5: Commit the final review package in the repository**

```powershell
git fetch --prune
git pull --ff-only
git add docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md
git diff --cached --check
git commit -m "docs(lxp02): finalize product architecture specification"
git status --short --branch
```

Expected: clean local branch based on the current remote, with documentation-only LXP02 commits. Do not push unless the user explicitly requests it.

- [ ] **Step 6: Move LXP02 to written review**

Set the task to `review`, mark every acceptance criterion except written user approval, record commit hashes and verification results, move its Kanban card to `Review`, and update initiative, roadmap, context package, project page and session summary. Do not create or start LXP03 yet.

- [ ] **Step 7: Ask for one bundled written review**

Provide the clickable specification path, exact Git status, scope statement and remaining gate. Ask the user to answer either `LXP02 freigegeben` or provide concrete change requests. Do not seek micro-approval for individual sections.

## Plan Self-Review Result

- LXP01 section 30 coverage: 12/12 required LXP02 results mapped to Tasks 1–8.
- LXP01 vertical situations: all three are exercised as integrated architecture walkthroughs in Task 8.
- Eight LXP01 quality dimensions: 24 judgments required across the three situations.
- Type and vocabulary consistency: one terminology ledger, one state-transition table and one shared walkthrough schema are normative.
- Scope: documentation and workspace status only; product code and all LXP03/LXP04 deliverables remain excluded.
- Execution shape: nine sequential tasks, one normative specification file, review after each independently rejectable architecture unit.
