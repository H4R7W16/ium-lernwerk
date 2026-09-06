"""The decision packet must not silently lose evidence or authorize deployment."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_v2_cutover import validate, CutoverError, current_digest, digest


class CutoverContractTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((ROOT / 'roadmap/v2/cutover/review.json').read_text(encoding='utf8'))

    def test_accepted_historical_packet_and_input_digests(self):
        validate(ROOT, self.packet, historical=True)

    def test_checkout_line_endings_do_not_invalidate_same_text(self):
        self.assertEqual(current_digest(b'first\r\nsecond\r\n'), current_digest(b'first\nsecond\n'))

    def test_historical_git_blob_digest_keeps_exact_bytes(self):
        self.assertNotEqual(digest(b'first\r\n'), digest(b'first\n'))

    def test_missing_packet_fails(self):
        with self.assertRaises(CutoverError):
            validate(ROOT, {}, historical=True)

    def test_input_drift_fails(self):
        self.packet['inputDigests']['roadmap/v2/status.json'] = '0' * 64
        with self.assertRaises(CutoverError):
            validate(ROOT, self.packet, historical=True)


MUTATIONS = {
    'missing_gate': lambda d: d['gates'].pop(),
    'duplicate_gate': lambda d: d['gates'].__setitem__(1, copy.deepcopy(d['gates'][0])),
    'reordered_gate': lambda d: d['gates'].reverse(),
    'fabricated_commit': lambda d: d['gates'][0].__setitem__('acceptedCommit', 'a' * 40),
    'wrong_historical_digest': lambda d: d['gates'][0]['artifacts'][0].__setitem__('sha256', '0' * 64),
    'missing_historical_artifact': lambda d: d['gates'][0]['artifacts'].clear(),
    'missing_approval_excerpt': lambda d: d['gates'][0]['approvalEvidence'].__setitem__('excerpt', ''),
    'wrong_approval_path': lambda d: d['gates'][0]['approvalEvidence'].__setitem__('path', '../private'),
    'wrong_candidate': lambda d: d.__setitem__('candidateCommit', 'a' * 40),
    'missing_requirement': lambda d: d['requirements'].pop(),
    'fabricated_coverage': lambda d: d['requirements'][0].__setitem__('coverage', 'fulfilled'),
    'missing_condition': lambda d: d['conditions'].pop(),
    'lost_risk_owner': lambda d: d['conditions'][0].__setitem__('owner', ''),
    'closed_evidence_question': lambda d: next(q for q in d['conditions'] if q['kind'] == 'curriculum-evidence').__setitem__('state', 'done'),
    'changed_condition_text': lambda d: next(q for q in d['conditions'] if q['id'] == 'R7-BUDGET').__setitem__('question', '43 UE sind vorhanden.'),
    'premature_activation': lambda d: d.__setitem__('activeBaseline', 'v2'),
    'premature_decision': lambda d: d.__setitem__('decisionState', 'approved'),
    'selected_option': lambda d: d['options'][0].__setitem__('decision', 'selected'),
    'production_opened': lambda d: d['options'][0].__setitem__('contentProduction', 'open'),
    'pilot_opened': lambda d: d['options'][0].__setitem__('pilot', 'approved'),
    'push_authorized': lambda d: d['options'][0].__setitem__('push', 'authorized'),
    'unknown_work_state': lambda d: d.__setitem__('workStatus', 'green'),
    'missing_input_binding': lambda d: d['inputDigests'].pop('roadmap/v2/status.json'),
    'failed_verification': lambda d: d['verification'].__setitem__('state', 'failed'),
    'activation_without_approval': lambda d: d['activationPlan'].__setitem__('approvalRequired', False),
}


def rejection_test(mutate):
    def test(self):
        mutate(self.packet)
        with self.assertRaises(CutoverError):
            validate(ROOT, self.packet, historical=True)
    return test


for name, mutate in MUTATIONS.items():
    setattr(CutoverContractTests, 'test_reject_' + name, rejection_test(mutate))

if __name__ == '__main__':
    unittest.main()
