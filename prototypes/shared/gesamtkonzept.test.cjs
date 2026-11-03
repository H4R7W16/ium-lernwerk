'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs');
test('reguläre Recherche führt sechs Hauptstationen und einen getrennten späteren Abruf',()=>{
 const p=A.load(5).find(p=>p.area==='recherche');
 assert.deepEqual(p.steps.filter(s=>s.timing!=='later').map(s=>s.id),['frage','suchplan','suchen','pruefen','ordnen','transfer']);
 assert.equal(p.steps.filter(s=>s.timing==='later').length,1);
 const workbook=p.media.find(m=>m.id==='notiz');assert.equal(workbook.printText,fs.readFileSync(path.join(__dirname,'inhalte',workbook.file),'utf8'));assert.equal(p.workbook,workbook.printText);assert.match(workbook.printText,/drei wichtige Informationen/);assert.match(workbook.printText,/zwei Überschriften/);assert.doesNotMatch(workbook.printText,/MEINE INFOKARTE|wächst zur Inhaltsentwurf/);
 const out=R.render(p);assert.ok(out.has('leas-weg-bildfolge.html'));assert.match(out.get('index.html'),/assets\/recherche\/recherche-notiz.txt/);
});
test('alle bisherigen Lernziel-IDs der regulären Klasse5/6-Pakete bleiben zugeordnet',()=>{
 for(const grade of [5,6])for(const p of A.load(grade)){
  const old=require('./legacy-catalog-'+grade+'.json').find(u=>u.id===p.id);
  assert.ok(old,p.id);assert.deepEqual([...p.curriculum.goalIds].sort(),[...old.curriculum.goalIds].sort(),p.id);
 }
});
test('gemeinsame Übersicht enthält alle17Reihen und die unveränderten getrennten Jahreskonten',()=>{
 const f=path.join(__dirname,'gesamtkonzept.json');assert.ok(fs.existsSync(f),'Gemeinsame Übersicht fehlt');
 const d=JSON.parse(fs.readFileSync(f));assert.equal(d.rows.length,17);
 for(const [grade,core,total]of [[5,1350,1710],[6,1305,1710],[7,1215,1620]]){
  assert.equal(d.rows.filter(r=>r.grade===grade).reduce((s,r)=>s+r.minutes,0),core);
  assert.equal(Object.values(d.budgets[grade]).reduce((s,n)=>s+n,0),total);
 }
 assert.equal(d.rows.find(r=>r.id==='G7-ALG').minutes,405);
});
