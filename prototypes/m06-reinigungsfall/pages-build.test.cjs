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
 assert.equal(assets.get('selbstlernen/index.html'),require('../m06-selbstlernen/render.cjs').render());
 for(const name of ['app.css','app.js','model.js','cleaning-core.js'])assert.ok(assets.has('selbstlernen/'+name));
});
