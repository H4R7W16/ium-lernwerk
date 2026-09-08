import { readFile, stat } from 'node:fs/promises';
import { isAbsolute, relative, resolve } from 'node:path';

type UnknownRecord = Record<string, unknown>;

const expectedSegments = [
  ['T1-01', 1, 10, 'orientationAndExplanation'],
  ['T1-02', 1, 10, 'orientationAndExplanation'],
  ['T1-03', 1, 15, 'guidedPractice'],
  ['T1-04', 1, 5, 'independentApplication'],
  ['T1-05', 1, 5, 'guidedPractice'],
  ['T2-06', 2, 5, 'orientationAndExplanation'],
  ['T2-07', 2, 10, 'orientationAndExplanation'],
  ['T2-08', 2, 20, 'guidedPractice'],
  ['T2-09', 2, 5, 'feedbackAndRevision'],
  ['T2-10', 2, 5, 'consolidationAndTransfer'],
  ['T3-11', 3, 5, 'consolidationAndTransfer'],
  ['T3-12', 3, 10, 'guidedPractice'],
  ['T3-13', 3, 20, 'independentApplication'],
  ['T3-14', 3, 10, 'feedbackAndRevision'],
  ['T4-15', 4, 5, 'guidedPractice'],
  ['T4-16', 4, 25, 'independentApplication'],
  ['T4-17', 4, 10, 'feedbackAndRevision'],
  ['T4-18', 4, 5, 'consolidationAndTransfer'],
  ['T5-19', 5, 10, 'independentApplication'],
  ['T5-20', 5, 15, 'feedbackAndRevision'],
  ['T5-21', 5, 15, 'consolidationAndTransfer'],
  ['T5-22', 5, 5, 'consolidationAndTransfer'],
] as const;

const expectedComponents: Readonly<Record<string, number>> = {
  orientationAndExplanation: 35,
  guidedPractice: 55,
  independentApplication: 60,
  feedbackAndRevision: 40,
  consolidationAndTransfer: 35,
};
const expectedMaterials = Array.from({ length: 10 }, (_, index) =>
  `MAT-${String(index + 1).padStart(2, '0')}`);
const expectedHelps = ['H1', 'H2', 'H3', 'H4'];
const expectedProducts = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6'];
const expectedLxfGates = [
  'evidence-integrity',
  'goal-action-evidence-alignment',
  'cognitive-economy',
  'disciplinary-learning-action',
  'representation-coherence',
  'support-without-task-removal',
  'feedback-and-next-action',
  'orientation-and-recovery',
  'accessibility-and-equivalence',
  'teacher-orchestration',
  'privacy-and-emotional-safety',
  'pilot-boundary',
] as const;
const expectedMaterialBindings: Readonly<Record<string, Readonly<{
  path: string;
  audience: 'learner' | 'teacher';
  productIds: readonly string[];
}>>> = {
  'MAT-01': { path: 'materials/start.md', audience: 'learner', productIds: ['P0'] },
  'MAT-02': { path: 'materials/legend.md', audience: 'learner', productIds: ['P0', 'P1', 'P2', 'P3'] },
  'MAT-03': { path: 'materials/worked-example.md', audience: 'learner', productIds: ['P1'] },
  'MAT-04': { path: 'materials/revision.md', audience: 'learner', productIds: ['P2'] },
  'MAT-05': { path: 'materials/own-program.md', audience: 'learner', productIds: ['P3'] },
  'MAT-06': { path: 'materials/helps.md', audience: 'learner', productIds: ['P1', 'P2', 'P3'] },
  'MAT-07': { path: 'materials/return-and-retrieval.md', audience: 'learner', productIds: ['P4'] },
  'MAT-08': { path: 'materials/transfer-and-systems.md', audience: 'learner', productIds: ['P5', 'P6'] },
  'MAT-09': { path: 'teacher/handbook.md', audience: 'teacher', productIds: expectedProducts },
  'MAT-10': { path: 'print/learner.html', audience: 'learner', productIds: expectedProducts },
};
const requiredFiles = [
  'content.json', 'cases.json', 'rights.json',
  'materials/start.md', 'materials/legend.md', 'materials/worked-example.md',
  'materials/revision.md', 'materials/own-program.md', 'materials/helps.md',
  'materials/return-and-retrieval.md', 'materials/transfer-and-systems.md',
  'teacher/handbook.md', 'teacher/briefing.md', 'print/learner.html',
];

