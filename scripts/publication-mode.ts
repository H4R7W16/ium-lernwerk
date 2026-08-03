import type { BuildProfile } from './build-module-registry.js';

export type PublicationMode =
  | 'development'
  | 'device-fixture'
  | 'gate-b-preview';

export type PublicationContract = Readonly<{
  profile: BuildProfile;
  mode: PublicationMode;
  buildRevision: string;
  previewId: string;
}>;

const MODES = new Set<PublicationMode>([
  'development',
  'device-fixture',
  'gate-b-preview',
]);

const ALLOWED_COMBINATIONS = new Set([
  'production:development',
  'production:gate-b-preview',
  'fixture:device-fixture',
]);

export function parsePublicationMode(value: string): PublicationMode {
  if (!MODES.has(value as PublicationMode)) {
    throw new Error(`Unknown publication mode: ${JSON.stringify(value)}`);
  }
  return value as PublicationMode;
}

export function assertPublicationCombination(
  profile: BuildProfile,
  mode: PublicationMode,
): void {
  if (!ALLOWED_COMBINATIONS.has(`${profile}:${mode}`)) {
    throw new Error(`Unsupported profile/publication combination: ${profile}:${mode}`);
  }
}

export function parseBuildRevision(value: string, mode: PublicationMode): string {
  if (mode === 'gate-b-preview') {
    if (!/^[0-9a-f]{40}$/.test(value)) {
      throw new Error('Gate-B build revision must be a full lowercase Git SHA');
    }
    return value;
  }
  if (value === '') return 'stable';
  if (!/^[A-Za-z0-9._-]{1,64}$/.test(value)) {
    throw new Error('Development or device build revision is invalid');
  }
  return value;
}

export function parsePreviewId(value: string, mode: PublicationMode): string {
  if (mode === 'gate-b-preview') {
    if (!/^ium5-gate-b-[a-z0-9-]{8,48}$/.test(value)) {
      throw new Error('Gate-B Preview-ID is missing or invalid');
    }
    return value;
  }
  if (value !== '') {
    throw new Error(`Preview-ID is forbidden in ${mode} mode`);
  }
  return '';
}

export function createPublicationContract(options: {
  profile: BuildProfile;
  mode: PublicationMode;
  buildRevision?: string;
  previewId?: string;
}): PublicationContract {
  assertPublicationCombination(options.profile, options.mode);
  return {
    profile: options.profile,
    mode: options.mode,
    buildRevision: parseBuildRevision(options.buildRevision ?? '', options.mode),
    previewId: parsePreviewId(options.previewId ?? '', options.mode),
  };
}
