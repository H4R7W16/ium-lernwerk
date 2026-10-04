const test=require('node:test'),assert=require('node:assert/strict');
const P=require('./class5-teacher-pages.cjs');
test('Jahreskonten und Reihenzeit passen ohne doppelten Abrufposten',()=>{
 const p=P.plan;assert.equal(p.modules.reduce((n,m)=>n+m.minutes,0),1350);
 assert.equal(p.modules.reduce((n,m)=>n+m.minutes,0)+Object.values(p.reserves).reduce((a,b)=>a+b,0),1710);
 assert.equal(p.series.phases.reduce((n,x)=>n+x.minutes,0),p.modules[0].minutes);
 assert.equal(p.series.later.minutes,12);assert.equal(p.series.later.account,'spacedPracticeMinutes');
 assert.equal(p.availability,'unconfirmed');assert.equal(p.modules.length,6);
 assert.throws(()=>P.validate({...p,availability:'confirmed'}),/Budget/);
 const invalid=structuredClone(p);invalid.series.phases[0].minutes+=45;assert.throws(()=>P.validate(invalid),/Reihenzeit/);
});
test('Planung ist vollständig im Build und aus Übersicht und Einheit erreichbar',()=>{
 const a=require('../m06-reinigungsfall/build.cjs').prepare();
 for(const file of ['stoffverteilung.html','reihe-arbeitsraum.html']){assert.ok(a.has('klasse5/'+file));assert.match(a.get('klasse5/mantel-sw.js'),new RegExp(file.replace('.','\\.')));}
 assert.match(a.get('klasse5/lehrkraft.html'),/href="stoffverteilung.html"/);
 assert.match(a.get('klasse5/lehrkraft.html'),/href="reihe-arbeitsraum.html"/);
 assert.match(a.get('klasse5/dateien/lehrkraft.html'),/href="..\/reihe-arbeitsraum.html"/);
 assert.match(a.get('klasse5/dateien/material.html'),/href="lehrkraft.html"/);
 assert.match(a.get('klasse5/reihe-arbeitsraum.html'),/dateien\/lehrkraft.html/);
 assert.match(a.get('klasse5/stoffverteilung.html'),/<th[^>]*scope="col"/);
 for(const [name,html]of a)if(name.startsWith('klasse5/')&&name.endsWith('.html')){
  const visible=html.replace(/<script[\s\S]*?<\/script>/g,'').replace(/<[^>]+>/g,' ');
  assert.doesNotMatch(visible,/\b(?:Lehrkraft|Lehrkräfte|Lehrer|Lehrerin)\b/,name);
 }
});
