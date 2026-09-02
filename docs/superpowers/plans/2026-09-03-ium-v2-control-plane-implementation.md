# IuM-Lernwerk V2 Control Plane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Choose superpowers:subagent-driven-development only when the task graph passes the execution-mode check below; otherwise use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the immutable V1 reference, V2 status model, requirements register, schemas, and fail-closed validation needed to control the re-baseline without changing V1 curriculum, roadmap, modules, or product code.

**Architecture:** V1 remains at its existing paths and is addressed by full Git SHA. New machine-readable state lives only below `roadmap/v2/` and is validated by one focused Python validator. JSON Schemas document the public contracts; Python tests enforce cross-file invariants that JSON Schema alone cannot express.

**Tech Stack:** Python 3 `unittest`, JSON, JSON Schema documents, npm script integration, Git.

**Spec:** `docs/superpowers/specs/2026-09-03-ium-v2-controlled-rebaseline-design.md`

## Global Constraints

- Work on `feat/ium-v2-rebaseline` after `git status --short --branch`, `git fetch --prune`, and `git pull --ff-only` have succeeded.
- Treat `main` at `dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0` as the initial V1 product baseline.
- Treat `origin/feat/lxp05-ium5-experience` at `645a1d4ea3c786b08e1320954b522edf86dc9f83` as a frozen, unmerged candidate.
- Do not modify existing V1 files below `curriculum/`, `modules/`, `pilot/`, or the current `roadmap/*.json` and `roadmap/*.md` files.
- Do not create learner content, restart LXP05, merge, push, host, or publish.
- Use German UTF-8 text with real umlauts; technical IDs and filenames remain ASCII.
- Keep curriculum coverage, concept, implementation, verification, review, pilot, and release as separate axes.
- Do not calculate a total progress percentage or overall traffic-light status.
- All references used as required evidence must be repository-relative paths, full Git SHAs, DOI URLs, public URLs, or Vault note names; never store absolute local paths.

---

### Task 1: Establish the V2 validator boundary

**Files:**
- Create: `scripts/validate_v2_rebaseline.py`
- Create: `tests/test_validate_v2_rebaseline.py`
- Modify: `package.json`

**Interfaces:**
- Consumes: repository root inferred from `Path(__file__).resolve().parents[1]`
- Produces: `validate_repository(root: Path) -> list[str]`, `main() -> int`, and npm command `verify:v2`

- [ ] **Step 1: Write the failing missing-contract test**

```python
from pathlib import Path
import tempfile
import unittest

from scripts.validate_v2_rebaseline import validate_repository


class ValidateV2RebaselineTests(unittest.TestCase):
    def test_missing_control_files_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))
        self.assertIn("roadmap/v2/status.json fehlt", errors)
        self.assertIn("roadmap/v2/archive/v1-baseline.json fehlt", errors)
        self.assertIn("roadmap/v2/requirements/requirements.json fehlt", errors)
```

- [ ] **Step 2: Run the focused test and confirm the import fails**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline.ValidateV2RebaselineTests.test_missing_control_files_fail_closed -v`

Expected: `ERROR` with `ModuleNotFoundError: No module named 'scripts.validate_v2_rebaseline'`.

- [ ] **Step 3: Add the minimal validator module**

```python
from __future__ import annotations

import json
from pathlib import Path


