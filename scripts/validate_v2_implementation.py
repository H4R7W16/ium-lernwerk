"""Validate authorized development separately from the unchanged activation seals.

No approval is produced here. User statements are recorded evidence, not a
cryptographic authentication mechanism. Historical code runs in a separate
process against materialized Git inputs; current changes use an exact allowlist.
"""
import argparse
from contextlib import contextmanager
from datetime import date
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PLAN_COMMIT='a702deaaafba464e2035f5be6d919bd30a9f4855'
HISTORICAL_COMMIT='150deea22ba9bcf3170915bb4b24852d376f6a8b'
PLAN='roadmap/v2/implementation-planning/plan.json'
AUTHORIZATION='roadmap/v2/implementation/authorization.json'
CHANGE_PLAN='roadmap/v2/implementation/change-plan.json'
PROGRESS='roadmap/v2/implementation/progress.json'
SCHEMA='schemas/v2/implementation.schema.json'
POINTER='roadmap/v2/cutover/active-baseline.json'
LIMITS=dict(contentProduction='frozen',curriculum='unassessed',usage='not-started',pilot='not-started',
            publication='closed',push='not-authorized',merge='not-authorized',lxp05='frozen-unmerged')
FOLLOW_UPS=[('technical','IUM-V2-FU-TECH','technical-inventory-and-migration-audit'),
            ('reference-module','IUM-V2-FU-MOD','reference-module-design'),
            ('pilot','IUM-V2-FU-PILOT','pilot-instrument-specification')]
PLAN_TASK='60_Organisation/Workspace-Entwicklung/Tasks/2026-09-07 - IUM-V2-PLAN Referenzmodul-Implementierung planen.md'
FU_TASKS={
 'IUM-V2-FU-TECH':'2026-09-06 - IUM-V2-FU-TECH Technische V1-Bausteine gegen V2 prüfen.md',
 'IUM-V2-FU-MOD':'2026-09-06 - IUM-V2-FU-MOD Erstes V2-Referenzmodul spezifizieren.md',
 'IUM-V2-FU-PILOT':'2026-09-06 - IUM-V2-FU-PILOT Prüf- und Pilotinstrumente an V2 binden.md'}


class ImplementationError(ValueError):
    pass


def require(condition,message):
    if not condition:raise ImplementationError(message)


def digest(data):
    return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()


def safe_path(value):
    require(isinstance(value,str) and value and not re.search(r'[\\:\x00-\x1f\x7f?#%]',value), 'Unsicherer Entwicklungspfad')
    require(not PurePosixPath(value).is_absolute() and not any(x in {'','.','..'} for x in value.split('/')), 'Unsicherer Entwicklungspfad')
    return value


def file_at(root,path):
    file=root/safe_path(path)
    require(file.resolve().is_relative_to(root.resolve()), 'Datei außerhalb des erlaubten Bereichs')
    return file


