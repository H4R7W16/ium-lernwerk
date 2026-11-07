'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),P=require('./papierturm.cjs');
const pack=A.load(6).find(p=>p.area==='kommunikation');
test('V2 hält den wahren Wortlaut konstant und unterscheidet Tischsituation von Bildbeiträgen',()=>{
 const h=P.gallery(pack);
 assert.equal((h.match(/class="pt-message">Unser Papierturm steht!</g)||[]).length,3);
 assert.equal((h.match(/src="assets\/kommunikation\/papierturm\/turm.webp"/g)||[]).length,2);
 assert.equal((h.match(/src="assets\/kommunikation\/papierturm\/tisch-v2.webp"/g)||[]).length,1);
 for(const t of ['Vier Personen','24 Klassenmitglieder','180 Aufrufe','12:18','14:40','andere Schule','Skizze'])assert.ok(h.includes(t),t);
 assert.doesNotMatch(h,/Das ging bei uns sofort|AG-Leitung|Teilnehmerliste|vierten Bauversuch|data-score|contenteditable|textarea|<iframe/);
 assert.ok(h.includes('data-pt-view="ab"'));assert.ok(h.includes('data-pt-view="bc"'));
});
test('Lernweg führt Erstdeutung, Kontext und Rückbezug; Rollenprüfung ist ein eigener Fall',()=>{
 const pages=P.integrate(pack,require('./class5-author-render.cjs').render(pack)),h=pages.get('schritt-vergleichen.html');
 assert.ok(h.indexOf('1 · Dein erster Eindruck')<h.indexOf('id="turm-hintergrund"'));
 assert.ok(h.indexOf('id="turm-hintergrund"')<h.indexOf('3 · Deine Deutung prüfen'));
 assert.ok(h.indexOf('3 · Deine Deutung prüfen')<h.indexOf('Zwei weitere Prüfanlässe'));
 assert.match(P.context(pack),/<details><summary>/);assert.doesNotMatch(P.context(pack),/<details open/);
 assert.match(h,/Greife deinen ersten Satz wieder auf/);assert.match(h,/schulischen Nachrichtendienst/);
 const w=pack.knowledge.find(k=>k.id==='wirkung');assert.doesNotMatch(w.example,/Turm|drei eingestürzte|vier/);assert.match(w.example,/Kuchen/);
});
test('Textzugang und Printtexte sind an dieselben vollständigen Falldaten gebunden',()=>{
 const pages=P.integrate(pack,require('./class5-author-render.cjs').render(pack)),h=pages.get('papierturm-text.html'),g=P.gallery(pack);
 for(const v of pack.papertower.views){for(const r of v.reactions){assert.ok(h.includes(A.esc(r.text)));assert.ok(h.includes(A.esc(r.time)));}for(const [,text]of v.conditions)assert.ok(h.includes(A.esc(text)));}
 assert.match(h,/schritt-vergleichen.html#papierturm/);assert.match(h,/Bildbeschreibung/);assert.match(h,/mit KI erzeugt/);
 assert.equal((g.match(/class="pt-print-post"/g)||[]).length,3);
 assert.match(g,/class="pt-print-rules"/);assert.match(g,/Mindestalter von 16/);
 assert.match(P.context(pack),/class="pt-print-context"/);
});
test('V2-Medienzugang ist vollständig und bleibt auf das Kommunikationspaket begrenzt',()=>{
 const assets=P.assets(pack);
 for(const f of ['papierturm.css','papierturm.js',pack.papertower.image,pack.papertower.sceneImage])assert.ok(assets.has(f),f);
 assert.equal(P.assets({...pack,grade:5}).size,0);
 assert.throws(()=>P.gallery({...pack,papertower:{...pack.papertower,sceneImage:'../fremd.png'}}),/unvollständig/);
});

