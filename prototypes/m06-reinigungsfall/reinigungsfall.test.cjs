const { test } = require('node:test');
const assert = require('node:assert/strict');
const { parse, run, rooms } = require('./reinigungsfall-core.js');
test('turning cleans no new field; start counts once', () => {
  const r = run(rooms.small, parse('links\nrechts'));
  assert.deepEqual(r.end, [1,2,1]);
  assert.equal(r.cleaned.length, 1);
  assert.equal(r.success, false);
});
test('complete body repeats in order and covers the small room', () => {
  const r = run(rooms.small, parse('wiederhole 4 [vor; links]'));
  assert.equal(r.trace.length, 9);
  assert.equal(r.success, true);
  assert.deepEqual(r.end, [1,2,1]);
});
test('misgrouped body stops at boundary without cleaning another field', () => {
  const r = run(rooms.main, parse('wiederhole 4 [vor; vor]\nlinks'));
  assert.equal(r.status, 'wall');
  assert.equal(r.trace.length, 4);
  assert.deepEqual(r.end, [3,3,1]);
  assert.equal(r.cleaned.length, 3);
  assert.equal(r.trace[3].action, 'vor');
});
test('returning to start is insufficient: perimeter leaves the centre', () => {
  const r = run(rooms.main, parse('wiederhole 4 [vor; vor; links]'));
  assert.equal(r.status, 'complete');
  assert.equal(r.success, false);
  assert.deepEqual(r.end, [1,3,1]);
  assert.deepEqual(r.missing, ['2,2']);
  assert.equal(r.trace.length, 13);
});
test('targeted repair reaches centre and preserves previous run', () => {
  const before = run(rooms.main, parse('wiederhole 4 [vor; vor; links]'));
  const after = run(rooms.main, parse('wiederhole 4 [vor; vor; links]\nvor\nlinks\nvor'));
  assert.equal(before.cleaned.length, 8);
  assert.equal(after.cleaned.length, 9);
  assert.equal(after.success, true);
  assert.deepEqual(after.end, [2,2,0]);
  assert.equal(after.trace[15].cleaned.length, 9);
});
test('own room admits different complete routes within command limits', () => {
  const a = run(rooms.own, parse('wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]'));
  const b = run(rooms.own, parse('links\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]'));
  assert.equal(a.success, true);
  assert.deepEqual(a.end, [4,1,1]);
  assert.equal(a.trace.length, 16);
  assert.equal(b.success, true);
});
test('invalid input is rejected without silently dropping commands', () => {
  for (const code of ['', 'warten', 'vor\nfliegen', 'wiederhole 1 [vor]', 'wiederhole 10 [vor]',
    'wiederhole 2 [vor;vor;vor;vor;vor;links]', 'wiederhole 2 [wiederhole 2 [vor]]', 'vor danach links']) {
    assert.throws(() => parse(code), undefined, code);
  }
});
test('coverage alone cannot turn an overlong or colliding run into success', () => {
  const r = run(rooms.small, parse('wiederhole 4 [vor; links]\nwiederhole 9 [links;links;links;links;links]\nwiederhole 9 [links;links;links;links;links]\nlinks\nlinks\nlinks'));
  assert.equal(r.status, 'limit');
  assert.equal(r.success, false);
  const collision = run(rooms.small, parse('wiederhole 4 [vor; links]\nvor\nvor'));
  assert.equal(collision.cleaned.length, 4);
  assert.equal(collision.success, false);
});
