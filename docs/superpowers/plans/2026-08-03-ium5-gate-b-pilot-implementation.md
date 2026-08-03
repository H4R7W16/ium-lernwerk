# IUM5 Gate B Pilot Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not create subagents unless the user explicitly changes the execution mode.

**Goal:** Das in `docs/superpowers/specs/2026-08-03-ium5-gate-b-pilot-design.md` definierte schlanke Gate-B-Paket für `IUM-5-CORE-05` testgetrieben implementieren: geschlossene Evidenzverträge, manuelle HTTPS-Prüffassung, druckbarer Beobachtungsbogen, Leitfäden und fail-closed Entscheidungsauswertung – ohne Pilotierung, reale Daten, LMS-Freigabe oder Statushochsetzung.

**Architecture:** Die bestehende fachliche Registry bleibt bei `production | fixture`. Ein orthogonaler `PublicationMode` steuert ausschließlich Kennzeichnung und Publikationszweck. Geschlossene JSON-Schemata und ein Python-Validator bilden technische Evidenz, zwei Unterrichtsläufe und das Entscheidungsdossier ab. Das Portal speichert oder überträgt keine Pilotdaten. Der bestehende Fixture-Pages-Workflow bleibt unverändert; eine neue manuelle Workflowdatei veröffentlicht ausschließlich den exakt geprüften IUM5-Produktionsbuild als deutlich gekennzeichnete Gate-B-Prüffassung.

**Tech Stack:** Node 22.20.0, npm 10.9.3, TypeScript 6.0.3, Astro 7.1.6, Vitest 4.1.10, Playwright 1.62.1, Python 3 Standardbibliothek, JSON Schema Draft 2020-12, GitHub Actions und GitHub Pages.

## Global Constraints

- Die schriftlich freigegebene Spezifikation `docs/superpowers/specs/2026-08-03-ium5-gate-b-pilot-design.md` steuert jeden Task. Vor ihrer ausdrücklichen Nutzerfreigabe beginnt keine Implementierung.
- Die Ausführung beginnt in einem isolierten Worktree und einem neuen Featurebranch, nicht direkt auf `main`.
- Vor Commit oder Push gelten Fetch-/Fast-forward-Regeln aus `AGENTS.md`; kein Force-Push, History-Rewrite oder manueller Eingriff in `.git/`.
- Jeder Verhaltenstask folgt TDD: roten Test schreiben, den erwarteten Fehlschlag beobachten, minimale Implementierung, grünen Test beobachten, Regressionen ausführen, diff prüfen, committen.
- Der Modulstatus bleibt in allen Dateien `working`; `docs/platform/device-verification.md` bleibt `device-verified: not-run`.
- IUM19 implementiert nur das Paket. Keine reale Prüffassung veröffentlichen, keine technischen Realgeräteevidenzen erheben und keinen Unterrichtspilot durchführen.
- Keine Namen, Konten, Schulen, Klassencodes, exakten Daten, Freitexte über Lernende, Lernprodukte, Einzelantworten, Gerätekennungen, IP-Adressen, Telemetrie, Punkte, Profile oder Geheimnisse.
- Reale Evidenzdateien bleiben außerhalb des Repositorys. Nur Schemata, Validator, Dokumentation, Druckvorlage und synthetische Beispiele werden committed.
- Kein IUM11-Cockpit, keine neue UI zur Piloterfassung und keine allgemeine Pilotplattform.
- Der bestehende Workflow `.github/workflows/device-fixture-pages.yml` wird nicht verändert.
- Die bestehende Buildprofilmenge `production | fixture` wird nicht erweitert.
- `gate-b-preview` ist ein Veröffentlichungsmodus für `production`, kein drittes Inhaltsprofil.
- Die Prüffassung ist öffentlich erreichbar, aber nicht als Produkt freigegeben. Sie enthält keine Zugangskontrolle und keine vertraulichen Inhalte.
- Alle Previewseiten tragen sichtbares Banner, `noindex,nofollow,noarchive`, vollständigen Git-SHA, Preview-ID, `working` und `not-run`.
- Keine Analytics, externen Runtime-Ressourcen, Drittanbieterrequests oder Gate-B-Zusatzspeicherung.
- Der Lernendenimpuls hat exakt drei Fragen und vier Antwortkategorien. Unter zehn gültigen Antworten wird die jeweilige Frage vollständig unterdrückt.
- Eine positive Gesamtempfehlung heißt ausschließlich `eligible-for-working-release-review` und ändert keine Produktmetadaten.
- Datenschutzverletzung oder ungelöster kritischer Befund ergibt `revise-required`; fehlende oder widersprüchliche Pflichtevidenz ergibt `not-evaluable`.
- Synthetische Beispiele verwenden ausschließlich offensichtlich fiktive Kennungen und dürfen keinen realen Schulkontext imitieren.
- Quelltexte UTF-8 ohne BOM und LF. Buildoutput, Testreports, `node_modules`, lokale Laufzeitdateien und reale Pilotpakete bleiben uncommitted.

## File Map

### Evidenz- und Entscheidungsverträge

