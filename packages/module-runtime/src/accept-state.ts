import {
  validateLearningState,
  type LearningStateEnvelope,
  type PlatformError,
} from '@ium/module-contract';
import { migrateStateCopy, type StateMigration } from './migrations.js';

export type StatePolicy = Readonly<{
  supportedModuleVersions: readonly string[];
  createInitialPayload: () => Record<string, unknown>;
  validatePayload: (payload: unknown) => boolean;
}>;

export type StateAcceptanceDependencies = Readonly<{
  moduleId: string;
  moduleVersion: string;
  targetStateSchemaVersion: number;
  migrations: readonly StateMigration[];
  statePolicy?: StatePolicy;
}>;

export type RuntimeFailure = Readonly<{ ok: false; error: PlatformError }>;
export type RuntimeStateSuccess = Readonly<{
  ok: true;
  state: LearningStateEnvelope;
}>;

function importError(
  code: Extract<PlatformError['code'], 'IMPORT_INVALID' | 'IMPORT_WRONG_MODULE' | 'IMPORT_UNSUPPORTED_VERSION'>,
  technicalDetails: string,
): PlatformError {
  const copy = {
    IMPORT_INVALID: [
      'Der Arbeitsstand ist kein gültiger IuM-Lernstand.',
      'Sichere bei Bedarf das Original und wähle einen gültigen Stand.',
    ],
    IMPORT_WRONG_MODULE: [
      'Der Arbeitsstand gehört zu einem anderen Lernmodul.',
      'Öffne das passende Modul oder wähle einen anderen Stand.',
    ],
    IMPORT_UNSUPPORTED_VERSION: [
      'Der Arbeitsstand gehört zu einer nicht unterstützten Modulversion.',
      'Sichere das Original und öffne es mit der passenden Lernwerkversion.',
    ],
  } as const;
  const [message, action] = copy[code];
  return { code, message, action, technicalDetails };
}

export function resolveStatePolicy(
  dependencies: Pick<StateAcceptanceDependencies, 'moduleVersion' | 'statePolicy'>,
): StatePolicy {
  return dependencies.statePolicy ?? {
    supportedModuleVersions: [dependencies.moduleVersion],
    createInitialPayload: () => ({}),
    validatePayload: (payload) => (
      payload !== null
      && typeof payload === 'object'
      && !Array.isArray(payload)
    ),
  };
}

export function acceptState(
  raw: unknown,
  dependencies: StateAcceptanceDependencies,
): RuntimeStateSuccess | RuntimeFailure {
  const structural = validateLearningState(raw);
  if (!structural.ok) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', JSON.stringify(structural.issues)),
    };
  }

  try {
    JSON.stringify(structural.value);
  } catch (error) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', `State is not JSON-serializable: ${String(error)}`),
    };
  }

  if (structural.value.moduleId !== dependencies.moduleId) {
    return {
      ok: false,
      error: importError(
        'IMPORT_WRONG_MODULE',
        `expected ${dependencies.moduleId}, received ${structural.value.moduleId}`,
      ),
    };
  }

  const policy = resolveStatePolicy(dependencies);
  if (!policy.supportedModuleVersions.includes(structural.value.moduleVersion)) {
    return {
      ok: false,
      error: importError(
        'IMPORT_UNSUPPORTED_VERSION',
        `supported ${policy.supportedModuleVersions.join(', ')}, received ${structural.value.moduleVersion}`,
      ),
    };
  }

  const migrated = migrateStateCopy(
    structuredClone(structural.value),
    dependencies.targetStateSchemaVersion,
    dependencies.migrations,
  );
  if (!migrated.ok) return { ok: false, error: migrated.error };

  const normalized = {
    ...structuredClone(migrated.state),
    moduleVersion: dependencies.moduleVersion,
  };
  const finalEnvelope = validateLearningState(normalized);
  if (!finalEnvelope.ok) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', JSON.stringify(finalEnvelope.issues)),
    };
  }

  let payloadAccepted = false;
  try {
    payloadAccepted = policy.validatePayload(finalEnvelope.value.payload);
  } catch (error) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', `Payload validation failed: ${String(error)}`),
    };
  }
  if (!payloadAccepted) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', 'Payload does not satisfy the module state policy'),
    };
  }
  return { ok: true, state: structuredClone(finalEnvelope.value) };
}
