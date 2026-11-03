'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),M=require('./mantel-model.js');
const id='12345678-1234-4234-9234-123456789abc',next='12345678-1234-4234-9234-123456789abd';
const old={id:'R5-test',version:'1.0.0',grade:5,family:'content',steps:[{id:'frage'}],fields:['i:alte-frage']};
const current={...old,version:'2.0.0',steps:[{id:'neu'}],fields:['i:neue-frage'],compatibleVersions:[old]};
const record=M.envelope(old,{step:'frage',fields:[{key:'i:alte-frage',type:'text',value:'Meine frühere Begründung',label:'Alte Frage',category:'work'}],tool:null},id,'2026-10-28T12:00:00.000Z');
test('bekannter alter Stand bleibt in seiner Fassung lesbar und unverändert exportierbar',()=>{
 const text=JSON.stringify(record),r=M.parse(text,[current]);assert.equal(r.ok,true,r.message);assert.equal(r.readOnly,true);assert.equal(r.unit.version,'1.0.0');assert.equal(JSON.stringify(r.record),text);
});
test('alte Fassung darf keine neuen oder privaten Felder einschleusen',()=>{
 for(const field of [{key:'i:neue-frage',type:'text',value:'nicht umdeuten'},{key:'i:alte-frage',type:'text',value:'privat',category:'private'}]){
  const r=structuredClone(record);r.payload.fields=[field];assert.equal(M.parse(JSON.stringify(r),[current]).ok,false);
 }
});
test('unbekannte Altversion wird weiterhin abgewiesen',()=>{const r={...record,moduleVersion:'0.0.1'};assert.equal(M.parse(JSON.stringify(r),[current]).ok,false);});
test('neuer Einstieg setzt alte aktive Antworten nicht fort',()=>{
 const store={records:[record],active:{[old.id]:id}};
 assert.equal(typeof M.resumeId,'function');
 assert.equal(M.resumeId(store,current,next),next);assert.deepEqual(store.records,[record]);
 const fresh=M.envelope(current,{step:'neu',fields:[],tool:null},next,'2026-11-03T12:00:00Z');
 assert.equal(M.resumeId({records:[record,fresh],active:{[old.id]:id}},current,'unused'),next);
});
test('Import kann keinen Stand einer anderen Inhaltsfassung überschreiben',()=>{
 const fresh=M.envelope(current,{step:'neu',fields:[],tool:null},next,'2026-11-03T12:00:00Z');
 const store={version:1,records:[fresh],active:{[old.id]:next}};
 assert.throws(()=>M.accept(store,record,'replace',next),/Fassung/);
 const separated=M.accept(store,record,'separate',id);
 assert.equal(separated.records.length,2);assert.deepEqual(separated.records[0],fresh);
});
test('Browserkatalog trägt beide Fassungen ohne vollständige Unterrichtstexte doppelt einzubetten',()=>{
 const A=require('./class5-content.cjs'),R=require('./mantel-render.cjs');for(const grade of [5,6]){
 const units=A.load(grade).map(A.unit),html=R.page('Probe','<p>Probe</p>',units),catalog=JSON.parse(html.match(/id="lw-catalog">([\s\S]*?)<\/script>/)[1]);
 assert.ok(JSON.stringify(catalog).length<100000,'Browserkatalog zu groß');
 for(const u of units){const c=catalog.find(x=>x.id===u.id);assert.deepEqual(c.fields,u.fields);assert.deepEqual(c.steps.map(x=>x.id),u.steps.map(x=>x.id));const old=c.compatibleVersions?.[0];assert.ok(old);const rec=M.envelope(old,{step:old.steps[0].id,fields:[],tool:null},id,'2026-10-28T12:00:00Z');assert.equal(M.parse(JSON.stringify(rec),catalog).ok,true);}
 }
});
