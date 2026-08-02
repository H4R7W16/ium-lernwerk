import copy
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from scripts.validate_ium11 import (
    IUM11ValidationError,
    derive_annual_result,
    derive_cluster_result,
    evaluate_learner_pulse,
    validate_evidence_package,
    validate_pilot_protocol,
)


ROOT = Path(__file__).resolve().parents[1]


class CockpitHTMLParser(HTMLParser):
    CONTROL_TAGS = {"input", "select", "textarea"}
    INTERACTIVE_TAGS = {"a", "button", "details", "input", "select", "summary", "textarea"}

    def __init__(self):
        super().__init__()
        self.elements = []
        self.label_targets = set()
        self.controls = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if tag == "label" and attributes.get("for"):
            self.label_targets.add(attributes["for"])
        if tag in self.CONTROL_TAGS and attributes.get("type") != "hidden":
            self.controls.append((tag, attributes))

    def count(self, tag):
        return sum(element_tag == tag for element_tag, _ in self.elements)

    def has_element(self, *, id, attributes=None):
        required = attributes or {}
        return any(
            values.get("id") == id
            and all(values.get(name) == value for name, value in required.items())
            for _, values in self.elements
        )

    def labels_cover_all_controls(self):
        return all(
            attributes.get("id")
            and (
                attributes["id"] in self.label_targets
                or "aria-label" in attributes
                or "aria-labelledby" in attributes
            )
            for _, attributes in self.controls
        )

    def has_positive_tabindex(self):
        return any(
            attributes.get("tabindex", "").lstrip("+").isdigit()
            and int(attributes["tabindex"]) > 0
            for _, attributes in self.elements
        )

    def has_click_only_noninteractive_elements(self):
        return any(
            "onclick" in attributes and tag not in self.INTERACTIVE_TAGS
            for tag, attributes in self.elements
        )


def parse_html(path):
    parser = CockpitHTMLParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def read_cockpit_sources(root):
    cockpit = root / "pilot/cockpit"
    return "\n".join(
        (cockpit / relative_path).read_text(encoding="utf-8")
        for relative_path in (
            "index.html",
            "assets/styles.css",
            "assets/protocol.js",
            "assets/app.js",
        )
    )


def run_node(source, payload=None):
    return subprocess.run(
        ["node", "-e", source],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        input=None if payload is None else json.dumps(payload, ensure_ascii=False),
    )


def load_build_module():
    path = ROOT / "scripts/build_ium11_cockpit.py"
    spec = importlib.util.spec_from_file_location("build_ium11_cockpit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IUM11CockpitBuildTests(unittest.TestCase):
    def test_protocol_asset_is_reproducible(self):
        asset_path = ROOT / "pilot/cockpit/assets/protocol.js"
        self.assertTrue(asset_path.is_file(), "generated protocol asset is missing")
        committed = asset_path.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary_directory:
            generated = Path(temporary_directory) / "protocol.js"
            load_build_module().build_cockpit_contract(ROOT, output_path=generated)
            self.assertEqual(generated.read_text(encoding="utf-8"), committed)

    def test_javascript_exports_exact_public_api(self):
        result = run_node("""
          const api = require('./pilot/cockpit/assets/app.js');
          process.stdout.write(JSON.stringify(Object.keys(api).sort()));
        """)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), sorted([
            "evaluateLearnerPulse", "deriveClusterResult", "deriveAnnualResult",
            "validateEvidencePackage", "createPackageId", "createEvidencePackage",
            "serializePackage", "parsePackage"
        ]))

    def test_compiled_contract_has_only_cockpit_fields_and_no_bom(self):
        expected_keys = {
            "schemaVersion", "protocolVersion", "protocolFingerprint",
            "toolVersion", "timeModelFingerprint", "minimumLearnerResponses",
            "learnerWarningRatio", "learnerPulseItems", "contextEnums",
            "clusters", "annualPilot",
        }
        compiled = load_build_module().compile_cockpit_contract(ROOT)
        self.assertEqual(set(compiled), expected_keys)
        self.assertFalse(
            (ROOT / "pilot/cockpit/assets/protocol.js").read_bytes().startswith(b"\xef\xbb\xbf")
        )


