const test=require('node:test');
const assert=require('node:assert/strict');
const W=require('./workshop-model.js');
test('Touch-Bausteine erhalten ganzen Schleifenkörper und Folgeanweisung',()=>{
 const blocks=W.blocks('wiederhole 4 [vor; links]\nvor');
 assert.equal(W.code(blocks),'wiederhole 4 [vor; links]\nvor');
 const run=W.run('after',W.code(blocks));
 assert.equal(run.trace.length,10);
 assert.deepEqual(run.end,[2,2,1]);
});
test('Reihenwechsel startet mit acht bereits gereinigten Kacheln',()=>{
 const r=W.run('switch','rechts\nvor\nrechts');
 assert.deepEqual(r.end,[1,1,1]);
 assert.equal(r.trace[0].cleaned.length,8);
 assert.equal(r.cleaned.length,9);
 assert.equal(W.assess('switch','rechts\nvor\nrechts').ok,true);
 assert.equal(W.assess('switch','links\nvor\nlinks').ok,false);
});
test('Eigener Plan akzeptiert Reihen und Spalten statt einer Musterzeichenfolge',()=>{
 const rows='wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]';
 const cols='links\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]';
 assert.equal(W.assess('own',rows).ok,true);assert.equal(W.assess('own',cols).ok,true);
 assert.equal(W.assess('own','wiederhole 4 [vor]').kind,'wall');
});
test('Stationsablauf bewertet Reihenfolge, nicht nur Anzahl der Aktionen',()=>{
 const a=W.station('A'),b=W.station('B');
 assert.equal(a.completed,3);assert.equal(a.error,null);
 assert.equal(b.completed,0);assert.equal(b.error.step,2);
 assert.equal(b.trace.at(-1).state,'belegt');
});
test('Randrunde lässt genau die zwei inneren Kacheln offen',()=>{
 const r=W.run('check',W.lessons.find(x=>x.id==='check').code);
 assert.deepEqual(r.missing,['2,2','3,2']);assert.equal(r.cleaned.length,10);
});
test('Abruf startet neu: links oben, Blick unten, Ende rechts oben nach oben',()=>{
 const r=W.run('return',W.lessons.find(x=>x.id==='return').code);
 assert.deepEqual(r.end,[2,1,0]);assert.equal(r.trace.length,8);
});

test('Reparatur verlangt Fahren und Drehen im wiederholten Körper',()=>{
 const falseRepair='wiederhole 4 [rechts]\nvor\nlinks\nvor\nlinks\nvor\nlinks\nvor\nlinks';
 assert.equal(W.assess('repair',falseRepair).ok,false);
 assert.equal(W.assess('repair','wiederhole 4 [vor; links]').ok,true);
 assert.equal(W.assess('repair','wiederhole 2 [vor; links; vor; links]').ok,true);
});
test('Vollständiger Musterweg erreicht sechs Kacheln in sieben Aktionen',()=>{
 const l=W.lesson('example'),r=W.run(l.id,l.code);
 assert.equal(r.trace.length,8);assert.equal(r.cleaned.length,6);assert.equal(r.status,'complete');
 assert.deepEqual(r.end,[1,1,3]);
});
test('Alle festen Beobachtungsaufgaben sind ohne Wandstopp ausführbar',()=>{
 for(const l of W.lessons.filter(l=>!l.station&&!l.editable)){
  const r=W.run(l.id,l.code);assert.equal(r.status,'complete',l.id);
 }
});
