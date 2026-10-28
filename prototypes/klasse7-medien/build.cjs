'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ROOT='klasse7/medien/';
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
const css='\n/* Native Klassenwahl innerhalb der Medienkopfzeile. */\nheader .lw-grade-switch{margin:0;padding:0;border:0;background:none}header .lw-grade-switch>.lw-grade-summary{width:327px;max-width:100%;padding:0;align-content:normal}header .lw-grade-summary .brand{width:100%;min-width:0}header .lw-grade-options{display:block;margin:0;gap:0}header .lw-grade-options a{padding:12px}@media(max-width:700px){header .lw-grade-switch>.lw-grade-summary{width:280px}}@media print{header .lw-grade-switch{display:none}}\n';
function adapt(name,html){
 let next=html.replace('<a href="index.html" aria-label="IuM 7 Medienwerkstatt Start">','<a class="brand" href="index.html" aria-label="IuM 7 Medienwerkstatt Start">');
 next=next.replace('<nav aria-label="Hauptnavigation">','<nav aria-label="Hauptnavigation"><a href="../programmieren/index.html">Programmieren</a>');
 next=next.replaceAll('Lokale Lesefassung','Webfassung');
 if(name==='medienbogen-produktionsbrief-und-reihenkommentar.html'){
  next=next.replace('Dieser Auftrag umfasst ein lokal nutzbares digitales Materialpaket; Veröffentlichung auf GitHub/Pages ist ein eigener Bereitstellungsschritt.','Diese Webfassung stellt das vollständig ausgearbeitete Materialpaket auf GitHub Pages bereit. Der bekannte schulische Editor und eigene Werkstattnotizen bleiben die Arbeitsumgebung.');
  next=next.replace(/<p>Status von Produktion, Bereitstellung und Prüfung steht im datierten [\s\S]*?<\/p>/,'<p>Redaktionelles Selbstreview vom 28.10.2026: sechs konkrete Befunde nachgearbeitet und an der Endfassung geprüft. Die Prüfung umfasst Materialien, Zeitrechnung, Verweise und ausgewählte Browser-/Bildhandlungen. Unterrichtserprobung und vollständiger Dateiweg am Schulgerät bleiben offen.</p>');
 }
 return next;
}
function addMedia(source){
 const all=new Map(source),dir=path.join(__dirname,'inhalt'),manifest=require('./quelle-sha256.json');let count=0;
 function walk(current,base=''){
  for(const entry of fs.readdirSync(current,{withFileTypes:true})){
   const file=path.posix.join(base,entry.name),absolute=path.join(current,entry.name);
   if(entry.isSymbolicLink())throw Error('Symlink im Medieninhalt: '+file);
   if(entry.isDirectory()){walk(absolute,file);continue;}
   if(/(?:^|\/)(?:Nachweise|qa|docs|node_modules|\.git)(?:\/|$)|(?:run\.json|\.env|\.test\.cjs)$/i.test(file))throw Error('Interner Medienpfad: '+file);
   const bytes=fs.readFileSync(absolute);
   if(sha(bytes)!==manifest.files[file])throw Error('Ungeprüfte Medienquelle: '+file);
   if(all.has(ROOT+file))throw Error('Medienpfad existiert bereits: '+file);
   let value=/\.(?:html|css|js|json|svg)$/.test(file)?bytes.toString('utf8'):bytes;
   if(file.endsWith('.html'))value=adapt(file,value);if(file==='medien.css')value+=css;
   all.set(ROOT+file,value);count++;
  }
 }
 walk(dir);if(count!==Object.keys(manifest.files).length)throw Error('Unvollständige Medienquelle');
 const year='klasse7/programmieren/lehrpersonen/jahrgang.html',html=all.get(year);
 if(typeof html!=='string'||!html.includes('Die übrigen Lernbögen bleiben in Materialproduktion offen.'))throw Error('Bekannter Jahrgangsstatus fehlt.');
 all.set(year,html.replace('Die übrigen Lernbögen bleiben in Materialproduktion offen.','Der Medienbogen liegt seit dem 28.10.2026 als vollständige, redaktionell geprüfte Fassung 1.0 mit 270 Minuten vor. <a href="../../medien/index.html">Zur Medienwerkstatt mit Durchführung, Sicherung und Briefings</a>. Unterrichtserprobung bleibt offen. Daten und Gaming/Wohlbefinden bleiben in Materialproduktion offen.'));
 return all;
}
function connectMedia(source){
 const all=new Map(source);
 for(const [name,html]of source){
  if(!name.startsWith('klasse7/programmieren/')||!name.endsWith('.html')||!html.includes('<nav class="lw-shell-nav"'))continue;
  const href=path.posix.relative(path.posix.dirname(name),ROOT+'index.html');
  all.set(name,html.replace(/(<nav class="lw-shell-nav"[^>]*>)/,'$1<a href="'+href+'">Medienwerkstatt</a>'));
 }
 return all;
}
module.exports={addMedia,connectMedia};