class IUM11CockpitMarkupTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT

    def test_cockpit_has_required_landmarks_and_status_regions(self):
        document = parse_html(self.root / "pilot/cockpit/index.html")
        self.assertEqual(document.count("main"), 1)
        self.assertTrue(
            document.has_element(id="error-summary", attributes={"tabindex": "-1"})
        )
        self.assertTrue(
            document.has_element(
                id="status-message", attributes={"aria-live": "polite"}
            )
        )
        self.assertTrue(document.labels_cover_all_controls())

    def test_cockpit_contains_no_network_or_persistence_capability(self):
        combined = read_cockpit_sources(self.root)
        for token in [
            "fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon",
            "localStorage", "sessionStorage", "indexedDB", "document.cookie",
            "serviceWorker", "http://", "https://", "@import", "url(//",
        ]:
            with self.subTest(token=token):
                self.assertNotIn(token, combined)

    def test_controls_use_native_keyboard_semantics(self):
        document = parse_html(self.root / "pilot/cockpit/index.html")
        self.assertFalse(document.has_positive_tabindex())
        self.assertFalse(document.has_click_only_noninteractive_elements())

    def test_cockpit_has_four_steps_seven_gates_and_json_only_import(self):
        source = (self.root / "pilot/cockpit/index.html").read_text(encoding="utf-8")
        document = parse_html(self.root / "pilot/cockpit/index.html")
        self.assertEqual(document.count("section"), 4)
        self.assertEqual(source.count('data-readiness="'), 7)
        self.assertEqual(source.count('data-context-field="'), 6)
        for number, title in (
            (1, "Bereitschaft prüfen"),
            (2, "Pilotstufe und Kontext"),
            (3, "Aggregierte Evidenz erfassen"),
            (4, "Prüfen und exportieren"),
        ):
            self.assertIn(f"{number}. {title}", source)
        self.assertTrue(
            document.has_element(
                id="cluster-import",
                attributes={"accept": "application/json,.json"},
            )
        )

    def test_css_declares_focus_touch_reflow_and_reduced_motion_baseline(self):
        source = (self.root / "pilot/cockpit/assets/styles.css").read_text(
            encoding="utf-8"
        )
        self.assertIn("max-width: 72rem", source)
        self.assertRegex(source, r":focus-visible\s*\{[^}]*outline:\s*[3-9]px")
        self.assertIn("min-block-size: 44px", source)
        self.assertIn("min-inline-size: 44px", source)
        self.assertIn("prefers-reduced-motion: reduce", source)
        self.assertIn("overflow-wrap: anywhere", source)


