# IUM11 Publication Contract Reset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the structurally unsound German natural-language publication parser with a deterministic publication contract, generated JSON, three byte-identical visible Markdown fact blocks, and a purely structural outside-block boundary.

**Architecture:** A new pure Python module compiles all mutable values from the validated IUM11 protocol, IUM10 result, and time model while binding the approved immutable governance constants. A separate CLI renders and atomically replaces the generated JSON and fact blocks. The IUM11 validator compares those artifacts byte-for-byte and rejects only reserved machine-readable declarations outside the blocks; it does not interpret German grammar.

**Tech Stack:** Python 3 standard library, `unittest`, JSON, Markdown, existing IUM09/IUM10/IUM11 validators, PowerShell verification commands.

## Global Constraints

- Architecture-reset review base is commit `a6bb298` on linked worktree branch `feat/ium-phase0`. Before Task 1 begins, record the documentation commit containing this plan as the implementation starting HEAD. The functional baseline remains 575 Python tests with all IUM09, IUM10, IUM11, Phase-0, cockpit-build, and Node checks green.
- The approved specification is `docs/superpowers/specs/2026-08-02-ium11-publication-contract-reset-design.md` and governs every exact field, value, marker, boundary, and acceptance criterion.
- Do not modify `roadmap/time-model.json`, `pilot/pilot-protocol.json`, either package schema, cockpit behavior, synthetic evidence packages, IUM09, or IUM10.
- Do not add dependencies, network access, telemetry, persistence, real pilot data, release state, Phase 1 work, or product-status mutations.
- All source edits use UTF-8. Generated JSON and Markdown use LF, no BOM, and exactly one final newline.
- `pilot/docs/publication-contract.json` is generated and never hand-maintained.
- The facts block markers are exactly `<!-- IUM11-PUBLICATION-CONTRACT:START -->` and `<!-- IUM11-PUBLICATION-CONTRACT:END -->`.
- The visible sentence stem `Flexible Vertiefungs-, Transfer- und Projektmodule bleiben` must remain in the generated block.
- Every task uses TDD, gets a task-specific commit, and must pass an independent review before the next task starts.
- Before every commit run `git status --short --branch`, `git fetch --prune`, and `git pull --ff-only`; if synchronization fails, do not commit or push.
- Do not push during Tasks 1–3. Re-entry into the original Task-8 review and the later branch handoff decide publication.

## File Map

- Create `scripts/ium11_publication.py`: pure compiler, deterministic renderers, block replacement/extraction, structural text boundary, and publication-specific exception.
- Create `scripts/build_ium11_publication_contract.py`: repository loader, validated compilation, expected-output calculation, per-file atomic writer, and `--check` CLI.
- Create `pilot/docs/publication-contract.json`: generated closed contract.
- Create `tests/test_ium11_publication_contract.py`: compiler, renderer, build, marker, boundary, mutation, and CLI tests.
- Modify `README.md`: generated facts block, nonduplicating explanatory prose, and build-check command.
- Modify `pilot/docs/teacher-guide.md`: generated facts block and removal of competing machine-readable declarations.
- Modify `pilot/docs/review-guide.md`: generated facts block, future decision values only inside the block, and nonduplicating prose.
- Modify `scripts/validate_ium11.py`: remove natural-language parser, integrate contract and structural boundary, update closed file map and result counts.
- Modify `tests/test_validate_ium11.py`: replace grammar matrices with generated-contract and structural-boundary integration tests.
- Modify `tests/test_validate_phase0.py`: assert the integrated repository chain still validates the generated publication contract exactly once through IUM11.

---

### Task 1: Implement the pure closed publication-contract compiler

**Files:**
- Create: `scripts/ium11_publication.py`
- Create: `tests/test_ium11_publication_contract.py`

**Interfaces:**
- Consumes: output of `validate_pilot_protocol(raw_protocol, time_model)`, the unchanged raw `time_model`, and output of `validate_ium10_repository(root)`.
- Produces: `IUM11PublicationError`, `compile_publication_contract(compiled_protocol, time_model, ium10_result) -> dict`, and public constants `PUBLICATION_CONTRACT_ID`, `PUBLICATION_CONTRACT_VERSION`, `PUBLICATION_START_MARKER`, `PUBLICATION_END_MARKER`.

- [ ] **Step 1: Add a real-repository fixture and exact compiler contract tests**

Create `tests/test_ium11_publication_contract.py` with imports and a class-level real fixture:

