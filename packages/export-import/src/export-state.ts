import {
  validateLearningState,
  type LearningStateEnvelope,
} from '@ium/module-contract';

export function serializeState(state: LearningStateEnvelope): Uint8Array {
  const validation = validateLearningState(state);
  if (!validation.ok) {
    throw new TypeError(`Cannot export invalid learning state: ${JSON.stringify(validation.issues)}`);
  }
  return new TextEncoder().encode(`${JSON.stringify(validation.value, null, 2)}\n`);
}

export function stateExportFilename(state: LearningStateEnvelope): string {
  const date = state.savedAt.slice(0, 10);
  const safeModuleId = state.moduleId
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
  return `ium-${safeModuleId}-${date}.json`;
}
