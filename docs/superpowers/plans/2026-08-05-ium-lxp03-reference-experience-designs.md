# IuM LXP03 Reference Experience Designs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a review-ready, code-free LXP03 specification containing three concrete, coherent and comparable reference experience designs plus one evidence-based selection and LXP04 handoff decision.

**Architecture:** One normative Markdown specification realizes the approved LXP01 experience strategy inside the approved LXP02 product architecture. It uses one end-to-end IUM5 learning journey as a concrete stress case, separates three decision-complete vertical reference situations, normalizes their wide/narrow, learner/teacher, accessibility and resilience descriptions, and cross-checks portability to analysis, judgment and production before naming any reusable pattern candidate.

**Tech Stack:** Markdown, Mermaid wireflows and state/sequence diagrams, text wireframes, PowerShell, ripgrep and Git; no application runtime, design tool, framework, package or new dependency.

## Global Constraints

- LXP01 at `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md` is the normative experience and quality contract and may not be weakened silently.
- LXP02 Fassung 1.0 at `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md` is the normative object, state, navigation, label, role, data, accessibility and recovery contract.
- Preserve the complementary Lernwerk-Kosmos and teacher-orchestrated Lernstudio architecture and the full learning-action loop.
- Use exactly the controlled LXP02 labels for spaces, learning states, navigation, securing and recovery; do not create synonyms locally.
- Treat IUM-5-CORE-05 as the concrete fachlich-didaktischer stress case, not as an approved UI or a global content template.
- Every design must make fachliche Eigenleistung, criteria, feedback, revision, teacher orchestration and non-telemetric evidence visible.
- Motivation comes from relevance, achievable challenge, meaningful bounded choice, visible product improvement, belonging and aesthetic care; do not add points, streaks, rankings, artificial scarcity or reward loops.
- Keep local learner data local; do not add accounts, class management, dashboards, telemetry, automated diagnosis, grading or personalization.
- Keep WCAG 2.2 AA, cognitive accessibility, keyboard/touch/text-AT equivalence, reduced-motion compatibility, 320 CSS-pixel reflow and 200-percent zoom as binding design inputs.
- Keep Local First, offline truthfulness, confirmed-state authority, export sensitivity and recovery consequences visible in the situation where they matter.
- Create concrete reference compositions and interaction sequences, not product code, high-fidelity brand styling, design tokens, component APIs, router/state libraries or a reusable design system.
- LXP04 may generalize only candidates evidenced across all three situations; LXP05 owns IUM5 product implementation and content rewrite.
- Do not preview, deploy, run real-device tests, pilot, integrate with an LMS, publish or raise product/module status.
- Execute sequentially and inline. The user has already selected full inline execution and has not authorized sub-agents.

## File Map

- Create: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md` — normative LXP03 reference-design and selection specification.
- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md` — LXP01 north star, quality model and reference-situation contract.
- Read: `docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md` — approved LXP02 architecture and explicit LXP03 risk ownership.
- Read: `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md` — IUM5 fachlicher stress case only.
- Read: `docs/fachprofil/ium-gymnasium-5-7.md` — working subject/stage planning profile.
- Modify at handoff: `Vault/60_Organisation/Workspace-Entwicklung/Tasks/2026-08-05 - LXP03 Vertikale Referenzsituationen entwerfen und vergleichen.md` — execution status, decisions, checks and review gate.
- Modify at handoff: initiative, Kanban, roadmap, context package, project page, development history and one dated LXP03 session summary named by the active workspace task.

---

### Task 1: Seal the LXP03 boundary, evidence hierarchy and traceability scaffold

**Files:**

