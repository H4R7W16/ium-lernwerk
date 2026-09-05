import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import validate_v2_reuse_audit as audit

ROOT = Path(__file__).resolve().parents[1]


class ReuseAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in (*audit.REVIEW_INPUTS, audit.STATUS):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        self.inventory = json.loads((self.root / audit.INVENTORY).read_text(encoding='utf-8'))
        self.followups = json.loads((self.root / audit.FOLLOWUPS).read_text(encoding='utf-8'))
        self.status = json.loads((self.root / audit.STATUS).read_text(encoding='utf-8'))
        self.lxp = json.loads((self.root / audit.LESSONS).read_text(encoding='utf-8'))
        self.git_mock = patch.object(audit, 'read_git_text', side_effect=self.git_text)
        self.git_mock.start()
        self.addCleanup(self.git_mock.stop)

    def git_text(self, root, commit, path):
        # Unit fixtures use the unchanged V1 files. Real repository integration is
        # exercised below with the actual Git reader, not this stand-in.
        if commit != audit.V1_COMMIT:
            return self.real_git(root=ROOT, commit=commit, path=path)
        return (ROOT / path).read_text(encoding='utf-8')

    real_git = staticmethod(audit.read_git_text)

    def check(self):
        return audit.validate_inventory(self.inventory, self.followups, self.root)

    def test_real_inventory_and_git_objects_pass(self):
        self.git_mock.stop()
        self.assertEqual([], audit.validate_repository(ROOT))

    def test_missing_contracts_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual([f'{p} fehlt' for p in audit.FILES], audit.validate_repository(Path(directory)))

    def test_missing_duplicate_and_extra_artifact_fail(self):
        original=copy.deepcopy(self.inventory['records'])
        for records in (original[:-1], original+[original[0]], original+[dict(original[0],artifactId='LXP05')]):
            self.inventory['records']=records
            self.assertTrue(self.check())

    def test_unknown_decision_and_blank_rationale_fail(self):
        for key,value in [('decision','approved'),('rationale',' '),('scope','')]:
            original=copy.deepcopy(self.inventory['records'][0])
            self.inventory['records'][0][key]=value
            self.assertTrue(self.check(),key)
            self.inventory['records'][0]=original

    def test_adapt_and_replace_require_registered_successors(self):
        for record in self.inventory['records']:
            if record['decision'] in ('adapt','replace'):
                original=record['successorTaskId']
                for bad in (None,'unregistered-task'):
                    record['successorTaskId']=bad
                    self.assertTrue(self.check(),record['artifactId'])
                record['successorTaskId']=original

    def test_task_status_cannot_replace_actual_artifact(self):
        self.inventory['records'][0]['artifactRef']['kind']='vault'
        self.inventory['records'][0]['artifactRef']['target']='IUM00 done'
        self.assertTrue(self.check())

    def test_wrong_artifact_family_path_and_missing_supporting_file_fail(self):
        self.inventory['records'][0]['artifactRef']['target']='LICENSE'
        self.assertTrue(self.check())
        self.inventory['records'][0]['artifactRef']['target']=audit.ARTIFACTS['IUM00'][0]
        self.inventory['records'][0]['supplementaryRefs'].pop()
        self.assertTrue(self.check())

    def test_unknown_requirement_and_absent_foundation_evidence_fail(self):
        self.inventory['records'][0]['requirementIds']=['V2-REQ-NONEXISTENT']
        self.assertTrue(self.check())
        self.inventory['records'][0]['evidence']=[]
        self.assertTrue(self.check())

    def test_false_locator_and_stale_legacy_digest_fail(self):
        record=self.inventory['records'][0]
        record['inspection']['locator']='Nicht vorhandene Fundstelle'
        self.assertTrue(self.check())
        self.inventory['legacyDigests'][record['artifactRef']['target']]='0'*64
        self.assertTrue(self.check())

    def test_no_automatic_activation_and_no_other_baseline(self):
        self.inventory['activation']='approved'
        self.assertTrue(self.check())
        self.inventory['baselineCommit']=audit.LXP05_COMMIT
        self.assertTrue(self.check())

    def test_prior_lxf01_lxp_decisions_are_preserved(self):
        for record in self.inventory['records']:
            if record['artifactId'].startswith('LXP'):
                original=record['decision']
                record['decision']='retain'
                self.assertTrue(self.check(),record['artifactId'])
                record['decision']=original

    def test_followups_require_real_scope_and_no_production_authorization(self):
        task=next(t for t in self.followups['tasks'] if t['id']=='IUM-V2-FU-TECH')
        for key,value in [('objective',''),('acceptanceCriteria',[]),('state','completed-foundation'),('execution','authorized')]:
            original=copy.deepcopy(task[key]);task[key]=value
            self.assertTrue(audit.validate_followups(self.followups,self.inventory))
            task[key]=original

    def test_followup_cycles_or_orphan_links_fail(self):
        self.followups['tasks'][0]['dependsOn']=[self.followups['tasks'][0]['id']]
        self.assertTrue(audit.validate_followups(self.followups,self.inventory))
        self.followups['tasks'][0]['artifactIds']=[]
        self.assertTrue(audit.validate_followups(self.followups,self.inventory))

    def test_lxp05_cannot_be_integrated_or_given_reuse_decision(self):
        for key,value in [('integration','merged'),('reuseAuthorized',True),('decision','retain')]:
            data=copy.deepcopy(self.lxp);data[key]=value
            self.assertTrue(audit.validate_lxp05(data,self.followups,self.root))

    def test_lxp05_lesson_needs_actual_candidate_evidence(self):
        self.lxp['inspectedFiles'][0]['sha256']='0'*64
        self.assertTrue(audit.validate_lxp05(self.lxp,self.followups,self.root))

    def test_future_gates_and_carry_forward_cannot_be_promoted(self):
        for key in ('userAcceptance','contentProduction','curriculumCoverage','pilot','release','nextTask'):
            data=copy.deepcopy(self.status);data[key]='approved'
            self.assertTrue(audit.validate_status(data,self.root),key)
        self.status['carryForward'].pop()
        self.assertTrue(audit.validate_status(self.status,self.root))

    def test_review_binds_every_input_and_rejects_changed_report(self):
        (self.root/audit.REPORT).write_text('Changed review',encoding='utf-8')
        self.assertTrue(audit.validate_status(self.status,self.root))
        self.status['inputDigests'].pop(audit.REPORT)
        self.assertTrue(audit.validate_status(self.status,self.root))

    def test_governance_approval_is_commit_bound(self):
        data=json.loads((self.root/audit.ACCEPTANCE).read_text(encoding='utf-8'))
        data['acceptedCommit']=audit.V1_COMMIT
        self.assertTrue(audit.validate_acceptance(data))

    def test_malformed_records_fail_without_crash(self):
        original=copy.deepcopy(self.inventory)
        for key in original:
            for value in (None,{},[],True,4):
                self.inventory=copy.deepcopy(original);self.inventory[key]=value
                with self.subTest(key=key,value=value): self.assertTrue(self.check())
        for key in original['records'][0]:
            self.inventory=copy.deepcopy(original)
            self.inventory['records'][0][key]={'bad':[]}
            with self.subTest(field=key): self.assertTrue(self.check())

    def test_unknown_fields_and_traversal_refs_fail(self):
        self.inventory['records'][0]['evidence'][0]['target']='../outside.md'
        self.assertTrue(self.check())
        self.inventory['records'][0]['approved']=True
        self.assertTrue(self.check())


if __name__=='__main__': unittest.main()
