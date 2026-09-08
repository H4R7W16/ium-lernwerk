export const MODULE_ID = 'V2-G5-M06' as const;
export const MODULE_VERSION = '0.1.0' as const;
export const DOSSIER_SCHEMA_VERSION = 1 as const;
export const MAX_EXECUTED_ACTIONS = 100 as const;
export const MAX_SHORT_TEXT_CODEPOINTS = 500 as const;
export const MAX_RETURN_TEXT_CODEPOINTS = 200 as const;

export type Direction = 'north' | 'east' | 'south' | 'west';
export type Position = Readonly<{ column: number; row: number }>;
export type State = Readonly<{ position: Position; direction: Direction }>;
export type Basic = Readonly<{
  id: string;
  kind: 'move' | 'turn-left' | 'turn-right';
}>;
export type Repeat = Readonly<{
  id: string;
  kind: 'repeat';
  count: number;
  body: readonly Basic[];
}>;
export type Program = readonly (Basic | Repeat)[];
export type Grid = Readonly<{ width: number; height: number; start: State }>;
export type TraceStep = Readonly<{
  step: number;
  commandId: string;
  iteration: number | null;
  before: State;
  after: State;
  error: 'OUT_OF_BOUNDS' | null;
}>;
export type Run = Readonly<{
  state: State;
  trace: readonly TraceStep[];
  status: 'complete' | 'OUT_OF_BOUNDS' | 'STEP_LIMIT';
}>;
export type Goal = Readonly<{
  checkpoints: readonly Position[];
  end: State;
  boundary: Readonly<{ left: number; right: number; top: number; bottom: number }>;
}>;
export type ParseResult<T> =
  | Readonly<{ ok: true; value: T }>
  | Readonly<{ ok: false; issues: readonly string[] }>;
