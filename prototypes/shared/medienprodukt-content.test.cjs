'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs'),M=require('./mantel-model.js');
const pack=A.load(6).find(p=>p.curriculum.moduleId==='G6-M07');
test('M07 owns distinct media paths and keeps downloads identical to paper text',()=>{
 const older=new Set([...A.load(5),...A.load(6).filter(p=>p.id!==pack.id)].flatMap(p=>p.media.map(m=>m.file)));
 for(const m of pack.media)assert.equal(older.has(m.file),false,m.file+' collides with an older module');
 assert.equal(A.assets(pack).size,pack.media.length);
});
test('M07 preserves actual production, peer feedback and two recipient checks in paper edition',()=>{
 const pages=R.render(pack);
 for(const prefix of ['schritt-','baustein-']){
  assert.match(pages.get(prefix+'entwurf.html'),/Wechselt die Bedienrolle/);
  assert.match(pages.get(prefix+'austausch.html'),/reale Zweiergruppe/);
  assert.match(pages.get(prefix+'revision.html'),/Öffnet die PDF neu/);
  assert.match(pages.get(prefix+'teilen.html'),/Empfangsperson öffnet genau diese Datei/);
  assert.match(pages.get(prefix+'teilen.html'),/zweiter Upload/);
 }
 assert.match(pages.get('lehrkraft.html'),/reihe-m07.html/);
});
test('M07 work export preserves project notes but does not pretend to contain external products',()=>{
 const u=A.unit(pack),key='i:answer-revision-ueberarbeiten';
 const result=M.envelope(u,{step:'revision',fields:[{key,type:'text',value:'v1 → v2: Beschriftung nach Rückfrage präzisiert.',category:'work'}],tool:null},'11111111-1111-4111-8111-111111111111','2026-10-22T12:00:00Z');
 assert.equal(M.parse(JSON.stringify(result),[u]).ok,true);
 assert.equal(result.payload.tool,null);
 assert.match(pack.workNotice,/Produktdateien.*getrennt/);
 assert.ok(u.fields.every(f=>!f.includes('private')));
});
test('M07 projection, teaching aids and material are in the build and offline cache',()=>{
 const assets=require('../m06-reinigungsfall/build.cjs').prepare();
 for(const file of ['medienprodukt/index.html','medienprodukt/projektion.html','medienprodukt/briefing.html','medienprodukt/baustein-teilen.html','reihe-m07.html'])assert.ok(assets.has('klasse6/'+file),file);
 assert.match(assets.get('klasse6/mantel-sw.js'),/medienprodukt\/projektion.html/);
 assert.match(assets.get('klasse6/medienprodukt/material.html'),/projektion.html/);
});
