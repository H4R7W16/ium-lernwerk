import { registerSW } from 'virtual:pwa-register';
import { announceError } from '@ium/ui-components/controllers/status-announcer';

export type PwaState = 'not-ready' | 'ready' | 'offline' | 'degraded';

export type FlushRequestDetail = Readonly<{
  add(task: Promise<boolean>): void;
}>;

export type PwaController = Readonly<{
  check(): Promise<void>;
  activateAfterFlush(): Promise<boolean>;
  dismiss(): void;
}>;

function setConnectionState(root: ParentNode, state: PwaState, message: string): void {
  for (const target of root.querySelectorAll<HTMLElement>('[data-connection-status]')) {
    target.dataset.pwaState = state;
    target.textContent = message;
  }
}

async function flushActiveRuntimes(target: Document): Promise<boolean> {
  const pending: Promise<boolean>[] = [];
  const detail: FlushRequestDetail = {
    add(task) {
      pending.push(task);
    },
  };
  target.dispatchEvent(new CustomEvent<FlushRequestDetail>('ium:flush-request', { detail }));
  const results = await Promise.all(pending);
  return results.every(Boolean);
}

export function connectPwaRegistration(
  root: ParentNode = document,
  browserWindow: Window = window,
): PwaController {
  const prompt = root.querySelector<HTMLElement>('[data-update-prompt]');
  const confirm = root.querySelector<HTMLButtonElement>('[data-update-confirm]');
  const dismissButton = root.querySelector<HTMLButtonElement>('[data-update-dismiss]');
  let updateServiceWorker: ((reloadPage?: boolean) => Promise<void>) | undefined;
  let offlineReady = false;

  const showOffline = () => {
    setConnectionState(
      root,
      offlineReady ? 'offline' : 'degraded',
      offlineReady
        ? 'Offline – lokal verfügbare Inhalte werden verwendet'
        : 'Offline – Offlinebereitschaft wurde noch nicht bestätigt',
    );
  };
  browserWindow.addEventListener('offline', showOffline);
  browserWindow.addEventListener('online', () => {
    setConnectionState(
      root,
      offlineReady ? 'ready' : 'not-ready',
      offlineReady
        ? 'Online – Offlinebereitschaft bestätigt'
        : 'Online – Offlinebereitschaft wird geprüft',
    );
  });

  if (!('serviceWorker' in browserWindow.navigator)) {
    setConnectionState(root, 'degraded', 'Offlinebetrieb wird von diesem Browser nicht unterstützt');
  } else {
    updateServiceWorker = registerSW({
      immediate: true,
      onOfflineReady() {
        offlineReady = true;
        setConnectionState(
          root,
          browserWindow.navigator.onLine ? 'ready' : 'offline',
          browserWindow.navigator.onLine
            ? 'Online – Offlinebereitschaft bestätigt'
            : 'Offline – lokal verfügbare Inhalte werden verwendet',
        );
      },
      onNeedRefresh() {
        if (prompt) {
          prompt.hidden = false;
          prompt.focus();
        }
      },
      onRegisterError(error) {
        setConnectionState(root, 'degraded', 'Offlinebereitschaft konnte nicht hergestellt werden');
        announceError(document, {
          code: 'UPDATE_INSTALL_FAILED',
          message: 'Die Offline-Installation ist fehlgeschlagen.',
          action: 'Bleibe online und versuche es später erneut.',
          technicalDetails: error instanceof Error ? error.message : String(error),
        });
      },
    });
  }

  const controller: PwaController = {
    async check() {
      const registration = await browserWindow.navigator.serviceWorker?.getRegistration();
      await registration?.update();
    },
    async activateAfterFlush() {
      if (!updateServiceWorker) {
        return false;
      }
      if (!(await flushActiveRuntimes(document))) {
        announceError(document, {
          code: 'STORAGE_WRITE_FAILED',
          message: 'Der Arbeitsstand konnte vor der Aktualisierung nicht gespeichert werden.',
          action: 'Die bisherige Version bleibt aktiv. Prüfe den lokalen Speicher und versuche es erneut.',
        });
        return false;
      }
      try {
        await updateServiceWorker(true);
        return true;
      } catch (error) {
        announceError(document, {
          code: 'UPDATE_INSTALL_FAILED',
          message: 'Die Aktualisierung konnte nicht aktiviert werden.',
          action: 'Die bisherige Version bleibt aktiv. Versuche es später erneut.',
          technicalDetails: error instanceof Error ? error.message : String(error),
        });
        return false;
      }
    },
    dismiss() {
      if (prompt) {
        prompt.hidden = true;
      }
    },
  };

  confirm?.addEventListener('click', () => void controller.activateAfterFlush());
  dismissButton?.addEventListener('click', () => controller.dismiss());
  return controller;
}
