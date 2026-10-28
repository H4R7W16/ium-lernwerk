'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),crypto=require('node:crypto'),path=require('node:path');
const {preparePages,preparePublishedPages}=require('../pages/build.cjs');
const original=preparePages(),published=preparePublishedPages(),ROOT='klasse7/medien/';
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
test('Medienbogen veröffentlicht sämtliche Aufgaben und Lehrmaterialien mit unveränderten Zeitbudgets',()=>{
 const files=[...published.keys()].filter(name=>name.startsWith(ROOT));
 assert.equal(files.filter(name=>name.endsWith('.html')).length,24);
 for(const file of ['index.html','medienbogen-durchfuhrung-und-auswertung.html','medienbogen-sicherung.html','medienbogen-briefing.html','med-3-bedienkarte-bildbearbeitung.html','material/hof-original.png','material/hof-original.svg','material/rollen-A.svg','material/rollen-B.svg'])assert.ok(published.has(ROOT+file),file);
 const f=JSON.parse(published.get(ROOT+'fassung.json'));
 assert.deepEqual(f.aufgaben,[45,45,90,45,45]);assert.equal(f.minuten,270);
 for(let i=1;i<=5;i++){assert.ok(published.has(ROOT+'med-'+i+'-briefing.html'));assert.ok(published.has(ROOT+'projektion-'+i+'.html'));}
});
test('Medien und Programmieren sind von Aufgaben und Startseiten gegenseitig erreichbar',()=>{
 for(const [name,html]of published){
  if(!name.endsWith('.html'))continue;
  if(name.startsWith(ROOT)&&!name.includes('/projektion-')){
   assert.match(html,/data-grade-switch/,name);
   assert.match(html,/aria-label="Klassenstufe wählen, aktuell Klasse 7"/,name);
   assert.match(html,/href="\.\.\/programmieren\/index\.html">Programmieren<\/a>/,name);
  }
  if(name.startsWith('klasse7/programmieren/')&&/<nav class="lw-shell-nav"/.test(html)){
   const nav=html.match(/<nav class="lw-shell-nav"[^>]*>([\s\S]*?)<\/nav>/)[1];
   const ref=nav.match(/href="([^"]+)">Medienwerkstatt<\/a>/)?.[1];assert.ok(ref,name);
   assert.equal(path.posix.normalize(path.posix.join(path.posix.dirname(name),ref)),ROOT+'index.html',name);
  }
 }
});
test('Redaktionell geprüfte Texte und Bilder bleiben außerhalb des dokumentierten Publikationsadapters gleich',()=>{
 const fs=require('node:fs'),dir=path.join(__dirname,'inhalt');
 for(const name of fs.readdirSync(dir))if(name.endsWith('.html')){
  const source=fs.readFileSync(path.join(dir,name),'utf8'),html=original.get(ROOT+name);
  assert.ok(html,name);
  const main=x=>x.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1];
  if(!name.includes('produktionsbrief'))assert.equal(main(html),main(source),name);
 }
 const expected=require('./quelle-sha256.json');
 for(const [file,hash]of Object.entries(expected.files))assert.equal(sha(fs.readFileSync(path.join(dir,file))),hash,file);
});
test('Öffentliche Medienausgabe enthält keine lokalen Pfade oder internen Prüfnachweise',()=>{
 for(const [name,data]of published){if(!name.startsWith(ROOT))continue;
  assert.doesNotMatch(name,/(?:^|\/)(?:Nachweise|qa|docs|node_modules|\.git)(?:\/|$)/i,name);
  if(/\.(?:html|css|js|json|svg)$/.test(name))assert.doesNotMatch(String(data),/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost|Lokale Lesefassung/,name);
 }
 const article=published.get(ROOT+'medienbogen-produktionsbrief-und-reihenkommentar.html');
 assert.doesNotMatch(article,/Veröffentlichung auf GitHub\/Pages ist ein eigener Bereitstellungsschritt/);
 assert.match(published.get(ROOT+'med-3-ein-bild-zwei-geschichten.html'),/download="hof-original\.png"/);
});
test('Jahrgangsbrief zeigt die veröffentlichte Medienfassung und grenzt offene Lernbögen korrekt ein',()=>{
 const html=published.get('klasse7/programmieren/lehrpersonen/jahrgang.html');
 assert.ok(!html.includes('Die übrigen Lernbögen bleiben in Materialproduktion offen.'));
 assert.ok(html.includes('Medienbogen liegt seit dem 28.10.2026'));
 assert.ok(html.includes('Datenbogen liegt seit dem 28.10.2026'));
 assert.ok(html.includes('Gaming und Wohlbefinden liegt seit dem 28.10.2026'));
 assert.ok(html.includes('href="../../medien/index.html">Zur Medienwerkstatt'));
});