function record(value: unknown): value is UnknownRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function exactKeys(value: UnknownRecord, keys: readonly string[]): boolean {
  const actual = Object.keys(value).sort();
  return actual.length === keys.length
    && actual.every((key, index) => key === [...keys].sort()[index]);
}

function exactIds(actual: unknown[], expected: readonly string[]): boolean {
  return actual.length === expected.length
    && [...actual].sort().every((value, index) => value === [...expected].sort()[index]);
}

async function exists(path: string): Promise<boolean> {
  try {
    return (await stat(path)).isFile();
  } catch {
    return false;
  }
}

function localPath(moduleRoot: string, candidate: unknown): string | null {
  if (typeof candidate !== 'string' || candidate.length === 0 || isAbsolute(candidate)) return null;
  const target = resolve(moduleRoot, candidate);
  const rel = relative(moduleRoot, target);
  return rel === '' || rel.startsWith('..') || isAbsolute(rel) ? null : target;
}

export async function checkMaterialPacket(
  rootDir: string,
): Promise<{ issues: readonly string[] }> {
  const issues: string[] = [];
  const moduleRoot = resolve(rootDir, 'modules-v2', 'V2-G5-M06');
  for (const path of requiredFiles) {
    if (!(await exists(resolve(moduleRoot, path)))) issues.push(`Fehlende Materialdatei: ${path}`);
  }

  let content: unknown;
  let cases: unknown;
  try {
    content = JSON.parse(await readFile(resolve(moduleRoot, 'content.json'), 'utf8'));
  } catch {
    issues.push('content.json fehlt oder ist kein gültiges JSON');
    return { issues };
  }
  try {
    cases = JSON.parse(await readFile(resolve(moduleRoot, 'cases.json'), 'utf8'));
  } catch {
    issues.push('cases.json fehlt oder ist kein gültiges JSON');
  }

  if (!record(content)
    || !exactKeys(content, ['schemaVersion', 'moduleId', 'materialRevision', 'segments', 'materials', 'helps'])) {
    issues.push('content.json muss exakt die freigegebenen Hauptfelder enthalten');
    return { issues };
  }
  if (content.schemaVersion !== 1 || content.moduleId !== 'V2-G5-M06'
    || content.materialRevision !== '0.1.0') {
    issues.push('Modul-, Schema- oder Materialrevision ist falsch');
  }

  if (!Array.isArray(content.materials)) {
    issues.push('materials muss eine Liste sein');
  } else {
    const ids = content.materials.map((entry) => record(entry) ? entry.id : null);
    if (!exactIds(ids, expectedMaterials)) issues.push('Material-IDs müssen exakt MAT-01 bis MAT-10 sein; MAT-08 ist verpflichtend');
    const products = new Set<string>();
    for (const [index, entry] of content.materials.entries()) {
      if (!record(entry)
        || !exactKeys(entry, ['id', 'path', 'productIds', 'audience'])) {
        issues.push(`materials[${index}] hat offene oder fehlende Felder`);
        continue;
      }
      if (entry.audience !== 'learner' && entry.audience !== 'teacher') {
        issues.push(`materials[${index}].audience ist ungültig`);
      }
      if (!Array.isArray(entry.productIds)
        || entry.productIds.some((id) => typeof id !== 'string' || !expectedProducts.includes(id))) {
        issues.push(`materials[${index}].productIds ist ungültig`);
      } else entry.productIds.forEach((id) => products.add(id as string));
      const binding = typeof entry.id === 'string' ? expectedMaterialBindings[entry.id] : undefined;
      if (binding !== undefined && (
        entry.path !== binding.path
        || entry.audience !== binding.audience
        || !Array.isArray(entry.productIds)
        || !exactIds(entry.productIds, binding.productIds)
      )) {
        issues.push(`${entry.id} weicht von seiner Pfad-, Zielgruppen- oder Produktbindung ab`);
      }
      const target = localPath(moduleRoot, entry.path);
      if (target === null || !(await exists(target))) {
        issues.push(`Materialpfad für ${String(entry.id)} fehlt oder verlässt den Modulordner`);
      }
    }
    if (!exactIds([...products], expectedProducts)) issues.push('Produktbindungen müssen P0 bis P6 vollständig abdecken');
  }

  if (!Array.isArray(content.helps)) {
    issues.push('helps muss eine Liste sein');
  } else {
    const ids = content.helps.map((entry) => record(entry) ? entry.id : null);
    if (!exactIds(ids, expectedHelps)) issues.push('Hilfen müssen exakt H1 bis H4 sein');
    for (const [index, entry] of content.helps.entries()) {
      if (!record(entry) || !exactKeys(entry, ['id', 'trigger', 'learnerText', 'ownFollowUp', 'fade'])) {
        issues.push(`helps[${index}] hat offene oder fehlende Felder`);
        continue;
      }
      for (const field of ['trigger', 'learnerText', 'ownFollowUp', 'fade']) {
        if (typeof entry[field] !== 'string' || entry[field].trim() === '') {
          issues.push(`helps[${index}].${field} muss ein sichtbarer Text sein`);
        }
      }
    }
  }

  if (!Array.isArray(content.segments)) {
    issues.push('segments muss eine Liste sein');
  } else {
    const byId = new Map(content.segments
      .filter(record)
      .map((entry) => [entry.id, entry]));
    if (!exactIds([...byId.keys()], expectedSegments.map(([id]) => id))) {
      issues.push('Zeitsegmente müssen exakt T1-01 bis T5-22 entsprechen');
    }
    for (const [id, meeting, minutes, component] of expectedSegments) {
      const entry = byId.get(id);
      if (!record(entry)) continue;
      if (!exactKeys(entry, ['id', 'meeting', 'minutes', 'component', 'learningFunctionIds', 'action', 'productIds'])) {
        issues.push(`${id} hat offene oder fehlende Felder`);
      }
      if (entry.meeting !== meeting || entry.minutes !== minutes || entry.component !== component) {
        issues.push(`${id} weicht von Termin, Minuten oder Hauptfunktion ab`);
      }
      if (!Array.isArray(entry.learningFunctionIds) || entry.learningFunctionIds.length === 0
        || !Array.isArray(entry.productIds) || typeof entry.action !== 'string' || entry.action.trim() === '') {
        issues.push(`${id} braucht Lernfunktion, Handlung und Produktbindung`);
      }
    }
    const total = content.segments.reduce((sum, entry) =>
      sum + (record(entry) && typeof entry.minutes === 'number' ? entry.minutes : 0), 0);
    if (total !== 225) issues.push(`Zeitbudget muss exakt 225 Minuten betragen, nicht ${total}`);
    for (let meeting = 1; meeting <= 5; meeting += 1) {
      const minutes = content.segments.reduce((sum, entry) =>
        sum + (record(entry) && entry.meeting === meeting && typeof entry.minutes === 'number'
          ? entry.minutes : 0), 0);
      if (minutes !== 45) issues.push(`Termin ${meeting} muss exakt 45 Minuten umfassen`);
    }
    for (const [component, expected] of Object.entries(expectedComponents)) {
      const actual = content.segments.reduce((sum, entry) =>
        sum + (record(entry) && entry.component === component && typeof entry.minutes === 'number'
          ? entry.minutes : 0), 0);
      if (actual !== expected) issues.push(`${component} muss ${expected} Minuten umfassen`);
    }
  }

  if (record(cases) && exactKeys(cases, ['schemaVersion', 'moduleId', 'gridCases', 'manualCases'])) {
    const gridIds = Array.isArray(cases.gridCases)
      ? cases.gridCases.map((entry) => record(entry) ? entry.id : null) : [];
    const manualIds = Array.isArray(cases.manualCases)
      ? cases.manualCases.map((entry) => record(entry) ? entry.id : null) : [];
    if (!exactIds(gridIds, ['S0', 'S1', 'S2', 'S3'])) issues.push('cases.json braucht exakt S0 bis S3 als Rasterfälle');
    if (!exactIds(manualIds, ['S4', 'S5'])) issues.push('cases.json braucht S4 und S5 als getrennte manuelle Fälle');
  } else issues.push('cases.json muss geschlossene Raster- und manuelle Fälle enthalten');

  try {
    const handbook = await readFile(resolve(moduleRoot, 'teacher', 'handbook.md'), 'utf8');
    for (const gate of expectedLxfGates) {
      if (!handbook.includes(`| ${gate} |`)) issues.push(`Autorenreview für LXF-Gate ${gate} fehlt`);
    }
  } catch {
    issues.push('Handbuch fehlt für den LXF-Autorenreview');
  }

  return { issues };
}

async function main(): Promise<void> {
  const result = await checkMaterialPacket(process.cwd());
  if (result.issues.length > 0) {
    result.issues.forEach((issue) => console.error(issue));
    process.exitCode = 1;
    return;
  }
  console.log('V2-M06-Materialvertrag gültig: 10 Materialien, 4 Hilfen, 22 Segmente, 225 Minuten.');
}

if (process.argv[1]?.endsWith('check-v2-m06-materials.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
