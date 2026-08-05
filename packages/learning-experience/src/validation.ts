import type {
  EvidenceCardSpec,
  EvidenceFieldId,
  ExperienceContentV1,
  FeedbackSpec,
  LearningActionSpec,
  LearningStateId,
  LearningTaskSpec,
  PersistenceKind,
  ResilienceSpec,
  SocialForm,
  StartBoardSpec,
  SupportSpec,
  TeacherCheckpointSpec,
} from './contracts.js';

export type ContractError = {
  readonly path: string;
  readonly code:
    | 'invalid_type'
    | 'missing_field'
    | 'unknown_field'
    | 'invalid_value'
    | 'duplicate_id'
    | 'limit_exceeded';
  readonly message: string;
};

export type ParseResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly errors: readonly ContractError[] };

const learningStates = new Set<LearningStateId>([
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
const socialForms = new Set<SocialForm>(['individual', 'pair', 'group', 'plenary']);
const persistenceKinds = new Set<PersistenceKind>([
  'none',
  'draft',
  'confirmed-product',
  'evidence',
]);
const evidenceFields = new Set<EvidenceFieldId>([
  'EVC-CONTEXT',
  'EVC-CLAIM',
  'EVC-ACTION',
  'EVC-EFFECT',
  'EVC-INTERPRET',
  'EVC-REVISION',
  'EVC-CONCLUSION',
  'EVC-TRANSFER',
  'EVC-RECOVERY',
]);
const inaccessibleActionLabels = new Set([
  'weiter',
  'fertig',
  'abschließen',
  'erfolg',
  'fehler',
  'richtig',
  'falsch',
  'next',
  'continue',
  'start',
  'resume',
  'reset',
  'submit',
  'save',
  'delete',
]);

type MutableError = {
  path: string;
  code: ContractError['code'];
  message: string;
};

class Collector {
  readonly errors: MutableError[] = [];

  add(path: string, code: ContractError['code'], message: string): void {
    this.errors.push({ path, code, message });
  }
}

function objectAt(
  value: unknown,
  path: string,
  keys: readonly string[],
  collector: Collector,
): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    collector.add(path, 'invalid_type', 'Expected an object.');
    return {};
  }
  const object = value as Record<string, unknown>;
  const allowed = new Set(keys);
  for (const key of Object.keys(object)) {
    if (!allowed.has(key)) {
      collector.add(`${path}.${key}`, 'unknown_field', `Unknown field: ${key}`);
    }
  }
  return object;
}

function field(
  object: Record<string, unknown>,
  key: string,
  path: string,
  collector: Collector,
): unknown {
  if (!Object.hasOwn(object, key)) {
    collector.add(`${path}.${key}`, 'missing_field', `Missing field: ${key}`);
    return undefined;
  }
  return object[key];
}

function text(
  value: unknown,
  path: string,
  collector: Collector,
  maximum: number,
  options: { readonly actionLabel?: boolean } = {},
): string {
  if (typeof value !== 'string') {
    collector.add(path, 'invalid_type', 'Expected a string.');
    return '';
  }
  if (value.trim().length === 0) {
    collector.add(path, 'invalid_value', 'Text must not be empty after trimming.');
  }
  if ([...value].length > maximum) {
    collector.add(path, 'limit_exceeded', `Text exceeds ${maximum} Unicode code points.`);
  }
  if (options.actionLabel && inaccessibleActionLabels.has(value.trim().toLocaleLowerCase('de-DE'))) {
    collector.add(path, 'invalid_value', 'Action label must name its fachliches object or result.');
  }
  return value;
}

function requiredText(
  object: Record<string, unknown>,
  key: string,
  path: string,
  collector: Collector,
  maximum: number,
  options: { readonly actionLabel?: boolean } = {},
): string {
  return text(field(object, key, path, collector), `${path}.${key}`, collector, maximum, options);
}

function nullableText(
  object: Record<string, unknown>,
  key: string,
  path: string,
  collector: Collector,
  maximum: number,
): string | null {
  const value = field(object, key, path, collector);
  if (value === null) {
    return null;
  }
  return text(value, `${path}.${key}`, collector, maximum);
}

