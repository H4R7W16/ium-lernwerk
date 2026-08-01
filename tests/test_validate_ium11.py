import json
import uuid
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts.validate_ium10 import IUM10ValidationError
from scripts.validate_ium11 import (
    IUM11ValidationError,
    canonical_sha256,
    derive_cluster_result,
    evaluate_learner_pulse,
    main,
    validate_evidence_package,
    validate_pilot_protocol,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
    payload = valid_cluster_package()
    root = Path(__file__).resolve().parents[1]
    time_model = load_json(root / "roadmap/time-model.json")
    protocol = validate_pilot_protocol(
        load_json(root / "pilot/pilot-protocol.json"), time_model
    )
    clusters = [
        protocol["clustersById"][cluster_id]
        for cluster_id in protocol["annualPilot"]["clusterIds"]
    ]
    modules = [module for cluster in clusters for module in cluster["modules"]]
    completed_phases = sorted({
        phase_id for module in modules for phase_id in module["requiredPhaseIds"]
    })
    payload["packageType"] = "annual-evidence"
    payload["scopeType"] = "annual"
    payload["scopeId"] = protocol["annualPilot"]["id"]
    payload["deliveryTimeEvidence"] = {
        "plannedUnits": protocol["annualPilot"]["budgetUnits"],
        "actualUnits": protocol["annualPilot"]["budgetUnits"],
        "completedPhaseIds": completed_phases,
        "requiredLearningPhasesCompleted": True,
        "fallbackActivated": False,
        "technicalStartupMinutes": 3,
        "supportDemandBand": "low",
        "externalDisruptionCode": "none",
        "clusterOrder": protocol["annualPilot"]["clusterIds"],
        "clusterActualUnits": [
            {"clusterId": cluster["id"], "actualUnits": cluster["budgetUnits"]}
            for cluster in clusters
        ],
    }
    payload["learningQualityEvidence"] = {
        "moduleResults": [
            {"pilotAssignmentId": module["pilotAssignmentId"], "moduleId": module["moduleId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in module["criteria"]], "result": "pass"}
            for module in modules
        ],
        "integrationResults": [
            {"pilotAssignmentId": cluster["integration"]["pilotAssignmentId"], "integrationContractId": cluster["integration"]["integrationContractId"], "criteria": [{"criterionId": criterion["criterionId"], "band": "strong"} for criterion in cluster["integration"]["criteria"]], "handoffProductPresent": True, "handoffReused": True, "result": "pass"}
            for cluster in clusters
        ],
    }
    return payload


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
