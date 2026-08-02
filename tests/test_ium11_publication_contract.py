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

    def test_emits_exact_nested_field_sets(self):
        contract = self.compile()
        self.assertEqual(set(contract["sourceBindings"]), {
            "protocolPath", "timeModelPath", "protocolVersion", "toolVersion",
            "timeModelFingerprintAlgorithm", "timeModelFingerprint",
        })
        self.assertEqual(set(contract["corePath"]), {
            "variantId", "targetUnits", "clusterCount", "moduleCount",
            "pilotStageCount", "clusters",
        })
        for cluster in contract["corePath"]["clusters"]:
            self.assertEqual(set(cluster), {
                "id", "order", "budgetUnits", "fallbackDeltaUnits",
            })
        self.assertEqual(set(contract["privacyBoundary"]), {
            "minimumLearnerResponses", "personalDataAllowed",
            "realPackagesInRepositoryAllowed",
        })
        self.assertEqual(set(contract["currentAxes"]), {
            "status", "availabilityStatus", "timeFeasibilityStatus",
            "sequenceEvidenceStatus", "pilotStatus", "semanticCoverageStatus",
        })
        self.assertEqual(set(contract["futureDecisionBoundary"]), {
            "requiresCommissionerDecision", "allowedChanges", "unchangedAxes",
            "secondIndependentAnnualRunRequiredForMaturity",
        })
        for row in (
            contract["futureDecisionBoundary"]["allowedChanges"]
            + contract["futureDecisionBoundary"]["unchangedAxes"]
        ):
            self.assertEqual(set(row), {"field", "value"})
        self.assertEqual(set(contract["preservationBoundary"]), {
            "flexibleModulesOutsideCorePreserved", "flexibleModuleSubstitution",
        })

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
                before = copy.deepcopy([protocol, time_model, ium10_result])
                with self.assertRaisesRegex(IUM11PublicationError, message):
                    compile_publication_contract(protocol, time_model, ium10_result)
                after = [protocol, time_model, ium10_result]
                self.assertEqual(after, before)

    def test_rejects_closed_structural_boundaries(self):
        cases = []

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0], protocol["clusters"][1] = (
            protocol["clusters"][1], protocol["clusters"][0]
        )
        cases.append((protocol, self.time_model, self.ium10_result, "cluster"))

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0]["modules"][1]["moduleId"] = "IUM-7-CORE-01"
        cases.append((protocol, self.time_model, self.ium10_result, "module"))

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][3]["modules"].pop()
        cases.append((protocol, self.time_model, self.ium10_result, "module"))

        time_model = copy.deepcopy(self.time_model)
        working_variant = next(
            variant
            for variant in time_model["annualVariants"]
            if variant["id"] == "GRADE-7-WORKING-40"
        )
        time_model["annualVariants"].append(copy.deepcopy(working_variant))
        cases.append((self.protocol, time_model, self.ium10_result, "variant"))

        ium10_result = copy.deepcopy(self.ium10_result)
        del ium10_result["availabilityContracts"]["AVAIL-GRADE-7-WORKING-40"]
        cases.append((self.protocol, self.time_model, ium10_result, "availability"))

        ium10_result = copy.deepcopy(self.ium10_result)
        del ium10_result["gradeJudgements"][7]
        cases.append((self.protocol, self.time_model, ium10_result, "judgement"))

        ium10_result = copy.deepcopy(self.ium10_result)
        ium10_result["annualVariants"]["GRADE-7-WORKING-40"]["targetUnits"] = 41
        cases.append((self.protocol, self.time_model, ium10_result, "variant"))

        for protocol, time_model, ium10_result, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(IUM11PublicationError, message):
                    self.compile(protocol, time_model, ium10_result)

    def test_rejects_protocol_source_and_cluster_identity_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["protocolVersion"] = "2.0.0"
        with self.assertRaisesRegex(IUM11PublicationError, "source"):
            self.compile(protocol=protocol)

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0]["id"] = "CLUSTER-7-UNBOUND"
        with self.assertRaisesRegex(IUM11PublicationError, "cluster"):
            self.compile(protocol=protocol)

    def test_rejects_compensating_cluster_budget_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0]["budgetUnits"] = 7
        protocol["clusters"][1]["budgetUnits"] = 12

        with self.assertRaisesRegex(IUM11PublicationError, "budget"):
            self.compile(protocol=protocol)

    def test_rejects_annual_pilot_variant_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["variantId"] = "GRADE-7-ROBUST-DEMAND"

        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

    def test_rejects_annual_pilot_identity_and_assignment_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["id"] = "ANNUAL-7-UNBOUND"
        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["pilotAssignmentId"] = "PILOT-INT-7-DATA-CODING"
        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

    def test_rejects_annual_pilot_cluster_order_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["clusterIds"][0], protocol["annualPilot"]["clusterIds"][1] = (
            protocol["annualPilot"]["clusterIds"][1],
            protocol["annualPilot"]["clusterIds"][0],
        )

        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

    def test_rejects_grade_7_judgement_availability_drift(self):
        ium10_result = copy.deepcopy(self.ium10_result)
        ium10_result["gradeJudgements"][7]["availabilityStatus"] = "available"

        with self.assertRaisesRegex(IUM11PublicationError, "availabilityStatus"):
            self.compile(ium10_result=ium10_result)
