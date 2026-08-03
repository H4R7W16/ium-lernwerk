import {
  MAX_RATIONALE_CODEPOINTS,
  type Algorithm,
  type BasicCommandKind,
  type Direction,
  type InterpreterErrorCode,
  type Position,
  type TraceEntry,
  type WorldState,
} from './model.js';
import {
  TRANSFER_CASE_IDS,
  WORKBENCH_SCENARIO_IDS,
  type LearningPhaseId,
  type TransferCaseId,
  type WorkbenchScenarioId,
} from './resources.js';
import { parseAlgorithm, type ParseResult } from './validation.js';

export type Prediction = Readonly<{
  position: Position;
  direction: Direction;
  success: 'yes' | 'no' | 'unsure';
}>;

export type EvidenceTrace = Readonly<{
  scenarioId: WorkbenchScenarioId;
  entries: readonly TraceEntry[];
  finalState: WorldState;
  missionSucceeded: boolean;
}>;

export type SystemClassification = Readonly<{
  caseId: TransferCaseId;
  classification: 'algorithmic' | 'not-algorithmic' | 'needs-information';
  rationale: string;
}>;

export type SelfCheckValue = 'yes' | 'review' | 'not-applicable';
export type SelfCheck = Readonly<{
  unambiguous: SelfCheckValue;
  traceMatches: SelfCheckValue;
  repairJustified: SelfCheckValue;
  loopAppropriate: SelfCheckValue;
}>;

export type WorkbenchPayload = Readonly<{
  phaseId: LearningPhaseId;
  scenarioId: WorkbenchScenarioId;
  initialAlgorithm: Algorithm;
  prediction: Prediction | null;
  evidenceTrace: EvidenceTrace | null;
  repairSource: 'own-draft' | 'standard-error-case' | null;
  repairHypothesis: string;
  revisedAlgorithm: Algorithm | null;
  loopDecision: string;
  systemClassifications: readonly SystemClassification[];
  selfCheck: SelfCheck;
}>;

type UnknownRecord = Readonly<Record<string, unknown>>;

const payloadKeys = [
  'phaseId',
  'scenarioId',
  'initialAlgorithm',
  'prediction',
  'evidenceTrace',
  'repairSource',
  'repairHypothesis',
  'revisedAlgorithm',
  'loopDecision',
  'systemClassifications',
  'selfCheck',
] as const;
const learningPhaseIds = new Set<LearningPhaseId>([
  'ue1-orientation',
  'ue1-prior-knowledge',
  'ue1-concept',
  'ue2-concept',
  'ue2-guided',
  'ue3-guided',
  'ue3-product',
  'ue4-product',
  'ue4-revision',
  'ue5-transfer',
  'ue5-consolidation',
  'ue6-extension',
]);
const workbenchScenarioIds = new Set<WorkbenchScenarioId>(WORKBENCH_SCENARIO_IDS);
const transferCaseIds = new Set<TransferCaseId>(TRANSFER_CASE_IDS);
const directions = new Set<Direction>(['north', 'east', 'south', 'west']);
const basicCommandKinds = new Set<BasicCommandKind>([
  'move',
  'turn-left',
  'turn-right',
  'pick-up',
  'drop',
]);
const interpreterErrors = new Set<InterpreterErrorCode>([
  'OBSTACLE',
  'OUT_OF_BOUNDS',
  'INVALID_PICK_UP',
  'INVALID_DROP',
  'INVALID_REPEAT',
  'STEP_LIMIT',
]);
const classifications = new Set<SystemClassification['classification']>([
  'algorithmic',
  'not-algorithmic',
  'needs-information',
]);
const selfCheckValues = new Set<SelfCheckValue>([
  'yes',
  'review',
  'not-applicable',
]);
const commandIdPattern = /^cmd-[1-9][0-9]*$/;

function failure<T>(path: string, message: string): ParseResult<T> {
  return { ok: false, issues: [{ path, message }] };
}

function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function hasExactKeys(value: UnknownRecord, keys: readonly string[]): boolean {
  const expected = new Set(keys);
  const actual = Object.keys(value);
  return actual.length === expected.size && actual.every((key) => expected.has(key));
}

function hasAtMostCodePoints(value: unknown, maximum: number): value is string {
  return typeof value === 'string' && [...value].length <= maximum;
}

function parsePosition(value: unknown, path: string): ParseResult<Position> {
  if (!isRecord(value) || !hasExactKeys(value, ['column', 'row'])) {
    return failure(path, 'must contain exactly column and row');
  }
  if (
    !Number.isInteger(value.column)
    || !Number.isInteger(value.row)
    || (value.column as number) < 1
    || (value.column as number) > 6
    || (value.row as number) < 1
    || (value.row as number) > 6
  ) {
    return failure(path, 'must be a position within the supported 6 by 6 grid');
  }
  return {
    ok: true,
    value: { column: value.column as number, row: value.row as number },
  };
}

