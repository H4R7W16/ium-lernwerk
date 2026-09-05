"""Validate the 25-family reuse audit without activating any V2 product work."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

if __package__:
    from .validate_v2_governance import fields, nonempty, read_input, string_set
else:
    from validate_v2_governance import fields, nonempty, read_input, string_set

BASE = 'roadmap/v2/audits/'
LXF = 'roadmap/v2/foundations/learning-experience/'
GOV = 'roadmap/v2/foundations/governance/'
INVENTORY = BASE+'artifact-inventory.json'
FOLLOWUPS = BASE+'follow-up-tasks.json'
LESSONS = BASE+'lxp05-lessons.json'
STATUS = BASE+'status.json'
REPORT = BASE+'validation-report.md'
ACCEPTANCE = GOV+'acceptance.json'
SCHEMA = 'schemas/v2/artifact-reuse.schema.json'
FILES = (INVENTORY, FOLLOWUPS, LESSONS, STATUS, REPORT, BASE+'README.md', ACCEPTANCE, SCHEMA)
V1_COMMIT = 'dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0'
LXP05_COMMIT = '645a1d4ea3c786b08e1320954b522edf86dc9f83'
BASE_COMMIT = '9f52cdc6f5e36b72b7a3fd9e64501ccfc4af2135'

# The artifact identity catalogue is fixed independently of editable decisions.
ARTIFACTS = {'IUM00': ('docs/research/phase-0/research-protocol.md',
           'docs/research/phase-0/data-contract.md',
           'docs/research/phase-0/source-register.json'),
 'IUM01': ('docs/research/phase-0/curated/01-informatikdidaktik.md', 'docs/research/phase-0/claim-ledger.json'),
 'IUM02': ('docs/research/phase-0/curated/02-medienbildung.md', 'docs/research/phase-0/claim-ledger.json'),
 'IUM03': ('docs/research/phase-0/curated/03-lernpsychologie-unterricht.md',
           'docs/research/phase-0/claim-ledger.json'),
 'IUM04': ('docs/research/phase-0/curated/04-digitale-lernumgebungen-oer.md',
           'docs/research/phase-0/claim-ledger.json'),
 'IUM05': ('curriculum/extraction-protocol.md',
           'curriculum/lesehilfe-2026-27/competencies.json',
           'curriculum/basiskurs-medienbildung/competencies.json',
           'curriculum/aufbaukurs-informatik/competencies.json',
           'curriculum/source-status.md'),
 'IUM06': ('docs/research/phase-0/synthesis.md',
           'docs/research/phase-0/design-principles.json',
           'docs/fachprofil/ium-gymnasium-5-7.md',
           'curriculum/crosswalk.json',
           'curriculum/operators.json',
           'curriculum/progression.md'),
 'IUM07': ('roadmap/module-candidates.json', 'roadmap/coverage-plan.json', 'roadmap/module-roadmap.md'),
 'IUM08': ('docs/research/phase-0/README.md', 'docs/research/phase-0/synthesis.md'),
 'IUM09': ('roadmap/coverage-remediation.json',
           'roadmap/coverage-plan.json',
           'docs/superpowers/specs/2026-07-29-ium09-curriculare-partial-nacharbeit-design.md'),
 'IUM10': ('roadmap/time-model.json',
           'docs/superpowers/specs/2026-07-30-ium10-zeitmodell-modulroadmap-design.md',
           'docs/superpowers/specs/2026-07-31-ium10-privacy-vertrag-design.md'),
 'IUM11': ('pilot/pilot-protocol.json', 'pilot/docs/publication-contract.json', 'scripts/validate_ium11.py'),
 'IUM12': ('docs/superpowers/specs/2026-08-03-ium-phase1-plattformfundament-design.md',
           'docs/superpowers/plans/2026-08-03-ium-phase1-plattformfundament-implementation.md'),
 'IUM13': ('docs/platform/implementation-report.md',
           'docs/platform/README.md',
           'packages/module-runtime/src/runtime.ts',
           'packages/local-state/src/indexeddb-repository.ts',
           'packages/export-import/src/import-state.ts'),
 'IUM14': ('docs/platform/device-verification.md',
           'docs/platform/device-verification-runs/2026-08-03-managed-ipad-primary.md'),
 'IUM15': ('docs/superpowers/specs/2026-08-03-ium-phase2-entwicklungs-und-einsatzgate-design.md',),
 'IUM16': ('docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md',
           'modules/IUM-5-CORE-05/curriculum-mapping.json'),
 'IUM17': ('docs/superpowers/plans/2026-08-03-ium-5-core-05-implementation.md',),
 'IUM18': ('packages/ium-5-core-05/src/interpreter.ts',
           'modules/IUM-5-CORE-05/module.yaml',
           'modules/IUM-5-CORE-05/lernumgebung/content.json',
           'modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md',
           'docs/reviews/ium-5-core-05-fach-didaktik.md'),
 'IUM19': ('docs/superpowers/specs/2026-08-03-ium5-gate-b-pilot-design.md',
           'docs/superpowers/plans/2026-08-03-ium5-gate-b-pilot-implementation.md'),
 'IUM20': ('pilot/ium5-gate-b/protocol.json',
           'pilot/ium5-gate-b/schemas/technical-evidence.schema.json',
           'pilot/ium5-gate-b/schemas/pilot-evidence.schema.json',
           'scripts/validate_ium5_gate_b.py'),
 'LXP01': ('docs/superpowers/specs/2026-08-04-ium-learning-experience-production-design.md',),
 'LXP02': ('docs/superpowers/specs/2026-08-04-ium-learning-experience-product-architecture.md',),
 'LXP03': ('docs/superpowers/specs/2026-08-05-ium-learning-experience-reference-designs.md',),
 'LXP04': ('docs/superpowers/specs/2026-08-05-ium-learning-experience-design-system.md',)}

V2_INPUTS = {
    'roadmap/v2/status.json', 'roadmap/v2/archive/v1-baseline.json', 'roadmap/v2/requirements/requirements.json',
    'roadmap/v2/foundations/curriculum/status.json', 'roadmap/v2/foundations/curriculum/source-basis.json',
    'roadmap/v2/foundations/curriculum/gap-assessments.json', 'roadmap/v2/foundations/sources/status.json',
    'roadmap/v2/foundations/sources/source-register.json', LXF+'legacy-audit.json', LXF+'status.json',
    LXF+'evidence-register.json', LXF+'learner-profile.json', LXF+'learning-architecture.json',
    LXF+'material-patterns.json', LXF+'teacher-orchestration.md', LXF+'experience-gates.json',
    GOV+'status.json', GOV+'governance-contract.json',
    'docs/superpowers/specs/2026-09-03-ium-v2-controlled-rebaseline-design.md',
}
LEGACY_PATHS = {p for paths in ARTIFACTS.values() for p in paths}
REVIEW_INPUTS = LEGACY_PATHS | V2_INPUTS | (set(FILES)-{STATUS})
DECISIONS = {'retain','adapt','replace','reference-only','drop'}
LXP_DECISIONS = {'LXP01':('adapt','LXF02'), 'LXP02':('adapt','LXF04'),
                 'LXP03':('reference-only',None), 'LXP04':('replace','LXF05')}
TASK_STATES = {**dict.fromkeys(('IUM-V2-SRC','IUM-V2-GOV','LXF02','LXF03','LXF04','LXF05'),'completed-foundation'),
               **dict.fromkeys(('IUM-V2-R5','IUM-V2-R6','IUM-V2-R7'),'planned-rebaseline'),
               **dict.fromkeys(('IUM-V2-FU-TECH','IUM-V2-FU-MOD','IUM-V2-FU-PILOT'),'blocked-follow-up')}
TASK_DEPENDENCIES = {'IUM-V2-R5':['IUM-V2-AUD'],'IUM-V2-R6':['IUM-V2-R5'],'IUM-V2-R7':['IUM-V2-R6'],
    'IUM-V2-FU-TECH':['IUM-V2-CUT'],'IUM-V2-FU-MOD':['IUM-V2-CUT'],
    'IUM-V2-FU-PILOT':['IUM-V2-FU-MOD','IUM-V2-FU-TECH']}
LXP_PATHS = {'docs/quality/ium-learning-experience-implementation-report.md',
    'modules/IUM-5-CORE-05/lernumgebung/experience.json',
    'apps/lernwerk-portal/src/components/AlgorithmWorkbench.astro',
    'packages/learning-experience/src/components/EvidenceCardComposer.astro'}
LESSON_IDS = {'LXP05-EVIDENCE','LXP05-COMPOSITION','LXP05-PRODUCT','LXP05-ORCHESTRATION'}
GOV_QUESTIONS = {'GOV-Q-OPERATOR','GOV-Q-SCHOOL','GOV-Q-REVIEWERS','CUR-Q-002','GOV-Q-RIGHTS'}


def strings(value, allow_empty=False):
    return value == [] if allow_empty and value == [] else string_set(value)


def rows(value, id_key, expected, keys, label, errors):
    if not isinstance(value,list):
        errors.append(f'AUD {label}: Liste erforderlich')
        return []
    valid=[]
    for item in value:
        if fields(item,keys,label,errors) and nonempty(item.get(id_key)):
            valid.append(item)
        else:
            errors.append(f'AUD {label}: ungültiger Eintrag')
    ids=[r[id_key] for r in valid]
    if set(ids)!=set(expected) or len(ids)!=len(set(ids)):
        errors.append(f'AUD {label}: Pflicht-IDs fehlen, sind doppelt oder unbekannt')
    return [r for r in valid if r[id_key] in expected]


def header(data, keys, label, errors):
    if not fields(data,keys,label,errors): return False
    if type(data.get('schemaVersion')) is not int or data['schemaVersion']!=1 or data.get('projectId')!='ium-lernwerk' or data.get('asOf')!='2026-09-06':
        errors.append(f'AUD {label}: Identität oder Stichtag ungültig')
    return True


def load(root,path):
    return json.loads(read_input(root,path))


def read_git_text(root, commit, path):
    if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):
        raise ValueError('vollständige Commit-SHA erforderlich')
    if (not nonempty(path) or '\\' in path or ':' in path
            or PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts):
        raise ValueError('ungültiger Git-Artefaktpfad')
    result=subprocess.run(['git','show',f'{commit}:{path}'],cwd=root,stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,timeout=30,check=True)
    return result.stdout.decode('utf-8').replace('\r\n','\n')


def ref(value, root, errors, allowed=None):
    if not fields(value,('kind','target','label','required'),'Beleg',errors): return None
    if value['kind']!='repo' or value['required'] is not True or not nonempty(value['label']) or not nonempty(value['target']):
        errors.append('AUD Beleg benötigt einen konkreten Repositorypfad')
        return None
    path=value['target']
    if allowed is not None and path not in allowed:
        errors.append(f'AUD nicht zulässiger Beleg: {path}')
        return None
    try: read_input(root,path)
    except (OSError,UnicodeError,ValueError):
        errors.append(f'AUD Beleg fehlt oder verlässt das Repository: {path}')
        return None
    return path


def task_ids(data):
    if not isinstance(data,dict) or not isinstance(data.get('tasks'),list): return set()
    return {r['id'] for r in data['tasks'] if isinstance(r,dict) and nonempty(r.get('id'))}


def validate_inventory(data, followups, root):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','baselineCommit','workStatus','activation','records','legacyDigests'),'Inventar',errors): return errors
    if data['baselineCommit']!=V1_COMMIT or data['workStatus']!='review' or data['activation']!='not-authorized':
        errors.append('AUD darf weder Baseline noch Produktionsfreigabe verändern')
    try:
        reqs={r['id'] for r in load(root,'roadmap/v2/requirements/requirements.json')['requirements']}
    except (OSError,UnicodeError,ValueError,KeyError,TypeError):
        errors.append('AUD Anforderungsregister unlesbar');reqs=set()
    known_tasks=task_ids(followups)
    records=rows(data['records'],'artifactId',ARTIFACTS,('artifactId','title','family','artifactRef','supplementaryRefs',
        'decision','scope','rationale','requirementIds','evidence','successorTaskId','additionalSuccessorTaskIds','inspection'),'Artefakte',errors)
    git_contents={}
    digests=data['legacyDigests']
    if not isinstance(digests,dict) or set(digests)!=LEGACY_PATHS:
        errors.append('AUD V1-Dateimanifest unvollständig oder verändert')
    else:
        for path in sorted(LEGACY_PATHS):
            try:
                text=read_git_text(root,V1_COMMIT,path)
                git_contents[path]=text
                if digests[path]!=hashlib.sha256(text.encode('utf-8')).hexdigest():
                    errors.append(f'AUD V1-Hash stimmt nicht: {path}')
            except (OSError,UnicodeError,ValueError,subprocess.SubprocessError):
                errors.append(f'AUD V1-Gitbeleg unlesbar: {path}')
    for record in records:
        aid=record['artifactId'];paths=ARTIFACTS[aid]
        if not all(nonempty(record[k]) for k in ('title','scope','rationale')) or record['family'] not in ('research','curriculum-planning','experience','platform-module-pilot'):
            errors.append(f'AUD {aid}: Prüfgegenstand oder Begründung fehlt')
        primary=ref(record['artifactRef'],root,errors,{paths[0]})
        supplementary=record['supplementaryRefs']
        if not isinstance(supplementary,list):
            errors.append(f'AUD {aid}: ergänzende Artefakte ungültig')
        else:
            targets=[ref(p,root,errors,set(paths[1:])) for p in supplementary]
            if None in targets or len(targets)!=len(set(targets)) or set(targets)!=set(paths[1:]):
                errors.append(f'AUD {aid}: ergänzende Artefakte fehlen oder sind doppelt')
        decision=record['decision']
        if not isinstance(decision,str) or decision not in DECISIONS:
            errors.append(f'AUD {aid}: unbekannte Übernahmeentscheidung')
        successor=record['successorTaskId']
        if successor is not None and (not nonempty(successor) or successor not in known_tasks):
            errors.append(f'AUD {aid}: unbekannter Nachfolger')
        if decision in ('adapt','replace') and not nonempty(successor):
            errors.append(f'AUD {aid}: adapt/replace benötigt konkreten Nachfolgetask')
        additional=record['additionalSuccessorTaskIds']
        if not strings(additional,True) or any(t not in known_tasks or t==successor for t in additional):
            errors.append(f'AUD {aid}: zusätzliche Nachfolgetasks ungültig')
        if aid in LXP_DECISIONS and (decision,successor)!=LXP_DECISIONS[aid]:
            errors.append(f'AUD {aid}: widerspricht dem freigegebenen LXF01-Audit')
        if not string_set(record['requirementIds']) or not set(record['requirementIds'])<=reqs:
            errors.append(f'AUD {aid}: unbekannter oder fehlender V2-Anforderungsbezug')
        evidence=record['evidence']
        if not isinstance(evidence,list) or not evidence:
            errors.append(f'AUD {aid}: V2-Grundlagenbelege fehlen')
        else:
            refs=[ref(p,root,errors,V2_INPUTS) for p in evidence]
            if len(refs)!=len(set(refs)): errors.append(f'AUD {aid}: doppelte Grundlagenbelege')
        inspection=record['inspection']
        if fields(inspection,('locator','observation','limitation'),'Artefaktprüfung',errors):
            if not all(nonempty(v) for v in inspection.values()):
                errors.append(f'AUD {aid}: tatsächlicher Prüfbefund fehlt')
            elif primary is None or inspection['locator'] not in git_contents.get(primary,''):
                errors.append(f'AUD {aid}: Prüffundstelle nicht im V1-Artefakt')
    return errors


def validate_followups(data, inventory):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','tasks'),'Nachfolgetasks',errors): return errors
    records=inventory.get('records',[]) if isinstance(inventory,dict) else []
    records=records if isinstance(records,list) else []
    tasks=rows(data['tasks'],'id',TASK_STATES,('id','title','state','vaultNote','objective','artifactIds','dependsOn','acceptanceCriteria','execution'),'Nachfolgetasks',errors)
    graph={}
    for task in tasks:
        tid=task['id'];expected_state=TASK_STATES[tid]
        if not all(nonempty(task[k]) for k in ('title','vaultNote','objective')) or not string_set(task['acceptanceCriteria']):
            errors.append(f'AUD {tid}: Nachfolgeauftrag nicht konkret')
        execution='already-completed-foundation' if expected_state=='completed-foundation' else 'requires-separate-user-order'
        if task['state']!=expected_state or task['execution']!=execution:
            errors.append(f'AUD {tid}: keine vorgezogene Ausführung oder Statushochsetzung')
        related={r['artifactId'] for r in records if isinstance(r,dict) and nonempty(r.get('artifactId')) and
            (r.get('successorTaskId')==tid or isinstance(r.get('additionalSuccessorTaskIds'),list) and tid in r['additionalSuccessorTaskIds'])}
        if not string_set(task['artifactIds']) or set(task['artifactIds'])!=related:
            errors.append(f'AUD {tid}: Artefaktzuordnung fehlt oder widerspricht Inventar')
        deps=task['dependsOn']
        if deps!=TASK_DEPENDENCIES.get(tid,[]) or not strings(deps,True):
            errors.append(f'AUD {tid}: Gateabhängigkeiten ungültig')
        if strings(deps,True): graph[tid]=deps
    visited=set();active=set()
    def visit(tid):
        if tid in active: errors.append(f'AUD zyklische Nachfolgeabhängigkeit: {tid}');return
        if tid in visited: return
        active.add(tid)
        for nxt in graph.get(tid,[]): visit(nxt)
        active.remove(tid);visited.add(tid)
    for tid in graph: visit(tid)
    return errors


def validate_lxp05(data, followups, root):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','candidateCommit','state','integration','disposition','reuseAuthorized','inspectedFiles','lessons'),'LXP05',errors): return errors
    if data['candidateCommit']!=LXP05_COMMIT or data['state']!='frozen' or data['integration']!='unmerged' or data['disposition']!='historical-only' or data['reuseAuthorized'] is not False:
        errors.append('AUD LXP05 bleibt ausschließlich eingefrorener Erfahrungsbestand')
    files=rows(data['inspectedFiles'],'path',LXP_PATHS,('path','sha256','locator','observation'),'LXP05-Belege',errors)
    for entry in files:
        try:
            text=read_git_text(root,LXP05_COMMIT,entry['path'])
            if not nonempty(entry['locator']) or entry['locator'] not in text or not nonempty(entry['observation']) or entry['sha256']!=hashlib.sha256(text.encode('utf-8')).hexdigest():
                errors.append(f"AUD LXP05: ungültiger konkreter Beleg {entry['path']}")
        except (OSError,UnicodeError,ValueError,subprocess.SubprocessError):
            errors.append(f"AUD LXP05-Gitbeleg fehlt: {entry['path']}")
    known=task_ids(followups)
    lessons=rows(data['lessons'],'id',LESSON_IDS,('id','finding','responsePaths','successorTaskIds'),'LXP05-Lehren',errors)
    for lesson in lessons:
        if not nonempty(lesson['finding']) or not string_set(lesson['successorTaskIds']) or not set(lesson['successorTaskIds'])<=known:
            errors.append('AUD LXP05-Erfahrung ohne Folgeauftrag')
        if not string_set(lesson['responsePaths']) or not set(lesson['responsePaths'])<=V2_INPUTS:
            errors.append('AUD LXP05-Erfahrung ohne V2-Antwort')
        else:
            for path in lesson['responsePaths']:
                try: read_input(root,path)
                except (OSError,UnicodeError,ValueError): errors.append(f'AUD fehlende V2-Antwort: {path}')
    return errors


def validate_acceptance(data):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',gate='IUM-V2-GOV',state='approved-by-user',date='2026-09-06',
        acceptedCommit=BASE_COMMIT,decisionBy='user',nextTask='IUM-V2-AUD',contentProduction='frozen',publication='closed',pilot='not-started')
    if not fields(data,(*expected,'evidence','acceptedOpenQuestionIds'),'GOV-Abnahme',errors): return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()):
        errors.append('AUD GOV-Freigabe muss den ausdrücklich angenommenen Commit und Scope belegen')
    evidence=data['evidence']
    if fields(evidence,('kind','target','label','required'),'GOV-Freigabebeleg',errors):
        if evidence['kind']!='vault' or evidence['target']!='2026-09-03 - IUM-V2-GOV Governance und öffentliche Wahrnehmung konsolidieren' or evidence['required'] is not True or not nonempty(evidence['label']):
            errors.append('AUD GOV-Freigabebeleg ungültig')
    if not string_set(data['acceptedOpenQuestionIds']) or set(data['acceptedOpenQuestionIds'])!=GOV_QUESTIONS:
        errors.append('AUD GOV-Folgefragen dürfen durch Freigabe nicht verschwinden')
    return errors


def validate_status(data, root):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',workStatus='review',
        reviewType='ai-assisted-document-self-review',reviewer='Codex',userAcceptance='pending',baseCommit=BASE_COMMIT,
        governanceAcceptance=ACCEPTANCE,nextTask='IUM-V2-R5',nextTaskCondition='explicit-aud-user-approval',
        contentProduction='frozen',curriculumCoverage='unassessed',pilot='not-started',release='closed',lxp05='frozen-unmerged')
    if not fields(data,(*expected,'carryForward','inputDigests'),'Auditstatus',errors): return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()):
        errors.append('AUD Status darf Folgegates nicht öffnen oder Prüfarten vermischen')
    question_sources={}
    try:
        for path,questions in ((GOV+'governance-contract.json',load(root,GOV+'governance-contract.json')['openQuestions']),
                               (LXF+'status.json',load(root,LXF+'status.json')['review']['openQuestions'])):
            for q in questions: question_sources.setdefault(q['id'],set()).add(path)
    except (OSError,UnicodeError,ValueError,KeyError,TypeError):
        errors.append('AUD offene Grundlagenfragen nicht auflösbar')
    carry=rows(data['carryForward'],'id',question_sources,('id','sourcePaths','disposition'),'Fragenübergabe',errors)
    for entry in carry:
        if entry['disposition']!='preserved-at-source' or not string_set(entry['sourcePaths']) or set(entry['sourcePaths'])!=question_sources[entry['id']]:
            errors.append(f"AUD Frage verändert oder nicht weitergegeben: {entry['id']}")
    digests=data['inputDigests']
    if not isinstance(digests,dict) or set(digests)!=REVIEW_INPUTS:
        errors.append('AUD Review-Dateimenge unvollständig oder verändert')
        return errors
    for path in sorted(REVIEW_INPUTS):
        try:
            actual=hashlib.sha256(read_input(root,path).encode('utf-8')).hexdigest()
            if digests[path]!=actual: errors.append(f'AUD Review veraltet: {path}')
        except (OSError,UnicodeError,ValueError): errors.append(f'AUD Prüfeingang fehlt: {path}')
    return errors


def validate_repository(root):
    errors=[f'{p} fehlt' for p in FILES if not (root/p).is_file()]
    payloads={}
    for path in (INVENTORY,FOLLOWUPS,LESSONS,STATUS,ACCEPTANCE):
        if not (root/path).is_file(): continue
        try: payloads[path]=load(root,path)
        except (OSError,UnicodeError,ValueError): errors.append(f'AUD ungültiges JSON: {path}')
    if INVENTORY in payloads: errors.extend(validate_inventory(payloads[INVENTORY],payloads.get(FOLLOWUPS,{}),root))
    if FOLLOWUPS in payloads: errors.extend(validate_followups(payloads[FOLLOWUPS],payloads.get(INVENTORY,{})))
    if LESSONS in payloads: errors.extend(validate_lxp05(payloads[LESSONS],payloads.get(FOLLOWUPS,{}),root))
    if STATUS in payloads: errors.extend(validate_status(payloads[STATUS],root))
    if ACCEPTANCE in payloads: errors.extend(validate_acceptance(payloads[ACCEPTANCE]))
    return errors