function enumValue<T extends string>(
  value: unknown,
  path: string,
  collector: Collector,
  allowed: ReadonlySet<T>,
): T {
  if (typeof value !== 'string') {
    collector.add(path, 'invalid_type', 'Expected a controlled string value.');
    return [...allowed][0]!;
  }
  if (!allowed.has(value as T)) {
    collector.add(path, 'invalid_value', `Unsupported value: ${value}`);
    return [...allowed][0]!;
  }
  return value as T;
}

function requiredEnum<T extends string>(
  object: Record<string, unknown>,
  key: string,
  path: string,
  collector: Collector,
  allowed: ReadonlySet<T>,
): T {
  return enumValue(field(object, key, path, collector), `${path}.${key}`, collector, allowed);
}

function arrayAt(value: unknown, path: string, collector: Collector): readonly unknown[] {
  if (!Array.isArray(value)) {
    collector.add(path, 'invalid_type', 'Expected an array.');
    return [];
  }
  return value;
}

function stringArray(
  value: unknown,
  path: string,
  collector: Collector,
  maximum: number,
): readonly string[] {
  return arrayAt(value, path, collector).map((entry, index) =>
    text(entry, `${path}[${index}]`, collector, maximum));
}

function timeWindow(
  value: unknown,
  path: string,
  collector: Collector,
): readonly [number, number] {
  if (!Array.isArray(value) || value.length !== 2) {
    collector.add(path, 'invalid_type', 'Expected a two-value time window.');
    return [0, 0];
  }
  const result = value.map((entry, index) => {
    if (typeof entry !== 'number' || !Number.isInteger(entry) || entry <= 0) {
      collector.add(`${path}[${index}]`, 'invalid_value', 'Expected a positive integer minute value.');
      return 0;
    }
    return entry;
  }) as [number, number];
  if (result[0] > result[1]) {
    collector.add(path, 'invalid_value', 'Time window minimum must not exceed maximum.');
  }
  return result;
}

function primaryAction(
  value: unknown,
  path: string,
  collector: Collector,
): Readonly<{ label: string; result: string }> {
  const object = objectAt(value, path, ['label', 'result'], collector);
  return {
    label: requiredText(object, 'label', path, collector, 72, { actionLabel: true }),
    result: requiredText(object, 'result', path, collector, 240),
  };
}

function startBoard(value: unknown, path: string, collector: Collector): StartBoardSpec {
  const object = objectAt(value, path, [
    'heading',
    'guidingQuestion',
    'expectedCapability',
    'timeWindowMinutes',
    'socialForm',
    'primaryAction',
    'resumeAction',
    'resetAction',
  ], collector);
  const resumeValue = field(object, 'resumeAction', path, collector);
  const resetValue = field(object, 'resetAction', path, collector);
  const resumeAction = resumeValue === null ? null : (() => {
    const nestedPath = `${path}.resumeAction`;
    const nested = objectAt(resumeValue, nestedPath, ['label', 'purpose'], collector);
    return {
      label: requiredText(nested, 'label', nestedPath, collector, 72, { actionLabel: true }),
      purpose: requiredText(nested, 'purpose', nestedPath, collector, 600),
    };
  })();
  const resetAction = resetValue === null ? null : (() => {
    const nestedPath = `${path}.resetAction`;
    const nested = objectAt(resetValue, nestedPath, ['label', 'consequence'], collector);
    return {
      label: requiredText(nested, 'label', nestedPath, collector, 72, { actionLabel: true }),
      consequence: requiredText(nested, 'consequence', nestedPath, collector, 240),
    };
  })();
  return {
    heading: requiredText(object, 'heading', path, collector, 72),
    guidingQuestion: requiredText(object, 'guidingQuestion', path, collector, 600),
    expectedCapability: requiredText(object, 'expectedCapability', path, collector, 600),
    timeWindowMinutes: timeWindow(field(object, 'timeWindowMinutes', path, collector), `${path}.timeWindowMinutes`, collector),
    socialForm: requiredEnum(object, 'socialForm', path, collector, socialForms),
    primaryAction: primaryAction(field(object, 'primaryAction', path, collector), `${path}.primaryAction`, collector),
    resumeAction,
    resetAction,
  };
}

