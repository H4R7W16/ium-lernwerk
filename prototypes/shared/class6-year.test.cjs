'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const Y=require('./class6-year.cjs'),A=require('./class5-content.cjs');
test('38 periods conserve every module and separate annual accounts without duplicate retrievals',()=>{
 assert.equal(Y.slots.length,38);const sums={},seen=[];
 for(const [i,slot]of Y.slots.entries()){
  assert.equal(slot.reduce((s,x)=>s+x[1],0),45,'UE'+(i+1));
  for(const [id,n]of slot){sums[id]=(sums[id]||0)+n;if(id.startsWith('R')){seen.push(id);const r=Y.recalls.find(x=>x.id===id);assert.equal(r.slot,i+1);assert.equal(r.minutes,n);}}
 }
 for(const m of Y.modules)assert.equal(sums[m.id],m.minutes,m.id);
 assert.equal(sums.D,90);assert.equal(sums.B,45);assert.equal(sums.O,45);assert.equal(sums.P,135);
 assert.equal(seen.length,14);assert.equal(new Set(seen).size,14);assert.equal(Y.recalls.reduce((n,r)=>n+r.minutes,0),90);
 const quotas={M01:12,M02:16,M03:12,M04:14,M05:14,M06:10,M07:12};
 for(const [id,n]of Object.entries(quotas))assert.equal(Y.recalls.filter(r=>r.module===id).reduce((s,r)=>s+r.minutes,0),n);
});
test('every recall maps to a real retained response and later M06/M07 appointments follow completion',()=>{
 const packs=A.load(6);
 for(const r of Y.recalls){const p=packs.find(p=>p.area===r.area),s=p.steps.find(s=>s.id===r.step);assert.ok(s,r.id);assert.ok(s.blocks.some(b=>b.id===r.block&&b.type==='retrieval'),r.id);}
 const end=id=>Math.max(...Y.slots.map((s,i)=>s.some(x=>x[0]===id)?i+1:0));
 assert.ok(Y.recalls.find(r=>r.id==='R11').slot>end('M06'));
 assert.ok(Y.recalls.find(r=>r.id==='R12').slot>Y.recalls.find(r=>r.id==='R11').slot);
 assert.ok(Y.recalls.find(r=>r.id==='R13').slot>end('M07'));
 assert.ok(Y.recalls.find(r=>r.id==='R14').slot>Y.recalls.find(r=>r.id==='R13').slot);
});
test('year pages, exact recall anchors and six onward links are present in the built offline product',()=>{
 const assets=require('../m06-reinigungsfall/build.cjs').prepare();
 for(const name of ['jahresplan.html','wiederholen.html','jahresstart.html','uebergaenge.html']){assert.ok(assets.has('klasse6/'+name));assert.ok(assets.get('klasse6/mantel-sw.js').includes(name));}
 for(const r of Y.recalls){const html=assets.get('klasse6/'+r.area+'/schritt-'+r.step+'.html');assert.ok(html.includes('id="answer-'+r.step+'-'+r.block+'"'),r.id);assert.ok(html.includes('id="recall-'+r.step+'-'+r.block+'"'),r.id+' task anchor');assert.ok(html.includes('../wiederholen.html#'+r.id),r.id+' return');}
 for(const t of Y.transitions){const from=Y.modules.find(m=>m.id===t.from),to=Y.modules.find(m=>m.id===t.to);assert.ok(assets.get('klasse6/'+from.area+'/schritt-'+from.last+'.html').includes('href="../'+to.area+'/index.html"'));}
 assert.match(assets.get('klasse6/suche/baustein-bruecke.html'),/kein zusätzlicher Auftrag/);
 assert.match(assets.get('klasse6/medienprodukt/lehrkraft.html'),/45\+45\+40\+45\+35/);
 assert.match(assets.get('klasse6/uebergaenge.html'),/Keine persönlichen Reflexionen/);
});
