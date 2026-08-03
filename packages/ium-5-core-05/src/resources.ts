import type { Algorithm, Scenario } from './model.js';
import {
  parseAlgorithm,
  parseScenario,
  type ParseResult,
} from './validation.js';

export type LearningPhaseId =
  | 'ue1-orientation'
  | 'ue1-prior-knowledge'
  | 'ue1-concept'
  | 'ue2-concept'
  | 'ue2-guided'
  | 'ue3-guided'
  | 'ue3-product'
  | 'ue4-product'
  | 'ue4-revision'
  | 'ue5-transfer'
  | 'ue5-consolidation'
  | 'ue6-extension';

const REGULAR_PHASE_IDS = [
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
] as const satisfies readonly LearningPhaseId[];
const ALL_PHASE_IDS = [...REGULAR_PHASE_IDS, 'ue6-extension'] as const;

export const WORKBENCH_SCENARIO_IDS = [
  'worked-sequence',
  'error-order',
  'error-turn',
  'error-missing-step',
  'error-repeat-count',
  'product-a',
  'product-b',
  'product-c',
  'repair-standard',
  'extended-inherited',
] as const;
export type WorkbenchScenarioId = typeof WORKBENCH_SCENARIO_IDS[number];

export const TRANSFER_CASE_IDS = [
  'navigation',
  'search-service',
  'digital-timetable',
  'paper-map',
  'mechanical-timer',
  'controlled-vehicle',
] as const;
export type TransferCaseId = typeof TRANSFER_CASE_IDS[number];

type ActivityFamily =
  | 'precision'
  | 'worked-example'
  | 'error-case'
  | 'product'
  | 'transfer';

export type LessonSegment = Readonly<{
  id: LearningPhaseId;
  lesson: 1 | 2 | 3 | 4 | 5 | 6;
  minutes: number;
  title: string;
  learningFunction: string;
  activityIds: readonly string[];
}>;

export type WorkbenchContent = Readonly<{
  schemaVersion: 1;
  moduleId: 'IUM-5-CORE-05';
  centralQuestion: string;
  paths: Readonly<{
    regular: Readonly<{
      totalMinutes: 225;
      segmentIds: readonly LearningPhaseId[];
    }>;
    extended: Readonly<{
      totalMinutes: 270;
      segmentIds: readonly LearningPhaseId[];
    }>;
  }>;
  segments: readonly LessonSegment[];
  activities: readonly Readonly<{
    id: string;
    family: ActivityFamily;
    title: string;
    instruction: string;
    scenarioIds: readonly WorkbenchScenarioId[];
  }>[];
  supports: readonly Readonly<{ id: string; title: string; text: string }>[];
  transferCases: readonly Readonly<{
    id: TransferCaseId;
    title: string;
    description: string;
  }>[];
  selfCheckQuestions: readonly Readonly<{ id: string; text: string }>[];
}>;

export type WorkbenchResources = Readonly<{
  content: WorkbenchContent;
  scenarios: readonly Readonly<{
    scenario: Scenario;
    starterAlgorithm: Algorithm | null;
    referenceAlgorithm: Algorithm;
  }>[];
}>;

type UnknownRecord = Readonly<Record<string, unknown>>;

const phaseIds = new Set<string>(ALL_PHASE_IDS);
const scenarioIds = new Set<string>(WORKBENCH_SCENARIO_IDS);
const activityFamilies = new Set<ActivityFamily>([
  'precision',
  'worked-example',
  'error-case',
  'product',
  'transfer',
]);
const productScenarioIds = new Set<WorkbenchScenarioId>([
  'product-a',
  'product-b',
  'product-c',
]);
const identifierPattern = /^[a-z][a-z0-9-]*$/;

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

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

function isIdentifier(value: unknown): value is string {
  return typeof value === 'string' && identifierPattern.test(value);
}

function hasUniqueValues(values: readonly string[]): boolean {
  return new Set(values).size === values.length;
}

function equals<T>(left: readonly T[], right: readonly T[]): boolean {
  return left.length === right.length
    && left.every((value, index) => value === right[index]);
}