function parseDirection(value: unknown, path: string): ParseResult<Direction> {
  if (typeof value !== 'string' || !directions.has(value as Direction)) {
    return failure(path, 'must be an approved direction');
  }
  return { ok: true, value: value as Direction };
}

function parseWorldState(value: unknown, path: string): ParseResult<WorldState> {
  if (!isRecord(value) || !hasExactKeys(value, [
    'position',
    'direction',
    'carrying',
    'itemPosition',
    'delivered',
  ])) {
    return failure(path, 'must contain exactly the approved world-state fields');
  }
  const position = parsePosition(value.position, `${path}.position`);
  if (!position.ok) {
    return position;
  }
  const direction = parseDirection(value.direction, `${path}.direction`);
  if (!direction.ok) {
    return direction;
  }
  if (typeof value.carrying !== 'boolean' || typeof value.delivered !== 'boolean') {
    return failure(path, 'carrying and delivered must be boolean');
  }
  let itemPosition: Position | null = null;
  if (value.itemPosition !== null) {
    const parsedItemPosition = parsePosition(value.itemPosition, `${path}.itemPosition`);
    if (!parsedItemPosition.ok) {
      return parsedItemPosition;
    }
    itemPosition = parsedItemPosition.value;
  }
  if (value.carrying && itemPosition !== null) {
    return failure(`${path}.itemPosition`, 'must be null while the item is carried');
  }
  return {
    ok: true,
    value: {
      position: position.value,
      direction: direction.value,
      carrying: value.carrying,
      itemPosition,
      delivered: value.delivered,
    },
  };
}

function parsePrediction(value: unknown): ParseResult<Prediction | null> {
  if (value === null) {
    return { ok: true, value: null };
  }
  if (!isRecord(value) || !hasExactKeys(value, ['position', 'direction', 'success'])) {
    return failure('$.prediction', 'must contain exactly position, direction and success');
  }
  const position = parsePosition(value.position, '$.prediction.position');
  if (!position.ok) {
    return position;
  }
  const direction = parseDirection(value.direction, '$.prediction.direction');
  if (!direction.ok) {
    return direction;
  }
  if (value.success !== 'yes' && value.success !== 'no' && value.success !== 'unsure') {
    return failure('$.prediction.success', 'must be yes, no or unsure');
  }
  return {
    ok: true,
    value: { position: position.value, direction: direction.value, success: value.success },
  };
}

function parseTraceEntry(value: unknown, index: number): ParseResult<TraceEntry> {
  const path = `$.evidenceTrace.entries[${index}]`;
  if (!isRecord(value) || !hasExactKeys(value, [
    'step',
    'sourceCommandId',
    'commandKind',
    'loop',
    'before',
    'after',
    'outcome',
    'error',
  ])) {
    return failure(path, 'must contain exactly the approved trace fields');
  }
  if (value.step !== index + 1) {
    return failure(`${path}.step`, 'must be consecutive and one-based');
  }
  if (typeof value.sourceCommandId !== 'string' || !commandIdPattern.test(value.sourceCommandId)) {
    return failure(`${path}.sourceCommandId`, 'must be a valid command identifier');
  }
  if (
    typeof value.commandKind !== 'string'
    || (value.commandKind !== 'repeat'
      && !basicCommandKinds.has(value.commandKind as BasicCommandKind))
  ) {
    return failure(`${path}.commandKind`, 'must be a closed command kind');
  }
  let loop: Readonly<{ iteration: number; total: number }> | null = null;
  if (value.loop !== null) {
    if (!isRecord(value.loop) || !hasExactKeys(value.loop, ['iteration', 'total'])) {
      return failure(`${path}.loop`, 'must contain exactly iteration and total');
    }
    if (
      !Number.isInteger(value.loop.iteration)
      || !Number.isInteger(value.loop.total)
      || (value.loop.iteration as number) < 1
      || (value.loop.total as number) < 2
      || (value.loop.total as number) > 9
      || (value.loop.iteration as number) > (value.loop.total as number)
    ) {
      return failure(`${path}.loop`, 'must describe a valid fixed-loop iteration');
    }
    loop = {
      iteration: value.loop.iteration as number,
      total: value.loop.total as number,
    };
  }
  const before = parseWorldState(value.before, `${path}.before`);
  if (!before.ok) {
    return before;
  }
  const after = parseWorldState(value.after, `${path}.after`);
  if (!after.ok) {
    return after;
  }
  if (value.outcome !== 'ok' && value.outcome !== 'error') {
    return failure(`${path}.outcome`, 'must be ok or error');
  }
  let error: InterpreterErrorCode | null = null;
  if (value.error !== null) {
    if (typeof value.error !== 'string' || !interpreterErrors.has(value.error as InterpreterErrorCode)) {
      return failure(`${path}.error`, 'must be a closed interpreter error');
    }
    error = value.error as InterpreterErrorCode;
  }
  if ((value.outcome === 'ok' && error !== null) || (value.outcome === 'error' && error === null)) {
    return failure(path, 'outcome and error must agree');
  }
  return {
    ok: true,
    value: {
      step: value.step as number,
      sourceCommandId: value.sourceCommandId,
      commandKind: value.commandKind as BasicCommandKind | 'repeat',
      loop,
      before: before.value,
      after: after.value,
      outcome: value.outcome,
      error,
    },
  };
}

