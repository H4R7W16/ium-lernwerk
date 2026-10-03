const test=require('node:test'),assert=require('node:assert/strict'),A=require('./class5-content.cjs');
const clone=x=>JSON.parse(JSON.stringify(x));
function fixture(){return {authorVersion:2,area:'datei-probe',id:'IUM-5-M01-PROBE',version:'1.0.0',grade:5,family:'content',title:'Ablage',topic:'Dateien',description:'Dateien wiederfinden.',product:'Eine geordnete Datei',prerequisites:['Ein vereinbarter Speicherort'],teacher:['Geräte prüfen'],curriculum:{moduleId:'G5-M01',goalIds:['3.1.5.1(2)'],source:'plan',scope:'Teilziel'},duration:'90 Minuten als Planungsannahme',sources:[{id:'plan',title:'Quelle',author:'Redaktion',url:'https://example.org/plan',license:'Nur verlinkt',checked:'2026-10-03'}],media:[{id:'bild',kind:'image',file:'assets/dateien/ablage.svg',title:'Ordnerbaum',alt:'Speicherort mit Ordner und Datei',caption:'Schematische Darstellung',creator:'Lernwerk',license:'CC BY-SA 4.0',sourceId:'plan'},{id:'probe',kind:'download',file:'assets/dateien/fundnotiz.txt',title:'Fundnotiz',printText:'FUNDNOTIZ: Eine blaue Trinkflasche liegt im Fundbüro.',creator:'Lernwerk',license:'CC BY-SA 4.0',sourceId:'plan'}],knowledge:[{id:'ordner',title:'Was ist ein Ordner?',paragraphs:['Ein Ordner gruppiert Dateien.'],example:'Ein Projektordner enthält eine Notiz.',boundary:'Das ist ein Modell, kein Bildschirmfoto.',steps:['einstieg'],sources:['plan'],media:['bild']}],coverage:Object.fromEntries(require('./class5-catalog.cjs').functions.map(f=>[f,['einstieg']])),steps:[{id:'einstieg',title:'Ablegen',goal:'Du legst eine Datei ab.',task:'Plane einen Ort.',outcome:'Dein begründeter Ablageort.',criteria:['Ich finde meine Datei wieder.'],knowledge:['ordner'],blocks:[{type:'external',context:'device',id:'weg',title:'Am Gerät arbeiten',text:'Arbeite im vereinbarten Übungsordner.',preparation:'Öffne deinen Übungsbereich.',action:'Lege die Datei ab.',return:'Öffne sie erneut.',prompt:'Dein Weg',media:['probe'],help:[{title:'Ein Hinweis',text:'Prüfe den übergeordneten Ordner.'}],routes:[{title:'iPad',items:['Öffne Dateien.'],sources:['plan']},{title:'Windows',items:['Öffne den Explorer.'],sources:['plan']}],solution:'Ort und Inhalt prüfen.'}]}]};}
test('Autorenpaket trägt lokale Gerätehandlung mit beiden Wegen und Fachwissen',()=>{const p=fixture();assert.doesNotThrow(()=>A.validate(p));const html=A.renderBlocks(p.steps[0],p);assert.match(html,/iPad/);assert.match(html,/Windows/);assert.match(html,/download/);assert.doesNotMatch(html,/Internet nötig/);assert.match(html,/answer-einstieg-weg/);});
test('Ungültige Medienpfade, fehlende Rechte und unbekannte Referenzen stoppen die Aufnahme',()=>{assert.doesNotThrow(()=>A.validate(fixture()));for(const mutate of [p=>p.media[0].file='../secret.txt',p=>p.media[0].file='assets/../../secret.svg',p=>p.media[0].license='',p=>p.knowledge[0].steps=['fremd'],p=>p.knowledge[0].sources=['fremd'],p=>p.steps[0].blocks[0].media=['fehlt'],p=>p.steps[0].blocks[0].routes[0].sources=['fehlt'],p=>p.steps[0].knowledge=['fehlt'],p=>p.sources[0].url='javascript:alert(1)',p=>p.media.push(clone(p.media[0]))]){const p=fixture();mutate(p);assert.throws(()=>A.validate(p));}});
test('Vollständige Ausgaben trennen Wissen von Material und enthalten Kriterien sowie druckbaren Dateitext',()=>{const R=require('./class5-author-render.cjs'),p=fixture();A.validate(p);const pages=R.render(p);const knowledge=pages.get('wissen.html'),material=pages.get('material.html'),sheet=pages.get('baustein-einstieg.html'),step=pages.get('schritt-einstieg.html');assert.match(knowledge,/Ein Ordner gruppiert Dateien/);assert.doesNotMatch(material,/Ein Ordner gruppiert Dateien/);assert.match(knowledge,/id="ordner"/);assert.match(knowledge,/data-lw-return/);assert.match(sheet,/FUNDNOTIZ/);assert.match(sheet,/Ich finde meine Datei wieder/);assert.doesNotMatch(sheet,/<textarea/);assert.match(sheet,/lw-solution/);assert.match(step,/schritt-einstieg.html/);assert.match(step,/Dein Auftrag/);assert.match(step,/lw-step-menu/);});
test('Erstes echtes Paket wird mit Dateien, Wissen, Lehrbrief und vollständigen Einzelmaterialien veröffentlicht',()=>{const pack=A.load().find(p=>p.area==='dateien');assert.ok(pack,'echtes Paket fehlt');const assets=require('../m06-reinigungsfall/build.cjs').prepare();for(const name of ['index.html','wissen.html','material.html','lehrkraft.html','briefing.html'])assert.ok(assets.has('klasse5/dateien/'+name),name);for(const m of pack.media)assert.ok(assets.has('klasse5/dateien/'+m.file),m.file);for(const s of pack.steps){const html=assets.get('klasse5/dateien/baustein-'+s.id+'.html');assert.ok(html,s.id);for(const c of s.criteria)assert.ok(html.includes(A.esc(c)),c);}assert.match(assets.get('klasse5/index.html'),/dateien\/index.html/);assert.doesNotMatch(assets.get('klasse5/index.html'),/Drei Themen/);assert.match(assets.get('klasse5/mantel-sw.js'),/dateien\/assets\/dateien\/fundnotiz.txt/);});