- Create: `pilot/ium5-gate-b/protocol.json`
- Create: `pilot/ium5-gate-b/schemas/technical-evidence.schema.json`
- Create: `pilot/ium5-gate-b/schemas/pilot-evidence.schema.json`
- Create: `pilot/ium5-gate-b/schemas/decision-package.schema.json`
- Create: `pilot/ium5-gate-b/examples/technical-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/pilot-exploratory-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/pilot-confirmation-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/decision-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/decision-revise.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/decision-not-evaluable.synthetic.json`
- Create: `scripts/validate_ium5_gate_b.py`
- Test: `tests/test_validate_ium5_gate_b.py`

### Veröffentlichungsmodus und Portal

- Create: `scripts/publication-mode.ts`
- Modify: `scripts/build-portal.ts`
- Modify: `scripts/preview-portal.ts`
- Modify: `apps/lernwerk-portal/src/layouts/BaseLayout.astro`
- Modify: `apps/lernwerk-portal/src/styles/global.css`
- Create: `apps/lernwerk-portal/public/robots.txt`
- Test: `tests/platform/publication-mode.test.ts`
- Test: `tests/platform/portal-build.test.ts`
- Create: `tests/platform/ium5-gate-b-preview.test.ts`

### Workflow und Verifikation

- Create: `.github/workflows/ium5-gate-b-preview.yml`
- Modify: `package.json`
- Create: `scripts/verify-ium5-gate-b.ts`
- Modify: `.github/workflows/ci.yml`
- Modify: `tests/platform/pages-workflow.test.ts`

### Durchführung, Druck und Review

- Create: `pilot/ium5-gate-b/docs/technical-runbook.md`
- Create: `pilot/ium5-gate-b/docs/pilot-guide.md`
- Create: `pilot/ium5-gate-b/docs/review-guide.md`
- Create: `pilot/ium5-gate-b/print/observation-sheet.html`
- Create: `tests/platform/ium5-gate-b-docs.test.ts`
- Create: `tests/platform/ium5-gate-b-observation-sheet.test.ts`
- Modify: `docs/modules/ium-5-core-05.md`
- Modify: `README.md`
- Create after actual reviews: `docs/reviews/ium5-gate-b-fach-didaktik.md`
- Create after actual reviews: `docs/reviews/ium5-gate-b-engineering-accessibility-privacy.md`

## Interfaces

### TypeScript

```ts
export type PublicationMode =
  | 'development'
  | 'device-fixture'
  | 'gate-b-preview';

export type PublicationContract = Readonly<{
  profile: BuildProfile;
  mode: PublicationMode;
  buildRevision: string;
  previewId: string;
}>;

export function parsePublicationMode(value: string): PublicationMode;
export function assertPublicationCombination(
  profile: BuildProfile,
  mode: PublicationMode,
): void;
export function parseBuildRevision(value: string, mode: PublicationMode): string;
export function parsePreviewId(value: string, mode: PublicationMode): string;
```

`buildPortalToDirectory` gains required `publicationMode` and optional `previewId`; `buildRevision` remains optional only in `development` and `device-fixture`.

### Python CLI

```text
python -B scripts/validate_ium5_gate_b.py protocol
python -B scripts/validate_ium5_gate_b.py evidence PATH
python -B scripts/validate_ium5_gate_b.py decision PATH
python -B scripts/validate_ium5_gate_b.py synthetic
```

Exit `0` means structurally and semantically valid. Exit `1` means validation failure. Human-readable errors go to stderr and use JSON pointer plus stable error code. The validator writes or modifies no files.

### Decision output

```json
{
  "technicalEntry": "pass",
  "exploratoryResult": "pass",
  "confirmationResult": "pass",
  "recommendation": "eligible-for-working-release-review",
  "productStatus": "working",
  "deviceVerified": "not-run"
}
```

## Execution Checkpoints

- Checkpoint 1 after Tasks 1–3: complete closed contract, evaluator and synthetic examples.
- Checkpoint 2 after Tasks 4–6: local Previewbuild and manual workflow contract, no deployment.
- Checkpoint 3 after Tasks 7–8: complete guides, print artifact and CI wiring.
- Checkpoint 4 after Task 9: full verification and actual internal reviews; handoff for user review, still no pilot.

---

### Task 1: Gate-B-Protokoll und geschlossene Basisschemata anlegen

**Files:**
- Create: `pilot/ium5-gate-b/protocol.json`
- Create: `pilot/ium5-gate-b/schemas/technical-evidence.schema.json`
- Create: `pilot/ium5-gate-b/schemas/pilot-evidence.schema.json`
- Create: `pilot/ium5-gate-b/schemas/decision-package.schema.json`
- Test: `tests/test_validate_ium5_gate_b.py`

**Contract:**
- `protocolId`: `IUM5-GATE-B-1`
- `schemaVersion`: `1`
- `moduleId`: `IUM-5-CORE-05`
- `moduleVersion`: `0.1.0`
- `productStatus`: `working`
- `deviceVerified`: `not-run`
- exactly six technical matrix IDs;
- exactly two pilot run kinds;
- exactly nine observation criteria;
- exactly three pulse prompts;
- all schemas use `additionalProperties: false` recursively.

- [ ] **Step 1: Create the first failing protocol contract test**

