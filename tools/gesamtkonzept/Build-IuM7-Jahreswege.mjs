// Quelltexte aus dem Vault in den lokalen Repo-Baustein übertragen.
// Aufruf: node SCRIPT WORKSPACE REPO MARKED_ESM
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const [workspace,repo,markedPath]=process.argv.slice(2);
if(!workspace||!repo||!markedPath)throw Error('WORKSPACE REPO MARKED_ESM fehlen');
const {marked}=await import(pathToFileURL(markedPath));
const source=path.join(workspace,'Vault/40_Projekte/IuM-Lernwerk/Klasse 7/Jahreswege');
const target=path.join(repo,'prototypes/klasse7-jahrgang');
const hashes={date:'2026-11-03',files:{},sources:{}};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const dir of ['inhalt','material'])fs.mkdirSync(path.join(target,dir),{recursive:true});
function write(file,data){fs.writeFileSync(path.join(target,file),data);hashes.files[file]=hash(data);}
for(const file of fs.readdirSync(source).filter(n=>n.endsWith('.md'))){
 const bytes=fs.readFileSync(path.join(source,file)),md=bytes.toString('utf8').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'');
 hashes.sources[file]=hash(bytes);write('material/'+file,md);
 const title=md.match(/^# (.+)$/m)?.[1];if(!title)throw Error('Titel fehlt: '+file);
 let body=marked.parse(md).replace(/<table>/g,'<div class="table-wrap" role="region" aria-label="Tabelle, horizontal scrollbar" tabindex="0"><table>').replace(/<\/table>/g,'</table></div>');
 const html='<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+' · IuM 7</title><link rel="stylesheet" href="medien/medien.css"><link rel="icon" href="programmieren/brand/favicon.svg"></head><body class="year-page"><a class="skip" href="#inhalt">Zum Inhalt</a><header><a class="brand" href="index.html">IuM Lernwerk 7</a><nav aria-label="Hauptnavigation"></nav></header><main id="inhalt">'+body+'</main><footer>IuM Lernwerk · Klasse 7 · Jahreswege 1.1 · <a href="index.html">Jahrgangsübersicht</a> · <a href="lehrpersonen.html">Für Lehrpersonen</a><br>Eigene Texte und fiktive Fälle: <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de">CC BY-SA 4.0</a> · Keine Antwortspeicherung</footer></body></html>\n';
 write('inhalt/'+file.replace(/\.md$/,'.html'),html);
}
const diagnosis=path.join(workspace,'Assets/IuM-Lernwerk/Klasse7-Eingangsdiagnose/2026-10-22');
fs.mkdirSync(path.join(target,'inhalt/material'),{recursive:true});
for(const [src,dest]of [['IuM7-Eingangsdiagnose-Lernende.pdf','eingangsdiagnose-lernende.pdf'],['IuM7-Eingangsdiagnose-Lehrpersonen.pdf','eingangsdiagnose-lehrpersonen.pdf'],['Startdatei.txt','Startdatei.txt'],['Beobachtungsraster.txt','Beobachtungsraster.txt']])write('inhalt/material/'+dest,fs.readFileSync(path.join(diagnosis,src)));
fs.writeFileSync(path.join(target,'quelle-sha256.json'),JSON.stringify(hashes,null,2)+'\n');
console.log(Object.keys(hashes.files).length+' gebundene Dateien erzeugt.');
