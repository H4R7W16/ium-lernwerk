'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {prepareClass5Pages}=require('../m06-reinigungsfall/build-class5-pages.cjs');
const {prepareAdditionalPages,prefix}=require('./build.cjs');
const digest=data=>crypto.createHash('sha256').update(data).digest('hex');
const old=prepareClass5Pages(),all=prepareAdditionalPages();
test('alle bisherigen Pages-Dateien einschließlich Wurzeleinstieg bleiben bytegleich',()=>{
 for(const [name,data]of old)assert.equal(digest(all.get(name)),digest(data),name);
 for(const name of all.keys())if(!old.has(name))assert.ok(name.startsWith('beispiele/'),name);
 assert.equal(all.get('index.html'),old.get('index.html'));
});
test('zusätzliches Recherchekapitel hat Einstieg, Vollfilm, Untertitel und beide Alternativen',()=>{
 const base=prefix+'klasse5/recherche/';
 for(const name of ['index.html','schritt-suchplan.html','leas-weg-bildfolge.html','leas-weg-lesetext.html','assets/recherche/rq05-film/leas-rechercheweg-1.0.mp4','assets/recherche/rq05-film/leas-rechercheweg.vtt','assets/recherche/rq05-film/leas-rechercheweg.srt'])assert.ok(all.has(base+name),name);
 assert.equal(digest(all.get(base+'assets/recherche/rq05-film/leas-rechercheweg-1.0.mp4')),'3ec7868b2c726ac24801934b2a037a3b434df532a4560fe0489d201212f5716f');
 assert.match(all.get(prefix+'index.html'),/url=klasse5\/recherche\//);
 assert.match(all.get('beispiele/index.html'),/Recherche-Beispiel/);
 const film=all.get(base+'schritt-suchplan.html');assert.match(film,/<video controls playsinline preload="metadata"/);assert.doesNotMatch(film,/<video[^>]*\bautoplay\b/);
 for(const name of ['leas-weg-bildfolge.html','leas-weg-lesetext.html']){const html=all.get(base+name);assert.ok((html.match(/<details/g)||[]).length>=2);assert.doesNotMatch(html,/<details[^>]*\bopen\b/);}
});
test('zusätzliche Umgebung verwendet eigene Speicher- und Offlinekennungen',()=>{
 const runtime=all.get(prefix+'klasse5/mantel-runtime.js'),worker=all.get(prefix+'klasse5/mantel-sw.js');
 assert.match(runtime,/KEY='ium-recherche-beispiel-20261013-mantel-v1'/);
 assert.doesNotMatch(runtime,/KEY='ium-klasse'/);
 assert.match(worker,/CACHE='ium-recherche-beispiel-20261013-'/);
 assert.notEqual(worker,old.get('klasse5/mantel-sw.js'));
});
test('neue Seiten tragen Zusatzkennzeichnung und Rückweg zur alten Fassung',()=>{
 for(const [name,html]of all){if(!name.startsWith(prefix+'klasse5/')||!name.endsWith('.html'))continue;assert.match(html,/aria-label="Zusätzliches Beispiel"/,name);assert.match(html,/Bisherige Version/,name);}
});
test('kein technischer Quellstand oder interner Prüfbericht wird im Zusatz ausgeliefert',()=>{
 for(const name of all.keys())assert.doesNotMatch(name,/(?:^|\/)(?:quelle|node_modules|qa|evidence|docs|\.git)(?:\/|$)|\.test\.cjs$/);
 for(const [name,data]of all)if(name.startsWith(prefix)&&typeof data==='string')assert.doesNotMatch(data,/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost/i,name);
});
