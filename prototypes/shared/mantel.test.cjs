const test=require('node:test'),assert=require('node:assert/strict');
const M=require('./mantel-model.js');
const unit={id:'IUM-5-CORE-02',version:'1.0.0',area:'quellenquest',steps:[{id:'belege'}],fields:['i:answer'],family:'source'};
const record=()=>M.envelope(unit,{step:'belege',fields:[{key:'i:answer',value:'Meine Erklärung',type:'text'}],tool:{family:'source',answers:{claims:{},transfer:{}},active:{claims:'x',transfer:'y'}}},'11111111-1111-4111-8111-111111111111','2026-10-03T00:00:00.000Z');
test('bestehendes Dateiformat wird validiert; falsche Version und Pflichtfelder abgewiesen',()=>{
const r=record();assert.equal(M.parse(JSON.stringify(r),[unit]).ok,true);
for(const change of [{formatVersion:2},{moduleVersion:'9.0.0'},{workspaceId:'../fremd'},{payload:{step:'falsch'}}])assert.equal(M.parse(JSON.stringify({...r,...change}),[unit]).ok,false);
assert.equal(M.parse('kaputt',[unit]).ok,false);
assert.equal(M.parse(' '.repeat(M.MAX_BYTES+1),[unit]).ok,false);
});
test('Import ist atomar und bevorzugt einen eigenen Stand',()=>{
const r=record(),store={records:[r],active:{[unit.id]:r.workspaceId}};
const next=M.accept(store,r,'separate','22222222-2222-4222-8222-222222222222');
assert.equal(store.records.length,1);assert.equal(next.records.length,2);assert.notEqual(next.records[1].workspaceId,r.workspaceId);
const replaced=M.accept(store,{...r,savedAt:'2026-10-04T00:00:00.000Z'},'replace',r.workspaceId);
assert.equal(replaced.records.length,1);assert.equal(store.records[0].savedAt,r.savedAt);
});
test('unbekannte und private Felder werden nicht importiert; HTML bleibt Text',()=>{
const r=record();r.payload.fields[0].value='<img src=x onerror=alert(1)>';
assert.equal(M.parse(JSON.stringify(r),[unit]).ok,true);
r.payload.fields.push({key:'i:private',value:'privat',type:'text',category:'private'});
assert.equal(M.parse(JSON.stringify(r),[unit]).ok,false);
});
test('Neuer Mantel erhält alte Seiten und erzeugt vollständige gemeinsame Zugänge',()=>{
const {prepare}=require('../m06-reinigungsfall/build.cjs');
const assets=prepare();
for(const name of ['index.html','arbeit.html','wissen.html','material.html','lehrkraft.html','informationen.html','mantel-sw.js'])
assert.ok(assets.has('klasse5/'+name),name);
for(const area of ['lernstudio','medienanalyse','quellenquest']){
const html=assets.get('klasse5/'+area+'/index.html');assert.match(html,/Deine Arbeit/);assert.match(html,/mantel-runtime.js/);
assert.ok(assets.has('klasse5/'+area+'/wiederaufnahme.html'));
}
assert.match(assets.get('index.html'),/url=reinigungsfall-v2\//);
assert.ok(assets.get('klasse5/quellenquest/baustein-belege.html').includes('Über einen größeren Garten im nächsten Jahr ist noch nicht entschieden.'), 'Vollständiges Quellenmaterial fehlt');
});

test('Kaputte Werkzeugdaten und versteckte Nutzdaten bleiben vor dem Import draußen',()=>{
 const assets=require('../m06-reinigungsfall/build.cjs').prepare(),units=require('./class5-catalog.cjs').catalog(assets);
 const media=units.find(u=>u.family==='media');
 const state={notes:{},answers:{},transferAnswers:{},checked:false,transferChecked:false,calibration:'',calibrationChecked:false,mode:'crop',crop:{x:0,width:680},headline:'Ein Bild',draft:{crop:{x:0,width:1536},headline:'',caption:'',reason:''},review:false,criteria:{},revised:false,decision:''};
 const make=(u,tool)=>M.envelope(u,{step:u.steps[0].id,fields:[],tool},'11111111-1111-4111-8111-111111111111','2026-10-03T00:00:00Z');
 const good=make(media,{family:'media',state,current:0});assert.equal(M.parse(JSON.stringify(good),units).ok,true);
 for(const bad of [{answers:null},{transferAnswers:[]},{criteria:null},{calibration:{}},{answers:{benches:'fremd'}}]){
  const r=M.clone(good);Object.assign(r.payload.tool.state,bad);assert.equal(M.parse(JSON.stringify(r),units).ok,false,JSON.stringify(bad));
 }
 const hidden=M.clone(good);hidden.payload.private={name:'privat'};assert.equal(M.parse(JSON.stringify(hidden),units).ok,false);
 const alg=units.find(u=>u.family==='algorithm'),S=require('../m06-lernstudio/studio-model.js'),work=S.fresh('start');
 const ar=make(alg,{family:'algorithm',data:{version:1,current:'start',works:{start:work}}});assert.equal(M.parse(JSON.stringify(ar),units).ok,true);
 ar.payload.tool.data.works.start.code='unbekannt';assert.equal(M.parse(JSON.stringify(ar),units).ok,false);
 ar.payload.tool.data.works.start.code=work.code;ar.payload.tool.data.works.start.prediction='kaputt';assert.equal(M.parse(JSON.stringify(ar),units).ok,false);
});
test('Lernbogen verweist nur auf vorhandene Schritte',()=>{
 const {validate}=require('./class5-catalog.cjs');
 const u={grade:5,id:'test',version:'1',title:'Test',area:'test',steps:[{id:'einstieg'}],learningDesign:{coverage:Object.fromEntries(require('./class5-catalog.cjs').functions.map(k=>[k,'einstieg']))}};
 assert.doesNotThrow(()=>validate(u));u.learningDesign.coverage.transfer='fehlender-schritt';assert.throws(()=>validate(u));
});
test('Gerätesicherung bleibt nach dem Wechsel im selben Tab eingeschaltet',()=>{
 const vm=require('node:vm'),fs=require('node:fs'),status={textContent:''},values=new Map([['ium-klasse5-mantel-v1-persistent','1']]),session=new Map([['ium-klasse5-mantel-v1',JSON.stringify({version:1,records:[],active:{}})]]);
 const storage=map=>({getItem:k=>map.get(k)||null,setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)});
 const document={currentScript:{src:'https://lernwerk.test/klasse5/mantel-runtime.js'},body:{dataset:{}},readyState:'complete',getElementById:id=>id==='lw-catalog'?{textContent:'[]'}:id==='lw-storage-status'?status:null,querySelectorAll:()=>[],addEventListener(){}};
 const window={LernwerkMantelModel:M,addEventListener(){}};
 vm.runInNewContext(fs.readFileSync(require.resolve('./mantel-runtime.js'),'utf8'),{document,window,location:{hash:'',href:'https://lernwerk.test/klasse5/arbeit.html'},URL,TextEncoder,crypto:require('node:crypto').webcrypto,sessionStorage:storage(session),localStorage:storage(values),navigator:{},queueMicrotask,console});
 assert.match(status.textContent,/auf diesem Gerät gespeichert/);
});

