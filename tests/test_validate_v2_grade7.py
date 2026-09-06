import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import validate_v2_grade7 as grade

ROOT=Path(__file__).resolve().parents[1]


class Grade7Tests(unittest.TestCase):
    def setUp(self):
        self.roadmap=json.loads((ROOT/grade.ROADMAP).read_text(encoding='utf-8'))
        self.matrix=json.loads((ROOT/grade.MATRIX).read_text(encoding='utf-8'))
        self.progression=json.loads((ROOT/grade.PROGRESSION).read_text(encoding='utf-8'))
        self.status=json.loads((ROOT/grade.STATUS).read_text(encoding='utf-8'))

    def check(self): return grade.validate_planning(self.roadmap,self.matrix,self.progression,ROOT)

    def row(self,disposition):return next(r for r in self.matrix['records'] if r['disposition']==disposition)

    def test_repository(self):self.assertEqual([],grade.validate_repository(ROOT))

    def test_missing_contracts(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual([f'{p} fehlt' for p in grade.FILES],grade.validate_repository(Path(temp)))

    def test_full_134_source_records(self):
        self.assertEqual(134,len(self.matrix['records']))
        self.matrix['records'].pop(0)
        self.assertTrue(self.check())

    def test_official_binding_cannot_be_reduced(self):
        self.matrix['records'][0]['sourceBinding']='orientation'
        self.assertTrue(self.check())

    def test_official_competency_not_context(self):
        self.matrix['records'][0]['disposition']='context-only'
        self.assertTrue(self.check())

    def test_context_does_not_count(self):
        self.row('context-only')['coverage']='covered'
        self.assertTrue(self.check())

    def test_official_requirements_stay_in_core(self):
        self.row('planned-core')['moduleIds']=['V2-G7-M06']
        self.assertTrue(self.check())

    def test_reflection_not_closed_by_fiction(self):
        self.row('open-reflection')['plannedEvidence']='Fremder Fall genügt als eigener Nutzungsnachweis.'
        self.assertTrue(self.check())

    def test_planned_evidence_required(self):
        self.row('planned-core')['plannedEvidence']=''
        self.assertTrue(self.check())

    def test_flex_cannot_substitute_requirement(self):
        self.row('planned-extension')['moduleIds']=['V2-G7-F01']
        self.assertTrue(self.check())

    def test_progression_must_include_all_r6_modules(self):
        self.progression['strands'].pop()
        self.assertTrue(self.check())

    def test_r5_reference_resolves(self):
        self.progression['strands'][0]['r5ModuleIds']=['unknown']
        self.assertTrue(self.check())

    def test_r6_product_matches_approved_plan(self):
        self.progression['strands'][0]['r6PlannedProduct']='V2 wurde erfolgreich absolviert.'
        self.assertTrue(self.check())

    def test_progression_reference_must_reach_mapped_module(self):
        self.row('planned-core')['progressionStrandIds']=['R7-PROG-02']
        self.assertTrue(self.check())

    def test_no_observed_knowledge_from_plan(self):
        self.progression['entryKnowledge']='mastered'
        self.assertTrue(self.check())

    def test_entry_check_must_not_claim_execution(self):
        self.progression['strands'][0]['entryCheck']['state']='passed'
        self.assertTrue(self.check())

    def test_weak_entry_requires_replanning(self):
        self.progression['broadGapAction']='continue'
        self.assertTrue(self.check())

    def test_module_phase_sum(self):
        self.roadmap['modules'][0]['timeComponents']['guidedPractice']+=5
        self.assertTrue(self.check())

    def test_time_double_counting(self):
        self.roadmap['paths'][0]['requiredMinutes']-=45
        self.assertTrue(self.check())

    def test_entry_minutes_accounted(self):
        self.roadmap['paths'][0]['entryCheckMinutes']=0
        self.assertTrue(self.check())

    def test_capacity_cannot_hide_deficit(self):
        self.roadmap['capacityChecks'][0]['deficitMinutes']=0
        self.assertTrue(self.check())

    def test_mathematical_fit_not_actual_availability(self):
        self.roadmap['capacityChecks'][1]['localAvailability']='available'
        self.assertTrue(self.check())

    def test_old_model_not_new_permission(self):
        self.roadmap['historicalTimeAudit'][0]['v2Availability']='available'
        self.assertTrue(self.check())

    def test_omitted_orientation_must_remain_visible(self):
        self.roadmap['paths'][0]['openCapacityRecordIds']=[]
        self.assertTrue(self.check())

    def test_all_open_reflections_in_each_path(self):
        self.roadmap['paths'][2]['openReflectionRecordIds'].pop()
        self.assertTrue(self.check())

    def test_integration_no_artificial_discount(self):
        self.roadmap['integrations'][0]['timeCreditMinutes']=45
        self.assertTrue(self.check())

    def test_cycle_rejected(self):
        self.roadmap['modules'][0]['dependsOn']=['V2-G7-M07']
        self.assertTrue(self.check())

    def test_unknown_principle(self):
        self.roadmap['modules'][0]['principleIds']=['unknown']
        self.assertTrue(self.check())

    def test_project_location_resolves(self):
        self.roadmap['projectRequirements'][0]['location']='unknown'
        self.assertTrue(self.check())

    def test_gates_stay_open(self):
        self.roadmap['entryGates'][0]['state']='passed'
        self.assertTrue(self.check())

    def test_dash_not_automatically_approved(self):
        self.status['nextTaskCondition']='automatic'
        self.assertTrue(grade.validate_status(self.status,ROOT))

    def test_previous_private_questions_preserved(self):
        self.status['privateRecordCarry'].pop()
        self.assertTrue(grade.validate_status(self.status,ROOT))

    def test_digest_staleness(self):
        self.status['inputDigests'][grade.PROGRESSION]='0'*64
        self.assertTrue(grade.validate_status(self.status,ROOT))

    def test_acceptance_binds_commit(self):
        d=json.loads((ROOT/grade.ACCEPTANCE).read_text(encoding='utf-8'))
        d['acceptedCommit']='0'*40
        self.assertTrue(grade.validate_acceptance(d))

    def test_malformed_types(self):
        initial=copy.deepcopy(self.roadmap)
        for field,value in [('dependsOn',[{}]),('minutes',True),('principleIds',False)]:
            with self.subTest(field=field):
                self.roadmap=copy.deepcopy(initial)
                self.roadmap['modules'][0][field]=value
                self.assertTrue(self.check())


if __name__=='__main__':unittest.main()