function learningAction(value: unknown, path: string, collector: Collector): LearningActionSpec {
  const object = objectAt(value, path, [
    'id', 'state', 'taskId', 'purpose', 'prompt', 'product', 'criteria',
    'primaryAction', 'secondaryActions', 'requiredEvidence', 'supportIds',
    'checkpointId', 'persistence', 'next',
  ], collector);
  return {
    id: requiredText(object, 'id', path, collector, 240),
    state: requiredEnum(object, 'state', path, collector, learningStates),
    taskId: requiredText(object, 'taskId', path, collector, 240),
    purpose: requiredText(object, 'purpose', path, collector, 600),
    prompt: requiredText(object, 'prompt', path, collector, 600),
    product: requiredText(object, 'product', path, collector, 600),
    criteria: stringArray(field(object, 'criteria', path, collector), `${path}.criteria`, collector, 240),
    primaryAction: primaryAction(field(object, 'primaryAction', path, collector), `${path}.primaryAction`, collector),
    secondaryActions: arrayAt(field(object, 'secondaryActions', path, collector), `${path}.secondaryActions`, collector).map((entry, index) => {
      const nestedPath = `${path}.secondaryActions[${index}]`;
      const nested = objectAt(entry, nestedPath, ['label', 'purpose'], collector);
      return {
        label: requiredText(nested, 'label', nestedPath, collector, 72, { actionLabel: true }),
        purpose: requiredText(nested, 'purpose', nestedPath, collector, 600),
      };
    }),
    requiredEvidence: stringArray(field(object, 'requiredEvidence', path, collector), `${path}.requiredEvidence`, collector, 240),
    supportIds: stringArray(field(object, 'supportIds', path, collector), `${path}.supportIds`, collector, 240),
    checkpointId: nullableText(object, 'checkpointId', path, collector, 240),
    persistence: requiredEnum(object, 'persistence', path, collector, persistenceKinds),
    next: arrayAt(field(object, 'next', path, collector), `${path}.next`, collector).map((entry, index) => {
      const nestedPath = `${path}.next[${index}]`;
      const nested = objectAt(entry, nestedPath, ['state', 'guard'], collector);
      return {
        state: requiredEnum(nested, 'state', nestedPath, collector, learningStates),
        guard: requiredText(nested, 'guard', nestedPath, collector, 600),
      };
    }),
  };
}

function learningTask(value: unknown, path: string, collector: Collector): LearningTaskSpec {
  const object = objectAt(value, path, [
    'id', 'learningGoal', 'purpose', 'thinkingAction', 'product', 'materialRefs',
    'criteria', 'requiredEvidence', 'supportIds', 'feedbackId', 'socialForm',
    'roleIds', 'persistence', 'offlineRequirement', 'recoverySpecId',
  ], collector);
  return {
    id: requiredText(object, 'id', path, collector, 240),
    learningGoal: requiredText(object, 'learningGoal', path, collector, 600),
    purpose: requiredText(object, 'purpose', path, collector, 600),
    thinkingAction: requiredText(object, 'thinkingAction', path, collector, 600),
    product: requiredText(object, 'product', path, collector, 600),
    materialRefs: stringArray(field(object, 'materialRefs', path, collector), `${path}.materialRefs`, collector, 600),
    criteria: stringArray(field(object, 'criteria', path, collector), `${path}.criteria`, collector, 240),
    requiredEvidence: stringArray(field(object, 'requiredEvidence', path, collector), `${path}.requiredEvidence`, collector, 240),
    supportIds: stringArray(field(object, 'supportIds', path, collector), `${path}.supportIds`, collector, 240),
    feedbackId: requiredText(object, 'feedbackId', path, collector, 240),
    socialForm: requiredEnum(object, 'socialForm', path, collector, socialForms),
    roleIds: stringArray(field(object, 'roleIds', path, collector), `${path}.roleIds`, collector, 240),
    persistence: requiredEnum(object, 'persistence', path, collector, persistenceKinds),
    offlineRequirement: requiredEnum(object, 'offlineRequirement', path, collector, new Set(['core', 'enhancement'] as const)),
    recoverySpecId: requiredText(object, 'recoverySpecId', path, collector, 240),
  };
}

