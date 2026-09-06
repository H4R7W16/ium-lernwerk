"""Grade 5 planning contracts: assignments are not observed curriculum coverage."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

if __package__:
    from .validate_v2_governance import fields, nonempty, read_input, string_set
else:
    from validate_v2_governance import fields, nonempty, read_input, string_set

BASE = 'roadmap/v2/grades/grade-5/'
ROADMAP = BASE+'roadmap.json'
MATRIX = BASE+'curriculum-map.json'
STATUS = BASE+'status.json'
ACCEPTANCE = 'roadmap/v2/audits/acceptance.json'
SCHEMA = 'schemas/v2/grade-5.schema.json'
FILES = (ROADMAP, MATRIX, STATUS, ACCEPTANCE, SCHEMA, BASE+'README.md', BASE+'validation-report.md')
BASE_COMMIT = 'dc059cffcb2866c6e0d7df3c83dbc0410d14d680'
LXF = 'roadmap/v2/foundations/learning-experience/'
SOURCES = {
    'curriculum/basiskurs-medienbildung/competencies.json': ('SRC-CUR-BMB-2016','official'),
    'curriculum/lesehilfe-2026-27/competencies.json': ('SRC-CUR-LESEHILFE-2026-27','orientation'),
}
INPUTS = set(SOURCES) | {
    'roadmap/v2/status.json','roadmap/v2/requirements/requirements.json',
    'roadmap/v2/foundations/curriculum/source-basis.json','roadmap/v2/foundations/curriculum/gap-assessments.json',
    LXF+'learner-profile.json',LXF+'learning-architecture.json',LXF+'evidence-register.json',LXF+'material-patterns.json',
    LXF+'teacher-orchestration.md',LXF+'experience-gates.json',LXF+'status.json',
    'roadmap/v2/foundations/governance/governance-contract.json','roadmap/v2/foundations/governance/status.json',
    'roadmap/v2/audits/artifact-inventory.json','roadmap/v2/audits/follow-up-tasks.json','roadmap/v2/audits/status.json',
} | (set(FILES)-{STATUS})
CORE = [f'V2-G5-M{i:02}' for i in range(1,7)]
FLEX = {'V2-G5-F01','V2-G5-F02'}
PRIVATE_RECORDS = {'BMB16-GYM-PK-RK-001','BMB16-GYM-IK-MG-001','LH26-E-DP-002','LH26-E-DP-003','LH26-E-DP-009','LH26-E-KS-011'}
GATES = {'R5-ACCESS','R5-BUDGET','R5-PRIVACY','R5-PILOT'}
TIME_COMPONENTS = {'orientationAndExplanation','guidedPractice','independentApplication','feedbackAndRevision','consolidationAndTransfer'}


def load(root, path):
    return json.loads(read_input(root,path))


def names(value, empty=False):
    return (empty and value == []) or string_set(value)


def positive(value):
    return type(value) is int and value > 0


def table(value, key, expected, keys, errors, label):
    if not isinstance(value,list):
        errors.append(f'R5 {label}: Liste erforderlich');return []
    valid=[]
    for row in value:
        if fields(row,keys,label,errors) and nonempty(row.get(key)):
            valid.append(row)
        else:
            errors.append(f'R5 {label}: ungültiger Eintrag')
    ids=[r[key] for r in valid]
    if set(ids)!=set(expected) or len(ids)!=len(set(ids)):
        errors.append(f'R5 {label}: Pflicht-IDs fehlen, sind doppelt oder unbekannt')
    return [r for r in valid if r[key] in expected]


def header(data, keys, errors, label):
    if not fields(data,keys,label,errors): return False
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',grade=5)
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()):
        errors.append(f'R5 {label}: Identität oder Jahrgang ungültig')
    return True


def source_records(root):
    return {r['id']:(path,sid,binding,r) for path,(sid,binding) in SOURCES.items()
            for r in load(root,path)['records'] if 5 in r['grades']}


def validate_matrix(data, root):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','grade','coverageMeaning','records'),errors,'Curriculummatrix'): return errors
    source=source_records(root)
    if not nonempty(data['coverageMeaning']): errors.append('R5 Aussagegrenze fehlt')
    rows=table(data['records'],'recordId',source,('recordId','sourceId','sourcePath','sourceBinding','sourceGrades','recordType','isRequirement','parentRecordId','coverage','disposition','fulfillmentMode','moduleIds','plannedEvidence','rationale','successorTaskId'),errors,'Curriculumrecords')
    reached=set()
    for row in rows:
        rid=row['recordId'];path,sid,binding,original=source[rid]
        required=original['recordType'] in ('competency','process-competency')
        expected=dict(sourcePath=path,sourceId=sid,sourceBinding=binding,sourceGrades=original['grades'],recordType=original['recordType'],isRequirement=required,parentRecordId=original.get('parentRecordId'),coverage='unassessed' if required else 'not-applicable')
        if any(row[k]!=v or type(row[k]) is not type(v) for k,v in expected.items()): errors.append(f'R5 {rid}: Quellenrolle oder Abdeckungsgrenze verändert')
        if not nonempty(row['rationale']): errors.append(f'R5 {rid}: Begründung fehlt')
        disposition=row['disposition']
        if not required:
            if disposition!='context-only' or row['moduleIds']!=[] or row['fulfillmentMode'] is not None or row['successorTaskId'] is not None or not nonempty(row['plannedEvidence']):
                errors.append(f'R5 {rid}: Kontextrecord darf keine Pflichtkompetenz erzeugen')
            continue
        if rid in PRIVATE_RECORDS:
            if disposition!='open-privacy' or row['successorTaskId']!='IUM-V2-CUR': errors.append(f'R5 {rid}: Eigenbezug muss offen bleiben')
        elif disposition=='handoff-grade-6':
            if binding!='orientation' or 6 not in original['grades'] or row['successorTaskId']!='IUM-V2-R6': errors.append(f'R5 {rid}: unzulässige Jahrgangsverschiebung')
        elif disposition!='planned-in-grade-5':
            errors.append(f'R5 {rid}: unbekannte oder unbegründet offene Disposition')
        if disposition=='planned-in-grade-5':
            ids=row['moduleIds'];mode=row['fulfillmentMode']
            if not string_set(ids) or not set(ids)<=set(CORE): errors.append(f'R5 {rid}: Kernmodulzuordnung fehlt')
            else: reached.update(ids)
            if mode not in ('direct-module','integrated','cross-cutting') or mode in ('integrated','cross-cutting') and (not isinstance(ids,list) or len(ids)<2): errors.append(f'R5 {rid}: Erfüllungsmodus ungültig')
            if not nonempty(row['plannedEvidence']) or row['successorTaskId'] is not None: errors.append(f'R5 {rid}: geplanter Nachweis fehlt')
            if rid=='BMB16-GYM-IK-GM-003' and (mode!='cross-cutting' or ids!=['V2-G5-M01','V2-G5-M02','V2-G5-M04']): errors.append('R5 Werkzeugkompetenz benötigt reguläre verteilte Lernhandlungen')
        elif row['moduleIds']!=[] or row['plannedEvidence'] is not None or row['fulfillmentMode'] is not None:
            errors.append(f'R5 {rid}: offener oder verschobener Record darf keinen Nachweis behaupten')
    if reached!=set(CORE): errors.append('R5 Kernmodul ohne Anforderungszuordnung')
    return errors


def validate_planning(roadmap, matrix, root):
    errors=[]
    keys=('schemaVersion','projectId','asOf','grade','scope','designDecision','sourceReview','coreOrder','modules','flexModules','timeAssumptions','variants','retrievalSchedule','toolEvidenceMatrix','toolMatrixAdditionalMinutes','projectRequirements','entryGates','auditApplications')
    if not header(roadmap,keys,errors,'Roadmap'): return errors
    errors.extend(validate_matrix(matrix,root))
    if roadmap['scope']!=dict(schoolType='Gymnasium Baden-Württemberg',level='E',planningYear='2026/2027',contentProduction='frozen',activeBaseline='v1'):
        errors.append('R5 Geltung oder Produktionsgrenze verändert')
    if not nonempty(roadmap['designDecision']): errors.append('R5 neue Planungsentscheidung fehlt')
    review=roadmap['sourceReview']
    if fields(review,('checkedAt','ministryUrl','lesehilfeUrl','finding','bmbContentCheck'),'Quellenprüfung',errors):
        if review['checkedAt']!='2026-09-06' or not all(nonempty(v) for v in review.values()) or review['bmbContentCheck']!='frozen-dataset-with-2026-09-03-foundation-review': errors.append('R5 Quellenprüfumfang ungültig')
        else:
            basis=load(root,'roadmap/v2/foundations/curriculum/source-basis.json')['sources']
            if review['ministryUrl']!=basis[0]['currentReview']['landingPageUrl'] or review['lesehilfeUrl']!=basis[2]['currentReview']['directUrl']: errors.append('R5 Quellenfundstelle verändert')
    if roadmap['coreOrder']!=CORE: errors.append('R5 neue Kernfolge fehlt oder wurde durch V1 ersetzt')
    principles={p['id'] for g in load(root,LXF+'learning-architecture.json')['principleGroups'] for p in g['principles']}
    modules=table(roadmap['modules'],'id',CORE,('id','kind','title','goal','learningAction','plannedProduct','feedbackAndRevision','support','digitalPurpose','fallback','minutes','timeComponents','dependsOn','principleIds','implementation','evidenceStatus','pilotQuestion'),errors,'Kernmodule')
    for m in modules:
        if not all(nonempty(m[k]) for k in ('title','goal','learningAction','plannedProduct','feedbackAndRevision','support','digitalPurpose','fallback','pilotQuestion')): errors.append(f"R5 {m['id']}: Lernbogen unvollständig")
        if m['kind']!='core' or m['implementation']!='not-started' or m['evidenceStatus']!='planned-only': errors.append('R5 Planung darf keine Umsetzung oder Evidenz hochstufen')
        if not names(m['dependsOn'],True) or not set(m['dependsOn'])<=set(CORE[:CORE.index(m['id'])]): errors.append('R5 zyklische oder unbekannte Modulvoraussetzung')
        if not string_set(m['principleIds']) or not set(m['principleIds'])<=principles: errors.append('R5 unbekannter Prinzipienbezug')
        times=m['timeComponents']
        if fields(times,TIME_COMPONENTS,'Modulzeiten',errors):
            if not all(positive(v) for v in times.values()) or not positive(m['minutes']) or sum(times.values())!=m['minutes']: errors.append('R5 Modulzeit benötigt Übung, Feedback, Sicherung und korrekte Summe')
    total=sum(m['minutes'] for m in modules if positive(m['minutes']))
    assumption=roadmap['timeAssumptions']
    if fields(assumption,('unitMinutes','status','coreMinutes','meaning','belowMinimum'),'Zeitannahmen',errors):
        if type(assumption['unitMinutes']) is not int or assumption['unitMinutes']!=45 or assumption['status']!='project-estimate-not-piloted' or assumption['coreMinutes']!=total or not nonempty(assumption['meaning']) or not nonempty(assumption['belowMinimum']): errors.append('R5 Zeitannahme fehlt oder widerspricht Modulen')
    flex=table(roadmap['flexModules'],'id',FLEX,('id','kind','title','minutes','dependsOn','purpose','newRequiredCoverage'),errors,'Flexmodule')
    flex_minutes={}
    for f in flex:
        if f['kind']!='flex' or f['newRequiredCoverage'] is not False or not positive(f['minutes']) or not nonempty(f['title']) or not nonempty(f['purpose']) or not string_set(f['dependsOn']) or not set(f['dependsOn'])<=set(CORE): errors.append('R5 Flexmodul unzulässig oder ohne Voraussetzung')
        if positive(f['minutes']): flex_minutes[f['id']]=f['minutes']
    retrieval=table(roadmap['retrievalSchedule'],'afterModule',('V2-G5-M02','V2-G5-M04','V2-G5-M06'),('afterModule','revisitModule','minimumMinutes','extendedMinutes','purpose'),errors,'Wiederaufnahme')
    minimum=extended=0
    for r in retrieval:
        if r['revisitModule'] not in CORE[:CORE.index(r['afterModule'])] or not nonempty(r['purpose']): errors.append('R5 Wiederaufnahme ohne früheren Lernbogen')
        if not positive(r['minimumMinutes']) or not positive(r['extendedMinutes']) or r['extendedMinutes']<r['minimumMinutes']: errors.append('R5 Wiederaufnahmezeit ungültig')
        else: minimum+=r['minimumMinutes'];extended+=r['extendedMinutes']
    variants=table(roadmap['variants'],'id',('V2-G5-T32','V2-G5-T36','V2-G5-T40'),('id','availableUnits','coreMinutes','spacedPracticeMinutes','orchestrationMinutes','bufferMinutes','flexIds','totalMinutes','limitation'),errors,'Jahresvarianten')
    for v in variants:
        if not all(positive(v[k]) for k in ('availableUnits','coreMinutes','spacedPracticeMinutes','orchestrationMinutes','bufferMinutes','totalMinutes')) or not names(v['flexIds'],True) or not set(v['flexIds'])<=set(flex_minutes):
            errors.append('R5 Jahreszeiten oder Flexverweise ungültig');continue
        if v['availableUnits']!=int(v['id'][-2:]) or v['coreMinutes']!=total or v['totalMinutes']!=v['availableUnits']*45 or v['totalMinutes']!=sum(v[k] for k in ('coreMinutes','spacedPracticeMinutes','orchestrationMinutes','bufferMinutes'))+sum(flex_minutes[i] for i in v['flexIds']): errors.append('R5 Zeitbudget stimmt nicht oder zählt doppelt')
        if v['spacedPracticeMinutes']!=(minimum if v['availableUnits']==32 else extended) or not nonempty(v['limitation']): errors.append('R5 verteilte Übung oder Zeitgrenze fehlt')
    tools=table(roadmap['toolEvidenceMatrix'],'moduleId',('V2-G5-M01','V2-G5-M02','V2-G5-M04'),('moduleId','toolFamily','routine','independence','evidence'),errors,'Werkzeugmatrix')
    if type(roadmap['toolMatrixAdditionalMinutes']) is not int or roadmap['toolMatrixAdditionalMinutes']!=0: errors.append('R5 Werkzeugmatrix darf keine Zusatzzeit erzeugen')
    for t in tools:
        if not all(nonempty(v) for v in t.values()): errors.append('R5 Werkzeugmatrix ohne konkrete Lernhandlung')
    if len({t['toolFamily'] for t in tools if nonempty(t['toolFamily'])})<3: errors.append('R5 unterschiedliche Werkzeugkontexte fehlen')
    reqs={r['id'] for r in load(root,'roadmap/v2/requirements/requirements.json')['requirements'] if 5 in r['grades']}
    for r in table(roadmap['projectRequirements'],'requirementId',reqs,('requirementId','disposition','location','rationale','coverage'),errors,'Projektanforderungen'):
        if r['coverage']!='unassessed' or r['disposition'] not in ('maintained-boundary','planning-assignment','handoff') or not nonempty(r['location']) or not nonempty(r['rationale']): errors.append('R5 Projektzuordnung oder Aussagegrenze ungültig')
        if not nonempty(r['location']) or r['location'] not in ('scope','curriculum-map.json','toolEvidenceMatrix','modules','entryGates','IUM-V2-DASH'):
            errors.append('R5 Projektbeleg verweist auf keinen vorhandenen Planungsabschnitt oder Folgeauftrag')
    for g in table(roadmap['entryGates'],'id',GATES,('id','owner','trigger','condition','state'),errors,'Eintrittsgates'):
        if g['state']!='open' or not all(nonempty(g[k]) for k in ('owner','trigger','condition')): errors.append('R5 reales Eintrittsgate darf nicht vorweggenommen werden')
    audit={r['artifactId']:r['decision'] for r in load(root,'roadmap/v2/audits/artifact-inventory.json')['records']}
    for a in table(roadmap['auditApplications'],'artifactId',('IUM01','IUM02','IUM05','IUM06','IUM07','IUM09','IUM10'),('artifactId','decision','application'),errors,'Auditfolgen'):
        if a['decision']!=audit[a['artifactId']] or not nonempty(a['application']): errors.append('R5 widerspricht dem abgenommenen Übernahmeaudit')
    return errors


def validate_acceptance(data):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',gate='IUM-V2-AUD',state='approved-by-user',date='2026-09-06',acceptedCommit=BASE_COMMIT,decisionBy='user',nextTask='IUM-V2-R5',contentProduction='frozen',pilot='not-started',publication='closed')
    if not fields(data,(*expected,'evidence'),'AUD-Abnahme',errors): return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()): errors.append('R5 benötigt die ausdrückliche AUD-Abnahme des geprüften Commits')
    evidence=data['evidence']
    if fields(evidence,('kind','target','label','required'),'AUD-Abnahmebeleg',errors):
        if evidence['kind']!='vault' or evidence['target']!='2026-09-03 - IUM-V2-AUD IUM- und LXP-Übernahmeaudit durchführen' or not nonempty(evidence['label']) or evidence['required'] is not True: errors.append('R5 AUD-Abnahmebeleg ungültig')
    return errors


def validate_status(data, root):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',grade=5,workStatus='review',reviewType='ai-assisted-document-self-review',reviewer='Codex',userAcceptance='pending',baseCommit=BASE_COMMIT,auditAcceptance=ACCEPTANCE,nextTask='IUM-V2-R6',nextTaskCondition='explicit-r5-user-approval',contentProduction='frozen')
    if not fields(data,(*expected,'maturity','verificationScope','carryForward','openGateIds','inputDigests'),'R5-Status',errors): return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()): errors.append('R5 Status darf keine Folgegates öffnen')
    maturity=dict(concept='reviewed',implementation='not-started',technicalVerification='passed',curriculumCoverage='unassessed',userTesting='not-started',classroomPilot='not-started',release='closed')
    if data['maturity']!=maturity or not nonempty(data['verificationScope']): errors.append('R5 Reifeachsen oder Prüfgrenzen ungültig')
    if data['carryForward']!=load(root,'roadmap/v2/audits/status.json')['carryForward'] or not string_set(data['openGateIds']) or set(data['openGateIds'])!=GATES: errors.append('R5 offene Grundlagen- oder Eintrittsfragen fehlen')
    digests=data['inputDigests']
    if not isinstance(digests,dict) or set(digests)!=INPUTS: errors.append('R5 Prüfeingänge unvollständig');return errors
    for p in sorted(INPUTS):
        try:
            if digests[p]!=hashlib.sha256(read_input(root,p).encode('utf-8')).hexdigest(): errors.append(f'R5 Review veraltet: {p}')
        except (OSError,UnicodeError,ValueError): errors.append(f'R5 Prüfeingang fehlt: {p}')
    return errors


def validate_repository(root: Path):
    errors=[f'{p} fehlt' for p in FILES if not (root/p).is_file()]
    payload={}
    for p in (ROADMAP,MATRIX,STATUS,ACCEPTANCE):
        if not (root/p).is_file(): continue
        try: payload[p]=load(root,p)
        except (OSError,UnicodeError,ValueError): errors.append(f'R5 ungültiges JSON: {p}')
    try:
        if ROADMAP in payload and MATRIX in payload: errors.extend(validate_planning(payload[ROADMAP],payload[MATRIX],root))
        if STATUS in payload: errors.extend(validate_status(payload[STATUS],root))
        if ACCEPTANCE in payload: errors.extend(validate_acceptance(payload[ACCEPTANCE]))
    except (OSError,UnicodeError,ValueError,KeyError,TypeError):
        errors.append('R5 benötigter Grundlagenvertrag fehlt oder ist ungültig')
    return errors
