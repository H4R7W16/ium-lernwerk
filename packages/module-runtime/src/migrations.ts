import {
  validateLearningState,
  type LearningStateEnvelope,
  type PlatformError,
} from '@ium/module-contract';

export type StateMigration = Readonly<{
  from: number;
  to: number;
  migrate: (
    payload: Readonly<Record<string, unknown>>,
  ) => Record<string, unknown>;
}>;

export type MigrationResult =
  | Readonly<{ ok: true; state: LearningStateEnvelope }>
  | Readonly<{
      ok: false;
      error: PlatformError;
      original: LearningStateEnvelope;
    }>;

function migrationError(error: unknown): PlatformError {
  return {
    code: 'MIGRATION_FAILED',
    message: 'Der vorhandene Arbeitsstand konnte nicht aktualisiert werden.',
    action: 'Exportiere das Original und versuche die Migration erneut.',
    technicalDetails: String(error),
  };
}

export function migrateStateCopy(
  state: LearningStateEnvelope,
  targetVersion: number,
  migrations: readonly StateMigration[],
): MigrationResult {
  const original = structuredClone(state);
  let current = structuredClone(state);
  try {
    if (current.stateSchemaVersion > targetVersion) {
      throw new Error(
        `State schema ${current.stateSchemaVersion} is newer than ${targetVersion}`,
      );
    }
    while (current.stateSchemaVersion < targetVersion) {
      const migration = migrations.find(
        (candidate) =>
          candidate.from === current.stateSchemaVersion
          && candidate.to === current.stateSchemaVersion + 1,
      );
      if (!migration) {
        throw new Error(`Missing migration from ${current.stateSchemaVersion}`);
      }
      const payload = migration.migrate(structuredClone(current.payload));
      current = {
        ...structuredClone(current),
        stateSchemaVersion: migration.to,
        payload: structuredClone(payload),
      };
      const validation = validateLearningState(current);
      if (!validation.ok) {
        throw new Error(`Migrated state is invalid: ${JSON.stringify(validation.issues)}`);
      }
      current = structuredClone(validation.value);
    }
    return { ok: true, state: current };
  } catch (error) {
    return { ok: false, error: migrationError(error), original };
  }
}
