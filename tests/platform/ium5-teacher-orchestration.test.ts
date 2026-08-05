import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { describe, expect, test } from 'vitest';
import {
  parseExperienceContent,
  type LearningStateId,
} from '../../packages/learning-experience/src/index.js';

const experiencePath = resolve('modules/IUM-5-CORE-05/lernumgebung/experience.json');
const allowedStates = new Set<LearningStateId>([
  'LS-ORIENT',
  'LS-READY',
  'LS-DECIDE',
  'LS-ACT',
  'LS-OBSERVE',
  'LS-INTERPRET',
  'LS-REVISE',
  'LS-SECURE',
  'LS-TRANSFER',
  'LS-PAUSE',
  'LS-RECOVER',
]);

async function productionValue(): Promise<Record<string, any>> {
  return JSON.parse(await readFile(experiencePath, 'utf8')) as Record<string, any>;
}

describe('IUM5 teacher orchestration', () => {
  test('defines two closed local checkpoints with a 2–4 minute window', async () => {
    const value = await productionValue();
    const parsed = parseExperienceContent(value);

    expect(parsed.ok).toBe(true);
    if (!parsed.ok) return;
    expect(parsed.value.checkpoints.map((checkpoint) => checkpoint.id)).toEqual([
      'checkpoint-comparison',
      'checkpoint-transfer',
    ]);
    for (const checkpoint of parsed.value.checkpoints) {
      expect(checkpoint.timeWindowMinutes).toEqual([2, 4]);
      expect(allowedStates.has(checkpoint.state)).toBe(true);
      expect(allowedStates.has(checkpoint.returnState)).toBe(true);
      expect(checkpoint.ordinaryEvidence.length).toBeGreaterThan(0);
      expect(checkpoint.neutralFallback).toMatch(/ohne private(n|r)? (Geräte|Gerätestand|Arbeitsstand)/i);
      expect(checkpoint.neutralFallback).toMatch(/ohne gemeinsame (Besprechung|Pause).*fort/i);
    }
  });

  test('contains no remote lock, account, dashboard, countdown or telemetry contract', async () => {
    const value = await productionValue();
    const serialized = JSON.stringify(value.checkpoints);

    expect(serialized).not.toMatch(
      /remote.?lock|teacher.?account|hidden.?dashboard|countdown|telemetry|analytics|automatic.?transmission/i,
    );
    for (const forbidden of ['remoteLock', 'teacherAccount', 'countdown', 'telemetry']) {
      const mutated = structuredClone(value);
      mutated.checkpoints[0][forbidden] = true;
      expect(parseExperienceContent(mutated).ok).toBe(false);
    }
  });

  test('connects checkpoint references without persisting a teacher bypass', async () => {
    const value = await productionValue();
    const checkpointIds = new Set(value.checkpoints.map((checkpoint: { id: string }) => checkpoint.id));
    const references = value.actions
      .map((action: { checkpointId: string | null }) => action.checkpointId)
      .filter((id: string | null): id is string => id !== null);

    expect(references).toEqual(expect.arrayContaining([...checkpointIds]));
    expect(JSON.stringify(value)).not.toMatch(/teacherBypass|checkpointTelemetry|sharedHoldState/i);
  });
});
