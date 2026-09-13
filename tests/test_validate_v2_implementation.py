"""Breaks caught: scope escapes, forged completion, lost historical evidence."""
import copy
from contextlib import contextmanager
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
if importlib.util.find_spec('validate_v2_implementation'):
    import validate_v2_implementation as impl
else:
    impl=None


class PathTests(unittest.TestCase):
    def test_only_exact_safe_paths_are_authorized(self):
        self.assertIsNotNone(impl, 'Implementation contract is not available')
        plan=dict(schemaVersion=1,packageId='IMP01',files=['package.json'],dependsOn=[])
        self.assertEqual(impl.validate_change_plan(plan,allowed_files={'package.json'}),plan)
        for bad in ['../secret','/tmp/file','C:/file','a\\b','a//b','a/./b','package.json\nsecret',
                    'roadmap/v2/cutover/active-baseline.json',None,42]:
            with self.subTest(path=bad),self.assertRaises(impl.ImplementationError):
                impl.validate_change_plan(dict(plan,files=[bad]),allowed_files={'package.json'})

    def test_unknown_fields_and_duplicate_paths_fail(self):
        self.assertIsNotNone(impl)
        plan=dict(schemaVersion=1,packageId='IMP01',files=['package.json'],dependsOn=[])
        for changed in [dict(plan,autoApprove=True),dict(plan,files=['package.json']*2),
                        dict(plan,schemaVersion=True),dict(plan,dependsOn='IMP00')]:
            with self.subTest(changed=changed),self.assertRaises(impl.ImplementationError):
                impl.validate_change_plan(changed,allowed_files={'package.json'})


class ImplementationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if impl is None:
            return
        cls.temp=tempfile.TemporaryDirectory(prefix='ium-implementation-tests-')
        cls.repo=Path(cls.temp.name)/'repo'
        subprocess.run(['git','clone','--quiet','--shared',str(ROOT),str(cls.repo)],check=True,capture_output=True)
        plan=json.loads((ROOT/'roadmap/v2/implementation/change-plan.json').read_text(encoding='utf-8'))
        for package in plan['packages']:
            for name in package['files']:
                source=ROOT/name
                if source.is_file():
                    target=cls.repo/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        # Exercise the current user-requested documentation alongside package scope.
        for name in ['README.md',
                     'docs/planning/ium-5-7/README.md',
                     'docs/planning/ium-5-7/lebenswelt-und-progression.md',
                     'docs/planning/ium-5-7/externe-angebote-und-comthink.md']:
            target=cls.repo/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,target)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls,'temp'):cls.temp.cleanup()

    def setUp(self):
        self.assertIsNotNone(impl, 'Implementation contract is not available')

    @contextmanager
    def changed(self,path,mutate):
        file=self.repo/path;original=file.read_bytes()
        try:
            data=json.loads(original);mutate(data)
            file.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
            yield
        finally:file.write_bytes(original)

    def test_actual_historical_activation_and_current_scope_are_separate(self):
        result=impl.validate(self.repo)
        self.assertEqual(result['historicalActivation']['productBaseline'],'v1')
        self.assertEqual(result['development']['authorizedPackages'],
                         ['IMP%02d'%number for number in range(1,9)])
        self.assertEqual(result['development']['limits']['pilot'],'not-started')
        self.assertEqual([x['taskId'] for x in result['followUps']],
                         ['IUM-V2-FU-TECH','IUM-V2-FU-MOD','IUM-V2-FU-PILOT'])
        self.assertTrue(all(x['state']=='approved-by-user' for x in result['followUps']))
        self.assertEqual(result['development']['vaultEvidence'],'not-checked')

    def test_historical_validator_rejects_tampered_materialized_input(self):
        with impl.historical_view(self.repo) as view:
            file=view/'roadmap/v2/status.json'
            data=json.loads(file.read_text());data['contentProduction']='open'
            file.write_text(json.dumps(data),encoding='utf-8')
            with self.assertRaises(impl.ImplementationError):
                impl.validate_historical_view(self.repo,view)

    def test_forged_or_unbound_authorization_is_rejected(self):
        auth=json.loads((self.repo/impl.AUTHORIZATION).read_text(encoding='utf-8'))
        changes=[lambda a:a.__setitem__('acceptedPlanCommit','a702dea'),
                 lambda a:a.__setitem__('acceptedPlanCommit','f'*40),
                 lambda a:a['planAcceptance'].__setitem__('decisionBy','assistant'),
                 lambda a:a['requests'][0].__setitem__('packageIds',['IMP09']),
                 lambda a:a['requests'][0].__setitem__('statement',''),
                 lambda a:a['limits'].__setitem__('pilot','passed')]
        for mutate in changes:
            changed=copy.deepcopy(auth);mutate(changed)
            with self.subTest(changed=changed),self.assertRaises(impl.ImplementationError):
                impl.validate(self.repo,authorization=changed)

    def test_unrequested_package_and_removed_foundation_fail(self):
        file=self.repo/'README.md';original=file.read_bytes()
        try:
            file.write_bytes(original+b'\n// unauthorized runtime repair\n')
            with self.assertRaisesRegex(impl.ImplementationError,'[Uu]nautorisiert|[Nn]icht autorisiert'):
                impl.validate(self.repo)
        finally:file.write_bytes(original)
        file=self.repo/'roadmap/v2/status.json';original=file.read_bytes()
        try:
            file.unlink()
            with self.assertRaises(impl.ImplementationError):impl.validate(self.repo)
        finally:file.write_bytes(original)

    def test_new_untracked_path_cannot_bypass_scope(self):
        file=self.repo/'unauthorized.txt'
        try:
            file.write_text('synthetic',encoding='utf-8')
            with self.assertRaisesRegex(impl.ImplementationError,'[Uu]nautorisiert|[Nn]icht autorisiert'):
                impl.validate(self.repo)
        finally:file.unlink(missing_ok=True)

    def test_planning_supplement_does_not_allow_other_documents(self):
        file=self.repo/'docs/planning/ium-5-7/unrequested.md'
        try:
            file.write_text('synthetic out-of-scope document',encoding='utf-8')
            with self.assertRaisesRegex(impl.ImplementationError,'Nicht autorisierte neue Datei: docs/planning/ium-5-7/unrequested.md'):
                impl.validate(self.repo)
        finally:file.unlink(missing_ok=True)

    def test_plan_and_fu_acceptances_cannot_be_rewritten(self):
        for path in ['roadmap/v2/implementation-planning/plan.json','roadmap/v2/follow-ups/pilot/acceptance.json']:
            with self.subTest(path=path),self.changed(path,lambda d:d.__setitem__('autoPilot',True)):
                with self.assertRaises(impl.ImplementationError):impl.validate(self.repo)

    def test_allowlist_cannot_be_widened_or_optional_scope_assumed(self):
        with self.changed(impl.CHANGE_PLAN,lambda d:d['packages'][0]['files'].append('package-lock.json')):
            with self.assertRaises(impl.ImplementationError):impl.validate(self.repo)
        with self.changed(impl.AUTHORIZATION,lambda d:d['requests'][0].__setitem__('optionalChanges',[])):
            with self.assertRaises(impl.ImplementationError):impl.validate(self.repo)

    def test_progress_cannot_claim_done_pilot_or_unrequested_work(self):
        mutations=[lambda d:d['packages'][7].__setitem__('state','done'),
                   lambda d:d['packages'][7].__setitem__('acceptance',dict(state='approved-by-user')),
                   lambda d:d['limits'].__setitem__('curriculum','passed'),
                   lambda d:d['packages'][0].__setitem__('checks',[{'exitCode':0}]),
                   lambda d:d['packages'][7].__setitem__('candidateCommit','f'*40)]
        for mutate in mutations:
            with self.subTest(mutation=mutate),self.changed(impl.PROGRESS,mutate):
                with self.assertRaises(impl.ImplementationError):impl.validate(self.repo)

    def test_review_evidence_becomes_invalid_when_authorized_code_changes(self):
        package=json.loads((self.repo/impl.CHANGE_PLAN).read_text(encoding='utf-8'))['packages'][7]
        measured=impl.package_digest(self.repo,package)
        def record_review(data):
            data['packages'][7].update(state='review',candidateCommit=None,checks=[dict(
                id='synthetic-check',command='synthetic-test-only',exitCode=0,scope='synthetic-contract',
                baseCommit='a702deaaafba464e2035f5be6d919bd30a9f4855',treeDigest=measured,summary='Synthetic fixture, not real execution evidence')])
        with self.changed(impl.PROGRESS,record_review):
            self.assertEqual(impl.validate(self.repo)['development']['packages'][7]['technicalState'],'passed')
            file=self.repo/'scripts/verify-v2-m06.ts';original=file.read_bytes()
            try:
                file.write_bytes(original+b'\n// synthetic change after recorded review\n')
                with self.assertRaisesRegex(impl.ImplementationError,'Prüfungen|verändert'):
                    impl.validate(self.repo)
            finally:file.write_bytes(original)


if __name__=='__main__':unittest.main()
