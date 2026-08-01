import json
from pathlib import Path
import unittest

from scripts.validate_ium11 import canonical_sha256, validate_pilot_protocol


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