function feedback(value: unknown, path: string, collector: Collector): FeedbackSpec {
  const object = objectAt(value, path, [
    'id', 'result', 'evidenceRef', 'criterion', 'interpretationPrompt',
    'nextCheck', 'strategySupportId', 'exampleSupportId',
  ], collector);
  const result = requiredText(object, 'result', path, collector, 240);
  if (/^(?:richtig|falsch|\d+(?:[.,]\d+)?\s*(?:%|\/\s*\d+|punkte?)?)$/i.test(result.trim())) {
    collector.add(
      `${path}.result`,
      'invalid_value',
      'Feedback result must describe observable evidence, not a bare judgment or score.',
    );
  }
  return {
    id: requiredText(object, 'id', path, collector, 240),
    result,
    evidenceRef: requiredText(object, 'evidenceRef', path, collector, 240),
    criterion: requiredText(object, 'criterion', path, collector, 240),
    interpretationPrompt: requiredText(object, 'interpretationPrompt', path, collector, 600),
    nextCheck: requiredText(object, 'nextCheck', path, collector, 600),
    strategySupportId: nullableText(object, 'strategySupportId', path, collector, 240),
    exampleSupportId: nullableText(object, 'exampleSupportId', path, collector, 240),
  };
}

function supportSpec(value: unknown, path: string, collector: Collector): SupportSpec {
  const object = objectAt(value, path, [
    'id', 'kind', 'title', 'trigger', 'content', 'preservesAction', 'nextSupportId',
  ], collector);
  return {
    id: requiredText(object, 'id', path, collector, 240),
    kind: requiredEnum(object, 'kind', path, collector, new Set(['operation', 'concept', 'strategy', 'example'] as const)),
    title: requiredText(object, 'title', path, collector, 72),
    trigger: requiredText(object, 'trigger', path, collector, 600),
    content: requiredText(object, 'content', path, collector, 1_200),
    preservesAction: requiredText(object, 'preservesAction', path, collector, 600),
    nextSupportId: nullableText(object, 'nextSupportId', path, collector, 240),
  };
}

function checkpoint(value: unknown, path: string, collector: Collector): TeacherCheckpointSpec {
  const object = objectAt(value, path, [
    'id', 'state', 'purpose', 'timeWindowMinutes', 'socialForm', 'learnerSignal',
    'ordinaryEvidence', 'teacherPrompt', 'neutralFallback', 'returnState', 'exitCriterion',
  ], collector);
  return {
    id: requiredText(object, 'id', path, collector, 240),
    state: requiredEnum(object, 'state', path, collector, learningStates),
    purpose: requiredText(object, 'purpose', path, collector, 600),
    timeWindowMinutes: timeWindow(field(object, 'timeWindowMinutes', path, collector), `${path}.timeWindowMinutes`, collector),
    socialForm: requiredEnum(object, 'socialForm', path, collector, socialForms),
    learnerSignal: requiredText(object, 'learnerSignal', path, collector, 600),
    ordinaryEvidence: stringArray(field(object, 'ordinaryEvidence', path, collector), `${path}.ordinaryEvidence`, collector, 600),
    teacherPrompt: requiredText(object, 'teacherPrompt', path, collector, 600),
    neutralFallback: requiredText(object, 'neutralFallback', path, collector, 600),
    returnState: requiredEnum(object, 'returnState', path, collector, learningStates),
    exitCriterion: requiredText(object, 'exitCriterion', path, collector, 240),
  };
}

