import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as status from '../../packages/project-status/index.mjs';
import Ajv2020 from 'ajv/dist/2020.js';

const acceptance = kind => JSON.parse(readFileSync(new URL(`../../roadmap/v2/follow-ups/${kind}/acceptance.json`,import.meta.url)));
test('an accepted pilot instrument does not assert a completed real pilot',()=>{
  assert.equal(typeof status.resolveFollowUpState,'function','Missing current FU projection');
  assert.deepEqual(status.resolveFollowUpState(acceptance('pilot')),
    {workStatus:'done',pilot:'not-started',publication:'closed'});
});
test('technical audit and module design acceptance do not assert implementation',()=>{
  assert.equal(typeof status.resolveFollowUpState,'function');
  for(const kind of ['technical','reference-module']) {
    const result=status.resolveFollowUpState(acceptance(kind));
    assert.equal(result.workStatus,'done');assert.equal(result.publication,'closed');
    assert.equal(result.pilot,'not-started');assert.equal(result.implementation,undefined);
  }
});
test('unknown or conflicting acceptance data fails closed',()=>{
  assert.equal(typeof status.resolveFollowUpState,'function');
  for(const patch of [{state:'passed'},{taskId:'OTHER'},{scope:'real-pilot'},
      {pilot:'passed'},{publication:'open'},{acceptedCommit:'150deea'}]) {
    assert.throws(()=>status.resolveFollowUpState({...acceptance('pilot'),...patch}));
  }
});

test('development evidence cannot serialize private local paths into a projection',()=>{
  const snapshot={evidence:[],development:{packages:[{checks:[{summary:'C:\\Users\\Private\\evidence.txt'}]}]}};
  for(const mode of ['presentation','internal'])assert.throws(()=>status.project(snapshot,mode),/lokaler Pfad/);
});

test('published JSON Schema rejects unknown nested fields and false success metadata',()=>{
  const schema=JSON.parse(readFileSync(new URL('../../schemas/v2/implementation.schema.json',import.meta.url)));
  const validate=new Ajv2020({strict:true,allErrors:true}).compile(schema);
  for(const name of ['authorization','change-plan','progress']) {
    const record=JSON.parse(readFileSync(new URL(`../../roadmap/v2/implementation/${name}.json`,import.meta.url)));
    assert.equal(validate(record),true,JSON.stringify(validate.errors));
    const bad=structuredClone(record);bad.autoApprove=true;assert.equal(validate(bad),false);
    const nested=structuredClone(record);
    if(name==='progress')nested.packages[0].state='probably-done';
    else if(name==='authorization')nested.requests[0].decisionBy='assistant';
    else nested.packages[0].files.push(nested.packages[0].files[0]);
    assert.equal(validate(nested),false);
  }
});
