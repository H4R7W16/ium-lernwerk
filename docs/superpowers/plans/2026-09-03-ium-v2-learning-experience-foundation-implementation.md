# IuM-Lernwerk V2 Learning and Experience Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Choose superpowers:subagent-driven-development only when the task graph passes the execution-mode check below; otherwise use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit the existing learning-psychology and LXP foundation, close its traceability gaps, and produce a reviewed learning architecture, learner profile, material grammar, orchestration standard, and experience gates without creating learner content.

**Architecture:** The work separates evidence claims, project decisions, design principles, material patterns, and verification methods. Machine-readable contracts live below `roadmap/v2/foundations/learning-experience/`; detailed human reasoning lives beside them as Markdown. The foundation can reach `reviewed` before content production, while `standard` remains impossible until later application and pilot evidence.

**Tech Stack:** JSON, Markdown, Python 3 `unittest`, the V2 Python validator, existing Phase-0 research records, authoritative external sources.

**Spec:** `docs/superpowers/specs/2026-09-03-ium-v2-controlled-rebaseline-design.md`

## Global Constraints

- Begin only after IUM-V2-00, IUM-V2-01, IUM-V2-CUR, and IUM-V2-SRC have passed their review gates.
- Work on `feat/ium-v2-rebaseline` after the required Git status, fetch, and fast-forward pull checks.
- Do not modify V1 research, curriculum, roadmap, module, pilot, LXP specification, or product-code files.
- Do not create learner content, module storyboards, visual designs, production components, or LXP05 code.
- Treat IUM03, the 13 `CLAIM-LP-*` records, the 15 `PRIN-*` records, the existing Fachprofil, and LXP01–LXP04 as audit inputs rather than standards.
- Keep source, claim, project decision, principle, pattern, and verification method as separate objects.
- Every empirical claim must state mechanism, learner context, scope, boundary conditions, source IDs, evidence level, and content status.
- Every design principle must state its decision basis, obligation, positive patterns, anti-patterns, observable criteria, and verification methods.
- A professional framework such as UDL or WCAG is not a domain-specific learning-effect claim.
- Do not encode universal page counts, item counts, minute limits, or age rules without direct evidence and boundary conditions.
- The maximum foundation status in this plan is `reviewed`; `standard` requires later application or pilot evidence.
- Validation must fail closed for unknown enum values, duplicate IDs, dangling required references, or status inflation.

---

### Task 1 / LXF01: Audit the existing learning and experience basis

**Files:**
- Create: `schemas/v2/legacy-learning-audit.schema.json`
- Create: `roadmap/v2/foundations/learning-experience/legacy-audit.json`
- Create: `roadmap/v2/foundations/learning-experience/legacy-audit.md`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: `CLAIM-LP-001` through `CLAIM-LP-013`, `PRIN-001` through `PRIN-015`, the current Fachprofil, and four LXP specifications
- Produces: one five-state audit decision for every required legacy input

- [x] **Step 1: Write failing completeness and status tests**

Use these exact expected sets:

```python
EXPECTED_LP_CLAIMS = {f"CLAIM-LP-{number:03d}" for number in range(1, 14)}
EXPECTED_PRINCIPLES = {f"PRIN-{number:03d}" for number in range(1, 16)}
EXPECTED_LXP_SPECS = {"LXP01", "LXP02", "LXP03", "LXP04"}
LEGACY_DECISIONS = {"retain", "adapt", "replace", "reference-only", "drop"}
```

Assert that missing IDs, duplicate IDs, unknown decisions, absent rationale, and a `retain` decision without evidence all fail.

- [x] **Step 2: Run the focused test and verify failure**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failures naming the absent learning-experience audit.

- [x] **Step 3: Create the audit schema**

Each record must contain:

```json
{
  "artifactId": "CLAIM-LP-001",
  "artifactKind": "claim",
  "artifactRef": "docs/research/phase-0/claim-ledger.json#CLAIM-LP-001",
  "decision": "adapt",
  "rationale": "Die Aussage bleibt relevant, benötigt aber im V2-Vertrag einen expliziten Wirkmechanismus, Lernendenkontext und überprüfbare Geltungsgrenzen.",
  "requirementIds": ["V2-REQ-LXF-001"],
  "evidence": ["docs/research/phase-0/curated/03-lernpsychologie-unterricht.md"],
  "successorTaskId": "LXF02"
}
```

