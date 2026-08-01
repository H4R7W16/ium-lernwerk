import copy
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
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
