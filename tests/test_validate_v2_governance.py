"""Negative release tests: document evidence cannot promote public product claims."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import validate_v2_governance as gov

ROOT = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in (*gov.REVIEW_INPUTS, gov.BASE + 'status.json'):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / relative).read_bytes())
        self.contract = json.loads((self.root / gov.CONTRACT).read_text(encoding='utf-8'))
        self.status = json.loads((self.root / (gov.BASE + 'status.json')).read_text(encoding='utf-8'))

    def check_contract(self):
        return gov.validate_contract(self.contract, self.root)

    def test_real_contract_passes(self):
        self.assertEqual([], self.check_contract())
        self.assertEqual([], gov.validate_repository(ROOT))

    def test_missing_contracts_fail_closed(self):
        with tempfile.TemporaryDirectory() as path:
            errors = gov.validate_repository(Path(path))
        self.assertEqual([f'{p} fehlt' for p in gov.FILES], errors)

    def test_each_weaker_evidence_type_rejected(self):
        for claim in self.contract['claims']:
            with self.subTest(claim=claim['id']):
                saved = claim['minimumEvidence']
                claim['minimumEvidence'] = 'document-review'
                self.assertTrue(self.check_contract())
                claim['minimumEvidence'] = saved

    def test_each_public_claim_is_blocked_even_with_otherwise_valid_contract(self):
        for claim in self.contract['claims']:
            with self.subTest(claim=claim['id']):
                claim['publicUseAllowed'] = True
                self.assertTrue(self.check_contract())
                claim['publicUseAllowed'] = False

    def test_unobserved_usage_pilot_and_effect_cannot_be_promoted(self):
        for claim in self.contract['claims']:
            if claim['id'] in ('usage', 'pilot', 'effect'):
                claim['assessment'] = 'foundation-only'
                self.assertTrue(self.check_contract())
                claim['assessment'] = 'not-established'

    def test_no_boundary_can_be_relaxed(self):
        for key, saved in list(self.contract['boundaries'].items()):
            self.contract['boundaries'][key] = True if saved is False else 'approved'
            with self.subTest(boundary=key):
                self.assertTrue(self.check_contract())
            self.contract['boundaries'][key] = saved

    def test_operator_is_not_invented_from_project_owner(self):
        role = next(r for r in self.contract['roles'] if r['id'] == 'operator')
        role['assignedTo'] = 'Jan'
        self.assertTrue(self.check_contract())

    def test_duplicate_or_missing_claim_role_question_and_recheck_rejected(self):
        for key in ('claims', 'roles', 'openQuestions', 'rechecks'):
            original = copy.deepcopy(self.contract[key])
            self.contract[key][-1] = copy.deepcopy(self.contract[key][0])
            self.assertTrue(self.check_contract(), key)
            self.contract[key] = original[:-1]
            self.assertTrue(self.check_contract(), key)
            self.contract[key] = original

    def test_unknown_review_role_rejected(self):
        self.contract['claims'][0]['reviewerRole'] = 'author'
        self.assertTrue(self.check_contract())

    def test_claim_label_cannot_disguise_different_assertion(self):
        self.contract['claims'][0]['label'] = 'garantiert lernwirksam'
        self.assertTrue(self.check_contract())

    def test_missing_or_irrelevant_evidence_rejected(self):
        for refs in ([], ['LICENSE'], ['../outside.md'], ['C:/private.txt'], ['roadmap/missing.json']):
            self.contract['claims'][0]['evidencePaths'] = refs
            self.assertTrue(self.check_contract(), refs)

    def test_forbidden_claim_list_cannot_be_shortened(self):
        self.contract['forbiddenClaims'].pop()
        self.assertTrue(self.check_contract())

    def test_malformed_nested_values_fail_without_crash(self):
        original = copy.deepcopy(self.contract)
        for key in original:
            for value in (None, [], {}, True, 7):
                self.contract = copy.deepcopy(original)
                self.contract[key] = value
                with self.subTest(key=key, value=value):
                    self.assertTrue(self.check_contract())
        for key in ('claims', 'roles', 'openQuestions', 'rechecks', 'sources'):
            for field in original[key][0]:
                self.contract = copy.deepcopy(original)
                self.contract[key][0][field] = {'unexpected': []}
                self.assertTrue(self.check_contract(), (key, field))

    def test_unknown_fields_rejected(self):
        self.contract['claims'][0]['approval'] = True
        self.assertTrue(self.check_contract())

    def test_open_question_cannot_be_closed_or_lose_gate(self):
        for key, value in [('status', 'closed'), ('owner', ''), ('trigger', ''), ('blocks', [])]:
            original = copy.deepcopy(self.contract['openQuestions'])
            self.contract['openQuestions'][0][key] = value
            self.assertTrue(self.check_contract(), key)
            self.contract['openQuestions'] = original

    def test_stale_input_and_missing_digest_rejected(self):
        path = self.root / gov.CONTRACT
        path.write_text(path.read_text(encoding='utf-8') + '\n', encoding='utf-8')
        self.assertTrue(gov.validate_status(self.status, self.root))
        self.status['inputDigests'].pop(gov.CONTRACT)
        self.assertTrue(gov.validate_status(self.status, self.root))

    def test_line_ending_conversion_preserves_review(self):
        path = self.root / gov.CONTRACT
        text = path.read_text(encoding='utf-8')
        path.write_bytes(text.replace('\n', '\r\n').encode('utf-8'))
        self.assertEqual([], gov.validate_status(self.status, self.root))

    def test_status_cannot_grant_user_acceptance_or_release(self):
        for key in ('userAcceptance', 'release', 'pilot', 'contentProduction', 'reviewType', 'nextGate'):
            data = copy.deepcopy(self.status)
            data[key] = 'approved'
            self.assertTrue(gov.validate_status(data, self.root), key)

    def test_false_lxf07_acceptance_revision_rejected(self):
        self.status['lxf07Acceptance']['commit'] = '1' * 40
        self.assertTrue(gov.validate_status(self.status, self.root))

    def test_invalid_json_and_empty_document_report_errors(self):
        (self.root / gov.CONTRACT).write_text('{', encoding='utf-8')
        (self.root / (gov.BASE + 'README.md')).write_text('', encoding='utf-8')
        self.assertTrue(gov.validate_repository(self.root))

    def test_lxf07_input_scope_does_not_expand(self):
        from scripts import validate_v2_rebaseline as v2
        self.assertEqual(35, len(v2.LXF_RELEASE_INPUTS))
        self.assertFalse(any('/governance/' in p for p in v2.LXF_RELEASE_INPUTS))


if __name__ == '__main__':
    unittest.main()
