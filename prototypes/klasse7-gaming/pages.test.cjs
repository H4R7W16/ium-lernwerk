'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const published=require('../pages/build.cjs').preparePublishedPages(),ROOT='klasse7/gaming/',dir=path.join(__dirname,'inhalt'),manifest=require('./quelle-sha256.json');
const main=x=>x.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1],sha=b=>crypto.createHash('sha256').update(b).digest('hex');
test('Gamingpaket enthält sechs Aufgaben, sieben Briefings, sechs Projektionen und genau 270 Minuten',()=>{
 assert.equal([...published.keys()].filter(p=>p.startsWith(ROOT)&&p.endsWith('.html')).length,27);
 const meta=JSON.parse(published.get(ROOT+'fassung.json'));assert.equal(meta.minuten,270);assert.deepEqual(meta.aufgaben,[45,45,60,45,60,15]);
 for(const f of ['index.html','gamingbogen-durchfuhrung-und-auswertung.html','gamingbogen-sicherung.html','gamingbogen-briefing.html','gamingbogen-fachnotizen.html','gamingbogen-private-denkpause.html'])assert.ok(published.has(ROOT+f),f);
 for(let i=1;i<=6;i++){assert.ok(published.has(ROOT+'gam-'+i+'-briefing.html'));assert.ok(published.has(ROOT+'projektion-'+i+'.html'));}
});
test('Lernhandlungen, Sicherung, private Reflexion und Briefings bleiben gegenüber der geprüften Quelle unverändert',()=>{
 assert.equal(Object.keys(manifest.files).length,31);
 for(const [file,hash]of Object.entries(manifest.files)){
  const source=fs.readFileSync(path.join(dir,file));assert.equal(sha(source),hash,file);
  if(file.endsWith('.html')&&!['gamingbogen-produktionsbrief-und-reihenkommentar.html','gamingbogen-durchfuhrung-und-auswertung.html','gamingbogen-quellen-und-nutzungsrechte.html'].includes(file))assert.equal(main(published.get(ROOT+file)),main(source.toString()),file);
  if(file.startsWith('material/'))assert.equal(sha(published.get(ROOT+file)),hash,file);
 }
 const plan=main(fs.readFileSync(path.join(dir,'gamingbogen-durchfuhrung-und-auswertung.html'),'utf8')).replace('<span class="reference" title="Projektgrundlage im Vault">Klasse 7 - Jahrgangsbrief</span>','<a href="../programmieren/lehrpersonen/jahrgang.html">Klasse 7 – Jahrgangsbrief</a>').replace(' lokal öffnen.',' öffnen.');
 assert.equal(main(published.get(ROOT+'gamingbogen-durchfuhrung-und-auswertung.html')),plan);
});
test('Alle vier Lernbögen und der Jahrgangseinstieg erreichen Gaming, Gaming erreicht die anderen Bögen',()=>{
 for(const [name,html]of published){if(!name.endsWith('.html'))continue;
  if(name.startsWith(ROOT)){
   assert.match(html,/data-grade-switch/,name);
   for(const other of ['programmieren','medien','daten'])assert.ok(html.includes('href="../'+other+'/index.html"'),name+' → '+other);
  }
  if(name.startsWith('klasse7/programmieren/')&&html.includes('<nav class="year-nav"')){
   const nav=html.match(/<nav class="year-nav"[^>]*>([\s\S]*?)<\/nav>/)[1],href=nav.match(/href="([^"]+)">Gaming<\/a>/)?.[1];assert.ok(href,name);
   assert.equal(path.posix.normalize(path.posix.join(path.posix.dirname(name),href)),ROOT+'index.html');
  }
  if(/^klasse7\/(medien|daten)\//.test(name)&&html.includes('<nav class="year-nav" aria-label="Hauptnavigation">'))assert.match(html,/href="\.\.\/gaming\/index.html">Gaming<\/a>/,name);
 }
 assert.match(published.get('klasse7/index.html'),/href="gaming\/index.html"/);
 const year=published.get('klasse7/lehrpersonen.html');assert.match(year,/href="gaming\/index.html"/);assert.match(year,/GAM-4 und GAM-6 müssen 1–2 Wochen/);assert.doesNotMatch(year,/bleibt in Materialproduktion offen/);
});
test('Öffentliche Webfassung enthält keine internen Freigabetexte, lokalen Pfade oder Antworterfassung',()=>{
 for(const [name,html]of published){if(!name.startsWith(ROOT)||!name.endsWith('.html'))continue;
  assert.doesNotMatch(html,/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost|Lokale Lesefassung|Konzeptfreigabe|nicht Teil dieses Auftrags|Projektgrundlage im Vault|Vor öffentlicher Veröffentlichung|<(?:input|textarea|iframe|form)\b/i,name);
  const scripts=[...html.matchAll(/<script\b[^>]*src="([^"]+)"/g)].map(m=>m[1]);assert.deepEqual(scripts,['grade-navigation.js'],name);
 }
 const js=published.get(ROOT+'grade-navigation.js');assert.doesNotMatch(js,/fetch\(|localStorage|sessionStorage|sendBeacon|XMLHttpRequest/);
 const plan=published.get(ROOT+'gamingbogen-durchfuhrung-und-auswertung.html');for(let i=1;i<=12;i++)assert.ok(plan.includes('G'+String(i).padStart(2,'0')));
 assert.match(plan,/Keine personenbezogene Reflexionsliste/);assert.match(plan,/ein bis zwei Wochen/);
});
