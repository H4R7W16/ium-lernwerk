'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const M = require('./work-overview-model.js');
const now = '2026-11-06T10:00:00.000Z';
const id = '00000000-0000-4000-8000-000000000001';
const id2 = '00000000-0000-4000-8000-000000000002';
const id3 = '00000000-0000-4000-8000-000000000003';
const catalog = {grade:7, version:1, areas:['medien','daten','programmieren','gaming'].map(id=>({id,name:id,path:id+'/index.html'})),tasks:[{id:'dat-1',area:'daten',title:'Daten untersuchen',path:'dat/dat-1.html',places:[{id:'',title:'Ganze Aufgabe'},{id:'auswerten',title:'Auswerten'}]},{id:'alg-5',area:'programmieren',title:'Eigenes Projekt',path:'alg/alg-5.html',places:[{id:'',title:'Ganze Aufgabe'}]}]};
const location = {kind:'heft',hint:'Seite 9',filename:''};
function add(store=M.empty(), options={}) {return M.save(store,{taskId:'dat-1',place:'auswerten',locations:[location],next:'Vergleiche die Häufigkeiten.',inheritAreaHint:false,...options},catalog,{id,now});}

test('DAT-1 card retains safe snapshot, working location and next action without mutating input',()=>{const before=M.empty();const r=add(before);assert.equal(r.ok,true);assert.equal(before.cards.length,0);assert.equal(r.card.title,'Daten untersuchen');assert.equal(r.card.placeTitle,'Auswerten');assert.equal(M.resolve(r.card,catalog).target,'dat/dat-1.html#auswerten');assert.equal(r.card.next,'Vergleiche die Häufigkeiten.');});
test('area hints are live internally and materialized as local locations on export/import',()=>{let s=add(undefined,{inheritAreaHint:true}).store;s=M.save(s,{taskId:'dat-1',place:'',locations:[{kind:'heft',hint:'Seite 12',filename:''}],next:'',inheritAreaHint:true},catalog,{id:id2,now}).store;assert.equal(M.effectiveLocations(s,s.cards[0])[0].hint,'Seite 12');const result=M.parseFile(M.exportFile(s,catalog,now),catalog);assert.equal(result.ok,true);assert.equal(result.cards[0].locations[0].hint,'Seite 12');assert.equal(result.cards[0].inheritAreaHint,false);});
test('import selected cards adds only selection and does not replace by default or alter area hints',()=>{const s=add(undefined,{inheritAreaHint:true}).store;const cards=M.parseFile(M.exportFile(s,catalog,now),catalog).cards;const r=M.applyImport(s,cards,[{sourceId:id,mode:'add',newId:id2}],catalog,now);assert.equal(r.ok,true);assert.equal(r.store.cards.length,2);assert.equal(r.store.cards[1].id,id2);assert.equal(r.store.cards[1].importedAt,now);assert.equal(r.store.cards[1].inheritAreaHint,false);assert.deepEqual(r.store.areaHints,s.areaHints);assert.deepEqual(M.applyImport(s,cards,[],catalog,now).store,s);});
test('targeted replacement only accepts same task and preserves target identity',()=>{let s=add().store;s=M.save(s,{taskId:'alg-5',place:'',locations:[],next:'XML öffnen',inheritAreaHint:false},catalog,{id:id2,now}).store;const cards=M.parseFile(M.exportFile(add().store,catalog,now),catalog).cards;const invalid=M.applyImport(s,cards,[{sourceId:id,mode:'replace',targetId:id2}],catalog,now);assert.equal(invalid.ok,false);assert.equal(s.cards[1].next,'XML öffnen');const valid=M.applyImport(s,cards,[{sourceId:id,mode:'replace',targetId:id}],catalog,now);assert.equal(valid.ok,true);assert.equal(valid.store.cards[0].id,id);});
test('old tasks and places survive import as data and resolve only through catalog',()=>{const file=JSON.parse(M.exportFile(add().store,catalog,now));file.cards[0].taskId='dat-99';file.cards[0].title='<img src=x onerror=alert(1)>';const parsed=M.parseFile(JSON.stringify(file),catalog);assert.equal(parsed.ok,true);assert.equal(M.resolve(parsed.cards[0],catalog).target,'daten/index.html');assert.equal(M.resolve(parsed.cards[0],catalog).missingTask,true);file.cards[0].taskId='dat-1';file.cards[0].place='old-place';const card=M.parseFile(JSON.stringify(file),catalog).cards[0];assert.equal(M.resolve(card,catalog).target,'dat/dat-1.html');assert.equal(M.resolve(card,catalog).missingPlace,true);});
test('foreign grade, format, executable URL fields, duplicates and unknown fields reject entire file',()=>{const base=JSON.parse(M.exportFile(add().store,catalog,now));for (const mutate of [f=>f.grade=6,f=>f.format='foreign',f=>f.extra=true,f=>f.cards[0].url='javascript:alert(1)',f=>f.cards[0].place='https://bad.test',f=>f.cards.push({...f.cards[0]}),f=>f.cards[0].area='alg',f=>f.cards[0].locations[0].url='file:///c:/x',f=>f.cards[0].inheritAreaHint=true]) {const f=structuredClone(base);mutate(f);assert.equal(M.parseFile(JSON.stringify(f),catalog).ok,false,JSON.stringify(f));}});
test('exact input size limits reject without silent truncation',()=>{for(const options of [{next:'x'.repeat(501)},{locations:[{...location,hint:'x'.repeat(301)}]},{locations:[{...location,filename:'x'.repeat(161)}]},{locations:Array.from({length:6},()=>location)}]){assert.equal(add(undefined,options).ok,false);}assert.equal(M.parseFile(' '.repeat(M.MAX_BYTES+1),catalog).ok,false);let s=add().store;s.cards=Array.from({length:201},(_,i)=>({...s.cards[0],id:`00000000-0000-4000-8000-${String(i).padStart(12,'0')}`}));assert.equal(M.parseStore(JSON.stringify(s),catalog).ok,false);});
test('invalid storage snapshots and invalid IDs cannot enter model',()=>{const s=add().store;assert.equal(M.parseStore(JSON.stringify({...s,grade:5}),catalog).ok,false);assert.equal(M.save(M.empty(),{taskId:'dat-1',place:'missing',locations:[],next:'',inheritAreaHint:false},catalog,{id,now}).ok,false);assert.equal(M.save(M.empty(),{taskId:'dat-1',place:'',locations:[],next:'',inheritAreaHint:false},catalog,{id:'no-id',now}).ok,false);assert.equal(M.applyImport(s,s.cards,[{sourceId:id,mode:'add',newId:id}],catalog,now).ok,false);});
test('edit and remove preserve unrelated cards and immutable input',()=>{let s=add().store;s=M.save(s,{taskId:'alg-5',place:'',locations:[],next:'Testnotiz',inheritAreaHint:false},catalog,{id:id2,now}).store;const edited=M.save(s,{id,taskId:'dat-1',place:'',locations:[],next:'Neuer Schritt',inheritAreaHint:false},catalog,{id:id3,now});assert.equal(edited.ok,true);assert.equal(edited.store.cards[0].id,id);assert.equal(s.cards[0].next,'Vergleiche die Häufigkeiten.');assert.equal(M.remove(edited.store,id).cards[0].id,id2);});