- Create: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`
- Read: the four normative/context files in the file map.

**Interfaces:**

- Consumes: approved LXP01/LXP02 contracts, IUM5 fachlicher stress case, working subject profile and the explicit full-execution order.
- Produces: status/gate boundary, source-of-truth hierarchy, decision ledger and a 12-row LXP03 traceability matrix.

- [ ] **Step 1: Confirm the documentation baseline and synchronization boundary**

Run:

```powershell
git status --short --branch
git fetch --prune
git pull --ff-only
git rev-parse HEAD
git rev-parse origin/main
```

Expected: `main` is clean, contains `eaa46b7`, fast-forward synchronization succeeds, and the local branch remains documentation-only ahead of `origin/main`. Stop before a commit if fetch/pull fails.

- [ ] **Step 2: Confirm the workspace lock and open only LXP03**

Verify the new task is `in_progress`, sequence `222`, depends only on completed LXP02 and records Codex takeover without `owner_agent`. Confirm LXP04 and all product/pilot/release steps remain closed.

- [ ] **Step 3: Create the specification boundary**

Create these opening sections in order:

1. `Entscheidung und Zweck`;
2. `Status, Geltungsbereich und Freigabegates`;
3. `Normative Eingaben und Vorrangregel`;
4. `LXP03-Ergebnisvertrag`;
5. `Entscheidungsledger und kontrollierter Wortschatz`.

State explicitly that concrete text wireframes, wide/narrow compositions and interaction sequences are in scope, while product code, high-fidelity brand styling, reusable system contracts, IUM5 rewriting, preview, pilot, LMS and release are not.

- [ ] **Step 4: Add exactly 12 traceability rows**

Use IDs `LXP03-01` through `LXP03-12` for the twelve results in the workspace task. Columns: `LXP03-ID`, `required result`, `normative input`, `specification section`, `reference-design check`, `review evidence`, `status`. Allowed drafting statuses: `specified`, `open-decision`, `not-applicable-with-rationale`.

- [ ] **Step 5: Validate and commit the scaffold**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
(Select-String -Path $specPath -Pattern '^\| LXP03-[0-9]{2} \|' -Encoding UTF8).Count
rg -n 'Produktcode|LXP04|Preview|Pilot|LMS|Release|Freigabegate' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): scaffold reference experience contract"
```

Expected: exactly 12 traceability rows and a documentation-only commit.

### Task 2: Compare concrete composition approaches and choose one working direction

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: LXP01 approach decision and LXP02 explicit risks for cognitive economy, reflow and equivalence.
- Produces: a bounded LXP03 approach comparison and one working composition decision without generalizing a design system.

- [ ] **Step 1: Compare three approaches**

Compare:

1. `Dokument-Stack` — a vertically sequenced document with all current and next regions;
2. `strikter Schritt-Wizard` — one isolated screen per state;
3. `stabile Fokusbühne mit rekonstruierbarem Kontext` — a stable current learning relation plus compact context and a deliberate map/help/data return.

For each record learning mechanism, strengths, cognitive/accessibility cost, teacher-orchestration consequence, narrow-screen behavior and fail signal.

- [ ] **Step 2: Select the working direction**

Select approach 3 only if it preserves LXP02 guards, visible relevant context, safe return and equal text/AT action. Record rejected elements that may still be used locally, such as document flow for teacher reference and short dialog steps for irreversible data actions.

- [ ] **Step 3: Define one normalized reference-design schema**

Require the same sections for all three designs: purpose, scenario and learning product, learner/teacher moment, wide composition, narrow order, interaction sequence, focus/announcement behavior, local state, offline/recovery case, help/feedback, social-form transition, copy examples, WU check, Q1–Q8 evidence and fail criteria.

- [ ] **Step 4: Add the visual-density and context budget**

Specify that each moment has exactly one primary fachliche Handlung, one dominant relation, at most two directly competing secondary actions, and an explicitly named route to map/help/data. Treat these as project hypotheses to validate, not universal research thresholds.

