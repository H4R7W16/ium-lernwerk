'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { prepareClass5Pages } = require('./build-class5-pages.cjs');

test('Pages liefert nur den Klasse-5-Einstieg und aktuelle Klasse-5-Dateien', () => {
  const assets = prepareClass5Pages();
  assert.deepEqual([...assets.keys()].filter(name => !name.startsWith('klasse5/')).sort(), ['index.html', 'sw.js']);
  for (const name of ['klasse5/index.html','klasse5/review.html','klasse5/identity.css','klasse5/brand/ium-lernwerk-5.png','klasse5/mantel-sw.js']) assert.ok(assets.has(name),name);
  for (const old of ['reinigungsfall.html','reinigungsfall-v2/index.html','selbstlernen/read.html','lernstudio/index.html','medienanalyse/index.html','quellenquest/index.html']) assert.equal(assets.has(old),false,old);
  assert.match(assets.get('index.html'), /url=klasse5\//);
  assert.match(assets.get('sw.js'), /registration\.unregister\(\)/);
});

test('alle lokalen HTML-Verweise bleiben im Klasse-5-Artefakt', () => {
  const assets = prepareClass5Pages();
  for (const [name,source] of assets) {
    if (!name.endsWith('.html')) continue;
    for (const [,reference] of source.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (/^(?:https?:|mailto:|tel:|data:|#)/i.test(reference)) continue;
      const target = new URL(reference, 'https://example.test/ium-lernwerk/' + name);
      assert.ok(target.pathname.startsWith('/ium-lernwerk/'), `${name}: ${reference} verlässt den Pages-Unterpfad`);
      const local = decodeURIComponent(target.pathname.slice('/ium-lernwerk/'.length));
      const file = local.endsWith('/') ? local + 'index.html' : local;
      assert.ok(assets.has(file), `${name}: ${reference} → ${file} fehlt`);
    }
  }
});
