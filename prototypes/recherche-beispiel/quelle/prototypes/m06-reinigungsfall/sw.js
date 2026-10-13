// Retire the previous technical fixture's worker at this same Pages scope.
// No cache or learner data is deleted, and open pages are not reloaded.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    await self.clients.claim();
    await self.registration.unregister();
  })());
});
