'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs'),P=require('./papierbruecke.cjs');
const make=()=>{
 const p=structuredClone(A.load().find(p=>p.area==='medienwirkung'));
 p.paperbridge={files:['index.html','alle.html','texte.html','karte-01.webp','karte-02.webp','karte-03.webp','karte-04.webp'],cards:[1,2,3,4].map(n=>({file:'karte-0'+n+'.webp',alt:'Beitrag Bild '+n}))};
 return p;
};
test('Papierbrückenbeitrag öffnet im B-Fall und bleibt im Einzelmaterial vollständig',()=>{
 const p=make(),pages=R.render(p),step=pages.get('schritt-werbung.html'),sheet=pages.get('baustein-werbung.html');
 assert.match(step,/id="jules-beitrag"/);
 assert.match(step,/assets\/medienwirkung\/papierbruecke\/index\.html\?lernwerk=1/);
 assert.doesNotMatch(step,/<iframe/);
 assert.match(step,/Jules’ Bilderbeitrag öffnen/);
 for(let n=1;n<=4;n++){assert.match(sheet,new RegExp('B · Bild '+n+' von 4'));assert.ok(sheet.includes('karte-0'+n+'.webp'));assert.ok(sheet.includes('Beitrag Bild '+n));}
 assert.ok(sheet.indexOf('karte-04.webp')<sheet.indexOf('lw-solution'),'Vier Bilder stehen vor der Lösung');
 assert.match(step,/magazin\.svg/);
 for(const name of ['briefing.html','lehrkraft.html'])assert.match(pages.get(name),/schritt-werbung\.html#jules-beitrag/);
});
test('Papierbrückenbundle weist fehlende Zugänge, doppelte Karten und Pfadflucht ab',()=>{
 for(const mutate of [p=>p.paperbridge.files.push('../outside.js'),p=>p.paperbridge.files.push('/outside.js'),p=>p.paperbridge.files.push('https://bad.test/x.js'),p=>p.paperbridge.files=p.paperbridge.files.filter(n=>n!=='texte.html'),p=>p.paperbridge.cards.pop(),p=>p.paperbridge.cards[1]=p.paperbridge.cards[0],p=>p.paperbridge.cards[0].alt='',p=>p.area='dateien']){
  const p=make();mutate(p);assert.throws(()=>P.validate(p),/Papierbrück/);
 }
});
test('Andere Lernbogenfassungen bleiben durch den Falladapter unverändert',()=>{
 const p=structuredClone(A.load().find(p=>p.area==='dateien')),pages=new Map([['probe','unverändert']]);
 assert.equal(P.integrate(p,pages),pages);assert.equal(P.assets(p).size,0);
});

test('Veröffentlichung bindet Beitrag samt URL-Parameter und allen Dateien in das Offlinepaket ein',()=>{
 const p=A.load().find(p=>p.area==='medienwirkung'),built=require('../m06-reinigungsfall/build.cjs').prepare();
 assert.ok(p.paperbridge,'Produktionsbundle fehlt');
 for(const file of p.paperbridge.files){
  const key='klasse5/medienwirkung/assets/medienwirkung/papierbruecke/'+file;
  assert.ok(built.has(key),key);
  assert.match(built.get('klasse5/mantel-sw.js'),new RegExp(file.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
 }
 const html=built.get('klasse5/medienwirkung/schritt-werbung.html');
 assert.match(html,/index\.html\?lernwerk=1/);
 assert.match(html,/Bildnummer/);
 assert.match(built.get('klasse5/medienwirkung/briefing.html'),/25-minütigen Werbevergleich/);
 assert.equal(p.steps.find(s=>s.id==='werbung').blocks[2].responseMode,'oral');
});

test('Erstidee steht vor Magazinvergleich und wird ohne Zusatzabgabe wieder aufgenommen',()=>{
 const p=make(),s=p.steps.find(s=>s.id==='werbung'),pages=R.render(p);
 assert.deepEqual(s.blocks.map(b=>b.type),['example','example','task']);
 assert.deepEqual(s.blocks[0].media,['video']);
 assert.deepEqual(s.blocks[1].media,['magazin']);
 assert.match(s.blocks[0].text,/30–60 Sekunden/);
 assert.match(s.blocks[0].text,/Was würdest du aus Jules’ Beitrag für deine Brücke übernehmen/);
 assert.equal(s.blocks[2].responseMode,'oral');
 assert.match(s.blocks[2].responseHint,/Vier kurze Aussagen/);
 assert.match(s.blocks[2].prompt,/Was würdest du weiterhin übernehmen, was bleibt ungeklärt/);
 assert.doesNotMatch(s.task,/Beginne mit dem sichtbaren Werbehinweis/);
 for(const name of ['schritt-werbung.html','baustein-werbung.html']){
  const html=pages.get(name);
  assert.ok(html.indexOf('Was würdest du aus Jules’ Beitrag')<html.indexOf('id="jules-beitrag"'),name+' Erstidee vor Material');
  assert.ok(html.indexOf('id="jules-beitrag"')<html.indexOf('magazin.svg'),name+' B vor A');
  assert.ok(html.indexOf('magazin.svg')<html.indexOf('Vergleiche die beiden Formate'),name+' Materialien vor Analyse');
 }
 assert.match(p.briefing.join(' '),/25-minütigen Werbevergleich/);
});
