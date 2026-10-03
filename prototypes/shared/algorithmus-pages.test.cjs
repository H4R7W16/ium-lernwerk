const test=require('node:test'),assert=require('node:assert/strict');
const S=require('../m06-lernstudio/studio-model.js');
const P=require('../m06-lernstudio/studio-learning.js');
const assets=()=>require('../m06-reinigungsfall/build.cjs').prepare();
test('Lernauftrag bestimmt die hervorgehobene Ausführung ohne Schritte zu sperren',()=>{
 for(const id of ['start','repair','return'])assert.equal(P.primaryAction(id),'step');
 assert.equal(P.primaryAction('after'),'cycle');
 for(const id of ['loop','example','rows','switch','own','check','transfer'])assert.equal(P.primaryAction(id),'play');
});
test('Materialauswahl führt einmal zu jedem vollständigen eigenständigen Blatt',()=>{
 const a=assets(),index=a.get('klasse5/lernstudio/material.html');
 assert.equal((index.match(/href="baustein-/g)||[]).length,11);
 assert.doesNotMatch(index,/class="guide-nav"/);
 for(const id of S.order){
  assert.equal((index.match(new RegExp('href="baustein-'+id+'\\.html"','g'))||[]).length,1);
  const sheet=a.get('klasse5/lernstudio/baustein-'+id+'.html');
  for(const text of ['Dein Auftrag','Eine gute Erklärung','Mögliche Lösung'])assert.ok(sheet.includes(text),id+': '+text);
  assert.ok(sheet.includes(P.lesson(id).solution.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;')),id+' solution');
 }
});
test('Nachschlagen erhält alle Direktanker und die frühe Rückkehr zur Aufgabe',()=>{
 const html=assets().get('klasse5/lernstudio/wissen.html');
 assert.ok(html.indexOf('data-lw-return')<html.indexOf('id="start"'));
 for(const id of [...S.order,'wege','begriffe'])assert.ok(html.includes('id="'+id+'"'),id);
 assert.match(html,/Was möchtest du verstehen/);
});
