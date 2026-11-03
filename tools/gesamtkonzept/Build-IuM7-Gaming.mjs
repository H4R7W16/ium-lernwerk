// Eigene portable Lesefassung. Code: MIT; eigene Inhalte: CC BY-SA 4.0.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [root,out]=process.argv.slice(2);
if(!root||!out)throw Error('node Build-IuM7-Gaming.mjs WORKSPACE AUSGABE');
const deps='C:/Users/Jan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {marked}=await import(pathToFileURL(path.join(deps,'marked/lib/marked.esm.js')));
const src=path.join(root,'Vault/40_Projekte/IuM-Lernwerk/Klasse 7/Gaming');
const original=fs.readFileSync(path.join(root,'Shared/Scripts/Build-IuM7-Medien.mjs'),'utf8');
const brand=path.join(root,'Assets/IuM-Lernwerk/Medien/2026-10-28-Fassung-1.0/material');
fs.mkdirSync(path.join(out,'material'),{recursive:true});
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const slug=s=>s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const files=fs.readdirSync(src).filter(f=>f.endsWith('.md'));
const names=Object.fromEntries(files.map(f=>[f.slice(0,-3),slug(f.slice(0,-3))+'.html']));
const target=n=>{if(!names[n])throw Error('Fehlender Text: '+n);return names[n];};
const renderer=new marked.Renderer();
renderer.heading=({tokens,depth,text})=>`<h${depth} id="${slug(text)}">${marked.parser(tokens).replace(/^<p>|<\/p>\n$/g,'')}</h${depth}>\n`;
marked.use({renderer});
function render(txt){
 txt=txt.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'');
 txt=txt.replace(/\[\[([^\]]+)\]\]/g,(_,ref)=>{const [dest,label]=ref.split('|');const [name,anchor]=dest.split('#');return names[name]?`[${label??(anchor||name)}](${names[name]}${anchor?'#'+slug(anchor):''})`:`<span class="reference" title="Projektgrundlage im Vault">${esc(label??name)}</span>`;});
 return marked.parse(txt).replace(/<table>/g,'<div class="table-wrap" tabindex="0" role="region" aria-label="Tabelle, bei Bedarf seitlich scrollen"><table>').replace(/<\/table>/g,'</table></div>');
}
const tasks=files.filter(f=>/^GAM-\d - /.test(f)&&!f.includes('Briefing'));
if(tasks.length!==6||files.length!==20)throw Error('Sechs Aufgaben und zwanzig Quellen erwartet');
const teacher=['Gamingbogen - Durchführung und Auswertung','Gamingbogen - Projektion','Gamingbogen - Briefing',...Array.from({length:6},(_,i)=>`GAM-${i+1} - Briefing`),'Gamingbogen - Produktionsbrief und Reihenkommentar','Gamingbogen - Quellen und Nutzungsrechte'];
function shell(title,body,extra=''){
return `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)} · IuM 7</title><link rel="icon" href="material/favicon.svg"><link rel="stylesheet" href="gaming.css"></head><body class="${extra}"><a class="skip" href="#inhalt">Zum Inhalt</a><header><a href="index.html" aria-label="IuM 7 Gaming Start"><img class="brand" src="material/ium-lernwerk-7.svg" alt="IuM Lernwerk 7"></a><nav aria-label="Hauptnavigation"><a href="index.html">Gaming</a><a href="${target('Gamingbogen - Fachnotizen')}">Fachnotizen</a><a href="${target('Gamingbogen - Private Denkpause')}">Private Denkpause</a><a href="${target('Gamingbogen - Sicherung')}">Sicherung</a></nav></header><nav class="course-nav" aria-label="Aufgaben">${tasks.map((f,i)=>`<a href="${names[f.slice(0,-3)]}">GAM-${i+1}</a>`).join('')}</nav><main id="inhalt">${body}</main><aside><details class="teacher-menu"><summary>Material für Lehrpersonen</summary><nav aria-label="Lehrpersonenmaterial">${teacher.map(n=>`<a href="${target(n)}">${esc(n.replace('Gamingbogen - ',''))}</a>`).join('')}</nav></details></aside><footer>Gaming und Wohlbefinden · Fassung 1.1 · 270 Minuten · Lokale Lesefassung<br><a href="${target('Gamingbogen - Quellen und Nutzungsrechte')}">Quellen und Nutzungsrechte</a> · Eigene Inhalte: <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de">CC BY-SA 4.0</a> · Keine Antwortspeicherung</footer></body></html>`;
}
const css=original.match(/const css=`([\s\S]*?)`;/)?.[1];
if(!css)throw Error('Reihenstil fehlt');
fs.writeFileSync(path.join(out,'gaming.css'),css+`
main>p,main>ul,main>ol{max-width:78ch}.case-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.offer-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.case,.offer{background:#f0f5f0;border:1px solid var(--line);border-radius:10px;padding:20px;margin:16px 0}.case h3,.offer h3{margin:0 0 16px}.offer .eyebrow{margin:0 0 10px}.offer h3{font-size:25px}.offer p{font-size:17px}.projection main{max-width:1280px;font-size:28px;line-height:1.4;padding:22px 32px;margin:16px auto}.projection h1{max-width:none;font-size:40px;margin:12px 0 24px}.projection p{margin:20px 0}.projection table{font-size:26px}.project-nav a{padding:6px;min-height:44px}header nav{gap:12px}header nav a{padding:10px 3px}@media(max-width:800px){.offer-grid{grid-template-columns:1fr}.case-grid{grid-template-columns:1fr}.case,.offer{margin:6px 0}.projection main{font-size:23px;padding:20px}.projection h1{font-size:32px}}@media print{.case-grid,.offer-grid{display:block}.case,.offer{break-inside:avoid}.project-nav{display:none}details>*{display:block}summary{font-size:12pt}}
`);
for(const f of files){const txt=fs.readFileSync(path.join(src,f),'utf8');fs.writeFileSync(path.join(out,names[f.slice(0,-3)]),shell(txt.match(/^# (.+)$/m)?.[1]??f,render(txt)));}
const durations=[45,45,60,45,60,15];
const titles=['Warum noch eine Runde?','Kostenlos – wer bezahlt?','Was tut gut, was belastet?','Eine Strategie ausprobieren','Grenzen und Hilfe','Mit Abstand neu entscheiden'];
const descriptions=['Erkläre Spielreiz, Teamplay und Druck an zwei Spielwelten.','Prüfe drei Angebote und die Interessen dahinter.','Unterscheide Beobachtung, mögliche Erklärung und Urteil.','Probiere eine Methode in echter schulischer Medienarbeit.','Begründe sichere Schritte und einen erreichbaren Hilfeweg.','Prüfe deine Entscheidung ein bis zwei Wochen später erneut.'];
fs.writeFileSync(path.join(out,'index.html'),shell('Wer bestimmt, wann Schluss ist?',`<p class="eyebrow">Klasse 7 · Gaming und Wohlbefinden</p><h1>Wer bestimmt, wann Schluss ist?</h1><p>Ein Rätsel reizt dich. Ein Team zählt auf dich. Ein Angebot wirbt um deine Aufmerksamkeit. Untersuche, was dahintersteckt – und wie begründete Entscheidungen möglich werden.</p><p><strong>270 Minuten</strong> · Sechs Aufgaben · Mit und ohne Spielerfahrung</p><div class="cards">${tasks.map((f,i)=>`<section class="card"><h2><a href="${names[f.slice(0,-3)]}">GAM-${i+1} · ${titles[i]}</a></h2><p>${descriptions[i]}</p><strong>${durations[i]} Minuten</strong></section>`).join('')}</div><h2>Dein Weg durch den Lernbogen</h2><p>Du untersuchst erfundene Fälle, begründest Entscheidungen und verbesserst eine Antwort nach Rückmeldung. Deine fachlichen Ergebnisse stehen in einem bekannten Dokument oder Heft. Eigene Erfahrungen bleiben in einer getrennten privaten Notiz. Du kannst den sachlichen Fallweg wählen.</p><p><a href="${target('Gamingbogen - Fachnotizen')}">Fachnotizen vorbereiten</a> · <a href="${target('Gamingbogen - Private Denkpause')}">So bleibt die Denkpause privat</a></p><h2>Für Lehrpersonen</h2><p>Vollständiger Minutenplan, Erwartungen, gemeinsame Sicherung, sechs Projektionen und sieben Briefings. Die letzte Viertelstunde wird mit zeitlichem Abstand eingeplant. Schulgeräte und konkrete Ansprechwege vor Einsatz klären.</p><p><a href="${target('Gamingbogen - Durchführung und Auswertung')}">Durchführung und Auswertung öffnen</a></p>`));
const projection=fs.readFileSync(path.join(src,'Gamingbogen - Projektion.md'),'utf8');
const parts=[...projection.matchAll(/^## (P\d[^\n]*)\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)];
if(parts.length!==6)throw Error('Sechs Projektionen erwartet');
for(let i=0;i<parts.length;i++)fs.writeFileSync(path.join(out,`projektion-${i+1}.html`),shell(parts[i][1],`<nav class="project-nav" aria-label="Projektionen"><a href="${target('Gamingbogen - Projektion')}">Impulse</a>${i?`<a href="projektion-${i}.html">Zurück</a>`:''}${i+1<parts.length?`<a href="projektion-${i+2}.html">Weiter</a>`:''}</nav>`+render('# '+parts[i][1]+'\n'+parts[i][2]),'projection'));
const overview=path.join(out,target('Gamingbogen - Projektion'));fs.writeFileSync(overview,fs.readFileSync(overview,'utf8').replace('<main id="inhalt">',`<main id="inhalt"><p>${parts.map((_,i)=>`<a href="projektion-${i+1}.html">Großansicht P${i+1}</a>`).join(' · ')}</p>`));
for(const f of ['ium-lernwerk-7.svg','favicon.svg'])fs.copyFileSync(path.join(brand,f),path.join(out,'material',f));
fs.writeFileSync(path.join(out,'fassung.json'),JSON.stringify({fassung:'1.1',datum:'2026-11-03',minuten:270,aufgaben:durations,phasen:[[10,10,15,10],[10,10,15,10],[15,15,20,10],[10,10,15,10],[15,15,20,10],[0,0,10,5]],stunden:[['GAM-1',45],['GAM-2',45],['GAM-3a',45],['GAM-3b',15,'GAM-4a',30],['GAM-4b',15,'GAM-5a',30],['GAM-5b',30,'GAM-6',15]],kriterien:Array.from({length:12},(_,i)=>`G${String(i+1).padStart(2,'0')}`),privateKriterien:['G04','G05','G07','G08','G09','G10'],quellen:files,html:files.length+1+parts.length},null,2));
console.log(JSON.stringify({out,quellen:files.length,html:files.length+1+parts.length,projektionen:parts.length,minuten:270}));
