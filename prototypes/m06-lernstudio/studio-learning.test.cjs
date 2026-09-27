'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const S = require('./studio-model.js');
const P = require('./studio-learning.js');
const rowPlan = 'wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]';

test('Ein richtiger Auswahlcheck ersetzt keinen eigenen ausgeführten Plan', () => {
  const s = S.fresh('own');
  S.answer('own', s, 2);
  assert.equal(P.evidence('own', s).kind, 'open');
  assert.equal(P.evidence('own', {...s, code: rowPlan}).kind, 'open');
  s.code = rowPlan; s.observed = true;
  assert.equal(P.evidence('own', s).kind, 'task');
  S.change(s, 'vor'); s.observed = true;
  assert.equal(P.evidence('own', s).kind, 'revise');
});

test('Ein beobachteter Wandstopp erfüllt den Arbeitsauftrag nicht', () => {
  const s = {...S.fresh('own'), code: 'wiederhole 4 [vor]', observed: true};
  assert.equal(P.evidence('own', s).kind, 'revise');
});

test('Prognose und ausgeschriebene Folge zählen erst nach passender Beobachtung', () => {
  const s = S.fresh('return');
  s.observed = true;
  assert.equal(P.evidence('return', s).kind, 'observed');
  s.prediction = [2,1,0];
  s.sequence = ['vor','links','vor','links','vor','links','rechts'];
  assert.equal(P.evidence('return', s).kind, 'task');
  s.prediction = [2,1,1];
  assert.equal(P.evidence('return', s).kind, 'observed');
});

test('Der Transfer weist erst nach beiden durchlaufenen Plänen einen Vergleich aus', () => {
  const s = S.fresh('transfer'); s.observed = true; s.compared = ['A'];
  assert.equal(P.evidence('transfer', s).kind, 'observed');
  s.compared.push('B');
  assert.equal(P.evidence('transfer', s).kind, 'compared');
});

test('Der Vergleich zeigt denselben Schritt, auch wenn ein Versuch schon gestoppt ist', () => {
  const pair = P.compare('own', 'wiederhole 4 [vor]', rowPlan, 6);
  assert.equal(pair.step, 6);
  assert.equal(pair.before.step, 4);
  assert.equal(pair.before.ended, true);
  assert.equal(pair.before.trace.error, 'wall');
  assert.deepEqual(pair.before.trace.pos, [4,3,1]);
  assert.equal(pair.after.step, 6);
  assert.deepEqual(pair.after.trace.pos, [4,2,3]);
});

test('Reihen- und Spaltenbeispiel erfüllen denselben Flächenauftrag mit verschiedenen Wegen', () => {
  for (const code of [P.examples.rows, P.examples.columns]) {
    const r = S.run('own', code);
    assert.equal(r.status, 'complete');
    assert.equal(r.cleaned.length, 12);
    assert.deepEqual(r.missing, []);
  }
  assert.equal(S.run('own', P.examples.rows).trace.length - 1, 15);
  assert.equal(S.run('own', P.examples.columns).trace.length - 1, 18);
});
