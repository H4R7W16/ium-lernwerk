'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const a=require('./planung/klasse5-abdeckung.json'),teacher=require('./class5-teacher-pages.cjs'),packs=require('./class5-content.cjs').load();
const key=x=>x.moduleId+'|'+x.competencyId;
test('Abgleich enthält jede aktive Inhalts- und Prozessplatzierung genau einmal',()=>{
 assert.equal(a.planningCommit,teacher.plan.source.commit);
 for(const [kind,expected]of [['content',a.expectedContent],['process',a.expectedProcess]]){
  const actual=a.records.filter(r=>r.kind===kind);assert.equal(new Set(actual.map(key)).size,actual.length);
  assert.deepEqual(actual.map(key).sort(),expected.map(key).sort());
 }
 for(const m of teacher.plan.modules){
  const actual=[...new Set(packs.filter(p=>p.curriculum.moduleId===m.id).flatMap(p=>p.curriculum.goalIds))].sort();
  assert.deepEqual(actual,a.expectedContent.filter(x=>x.moduleId===m.id).map(x=>x.competencyId).sort(),m.id);
 }
 assert.equal(a.privateContracts.length,2);assert.equal(a.band56NotInGrade5.length,19);
 const current=new Set(a.expectedContent.map(x=>x.competencyId));assert.ok(a.band56NotInGrade5.every(x=>!current.has(x.competencyId)));
});
test('Jeder Nachweis und jede private Reflexion verweist auf einen realen Schritt',()=>{
 for(const r of [...a.records,...a.privateContracts]){assert.ok(r.refs.length);for(const ref of r.refs){
  const p=packs.find(p=>p.area===ref.unit);assert.ok(p?.steps.some(s=>s.id===ref.step),JSON.stringify(ref));assert.equal(p.curriculum.moduleId,r.moduleId);
 }}
 assert.ok(a.records.every(r=>r.status==='offered-not-observed'&&r.action&&r.limit));
});
test('Übergänge bleiben vollständig; Abrufe werden nicht doppelt gebucht',()=>{
 assert.deepEqual(teacher.plan.review.transitions.map(x=>x.moduleId),teacher.plan.modules.map(x=>x.id));
 assert.equal(teacher.allSeries().reduce((n,s)=>n+s.later.minutes,0),37);
 assert.equal(teacher.plan.reserves.spacedPracticeMinutes-37,98);
});
test('Gesamtübersicht und Rückwege werden gebaut und im Offlinepaket verlinkt',()=>{
 const built=require('../m06-reinigungsfall/build.cjs').prepare();
 assert.ok(built.has('klasse5/zusammenhaenge.html'));
 assert.match(built.get('klasse5/lehrkraft.html'),/href="zusammenhaenge.html"/);
 assert.match(built.get('klasse5/mantel-sw.js'),/zusammenhaenge.html/);
 for(const x of teacher.plan.review.transitions){assert.ok(built.has('klasse5/'+x.href));assert.ok(built.get('klasse5/zusammenhaenge.html').includes('href="'+x.href+'"'));}
 assert.ok(built.get('klasse5/quellenquest/index.html').includes('href="../recherche/schritt-suchen.html"'));
 for(const step of ['selbstbild','rueckmeldung','handeln'])assert.ok(built.get('klasse5/medienanalyse/index.html').includes('../medienwirkung/schritt-'+step+'.html'));
});