- [ ] **Step 5: Validate and commit the decision**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
rg -n 'Dokument-Stack|Schritt-Wizard|Fokusbühne|Auswahlentscheidung|Projektbenchmark' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): choose reference composition direction"
```

### Task 3: Design reference situation 1 — entry, orientation and re-entry

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: LXP02 Startboard, five entry modes, six continuation cases, controlled labels and Q2/Q7 risk signals.
- Produces: one concrete coherent entry design covering new start, teacher-directed start, short continuation and later re-entry.

- [ ] **Step 1: Fix the concrete IUM5 entry scenario**

Use the current Unterrichtseinheit around the question `Wie genau muss eine Vorschrift sein, damit Mensch und digitales System denselben Ablauf ausführen?`, the visible product `einen präzisen Ablauf entwerfen, vorhersagen und prüfen`, one shared start and one valid local prior stand. Record assumed class/device conditions as working assumptions rather than real evidence.

- [ ] **Step 2: Draw concrete wide and narrow text wireframes**

The wide design must show context, purpose/product, primary start decision and compact time/social/offline facts without exposing later tools. The narrow design must preserve order `Ziel → lokaler Stand/Startmodus → primäre Handlung → Bedingungen/Rückweg`; no essential item may depend on a side column.

- [ ] **Step 3: Specify the interaction and focus sequence**

Cover keyboard, touch and text/AT paths for `neu beginnen`, `zum gemeinsamen Start`, `fortsetzen`, `wieder einsteigen`, map opening, help, pause and recovery. Define focus target and focus return for every overlay/expanded region.

- [ ] **Step 4: Connect the teacher lane**

Specify preparation, shared impulse, partner explanation, first halt, teacher-directed target, ordinary evidence and the fallback when learners cannot state goal/product/next action. No remote device state may be required.

- [ ] **Step 5: Add Local-First and recovery variants**

Include one calm `offline bereit` path, one existing local-state conflict and one blocking missing-core-content path. State what work is preserved and which action remains safe.

- [ ] **Step 6: Run situation-specific checks and commit**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
rg -n 'Referenzentwurf 1|Wide-Komposition 1|Schmal-Komposition 1|neu beginnen|zum gemeinsamen Start|wieder einsteigen|offline bereit' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): design entry and orientation reference"
```

### Task 4: Design reference situation 2 — core learning action, feedback and revision

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: IUM5 prediction/execution/trace/repair contract; LXP02 LS-DECIDE through LS-SECURE and Q2/Q7/Q8 risk signals.
- Produces: a concrete core-action design with preserved cause/effect, revision guards and a teacher whole-class halt.

- [ ] **Step 1: Define the concrete learning relation**

Use one deterministic delivery-robot case and make `Vorhersage`, `Algorithmus`, `aktueller Zustand/Laufspur`, `erste Abweichung`, `Reparaturhypothese` and `Revision` distinct. Do not add free programming, gamification or a full attempt history.

- [ ] **Step 2: Draw wide and narrow state compositions**

For each of LS-DECIDE, LS-ACT/LS-OBSERVE, LS-INTERPRET and LS-REVISE define the wide relationship and narrow reading/focus order. Keep input, affected representation and feedback in a reconstructible relation without making every tool simultaneously primary.

- [ ] **Step 3: Specify interaction equivalence**

Show how block insertion/reordering, prediction, step execution, trace reading, relevant-step selection, hypothesis and revision work by touch, keyboard and text/AT. Reduced motion uses the same semantic state source and must not reveal the answer early.

- [ ] **Step 4: Specify feedback and help escalation**

Provide concrete copy for result, process, strategy and criterion feedback. Define help layers from term/operation support to strategic hint and only then a complete worked example. Help use is not stored.

- [ ] **Step 5: Specify teacher halt, 1:2 roles and fallback evidence**

Use symmetric `steuern` and `vorhersagen/prüfen` roles with an explicit switch. Define a neutral projected error case, learner-selected sharing, a five-to-ten-minute intermediate check and a fresh short case if a product is missing.

- [ ] **Step 6: Add offline/action-limiting and recovery variants**

The interpreter core must be locally available; a missing noncentral help may be RES-LIMIT with a local equivalent, while a missing interpreter or failed save before revision is RES-BLOCK. Preserve the last confirmed starting/revision state.

