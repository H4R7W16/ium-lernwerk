import {
  allReady,
  collectReadiness,
  type ReloadReadiness,
} from './reload-readiness.js';

export const UPDATE_PROTOCOL = 1;
const COORDINATOR_TIMEOUT_MS = 6_000;

export type ReloadRequestDetail = Readonly<{
  add(task: Promise<ReloadReadiness>): void;
}>;

export type PreparedClients = Readonly<{
  clientIds: readonly string[];
  values: readonly ReloadReadiness[];
}>;

export type UpdateBridge = Readonly<{
  prepare(requestId: string): Promise<PreparedClients>;
  commit(requestId: string, clientIds: readonly string[]): Promise<boolean>;
  release(requestId: string): Promise<void>;
  activate(requestId: string): Promise<void>;
}>;

export type UpdateOutcome = Readonly<{
  activated: boolean;
  reason: 'activated' | ReloadReadiness['reason'] | 'activation-failed';
}>;

function errorReason(values: readonly ReloadReadiness[]): ReloadReadiness['reason'] {
  return values.find((value) => !value.safe)?.reason ?? 'unknown-client';
}

export async function coordinateUpdate(
  bridge: UpdateBridge,
  requestId: string,
): Promise<UpdateOutcome> {
  let prepared: PreparedClients;
  try {
    prepared = await bridge.prepare(requestId);
  } catch {
    await bridge.release(requestId).catch(() => undefined);
    return { activated: false, reason: 'unknown-client' };
  }
  if (!allReady(prepared.values)) {
    await bridge.release(requestId).catch(() => undefined);
    return { activated: false, reason: errorReason(prepared.values) };
  }
  let committed = false;
  try {
    committed = await bridge.commit(requestId, prepared.clientIds);
  } catch {
    committed = false;
  }
  if (!committed) {
    await bridge.release(requestId).catch(() => undefined);
    return { activated: false, reason: 'unknown-client' };
  }
  try {
    await bridge.activate(requestId);
    return { activated: true, reason: 'activated' };
  } catch {
    await bridge.release(requestId).catch(() => undefined);
    return { activated: false, reason: 'activation-failed' };
  }
}

function randomRequestId(): string {
  if (typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  return `${Date.now()}-${crypto.getRandomValues(new Uint32Array(2)).join('-')}`;
}

function workerRequest<T>(
  serviceWorkers: ServiceWorkerContainer,
  message: Readonly<Record<string, unknown>>,
): Promise<T> {
  const controller = serviceWorkers.controller;
  if (!controller) return Promise.reject(new Error('No controlling service worker'));
  const channel = new MessageChannel();
  return new Promise<T>((resolve, reject) => {
    const timeout = setTimeout(() => {
      channel.port1.close();
      reject(new Error('Update coordination timed out'));
    }, COORDINATOR_TIMEOUT_MS);
    channel.port1.onmessage = (event: MessageEvent<T>) => {
      clearTimeout(timeout);
      channel.port1.close();
      resolve(event.data);
    };
    controller.postMessage(message, [channel.port2]);
  });
}

export function createBrowserUpdateBridge(
  serviceWorkers: ServiceWorkerContainer,
  browserWindow: Window,
): UpdateBridge {
  return {
    async prepare(requestId) {
      const response = await workerRequest<{
        type: string;
        protocol: number;
        requestId: string;
        clientIds: string[];
        values: ReloadReadiness[];
      }>(serviceWorkers, { type: 'IUM_UPDATE_PREPARE', protocol: UPDATE_PROTOCOL, requestId });
      if (
        response.type !== 'IUM_UPDATE_PREPARED'
        || response.protocol !== UPDATE_PROTOCOL
        || response.requestId !== requestId
      ) throw new Error('Invalid update preparation response');
      return { clientIds: response.clientIds, values: response.values };
    },
    async commit(requestId, clientIds) {
      const response = await workerRequest<{
        type: string;
        protocol: number;
        requestId: string;
        committed: boolean;
      }>(serviceWorkers, {
        type: 'IUM_UPDATE_COMMIT',
        protocol: UPDATE_PROTOCOL,
        requestId,
        clientIds: [...clientIds],
      });
      return response.type === 'IUM_UPDATE_COMMITTED'
        && response.protocol === UPDATE_PROTOCOL
        && response.requestId === requestId
        && response.committed;
    },
    async release(requestId) {
      serviceWorkers.controller?.postMessage({
        type: 'IUM_UPDATE_RELEASE',
        protocol: UPDATE_PROTOCOL,
        requestId,
      });
    },
    async activate(requestId) {
      const registration = await serviceWorkers.getRegistration();
      const waiting = registration?.waiting;
      if (!waiting) throw new Error('No verified update candidate is waiting');
      const changed = new Promise<void>((resolve, reject) => {
        const timeout = setTimeout(
          () => reject(new Error('Update activation timed out')),
          COORDINATOR_TIMEOUT_MS,
        );
        serviceWorkers.addEventListener('controllerchange', () => {
          clearTimeout(timeout);
          resolve();
        }, { once: true });
      });
      waiting.postMessage({ type: 'IUM_UPDATE_ACTIVATE', protocol: UPDATE_PROTOCOL, requestId });
      await changed;
      browserWindow.location.reload();
    },
  };
}

export async function prepareDocumentForReload(target: Document): Promise<PreparedClients['values']> {
  const tasks: Promise<ReloadReadiness>[] = [];
  const detail: ReloadRequestDetail = { add: (task) => tasks.push(task) };
  target.dispatchEvent(new CustomEvent<ReloadRequestDetail>('ium:reload-request', { detail }));
  if (tasks.length === 0) {
    return target.querySelector('[data-reload-client="true"]')
      ? [{ safe: false, reason: 'unknown-client' }]
      : [{ safe: true, reason: 'no-work', revision: 0 }];
  }
  return (await collectReadiness(tasks)).values;
}

export function installReloadClientBridge(
  target: Document,
  serviceWorkers: ServiceWorkerContainer,
): () => void {
  const onMessage = (event: MessageEvent<unknown>) => {
    const message = event.data as { type?: string; protocol?: number; requestId?: string };
    if (message.protocol !== UPDATE_PROTOCOL || typeof message.requestId !== 'string') return;
    if (message.type === 'IUM_RELOAD_RELEASE') {
      target.dispatchEvent(new CustomEvent('ium:reload-release', {
        detail: { requestId: message.requestId },
      }));
      return;
    }
    if (message.type !== 'IUM_RELOAD_PREPARE') return;
    const port = event.ports[0];
    if (!port) return;
    void prepareDocumentForReload(target).then((values) => {
      port.postMessage({
        type: 'IUM_RELOAD_RESULT',
        protocol: UPDATE_PROTOCOL,
        requestId: message.requestId,
        values,
      });
    }).catch(() => {
      port.postMessage({
        type: 'IUM_RELOAD_RESULT',
        protocol: UPDATE_PROTOCOL,
        requestId: message.requestId,
        values: [{ safe: false, reason: 'unknown-client' }],
      });
    });
  };
  serviceWorkers.addEventListener('message', onMessage);
  return () => serviceWorkers.removeEventListener('message', onMessage);
}

export async function coordinateBrowserUpdate(
  serviceWorkers: ServiceWorkerContainer,
  browserWindow: Window,
): Promise<UpdateOutcome> {
  return coordinateUpdate(
    createBrowserUpdateBridge(serviceWorkers, browserWindow),
    randomRequestId(),
  );
}
