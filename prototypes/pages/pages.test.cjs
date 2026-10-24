'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {preparePages}=require('./build.cjs'),preserved=require('./bestand-sha256.json');
const all=preparePages(),Y=require('../shared/class6-year.cjs');
test('alle veröffentlichten Bestandsdateien und der bisherige Einstieg bleiben bytegleich',()=>{
 assert.equal(Object.keys(preserved.files).length,812);
 for(const [name,hash]of Object.entries(preserved.files))assert.equal(crypto.createHash('sha256').update(all.get(name)).digest('hex'),hash,name);
 for(const name of all.keys())if(!Object.hasOwn(preserved.files,name))assert.ok(name.startsWith('klasse6/')||name.startsWith('klasse7/'),name);
});
test('vollständiger Klasse6-Jahrgang mit Materialien, Werkzeugen und allen Jahreszugängen wird veröffentlicht',()=>{
 for(const m of Y.modules)for(const file of ['index.html','wissen.html','material.html','lehrkraft.html','briefing.html'])assert.ok(all.has('klasse6/'+m.area+'/'+file),m.id+'/'+file);
 for(const file of ['index.html','arbeit.html','stoffverteilung.html','jahresplan.html','wiederholen.html','jahresstart.html','uebergaenge.html','netze/netz-app.js','algorithmen/zeichnen-app.js','manifest.webmanifest','mantel-runtime.js'])assert.ok(all.has('klasse6/'+file),file);
 for(const r of Y.recalls)assert.ok(all.get('klasse6/'+r.area+'/schritt-'+r.step+'.html').includes('id="recall-'+r.step+'-'+r.block+'"'),r.id);
});
test('Klasse6-Speicher, Manifest und Offlinepaket bleiben im eigenen Unterpfad',()=>{
 const manifest=JSON.parse(all.get('klasse6/manifest.webmanifest'));
 assert.equal(manifest.scope,'./');assert.equal(manifest.start_url,'./');
 assert.match(all.get('klasse6/mantel-runtime.js'),/KEY='ium-klasse'\+\(/);
 const worker=all.get('klasse6/mantel-sw.js');
 for(const [name]of all)if(name.startsWith('klasse6/')&&!name.endsWith('mantel-sw.js'))assert.ok(worker.includes(JSON.stringify(name.slice('klasse6/'.length))),name);
 assert.notEqual(worker,all.get('klasse5/mantel-sw.js'));
 assert.doesNotMatch(worker,/beispiele\/recherche/);
});