function evidenceCard(value: unknown, path: string, collector: Collector): EvidenceCardSpec {
  const object = objectAt(value, path, [
    'id', 'actionKind', 'requiredFields', 'modelBoundaryPrompt',
    'transferPromptId', 'reentryPromptId',
  ], collector);
  const requiredFields = arrayAt(field(object, 'requiredFields', path, collector), `${path}.requiredFields`, collector)
    .map((entry, index) => enumValue(entry, `${path}.requiredFields[${index}]`, collector, evidenceFields));
  return {
    id: requiredText(object, 'id', path, collector, 240),
    actionKind: requiredEnum(object, 'actionKind', path, collector, new Set([
      'predict-test', 'create-revise', 'analyze-judge', 'secure-transfer',
    ] as const)),
    requiredFields,
    modelBoundaryPrompt: requiredText(object, 'modelBoundaryPrompt', path, collector, 600),
    transferPromptId: nullableText(object, 'transferPromptId', path, collector, 240),
    reentryPromptId: nullableText(object, 'reentryPromptId', path, collector, 240),
  };
}

function resilience(value: unknown, path: string, collector: Collector): ResilienceSpec {
  const object = objectAt(value, path, [
    'code', 'severity', 'affectedWork', 'preservedState', 'consequence',
    'primaryAction', 'secondaryAction', 'returnTarget',
  ], collector);
  return {
    code: requiredText(object, 'code', path, collector, 240),
    severity: requiredEnum(object, 'severity', path, collector, new Set(['info', 'limit', 'block'] as const)),
    affectedWork: requiredText(object, 'affectedWork', path, collector, 600),
    preservedState: requiredText(object, 'preservedState', path, collector, 600),
    consequence: requiredText(object, 'consequence', path, collector, 600),
    primaryAction: requiredText(object, 'primaryAction', path, collector, 72, { actionLabel: true }),
    secondaryAction: nullableText(object, 'secondaryAction', path, collector, 72),
    returnTarget: requiredText(object, 'returnTarget', path, collector, 600),
  };
}

function duplicates(
  values: readonly string[],
  path: string,
  key: string,
  collector: Collector,
): void {
  const seen = new Set<string>();
  values.forEach((value, index) => {
    if (seen.has(value)) {
      collector.add(`${path}[${index}].${key}`, 'duplicate_id', `Duplicate identifier: ${value}`);
    }
    seen.add(value);
  });
}

function reference(
  value: string | null,
  allowed: ReadonlySet<string>,
  path: string,
  collector: Collector,
): void {
  if (value !== null && !allowed.has(value)) {
    collector.add(path, 'invalid_value', `Dangling reference: ${value}`);
  }
}

function validateReferences(content: ExperienceContentV1, collector: Collector): void {
  const actionIds = new Set(content.actions.map((entry) => entry.id));
  const taskIds = new Set(content.tasks.map((entry) => entry.id));
  const feedbackIds = new Set(content.feedback.map((entry) => entry.id));
  const supportIds = new Set(content.supports.map((entry) => entry.id));
  const checkpointIds = new Set(content.checkpoints.map((entry) => entry.id));
  const evidenceIds = new Set(content.evidenceCards.map((entry) => entry.id));
  const resilienceIds = new Set(content.resilience.map((entry) => entry.code));

  duplicates(content.actions.map((entry) => entry.id), '$.actions', 'id', collector);
  duplicates(content.tasks.map((entry) => entry.id), '$.tasks', 'id', collector);
  duplicates(content.feedback.map((entry) => entry.id), '$.feedback', 'id', collector);
  duplicates(content.supports.map((entry) => entry.id), '$.supports', 'id', collector);
  duplicates(content.checkpoints.map((entry) => entry.id), '$.checkpoints', 'id', collector);
  duplicates(content.evidenceCards.map((entry) => entry.id), '$.evidenceCards', 'id', collector);
  duplicates(content.resilience.map((entry) => entry.code), '$.resilience', 'code', collector);

  content.actions.forEach((entry, index) => {
    reference(entry.taskId, taskIds, `$.actions[${index}].taskId`, collector);
    entry.supportIds.forEach((id, supportIndex) =>
      reference(id, supportIds, `$.actions[${index}].supportIds[${supportIndex}]`, collector));
    entry.requiredEvidence.forEach((id, evidenceIndex) =>
      reference(id, evidenceIds, `$.actions[${index}].requiredEvidence[${evidenceIndex}]`, collector));
    reference(entry.checkpointId, checkpointIds, `$.actions[${index}].checkpointId`, collector);
  });
  content.tasks.forEach((entry, index) => {
    reference(entry.feedbackId, feedbackIds, `$.tasks[${index}].feedbackId`, collector);
    entry.supportIds.forEach((id, supportIndex) =>
      reference(id, supportIds, `$.tasks[${index}].supportIds[${supportIndex}]`, collector));
    entry.requiredEvidence.forEach((id, evidenceIndex) =>
      reference(id, evidenceIds, `$.tasks[${index}].requiredEvidence[${evidenceIndex}]`, collector));
    reference(entry.recoverySpecId, resilienceIds, `$.tasks[${index}].recoverySpecId`, collector);
  });
  content.feedback.forEach((entry, index) => {
    reference(entry.evidenceRef, evidenceIds, `$.feedback[${index}].evidenceRef`, collector);
    reference(entry.strategySupportId, supportIds, `$.feedback[${index}].strategySupportId`, collector);
    reference(entry.exampleSupportId, supportIds, `$.feedback[${index}].exampleSupportId`, collector);
  });
  content.supports.forEach((entry, index) =>
    reference(entry.nextSupportId, supportIds, `$.supports[${index}].nextSupportId`, collector));
  content.evidenceCards.forEach((entry, index) => {
    duplicates(entry.requiredFields, `$.evidenceCards[${index}].requiredFields`, '', collector);
    reference(entry.transferPromptId, actionIds, `$.evidenceCards[${index}].transferPromptId`, collector);
    reference(entry.reentryPromptId, actionIds, `$.evidenceCards[${index}].reentryPromptId`, collector);
  });
}