function parsePath(
  value: unknown,
  path: string,
  totalMinutes: 225 | 270,
  expectedIds: readonly LearningPhaseId[],
): ParseResult<Readonly<{
  totalMinutes: 225 | 270;
  segmentIds: readonly LearningPhaseId[];
}>> {
  if (!isRecord(value) || !hasExactKeys(value, ['totalMinutes', 'segmentIds'])) {
    return failure(path, 'must contain exactly totalMinutes and segmentIds');
  }
  if (value.totalMinutes !== totalMinutes) {
    return failure(`${path}.totalMinutes`, `must be ${totalMinutes}`);
  }
  if (
    !Array.isArray(value.segmentIds)
    || !value.segmentIds.every((entry): entry is LearningPhaseId =>
      typeof entry === 'string' && phaseIds.has(entry))
    || !equals(value.segmentIds, expectedIds)
  ) {
    return failure(`${path}.segmentIds`, 'must match the approved learning path');
  }
  return {
    ok: true,
    value: { totalMinutes, segmentIds: value.segmentIds },
  };
}

function parseSegment(value: unknown, index: number): ParseResult<LessonSegment> {
  const path = `$.segments[${index}]`;
  if (!isRecord(value) || !hasExactKeys(value, [
    'id',
    'lesson',
    'minutes',
    'title',
    'learningFunction',
    'activityIds',
  ])) {
    return failure(path, 'must contain exactly the approved segment fields');
  }
  if (typeof value.id !== 'string' || !phaseIds.has(value.id)) {
    return failure(`${path}.id`, 'must be an approved learning phase');
  }
  if (!Number.isInteger(value.lesson) || (value.lesson as number) < 1 || (value.lesson as number) > 6) {
    return failure(`${path}.lesson`, 'must be an integer from 1 to 6');
  }
  if (!Number.isInteger(value.minutes) || (value.minutes as number) < 1) {
    return failure(`${path}.minutes`, 'must be a positive integer');
  }
  if (!isNonEmptyString(value.title) || !isNonEmptyString(value.learningFunction)) {
    return failure(path, 'title and learningFunction must be non-empty strings');
  }
  if (
    !Array.isArray(value.activityIds)
    || value.activityIds.length === 0
    || !value.activityIds.every(isIdentifier)
    || !hasUniqueValues(value.activityIds)
  ) {
    return failure(`${path}.activityIds`, 'must contain unique activity identifiers');
  }
  return {
    ok: true,
    value: {
      id: value.id as LearningPhaseId,
      lesson: value.lesson as 1 | 2 | 3 | 4 | 5 | 6,
      minutes: value.minutes as number,
      title: value.title,
      learningFunction: value.learningFunction,
      activityIds: value.activityIds,
    },
  };
}

function parseActivity(value: unknown, index: number): ParseResult<WorkbenchContent['activities'][number]> {
  const path = `$.activities[${index}]`;
  if (!isRecord(value) || !hasExactKeys(value, [
    'id',
    'family',
    'title',
    'instruction',
    'scenarioIds',
  ])) {
    return failure(path, 'must contain exactly the approved activity fields');
  }
  if (!isIdentifier(value.id)) {
    return failure(`${path}.id`, 'must be a kebab-case identifier');
  }
  if (
    typeof value.family !== 'string'
    || !activityFamilies.has(value.family as ActivityFamily)
  ) {
    return failure(`${path}.family`, 'must be an approved activity family');
  }
  if (!isNonEmptyString(value.title) || !isNonEmptyString(value.instruction)) {
    return failure(path, 'title and instruction must be non-empty strings');
  }
  if (
    !Array.isArray(value.scenarioIds)
    || !value.scenarioIds.every((entry): entry is WorkbenchScenarioId =>
      typeof entry === 'string' && scenarioIds.has(entry))
    || !hasUniqueValues(value.scenarioIds)
  ) {
    return failure(`${path}.scenarioIds`, 'must contain only unique approved scenarios');
  }
  return {
    ok: true,
    value: {
      id: value.id,
      family: value.family as ActivityFamily,
      title: value.title,
      instruction: value.instruction,
      scenarioIds: value.scenarioIds,
    },
  };
}

function parseTextEntries(
  value: unknown,
  path: string,
  expectedCount?: number,
): ParseResult<readonly Readonly<{ id: string; title?: string; text: string }>[]> {
  if (!Array.isArray(value) || (expectedCount !== undefined && value.length !== expectedCount)) {
    return failure(path, expectedCount === undefined
      ? 'must be an array'
      : `must contain exactly ${expectedCount} entries`);
  }
  const entries: Readonly<{ id: string; title?: string; text: string }>[] = [];
  for (const [index, candidate] of value.entries()) {
    if (!isRecord(candidate)) {
      return failure(`${path}[${index}]`, 'must be an object');
    }
    const titled = 'title' in candidate;
    const keys = titled ? ['id', 'title', 'text'] : ['id', 'text'];
    if (
      !hasExactKeys(candidate, keys)
      || !isIdentifier(candidate.id)
      || !isNonEmptyString(candidate.text)
      || (titled && !isNonEmptyString(candidate.title))
    ) {
      return failure(`${path}[${index}]`, 'must contain approved non-empty text fields');
    }
    entries.push(titled
      ? { id: candidate.id, title: candidate.title as string, text: candidate.text }
      : { id: candidate.id, text: candidate.text });
  }
  if (!hasUniqueValues(entries.map((entry) => entry.id))) {
    return failure(path, 'entry identifiers must be unique');
  }
  return { ok: true, value: entries };
}