function runtimePage(page,session,{printMode='learner',details=[]}={}){
 const vm=require('node:vm'),fs=require('node:fs'),M=require('./mantel-model.js'),p=A.load().find(p=>p.area==='dateien'),u=A.unit(p),events={},select={value:printMode,addEventListener(){}},back={href:'index.html'};
 const document={currentScript:{src:'https://lernwerk.test/klasse5/mantel-runtime.js'},body:{dataset:{lwArea:'dateien',lwPage:page}},readyState:'complete',getElementById:id=>id==='lw-catalog'?{textContent:JSON.stringify([u])}:id==='lw-print-mode'?select:null,
 querySelectorAll:s=>s==='[data-lw-return]'?[back]:s==='.lw-author .lw-help,.lw-author .lw-solution,.lw-author .lw-device-route'?details:[],addEventListener(){}};
 const storage={getItem:k=>session.get(k)||null,setItem:(k,v)=>session.set(k,v)};
 const window={LernwerkMantelModel:M,addEventListener:(e,fn)=>{events[e]=fn;}};
 vm.runInNewContext(fs.readFileSync(require.resolve('./mantel-runtime.js'),'utf8'),{document,window,location:{hash:'',href:'https://lernwerk.test/klasse5/dateien/'+page},URL,TextEncoder,crypto:require('node:crypto').webcrypto,sessionStorage:storage,localStorage:{getItem:()=>null},navigator:{},queueMicrotask,console});
 return {back,events,body:document.body};
}
test('Wissen kehrt auch ohne erste Antwort zum zuletzt geöffneten Inhaltsschritt zurück',()=>{
 const session=new Map();runtimePage('schritt-planen.html',session);const page=runtimePage('wissen.html',session);
 assert.equal(page.back.href,'schritt-planen.html');
 const saved=JSON.parse(session.get('ium-klasse5-mantel-v1'));assert.equal(saved.records.length,0,'Lesen ist kein Lernnachweis');
 runtimePage('schritt-transfer.html',session);assert.equal(runtimePage('material.html',session).back.href,'schritt-transfer.html');
});
test('Drucken trennt Hilfen und Lösungen und stellt danach den Lesestand wieder her',()=>{
 for(const mode of ['learner','helpers','solutions']){
  const help={open:false,classList:{contains:()=>false}},solution={open:true,classList:{contains:c=>c==='lw-solution'}},page=runtimePage('baustein-ablegen.html',new Map(),{printMode:mode,details:[help,solution]});
  page.events.beforeprint();assert.equal(help.open,mode!=='learner');assert.equal(solution.open,mode==='solutions');assert.equal(page.body.dataset.lwPrint,mode);
  page.events.afterprint();assert.equal(help.open,false);assert.equal(solution.open,true);
 }
});