test('Neue Inhalte tragen reale Handlungen und schützen private Reflexion',()=>{
 const A=require('./class5-content.cjs');
 const pack={area:'neue-einheit',id:'IUM-5-FLEX-99',version:'1.0.0',grade:5,family:'content',title:'Ein neuer Lernbogen',topic:'Medien',description:'Prüfen und erklären.',product:'Eine Erklärung',prerequisites:[],teacher:['Vorbereitung durch die Lehrperson'],coverage:Object.fromEntries(require('./class5-catalog.cjs').functions.map(f=>[f,['einstieg']])),steps:[{id:'einstieg',title:'Erkläre deinen Weg',goal:'Du begründest eine Entscheidung.',criteria:['Ich nenne einen Grund.'],blocks:[
 {type:'external',id:'recherche',title:'Im Werkzeug prüfen',text:'Prüfe eine Quelle.',prompt:'Dein Ergebnis mit Herkunft',preparation:'Wähle einen sachlichen Suchbegriff.',action:'Suche und lies die Fundstelle.',return:'Bringe den Fund und begründe die Auswahl.',url:'https://example.org/'},
 {type:'cooperative',id:'austausch',title:'Zu zweit prüfen',text:'Vergleicht eure Gründe.',prompt:'Deine eigene überarbeitete Erklärung',contribution:'Jede Person nennt einen Beleg.',exchange:'Fragt nach und vergleicht Unterschiede.',return:'Schreibe danach selbst einen begründeten Satz.'},
 {type:'private',id:'reflexion',title:'Nur für dich',text:'Eine harmlose eigene Erfahrung oder Nichtnutzung genügt.',prompt:'Dein eigener Gedanke'},
 {type:'retrieval',id:'abruf',title:'Später erklären',text:'Erkläre zuerst aus dem Kopf.',prompt:'Deine erneute Erklärung',when:'In einer späteren Unterrichtsstunde.',solution:'Vergleiche danach mit deinem Beleg.'}
 ]}]};
 assert.doesNotThrow(()=>A.validate(pack));const u=A.unit(pack),html=A.renderBlocks(pack.steps[0]);
 assert.ok(!u.fields.some(k=>k.includes('reflexion')));assert.match(html,/data-private/);assert.match(html,/Danach wieder selbst/);assert.match(html,/neuer Tab, Internet nötig/);
 const invalid=M.clone(pack);invalid.steps[0].blocks[0].return='';assert.throws(()=>A.validate(invalid));
 invalid.steps[0].blocks[0].return='Zurück';invalid.steps[0].blocks[0].url='javascript:alert(1)';assert.throws(()=>A.validate(invalid));
});

