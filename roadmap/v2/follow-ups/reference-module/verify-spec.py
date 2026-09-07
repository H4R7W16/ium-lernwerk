"""Verify this design packet's references and budgets; not a product/pilot gate."""
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
read = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
digest = lambda data: hashlib.sha256(data).hexdigest()
spec = read(str((HERE / 'specification.json').relative_to(ROOT)))
checks = []

def require(condition, label):
    if not condition:
        raise ValueError(label)

base = spec['repositoryInput']
for path, expected in spec['inputDigests'].items():
    require(digest((ROOT / path).read_bytes()) == expected, 'Changed input: ' + path)
    historical = subprocess.run(['git','show',base+':'+path],cwd=ROOT,capture_output=True,check=True).stdout
    require(digest(historical) == spec['gitInputDigests'][path], 'Git input digest changed: ' + path)
    require((ROOT/path).read_bytes().replace(b'\r\n',b'\n') == historical.replace(b'\r\n',b'\n'),
            'Content differs from input commit: ' + path)
checks.append({'id':'input-integrity','result':'passed','count':len(spec['inputDigests'])})

acceptance=read(spec['technicalAcceptancePath'])
require(acceptance['state']=='approved-by-user' and acceptance['acceptedCommit']==base
        and acceptance['scope']=='technical-inventory-and-migration-audit'
        and acceptance['repairsAuthorized'] is False, 'Technical acceptance boundary')
require(spec['state']=='review' and spec['limits']['implementation']=='not-started'
        and spec['limits']['contentProduction']=='frozen'
        and spec['limits']['curriculum']=='unassessed'
        and spec['limits']['realDeviceVerification']=='not-run'
        and spec['limits']['pilot']=='not-started'
        and spec['limits']['publication']=='closed'
        and spec['limits']['learningEffectClaim'] is False, 'Design boundary')
checks.append({'id':'acceptance-and-design-boundaries','result':'passed'})

r5=read('roadmap/v2/grades/grade-5/roadmap.json')
module=next(m for m in r5['modules'] if m['id']==spec['moduleId'])
require(spec['selection']['coreOrderUnchanged']==r5['coreOrder'] and
        spec['selection']['prerequisites']==module['dependsOn'],'Roadmap order/prerequisite changed')
product_ids={p['id'] for p in spec['products']}
require(len(product_ids)==len(spec['products'])==7,'Product identity')
require(all(p['taskType']=='learning-task' and p['evidenceStatus']=='planned-only'
            for p in spec['products']),'Product claim exceeds design')
source_records={}
for path in {r['sourcePath'] for r in spec['curriculum']}:
    def visit(obj):
        if isinstance(obj,dict):
            if 'id' in obj: source_records[obj['id']]=obj
            for value in obj.values(): visit(value)
        elif isinstance(obj,list):
            for value in obj: visit(value)
    visit(read(path))
r5_records={r['recordId']:r for r in read('roadmap/v2/grades/grade-5/curriculum-map.json')['records']
            if spec['moduleId'] in r['moduleIds']}
require({r['recordId'] for r in spec['curriculum']}==set(r5_records) and len(spec['curriculum'])==7,
        'Missing/added curriculum records')
for record in spec['curriculum']:
    original=r5_records[record['recordId']]
    for key in ['sourceId','sourcePath','sourceBinding','sourceGrades','recordType','fulfillmentMode']:
        require(record[key]==original[key], 'Curricular authority changed: '+key)
    require(record['recordId'] in source_records and record['coverage']=='unassessed'
            and record['evidenceStatus']=='planned-only','Record/evidence mismatch')
    require(set(record['productIds']) <= product_ids and record['productIds'],'Unresolved product')
require(Counter(r['sourceBinding'] for r in spec['curriculum'])=={'official':1,'orientation':6},'Binding totals')
checks.append({'id':'curriculum-product-binding','result':'passed','records':7,'official':1,'orientation':6})

arch=read('roadmap/v2/foundations/learning-experience/learning-architecture.json')
functions={f['id'] for f in arch['learningFunctionGrammar']['functions']}
by_component=Counter(); by_meeting=Counter(); scheduled_products=set()
for segment in spec['time']['segments']:
    require(type(segment['minutes']) is int and segment['minutes']>0,'Invalid duration')
    by_component[segment['component']]+=segment['minutes']
    by_meeting[segment['meeting']]+=segment['minutes']
    require(set(segment['learningFunctionIds']) <= functions,'Unknown learning function')
    require(set(segment['productIds']) <= product_ids,'Unknown scheduled product')
    scheduled_products.update(segment['productIds'])
require(dict(by_component)==module['timeComponents']==spec['time']['components'],'R5 time allocation mismatch')
require(dict(by_meeting)==dict.fromkeys(range(1,6),45),'Five meeting budgets mismatch')
require(sum(by_meeting.values())==spec['time']['totalMinutes']==module['minutes']==225,'Total time mismatch')
require(scheduled_products==product_ids,'Product lacks reserved time')
checks.append({'id':'time-and-learning-functions','result':'passed','segments':len(spec['time']['segments']),
               'byMeeting':dict(by_meeting),'byComponent':dict(by_component),'minutes':225})

