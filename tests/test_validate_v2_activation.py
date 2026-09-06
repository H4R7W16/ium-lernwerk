import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_v2_activation import validate, resolve_decision, ActivationError


class ActivationTests(unittest.TestCase):
    def setUp(self):
        self.decision = json.loads((ROOT / 'roadmap/v2/cutover/decision.json').read_text(encoding='utf8'))
        self.pointer = json.loads((ROOT / 'roadmap/v2/cutover/active-baseline.json').read_text(encoding='utf8'))

    def test_actual_activation_preserves_product_and_limits(self):
        status = validate(ROOT)
        self.assertEqual(status['activeBaseline'], 'v2')
        self.assertEqual(status['productBaseline'], 'v1')
        self.assertEqual(status['contentProduction'], 'frozen')
        self.assertEqual(status['cutover']['state'], 'approved')

    def test_defer_and_revise_keep_v1(self):
        for selection in ['defer', 'revise']:
            self.decision['selection'] = selection
            self.assertEqual(resolve_decision(self.decision)['activeBaseline'], 'v1')

    def test_missing_decision_fails(self):
        with self.assertRaises(ActivationError):
            resolve_decision(None)


MUTATIONS = {
    'wrong_commit': lambda d,p: d.__setitem__('acceptedCommit', 'a'*40),
    'unapproved': lambda d,p: d.__setitem__('state', 'pending'),
    'non_user_decision': lambda d,p: d.__setitem__('decisionBy', 'assistant'),
    'unknown_selection': lambda d,p: d.__setitem__('selection', 'automatic'),
    'deferred_pointer': lambda d,p: d.__setitem__('selection', 'defer'),
    'lost_condition': lambda d,p: d['acceptedConditions'].pop(),
    'opened_production': lambda d,p: d['limits'].__setitem__('contentProduction', 'open'),
    'opened_publication': lambda d,p: d['limits'].__setitem__('publication', 'open'),
    'opened_pilot': lambda d,p: d['limits'].__setitem__('pilot', 'approved'),
    'bad_decision_digest': lambda d,p: p.__setitem__('decisionSha256', '0'*64),
    'bad_review_digest': lambda d,p: d.__setitem__('reviewSha256', '0'*64),
    'changed_product': lambda d,p: p.__setitem__('productBaseline', 'v2'),
    'unknown_scope': lambda d,p: p.__setitem__('scope', 'production'),
    'unsafe_path': lambda d,p: p.__setitem__('decisionPath', '../secret.json'),
    'input_drift': lambda d,p: p['inputDigests'].__setitem__('packages/project-status/index.mjs','0'*64),
    'missing_input': lambda d,p: p['inputDigests'].pop('roadmap/v2/status.json'),
    'resealed_foundation': lambda d,p: p['inputDigests'].__setitem__('roadmap/v2/status.json','0'*64),
    'unknown_pointer_field': lambda d,p: p.__setitem__('autoRelease', True),
}


def reject(mutate):
    def test(self):
        mutate(self.decision, self.pointer)
        with self.assertRaises(ActivationError):
            validate(ROOT, decision=self.decision, pointer=self.pointer)
    return test


for name, mutate in MUTATIONS.items():
    setattr(ActivationTests, 'test_reject_' + name, reject(mutate))

if __name__ == '__main__':
    unittest.main()
