'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const J=require('./journey-model.js');
test('4×2: drei Fahrten je Reihe erreichen alle acht Kacheln',()=>{
 const a=J.bridge({first:'3',turn:'links',last:'3'});
 assert.equal(a.kind,'success');assert.equal(a.result.cleaned.length,8);assert.deepEqual(a.result.end,[1,1,3]);assert.equal(a.result.trace.length,10);
});
test('4×2: vier Fahrten stoppen an der Wand, nicht als Erfolg werten',()=>{
 const a=J.bridge({first:'4',turn:'links',last:'3'});
 assert.equal(a.kind,'wall');assert.deepEqual(a.result.end,[4,2,1]);assert.equal(a.result.trace.length,5);
});
test('4×2: zu kurze Reihe meldet fehlende Fläche',()=>{
 const a=J.bridge({first:'3',turn:'links',last:'2'});
 assert.equal(a.kind,'incomplete');assert.deepEqual(a.result.missing,['1,1']);
});
test('4×2: leere, ungültige und nicht unterstützte Lücken starten keine Fahrt',()=>{
 for(const first of ['', '0','1','3.5','10','3\nvor'])assert.equal(J.bridge({first,turn:'links',last:'3'}).result,undefined);
 assert.equal(J.bridge({first:'3',turn:'vor',last:'3'}).result,undefined);
});
test('Linker Wechsel behält acht zuvor erreichte Kacheln und prüft auch den Blick',()=>{
 const a=J.switchRow(['rechts','vor','rechts']);
 assert.equal(a.kind,'success');assert.deepEqual(a.result.trace[0].pos,[1,2,3]);
 assert.equal(a.result.trace[0].cleaned.length,8);assert.equal(a.result.cleaned.length,9);
 assert.deepEqual(a.result.end,[1,1,1]);assert.equal(a.result.trace.length,4);
});
test('Linker Wechsel unterscheidet falsche Reihe, falschen Blick und Wand',()=>{
 assert.equal(J.switchRow(['links','vor','links']).kind,'position');
 assert.equal(J.switchRow(['rechts','vor','links']).kind,'direction');
 assert.equal(J.switchRow(['vor','rechts','rechts']).kind,'wall');
 assert.equal(J.switchRow(['rechts','','rechts']).result,undefined);
});
test('Teilfahrt verändert den Zustand nachfolgender Versuche nicht',()=>{
 J.switchRow(['links','vor','links']);
 const a=J.switchRow(['rechts','vor','rechts']);
 assert.equal(a.result.trace[0].cleaned.length,8);assert.equal(a.result.cleaned.length,9);
});
