"""Grade 6 planning: an approved predecessor plan is not observed prior knowledge."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

if __package__:
    from .validate_v2_governance import fields, nonempty, read_input, string_set
else:
    from validate_v2_governance import fields, nonempty, read_input, string_set

BASE = 'roadmap/v2/grades/grade-6/'
PREV = 'roadmap/v2/grades/grade-5/'
ROADMAP = BASE+'roadmap.json'
MATRIX = BASE+'curriculum-map.json'
STATUS = BASE+'status.json'
ACCEPTANCE = PREV+'acceptance.json'
SCHEMA = 'schemas/v2/grade-6.schema.json'
FILES = (ROADMAP, MATRIX, STATUS, ACCEPTANCE, SCHEMA, BASE+'README.md', BASE+'validation-report.md')
BASE_COMMIT = '5146310ae855636d3529e8d31b079b5ca265da6e'
SOURCE = 'curriculum/lesehilfe-2026-27/competencies.json'
LXF = 'roadmap/v2/foundations/learning-experience/'
INPUTS = {SOURCE, 'curriculum/basiskurs-medienbildung/competencies.json',
    'roadmap/v2/status.json','roadmap/v2/requirements/requirements.json',
    'roadmap/v2/foundations/curriculum/source-basis.json','roadmap/v2/foundations/curriculum/gap-assessments.json',
    LXF+'learner-profile.json',LXF+'learning-architecture.json',LXF+'evidence-register.json',LXF+'material-patterns.json',
    LXF+'teacher-orchestration.md',LXF+'experience-gates.json',LXF+'status.json',
    'roadmap/v2/foundations/governance/governance-contract.json','roadmap/v2/foundations/governance/status.json',
    'roadmap/v2/audits/artifact-inventory.json','roadmap/v2/audits/follow-up-tasks.json','roadmap/v2/audits/status.json',
    PREV+'roadmap.json',PREV+'curriculum-map.json',PREV+'status.json',PREV+'validation-report.md',PREV+'README.md',
} | (set(FILES)-{STATUS})
CORE = [f'V2-G6-M{i:02}' for i in range(1,8)]
FLEX = {'V2-G6-F01','V2-G6-F02'}
GATES = {'R6-ENTRY','R6-ACCESS','R6-BUDGET','R6-PRIVACY','R6-PILOT','R6-R7-TRANSITION'}
COMPONENTS = {'orientationAndExplanation','guidedPractice','independentApplication','feedbackAndRevision','consolidationAndTransfer'}
PRIVATE = {'BMB16-GYM-PK-RK-001','BMB16-GYM-IK-MG-001','LH26-E-DP-002','LH26-E-DP-003','LH26-E-DP-009','LH26-E-KS-011'}


def load(root, path): return json.loads(read_input(root, path))
def positive(v): return type(v) is int and v > 0
def natural(v): return type(v) is int and v >= 0
def names(v, empty=False): return (empty and v == []) or string_set(v)


def table(value, key, expected, keys, errors, label):
    if not isinstance(value, list):
        errors.append(f'R6 {label}: Liste erforderlich'); return []
    valid=[]
    for row in value:
        if fields(row, keys, label, errors) and nonempty(row.get(key)): valid.append(row)
        else: errors.append(f'R6 {label}: ungültiger Eintrag')
    ids=[r[key] for r in valid]
    if set(ids)!=set(expected) or len(ids)!=len(set(ids)): errors.append(f'R6 {label}: Pflicht-IDs fehlen, sind doppelt oder unbekannt')
    return [r for r in valid if r[key] in expected]


def header(data, keys, errors, label):
    if not fields(data, keys, label, errors): return False
    for k,v in dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',grade=6).items():
        if data[k]!=v or type(data[k]) is not type(v): errors.append(f'R6 {label}: Identität oder Jahrgang ungültig')
    return True


def validate_matrix(data, root):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','grade','coverageMeaning','records'),errors,'Curriculummatrix'): return errors
    source={r['id']:r for r in load(root,SOURCE)['records'] if 6 in r['grades']}
    prior={r['recordId']:r for r in load(root,PREV+'curriculum-map.json')['records']}
    rows=table(data['records'],'recordId',source,('recordId','sourceId','sourcePath','sourceBinding','sourceGrades','recordType','isRequirement','parentRecordId','coverage','r5Disposition','r5ModuleIds','disposition','fulfillmentMode','moduleIds','plannedEvidence','progression','rationale','successorTaskId'),errors,'Curriculumrecords')
    if not nonempty(data['coverageMeaning']): errors.append('R6 Aussagegrenze fehlt')
    reached=set();counts={}
    for row in rows:
        rid=row['recordId'];original=source[rid];old=prior[rid];required=original['recordType']=='competency'
        disposition='context-only' if not required else 'open-privacy' if rid in PRIVATE else 'introduced-in-grade-6' if old['disposition']=='handoff-grade-6' else 'revisit-and-extend'
        expected=dict(sourceId=original['sourceId'],sourcePath=SOURCE,sourceBinding='orientation',sourceGrades=original['grades'],recordType=original['recordType'],isRequirement=required,parentRecordId=original.get('parentRecordId'),coverage='unassessed' if required else 'not-applicable',r5Disposition=old['disposition'],r5ModuleIds=old['moduleIds'],disposition=disposition)
        if any(row[k]!=v or type(row[k]) is not type(v) for k,v in expected.items()): errors.append(f'R6 {rid}: Quellenrolle, R5-Anschluss oder Disposition verändert')
        counts[disposition]=counts.get(disposition,0)+1
        if not nonempty(row['rationale']): errors.append(f'R6 {rid}: Begründung fehlt')
        if disposition in ('context-only','open-privacy'):
            if row['moduleIds']!=[] or row['fulfillmentMode'] is not None or row['progression'] is not None or row['successorTaskId']!=('IUM-V2-CUR' if required else None): errors.append(f'R6 {rid}: offene oder Kontextrecords ohne Pflichtzuordnung führen')
            if required and row['plannedEvidence'] is not None or not required and not nonempty(row['plannedEvidence']): errors.append(f'R6 {rid}: unzulässiger Eigenbezugsnachweis oder fehlender Kontext')
            continue
        ids=row['moduleIds'];mode=row['fulfillmentMode']
        if not string_set(ids) or not set(ids)<=set(CORE): errors.append(f'R6 {rid}: Nachweis benötigt Kernmodule')
        else: reached.update(ids)
        if mode not in ('direct-module','integrated','cross-cutting') or mode in ('integrated','cross-cutting') and (not isinstance(ids,list) or len(ids)<2): errors.append(f'R6 {rid}: Erfüllungsmodus ungültig')
        if not nonempty(row['plannedEvidence']) or not nonempty(row['progression']) or row['successorTaskId'] is not None: errors.append(f'R6 {rid}: Evidenz oder Progression fehlt; keine Verschiebung nach R7')
    if counts!={'context-only':25,'open-privacy':4,'introduced-in-grade-6':17,'revisit-and-extend':39}: errors.append('R6 17 Übergaben, 39 Wiederaufnahmen, vier offene Eigenbezüge und 25 Kontexte erforderlich')
    if reached!=set(CORE): errors.append('R6 Kernmodul ohne Anforderungszuordnung')
    return errors


def validate_planning(roadmap, matrix, root):
    errors=[]
    keys=('schemaVersion','projectId','asOf','grade','scope','designDecision','sourceReview','entryKnowledge','coreOrder','modules','flexModules','timeAssumptions','variants','retrievalSchedule','projectRequirements','entryGates','auditApplications','grade7Handoff')
    if not header(roadmap,keys,errors,'Roadmap'): return errors
    errors.extend(validate_matrix(matrix,root))
    if roadmap['scope']!=dict(schoolType='Gymnasium Baden-Württemberg',level='E',planningYear='2026/2027',contentProduction='frozen',activeBaseline='v1') or not nonempty(roadmap['designDecision']): errors.append('R6 Geltung, Planungsentscheidung oder Produktionsgrenze ungültig')
    prior=load(root,PREV+'roadmap.json')
    review=roadmap['sourceReview']
    if fields(review,('basisPath','basisCheckedAt','ministryUrl','lesehilfeUrl','finding'),'R6 Quellenprüfung',errors):
        if review['basisPath']!=PREV+'roadmap.json' or review['basisCheckedAt']!=prior['sourceReview']['checkedAt'] or not nonempty(review['finding']) or any(review[k]!=prior['sourceReview'][k] for k in ('ministryUrl','lesehilfeUrl')): errors.append('R6 Quellenprüfung ohne überprüfbare R5-Grundlage')
    entry=roadmap['entryKnowledge'];entry_minutes=0
    if fields(entry,('status','basis','cohortCaveat','checks','totalMinutes','budgetLocation','broadGapAction','decisionRule'),'R6 Anschlusswissen',errors):
        if entry['status']!='not-observed' or entry['basis']!='approved-plan-not-cohort-evidence' or entry['broadGapAction']!='replan-before-dependent-module' or entry['budgetLocation']!='variants.entryCheckMinutes' or not nonempty(entry['cohortCaveat']) or not nonempty(entry['decisionRule']): errors.append('R6 Planungsabnahme darf keine Vorkenntnisse belegen; breite Lücken benötigen Neuplanung')
        checks=table(entry['checks'],'id',[f'R6-ENTRY-{i:02}' for i in range(1,7)],('id','r5ModuleId','beforeModule','minutes','plannedProduct','criterion','gapResponse','state'),errors,'Einstiegsklärungen')
        before=(CORE[0],CORE[1],CORE[5],CORE[6],CORE[2],CORE[4])
        for c in checks:
            n=int(c['id'][-2:])
            if c['r5ModuleId']!=f'V2-G5-M{n:02}' or c['beforeModule']!=before[n-1] or c['state']!='not-run' or not all(nonempty(c[k]) for k in ('plannedProduct','criterion','gapResponse')) or not positive(c['minutes']): errors.append('R6 Einstieg benötigt geplante Handlung, Kriterium und Anschlussentscheidung vor dem Zielmodul')
            if positive(c['minutes']): entry_minutes+=c['minutes']
        if not positive(entry['totalMinutes']) or entry['totalMinutes']!=entry_minutes: errors.append('R6 Einstiegszeit widerspricht Einzelklärungen')
    if roadmap['coreOrder']!=CORE: errors.append('R6 neue Kernfolge erforderlich')
    principles={p['id'] for g in load(root,LXF+'learning-architecture.json')['principleGroups'] for p in g['principles']}
    modules=table(roadmap['modules'],'id',CORE,('id','kind','title','goal','learningAction','plannedProduct','feedbackAndRevision','support','digitalPurpose','fallback','minutes','timeComponents','dependsOn','principleIds','implementation','evidenceStatus','pilotQuestion'),errors,'Kernmodule')
    for m in modules:
        if not all(nonempty(m[k]) for k in ('title','goal','learningAction','plannedProduct','feedbackAndRevision','support','digitalPurpose','fallback','pilotQuestion')): errors.append(f"R6 {m['id']}: Lernbogen unvollständig")
        if m['kind']!='core' or m['implementation']!='not-started' or m['evidenceStatus']!='planned-only': errors.append('R6 Planung ist keine Umsetzung oder Evidenz')
        if not names(m['dependsOn'],True) or not set(m['dependsOn'])<=set(CORE[:CORE.index(m['id'])]): errors.append('R6 zyklische oder unbekannte Modulvoraussetzung')
        if not string_set(m['principleIds']) or not set(m['principleIds'])<=principles: errors.append('R6 unbekannter Prinzipienbezug')
        if fields(m['timeComponents'],COMPONENTS,'R6 Modulzeiten',errors):
            if not all(positive(v) for v in m['timeComponents'].values()) or not positive(m['minutes']) or sum(m['timeComponents'].values())!=m['minutes']: errors.append('R6 vollständige Modulzeiten und korrekte Summe erforderlich')
    total=sum(m['minutes'] for m in modules if positive(m['minutes']))
    assumption=roadmap['timeAssumptions']
    if fields(assumption,('unitMinutes','status','derivation','coreMinutes','meaning','belowMinimum','bridgingRule'),'R6 Zeitannahmen',errors):
        if type(assumption['unitMinutes']) is not int or assumption['unitMinutes']!=45 or assumption['status']!='project-estimate-not-piloted' or assumption['derivation']!='independent-grade-6-task-budget' or not positive(assumption['coreMinutes']) or assumption['coreMinutes']!=total or not all(nonempty(assumption[k]) for k in ('meaning','belowMinimum','bridgingRule')): errors.append('R6 eigenständig kalkulierte Zeitannahme fehlt')
    flex_minutes={}
    for f in table(roadmap['flexModules'],'id',FLEX,('id','kind','title','minutes','dependsOn','purpose','newRequiredCoverage'),errors,'Flexmodule'):
        if f['kind']!='flex' or f['newRequiredCoverage'] is not False or not positive(f['minutes']) or not nonempty(f['title']) or not nonempty(f['purpose']) or not string_set(f['dependsOn']) or not set(f['dependsOn'])<=set(CORE): errors.append('R6 Flexmodul ohne Grenze oder Voraussetzung')
        if positive(f['minutes']): flex_minutes[f['id']]=f['minutes']
    minimum=extended=0
    for r in table(roadmap['retrievalSchedule'],'afterModule',(CORE[2],CORE[4],CORE[6]),('afterModule','revisitModule','minimumMinutes','extendedMinutes','purpose'),errors,'Wiederaufnahme'):
        if r['revisitModule'] not in CORE[:CORE.index(r['afterModule'])] or not nonempty(r['purpose']): errors.append('R6 Wiederaufnahme ohne früheren Lernbogen')
        if not positive(r['minimumMinutes']) or not positive(r['extendedMinutes']) or r['extendedMinutes']<r['minimumMinutes']: errors.append('R6 Wiederaufnahmezeit ungültig')
        else: minimum+=r['minimumMinutes'];extended+=r['extendedMinutes']
    year_parts=('coreMinutes','entryCheckMinutes','bridgingMinutes','spacedPracticeMinutes','orchestrationMinutes','bufferMinutes')
    for v in table(roadmap['variants'],'id',('V2-G6-T32','V2-G6-T36','V2-G6-T40'),('id','availableUnits',*year_parts,'flexIds','totalMinutes','limitation'),errors,'Jahresvarianten'):
        if not all(natural(v[k]) for k in year_parts) or not positive(v['availableUnits']) or not positive(v['totalMinutes']) or not names(v['flexIds'],True) or not set(v['flexIds'])<=set(flex_minutes): errors.append('R6 Jahreszeiten oder Flexverweise ungültig');continue
        units=v['availableUnits']
        if units!=int(v['id'][-2:]) or v['coreMinutes']!=total or v['entryCheckMinutes']!=entry_minutes or v['bridgingMinutes']!=(0 if units==32 else 45) or v['totalMinutes']!=units*45 or v['totalMinutes']!=sum(v[k] for k in year_parts)+sum(flex_minutes[i] for i in v['flexIds']): errors.append('R6 Zeitbudget zählt falsch, doppelt oder ohne Einstieg/Überbrückung')
        if v['spacedPracticeMinutes']!=(minimum if units==32 else extended) or not nonempty(v['limitation']): errors.append('R6 verteilte Übung oder Einsatzgrenze fehlt')
    reqs={r['id'] for r in load(root,'roadmap/v2/requirements/requirements.json')['requirements'] if 6 in r['grades']}
    for r in table(roadmap['projectRequirements'],'requirementId',reqs,('requirementId','disposition','location','rationale','coverage'),errors,'Projektanforderungen'):
        if r['coverage']!='unassessed' or r['disposition'] not in ('maintained-boundary','planning-assignment','handoff') or not nonempty(r['rationale']) or r['location'] not in ('scope','curriculum-map.json','modules','entryGates','IUM-V2-DASH'): errors.append('R6 Projektzuordnung oder Abschnittsreferenz ungültig')
    for g in table(roadmap['entryGates'],'id',GATES,('id','owner','risk','trigger','condition','state'),errors,'Eintrittsgates'):
        if g['state']!='open' or not all(nonempty(g[k]) for k in ('owner','risk','trigger','condition')): errors.append('R6 reale Risiken und Gates dürfen nicht vorweggenommen werden')
    audit={r['artifactId']:r['decision'] for r in load(root,'roadmap/v2/audits/artifact-inventory.json')['records']}
    for a in table(roadmap['auditApplications'],'artifactId',('IUM01','IUM02','IUM05','IUM06','IUM07','IUM09','IUM10'),('artifactId','decision','application'),errors,'Auditfolgen'):
        if a['decision']!=audit[a['artifactId']] or not nonempty(a['application']): errors.append('R6 widerspricht dem Übernahmeaudit')
    handoff=roadmap['grade7Handoff']
    if fields(handoff,('nextTask','state','activation','plannedEntryEvidence','limitation'),'R7-Anschluss',errors):
        if handoff['nextTask']!='IUM-V2-R7' or handoff['state']!='planning-only' or handoff['activation']!='explicit-r6-user-approval' or not nonempty(handoff['limitation']): errors.append('R6 darf R7 weder aktivieren noch Vorkenntnisse bestätigen')
        products={m['id']:m['plannedProduct'] for m in modules}
        for h in table(handoff['plannedEntryEvidence'],'moduleId',CORE,('moduleId','evidence'),errors,'R7-Eingangsprodukte'):
            if not nonempty(h['evidence']) or h['evidence']!=products.get(h['moduleId']): errors.append('R6 R7-Übergabe benötigt geplantes Modulprodukt')
    return errors


def validate_acceptance(data):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',gate='IUM-V2-R5',state='approved-by-user',date='2026-09-06',acceptedCommit=BASE_COMMIT,decisionBy='user',nextTask='IUM-V2-R6',contentProduction='frozen',pilot='not-started',publication='closed')
    if not fields(data,(*expected,'evidence'),'R5-Abnahme',errors): return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()): errors.append('R6 benötigt ausdrückliche R5-Abnahme des geprüften Commits')
    evidence=data['evidence']
    if fields(evidence,('kind','target','label','required'),'R5-Abnahmebeleg',errors):
        if evidence['kind']!='vault' or evidence['target']!='2026-09-03 - IUM-V2-R5 Roadmap Klasse 5 neu aufbauen' or not nonempty(evidence['label']) or evidence['required'] is not True: errors.append('R6 R5-Abnahmebeleg ungültig')
    return errors


def validate_status(data, root):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',grade=6,workStatus='review',reviewType='ai-assisted-document-self-review',reviewer='Codex',userAcceptance='pending',baseCommit=BASE_COMMIT,r5Acceptance=ACCEPTANCE,nextTask='IUM-V2-R7',nextTaskCondition='explicit-r6-user-approval',contentProduction='frozen')
    if not fields(data,(*expected,'maturity','verificationScope','carryForward','privateRecordCarry','openGateIds','inputDigests'),'R6-Status',errors): return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()): errors.append('R6 Status darf keine Folgegates öffnen')
    maturity=dict(concept='reviewed',implementation='not-started',technicalVerification='passed',curriculumCoverage='unassessed',userTesting='not-started',classroomPilot='not-started',release='closed')
    if data['maturity']!=maturity or not nonempty(data['verificationScope']): errors.append('R6 Reifeachsen oder Prüfgrenzen ungültig')
    if data['carryForward']!=load(root,PREV+'status.json')['carryForward'] or data['privateRecordCarry']!=sorted(PRIVATE) or not string_set(data['openGateIds']) or set(data['openGateIds'])!=GATES: errors.append('R6 offene Grundlagen-, Eigenbezugs- oder Übergangsfragen fehlen')
    digests=data['inputDigests']
    if not isinstance(digests,dict) or set(digests)!=INPUTS: errors.append('R6 Prüfeingänge unvollständig');return errors
    for p in sorted(INPUTS):
        try:
            if digests[p]!=hashlib.sha256(read_input(root,p).encode('utf-8')).hexdigest(): errors.append(f'R6 Review veraltet: {p}')
        except (OSError,UnicodeError,ValueError): errors.append(f'R6 Prüfeingang fehlt: {p}')
    return errors


def validate_repository(root: Path):
    errors=[f'{p} fehlt' for p in FILES if not (root/p).is_file()]
    payload={}
    for p in (ROADMAP,MATRIX,STATUS,ACCEPTANCE):
        if not (root/p).is_file(): continue
        try: payload[p]=load(root,p)
        except (OSError,UnicodeError,ValueError): errors.append(f'R6 ungültiges JSON: {p}')
    try:
        if ROADMAP in payload and MATRIX in payload: errors.extend(validate_planning(payload[ROADMAP],payload[MATRIX],root))
        if STATUS in payload: errors.extend(validate_status(payload[STATUS],root))
        if ACCEPTANCE in payload: errors.extend(validate_acceptance(payload[ACCEPTANCE]))
    except (OSError,UnicodeError,ValueError,KeyError,TypeError): errors.append('R6 benötigter Grundlagenvertrag fehlt oder ist ungültig')
    return errors
