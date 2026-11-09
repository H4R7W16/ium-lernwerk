'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs');
const pack=()=>structuredClone(A.load().find(p=>p.area==='recherche'));
const block=p=>p.steps.find(s=>s.id==='pruefen').blocks.find(b=>b.id==='lea-prueft');
test('RQ02 Vergleich bewahrt unmarkierte Originalauszüge, Herkunft und eindeutige Quellen',()=>{
 const p=pack(),c=block(p).sourceComparison;assert.ok(c,'Quellenvergleich fehlt');assert.equal(c.sources.length,2);
 assert.equal(c.sources[0].text,p.steps.find(s=>s.id==='suchplan').blocks.find(b=>b.id==='lea-liest').passages.options[0].text);
 assert.equal(c.sources[1].text,'Denn er leuchtet ja nicht selbst, sondern erscheint nur so hell, weil die Sonne ihn beleuchtet.');
 for(const s of c.sources){assert.ok(s.source&&s.location);assert.equal(new URL(s.url).protocol,'https:');assert.doesNotMatch(s.text,/<|\*\*/);}
 assert.match(c.sources[1].url,/\/wie-der-mond-die-erde-umkreist$/);
 for(const corrupt of [c=>c.sources.pop(),c=>c.sources[1].url='javascript:alert(1)',c=>c.sources[1].url=c.sources[0].url,c=>c.claim='',c=>c.sources[0].location='']){
  const x=pack();corrupt(block(x).sourceComparison);assert.throws(()=>A.validate(x),/Quellenvergleich|HTTPS/);
 }
});
test('RQ02 Lernseite und Papier vergleichen vor der geschlossenen Lösung; Arbeitsstand bleibt gleich',()=>{
 const p=pack(),out=R.render(p);for(const f of ['schritt-pruefen.html','baustein-pruefen.html']){
  const html=out.get(f);assert.match(html,/class="lw-ref-source-comparison"/);assert.equal((html.match(/class="lw-ref-source-card"/g)||[]).length,2);
  const solution=html.match(/<details[^>]*><summary>Leas Prüfnotiz · nach deinem Versuch<\/summary>[\s\S]*?<\/details>/)?.[0];assert.ok(solution,'Fertige Prüfnotiz muss geschlossen bleiben');assert.doesNotMatch(solution.slice(0,solution.indexOf('>')),/\bopen\b/);
  assert.ok(html.indexOf('Zeige in beiden Textstellen')<html.indexOf('class="lw-ref-source-comparison"'));assert.ok(html.indexOf('Zeige in beiden Textstellen')<html.indexOf(solution));assert.match(solution,/Bestätigt, weil beide Stellen/);
  assert.match(html,/id="lea-prueft"/);assert.match(html,/id="lea-vergleich"/);assert.match(html,/Kehre jetzt zu deinem markierten Satz über rund und Sichel zurück/);
  const cards=html.match(/<section class="lw-ref-source-comparison"[\s\S]*?<\/section>/)[0];assert.doesNotMatch(cards,/<(?:strong|mark|b)\b/);
 }
 assert.match(out.get('baustein-pruefen.html'),/class="lw-print-url">https:\/\/www\.dlr\.de/);
 assert.equal(p.version,'2.0.0');assert.equal(A.unit(p).fields.length,0);assert.equal(p.steps.length,7);assert.equal(p.teachingPlan.reduce((a,s)=>a+s.minutes,0),225);
});