Require `successorTaskId` for `adapt` and `replace`; require `null` for `retain`, `reference-only`, and `drop`.

- [x] **Step 4: Audit all required inputs**

Read the actual records rather than their summaries. Compare claims with source verification status and limitations; compare principles with claims; compare LXP01–LXP04 with the LXP05 failure analysis. Explicitly test these known gaps:

- six LXP01 sources are documented outside the machine-readable source register;
- existing principles omit explicit mechanism, boundary conditions, observable criteria, and method-specific verification;
- technical contract completeness could be mistaken for learning quality;
- LXP04 patterns may be too specific to the failed IUM5 composition;
- the existing Fachprofil combines strong fachliche content with only partially validated age and experience assumptions.

- [x] **Step 5: Write the human-readable audit synthesis**

Use these headings:

```text
# LXF01 Bestandsaudit
## Tragfähiger Bestand
## Anpassungsbedürftiger Bestand
## Zu ersetzende Annahmen
## Nur historische Referenz
## Entfallende Regeln
## Querschnittliche Ursachen des LXP05-Fehlschlags
## Übergabe an LXF02
```

The synthesis must distinguish evidence weakness, translation weakness, implementation weakness, and missing pilot evidence.

- [x] **Step 6: Validate and commit LXF01**

Run: `npm run verify:v2`

Expected: pass with the learning-experience foundation still below `reviewed`.

```bash
git add schemas/v2/legacy-learning-audit.schema.json roadmap/v2/foundations/learning-experience/legacy-audit.json roadmap/v2/foundations/learning-experience/legacy-audit.md scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf01): audit legacy learning experience basis"
```

### Task 2 / LXF02: Consolidate the evidence register and close priority gaps

