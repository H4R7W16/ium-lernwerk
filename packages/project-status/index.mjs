import { readFileSync, writeFileSync, renameSync, mkdirSync, realpathSync, existsSync } from 'node:fs';
import { dirname, resolve, relative, isAbsolute } from 'node:path';
import { execFileSync } from 'node:child_process';
import { createHash, randomUUID } from 'node:crypto';
import { parseDocument } from 'yaml';

export const axes = { curriculum: 'Curriculumabdeckung', concept: 'Konzept', implementation: 'Implementierung', technical: 'Technische Verifikation', didactic: 'Fachlich-didaktischer Review', usage: 'Nutzungsprüfung', pilot: 'Unterrichtspilot', release: 'Publikations-/Releasefreigabe' };
export const labels = { unassessed: 'Nicht nachgewiesen', reviewed: 'Planung geprüft', draft: 'Entwurf', 'not-started': 'Nicht begonnen', 'not-run': 'Nicht geprüft', passed: 'Vertragsprüfung bestanden', closed: 'Geschlossen', planned: 'Geplant', in_progress: 'In Arbeit', review: 'Zur Abnahme', done: 'Freigegeben', blocked: 'Gesperrt', stale: 'Anderer Commit · veraltet' };
const workStates = ['planned', 'in_progress', 'review', 'done', 'blocked'];
const maturityStates = { curriculum: ['unassessed'], concept: ['draft', 'reviewed'], implementation: ['not-started'], technical: ['passed', 'not-run'], didactic: ['reviewed', 'not-started'], usage: ['not-started'], pilot: ['not-started'], release: ['closed'] };
const fail = message => { throw new Error(message); };
const check = (condition, message) => { if (!condition) fail(message); };
const object = v => v && typeof v === 'object' && !Array.isArray(v);
const text = v => typeof v === 'string' && v.trim().length > 0;
const sha = v => typeof v === 'string' && /^[a-f0-9]{40}$/.test(v);
const localPath = /(?:\b[a-z]:[\\/]|\\\\[^\\\s]+\\|(?:^|[\s"'])\/(?:Users|home|tmp|mnt|private|var)\/)/i;
const safeText = v => check(text(v) && !localPath.test(v), 'Leerer Text oder absoluter lokaler Pfad');
function keys(v, expected) { check(object(v) && Object.keys(v).sort().join('|') === [...expected].sort().join('|'), `Ungültige Felder: ${expected.join(', ')}`); }
function list(v) { check(Array.isArray(v) && v.length > 0, 'Liste fehlt'); }
function exactIds(items, ids) { list(items); check(items.map(x => x.id).sort().join('|') === [...ids].sort().join('|'), 'Pflicht-IDs fehlen oder sind doppelt'); }
export function parseRegister(markdown) {
  const matches = [...markdown.matchAll(/<!-- IUM-PROJECT-STATUS:START -->\s*```yaml\n([\s\S]*?)\n```\s*<!-- IUM-PROJECT-STATUS:END -->/g)];
  check(matches.length === 1, 'Genau ein Statusblock erforderlich');
  const doc = parseDocument(matches[0][1], { uniqueKeys: true });
  check(doc.errors.length === 0, 'Ungültiges YAML');
  return doc.toJS();
}
export function validateEditorial(d) {
  keys(d, ['schemaVersion','projectId','publicationScope','asOf','summary','currentFocus','nextDecision','streams','experienceAxes','uncertainties','technicalEvidence','evidence']);
  check(d.schemaVersion === 2 && d.projectId === 'ium-lernwerk' && d.publicationScope === 'local', 'Falscher Dashboardvertrag');
  check(/^\d{4}-\d{2}-\d{2}$/.test(d.asOf) && new Date(d.asOf).toISOString().slice(0,10) === d.asOf, 'Ungültiger Stichtag');
  safeText(d.summary);
  for (const part of [d.currentFocus, d.nextDecision]) { keys(part, ['title','summary','workStatus']); safeText(part.title); safeText(part.summary); check(workStates.includes(part.workStatus), 'Unbekannter Arbeitsstatus'); }
  list(d.evidence); const ids = new Set();
  for (const e of d.evidence) {
    keys(e, ['id','kind','target','label','visibility','required']);
    check(/^[a-z][a-z0-9-]*$/.test(e.id) && !ids.has(e.id), 'Doppelte/ungültige Evidenz-ID'); ids.add(e.id);
    check(['repo','vault'].includes(e.kind) && ['presentation','internal'].includes(e.visibility) && typeof e.required === 'boolean', 'Ungültige Evidenz');
    safeText(e.label); safeText(e.target);
    check(!isAbsolute(e.target) && !e.target.includes('\\') && !e.target.split('/').some(x => ['..','.',''].includes(x)) && !/[:?#%]/.test(e.target), 'Ungültiger Evidenzpfad');
  }
  function refs(v) { list(v); check(new Set(v).size === v.length, 'Doppelte Evidenzreferenz'); for (const id of v) check(d.evidence.some(e => e.id === id && e.visibility === 'presentation' && e.required), 'Präsentationsreferenz fehlt oder ist intern/optional'); }
  exactIds(d.streams, ['foundation','roadmap','platform','experience','validation-release']);
  for (const s of d.streams) {
    keys(s, ['id','title','summary','maturity','evidenceIds']); safeText(s.title); safeText(s.summary); refs(s.evidenceIds);
    keys(s.maturity, Object.keys(axes));
    for (const [k,v] of Object.entries(s.maturity)) check(maturityStates[k].includes(v), `Unbekannte oder noch nicht autorisierte Reife: ${k}`);
  }
  exactIds(d.experienceAxes, ['evidence','learner','architecture','material','interaction','orchestration','review','pilot']);
  for (const a of d.experienceAxes) { keys(a, ['id','label','state','evidenceIds']); safeText(a.label); check((a.id === 'pilot' ? ['not-started'] : ['reviewed','draft']).includes(a.state), 'Ungültige Experience-Reife'); refs(a.evidenceIds); }
  exactIds(d.uncertainties, ['capacity','privacy','cohort','governance']);
  for (const u of d.uncertainties) { keys(u, ['id','title','summary','evidenceIds']); safeText(u.title); safeText(u.summary); refs(u.evidenceIds); }
  keys(d.technicalEvidence, ['commit','date','state','scope']);
  check(sha(d.technicalEvidence.commit) && d.technicalEvidence.state === 'passed' && /^\d{4}-\d{2}-\d{2}$/.test(d.technicalEvidence.date), 'Ungültiger technischer Nachweis'); safeText(d.technicalEvidence.scope);
  return d;
}
export function atomicWrite(file, content, validate = () => {}) {
  validate(content); mkdirSync(dirname(file), { recursive: true });
  const temp = `${file}.${randomUUID()}.tmp`;
  writeFileSync(temp, content, { encoding: 'utf8', flag: 'wx' });
  renameSync(temp, file);
}
export function freshness(evidence, head) { return evidence.commit === head ? evidence.state : 'stale'; }
export function githubEvidence(commit, path, remoteReachable, identical) {
  return sha(commit) && remoteReachable && identical ? `https://github.com/H4R7W16/ium-lernwerk/blob/${commit}/${path.split('/').map(encodeURIComponent).join('/')}` : null;
}
export function project(snapshot, mode) {
  check(['presentation','internal'].includes(mode), 'Ungültiger Modus');
  const result = structuredClone(snapshot);
  result.evidence = result.evidence.filter(e => mode === 'internal' || e.visibility === 'presentation');
  // Never serialize private missing-source names in presentation mode.
  if (mode === 'presentation' && result.warnings) {
    const internalCount = result.warnings.filter(w=>w.visibility==='internal').length;
    result.warnings = result.warnings.filter(w=>w.visibility==='presentation');
    if (internalCount) result.warnings.push({message:`${internalCount} optionale historische Quellen fehlen; die aktuelle Planung ist davon unabhängig.`,visibility:'presentation'});
  }
  return { ...result, mode };
}
export function containedFile(root, target) {
  check(text(target) && !isAbsolute(target) && !target.includes('\\') && !target.split('/').some(x => ['..','.',''].includes(x)) && !/[:?#%]/.test(target), 'Unsicherer Quellpfad');
  const file = resolve(root, target), rel = relative(realpathSync(root), realpathSync(file));
  check(rel && !rel.startsWith('..') && !isAbsolute(rel), 'Quelle außerhalb des erlaubten Bereichs');
  return file;
}
export function buildSnapshot({ repo, vault, register }) {
  const git = (...args) => execFileSync('git', args, { cwd: repo, encoding: 'utf8', stdio: ['ignore','pipe','pipe'] }).trim();
  const d = validateEditorial(parseRegister(readFileSync(register, 'utf8')));
  const readJSON = p => JSON.parse(readFileSync(containedFile(repo,p), 'utf8'));
  const baseline = readJSON('roadmap/v2/status.json');
  check(baseline.activeBaseline === 'v1' && baseline.v2State === 'building' && baseline.contentProduction === 'frozen' && baseline.cutover.state === 'not-approved' && baseline.lxp05.state === 'frozen' && baseline.lxp05.integration === 'unmerged', 'DASH-Vertrag vor Cutover verletzt');
  const head = git('rev-parse','HEAD'); check(sha(head), 'HEAD fehlt');
  const warnings = [], evidence = [];
  for (const e of d.evidence) {
    let file;
    try { file = containedFile(e.kind === 'repo' ? repo : vault, e.target); }
    catch (err) { if (e.required || err.code !== 'ENOENT') throw err; warnings.push({ message: e.label, visibility: e.visibility }); continue; }
    const bytes = readFileSync(file), content = new TextDecoder('utf-8',{fatal:true}).decode(bytes);
    check(!localPath.test(content), `Absoluter lokaler Pfad in Beleg ${e.id}`);
    const digest = createHash('sha256').update(bytes).digest('hex');
    let commit = null, githubUrl = null, identical = false;
    if (e.kind === 'repo') {
      commit = git('log','-1','--format=%H','--',e.target) || null;
      if (commit) {
        const committed = execFileSync('git',['show',`${commit}:${e.target}`], { cwd: repo, stdio: ['ignore','pipe','pipe'] });
        // Git may normalize CRLF in the checkout. Compare semantic UTF-8 bytes.
        identical = committed.toString('utf8').replace(/\r\n/g,'\n') === content.replace(/\r\n/g,'\n');
        const reachable = Boolean(git('for-each-ref',`--contains=${commit}`,'--format=%(refname)','refs/remotes/origin'));
        githubUrl = githubEvidence(commit,e.target,reachable,identical);
      }
    }
    evidence.push({ ...e, digest, commit: identical ? commit : null, githubUrl, content, provenance: identical ? 'committed' : 'working-copy' });
  }
  const manifest = readJSON('roadmap/v2/dashboard/gates.json');
  const expected = ['IUM-V2-00','IUM-V2-01','IUM-V2-CUR','IUM-V2-SRC',...Array.from({length:7},(_,i)=>`LXF0${i+1}`),'IUM-V2-GOV','IUM-V2-AUD','IUM-V2-R5','IUM-V2-R6','IUM-V2-R7','IUM-V2-DASH','IUM-V2-CUT'];
  check(manifest.map(g=>g.id).join('|') === expected.join('|'), '18 Gates fehlen oder falsche Reihenfolge');
  const gates = manifest.map((g,i) => {
    keys(g,['id','path']);
    const content = readFileSync(containedFile(vault,g.path), 'utf8');
    const front = content.match(/^\uFEFF?---\r?\n([\s\S]*?)\r?\n---/); check(front, 'Task-Frontmatter fehlt');
    const doc = parseDocument(front[1],{uniqueKeys:true}); check(!doc.errors.length, 'Task-YAML ungültig'); const meta = doc.toJS();
    check(workStates.includes(meta.status) && meta.sequence === i+1 && meta.strand === 'ium-v2-rebaseline' && meta.owner_agent === 'Codex', 'Gate-Status/Sequenz/Verantwortung ungültig');
    if (i < 16) check(meta.status === 'done', 'DASH-Vorgänger nicht freigegeben');
    if (i === 16) check(['in_progress','review','done'].includes(meta.status), 'DASH nicht übernommen');
    if (i === 17) check(meta.status === 'planned', 'CUT nicht autorisiert');
    const title = content.match(/^# (.+)$/m)?.[1]; safeText(title);
    return { id:g.id, title, state:meta.status, date:meta.updated, sequence:i+1, source:g.path, digest:createHash('sha256').update(content).digest('hex') };
  });
  const grades = [5,6,7].map(grade => {
    const base = `roadmap/v2/grades/grade-${grade}/`, plan = readJSON(base+'roadmap.json'), status = readJSON(base+'status.json'), acceptance = readJSON(base+'acceptance.json');
    check(acceptance.state === 'approved-by-user' && acceptance.gate === `IUM-V2-R${grade}` && sha(acceptance.acceptedCommit), 'Jahrgangsabnahme fehlt');
    git('cat-file','-e',`${acceptance.acceptedCommit}^{commit}`);
    const historical = JSON.parse(git('show',`${acceptance.acceptedCommit}:${base}roadmap.json`));
    check(JSON.stringify(historical) === JSON.stringify(plan), 'Jahrgangsplan seit Abnahme verändert');
    return { grade, modules: plan.modules.map(m=>({id:m.id,title:m.title,minutes:m.minutes,kind:m.kind})), coreMinutes: plan.timeAssumptions.coreMinutes, state:'approved-by-user', acceptedCommit:acceptance.acceptedCommit, date:acceptance.date, maturity:status.maturity, paths:plan.paths ?? plan.variants, capacityChecks:plan.capacityChecks ?? [], evidenceId:'data'+grade };
  });
  const progression = readJSON('roadmap/v2/grades/grade-7/progression.json');
  const openEvidence = { inherited:progression.privacyCarry, new:progression.newOpenReflectionIds };
  check(new Set([...openEvidence.inherited,...openEvidence.new]).size === 9, 'Offene Nachweisfragen inkonsistent');
  const archive = readJSON('roadmap/v2/archive/v1-baseline.json');
  check(sha(archive.mainCommit), 'V1-Archivcommit fehlt');
  const inventory = readJSON('roadmap/v2/audits/artifact-inventory.json');
  const auditCounts = {'retain':0,'adapt':0,'replace':0,'reference-only':0};
  for (const record of inventory.records) { check(Object.hasOwn(auditCounts,record.decision),'Unbekannte Auditentscheidung'); auditCounts[record.decision]++; }
  const followUps = readJSON('roadmap/v2/audits/follow-up-tasks.json').tasks.filter(t=>t.id.startsWith('IUM-V2-FU-'));
  check(followUps.length === 3 && followUps.every(t=>t.state==='blocked-follow-up'), 'Audit-Folgeaufträge benötigen neuen Dashboardvertrag');
  return { ...d, baseline, evidence, gates, grades, openEvidence, auditCounts, followUps:followUps.map(t=>({id:t.id,title:t.title,state:'blocked'})), warnings, git: { head, branch:git('branch','--show-current'), dirty:Boolean(git('status','--porcelain')), main:archive.mainCommit, remote:git('rev-parse','origin/feat/ium-v2-rebaseline') }, technicalFreshness:freshness(d.technicalEvidence,head), generatedAt:new Date().toISOString(), registerDigest:createHash('sha256').update(readFileSync(register)).digest('hex') };
}

export function markdown(snapshot) {
  const s = project(snapshot,'internal');
  const refs = ids => ids.map(id=>{const e=s.evidence.find(e=>e.id===id); return e.kind==='vault' ? `[[${e.target.replace(/^.*\//,'').replace(/\.md$/,'')}|${e.label}]]` : `[${e.label}](../../../Repos/ium-lernwerk/${e.target})`;}).join(' · ');
  const rows = s.streams.map(x=>`| ${x.title} | ${Object.keys(axes).map(k=>labels[x.maturity[k]]).join(' | ')} |`).join('\n');
  return `---\ntype: dashboard\nstatus: active\nproject: IuM-Lernwerk\nupdated: ${s.asOf}\ngenerated: true\nrepo: H4R7W16/ium-lernwerk\n---\n\n# IuM-Lernwerk Dashboard\n\n> Generiert aus [[IuM-Lernwerk Statusregister]]. Keine Gesamtbewertung.\n\n**Stichtag ${s.asOf} · Checkout \`${s.git.head}\` · ${s.git.dirty?'Arbeitskopie verändert':'Arbeitskopie sauber'}**\n\n${s.summary}\n\n## Aktueller Fokus\n\n${s.currentFocus.title} — ${labels[s.currentFocus.workStatus]}. ${s.currentFocus.summary}\n\n## Baselines\n\n- V1: aktive Baseline und archivierte Referenz bei \`${s.git.main}\`. ${refs(['archive'])}\n- V2: building; CUT nicht freigegeben.\n- LXP05: eingefrorener, ungemergter Kandidat. Inhaltsproduktion geschlossen.\n\n## Getrennte Reifeachsen\n\n| Strang | ${Object.values(axes).join(' | ')} |\n| ${Array(9).fill('---').join(' | ')} |\n${rows}\n\nTechnische Prüfung: ${labels[s.technicalFreshness]}, Nachweis bei \`${s.technicalEvidence.commit}\` (${s.technicalEvidence.date}). ${s.technicalEvidence.scope} Kein automatischer Reifewechsel durch Checkout oder Tests.\n\n## Grundlagen und Experience\n\n${s.streams.map(x=>`- **${x.title}:** ${x.summary} ${refs(x.evidenceIds)}`).join('\n')}\n\n${s.experienceAxes.map(x=>`- ${x.label}: ${labels[x.state]}. ${refs(x.evidenceIds)}`).join('\n')}\n\n## Jahrgänge und Kapazität\n\n${s.grades.map(g=>`- **Klasse ${g.grade}:** Planung freigegeben am ${g.date}, \`${g.acceptedCommit}\`; ${g.coreMinutes} Minuten Kernmodule. ${refs([g.evidenceId])}`).join('\n')}\n\n| R7-Pfad | Bedarf | Zeitbedingt offene Orientierung | Offene Reflexion |\n|---|---|---|---|\n${s.grades[2].paths.map(p=>`| ${p.id} | ${p.requiredUnits} UE | ${p.openCapacityRecordIds?.length ?? 'siehe Beleg'} | ${p.openReflectionRecordIds?.length ?? 3} |`).join('\n')}\n\n${s.uncertainties.map(u=>`### ${u.title}\n\n${u.summary} ${refs(u.evidenceIds)}`).join('\n\n')}\n\nSechs übernommene Fragen: ${s.openEvidence.inherited.map(x=>'\`'+x+'\`').join(', ')}.\n\nDrei neue Reflexionsfragen: ${s.openEvidence.new.map(x=>'\`'+x+'\`').join(', ')}.\n\n## Alle 18 V2-Gates\n\n| Nr. | Gate | Status | Stichtag |\n|---|---|---|---|\n${s.gates.map(g=>`| ${g.sequence} | [[${g.source.replace(/^.*\//,'').replace(/\.md$/,'')}|${g.id}]] | ${labels[g.state]} | ${g.date} |`).join('\n')}\n\n## Nächste Entscheidung\n\n**${s.nextDecision.title}.** ${s.nextDecision.summary}\n\n## Evidenz und Aktualität\n\n${s.evidence.map(e=>`- ${refs([e.id])} · ${e.visibility} · ${e.commit ? '\`'+e.commit+'\`' : 'Arbeitskopie / Vault'} · SHA-256 \`${e.digest}\`${e.githubUrl?' · [Verifizierter origin-Stand]('+e.githubUrl+')':''}`).join('\n')}\n\n${s.warnings.map(w=>'> Quellenlücke: '+w.message).join('\n')}\n\nErzeugt: ${s.generatedAt}. Register-Digest: \`${s.registerDigest}\`. Änderungen erfordern \`npm run dashboard:update\`; Vorschau aktualisiert den Snapshot automatisch.\n`;
}
