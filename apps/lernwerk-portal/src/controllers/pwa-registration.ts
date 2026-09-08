import { registerSW } from 'virtual:pwa-register';
import { announceError } from '@ium/ui-components/controllers/status-announcer';
import {
  coordinateBrowserUpdate,
  installReloadClientBridge,
} from './update-coordinator.js';

export type { ReloadRequestDetail } from './update-coordinator.js';

export type PwaState = 'not-ready' | 'ready' | 'offline' | 'degraded';

export type PwaController = Readonly<{
  check(): Promise<void>;
  activatePreparedUpdate(): Promise<boolean>;
  dismiss(): void;
}>;

function setConnectionState(root: ParentNode, state: PwaState, message: string): void {
  for (const target of root.querySelectorAll<HTMLElement>('[data-connection-status]')) {
    target.dataset.pwaState = state;
    target.textContent = message;
  }
}

export function connectPwaRegistration(
  root: ParentNode = document,
  browserWindow: Window = window,
): PwaController {
  let prompt = root.querySelector<HTMLElement>('[data-update-prompt]');
  let confirm = root.querySelector<HTMLButtonElement>('[data-update-confirm]');
  let dismissButton = root.querySelector<HTMLButtonElement>('[data-update-dismiss]');
  let offlineReady = false;
  let discardButton: HTMLButtonElement | null = null;
  let updateStatus: HTMLElement | null = null;

  const showUpdatePrompt = () => {
    prompt = root.querySelector<HTMLElement>('[data-update-prompt]');
    if (prompt) {
      prompt.hidden = false;
      prompt.focus();
    }
  };

  const ensureRecoveryActions = () => {
    prompt = root.querySelector<HTMLElement>('[data-update-prompt]');
    confirm = root.querySelector<HTMLButtonElement>('[data-update-confirm]');
    dismissButton = root.querySelector<HTMLButtonElement>('[data-update-dismiss]');
    if (!prompt || updateStatus) return;
    updateStatus = document.createElement('p');
    updateStatus.dataset.updateStatus = 'true';
    updateStatus.setAttribute('role', 'status');
    updateStatus.textContent = 'Noch keine Arbeitsstände geprüft.';
    prompt.querySelector('.actions')?.before(updateStatus);
    const guidance = document.createElement('p');
    guidance.textContent = 'Du kannst weiterarbeiten, später aktualisieren oder den Export im Arbeitsbereich bewusst anfordern.';
    prompt.querySelector('.actions')?.before(guidance);
    discardButton = document.createElement('button');
    discardButton.type = 'button';
    discardButton.dataset.updateDiscard = 'true';
    discardButton.textContent = 'Diesen ungesicherten Stand verwerfen und aktualisieren';
    discardButton.hidden = true;
    prompt.querySelector('.actions')?.append(discardButton);
  };

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
    installReloadClientBridge(document, browserWindow.navigator.serviceWorker);
    registerSW({
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
        showUpdatePrompt();
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
    void browserWindow.navigator.serviceWorker.getRegistration().then((registration) => {
      if (!registration) return;
      if (registration.waiting) showUpdatePrompt();
      registration.addEventListener('updatefound', () => {
        const candidate = registration.installing;
        candidate?.addEventListener('statechange', () => {
          if (candidate.state === 'installed' && registration.waiting) showUpdatePrompt();
        });
      });
    });
  }

  const controller: PwaController = {
    async check() {
      const registration = await browserWindow.navigator.serviceWorker?.getRegistration();
      await registration?.update();
    },
    async activatePreparedUpdate() {
      if (!('serviceWorker' in browserWindow.navigator)) {
        return false;
      }
      ensureRecoveryActions();
      if (prompt) {
        prompt.dataset.updateAttempt = String(Number(prompt.dataset.updateAttempt ?? '0') + 1);
      }
      if (confirm) confirm.disabled = true;
      if (discardButton) discardButton.disabled = true;
      if (updateStatus) updateStatus.textContent = 'Arbeitsstände in allen offenen Seiten werden geprüft.';
      const outcome = await coordinateBrowserUpdate(
        browserWindow.navigator.serviceWorker,
        browserWindow,
      ).catch(() => ({ activated: false as const, reason: 'activation-failed' as const }));
      if (outcome.activated) return true;
      if (confirm) confirm.disabled = false;
      if (discardButton) discardButton.disabled = false;
      if (discardButton) discardButton.hidden = outcome.reason !== 'volatile';
      if (updateStatus) {
        updateStatus.textContent = outcome.reason === 'volatile'
          ? 'Mindestens ein ungesicherter Sitzungsstand verhindert die Aktualisierung.'
          : outcome.reason === 'unknown-client'
            ? 'Nicht alle offenen Seiten haben geantwortet; die Aktualisierung wurde abgebrochen.'
          : 'Die Aktualisierung wurde abgebrochen; alle vorbereiteten Seiten sind wieder freigegeben.';
      }
      if (outcome.reason === 'volatile') {
        announceError(document, {
          code: 'STORAGE_WRITE_FAILED',
          message: 'Ein flüchtiger Arbeitsstand ist nicht wiederherstellbar.',
          action: 'Arbeite weiter, fordere bewusst einen Export an oder verwirf nur den Stand dieser Seite nach Bestätigung.',
        });
        return false;
      }
      announceError(document, {
        code: outcome.reason === 'conflict' ? 'STORAGE_CONFLICT' : 'UPDATE_INSTALL_FAILED',
        message: outcome.reason === 'unknown-client'
          ? 'Nicht alle offenen Seiten haben die Aktualisierung bestätigt.'
          : 'Die Aktualisierung konnte nicht sicher vorbereitet werden.',
        action: outcome.reason === 'unknown-client'
          ? 'Schließe nicht reagierende alte Seiten geordnet oder versuche es später erneut.'
          : 'Die bisherige Version bleibt aktiv. Prüfe den lokalen Stand und versuche es erneut.',
        technicalDetails: outcome.reason,
      });
      return false;
    },
    dismiss() {
      prompt = root.querySelector<HTMLElement>('[data-update-prompt]');
      if (prompt) {
        prompt.hidden = true;
      }
    },
  };

  const bindPromptControls = () => {
    ensureRecoveryActions();
    if (confirm && confirm.dataset.pwaBound !== 'true') {
      confirm.dataset.pwaBound = 'true';
      confirm.addEventListener('click', () => void controller.activatePreparedUpdate());
    }
    if (discardButton && discardButton.dataset.pwaBound !== 'true') {
      discardButton.dataset.pwaBound = 'true';
      discardButton.addEventListener('click', () => {
        if (!browserWindow.confirm(
          'Diesen ungesicherten Stand dieser Seite wirklich verwerfen? Nicht gespeicherte Änderungen gehen beim Aktualisieren verloren.',
        )) return;
        document.dispatchEvent(new CustomEvent('ium:reload-discard'));
        void controller.activatePreparedUpdate();
      });
    }
    if (dismissButton && dismissButton.dataset.pwaBound !== 'true') {
      dismissButton.dataset.pwaBound = 'true';
      dismissButton.addEventListener('click', () => controller.dismiss());
    }
  };
  document.addEventListener('ium:update-ui-ready', bindPromptControls);
  bindPromptControls();
  return controller;
}
