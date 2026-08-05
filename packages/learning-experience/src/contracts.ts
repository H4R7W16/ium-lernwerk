export type LearningStateId =
  | 'LS-ORIENT'
  | 'LS-READY'
  | 'LS-DECIDE'
  | 'LS-ACT'
  | 'LS-OBSERVE'
  | 'LS-INTERPRET'
  | 'LS-REVISE'
  | 'LS-SECURE'
  | 'LS-TRANSFER'
  | 'LS-PAUSE'
  | 'LS-RECOVER';

export type SocialForm = 'individual' | 'pair' | 'group' | 'plenary';

export type PersistenceKind =
  | 'none'
  | 'draft'
  | 'confirmed-product'
  | 'evidence';

export interface StartBoardSpec {
  readonly heading: string;
  readonly guidingQuestion: string;
  readonly expectedCapability: string;
  readonly timeWindowMinutes: readonly [number, number];
  readonly socialForm: SocialForm;
  readonly primaryAction: Readonly<{
    label: string;
    result: string;
  }>;
  readonly resumeAction: Readonly<{
    label: string;
    purpose: string;
  }> | null;
  readonly resetAction: Readonly<{
    label: string;
    consequence: string;
  }> | null;
}

export interface LearningActionSpec {
  readonly id: string;
  readonly state: LearningStateId;
  readonly taskId: string;
  readonly purpose: string;
  readonly prompt: string;
  readonly product: string;
  readonly criteria: readonly string[];
  readonly primaryAction: Readonly<{
    label: string;
    result: string;
  }>;
  readonly secondaryActions: readonly Readonly<{
    label: string;
    purpose: string;
  }>[];
  readonly requiredEvidence: readonly string[];
  readonly supportIds: readonly string[];
  readonly checkpointId: string | null;
  readonly persistence: PersistenceKind;
  readonly next: readonly Readonly<{
    state: LearningStateId;
    guard: string;
  }>[];
}

export interface LearningTaskSpec {
  readonly id: string;
  readonly learningGoal: string;
  readonly purpose: string;
  readonly thinkingAction: string;
  readonly product: string;
  readonly materialRefs: readonly string[];
  readonly criteria: readonly string[];
  readonly requiredEvidence: readonly string[];
  readonly supportIds: readonly string[];
  readonly feedbackId: string;
  readonly socialForm: SocialForm;
  readonly roleIds: readonly string[];
  readonly persistence: PersistenceKind;
  readonly offlineRequirement: 'core' | 'enhancement';
  readonly recoverySpecId: string;
}

export interface FeedbackSpec {
  readonly id: string;
  readonly result: string;
  readonly evidenceRef: string;
  readonly criterion: string;
  readonly interpretationPrompt: string;
  readonly nextCheck: string;
  readonly strategySupportId: string | null;
  readonly exampleSupportId: string | null;
}

export interface SupportSpec {
  readonly id: string;
  readonly kind: 'operation' | 'concept' | 'strategy' | 'example';
  readonly title: string;
  readonly trigger: string;
  readonly content: string;
  readonly preservesAction: string;
  readonly nextSupportId: string | null;
}

export interface TeacherCheckpointSpec {
  readonly id: string;
  readonly state: LearningStateId;
  readonly purpose: string;
  readonly timeWindowMinutes: readonly [number, number];
  readonly socialForm: SocialForm;
  readonly learnerSignal: string;
  readonly ordinaryEvidence: readonly string[];
  readonly teacherPrompt: string;
  readonly neutralFallback: string;
  readonly returnState: LearningStateId;
  readonly exitCriterion: string;
}

export type EvidenceFieldId =
  | 'EVC-CONTEXT'
  | 'EVC-CLAIM'
  | 'EVC-ACTION'
  | 'EVC-EFFECT'
  | 'EVC-INTERPRET'
  | 'EVC-REVISION'
  | 'EVC-CONCLUSION'
  | 'EVC-TRANSFER'
  | 'EVC-RECOVERY';

export interface EvidenceCardSpec {
  readonly id: string;
  readonly actionKind:
    | 'predict-test'
    | 'create-revise'
    | 'analyze-judge'
    | 'secure-transfer';
  readonly requiredFields: readonly EvidenceFieldId[];
  readonly modelBoundaryPrompt: string;
  readonly transferPromptId: string | null;
  readonly reentryPromptId: string | null;
}

export interface ResilienceSpec {
  readonly code: string;
  readonly severity: 'info' | 'limit' | 'block';
  readonly affectedWork: string;
  readonly preservedState: string;
  readonly consequence: string;
  readonly primaryAction: string;
  readonly secondaryAction: string | null;
  readonly returnTarget: string;
}

export interface ExperienceContentV1 {
  readonly schemaVersion: 1;
  readonly moduleId: string;
  readonly terminologyVersion: 'lxp04-1';
  readonly start: StartBoardSpec;
  readonly actions: readonly LearningActionSpec[];
  readonly tasks: readonly LearningTaskSpec[];
  readonly feedback: readonly FeedbackSpec[];
  readonly supports: readonly SupportSpec[];
  readonly checkpoints: readonly TeacherCheckpointSpec[];
  readonly evidenceCards: readonly EvidenceCardSpec[];
  readonly resilience: readonly ResilienceSpec[];
}
