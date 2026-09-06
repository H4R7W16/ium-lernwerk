import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import validate_v2_grade5 as grade

ROOT = Path(__file__).resolve().parents[1]


class Grade5Tests(unittest.TestCase):
    def setUp(self):
        self.roadmap = json.loads((ROOT / grade.ROADMAP).read_text(encoding='utf-8'))
        self.matrix = json.loads((ROOT / grade.MATRIX).read_text(encoding='utf-8'))
        self.status = json.loads((ROOT / grade.STATUS).read_text(encoding='utf-8'))

    def check(self):
        return grade.validate_planning(self.roadmap, self.matrix, ROOT)

    def test_real_repository_passes(self):
        self.assertEqual([], grade.validate_repository(ROOT))

    def test_missing_contracts_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual([f'{p} fehlt' for p in grade.FILES], grade.validate_repository(Path(temp)))

    def test_missing_duplicate_and_unknown_records_fail(self):
        rows = self.matrix['records']
        for value in (rows[:-1], rows + [rows[0]], rows + [dict(rows[0], recordId='invented')]):
            self.matrix['records'] = value
            self.assertTrue(self.check())

    def test_source_binding_type_grades_and_parent_are_preserved(self):
        row = self.matrix['records'][0]
        for key, value in [('sourceBinding', 'orientation'), ('recordType', 'example'), ('sourceGrades', [7]), ('parentRecordId', 'invented'), ('sourcePath', '../outside')]:
            old = row[key]; row[key] = value
            self.assertTrue(self.check(), key); row[key] = old

    def test_examples_and_operators_cannot_be_required_coverage(self):
        row = next(r for r in self.matrix['records'] if not r['isRequirement'])
        row.update(isRequirement=True, disposition='planned-in-grade-5', coverage='covered', moduleIds=['V2-G5-M01'])
        self.assertTrue(self.check())

    def test_private_records_cannot_be_closed_with_fictional_evidence(self):
        for row in self.matrix['records']:
            if row['recordId'] in grade.PRIVATE_RECORDS:
                old = copy.deepcopy(row)
                row.update(disposition='planned-in-grade-5', plannedEvidence='Fiktiven Fall beurteilen', moduleIds=['V2-G5-M05'], fulfillmentMode='direct-module', successorTaskId=None)
                self.assertTrue(self.check(), row['recordId']); row.clear(); row.update(old)

    def test_official_competency_cannot_be_postponed_to_grade6(self):
        row = self.matrix['records'][0]
        row.update(disposition='handoff-grade-6', moduleIds=[], fulfillmentMode=None, plannedEvidence=None, successorTaskId='IUM-V2-R6')
        self.assertTrue(self.check())

    def test_grade6_handoffs_require_reason_and_successor(self):
        row = next(r for r in self.matrix['records'] if r['disposition']=='handoff-grade-6')
        row.update(rationale='', successorTaskId=None)
        self.assertTrue(self.check())

    def test_planned_evidence_requires_core_module_and_text(self):
        row = self.matrix['records'][0]
        for key, value in [('plannedEvidence',''),('moduleIds',['V2-G5-F01']),('moduleIds',[]),('coverage','covered'),('fulfillmentMode','done')]:
            old=row[key];row[key]=value;self.assertTrue(self.check(),key);row[key]=old

    def test_tool_matrix_has_multiple_contexts_and_no_extra_time(self):
        self.roadmap['toolMatrixAdditionalMinutes']=45
        self.assertTrue(self.check())
        self.roadmap['toolMatrixAdditionalMinutes']=0
        self.roadmap['toolEvidenceMatrix']=self.roadmap['toolEvidenceMatrix'][:1]
        self.assertTrue(self.check())

    def test_core_order_and_dependencies_reject_cycles_and_v1(self):
        self.roadmap['modules'][0]['dependsOn']=['V2-G5-M06']
        self.assertTrue(self.check())
        self.roadmap['modules'][0]['dependsOn']=[]
        self.roadmap['coreOrder'][0]='IUM-5-CORE-01'
        self.assertTrue(self.check())

    def test_module_times_include_feedback_practice_and_consolidation(self):
        row=self.roadmap['modules'][0]
        row['timeComponents']['feedbackAndRevision']=0
        row['timeComponents']['independentApplication']+=30
        self.assertTrue(self.check())

    def test_time_variants_reject_double_counting_and_missing_buffer(self):
        for key,value in [('totalMinutes',1800),('availableUnits',True),('coreMinutes',1200),('bufferMinutes',0),('flexIds',['unknown'])]:
            row=self.roadmap['variants'][0];old=row[key];row[key]=value
            self.assertTrue(self.check(),key);row[key]=old

    def test_flex_cannot_be_required_or_precede_its_prerequisites(self):
        self.roadmap['flexModules'][0]['newRequiredCoverage']=True
        self.assertTrue(self.check())

    def test_retrieval_has_valid_earlier_reference_and_budget(self):
        self.roadmap['retrievalSchedule'][0]['revisitModule']='V2-G5-M06'
        self.assertTrue(self.check())

    def test_project_requirements_and_design_principles_must_resolve(self):
        self.roadmap['projectRequirements'][0]['requirementId']='UNKNOWN'
        self.roadmap['modules'][0]['principleIds']=['unregistered']
        self.assertTrue(self.check())

    def test_project_evidence_location_must_resolve(self):
        self.roadmap['projectRequirements'][0]['location']='nonexistent-section'
        self.assertTrue(self.check())

    def test_audit_decisions_and_entry_gates_cannot_be_promoted(self):
        self.roadmap['auditApplications'][0]['decision']='retain'
        self.roadmap['entryGates'][0]['state']='passed'
        self.assertTrue(self.check())

    def test_malformed_roots_nested_objects_and_types_do_not_crash(self):
        for value in (None,[],True,'bad'):
            self.assertTrue(grade.validate_planning(value,self.matrix,ROOT))
        for key,value in [('modules',None),('variants',[None]),('toolMatrixAdditionalMinutes',False),('entryGates',{}),('projectRequirements',[3])]:
            old=self.roadmap[key];self.roadmap[key]=value
            self.assertTrue(self.check(),key);self.roadmap[key]=old

    def test_status_preserves_pending_review_and_questions(self):
        for key,value in [('userAcceptance','approved'),('nextTask','IUM-V2-CUT'),('carryForward',[]),('contentProduction','open')]:
            old=self.status[key];self.status[key]=value
            self.assertTrue(grade.validate_status(self.status,ROOT),key);self.status[key]=old

    def test_stale_review_and_unapproved_audit_fail(self):
        self.status['inputDigests'][grade.ROADMAP]='0'*64
        self.assertTrue(grade.validate_status(self.status,ROOT))
        receipt=json.loads((ROOT/grade.ACCEPTANCE).read_text(encoding='utf-8'))
        receipt['acceptedCommit']='9f52cdc6f5e36b72b7a3fd9e64501ccfc4af2135'
        self.assertTrue(grade.validate_acceptance(receipt))


if __name__ == '__main__':
    unittest.main()