```python
import copy
import json
import unittest
from pathlib import Path

from scripts.ium11_publication import (
    IUM11PublicationError,
    compile_publication_contract,
)
from scripts.validate_ium10 import validate_ium10_repository
from scripts.validate_ium11 import validate_pilot_protocol

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class IUM11PublicationCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.time_model = load_json(ROOT / "roadmap/time-model.json")
        cls.ium10_result = validate_ium10_repository(ROOT)
        cls.protocol = validate_pilot_protocol(
            load_json(ROOT / "pilot/pilot-protocol.json"),
            cls.time_model,
        )

    def compile(self, protocol=None, time_model=None, ium10_result=None):
        return compile_publication_contract(
            copy.deepcopy(protocol if protocol is not None else self.protocol),
            copy.deepcopy(time_model if time_model is not None else self.time_model),
            copy.deepcopy(
                ium10_result if ium10_result is not None else self.ium10_result
            ),
        )

    def test_compiles_exact_closed_contract(self):
        contract = self.compile()
        self.assertEqual(set(contract), {
            "schemaVersion", "id", "contractVersion", "sourceBindings",
            "corePath", "privacyBoundary", "currentAxes",
            "statementBoundary", "allowedRecommendation",
            "forbiddenMaturityValues", "futureDecisionBoundary",
            "preservationBoundary", "realPilotCompleted",
            "syntheticValidationOnly",
        })
        self.assertEqual(contract["schemaVersion"], 1)
        self.assertEqual(contract["id"], "IUM11-PUBLICATION-CONTRACT")
        self.assertEqual(contract["contractVersion"], "1.0.0")
        self.assertEqual(contract["sourceBindings"], {
            "protocolPath": "pilot/pilot-protocol.json",
            "timeModelPath": "roadmap/time-model.json",
            "protocolVersion": "1.0.0",
            "toolVersion": "1.0.0",
            "timeModelFingerprintAlgorithm": "sha256-canonical-json-v1",
            "timeModelFingerprint": "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1",
        })
        self.assertEqual(contract["currentAxes"], {
            "status": "working",
            "availabilityStatus": "conditional",
            "timeFeasibilityStatus": "amber",
            "sequenceEvidenceStatus": "covered",
            "pilotStatus": "not-started",
            "semanticCoverageStatus": "partial",
        })

    def test_compiles_exact_core_and_governance_boundaries(self):
        contract = self.compile()
        self.assertEqual(contract["corePath"]["variantId"], "GRADE-7-WORKING-40")
        self.assertEqual(contract["corePath"]["targetUnits"], 40)
        self.assertEqual(contract["corePath"]["clusterCount"], 4)
        self.assertEqual(contract["corePath"]["moduleCount"], 10)
        self.assertEqual(contract["corePath"]["pilotStageCount"], 5)
        self.assertEqual(
            [
                (item["id"], item["order"], item["budgetUnits"], item["fallbackDeltaUnits"])
                for item in contract["corePath"]["clusters"]
            ],
            [
                ("CLUSTER-7-DATA-CODING", 1, 8, 3),
                ("CLUSTER-7-PROGRAMMING", 2, 11, 2),
                ("CLUSTER-7-NET-SECURITY", 3, 11, 3),
                ("CLUSTER-7-DATA-MEDIA-SOCIETY", 4, 10, 6),
            ],
        )
        self.assertEqual(contract["privacyBoundary"], {
            "minimumLearnerResponses": 10,
            "personalDataAllowed": False,
            "realPackagesInRepositoryAllowed": False,
        })
        self.assertEqual(contract["statementBoundary"], "documented-conditions-only")
        self.assertEqual(
            contract["allowedRecommendation"],
            "eligible-for-working-availability-review",
        )
        self.assertEqual(contract["forbiddenMaturityValues"], ["reviewed", "standard"])
        self.assertFalse(contract["realPilotCompleted"])
        self.assertTrue(contract["syntheticValidationOnly"])
        self.assertEqual(contract["preservationBoundary"], {
            "flexibleModulesOutsideCorePreserved": True,
            "flexibleModuleSubstitution": "forbidden",
        })
```

- [ ] **Step 2: Add fail-closed mutation and purity tests**

Add tests that mutate one source fact at a time and require `IUM11PublicationError`:

