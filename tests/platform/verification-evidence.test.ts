import { spawnSync } from 'node:child_process';
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { expect, test } from 'vitest';
import { archiveBuild, createRunDirectory, browserEvidence } from '../../scripts/verification-evidence.js';

test('F03 archives immutable build bytes and binds every browser group to its actual build', () => {
  const run = createRunDirectory(resolve('reports/evidence-tests'), 'same-label');
  expect(createRunDirectory(resolve('reports/evidence-tests'), 'same-label')).not.toBe(run);
  const dist = resolve(run, 'fixture-dist'); mkdirSync(dist);
  writeFileSync(resolve(dist, 'index.html'), 'ROOT');
  const first = archiveBuild(run, dist, { revision: 'a'.repeat(40), profile: 'v2-development', base: '/' });
  writeFileSync(resolve(dist, 'index.html'), 'SUBPATH');
  const second = archiveBuild(run, dist, { revision: 'a'.repeat(40), profile: 'v2-development', base: '/ium-lernwerk/' });
  expect(first.sha256).not.toBe(second.sha256);
  expect(readFileSync(resolve(first.directory, 'files/index.html'), 'utf8')).toBe('ROOT');
  expect(JSON.parse(readFileSync(second.manifest, 'utf8'))).toMatchObject({ base: '/ium-lernwerk/', files: [{ path: 'index.html' }] });
  expect(() => browserEvidence(run, 'unbuilt', resolve(run, 'missing.json'))).toThrow();
});

test.runIf(process.env.IUM_TEST_EVIDENCE_BROWSER === '1')('F02 early Playwright failure artifacts survive a later successful group', () => {
  const run = createRunDirectory(resolve('reports/evidence-tests'), 'failure-then-pass');
  const dist = resolve(run, 'fixture-dist'); mkdirSync(dist); writeFileSync(resolve(dist, 'index.html'), 'PROBE');
  const build = archiveBuild(run, dist, { revision: 'b'.repeat(40), profile: 'fixture', base: '/' });
  const config = resolve(run, 'probe.config.cjs');
  writeFileSync(config, 'module.exports={testDir:__dirname,testMatch:"probe.spec.cjs",use:{trace:"retain-on-failure"}};');
  writeFileSync(resolve(run, 'probe.spec.cjs'), `const {test,expect}=require(${JSON.stringify(resolve('node_modules/@playwright/test'))});
test('artifact retention probe',async({page})=>{await page.setContent('<p>probe</p>');expect(process.env.PROBE_FAIL).toBe('no');});`);
  const invoke = (fail: boolean) => {
    const evidence = browserEvidence(run, 'same-group', build.manifest);
    const result = spawnSync(process.execPath, [resolve('node_modules/@playwright/test/cli.js'), 'test', '--config', config, ...evidence.args], {
      env: { ...process.env, ...evidence.env, PROBE_FAIL: fail ? 'yes' : 'no' }, encoding: 'utf8', timeout: 60_000,
    });
    expect(result.error).toBeUndefined();
    expect(result.status, result.stdout + result.stderr).toBe(fail ? 1 : 0);
    evidence.finish();
    return evidence;
  };
  const failed = invoke(true);
  const paths = readdirSync(resolve(failed.directory, 'test-results'), { recursive: true }).map(String);
  const trace = paths.find((path) => path.endsWith('trace.zip'))!;
  expect(trace).toBeTruthy();
  const original = readFileSync(resolve(failed.directory, 'test-results', trace));
  const passed = invoke(false);
  expect(failed.directory).not.toBe(passed.directory);
  expect(readFileSync(resolve(failed.directory, 'test-results', trace))).toEqual(original);
  expect(JSON.parse(readFileSync(resolve(failed.directory, 'results.json'), 'utf8')).stats.unexpected).toBe(1);
  expect(JSON.parse(readFileSync(resolve(passed.directory, 'results.json'), 'utf8')).stats.expected).toBe(1);
  expect(JSON.parse(readFileSync(resolve(failed.directory, 'group.json'), 'utf8'))).toMatchObject({ buildSha256: build.sha256, revision: 'b'.repeat(40) });
}, 120_000);