COCKPIT_FLOW_NODE = r"""
global.window = {};
require('./pilot/cockpit/assets/protocol.js');

const request = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const staticHtml = require('node:fs').readFileSync('./pilot/cockpit/index.html', 'utf8');
const focused = [];
const downloads = [];
const objectUrls = new Map();
let resetCount = 0;
let objectUrlCounter = 0;

function firstOptionValue(markup) {
  const option = markup.match(/<option\s+value="([^"]*)"/);
  return option ? option[1] : '';
}

function staticSelectDefault(id) {
  const match = staticHtml.match(
    new RegExp(`<select[^>]*id="${id}"[^>]*>([\\s\\S]*?)<\\/select>`)
  );
  return match ? firstOptionValue(match[1]) : '';
}

class FakeElement {
  constructor(id) {
    this.id = id;
    this.checked = false;
    this.disabled = false;
    this.files = [];
    this.hidden = false;
    this._innerHTML = '';
    this.listeners = {};
    this.textContent = '';
    this.defaultValue = staticSelectDefault(id);
    this.value = this.defaultValue;
  }
  get innerHTML() { return this._innerHTML; }
  set innerHTML(markup) {
    this._innerHTML = markup;
    const ownDefault = firstOptionValue(markup);
    if (ownDefault || /<option\s+value=""/.test(markup)) {
      this.defaultValue = ownDefault;
      this.value = ownDefault;
    }
    const selects = markup.matchAll(/<select[^>]*id="([^"]+)"([^>]*)>([\s\S]*?)<\/select>/g);
    for (const match of selects) {
      const child = element(match[1]);
      child.defaultValue = firstOptionValue(match[3]);
      child.value = child.defaultValue;
      child.required = /\brequired\b/.test(match[2]);
    }
    const inputs = markup.matchAll(/<input[^>]*id="([^"]+)"[^>]*>/g);
    for (const match of inputs) element(match[1]);
  }
  addEventListener(type, handler) {
    (this.listeners[type] ||= []).push(handler);
  }
  async dispatch(type) {
    const event = {target: this, preventDefault() {}};
    for (const handler of this.listeners[type] || []) {
      await handler(event);
    }
  }
  click() {
    return this.dispatch('click');
  }
  focus() {
    focused.push(this.id);
  }
}

const elements = new Map();
const element = (id) => {
  if (!elements.has(id)) elements.set(id, new FakeElement(id));
  return elements.get(id);
};
const form = element('pilot-form');
form.reset = function () {
  resetCount += 1;
  for (const item of elements.values()) {
    item.checked = false;
    item.files = [];
    item.value = item.defaultValue;
  }
};

global.document = {
  readyState: 'complete',
  getElementById: element,
  querySelector(selector) {
    return selector === 'form' ? form : null;
  },
  createElement(tag) {
    const created = new FakeElement(tag);
    if (tag === 'a') {
      created.click = function () {
        const blob = objectUrls.get(created.href);
        downloads.push({name: created.download, source: blob.parts.join('')});
      };
    }
    return created;
  },
  addEventListener() {},
};

global.Blob = class {
  constructor(parts, options) {
    this.parts = parts;
    this.type = options.type;
  }
};
global.URL = {
  createObjectURL(blob) {
    const url = `blob:ium11-${++objectUrlCounter}`;
    objectUrls.set(url, blob);
    return url;
  },
  revokeObjectURL(url) {
    objectUrls.delete(url);
  },
};
global.FileReader = class {
  readAsText(file) {
    if (file.error) {
      this.onerror({target: this});
      return;
    }
    this.result = file.text;
    this.onload({target: this});
  }
};

require('./pilot/cockpit/assets/app.js');
const protocol = window.IUM11_PROTOCOL;

const slug = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, '-');
const readinessIds = [
  'readiness-materials', 'readiness-handbook', 'readiness-anchor-tasks',
  'readiness-tools-fallback', 'readiness-privacy', 'readiness-capacity',
  'readiness-fingerprint',
];

async function makeReady(count = 7) {
  for (const id of readinessIds.slice(0, count)) {
    element(id).checked = true;
    await element(id).dispatch('change');
  }
}

async function selectScope(scopeId) {
  element('scope-id').value = scopeId;
  await element('scope-id').dispatch('change');
}

function seedPackage(payload, options = {}) {
  const contextIds = {
    schoolYear: 'context-school-year', term: 'context-term',
    classSizeBand: 'context-class-size-band', deviceClass: 'context-device-class',
    browserFamily: 'context-browser-family', networkMode: 'context-network-mode',
  };
  for (const [field, id] of Object.entries(contextIds)) {
    element(id).value = field === 'schoolYear'
      ? payload.context[field].slice(0, 4)
      : payload.context[field];
  }
  const delivery = payload.deliveryTimeEvidence;
  element('actual-units').value = String(delivery.actualUnits);
  element('fallback-activated').checked = delivery.fallbackActivated;
  element('technical-startup-minutes').value = String(delivery.technicalStartupMinutes);
  if (!options.preserveOutcomeSelects) {
    element('support-demand-band').value = delivery.supportDemandBand;
    element('external-disruption-code').value = delivery.externalDisruptionCode;
  }
  for (const phaseId of delivery.completedPhaseIds) {
    element(`phase-${slug(phaseId)}`).checked = true;
  }
  for (const record of delivery.clusterActualUnits || []) {
    element(`annual-units-${slug(record.clusterId)}`).value = String(record.actualUnits);
  }
  for (const moduleResult of payload.learningQualityEvidence.moduleResults) {
    for (const criterion of moduleResult.criteria) {
      if (!options.preserveCriteria) {
        element(`criterion-${slug(criterion.criterionId)}`).value = criterion.band;
      }
    }
  }
  for (const integrationResult of payload.learningQualityEvidence.integrationResults) {
    for (const criterion of integrationResult.criteria) {
      if (!options.preserveCriteria) {
        element(`criterion-${slug(criterion.criterionId)}`).value = criterion.band;
      }
    }
    const integrationId = slug(integrationResult.integrationContractId);
    element(`handoff-present-${integrationId}`).checked = integrationResult.handoffProductPresent;
    element(`handoff-reused-${integrationId}`).checked = integrationResult.handoffReused;
  }
  const pulse = payload.learnerPulseEvidence;
  if (!options.preserveOutcomeSelects) {
    element('learner-pulse-status').value = pulse.status;
  }
  if (pulse.status === 'reported') {
    element('class-response-count').value = String(pulse.classResponseCount);
    for (const item of pulse.items) {
      for (const field of ['agree', 'partly', 'disagree', 'noAnswer']) {
        element(`pulse-${slug(item.itemId)}-${slug(field)}`).value = String(item[field]);
      }
    }
  }
  const technical = payload.technicalPrivacyEvidence;
  element('fallback-equivalent').checked = technical.fallbackEquivalentLearningFunction;
  if (!options.preserveOutcomeSelects) {
    element('technical-function').value = technical.technicalFunction;
    element('problem-code').value = technical.problemCode;
    element('severity').value = technical.severity;
    element('privacy-gate').value = technical.privacyGate;
  }
}

async function importPackages(packages) {
  element('cluster-import').files = packages.map((payload) => ({
    text: JSON.stringify(payload),
  }));
  await element('cluster-import').dispatch('change');
  await element('import-button').click();
}

(async function () {
  let output;
  if (request.scenario === 'readiness') {
    const initial = element('pilot-context-fields').disabled;
    await makeReady(6);
    const afterSix = element('pilot-context-fields').disabled;
    await makeReady(7);
    output = {initial, afterSix, afterSeven: element('pilot-context-fields').disabled};
  } else if (request.scenario === 'validate') {
    await makeReady();
    await selectScope(request.package.scopeId);
    seedPackage(request.package);
    await form.dispatch('input');
    await element('validate-button').click();
    await element('download-button').click();
    output = {
      downloadDisabled: element('download-button').disabled,
      downloads,
      error: element('error-summary').textContent,
      focused,
      result: element('derived-result').textContent,
    };
  } else if (request.scenario === 'unselected-result-controls') {
    await makeReady();
    await selectScope(request.package.scopeId);
    seedPackage(request.package, request.options);
    await form.dispatch('input');
    await element('validate-button').click();
    await element('download-button').click();
    output = {
      downloadDisabled: element('download-button').disabled,
      downloads,
      error: element('error-summary').textContent,
      focused,
      result: element('derived-result').textContent,
    };
  } else if (request.scenario === 'annual-import') {
    await makeReady();
    await selectScope(protocol.annualPilot.id);
    const before = element('evidence-fields').disabled;
    await importPackages(request.packages);
    output = {
      before,
      after: element('evidence-fields').disabled,
      error: element('error-summary').textContent,
      focused,
      status: element('import-status').textContent,
    };
  } else if (request.scenario === 'annual-validate') {
    await makeReady();
    await selectScope(protocol.annualPilot.id);
    await importPackages(request.packages);
    seedPackage(request.package);
    await form.dispatch('input');
    await element('validate-button').click();
    await element('download-button').click();
    output = {
      downloadDisabled: element('download-button').disabled,
      downloads,
      error: element('error-summary').textContent,
      result: element('derived-result').textContent,
    };
  } else if (request.scenario === 'clear') {
    await makeReady();
    await selectScope(protocol.annualPilot.id);
    await importPackages(request.packages);
    await element('clear-button').click();
    await makeReady();
    await selectScope(protocol.annualPilot.id);
    output = {
      annualLocked: element('evidence-fields').disabled,
      downloadDisabled: element('download-button').disabled,
      resetCount,
      importStatus: element('import-status').textContent,
    };
  }
  process.stdout.write(JSON.stringify(output));
}()).catch((error) => {
  process.stderr.write(error.stack || String(error));
  process.exitCode = 1;
});
"""