- [ ] **Step 7: Validate and commit**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
rg -n 'Referenzentwurf 2|Wide-Komposition 2|Schmal-Komposition 2|Vorhersage|Laufspur|erste Abweichung|Reparaturhypothese|Reduced Motion' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): design feedback and revision reference"
```

### Task 5: Design reference situation 3 — securing, transfer and later return

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: LXP02 securing-space/evidence-card grammar, export/deletion contract and Q2/Q7 risk signals.
- Produces: a concrete securing/transfer/re-entry design without portfolio, duplicate writing or automatic sharing.

- [ ] **Step 1: Define the concrete securing product**

Assemble a Belegkarte from the real IUM5 Ausgangsalgorithmus, selected trace, interpretation, revision, loop decision, secured statement and model boundary. Do not require a second full narrative or personal reflection.

- [ ] **Step 2: Draw wide and narrow compositions**

Show selected evidence and editable conclusion in a clear relation. In the narrow order preserve source context and evidence before editing/confirmation. Separate `Belegkarte sichern`, `auf neuen Fall übertragen`, `exportieren`, `pausieren` and `zum Lernwerk-Kosmos`.

- [ ] **Step 3: Specify transfer and active re-entry**

Use a system-classification boundary case outside the robot context, then a later short active recall before showing the old card in full. The new answer remains separate from the source card.

- [ ] **Step 4: Specify export, deletion and version recovery**

Provide concrete sensitivity/ownership copy, focus behavior and safe cancel for export. Include incompatible-version recovery that preserves the original card and forbids partial merge.

- [ ] **Step 5: Connect teacher securing and follow-up**

Define shared statement/model-boundary consolidation, neutral or learner-selected evidence, no collection requirement, a diagnosis fallback and the next retrieval point.

- [ ] **Step 6: Validate and commit**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
rg -n 'Referenzentwurf 3|Wide-Komposition 3|Schmal-Komposition 3|Belegkarte sichern|auf neuen Fall übertragen|Datei gehört dir|aktive Abruffrage' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): design securing and re-entry reference"
```

### Task 6: Validate subject specificity, effective teaching and cross-domain portability

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: all three designs, the IuM working profile and IBBW WU excerpts 1, 3, 6 and 9.
- Produces: explicit instructional-quality decisions and a portability test preventing overfitting to robot programming.

- [ ] **Step 1: Add the plan anchor and maturity statement**

Record curriculum status: Basiskurs Medienbildung 2016 and Aufbaukurs Informatik 7 are enacted, the 2026/27 reading aid is orientation, the IuM profile is working, and LXP03 creates no new curriculum mapping.

- [ ] **Step 2: Run one WU check per reference design**

For each design record kognitive Aktivierung, konstruktive Unterstützung, Klassenführung/Struktur, Aufgabenqualität, Feedback/Diagnose, Kooperation/Verantwortlichkeit, Diagnose-Fallback, sprachliche/kognitive Zugänglichkeit, digitaler Mehrwert and most important residual risk. Cite the four loaded local excerpts as orientation, not causal proof.

- [ ] **Step 3: Verify task validity and own-work necessity**

For each situation state why learners must think, decide, test, justify or revise themselves and why generative AI or answer copying cannot replace the required situated product/evidence relation.

- [ ] **Step 4: Run three portability probes**

Map the composition, without inventing full new lessons, to:

1. source/evidence analysis and judgment;
2. data/system modeling;
3. media-product critique and revision.

For every probe list stable learning-state relation, content-specific representation that changes, teacher evidence and one point that must not be generalized from IUM5.

