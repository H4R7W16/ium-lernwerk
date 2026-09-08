import {
  DOSSIER_SCHEMA_VERSION,
  MAX_EXECUTED_ACTIONS,
  MAX_RETURN_TEXT_CODEPOINTS,
  MAX_SHORT_TEXT_CODEPOINTS,
  type ParseResult,
  type Program,
  type Run,
  type State,
} from './model.js';
import {
  executedActionCount,
  failure,
  hasExactKeys,
  isRecord,
  parseProgram,
  parseState,
} from './validation.js';

export type Diagram = Readonly<{ program: Program; explanation: string }>;
export type Evidence = Readonly<{
  program: Program;
  predicted: State | null;
  steps: readonly number[];
  rationale: string;
}>;
export type Dossier = Readonly<{
  schemaVersion: 1;
  p1: Readonly<{ diagram: Diagram }>;
  p2: Readonly<{
    before: Evidence;
    after: Evidence;
    firstDeviation: number | null;
  }>;
  p3: Readonly<{
    diagram: Diagram;
    draftProgram: Program;
    evidence: Evidence;
  }>;
  p5: Readonly<{
    sequence: readonly ('aufnehmen' | 'prüfen' | 'ablegen')[];
    rationale: string;
  }>;
  p6: Readonly<{
    timeControl: string;
    routeCalculation: string;
    boundary: string;
  }>;
  returnNote: Readonly<{
    area: 'auftrag' | 'dossier' | 'sicherung';
    openPoint: string;
    nextAction: string;
  }>;
}>;

export type SessionState = Readonly<{
  dossier: Dossier;
  p0: string;
  p4: string;
  selectedHelp: 'H1' | 'H2' | 'H3' | 'H4' | null;
  currentRun: Run | null;
}>;

function textField(
  input: unknown,
  path: string,
  maximum: number = MAX_SHORT_TEXT_CODEPOINTS,
): ParseResult<string> {
  if (typeof input !== 'string') return failure(path, 'must be a string');
  if ([...input].length > maximum) {
    return failure(path, `must contain at most ${maximum} Unicode codepoints`);
  }
  return { ok: true, value: input };
}

function parseDiagram(input: unknown, path: string): ParseResult<Diagram> {
  if (!isRecord(input) || !hasExactKeys(input, ['program', 'explanation'])) {
    return failure(path, 'must contain exactly program and explanation');
  }
  const program = parseProgram(input.program);
  if (!program.ok) return failure(`${path}.program`, program.issues.join('; '));
  const explanation = textField(input.explanation, `${path}.explanation`);
  if (!explanation.ok) return explanation;
  return { ok: true, value: { program: program.value, explanation: explanation.value } };
}

function parseEvidence(input: unknown, path: string): ParseResult<Evidence> {
  if (!isRecord(input)
    || !hasExactKeys(input, ['program', 'predicted', 'steps', 'rationale'])) {
    return failure(path, 'must contain exactly program, predicted, steps and rationale');
  }
  const program = parseProgram(input.program);
  if (!program.ok) return failure(`${path}.program`, program.issues.join('; '));
  let predicted: State | null = null;
  if (input.predicted !== null) {
    const parsed = parseState(input.predicted, `${path}.predicted`);
    if (!parsed.ok) return parsed;
    predicted = parsed.value;
  }
  if (!Array.isArray(input.steps)) return failure(`${path}.steps`, 'must be an array');
  const maximumStep = Math.min(executedActionCount(program.value), MAX_EXECUTED_ACTIONS);
  const steps: number[] = [];
  const seen = new Set<number>();
  for (const [index, step] of input.steps.entries()) {
    if (!Number.isInteger(step) || (step as number) < 1 || (step as number) > maximumStep) {
      return failure(
        `${path}.steps[${index}]`,
        'must identify an action in this evidence program, up to action 100',
      );
    }
    if (seen.has(step as number)) {
      return failure(`${path}.steps[${index}]`, 'must not duplicate a selected step');
    }
    seen.add(step as number);
    steps.push(step as number);
  }
  const rationale = textField(input.rationale, `${path}.rationale`);
  if (!rationale.ok) return rationale;
  return { ok: true, value: { program: program.value, predicted, steps, rationale: rationale.value } };
}

