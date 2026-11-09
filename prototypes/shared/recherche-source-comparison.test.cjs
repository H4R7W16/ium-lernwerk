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

test('RQ02 Quellenwahl steht nur im eigenen Vergleich vor den aktivierbaren Links',()=>{
 const p=pack(),own=p.steps.find(s=>s.id==='pruefen').blocks.find(b=>b.id==='eigene-zweite-seite');
 assert.equal(own.linksAfterItems,true,'Wahlregel braucht Vorrang');
 const pages=R.render(p);
 for(const file of ['schritt-pruefen.html','baustein-pruefen.html']){
  const html=pages.get(file),body=html.slice(html.indexOf('id="eigene-zweite-seite"'),html.indexOf('id="aussage-vergleichen"'));
  for(const [,url]of own.externalLinks)assert.ok(body.indexOf(A.esc(own.items[0]))<body.indexOf('href="'+A.esc(url)+'"'),'Regel vor '+url);
  assert.match(body,/Erste Quelle DLR_next\? Nimm jetzt timeanddate\. Erste Quelle timeanddate\? Nimm jetzt DLR_next\./);
 }
 const search=pages.get('schritt-suchen.html');const ordinary=search.slice(search.indexOf('id="eigene-suche"'),search.indexOf('id="eigene-notiz"'));
 assert.ok(ordinary.indexOf('https://www.fragfinn.de/')<ordinary.indexOf('<ol>'),'Andere Reihenfolge bleibt erhalten');
 const invalid=pack();invalid.steps.find(s=>s.id==='pruefen').blocks.find(b=>b.id==='lea-prueft').linksAfterItems=true;assert.throws(()=>A.validate(invalid),/Quellenwahl/);
});

test('RQ02 Worthilfe kommt beim Lesen rechtzeitig; Herkunft bleibt sichtbar, nachschlagbar und auf Papier vollständig',()=>{
 const p=pack(),c=block(p).sourceComparison,out=R.render(p);
 for(const file of ['schritt-pruefen.html','baustein-pruefen.html']){
  const html=out.get(file),start=html.indexOf('class="lw-ref-source-comparison"'),end=html.indexOf('id="lea-vergleich"'),comparison=html.slice(start,end);
  assert.ok(comparison.indexOf('class="lw-ref-wordhelp"')<comparison.indexOf('class="lw-ref-source-grid"'),'Worthilfe vor Auszügen');
  for(const source of c.sources){
   assert.ok(source.shortSource);assert.ok(comparison.includes(A.esc(source.shortSource)));
   assert.ok(comparison.includes('href="'+A.esc(source.url)+'"'));
   assert.ok(comparison.includes('<details class="lw-ref-source-details">'),'Quellenangaben geschlossen nachschlagbar');
   assert.ok(comparison.includes('<p class="lw-ref-source-print">'+A.esc(source.location)+' · '+A.esc(source.source)+'</p>'),'Druckherkunft unabhängig vom Klappzustand');
  }
 }
 const bad=pack();block(bad).sourceComparison.sources[0].shortSource='';assert.throws(()=>A.validate(bad),/Quellenvergleich/);
});
