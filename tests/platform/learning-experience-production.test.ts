import { fileURLToPath } from 'node:url';
import { describe, expect, test } from 'vitest';
import { verifyLearningExperience } from '../../scripts/verify-learning-experience.js';

const repoRoot = fileURLToPath(new URL('../..', import.meta.url));

describe('learning-experience production gate', () => {
  test('closes every automated production contract', async () => {
    const report = await verifyLearningExperience(repoRoot);

    expect(report.checks.map((check) => check.id)).toEqual([
      'content-contracts',
      'component-contracts',
      'semantic-contrast',
      'directed-boundaries',
      'local-assets-only',
      'data-minimization',
      'reference-situations',
      'portability-boundaries',
      'documentation-contract',
    ]);
    expect(
      report.checks.filter((check) => !check.ok),
      JSON.stringify(report.checks, null, 2),
    ).toEqual([]);
    expect(report.ok).toBe(true);
  });
});
