const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const file = path.join(__dirname, 'model.js');
const model = fs.existsSync(file) ? require(file) : {};
test('Ausschnitte bleiben auch bei Randwerten innerhalb des Originalbilds', () => {
 assert.equal(typeof model.crop, 'function');
 for (const input of [{x:-100,width:100},{x:9000,width:800},{x:300,width:2000},{x:NaN,width:NaN}]) {
  const c=model.crop(input);
  assert.ok(c.x>=0 && c.y>=0 && c.width>=600);
  assert.ok(c.x+c.width<=1536 && c.y+c.height<=1024);
  assert.equal(c.width/c.height,1.5);
 }
});
test('Untersuchung verändert immer nur Ausschnitt oder Überschrift', () => {
 assert.equal(typeof model.experiment, 'function');
 const a=model.experiment('crop',{x:800,width:650},'Nichts los!');
 assert.equal(a.before.headline,a.after.headline);
 assert.notDeepEqual(a.before.crop,a.after.crop);
 const b=model.experiment('headline',{x:800,width:650},'Nichts los!');
 assert.deepEqual(b.before.crop,b.after.crop);
 assert.notEqual(b.before.headline,b.after.headline);
});
test('Rückmeldung unterscheidet offene, passende und unpassende Belege', () => {
 assert.equal(typeof model.assess, 'function');
 const open=model.assess({});
 assert.ok(open.every(row=>row.status==='open'));
 const rows=model.assess({benches:'image',time:'context',all:'image',feeling:'unknown'});
 assert.equal(rows.find(r=>r.id==='benches').status,'match');
 assert.equal(rows.find(r=>r.id==='time').status,'match');
 assert.equal(rows.find(r=>r.id==='all').status,'revise');
 assert.equal(rows.find(r=>r.id==='feeling').status,'match');
 assert.ok(rows.every(r=>r.feedback.length>20));
});
test('Eigene Überschriften werden auch mit HTML-Zeichen als Text ausgegeben', () => {
 assert.equal(typeof model.escapeHtml, 'function');
 assert.equal(model.escapeHtml('<img src=x onerror="alert(1)"> &'), '&lt;img src=x onerror=&quot;alert(1)&quot;&gt; &amp;');
});
