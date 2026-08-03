/// <reference lib="webworker" />

import { matchPrecache, precacheAndRoute } from 'workbox-precaching';
import { registerRoute, setCatchHandler } from 'workbox-routing';

declare const self: ServiceWorkerGlobalScope & {
  __WB_MANIFEST: Array<{ url: string; revision?: string }>;
};

const offlineUrl = new URL('offline/index.html', self.registration.scope).pathname;

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

self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    void self.skipWaiting();
  }
});