CONTROL_FILES = (
    Path("roadmap/v2/status.json"),
    Path("roadmap/v2/archive/v1-baseline.json"),
    Path("roadmap/v2/requirements/requirements.json"),
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_repository(root: Path) -> list[str]:
    return [f"{path.as_posix()} fehlt" for path in CONTROL_FILES if not (root / path).is_file()]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("V2 re-baseline validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add the npm entry point**

Insert in `package.json` under `scripts`:

```json
"verify:v2": "python -B scripts/validate_v2_rebaseline.py"
```

- [ ] **Step 5: Run the focused test and full Python baseline**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: `OK`.

Run: `npm run test:python`

Expected: the existing Python suite remains green.

- [ ] **Step 6: Commit the validator boundary**

```bash
git add scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py package.json
git commit -m "test(v2): establish rebaseline validator boundary"
```

### Task 2: Seal the V1 baseline and declare V2 building state

**Files:**
- Create: `schemas/v2/status.schema.json`
- Create: `schemas/v2/archive.schema.json`
- Create: `roadmap/v2/status.json`
- Create: `roadmap/v2/archive/v1-baseline.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: full SHAs for `main` and the LXP05 candidate; `git cat-file -e <sha>^{commit}`
- Produces: `V2StatusV1`, `V1ArchiveManifestV1`, and cross-file status invariants

- [ ] **Step 1: Add failing tests for immutable baseline semantics**

Add tests that build temporary JSON files and assert these exact failures:

```python
self.assertIn("activeBaseline muss v1 sein, solange v2State building ist", errors)
self.assertIn("contentProduction muss frozen sein", errors)
self.assertIn("LXP05 muss frozen und unmerged bleiben", errors)
self.assertIn("V1 mainCommit muss eine vollständige 40-stellige SHA sein", errors)
```

- [ ] **Step 2: Run the tests and verify they fail because semantic validation is absent**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: at least four assertion failures for the missing semantic errors.

- [ ] **Step 3: Create the schemas**

Define `V2StatusV1` with these required values:

```json
{
  "schemaVersion": 1,
  "projectId": "ium-lernwerk",
  "activeBaseline": "v1",
  "v2State": "building",
  "contentProduction": "frozen",
  "lxp05": {"state": "frozen", "integration": "unmerged"},
  "cutover": {"state": "not-approved"}
}
```

Define `V1ArchiveManifestV1` with `repository`, `remote`, `mainCommit`, `candidateRefs`, `artifactRoots`, `capturedAt`, and `limitations`. Require full 40-character lowercase hexadecimal SHAs.

- [ ] **Step 4: Create the real status and archive records**

Use these verified commits:

```json
{
  "mainCommit": "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0",
  "candidateRefs": [
    {
      "ref": "origin/feat/lxp05-ium5-experience",
      "commit": "645a1d4ea3c786b08e1320954b522edf86dc9f83",
      "role": "historical-unmerged-review-candidate"
    }
  ]
}
```

Record `07bc15e1e70d` only in `limitations` as an unverified Vault-reported local dashboard commit. Do not create a GitHub URL for it.

- [ ] **Step 5: Implement status and archive validation**

Add `validate_status(data: object) -> list[str]` and `validate_archive(data: object) -> list[str]`. Enforce exact enum values, full SHAs, repository-relative artifact roots, and the `building → activeBaseline: v1` invariant.

- [ ] **Step 6: Verify the files and Git objects**

Run: `npm run verify:v2`

Expected: failure only because the requirements file does not yet exist.

Run: `git cat-file -e dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0^{commit}`

Expected: exit code `0`.

Run: `git cat-file -e 645a1d4ea3c786b08e1320954b522edf86dc9f83^{commit}`

Expected: exit code `0`.

- [ ] **Step 7: Commit the immutable control state**

```bash
git add schemas/v2/status.schema.json schemas/v2/archive.schema.json roadmap/v2/status.json roadmap/v2/archive/v1-baseline.json scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "feat(v2): seal v1 baseline and declare rebuilding state"
```

### Task 3: Add the requirements-first contract

**Files:**
- Create: `schemas/v2/requirements.schema.json`
- Create: `roadmap/v2/requirements/requirements.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: domains, bindings, scopes, fulfillment modes, and evidence pointer rules from the specification
- Produces: `V2RequirementsV1` with unique IDs and acyclic dependencies

- [ ] **Step 1: Add failing tests for contract errors**

Create fixtures in memory and assert exact failures for:

```text
doppelte Anforderungs-ID V2-REQ-001
unbekannte Domäne ui-decoration
Pflichtreferenz ohne Ziel in V2-REQ-001
unbekannte Abhängigkeit V2-REQ-999
zyklische Anforderungsabhängigkeit V2-REQ-001 -> V2-REQ-002 -> V2-REQ-001
```

- [ ] **Step 2: Run the tests and confirm the new assertions fail**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failures for duplicate, enum, evidence, unknown dependency, and cycle checks.

- [ ] **Step 3: Create the requirements schema**

Encode the exact enums from section 5 of the spec. Require nonempty `title`, `statement`, `origin`, `grades`, `fulfillmentModes`, `risks`, and `gate`. Restrict grades to `5`, `6`, and `7` and set `additionalProperties: false` on every contract object.

- [ ] **Step 4: Seed the register with approved cross-cutting requirements**

Create explicit records for these decisions:

```text
V2-REQ-SYS-001  V1 and V2 remain separated until cutover
V2-REQ-SYS-002  content production remains frozen
V2-REQ-CUR-001  official curriculum and orientation sources remain distinct
V2-REQ-CUR-002  curriculum fulfillment supports direct, integrated, and cross-cutting modes
V2-REQ-SRC-001  source, claim, decision, pattern, and verification remain traceable
V2-REQ-LXF-001  the full learning architecture is governed by the experience foundation
V2-REQ-GOV-001  public claims are bound to their minimum evidence
V2-REQ-DASH-001 dashboard exposes V1, V2, frozen LXP05, dates, commits, and evidence without a total percentage
```

Set unresolved fulfillment to `unassessed`; do not infer implementation or coverage from V1.

- [ ] **Step 5: Implement requirements validation**

Add `validate_requirements(data: object) -> list[str]` and a deterministic depth-first dependency cycle check. Validate required repository paths against the supplied root, but allow optional missing historical Vault references to return warnings instead of errors.

- [ ] **Step 6: Run the V2 and regression suites**

Run: `npm run verify:v2`

Expected: `V2 re-baseline validation passed`.

Run: `npm run test:python`

Expected: all tests pass.

- [ ] **Step 7: Commit the requirements contract**

```bash
git add schemas/v2/requirements.schema.json roadmap/v2/requirements/requirements.json scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "feat(v2): add requirements-first control contract"
```

### Task 4: Create foundation and reuse-audit boundaries without changing decisions

**Files:**
- Create: `schemas/v2/foundation-status.schema.json`
- Create: `schemas/v2/artifact-reuse.schema.json`
- Create: `roadmap/v2/foundations/curriculum/status.json`
- Create: `roadmap/v2/foundations/sources/status.json`
- Create: `roadmap/v2/foundations/learning-experience/status.json`
- Create: `roadmap/v2/foundations/governance/status.json`
- Create: `roadmap/v2/audits/artifact-inventory.json`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: V2 requirement IDs and the legacy task range IUM00–IUM20 plus LXP01–LXP04
- Produces: four explicit foundation gates and a complete inventory awaiting five-state decisions

- [ ] **Step 1: Add failing completeness tests**

Assert that validation fails if a required foundation is missing or if the inventory omits any ID in these exact sets:

```python
EXPECTED_IUM = {f"IUM{number:02d}" for number in range(21)}
EXPECTED_LXP = {f"LXP{number:02d}" for number in range(1, 5)}
EXPECTED_FOUNDATIONS = {"curriculum", "sources", "learning-experience", "governance"}
```

- [ ] **Step 2: Run the tests and confirm incomplete inventories fail**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failures naming missing foundation and artifact IDs.

- [ ] **Step 3: Create the foundation status schema and records**

Each record must contain `schemaVersion`, `id`, `workStatus`, separate maturity axes, `requirementIds`, `evidence`, `openQuestions`, and `nextGate`. Set all four foundations to an honest initial state; do not mark them complete merely because V1 artifacts exist.

- [ ] **Step 4: Create the reuse schema and complete inventory**

The inventory lists IUM00–IUM20 and LXP01–LXP04 with repository-relative evidence pointers and `auditState: "not-assessed"`. The five final decisions are `retain`, `adapt`, `replace`, `reference-only`, and `drop`; no final decision is populated before IUM-V2-AUD.

- [ ] **Step 5: Implement cross-file validation**

Enforce:

- every foundation requirement ID exists;
- every inventory artifact ID is unique and present exactly once;
- LXP05 is rejected from the reusable artifact inventory;
- no final reuse decision is accepted without rationale, requirement IDs, evidence, and a successor task when the decision is `adapt` or `replace`.

- [ ] **Step 6: Verify and commit the boundaries**

Run: `npm run verify:v2`

Expected: pass with explicit non-blocking warnings for unassessed foundations and artifacts.

```bash
git add schemas/v2/foundation-status.schema.json schemas/v2/artifact-reuse.schema.json roadmap/v2/foundations roadmap/v2/audits/artifact-inventory.json scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "feat(v2): define foundation and reuse audit boundaries"
```

### Task 5: Document operation and preserve regression safety

**Files:**
- Create: `roadmap/v2/README.md`
- Modify: `README.md`
- Modify: `scripts/validate_v2_rebaseline.py`
- Modify: `tests/test_validate_v2_rebaseline.py`

**Interfaces:**
- Consumes: all control-plane contracts from Tasks 1–4
- Produces: operator documentation and a single deterministic verification entry point

- [ ] **Step 1: Add a failing documentation test**

Require `roadmap/v2/README.md` to contain these exact headings:

```text
# IuM-Lernwerk V2 Re-Baseline
## Aktiver Stand
## V1-Archiv
## Sequenz
## Statusgrenzen
## Validierung
## Nicht freigegeben
```

- [ ] **Step 2: Run the documentation test and verify it fails**

Run: `python -B -m unittest tests.test_validate_v2_rebaseline -v`

Expected: failure naming the missing README.

- [ ] **Step 3: Write the operator README**

Document the exact sequence from IUM-V2-00 through IUM-V2-CUT, the `npm run verify:v2` command, the V1 immutability rule, the content freeze, the LXP05 boundary, and the rule that `reviewed` is the maximum pre-production status for the learning-experience foundation.

- [ ] **Step 4: Add a short root README pointer**

Add a section linking to the V2 design spec and `roadmap/v2/README.md`. State that existing roadmap files remain V1 historical evidence until an explicit cutover.

- [ ] **Step 5: Run all proportionate verification**

Run: `npm run verify:v2`

Expected: pass.

Run: `npm run test:python`

Expected: pass.

Run: `npm run typecheck`

Expected: pass.

Run: `npm run test:platform`

Expected: pass.

Run: `npm run verify:phase1`

Expected: pass.

Run: `npm run verify:ium5`

Expected: pass on the unchanged V1 product baseline.

- [ ] **Step 6: Commit the control-plane handoff**

```bash
git add roadmap/v2/README.md README.md scripts/validate_v2_rebaseline.py tests/test_validate_v2_rebaseline.py
git commit -m "docs(v2): hand off controlled rebaseline workflow"
```

## Execution-mode check

Use **Inline Execution** with `superpowers:executing-plans`. The tasks write to the same validator, test file, V2 contract tree, and branch; each checkpoint depends on the preceding schema and therefore does not meet the safe parallel-delegation criteria.