```python
    def test_rejects_source_and_ium10_drift_without_mutating_inputs(self):
        cases = []

        protocol = copy.deepcopy(self.protocol)
        protocol["timeModelFingerprint"] = "0" * 64
        cases.append((protocol, self.time_model, self.ium10_result, "fingerprint"))

        ium10_result = copy.deepcopy(self.ium10_result)
        ium10_result["gradeJudgements"][7]["pilotStatus"] = "completed"
        cases.append((self.protocol, self.time_model, ium10_result, "pilotStatus"))

        ium10_result = copy.deepcopy(self.ium10_result)
        del ium10_result["annualVariants"]["GRADE-7-WORKING-40"]["allocations"][0]
        cases.append((self.protocol, self.time_model, ium10_result, "module"))

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][1]["order"] = 1
        cases.append((protocol, self.time_model, self.ium10_result, "cluster"))

        for protocol, time_model, ium10_result, message in cases:
            with self.subTest(message=message):
                before = json.dumps(
                    [protocol, time_model, ium10_result],
                    ensure_ascii=False,
                    sort_keys=True,
                )
                with self.assertRaisesRegex(IUM11PublicationError, message):
                    compile_publication_contract(protocol, time_model, ium10_result)
                after = json.dumps(
                    [protocol, time_model, ium10_result],
                    ensure_ascii=False,
                    sort_keys=True,
                )
                self.assertEqual(after, before)
```

Add separate table-driven cases for an unsorted cluster list, a duplicated cluster module, a missing cluster module, a duplicated raw `GRADE-7-WORKING-40` variant, a missing indexed availability contract, a missing Grade-7 judgement, and a mismatch between raw time model and indexed IUM10 result. Each case must raise `IUM11PublicationError` with the affected boundary in the message.

Also assert exact nested field sets for `sourceBindings`, `corePath`, every cluster row, `privacyBoundary`, `currentAxes`, `futureDecisionBoundary`, every future row, and `preservationBoundary`.

- [ ] **Step 3: Run the new compiler tests and confirm RED**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract.IUM11PublicationCompilerTests -v
```

Expected: import failure for missing `scripts.ium11_publication` or missing public functions. Record the failing command and output in the task report before adding product code.

- [ ] **Step 4: Implement the pure compiler with exact closed helpers**

Create `scripts/ium11_publication.py` with these constants and boundaries:

```python
import hashlib
import json
import re

PUBLICATION_CONTRACT_ID = "IUM11-PUBLICATION-CONTRACT"
PUBLICATION_CONTRACT_VERSION = "1.0.0"
PUBLICATION_START_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:START -->"
PUBLICATION_END_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:END -->"
PUBLICATION_PATHS = (
    "README.md",
    "pilot/docs/teacher-guide.md",
    "pilot/docs/review-guide.md",
)
STATEMENT_BOUNDARY = "documented-conditions-only"
FUTURE_ALLOWED_CHANGES = [
    {"field": "availabilityStatus", "value": "available"},
    {"field": "timeFeasibilityStatus", "value": "green"},
    {"field": "pilotStatus", "value": "completed"},
]
UNCHANGED_AXES = [
    {"field": "status", "value": "working"},
    {"field": "semanticCoverageStatus", "value": "partial"},
]


class IUM11PublicationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM11PublicationError(message)