```py
class ProtocolContractTests(unittest.TestCase):
    def test_protocol_seals_module_status_and_matrix(self):
        protocol = load_json(ROOT / "pilot/ium5-gate-b/protocol.json")
        self.assertEqual(protocol["protocolId"], "IUM5-GATE-B-1")
        self.assertEqual(protocol["module"], {
            "id": "IUM-5-CORE-05",
            "version": "0.1.0",
            "status": "working",
            "deviceVerified": "not-run",
        })
        self.assertEqual(
            [row["id"] for row in protocol["technicalMatrix"]],
            [
                "TECH-IPAD-TOUCH",
                "TECH-IPAD-VO",
                "TECH-DESKTOP-CHROMIUM",
                "TECH-DESKTOP-FIREFOX",
                "TECH-NET-OFFLINE-UPDATE",
                "TECH-LMS-ROUTE",
            ],
        )
```

- [ ] **Step 2: Run the test and observe the missing-file failure**

Run: `python -B -m unittest tests.test_validate_ium5_gate_b.ProtocolContractTests -v`
Expected: FAIL because `protocol.json` does not exist.

- [ ] **Step 3: Add the minimal protocol with all fixed enums and privacy rules**

Encode matrix rows, phases, observation criteria, pulse prompts, result enums, disruption codes, allowed context enums, forbidden key fragments and retention rule `30-days-after-decision`.

- [ ] **Step 4: Add schema closure tests before the schemas**

Test recursively that every object schema has explicit `additionalProperties: false`, every required field is listed in `properties`, and no schema contains a property matching:

```py
FORBIDDEN_KEYS = {
    "name", "email", "school", "classCode", "exactDate", "ipAddress",
    "macAddress", "serialNumber", "deviceId", "freeText", "score",
    "grade", "studentId", "learningProduct", "telemetry",
}
```

- [ ] **Step 5: Run the schema test and observe the expected missing-schema failure**

Run: `python -B -m unittest tests.test_validate_ium5_gate_b.SchemaContractTests -v`
Expected: FAIL on the first absent schema.

- [ ] **Step 6: Implement the three schemas minimally**

Technical schema must define build identity plus six rows. Pilot schema must define one run with closed class aggregates. Decision schema must reference one technical package, one exploratory run and one confirmation run, plus human review decisions. Do not add narrative fields.

- [ ] **Step 7: Run Task 1 tests and repository JSON parse regression**

Run:

```text
python -B -m unittest tests.test_validate_ium5_gate_b.ProtocolContractTests tests.test_validate_ium5_gate_b.SchemaContractTests -v
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: all green.

- [ ] **Step 8: Commit Task 1**

```text
git add pilot/ium5-gate-b/protocol.json pilot/ium5-gate-b/schemas tests/test_validate_ium5_gate_b.py
git commit -m "test: seal IUM5 Gate B evidence contracts"
```

---

### Task 2: Fail-closed Validator für Protokoll und Evidenz implementieren

**Files:**
- Create: `scripts/validate_ium5_gate_b.py`
- Modify: `tests/test_validate_ium5_gate_b.py`

**Interfaces:**
- `load_protocol() -> dict[str, object]`
- `validate_protocol() -> list[Issue]`
- `validate_evidence(document: object) -> list[Issue]`
- `validate_decision(document: object) -> tuple[list[Issue], dict[str, str] | None]`
- `scan_forbidden_content(value, pointer="$", issues=None) -> list[Issue]`
- `Issue(code: str, pointer: str, message: str)`

- [ ] **Step 1: Add red tests for valid and recursively invalid technical evidence**

Tests must prove rejection of unknown nested fields, a seventh matrix row, missing build revision, serial number, IP address, free prose and mismatched matrix ID. Use in-memory dictionaries, not fixtures.

- [ ] **Step 2: Run the focused tests and observe import failure**

Run: `python -B -m unittest tests.test_validate_ium5_gate_b.ValidatorTests -v`
Expected: FAIL because `scripts.validate_ium5_gate_b` does not exist.

- [ ] **Step 3: Implement a small schema engine from the Python standard library**

Support only the schema keywords used by this package: `type`, `const`, `enum`, `required`, `properties`, `additionalProperties`, `items`, `minItems`, `maxItems`, `minLength`, `maxLength`, `pattern`, `oneOf`, `$ref`. Resolve only local refs below `pilot/ium5-gate-b/schemas/`; reject remote refs.

- [ ] **Step 4: Add stable privacy scan before semantic validation**

The scan rejects forbidden keys case-insensitively and string values containing email addresses, IPv4/IPv6 candidates or 40-character secrets. It must not reject a full lowercase hexadecimal Git SHA because `buildRevision` is explicitly typed and located.

- [ ] **Step 5: Add CLI red tests**

Use `subprocess.run` to verify exit 0 for `protocol`, exit 1 and error code for a temporary invalid package, and no file changes before/after a run.

- [ ] **Step 6: Implement the four CLI commands**

`protocol` validates protocol plus schemas. `evidence PATH` validates either technical or pilot package based on `documentType`. `decision PATH` validates and evaluates. `synthetic` is added in Task 3 but currently fails with code `SYNTHETIC_EXAMPLES_MISSING`.

- [ ] **Step 7: Run tests and syntax check**

```text
python -B -m unittest tests.test_validate_ium5_gate_b.ValidatorTests tests.test_validate_ium5_gate_b.CliTests -v
python -B -m py_compile scripts/validate_ium5_gate_b.py
```

Expected: all implemented commands green; `synthetic` expected red only in its explicitly isolated future test.

- [ ] **Step 8: Commit Task 2**

```text
git add scripts/validate_ium5_gate_b.py tests/test_validate_ium5_gate_b.py
git commit -m "feat: validate IUM5 Gate B evidence fail closed"
```

---

### Task 3: Entscheidungslogik, Unterdrückung und synthetische Beispiele schließen

**Files:**
- Create: `pilot/ium5-gate-b/examples/technical-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/pilot-exploratory-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/pilot-confirmation-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/decision-pass.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/decision-revise.synthetic.json`
- Create: `pilot/ium5-gate-b/examples/decision-not-evaluable.synthetic.json`
- Modify: `scripts/validate_ium5_gate_b.py`
- Modify: `tests/test_validate_ium5_gate_b.py`

**Decision rules:**
- technical pass requires all six rows pass, same SHA/preview ID and no unresolved high/critical issue;
- pilot pass requires all phases, criteria 1–6 no `not-met`/`not-observable`, at most one `partly`, shared consolidation, time fit and no critical/privacy issue;
- positive recommendation requires technical pass, both run passes, different class, all reviews approved and deletion confirmed;
- `limited-accepted` never produces positive overall recommendation;
- privacy breach always wins over otherwise positive evidence;
- missing or contradictory evidence becomes `not-evaluable`;
- product status and device status are constants in every output.

- [ ] **Step 1: Write the decision table as parameterized red tests**

Include at least these mutations from a valid in-memory package:

```py
cases = [
    ("technical row blocked", mutate_technical_blocked, "not-evaluable"),
    ("privacy breach", mutate_privacy_breach, "revise-required"),
    ("same class", mutate_same_class, "not-evaluable"),
    ("missing confirmation", mutate_missing_confirmation, "not-evaluable"),
    ("criterion not met", mutate_criterion_not_met, "revise-required"),
    ("two partly", mutate_two_partly, "revise-required"),
    ("review rejected", mutate_review_rejected, "revise-required"),
    ("limited technical entry", mutate_limited_entry, "not-evaluable"),
]
```

- [ ] **Step 2: Observe the expected evaluator failure**

Run: `python -B -m unittest tests.test_validate_ium5_gate_b.DecisionTests -v`
Expected: FAIL because semantic evaluation is incomplete.

- [ ] **Step 3: Implement pure evaluation functions**

No timestamps, environment access or file writes. Privacy precedence is evaluated first, then completeness/consistency, then negative criteria, then positive eligibility.

- [ ] **Step 4: Add pulse suppression red tests**

For each prompt, 9 valid answers must yield only `{ "status": "suppressed" }`. Ten answers may yield category sums plus `validResponses: 10`. Mixed small counts may not leak totals.

- [ ] **Step 5: Implement and bind `normalize_pulse`**

The decision package stores already-suppressed aggregates only. The validator rejects unsuppressed totals below 10 and any attempt to include values alongside `suppressed`.

- [ ] **Step 6: Add six synthetic examples**

All examples use:

```json
{
  "buildRevision": "1111111111111111111111111111111111111111",
  "previewId": "ium5-gate-b-synthetic-001"
}
```

Pass examples must cover regular exploratory and extended confirmation paths. Negative examples differ by one decisive condition each.

- [ ] **Step 7: Make `synthetic` validate all examples and assert expected outcome**

Run:

```text
python -B scripts/validate_ium5_gate_b.py synthetic
python -B -m unittest tests.test_validate_ium5_gate_b -v
python -B -m unittest discover -s tests -p "test_*.py"
```

Expected: all green; validator prints six checked examples and three expected decision outcomes.

- [ ] **Step 8: Checkpoint 1 diff and commit**

Confirm `git diff --check`, no real context strings, no open prose fields and no file writes by validator.

```text
git add pilot/ium5-gate-b/examples scripts/validate_ium5_gate_b.py tests/test_validate_ium5_gate_b.py
git commit -m "feat: evaluate synthetic IUM5 Gate B packages"
```

---

### Task 4: Orthogonalen Veröffentlichungsmodus testgetrieben einführen

**Files:**
- Create: `scripts/publication-mode.ts`
- Modify: `scripts/build-portal.ts`
- Modify: `scripts/preview-portal.ts`
- Test: `tests/platform/publication-mode.test.ts`
- Modify: `tests/platform/portal-build.test.ts`

**Compatibility matrix:**

```ts
const ALLOWED = new Set([
  'production:development',
  'production:gate-b-preview',
  'fixture:device-fixture',
]);
```

- [ ] **Step 1: Write red unit tests for all six profile/mode pairs**

Assert the three allowed and three rejected combinations. Assert unknown mode, short SHA, nonhex SHA, missing Preview-ID and path/control characters are rejected.

- [ ] **Step 2: Run the focused unit and observe missing module failure**

Run: `npm run test:platform -- tests/platform/publication-mode.test.ts`
Expected: FAIL because `scripts/publication-mode.ts` is missing.

- [ ] **Step 3: Implement the closed parser and compatibility assertion**

For `gate-b-preview`, `buildRevision` must match `/^[0-9a-f]{40}$/` and `previewId` must match `/^ium5-gate-b-[a-z0-9-]{8,48}$/`. Development may use `stable`; device fixture retains its explicit synthetic revision.

- [ ] **Step 4: Add red integration tests for buildPortalToDirectory**

Mock/spawn boundary tests assert that the environment includes:

```text
PUBLIC_IUM_PUBLICATION_MODE=gate-b-preview
PUBLIC_IUM_BUILD_REVISION=<40-char-sha>
PUBLIC_IUM_PREVIEW_ID=ium5-gate-b-test-0001
```

and that an invalid combination fails before registry generation or Astro spawn.

- [ ] **Step 5: Thread the explicit mode through build and preview scripts**

Existing commands become explicit:

```json
{
  "build": "tsx scripts/build-portal.ts production development /",
  "build:fixture": "tsx scripts/build-portal.ts fixture device-fixture /",
  "build:fixture:subpath": "tsx scripts/build-portal.ts fixture device-fixture /ium-lernwerk/"
}
```

Add later in Task 6:

```json
"build:gate-b-preview": "tsx scripts/build-portal.ts production gate-b-preview /ium-lernwerk/"
```

- [ ] **Step 6: Run platform, type and both existing build regressions**

```text
npm run typecheck
npm run test:platform -- tests/platform/publication-mode.test.ts tests/platform/portal-build.test.ts
npm run build
npm run build:fixture
npm run build:fixture:subpath
```

Expected: green; fixture isolation unchanged.

- [ ] **Step 7: Commit Task 4**

```text
git add scripts/publication-mode.ts scripts/build-portal.ts scripts/preview-portal.ts tests/platform/publication-mode.test.ts tests/platform/portal-build.test.ts package.json
git commit -m "feat: separate portal publication modes"
```

---

### Task 5: Gate-B-Kennzeichnung und Previewbuild ausliefern

**Files:**
- Modify: `apps/lernwerk-portal/src/layouts/BaseLayout.astro`
- Modify: `apps/lernwerk-portal/src/styles/global.css`
- Create: `apps/lernwerk-portal/public/robots.txt`
- Create: `tests/platform/ium5-gate-b-preview.test.ts`
- Modify: `package.json`

**Rendered contract:**

```html
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="ium-publication-mode" content="gate-b-preview">
<meta name="ium-build-revision" content="<full sha>">
<meta name="ium-preview-id" content="ium5-gate-b-...">
<meta name="ium-product-status" content="working">
<meta name="ium-device-verified" content="not-run">
<aside data-gate-b-preview role="status">
  Gate-B-Prüffassung – keine Unterrichts- oder Produktfreigabe