function parseTransferCases(value: unknown): ParseResult<WorkbenchContent['transferCases']> {
  if (!Array.isArray(value) || value.length !== TRANSFER_CASE_IDS.length) {
    return failure('$.transferCases', 'must contain exactly the six approved cases');
  }
  const cases: WorkbenchContent['transferCases'][number][] = [];
  for (const [index, candidate] of value.entries()) {
    const path = `$.transferCases[${index}]`;
    if (
      !isRecord(candidate)
      || !hasExactKeys(candidate, ['id', 'title', 'description'])
      || candidate.id !== TRANSFER_CASE_IDS[index]
      || !isNonEmptyString(candidate.title)
      || !isNonEmptyString(candidate.description)
    ) {
      return failure(path, 'must match the approved transfer case without a solution field');
    }
    cases.push({
      id: candidate.id as TransferCaseId,
      title: candidate.title,
      description: candidate.description,
    });
  }
  return { ok: true, value: cases };
}

function parseContent(value: unknown): ParseResult<WorkbenchContent> {
  if (!isRecord(value) || !hasExactKeys(value, [
    'schemaVersion',
    'moduleId',
    'centralQuestion',
    'paths',
    'segments',
    'activities',
    'supports',
    'transferCases',
    'selfCheckQuestions',
  ])) {
    return failure('$', 'must contain exactly the approved content fields');
  }
  if (value.schemaVersion !== 1 || value.moduleId !== 'IUM-5-CORE-05') {
    return failure('$', 'must bind schema version 1 and IUM-5-CORE-05');
  }
  if (!isNonEmptyString(value.centralQuestion)) {
    return failure('$.centralQuestion', 'must be a non-empty string');
  }
  if (!isRecord(value.paths) || !hasExactKeys(value.paths, ['regular', 'extended'])) {
    return failure('$.paths', 'must contain exactly regular and extended');
  }
  const regularPath = parsePath(value.paths.regular, '$.paths.regular', 225, REGULAR_PHASE_IDS);
  if (!regularPath.ok) {
    return regularPath;
  }
  const extendedPath = parsePath(value.paths.extended, '$.paths.extended', 270, ALL_PHASE_IDS);
  if (!extendedPath.ok) {
    return extendedPath;
  }
  if (!Array.isArray(value.segments) || value.segments.length !== ALL_PHASE_IDS.length) {
    return failure('$.segments', 'must contain exactly twelve learning segments');
  }
  const segments: LessonSegment[] = [];
  for (const [index, candidate] of value.segments.entries()) {
    const segment = parseSegment(candidate, index);
    if (!segment.ok) {
      return segment;
    }
    segments.push(segment.value);
  }
  if (!equals(segments.map((segment) => segment.id), ALL_PHASE_IDS)) {
    return failure('$.segments', 'must follow the approved phase order');
  }
  const minutesById = new Map(segments.map((segment) => [segment.id, segment.minutes]));
  const regularMinutes = REGULAR_PHASE_IDS.reduce(
    (sum, id) => sum + (minutesById.get(id) ?? 0),
    0,
  );
  const extendedMinutes = ALL_PHASE_IDS.reduce(
    (sum, id) => sum + (minutesById.get(id) ?? 0),
    0,
  );
  if (regularMinutes !== 225 || extendedMinutes !== 270) {
    return failure('$.segments', 'segment minutes must add up to 225 and 270');
  }
  if (!Array.isArray(value.activities) || value.activities.length < 5) {
    return failure('$.activities', 'must represent all five activity families');
  }
  const activities: WorkbenchContent['activities'][number][] = [];
  for (const [index, candidate] of value.activities.entries()) {
    const activity = parseActivity(candidate, index);
    if (!activity.ok) {
      return activity;
    }
    activities.push(activity.value);
  }
  if (!hasUniqueValues(activities.map((activity) => activity.id))) {
    return failure('$.activities', 'activity identifiers must be unique');
  }
  const representedFamilies = new Set(activities.map((activity) => activity.family));
  if (
    representedFamilies.size !== activityFamilies.size
    || [...activityFamilies].some((family) => !representedFamilies.has(family))
  ) {
    return failure('$.activities', 'must represent exactly all five activity families');
  }
  const activityIds = new Set(activities.map((activity) => activity.id));
  const referencedActivityIds = new Set(segments.flatMap((segment) => segment.activityIds));
  if (
    [...referencedActivityIds].some((id) => !activityIds.has(id))
    || [...activityIds].some((id) => !referencedActivityIds.has(id))
  ) {
    return failure('$.segments', 'all activity references must resolve in both directions');
  }
  const supports = parseTextEntries(value.supports, '$.supports');
  if (!supports.ok || supports.value.length < 6 || supports.value.some((entry) => entry.title === undefined)) {
    return failure('$.supports', 'must contain the four supports and two explicit language/revision aids');
  }
  const transferCases = parseTransferCases(value.transferCases);
  if (!transferCases.ok) {
    return transferCases;
  }
  const selfCheckQuestions = parseTextEntries(
    value.selfCheckQuestions,
    '$.selfCheckQuestions',
    4,
  );
  if (!selfCheckQuestions.ok || selfCheckQuestions.value.some((entry) => entry.title !== undefined)) {
    return failure('$.selfCheckQuestions', 'must contain exactly four untitled questions');
  }
  return {
    ok: true,
    value: {
      schemaVersion: 1,
      moduleId: 'IUM-5-CORE-05',
      centralQuestion: value.centralQuestion,
      paths: {
        regular: {
          totalMinutes: 225,
          segmentIds: regularPath.value.segmentIds,
        },
        extended: {
          totalMinutes: 270,
          segmentIds: extendedPath.value.segmentIds,
        },
      },
      segments,
      activities,
      supports: supports.value.map((entry) => ({
        id: entry.id,
        title: entry.title as string,
        text: entry.text,
      })),
      transferCases: transferCases.value,
      selfCheckQuestions: selfCheckQuestions.value.map((entry) => ({
        id: entry.id,
        text: entry.text,
      })),
    },
  };
}