**Files:**
- Create: `schemas/v2/learning-evidence.schema.json`
- Create: `roadmap/v2/foundations/learning-experience/evidence-register.json`
- Create: `roadmap/v2/foundations/learning-experience/evidence-synthesis.md`
- Modify: `roadmap/v2/foundations/sources/source-register.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: LXF01 decisions and the V2 source contract
- Produces: `LearningEvidenceRegisterV1` and complete source-to-claim traceability

- [x] **Step 1: Add failing evidence-contract tests**

Assert failures for a claim without `mechanism`, an empty `boundaryConditions`, an unknown source ID, `reviewed` without a primary-checked source, and a professional standard represented as `evidenceLevel: high` learning-effect evidence.

- [x] **Step 2: Run the tests and confirm the contract is absent**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failures naming the missing evidence register and validators.

- [x] **Step 3: Create the evidence schema**

Implement `LearningEvidenceClaimV2` exactly as specified, plus top-level `schemaVersion`, `asOf`, and `claims`. Restrict statuses to `draft`, `working`, `reviewed`, and `standard`; reject `standard` in this plan.

- [x] **Step 4: Normalize the six LXP01 sources into the V2 source register**

Create traceable V2 source records for:

```text
SRC-V2-LXF-SDT-2024       Wang et al. 2024, DOI 10.1016/j.lmot.2024.102015
SRC-V2-LXF-SEGMENT-2019   Rey et al. 2019, DOI 10.1007/s10648-018-9456-4
SRC-V2-LXF-SIGNAL-2016    Richter et al. 2016, DOI 10.1016/j.edurev.2015.12.003
SRC-V2-LXF-W3C-COGA-2021  W3C cognitive accessibility supplemental guidance
SRC-V2-LXF-UDL30-2024     CAST UDL Guidelines 3.0
SRC-V2-LXF-COS-2023       Feng et al. 2023, DOI 10.1016/j.compedu.2023.104864
```

Preserve their actual source kinds and do not represent W3C COGA or UDL as causal effectiveness studies.

- [x] **Step 5: Add the approved gap-check sources**

Verify and register:

```text
SRC-V2-LXF-MAYER-2024     DOI 10.1007/s10648-023-09842-1
SRC-V2-LXF-ICAP-2014      DOI 10.1080/00461520.2014.965823
SRC-V2-LXF-EEF-META-2025  EEF Metacognition and Self-Regulated Learning, second edition
SRC-V2-LXF-UDL30-2024     https://udlguidelines.cast.org/
SRC-V2-LXF-WCAG22-2024    https://www.w3.org/TR/wcag/
```

For each source, record access date, direct URL or DOI, verification status, source kind, licensing or use status, relevance, and update risk.

- [x] **Step 6: Rebuild retained and adapted claims**

For every retained or adapted LXF01 claim, create one V2 claim with:

- one bounded statement;
- the proposed cognitive, motivational, instructional, or accessibility mechanism;
- explicit learner context and transfer limits;
- only verified source IDs;
- an evidence level justified by source type and consistency;
- `working` or `reviewed` status.

Do not import numeric effect sizes unless the original publication, population, comparison, uncertainty, and heterogeneity are recorded together.

- [x] **Step 7: Write the synthesis across evidence families**

Use separate sections for learning architecture, cognitive load and multimedia, activation and task quality, support and explanation, practice and transfer, feedback and metacognition, motivation and agency, inclusion and accessibility, digital interaction, orchestration, and subject-specific boundaries.

- [x] **Step 8: Validate and commit LXF02**

Run: `npm run verify:v2`

Expected: pass; no dangling source IDs; no `standard` claim.

```bash
git add schemas/v2/learning-evidence.schema.json roadmap/v2/foundations/learning-experience/evidence-register.json roadmap/v2/foundations/learning-experience/evidence-synthesis.md roadmap/v2/foundations/sources/source-register.json scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf02): consolidate bounded learning evidence"
```

### Task 3 / LXF03: Build the IuM learner and stage profile for grades 5–7

**Files:**
- Create: `schemas/v2/learner-profile.schema.json`
- Create: `roadmap/v2/foundations/learning-experience/learner-profile.json`
- Create: `roadmap/v2/foundations/learning-experience/learner-profile.md`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: V2 evidence claims, official curriculum requirements, and the current Fachprofil audit
- Produces: a non-diagnostic, evidence-bounded profile for grades 5, 6, and 7

- [x] **Step 1: Add failing anti-stereotype and traceability tests**

Require each profile statement to include `claimIds`, `grades`, `variability`, `designConsequence`, `status`, and `limitations`. Reject statements with no evidence, stable deficit labels, click-time inferences, or a single undifferentiated `averageLearner` object.

- [x] **Step 2: Run the tests and verify the learner profile is missing**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failure naming both profile files.

- [x] **Step 3: Create the structured profile**

Cover these exact dimensions:

```text
prior-knowledge-and-conceptions
reading-and-disciplinary-language
attention-and-working-memory-load
digital-operation-routines
self-regulation-and-help-use
motivation-and-perceived-purpose
access-barriers-and-expression
classroom-collaboration-and-orchestration
```

Represent predictable variability and planning consequences; do not diagnose individuals.

- [x] **Step 4: Write the human-readable profile**

For each dimension, separate:

- evidence-supported assumptions;
- curriculum- or project-defined expectations;
- open age-specific questions;
- consequences for learner material;
- consequences for teacher orchestration;
- pilot questions.

- [x] **Step 5: Validate and commit LXF03**

Run: `npm run verify:v2`

Expected: pass with all profile statements linked to claims and grades.

```bash
git add schemas/v2/learner-profile.schema.json roadmap/v2/foundations/learning-experience/learner-profile.json roadmap/v2/foundations/learning-experience/learner-profile.md scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf03): define bounded learner profile for grades five to seven"
```

### Task 4 / LXF04: Derive the learning architecture contract

**Files:**
- Create: `schemas/v2/learning-design.schema.json`
- Create: `roadmap/v2/foundations/learning-experience/learning-architecture.json`
- Create: `roadmap/v2/foundations/learning-experience/learning-architecture.md`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: LXF02 claims, LXF03 profile, and V2 curriculum requirements
- Produces: reviewed design principles and a flexible learning-function grammar

- [x] **Step 1: Add failing principle-contract tests**

Reject a principle without claim IDs, decision basis, obligation, positive pattern, anti-pattern, observable criterion, or verification method. Reject `automated-check` as the sole verification method for a didactic principle.

- [x] **Step 2: Run the tests and confirm failure**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failures naming incomplete principles.

- [x] **Step 3: Encode the eight approved quality dimensions**

Create principles grouped under:

```text
goal-and-purpose
prior-knowledge-and-cognitive-load
disciplinary-learning-action
explanation-and-representation
task-and-support
feedback-practice-and-transfer
orientation-and-access
teacher-orchestration
```

Each group must contain at least one `required` principle and may contain bounded `conditional`, `recommended`, or `avoid` principles.

- [x] **Step 4: Encode the learning-function grammar**

Represent these functions without forcing one page per function or one universal order:

```text
orient
surface-prior-knowledge
open-disciplinary-problem
explain-or-model
guided-action
independent-application
use-feedback
secure-and-transfer
```

Require every transition to contain a pedagogical rationale and every digital interaction to name a learning function.

- [x] **Step 5: Write the architecture guide**

Explain valid order variations, the distinction between learning and performance tasks, the role of explicit instruction, the conditions for exploration, and the separation of immediate application, delayed retrieval, and transfer.

- [x] **Step 6: Validate and commit LXF04**

Run: `npm run verify:v2`

Expected: pass with no unreferenced claims and no principle verified only by automation.

```bash
git add schemas/v2/learning-design.schema.json roadmap/v2/foundations/learning-experience/learning-architecture.json roadmap/v2/foundations/learning-experience/learning-architecture.md scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf04): derive evidence bounded learning architecture"
```

### Task 5 / LXF05: Define the material and experience grammar

**Files:**
- Create: `schemas/v2/material-patterns.schema.json`
- Create: `roadmap/v2/foundations/learning-experience/material-patterns.json`
- Create: `roadmap/v2/foundations/learning-experience/material-experience-guide.md`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: reviewed LXF04 principles
- Produces: reusable patterns and anti-patterns without product components or visual styling

- [x] **Step 1: Add failing pattern traceability tests**

Reject a pattern without principle IDs, learner purpose, teacher purpose, applicability, required elements, forbidden elements, observable checks, or accessibility considerations. Reject page-count and minute-count universals that lack a claim reference.

- [x] **Step 2: Run the tests and confirm the missing-pattern failure**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failure naming `material-patterns.json`.

- [x] **Step 3: Define the minimum pattern families**

Create bounded patterns for:

```text
entry-and-orientation
worked-example-with-active-processing
linked-representations-and-signaling
prediction-execution-comparison
guided-practice-and-help
feedback-and-revision
retrieval-and-return
transfer
progress-and-reentry
accessible-alternative
```

Each pattern must explain when not to use it.

- [x] **Step 4: Write the material and experience guide**

Document coherence, signaling, spatial and temporal correspondence, purposeful segmentation, progressive disclosure, language, help proximity, state visibility, error recovery, meaningful choice, and the prohibition on decorative gamification as universal rules.

- [x] **Step 5: Review against neutral skeletons only**

Create no learner-facing module. Use three abstract walkthrough tables representing entry, central learning action, and securing/re-entry. Each table records learner question, required information, action, feedback, teacher role, barrier, and verification method.

- [x] **Step 6: Validate and commit LXF05**

Run: `npm run verify:v2`

Expected: pass; every pattern traces to reviewed principles; no product component files are added.

```bash
git add schemas/v2/material-patterns.schema.json roadmap/v2/foundations/learning-experience/material-patterns.json roadmap/v2/foundations/learning-experience/material-experience-guide.md scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf05): define material and experience grammar"
```

### Task 6 / LXF06: Define orchestration and experience gates

**Files:**
- Create: `schemas/v2/experience-gates.schema.json`
- Create: `roadmap/v2/foundations/learning-experience/teacher-orchestration.md`
- Create: `roadmap/v2/foundations/learning-experience/experience-gates.json`
- Create: `roadmap/v2/foundations/learning-experience/review-form.md`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: learner profile, learning architecture, and material patterns
- Produces: method-specific pre-production gates and teacher workflow

- [x] **Step 1: Add failing gate-method tests**

Require each gate to define `question`, `evidenceRequired`, `method`, `passCondition`, `failAction`, `ownerRole`, and `statusEffect`. Reject a didactic gate whose method is only `automated-check`; reject any gate that sets `pilot` or `standard` before real use.

- [x] **Step 2: Run the tests and verify failure**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failures naming the missing orchestration and gate artifacts.

- [x] **Step 3: Write the orchestration standard**

Cover preparation, opening, teacher modelling, individual and partner work, hold points, observation without personal telemetry, common securing, time variants, technical fallback, absent-result fallback, and re-entry.

- [x] **Step 4: Encode the gate set**

Create gates for:

```text
evidence-integrity
goal-action-evidence-alignment
cognitive-economy
disciplinary-learning-action
representation-coherence
support-without-task-removal
feedback-and-next-action
orientation-and-recovery
accessibility-and-equivalence
teacher-orchestration
privacy-and-emotional-safety
pilot-boundary
```

Map every gate to at least one principle and one non-automated review method.

- [x] **Step 5: Create the human review form**

The form must record reviewer role, artifact and commit, learner perspective, teacher perspective, observed evidence, uncertainties, decision, required changes, and explicit statement that no learning-effect claim follows from the review.

- [x] **Step 6: Validate and commit LXF06**

Run: `npm run verify:v2`

Expected: pass with `pilot: not-started` and no `standard` artifact.

```bash
git add schemas/v2/experience-gates.schema.json roadmap/v2/foundations/learning-experience/teacher-orchestration.md roadmap/v2/foundations/learning-experience/experience-gates.json roadmap/v2/foundations/learning-experience/review-form.md scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf06): define orchestration and experience gates"
```

LXF06 implementation note (2026-09-05): Gates remain definitions with `executionStatus: not-run`; the blank review form grants no approval. All twelve gates bind to reviewed LXF04 principles and LXF05 patterns. Task 7 remains closed until explicit LXF06 user approval.

### Task 7 / LXF07: Review and release the foundation at reviewed status

**Files:**
- Create: `roadmap/v2/foundations/learning-experience/validation-report.md`
- Modify: `roadmap/v2/foundations/learning-experience/status.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: all LXF01–LXF06 artifacts
- Produces: one explicit `reviewed` foundation decision or a fail-closed lower status

