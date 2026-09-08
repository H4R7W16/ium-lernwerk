import type { LearningStateEnvelope } from '@ium/module-contract';

export type VersionToken = Readonly<{
  generation: number;
  revision: number;
}>;

export type StoredRow = Readonly<{
  moduleId: string;
  revision: number;
  state: LearningStateEnvelope | null;
}>;

export function sameVersion(a: VersionToken, b: VersionToken): boolean {
  return a.generation === b.generation && a.revision === b.revision;
}
