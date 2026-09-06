import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import validate_v2_grade6 as grade

ROOT = Path(__file__).resolve().parents[1]


class Grade6Tests(unittest.TestCase):
    def setUp(self):
        self.roadmap = json.loads((ROOT / grade.ROADMAP).read_text(encoding='utf-8'))
        self.matrix = json.loads((ROOT / grade.MATRIX).read_text(encoding='utf-8'))
        self.status = json.loads((ROOT / grade.STATUS).read_text(encoding='utf-8'))

    def check(self):
        return grade.validate_planning(self.roadmap, self.matrix, ROOT)

    def row(self, disposition):
        return next(r for r in self.matrix['records'] if r['disposition'] == disposition)

    def test_real_repository(self):
        self.assertEqual([], grade.validate_repository(ROOT))

    def test_missing_contracts(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual([f'{p} fehlt' for p in grade.FILES], grade.validate_repository(Path(temp)))

    def test_complete_source_set(self):
        self.assertEqual(85, len(self.matrix['records']))
        self.matrix['records'].pop()
        self.assertTrue(self.check())

    def test_no_bmb_promotion(self):
        self.matrix['records'][0]['sourceBinding'] = 'official'
        self.assertTrue(self.check())

    def test_context_cannot_become_competency(self):
        self.row('context-only')['coverage'] = 'covered'
        self.assertTrue(self.check())

    def test_handoff_cannot_be_deferred_again(self):
        self.row('introduced-in-grade-6')['disposition'] = 'handoff-grade-7'
        self.assertTrue(self.check())

    def test_handoff_requires_core_evidence(self):
        self.row('introduced-in-grade-6')['moduleIds'] = ['V2-G6-F01']
        self.assertTrue(self.check())

    def test_spiral_requires_explicit_progression(self):
        self.row('revisit-and-extend')['progression'] = ''
        self.assertTrue(self.check())

    def test_prior_assignment_must_match_approved_r5(self):
        self.row('revisit-and-extend')['r5ModuleIds'] = []
        self.assertTrue(self.check())

    def test_privacy_cannot_be_met_by_case(self):
        self.row('open-privacy')['plannedEvidence'] = 'Fiktiver Fall genügt.'
        self.assertTrue(self.check())

    def test_entry_knowledge_is_not_observed(self):
        self.roadmap['entryKnowledge']['status'] = 'mastered'
        self.assertTrue(self.check())

    def test_all_six_entry_domains_required(self):
        self.roadmap['entryKnowledge']['checks'].pop()
        self.assertTrue(self.check())

    def test_entry_cannot_claim_execution(self):
        self.roadmap['entryKnowledge']['checks'][0]['state'] = 'passed'
        self.assertTrue(self.check())

    def test_entry_budget_not_double_counted(self):
        self.roadmap['variants'][1]['entryCheckMinutes'] = 0
        self.assertTrue(self.check())

    def test_broad_gaps_require_replanning(self):
        self.roadmap['entryKnowledge']['broadGapAction'] = 'continue-without-adjustment'
        self.assertTrue(self.check())

    def test_module_time_and_year_total(self):
        self.roadmap['modules'][0]['timeComponents']['guidedPractice'] += 5
        self.assertTrue(self.check())

    def test_year_time_and_bridging(self):
        self.roadmap['variants'][1]['bridgingMinutes'] += 45
        self.assertTrue(self.check())

    def test_flex_cannot_carry_exclusive_requirement(self):
        self.roadmap['flexModules'][0]['newRequiredCoverage'] = True
        self.assertTrue(self.check())

    def test_cycle_and_unknown_principle(self):
        original = copy.deepcopy(self.roadmap)
        self.roadmap['modules'][0]['dependsOn'] = ['V2-G6-M07']
        self.assertTrue(self.check())
        self.roadmap = original
        self.roadmap['modules'][0]['principleIds'] = ['invented']
        self.assertTrue(self.check())

    def test_spaced_practice_requires_earlier_module(self):
        self.roadmap['retrievalSchedule'][0]['revisitModule'] = 'V2-G6-M07'
        self.assertTrue(self.check())

    def test_project_reference_must_resolve(self):
        self.roadmap['projectRequirements'][0]['location'] = 'missing-section'
        self.assertTrue(self.check())

    def test_gates_must_remain_open(self):
        self.roadmap['entryGates'][0]['state'] = 'passed'
        self.assertTrue(self.check())

    def test_r7_requires_separate_approval(self):
        self.status['nextTaskCondition'] = 'automatic'
        self.assertTrue(grade.validate_status(self.status, ROOT))

    def test_all_private_records_carry_forward(self):
        self.status['privateRecordCarry'].pop()
        self.assertTrue(grade.validate_status(self.status, ROOT))

    def test_snapshot_digest_cannot_be_stale(self):
        self.status['inputDigests'][grade.ROADMAP] = '0' * 64
        self.assertTrue(grade.validate_status(self.status, ROOT))

    def test_acceptance_binds_approved_commit(self):
        data = json.loads((ROOT / grade.ACCEPTANCE).read_text(encoding='utf-8'))
        data['acceptedCommit'] = '0' * 40
        self.assertTrue(grade.validate_acceptance(data))

    def test_malformed_collections_and_boolean_minutes(self):
        original = copy.deepcopy(self.roadmap)
        for field, value in [('dependsOn', [False]), ('principleIds', {}), ('minutes', True)]:
            with self.subTest(field=field):
                self.roadmap = copy.deepcopy(original)
                self.roadmap['modules'][0][field] = value
                self.assertTrue(self.check())


if __name__ == '__main__':
    unittest.main()
