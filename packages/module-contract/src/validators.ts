import Ajv2020, { type ErrorObject, type ValidateFunction } from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import learningStateSchema from '../../../schemas/learning-state-envelope.schema.json';
import moduleManifestSchema from '../../../schemas/module-manifest.schema.json';
import type { LearningStateEnvelope } from './generated/learning-state-envelope.js';
import type { ModuleManifest } from './generated/module-manifest.js';

export type ValidationIssue = Readonly<{
  path: string;
  keyword: string;
  message: string;
}>;

export type ValidationResult<T> =
  | Readonly<{ ok: true; value: T }>
  | Readonly<{ ok: false; issues: readonly ValidationIssue[] }>;

const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);

const moduleValidator = ajv.compile<ModuleManifest>(moduleManifestSchema);
const stateValidator = ajv.compile<LearningStateEnvelope>(learningStateSchema);

function toIssues(errors: ErrorObject[] | null | undefined): ValidationIssue[] {
  return (errors ?? []).map((error) => ({
    path: error.instancePath || '/',
    keyword: error.keyword,
    message: error.message ?? 'Ungültiger Wert',
  }));
}

function validate<T>(
  validator: ValidateFunction<T>,
  value: unknown,
): ValidationResult<T> {
  if (!validator(value)) {
    return { ok: false, issues: toIssues(validator.errors) };
  }
  return { ok: true, value };
}

export function validateModuleManifest(
  value: unknown,
): ValidationResult<ModuleManifest> {
  const structural = validate(moduleValidator, value);
  if (!structural.ok) {
    return structural;
  }
  if (structural.value.time.minLessons > structural.value.time.maxLessons) {
    return {
      ok: false,
      issues: [
        {
          path: '/time/maxLessons',
          keyword: 'semantic',
          message: 'muss mindestens minLessons entsprechen',
        },
      ],
    };
  }
  return structural;
}

export function validateLearningState(
  value: unknown,
): ValidationResult<LearningStateEnvelope> {
  return validate(stateValidator, value);
}