def _canonical_sha256(payload):
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
```

Implement `compile_publication_contract` without mutating inputs. It must:

1. require the exact source fingerprint `873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1` both computed and stored;
2. require exactly one raw `GRADE-7-WORKING-40` variant plus the identically keyed IUM10 variant, its single matching availability contract, the integer-keyed Grade-7 judgement, four ordered compiled clusters, ten unique cluster modules, and allocation equality;
3. derive `minimumLearnerResponses` from the compiled protocol and require it to be `10`; require every referenced IUM10 pilot assignment to prohibit personal data before binding `personalDataAllowed: false`;
4. require current Grade-7 axes to match the raw variant, indexed IUM10 variant, Grade-7 judgement, availability contract, and compiled protocol; the resulting values must equal the approved six-axis object;
5. derive `allowedRecommendation` and `forbiddenMaturityValues` from the compiled protocol and require their exact approved values and order;
6. require `flexible-module-substitution` in the availability contract's `forbiddenCompensations`;
7. bind `statementBoundary`, future-decision rules, preservation rule, `realPilotCompleted`, `syntheticValidationOnly`, and `realPackagesInRepositoryAllowed` as the immutable governance constants from the approved specification;
8. return this exact governance structure:

```python
"futureDecisionBoundary": {
    "requiresCommissionerDecision": True,
    "allowedChanges": FUTURE_ALLOWED_CHANGES,
    "unchangedAxes": UNCHANGED_AXES,
    "secondIndependentAnnualRunRequiredForMaturity": True,
},
"preservationBoundary": {
    "flexibleModulesOutsideCorePreserved": True,
    "flexibleModuleSubstitution": "forbidden",
},
"realPilotCompleted": False,
"syntheticValidationOnly": True,
```

- [ ] **Step 5: Run focused and regression tests**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract.IUM11PublicationCompilerTests -v
python -B -m unittest tests.test_validate_ium11 -v
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: all new compiler tests pass; the existing 575-test suite remains green because no validator call site has changed yet.

- [ ] **Step 6: Synchronize and commit Task 1**

Run:

```powershell
git status --short --branch
git fetch --prune
git pull --ff-only
git diff --check
git add scripts/ium11_publication.py tests/test_ium11_publication_contract.py
git diff --cached --check
git commit -m "feat: compile ium11 publication contract"
```

Expected: one Task-1 commit, no push, clean worktree.

---

### Task 2: Render, build, and embed deterministic publication artifacts

**Files:**
- Modify: `scripts/ium11_publication.py`
- Create: `scripts/build_ium11_publication_contract.py`
- Create: `pilot/docs/publication-contract.json`
- Modify: `README.md`
- Modify: `pilot/docs/teacher-guide.md`
- Modify: `pilot/docs/review-guide.md`
- Modify: `tests/test_ium11_publication_contract.py`

**Interfaces:**
- Consumes: `compile_publication_contract` from Task 1 and validated repository sources.
- Produces: `render_publication_contract_json`, `render_publication_markdown_block`, `extract_publication_block`, `replace_publication_block`, `validate_publication_text_boundary`, `compile_repository_publication_contract(root)`, and `build_publication_contract(root, check=False)`.

- [ ] **Step 1: Add failing renderer, marker, structural-boundary, and build tests**

Extend `tests/test_ium11_publication_contract.py` with:

```python
import subprocess
import tempfile
from unittest import mock

from scripts.ium11_publication import (
    PUBLICATION_END_MARKER,
    PUBLICATION_START_MARKER,
    extract_publication_block,
    render_publication_contract_json,
    render_publication_markdown_block,
    replace_publication_block,
    validate_publication_text_boundary,
)