test('Reguläre Medien-Transferantwort und schrittfremde generische Felder',()=>{
 const assets=require('../m06-reinigungsfall/build.cjs').prepare(),u=require('./class5-catalog.cjs').catalog(assets).find(u=>u.family==='media');
 assert.ok(u.mediaTransferChoices?.includes('fits'));
 const state={notes:{},answers:{},transferAnswers:{library:'fits'},checked:false,transferChecked:true,calibration:'',calibrationChecked:false,mode:'crop',crop:{x:0,width:680},headline:'Ein Bild',draft:{crop:{x:0,width:1536},headline:'',caption:'',reason:''},review:false,criteria:{},revised:false,decision:''};
 assert.equal(M.toolValid({family:'media',state,current:4},u),true);
 assert.equal(M.genericFieldAllowed({family:'algorithm'},'i:note'),false);
 assert.equal(M.genericFieldAllowed({family:'algorithm'},'i:lw-retrieval'),true);
 assert.equal(M.genericFieldAllowed({family:'source'},'i:beleg-grund'),true);
});
test('Inkompatible Tabkopie bleibt bei neuer Arbeit in Quarantäne',()=>{
 const vm=require('node:vm'),fs=require('node:fs'),session=new Map([['ium-klasse5-mantel-v1','{"version":0,"records":[]}']]);
 const storage={getItem:k=>session.get(k)||null,setItem:(k,v)=>session.set(k,v),removeItem:k=>session.delete(k)};
 const node={textContent:'',after(){}},document={currentScript:{src:'https://lernwerk.test/klasse5/mantel-runtime.js'},body:{dataset:{}},readyState:'complete',getElementById:id=>id==='lw-catalog'?{textContent:'[]'}:id==='lw-storage-status'||id==='lw-storage-warning'?node:null,querySelectorAll:()=>[],addEventListener(){},createElement:()=>({})};
 vm.runInNewContext(fs.readFileSync(require.resolve('./mantel-runtime.js'),'utf8'),{document,window:{LernwerkMantelModel:M,addEventListener(){}},location:{hash:'',href:'https://lernwerk.test/klasse5/arbeit.html'},URL,TextEncoder,crypto:require('node:crypto').webcrypto,sessionStorage:storage,localStorage:{getItem:()=>null,setItem(){}},navigator:{},queueMicrotask,setTimeout,console});
 assert.equal(session.get('ium-klasse5-mantel-v1-recovery'),'{"version":0,"records":[]}');
});

