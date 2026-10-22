'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs'),M=require('./mantel-model.js');
const pack=A.load(6).find(p=>p.area==='kommunikation');
test('M06 private thoughts are excluded from catalog, paper and ordinary export schema',()=>{
 const u=A.unit(pack),pages=R.render(pack);
 assert.ok(u.fields.includes('i:answer-entscheidung-karte'));
 assert.ok(u.fields.includes('i:answer-revision-revision'));
 assert.ok(u.fields.every(f=>!f.includes('private')&&!f.includes('persoenlich')));
 assert.match(pages.get('schritt-rechte.html'),/data-private/);
 assert.doesNotMatch(pages.get('baustein-rechte.html'),/private-rechte-persoenlich|data-private/);
 assert.match(pages.get('baustein-rechte.html'),/15 Minuten: dein eigener schulischer Bezug/);
 const record=M.envelope(u,{step:'entscheidung',fields:[{key:'i:answer-entscheidung-karte',type:'text',value:'Eigene sachliche Entscheidung',category:'work'}],tool:null},'11111111-1111-4111-8111-111111111111','2026-10-22T12:00:00Z');
 assert.equal(M.parse(JSON.stringify(record),[u]).ok,true);
 record.payload.fields.push({key:'i:private-rechte-persoenlich',type:'text',value:'private-test',category:'work'});
 assert.equal(M.parse(JSON.stringify(record),[u]).ok,false);
});
test('M06 actual exchange and offline boundary are retained in both editions',()=>{
 const pages=R.render(pack);
 for(const prefix of ['schritt-','baustein-']){
  assert.match(pages.get(prefix+'entscheidung.html'),/Eine Notiz im Lernwerk sendet keine Nachricht/);
  assert.match(pages.get(prefix+'entscheidung.html'),/digitalen Austausch als offen/);
  assert.match(pages.get(prefix+'revision.html'),/tatsächlich erhaltene/);
 }
 assert.match(pages.get('lehrkraft.html'),/reihe-m06.html/);
});
test('M06 assets, series and offline cache are emitted together',()=>{
 const assets=require('../m06-reinigungsfall/build.cjs').prepare();
 for(const file of ['kommunikation/index.html','kommunikation/briefing.html','kommunikation/baustein-rechte.html','kommunikation/assets/kommunikation/schulwegkarte.txt','reihe-m06.html'])assert.ok(assets.has('klasse6/'+file),file);
 assert.match(assets.get('klasse6/mantel-sw.js'),/kommunikation\/wissen.html/);
 assert.match(assets.get('klasse6/stoffverteilung.html'),/kommunikation\/index.html/);
});
