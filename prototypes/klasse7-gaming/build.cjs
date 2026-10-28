'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ROOT='klasse7/gaming/',sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const css='\n/* Klassenwahl im Gamingbogen. */\nheader .lw-grade-switch{margin:0;padding:0;border:0;background:none}header .lw-grade-switch>.lw-grade-summary{width:327px;max-width:100%;padding:0;align-content:normal}header .lw-grade-summary .brand{width:100%;min-width:0}header .lw-grade-options{display:block;margin:0;gap:0}header .lw-grade-options a{padding:12px}@media(max-width:700px){header .lw-grade-switch>.lw-grade-summary{width:280px}}@media print{header .lw-grade-switch{display:none}}\n';
function adapt(name,html){
 let next=html.replace('<a href="index.html" aria-label="IuM 7 Gaming Start">','<a class="brand" href="index.html" aria-label="IuM 7 Gaming Start">')
 .replace('<nav aria-label="Hauptnavigation">','<nav aria-label="Hauptnavigation"><a href="../programmieren/index.html">Programmieren</a><a href="../medien/index.html">Medienwerkstatt</a><a href="../daten/index.html">Datenwerkstatt</a>')
 .replaceAll('Lokale Lesefassung','Webfassung')
 .replaceAll('<span class="reference" title="Projektgrundlage im Vault">Klasse 7 - Jahrgangsbrief</span>','<a href="../programmieren/lehrpersonen/jahrgang.html">Klasse 7 – Jahrgangsbrief</a>')
 .replaceAll('title="Projektgrundlage im Vault"','title="Redaktionelle Projektgrundlage"');
 if(name==='gamingbogen-durchfuhrung-und-auswertung.html')next=next.replace(' lokal öffnen.',' öffnen.');
 if(name==='gamingbogen-quellen-und-nutzungsrechte.html')next=next.replace('Die portable Lesefassung','Diese Webfassung').replace('Vor öffentlicher Veröffentlichung: lokale Kontaktangaben nicht in den allgemeinen Materialien ergänzen; Hosting und öffentliche Pfade gesondert prüfen.','Öffentliche Bereitstellung auf GitHub Pages: Die Inhalte und Materialpfade sind vollständig enthalten. Lokale Kontaktangaben gehören weiterhin nicht in die allgemeinen Materialien.');
 if(name==='gamingbogen-produktionsbrief-und-reihenkommentar.html'){
  next=next.replace(/<h2 id="auftrag-und-arbeitsplan">[\s\S]*?<\/ol>/,'<h2 id="auftrag-und-arbeitsplan">Rahmen und Bereitstellung</h2><p>Der Lernbogen Gaming und Wohlbefinden umfasst sechs Aufgaben mit Wissen, Hilfen und privaten Reflexionswegen, Fachnotizen, Durchführung und Auswertung, gemeinsamer Sicherung, sechs Projektionen und sieben Briefings als Vorlesetexte. Die redaktionell geprüfte Fassung 1.0 steht auf GitHub Pages bereit. Das Zeitbudget beträgt 270 Minuten; GAM-6 wird mit ein bis zwei Wochen Abstand zur ersten Erprobung eingeplant.</p>');
  next=next.replace('Das ist eine Produktionsentscheidung innerhalb des bestätigten Auftrags, keine vom Nutzer neu gewählte Variante.','Die Fallanalyse und eigene schulische Erprobung erschließen die vorgesehenen Lernziele innerhalb des Zeitbudgets.');
  next=next.replace(/Prüfbericht: <span class="reference"[^>]*>2026-10-28 - Gamingbogen Klasse 7 Qualitätsbericht<\/span>\./,'Redaktionelles Selbstreview vom 28.10.2026: drei konkrete Befunde zu Fallwahl, Jahrgangsstatus und privater Notiz nachgearbeitet und an der Endfassung überprüft. Die Veröffentlichung wurde zusätzlich auf Vollständigkeit und Navigation geprüft.');
 }
 return next;
}
function addGaming(source){
 const all=new Map(source),dir=path.join(__dirname,'inhalt'),manifest=require('./quelle-sha256.json');let count=0;
 function walk(current,base=''){for(const entry of fs.readdirSync(current,{withFileTypes:true})){
  const file=path.posix.join(base,entry.name),absolute=path.join(current,entry.name);
  if(entry.isSymbolicLink())throw Error('Symlink im Gaminginhalt: '+file);
  if(entry.isDirectory()){walk(absolute,file);continue;}
  if(/(?:^|\/)(?:Nachweise|qa|docs|node_modules|\.git)(?:\/|$)|(?:run\.json|\.env|\.test\.cjs)$/i.test(file))throw Error('Interner Gamingpfad: '+file);
  const bytes=fs.readFileSync(absolute);if(sha(bytes)!==manifest.files[file])throw Error('Ungeprüfte Gamingquelle: '+file);
  if(all.has(ROOT+file))throw Error('Gamingpfad existiert bereits: '+file);
  let value=/\.(?:html|css|js|json|svg)$/.test(file)?bytes.toString('utf8'):bytes;
  if(file.endsWith('.html'))value=adapt(file,value);if(file==='gaming.css')value+=css;
  all.set(ROOT+file,value);count++;
 }}
 walk(dir);if(count!==Object.keys(manifest.files).length)throw Error('Unvollständige Gamingquelle');
 const year='klasse7/programmieren/lehrpersonen/jahrgang.html',html=all.get(year),old='Gaming/Wohlbefinden bleibt in Materialproduktion offen.';
 if(typeof html!=='string'||!html.includes(old))throw Error('Bekannter Jahrgangsstatus fehlt.');
 all.set(year,html.replace('<p>Fassung 2.3 · 28.10.2026 · Gymnasium','<p>Fassung 2.5 · 28.10.2026 · Gymnasium').replace(old,'Auch Gaming und Wohlbefinden liegt seit dem 28.10.2026 als vollständige, redaktionell geprüfte Fassung 1.0 mit 270 Minuten vor. <a href="../../gaming/index.html">Zum Lernbogen mit Lernendenmaterialien, Durchführung, Sicherung und Briefings</a>. Die letzte Viertelstunde bleibt mit ein bis zwei Wochen Abstand zur ersten Erprobung eingeplant. Unterrichtserprobung bleibt offen.'));
 const entry='klasse7/index.html';
 all.set(entry,all.get(entry).replace('derzeit bereitgestellter Testbereich:','vier vollständig ausgearbeitete Lernbögen:').replace('</main>','<p><a href="medien/index.html">Medienwerkstatt</a> · <a href="daten/index.html">Datenwerkstatt</a> · <a href="gaming/index.html">Gaming und Wohlbefinden</a></p></main>'));
 return all;
}
function connectGaming(source){
 const all=new Map(source);
 for(const [name,html]of source){
  if(!name.endsWith('.html'))continue;
  if(name.startsWith('klasse7/programmieren/')&&html.includes('<nav class="lw-shell-nav"')){
   const href=path.posix.relative(path.posix.dirname(name),ROOT+'index.html');
   all.set(name,html.replace(/(<nav class="lw-shell-nav"[^>]*>)/,'$1<a href="'+href+'">Gaming</a>'));
  }else if((name.startsWith('klasse7/medien/')||name.startsWith('klasse7/daten/'))&&html.includes('<nav aria-label="Hauptnavigation">')){
   all.set(name,html.replace('<nav aria-label="Hauptnavigation">','<nav aria-label="Hauptnavigation"><a href="../gaming/index.html">Gaming</a>'));
  }
 }
 return all;
}
module.exports={addGaming,connectGaming};