</aside>
```

- [ ] **Step 1: Write red build-output tests**

Build to a temporary directory using a fixed SHA and Preview-ID. Enumerate every `.html` file and require all seven contract markers. Require `robots.txt` to contain `User-agent: *` and `Disallow: /`.

- [ ] **Step 2: Observe the absent-marker failure**

Run: `npm run test:platform -- tests/platform/ium5-gate-b-preview.test.ts`
Expected: FAIL because mode metadata and banner are absent.

- [ ] **Step 3: Add conditional metadata and the persistent banner to BaseLayout**

Read only `PUBLIC_IUM_PUBLICATION_MODE`, `PUBLIC_IUM_BUILD_REVISION` and `PUBLIC_IUM_PREVIEW_ID`. Render banner and robot meta only in `gate-b-preview`; existing development and fixture HTML remains semantically unchanged.

- [ ] **Step 4: Add accessible CSS and robots file**

Banner must remain visible at 320 CSS px and 200% zoom, not overlap skip link or focus. It cannot be dismissible. `robots.txt` is static and may also ship in other builds; this repository currently has no product release workflow.

- [ ] **Step 5: Add build script and local preview command**

```json
{
  "build:gate-b-preview": "tsx scripts/build-portal.ts production gate-b-preview /ium-lernwerk/",
  "preview:gate-b": "tsx scripts/preview-portal.ts production gate-b-preview /ium-lernwerk/ 4323"
}
```

The build command requires environment variables `IUM_BUILD_REVISION` and `IUM_PREVIEW_ID`; without them it fails.

- [ ] **Step 6: Prove profile isolation and no additional storage**

Tests must require IUM5 in Preview output, forbid `TEST-PLATFORM-REFERENCE`, scan output for analytics domains/scripts, and ensure no source code calls a Gate-B storage key or network collection endpoint.

- [ ] **Step 7: Run build, quality and browser smoke**

```text
$env:IUM_BUILD_REVISION='1111111111111111111111111111111111111111'
$env:IUM_PREVIEW_ID='ium5-gate-b-test-0001'
npm run build:gate-b-preview
npm run quality:build
npm run test:platform -- tests/platform/ium5-gate-b-preview.test.ts tests/platform/portal-build.test.ts
npm run test:ium5:browser -- --project=chromium
```

Expected: green. Clear only the two task-specific environment variables after the run.

- [ ] **Step 8: Commit Task 5**

```text
git add apps/lernwerk-portal/src/layouts/BaseLayout.astro apps/lernwerk-portal/src/styles/global.css apps/lernwerk-portal/public/robots.txt tests/platform/ium5-gate-b-preview.test.ts package.json
git commit -m "feat: mark IUM5 Gate B preview builds"
```

---

### Task 6: Manuellen GitHub-Pages-Vertrag hinzufügen

**Files:**
- Create: `.github/workflows/ium5-gate-b-preview.yml`
- Modify: `tests/platform/pages-workflow.test.ts`
- Modify: `package.json`
- Create: `scripts/verify-ium5-gate-b.ts`

**Workflow contract:**
- `workflow_dispatch` only;
- main branch only;
- boolean input `acknowledge_non_release` required and true;
- string input `preview_id` matching the closed pattern;
- exact `github.sha` as `IUM_BUILD_REVISION`;
- `npm ci`;
- `npm run verify:ium5`;
- `npm run verify:ium5:gate-b`;
- `npm run build:gate-b-preview`;
- `npm run quality:build`;
- Pages configure/upload/deploy;
- `pages: write` and `id-token: write` only in deploy job;
- concurrency group `pages`, no cancellation;
- no artifact containing real evidence;
- no automatic trigger, environment secret or status mutation.

- [ ] **Step 1: Extend workflow contract tests before creating the workflow**

Assert exact triggers, permissions, acknowledgement condition, use of `github.sha`, required commands, absence of `schedule`, `push`, `pull_request`, `workflow_run`, secrets and any command that edits `module.yaml` or device verification.

Also hash or compare the parsed existing fixture workflow against a checked-in inline semantic snapshot so a modification fails.

- [ ] **Step 2: Run the workflow test and observe missing file failure**

Run: `npm run test:platform -- tests/platform/pages-workflow.test.ts`
Expected: FAIL because the new workflow does not exist.

- [ ] **Step 3: Add the minimal manual workflow**

Use:

```yaml
jobs:
  build:
    if: >-
      github.ref == 'refs/heads/main' &&
      inputs.acknowledge_non_release == true