- [ ] **Step 5: Validate and commit**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
(Select-String -Path $specPath -Pattern '^### WU-Check Referenzentwurf ' -Encoding UTF8).Count
(Select-String -Path $specPath -Pattern '^\| PORT-' -Encoding UTF8).Count
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): validate learning quality and portability"
```

Expected: exactly three WU checks and three portability rows.

### Task 7: Compare the three designs against every approved quality and risk signal

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: normalized reference designs, LXP01 Q1–Q8, global anti-patterns and seven LXP02 pass-with-explicit-risk signals.
- Produces: 24 situation-quality judgments, seven explicit risk answers and a cross-situation contradiction ledger.

- [ ] **Step 1: Create exactly 24 quality judgments**

For each of the three situations evaluate Q1–Q8 as `pass`, `pass-with-explicit-risk` or `fail`. Each row includes concrete design evidence, remaining risk, owner phase and observable fail signal. Any `fail` blocks review.

- [ ] **Step 2: Answer the seven LXP02 risks explicitly**

Cover entry cognitive economy, entry accessibility, core cause/effect composition, core equal interaction, core offline truth, securing cognitive economy and securing accessibility. Mark `answered-in-LXP03` or `open-for-LXP04/LXP06-with-fail-signal`.

- [ ] **Step 3: Run the global anti-pattern scan**

Evaluate Mega-Seite, infrastructure-first, pseudo-progress, gamification, unstructured choice, wizard-without-overview, feedback-as-judgment, adaptive black box, teacher-as-afterthought, accessibility parallel product, narration-as-substitute and export-as-completion.

- [ ] **Step 4: Resolve cross-situation contradictions**

Record chosen priority, mechanism, cost and later validation for focus versus overview, dense relationships versus narrow reflow, teacher timing versus local agency, redundant accessibility versus cognitive economy, and data truth versus uninterrupted flow.

- [ ] **Step 5: Validate and commit**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
(Select-String -Path $specPath -Pattern '^\| [123] \| Q[1-8] ' -Encoding UTF8).Count
(Select-String -Path $specPath -Pattern '^\| RISK-LXP02-' -Encoding UTF8).Count
rg -n '\| fail \|' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): compare reference experience designs"
```

Expected: 24 quality rows, 7 risk rows and no unresolved `fail`.

### Task 8: Make the selection decision and seal the LXP04 handoff

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`

**Interfaces:**

- Consumes: the three designs, WU/portability checks, quality scorecard and contradiction ledger.
- Produces: one selected cross-situation composition, pattern candidates, non-generalizations and exact LXP04 inputs.

- [ ] **Step 1: Compare the three designs on one normalized matrix**

Compare orientation cost, task focus, cause/effect clarity, teacher orchestration, narrow/reflow integrity, interaction equivalence, resilience truthfulness, product continuity and portability.

- [ ] **Step 2: Select one cross-situation composition**

State which stable elements carry across all three situations and which situation-specific elements remain local. The decision must explain why it is superior to the document stack and strict wizard without claiming usability or learning effectiveness before LXP06/pilot.

- [ ] **Step 3: List LXP04 pattern candidates**

Candidates may include context band, focus relation, action boundary, comparison/revision relation, teacher halt, evidence assembly and recovery interruption only if evidenced in at least two situations and not contradicted by the third.

- [ ] **Step 4: List explicit non-generalizations**

Do not generalize robot grid, block editor, trace table, evidence-card visual form, exact action count, exact region count, animation, colors, tokens, typography, icons or component names.

- [ ] **Step 5: Define the written gate**

The bundled LXP03 review decides the full specification and selection. Approval opens only separate LXP04 planning; it does not open code, IUM5 rewrite, preview, pilot, LMS or release.

- [ ] **Step 6: Validate and commit**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
rg -n 'Auswahlentscheidung|LXP04-Musterkandidaten|Nicht generalisieren|Schriftliches Freigabegate' $specPath
git add $specPath
git diff --cached --check
git commit -m "docs(lxp03): select reference experience direction"
```

### Task 9: Complete the LXP03 written review package and workspace handoff

**Files:**

- Modify: `docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md`
- Modify: `Vault/60_Organisation/Workspace-Entwicklung/Tasks/2026-08-05 - LXP03 Vertikale Referenzsituationen entwerfen und vergleichen.md`
- Modify: initiative, Kanban, roadmap, context package, project page and development history.
- Create: one dated LXP03 session summary under `Vault/50_Codex/Sessions/`.

**Interfaces:**

- Consumes: all LXP03 sections and fresh verification evidence.
- Produces: a self-reviewed specification at `review`, documentation-only repository history and one explicit written user gate.