- [ ] **Step 1: Add failing release-gate tests**

Reject `workStatus: done` or `concept: reviewed` when any required LXF file is absent, any required reference dangles, any claim or principle is `draft`, any required gate lacks evidence, or any file claims `standard` or completed pilot evidence.

- [ ] **Step 2: Run the tests and verify the current status cannot pass**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failure listing incomplete release conditions.

- [ ] **Step 3: Perform the consistency review**

Check:

- every spec requirement has an implementing LXF artifact;
- every principle traces to claims;
- every pattern traces to principles;
- every gate names suitable evidence and method;
- learner and teacher perspectives are both represented;
- curriculum, privacy, source, governance, and accessibility boundaries do not conflict;
- no numeric or age-specific universal survives without evidence and limitations;
- neutral walkthroughs expose no unresolved structural contradiction.

- [ ] **Step 4: Write the validation report**

Use these decision sections:

```text
# LXF07 Validierungsbericht
## Prüfgegenstand und Commit
## Quellen- und Claim-Konsistenz
## Fach- und Stufenpassung
## Lernarchitektur
## Material- und Interaktionsmuster
## Lehrkraftorchestrierung
## Accessibility, Datenschutz und Sicherheit
## Neutrale Walkthroughs
## Offene Pilotfragen
## Statusentscheidung
```

