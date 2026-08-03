export const MODULE_ID = 'IUM-5-CORE-05' as const;
export const MODULE_VERSION = '0.1.0' as const;
export const PAYLOAD_SCHEMA_VERSION = 1 as const;
export const MAX_EXECUTED_STEPS = 100 as const;
export const MAX_RATIONALE_CODEPOINTS = 500 as const;

export type Direction = 'north' | 'east' | 'south' | 'west';
export type Position = Readonly<{ column: number; row: number }>;
export type BasicCommandKind =
  | 'move'
  | 'turn-left'
  | 'turn-right'
  | 'pick-up'
  | 'drop';
export type BasicCommand = Readonly<{ id: string; kind: BasicCommandKind }>;
export type RepeatCommand = Readonly<{
  id: string;
  kind: 'repeat';
  count: number;
  body: readonly BasicCommand[];
}>;
export type Command = BasicCommand | RepeatCommand;
export type Algorithm = readonly Command[];

export type WorldState = Readonly<{
  position: Position;
  direction: Direction;
  carrying: boolean;
  itemPosition: Position | null;
  delivered: boolean;
}>;

export type Scenario = Readonly<{
  id: string;
  title: string;
  width: number;
  height: number;
  start: Readonly<{
    position: Position;
    direction: Direction;
    carrying: false;
  }>;
  itemPosition: Position;
  targetPosition: Position;
  obstacles: readonly Position[];
}>;

export type InterpreterErrorCode =
  | 'OBSTACLE'
  | 'OUT_OF_BOUNDS'
  | 'INVALID_PICK_UP'
  | 'INVALID_DROP'
  | 'INVALID_REPEAT'
  | 'STEP_LIMIT';

export type TraceEntry = Readonly<{
  step: number;
  sourceCommandId: string;
  commandKind: BasicCommandKind | 'repeat';
  loop: Readonly<{ iteration: number; total: number }> | null;
  before: WorldState;
  after: WorldState;
  outcome: 'ok' | 'error';
  error: InterpreterErrorCode | null;
}>;