def run_cockpit_flow(scenario, *, package=None, packages=None, options=None):
    result = run_node(
        COCKPIT_FLOW_NODE,
        {
            "scenario": scenario,
            "package": package,
            "packages": packages,
            "options": options,
        },
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class IUM11CockpitFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        example_root = ROOT / "pilot/examples"
        cls.cluster = load_json(example_root / "synthetic-cluster-pass.json")
        cls.clusters = [
            load_json(example_root / name)
            for name in (
                "synthetic-cluster-pass.json",
                "synthetic-cluster-programming-pass.json",
                "synthetic-cluster-net-security-pass.json",
                "synthetic-cluster-data-media-society-pass.json",
            )
        ]
        cls.annual = load_json(example_root / "synthetic-annual-pass.json")

    def test_all_seven_readiness_gates_are_required(self):
        result = run_cockpit_flow("readiness")
        self.assertEqual(result, {"initial": True, "afterSix": True, "afterSeven": False})

    def test_privacy_failure_focuses_explanation_and_blocks_download(self):
        package = copy.deepcopy(self.cluster)
        package["technicalPrivacyEvidence"]["privacyGate"] = "fail"
        result = run_cockpit_flow("validate", package=package)
        self.assertTrue(result["downloadDisabled"])
        self.assertEqual(result["downloads"], [])
        self.assertEqual(result["result"], "fail")
        self.assertEqual(result["focused"][-1], "error-summary")
        self.assertIn(package["scopeId"], result["error"])
        self.assertEqual(result["error"].count("Nächster Schritt:"), 1)

    def test_untouched_criteria_cannot_produce_pass_or_download(self):
        result = run_cockpit_flow(
            "unselected-result-controls",
            package=self.cluster,
            options={"preserveCriteria": True},
        )
        self.assertNotEqual(result["result"], "pass")
        self.assertTrue(result["downloadDisabled"])
        self.assertEqual(result["downloads"], [])
        self.assertEqual(result["focused"][-1], "error-summary")
        self.assertEqual(result["error"].count("Nächster Schritt:"), 1)

    def test_untouched_technical_privacy_selects_cannot_produce_pass_or_download(self):
        result = run_cockpit_flow(
            "unselected-result-controls",
            package=self.cluster,
            options={"preserveOutcomeSelects": True},
        )
        self.assertNotEqual(result["result"], "pass")
        self.assertTrue(result["downloadDisabled"])
        self.assertEqual(result["downloads"], [])
        self.assertEqual(result["focused"][-1], "error-summary")
        self.assertEqual(result["error"].count("Nächster Schritt:"), 1)

    def test_suppressed_small_group_download_contains_no_counts(self):
        package = copy.deepcopy(self.cluster)
        package["learnerPulseEvidence"] = {"status": "suppressed-small-group"}
        result = run_cockpit_flow("validate", package=package)
        self.assertFalse(result["downloadDisabled"])
        self.assertEqual(len(result["downloads"]), 1)
        exported = json.loads(result["downloads"][0]["source"])
        self.assertEqual(
            exported["learnerPulseEvidence"], {"status": "suppressed-small-group"}
        )

    def test_warning_focuses_summary_and_prevents_pass(self):
        package = copy.deepcopy(self.cluster)
        package["learnerPulseEvidence"] = pulse(4, 12)
        result = run_cockpit_flow("validate", package=package)
        self.assertEqual(result["result"], "fail")
        self.assertEqual(result["focused"][-1], "error-summary")
        self.assertIn("Entwicklungswarnung", result["error"])

    def test_unknown_import_field_is_rejected_before_annual_unlock(self):
        packages = copy.deepcopy(self.clusters)
        packages[1]["studentName"] = "Ada"
        result = run_cockpit_flow("annual-import", packages=packages)
        self.assertTrue(result["after"])
        self.assertEqual(result["focused"][-1], "error-summary")
        self.assertIn("Import", result["error"])

    def test_annual_mode_unlocks_only_for_four_positive_same_version_clusters(self):
        incomplete = run_cockpit_flow("annual-import", packages=self.clusters[:3])
        self.assertTrue(incomplete["before"])
        self.assertTrue(incomplete["after"])

        mixed = copy.deepcopy(self.clusters)
        mixed[0]["protocolVersion"] = "2.0.0"
        self.assertTrue(run_cockpit_flow("annual-import", packages=mixed)["after"])

        negative = copy.deepcopy(self.clusters)
        negative[0]["learningQualityEvidence"]["moduleResults"][0]["criteria"][0][
            "band"
        ] = "mixed"
        negative[0]["learningQualityEvidence"]["moduleResults"][0]["result"] = "fail"
        negative[0]["result"] = "fail"
        self.assertTrue(run_cockpit_flow("annual-import", packages=negative)["after"])

        duplicate = copy.deepcopy(self.clusters)
        duplicate[1] = copy.deepcopy(duplicate[0])
        self.assertTrue(run_cockpit_flow("annual-import", packages=duplicate)["after"])

        reordered = copy.deepcopy(self.clusters)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        self.assertTrue(run_cockpit_flow("annual-import", packages=reordered)["after"])

        accepted = run_cockpit_flow("annual-import", packages=self.clusters)
        self.assertTrue(accepted["before"])
        self.assertFalse(accepted["after"])
        self.assertIn("4 von 4", accepted["status"])

    def test_unlocked_annual_mode_derives_and_downloads_a_valid_package(self):
        result = run_cockpit_flow(
            "annual-validate", package=self.annual, packages=self.clusters
        )
        self.assertFalse(result["downloadDisabled"])
        self.assertEqual(result["result"], "pass")
        self.assertEqual(len(result["downloads"]), 1)
        exported = json.loads(result["downloads"][0]["source"])
        self.assertEqual(exported["scopeId"], "ANNUAL-7-WORKING-40")
        self.assertNotIn("clusterPackages", exported)

    def test_clear_state_removes_all_in_memory_values(self):
        result = run_cockpit_flow("clear", packages=self.clusters)
        self.assertTrue(result["annualLocked"])
        self.assertTrue(result["downloadDisabled"])
        self.assertEqual(result["resetCount"], 1)
        self.assertIn("0 von 4", result["importStatus"])

    def test_download_filename_contains_only_scope_and_random_package_id(self):
        result = run_cockpit_flow("validate", package=self.cluster)
        self.assertEqual(len(result["downloads"]), 1)
        exported = json.loads(result["downloads"][0]["source"])
        self.assertEqual(
            result["downloads"][0]["name"],
            f"ium11-{exported['scopeId'].lower()}-{exported['packageId']}.json",
        )
        self.assertNotIn(exported["context"]["schoolYear"], result["downloads"][0]["name"])


NODE_CALL = r"""
global.window = {};
require('./pilot/cockpit/assets/protocol.js');
const api = require('./pilot/cockpit/assets/app.js');
const request = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const args = request.withProtocol === false
  ? request.args
  : [...request.args, window.IUM11_PROTOCOL];
const result = api[request.operation](...args);
process.stdout.write(JSON.stringify(result));
"""


def call_javascript(operation, *args, with_protocol=True):
    result = run_node(
        NODE_CALL,
        {"operation": operation, "args": args, "withProtocol": with_protocol},
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def javascript_rejects(operation, *args, with_protocol=True):
    result = run_node(
        NODE_CALL,
        {"operation": operation, "args": args, "withProtocol": with_protocol},
    )
    return result.returncode != 0


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pulse(disagree, valid, no_answer=0):
    agree = valid - disagree
    return {
        "status": "reported",
        "classResponseCount": valid + no_answer,
        "items": [
            {
                "itemId": item_id,
                "agree": agree,
                "partly": 0,
                "disagree": disagree,
                "noAnswer": no_answer,
            }
            for item_id in ("clarity", "cognitiveEngagement", "supportUsefulness")
        ],
    }


def form_value(package):
    return {
        field: copy.deepcopy(package[field])
        for field in (
            "context", "deliveryTimeEvidence", "learningQualityEvidence",
            "learnerPulseEvidence", "technicalPrivacyEvidence",
        )
    }


class IUM11CockpitParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.time_model = load_json(ROOT / "roadmap/time-model.json")
        cls.protocol = validate_pilot_protocol(
            load_json(ROOT / "pilot/pilot-protocol.json"), cls.time_model
        )
        cls.compiled_contract = load_build_module().compile_cockpit_contract(ROOT)
        cls.examples = {
            path.name: load_json(path)
            for path in sorted((ROOT / "pilot/examples").glob("synthetic-*.json"))
            if load_json(path).get("packageType") in {"cluster-evidence", "annual-evidence"}
        }
        cls.positive_clusters = [
            cls.examples[name]
            for name in (
                "synthetic-cluster-pass.json",
                "synthetic-cluster-programming-pass.json",
                "synthetic-cluster-net-security-pass.json",
                "synthetic-cluster-data-media-society-pass.json",
            )
        ]
        cls.annual = cls.examples["synthetic-annual-pass.json"]

    def assert_python_and_javascript_reject(self, payload):
        with self.assertRaises(IUM11ValidationError):
            validate_evidence_package(payload, self.protocol, self.time_model)
        self.assertTrue(
            javascript_rejects("validateEvidencePackage", payload),
            "JavaScript accepted a package rejected by Python",
        )

    def test_all_synthetic_evidence_examples_validate_and_derive_identically(self):
        self.assertEqual(len(self.examples), 6)
        for name, package in self.examples.items():
            with self.subTest(name=name):
                self.assertEqual(
                    call_javascript("validateEvidencePackage", package),
                    validate_evidence_package(package, self.protocol, self.time_model),
                )
                if package["packageType"] == "cluster-evidence":
                    cluster = self.protocol["clustersById"][package["scopeId"]]
                    expected = derive_cluster_result(package, cluster, self.protocol)
                    actual = call_javascript(
                        "deriveClusterResult",
                        package,
                        self.compiled_contract["clusters"][cluster["order"] - 1],
                    )
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual["result"], package["result"])
                else:
                    expected = derive_annual_result(
                        package, self.positive_clusters, self.protocol
                    )
                    actual = call_javascript(
                        "deriveAnnualResult", package, self.positive_clusters
                    )
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual["result"], package["result"])

    def test_learner_warning_boundaries_match_valid_response_denominator(self):
        cases = (
            (2, 7, "reject"),
            (3, 9, "reject"),
            (3, 10, []),
            (4, 12, ["WARN-clarity", "WARN-cognitiveEngagement", "WARN-supportUsefulness"]),
            (4, 13, []),
        )
        for disagree, valid, expected in cases:
            sample = pulse(disagree, valid)
            with self.subTest(disagree=disagree, valid=valid):
                if expected == "reject":
                    with self.assertRaises(IUM11ValidationError):
                        evaluate_learner_pulse(sample, self.protocol)
                    self.assertTrue(javascript_rejects("evaluateLearnerPulse", sample))
                else:
                    python_result = evaluate_learner_pulse(sample, self.protocol)
                    javascript_result = call_javascript("evaluateLearnerPulse", sample)
                    self.assertEqual(javascript_result, python_result)
                    self.assertEqual(
                        [warning["id"] for warning in javascript_result["warnings"]],
                        expected,
                    )

    def test_reported_nine_and_suppressed_extra_field_fail_closed(self):
        reported_nine = pulse(0, 9)
        suppressed_extra = {"status": "suppressed-small-group", "classResponseCount": 9}
        for sample in (reported_nine, suppressed_extra):
            with self.subTest(sample=sample):
                with self.assertRaises(IUM11ValidationError):
                    evaluate_learner_pulse(sample, self.protocol)
                self.assertTrue(javascript_rejects("evaluateLearnerPulse", sample))

    def test_cluster_mutations_match_python_results_and_validation(self):
        baseline = self.examples["synthetic-cluster-programming-pass.json"]
        cluster = self.protocol["clustersById"][baseline["scopeId"]]
        compiled_cluster = self.compiled_contract["clusters"][cluster["order"] - 1]

        mutations = []
        over_budget = copy.deepcopy(baseline)
        over_budget["deliveryTimeEvidence"]["actualUnits"] = cluster["budgetUnits"] + 1
        mutations.append(("budget+1", over_budget, "fail"))
        missing_phase = copy.deepcopy(baseline)
        missing_phase["deliveryTimeEvidence"]["completedPhaseIds"].pop()
        mutations.append(("missing phase", missing_phase, "fail"))
        mixed = copy.deepcopy(baseline)
        mixed["learningQualityEvidence"]["moduleResults"][0]["criteria"][0]["band"] = "mixed"
        mutations.append(("mixed", mixed, "fail"))
        privacy = copy.deepcopy(baseline)
        privacy["technicalPrivacyEvidence"]["privacyGate"] = "fail"
        mutations.append(("privacy", privacy, "fail"))

        for label, package, expected_result in mutations:
            with self.subTest(label=label):
                expected = derive_cluster_result(package, cluster, self.protocol)
                actual = call_javascript(
                    "deriveClusterResult", package, compiled_cluster
                )
                self.assertEqual(actual, expected)
                self.assertEqual(actual["result"], expected_result)

        self.assert_python_and_javascript_reject(missing_phase)
        self.assert_python_and_javascript_reject(privacy)

    def test_privacy_failure_precedes_interpretability_loss_across_runtimes(self):
        cluster_package = copy.deepcopy(
            self.examples["synthetic-cluster-programming-pass.json"]
        )
        cluster_package["deliveryTimeEvidence"]["externalDisruptionCode"] = "interpretability-lost"
        cluster_package["technicalPrivacyEvidence"]["privacyGate"] = "fail"
        cluster = self.protocol["clustersById"][cluster_package["scopeId"]]
        python_cluster = derive_cluster_result(cluster_package, cluster, self.protocol)
        javascript_cluster = call_javascript(
            "deriveClusterResult",
            cluster_package,
            self.compiled_contract["clusters"][cluster["order"] - 1],
        )
        self.assertEqual(javascript_cluster, python_cluster)
        self.assertEqual(javascript_cluster["result"], "fail")

        annual = copy.deepcopy(self.annual)
        annual["deliveryTimeEvidence"]["externalDisruptionCode"] = "interpretability-lost"
        annual["technicalPrivacyEvidence"]["privacyGate"] = "fail"
        python_annual = derive_annual_result(
            annual, self.positive_clusters, self.protocol
        )
        javascript_annual = call_javascript(
            "deriveAnnualResult", annual, self.positive_clusters
        )
        self.assertEqual(javascript_annual, python_annual)
        self.assertEqual(javascript_annual["result"], "fail")

    def test_context_consistency_fails_closed_across_runtimes(self):
        cases = []
        under_ten = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
        under_ten["context"]["classSizeBand"] = "under-10"
        cases.append(under_ten)
        annual_half_year = copy.deepcopy(self.annual)
        annual_half_year["context"]["term"] = "first-half"
        cases.append(annual_half_year)

        for package in cases:
            with self.subTest(scope_id=package["scopeId"]):
                self.assert_python_and_javascript_reject(package)

        clusters = copy.deepcopy(self.positive_clusters)
        clusters[0]["context"]["schoolYear"] = "2025-26"
        with self.assertRaisesRegex(IUM11ValidationError, "schoolYear"):
            derive_annual_result(self.annual, clusters, self.protocol)
        self.assertTrue(
            javascript_rejects("deriveAnnualResult", self.annual, clusters)
        )

    def test_equivalent_fallback_replaces_technical_failure(self):
        package = copy.deepcopy(self.examples["synthetic-cluster-programming-pass.json"])
        package["deliveryTimeEvidence"]["fallbackActivated"] = True
        package["technicalPrivacyEvidence"].update(
            technicalFunction="fail",
            fallbackEquivalentLearningFunction=True,
            problemCode="execution",
            severity="major",
        )
        cluster = self.protocol["clustersById"][package["scopeId"]]
        expected = derive_cluster_result(package, cluster, self.protocol)
        actual = call_javascript(
            "deriveClusterResult",
            package,
            self.compiled_contract["clusters"][cluster["order"] - 1],
        )
        self.assertEqual(actual, expected)
        self.assertEqual(actual["result"], "pass")

    def test_annual_can_pass_fail_or_be_not_evaluable_after_positive_clusters(self):
        cases = []
        passed = copy.deepcopy(self.annual)
        cases.append(("pass", passed))
        failed = copy.deepcopy(self.annual)
        failed["learningQualityEvidence"]["integrationResults"][0]["criteria"][0]["band"] = "mixed"
        failed["learningQualityEvidence"]["integrationResults"][0]["result"] = "fail"
        cases.append(("fail", failed))
        not_evaluable = copy.deepcopy(self.annual)
        not_evaluable["deliveryTimeEvidence"]["externalDisruptionCode"] = "interpretability-lost"
        cases.append(("not-evaluable", not_evaluable))

        for expected_result, annual in cases:
            with self.subTest(expected_result=expected_result):
                expected = derive_annual_result(
                    annual, self.positive_clusters, self.protocol
                )
                actual = call_javascript(
                    "deriveAnnualResult", annual, self.positive_clusters
                )
                self.assertEqual(actual, expected)
                self.assertEqual(actual["result"], expected_result)

    def test_positive_annual_capacity_is_exactly_40(self):
        annual = copy.deepcopy(self.annual)
        annual["deliveryTimeEvidence"]["actualUnits"] = 39
        annual["deliveryTimeEvidence"]["clusterActualUnits"][0]["actualUnits"] -= 1
        expected = derive_annual_result(annual, self.positive_clusters, self.protocol)
        actual = call_javascript("deriveAnnualResult", annual, self.positive_clusters)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["result"], "fail")

        annual["deliveryTimeEvidence"]["actualUnits"] = 41
        annual["deliveryTimeEvidence"]["clusterActualUnits"][0]["actualUnits"] += 2
        with self.assertRaises(IUM11ValidationError):
            derive_annual_result(annual, self.positive_clusters, self.protocol)
        self.assertTrue(
            javascript_rejects("deriveAnnualResult", annual, self.positive_clusters)
        )

    def test_wrong_fingerprint_and_recursive_extra_field_fail_closed(self):
        wrong_fingerprint = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
        wrong_fingerprint["protocolFingerprint"] = "0" * 64
        nested_extra = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
        nested_extra["learningQualityEvidence"]["moduleResults"][0]["criteria"][0][
            "studentName"
        ] = "Ada"
        for package in (wrong_fingerprint, nested_extra):
            with self.subTest(package=package):
                self.assert_python_and_javascript_reject(package)

    def test_semantic_result_tampering_fails_at_validate_parse_and_create(self):
        mutations = (
            lambda package: package["learningQualityEvidence"]["moduleResults"][0]["criteria"][0].__setitem__("band", "mixed"),
            lambda package: package["learningQualityEvidence"]["integrationResults"][0].__setitem__("handoffReused", False),
        )
        for mutate in mutations:
            package = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
            mutate(package)
            serialized = json.dumps(package, ensure_ascii=False)
            with self.subTest(mutation=mutate):
                self.assert_python_and_javascript_reject(package)
                self.assertTrue(javascript_rejects("parsePackage", serialized))
                self.assertTrue(javascript_rejects(
                    "createEvidencePackage", package["scopeId"], form_value(package)
                ))

        top_level = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
        top_level["result"] = "fail"
        self.assert_python_and_javascript_reject(top_level)
        self.assertTrue(javascript_rejects(
            "parsePackage", json.dumps(top_level, ensure_ascii=False)
        ))

    def test_reordered_nested_object_keys_are_equal_across_runtimes(self):
        package = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
        package["context"] = {
            key: package["context"][key]
            for key in reversed(list(package["context"]))
        }
        module = package["learningQualityEvidence"]["moduleResults"][0]
        module["criteria"][0] = {
            key: module["criteria"][0][key]
            for key in reversed(list(module["criteria"][0]))
        }
        package["learningQualityEvidence"]["moduleResults"][0] = {
            key: module[key]
            for key in reversed(list(module))
        }
        package["learnerPulseEvidence"] = pulse(4, 12)
        package["developmentWarnings"] = [
            {
                "status": "open",
                "itemId": item_id,
                "id": f"WARN-{item_id}",
            }
            for item_id in ("clarity", "cognitiveEngagement", "supportUsefulness")
        ]
        package["result"] = "fail"

        python_result = validate_evidence_package(
            package, self.protocol, self.time_model
        )
        validation = run_node(
            NODE_CALL,
            {
                "operation": "validateEvidencePackage",
                "args": [package],
                "withProtocol": True,
            },
        )
        self.assertEqual(validation.returncode, 0, validation.stderr)
        self.assertEqual(json.loads(validation.stdout), python_result)
        serialized = json.dumps(package, ensure_ascii=False)
        self.assertEqual(call_javascript("parsePackage", serialized), python_result)
        created = call_javascript(
            "createEvidencePackage", package["scopeId"], form_value(package)
        )
        self.assertEqual(created["result"], "fail")
        self.assertEqual(
            [warning["id"] for warning in created["developmentWarnings"]],
            [
                "WARN-clarity", "WARN-cognitiveEngagement",
                "WARN-supportUsefulness",
            ],
        )

    def test_array_order_remains_part_of_the_cross_runtime_contract(self):
        package = copy.deepcopy(self.examples["synthetic-cluster-pass.json"])
        package["learningQualityEvidence"]["moduleResults"].reverse()
        self.assert_python_and_javascript_reject(package)

    def test_annual_derivation_revalidates_imported_cluster_packages(self):
        cases = []
        manipulated = copy.deepcopy(self.positive_clusters)
        manipulated[0]["learningQualityEvidence"]["moduleResults"][0]["criteria"][0]["band"] = "mixed"
        cases.append(("manipulated", manipulated))
        negative = copy.deepcopy(self.positive_clusters)
        module = negative[0]["learningQualityEvidence"]["moduleResults"][0]
        module["criteria"][0]["band"] = "mixed"
        module["result"] = "fail"
        negative[0]["result"] = "fail"
        cases.append(("negative", negative))
        duplicated = copy.deepcopy(self.positive_clusters)
        duplicated[1] = copy.deepcopy(duplicated[0])
        cases.append(("duplicated", duplicated))
        mixed_version = copy.deepcopy(self.positive_clusters)
        mixed_version[0]["protocolVersion"] = "2.0.0"
        cases.append(("mixed-version", mixed_version))

        for label, clusters in cases:
            with self.subTest(label=label):
                with self.assertRaises(IUM11ValidationError):
                    derive_annual_result(self.annual, clusters, self.protocol)
                self.assertTrue(javascript_rejects(
                    "deriveAnnualResult", self.annual, clusters
                ))

    def test_package_creation_serialization_and_parsing_are_closed_and_pure(self):
        package = self.examples["synthetic-cluster-pass.json"]
        source = form_value(package)
        original = copy.deepcopy(source)
        created = call_javascript(
            "createEvidencePackage", package["scopeId"], source
        )
        self.assertEqual(source, original)
        self.assertEqual(created["scopeId"], package["scopeId"])
        self.assertEqual(created["packageType"], "cluster-evidence")
        self.assertEqual(created["result"], "pass")
        self.assertEqual(created["developmentWarnings"], [])
        self.assertRegex(
            created["packageId"],
            r"^PKG-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        )
        self.assertEqual(
            call_javascript("validateEvidencePackage", created), created
        )

        serialized = call_javascript("serializePackage", created, with_protocol=False)
        self.assertEqual(serialized, json.dumps(created, indent=2, ensure_ascii=False) + "\n")
        self.assertEqual(call_javascript("parsePackage", serialized), created)
        self.assertTrue(javascript_rejects("parsePackage", "[]"))

    def test_package_creator_has_exact_signature_and_rejects_unknown_scope(self):
        result = run_node("""
          const api = require('./pilot/cockpit/assets/app.js');
          process.stdout.write(String(api.createEvidencePackage.length));
        """)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "3")
        self.assertTrue(javascript_rejects(
            "createEvidencePackage", "CLUSTER-UNKNOWN", form_value(
                self.examples["synthetic-cluster-pass.json"]
            )
        ))

    def test_annual_creator_uses_four_clusters_without_serializing_them(self):
        source = form_value(self.annual)
        source["clusterPackages"] = copy.deepcopy(self.positive_clusters)
        original = copy.deepcopy(source)
        created = call_javascript(
            "createEvidencePackage", self.annual["scopeId"], source
        )
        self.assertEqual(source, original)
        self.assertNotIn("clusterPackages", created)
        self.assertEqual(created["packageType"], "annual-evidence")
        self.assertEqual(created["scopeType"], "annual")
        self.assertEqual(created["result"], "pass")
        serialized = call_javascript("serializePackage", created, with_protocol=False)
        self.assertNotIn("clusterPackages", serialized)

        source["clusterPackages"].pop()
        self.assertTrue(javascript_rejects(
            "createEvidencePackage", self.annual["scopeId"], source
        ))

    def test_package_ids_are_unique_uuid_v4_values(self):
        ids = {
            call_javascript("createPackageId", with_protocol=False)
            for _ in range(20)
        }
        self.assertEqual(len(ids), 20)
        for package_id in ids:
            self.assertTrue(re.fullmatch(
                r"PKG-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
                package_id,
            ))


if __name__ == "__main__":
    unittest.main()
