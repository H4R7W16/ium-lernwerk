"""Grade 7 contracts: curricular planning and arithmetic fit never imply availability."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

if __package__:
    from .validate_v2_governance import fields, nonempty, read_input, string_set
    from .validate_v2_grade6 import INPUTS as PREVIOUS_INPUTS, positive, natural, names
else:
    from validate_v2_governance import fields, nonempty, read_input, string_set
    from validate_v2_grade6 import INPUTS as PREVIOUS_INPUTS, positive, natural, names

BASE='roadmap/v2/grades/grade-7/'
PREV='roadmap/v2/grades/grade-6/'
G5='roadmap/v2/grades/grade-5/'
ROADMAP=BASE+'roadmap.json'
MATRIX=BASE+'curriculum-map.json'
PROGRESSION=BASE+'progression.json'
STATUS=BASE+'status.json'
ACCEPTANCE=PREV+'acceptance.json'
SCHEMA='schemas/v2/grade-7.schema.json'
FILES=(ROADMAP,MATRIX,PROGRESSION,STATUS,ACCEPTANCE,SCHEMA,BASE+'README.md',BASE+'validation-report.md')
BASE_COMMIT='c38ff9b0b037539b37d6964091c38dc3c323344a'
SOURCES={'curriculum/aufbaukurs-informatik/competencies.json':'official','curriculum/lesehilfe-2026-27/competencies.json':'orientation'}
INPUTS=set(PREVIOUS_INPUTS)|{PREV+'status.json','curriculum/aufbaukurs-informatik/competencies.json','roadmap/time-model.json'}|(set(FILES)-{STATUS})
MODULES=[f'V2-G7-M{i:02}' for i in range(1,8)]
CORE=MODULES[:5]
EXTENSIONS=MODULES[5:]
FLEX={'V2-G7-F01','V2-G7-F02'}
STRANDS=[f'R7-PROG-{i:02}' for i in range(1,8)]
REFLECTION={'LH26-E-DP-013','LH26-E-DP-014','LH26-E-DP-018'}
GATES={'R7-ENTRY','R7-ACCESS','R7-BUDGET','R7-SCOPE','R7-REFLECTION','R7-PRIVACY','R7-PILOT','R7-DASH'}
COMPONENTS={'orientationAndExplanation','guidedPractice','independentApplication','feedbackAndRevision','consolidationAndTransfer'}
PATH_MODULES={'R7-CORE36':MODULES[:5],'R7-MEDIA40':MODULES[:6],'R7-DEMAND43':MODULES}
LXF='roadmap/v2/foundations/learning-experience/'


def load(root,path):return json.loads(read_input(root,path))


def table(value,key,expected,keys,errors,label):
    if not isinstance(value,list):errors.append(f'R7 {label}: Liste erforderlich');return []
    valid=[]
    for row in value:
        if fields(row,keys,label,errors) and nonempty(row.get(key)):valid.append(row)
        else:errors.append(f'R7 {label}: ungültiger Eintrag')
    ids=[r[key] for r in valid]
    if set(ids)!=set(expected) or len(ids)!=len(set(ids)):errors.append(f'R7 {label}: Pflicht-IDs fehlen, sind doppelt oder unbekannt')
    return [r for r in valid if r[key] in expected]


def header(data,keys,errors,label):
    if not fields(data,keys,label,errors):return False
    for k,v in dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',grade=7).items():
        if data[k]!=v or type(data[k]) is not type(v):errors.append(f'R7 {label}: Identität oder Jahrgang ungültig')
    return True


def validate_matrix(data,root):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','grade','coverageMeaning','records'),errors,'Matrix'):return errors
    source={r['id']:(path,binding,r) for path,binding in SOURCES.items() for r in load(root,path)['records'] if 7 in r['grades']}
    rows=table(data['records'],'recordId',source,('recordId','sourceId','sourcePath','sourceBinding','sourceGrades','recordType','isRequirement','parentRecordId','coverage','disposition','fulfillmentMode','moduleIds','plannedEvidence','progressionStrandIds','rationale','successorGateId'),errors,'Curriculumrecords')
    if not nonempty(data['coverageMeaning']):errors.append('R7 Aussagegrenze fehlt')
    reached=set();counts={}
    for row in rows:
        rid=row['recordId'];path,binding,original=source[rid];req=original['recordType'] in ('competency','process-competency')
        expected=dict(sourceId=original['sourceId'],sourcePath=path,sourceBinding=binding,sourceGrades=original['grades'],recordType=original['recordType'],isRequirement=req,parentRecordId=original.get('parentRecordId'),coverage='unassessed' if req else 'not-applicable')
        if any(row[k]!=v or type(row[k]) is not type(v) for k,v in expected.items()):errors.append(f'R7 {rid}: Quellenrolle oder Abdeckungsgrenze verändert')
        d=row['disposition']
        if not nonempty(d):errors.append('R7 Disposition fehlt');continue
        counts[d]=counts.get(d,0)+1
        if not nonempty(row['rationale']):errors.append(f'R7 {rid}: Begründung fehlt')
        if not req:
            if d!='context-only' or row['moduleIds']!=[] or row['fulfillmentMode'] is not None or row['progressionStrandIds']!=[] or row['successorGateId'] is not None or not nonempty(row['plannedEvidence']):errors.append(f'R7 {rid}: Kontext darf keine Pflichtkompetenz erzeugen')
            continue
        if not string_set(row['progressionStrandIds']) or not set(row['progressionStrandIds'])<=set(STRANDS):errors.append(f'R7 {rid}: Progressionsbezug fehlt')
        if rid in REFLECTION:
            if d!='open-reflection' or row['plannedEvidence'] is not None or row['fulfillmentMode'] is not None or row['moduleIds']!=[] or row['successorGateId']!='R7-REFLECTION':errors.append(f'R7 {rid}: persönliche Reflexionsentscheidung muss offen bleiben')
            continue
        ids=row['moduleIds'];mode=row['fulfillmentMode']
        if not string_set(ids) or not set(ids)<=set(MODULES):errors.append(f'R7 {rid}: gültige curriculare Module erforderlich')
        else:
            reached.update(ids)
            wanted='planned-core' if set(ids)<=set(CORE) else 'planned-extension'
            if d!=wanted or binding=='official' and wanted!='planned-core':errors.append(f'R7 {rid}: amtliche Anforderungen im Kern, Erweiterungen separat führen')
        if mode not in ('direct-module','integrated','cross-cutting') or mode in ('integrated','cross-cutting') and (not isinstance(ids,list) or len(ids)<2):errors.append(f'R7 {rid}: Erfüllungsmodus ungültig')
        if not nonempty(row['plannedEvidence']) or row['successorGateId'] is not None:errors.append(f'R7 {rid}: geplante Evidenz fehlt')
    if counts!={'planned-core':71,'planned-extension':8,'open-reflection':3,'context-only':52}:errors.append('R7 vollständige Disposition 71/8/3/52 erforderlich')
    if reached!=set(MODULES):errors.append('R7 curricularer Lernbogen ohne Anforderungsbezug')
    return errors


def validate_progression(data,root):
    errors=[]
    if not header(data,('schemaVersion','projectId','asOf','grade','entryKnowledge','basis','broadGapAction','totalEntryMinutes','strands','privacyCarry','newOpenReflectionIds','interpretation'),errors,'Progression'):return errors
    if data['entryKnowledge']!='not-observed' or data['basis']!='approved-plans-not-cohort-evidence' or data['broadGapAction']!='replan-before-dependent-module' or not nonempty(data['interpretation']):errors.append('R7 Vorjahresplan ist kein Vorwissensnachweis; breite Lücken benötigen Neuplanung')
    old5={m['id'] for m in load(root,G5+'roadmap.json')['modules']}
    old6={m['id']:m for m in load(root,PREV+'roadmap.json')['modules']}
    total=0
    for s in table(data['strands'],'id',STRANDS,('id','r5ModuleIds','r6ModuleId','r6PlannedProduct','r7ModuleIds','progression','entryCheck','boundary'),errors,'Stränge 5–7'):
        prev=f"V2-G6-M{int(s['id'][-2:]):02}"
        if not string_set(s['r5ModuleIds']) or not set(s['r5ModuleIds'])<=old5 or s['r6ModuleId']!=prev or s['r6PlannedProduct']!=old6[prev]['plannedProduct']:errors.append('R7 Anschluss muss auf abgenommene R5/R6-Module und R6-Produkt verweisen')
        if not string_set(s['r7ModuleIds']) or not set(s['r7ModuleIds'])<=set(MODULES) or not nonempty(s['progression']) or not nonempty(s['boundary']):errors.append('R7 neue Progression und Aussagegrenze fehlen')
        c=s['entryCheck']
        if fields(c,('beforeModule','minutes','plannedProduct','criterion','gapResponse','state'),'R7 Einstieg',errors):
            if not names(s['r7ModuleIds']) or c['beforeModule'] not in s['r7ModuleIds'] or c['beforeModule'] not in CORE or c['state']!='not-run' or not positive(c['minutes']) or not all(nonempty(c[k]) for k in ('plannedProduct','criterion','gapResponse')):errors.append('R7 Einstieg benötigt geplantes Produkt, Kriterium und Hilfereaktion vor Kernziel')
            if positive(c['minutes']):total+=c['minutes']
    if not positive(data['totalEntryMinutes']) or data['totalEntryMinutes']!=total:errors.append('R7 Eingangsbudget stimmt nicht')
    if data['privacyCarry']!=load(root,PREV+'status.json')['privateRecordCarry'] or data['newOpenReflectionIds']!=sorted(REFLECTION):errors.append('R7 sechs Vorgängerfragen und drei neue Reflexionsentscheidungen erhalten')
    return errors


def validate_planning(roadmap,matrix,progression,root):
    errors=[]
    keys=('schemaVersion','projectId','asOf','grade','scope','designDecision','sourceReview','moduleOrder','modules','flexModules','timeAssumptions','paths','capacityChecks','retrievalSchedule','integrations','historicalTimeAudit','projectRequirements','entryGates','auditApplications','nextHandoff')
    if not header(roadmap,keys,errors,'Roadmap'):return errors
    errors.extend(validate_matrix(matrix,root));errors.extend(validate_progression(progression,root))
    if roadmap['scope']!=dict(schoolType='Gymnasium Baden-Württemberg',level='E',planningYear='2026/2027',contentProduction='frozen',activeBaseline='v1') or not nonempty(roadmap['designDecision']):errors.append('R7 Geltung, Entscheidung oder Produktionsgrenze ungültig')
    review=roadmap['sourceReview']
    if fields(review,('checkedAt','ministryUrl','lesehilfeUrl','inf7Url','finding','contentIdentity'),'R7 Quellenstand',errors):
        basis=load(root,'roadmap/v2/foundations/curriculum/source-basis.json')['sources']
        if review['checkedAt']!='2026-09-06' or review['ministryUrl']!=basis[0]['currentReview']['landingPageUrl'] or review['inf7Url']!=basis[1]['currentReview']['directUrl'] or review['lesehilfeUrl']!=basis[2]['currentReview']['directUrl'] or review['contentIdentity']!='frozen-datasets-not-byte-rechecked' or not nonempty(review['finding']):errors.append('R7 Quellenrolle oder Prüfumfang ungültig')
    if roadmap['moduleOrder']!=MODULES:errors.append('R7 neue Folge fehlt')
    principles={p['id'] for g in load(root,LXF+'learning-architecture.json')['principleGroups'] for p in g['principles']}
    modules=table(roadmap['modules'],'id',MODULES,('id','kind','title','goal','learningAction','plannedProduct','feedbackAndRevision','support','digitalPurpose','fallback','minutes','timeComponents','dependsOn','principleIds','implementation','evidenceStatus','pilotQuestion'),errors,'Lernbögen')
    times={}
    for m in modules:
        if m['kind']!=('core' if m['id'] in CORE else 'curriculum-extension') or m['implementation']!='not-started' or m['evidenceStatus']!='planned-only':errors.append('R7 Kern, curriculare Erweiterung und Umsetzung getrennt halten')
        if not all(nonempty(m[k]) for k in ('title','goal','learningAction','plannedProduct','feedbackAndRevision','support','digitalPurpose','fallback','pilotQuestion')):errors.append('R7 Lernbogen unvollständig')
        if not names(m['dependsOn'],True) or not set(m['dependsOn'])<=set(MODULES[:MODULES.index(m['id'])]):errors.append('R7 zyklische oder unbekannte Voraussetzung')
        if not string_set(m['principleIds']) or not set(m['principleIds'])<=principles:errors.append('R7 unbekannter Prinzipienbezug')
        if fields(m['timeComponents'],COMPONENTS,'R7 Modulzeiten',errors):
            if not all(positive(v) for v in m['timeComponents'].values()) or not positive(m['minutes']) or sum(m['timeComponents'].values())!=m['minutes']:errors.append('R7 Modulzeit benötigt vollständige Lernfunktionen und richtige Summe')
        if positive(m['minutes']):times[m['id']]=m['minutes']
    assumption=roadmap['timeAssumptions']
    if fields(assumption,('unitMinutes','status','derivation','coreMinutes','extensionMinutes','meaning','broadGapRule','capacityRule'),'R7 Zeitannahmen',errors):
        if type(assumption['unitMinutes']) is not int or assumption['unitMinutes']!=45 or assumption['status']!='project-estimate-not-piloted' or assumption['derivation']!='independent-grade-7-task-budget' or assumption['coreMinutes']!=sum(times.get(i,0) for i in CORE) or assumption['extensionMinutes']!=sum(times.get(i,0) for i in EXTENSIONS) or not all(nonempty(assumption[k]) for k in ('meaning','broadGapRule','capacityRule')):errors.append('R7 eigenständige Zeitbilanz fehlt')
    for f in table(roadmap['flexModules'],'id',FLEX,('id','kind','title','minutes','dependsOn','purpose','newRequiredCoverage'),errors,'Flexmodule'):
        if f['kind']!='flex' or f['newRequiredCoverage'] is not False or not positive(f['minutes']) or not nonempty(f['title']) or not nonempty(f['purpose']) or not string_set(f['dependsOn']) or not set(f['dependsOn'])<=set(CORE):errors.append('R7 Flexmodul unzulässig')
    retrieval=0
    for r in table(roadmap['retrievalSchedule'],'afterModule',MODULES[2:5],('afterModule','revisitModule','minutes','purpose','principleIds'),errors,'Wiederaufnahme'):
        if r['revisitModule'] not in MODULES[:MODULES.index(r['afterModule'])] or not positive(r['minutes']) or not nonempty(r['purpose']) or r['principleIds']!=['LXF04-PR-014','LXF04-PR-015']:errors.append('R7 spätere Wiederaufnahme ohne begründeten Bezug')
        if positive(r['minutes']):retrieval+=r['minutes']
    for i in table(roadmap['integrations'],'id',('R7-INT-01','R7-INT-02','R7-INT-03'),('id','moduleIds','purpose','evidence','timeCreditMinutes','additionalMinutes'),errors,'Integrationen'):
        if not string_set(i['moduleIds']) or not set(i['moduleIds'])<=set(CORE) or not nonempty(i['purpose']) or not nonempty(i['evidence']) or type(i['timeCreditMinutes']) is not int or i['timeCreditMinutes']!=0 or type(i['additionalMinutes']) is not int or i['additionalMinutes']!=0:errors.append('R7 Integration ohne Beleg oder mit künstlicher Zeitgutschrift')
    year_parts=('moduleMinutes','entryCheckMinutes','bridgingMinutes','spacedPracticeMinutes','orchestrationMinutes','bufferMinutes')
    paths=table(roadmap['paths'],'id',PATH_MODULES,('id','label','moduleIds','flexIds',*year_parts,'requiredMinutes','requiredUnits','plannedRecordIds','openCapacityRecordIds','openReflectionRecordIds','availability','decisionGate'),errors,'Jahrespfade')
    requirements=[r for r in matrix.get('records',[]) if isinstance(r,dict) and r.get('disposition') in ('planned-core','planned-extension') and string_set(r.get('moduleIds')) and nonempty(r.get('recordId'))] if isinstance(matrix,dict) and isinstance(matrix.get('records'),list) else []
    strand_targets={s['id']:set(s['r7ModuleIds']) for s in progression.get('strands',[]) if isinstance(s,dict) and nonempty(s.get('id')) and string_set(s.get('r7ModuleIds'))} if isinstance(progression,dict) and isinstance(progression.get('strands'),list) else {}
    for r in requirements:
        refs=r.get('progressionStrandIds')
        if string_set(refs) and any(not (set(r['moduleIds']) & strand_targets.get(s,set())) for s in refs):
            errors.append(f"R7 {r['recordId']}: Progressionsverweis erreicht keinen zugeordneten Lernbogen")
    for p in paths:
        mids=PATH_MODULES[p['id']]
        if p['moduleIds']!=mids or p['flexIds']!=[] or p['availability']!='not-verified' or p['decisionGate']!='R7-SCOPE' or not nonempty(p['label']):errors.append('R7 Pfadgrenze oder Verfügbarkeit unzulässig')
        if not all(natural(p[k]) for k in year_parts) or not positive(p['requiredMinutes']) or not positive(p['requiredUnits']):errors.append('R7 Jahreszeiten müssen ganzzahlig sein');continue
        if p['moduleMinutes']!=sum(times.get(i,0) for i in mids) or p['entryCheckMinutes']!=progression.get('totalEntryMinutes') or p['bridgingMinutes']!=45 or p['spacedPracticeMinutes']!=retrieval or p['orchestrationMinutes']!=30 or p['bufferMinutes']!=90 or p['requiredMinutes']!=sum(p[k] for k in year_parts) or p['requiredMinutes']!=p['requiredUnits']*45:errors.append('R7 Pfadzeit zählt falsch oder doppelt')
        included=sorted(r['recordId'] for r in requirements if set(r['moduleIds'])<=set(mids))
        excluded=sorted(r['recordId'] for r in requirements if not set(r['moduleIds'])<=set(mids))
        if p['plannedRecordIds']!=included or p['openCapacityRecordIds']!=excluded or p['openReflectionRecordIds']!=sorted(REFLECTION):errors.append('R7 pfadabhängige Coverageprojektion verschweigt offene Anforderungen')
    pathmap={p['id']:p for p in paths}
    checks=[f'{pid}-AT{units}' for pid in PATH_MODULES for units in (32,36,40)]
    for c in table(roadmap['capacityChecks'],'id',checks,('id','pathId','availableUnits','requiredMinutes','deficitMinutes','remainingMinutes','arithmeticFit','localAvailability'),errors,'Kapazitätschecks'):
        pid,units=c['id'].rsplit('-AT',1);units=int(units)
        p=pathmap.get(pid)
        if p is None or not positive(p['requiredMinutes']):errors.append('R7 Kapazitätscheck ohne Pfad');continue
        diff=units*45-p['requiredMinutes']
        expected=dict(pathId=pid,availableUnits=units,requiredMinutes=p['requiredMinutes'],deficitMinutes=max(0,-diff),remainingMinutes=max(0,diff),arithmeticFit=diff>=0,localAvailability='not-verified')
        if any(c[k]!=v or type(c[k]) is not type(v) for k,v in expected.items()):errors.append('R7 Kapazitätsdefizit oder unbestätigte lokale Verfügbarkeit verändert')
    historical={p['id']:p for p in load(root,'roadmap/time-model.json')['annualVariants'] if p.get('grade')==7}
    for h in table(roadmap['historicalTimeAudit'],'variantId',historical,('variantId','sourcePath','historicalUnits','historicalAvailability','role','v2Availability','decision'),errors,'Historische Zeitpfade'):
        old=historical[h['variantId']]
        if h['sourcePath']!='roadmap/time-model.json' or h['historicalUnits']!=old['targetUnits'] or h['historicalAvailability']!=old['availabilityStatus'] or h['role']!='audit-input-only' or h['v2Availability']!='not-derived' or not nonempty(h['decision']):errors.append('R7 historische Pfade erlauben keine V2-Verfügbarkeit')
    reqs={r['id'] for r in load(root,'roadmap/v2/requirements/requirements.json')['requirements'] if 7 in r['grades']}
    for r in table(roadmap['projectRequirements'],'requirementId',reqs,('requirementId','disposition','location','rationale','coverage'),errors,'Projektanforderungen'):
        if r['coverage']!='unassessed' or r['disposition'] not in ('maintained-boundary','planning-assignment','handoff') or r['location'] not in ('scope','curriculum-map.json','paths','progression.json','modules','entryGates','IUM-V2-DASH') or not nonempty(r['rationale']):errors.append('R7 Projektzuordnung oder Abschnittsreferenz ungültig')
    for g in table(roadmap['entryGates'],'id',GATES,('id','owner','risk','trigger','condition','state'),errors,'Eintrittsgates'):
        if g['state']!='open' or not all(nonempty(g[k]) for k in ('owner','risk','trigger','condition')):errors.append('R7 reale Risiken und Gates bleiben offen')
    audit={r['artifactId']:r['decision'] for r in load(root,'roadmap/v2/audits/artifact-inventory.json')['records']}
    for a in table(roadmap['auditApplications'],'artifactId',('IUM01','IUM02','IUM05','IUM06','IUM07','IUM09','IUM10'),('artifactId','decision','application'),errors,'Auditfolgen'):
        if a['decision']!=audit[a['artifactId']] or not nonempty(a['application']):errors.append('R7 widerspricht dem Übernahmeaudit')
    h=roadmap['nextHandoff']
    if fields(h,('nextTask','activation','state','condition'),'DASH-Übergabe',errors):
        if h['nextTask']!='IUM-V2-DASH' or h['activation']!='explicit-r7-user-approval' or h['state']!='planning-only' or not nonempty(h['condition']):errors.append('R7 darf DASH oder Cutover nicht vorwegnehmen')
    return errors


def validate_acceptance(data):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',gate='IUM-V2-R6',state='approved-by-user',date='2026-09-06',acceptedCommit=BASE_COMMIT,decisionBy='user',nextTask='IUM-V2-R7',contentProduction='frozen',pilot='not-started',publication='closed')
    if not fields(data,(*expected,'evidence'),'R6-Abnahme',errors):return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()):errors.append('R7 benötigt ausdrückliche R6-Abnahme des geprüften Commits')
    e=data['evidence']
    if fields(e,('kind','target','label','required'),'R6-Abnahmebeleg',errors):
        if e['kind']!='vault' or e['target']!='2026-09-03 - IUM-V2-R6 Roadmap Klasse 6 neu aufbauen' or not nonempty(e['label']) or e['required'] is not True:errors.append('R7 R6-Abnahmebeleg ungültig')
    return errors


def validate_status(data,root):
    errors=[]
    expected=dict(schemaVersion=1,projectId='ium-lernwerk',asOf='2026-09-06',grade=7,workStatus='review',reviewType='ai-assisted-document-self-review',reviewer='Codex',userAcceptance='pending',baseCommit=BASE_COMMIT,r6Acceptance=ACCEPTANCE,nextTask='IUM-V2-DASH',nextTaskCondition='explicit-r7-user-approval',contentProduction='frozen')
    if not fields(data,(*expected,'maturity','verificationScope','carryForward','privateRecordCarry','newOpenReflectionIds','openGateIds','inputDigests'),'R7-Status',errors):return errors
    if any(data[k]!=v or type(data[k]) is not type(v) for k,v in expected.items()):errors.append('R7 Status darf keine Folgegates öffnen')
    maturity=dict(concept='reviewed',implementation='not-started',technicalVerification='passed',curriculumCoverage='unassessed',userTesting='not-started',classroomPilot='not-started',release='closed')
    if data['maturity']!=maturity or not nonempty(data['verificationScope']):errors.append('R7 Reifeachsen oder Prüfgrenzen ungültig')
    previous=load(root,PREV+'status.json')
    if data['carryForward']!=previous['carryForward'] or data['privateRecordCarry']!=previous['privateRecordCarry'] or data['newOpenReflectionIds']!=sorted(REFLECTION) or not string_set(data['openGateIds']) or set(data['openGateIds'])!=GATES:errors.append('R7 offene Grundlagen-, Reflexions- oder Eintrittsfragen fehlen')
    digests=data['inputDigests']
    if not isinstance(digests,dict) or set(digests)!=INPUTS:errors.append('R7 Prüfeingänge unvollständig');return errors
    for p in sorted(INPUTS):
        try:
            if digests[p]!=hashlib.sha256(read_input(root,p).encode('utf-8')).hexdigest():errors.append(f'R7 Review veraltet: {p}')
        except (OSError,UnicodeError,ValueError):errors.append(f'R7 Prüfeingang fehlt: {p}')
    return errors


def validate_repository(root:Path):
    errors=[f'{p} fehlt' for p in FILES if not (root/p).is_file()]
    payload={}
    for p in (ROADMAP,MATRIX,PROGRESSION,STATUS,ACCEPTANCE):
        if not (root/p).is_file():continue
        try:payload[p]=load(root,p)
        except (OSError,UnicodeError,ValueError):errors.append(f'R7 ungültiges JSON: {p}')
    try:
        if all(p in payload for p in (ROADMAP,MATRIX,PROGRESSION)):errors.extend(validate_planning(payload[ROADMAP],payload[MATRIX],payload[PROGRESSION],root))
        if STATUS in payload:errors.extend(validate_status(payload[STATUS],root))
        if ACCEPTANCE in payload:errors.extend(validate_acceptance(payload[ACCEPTANCE]))
    except (OSError,UnicodeError,ValueError,KeyError,TypeError):errors.append('R7 benötigter Grundlagenvertrag fehlt oder ist ungültig')
    return errors
