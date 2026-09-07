"""Read-only verification of the planning packet, not of future implementation."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
PACKET = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def safe_path(value):
    p = PurePosixPath(value)
    require(isinstance(value, str) and value and not p.is_absolute()
            and '\\' not in value and ':' not in value
            and not any(x in {'', '.', '..'} for x in value.split('/')),
            'Unsafe path: ' + str(value))
    return value


def validate(vault=None):
    plan = load(PACKET / 'plan.json')
    bound = load(PACKET / 'input-bindings.json')
    base = plan['baseCommit']
    require(re.fullmatch('[a-f0-9]{40}', base), 'Full baseline commit required')
    require(git('rev-parse', base).decode().strip() == base, 'Missing baseline commit')
    git('merge-base', '--is-ancestor', base, 'HEAD')
    require(bound['acceptedInputCommit'] == base, 'Input commit mismatch')
    for item in bound['inputs']:
        path = safe_path(item['path'])
        expected = item['sha256LfNormalized']
        require(sha(git('show', base + ':' + path)) == expected, 'Historical binding: ' + path)
        require(sha((ROOT/path).read_bytes()) == expected, 'Current input drift: ' + path)
    for item in bound['planningDocuments']:
        require(sha((ROOT/safe_path(item['path'])).read_bytes()) == item['sha256LfNormalized'],
                'Plan document drift: ' + item['path'])

    require(plan['state'] == 'review' and plan['scope'] == 'implementation-planning-only'
            and plan['implementationAuthorized'] is False and plan['currentPackage'] is None
            and plan['parallelExecution'] is False, 'Planning scope changed')
    for field, expected in {'contentProduction':'frozen','curriculum':'unassessed',
                             'pilot':'not-started','publication':'closed'}.items():
        require(plan[field] == expected, 'Premature maturity: ' + field)
    acceptance = load(ROOT/'roadmap/v2/follow-ups/pilot/acceptance.json')
    require(acceptance['acceptedCommit'] == base and acceptance['state'] == 'approved-by-user'
            and acceptance['taskId'] == 'IUM-V2-FU-PILOT'
            and acceptance['scope'] == 'pilot-instrument-specification'
            and acceptance['implementationAuthorized'] is False
            and acceptance['realPilotGate'] == 'open', 'PILOT acceptance scope')
    require(not (ROOT/'roadmap/v2/implementation/authorization.json').exists(),
            'This planning packet has no implementation authorization')

    packages = plan['packages']
    require([p['id'] for p in packages] == ['IMP%02d'%i for i in range(1,9)], 'Package series')
    baseline_paths = set(git('ls-tree','-r','--name-only',base).decode().splitlines())
    available = set(baseline_paths)
    created = set()
    touched = set()
    for index,p in enumerate(packages):
        require(p['taskId'] == 'IUM-V2-'+p['id'] and p['status'] == 'blocked', 'Task identity/state')
        expected_dep = 'IUM-V2-PLAN' if index == 0 else packages[index-1]['taskId']
        require(p['dependsOn'] == [expected_dep], 'Sequence/dependency mismatch')
        require(p['plan'] in {d['path'] for d in bound['planningDocuments']}, 'Unknown subplan')
        doc=(ROOT/p['plan']).read_text(encoding='utf-8')
        require('## '+p['id']+' – ' in doc, 'Missing package section')
        require(len(p['criteria']) >= 3, 'Missing completion criteria')
        modifications=p['modify']+list(p.get('optionalModify',{}))
        require(len(set(modifications)) == len(modifications), 'Duplicate modify path')
        for path in modifications:
            safe_path(path)
            require(path in available, 'Modification has no preceding file: '+path)
            touched.add(path)
        for path in p['create']:
            safe_path(path)
            require(path not in available, 'Create path already exists: '+path)
            require(not (ROOT/path).exists(), 'Future implementation already present: '+path)
            created.add(path)
            available.add(path)
            touched.add(path)
    require(set(plan['sharedStatusFiles']) <= created, 'Shared status files have no creator')

    links=0
    for item in bound['planningDocuments']:
        path=ROOT/item['path']
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)',path.read_text(encoding='utf-8')):
            target=unquote(target.split('#',1)[0].strip('<>'))
            if not target or '://' in target:
                continue
            require((path.parent/target).resolve().is_file(), 'Broken plan link: '+target)
            links+=1

    allowed = {d['path'] for d in bound['planningDocuments']}
    allowed.add('roadmap/v2/follow-ups/pilot/acceptance.json')
    allowed.update('roadmap/v2/implementation-planning/'+x for x in
                   ['plan.json','input-bindings.json','verify-plan.py','validation-report.md','validation.json'])
    changed=git('diff','--name-only',base).decode().splitlines()
    untracked=git('ls-files','--others','--exclude-standard').decode().splitlines()
    require(set(changed+untracked) <= allowed, 'Changes exceed planning scope: '+str(set(changed+untracked)-allowed))
    require(not git('diff','--name-only',base,'--',*sorted(baseline_paths)).strip(),
            'Existing baseline files modified during planning')

    vault_result='not-requested'
    if vault is not None:
        board=(vault/'60_Organisation/Workspace-Entwicklung/Workspace Kanban.md').read_text(encoding='utf-8-sig')
        blocked=board.split('## Blockiert\n',1)[1].split('\n## ',1)[0]
        previous='2026-09-07 - IUM-V2-PLAN Referenzmodul-Implementierung planen'
        for index,p in enumerate(packages):
            path=vault/safe_path(p['taskPath'])
            task=path.read_text(encoding='utf-8-sig')
            front=task.split('---',2)[1]
            for line in ['owner_agent: Codex','status: blocked','parallelizable: false',f'sequence: {index+23}']:
                require(line in front.splitlines(), 'Task property '+line+': '+p['taskId'])
            require('[['+previous+']]' in front, 'Vault dependency '+p['taskId'])
            require('[['+path.stem+']]' in blocked, 'Task missing in blocked board: '+p['taskId'])
            previous=path.stem
        planning=(vault/'60_Organisation/Workspace-Entwicklung/Tasks/2026-09-07 - IUM-V2-PLAN Referenzmodul-Implementierung planen.md').read_text(encoding='utf-8-sig')
        pilot=(vault/'60_Organisation/Workspace-Entwicklung/Tasks/2026-09-06 - IUM-V2-FU-PILOT Prüf- und Pilotinstrumente an V2 binden.md').read_text(encoding='utf-8-sig')
        require('status: review' in planning.split('---',2)[1], 'Plan not in review')
        require('status: done' in pilot.split('---',2)[1], 'PILOT acceptance missing')
        vault_result='passed'
    return dict(state='passed', scope='planning-packet-only', groups=6,
                boundInputs=len(bound['inputs']), boundPlans=len(bound['planningDocuments']),
                sequentialPackages=len(packages), plannedUniqueFiles=len(touched),
                plannedNewFiles=len(created), localPlanLinks=links, vault=vault_result,
                implementationTestsRun=False, independentReview=False)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault',type=Path)
    args=parser.parse_args()
    try:
        print(json.dumps(validate(args.vault),ensure_ascii=False,indent=2))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit('Plan verification failed: '+str(error))
