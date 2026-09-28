const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const file=path.join(__dirname,'model.js'),M=fs.existsSync(file)?require(file):{};
test('Unbeantwortete und ungültige Zuordnungen erhalten keine positive Rückmeldung',()=>{
 assert.equal(typeof M.assess,'function');
 for(const a of [{},{verdict:'belegt'},{verdict:'x',evidence:'C1'}])assert.equal(M.assess('beete',a).status,'open');
});
test('Ein richtiges Urteil mit einem unpassenden Beleg muss überarbeitet werden',()=>{
 assert.equal(typeof M.assess,'function');
 assert.equal(M.assess('wiese',{verdict:'widerlegt',evidence:'B1'}).status,'evidence');
 assert.equal(M.assess('wiese',{verdict:'widerlegt',evidence:'C2'}).status,'match');
});
test('Nicht belegte Zukunftsaussagen sind offen und nicht widerlegt',()=>{
 assert.equal(typeof M.assess,'function');
 assert.equal(M.assess('zukunft',{verdict:'offen',evidence:'C3'}).status,'match');
 assert.equal(M.assess('zukunft',{verdict:'widerlegt',evidence:'C3'}).status,'verdict');
});
test('Ein älterer Vorschlag belegt weiterhin den damaligen Wunsch',()=>{
 assert.equal(typeof M.assess,'function');
 assert.equal(M.assess('wunsch',{verdict:'belegt',evidence:'B1'}).status,'match');
 assert.equal(M.assess('wunsch',{verdict:'belegt',evidence:'C2'}).status,'evidence');
});
test('Beim Transfer zählt der genaue Inhalt auch gegenüber einem neueren Chat',()=>{
 assert.equal(typeof M.assess,'function');
 assert.equal(M.assess('tag',{verdict:'widerlegt',evidence:'D2'},'transfer').status,'match');
 assert.equal(M.assess('tag',{verdict:'belegt',evidence:'E1'},'transfer').status,'verdict');
 assert.equal(M.assess('computer',{verdict:'offen',evidence:'none'},'transfer').status,'match');
});
test('Quellenauswahl hängt von der Frage ab',()=>{
 assert.equal(typeof M.checkSource,'function');
 assert.equal(M.checkSource('beschluss','C').status,'match');
 assert.equal(M.checkSource('wunsch','B').status,'match');
 assert.equal(M.checkSource('wunsch','C').status,'revise');
 assert.equal(M.checkSource('beschluss','').status,'open');
});
test('Materialbausteine enthalten sämtliche benötigten Quellen auch ohne JavaScript',()=>{
 const renderer=path.join(__dirname,'render.cjs');assert.ok(fs.existsSync(renderer));
 const R=require(renderer),C=require('./content.js');
 for(const step of C.steps){
  const html=R.material(step.id);
  assert.ok(html.includes(step.title));
  for(const id of step.sources)for(const line of C.sources[id].lines)assert.ok(html.includes(line.text),step.id+': '+line.id);
  assert.ok(!html.includes('<script'));
 }
 assert.throws(()=>R.material('unbekannt'));
});
test('Der Pages-Build veröffentlicht den neuen Weg und alle Direktmaterialien',()=>{
 const assets=require('../m06-reinigungsfall/build.cjs').prepare();
 for(const f of ['index.html','app.js','content.js','model.js','style.css','wissen.html','lehrkraft.html','material.html','baustein-auftrag.html','baustein-quellen.html','baustein-belege.html','baustein-antwort.html','baustein-transfer.html'])
 assert.ok(assets.has('quellenquest/'+f),f);
});