function parseEvidenceTrace(
  value: unknown,
  payloadScenarioId: WorkbenchScenarioId,
): ParseResult<EvidenceTrace | null> {
  if (value === null) {
    return { ok: true, value: null };
  }
  if (!isRecord(value) || !hasExactKeys(value, [
    'scenarioId',
    'entries',
    'finalState',
    'missionSucceeded',
  ])) {
    return failure('$.evidenceTrace', 'must contain exactly the approved evidence fields');
  }
  if (value.scenarioId !== payloadScenarioId) {
    return failure('$.evidenceTrace.scenarioId', 'must match the active payload scenario');
  }
  if (!Array.isArray(value.entries) || value.entries.length > 101) {
    return failure('$.evidenceTrace.entries', 'must contain at most 101 trace entries');
  }
  const entries: TraceEntry[] = [];
  for (const [index, candidate] of value.entries.entries()) {
    const entry = parseTraceEntry(candidate, index);
    if (!entry.ok) {
      return entry;
    }
    entries.push(entry.value);
  }
  const finalState = parseWorldState(value.finalState, '$.evidenceTrace.finalState');
  if (!finalState.ok) {
    return finalState;
  }
  if (typeof value.missionSucceeded !== 'boolean') {
    return failure('$.evidenceTrace.missionSucceeded', 'must be boolean');
  }
  if (
    entries.length > 0
    && JSON.stringify(entries.at(-1)?.after) !== JSON.stringify(finalState.value)
  ) {
    return failure('$.evidenceTrace.finalState', 'must equal the last trace state');
  }
  return {
    ok: true,
    value: {
      scenarioId: value.scenarioId as WorkbenchScenarioId,
      entries,
      finalState: finalState.value,
      missionSucceeded: value.missionSucceeded,
    },
  };
}

function parseSystemClassifications(value: unknown): ParseResult<readonly SystemClassification[]> {
  if (!Array.isArray(value) || value.length > TRANSFER_CASE_IDS.length) {
    return failure('$.systemClassifications', 'must be an array with at most six entries');
  }
  const result: SystemClassification[] = [];
  const seen = new Set<TransferCaseId>();
  for (const [index, candidate] of value.entries()) {
    const path = `$.systemClassifications[${index}]`;
    if (!isRecord(candidate) || !hasExactKeys(candidate, [
      'caseId',
      'classification',
      'rationale',
    ])) {
      return failure(path, 'must contain exactly caseId, classification and rationale');
    }
    if (typeof candidate.caseId !== 'string' || !transferCaseIds.has(candidate.caseId as TransferCaseId)) {
      return failure(`${path}.caseId`, 'must be an approved transfer case');
    }
    const caseId = candidate.caseId as TransferCaseId;
    if (seen.has(caseId)) {
      return failure(`${path}.caseId`, 'must be unique');
    }
    seen.add(caseId);
    if (
      typeof candidate.classification !== 'string'
      || !classifications.has(candidate.classification as SystemClassification['classification'])
    ) {
      return failure(`${path}.classification`, 'must be an approved classification');
    }
    if (
      !hasAtMostCodePoints(candidate.rationale, MAX_RATIONALE_CODEPOINTS)
      || candidate.rationale.trim().length === 0
    ) {
      return failure(`${path}.rationale`, 'must be a non-empty rationale of at most 500 code points');
    }
    result.push({
      caseId,
      classification: candidate.classification as SystemClassification['classification'],
      rationale: candidate.rationale,
    });
  }
  return { ok: true, value: result };
}

