const test=require('node:test'),assert=require('node:assert/strict'),A=require('./class5-content.cjs'),M=require('./mantel-model.js');
for(const area of ['geraete','speicher-zugang'])test('Inhalt '+area+' ist vollständig erreichbar, offline enthalten und von Dateien-Arbeit getrennt',()=>{
 const packs=A.load(),p=packs.find(p=>p.area===area),d=packs.find(p=>p.area==='dateien');assert.ok(p);
 const assets=require('../m06-reinigungsfall/build.cjs').prepare(),R=require('./class5-author-render.cjs');
 for(const file of [...R.render(p).keys(),...A.assets(p).keys()]){assert.ok(assets.has('klasse5/'+area+'/'+file),file);assert.ok(assets.get('klasse5/mantel-sw.js').includes(area+'/'+file),file+' fehlt offline');}
 assert.match(assets.get('klasse5/reihe-arbeitsraum.html'),new RegExp(area+'/lehrkraft.html'));
 const u=A.unit(p),du=A.unit(d),key=u.fields[0],record=M.envelope(u,{step:p.steps[0].id,fields:[{key,value:'Meine eigene Erklärung',type:'text'}]},'11111111-1111-4111-8111-111111111111','2026-10-04T10:00:00.000Z');
 assert.equal(M.parse(JSON.stringify(record),[u,du]).ok,true);
 assert.equal(M.parse(JSON.stringify({...record,moduleId:du.id,moduleVersion:du.version}),[u,du]).ok,false);
 assert.doesNotMatch(assets.get('klasse5/'+area+'/material.html'),/<h2>Übungsdateien<\/h2>/);
});
