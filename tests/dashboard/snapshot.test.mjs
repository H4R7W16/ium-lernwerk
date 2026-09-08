import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { stringify } from 'yaml';
import { buildSnapshot, markdown, project } from '../../packages/project-status/index.mjs';

const repo = resolve(dirname(fileURLToPath(import.meta.url)),'../..');
const manifest = JSON.parse(readFileSync(join(repo,'roadmap/v2/dashboard/gates.json')));
const seed = JSON.parse(readFileSync(join(repo,'roadmap/v2/dashboard/editorial-seed.json')));
const implementationPlan = JSON.parse(readFileSync(join(repo,'roadmap/v2/implementation-planning/plan.json')));
const authorization = JSON.parse(readFileSync(join(repo,'roadmap/v2/implementation/authorization.json')));
const progress = JSON.parse(readFileSync(join(repo,'roadmap/v2/implementation/progress.json')));
const cutoverReview = JSON.parse(readFileSync(join(repo,'roadmap/v2/cutover/review.json')));
function fixture(mutate = () => {}) {
  const vault = mkdtempSync(join(tmpdir(),'ium-dash-vault-')), d = structuredClone(seed);
  for (const [i,g] of manifest.entries()) {
    const file = join(vault,g.path); mkdirSync(dirname(file),{recursive:true});
    const approval = cutoverReview.gates[i]?.approvalEvidence.excerpt
      ?? 'V2-Aktivierung freigegeben. 0032509af1dfe758548f34f37bb633bae403a9fa';
    writeFileSync(file,`---\nstatus: done\nsequence: ${i+1}\nstrand: ium-v2-rebaseline\nowner_agent: Codex\nupdated: 2026-09-06\n---\n# ${g.id} Synthetischer Test-Gate\n${approval}\n`);
  }
  const taskRoot='60_Organisation/Workspace-Entwicklung/Tasks/';
  const task=(path,state,body)=>{
    const file=join(vault,path);mkdirSync(dirname(file),{recursive:true});
    writeFileSync(file,`---\nstatus: ${state}\nowner_agent: Codex\n---\n# Synthetischer Taskbeleg\n${body}\n`);
  };
  task(taskRoot+'2026-09-07 - IUM-V2-PLAN Referenzmodul-Implementierung planen.md','done',
    `${authorization.acceptedPlanCommit}\n${authorization.planAcceptance.statement}\n${authorization.requests[0].statement}`);
  for(const [i,p] of implementationPlan.packages.entries()) task(p.taskPath,
    progress.packages[i].state==='planned'?'blocked':progress.packages[i].state,'synthetic');
  for(const [folder,name] of [
    ['technical','2026-09-06 - IUM-V2-FU-TECH Technische V1-Bausteine gegen V2 prüfen.md'],
    ['reference-module','2026-09-06 - IUM-V2-FU-MOD Erstes V2-Referenzmodul spezifizieren.md'],
    ['pilot','2026-09-06 - IUM-V2-FU-PILOT Prüf- und Pilotinstrumente an V2 binden.md'],
  ]) task(taskRoot+name,'done',JSON.parse(readFileSync(join(repo,`roadmap/v2/follow-ups/${folder}/acceptance.json`))).acceptedCommit);
  mutate(d,vault);
  const register = join(vault,'register.md');
  writeFileSync(register,'<!-- IUM-PROJECT-STATUS:START -->\n```yaml\n'+stringify(d)+'```\n<!-- IUM-PROJECT-STATUS:END -->');
  return {repo,vault,register};
}
test('actual source projection binds 18 gates and keeps R7 capacity/evidence open', () => {
  const s = buildSnapshot(fixture());
  assert.equal(s.gates.length,18);
  assert.deepEqual(s.grades[2].paths.map(p=>p.openCapacityRecordIds.length),[8,3,0]);
  assert.equal(s.openEvidence.inherited.length,6); assert.equal(s.openEvidence.new.length,3);
  assert.equal(s.warnings.length,2);
  const md = markdown(s);
  assert.match(md,/R7-CORE36 \| 36 UE \| 8 \| 3/);
  assert.ok(!JSON.stringify(project(s,'presentation')).includes('internal-review'));
  assert.ok(s.evidence.every(e=>!e.githubUrl || e.githubUrl.includes('/'+e.commit+'/')), 'Remote links must name the verified full source commit');
});
test('missing required source stops snapshot; historical optional omission is a warning', () => {
  assert.throws(()=>buildSnapshot(fixture(d=>d.evidence[0].target='missing-source.md')),/ENOENT/);
});
test('absolute paths in a selected source cannot enter the snapshot', () => {
  assert.throws(()=>buildSnapshot(fixture((d,vault)=>{
    d.evidence[0].kind='vault';d.evidence[0].target='source.md';writeFileSync(join(vault,'source.md'),'C:\\Users\\Someone\\secret.txt');
  })),/Absoluter lokaler Pfad/);
});
test('invalid task states fail closed instead of being silently shown as done', () => {
  assert.throws(()=>buildSnapshot(fixture((d,vault)=>{
    const p=join(vault,manifest[0].path);writeFileSync(p,readFileSync(p,'utf8').replace('status: done','status: green'));
  })),/Gate-Status|Vault-Freigabe nicht nachweisbar: IUM-V2-00/);
});
test('closed predecessor blocks DASH snapshot generation', () => {
  assert.throws(()=>buildSnapshot(fixture((d,vault)=>{
    const p=join(vault,manifest[15].path);writeFileSync(p,readFileSync(p,'utf8').replace('status: done','status: review'));
  })),/Vorgänger|Vault-Freigabe nicht nachweisbar: IUM-V2-R7/);
});
test('URI schemes are not mistaken for absolute drive paths', () => {
  const s = buildSnapshot(fixture());
  assert.match(s.evidence.find(e=>e.id==='archive').content,/https:\/\//);
});
test('stale CUT review metadata cannot coexist with the approved active pointer', () => {
  assert.throws(()=>buildSnapshot(fixture((d,vault)=>{
    const p=join(vault,manifest[17].path);
    writeFileSync(p,readFileSync(p,'utf8').replace('status: done','status: review'));
  })),/CUT-Status/);
});
test('active V2 retains product V1, every condition and all separate maturity axes', () => {
  const s=buildSnapshot(fixture());
  assert.equal(s.baseline.activeBaseline,'v2');
  assert.equal(s.baseline.productBaseline,'v1');
  assert.equal(s.baseline.cutover.state,'approved');
  assert.equal(s.gates[17].state,'done');
  assert.equal(s.cutover.conditions.length,46);
  assert.deepEqual(s.streams.map(x=>x.maturity),seed.streams.map(x=>x.maturity));
  assert.match(markdown(s),/V2: aktive Planungs-/);
});

test('follow-up approvals are current while pilot and future packages remain open',()=>{
  const s=buildSnapshot(fixture());
  assert.deepEqual(s.followUps.map(x=>x.state),['done','done','done']);
  assert.deepEqual(s.development.authorizedPackages,['IMP01']);
  assert.equal(s.development.packages[1].state,'planned');
  assert.equal(s.development.limits.pilot,'not-started');
  assert.match(markdown(s),/FU-PILOT/);
});

test('a conflicting current follow-up task cannot be rendered as accepted',()=>{
  assert.throws(()=>buildSnapshot(fixture((_d,vault)=>{
    const path=join(vault,'60_Organisation/Workspace-Entwicklung/Tasks/2026-09-06 - IUM-V2-FU-PILOT Prüf- und Pilotinstrumente an V2 binden.md');
    writeFileSync(path,readFileSync(path,'utf8').replace('status: done','status: review'));
  })),/Vault-Task/);
});