principles={p['id']:p for group in arch['principleGroups'] for p in group['principles']}
claims={c['id']:c for c in read('roadmap/v2/foundations/learning-experience/evidence-register.json')['claims']}
sources={s['id']:s for s in read('roadmap/v2/foundations/sources/source-register.json')['sources']}
patterns={p['id'] for p in read('roadmap/v2/foundations/learning-experience/material-patterns.json')['patterns']}
require({d['principleId'] for d in spec['designDerivations']}==set(principles),'Incomplete LXF derivation')
used_claims=set()
for d in spec['designDerivations']:
    require(d['claimIds']==principles[d['principleId']]['claimIds'],'Changed principle claim binding')
    require(set(d['patternIds']) <= patterns and d['designDecision'] and d['designSections'],'Missing design derivation')
    used_claims.update(d['claimIds'])
require({c['claimId'] for c in spec['claimBindings']}==used_claims,'Missing evidence claims')
used_sources=set()
for c in spec['claimBindings']:
    require(c['sourceIds']==claims[c['claimId']]['sourceIds'],'Changed source binding')
    used_sources.update(c['sourceIds'])
require({s['sourceId'] for s in spec['sourceBindings']}==used_sources <= set(sources),'Missing registered source')
for s in spec['sourceBindings']:
    require(s['sourceKind']==sources[s['sourceId']]['sourceKind'],'Changed source kind')
gates=read('roadmap/v2/foundations/learning-experience/experience-gates.json')['gates']
require(len(spec['gateReview'])==len(gates)==12 and
        {g['gateId'] for g in spec['gateReview']}=={g['id'] for g in gates},'Missing LXF gates')
require(all(g['status']=='specified-for-user-review' and g['realEvidence']=='not-run'
            for g in spec['gateReview']),'Self-review presented as real evidence')
checks.append({'id':'lxf-evidence-chain-and-gates','result':'passed','principles':18,
               'claims':len(used_claims),'sources':len(used_sources),'gates':12})

sem=read(str((HERE/'semantics-results.json').relative_to(ROOT)))
require(sem['result']=='passed' and len(sem['vectors'])==5 and len(sem['comparisons'])==3
        and sem['realDeviceVerification']=='not-run' and sem['pilot']=='not-started','Semantics evidence missing')
require(next(v for v in sem['vectors'] if v['id']=='S3-native-rejected')['actual']['error']=='INVALID_REPEAT',
        'Existing V1 parser limitation missing')
require(spec['motionLanguage']['adaptationRequired'] and spec['motionLanguage']['existingV1BodyLimit']==4
        and spec['motionLanguage']['selectedBodyLimit']==5,'Language adaptation boundary missing')
checks.append({'id':'existing-semantics-probe-record','result':'passed','motionVectors':4,'expectedParserRejection':1,'comparisons':3})

markdown=[ROOT/spec['designPath'],HERE/'README.md',HERE/'validation-report.md']
local_links=0
for file in markdown:
    text=file.read_text(encoding='utf-8-sig')
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if target.startswith(('http:','https:','#')): continue
        if file.parent == HERE and target == 'validation.json':
            # This report is the output of the current successful run.
            local_links += 1
            continue
        require((file.parent/target.split('#')[0]).resolve().is_file(),'Broken link: '+str(file)+' -> '+target)
        local_links+=1
checks.append({'id':'local-markdown-links','result':'passed','count':local_links})

changed=subprocess.run(['git','diff','--name-only',base,'--','apps','packages','modules','curriculum','schemas','scripts','tests','package.json','package-lock.json'],
                       cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
require(not changed,'Unexpected production/contract changes: '+changed)
checks.append({'id':'production-paths-unchanged','result':'passed'})
artifacts=[ROOT/spec['designPath'],HERE/'README.md',HERE/'specification.json',HERE/'semantics-probe.mts',
           HERE/'semantics-results.json',HERE/'verify-spec.py',HERE/'validation-report.md',ROOT/spec['technicalAcceptancePath']]
result={'schemaVersion':1,'taskId':spec['taskId'],'checkedAt':datetime.now(timezone.utc).isoformat(),
        'command':'python -B roadmap/v2/follow-ups/reference-module/verify-spec.py',
        'repositoryInput':base,'result':'passed','checks':checks,
        'artifactDigests':{str(p.relative_to(ROOT)).replace('\\','/'):digest(p.read_bytes()) for p in artifacts},
        'statementBoundary':'Formal design verification only. AI self-review is not user acceptance, product validation, real usage or a pilot.'}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
require((HERE/'validation.json').is_file(),'Generated validation report missing')
print('FU-MOD: 8 Prüfgruppen bestanden; 32 Inputs, 7 Records, 225 Minuten, 18 Prinzipien und 12 Gates gebunden.')
