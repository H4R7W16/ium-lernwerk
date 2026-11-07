'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),P=require('./papierturm.cjs');
const pack=A.load(6).find(p=>p.area==='kommunikation');
test('Papierturm kontrolliert Wortlaut und Bild, variiert nachvollziehbare Kommunikationsbedingungen',()=>{
 const m=pack.papertower,html=P.gallery(pack);
 assert.equal((html.match(/class="pt-message">Unser Papierturm steht! Das ging bei uns sofort\./g)||[]).length,3);
 assert.equal((html.match(/src="assets\/kommunikation\/papierturm\/turm.webp"/g)||[]).length,3);
 for(const t of ['Vier Personen','24 Klassenmitglieder','180 Aufrufe','12:18','14:40','unbekanntes Konto','Mindestalter von 16','Kopien außerhalb'])assert.ok(html.includes(t),t);
 assert.doesNotMatch(html,/vier Bauversuche|data-score|contenteditable|textarea|<iframe/);
 assert.equal(m.views[0].reactions[0].text,m.views[1].reactions[0].text);
});
test('Hintergrund wird getrennt nach erster Deutung geöffnet; Falllösung bleibt zuschaltbar',()=>{
 const pages=P.integrate(pack,require('./class5-author-render.cjs').render(pack));
 const h=pages.get('schritt-vergleichen.html');
 assert.ok(h.indexOf('Lies die Ansichten gegeneinander')<h.indexOf('id="turm-hintergrund"'));
 assert.ok(h.indexOf('id="turm-hintergrund"')<h.indexOf('Wirkung ist eine begründete Vermutung'));
 assert.match(P.context(pack),/<details><summary>/);
 assert.doesNotMatch(P.context(pack),/<details open/);
 assert.match(h,/Belege zuerst deine Vermutung/);
});
test('Textzugang enthält alle Fallangaben, Rückwege und denselben getrennten Hintergrund',()=>{
 const pages=P.integrate(pack,require('./class5-author-render.cjs').render(pack)),h=pages.get('papierturm-text.html');
 for(const v of pack.papertower.views){for(const r of v.reactions){assert.ok(h.includes(r.text));assert.ok(h.includes(r.time));}for(const [,text]of v.conditions)assert.ok(h.includes(text));}
 assert.match(h,/schritt-vergleichen.html#papierturm/);
 assert.match(h,/Bildbeschreibung/);assert.match(h,/mit KI erzeugt/);
});
test('Medienzugang ist vollständig und bleibt auf das Kommunikationspaket begrenzt',()=>{
 const assets=P.assets(pack);
 for(const f of ['papierturm.css','papierturm.js',pack.papertower.image])assert.ok(assets.has(f),f);
 assert.equal(P.assets({...pack,grade:5}).size,0);
 assert.throws(()=>P.gallery({...pack,papertower:{...pack.papertower,image:'../fremd.png'}}),/unvollständig/);
});


