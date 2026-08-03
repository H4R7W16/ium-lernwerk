import type { ExportPort } from '@ium/module-contract';

export function createBrowserExportPort(workspace: HTMLElement): ExportPort {
  return {
    async download(filename, bytes, mediaType) {
      const frame = window.frameElement;
      const blockedBySandbox = frame instanceof HTMLIFrameElement
        && frame.hasAttribute('sandbox')
        && !frame.sandbox.contains('allow-downloads');
      if (window.origin === 'null' || window.self !== window.top || blockedBySandbox) {
        return false;
      }
      const blobBytes = new Uint8Array(bytes.byteLength);
      blobBytes.set(bytes);
      const url = URL.createObjectURL(new Blob([blobBytes.buffer], { type: mediaType }));
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.hidden = true;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 0);
      return true;
    },
    async copyText(value) {
      const fallback = workspace.querySelector<HTMLElement>('[data-copy-fallback]');
      const field = workspace.querySelector<HTMLTextAreaElement>('[data-copy-fallback-text]');
      if (fallback && field) {
        fallback.hidden = false;
        field.value = value;
        field.focus();
        field.select();
      }
      try {
        await navigator.clipboard.writeText(value);
      } catch {
        // The visible read-only field remains available as the manual fallback.
      }
      return fallback !== null && field !== null;
    },
  };
}

export function createWorkspaceId(): string {
  if (typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6]! & 0x0f) | 0x40;
  bytes[8] = (bytes[8]! & 0x3f) | 0x80;
  const hex = [...bytes].map((value) => value.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}