function parseSelfCheck(value: unknown): ParseResult<SelfCheck> {
  if (!isRecord(value) || !hasExactKeys(value, [
    'unambiguous',
    'traceMatches',
    'repairJustified',
    'loopAppropriate',
  ])) {
    return failure('$.selfCheck', 'must contain exactly the four self-check fields');
  }
  for (const key of [
    'unambiguous',
    'traceMatches',
    'repairJustified',
    'loopAppropriate',
  ] as const) {
    if (typeof value[key] !== 'string' || !selfCheckValues.has(value[key] as SelfCheckValue)) {
      return failure(`$.selfCheck.${key}`, 'must be yes, review or not-applicable');
    }
  }
  return {
    ok: true,
    value: {
      unambiguous: value.unambiguous as SelfCheckValue,
      traceMatches: value.traceMatches as SelfCheckValue,
      repairJustified: value.repairJustified as SelfCheckValue,
      loopAppropriate: value.loopAppropriate as SelfCheckValue,
    },
  };
}

export function createInitialPayload(): WorkbenchPayload {
  return {
    phaseId: 'ue1-orientation',
    scenarioId: 'worked-sequence',
    initialAlgorithm: [],
    prediction: null,
    evidenceTrace: null,
    repairSource: null,
    repairHypothesis: '',
    revisedAlgorithm: null,
    loopDecision: '',
    systemClassifications: [],
    selfCheck: {
      unambiguous: 'review',
      traceMatches: 'review',
      repairJustified: 'review',
      loopAppropriate: 'review',
    },
  };
}

export function parseWorkbenchPayload(value: unknown): ParseResult<WorkbenchPayload> {
  if (!isRecord(value) || !hasExactKeys(value, payloadKeys)) {
    return failure('$', 'must contain exactly the eleven approved product fields');
  }
  if (typeof value.phaseId !== 'string' || !learningPhaseIds.has(value.phaseId as LearningPhaseId)) {
    return failure('$.phaseId', 'must be an approved learning phase');
  }
  if (
    typeof value.scenarioId !== 'string'
    || !workbenchScenarioIds.has(value.scenarioId as WorkbenchScenarioId)
  ) {
    return failure('$.scenarioId', 'must be an approved workbench scenario');
  }
  const scenarioId = value.scenarioId as WorkbenchScenarioId;
  const initialAlgorithm = parseAlgorithm(value.initialAlgorithm);
  if (!initialAlgorithm.ok) {
    return failure('$.initialAlgorithm', 'must be a valid closed algorithm');
  }
  const prediction = parsePrediction(value.prediction);
  if (!prediction.ok) {
    return prediction;
  }
  const evidenceTrace = parseEvidenceTrace(value.evidenceTrace, scenarioId);
  if (!evidenceTrace.ok) {
    return evidenceTrace;
  }
  if (
    value.repairSource !== null
    && value.repairSource !== 'own-draft'
    && value.repairSource !== 'standard-error-case'
  ) {
    return failure('$.repairSource', 'must be a closed repair source or null');
  }
  if (!hasAtMostCodePoints(value.repairHypothesis, MAX_RATIONALE_CODEPOINTS)) {
    return failure('$.repairHypothesis', 'must contain at most 500 code points');
  }
  let revisedAlgorithm: Algorithm | null = null;
  if (value.revisedAlgorithm !== null) {
    const parsedRevised = parseAlgorithm(value.revisedAlgorithm);
    if (!parsedRevised.ok) {
      return failure('$.revisedAlgorithm', 'must be a valid closed algorithm or null');
    }
    revisedAlgorithm = parsedRevised.value;
  }
  if (!hasAtMostCodePoints(value.loopDecision, MAX_RATIONALE_CODEPOINTS)) {
    return failure('$.loopDecision', 'must contain at most 500 code points');
  }
  const systemClassifications = parseSystemClassifications(value.systemClassifications);
  if (!systemClassifications.ok) {
    return systemClassifications;
  }
  const selfCheck = parseSelfCheck(value.selfCheck);
  if (!selfCheck.ok) {
    return selfCheck;
  }
  return {
    ok: true,
    value: {
      phaseId: value.phaseId as LearningPhaseId,
      scenarioId,
      initialAlgorithm: initialAlgorithm.value,
      prediction: prediction.value,
      evidenceTrace: evidenceTrace.value,
      repairSource: value.repairSource,
      repairHypothesis: value.repairHypothesis,
      revisedAlgorithm,
      loopDecision: value.loopDecision,
      systemClassifications: systemClassifications.value,
      selfCheck: selfCheck.value,
    },
  };
}

export function projectPersistentPayload(value: unknown): WorkbenchPayload {
  if (!isRecord(value)) {
    throw new TypeError('Workbench payload source must be an object');
  }
  const projected = Object.fromEntries(
    payloadKeys.map((key) => [key, value[key]]),
  );
  const parsed = parseWorkbenchPayload(projected);
  if (!parsed.ok) {
    throw new TypeError(`Invalid workbench payload: ${JSON.stringify(parsed.issues)}`);
  }
  return parsed.value;
}
