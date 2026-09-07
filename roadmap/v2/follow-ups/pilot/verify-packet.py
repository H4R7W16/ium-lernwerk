"""Check this fixed specification packet, never ingest real pilot evidence.

No CLI file input, production status writer or runtime dependency. The decision
probe illustrates the specified work-decision boundary with synthetic facts only.
"""
import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '9365045a2c2a50d2259d01ef172b7b292cd0ee24'
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def require(condition, message):
    if not condition:
        raise ValueError(message)

mod = read(HERE.parent / 'reference-module/specification.json')
protocol = read(HERE / 'protocol.json')
checks = []

def validate_contract(p):
    require(p['state'] == 'review' and p['scope'] == 'instrument-specification-only', 'Specification scope')
    require(p['moduleId'] == mod['moduleId'] == 'V2-G5-M06', 'Module identity')
    require(p['acceptedDesignCommit'] == BASE, 'Accepted design revision')
    require(p['actualState'] == {'moduleImplementation':'not-started','technicalTargetChecks':'not-run','learnerUsage':'not-run','classroomPilot':'not-started','effectEvidence':'not-run','publication':'closed','contentProduction':'frozen','curriculumCoverage':'unassessed'}, 'Actual evidence boundary')
    require(p['realEvidence'] == [] and p['currentBuild'] is None, 'No real evidence or invented build')
    require(p['time'] == mod['time'] and p['products'] == mod['products'] and p['curriculum'] == mod['curriculum'], 'Exact MOD time/product/curriculum binding')
    segments = {s['id']:s for s in p['time']['segments']}
    require(len(segments) == 22, '22 unique segments')
    totals = Counter()
    meetings = Counter()
    for s in segments.values():
        require(type(s['minutes']) is int and s['minutes'] > 0, 'Positive whole minutes')
        totals[s['component']] += s['minutes']
        meetings[s['meeting']] += s['minutes']
    require(dict(totals) == p['time']['components'] and sum(totals.values()) == 225, 'R5 functional budgets')
    require(meetings == Counter({i:45 for i in range(1,6)}), 'Five 45-minute meetings')
    require([(r['id'],r['minutes'],r['actualState']) for r in p['runs']] == [('exploratory',225,'not-started'),('confirmation',225,'not-started')], 'New run binding')
    require(p['runs'][1]['context'] == 'different-class-after-review' and p['buildBinding']['legacy270PathAllowed'] is False, 'No legacy confirmation shortcut')
    require({t['id'] for t in p['tracks']} == {'TECH','USE','TEACH','REVIEW'} and all(t['actualResult']=='not-run' for t in p['tracks']), 'Four separate unrun tracks')
    technical = p['technicalChecks']
    usage = p['usageChecks']
    observations = p['observations']
    require(len(technical)==11 and len(usage)==5 and len(observations)==12, 'Instrument coverage')
    ids = [x['id'] for x in technical+usage+observations+p['otherInstruments']]
    require(len(ids)==len(set(ids)), 'Unique instrument ids')
    require({f for t in technical for f in t['findingIds']} == {f'TECH-F{i:02d}' for i in range(1,9)}, 'All eight open TECH findings')
    products = {x['id'] for x in p['products']}
    for o in observations:
        require(set(o['productIds']) <= products and set(o['segmentIds']) <= set(segments), 'Observation references')
        require(o['minimumOpportunities']==2 and o['recording']=='combined-category-only' and o['actualResult']=='not-run', 'Observation boundary')
        require(set(o['productIds']) <= {pid for sid in o['segmentIds'] for pid in segments[sid]['productIds']}, 'Products occur in observation windows')
    require({g['gateId'] for g in p['experienceGates']} == {g['gateId'] for g in mod['gateReview']} and len(p['experienceGates'])==12, 'All twelve LXF gates')
    for g in p['experienceGates']:
        require(g['instrumentIds'] and set(g['instrumentIds']) <= set(ids), 'Gate instrument references')
        require(g['realEvidence']=='not-run' and g['state']=='specified-for-user-review', 'Gates not executed')
    profile = read(ROOT / 'roadmap/v2/foundations/learning-experience/learner-profile.json')
    expected = {q['id']:q['question'] for d in profile['dimensions'] for q in d['pilotQuestions']}
    require({q['id']:q['question'] for q in p['profileQuestions']} == expected, 'Eight exact LXF03 questions')
    for q in p['profileQuestions']:
        require(set(q['instrumentIds']) <= set(ids) and q['status']=='operationalized-not-answered' and q['gradeScope']==[5], 'Profile scope')
    threshold = p['thresholds']
    require(threshold['status']=='project-defined-not-empirically-validated' and threshold['criticalEventsToStop']==1 and threshold['observationOpportunities']==2, 'Threshold provenance')
    require(threshold['pulseCountsStored'] is False and threshold['pulseAnswersStored'] is False and threshold['pulseMinimumResponses'] is None, 'No pulse dataset')
    require(len(p['dataClasses'])==8 and len({d['id'] for d in p['dataClasses']})==8, 'Data classes')
    require(all(d.get('workspaceAllowed') is False for d in p['dataClasses'] if d['realDataAllowed']), 'Real data stays outside workspace')
    require(p['dataDecision']['state']=='proposed-not-institutionally-approved' and p['dataDecision']['personalDataInRepositoryVaultOrWorkspace'] is False, 'No invented institutional approval')
    require(all(e['status']=='open' for e in p['entryConditions']) and len(p['entryConditions'])==8, 'Actual entry conditions remain open')
    require(all(p['decisionBoundary'][key] is False for key in ['authorizesUse','authorizesPublication','effectClaimAllowed','automaticStatusMutation']), 'No automatic permission')
    for t in p['tracks']+technical+usage+p['otherInstruments']:
        require((HERE/t['instrument']).is_file(), 'Instrument file exists')