function parseP1(input: unknown): ParseResult<Dossier['p1']> {
  if (!isRecord(input) || !hasExactKeys(input, ['diagram'])) {
    return failure('$.p1', 'must contain exactly diagram');
  }
  const diagram = parseDiagram(input.diagram, '$.p1.diagram');
  return diagram.ok ? { ok: true, value: { diagram: diagram.value } } : diagram;
}

function parseP2(input: unknown): ParseResult<Dossier['p2']> {
  if (!isRecord(input) || !hasExactKeys(input, ['before', 'after', 'firstDeviation'])) {
    return failure('$.p2', 'must contain exactly before, after and firstDeviation');
  }
  const before = parseEvidence(input.before, '$.p2.before');
  if (!before.ok) return before;
  const after = parseEvidence(input.after, '$.p2.after');
  if (!after.ok) return after;
  const maximum = Math.min(
    Math.max(executedActionCount(before.value.program), executedActionCount(after.value.program)),
    MAX_EXECUTED_ACTIONS,
  );
  if (input.firstDeviation !== null && (
    !Number.isInteger(input.firstDeviation)
    || (input.firstDeviation as number) < 1
    || (input.firstDeviation as number) > maximum
  )) {
    return failure('$.p2.firstDeviation', 'must identify an action in the compared programs');
  }
  return {
    ok: true,
    value: {
      before: before.value,
      after: after.value,
      firstDeviation: input.firstDeviation as number | null,
    },
  };
}

function parseP3(input: unknown): ParseResult<Dossier['p3']> {
  if (!isRecord(input)
    || !hasExactKeys(input, ['diagram', 'draftProgram', 'evidence'])) {
    return failure('$.p3', 'must contain exactly diagram, draftProgram and evidence');
  }
  const diagram = parseDiagram(input.diagram, '$.p3.diagram');
  if (!diagram.ok) return diagram;
  const draftProgram = parseProgram(input.draftProgram);
  if (!draftProgram.ok) return failure('$.p3.draftProgram', draftProgram.issues.join('; '));
  const evidence = parseEvidence(input.evidence, '$.p3.evidence');
  if (!evidence.ok) return evidence;
  return {
    ok: true,
    value: { diagram: diagram.value, draftProgram: draftProgram.value, evidence: evidence.value },
  };
}

function parseP5(input: unknown): ParseResult<Dossier['p5']> {
  if (!isRecord(input) || !hasExactKeys(input, ['sequence', 'rationale'])) {
    return failure('$.p5', 'must contain exactly sequence and rationale');
  }
  if (!Array.isArray(input.sequence)) return failure('$.p5.sequence', 'must be an array');
  const allowed = new Set(['aufnehmen', 'prüfen', 'ablegen']);
  if (!input.sequence.every((entry) => typeof entry === 'string' && allowed.has(entry))) {
    return failure('$.p5.sequence', 'contains an unknown manual transfer action');
  }
  const rationale = textField(input.rationale, '$.p5.rationale');
  if (!rationale.ok) return rationale;
  return {
    ok: true,
    value: {
      sequence: [...input.sequence] as Dossier['p5']['sequence'],
      rationale: rationale.value,
    },
  };
}

function parseP6(input: unknown): ParseResult<Dossier['p6']> {
  if (!isRecord(input)
    || !hasExactKeys(input, ['timeControl', 'routeCalculation', 'boundary'])) {
    return failure('$.p6', 'must contain exactly timeControl, routeCalculation and boundary');
  }
  const timeControl = textField(input.timeControl, '$.p6.timeControl');
  if (!timeControl.ok) return timeControl;
  const routeCalculation = textField(input.routeCalculation, '$.p6.routeCalculation');
  if (!routeCalculation.ok) return routeCalculation;
  const boundary = textField(input.boundary, '$.p6.boundary');
  if (!boundary.ok) return boundary;
  return {
    ok: true,
    value: {
      timeControl: timeControl.value,
      routeCalculation: routeCalculation.value,
      boundary: boundary.value,
    },
  };
}

