const test=require('node:test'),a=require('node:assert/strict'),M=require('./model.js'),V=require('./view.js');
test('Kartenansicht zeigt jede Karte am richtigen Ort und erhält die Ausgabereihenfolge',()=>{
 const run=M.run('nimm lege nimm markiere lege',3),before=JSON.stringify(run);
 const start=V.describe(run.trace[0]);a.equal(start.groups[0].cards.length,3);a.equal(start.groups[1].cards.length,0);a.equal(start.groups[2].cards.length,0);
 const taken=V.describe(run.trace[1]);a.equal(taken.groups[0].cards.length,2);a.deepEqual(taken.groups[1].cards,[false]);
 const marked=V.describe(run.trace[4]);a.deepEqual(marked.groups[1].cards,[true]);
 const end=V.describe(run.trace[5]);a.deepEqual(end.groups[2].cards,[false,true]);a.match(end.groups[2].text,/1: unmarkiert.*2: markiert/);a.equal(JSON.stringify(run),before);
});
test('Schleifendurchlauf und zuletzt ausgeführter Befehl bleiben auch beim Fehler korrekt',()=>{
 const run=M.run('wiederhole 3 [nimm markiere lege]',2),last=run.trace.at(-1),v=V.describe(last);
 a.equal(run.error.step,7);a.match(v.command,/lege/);a.match(v.command,/Durchlauf 2/);a.equal(v.groups[0].cards.length,0);a.deepEqual(v.groups[2].cards,[true,true]);
});
