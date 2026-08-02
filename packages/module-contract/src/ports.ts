import type { LearningStateEnvelope } from './generated/learning-state-envelope.js';
import type { PlatformError } from './errors.js';

export type StorageMode =
  | 'persistent'
  | 'volatile-selected'
  | 'volatile-fallback';

export type SaveResult =
  | Readonly<{ ok: true; mode: StorageMode }>
  | Readonly<{ ok: false; error: PlatformError }>;

export type DeleteResult =
  | Readonly<{ ok: true; deleted: boolean }>
  | Readonly<{ ok: false; error: PlatformError }>;

export interface StateRepository {
  readonly mode: StorageMode;
  load(moduleId: string): Promise<LearningStateEnvelope | null>;
  save(state: LearningStateEnvelope): Promise<SaveResult>;
  deleteModule(moduleId: string): Promise<DeleteResult>;
  deleteAll(): Promise<DeleteResult>;
}

export interface ClockPort {
  now(): Date;
}

export interface ExportPort {
  download(
    filename: string,
    bytes: Uint8Array,
    mediaType: 'application/json',
  ): Promise<boolean>;
  copyText(text: string): Promise<boolean>;
}

export interface UpdatePort {
  check(): Promise<void>;
  activate(): Promise<void>;
}

export interface ErrorPort {
  show(error: PlatformError): void;
}