const xml = '<project name="Mein Rover" app="Snap!" version="1"><notes>Eigene Arbeit</notes><stage name="Stage"><sprites><sprite name="Rover"><scripts/></sprite></sprites></stage></project>';
function project(value=xml) { return {format:'snap-project',version:1,xml:value,filename:'Mein_Rover.xml',savedAt:now}; }
function algStore() { return M.save(add().store,{taskId:'alg-5',place:'',locations:[],next:'Station 60 testen',inheritAreaHint:false},catalog,{id:id2,now}).store; }
test('ALG-5 project survives save, hint edit, export, selected import and targeted replacement',()=>{
 const before=algStore(), result=M.setProject(before,id2,project(),catalog);
 assert.equal(result.ok,true); assert.equal(before.cards[1].project,undefined);
 assert.equal(result.store.version,2); assert.equal(result.card.project.xml,xml);
 const edited=M.save(result.store,{id:id2,taskId:'alg-5',place:'',locations:[],next:'Danach Station 80 testen',inheritAreaHint:false},catalog,{id:id3,now});
 assert.equal(edited.card.project.xml,xml); assert.equal(edited.card.project.savedAt,now);
 const exported=JSON.parse(M.exportFile(edited.store,catalog,now)); assert.equal(exported.version,2);
 const imported=M.parseFile(JSON.stringify(exported),catalog); assert.equal(imported.ok,true);
 const adopted=M.applyImport(before,imported.cards,[{sourceId:id2,mode:'replace',targetId:id2}],catalog,now);
 assert.equal(adopted.ok,true); assert.equal(adopted.store.cards[1].project.xml,xml); assert.deepEqual(adopted.store.cards[0],before.cards[0]);
 const removed=M.removeProject(adopted.store,id2,catalog,now); assert.equal(removed.ok,true); assert.equal(removed.card.project,undefined); assert.equal(adopted.store.cards[1].project.xml,xml);
});
test('v1 files and stores migrate, while v1 project injection and unsupported versions fail',()=>{
 const legacy=add().store; legacy.version=1;
 const parsed=M.parseStore(JSON.stringify(legacy),catalog); assert.equal(parsed.ok,true); assert.equal(parsed.store.version,2); assert.deepEqual(parsed.store.cards,legacy.cards);
 const file=JSON.parse(M.exportFile(algStore(),catalog,now)); file.version=1;
 assert.equal(M.parseFile(JSON.stringify(file),catalog).ok,true);
 file.cards[1].project=project(); assert.equal(M.parseFile(JSON.stringify(file),catalog).ok,false);
 file.version=3; assert.equal(M.parseFile(JSON.stringify(file),catalog).ok,false);
 legacy.cards[0].project=project(); assert.equal(M.parseStore(JSON.stringify(legacy),catalog).ok,false);
});
test('projects only attach to ALG-5 and invalid project input never changes existing state',()=>{
 const base=M.setProject(algStore(),id2,project(),catalog).store, snapshot=JSON.stringify(base);
 assert.equal(M.setProject(base,id,project(),catalog).ok,false);
 for(const invalid of [{...project(),xml:'<project><stage></project>'},{...project(),filename:'../Rover.xml'},{...project(),savedAt:'yesterday'},{...project(),extra:true},{...project(),version:2}]) assert.equal(M.setProject(base,id2,invalid,catalog).ok,false);
 assert.equal(JSON.stringify(base),snapshot);
 const file=JSON.parse(M.exportFile(base,catalog,now)); file.cards[0].project=project(); assert.equal(M.parseFile(JSON.stringify(file),catalog).ok,false);
});
test('project limits and total package limit reject atomically without dropping previous projects',()=>{
 const big='<project><notes>'+('x'.repeat(9*1024*1024))+'</notes><stage/></project>';
 let store=algStore();
 store=M.setProject(store,id2,project(big),catalog).store;
 for(let n=3;n<=4;n++){const nextId='00000000-0000-4000-8000-'+String(n).padStart(12,'0');store=M.save(store,{taskId:'alg-5',place:'',locations:[],next:'',inheritAreaHint:false},catalog,{id:nextId,now}).store;store=M.setProject(store,nextId,project(big),catalog).store;assert.ok(store);}
 const lastId='00000000-0000-4000-8000-000000000005'; store=M.save(store,{taskId:'alg-5',place:'',locations:[],next:'',inheritAreaHint:false},catalog,{id:lastId,now}).store;
 const before=JSON.stringify(store); const refused=M.setProject(store,lastId,project(big),catalog); assert.equal(refused.ok,false); assert.match(refused.error,/32/); assert.equal(JSON.stringify(store),before);
 const oversize=project('<project><stage>'+('x'.repeat(M.MAX_PROJECT_BYTES))+'</stage></project>'); assert.equal(M.validateProject(oversize).ok,false);
});