function parseReturnNote(input: unknown): ParseResult<Dossier['returnNote']> {
  if (!isRecord(input) || !hasExactKeys(input, ['area', 'openPoint', 'nextAction'])) {
    return failure('$.returnNote', 'must contain exactly area, openPoint and nextAction');
  }
  if (input.area !== 'auftrag' && input.area !== 'dossier' && input.area !== 'sicherung') {
    return failure('$.returnNote.area', 'must be auftrag, dossier or sicherung');
  }
  const openPoint = textField(input.openPoint, '$.returnNote.openPoint', MAX_RETURN_TEXT_CODEPOINTS);
  if (!openPoint.ok) return openPoint;
  const nextAction = textField(input.nextAction, '$.returnNote.nextAction', MAX_RETURN_TEXT_CODEPOINTS);
  if (!nextAction.ok) return nextAction;
  return {
    ok: true,
    value: { area: input.area, openPoint: openPoint.value, nextAction: nextAction.value },
  };
}

export function parseDossier(input: unknown): ParseResult<Dossier> {
  if (!isRecord(input) || !hasExactKeys(input, [
    'schemaVersion', 'p1', 'p2', 'p3', 'p5', 'p6', 'returnNote',
  ])) {
    return failure('$', 'must contain exactly the approved dossier fields');
  }
  if (input.schemaVersion !== DOSSIER_SCHEMA_VERSION) {
    return failure('$.schemaVersion', 'must equal 1');
  }
  const p1 = parseP1(input.p1);
  if (!p1.ok) return p1;
  const p2 = parseP2(input.p2);
  if (!p2.ok) return p2;
  const p3 = parseP3(input.p3);
  if (!p3.ok) return p3;
  const p5 = parseP5(input.p5);
  if (!p5.ok) return p5;
  const p6 = parseP6(input.p6);
  if (!p6.ok) return p6;
  const returnNote = parseReturnNote(input.returnNote);
  if (!returnNote.ok) return returnNote;
  return {
    ok: true,
    value: {
      schemaVersion: 1,
      p1: p1.value,
      p2: p2.value,
      p3: p3.value,
      p5: p5.value,
      p6: p6.value,
      returnNote: returnNote.value,
    },
  };
}

function emptyEvidence(): Evidence {
  return { program: [], predicted: null, steps: [], rationale: '' };
}

export function createInitialDossier(): Dossier {
  return {
    schemaVersion: 1,
    p1: { diagram: { program: [], explanation: '' } },
    p2: { before: emptyEvidence(), after: emptyEvidence(), firstDeviation: null },
    p3: {
      diagram: { program: [], explanation: '' },
      draftProgram: [],
      evidence: emptyEvidence(),
    },
    p5: { sequence: [], rationale: '' },
    p6: { timeControl: '', routeCalculation: '', boundary: '' },
    returnNote: { area: 'auftrag', openPoint: '', nextAction: '' },
  };
}

export function projectDossier(session: SessionState): Dossier {
  const parsed = parseDossier(session.dossier);
  if (!parsed.ok) throw new TypeError(`Invalid dossier: ${parsed.issues.join('; ')}`);
  const value = parsed.value;
  return {
    schemaVersion: 1,
    p1: { diagram: value.p1.diagram },
    p2: {
      before: value.p2.before,
      after: value.p2.after,
      firstDeviation: value.p2.firstDeviation,
    },
    p3: {
      diagram: value.p3.diagram,
      draftProgram: value.p3.draftProgram,
      evidence: value.p3.evidence,
    },
    p5: value.p5,
    p6: value.p6,
    returnNote: value.returnNote,
  };
}

function programsExactlyEqual(left: Program, right: Program): boolean {
  if (left.length !== right.length) return false;
  return left.every((leftCommand, index) => {
    const rightCommand = right[index];
    if (rightCommand === undefined
      || leftCommand.id !== rightCommand.id
      || leftCommand.kind !== rightCommand.kind) return false;
    if (leftCommand.kind !== 'repeat' || rightCommand.kind !== 'repeat') return true;
    return leftCommand.count === rightCommand.count
      && leftCommand.body.length === rightCommand.body.length
      && leftCommand.body.every((entry, bodyIndex) => {
        const other = rightCommand.body[bodyIndex];
        return other !== undefined && entry.id === other.id && entry.kind === other.kind;
      });
  });
}

export function evidenceBelongsToProgram(evidence: Evidence, program: Program): boolean {
  return programsExactlyEqual(evidence.program, program);
}
