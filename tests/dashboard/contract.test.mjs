import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { parseRegister, validateEditorial, project, atomicWrite, githubEvidence, freshness } from '../../packages/project-status/index.mjs';

const seed = JSON.parse(readFileSync(new URL('../../roadmap/v2/dashboard/editorial-seed.json', import.meta.url)));
const copy = () => structuredClone(seed);
test('accepts V2 editorial source and rejects duplicate YAML keys', () => {
  validateEditorial(copy());
  assert.throws(() => parseRegister('<!-- IUM-PROJECT-STATUS:START -->\n```yaml\na: 1\na: 2\n```\n<!-- IUM-PROJECT-STATUS:END -->'));
});
for (const [label, mutate] of [
  ['unknown work status', d => d.currentFocus.workStatus = 'green'],
  ['duplicate stream', d => d.streams[1].id = 'foundation'],
  ['missing mandatory stream', d => d.streams.pop()],
  ['missing maturity axis', d => delete d.streams[0].maturity.usage],
  ['unknown maturity', d => d.streams[0].maturity.pilot = 'probably-done'],
  ['unknown experience axis', d => d.experienceAxes[0].id = 'score'],
  ['duplicate evidence', d => d.evidence[1].id = d.evidence[0].id],
  ['unknown evidence reference', d => d.streams[0].evidenceIds.push('missing')],
  ['internal evidence used by presentation', d => d.streams[0].evidenceIds.push('internal-review')],
  ['absolute path in prose', d => d.summary = 'C:\\Users\\Private\\file.md'],
  ['traversal evidence', d => d.evidence[0].target = '../secret.md'],
  ['invalid visibility', d => d.evidence[0].visibility = 'public'],
  ['abbreviated SHA', d => d.technicalEvidence.commit = '60c7d0a'],
  ['unknown property', d => d.overallProgress = 100],
]) test(`fails closed: ${label}`, () => { const d = copy(); mutate(d); assert.throws(() => validateEditorial(d)); });

test('presentation removes internal evidence before serialization; uncertainties remain', () => {
  const d = copy(); d.evidence.find(e => e.visibility === 'internal').content = 'INTERNAL_SENTINEL';
  const p = project(d, 'presentation');
  assert.ok(!JSON.stringify(p).includes('INTERNAL_SENTINEL'));
  assert.equal(p.uncertainties.length, 4);
  assert.ok(project(d, 'internal').evidence.some(e => e.content === 'INTERNAL_SENTINEL'));
});
test('commit freshness does not mutate maturity and dirty is independent', () => {
  const d = copy(), before = structuredClone(d.streams);
  assert.equal(freshness(d.technicalEvidence, 'a'.repeat(40)), 'stale');
  assert.equal(freshness(d.technicalEvidence, d.technicalEvidence.commit), 'passed');
  assert.deepEqual(d.streams, before);
});
test('GitHub links require full SHA, remote reachability and identical committed bytes', () => {
  const sha = 'a'.repeat(40);
  assert.equal(githubEvidence(sha, 'docs/a.md', false, true), null);
  assert.equal(githubEvidence(sha, 'docs/a.md', true, false), null);
  assert.equal(githubEvidence('unknown', 'docs/a.md', true, true), null);
  assert.equal(githubEvidence(sha, 'docs/a.md', true, true), `https://github.com/H4R7W16/ium-lernwerk/blob/${sha}/docs/a.md`);
});
test('failed validation preserves the previous atomic snapshot byte for byte', () => {
  const dir = mkdtempSync(join(tmpdir(), 'ium-dashboard-')), file = join(dir, 'snapshot.json');
  writeFileSync(file, 'previous-valid-snapshot');
  assert.throws(() => atomicWrite(file, 'invalid', () => { throw new Error('invalid'); }));
  assert.equal(readFileSync(file, 'utf8'), 'previous-valid-snapshot');
  atomicWrite(file, 'next-valid-snapshot');
  assert.equal(readFileSync(file, 'utf8'), 'next-valid-snapshot');
});
