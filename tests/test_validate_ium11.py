import copy
import json
import shutil
import tempfile
import uuid
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch

import scripts.validate_ium11 as validate_ium11_script
from scripts.validate_ium10 import IUM10ValidationError
from scripts.validate_ium11 import (
    IUM11ValidationError,
    PROHIBITED_FIELD_NAMES,
    build_decision_package,
    canonical_sha256,
    derive_annual_result,
    derive_cluster_result,
    evaluate_learner_pulse,
    main,
    validate_decision_package,
    validate_evidence_package,
    validate_ium11_repository,
    validate_pilot_protocol,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_positive_example_packages(root):
    names = [
        "synthetic-cluster-pass.json",
        "synthetic-cluster-programming-pass.json",
        "synthetic-cluster-net-security-pass.json",
        "synthetic-cluster-data-media-society-pass.json",
        "synthetic-annual-pass.json",
    ]
    return [load_json(root / "pilot/examples" / name) for name in names]


def collect_keys(value):
    if isinstance(value, dict):
        return set(value) | set().union(*(collect_keys(item) for item in value.values()), set())
    if isinstance(value, list):
        return set().union(*(collect_keys(item) for item in value), set())
    return set()


class IUM11SyntheticExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(cls.root / "roadmap/time-model.json")
        cls.protocol = validate_pilot_protocol(
            load_json(cls.root / "pilot/pilot-protocol.json"), cls.time_model
        )

    def test_all_examples_are_closed_nonpersonal_and_derivable(self):
        result = validate_ium11_repository(self.root)
        self.assertEqual(result["exampleCounts"], {
            "clusterPass": 4,
            "clusterFail": 1,
            "annualPass": 1,
            "decisionEligible": 1,
        })

    def test_positive_examples_rebuild_committed_decision_byte_for_byte(self):
        positive = load_positive_example_packages(self.root)
        rebuilt = build_decision_package(positive, self.protocol, self.time_model)
        committed = load_json(self.root / "pilot/examples/synthetic-decision-eligible.json")
        self.assertEqual(rebuilt, committed)

    def test_examples_contain_no_identifying_or_free_text_keys(self):
        for path in sorted((self.root / "pilot/examples").glob("*.json")):
            flattened_keys = collect_keys(load_json(path))
            self.assertTrue(flattened_keys.isdisjoint(PROHIBITED_FIELD_NAMES), path)

    def test_synthetic_cli_writes_only_the_committed_decision_path(self):
        target = self.root / "pilot/examples/synthetic-decision-eligible.json"
        self.assertEqual(
            main([
                "--root", str(self.root), "--write-synthetic-decision",
                "pilot/examples/synthetic-decision-eligible.json",
            ]),
            0,
        )
        self.assertTrue(target.is_file())


def reported_pulse(agree=8, partly=2, disagree=1, no_answer=1):
    count = agree + partly + disagree + no_answer
    return {
        "status": "reported",
        "classResponseCount": count,
        "items": [
            {
                "itemId": item_id,
                "agree": agree,
                "partly": partly,
                "disagree": disagree,
                "noAnswer": no_answer,
            }
            for item_id in ("clarity", "cognitiveEngagement", "supportUsefulness")
        ],
    }


def valid_cluster_package(scope_id="CLUSTER-7-DATA-CODING"):
    root = Path(__file__).resolve().parents[1]
    time_model = load_json(root / "roadmap/time-model.json")
    protocol = validate_pilot_protocol(
        load_json(root / "pilot/pilot-protocol.json"), time_model
    )
    cluster = protocol["clustersById"][scope_id]
    completed_phases = sorted({
        phase_id
        for module in cluster["modules"]
        for phase_id in module["requiredPhaseIds"]
    })
    return {
        "schemaVersion": 1,
        "packageType": "cluster-evidence",
        "packageId": f"PKG-{uuid.uuid4()}",
        "protocolVersion": protocol["protocolVersion"],
        "protocolFingerprint": protocol["protocolFingerprint"],
        "toolVersion": protocol["toolVersion"],
        "timeModelFingerprint": protocol["timeModelFingerprint"],
        "scopeType": "cluster",
        "scopeId": scope_id,
        "context": {"schoolYear": "2026-27", "term": "first-half", "classSizeBand": "20-29", "deviceClass": "mixed", "browserFamily": "chromium", "networkMode": "offline"},
        "deliveryTimeEvidence": {"plannedUnits": cluster["budgetUnits"], "actualUnits": cluster["budgetUnits"], "completedPhaseIds": completed_phases, "requiredLearningPhasesCompleted": True, "fallbackActivated": False, "technicalStartupMinutes": 3, "supportDemandBand": "low", "externalDisruptionCode": "none"},
        "learningQualityEvidence": {
            "moduleResults": [
                {"pilotAssignmentId": module["pilotAssignmentId"], "moduleId": module["moduleId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in module["criteria"]], "result": "pass"}
                for module in cluster["modules"]
            ],
            "integrationResults": [{"pilotAssignmentId": cluster["integration"]["pilotAssignmentId"], "integrationContractId": cluster["integration"]["integrationContractId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in cluster["integration"]["criteria"]], "handoffProductPresent": True, "handoffReused": True, "result": "pass"}],
        },
        "learnerPulseEvidence": reported_pulse(),
        "technicalPrivacyEvidence": {"technicalFunction": "pass", "fallbackEquivalentLearningFunction": False, "problemCode": "none", "severity": "none", "privacyGate": "pass"},
        "result": "pass",
        "developmentWarnings": [],
        "retentionClass": "until-decision",
    }


def valid_annual_package():
    root = Path(__file__).resolve().parents[1]
    time_model = load_json(root / "roadmap/time-model.json")
    protocol = validate_pilot_protocol(
        load_json(root / "pilot/pilot-protocol.json"),
        time_model,
    )
    clusters = protocol["clusters"]
    modules = [module for cluster in clusters for module in cluster["modules"]]
    completed_phases = sorted({
        phase_id
        for module in modules
        for phase_id in module["requiredPhaseIds"]
    })
    return {
        "schemaVersion": 1,
        "packageType": "annual-evidence",
        "packageId": f"PKG-{uuid.uuid4()}",
        "protocolVersion": protocol["protocolVersion"],
        "protocolFingerprint": protocol["protocolFingerprint"],
        "toolVersion": protocol["toolVersion"],
        "timeModelFingerprint": protocol["timeModelFingerprint"],
        "scopeType": "annual",
        "scopeId": "ANNUAL-7-WORKING-40",
        "context": {"schoolYear": "2026-27", "term": "full-year", "classSizeBand": "20-29", "deviceClass": "mixed", "browserFamily": "chromium", "networkMode": "offline"},
        "deliveryTimeEvidence": {
            "plannedUnits": 40,
            "actualUnits": 40,
            "completedPhaseIds": completed_phases,
            "requiredLearningPhasesCompleted": True,
            "fallbackActivated": False,
            "technicalStartupMinutes": 12,
            "supportDemandBand": "low",
            "externalDisruptionCode": "none",
            "clusterOrder": [cluster["id"] for cluster in clusters],
            "clusterActualUnits": [{"clusterId": cluster["id"], "actualUnits": cluster["budgetUnits"]} for cluster in clusters],
        },
        "learningQualityEvidence": {
            "moduleResults": [
                {"pilotAssignmentId": module["pilotAssignmentId"], "moduleId": module["moduleId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in module["criteria"]], "result": "pass"}
                for module in modules
            ],
            "integrationResults": [
                {"pilotAssignmentId": cluster["integration"]["pilotAssignmentId"], "integrationContractId": cluster["integration"]["integrationContractId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in cluster["integration"]["criteria"]], "handoffProductPresent": True, "handoffReused": True, "result": "pass"}
                for cluster in clusters
            ],
        },
        "learnerPulseEvidence": reported_pulse(),
        "technicalPrivacyEvidence": {"technicalFunction": "pass", "fallbackEquivalentLearningFunction": False, "problemCode": "none", "severity": "none", "privacyGate": "pass"},
        "result": "pass",
        "developmentWarnings": [],
        "retentionClass": "until-decision",
    }


def five_positive_packages():
    return [
        valid_cluster_package("CLUSTER-7-DATA-CODING"),
        valid_cluster_package("CLUSTER-7-PROGRAMMING"),
        valid_cluster_package("CLUSTER-7-NET-SECURITY"),
        valid_cluster_package("CLUSTER-7-DATA-MEDIA-SOCIETY"),
        valid_annual_package(),
    ]


def packages_by_scope(packages):
    return {package["scopeId"]: package for package in packages}


class IUM11ProtocolContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(cls.root / "roadmap/time-model.json")
        cls.protocol = load_json(cls.root / "pilot/pilot-protocol.json")

    def test_time_model_fingerprint_is_canonical_and_pinned(self):
        self.assertEqual(
            canonical_sha256(self.time_model),
            "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1",
        )
        self.assertEqual(
            self.protocol["timeModelFingerprint"],
            canonical_sha256(self.time_model),
        )

    def test_protocol_binds_exact_cluster_sequence(self):
        compiled = validate_pilot_protocol(self.protocol, self.time_model)
        self.assertEqual(
            [
                (
                    cluster["id"],
                    cluster["moduleIds"],
                    cluster["budgetUnits"],
                    cluster["fallbackDeltaUnits"],
                )
                for cluster in compiled["clusters"]
            ],
            [
                ("CLUSTER-7-DATA-CODING", ["IUM-7-CORE-01", "IUM-7-CORE-02"], 8, 3),
                ("CLUSTER-7-PROGRAMMING", ["IUM-7-CORE-03", "IUM-7-CORE-04"], 11, 2),
                (
                    "CLUSTER-7-NET-SECURITY",
                    ["IUM-7-CORE-05", "IUM-7-CORE-06", "IUM-7-CORE-07"],
                    11,
                    3,
                ),
                (
                    "CLUSTER-7-DATA-MEDIA-SOCIETY",
                    ["IUM-7-CORE-08", "IUM-7-CORE-09", "IUM-7-CORE-10"],
                    10,
                    6,
                ),
            ],
        )

    def test_protocol_keeps_status_and_recommendation_boundaries(self):
        compiled = validate_pilot_protocol(self.protocol, self.time_model)
        self.assertEqual(compiled["status"], "working")
        self.assertEqual(
            compiled["allowedRecommendation"],
            "eligible-for-working-availability-review",
        )
        self.assertEqual(compiled["forbiddenRecommendations"], ["reviewed", "standard"])

    def test_main_formats_ium10_validation_errors_with_ium11_prefix(self):
        stderr = StringIO()
        with patch(
            "scripts.validate_ium11.validate_ium11_repository",
            side_effect=IUM10ValidationError("broken IUM10 prerequisite"),
        ), redirect_stderr(stderr):
            self.assertEqual(main([]), 1)
        self.assertEqual(
            stderr.getvalue(),
            "IUM11 repository validation failed: broken IUM10 prerequisite\n",
        )


class IUM11EvidencePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(cls.root / "roadmap/time-model.json")
        cls.protocol = validate_pilot_protocol(
            load_json(cls.root / "pilot/pilot-protocol.json"), cls.time_model
        )

    def test_unknown_or_personal_fields_fail_closed(self):
        for field, value in [
            ("studentName", "Ada"),
            ("schoolName", "Beispielgymnasium"),
            ("freeText", "Beobachtung"),
            ("studentProductUrl", "file:///produkt.txt"),
            ("ipAddress", "192.0.2.1"),
        ]:
            payload = valid_cluster_package()
            payload[field] = value
            with self.subTest(field=field):
                with self.assertRaisesRegex(IUM11ValidationError, "fields|prohibited"):
                    validate_evidence_package(payload, self.protocol, self.time_model)

    def test_small_group_exports_no_counts(self):
        payload = valid_cluster_package()
        payload["learnerPulseEvidence"] = {"status": "suppressed-small-group"}
        validated = validate_evidence_package(payload, self.protocol, self.time_model)
        self.assertEqual(
            validated["learnerPulseEvidence"], {"status": "suppressed-small-group"}
        )

    def test_school_year_accepts_any_four_digit_year_prefix(self):
        payload = valid_cluster_package()
        payload["context"]["schoolYear"] = "1999-00"
        validated = validate_evidence_package(payload, self.protocol, self.time_model)
        self.assertEqual(validated["context"]["schoolYear"], "1999-00")

    def test_one_third_disagree_creates_warning(self):
        pulse = reported_pulse(agree=8, partly=0, disagree=4, no_answer=0)
        result = evaluate_learner_pulse(pulse, self.protocol)
        self.assertEqual(result["warnings"][0]["itemId"], "clarity")
        self.assertEqual(result["warnings"][0]["status"], "open")

    def test_nested_and_warning_fields_fail_closed(self):
        mutations = [
            ("context", "schoolName", "Beispielgymnasium"),
            ("deliveryTimeEvidence", "freeText", "Beobachtung"),
            ("learningQualityEvidence", "studentProductUrl", "file:///produkt.txt"),
            ("learnerPulseEvidence", "ipAddress", "192.0.2.1"),
            ("technicalPrivacyEvidence", "telemetry", True),
        ]
        for parent, field, value in mutations:
            payload = valid_cluster_package()
            payload[parent][field] = value
            with self.subTest(parent=parent, field=field):
                with self.assertRaisesRegex(IUM11ValidationError, "fields|prohibited"):
                    validate_evidence_package(payload, self.protocol, self.time_model)

        payload = valid_cluster_package()
        payload["developmentWarnings"] = [
            {"id": "WARN-clarity", "itemId": "clarity", "status": "open", "freeText": "x"}
        ]
        with self.assertRaisesRegex(IUM11ValidationError, "fields|warnings"):
            validate_evidence_package(payload, self.protocol, self.time_model)

    def test_pulse_rejects_non_aggregate_or_invalid_forms(self):
        mutations = [
            ("classResponseCount", True),
            ("classResponseCount", 9),
            ("items", reported_pulse()["items"] + [reported_pulse()["items"][0]]),
        ]
        for field, value in mutations:
            payload = valid_cluster_package()
            payload["learnerPulseEvidence"][field] = value
            with self.subTest(field=field):
                with self.assertRaises(IUM11ValidationError):
                    validate_evidence_package(payload, self.protocol, self.time_model)

        payload = valid_cluster_package()
        payload["learnerPulseEvidence"]["items"][0]["itemId"] = "supportUsefulness"
        with self.assertRaisesRegex(IUM11ValidationError, "order"):
            validate_evidence_package(payload, self.protocol, self.time_model)

        payload = valid_cluster_package()
        payload["learnerPulseEvidence"] = {"status": "suppressed-small-group", "classResponseCount": 9}
        with self.assertRaises(IUM11ValidationError):
            validate_evidence_package(payload, self.protocol, self.time_model)

    def test_package_rejects_contract_mismatches_and_untrusted_warnings(self):
        mutations = [
            ("schemaVersion", 2),
            ("protocolVersion", "2.0.0"),
            ("toolVersion", "2.0.0"),
            ("protocolFingerprint", "0" * 64),
            ("timeModelFingerprint", "0" * 64),
        ]
        for field, value in mutations:
            payload = valid_cluster_package()
            payload[field] = value
            with self.subTest(field=field):
                with self.assertRaises(IUM11ValidationError):
                    validate_evidence_package(payload, self.protocol, self.time_model)

        payload = valid_cluster_package()
        payload["learnerPulseEvidence"] = reported_pulse(agree=8, partly=0, disagree=4, no_answer=0)
        payload["developmentWarnings"] = []
        with self.assertRaisesRegex(IUM11ValidationError, "warnings"):
            validate_evidence_package(payload, self.protocol, self.time_model)

    def test_package_rejects_claimed_results_that_differ_from_derived_evidence(self):
        cluster_mutations = (
            lambda payload: payload["learningQualityEvidence"]["moduleResults"][0]["criteria"][0].__setitem__("band", "mixed"),
            lambda payload: payload["learningQualityEvidence"]["integrationResults"][0].__setitem__("handoffReused", False),
        )
        for mutate in cluster_mutations:
            payload = valid_cluster_package()
            mutate(payload)
            with self.subTest(package_type="cluster", mutation=mutate):
                with self.assertRaisesRegex(IUM11ValidationError, "result|results"):
                    validate_evidence_package(payload, self.protocol, self.time_model)

        annual = valid_annual_package()
        annual["learningQualityEvidence"]["moduleResults"][0]["criteria"][0]["band"] = "weak"
        with self.assertRaisesRegex(IUM11ValidationError, "result|results"):
            validate_evidence_package(annual, self.protocol, self.time_model)

        for payload in (valid_cluster_package(), valid_annual_package()):
            payload["result"] = "fail"
            with self.subTest(package_type=payload["packageType"], mutation="top-level"):
                with self.assertRaisesRegex(IUM11ValidationError, "result"):
                    validate_evidence_package(payload, self.protocol, self.time_model)

    def test_reported_pulse_with_nine_valid_responses_fails_closed(self):
        payload = valid_cluster_package()
        payload["learnerPulseEvidence"] = reported_pulse(
            agree=8, partly=0, disagree=1, no_answer=1
        )
        with self.assertRaisesRegex(IUM11ValidationError, "fewer than 10 valid"):
            validate_evidence_package(payload, self.protocol, self.time_model)

    def test_annual_package_requires_bound_cluster_totals(self):
        payload = valid_annual_package()
        self.assertEqual(
            validate_evidence_package(payload, self.protocol, self.time_model)["scopeType"],
            "annual",
        )
        payload["deliveryTimeEvidence"]["clusterActualUnits"][0]["actualUnits"] += 1
        with self.assertRaisesRegex(IUM11ValidationError, "sum"):
            validate_evidence_package(payload, self.protocol, self.time_model)

    def test_all_prohibited_field_names_fail_closed_in_every_evidence_object(self):
        targets = (
            lambda package: package,
            lambda package: package["context"],
            lambda package: package["deliveryTimeEvidence"],
            lambda package: package["learningQualityEvidence"],
            lambda package: package["learnerPulseEvidence"],
            lambda package: package["technicalPrivacyEvidence"],
        )
        for target in targets:
            for field in self.protocol["prohibitedFieldNames"]:
                payload = valid_cluster_package()
                target(payload)[field] = "prohibited"
                with self.subTest(target=target, field=field):
                    with self.assertRaisesRegex(IUM11ValidationError, "fields|prohibited"):
                        validate_evidence_package(payload, self.protocol, self.time_model)

        for field in self.protocol["prohibitedFieldNames"]:
            payload = valid_cluster_package()
            payload["developmentWarnings"] = [{
                "id": "WARN-clarity", "itemId": "clarity", "status": "open", field: "prohibited"
            }]
            with self.subTest(target="warning", field=field):
                with self.assertRaisesRegex(IUM11ValidationError, "fields|prohibited"):
                    validate_evidence_package(payload, self.protocol, self.time_model)

    def test_aggregate_types_and_privacy_gate_fail_closed(self):
        mutations = [
            ("deliveryTimeEvidence", "plannedUnits", True),
            ("deliveryTimeEvidence", "actualUnits", -1),
            ("deliveryTimeEvidence", "technicalStartupMinutes", True),
            ("deliveryTimeEvidence", "fallbackActivated", 1),
            ("technicalPrivacyEvidence", "fallbackEquivalentLearningFunction", 0),
            ("technicalPrivacyEvidence", "privacyGate", "fail"),
        ]
        for parent, field, value in mutations:
            payload = valid_cluster_package()
            payload[parent][field] = value
            with self.subTest(parent=parent, field=field):
                with self.assertRaises(IUM11ValidationError):
                    validate_evidence_package(payload, self.protocol, self.time_model)

        payload = valid_cluster_package()
        payload["learnerPulseEvidence"]["items"][0]["agree"] = -1
        with self.assertRaises(IUM11ValidationError):
            validate_evidence_package(payload, self.protocol, self.time_model)


class IUM11ClusterResultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(root / "roadmap/time-model.json")
        cls.protocol = validate_pilot_protocol(
            load_json(root / "pilot/pilot-protocol.json"), cls.time_model
        )

    def derive(self, payload):
        cluster = self.protocol["clustersById"][payload["scopeId"]]
        return derive_cluster_result(payload, cluster, self.protocol)

    def test_positive_cluster_requires_every_gate(self):
        expected_module_counts = {
            "CLUSTER-7-DATA-CODING": 2,
            "CLUSTER-7-PROGRAMMING": 2,
            "CLUSTER-7-NET-SECURITY": 3,
            "CLUSTER-7-DATA-MEDIA-SOCIETY": 3,
        }
        for scope_id, module_count in expected_module_counts.items():
            payload = valid_cluster_package(scope_id=scope_id)
            with self.subTest(scope_id=scope_id):
                result = self.derive(payload)
                self.assertEqual(result["result"], "pass")
                self.assertEqual(
                    [item["result"] for item in result["moduleResults"]],
                    ["pass"] * module_count,
                )
                self.assertEqual(result["integrationResult"]["result"], "pass")
                self.assertEqual(result["developmentWarnings"], [])
                self.assertEqual(result["fallbackDeltaUnits"], 0)

    def test_mixed_or_weak_must_criterion_fails(self):
        for scope_id in self.protocol["clustersById"]:
            baseline = valid_cluster_package(scope_id=scope_id)
            for module_index, module in enumerate(baseline["learningQualityEvidence"]["moduleResults"]):
                for criterion_index, _ in enumerate(module["criteria"]):
                    for band in ("mixed", "weak"):
                        payload = valid_cluster_package(scope_id=scope_id)
                        payload["learningQualityEvidence"]["moduleResults"][module_index]["criteria"][criterion_index]["band"] = band
                        with self.subTest(scope_id=scope_id, module_index=module_index, criterion_index=criterion_index, band=band):
                            result = self.derive(payload)
                            self.assertEqual(result["result"], "fail")
                            self.assertEqual(result["moduleResults"][module_index]["result"], "fail")

    def test_each_cluster_applies_non_compensating_budget_and_fallback_delta(self):
        expected_fallback_deltas = {
            "CLUSTER-7-DATA-CODING": 3,
            "CLUSTER-7-PROGRAMMING": 2,
            "CLUSTER-7-NET-SECURITY": 3,
            "CLUSTER-7-DATA-MEDIA-SOCIETY": 6,
        }
        for scope_id, fallback_delta in expected_fallback_deltas.items():
            payload = valid_cluster_package(scope_id=scope_id)
            payload["deliveryTimeEvidence"]["actualUnits"] += 1
            with self.subTest(scope_id=scope_id):
                result = self.derive(payload)
                self.assertEqual(result["result"], "fail")
                self.assertEqual(result["fallbackDeltaUnits"], fallback_delta)

    def test_each_missing_phase_fails_even_if_claimed_complete(self):
        for scope_id in self.protocol["clustersById"]:
            payload = valid_cluster_package(scope_id=scope_id)
            expected_phase_ids = payload["deliveryTimeEvidence"]["completedPhaseIds"]
            for missing_phase_id in expected_phase_ids:
                changed = valid_cluster_package(scope_id=scope_id)
                changed["deliveryTimeEvidence"]["completedPhaseIds"] = [
                    phase_id for phase_id in expected_phase_ids if phase_id != missing_phase_id
                ]
                with self.subTest(scope_id=scope_id, missing_phase_id=missing_phase_id):
                    self.assertEqual(self.derive(changed)["result"], "fail")

    def test_integration_handoff_and_technical_gates_fail(self):
        mutations = (
            ("handoff product absent", lambda payload: payload["learningQualityEvidence"]["integrationResults"][0].update(handoffProductPresent=False)),
            ("handoff not reused", lambda payload: payload["learningQualityEvidence"]["integrationResults"][0].update(handoffReused=False)),
            ("technical function failed", lambda payload: payload["technicalPrivacyEvidence"].update(technicalFunction="fail")),
            ("non-equivalent fallback", lambda payload: payload["deliveryTimeEvidence"].update(fallbackActivated=True) or payload["technicalPrivacyEvidence"].update(technicalFunction="fail", fallbackEquivalentLearningFunction=False)),
            ("privacy gate failed", lambda payload: payload["technicalPrivacyEvidence"].update(privacyGate="fail")),
        )
        for scope_id in self.protocol["clustersById"]:
            for label, mutate in mutations:
                payload = valid_cluster_package(scope_id=scope_id)
                mutate(payload)
                with self.subTest(scope_id=scope_id, label=label):
                    result = self.derive(payload)
                    self.assertEqual(result["result"], "fail")
                    self.assertEqual(result["integrationResult"]["result"], "fail" if "handoff" in label else "pass")

    def test_mixed_or_weak_integration_criterion_fails(self):
        for scope_id in self.protocol["clustersById"]:
            for criterion_index in (0, 1):
                for band in ("mixed", "weak"):
                    payload = valid_cluster_package(scope_id=scope_id)
                    payload["learningQualityEvidence"]["integrationResults"][0]["criteria"][criterion_index]["band"] = band
                    with self.subTest(scope_id=scope_id, criterion_index=criterion_index, band=band):
                        result = self.derive(payload)
                        self.assertEqual(result["result"], "fail")
                        self.assertEqual(result["integrationResult"]["result"], "fail")

    def test_equivalent_activated_fallback_replaces_failed_technical_function_within_budget(self):
        for scope_id in self.protocol["clustersById"]:
            payload = valid_cluster_package(scope_id=scope_id)
            payload["deliveryTimeEvidence"]["fallbackActivated"] = True
            payload["technicalPrivacyEvidence"].update(
                technicalFunction="fail",
                fallbackEquivalentLearningFunction=True,
            )
            with self.subTest(scope_id=scope_id):
                self.assertEqual(self.derive(payload)["result"], "pass")

    def test_interpretability_loss_has_priority_over_other_failures(self):
        payload = valid_cluster_package()
        payload["deliveryTimeEvidence"]["externalDisruptionCode"] = "interpretability-lost"
        payload["deliveryTimeEvidence"]["actualUnits"] += 1

        result = self.derive(payload)

        self.assertEqual(result["result"], "not-evaluable")
        self.assertEqual(result["fallbackDeltaUnits"], 0)

    def test_learner_warning_boundaries_are_derived_from_valid_responses(self):
        cases = (
            (3, 10, "pass", []),
            (4, 12, "fail", ["WARN-clarity", "WARN-cognitiveEngagement", "WARN-supportUsefulness"]),
            (4, 13, "pass", []),
        )
        for scope_id in self.protocol["clustersById"]:
            for disagree, valid, expected_result, expected_warning_ids in cases:
                payload = valid_cluster_package(scope_id=scope_id)
                payload["learnerPulseEvidence"] = reported_pulse(
                    agree=valid - disagree, partly=0, disagree=disagree, no_answer=0
                )
                with self.subTest(scope_id=scope_id, disagree=disagree, valid=valid):
                    result = self.derive(payload)
                    self.assertEqual(result["result"], expected_result)
                    self.assertEqual(
                        [warning["id"] for warning in result["developmentWarnings"]],
                        expected_warning_ids,
                    )


class IUM11DecisionPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(cls.root / "roadmap/time-model.json")
        cls.protocol = validate_pilot_protocol(
            load_json(cls.root / "pilot/pilot-protocol.json"),
            cls.time_model,
        )

    def test_positive_minimal_pilot_only_recommends_working_review(self):
        package = build_decision_package(
            five_positive_packages(),
            self.protocol,
            self.time_model,
        )
        self.assertEqual(
            package["recommendation"],
            "eligible-for-working-availability-review",
        )
        self.assertEqual(package["statementBoundary"], "documented-conditions-only")
        self.assertEqual(package["reviewStatus"], {
            "fach": "not-started",
            "engineeringPrivacy": "not-started",
            "commissioner": "not-started",
        })
        self.assertEqual(package["availabilityGateResults"], {
            "capacity": "passed",
            "integration": "passed",
            "technical": "passed",
            "privacy": "passed",
            "pilot": "passed",
        })
        self.assertNotIn("timeModelMutation", package)

    def test_annual_requires_four_positive_same_version_clusters(self):
        mutations = [
            lambda packages: packages.pop(0),
            lambda packages: packages[0].__setitem__("result", "fail"),
            lambda packages: packages[0].__setitem__("protocolVersion", "2.0.0"),
            lambda packages: packages[0].__setitem__("timeModelFingerprint", "0" * 64),
        ]
        for mutate in mutations:
            packages = five_positive_packages()
            mutate(packages)
            with self.subTest(mutation=mutate):
                with self.assertRaises(IUM11ValidationError):
                    build_decision_package(packages, self.protocol, self.time_model)

    def test_annual_interpretability_loss_builds_not_evaluable_decision(self):
        packages = five_positive_packages()
        annual = packages[-1]
        annual["deliveryTimeEvidence"]["externalDisruptionCode"] = "interpretability-lost"
        annual["result"] = "not-evaluable"

        package = build_decision_package(packages, self.protocol, self.time_model)

        self.assertEqual(package["pilotResults"][-1]["result"], "not-evaluable")
        self.assertEqual(package["availabilityGateResults"]["pilot"], "failed")
        self.assertEqual(package["recommendation"], "not-evaluable")
        validate_decision_package(package, self.protocol, self.time_model)

    def test_annual_failure_builds_repeat_required_decision(self):
        packages = five_positive_packages()
        annual = packages[-1]
        integration = annual["learningQualityEvidence"]["integrationResults"][0]
        integration["handoffReused"] = False
        integration["result"] = "fail"
        annual["result"] = "fail"

        package = build_decision_package(packages, self.protocol, self.time_model)

        self.assertEqual(package["pilotResults"][-1]["result"], "fail")
        self.assertEqual(package["availabilityGateResults"]["integration"], "failed")
        self.assertEqual(package["availabilityGateResults"]["pilot"], "failed")
        self.assertEqual(package["recommendation"], "repeat-required")
        validate_decision_package(package, self.protocol, self.time_model)

    def test_39_annual_units_never_pass_capacity_or_become_eligible(self):
        packages = five_positive_packages()
        annual = packages[-1]
        annual["deliveryTimeEvidence"]["actualUnits"] = 39
        annual["deliveryTimeEvidence"]["clusterActualUnits"][0]["actualUnits"] = 7
        annual["result"] = "fail"

        package = build_decision_package(packages, self.protocol, self.time_model)

        self.assertEqual(package["timeAndFallbackSummary"]["actualUnits"], 39)
        self.assertEqual(package["availabilityGateResults"]["capacity"], "failed")
        self.assertEqual(package["recommendation"], "repeat-required")
        validate_decision_package(package, self.protocol, self.time_model)

    def test_no_cluster_time_compensation(self):
        packages = five_positive_packages()
        packages_by_scope(packages)["CLUSTER-7-DATA-CODING"]["deliveryTimeEvidence"]["actualUnits"] = 9
        packages_by_scope(packages)["CLUSTER-7-PROGRAMMING"]["deliveryTimeEvidence"]["actualUnits"] = 10
        with self.assertRaisesRegex(IUM11ValidationError, "cluster budget"):
            build_decision_package(packages, self.protocol, self.time_model)

    def test_annual_result_reobserves_every_annual_gate(self):
        mutations = (
            lambda annual: annual["learningQualityEvidence"]["moduleResults"][0]["criteria"][0].__setitem__("band", "weak"),
            lambda annual: annual["learningQualityEvidence"]["integrationResults"][0].__setitem__("handoffReused", False),
            lambda annual: annual["deliveryTimeEvidence"].__setitem__("requiredLearningPhasesCompleted", False),
            lambda annual: annual["technicalPrivacyEvidence"].__setitem__("technicalFunction", "fail"),
        )
        for mutate in mutations:
            packages = five_positive_packages()
            mutate(packages[-1])
            with self.subTest(mutation=mutate):
                with self.assertRaises(IUM11ValidationError):
                    build_decision_package(packages, self.protocol, self.time_model)

    def test_derive_annual_result_has_closed_public_shape(self):
        packages = five_positive_packages()
        result = derive_annual_result(packages[-1], packages[:4], self.protocol)
        self.assertEqual(result, {
            "result": "pass",
            "actualUnits": 40,
            "availabilityGateResults": {
                "capacity": "passed",
                "integration": "passed",
                "technical": "passed",
                "privacy": "passed",
                "pilot": "passed",
            },
        })

    def test_derive_annual_result_requires_distinct_version_bound_sources(self):
        for mutate in (
            lambda packages: packages[1].__setitem__("packageId", packages[0]["packageId"]),
            lambda packages: packages[1].__setitem__("protocolVersion", "2.0.0"),
            lambda packages: packages[1].__setitem__("protocolFingerprint", "0" * 64),
            lambda packages: packages[1].__setitem__("toolVersion", "2.0.0"),
            lambda packages: packages[1].__setitem__("timeModelFingerprint", "0" * 64),
        ):
            packages = five_positive_packages()
            mutate(packages)
            with self.subTest(mutation=mutate):
                with self.assertRaises(IUM11ValidationError):
                    derive_annual_result(packages[-1], packages[:4], self.protocol)

    def test_derive_annual_result_revalidates_every_cluster_semantically(self):
        def claim_pass_for_mixed_evidence(packages):
            packages[0]["learningQualityEvidence"]["moduleResults"][0]["criteria"][0]["band"] = "mixed"

        def make_consistent_negative_cluster(packages):
            module = packages[0]["learningQualityEvidence"]["moduleResults"][0]
            module["criteria"][0]["band"] = "mixed"
            module["result"] = "fail"
            packages[0]["result"] = "fail"

        mutations = (
            claim_pass_for_mixed_evidence,
            make_consistent_negative_cluster,
            lambda packages: packages.__setitem__(1, copy.deepcopy(packages[0])),
            lambda packages: packages[0].__setitem__("protocolVersion", "2.0.0"),
        )
        for mutate in mutations:
            packages = five_positive_packages()
            mutate(packages)
            with self.subTest(mutation=mutate):
                with self.assertRaises(IUM11ValidationError):
                    derive_annual_result(packages[-1], packages[:4], self.protocol)

    def test_decision_is_deterministic_and_does_not_mutate_inputs(self):
        packages = five_positive_packages()
        packages_before = canonical_sha256(packages)
        time_model_before = canonical_sha256(self.time_model)

        first = build_decision_package(packages, self.protocol, self.time_model)
        second = build_decision_package(list(reversed(packages)), self.protocol, self.time_model)

        self.assertEqual(first, second)
        self.assertRegex(
            first["packageId"],
            r"^PKG-[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        )
        self.assertEqual(canonical_sha256(packages), packages_before)
        self.assertEqual(canonical_sha256(self.time_model), time_model_before)
        self.assertEqual(
            first["sourcePackageIds"],
            [package["packageId"] for package in packages],
        )

    def test_decision_package_and_schema_are_recursively_closed(self):
        package = build_decision_package(
            five_positive_packages(),
            self.protocol,
            self.time_model,
        )
        self.assertEqual(set(package), {
            "schemaVersion", "packageType", "packageId", "protocolVersion",
            "protocolFingerprint", "toolVersion", "timeModelFingerprint",
            "sourcePackageIds", "pilotResults", "moduleResults",
            "integrationResults", "availabilityGateResults",
            "timeAndFallbackSummary", "technicalPrivacySummary",
            "developmentWarnings", "statementBoundary", "recommendation",
            "reviewStatus", "retentionClass",
        })
        schema = load_json(self.root / "pilot/schemas/decision-package.schema.json")

        def assert_objects_closed(node):
            if isinstance(node, dict):
                if node.get("type") == "object":
                    self.assertIs(node.get("additionalProperties"), False)
                for value in node.values():
                    assert_objects_closed(value)
            elif isinstance(node, list):
                for value in node:
                    assert_objects_closed(value)

        assert_objects_closed(schema)
        self.assertEqual(set(schema["required"]), set(package))

    def test_public_decision_boundary_rejects_maturity_and_status_mutations(self):
        for recommendation in ("reviewed", "standard", "available", "green"):
            package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
            package["recommendation"] = recommendation
            with self.subTest(recommendation=recommendation):
                with self.assertRaises(IUM11ValidationError):
                    validate_decision_package(package, self.protocol, self.time_model)

    def test_positive_recommendation_rejects_failed_modules_or_warnings(self):
        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["moduleResults"][0]["result"] = "fail"
        with self.assertRaises(IUM11ValidationError):
            validate_decision_package(package, self.protocol, self.time_model)

        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["developmentWarnings"] = [
            {"id": "WARN-clarity", "itemId": "clarity", "status": "open"},
        ]
        with self.assertRaises(IUM11ValidationError):
            validate_decision_package(package, self.protocol, self.time_model)

        for field, value in (("semanticCoverageStatus", "covered"), ("status", "available")):
            package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
            package[field] = value
            with self.subTest(field=field):
                with self.assertRaises(IUM11ValidationError):
                    validate_decision_package(package, self.protocol, self.time_model)

    def test_decision_rejects_negative_cluster_with_positive_annual_result(self):
        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["pilotResults"][0]["result"] = "fail"
        package["availabilityGateResults"]["pilot"] = "failed"
        package["recommendation"] = "repeat-required"

        with self.assertRaisesRegex(IUM11ValidationError, "cluster|first four"):
            validate_decision_package(package, self.protocol, self.time_model)

    def test_decision_rejects_negative_cluster_module_or_integration_results(self):
        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["pilotResults"][-1]["result"] = "fail"
        package["availabilityGateResults"]["pilot"] = "failed"
        package["recommendation"] = "repeat-required"
        package["moduleResults"][0]["result"] = "fail"
        with self.assertRaisesRegex(IUM11ValidationError, "module"):
            validate_decision_package(package, self.protocol, self.time_model)

        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["pilotResults"][-1]["result"] = "fail"
        package["integrationResults"][0]["result"] = "fail"
        package["integrationResults"][0]["fallbackDeltaUnits"] = 3
        package["availabilityGateResults"]["integration"] = "failed"
        package["availabilityGateResults"]["pilot"] = "failed"
        package["timeAndFallbackSummary"]["fallbackUnits"] = 3
        package["timeAndFallbackSummary"]["requiredUnits"] = 43
        package["recommendation"] = "repeat-required"
        with self.assertRaisesRegex(IUM11ValidationError, "integration"):
            validate_decision_package(package, self.protocol, self.time_model)

    def test_decision_rejects_unknown_development_warning(self):
        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["pilotResults"][-1]["result"] = "fail"
        package["availabilityGateResults"]["pilot"] = "failed"
        package["recommendation"] = "repeat-required"
        package["developmentWarnings"] = [
            {"id": "WARN-impossible", "itemId": "impossible", "status": "open"},
        ]

        with self.assertRaisesRegex(IUM11ValidationError, "warning"):
            validate_decision_package(package, self.protocol, self.time_model)

    def test_public_decision_boundary_rejects_source_review_and_time_mutations(self):
        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["sourcePackageIds"].pop()
        with self.assertRaises(IUM11ValidationError):
            validate_decision_package(package, self.protocol, self.time_model)

        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["pilotResults"][1]["scopeId"] = package["pilotResults"][0]["scopeId"]
        with self.assertRaises(IUM11ValidationError):
            validate_decision_package(package, self.protocol, self.time_model)

        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["pilotResults"][-1]["result"] = "fail"
        package["availabilityGateResults"]["pilot"] = "failed"
        package["recommendation"] = "repeat-required"
        package["reviewStatus"]["fach"] = "passed"
        with self.assertRaisesRegex(IUM11ValidationError, "Reviews|reviews"):
            validate_decision_package(package, self.protocol, self.time_model)

        package = build_decision_package(five_positive_packages(), self.protocol, self.time_model)
        package["timeAndFallbackSummary"]["actualUnits"] = 41
        package["availabilityGateResults"]["capacity"] = "failed"
        package["recommendation"] = "repeat-required"
        with self.assertRaisesRegex(IUM11ValidationError, "40|budget"):
            validate_decision_package(package, self.protocol, self.time_model)

    def test_build_rejects_duplicate_scopes_and_mixed_fingerprints(self):
        packages = five_positive_packages()
        packages[-1] = valid_cluster_package("CLUSTER-7-DATA-CODING")
        with self.assertRaises(IUM11ValidationError):
            build_decision_package(packages, self.protocol, self.time_model)

        packages = five_positive_packages()
        packages[1]["protocolFingerprint"] = "0" * 64
        with self.assertRaises(IUM11ValidationError):
            build_decision_package(packages, self.protocol, self.time_model)

    def _private_cli_arguments(self, directory, packages=None):
        packages = five_positive_packages() if packages is None else packages
        arguments = ["--root", str(self.root)]
        for index, package in enumerate(packages, start=1):
            path = directory / f"evidence-{index}.json"
            path.write_text(json.dumps(package), encoding="utf-8")
            arguments.extend(("--evidence", str(path)))
        return arguments

    def test_private_offline_cli_writes_valid_decision_atomically(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            output = directory / "decision.json"
            arguments = self._private_cli_arguments(directory)
            arguments.extend(("--decision-output", str(output)))

            self.assertEqual(main(arguments), 0)

            self.assertTrue(output.is_file())
            validate_decision_package(
                load_json(output),
                self.protocol,
                self.time_model,
            )
            self.assertEqual(
                sorted(path.name for path in directory.iterdir()),
                ["decision.json", *[f"evidence-{index}.json" for index in range(1, 6)]],
            )

    def test_private_offline_cli_rejects_wrong_count_public_paths_and_existing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)

            output = directory / "wrong-count.json"
            arguments = self._private_cli_arguments(directory, five_positive_packages()[:4])
            arguments.extend(("--decision-output", str(output)))
            self.assertEqual(main(arguments), 1)
            self.assertFalse(output.exists())

            output = directory / "public-path.json"
            arguments = self._private_cli_arguments(directory)
            arguments[3] = str(self.root / "pilot/pilot-protocol.json")
            arguments.extend(("--decision-output", str(output)))
            self.assertEqual(main(arguments), 1)
            self.assertFalse(output.exists())

            output = directory / "existing.json"
            output.write_text("sentinel", encoding="utf-8")
            arguments = self._private_cli_arguments(directory)
            arguments.extend(("--decision-output", str(output)))
            self.assertEqual(main(arguments), 1)
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_private_offline_cli_invalid_input_leaves_no_partial_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            output = directory / "decision.json"
            arguments = self._private_cli_arguments(directory)
            Path(arguments[3]).write_text("{not-json", encoding="utf-8")
            arguments.extend(("--decision-output", str(output)))
            files_before = sorted(path.name for path in directory.iterdir())

            self.assertEqual(main(arguments), 1)

            self.assertFalse(output.exists())
            self.assertEqual(
                sorted(path.name for path in directory.iterdir()),
                files_before,
            )


class IUM11PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.time_model = load_json(cls.root / "roadmap/time-model.json")
        cls.protocol = validate_pilot_protocol(
            load_json(cls.root / "pilot/pilot-protocol.json"),
            cls.time_model,
        )

    def copy_publication_fixture(self, destination):
        shutil.copytree(self.root / "pilot", destination / "pilot")
        for relative_path in (
            "README.md",
            "scripts/validate_ium11.py",
            "scripts/build_ium11_cockpit.py",
            "scripts/validate_phase0.py",
            "tests/test_validate_ium11.py",
            "tests/test_ium11_cockpit_contract.py",
            "tests/test_validate_phase0.py",
            "docs/superpowers/plans/2026-08-01-ium11-grade7-working-40-pilot-implementation.md",
        ):
            source = self.root / relative_path
            target = destination / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def test_readme_states_exact_pilot_boundary(self):
        text = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn("IUM11-Pilotinstrument", text)
        self.assertIn("keine reale Pilotierung", text)
        self.assertIn("eligible-for-working-availability-review", text)
        self.assertIn(
            "Flexible Vertiefungs-, Transfer- und Projektmodule bleiben",
            text,
        )
        for forbidden in [
            "GRADE-7-WORKING-40 ist available",
            "GRADE-7-WORKING-40 ist reviewed",
            "Pilotierung abgeschlossen",
        ]:
            self.assertNotIn(forbidden, text)

    def test_guides_name_privacy_retention_and_repeat_rules(self):
        teacher = (self.root / "pilot/docs/teacher-guide.md").read_text(
            encoding="utf-8"
        )
        review = (self.root / "pilot/docs/review-guide.md").read_text(
            encoding="utf-8"
        )
        for anchor in [
            "unter zehn",
            "keine Freitexte",
            "bis zur Auftraggeberentscheidung",
            "löschen",
            "fail",
            "not-evaluable",
            "wiederholen",
        ]:
            self.assertIn(anchor, teacher)
        for anchor in [
            "Fachreview",
            "Engineering-/Privacyreview",
            "Auftraggebergate",
            "zweite unabhängige",
            "documented-conditions-only",
        ]:
            self.assertIn(anchor, review)

    def test_repository_publication_contract_is_complete_and_current(self):
        result = validate_ium11_script._validate_publication_contract(
            self.root,
            self.protocol,
        )
        self.assertEqual(
            result,
            {"productFiles": 23, "syntheticExamples": 7, "publications": 3},
        )

    def test_publication_contract_rejects_documentation_version_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.copy_publication_fixture(root)
            guide = root / "pilot/docs/teacher-guide.md"
            guide.write_text(
                guide.read_text(encoding="utf-8").replace("1.0.0", "2.0.0"),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(IUM11ValidationError, "version|Version"):
                validate_ium11_script._validate_publication_contract(
                    root,
                    self.protocol,
                )

    def test_repository_scan_rejects_unexpected_pilot_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.copy_publication_fixture(root)
            (root / "pilot/real-evidence.json").write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(IUM11ValidationError, "JSON|json"):
                validate_ium11_script._validate_publication_contract(
                    root,
                    self.protocol,
                )

    def test_publication_contract_rejects_conflicting_declarations_in_every_document(self):
        conflicting_declarations = (
            "Pilotierung abgeschlossen.",
            "Available ist der Working-40-Pfad.",
            "Der Working-40-Pfad: available.",
            "Der Working-40-Pfad ist available.",
            "Der Working-40-Pfad ist reviewed.",
            "Der Working-40-Pfad ist standard.",
            "Die reale Pilotierung wurde abgeschlossen.",
            "Der reale Pilot ist abgeschlossen.",
            "AvailabilityStatus: available",
            "availabilityStatus : available",
            "availabilityStatus: reviewed",
            "status: available",
            "Empfehlung: eligible-for-standard-review.",
            "Protokollversion `9.9.9`.",
            "Protokoll-Version 9.9.9.",
            "Version des Protokolls: 9.9.9.",
            "Werkzeugversion `9.9.9`.",
            "Der Umfang beträgt 41 UE.",
            "Der Umfang umfasst 5 Cluster.",
            "Cluster: 5.",
            "Der Umfang umfasst 11 Module.",
            "Module: 11.",
            "Der Umfang umfasst 6 Pilotstufen.",
            "Die Privacy-Schwelle 9 gilt.",
            "Privacy-Schwelle: 9.",
        )
        for relative_path in (
            "README.md",
            "pilot/docs/teacher-guide.md",
            "pilot/docs/review-guide.md",
        ):
            with self.subTest(document=relative_path):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.copy_publication_fixture(root)
                    publication = root / relative_path
                    original = publication.read_text(encoding="utf-8")
                    for declaration in conflicting_declarations:
                        with self.subTest(
                            document=relative_path,
                            declaration=declaration,
                        ):
                            publication.write_text(
                                f"{original}\n\n{declaration}\n",
                                encoding="utf-8",
                            )
                            with self.assertRaises(IUM11ValidationError):
                                validate_ium11_script._validate_publication_contract(
                                    root,
                                    self.protocol,
                                )
                    publication.write_text(original, encoding="utf-8")

    def test_publication_contract_allows_negated_boundary_and_future_gate_lines(self):
        negative_counterexamples = (
            "Keine reale Pilotierung ist abgeschlossen.",
            "Weder IUM11 noch der Pfad ist standard.",
            "Der Pfad umfasst nicht 41 UE, sondern 40 UE.",
            "Das Instrument umfasst keine 5 Cluster, sondern 4 Cluster.",
            "eligible-for-standard-review ist ausdrücklich keine zulässige Empfehlung.",
            "Protokollversion 9.9.9 ist ausdrücklich falsch; maßgeblich bleibt 1.0.0.",
            "Der Working-40-Pfad ist nicht available oder reviewed.",
            "Der reale Pilot ist ausdrücklich nicht abgeschlossen.",
        )
        for relative_path in (
            "README.md",
            "pilot/docs/teacher-guide.md",
            "pilot/docs/review-guide.md",
        ):
            with self.subTest(document=relative_path):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.copy_publication_fixture(root)
                    publication = root / relative_path
                    publication.write_text(
                        publication.read_text(encoding="utf-8")
                        + "\n"
                        + "\n".join(negative_counterexamples)
                        + "\n",
                        encoding="utf-8",
                    )
                    review = (root / "pilot/docs/review-guide.md").read_text(
                        encoding="utf-8"
                    )
                    for declaration in (
                        "availabilityStatus: available",
                        "timeFeasibilityStatus: green",
                        "pilotStatus: completed",
                    ):
                        self.assertIn(declaration, review)

                    validate_ium11_script._validate_publication_contract(
                        root,
                        self.protocol,
                    )
