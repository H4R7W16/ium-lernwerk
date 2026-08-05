import { readdir, readFile } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import {
  parseExperienceContent,
  type ContractError,
  type ExperienceContentV1,
} from '@ium/learning-experience';

const EXPERIENCE_PATH = 'lernumgebung/experience.json';
const IUM5_PHASE_IDS = new Set([
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
  'ue6-extension',
]);

export type ExperienceValidationResult =
  | Readonly<{ ok: true; value: ExperienceContentV1 }>
  | Readonly<{ ok: false; errors: readonly ContractError[] }>;

function error(path: string, code: ContractError['code'], message: string): ContractError {
  return { path, code, message };
}

function scanClosedContent(value: unknown, path: string, errors: ContractError[]): void {
  if (typeof value === 'string') {
    if (/<\/?[a-z][^>]*>|<script|javascript:/i.test(value)) {
      errors.push(error(path, 'invalid_value', 'Learner-facing text must not contain HTML or script content.'));
    }
    if (/https?:\/\/|www\./i.test(value)) {
      errors.push(error(path, 'invalid_value', 'Learner-facing text must not contain URLs.'));
    }
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((entry, index) => scanClosedContent(entry, `${path}[${index}]`, errors));
    return;
  }
  if (value !== null && typeof value === 'object') {
    for (const [key, entry] of Object.entries(value as Record<string, unknown>)) {
      if (/^(?:utm_|tracking|analytics|telemetry)/i.test(key)) {
        errors.push(error(`${path}.${key}`, 'unknown_field', `Forbidden tracking property: ${key}`));
      }
      scanClosedContent(entry, `${path}.${key}`, errors);
    }
  }
}

export function validateExperienceValue(
  value: unknown,
  expectedModuleId?: string,
): ExperienceValidationResult {
  const parsed = parseExperienceContent(value);
  const errors: ContractError[] = parsed.ok ? [] : [...parsed.errors];
  scanClosedContent(value, '$', errors);

  if (!parsed.ok) {
    return { ok: false, errors };
  }
  if (expectedModuleId && parsed.value.moduleId !== expectedModuleId) {
    errors.push(error(
      '$.moduleId',
      'invalid_value',
      `Expected moduleId ${expectedModuleId}, received ${parsed.value.moduleId}.`,
    ));
  }
  parsed.value.tasks.forEach((task, taskIndex) => {
    task.materialRefs.forEach((referenceValue, referenceIndex) => {
      if (referenceValue.startsWith('phase:')) {
        const phaseId = referenceValue.slice('phase:'.length);
        if (!IUM5_PHASE_IDS.has(phaseId)) {
          errors.push(error(
            `$.tasks[${taskIndex}].materialRefs[${referenceIndex}]`,
            'invalid_value',
            `Unknown phase reference: ${phaseId}`,
          ));
        }
      }
    });
  });

  return errors.length > 0 ? { ok: false, errors } : { ok: true, value: parsed.value };
}

async function findExperienceFiles(directory: string): Promise<string[]> {
  const found: string[] = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      found.push(...await findExperienceFiles(path));
    } else if (entry.name === 'experience.json') {
      found.push(path);
    }
  }
  return found;
}

function displayPath(moduleDirectory: string, path: string): string {
  return relative(resolve(moduleDirectory), resolve(path)).split(sep).join('/');
}

export async function readExperienceContent(moduleDirectory: string): Promise<ExperienceContentV1> {
  const expectedPath = resolve(moduleDirectory, EXPERIENCE_PATH);
  const files = await findExperienceFiles(resolve(moduleDirectory));
  if (files.length === 0) {
    throw new Error(`${EXPERIENCE_PATH} is missing.`);
  }
  if (files.length !== 1 || resolve(files[0]!) !== expectedPath) {
    throw new Error(
      `Expected exactly one ${EXPERIENCE_PATH}; found ${files.map((path) => displayPath(moduleDirectory, path)).join(', ')}.`,
    );
  }

  let value: unknown;
  try {
    value = JSON.parse(await readFile(expectedPath, 'utf8')) as unknown;
  } catch (cause) {
    throw new Error(`${EXPERIENCE_PATH} contains malformed JSON.`, { cause });
  }

  const result = validateExperienceValue(value);
  if (!result.ok) {
    const details = result.errors.map((issue) => `${issue.path}: ${issue.message}`).join('\n');
    throw new Error(`Invalid experience contract ${EXPERIENCE_PATH}:\n${details}`);
  }
  return result.value;
}
