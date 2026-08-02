export type PlatformErrorCode =
  | 'STORAGE_UNAVAILABLE'
  | 'STORAGE_QUOTA'
  | 'STORAGE_WRITE_FAILED'
  | 'IMPORT_TOO_LARGE'
  | 'IMPORT_INVALID'
  | 'IMPORT_WRONG_MODULE'
  | 'IMPORT_UNSUPPORTED_VERSION'
  | 'MIGRATION_FAILED'
  | 'OFFLINE_NOT_READY'
  | 'UPDATE_INSTALL_FAILED';

export type PlatformError = Readonly<{
  code: PlatformErrorCode;
  message: string;
  action: string;
  technicalDetails?: string;
}>;
