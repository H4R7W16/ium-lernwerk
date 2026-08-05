import { mkdtemp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { afterEach, describe, expect, test } from 'vitest';
import {
  readExperienceContent,
  validateExperienceValue,
} from '../../scripts/validate-experience-content.js';

const productionModule = resolve('modules/IUM-5-CORE-05');
const temporaryDirectories: string[] = [];

afterEach(async () => {
  await Promise.all(temporaryDirectories.splice(0).map((path) => rm(path, { recursive: true, force: true })));
});

async function temporaryModule(value?: unknown, raw?: string): Promise<string> {
  const directory = await mkdtemp(join(tmpdir(), 'ium-experience-'));
  temporaryDirectories.push(directory);
  await mkdir(join(directory, 'lernumgebung'), { recursive: true });
  if (raw !== undefined) {
    await writeFile(join(directory, 'lernumgebung', 'experience.json'), raw, 'utf8');
  } else if (value !== undefined) {
    await writeFile(
      join(directory, 'lernumgebung', 'experience.json'),
      `${JSON.stringify(value, null, 2)}\n`,
      'utf8',
    );
  }
  return directory;
}

async function productionValue(): Promise<Record<string, any>> {
  return JSON.parse(await readFile(
    join(productionModule, 'lernumgebung', 'experience.json'),
    'utf8',
  )) as Record<string, any>;
}

async function countNamedFiles(directory: string, name: string): Promise<number> {
  let count = 0;
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) count += await countNamedFiles(path, name);
    else if (entry.name === name) count += 1;
  }
  return count;
}

test('loads one closed production contract for all three reference situations', async () => {
  const content = await readExperienceContent(productionModule);

  expect(await countNamedFiles(productionModule, 'experience.json')).toBe(1);
  expect(content.schemaVersion).toBe(1);
  expect(content.moduleId).toBe('IUM-5-CORE-05');
  expect(content.terminologyVersion).toBe('lxp04-1');
  expect(content.start.primaryAction.label).toBe('Mit der Vermutung beginnen');
  expect(content.actions.map((entry) => entry.id)).toEqual(expect.arrayContaining([
    'orientation', 'prediction', 'run', 'evidence', 'revision', 'secure', 'transfer', 'reentry',
  ]));
  expect(content.checkpoints.map((entry) => entry.id)).toEqual(expect.arrayContaining([
    'checkpoint-comparison', 'checkpoint-transfer',
  ]));
  expect(content.evidenceCards.map((entry) => entry.actionKind)).toEqual(expect.arrayContaining([
    'predict-test', 'create-revise', 'analyze-judge', 'secure-transfer',
  ]));
});

test('uses only known IUM5 phase references', async () => {
  const content = await readExperienceContent(productionModule);
  const phaseReferences = content.tasks.flatMap((task) => task.materialRefs)
    .filter((reference) => reference.startsWith('phase:'));

  expect(phaseReferences.length).toBeGreaterThan(0);
  expect(phaseReferences).not.toContain('phase:unknown');
});

test('keeps learner-facing content free of markup, scripts, tracking keys and URLs', async () => {
  const value = await productionValue();
  const result = validateExperienceValue(value, 'IUM-5-CORE-05');

  expect(result.ok).toBe(true);
  expect(JSON.stringify(value)).not.toMatch(/<[^>]+>|https?:\/\/|utm_|tracking|analytics/i);
});

describe('closed validator failures', () => {
  test('reports a missing file with its module-relative path', async () => {
    const directory = await temporaryModule();
    await expect(readExperienceContent(directory)).rejects.toThrow(/lernumgebung\/experience\.json.*missing/i);
  });

  test('reports malformed JSON', async () => {
    const directory = await temporaryModule(undefined, '{not-json');
    await expect(readExperienceContent(directory)).rejects.toThrow(/lernumgebung\/experience\.json.*JSON/i);
  });

  test.each([
    ['schemaVersion', 2, /\$\.schemaVersion/],
    ['terminologyVersion', 'lxp99', /\$\.terminologyVersion/],
  ])('rejects unsupported %s', async (key, invalidValue, pathPattern) => {
    const value = await productionValue();
    value[key] = invalidValue;
    const directory = await temporaryModule(value);
    await expect(readExperienceContent(directory)).rejects.toThrow(pathPattern);
  });

  test('rejects an unknown phase reference', async () => {
    const value = await productionValue();
    value.tasks[0].materialRefs = ['phase:unknown'];
    const directory = await temporaryModule(value);
    await expect(readExperienceContent(directory)).rejects.toThrow(/\$\.tasks\[0\]\.materialRefs\[0\].*unknown phase/i);
  });

  test('rejects duplicate action identifiers', async () => {
    const value = await productionValue();
    value.actions[1].id = value.actions[0].id;
    const directory = await temporaryModule(value);
    await expect(readExperienceContent(directory)).rejects.toThrow(/duplicate identifier/i);
  });

  test('rejects unknown properties', async () => {
    const value = await productionValue();
    value.tracking = true;
    const directory = await temporaryModule(value);
    await expect(readExperienceContent(directory)).rejects.toThrow(/\$\.tracking.*unknown field/i);
  });

  test('rejects learner copy beyond the code-point limit', async () => {
    const value = await productionValue();
    value.supports[0].content = 'ä'.repeat(1_201);
    const directory = await temporaryModule(value);
    await expect(readExperienceContent(directory)).rejects.toThrow(/\$\.supports\[0\]\.content.*1200 Unicode code points/i);
  });
});
