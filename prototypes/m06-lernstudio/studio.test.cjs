'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const S=require('./studio-model.js'),W=require('../m06-lernwerkstatt/workshop-model.js');
test('Alle elf Stationen haben einen fachlichen Check mit erklärender Rückmeldung',()=>{
 assert.equal(S.order.length,11);
 for(const id of S.order){const q=S.checks[id];assert.ok(q.prompt&&q.options.length===3);assert.ok(q.feedback.length===3);assert.ok(q.answer>=0&&q.answer<3);}
});
test('Programmänderung verwirft vorherige Fahrtergebnisse und Checknachweise',()=>{
 const s=S.fresh('own');s.observed=true;s.checked=true;s.attempts=2;s.step=4;
 S.change(s,'vor');assert.equal(s.observed,false);assert.equal(s.checked,false);assert.equal(s.step,0);assert.equal(s.attempts,0);
});
test('Ein falscher Check markiert keinen Erfolg, ein korrigierter bleibt als Wiederholung erkennbar',()=>{
 const s=S.fresh('loop');assert.equal(S.answer('loop',s,0).ok,false);assert.equal(s.checked,false);
 assert.equal(S.answer('loop',s,1).ok,true);assert.equal(s.checked,true);assert.equal(s.independent,false);
});
test('Unbeeinflusster erster Check und unterstützter Check bleiben unterscheidbar',()=>{
 const a=S.fresh('start');S.answer('start',a,1);assert.equal(a.independent,true);
 const b=S.fresh('start');b.help=1;S.answer('start',b,1);assert.equal(b.independent,false);
});
test('Ungültige Antworten verändern keinen Checknachweis',()=>{
 const s=S.fresh('start');assert.throws(()=>S.answer('start',s,99));assert.equal(s.attempts,0);
});
test('Wiederherstellung begrenzt Daten und übernimmt nur bekannte Stationen und gültigen Code',()=>{
 const r=S.restore(JSON.stringify({version:1,current:'evil',works:{own:{code:'go();',note:'a'.repeat(3000),step:99999},evil:{code:'vor'}}}));
 assert.equal(r.current,'start');assert.equal(r.works.own.code,'');assert.equal(r.works.own.note.length,2000);
 assert.equal(r.works.own.step,0);assert.equal(r.works.evil,undefined);
 assert.equal(S.restore('not JSON'),null);assert.equal(S.restore('{"version":99}'),null);
});
test('Endprognose prüft Position und Blick gemeinsam, nicht nur die Kachel',()=>{
 assert.equal(S.prediction('start',[2,1,0]),true);
 assert.equal(S.prediction('start',[2,1,1]),false);
 assert.equal(S.prediction('start',null),null);
});
test('Checklösungen passen zu den unveränderten fachlichen Simulationen',()=>{
 assert.equal(W.run('loop',W.lesson('loop').code).trace.length-1,8);
 assert.equal(W.run('example',W.lesson('example').code).trace.length-1,7);
 assert.deepEqual(W.run('return',W.lesson('return').code).end,[2,1,0]);
 assert.equal(W.run('check',W.lesson('check').code).missing.length,2);
 assert.equal(W.station('A').completed,3);assert.equal(W.station('B').error.step,2);
});

test('Ein leerer eigener Plan zeigt den Startzustand ohne Fahrt oder Erfolg',()=>{
 const r=S.run('own','');
 assert.equal(r.status,'empty');assert.equal(r.success,false);
 assert.equal(r.trace.length,1);assert.deepEqual(r.trace[0].pos,[1,3,1]);
 assert.equal(r.cleaned.length,1);assert.equal(r.missing.length,11);
});

test('Ein unzulässiger Schleifenkörper verändert den vorhandenen Plan nicht',()=>{
 const s=S.fresh('own');s.code='vor';s.observed=true;
 assert.throws(()=>S.change(s,'wiederhole 2 [vor; vor; vor; vor; vor; vor]'));
 assert.equal(s.code,'vor');assert.equal(s.observed,true);assert.deepEqual(s.undo,[]);
});
