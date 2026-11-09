'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs');
const core=()=>{assert.ok(fs.existsSync(path.join(__dirname,'b17-model.js')),'B17-Regel-/Zustandsmodul fehlt');return require('./b17-model.js');};
const pack=()=>JSON.parse(fs.readFileSync(path.join(__dirname,'inhalte/klasse6/werbung.json'),'utf8'));
test('B17 Kontext benutzt nur die aktuelle Seite, Verlauf nur frühere Mehrheiten',()=>{
 const M=core();
 for(const [current,visits,k,v]of [
 ['lesen',['zeichnen','zeichnen'],'buch','stifte'],
 ['zeichnen',['lesen','lesen'],'stifte','buch'],
 ['lesen',['lesen','zeichnen','zeichnen'],'buch','stifte'],
 ['zeichnen',['zeichnen','lesen','lesen'],'stifte','buch']]){
  const r=M.evaluate(current,visits);assert.equal(r.context,k);assert.equal(r.history,v);
  assert.equal(r.counts.lesen+r.counts.zeichnen,visits.length);
 }
});
test('B17 Gleichstand fällt auf aktuelle Seite zurück, einschließlich vorgemachtem Beispiel',()=>{
 const M=core();
 for(const current of ['lesen','zeichnen'])for(const visits of [[],['lesen','zeichnen'],['lesen','zeichnen','zeichnen','lesen']]){
  const r=M.evaluate(current,visits);assert.equal(r.tie,true);assert.equal(r.history,current==='lesen'?'buch':'stifte');
 }
});
test('B17 eigener Eingriff kann V ändern oder bewusst unverändert lassen',()=>{
 const M=core();
 for(const [index,expected]of [[0,'stifte'],[1,'buch'],[2,'buch']]){
  let s=M.transition(M.createState(),'CHECK_START');s=M.transition(s,'CHOOSE_VISIT',index);s=M.transition(s,'CHECK_CHANGE');
  assert.equal(s.phase,'compare');const r=M.evaluate('lesen',M.historyFor(s));assert.equal(r.context,'buch');assert.equal(r.history,expected);
 }
});
test('B17 erneute Wahl vor Prüfung verändert weiterhin genau einen ursprünglichen Besuch',()=>{
 const M=core(),start=M.createState(),original=M.historyFor(start);
 let s=M.transition(start,'CHECK_START');s=M.transition(s,'CHOOSE_VISIT',0);s=M.transition(s,'CHOOSE_VISIT',1);
 assert.deepEqual(M.historyFor(s),['lesen','lesen','zeichnen']);
 assert.equal(M.historyFor(s).filter((x,i)=>x!==original[i]).length,1);
 assert.deepEqual(M.historyFor(start),['lesen','zeichnen','zeichnen']);
});
test('B17 erzwingt Reihenfolge und Reset gibt nur den Modellanfang zurück',()=>{
 const M=core();let s=M.createState();assert.equal(s.phase,'predict-start');
 assert.throws(()=>M.transition(s,'CHOOSE_VISIT',1));
 s=M.transition(s,'CHECK_START');assert.throws(()=>M.transition(s,'CHECK_CHANGE'));
 s=M.transition(s,'CHOOSE_VISIT',2);assert.equal(s.phase,'predict-change');
 s=M.transition(s,'CHECK_CHANGE');assert.throws(()=>M.transition(s,'CHOOSE_VISIT',0));
 assert.deepEqual(M.transition(s,'RESET'),M.createState());
});
test('B17 weist ungültige Themen, Zustände und Besuchspositionen zurück',()=>{
 const M=core();assert.throws(()=>M.evaluate('sport',['lesen']));assert.throws(()=>M.evaluate('lesen',['lesen','sport']));
 for(const index of [-1,3,0.5,'1'])assert.throws(()=>M.transition(M.transition(M.createState(),'CHECK_START'),'CHOOSE_VISIT',index));
 assert.throws(()=>M.transition({phase:'fremd'},'CHECK_START'));assert.throws(()=>M.transition(M.createState(),'FREMD'));
});
test('B17 Autorenflag ist auf den vorgesehenen Versuch mit Papiertext begrenzt',()=>{
 const p=pack(),b=p.steps.find(s=>s.id==='modell').blocks.find(b=>b.id==='versuch');b.selectionModel=true;b.paperText=b.text;
 assert.doesNotThrow(()=>A.validate(p));
 const invalid=JSON.parse(JSON.stringify(p));invalid.steps.find(s=>s.id==='modell').blocks.find(b=>b.id==='versuch').type='example';
 assert.throws(()=>A.validate(invalid),/Auswahlmodell/);
 const missing=JSON.parse(JSON.stringify(p));delete missing.steps.find(s=>s.id==='modell').blocks.find(b=>b.id==='versuch').paperText;
 assert.throws(()=>A.validate(missing),/Auswahlmodell|Papier/);
});
test('B17 ist optional am eigenen Auftrag, Papierweg und bestehende Antwortfelder bleiben',()=>{
 const p=pack(),b=p.steps.find(s=>s.id==='modell').blocks.find(b=>b.id==='versuch');
 assert.equal(b.selectionModel,true);const pages=R.render(p),step=pages.get('schritt-modell.html'),paper=pages.get('baustein-modell.html');
 assert.ok(step.includes('data-b17-model'),'Bildschirmmodell fehlt');assert.match(step,/<details[^>]*class="[^"]*b17/);
 assert.doesNotMatch(paper,/data-b17-model/);assert.ok(paper.includes(A.esc(b.paperText)));
 const fields=A.unit(p).fields;assert.ok(fields.includes('i:answer-modell-versuch'));assert.ok(fields.every(f=>!f.includes('b17-visit')));
 assert.equal(p.version,'2.0.0');
});
test('B17 Laufzeit wird nur im Modellschritt ausgeliefert und ist im lokalen Gesamtbuild erreichbar',()=>{
 const all=require('../pages/build.cjs').preparePublishedPages(),root='klasse6/werbung/';
 const step=all.get(root+'schritt-modell.html');assert.ok(step.includes('b17-model.js'),'Modelllaufzeit fehlt');
 assert.ok(step.includes('b17-model.css'));assert.ok(all.has(root+'b17-model.js'));assert.ok(all.has(root+'b17-model.css'));
 for(const f of ['schritt-fluss.html','baustein-modell.html','schritt-gestalten.html'])assert.doesNotMatch(all.get(root+f),/b17-model\.(?:js|css)|data-b17-model/);
 assert.ok(all.get(root+'schritt-fluss.html').includes('B42'));assert.ok(all.get(root+'schritt-fluss.html').includes('answer-fluss-datenbild'));
});
test('B17 Browserlaufzeit erzeugt keine Cookies, Speicherstände oder Netzabfragen',()=>{
 core();const source=fs.readFileSync(path.join(__dirname,'b17-model.js'),'utf8');
 assert.doesNotMatch(source,/\b(?:fetch|XMLHttpRequest|WebSocket|localStorage|sessionStorage|indexedDB)\b|document\.cookie|history\./);
 assert.match(source,/stopPropagation/);
});