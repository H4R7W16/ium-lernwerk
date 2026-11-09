'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs');
const pack=()=>structuredClone(A.load(6).find(p=>p.area==='medienprodukt'));
const example=p=>p.steps.find(s=>s.id==='auftrag').blocks.find(b=>b.id==='bibliotheksvergleich');
const plain=s=>s.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
const facts=html=>[...html.matchAll(/<(?:p|div)\b[^>]*data-m07-fact="([^"]+)"[^>]*>([\s\S]*?)<\/(?:p|div)>/g)].map(m=>[m[1],plain(m[2])]);
test('M07 B und C zeigen exakt dieselben Fakten und Quellen bei unterschiedlicher Gestaltung',()=>{
 const p=pack(),b=example(p);assert.ok(b?.libraryComparison,'Bibliotheksvergleich fehlt');
 const C=require('./m07-comparison.cjs'),model=b.libraryComparison;
 const a=C.card(model,'A'),corrected=C.card(model,'B'),clear=C.card(model,'C');
 assert.deepEqual(facts(corrected),facts(clear));assert.ok(facts(clear).length>=7,'Vollständige Fakten einschließlich Quelle und Rechte nötig');
 for(const content of ['Romane','14 Tage','Sachbücher','7 Tage','Ab Juni','Mai-Aushang','Quelle:'])assert.ok(plain(clear).includes(content),content);
 assert.match(a,/m07-rough/);assert.match(corrected,/m07-rough/);assert.match(a,/m07-star/);assert.match(corrected,/m07-star/);assert.doesNotMatch(clear,/m07-star/);
 assert.match(plain(a),/ALLE BÜCHER 14 TAGE/);
 const bad=pack();example(bad).libraryComparison.facts.source='';assert.throws(()=>A.validate(bad),/Bibliotheksvergleich/);
 const wrong=pack(),config=example(wrong).libraryComparison;delete example(wrong).libraryComparison;wrong.steps.find(s=>s.id==='entwurf').blocks[0].libraryComparison=config;assert.throws(()=>A.validate(wrong),/Bibliotheksvergleich/);
});
test('M07 nutzt denselben optionalen Vergleich auf Lernseite, Projektion und Einzelansicht; Papier behält Hilfenschicht',()=>{
 const p=pack(),pages=R.render(p),projection=require('./class6-media-project.cjs').projection();
 for(const html of [pages.get('schritt-auftrag.html'),pages.get('bild-vergleich.html'),projection]){
  assert.match(html,/class="m07-comparison m07-comparison-screen"/);
  const toggle=html.match(/<input\b[^>]*class="m07-choice"[^>]*>/)?.[0];assert.ok(toggle);assert.doesNotMatch(toggle,/\bchecked\b/);assert.match(toggle,/aria-controls="m07-state-a m07-state-b"/);
  assert.equal((html.match(/data-m07-state="C"/g)||[]).length,1);assert.match(html,/Bei Bedarf/);assert.doesNotMatch(html,/<img[^>]+vergleich\.svg/);
 }
 const paper=pages.get('baustein-auftrag.html');assert.match(paper,/m07-comparison-paper/);assert.match(paper,/<details class="lw-help m07-paper-help">/);assert.doesNotMatch(paper,/class="m07-choice"/);
 const u=A.unit(p);assert.equal(p.version,'2.0.0');assert.ok(u.fields.every(f=>!f.includes('m07-choice')));assert.match(p.duration,/210 Kernminuten/);
 assert.match(pages.get('schritt-auftrag.html'),/answer-auftrag-wirkung/);
});
