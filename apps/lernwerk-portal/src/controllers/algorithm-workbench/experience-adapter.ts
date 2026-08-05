import type { WorkbenchPayload } from '@ium/ium-5-core-05';
import type {
  ExperienceStage,
  Ium5ExperienceFacts,
  Ium5ExperienceState,
} from './experience-state.js';

function deriveStage(payload: WorkbenchPayload): ExperienceStage {
  if (payload.initialAlgorithm.length === 0) return 'start';
  if (payload.prediction === null) return 'prediction';
  if (payload.evidenceTrace === null) return 'run';
  if (payload.repairHypothesis.trim().length === 0) return 'evidence';
  if (payload.revisedAlgorithm === null) return 'revision';
  if (payload.evidenceCard === null || payload.systemClassifications.length === 0) return 'transfer';
  return 'reentry';
}

function deriveRecovery(facts: Ium5ExperienceFacts): Ium5ExperienceState['recovery'] {
  if (facts.validationFailed) return 'validation';
  if (facts.importFailed) return 'import';
  if (facts.persistenceAvailable === false) return 'storage';
  return 'none';
}

export function deriveIum5ExperienceState(
  payload: WorkbenchPayload,
  facts: Ium5ExperienceFacts = {},
): Ium5ExperienceState {
  const stage = deriveStage(payload);
  return {
    stage,
    canResume: (facts.hasStoredState ?? false) && stage !== 'start',
    saveState: facts.saveState ?? 'idle',
    connectivity: facts.connectivity ?? 'online',
    recovery: deriveRecovery(facts),
  };
}