bindings = read(HERE / 'input-bindings.json')
require(bindings['inputCommit']==BASE and len(bindings['inputs'])==25, 'Input binding identity')
for item in bindings['inputs']:
    path = item['path']
    raw = (ROOT/path).read_bytes()
    old = subprocess.run(['git','show',BASE+':'+path],cwd=ROOT,capture_output=True,check=True).stdout
    require(digest(raw)==item['checkoutSha256'] and digest(old)==item['gitBlobSha256'], 'Input digest: '+path)
    require(raw.replace(b'\r\n',b'\n')==old.replace(b'\r\n',b'\n'), 'Unchanged historical input: '+path)
checks.append({'id':'input-integrity','result':'passed','count':25})

acceptance = read(ROOT/protocol['modAcceptancePath'])
require(acceptance['state']=='approved-by-user' and acceptance['acceptedCommit']==BASE and acceptance['fulfilledCondition']=='MOD-DESIGN' and acceptance['implementationAuthorized'] is False, 'MOD acceptance only')
require(set(acceptance['remainingConditions'])=={'MOD-TECH','MOD-LANGUAGE','MOD-CONTEXT','MOD-GOV','MOD-PILOT'}, 'MOD real gates preserved')
tech_acceptance = read(ROOT/protocol['technicalAcceptancePath'])
require(tech_acceptance['state']=='approved-by-user' and len(tech_acceptance['openFindings'])==8 and tech_acceptance['repairsAuthorized'] is False, 'TECH audit boundary')
checks.append({'id':'acceptance-boundaries','result':'passed','count':2})

validate_contract(protocol)
checks.append({'id':'time-products-instruments-gates-data','result':'passed','segments':22,'observations':12,'experienceGates':12,'profileQuestions':8})

