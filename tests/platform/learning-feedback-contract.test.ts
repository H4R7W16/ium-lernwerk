import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { describe, expect, test } from 'vitest';
import { parseExperienceContent } from '@ium/learning-experience';

async function productionExperience(): Promise<Record<string, any>> {
  return JSON.parse(await readFile(
    resolve('modules/IUM-5-CORE-05/lernumgebung/experience.json'),
    'utf8',
  )) as Record<string, any>;
}

describe('evidence-led feedback contract', () => {
  test('requires result, evidence, criterion, interpretation and next check', async () => {
    const value = await productionExperience();
    delete value.feedback[0].nextCheck;

    const result = parseExperienceContent(value);
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.errors).toEqual(expect.arrayContaining([
      expect.objectContaining({ path: '$.feedback[0].nextCheck', code: 'missing_field' }),
    ]));
  });

  test.each(['Richtig', 'Falsch', '8/10', '92 %'])('rejects bare result label %s', async (label) => {
    const value = await productionExperience();
    value.feedback[0].result = label;

    const result = parseExperienceContent(value);
    expect(result.ok).toBe(false);
  });

  test('rejects duplicate feedback IDs and dangling evidence or support references', async () => {
    const value = await productionExperience();
    value.feedback[1].id = value.feedback[0].id;
    value.feedback[0].evidenceRef = 'EVC-UNKNOWN';
    value.feedback[0].strategySupportId = 'SUP-UNKNOWN';

    const result = parseExperienceContent(value);
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.errors.map((entry) => entry.code)).toEqual(
      expect.arrayContaining(['duplicate_id', 'invalid_value']),
    );
  });

  test('publishes all six semantic learning-cycle components', async () => {
    const names = [
      'PredictionForm',
      'SemanticModelView',
      'EvidenceView',
      'EvidenceFeedback',
      'RevisionCompare',
      'SupportDisclosure',
    ];
    const sources = await Promise.all(names.map((name) => readFile(
      resolve(`packages/learning-experience/src/components/${name}.astro`),
      'utf8',
    )));
    const combined = sources.join('\n');

    expect(combined).toContain('<fieldset');
    expect(combined).toContain('data-evidence-feedback');
    expect(combined).toContain('Vorher');
    expect(combined).toContain('Nachher');
    expect(combined).toContain('preservesAction');
    expect(combined).not.toMatch(/data-save|connectivity|aria-live/i);
  });
});