test('Fehlende Medien und abweichende Drucktexte werden vor der Ausgabe abgewiesen',()=>{
 const p=clone(A.load().find(p=>p.area==='dateien'));p.media.find(m=>m.kind==='download').printText+=' Fremder Text';
 assert.throws(()=>A.assets(p),/Druckinhalt weichen ab/);
 const missing=clone(p);missing.media[0].file='assets/dateien/fehlt.svg';assert.throws(()=>A.assets(missing),/ENOENT/);
});

test('Gerätekarten erlauben Medien am Handlungspunkt und prüfen deren Verweise',()=>{
 const p=fixture(),b=p.steps[0].blocks.find(b=>b.routes);
 b.routes[0].items=[{title:'Datei holen',text:'Jetzt herunterladen.',media:['probe']}];
 assert.doesNotThrow(()=>A.validate(p));
 const html=A.renderBlocks(p.steps[0],p);
 assert.match(html,/<details class="lw-device-route"[^>]*>[\s\S]*?<li><h4>Datei holen<\/h4>[\s\S]*?download/);
 assert.match(A.renderBlocks(p.steps[0],p,{paper:true}),/<details class="lw-device-route" open>/);
 b.routes[0].items[0].media=['fehlt'];assert.throws(()=>A.validate(p),/Verweis/);
});
test('Kurze Antworterwartung steht vor dem Feld; mündliche Aufgaben behalten optionale Notizen',()=>{
 const p=fixture(),s=p.steps[0],b=s.blocks.find(b=>b.id);
 b.responseHint='Ein Satz genügt. Auch mündlich möglich.';b.responseMode='oral';
 const html=A.renderBlocks(s,p),id='answer-'+s.id+'-'+b.id;
 assert.ok(html.indexOf(b.responseHint)<html.indexOf('<textarea'));
 assert.match(html,/<details class="lw-optional-answer"><summary>Wenn du möchtest: hier notieren<\/summary>/);
 assert.ok(html.includes('id="'+id+'"'));assert.ok(html.includes('aria-describedby="'+id+'-hint"'));
 assert.doesNotMatch(A.renderBlocks(s,p,{paper:true}),/textarea/);
});
test('Späterer Abruf folgt auf einen sichtbaren Abschluss statt auf einen normalen Weiter-Link',()=>{
 const p=clone(A.load().find(p=>p.area==='dateien'));
 p.steps.at(-1).timing='later';p.steps.at(-2).completion={title:'Für heute fertig',text:'Prüfe die Dateien.'};
 const pages=require('./class5-author-render.cjs').render(p),html=pages.get('schritt-transfer.html');
 assert.match(html,/Für heute fertig/);assert.doesNotMatch(html,/Weiter: Später/);
 assert.match(html,/In einer späteren Stunde/);assert.match(pages.get('baustein-transfer.html'),/Für heute fertig/);
 assert.match(pages.get('index.html'),/In einer späteren Stunde/);
});
test('Gerätewege bleiben in allen Druckmodi vollständig, danach kehrt der Klappzustand zurück',()=>{
 for(const mode of ['learner','helpers','solutions']){
  const route={open:false,classList:{contains:c=>c==='lw-device-route'}};
  const page=runtimePage('baustein-ablegen.html',new Map(),{printMode:mode,details:[route]});
  page.events.beforeprint();assert.equal(route.open,true,mode);page.events.afterprint();assert.equal(route.open,false);
 }
});