def hypothetical_work_result(facts):
    expected = {'criticalIncident','bindingValid','requiredEvidenceComplete','materiallyOpenFinding','coreActionsComplete','withinMeetingBudgets','ownExecutableP3','confirmationComplete','institutionalConditionsComplete'}
    require(set(facts)==expected and all(type(v) is bool for v in facts.values()), 'Closed synthetic fact vocabulary')
    if facts['criticalIncident'] or facts['materiallyOpenFinding'] or not all(facts[k] for k in ['coreActionsComplete','withinMeetingBudgets','ownExecutableP3']):
        return 'revise-required'
    if not all(facts[k] for k in ['bindingValid','requiredEvidenceComplete','confirmationComplete','institutionalConditionsComplete']):
        return 'not-evaluable'
    return 'ready-for-human-review'

scenarios = read(HERE/'decision-scenarios.synthetic.json')
require(scenarios['evidenceKind']=='synthetic' and scenarios['realParticipants']==0, 'Synthetic evidence only')
require(len(scenarios['cases'])==12 and len({c['id'] for c in scenarios['cases']})==12, 'Twelve unique scenarios')
scenario_results=[]
for case in scenarios['cases']:
    actual = hypothetical_work_result(case['facts'])
    require(actual==case['expectedHypotheticalWorkResult'], 'Scenario: '+case['id'])
    require(case['actualEvidenceUsability']=='synthetic-only' and all(case[k] is False for k in ['authorizesUse','authorizesPublication','effectClaimAllowed']), 'Scenario cannot authorize use')
    scenario_results.append({'id':case['id'],'simulatedWorkResult':actual,'realEvidenceUsability':'synthetic-only'})
checks.append({'id':'synthetic-decision-counterexamples','result':'passed','count':12})

# Negative changes happen only in memory: protect against silent time drift,
# omitted gates, maturity promotion, data collection and ambiguous fact types.
mutations = [
    ('time-drift',lambda p:p['time']['segments'][0].update(minutes=11)),
    ('missing-gate',lambda p:p['experienceGates'].pop()),
    ('invented-real-pass',lambda p:p['actualState'].update(technicalTargetChecks='passed')),
    ('permission-promotion',lambda p:p['decisionBoundary'].update(authorizesUse=True)),
    ('pulse-data',lambda p:p['thresholds'].update(pulseAnswersStored=True)),
]
for label,change in mutations:
    altered=copy.deepcopy(protocol)
    change(altered)
    try:
        validate_contract(altered)
    except ValueError:
        continue
    raise ValueError('Negative mutation accepted: '+label)
bad=copy.deepcopy(scenarios['cases'][0]['facts'])
bad['criticalIncident']='false'
try:
    hypothetical_work_result(bad)
except ValueError:
    pass
else:
    raise ValueError('String boolean accepted')
checks.append({'id':'negative-mutations-rejected','result':'passed','count':6})

links=0
for path in HERE.glob('*.md'):
    text=path.read_text(encoding='utf-8')
    require('\ufffd' not in text, 'No replacement characters: '+path.name)
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if target.startswith(('https://','http://','#')):
            continue
        require((path.parent/target.split('#')[0]).resolve().exists(), 'Local link: '+path.name+' -> '+target)
        links+=1
checks.append({'id':'local-links','result':'passed','count':links})

changed=subprocess.run(['git','diff','--name-only',BASE,'--'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
untracked=subprocess.run(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
allowed_prefix='roadmap/v2/follow-ups/pilot/'
allowed_acceptance='roadmap/v2/follow-ups/reference-module/acceptance.json'
require(all(p.startswith(allowed_prefix) or p==allowed_acceptance for p in changed+untracked), 'No out-of-scope repository mutation')
checks.append({'id':'repository-scope','result':'passed'})

artifacts={p.name:digest(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in {'validation.json','validation-report.md','work-plan.md'}}
report={'schemaVersion':1,'checkedAt':datetime.now(timezone.utc).isoformat(),'inputCommit':BASE,'result':'passed','checks':checks,'syntheticScenarios':scenario_results,'artifactSha256':artifacts,'claimBoundary':'Only this specification packet and synthetic decision examples checked; no V2 runtime, real devices, learner use or pilot verified.'}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'FU-PILOT: {len(checks)} check groups passed; 12 synthetic scenarios, 6 negative mutations, {links} local links. No real pilot evidence.')