The decision is `reviewed` only if every pre-production gate passes. Record pilot status as `not-started` and standardization as `not-eligible`.

- [ ] **Step 5: Update the foundation status atomically**

Set `concept: reviewed` and `workStatus: done` only in the same commit as the passing report. Keep `pilot: not-started` and `standardization: not-eligible`.

- [ ] **Step 6: Run full verification**

Run: `npm run verify:v2`

Expected: pass.

Run: `npm run test:python`

Expected: pass.

Run: `npm run typecheck`

Expected: pass.

Run: `npm run test:platform`

Expected: pass with unchanged V1 product code.

Run: `npm run verify:phase1`

Expected: pass.

Run: `npm run verify:ium5`

Expected: pass; this verifies regression safety, not LXP05 approval.

- [ ] **Step 7: Commit the reviewed foundation handoff**

```bash
git add roadmap/v2/foundations/learning-experience/validation-report.md roadmap/v2/foundations/learning-experience/status.json scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(lxf07): approve reviewed learning experience foundation"
```

## Execution-mode check

Use **Inline Execution** with `superpowers:executing-plans`. The seven tasks form a strict evidence-to-design chain and repeatedly modify the same validator, test file, source register, and foundation status. Parallel workers would either duplicate interpretation or create cross-file conflicts.