- [ ] **Step 1: Close the traceability matrix and acceptance checklist**

Every LXP03 row must be `specified`. Every acceptance item except written user approval must be checked from explicit evidence.

- [ ] **Step 2: Run the full coverage check**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
$specText = Get-Content -Raw -Encoding UTF8 -LiteralPath $specPath
$required = @(
  'Ansatzvergleich', 'Auswahlentscheidung', 'Referenzentwurf 1', 'Referenzentwurf 2',
  'Referenzentwurf 3', 'Wide-Komposition', 'Schmal-Komposition', 'Lehrkraftspur',
  'Tastatur', 'Touch', 'Text-/Assistive-Technology', 'Reduced Motion', 'Local First',
  'Offline', 'Recovery', 'WU-Check', 'Portabilitätsprüfung', 'Qualitätsurteile',
  'LXP04-Musterkandidaten', 'Schriftliches Freigabegate'
)
$missing = @($required | Where-Object { -not $specText.Contains($_) })
if ($missing.Count -gt 0) { $missing; exit 1 }
Write-Output "PASS: $($required.Count)/$($required.Count) LXP03-Marker vorhanden"
```

Expected: `20/20` markers.

- [ ] **Step 3: Run structural counts and hygiene checks**

```powershell
$specPath = 'docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md'
"traceability=$((Select-String -Path $specPath -Pattern '^\| LXP03-[0-9]{2} \|' -Encoding UTF8).Count)"
"quality=$((Select-String -Path $specPath -Pattern '^\| [123] \| Q[1-8] ' -Encoding UTF8).Count)"
"risks=$((Select-String -Path $specPath -Pattern '^\| RISK-LXP02-' -Encoding UTF8).Count)"
"portability=$((Select-String -Path $specPath -Pattern '^\| PORT-' -Encoding UTF8).Count)"
git diff --check
rg -n 'TBD|TODO|FIXME|PLACEHOLDER|\| fail \|' $specPath
```

Expected: `traceability=12`, `quality=24`, `risks=7`, `portability=3`, clean diff and no placeholder or unresolved fail.

- [ ] **Step 4: Perform the spec self-review**

Check terminology against the LXP02 controlled vocabulary, every wireflow against state guards, wide/narrow equivalence, focus return, learner/teacher vocabulary, WU maturity claims, portability limits and LXP04 boundary. Fix ambiguity, contradiction or accidental system generalization inline.

- [ ] **Step 5: Verify repository scope and commit the final review package**

```powershell
git fetch --prune
git pull --ff-only
git diff --name-only origin/main..HEAD
git diff --check
git add docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md
git diff --cached --check
git commit -m "docs(lxp03): finalize reference experience specification"
git status --short --branch
```

Expected: only documentation files differ from `origin/main`; local `main` is clean and ahead. Do not push or open a PR.

- [ ] **Step 6: Consolidate the workspace**

Set LXP03 to `review`, mark all acceptance criteria except written user approval, record all commit hashes and verification counts, move the task card to `Review`, update initiative/roadmap/context/project/history and create the session summary. Keep LXP04 closed.

- [ ] **Step 7: Request one bundled written review**

Provide the clickable specification path, current commit/branch/push status, verification counts and scope boundary. The remaining gate is a written `LXP03 freigegeben` or concrete change requests.

## Plan Self-Review Result

- LXP01 section 31 and LXP02 ownership-matrix coverage: all 12 LXP03 outcomes are mapped to Tasks 1–8.
- Reference coverage: exactly three decision-complete designs with one normalized schema and explicit learner/teacher, wide/narrow, accessibility and recovery views.
- Quality coverage: 24 Q1–Q8 judgments, seven inherited LXP02 risk answers, three WU checks and three portability probes are mandatory.
- Scope control: documentation only; no product code, component system, IUM5 rewrite, preview, pilot, LMS or release.
- Execution shape: nine sequential tasks in one specification file; inline execution is already selected by the user.