function parseScenarioResources(value: unknown): ParseResult<WorkbenchResources['scenarios']> {
  if (!Array.isArray(value) || value.length !== WORKBENCH_SCENARIO_IDS.length) {
    return failure('$.scenarios', 'must contain exactly ten scenarios');
  }
  const resources: WorkbenchResources['scenarios'][number][] = [];
  for (const [index, candidate] of value.entries()) {
    const path = `$.scenarios[${index}]`;
    if (!isRecord(candidate) || !hasExactKeys(candidate, [
      'scenario',
      'starterAlgorithm',
      'referenceAlgorithm',
    ])) {
      return failure(path, 'must contain exactly scenario, starterAlgorithm and referenceAlgorithm');
    }
    const scenario = parseScenario(candidate.scenario);
    if (!scenario.ok) {
      return failure(`${path}.scenario`, scenario.issues[0]?.message ?? 'invalid scenario');
    }
    const expectedId = WORKBENCH_SCENARIO_IDS[index];
    if (scenario.value.id !== expectedId) {
      return failure(`${path}.scenario.id`, `must be ${expectedId}`);
    }
    const referenceAlgorithm = parseAlgorithm(candidate.referenceAlgorithm);
    if (!referenceAlgorithm.ok || referenceAlgorithm.value.length === 0) {
      return failure(`${path}.referenceAlgorithm`, 'must be a non-empty valid algorithm');
    }
    const isProduct = productScenarioIds.has(expectedId);
    let starterAlgorithm: Algorithm | null = null;
    if (isProduct) {
      if (candidate.starterAlgorithm !== null) {
        return failure(`${path}.starterAlgorithm`, 'product cards must start without an algorithm');
      }
    } else {
      const parsedStarter = parseAlgorithm(candidate.starterAlgorithm);
      if (!parsedStarter.ok || parsedStarter.value.length === 0) {
        return failure(`${path}.starterAlgorithm`, 'must be a non-empty valid starter algorithm');
      }
      starterAlgorithm = parsedStarter.value;
    }
    resources.push({
      scenario: scenario.value,
      starterAlgorithm,
      referenceAlgorithm: referenceAlgorithm.value,
    });
  }
  return { ok: true, value: resources };
}

export function parseWorkbenchResources(
  contentValue: unknown,
  scenariosValue: unknown,
): ParseResult<WorkbenchResources> {
  const content = parseContent(contentValue);
  if (!content.ok) {
    return content;
  }
  const scenarios = parseScenarioResources(scenariosValue);
  if (!scenarios.ok) {
    return scenarios;
  }
  return { ok: true, value: { content: content.value, scenarios: scenarios.value } };
}
