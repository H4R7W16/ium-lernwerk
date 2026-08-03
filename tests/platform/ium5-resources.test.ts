import { readFile } from 'node:fs/promises';
import { parse } from 'yaml';
import { describe, expect, test } from 'vitest';
import { validateModuleManifest } from '../../packages/module-contract/src/index.js';
import { parseWorkbenchResources } from '../../packages/ium-5-core-05/src/index.js';

const readJson = async (path: string): Promise<unknown> =>
  JSON.parse(await readFile(path, 'utf8')) as unknown;

describe('IUM-5-CORE-05 resources', () => {
  test('binds the approved manifest exactly', async () => {
    const manifest = parse(
      await readFile('modules/IUM-5-CORE-05/module.yaml', 'utf8'),
    ) as Record<string, any>;
    expect(validateModuleManifest(manifest).ok).toBe(true);
    expect(manifest).toMatchObject({
      id: 'IUM-5-CORE-05',
      version: '0.1.0',
      status: 'working',
      grade: 5,
      kind: 'core',
      strands: ['STRAND-A'],
      time: {
        minLessons: 5,
        maxLessons: 6,
        contractId: 'TC-IUM-5-CORE-05',
      },
      prerequisites: ['IUM-5-CORE-01'],
      components: ['algorithm-workbench'],
      offline: { core: true, externalResources: [] },
    });
    expect(manifest.curriculum.competencyIds).toEqual([
      'LH26-E-PROG-002',
      'LH26-E-ALG-001',
      'LH26-E-ALG-002',
      'LH26-E-ALG-003',
      'LH26-E-ALG-004',
    ]);
    expect(manifest.media.analogMaterials).toEqual([]);

    const timeModel = await readJson('roadmap/time-model.json') as {
      moduleContracts: readonly Record<string, unknown>[];
    };
    const timeContract = timeModel.moduleContracts.find(
      (contract) => contract.moduleId === 'IUM-5-CORE-05',
    );
    expect(timeContract).toMatchObject({
      id: 'TC-IUM-5-CORE-05',
      pilotRequired: true,
      status: 'working',
    });
  });

  test('contains exact 225/270 minute paths and ten valid scenarios', async () => {
    const content = await readJson(
      'modules/IUM-5-CORE-05/lernumgebung/content.json',
    );
    const scenarios = await readJson(
      'modules/IUM-5-CORE-05/lernumgebung/scenarios.json',
    );
    const result = parseWorkbenchResources(content, scenarios);
    expect(result.ok).toBe(true);
    if (!result.ok) {
      return;
    }
    expect(result.value.content.paths.regular.totalMinutes).toBe(225);
    expect(result.value.content.paths.extended.totalMinutes).toBe(270);
    expect(result.value.scenarios.map((entry) => entry.scenario.id)).toEqual([
      'worked-sequence',
      'error-order',
      'error-turn',
      'error-missing-step',
      'error-repeat-count',
      'product-a',
      'product-b',
      'product-c',
      'repair-standard',
      'extended-inherited',
    ]);

    const timeModel = await readJson('roadmap/time-model.json') as {
      moduleContracts: readonly {
        moduleId: string;
        pathBudgets: readonly { pathId: string; phaseBudgets: readonly { minutes: number }[] }[];
      }[];
    };
    const contract = timeModel.moduleContracts.find(
      (entry) => entry.moduleId === 'IUM-5-CORE-05',
    );
    expect(contract?.pathBudgets.find((path) => path.pathId === 'regular')
      ?.phaseBudgets.map((phase) => phase.minutes)).toEqual([15, 20, 35, 45, 55, 35, 20]);
    expect(contract?.pathBudgets.find((path) => path.pathId === 'extended')
      ?.phaseBudgets.map((phase) => phase.minutes)).toEqual([15, 20, 35, 60, 75, 40, 25]);

    const extension = result.value.content.activities.find(
      (activity) => activity.id === 'extended-repair',
    );
    expect(extension?.scenarioIds).toEqual(['extended-inherited']);
    expect(extension?.instruction.toLocaleLowerCase('de-DE')).toMatch(/vorhers|ausführ/);
    expect(extension?.instruction.toLocaleLowerCase('de-DE')).toMatch(/abweich|lokalis/);
    expect(extension?.instruction.toLocaleLowerCase('de-DE')).toMatch(/hypothese/);
    expect(extension?.instruction.toLocaleLowerCase('de-DE')).toMatch(/revid/);
    expect(extension?.instruction.toLocaleLowerCase('de-DE')).toMatch(/vergleich/);
  });

  test('rejects unknown fields, learner-facing solutions and broken references', async () => {
    const content = await readJson(
      'modules/IUM-5-CORE-05/lernumgebung/content.json',
    ) as Record<string, unknown>;
    const scenarios = await readJson(
      'modules/IUM-5-CORE-05/lernumgebung/scenarios.json',
    );

    expect(parseWorkbenchResources({ ...content, score: 10 }, scenarios).ok)
      .toBe(false);
    expect(parseWorkbenchResources({
      ...content,
      transferCases: [{
        id: 'navigation',
        title: 'Navigation',
        description: 'Wegbeschreibung',
        expectedClassification: 'algorithmic-system',
      }],
    }, scenarios).ok).toBe(false);

    const activities = content.activities as readonly Record<string, unknown>[];
    expect(parseWorkbenchResources({
      ...content,
      activities: [
        { ...activities[0], scenarioIds: ['unknown-scenario'] },
        ...activities.slice(1),
      ],
    }, scenarios).ok).toBe(false);
  });

  test('maps every competency and records asset and handbook evidence', async () => {
    const mapping = await readJson(
      'modules/IUM-5-CORE-05/curriculum-mapping.json',
    ) as { records: readonly Record<string, any>[] };
    expect(mapping.records.map((record) => record.competencyId)).toEqual([
      'LH26-E-PROG-002',
      'LH26-E-ALG-001',
      'LH26-E-ALG-002',
      'LH26-E-ALG-003',
      'LH26-E-ALG-004',
    ]);
    for (const record of mapping.records) {
      expect(record.segmentIds.length).toBeGreaterThan(0);
      expect(record.productEvidence).toBeTruthy();
    }
    const licenses = await readJson(
      'modules/IUM-5-CORE-05/assets/licenses.json',
    ) as { assets: unknown[] };
    expect(licenses.assets).toEqual([expect.objectContaining({
      path: 'delivery-robot.svg',
      license: 'CC-BY-SA-4.0',
    })]);
    const handbook = await readFile(
      'modules/IUM-5-CORE-05/handbuch/lehrkraeftehandbuch.md',
      'utf8',
    );
    for (const heading of [
      'Fachlicher Hintergrund',
      'Voraussetzungen',
      'Fünf Unterrichtseinheiten',
      'Sechs Unterrichtseinheiten',
      'Erwartbare Fehler',
      'Accessibility',
      'Datenschutz und Export',
      'Status- und Einsatzgrenze',
    ]) {
      expect(handbook).toContain(heading);
    }
  });

  test('keeps content free of gamification and diagnostic collection', async () => {
    const source = await readFile(
      'modules/IUM-5-CORE-05/lernumgebung/content.json',
      'utf8',
    );
    expect(source).not.toMatch(
      /punkte|badge|rangliste|level|telemetrie|diagnoseprofil/i,
    );
  });
});