```

Set `IUM_BUILD_REVISION: ${{ github.sha }}` and `IUM_PREVIEW_ID: ${{ inputs.preview_id }}` only on the preview build step.

- [ ] **Step 4: Add fail-fast Gate-B verification orchestrator**

`scripts/verify-ium5-gate-b.ts` runs:

```text
npm run contracts:check
npm run typecheck
npm run check:astro
npm run test:platform
python -B scripts/validate_ium5_gate_b.py protocol
python -B scripts/validate_ium5_gate_b.py synthetic
npm run build:gate-b-preview
npm run quality:build
```

It uses the provided SHA/Preview-ID and writes no real evidence.

- [ ] **Step 5: Add package command**

```json
"verify:ium5:gate-b": "tsx scripts/verify-ium5-gate-b.ts"
```

- [ ] **Step 6: Run workflow and orchestrator contracts locally**

```text
npm run test:platform -- tests/platform/pages-workflow.test.ts tests/platform/ium5-gate-b-preview.test.ts
$env:IUM_BUILD_REVISION='1111111111111111111111111111111111111111'
$env:IUM_PREVIEW_ID='ium5-gate-b-test-0001'
npm run verify:ium5:gate-b
```

Expected: green; no deployment occurs locally.

- [ ] **Step 7: Checkpoint 2 diff and commit**

Verify the existing fixture workflow has no diff.

```text
git diff -- .github/workflows/device-fixture-pages.yml
git diff --check
git add .github/workflows/ium5-gate-b-preview.yml tests/platform/pages-workflow.test.ts scripts/verify-ium5-gate-b.ts package.json
git commit -m "ci: add manual IUM5 Gate B preview contract"
```

---

### Task 7: Technischen Runbook- und Pilotleitfaden schließen

**Files:**
- Create: `pilot/ium5-gate-b/docs/technical-runbook.md`
- Create: `pilot/ium5-gate-b/docs/pilot-guide.md`
- Create: `pilot/ium5-gate-b/docs/review-guide.md`
- Create: `tests/platform/ium5-gate-b-docs.test.ts`

**Required sections:**

Technical runbook:

```text
Purpose and non-release boundary
Authorization preflight
Exact build identity
Publish and rollback
Six-row technical matrix
Evidence hygiene
Limited exception route
Stop conditions
Deletion and handoff
```

Pilot guide:

```text
Purpose and non-efficacy boundary
Roles
Pilot-entry checklist
Exploratory regular-225 run
Repair checkpoint
Confirmation extended-270 run
Nine observations
Optional three-question pulse
Abort and fallback
Aggregation, destruction and deletion
```

Review guide:

```text
Evidence classes
Build consistency
Privacy precedence
Pass/revise/not-evaluable rules
Four-eye review sequence
Separate pilot/LMS/release decisions
Allowed final recommendation
```

- [ ] **Step 1: Write structural and wording tests first**

Tests require all sections, exact six matrix IDs, nine observation IDs, three pulse prompts, both time paths, 30-day deletion, public URL warning, and all separate decision labels.

- [ ] **Step 2: Add privacy-negative tests**

Scan guides for prohibited collection instructions such as `Name:`, `Schule:`, `Klasse:`, `Datum:`, `Freitext`, `Screenshot der Lernenden`, `IP-Adresse`, `Geräte-ID`, `Einzelantwort`. Explanations in a clearly marked `Verboten` section are permitted through exact fenced markers, not by broad substring exclusion.

- [ ] **Step 3: Observe missing-doc failures**

Run: `npm run test:platform -- tests/platform/ium5-gate-b-docs.test.ts`
Expected: FAIL for the first missing guide.

- [ ] **Step 4: Write the technical runbook as an executable checklist**

Every step names actor, input, command/action, expected evidence, failure branch and cleanup. State explicitly that this implementation task does not authorize running the publication workflow.

- [ ] **Step 5: Write the two-stage pilot guide**

Bind the first run to `regular-225`, the second to `extended-270`, require a different class, include the analog observation handoff and prohibit learner-level notes.

- [ ] **Step 6: Write the review guide with the full decision table**

Include privacy-first precedence, limited-exception behavior and the exact output `eligible-for-working-release-review`.

- [ ] **Step 7: Run docs tests and Markdown hygiene**

```text
npm run test:platform -- tests/platform/ium5-gate-b-docs.test.ts
rg -n "TO[D]O|T[B]D|FIX[M]E|PLACEH[O]LDER|noch festzulege[n]" pilot/ium5-gate-b/docs
```

Expected: test green; `rg` has no hits.

- [ ] **Step 8: Commit Task 7**

```text
git add pilot/ium5-gate-b/docs tests/platform/ium5-gate-b-docs.test.ts
git commit -m "docs: define IUM5 Gate B execution and review"
```

---

### Task 8: Medienbegründeten analogen Beobachtungsbogen umsetzen

**Files:**
- Create: `pilot/ium5-gate-b/print/observation-sheet.html`
- Create: `tests/platform/ium5-gate-b-observation-sheet.test.ts`

**Format contract:**
- self-contained HTML and CSS;
- one A4 portrait page under normal print settings;
- no script, external resource, web font or network reference;
- print title and nonrelease label;
- SHA and Preview-ID fields;
- exactly two run-kind choices;
- nine criterion rows with four closed categories;
- six phase/time rows;
- closed disruption/support/abort codes;
- no learner identifiers or open prose;
- destruction reminder;
- accessible semantic table structure in the source document.

- [ ] **Step 1: Write red DOM-contract tests**

Parse the HTML as text/DOM fixture. Assert exact checkbox/radio counts, labels, table headers, page size rule, absence of `<script>`, external URLs, text inputs for names/free prose and any learner-level field.

- [ ] **Step 2: Observe the missing-file failure**

Run: `npm run test:platform -- tests/platform/ium5-gate-b-observation-sheet.test.ts`
Expected: FAIL because the print artifact is absent.

- [ ] **Step 3: Implement semantic one-page HTML**

Use CSS `@page { size: A4 portrait; margin: 10mm; }`, system fonts, black/white-compatible borders, at least 10pt print body text and 4.5 mm check targets. Do not reduce text below the stated size to force fit.

- [ ] **Step 4: Add an explicit media rationale block to the footer**

Short wording: analog because observation attention must remain on the lesson and because the record must remain independent of the tested application; destroy after checked aggregate transfer.

- [ ] **Step 5: Render and inspect the PDF locally**

Use Chromium print-to-PDF through a focused Playwright test or existing browser runtime. Assert exactly one page, then visually inspect at 100% and 200% for clipping, unreadable codes, unchecked boxes and grayscale contrast. Store no generated PDF in the repository.

- [ ] **Step 6: Run all Gate-B docs/print tests**

```text
npm run test:platform -- tests/platform/ium5-gate-b-docs.test.ts tests/platform/ium5-gate-b-observation-sheet.test.ts
```

Expected: green.

- [ ] **Step 7: Checkpoint 3 diff and commit**

```text
git diff --check
git add pilot/ium5-gate-b/print/observation-sheet.html tests/platform/ium5-gate-b-observation-sheet.test.ts
git commit -m "feat: add privacy-safe IUM5 observation sheet"
```

---

### Task 9: CI, Dokumentation, Vollverifikation und Handoff schließen

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `docs/modules/ium-5-core-05.md`
- Modify: `README.md`
- Create: `docs/reviews/ium5-gate-b-fach-didaktik.md`
- Create: `docs/reviews/ium5-gate-b-engineering-accessibility-privacy.md`
- Modify only after all verification: workspace Task, Initiative, Kanban, Roadmap, Entwicklungshistorie and Session Summary outside the repository.

**CI rule:** Existing four jobs remain. Add Gate-B validation to `legacy` and Preview contract/build tests to `contracts-build`; do not add deployment to CI.

- [ ] **Step 1: Add CI contract tests before editing the workflow**

Extend existing workflow tests to require:

```text
python -B scripts/validate_ium5_gate_b.py protocol
python -B scripts/validate_ium5_gate_b.py synthetic
npm run build:gate-b-preview
```

and to forbid Pages deploy actions in `.github/workflows/ci.yml`.

- [ ] **Step 2: Observe CI contract failure**

Run: `npm run test:platform -- tests/platform/pages-workflow.test.ts`
Expected: FAIL because CI does not yet include Gate-B checks.

- [ ] **Step 3: Wire the smallest CI additions**

In `legacy`, run protocol and synthetic validator after Python tests. In `contracts-build`, set fixed synthetic SHA/Preview-ID and run `build:gate-b-preview`; existing `test:platform` already executes TypeScript contract tests. Keep exactly four jobs and no deployment permissions.

- [ ] **Step 4: Update module and root documentation**

Document:

- local protocol validation;
- local Previewbuild;
- public/nonrelease nature of Pages preview;
- implementation-versus-execution boundary;
- real evidence outside repo;
- rollback to fixture;
- current unchanged `working` / `not-run` state;
- separate future decisions for technical entry, pilot, LMS and release.

- [ ] **Step 5: Run the full baseline plus Gate-B verification**

```text
npm ci
npm run verify:ium5
$env:IUM_BUILD_REVISION='1111111111111111111111111111111111111111'
$env:IUM_PREVIEW_ID='ium5-gate-b-test-0001'
npm run verify:ium5:gate-b
python -B -m unittest discover -s tests -p "test_*.py"
git diff --check
git status --short
```

Expected: all commands green, only intended source/docs files changed, no generated output or real evidence.

- [ ] **Step 6: Perform actual separate internal reviews**

Fach-/Didaktikreview checks the nine observations, complete five-/six-UE path, teacher orchestration, feedback and non-efficacy boundary. Engineering-/Accessibility-/Privacyreview checks preview isolation, noindex/banner, workflow, matrix, storage/network behavior, schemas, suppression, deletion and fail-closed decision logic.

Each review document must state reviewed commit, evidence commands, findings with severity, fixes actually verified and final verdict `APPROVED`, `APPROVED AFTER FIXES` or `CHANGES REQUIRED`. Do not prewrite approval.

- [ ] **Step 7: Fix review findings test-first and rerun full verification**

Every behavioral finding gets a reproducing red test. Repeat Step 5 after fixes. A `CHANGES REQUIRED` verdict blocks handoff.

- [ ] **Step 8: Commit implementation handoff**

```text
git add .github/workflows/ci.yml docs/modules/ium-5-core-05.md README.md docs/reviews
git commit -m "docs: hand off the IUM5 Gate B package"
```

- [ ] **Step 9: Publish through a draft PR, not directly as a release**

Follow `github:yeet`: fetch, `pull --ff-only`, verify branch scope, push featurebranch, create draft PR with explicit statement that no preview has been deployed and no pilot is authorized. Wait for all PR checks.

- [ ] **Step 10: Update workspace records after remote verification**

Record branch, commit, PR, CI run, exact test totals, review verdicts and unchanged gates. Set implementation task to `review`, not `done`, until the user accepts the written implementation handoff. Keep pilot execution as a new, blocked follow-up task.

## Final Verification Checklist

- [ ] Written specification was explicitly approved before Task 1.
- [ ] No subagent or parallel implementation path was used without explicit user choice.
- [ ] All nine tasks used observed red-green TDD for behavioral changes.
- [ ] Protocol, three schemas and six synthetic examples validate.
- [ ] Recursive unknown-field and privacy scans fail closed.
- [ ] Pulse suppression below ten is regression-tested.
- [ ] `PublicationMode` is orthogonal to `BuildProfile`.
- [ ] Existing fixture workflow is byte-for-byte or semantically unchanged.
- [ ] Preview build exposes only the IUM5 production module.
- [ ] Every Preview HTML page has banner, noindex, SHA, Preview-ID, `working`, `not-run`.
- [ ] No analytics, external runtime requests or Gate-B storage was introduced.
- [ ] New Pages workflow is manual, main-only, acknowledged and least-privilege.
- [ ] CI contains no deploy job and remains four jobs.
- [ ] Technical matrix contains exactly six target rows.
- [ ] Pilot requires exploratory regular-225 and confirmation extended-270 in another class.
- [ ] Observation sheet is justified, one-page, closed, privacy-safe and visually inspected.
- [ ] No real evidence exists in Git or GitHub artifacts.
- [ ] Positive recommendation cannot mutate status or device verification.
- [ ] `module.yaml` remains `status: working`.
- [ ] `docs/platform/device-verification.md` remains `device-verified: not-run`.
- [ ] `npm run verify:ium5` passes.
- [ ] `npm run verify:ium5:gate-b` passes.
- [ ] All Python and platform tests pass.
- [ ] Both actual internal reviews are nonblocking.
- [ ] Featurebranch and draft PR CI are green.
- [ ] No real preview deployment, LMS use or pilot occurred.

## Spec Coverage Map

| Spezifikationsabschnitt | Plantask(s) |
|---|---|
| 1 Entscheidungsgrenze | 3, 7, 9 |
| 2 Normative Ausgangsbasis | 7, 9 |
| 3 Geltungsbereich | alle, besonders 7 und 9 |
| 4 Leitprinzipien | 1–3, 7–8 |
| 5 Publikationsarchitektur | 4–6 |
| 6 Gate-B-Phasen | 1–3, 7, 9 |
| 7 Fachlich-didaktischer Pilotvertrag | 1, 3, 7–8 |
| 8 Analoger Beobachtungsbogen | 8 |
| 9 Evidenzklassen | 1–3, 7 |
| 10 Datenvertrag | 1–3, 7–8 |
| 11 Ergebnislogik | 3 |
| 12 Rollen | 7, 9 |
| 13 Fehler und Nacharbeit | 1–3, 7 |
| 14 Implementierungsartefakte | 1–9 |
| 15 Automatische Qualitätsgates | 1–6, 8–9 |
| 16 Akzeptanzkriterien | 9 |
| 17 Nichtfreigaben | Global Constraints, 6, 9 |
| 18 Designabdeckung | alle |

Abdeckung: 18/18 Spezifikationsabschnitte. Es verbleibt keine absichtlich unimplementierte Spezifikationsanforderung. Die reale Durchführung ist ausdrücklich kein Implementierungsbestandteil und wird nicht als Lücke gezählt.

## Handoff State

Nach vollständiger Abarbeitung dieses Plans ist nur folgender Zustand zulässig:

```text
Gate-B package: implemented and internally reviewed
Preview publication: not run
Real technical evidence: not collected
Exploratory pilot: not run
Confirmation pilot: not run
LMS decision: not granted
Release decision: not granted
Module status: working
device-verified: not-run
Next decision: user acceptance of implementation, then separate technical-entry authorization
```