export function parseExperienceContent(input: unknown): ParseResult<ExperienceContentV1> {
  const collector = new Collector();
  const root = objectAt(input, '$', [
    'schemaVersion', 'moduleId', 'terminologyVersion', 'start', 'actions', 'tasks',
    'feedback', 'supports', 'checkpoints', 'evidenceCards', 'resilience',
  ], collector);
  const schemaVersion = field(root, 'schemaVersion', '$', collector);
  if (schemaVersion !== 1) {
    collector.add('$.schemaVersion', 'invalid_value', 'Only schemaVersion 1 is supported.');
  }
  const terminologyVersion = field(root, 'terminologyVersion', '$', collector);
  if (terminologyVersion !== 'lxp04-1') {
    collector.add('$.terminologyVersion', 'invalid_value', 'Only terminologyVersion lxp04-1 is supported.');
  }
  const content: ExperienceContentV1 = {
    schemaVersion: 1,
    moduleId: requiredText(root, 'moduleId', '$', collector, 240),
    terminologyVersion: 'lxp04-1',
    start: startBoard(field(root, 'start', '$', collector), '$.start', collector),
    actions: arrayAt(field(root, 'actions', '$', collector), '$.actions', collector)
      .map((entry, index) => learningAction(entry, `$.actions[${index}]`, collector)),
    tasks: arrayAt(field(root, 'tasks', '$', collector), '$.tasks', collector)
      .map((entry, index) => learningTask(entry, `$.tasks[${index}]`, collector)),
    feedback: arrayAt(field(root, 'feedback', '$', collector), '$.feedback', collector)
      .map((entry, index) => feedback(entry, `$.feedback[${index}]`, collector)),
    supports: arrayAt(field(root, 'supports', '$', collector), '$.supports', collector)
      .map((entry, index) => supportSpec(entry, `$.supports[${index}]`, collector)),
    checkpoints: arrayAt(field(root, 'checkpoints', '$', collector), '$.checkpoints', collector)
      .map((entry, index) => checkpoint(entry, `$.checkpoints[${index}]`, collector)),
    evidenceCards: arrayAt(field(root, 'evidenceCards', '$', collector), '$.evidenceCards', collector)
      .map((entry, index) => evidenceCard(entry, `$.evidenceCards[${index}]`, collector)),
    resilience: arrayAt(field(root, 'resilience', '$', collector), '$.resilience', collector)
      .map((entry, index) => resilience(entry, `$.resilience[${index}]`, collector)),
  };
  validateReferences(content, collector);
  if (collector.errors.length > 0) {
    return { ok: false, errors: collector.errors };
  }
  return { ok: true, value: content };
}
