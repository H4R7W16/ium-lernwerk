'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const { addArbeitsstellen } = require('./arbeitsstellen.cjs');

const root = 'https://lernwerk.invalid/ium-lernwerk/klasse6/';
const steps = ['grundnetz', 'einstieg'];
const shell = main => '<head></head><body><header class="lw-shell-header"></header><main>' + main + '</main></body>';
const files = new Map(steps.map(id => ['klasse6/netze/schritt-' + id + '.html', shell(
  '<section class="lw-content-block"><h2>Versuch ' + id + '</h2><label for="answer-' + id + '-versuch">Vorhersage</label>'
  + '<a href="wissen.html#rollen">Rollen erklären</a></section>'
)]));
files.set('klasse6/netze/wissen.html', shell('<a href="index.html" data-lw-return>Zurück</a><h2 id="rollen">Rollen</h2>'));
const pages = addArbeitsstellen(files);

// Nur das fertig gerenderte Verweisziel betrachten. Das Szenario enthält weder Lernstand noch Browser-Speicher.
function readReturn(query) {
  let inserted;
  const heading = {matches: () => true, insertAdjacentElement: (_, link) => { inserted = link; }};
  const main = {contains: node => node === heading};
  const location = new URL('netze/wissen.html' + query + '#rollen', root);
  const document = {
    currentScript: {src: root + 'arbeitsstellen.js'},
    querySelectorAll: () => [],
    querySelector: selector => selector === 'main' ? main : null,
    getElementById: () => heading,
    createElement: () => ({setAttribute() {}}),
  };
  vm.runInNewContext(pages.get('klasse6/arbeitsstellen.js'), { URL, location, document, window: { addEventListener() {} } });
  return inserted;
}

test('Eine Wissensüberschrift behält für zwei Aufgaben ihre jeweilige Arbeitsstelle', () => {
  for (const id of steps) {
    const file = 'netze/schritt-' + id + '.html';
    const anchor = 'arbeitsstelle-' + id + '-versuch';
    const from = file + '#' + anchor;
    assert.ok(pages.get('klasse6/' + file).includes('id="' + anchor + '"'));
    const back = readReturn('?arbeitsstelle=' + encodeURIComponent(from));
    assert.equal(back.href, new URL(from, root).href);
    assert.match(back.textContent, new RegExp('Versuch ' + id));
  }
});

test('Direkteinstieg und unbekannte oder mehrdeutige Herkunft behalten den normalen Lesepfad', () => {
  const valid = encodeURIComponent('netze/schritt-einstieg.html#arbeitsstelle-einstieg-versuch');
  for (const query of ['', '?arbeitsstelle=https%3A%2F%2Fexample.org', '?arbeitsstelle=netze%2Fschritt-einstieg.html%23fremd',
    '?arbeitsstelle=' + valid + '%23zusatz', '?arbeitsstelle=' + valid + '&arbeitsstelle=' + valid]) {
    assert.equal(readReturn(query), undefined);
  }
  assert.match(pages.get('klasse6/netze/wissen.html'), /href="index.html" data-lw-return/);
});
