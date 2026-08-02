import {
  validateLearningState,
  type LearningStateEnvelope,
  type PlatformError,
} from '@ium/module-contract';

export const MAX_IMPORT_BYTES = 5 * 1024 * 1024;

export type ImportPreview = Readonly<{
  moduleId: string;
  moduleVersion: string;
  savedAt: string;
  payloadFields: readonly string[];
}>;

export type ImportParseResult =
  | Readonly<{
      ok: true;
      state: LearningStateEnvelope;
      preview: ImportPreview;
    }>
  | Readonly<{ ok: false; error: PlatformError }>;

function importError(
  code: Extract<
    PlatformError['code'],
    | 'IMPORT_TOO_LARGE'
    | 'IMPORT_INVALID'
    | 'IMPORT_WRONG_MODULE'
    | 'IMPORT_UNSUPPORTED_VERSION'
  >,
  technicalDetails?: string,
): PlatformError {
  const messages = {
    IMPORT_TOO_LARGE: [
      'Die Importdatei ist größer als 5 MiB.',
      'Wähle eine gültige kleinere Lernwerkdatei.',
    ],
    IMPORT_INVALID: [
      'Die Datei ist kein gültiger IuM-Lernstand.',
      'Prüfe die Datei und wähle sie erneut aus.',
    ],
    IMPORT_WRONG_MODULE: [
      'Die Datei gehört zu einem anderen Lernmodul.',
      'Öffne das passende Modul oder wähle eine andere Datei.',
    ],
    IMPORT_UNSUPPORTED_VERSION: [
      'Die Datei verwendet eine noch nicht unterstützte Version.',
      'Öffne sie mit einer neueren Lernwerkversion.',
    ],
  } as const;
  const [message, action] = messages[code];
  return {
    code,
    message,
    action,
    ...(technicalDetails === undefined ? {} : { technicalDetails }),
  };
}

export function parseImport(
  bytes: Uint8Array,
  expectedModuleId: string,
): ImportParseResult {
  if (bytes.byteLength > MAX_IMPORT_BYTES) {
    return { ok: false, error: importError('IMPORT_TOO_LARGE') };
  }

  let value: unknown;
  try {
    const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    value = JSON.parse(text) as unknown;
  } catch (error) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', String(error)),
    };
  }

  if (
    value !== null
    && typeof value === 'object'
    && typeof (value as { formatVersion?: unknown }).formatVersion === 'number'
    && (value as { formatVersion: number }).formatVersion > 1
  ) {
    return {
      ok: false,
      error: importError('IMPORT_UNSUPPORTED_VERSION'),
    };
  }

  const validation = validateLearningState(value);
  if (!validation.ok) {
    return {
      ok: false,
      error: importError('IMPORT_INVALID', JSON.stringify(validation.issues)),
    };
  }
  if (validation.value.moduleId !== expectedModuleId) {
    return { ok: false, error: importError('IMPORT_WRONG_MODULE') };
  }
  const state = structuredClone(validation.value);
  return {
    ok: true,
    state,
    preview: {
      moduleId: state.moduleId,
      moduleVersion: state.moduleVersion,
      savedAt: state.savedAt,
      payloadFields: Object.keys(state.payload).sort(),
    },
  };
}