test('Modell und Denkfrage bilden auf Lernseite und Material eine gemeinsame Gruppe',()=>{
 const p=clone(A.load().find(p=>p.area==='dateien')),s=p.steps.find(s=>s.id==='verstehen');
 s.layout='model-task';
 const pages=require('./class5-author-render.cjs').render(p);
 for(const name of ['schritt-verstehen.html','baustein-verstehen.html']){
  assert.match(pages.get(name),/<div class="lw-model-task">[\s\S]*?lw-block-example[\s\S]*?lw-block-task/);
 }
});
test('Selbstprüfung und Geübteneinstieg verwenden geprüfte Ziele und vollständige Hilfe',()=>{
 const p=fixture(),s=p.steps[0];
 p.experiencedEntry={title:'Schon geübt?',text:'Beginne mit deiner Planung.',step:'einstieg',label:'Planung öffnen'};
 s.checkHelp=[{title:'Datei nicht gefunden?',text:'Beginne wieder am Startort. Prüfe den Weg erneut.',step:'einstieg',label:'Geräteweg öffnen'}];
 s.materialNeeds=['Dieses Blatt und einen Stift'];
 const pages=require('./class5-author-render.cjs').render(p);
 assert.match(pages.get('index.html'),/Schon geübt\?[\s\S]*?href="schritt-einstieg.html"/);
 for(const name of ['schritt-einstieg.html','baustein-einstieg.html'])assert.match(pages.get(name),/lw-check-help[\s\S]*?Beginne wieder am Startort[\s\S]*?href="schritt-einstieg.html"/);
 assert.match(pages.get('baustein-einstieg.html'),/Benötigt:<\/b> Dieses Blatt und einen Stift/);
 assert.doesNotMatch(pages.get('baustein-einstieg.html'),/Benötigt:<\/b> Ein vereinbarter Speicherort/);
 s.checkHelp[0].step='fehlt';assert.throws(()=>A.validate(p),/Verweis/);
 s.checkHelp[0].step='einstieg';p.experiencedEntry.step='fehlt';assert.throws(()=>A.validate(p),/Verweis/);
});
test('Eigenständige Geräteblätter enthalten nur ihren vollständigen Geräteweg',()=>{
 const p=fixture(),s=p.steps[0],b=s.blocks[0];
 b.routes[0].device='ipad';b.routes[1].device='windows';
 const pages=require('./class5-author-render.cjs').render(p);
 for(const [device,other,title]of [['ipad','Windows','iPad'],['windows','iPad','Windows']]){
  const sheet=pages.get('baustein-einstieg-'+device+'.html');
  assert.ok(sheet,device);assert.match(sheet,/FUNDNOTIZ/);assert.match(sheet,/Ich finde meine Datei wieder/);
  assert.ok(sheet.includes('Geräteweg: '+title));
  const routes=[...sheet.matchAll(/<details class="lw-device-route"[^>]*>[\s\S]*?<\/details>/g)];
  assert.equal(routes.length,1);assert.ok(!routes[0][0].includes(other));
 }
 assert.match(pages.get('material.html'),/baustein-einstieg-ipad.html/);
 assert.match(pages.get('baustein-einstieg.html'),/baustein-einstieg-windows.html/);
 b.routes[1].device='invalid';assert.throws(()=>A.validate(p),/Gerät/);
});