def _pairs(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Doppeltes JSON-Feld: '+key);result[key]=value
    return result


def parse(data):
    return json.loads(data,object_pairs_hook=_pairs,parse_constant=lambda _: (_ for _ in ()).throw(ImplementationError('Nicht endlicher JSON-Wert')))


def read(repo,path):
    return parse(file_at(repo,path).read_text(encoding='utf-8-sig'))


def git(repo,*args,input=None):
    return subprocess.check_output(['git',*args],cwd=repo,input=input,stderr=subprocess.PIPE)


def commit(repo,value):
    require(isinstance(value,str) and re.fullmatch('[a-f0-9]{40}',value),'Vollständiger Commit fehlt')
    require(git(repo,'rev-parse',value+'^{commit}').decode().strip()==value,'Kein Commitobjekt')
    git(repo,'merge-base','--is-ancestor',value,'HEAD')
    return value


def blobs(repo,revision,paths):
    """One Git process, strict blob framing; never extract paths from an archive."""
    names=list(paths)
    requests=''.join(revision+':'+safe_path(p)+'\n' for p in names).encode()
    stream=io.BytesIO(git(repo,'cat-file','--batch',input=requests))
    result={}
    for path in names:
        header=stream.readline().split()
        require(len(header)==3 and header[1]==b'blob','Historischer Blob fehlt: '+path)
        size=int(header[2]);content=stream.read(size)
        require(len(content)==size and stream.read(1)==b'\n','Ungültige Git-Blobantwort')
        result[path]=content
    return result


@contextmanager
def historical_view(repo):
    commit(repo,HISTORICAL_COMMIT)
    pointer=parse(git(repo,'show',HISTORICAL_COMMIT+':'+POINTER))
    paths=set(pointer['inputDigests'])|{POINTER,'roadmap/v2/cutover/review.json'}
    contents=blobs(repo,HISTORICAL_COMMIT,sorted(paths))
    with tempfile.TemporaryDirectory(prefix='ium-activation-history-') as directory:
        root=Path(directory)
        for name,data in contents.items():
            file=file_at(root,name);file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(data)
        yield root


def _historical_worker(repo,view,vault,overrides):
    # Only this child imports the historical modules. Current module objects are
    # never monkeypatched in the parent/test process.
    sys.path.insert(0,str(view/'scripts'))
    import validate_v2_activation as activation
    import validate_v2_cutover as cutover
    def historical_git(_repo,*args):
        require(args and args[0] in {'show','rev-parse','merge-base'},'Historischer Git-Befehl nicht lesend')
        # HEAD in historical checks denotes the accepted checkpoint, not today's branch.
        return git(repo,*(HISTORICAL_COMMIT if x=='HEAD' else x for x in args))
    activation.git=cutover.git=historical_git
    activation.ROOT=cutover.ROOT=view
    return activation.validate(view,vault=vault,**overrides)


def validate_historical_view(repo,view,*,vault=None,decision=None,pointer=None):
    options={k:v for k,v in dict(decision=decision,pointer=pointer).items() if v is not None}
    args=[sys.executable,'-B',str(Path(__file__).resolve()),'--historical-worker',str(repo.resolve()),str(view.resolve())]
    if vault:args+=['--vault',str(vault.resolve())]
    result=subprocess.run(args,input=json.dumps(options).encode(),capture_output=True)
    require(result.returncode==0,'Historische Aktivierung ungültig: '+result.stderr.decode('utf-8',errors='replace').strip())
    return parse(result.stdout)


def validate_historical_activation(repo,*,vault=None,decision=None,pointer=None):
    with historical_view(repo) as view:
        return validate_historical_view(repo,view,vault=vault,decision=decision,pointer=pointer)


def schema_check(value,node,schema,path='$'):
    """Small explicit subset used by this closed schema; unsupported keywords fail."""
    supported={'$ref','type','const','enum','anyOf','properties','required','additionalProperties','items','minItems','uniqueItems','minLength','pattern','minimum'}
    require(set(node)<=supported,'Nicht unterstütztes Schemawort: '+str(set(node)-supported))
    if '$ref' in node:
        require(node['$ref'].startswith('#/$defs/'),'Externes Schema verboten')
        return schema_check(value,schema['$defs'][node['$ref'].split('/')[-1]],schema,path)
    if 'anyOf' in node:
        for alternative in node['anyOf']:
            try:schema_check(value,alternative,schema,path);return
            except ImplementationError:pass
        raise ImplementationError(path+': kein erlaubter Datentyp')
    if 'const' in node:
        require(type(value) is type(node['const']) and value==node['const'],path+': falscher Konstantwert')
    if 'enum' in node:require(value in node['enum'],path+': unbekannter Status')
    checks={'object':lambda:type(value) is dict,'array':lambda:type(value) is list,'string':lambda:type(value) is str,'integer':lambda:type(value) is int,'null':lambda:value is None}
    if 'type' in node:require(node['type'] in checks and checks[node['type']](),path+': falscher Typ')
    if type(value) is dict and 'properties' in node:
        require(set(node['required'])<=set(value) and (node.get('additionalProperties') is not False or set(value)<=set(node['properties'])),path+': Felder fehlen oder unbekannt')
        for k,v in value.items():schema_check(v,node['properties'][k],schema,path+'.'+k)
    if type(value) is list:
        require(len(value)>=node.get('minItems',0),path+': unvollständige Liste')
        if node.get('uniqueItems'):require(len({json.dumps(x,sort_keys=True) for x in value})==len(value),path+': doppelte Einträge')
        if 'items' in node:
            for item in value:schema_check(item,node['items'],schema,path+'[]')
    if type(value) is str:
        require(len(value.strip())>=node.get('minLength',0),path+': leerer Text')
        if 'pattern' in node:require(re.search(node['pattern'],value) is not None,path+': ungültiges Format')
    if type(value) is int and 'minimum' in node:require(value>=node['minimum'],path+': Wert zu klein')


def validate_change_plan(plan,*,allowed_files):
    require(type(plan) is dict and set(plan)=={'schemaVersion','packageId','files','dependsOn'},'Paketfelder fehlen oder unbekannt')
    require(type(plan['schemaVersion']) is int and plan['schemaVersion']==1,'Unbekannte Paketversion')
    require(type(plan['packageId']) is str and re.fullmatch('IMP0[1-8]',plan['packageId']),'Unbekanntes Paket')
    require(type(plan['files']) is list and plan['files'],'Leere Dateiliste')
    checked=[safe_path(p) for p in plan['files']]
    require(len(checked)==len(set(checked)) and set(checked)<=allowed_files,'Nicht autorisierter Entwicklungspfad')
    require(type(plan['dependsOn']) is list and all(type(p) is str for p in plan['dependsOn']),'Ungültige Abhängigkeiten')
    require(len(set(plan['dependsOn']))==len(plan['dependsOn']),'Doppelte Abhängigkeit')
    return plan


def _date(value):
    require(date.fromisoformat(value).isoformat()==value and date.fromisoformat(value)<=date.today(),'Ungültiges/Zukünftiges Entscheidungsdatum')


def _authorization(repo,auth,spec):
    require(auth['acceptedPlanCommit']==PLAN_COMMIT,'Nicht angenommener Plancommit')
    commit(repo,auth['acceptedPlanCommit'])
    require(auth['planAcceptance']==dict(state='approved-by-user',decisionBy='user',date='2026-09-08',statement='Der Plan ist angenommen.'),'Planannahme verändert')
    require(auth['limits']==LIMITS,'Einsatzgrenzen verändert')
    first=auth['requests'][0]
    require(first['id']=='IUM-V2-IMP01-2026-09-08' and first['date']=='2026-09-08'
            and first['statement']=='Führe IUM-V2-IMP01 jetzt aus.' and first['packageIds']==['IMP01'],'Erster Umsetzungsauftrag verändert')
    selected=[];optional=set();request_ids=set()
    previous_date=auth['planAcceptance']['date']
    for request in auth['requests']:
        _date(request['date']);require(request['date']>=previous_date,'Aufträge zeitlich umsortiert');previous_date=request['date']
        require(request['id'] not in request_ids,'Doppelter Auftrag');request_ids.add(request['id'])
        candidates={path for p in spec['packages'] if p['id'] in request['packageIds'] for path in p.get('optionalModify',{})}
        for change in request['optionalChanges']:
            path=safe_path(change['path']);require(path in candidates and path not in optional,'Optionale Änderung ohne passenden Auftrag');optional.add(path)
        selected+=request['packageIds']
    require(selected==['IMP%02d'%i for i in range(1,len(selected)+1)] and len(selected)<=8,'Nicht sequenzielle oder doppelte Paketautorisierung')
    # Once committed, earlier requests are immutable; future requests are appended.
    names=git(repo,'ls-tree','-r','--name-only','HEAD','--',AUTHORIZATION).decode().splitlines()
    if names:
        previous=parse(git(repo,'show','HEAD:'+AUTHORIZATION))
        require(auth['requests'][:len(previous['requests'])]==previous['requests'],'Historischen Auftrag überschrieben')
    return selected,optional


def package_digest(repo,package,*,revision=None):
    paths=[p for p in package['files'] if p!=PROGRESS]
    if revision:
        tree=set(git(repo,'ls-tree','-r','--name-only',revision).decode().splitlines())
        values=blobs(repo,revision,[p for p in paths if p in tree])
    else:values={p:file_at(repo,p).read_bytes() for p in paths if file_at(repo,p).is_file()}
    # Include absence as well as content, including optional existing files.
    manifest=[[p,digest(values[p]) if p in values else None] for p in sorted(paths)]
    return digest(json.dumps(manifest,separators=(',',':')).encode())


def _progress(repo,data,packages,authorized):
    require(data['limits']==LIMITS,'Fortschritt überschreitet Einsatzgrenzen');_date(data['updated'])
    require([p['id'] for p in data['packages']]==[p['packageId'] for p in packages],'Acht Fortschrittseinträge fehlen/umgeordnet')
    result=[]
    for index,(entry,package) in enumerate(zip(data['packages'],packages)):
        state=entry['state'];candidate=entry['candidateCommit'];checks=entry['checks'];approval=entry['acceptance']
        require(state=='planned' or entry['id'] in authorized,'Nicht autorisierte Paketarbeit')
        if state!='planned' and index:require(data['packages'][index-1]['state']=='done','Vorgänger noch nicht angenommen')
        if candidate:commit(repo,candidate)
        if state=='planned':require(not checks and candidate is None and approval is None,'Unbegonnenes Paket mit Erfolgsbeleg')
        if approval:
            require(state=='done' and approval['acceptedCommit']==candidate,'Paketabnahme ohne passenden Kandidaten')
            _date(approval['date']);commit(repo,approval['acceptedCommit'])
        require(state!='done' or approval is not None,'done benötigt Nutzerabnahme')
        current_digest=package_digest(repo,package)
        tested_digest=package_digest(repo,package,revision=candidate) if candidate else current_digest
        for check in checks:
            commit(repo,check['baseCommit'])
        require(len({c['id'] for c in checks})==len(checks),'Doppelte Prüfevidenz')
        passed=bool(checks) and all(c['exitCode']==0 and c['treeDigest']==tested_digest for c in checks)
        if state in {'review','done'}:require(passed,'Review/Abschluss ohne passende erfolgreiche Prüfungen')
        if state=='review':require(tested_digest==current_digest,'Reviewkandidat seit Prüfung verändert')
        result.append(dict(entry,authorized=entry['id'] in authorized,technicalState='passed' if passed else 'failed' if any(c['exitCode'] for c in checks) else 'stale' if checks else 'not-run',currentTreeDigest=current_digest))
    return result


def _vault_status(vault,path,allowed,*,contains=()):
    note=file_at(vault,path).read_text(encoding='utf-8-sig')
    match=re.match(r'^---\r?\n([\s\S]*?)\r?\n---',note);require(match,'Task-Frontmatter fehlt: '+path)
    front=match[1]
    statuses=re.findall(r'^status:\s*(\S+)\s*$',front,re.M)
    owners=re.findall(r'^owner_agent:\s*(\S+)\s*$',front,re.M)
    require(len(statuses)==1 and statuses[0] in allowed and owners==['Codex'],'Widersprüchlicher Vault-Task: '+path)
    require(all(text in note for text in contains),'Entscheidungsbeleg im Vault fehlt: '+path)


def _validate(repo,authorization,vault):
    spec=parse(git(repo,'show',PLAN_COMMIT+':'+PLAN))
    schema=read(repo,SCHEMA)
    auth=read(repo,AUTHORIZATION) if authorization is None else authorization
    change=read(repo,CHANGE_PLAN);progress=read(repo,PROGRESS)
    for name,value in [('authorization',auth),('changePlan',change),('progress',progress)]:
        schema_check(value,schema['$defs'][name],schema,name)
    require(authorization is None or auth==read(repo,AUTHORIZATION),'Autorisierung weicht vom aufgezeichneten Auftrag ab')
    authorized,optional=_authorization(repo,auth,spec)
    require(change['acceptedPlanCommit']==PLAN_COMMIT and change['historicalActivationCommit']==HISTORICAL_COMMIT,'Changeplan nicht an Eingänge gebunden')
    expected=[dict(schemaVersion=1,packageId=p['id'],files=p['create']+p['modify']+list(p.get('optionalModify',{})),dependsOn=p['dependsOn']) for p in spec['packages']]
    require(change['packages']==expected and change['sharedStatusFiles']==spec['sharedStatusFiles'],'Dateiliste/Abhängigkeiten weichen vom angenommenen Plan ab')
    allowed=set(spec['sharedStatusFiles'])
    for p,package in zip(spec['packages'],change['packages']):
        validate_change_plan(package,allowed_files=set(package['files']))
        if p['id'] in authorized:allowed.update(p['create']+p['modify']);allowed.update(set(p.get('optionalModify',{}))&optional)
    diff=git(repo,'diff','--name-status','--no-renames','-z',PLAN_COMMIT,'--').decode().split('\0')
    changes=[]
    for index in range(0,len(diff)-1,2):
        status,path=diff[index:index+2];safe_path(path)
        require(status in {'A','M'},'Löschung oder Typänderung nicht autorisiert: '+path)
        require(path in allowed,'Nicht autorisierte Änderung: '+path);changes.append(path)
    for path in filter(None,git(repo,'ls-files','--others','--exclude-standard','-z').decode().split('\0')):
        safe_path(path);require(path in allowed,'Nicht autorisierte neue Datei: '+path);changes.append(path)
    for path in allowed:
        if (repo/path).exists():file_at(repo,path)
    bindings=parse(git(repo,'show',PLAN_COMMIT+':roadmap/v2/implementation-planning/input-bindings.json'))
    pointer=parse(git(repo,'show',HISTORICAL_COMMIT+':'+POINTER))
    protected=set(pointer['inputDigests'])|{POINTER}|{d['path'] for d in bindings['inputs']+bindings['planningDocuments']}
    protected.update(git(repo,'ls-tree','-r','--name-only',PLAN_COMMIT,'--','roadmap/v2/implementation-planning').decode().splitlines())
    originals=blobs(repo,PLAN_COMMIT,sorted(protected-allowed))
    for path,original in originals.items():
        require(digest(file_at(repo,path).read_bytes())==digest(original),'Geschützter Eingabedigest verändert: '+path)
    # Exact immutable FU records at the accepted plan include the PILOT approval.
    followups=[]
    for folder,task_id,scope in FOLLOW_UPS:
        path=f'roadmap/v2/follow-ups/{folder}/acceptance.json'
        approval=read(repo,path)
        require(approval==parse(git(repo,'show',PLAN_COMMIT+':'+path)),'FU-Annahme seit Planannahme verändert')
        require(approval['taskId']==task_id and approval['scope']==scope and approval['state']=='approved-by-user' and approval['decisionBy']=='user','Falscher FU-Abnahmevertrag')
        require(approval['pilot']=='not-started' and approval['publication']=='closed','Instrumentenannahme ist kein Pilot')
        commit(repo,approval['acceptedCommit']);followups.append(approval)
    state=_progress(repo,progress,change['packages'],authorized)
    if vault:
        _vault_status(vault,PLAN_TASK,{'done'},contains=[PLAN_COMMIT,auth['planAcceptance']['statement'],auth['requests'][0]['statement']])
        for entry,p in zip(state,spec['packages']):
            _vault_status(vault,p['taskPath'],{'blocked','planned'} if entry['state']=='planned' else {entry['state']})
        for a in followups:
            _vault_status(vault,'60_Organisation/Workspace-Entwicklung/Tasks/'+FU_TASKS[a['taskId']],{'done'},contains=[a['acceptedCommit']])
    historical=validate_historical_activation(repo,vault=vault)
    return dict(historicalActivation=historical,followUps=followups,development=dict(
        acceptedPlanCommit=PLAN_COMMIT,historicalActivationCommit=HISTORICAL_COMMIT,
        authorizedPackages=authorized,packages=state,limits=LIMITS,
        changedFiles=sorted(set(changes)),vaultEvidence='task-records-checked' if vault else 'not-checked'))


def validate(repo,*,authorization=None,vault=None):
    try:return _validate(Path(repo).resolve(),authorization,Path(vault).resolve() if vault else None)
    except ImplementationError:raise
    except (OSError,ValueError,KeyError,TypeError,IndexError,subprocess.CalledProcessError) as error:
        raise ImplementationError('Entwicklungsvertrag ungültig oder nicht lesbar: '+str(error)) from error


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault',type=Path)
    parser.add_argument('--json',action='store_true')
    parser.add_argument('--historical-only',action='store_true',help='Nur die unveränderte historische Aktivierung prüfen')
    parser.add_argument('--historical-worker',nargs=2,metavar=('REPO','VIEW'),help=argparse.SUPPRESS)
    args=parser.parse_args()
    try:
        if args.historical_worker:
            repo,view=map(Path,args.historical_worker)
            result=_historical_worker(repo,view,args.vault,parse(sys.stdin.buffer.read()))
        elif args.historical_only:result=validate_historical_activation(ROOT,vault=args.vault)
        else:result=validate(ROOT,vault=args.vault)
        if args.json or args.historical_worker:
            sys.stdout.buffer.write((json.dumps(result,ensure_ascii=False)+'\n').encode('utf-8'))
        elif args.historical_only:print('Historische V2-Aktivierung an '+HISTORICAL_COMMIT+' gültig; aktueller Entwicklungsstand separat.')
        else:print('V2-Entwicklungsvertrag gültig: historische Aktivierung erhalten; autorisiert: '+', '.join(result['development']['authorizedPackages'])+'. Nutzung, Pilot und Veröffentlichung bleiben geschlossen.')
    except (ImplementationError,OSError,ValueError,KeyError,TypeError,subprocess.CalledProcessError) as error:
        sys.stderr.buffer.write(('V2-Entwicklungsprüfung fehlgeschlagen: '+str(error)+'\n').encode('utf-8'));sys.exit(1)