class IUM11PublicationRenderTests(IUM11PublicationCompilerTests):
    def test_json_and_markdown_are_deterministic_utf8_lf(self):
        contract = self.compile()
        rendered_json = render_publication_contract_json(contract)
        rendered_block = render_publication_markdown_block(contract)
        self.assertIsInstance(rendered_json, bytes)
        self.assertFalse(rendered_json.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(rendered_json.endswith(b"\n"))
        self.assertNotIn(b"\r\n", rendered_json)
        self.assertEqual(
            json.loads(rendered_json.decode("utf-8")),
            contract,
        )
        self.assertEqual(rendered_block.count(PUBLICATION_START_MARKER), 1)
        self.assertEqual(rendered_block.count(PUBLICATION_END_MARKER), 1)
        self.assertIn("Flexible Vertiefungs-, Transfer- und Projektmodule bleiben", rendered_block)
        self.assertIn("status: working", rendered_block)
        self.assertIn("pilotStatus: not-started", rendered_block)
        self.assertIn("availabilityStatus: available", rendered_block)

    def test_marker_replacement_requires_one_ordered_pair(self):
        block = render_publication_markdown_block(self.compile())
        source = f"vor\n{PUBLICATION_START_MARKER}\nalt\n{PUBLICATION_END_MARKER}\nnach\n"
        replaced = replace_publication_block(source, block)
        self.assertEqual(extract_publication_block(replaced), block)
        for malformed in (
            "ohne marker\n",
            f"{PUBLICATION_START_MARKER}\n",
            f"{PUBLICATION_END_MARKER}\n{PUBLICATION_START_MARKER}\n",
            source + source,
        ):
            with self.subTest(malformed=malformed):
                with self.assertRaises(IUM11PublicationError):
                    replace_publication_block(malformed, block)

    def test_outside_block_boundary_is_lexical_and_readme_scoped(self):
        block = render_publication_markdown_block(self.compile())
        guide = f"# Anleitung\n\n{block}\n\nErklärende deutsche Prosa.\n"
        validate_publication_text_boundary("pilot/docs/teacher-guide.md", guide)
        reserved = (
            "Version 9.9.9", "eligible-for-standard-review",
            "status: available", "available", "GRADE-7-WORKING-40",
            "41 UE", "5 Cluster", "11 Module", "6 Pilotstufen",
            "Privacy-Schwelle 9",
        )
        for declaration in reserved:
            with self.subTest(declaration=declaration):
                with self.assertRaises(IUM11PublicationError):
                    validate_publication_text_boundary(
                        "pilot/docs/teacher-guide.md",
                        guide + declaration + "\n",
                    )

        readme = (
            "## Phase 0\nKlasse 5: available.\n\n"
            "## IUM11-Pilotinstrument\n" + block + "\nErklärende Prosa.\n\n"
            "## Zentrale Einstiege\nIUM10 ist working.\n"
        )
        validate_publication_text_boundary("README.md", readme)
```

Add a real repository build test that requires the generated JSON and all three blocks to match `compile_repository_publication_contract(ROOT)`. Add malformed-marker cases for nested markers and duplicate or missing README IUM11 section headings. Run every reserved-form case against README's IUM11 section and each guide; assert that the same literals inside the exact generated block pass. Add a subprocess test for:

```powershell
python -B scripts/build_ium11_publication_contract.py --check
```

Snapshot the four target files before and after `--check` and assert byte equality.

- [ ] **Step 2: Run render/build tests and confirm RED**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract.IUM11PublicationRenderTests -v
```

Expected: missing renderer/build functions and missing generated JSON cause failure. Record the actual RED output.

- [ ] **Step 3: Implement deterministic rendering and marker functions**

In `scripts/ium11_publication.py`, implement:

```python
def render_publication_contract_json(contract):
    return (
        json.dumps(contract, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    ).encode("utf-8")


def extract_publication_block(text):
    _require(text.count(PUBLICATION_START_MARKER) == 1, "publication start marker must occur once")
    _require(text.count(PUBLICATION_END_MARKER) == 1, "publication end marker must occur once")
    start = text.index(PUBLICATION_START_MARKER)
    end = text.index(PUBLICATION_END_MARKER)
    _require(start < end, "publication markers are out of order")
    return text[start:end + len(PUBLICATION_END_MARKER)]


def replace_publication_block(text, block):
    current = extract_publication_block(text)
    _require(block.startswith(PUBLICATION_START_MARKER), "rendered block start differs")
    _require(block.endswith(PUBLICATION_END_MARKER), "rendered block end differs")
    return text.replace(current, block, 1)
```

Render exactly this block envelope and one fixed-order GitHub Markdown table:

```markdown
<!-- IUM11-PUBLICATION-CONTRACT:START -->
<!-- Generiert aus Pilotprotokoll und Zeitmodell; nicht manuell bearbeiten. -->
| Bereich | Verbindliche Fakten |
| --- | --- |
...
<!-- IUM11-PUBLICATION-CONTRACT:END -->
```

Use these row labels and include the listed complete field groups:

1. `Vertragsbindung`: `schemaVersion`, `id`, `contractVersion`, and every `sourceBindings` field;
2. `Kernpfad`: `variantId`, `targetUnits`, `clusterCount`, `moduleCount`, and `pilotStageCount`;
3. `Clusterbudgets und Rückfälle`: every cluster's `id`, `order`, `budgetUnits`, and `fallbackDeltaUnits` in contract order;
4. `Privacygrenze`: every `privacyBoundary` field;
5. `Aktuelle Urteilachsen`: every `currentAxes` field;
6. `Aussagegrenze`: `statementBoundary`;
7. `Zulässige Empfehlung`: `allowedRecommendation`;
8. `Gesperrte Reifegrade`: every ordered `forbiddenMaturityValues` item;
9. `Spätere Auftraggeberentscheidung`: every `futureDecisionBoundary` field and every ordered child row;
10. `Reale Pilotierung`: `realPilotCompleted` and `syntheticValidationOnly`;
11. `Flexible Module`: every `preservationBoundary` field and the exact visible sentence stem `Flexible Vertiefungs-, Transfer- und Projektmodule bleiben`.

Render booleans as lowercase JSON literals, use `; ` between multiple facts in a cell, escape Markdown cell separators in dynamic values, and do not introduce HTML other than the two markers and generated-warning comment.

- [ ] **Step 4: Implement the non-semantic structural boundary**

In `validate_publication_text_boundary`:

1. extract and remove exactly one generated block;
2. for README, isolate exactly one `## IUM11-Pilotinstrument` section ending at the next level-2 heading;
3. for each guide, inspect all remaining text;
4. reject these case-insensitive reserved forms without considering negation or sentence structure:

```python
RESERVED_OUTSIDE_BLOCK_PATTERNS = (
    re.compile(r"\b[0-9]+\.[0-9]+\.[0-9]+\b"),
    re.compile(r"\beligible-for-[a-z0-9-]+\b", re.IGNORECASE),
    re.compile(
        r"\b(?:status|availabilityStatus|timeFeasibilityStatus|"
        r"sequenceEvidenceStatus|pilotStatus|semanticCoverageStatus)\s*:",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:working|available|unavailable|reviewed|standard|conditional|"
        r"green|amber|red|covered|not-started|partial|completed|"
        r"documented-conditions-only)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bGRADE-7-WORKING-40\b", re.IGNORECASE),
    re.compile(r"\b[0-9]+\s*UE\b", re.IGNORECASE),
    re.compile(r"\b[0-9]+\s*(?:Cluster|Module?|Pilotstufen?)\b", re.IGNORECASE),
    re.compile(r"\bPrivacy-?Schwelle\s*:?[ ]*[0-9]+\b", re.IGNORECASE),
)
```

The function raises `IUM11PublicationError` with the relative path and the matching reserved form. It must not inspect words such as `nicht`, `obwohl`, `und`, `oder`, `sondern`, or German forms of `abgeschlossen`.

- [ ] **Step 5: Implement the repository build CLI and per-file atomic writes**

Create `scripts/build_ium11_publication_contract.py` with:

```python
import argparse
import json
import os
import tempfile
from pathlib import Path

try:
    from .ium11_publication import (
        PUBLICATION_PATHS,
        compile_publication_contract,
        render_publication_contract_json,
        render_publication_markdown_block,
        replace_publication_block,
    )
    from .validate_ium10 import validate_ium10_repository
    from .validate_ium11 import validate_pilot_protocol
except ImportError:
    from ium11_publication import (
        PUBLICATION_PATHS,
        compile_publication_contract,
        render_publication_contract_json,
        render_publication_markdown_block,
        replace_publication_block,
    )
    from validate_ium10 import validate_ium10_repository
    from validate_ium11 import validate_pilot_protocol

CONTRACT_PATH = "pilot/docs/publication-contract.json"
```

Expose:

```python
def compile_repository_publication_contract(root): ...
def expected_publication_outputs(root): ...  # dict[Path, bytes]
def build_publication_contract(root, check=False): ...
def main(argv=None): ...
```

`expected_publication_outputs` loads and validates the repository, renders all four outputs before writing, and returns absolute target paths in fixed order: generated JSON, README, teacher guide, review guide. `_write_replace_atomic(path, payload)` uses `tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)`, writes binary bytes through the returned descriptor, flushes, calls `os.fsync`, and finishes with `os.replace`; it removes the temporary file in `finally`.

In `check=True`, compare all four expected byte payloads without opening a write handle and raise one aggregate `IUM11PublicationError` listing every drifted target.

- [ ] **Step 6: Insert marker pairs, remove competing literals, and generate artifacts**

Use `apply_patch` to insert exactly one empty marker pair near the top of each publication. Rewrite only contract-bearing prose so all reserved forms in the IUM11 README section and both guides occur inside the generated block. Preserve execution instructions, privacy/retention rules, `fail`/`not-evaluable` behavior, review questions, and the sentence stem about flexible modules.

Then run:

```powershell
python -B scripts/build_ium11_publication_contract.py
python -B scripts/build_ium11_publication_contract.py --check
```

Expected: `pilot/docs/publication-contract.json` exists; all three extracted blocks are byte-identical; the second command exits 0 and changes no file. Run the normal build a second time in the temporary-fixture test and assert byte-for-byte idempotence of all four outputs.

- [ ] **Step 7: Test interrupted multi-file replacement detection**

Patch `os.replace` in a temporary copied publication fixture so the second replacement raises `OSError`. Assert:

- no target file contains partial bytes;
- no `.tmp` file remains;
- a subsequent check reports all drifted paths;
- a normal rebuild restores a fully green check.

Do not claim a cross-file transaction; only each individual target replacement is atomic.

- [ ] **Step 8: Run focused and full verification**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract -v
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/app.js
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: all new build tests and the existing full suite pass.

- [ ] **Step 9: Synchronize and commit Task 2**

Run:

```powershell
git status --short --branch
git fetch --prune
git pull --ff-only
git diff --check
git add scripts/ium11_publication.py scripts/build_ium11_publication_contract.py pilot/docs/publication-contract.json README.md pilot/docs/teacher-guide.md pilot/docs/review-guide.md tests/test_ium11_publication_contract.py
git diff --cached --check
git commit -m "docs: generate ium11 publication facts"
```

Expected: one Task-2 commit, no push, clean worktree.

---

### Task 3: Replace the IUM11 parser boundary and re-enter the original Task-8 gate

**Files:**
- Modify: `scripts/validate_ium11.py`
- Modify: `tests/test_validate_ium11.py`
- Modify: `tests/test_validate_phase0.py`
- Modify: `README.md`
- Test: `tests/test_ium11_publication_contract.py`

**Interfaces:**
- Consumes: pure compiler/render/boundary functions and generated artifacts from Tasks 1–2.
- Produces: `_validate_publication_contract(root, compiled_protocol, time_model, ium10_result) -> dict` with exact result `{"productFiles": 27, "syntheticExamples": 7, "publications": 3, "publicationContracts": 1}` and a fully integrated Phase-0 path.

- [ ] **Step 1: Replace grammar-matrix tests with failing validator-integration tests**

In `tests/test_validate_ium11.py`:

1. update `copy_publication_fixture` to include `scripts/ium11_publication.py`, `scripts/build_ium11_publication_contract.py`, `tests/test_ium11_publication_contract.py`, and the new reset spec;
2. change `_validate_publication_contract` calls to pass `self.time_model` and `self.ium10_result` in addition to `self.protocol`;
3. update the expected result to:

```python
{
    "productFiles": 27,
    "syntheticExamples": 7,
    "publications": 3,
    "publicationContracts": 1,
}
```

4. delete both long natural-language conflict/counterexample matrices;
5. add exact integration tests for JSON tampering, block tampering, missing marker, duplicate marker, reserved literal outside the block, a German subordinate clause that contains no reserved machine literal, and README scoping.

Use these core assertions:

```python
def test_publication_contract_rejects_generated_json_and_block_drift(self):
    mutations = (
        ("pilot/docs/publication-contract.json", b'{}\n'),
        ("pilot/docs/teacher-guide.md", b"marker drift"),
    )
    for relative_path, replacement in mutations:
        with self.subTest(relative_path=relative_path):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.copy_publication_fixture(root)
                target = root / relative_path
                if relative_path.endswith(".json"):
                    target.write_bytes(replacement)
                else:
                    target.write_text(
                        target.read_text(encoding="utf-8").replace(
                            "<!-- IUM11-PUBLICATION-CONTRACT:START -->",
                            "<!-- IUM11-PUBLICATION-CONTRACT:BROKEN -->",
                            1,
                        ),
                        encoding="utf-8",
                    )
                with self.assertRaises(IUM11ValidationError):
                    validate_ium11_script._validate_publication_contract(
                        root,
                        self.protocol,
                        self.time_model,
                        self.ium10_result,
                    )


def test_publication_boundary_does_not_parse_german_grammar(self):
    sentence = "Die Pilotierung ist nicht beendet, obwohl das Fachreview beendet ist."
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        self.copy_publication_fixture(root)
        guide = root / "pilot/docs/teacher-guide.md"
        guide.write_text(
            guide.read_text(encoding="utf-8") + "\n" + sentence + "\n",
            encoding="utf-8",
        )
        validate_ium11_script._validate_publication_contract(
            root,
            self.protocol,
            self.time_model,
            self.ium10_result,
        )
```

- [ ] **Step 2: Run the new integration tests and confirm RED**

Run:

```powershell
python -B -m unittest tests.test_validate_ium11.IUM11PublicationTests -v
```

Expected: old function signature/result and old parser behavior cause failures. Record the actual RED output.

- [ ] **Step 3: Remove the natural-language parser and integrate the generated contract**

In `scripts/validate_ium11.py`:

- remove `PUBLICATION_DECLARATION_CONTRACTS`;
- remove `_validate_publication_declarations` and every nested normalization, clause, polarity, subject, and grammar helper;
- remove imports used only by that parser;
- import from `ium11_publication` using the repository's package/nonpackage fallback pattern:

```python
from .ium11_publication import (
    IUM11PublicationError,
    PUBLICATION_PATHS,
    compile_publication_contract,
    extract_publication_block,
    render_publication_contract_json,
    render_publication_markdown_block,
    validate_publication_text_boundary,
)
```

- change `_validate_publication_contract` to compile the expected contract, compare exact JSON bytes, compare each exact extracted block, and run the structural boundary;
- catch `IUM11PublicationError` only at the IUM11 validator boundary and rethrow `IUM11ValidationError` with the original message;
- add `pilot/docs/publication-contract.json`, `scripts/ium11_publication.py`, `scripts/build_ium11_publication_contract.py`, and `tests/test_ium11_publication_contract.py` to the existing 23-entry exact product map, yielding exactly 27 product files;
- add `pilot/docs/publication-contract.json` to the exact allowed pilot JSON set;
- pass `time_model` and `ium10_result` from `validate_ium11` to `_validate_publication_contract`.

No validator code may inspect German negation, conjunction, clause order, subject inheritance, or prose truth conditions.

- [ ] **Step 4: Update publication content tests and README commands**

Keep the existing content anchors for privacy, retention, repeat rules, separated reviews, and flexible modules. Change status/version/count assertions to parse `pilot/docs/publication-contract.json` and compare the three exact blocks.

Add this command to README's validation block:

```powershell
python -B scripts/build_ium11_publication_contract.py --check
```

Assert it appears exactly once and before `python -B scripts/validate_ium11.py`.

- [ ] **Step 5: Strengthen the Phase-0 integration test without another validator call**

In `tests/test_validate_phase0.py`, retain call order `ium10`, `ium09`, `ium11`. Capture `validate_ium11 = validate_phase0_script.validate_ium11` before entering the patch context. Make the patched recorder delegate once to that captured real function and store its result:

```python
def record_ium11(*args, **kwargs):
    call_order.append("ium11")
    result = validate_ium11(*args, **kwargs)
    ium11_results.append(result)
    return result
```

Then assert:

```python
self.assertEqual(
    ium11_results[0]["publication"],
    {
        "productFiles": 27,
        "syntheticExamples": 7,
        "publications": 3,
        "publicationContracts": 1,
    },
)
```

Keep `validate_ium11_mock.assert_called_once()` and assert `ium11_results` has one entry. This delegates the one intercepted orchestration call to the real validator, reuses the IUM10 result already produced by Phase 0, and must not invoke `validate_ium11_repository` or IUM10 a second time.

- [ ] **Step 6: Run focused migration verification**

Run:

```powershell
python -B -m unittest tests.test_ium11_publication_contract -v
python -B -m unittest tests.test_validate_ium11.IUM11PublicationTests -v
python -B -m unittest tests.test_validate_phase0.CoverageRepositoryTests -v
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/protocol.js
node --check pilot/cockpit/assets/app.js
```

Expected: compiler, artifacts, boundaries, IUM11 publication integration, Phase-0 orchestration, cockpit build, and Node syntax all pass.

- [ ] **Step 7: Run full repository verification**

Run:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/validate_ium11.py
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
git diff --check
```

Expected: the full test count is greater than 575 with zero failures and zero skips; all four CLIs exit 0; no real packages or status mutations appear.

- [ ] **Step 8: Synchronize and commit Task 3**

Run:

```powershell
git status --short --branch
git fetch --prune
git pull --ff-only
git diff --check
git add README.md scripts/validate_ium11.py tests/test_validate_ium11.py tests/test_validate_phase0.py
git diff --cached --check
git commit -m "refactor: replace ium11 publication parser"
```

Expected: one Task-3 commit, no push, clean worktree.

---

## Post-Plan Re-entry Gate

After all three reset tasks and their independent reviews are clean:

1. run the reset plan's final whole-diff review from base `a6bb298` to current HEAD;
2. run one fresh original Task-8 review over `d5fcdd636d38d3dbd0757b27bd3baa51f2518c3d..HEAD`, reading both the original Task-8 brief and the approved reset specification;
3. require explicit confirmation that teacher/review processes, README boundary, Phase-0 integration, generated publication contract, and structural text boundary are all compliant;
4. append the reset commits and clean review verdict to the original SDD ledger, replace the earlier `BLOCKED` terminal state with a documented architecture-reset resolution entry without deleting history, and then append `Task 8: complete`;
5. update the original ten-task plan so Task 8 is complete and Task 9 is in progress;
6. continue with the already planned independent Fachreview; do not begin real pilot work, status mutation, release, or Phase 1.

If either final review reports a load-bearing finding, follow that plan's single final-fix wave and breaker rules. Do not silently park a structural publication-boundary defect.
