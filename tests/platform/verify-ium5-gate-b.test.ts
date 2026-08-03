import { afterEach, expect, test, vi } from 'vitest';
import {
  createGateBVerificationSteps,
  runGateBVerification,
} from '../../scripts/verify-ium5-gate-b.js';

afterEach(() => {
  vi.unstubAllEnvs();
});

test('Gate-B verifier has the closed eight-step order and isolates preview variables', () => {
  const steps = createGateBVerificationSteps({
    npmCli: '/npm-cli.js',
    node: '/node',
    python: '/python',
    buildRevision: '1'.repeat(40),
    previewId: 'ium5-gate-b-test-0001',
  });

  expect(steps.map((step) => step.label)).toEqual([
    'contracts:check',
    'typecheck',
    'check:astro',
    'test:platform',
    'validate_ium5_gate_b protocol',
    'validate_ium5_gate_b synthetic',
    'build:gate-b-preview',
    'quality:build',
  ]);
  expect(steps.filter((step) => step.environment)).toEqual([
    expect.objectContaining({
      label: 'build:gate-b-preview',
      environment: {
        IUM_BUILD_REVISION: '1'.repeat(40),
        IUM_PREVIEW_ID: 'ium5-gate-b-test-0001',
      },
    }),
  ]);
});

test('Gate-B verifier stops at the first failed child process', () => {
  const steps = createGateBVerificationSteps({
    npmCli: '/npm-cli.js',
    node: '/node',
    python: '/python',
    buildRevision: '1'.repeat(40),
    previewId: 'ium5-gate-b-test-0001',
  });
  const spawn = vi.fn()
    .mockReturnValueOnce({ status: 0 })
    .mockReturnValueOnce({ status: 7 });

  expect(runGateBVerification(steps, spawn)).toBe(7);
  expect(spawn).toHaveBeenCalledTimes(2);
});

test('Gate-B variables are removed from every non-preview child', () => {
  vi.stubEnv('IUM_BUILD_REVISION', 'outer-revision');
  vi.stubEnv('IUM_PREVIEW_ID', 'outer-preview');
  const steps = createGateBVerificationSteps({
    npmCli: '/npm-cli.js',
    node: '/node',
    python: '/python',
    buildRevision: '1'.repeat(40),
    previewId: 'ium5-gate-b-test-0001',
  });
  const spawn = vi.fn(() => ({ status: 0 }));

  expect(runGateBVerification(steps, spawn)).toBe(0);
  for (const [index, call] of spawn.mock.calls.entries()) {
    const environment = call[2].env as Record<string, string>;
    if (index === 6) {
      expect(environment.IUM_BUILD_REVISION).toBe('1'.repeat(40));
      expect(environment.IUM_PREVIEW_ID).toBe('ium5-gate-b-test-0001');
    } else {
      expect(environment).not.toHaveProperty('IUM_BUILD_REVISION');
      expect(environment).not.toHaveProperty('IUM_PREVIEW_ID');
    }
  }
});
