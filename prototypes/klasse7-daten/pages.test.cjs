'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {preparePages,preparePublishedPages}=require('../pages/build.cjs');
const original=preparePages(),published=preparePublishedPages(),ROOT='klasse7/daten/';
const main=x=>x.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1],sha=b=>crypto.createHash('sha256').update(b).digest('hex');
test('Datenbogen ist vollständig mit fünf Aufgaben, sechs Briefings, Sicherung und 270 Minuten',()=>{
 assert.equal([...published.keys()].filter(p=>p.startsWith(ROOT)&&p.endsWith('.html')).length,24);
 const meta=JSON.parse(published.get(ROOT+'fassung.json'));assert.equal(meta.minuten,270);assert.deepEqual(meta.aufgaben,[60,45,75,60,30]);
 for(const f of ['index.html','datenbogen-durchfuhrung-und-auswertung.html','datenbogen-sicherung.html','datenbogen-briefing.html','datenbogen-material-und-alternativzugange.html','material/modell-daten.json'])assert.ok(published.has(ROOT+f),f);
 for(let i=1;i<=5;i++){assert.ok(published.has(ROOT+'dat-'+i+'-briefing.html'));assert.ok(published.has(ROOT+'projektion-'+i+'.html'));}
});
test('Geprüfte Quellen, Lernaufträge, Briefings und alle Bilder bleiben gebunden',()=>{
 const manifest=require('./quelle-sha256.json'),dir=path.join(__dirname,'inhalt');assert.equal(Object.keys(manifest.files).length,38);
 for(const [file,hash]of Object.entries(manifest.files)){
  const source=fs.readFileSync(path.join(dir,file));assert.equal(sha(source),hash,file);
  if(file.endsWith('.html')&&!['datenbogen-produktionsbrief-und-reihenkommentar.html','datenbogen-durchfuhrung-und-auswertung.html','datenbogen-quellen-und-nutzungsrechte.html'].includes(file))assert.equal(main(published.get(ROOT+file)),main(source.toString()),file);
  if(file.startsWith('material/'))assert.equal(sha(published.get(ROOT+file)),hash,file);
 }
 const plan=main(fs.readFileSync(path.join(dir,'datenbogen-durchfuhrung-und-auswertung.html'),'utf8')).replace('<span class="reference" title="Projektgrundlage im Vault">Klasse 7 - Jahrgangsbrief</span>','<a href="../programmieren/lehrpersonen/jahrgang.html">Klasse 7 – Jahrgangsbrief</a>').replace('Die Startseite der lokalen Lesefassung öffnen.','Die Startseite der Datenwerkstatt öffnen.');
 assert.equal(main(published.get(ROOT+'datenbogen-durchfuhrung-und-auswertung.html')),plan);
});
test('Datenwerkstatt und übrige Klasse-7-Lernbögen sind von Unterseiten gegenseitig erreichbar',()=>{
 for(const [name,html]of published){if(!name.endsWith('.html'))continue;
  if(name.startsWith(ROOT)&&!name.includes('/projektion-')){
   assert.match(html,/data-grade-switch/,name);
   assert.match(html,/href="\.\.\/programmieren\/index.html">Programmieren<\/a>/,name);
   assert.match(html,/href="\.\.\/medien\/index.html">Medienwerkstatt<\/a>/,name);
  }
  if(name.startsWith('klasse7/programmieren/')&&html.includes('<nav class="lw-shell-nav"')){
   const nav=html.match(/<nav class="lw-shell-nav"[^>]*>([\s\S]*?)<\/nav>/)[1],href=nav.match(/href="([^"]+)">Datenwerkstatt<\/a>/)?.[1];assert.ok(href,name);
   assert.equal(path.posix.normalize(path.posix.join(path.posix.dirname(name),href)),ROOT+'index.html');
  }
  if(name.startsWith('klasse7/medien/')&&html.includes('<nav aria-label="Hauptnavigation">'))assert.match(html,/href="\.\.\/daten\/index.html">Datenwerkstatt<\/a>/,name);
 }
});
test('Öffentliche Datenfassung enthält keine lokalen Pfade, Freigabetexte oder internen Nachweise',()=>{
 for(const [name,value]of published){if(!name.startsWith(ROOT))continue;
  assert.doesNotMatch(name,/(?:^|\/)(?:qa|docs|node_modules|\.git)(?:\/|$)/i,name);
  if(typeof value==='string')assert.doesNotMatch(value,/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost|Lokale Lesefassung|Konzeptfreigabe|nicht Bestandteil dieses Produktionsauftrags|Projektgrundlage im Vault/,name);
 }
 const sources=published.get(ROOT+'datenbogen-quellen-und-nutzungsrechte.html');assert.match(sources,/vollständig in dieser Webfassung enthalten/);
});
test('Jahrgangsbrief meldet Daten und Medien als ausgearbeitet mit direkten Einstiegen',()=>{
 const html=published.get('klasse7/programmieren/lehrpersonen/jahrgang.html');
 assert.match(html,/<p>Fassung 2.5 · 28.10.2026/);assert.match(html,/Medienbogen liegt seit dem 28.10.2026/);assert.match(html,/Datenbogen liegt seit dem 28.10.2026/);
 assert.match(html,/href="\.\.\/\.\.\/daten\/index.html"/);assert.match(html,/Gaming und Wohlbefinden liegt seit dem 28.10.2026/);
 assert.doesNotMatch(html,/Daten und Gaming\/Wohlbefinden bleiben in Materialproduktion offen/);
});
test('Datenmenge und Auflösung bleiben in tatsächlicher Ausgabe konsistent',()=>{
 const model=JSON.parse(published.get(ROOT+'material/modell-daten.json'));
 assert.deepEqual(model.rasters['dreieck-4'],['0000','0110','0110','1111']);
 const plan=published.get(ROOT+'datenbogen-durchfuhrung-und-auswertung.html');
 for(let i=1;i<=12;i++)assert.ok(plan.includes('D'+String(i).padStart(2,'0')));
 for(const term of ['48 Bit','26 Byte'])assert.ok(plan.includes(term),term);
});
