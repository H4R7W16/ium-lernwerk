/** Internal design verification, not a V2 module/adapter or learner material. */
import assert from 'node:assert/strict';
import { writeFileSync } from 'node:fs';
import { beginExecution, finishExecution } from '../../../../packages/ium-5-core-05/src/interpreter.js';
import type { Algorithm, Scenario } from '../../../../packages/ium-5-core-05/src/model.js';

// Current V1 schema requires transport fields. They are unused in these probes.
function grid(id: string, width: number, height: number, column: number, row: number,
  direction: 'north' | 'east'): Scenario {
  return { id, title: id, width, height,
    start: { position: { column, row }, direction, carrying: false },
    itemPosition: { column, row }, targetPosition: { column, row }, obstacles: [] };
}
const action = (id: string, kind: 'move' | 'turn-left' | 'turn-right') => ({ id, kind });
const square = [{ id: 'cmd-1', kind: 'repeat', count: 4,
  body: [action('cmd-2','move'), action('cmd-3','turn-left')] }] as const;
const faulty = [{ id: 'cmd-1', kind: 'repeat', count: 4,
  body: [action('cmd-2','move')] }, action('cmd-3','turn-left')] as const;
const rectangle = [{ id: 'cmd-1', kind: 'repeat', count: 2,
  body: [action('cmd-2','move'), action('cmd-3','move'),
    action('cmd-4','turn-left'), action('cmd-5','move'), action('cmd-6','turn-left')] }] as const;
// The five-command body is a new design requirement, not supported by the old
// parser (maximum four). Unfold only this motion vector to check its geometry.
const unfoldedRectangle = [...rectangle[0].body,...rectangle[0].body]
  .map((c,i)=>action(`cmd-${i+1}`,c.kind));
const vectors: { id: string; scenario: Scenario; code: Algorithm;
  expected: { status: string; error: string | null; position: {column:number;row:number}; direction:string; steps:number } }[] = [
  { id:'S0', scenario:grid('mod-s0',3,3,1,3,'north'),
    code:[action('cmd-1','move'),action('cmd-2','turn-right'),action('cmd-3','move')],
    expected:{status:'complete',error:null,position:{column:2,row:2},direction:'east',steps:3} },
  { id:'S1', scenario:grid('mod-s1',4,4,2,3,'east'),code:square,
    expected:{status:'complete',error:null,position:{column:2,row:3},direction:'east',steps:8} },
  { id:'S2', scenario:grid('mod-s2',4,4,2,3,'east'),code:faulty,
    expected:{status:'error',error:'OUT_OF_BOUNDS',position:{column:4,row:3},direction:'east',steps:3} },
  { id:'S3-native-rejected', scenario:grid('mod-s3',5,4,1,3,'east'),code:rectangle,
    expected:{status:'error',error:'INVALID_REPEAT',position:{column:1,row:3},direction:'east',steps:1} },
  { id:'S3', scenario:grid('mod-s3',5,4,1,3,'east'),code:unfoldedRectangle,
    expected:{status:'complete',error:null,position:{column:1,row:3},direction:'east',steps:10} },
];
const results = vectors.map(v => {
  const result = finishExecution(beginExecution(v.scenario,v.code));
  const actual = { status:result.status,error:result.error,position:result.state.position,
    direction:result.state.direction,steps:result.trace.length };
  assert.deepEqual(actual,v.expected,v.id);
  return { id:v.id, actual, trace:result.trace.map(t=>({step:t.step,kind:t.commandKind,
    loop:t.loop,before:{position:t.before.position,direction:t.before.direction},
    after:{position:t.after.position,direction:t.after.direction},outcome:t.outcome})) };
});
const good = results.find(r=>r.id==='S1')!;
const bad = results.find(r=>r.id==='S2')!;
const firstDivergence = bad.trace.find(t =>
  JSON.stringify(t.after) !== JSON.stringify(good.trace[t.step-1].after))!.step;
assert.equal(firstDivergence,2);
assert.equal(bad.trace.find(t=>t.outcome==='error')!.step,3);
const s3=results.find(r=>r.id==='S3')!;
assert.deepEqual(s3.trace.filter(t=>t.kind==='move').map(t=>t.after.position),[
  {column:2,row:3},{column:3,row:3},{column:3,row:2},
  {column:2,row:2},{column:1,row:2},{column:1,row:3},
]);
// Empty code ends at the requested final state but visits none of the checkpoints.
// This proves final position/direction is insufficient; it is not a new goal checker.
const empty = finishExecution(beginExecution(vectors[3].scenario,[]));
assert.equal(empty.status,'complete');
assert.deepEqual(empty.state.position,s3.actual.position);
assert.equal(empty.state.direction,s3.actual.direction);
assert.equal(empty.trace.length,0);
const output = {asOf:'2026-09-07',method:'synthetic-existing-v1-interpreter',
  purpose:'Verify internal motion examples only; no V2 adapter/UI or learner evidence.',
  result:'passed',vectors:results,
  comparisons:[{id:'S2-first-divergence',step:2,technicalErrorStep:3,result:'passed'},
    {id:'S3-traversal',result:'passed'},
    {id:'S3-empty-counterexample',result:'passed',meaning:'Final state alone cannot prove task fulfillment.'}],
  manualOnly:['S4 transfer-state model','S5 system classification'],
  realDeviceVerification:'not-run',pilot:'not-started'};
writeFileSync(new URL('./semantics-results.json',import.meta.url),JSON.stringify(output,null,2)+'\n');
console.log('4 Bewegungsfälle, 1 erwartete V1-Parserablehnung und 3 Vergleichsprüfungen bestätigt; keine V2-Implementierung.');
