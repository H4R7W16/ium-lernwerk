const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { prepare } = require('./build.cjs');

test('Pages bietet aktuellen Einstieg und erhält beide unabhängigen Fassungen', () => {
  const assets = prepare();
  assert.ok(assets.size >= 16);
  assert.match(assets.get('index.html'), /url=reinigungsfall-v2\//);
  assert.match(assets.get('reinigungsfall-v2/index.html'), /href="\.\.\/reinigungsfall.html"/);
  assert.equal(assets.get('reinigungsfall.html'), fs.readFileSync(path.join(__dirname,'reinigungsfall.html'),'utf8'));
  assert.equal(assets.get('reinigungsfall-v2/lesson-model.js'), fs.readFileSync(path.join(__dirname,'../m06-reinigungsfall-v2/lesson-model.js'),'utf8'));
});
test('Veröffentlichung enthält keine Tests, lokalen Nachweise oder Lernstände', () => {
  const assets = prepare();
  assert.ok(![...assets.keys()].some(name=> /test|QA|IMPLEMENTATION|\.json$/i.test(name)));
  for (const source of assets.values()) assert.doesNotMatch(source,/C:[\\/]Users[\\/]/i);
  assert.match(assets.get('reinigungsfall-v2/index.html'), /name="robots" content="noindex"/);
});

test('Selbstlernstrecke wird aus einer Quelle gebaut und hat alle Laufzeitdateien',()=>{
 const assets=prepare();
 assert.equal(assets.get('selbstlernen/index.html'),require('../m06-selbstlernen/render.cjs').render().replaceAll('../m06-reinigungsfall-v2/index.html','../reinigungsfall-v2/index.html').replaceAll('../m06-lernfassung3/index.html','../lernfassung-3/index.html').replaceAll('../m06-lernwerkstatt/index.html','../lernwerkstatt/index.html'));
 for(const name of ['app.css','app.js','model.js','cleaning-core.js'])assert.ok(assets.has('selbstlernen/'+name));
});

test('Pages stellt die dritte Fassung mit erreichbaren Varianten und Lesefassung bereit',()=>{
 const assets=prepare();
 assert.ok(assets.has('lernfassung-3/index.html'));
 assert.ok(assets.has('lernfassung-3/read.html'));
 for(const file of ['reinigungsfall-v2/index.html','selbstlernen/index.html','selbstlernen/read.html'])
  assert.match(assets.get(file),/href="\.\.\/lernfassung-3\/index.html"/);
 const third=assets.get('lernfassung-3/index.html'),reading=assets.get('lernfassung-3/read.html');
 for(const id of ['a6-first','a7-first','a7-last','plan-code'])assert.match(third,new RegExp('id="'+id+'"'));
 assert.equal((third.match(/data-stage-panel=/g)||[]).length,4);
 assert.match(third,/data-storage-key="ium-schleifen-planung-v3"/);
 assert.doesNotMatch(reading,/<script|<select|<input[^>]*type="number"/);
 assert.equal((reading.match(/data-stage-panel=/g)||[]).length,4);
 assert.match(reading,/Eine andere gültige Lösung: spaltenweise/);
 for(const f of ['journey.js','journey-model.js','journey.css'])assert.ok(assets.has('lernfassung-3/'+f));
});

test('Lernwerkstatt ist unabhängig erreichbar und hat alle Simulationsdateien',()=>{
 const assets=prepare();
 for(const f of ['index.html','workshop.js','workshop-model.js','workshop.css'])assert.ok(assets.has('lernwerkstatt/'+f));
 for(const f of ['reinigungsfall-v2/index.html','selbstlernen/index.html','selbstlernen/read.html','lernfassung-3/index.html'])
  assert.match(assets.get(f),/href="\.\.\/lernwerkstatt\/index.html"/);
 const page=assets.get('lernwerkstatt/index.html');
 assert.match(page,/src="\.\.\/selbstlernen\/model.js"/);
 assert.match(page,/src="\.\.\/selbstlernen\/cleaning-core.js"/);
});
test('Lernstudio veröffentlicht nur die zusätzlichen Laufzeitdateien und löst alle Modellverweise auf',()=>{
 const assets=prepare();
 for(const f of ['index.html','studio.css','studio.js','studio-model.js'])assert.ok(assets.has('lernstudio/'+f));
 const html=assets.get('lernstudio/index.html'),js=assets.get('lernstudio/studio.js');
 assert.match(html,/src="\.\.\/lernwerkstatt\/workshop-model.js"/);
 assert.match(html,/src="\.\.\/selbstlernen\/model.js"/);
 assert.doesNotMatch(js,/\.\.\/m06-/);
 assert.match(assets.get('lernwerkstatt/workshop.js'),/href="\.\.\/lernstudio\/index.html"/);
});
