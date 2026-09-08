import type { ReloadReadiness } from '@ium/module-runtime';

export type { ReloadReadiness } from '@ium/module-runtime';

export type ReadinessCollection = Readonly<{
  safe: boolean;
  values: readonly ReloadReadiness[];
  errors: readonly string[];
}>;

export function allReady(values: readonly ReloadReadiness[]): boolean {
  return values.every((value) => value.safe);
}

export function isCurrentReadiness(value: ReloadReadiness, revision: number): boolean {
  return value.safe && value.revision === revision;
}

export async function collectReadiness(
  tasks: readonly Promise<ReloadReadiness>[],
): Promise<ReadinessCollection> {
  const errors: string[] = [];
  const values = await Promise.all(tasks.map(async (task): Promise<ReloadReadiness> => {
    try {
      return await task;
    } catch (error) {
      errors.push(error instanceof Error ? error.message : String(error));
      return { safe: false, reason: 'unknown-client' };
    }
  }));
  return { safe: allReady(values), values, errors };
}
