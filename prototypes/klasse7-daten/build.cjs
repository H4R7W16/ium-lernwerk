'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ROOT='klasse7/daten/',sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const css='\n/* Klassenwahl in der Datenwerkstatt. */\nheader .lw-grade-switch{margin:0;padding:0;border:0;background:none}header .lw-grade-switch>.lw-grade-summary{width:327px;max-width:100%;padding:0;align-content:normal}header .lw-grade-summary .brand{width:100%;min-width:0}header .lw-grade-options{display:block;margin:0;gap:0}header .lw-grade-options a{padding:12px}@media(max-width:700px){header .lw-grade-switch>.lw-grade-summary{width:280px}}@media print{header .lw-grade-switch{display:none}}\n';
function adapt(name,html){
 let next=html.replace('<a href="index.html" aria-label="IuM 7 Datenwerkstatt Start">','<a class="brand" href="index.html" aria-label="IuM 7 Datenwerkstatt Start">')
 .replace('<nav aria-label="Hauptnavigation">','<nav aria-label="Hauptnavigation"><a href="../programmieren/index.html">Programmieren</a><a href="../medien/index.html">Medienwerkstatt</a>')
 .replaceAll('Lokale Lesefassung','Webfassung')
 .replaceAll('<span class="reference" title="Projektgrundlage im Vault">Klasse 7 - Jahrgangsbrief</span>','<a href="../programmieren/lehrpersonen/jahrgang.html">Klasse 7 – Jahrgangsbrief</a>')
 .replaceAll('title="Projektgrundlage im Vault"','title="Redaktionelle Projektgrundlage"');
 if(name==='datenbogen-durchfuhrung-und-auswertung.html')next=next.replace('Die Startseite der lokalen Lesefassung öffnen.','Die Startseite der Datenwerkstatt öffnen.');
 if(name==='datenbogen-quellen-und-nutzungsrechte.html')next=next.replace('vollständig lokal verfügbar','vollständig in dieser Webfassung enthalten');
 if(name==='datenbogen-produktionsbrief-und-reihenkommentar.html'){
  next=next.replace(/<h2 id="auftrag-und-arbeitsplan">[\s\S]*?<\/ol>/,'<h2 id="auftrag-und-arbeitsplan">Rahmen und Bereitstellung</h2><p>Die Datenwerkstatt umfasst fünf Lernendenaufgaben mit Materialien und Hilfen, Durchführung und Auswertung, gemeinsamer Sicherung, fünf Projektionen und sechs Briefings als Vorlesetexte. Die redaktionell geprüfte Fassung 1.0 steht auf GitHub Pages bereit. Eigene Ergebnisse entstehen im bekannten Dokument oder Heft. Das Zeitbudget beträgt 270 Minuten.</p>');
  next=next.replace(/<p>Dokumentierte Endprüfung:[\s\S]*?<\/p>/,'<p>Redaktionelles Selbstreview vom 28.10.2026 mit Nacharbeit und Prüfung der Endfassung: Codierungen, Rechenfälle, Rastergeometrie, Materialien und Zeitbudget wurden kontrolliert. Die Veröffentlichung wurde zusätzlich auf Vollständigkeit und Navigation geprüft. Unterrichtserprobung und die Prüfung benötigter Zugänge am Schulgerät bleiben offen.</p>');
 }
 return next;
}
function addData(source){
 const all=new Map(source),dir=path.join(__dirname,'inhalt'),manifest=require('./quelle-sha256.json');let count=0;
 function walk(current,base=''){for(const entry of fs.readdirSync(current,{withFileTypes:true})){
  const file=path.posix.join(base,entry.name),absolute=path.join(current,entry.name);
  if(entry.isSymbolicLink())throw Error('Symlink im Dateninhalt: '+file);
  if(entry.isDirectory()){walk(absolute,file);continue;}
  if(/(?:^|\/)(?:Nachweise|qa|docs|node_modules|\.git)(?:\/|$)|(?:run\.json|\.env|\.test\.cjs)$/i.test(file))throw Error('Interner Datenpfad: '+file);
  const bytes=fs.readFileSync(absolute);if(sha(bytes)!==manifest.files[file])throw Error('Ungeprüfte Datenquelle: '+file);
  if(all.has(ROOT+file))throw Error('Datenpfad existiert bereits: '+file);
  let value=/\.(?:html|css|js|json|svg)$/.test(file)?bytes.toString('utf8'):bytes;
  if(file.endsWith('.html'))value=adapt(file,value);if(file==='daten.css')value+=css;
  all.set(ROOT+file,value);count++;
 }}
 walk(dir);if(count!==Object.keys(manifest.files).length)throw Error('Unvollständige Datenquelle');
 const year='klasse7/programmieren/lehrpersonen/jahrgang.html',html=all.get(year),old='Daten und Gaming/Wohlbefinden bleiben in Materialproduktion offen.';
 if(typeof html!=='string'||!html.includes(old))throw Error('Bekannter Jahrgangsstatus fehlt.');
 all.set(year,html.replace('<p>Fassung 2.2 · 27.10.2026 · Gymnasium','<p>Fassung 2.3 · 28.10.2026 · Gymnasium').replace(old,'Auch der Datenbogen liegt seit dem 28.10.2026 als vollständige, redaktionell geprüfte Fassung 1.0 mit 270 Minuten vor. <a href="../../daten/index.html">Zur Datenwerkstatt mit Lernendenmaterialien, Durchführung, Sicherung und Briefings</a>. Unterrichtserprobung bleibt offen. Gaming/Wohlbefinden bleibt in Materialproduktion offen.'));
 return all;
}
function connectData(source){
 const all=new Map(source);
 for(const [name,html]of source){
  if(!name.endsWith('.html'))continue;
  if(name.startsWith('klasse7/programmieren/')&&html.includes('<nav class="lw-shell-nav"')){
   const href=path.posix.relative(path.posix.dirname(name),ROOT+'index.html');
   all.set(name,html.replace(/(<nav class="lw-shell-nav"[^>]*>)/,'$1<a href="'+href+'">Datenwerkstatt</a>'));
  }else if(name.startsWith('klasse7/medien/')&&html.includes('<nav aria-label="Hauptnavigation">')){
   all.set(name,html.replace('<nav aria-label="Hauptnavigation">','<nav aria-label="Hauptnavigation"><a href="../daten/index.html">Datenwerkstatt</a>'));
  }
 }
 return all;
}
module.exports={addData,connectData};
