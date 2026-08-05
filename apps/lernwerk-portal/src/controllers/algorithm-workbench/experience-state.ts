export type ExperienceStage =
  | 'start'
  | 'prediction'
  | 'run'
  | 'evidence'
  | 'revision'
  | 'transfer'
  | 'reentry';

export interface Ium5ExperienceState {
  readonly stage: ExperienceStage;
  readonly canResume: boolean;
  readonly saveState: 'idle' | 'saving' | 'saved' | 'failed';
  readonly connectivity: 'online' | 'offline';
  readonly recovery: 'none' | 'validation' | 'storage' | 'import';
}

export interface Ium5ExperienceFacts {
  readonly hasStoredState?: boolean;
  readonly saveState?: Ium5ExperienceState['saveState'];
  readonly connectivity?: Ium5ExperienceState['connectivity'];
  readonly persistenceAvailable?: boolean;
  readonly validationFailed?: boolean;
  readonly importFailed?: boolean;
}
