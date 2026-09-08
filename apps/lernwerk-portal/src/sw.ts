/// <reference lib="webworker" />

import { matchPrecache, precacheAndRoute } from 'workbox-precaching';
import { registerRoute, setCatchHandler } from 'workbox-routing';

declare const self: ServiceWorkerGlobalScope & {
  __WB_MANIFEST: Array<{ url: string; revision?: string }>;
};

const offlineUrl = new URL('offline/index.html', self.registration.scope).pathname;
const UPDATE_PROTOCOL = 1;
const CLIENT_TIMEOUT_MS = 5_000;
const preparations = new Map<string, readonly string[]>();

type ReloadReadiness =
  | Readonly<{
    safe: true;
    reason: 'persisted-readback' | 'no-work' | 'explicit-discard';
    revision: number;
  }>
  | Readonly<{
    safe: false;
    reason: 'volatile' | 'write-failed' | 'conflict' | 'readback-failed' | 'unknown-client';
  }>;

precacheAndRoute(self.__WB_MANIFEST);

registerRoute(
  ({ request }) => request.mode === 'navigate',
  ({ request }) => fetch(request),
  'GET',
);

setCatchHandler(async ({ event }) => {
  if (event instanceof FetchEvent && event.request.mode === 'navigate') {
    return (await matchPrecache(offlineUrl)) ?? Response.error();
  }
  return Response.error();
});

async function controlledWindows(): Promise<readonly WindowClient[]> {
  return self.clients.matchAll({ type: 'window', includeUncontrolled: false });
}

async function releaseClients(requestId: string): Promise<void> {
  const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: false });
  for (const client of windows) {
    client.postMessage({
      type: 'IUM_RELOAD_RELEASE',
      protocol: UPDATE_PROTOCOL,
      requestId,
    });
  }
  preparations.delete(requestId);
}

function askClient(client: WindowClient, requestId: string): Promise<readonly ReloadReadiness[]> {
  const channel = new MessageChannel();
  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      channel.port1.close();
      resolve([{ safe: false, reason: 'unknown-client' }]);
    }, CLIENT_TIMEOUT_MS);
    channel.port1.onmessage = (reply: MessageEvent<unknown>) => {
      clearTimeout(timeout);
      channel.port1.close();
      const message = reply.data as {
        type?: string;
        protocol?: number;
        requestId?: string;
        values?: ReloadReadiness[];
      };
      const validValues = Array.isArray(message.values)
        && message.values.length > 0
        && message.values.every((value) => {
          if (!value || typeof value !== 'object' || typeof value.safe !== 'boolean') return false;
          if (value.safe) {
            return ['persisted-readback', 'no-work', 'explicit-discard'].includes(value.reason)
              && Number.isInteger(value.revision)
              && value.revision >= 0;
          }
          return ['volatile', 'write-failed', 'conflict', 'readback-failed', 'unknown-client']
            .includes(value.reason);
        });
      if (
        message.type !== 'IUM_RELOAD_RESULT'
        || message.protocol !== UPDATE_PROTOCOL
        || message.requestId !== requestId
        || !validValues
      ) {
        resolve([{ safe: false, reason: 'unknown-client' }]);
        return;
      }
      resolve(message.values);
    };
    client.postMessage({
      type: 'IUM_RELOAD_PREPARE',
      protocol: UPDATE_PROTOCOL,
      requestId,
    }, [channel.port2]);
  });
}

self.addEventListener('message', (event: ExtendableMessageEvent) => {
  const message = event.data as {
    type?: string;
    protocol?: number;
    requestId?: string;
    clientIds?: string[];
  };
  if (
    message.type === 'IUM_UPDATE_ACTIVATE'
    && message.protocol === UPDATE_PROTOCOL
    && typeof message.requestId === 'string'
  ) {
    event.waitUntil(self.skipWaiting());
    return;
  }
  if (message.protocol !== UPDATE_PROTOCOL || typeof message.requestId !== 'string') return;
  const responsePort = event.ports[0];
  if (message.type === 'IUM_UPDATE_RELEASE') {
    event.waitUntil(releaseClients(message.requestId));
    return;
  }
  if (message.type === 'IUM_UPDATE_PREPARE' && responsePort) {
    event.waitUntil((async () => {
      const windows = await controlledWindows();
      const clientIds = windows.map((client) => client.id).sort();
      const values = windows.length === 0
        ? [{ safe: false, reason: 'unknown-client' } as const]
        : (await Promise.all(
          windows.map((client) => askClient(client, message.requestId!)),
        )).flat();
      preparations.set(message.requestId!, clientIds);
      responsePort.postMessage({
        type: 'IUM_UPDATE_PREPARED',
        protocol: UPDATE_PROTOCOL,
        requestId: message.requestId,
        clientIds,
        values,
      });
      if (values.some((value) => !value.safe)) {
        await releaseClients(message.requestId!);
      }
    })());
    return;
  }
  if (message.type === 'IUM_UPDATE_COMMIT' && responsePort) {
    event.waitUntil((async () => {
      const windows = await controlledWindows();
      const currentIds = windows.map((client) => client.id).sort();
      const preparedIds = preparations.get(message.requestId!);
      const requestedIds = Array.isArray(message.clientIds) ? [...message.clientIds].sort() : [];
      const committed = preparedIds !== undefined
        && JSON.stringify(preparedIds) === JSON.stringify(requestedIds)
        && JSON.stringify(currentIds) === JSON.stringify(requestedIds);
      responsePort.postMessage({
        type: 'IUM_UPDATE_COMMITTED',
        protocol: UPDATE_PROTOCOL,
        requestId: message.requestId,
        committed,
      });
      if (!committed) await releaseClients(message.requestId!);
    })());
  }
});
