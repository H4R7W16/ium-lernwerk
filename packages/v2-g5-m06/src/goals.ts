import type { Goal, Position, Run, State } from './model.js';

export type GoalResult = Readonly<{
  ok: boolean;
  reason: 'complete' | 'missing-checkpoint' | 'wrong-end' | 'off-boundary' | 'execution-error';
}>;

function samePosition(left: Position, right: Position): boolean {
  return left.column === right.column && left.row === right.row;
}

function sameState(left: State, right: State): boolean {
  return samePosition(left.position, right.position) && left.direction === right.direction;
}

function onBoundary(position: Position, goal: Goal): boolean {
  const { left, right, top, bottom } = goal.boundary;
  const inside = position.column >= left && position.column <= right
    && position.row >= top && position.row <= bottom;
  return inside && (
    position.column === left || position.column === right
    || position.row === top || position.row === bottom
  );
}

export function checkGoal(execution: Run, goal: Goal): GoalResult {
  if (execution.status !== 'complete') return { ok: false, reason: 'execution-error' };
  const movementSteps = execution.trace.filter((entry) =>
    entry.error === null && !samePosition(entry.before.position, entry.after.position));
  if (movementSteps.length === 0) return { ok: false, reason: 'missing-checkpoint' };

  let checkpointIndex = 0;
  for (const entry of movementSteps) {
    const expected = goal.checkpoints[checkpointIndex];
    if (expected !== undefined && samePosition(entry.after.position, expected)) {
      checkpointIndex += 1;
    }
  }
  if (checkpointIndex !== goal.checkpoints.length) {
    return { ok: false, reason: 'missing-checkpoint' };
  }
  if (movementSteps.some((entry) =>
    !onBoundary(entry.before.position, goal) || !onBoundary(entry.after.position, goal))) {
    return { ok: false, reason: 'off-boundary' };
  }
  if (!sameState(execution.state, goal.end)) return { ok: false, reason: 'wrong-end' };
  return { ok: true, reason: 'complete' };
}