function runtimeHarness({limited=false,badTool=false}={}){
 const vm=require('node:vm'),fs=require('node:fs'),r=record(),store={version:1,records:[r],active:{[unit.id]:r.workspaceId}},events={},node={textContent:'',hidden:true,after(){}};
 const input={id:'answer',name:'',type:'textarea',tagName:'TEXTAREA',dataset:{},value:'Aktuelle neue Erklärung',closest:()=>null,getAttribute:()=>null};
 const doc={currentScript:{src:'https://lernwerk.test/klasse5/mantel-runtime.js'},body:{dataset:badTool?{lwArea:'quellenquest',lwPage:'index.html'}:{lwPage:'arbeit.html'}},readyState:'complete',
 getElementById:id=>id==='lw-catalog'?{textContent:JSON.stringify([unit])}:['lw-storage-status','lw-storage-warning','lw-emergency-export'].includes(id)?node:null,
 querySelectorAll:selector=>selector==='main input,main textarea,main select'?[input]:[],
 addEventListener:(event,fn)=>events[event]=fn,createElement:()=>({})};
 const window={LernwerkMantelModel:M,addEventListener(){},scrollY:0};
 const storage={getItem:k=>k==='ium-klasse5-mantel-v1'?JSON.stringify(store):null,setItem:()=>{if(limited)throw new Error('quota');}};
 vm.runInNewContext(fs.readFileSync(require.resolve('./mantel-runtime.js'),'utf8'),{document:doc,window,location:{hash:'#belege',href:'https://lernwerk.test/klasse5/arbeit.html'},history:{replaceState(){}},URL,TextEncoder,crypto:require('node:crypto').webcrypto,sessionStorage:storage,localStorage:{getItem:()=>null,setItem(){}},navigator:{},queueMicrotask:fn=>fn(),setTimeout,console});
 if(badTool){window.LernwerkMantel.register({capture:()=>({family:'source',answers:null}),restore(){}});window.LernwerkMantel.changed();}
 let prevented=false;const link={href:'https://lernwerk.test/klasse5/quellenquest/index.html#belege',target:'',dataset:{lwOpen:r.workspaceId}},target={closest:s=>s==='a'?link:null};
 events.click({target,preventDefault(){prevented=true;}});
 return {prevented,message:node.textContent};
}
test('Navigation schützt RAM-Arbeit auch auf der Arbeitsübersicht bei Speicherfehler',()=>{
 const result=runtimeHarness({limited:true});assert.equal(result.prevented,true);assert.match(result.message,/nicht sicher mitnehmbar/);
});
test('Navigation schützt den aktuellen Stand nach abgewiesener Autosicherung',()=>{
 const result=runtimeHarness({badTool:true});assert.equal(result.prevented,true);assert.match(result.message,/nicht sicher mitnehmbar/);
});

test('Bewusstes Löschen aller Lernwerkdaten entfernt auch die Quarantäne aus der laufenden Ansicht',()=>{
 const vm=require('node:vm'),fs=require('node:fs'),session=new Map([['ium-klasse5-mantel-v1','{"version":0,"records":[]}']]),all={},status={textContent:'',after(node){attached=node;}};
 let attached=null;
 const storage={getItem:k=>session.get(k)||null,setItem:(k,v)=>session.set(k,v),removeItem:k=>session.delete(k)};
 const document={currentScript:{src:'https://lernwerk.test/klasse5/mantel-runtime.js'},body:{dataset:{}},readyState:'complete',getElementById:id=>id==='lw-catalog'?{textContent:'[]'}:id==='lw-delete-all'?all:id==='lw-recovery-export'?attached: id==='lw-storage-status'||id==='lw-storage-warning'?status:null,querySelectorAll:()=>[],addEventListener(){},createElement:()=>({remove(){attached=null;}})};
 vm.runInNewContext(fs.readFileSync(require.resolve('./mantel-runtime.js'),'utf8'),{document,window:{LernwerkMantelModel:M,addEventListener(){}},location:{hash:'',href:'https://lernwerk.test/klasse5/arbeit.html'},URL,TextEncoder,crypto:require('node:crypto').webcrypto,sessionStorage:storage,localStorage:storage,navigator:{},queueMicrotask,setTimeout,confirm:()=>true,console});
 assert.ok(attached);all.onclick();assert.equal(session.get('ium-klasse5-mantel-v1-recovery'),undefined);assert.equal(attached,null);
});
