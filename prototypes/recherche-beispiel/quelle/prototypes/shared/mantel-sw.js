'use strict';
const VERSION='__VERSION__',FILES=__FILES__,CACHE='ium-klasse5-mantel-'+VERSION;
self.addEventListener('install',event=>event.waitUntil((async()=>{
try{const cache=await caches.open(CACHE);await cache.addAll(FILES.map(n=>'./'+n));}
catch(error){await caches.delete(CACHE);throw error;}
})()));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{
if(event.request.method!=='GET')return;
const url=new URL(event.request.url),scope=new URL('./',self.location.href);
if(url.origin!==scope.origin||!url.pathname.startsWith(scope.pathname))return;
let relative=decodeURIComponent(url.pathname.slice(scope.pathname.length));if(!relative||relative.endsWith('/'))relative+='index.html';
if(!FILES.includes(relative))return;
event.respondWith((async()=>{const cached=await (await caches.open(CACHE)).match('./'+relative);return cached||fetch(event.request);})());
});
self.addEventListener('message',event=>{
if(event.data?.type==='activate')self.skipWaiting();
if(event.data?.type==='verify')event.waitUntil((async()=>{
const cache=await caches.open(CACHE),found=await Promise.all(FILES.map(n=>cache.match('./'+n)));
event.ports[0]?.postMessage({ok:found.every(Boolean),count:found.filter(Boolean).length,version:VERSION});
})());
});
