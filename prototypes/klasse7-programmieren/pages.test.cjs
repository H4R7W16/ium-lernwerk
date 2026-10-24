'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {preparePages}=require('../pages/build.cjs');
const all=preparePages(),prefix='klasse7/programmieren/';
const hash=data=>crypto.createHash('sha256').update(data).digest('hex');
test('alle sechs ALG-Aufgaben mit vollständigen Startprojekten und Lehrhinweisen sind erreichbar',()=>{
 for(const id of [1,2,3,4,5,6]){const html=all.get(prefix+'lernende/alg-'+id+'.html');assert.ok(html,'ALG-'+id);assert.match(html,/Startprojekt speichern/);assert.match(html,/snap\/index\.html#open:/);assert.match(html,/405|Vorhersage|vorhersagen/);}
 for(const f of ['index.html','lehrpersonen/durchfuehrung-134.html','lehrpersonen/durchfuehrung-256.html','lehrpersonen/sicherung.html','lehrpersonen/hoerbriefing.html','lehrpersonen/safari-test.html','snap/index.html'])assert.ok(all.has(prefix+f),f);
 for(const f of ['ALG-1-Start','ALG-2-Start','ALG-3-Start','ALG-4-Fehlersuche','ALG-5-Start','ALG-6-Fehlersuche'])assert.match(all.get(prefix+'projekte/'+f+'.xml').toString(),/<project /,f);
});
test('1066 veröffentlichte Dateien bleiben bytegleich und Zusätze liegen ausschließlich unter Klasse 7',()=>{
 const baseline=require('./bestand-sha256.json');assert.equal(Object.keys(baseline.files).length,1066);
 for(const [name,h]of Object.entries(baseline.files))assert.equal(hash(all.get(name)),h,name);
 for(const name of all.keys())if(!Object.hasOwn(baseline.files,name))assert.ok(name.startsWith('klasse7/'),name);
});
test('Snap startet auf Deutsch ohne Cloud und Tracking mit auf eigenen Ursprung begrenzten Verbindungen',()=>{
 const html=all.get(prefix+'snap/index.html').toString();assert.match(html,/noCloud:\s*true/);assert.match(html,/lang:\s*'de'/);assert.match(html,/connect-src 'self'/);assert.doesNotMatch(html,/matomo|_paq|serviceWorker\.register|snap\.berkeley\.edu\//i);
 for(const [,ref]of html.matchAll(/(?:src|href)="([^"]+)"/g)){assert.ok(!/^(?:https?:)?\/\//i.test(ref),ref);const url=new URL(ref,'https://example.test/ium-lernwerk/'+prefix+'snap/index.html');assert.ok(all.has(url.pathname.slice('/ium-lernwerk/'.length)),ref);}
 assert.ok(all.has(prefix+'snap/locale/lang-de.js'));assert.match(all.get(prefix+'snap/LICENSE').toString(),/GNU AFFERO GENERAL PUBLIC LICENSE/);assert.ok(all.has(prefix+'snap/AENDERUNGEN.md'));
});
test('Testauftrag trennt Safari, Dateirückkehr, externe Verbindungen und Offlinebeobachtung',()=>{
 const html=all.get(prefix+'lehrpersonen/safari-test.html').toString();for(const term of ['Safari','Betriebssystem','Schrittmodus','Wiederimport','Verbindungen','Offline'])assert.ok(html.includes(term),term);
 assert.match(html,/GitHub/);assert.match(all.get(prefix+'index.html').toString(),/405/);
});
test('keine lokalen Arbeits-, Prüf- oder Geheimnisdateien gelangen in das neue öffentliche Paket',()=>{
 for(const [name,data]of all)if(name.startsWith('klasse7/')){assert.doesNotMatch(name,/(?:^|\/)(?:qa|node_modules|\.git|quellen)(?:\/|$)|(?:run\.json|\.env|\.test\.cjs)$/);if(name.endsWith('.html'))assert.doesNotMatch(data.toString(),/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost/);}
});
test('ein veränderter Altbestand wird vor Veröffentlichung abgewiesen',()=>{const {addClass7}=require('./build.cjs');const base=new Map([...all].filter(([name])=>!name.startsWith('klasse7/')));base.set('index.html','unbeabsichtigt verändert');assert.throws(()=>addClass7(base),/Veröffentlichter Bestand verändert/);});

test('alle ausgelieferten Snap-Dateien sind durch das Herkunftsmanifest gebunden',()=>{const p=JSON.parse(all.get(prefix+'snap/provenienz.json'));assert.equal(p.release,'v12.3.6');for(const [file,h]of Object.entries(p.files))assert.equal(hash(all.get(prefix+'snap/'+file)),h,file);});

test('Start- und Lehrprojekte zeigen in Snap den passenden Projektnamen',()=>{
 for(const [name,data]of all)if(name.startsWith(prefix)&&name.endsWith('.xml')){const xml=data.toString(),project=xml.match(/<project\s+name="([^"]+)"/),scene=xml.match(/<scene\s+name="([^"]+)"/);assert.ok(project,name);assert.ok(scene,name);assert.equal(scene[1],project[1],name);}
});