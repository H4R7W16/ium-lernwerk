// Reproduzierbare Lesefassung aus den kanonischen Vault-Texten. Keine Netzwerkzugriffe.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';
const root=process.argv[2], out=process.argv[3];
if(!root||!out) throw Error('Aufruf: node Build-IuM7-Medien.mjs WORKSPACE AUSGABE [LOKALES_REPO]');
const deps=path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const repo=process.argv[4]??path.join(os.homedir(),'AI-Workspace-Local/Work/ium-alg4-revision-20261027');
const {marked}=await import(pathToFileURL(path.join(deps,'marked/lib/marked.esm.js')));
const {default:sharp}=await import(pathToFileURL(path.join(deps,'sharp/dist/index.mjs')));
const src=path.join(root,'Vault/40_Projekte/IuM-Lernwerk/Klasse 7/Medien');
const brand=path.join(repo,'prototypes/klasse7-programmieren/brand');
fs.mkdirSync(path.join(out,'material'),{recursive:true});
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const slug=s=>s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const files=fs.readdirSync(src).filter(f=>f.endsWith('.md'));
const names=Object.fromEntries(files.map(f=>[f.slice(0,-3),slug(f.slice(0,-3))+'.html']));
const target=name=>names[name];
const titleOf=s=>s.match(/^# (.+)$/m)?.[1]??'Medienwerkstatt';
const renderer=new marked.Renderer();
renderer.heading=({tokens,depth,text})=>`<h${depth} id="${slug(text)}">${marked.parser(tokens).replace(/^<p>|<\/p>\n$/g,'')}</h${depth}>\n`;
marked.use({renderer});
const fizzFolder='Assets/Outputs/IuM-Lernwerk/Fizz-MED-1-20261105-v4';
const fizzClips=[
 {id:'spot',video:'Fizz-MED-1-v4.mp4',captions:'fizz-med1-v4.de.vtt',poster:'spot-vorschau.jpg'},
 {id:'tonvergleich',video:'Fizz-MED-1-Tonvergleich-v4.mp4',captions:'fizz-tonvergleich-v4.de.vtt',poster:'vergleich-vorschau.jpg'}
];
function renderFizzClips(html) {
 return html.replace(/<p><a href="([^"]+)">([^<]+)<\/a><\/p>/g,(original,href,label)=>{
  const clip=fizzClips.find(item=>href==='../../../../../'+fizzFolder+'/'+item.video);
  if(!clip)return original;
  const base='material/fizz/'+clip.id;
  return `<figure class="mp-clip"><figcaption id="fizz-${clip.id}">${label}</figcaption>
<video controls playsinline preload="none" width="900" height="1600" aria-labelledby="fizz-${clip.id}" src="${base}.mp4" poster="${base}.jpg">
<track kind="captions" srclang="de" label="Deutsch · Sprache und Geräusche" src="${base}.de.vtt">
<a href="${base}.mp4">${label}</a></video></figure>`;
 });
}
function render(text){
 text=text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'');
 text=text.replaceAll('../../../../../Assets/IuM-Lernwerk/Medien/2026-10-28-Fassung-1.0/material/','material/');
 text=text.replace(/\[\[([^\]]+)\]\]/g,(_,ref)=>{let [name,anchor]=ref.split('#'),[actual,label]=name.split('|'); return names[actual]?`[${label??(anchor||actual)}](${names[actual]}${anchor?'#'+slug(anchor):''})`:`<span class="reference" title="Projektgrundlage im Vault">${esc(label??actual)}</span>`;});
 let html=marked.parse(text);
 html=html.replace(/<a href="(material\/[^"\s]+\.(?:png|svg))">/g,(_,url)=>`<a href="${url}" download="${path.basename(url)}">`);
 html=html.replace(/<table>/g,'<div class="table-wrap" tabindex="0" role="region" aria-label="Tabelle, bei Bedarf seitlich scrollen"><table>').replace(/<\/table>/g,'</table></div>');
 return html;
}
const tasks=files.filter(f=>/^MED-\d - /.test(f)&&!f.includes('Briefing')&&!f.includes('Bedienkarte'));
const nav=tasks.map((f,i)=>`<a href="${names[f.slice(0,-3)]}">MED-${i+1}</a>`).join('');
const teacherNames=['Medienbogen - Durchführung und Auswertung','Medienbogen - Projektion','Medienbogen - Briefing','MED-1 - Briefing','MED-2 - Briefing','MED-3 - Briefing','MED-4 - Briefing','MED-5 - Briefing','Medienbogen - Produktionsbrief und Reihenkommentar','Medienbogen - Quellen und Nutzungsrechte'];
const menu=`<details class="teacher-menu"><summary>Material für Lehrpersonen</summary><nav aria-label="Lehrpersonenmaterial">${teacherNames.map(n=>`<a href="${target(n)}">${esc(n.replace('Medienbogen - ',''))}</a>`).join('')}</nav></details>`;
function shell(title,body,extra=''){
const pilot=extra==='media-path';
const sheet=pilot?'<link rel="stylesheet" href="lernweg.css">':'';
const shortcuts=pilot?'':`<div class="course-nav" aria-label="Aufgaben">${nav}</div>`;
const materials=pilot?menu.replace('<nav aria-label="Lehrpersonenmaterial">','<nav aria-label="Lehrpersonenmaterial"><!--year-plan-->'):menu;
return `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)} · IuM 7</title><link rel="icon" href="material/favicon.svg"><link rel="stylesheet" href="medien.css">${sheet}</head><body class="${extra}"><a class="skip" href="#inhalt">Zum Inhalt</a><header><a href="index.html" aria-label="IuM 7 Medienwerkstatt Start"><img class="brand" src="material/ium-lernwerk-7.svg" alt="IuM Lernwerk 7"></a><nav aria-label="Hauptnavigation"><a href="index.html">Medienwerkstatt</a><a href="${target('Medienbogen - Werkstattnotizen')}">Meine Notizen</a><a href="${target('Medienbogen - Sicherung')}">Sicherung</a></nav></header>${shortcuts}<main id="inhalt"${pilot?' tabindex="-1"':''}>${body}</main><aside>${materials}</aside><footer>Medienwerkstatt · Fassung 1.1 · 270 Minuten · Lokale Lesefassung<br><a href="${target('Medienbogen - Quellen und Nutzungsrechte')}">Quellen und Nutzungsrechte</a> · Eigene Inhalte: <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de">CC BY-SA 4.0</a> · Keine Antwortspeicherung</footer></body></html>`;
}
const css=`:root{--paper:#f7f7f2;--ink:#222a2f;--muted:#5b656d;--accent:#245743;--soft:#eaf2ec;--line:#c8d1cb;font-family:'Segoe UI',Arial,sans-serif;color:var(--ink);background:var(--paper);font-size:18px;line-height:1.65}*{box-sizing:border-box}body{margin:0}a{color:var(--accent);text-underline-offset:3px}a:hover{color:#173c2d}a:focus-visible,summary:focus-visible,.table-wrap:focus-visible{outline:3px solid #a85100;outline-offset:4px}.skip{position:absolute;top:-90px;left:16px;background:white;padding:12px}.skip:focus{top:10px;z-index:5}header{max-width:1280px;margin:auto;padding:24px 32px;display:flex;align-items:center;justify-content:space-between;gap:28px;border-bottom:1px solid var(--line)}.brand{width:327px;max-width:100%;display:block}header nav{display:flex;gap:22px;flex-wrap:wrap}header nav a{padding:10px 0;font-size:16px}.course-nav{max-width:1040px;margin:18px auto;display:flex;gap:10px;padding:0 24px;flex-wrap:wrap}.course-nav a{border:1px solid var(--line);padding:8px 18px;border-radius:7px;text-decoration:none;background:white;font-weight:650;min-height:44px}main{max-width:1040px;margin:24px auto 40px;padding:30px 42px;background:white;border:1px solid var(--line);border-radius:12px;overflow-wrap:anywhere}h1{font-size:clamp(30px,4vw,44px);letter-spacing:-.035em;line-height:1.15;margin:8px 0 24px;max-width:25ch}h2{font-size:27px;line-height:1.3;margin:38px 0 18px;padding-top:24px;border-top:1px solid var(--line);scroll-margin-top:20px}h3{font-size:21px;line-height:1.4;margin:26px 0 12px}p{margin:14px 0}li{margin:8px 0}main img{max-width:100%;height:auto;display:block;border-radius:8px;margin:20px auto}main img[src$='rollen-A.svg'],main img[src$='rollen-B.svg']{width:740px}blockquote{border-left:5px solid var(--accent);margin:20px 0;background:var(--soft);padding:12px 24px}.table-wrap{overflow-x:auto;max-width:100%;margin:20px 0;border:1px solid var(--line);border-radius:8px}table{border-collapse:collapse;width:100%;font-size:16px;line-height:1.5;min-width:550px}td,th{text-align:left;vertical-align:top;padding:13px 16px;border-bottom:1px solid var(--line);border-right:1px solid var(--line)}th{background:var(--soft);font-weight:650}details{margin:18px 0;border:1px solid var(--line);border-radius:9px;padding:10px 18px;background:#fff6df}summary{cursor:pointer;font-weight:650;min-height:44px;align-content:center}details p{margin:12px 0}code{background:#eef1ed;padding:2px 5px;border-radius:3px;font-size:.9em}aside,footer{max-width:1040px;margin:20px auto;padding:0 24px}footer{color:var(--muted);font-size:14px;padding-bottom:30px}.teacher-menu{background:var(--soft)}.teacher-menu nav{display:grid;grid-template-columns:1fr 1fr;gap:8px}.teacher-menu a{padding:8px;min-height:44px;font-size:16px}.reference{color:var(--muted)}.eyebrow{font-size:15px;color:var(--muted);text-transform:uppercase;letter-spacing:.09em}.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{border:1px solid var(--line);border-radius:10px;padding:20px;background:var(--soft)}.card h2{font-size:23px;border:0;margin:0 0 10px;padding:0}.card a{text-decoration:none}.card p{font-size:16px}.projection main{font-size:30px;max-width:1280px}.projection h1{font-size:44px}.projection header,.projection .course-nav,.projection aside,.projection footer{display:none}.projection main img{max-height:57vh;width:auto}.projection .project-nav{display:flex;gap:18px;font-size:18px}.projection blockquote{font-size:35px}@media(max-width:700px){header{padding:18px 20px;display:block}.brand{width:280px}header nav{gap:16px;margin-top:14px}main{margin:16px 12px;padding:23px 20px}.course-nav{padding:0 12px;gap:6px}.course-nav a{padding:8px 12px}h2{font-size:24px}.cards,.teacher-menu nav{grid-template-columns:1fr}aside,footer{padding:0 14px}.projection main{font-size:23px}.projection h1{font-size:32px}}@media print{header,.course-nav,aside,footer,.skip{display:none}main{border:0;margin:0;padding:0;max-width:none}details{break-inside:avoid}h2,h3{break-after:avoid}main img{max-height:70vh}.table-wrap{overflow:visible}table{min-width:0;font-size:11pt}a{color:inherit}}`;
fs.writeFileSync(path.join(out,'medien.css'),css);
const descriptions=[
 'Interessen erkennen und vier Einflusswege auseinanderhalten.',
 'Eine Meldung mit Originalbeleg und unabhängiger Beobachtung prüfen.',
 'Zwei eigene Bildwirkungen entwerfen, bearbeiten und revidieren.',
 'Rollenbilder und Aussehensnormen an Bild und Text untersuchen.',
 'Kommunikationswege vergleichen und begründet sicher reagieren.'
];
const minutes=[45,45,90,45,45];
const lessons=tasks.map((file,i)=>({
 href:names[file.slice(0,-3)],
 title:esc(titleOf(fs.readFileSync(path.join(src,file),'utf8')).replace(/^MED-\d+ · /,'')),
 code:'MED-'+(i+1), minutes:minutes[i], description:descriptions[i]
}));
const notes=target('Medienbogen - Werkstattnotizen');
const recap=target('Medienbogen - Sicherung');
const arrow='<span aria-hidden="true">→</span>';

function materialsLinks(){
 return `<nav class="mp-materials" aria-label="Arbeitsmaterial"><a href="${notes}">Werkstattnotizen</a><a href="${recap}">Gemeinsame Sicherung</a><a href="${target('MED-3 - Bedienkarte Bildbearbeitung')}">Bedienkarte für die Bildwerkstatt</a></nav>`;
}

function mediaHome(){
 const rows=lessons.map(item=>`<li><a href="${item.href}"><span class="mp-code">${item.code}</span><span class="mp-row-copy"><strong>${item.title}</strong><small>${item.description}</small></span><span class="mp-time">${item.minutes} Min.</span>${arrow}</a></li>`).join('');
 return `<section class="mp-home-hero">
 <div><p class="mp-kicker">Klasse 7 · Medienwerkstatt</p>
 <h1>Was zeigen wir – <span>und was lassen wir weg?</span></h1>
 <p class="mp-lead">Du arbeitest in einer Schulredaktion. Prüfe Beiträge, verändere Bilder und begründe, was ihr veröffentlicht.</p>
 <div class="mp-actions"><a class="mp-primary" href="${lessons[0].href}">Mit MED-1 beginnen ${arrow}</a><a class="mp-secondary" href="#aufgaben">Alle Aufgaben <span aria-hidden="true">↓</span></a></div>
 </div>
 <figure class="mp-comparison"><div class="mp-pair">
 <div class="mp-crop mp-left"><img src="material/hof-original.svg" alt="Ausschnitt mit Baum und Sitzbank auf dem Schulhof."></div>
 <div class="mp-crop mp-right"><img src="material/hof-original.svg" alt="Ausschnitt mit Papierkorb und herumliegendem Papier auf demselben Hof."></div>
 </div><figcaption>Ein Schulhof, zwei Bildausschnitte.</figcaption></figure>
 </section>
 <section class="mp-route" id="aufgaben" tabindex="-1" aria-labelledby="mp-aufgaben"><div class="mp-section-title"><h2 id="mp-aufgaben">Deine Aufgaben</h2><span>5 Aufgaben · 270 Minuten</span></div><ol>${rows}</ol></section>
 <section class="mp-support"><h2>Deine Ergebnisse</h2><p>Eine Redaktionstabelle, ein Quellenurteil, eigene Bildvarianten, ein Kartenvergleich und begründete Kommunikationsentscheidungen. Persönliche Denkpausen bleiben privat.</p><p>Halte deine Notizen im bekannten Dokument oder Heft fest. Du brauchst keine Anmeldung.</p>${materialsLinks()}</section>
 <section class="mp-support"><h2>Für Lehrpersonen</h2><p>Hier finden Sie Durchführung, Sicherung, Projektionsimpulse und Briefings. Die Fassung ist redaktionell geprüft. Die Unterrichtserprobung steht aus.</p></section>`;
}

function firstLesson(text){
 // MED-1 beginnt in der Autorenfassung mit Ergebnis, Schulblogauftrag und Fallhinweisen.
 const md=text.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'').trim();
 const start=md.search(/^## /m);
 if(start<0)throw Error('MED-1: Arbeitsschritte fehlen');
 const [title,result,assignment,...context]=md.slice(0,start).trim().split(/\r?\n\s*\r?\n/);
 const outcomePrefix='**'+lessons[0].minutes+' Minuten · Dein Ergebnis:**';
 if(!result?.startsWith(outcomePrefix)||!assignment||!context.length)throw Error('MED-1: Autorenstruktur des Einstiegs prüfen');
 const steps=renderFizzClips(render(md.slice(start)));
 const firstId=steps.match(/^<h2 id="([^"]+)"/)?.[1];
 if(!firstId)throw Error('MED-1: Ziel des ersten Arbeitsschritts fehlt');
 const choices=lessons.map((item,i)=>`<a href="${item.href}"${i===0?' aria-current="page"':''}><b>${item.code}</b> ${item.title}</a>`).join('');
 return `<section class="mp-task-hero">
 <div class="mp-task-bar"><p class="mp-kicker">Medien · Aufgabe 1 von 5</p>
 <details class="mp-picker"><summary>Alle Aufgaben</summary><nav aria-label="Aufgabe wählen">${choices}</nav></details></div>
 <div class="mp-task-intro"><div>${render(title).replace('>MED-1 · ','>')}<div class="mp-lead">${render(assignment)}</div>
 <a class="mp-primary" href="#${firstId}">Zum ersten Arbeitsschritt <span aria-hidden="true">↓</span></a></div>
 <aside class="mp-outcome" aria-label="Ergebnis und Zeit"><p class="mp-kicker">${lessons[0].minutes} Minuten</p><h2>Dein Ergebnis</h2>${render(result.slice(outcomePrefix.length).trim().replace(/^eine /,'Eine '))}</aside></div></section>
 <article class="mp-article"><div class="mp-context">${render(context.join('\n\n'))}</div>${steps}</article>
 <nav class="mp-next" aria-label="Weiter im Lernbogen"><a class="mp-secondary" href="index.html">← Zur Medienübersicht</a><a class="mp-primary" href="${lessons[1].href}">Weiter zu ${lessons[1].code} · ${lessons[1].title} ${arrow}</a></nav>
 ${materialsLinks()}
 <script>
 const fizzPlayers = document.querySelectorAll('.mp-clip video');
 for (const player of fizzPlayers) {
   player.addEventListener('play', () => {
     for (const other of fizzPlayers) if (other !== player) other.pause();
   });
   const disclosure = player.closest('details');
   if (disclosure) disclosure.addEventListener('toggle', () => {
     if (!disclosure.open) player.pause();
   });
 }
 </script>`;
}

for(const f of files){
 const txt=fs.readFileSync(path.join(src,f),'utf8');
 const first=f===tasks[0];
 fs.writeFileSync(path.join(out,names[f.slice(0,-3)]),shell(titleOf(txt),first?firstLesson(txt):render(txt),first?'media-path':''));
}
fs.writeFileSync(path.join(out,'index.html'),shell('Was zeigen wir – und was lassen wir weg?',mediaHome(),'media-path'));
const layoutSheet=path.join(repo,'prototypes/klasse7-medien/inhalt/lernweg.css');
if(path.resolve(out,'lernweg.css')!==path.resolve(layoutSheet))fs.copyFileSync(layoutSheet,path.join(out,'lernweg.css'));
const projectionText=fs.readFileSync(path.join(src,'Medienbogen - Projektion.md'),'utf8');
const parts=[...projectionText.matchAll(/^## (P\d[^\n]*)\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)];
for(let i=0;i<parts.length;i++) fs.writeFileSync(path.join(out,`projektion-${i+1}.html`),shell(parts[i][1],`<div class="project-nav"><a href="${target('Medienbogen - Projektion')}">Impulse</a>${i?`<a href="projektion-${i}.html">Zurück</a>`:''}${i+1<parts.length?`<a href="projektion-${i+2}.html">Weiter</a>`:''}</div>`+render('# '+parts[i][1]+'\n'+parts[i][2]),'projection'));
let overview=path.join(out,target('Medienbogen - Projektion'));fs.writeFileSync(overview,fs.readFileSync(overview,'utf8').replace('<main id="inhalt">',`<main id="inhalt"><p>${parts.map((_,i)=>`<a href="projektion-${i+1}.html">Großansicht P${i+1}</a>`).join(' · ')}</p>`));
for(const f of ['ium-lernwerk-7.svg','favicon.svg'])fs.copyFileSync(path.join(brand,f),path.join(out,'material',f));
const fizzOut=path.join(out,'material','fizz');
fs.mkdirSync(fizzOut,{recursive:true});
for(const clip of fizzClips){
 for(const [source,suffix] of [[clip.video,'.mp4'],[clip.captions,'.de.vtt'],[clip.poster,'.jpg']]){
  const from=path.join(root,fizzFolder,source), to=path.join(fizzOut,clip.id+suffix);
  if(suffix==='.de.vtt') fs.writeFileSync(to,fs.readFileSync(from,'utf8').replace(/\r\n/g,'\n'));
  else fs.copyFileSync(from,to);
 }
}
const hof=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720"><title>Ein Hof mit verschiedenen Ecken</title><desc>Eigene schematische Illustration. Links grüne Bäume und Bank, rechts grauer Papierkorb und drei Papierstücke, hinten Schule und Spielfeld. Keine Personen.</desc><rect width="1200" height="720" fill="#dcecf0"/><rect y="310" width="1200" height="410" fill="#d6d2c7"/><path d="M0 530L1200 420M0 650L1200 540M220 310L350 720M580 310L700 720M930 310L1080 720" stroke="#c0bdaf" stroke-width="3"/><rect x="470" y="100" width="630" height="245" rx="4" fill="#e7bb7d"/><path d="M440 100L780 28L1130 100" fill="#687f89"/><g fill="#648c99" stroke="#fff" stroke-width="8"><rect x="510" y="145" width="100" height="85"/><rect x="650" y="145" width="100" height="85"/><rect x="790" y="145" width="100" height="85"/><rect x="930" y="145" width="100" height="85"/></g><rect x="750" y="260" width="70" height="85" fill="#556e76"/><path d="M450 390H790L860 485H390Z" fill="#86adac" stroke="#fff" stroke-width="5"/><path d="M620 390L630 485" stroke="#fff" stroke-width="4"/><ellipse cx="213" cy="585" rx="200" ry="90" fill="#a3bd74"/><rect x="155" y="225" width="40" height="260" rx="8" fill="#8b6545"/><g fill="#5d995d"><circle cx="170" cy="185" r="115"/><circle cx="85" cy="230" r="75"/><circle cx="250" cy="232" r="85"/></g><g fill="#ca8c4e" stroke="#6e563d" stroke-width="8"><path d="M75 470H345V495H75Z"/><path d="M85 420H335V448H85Z"/><path d="M105 495V550M315 495V550"/></g><g fill="#767f85" stroke="#4c555b" stroke-width="7"><path d="M950 435H1080L1068 575H962Z"/><rect x="942" y="420" width="146" height="24" rx="9"/></g><g stroke="#b4b2a8" stroke-width="3" fill="#faf9f0"><path d="M895 590L930 574L945 605L910 620Z"/><path d="M1040 630L1070 618L1090 645L1053 653Z"/><path d="M1130 565L1160 580L1142 606L1117 588Z"/></g><circle cx="400" cy="560" r="20" fill="#efad45"/><path d="M380 560H420M400 540V580" stroke="#965d2b" stroke-width="3"/></svg>`;
fs.writeFileSync(path.join(out,'material/hof-original.svg'),hof);
await sharp(Buffer.from(hof)).png().toFile(path.join(out,'material/hof-original.png'));
function person(x,y,scale,color,name){return `<g transform="translate(${x} ${y}) scale(${scale})"><circle cx="0" cy="0" r="27" fill="#d6ad88"/><path d="M-35 40Q0 14 35 40L30 133H-30Z" fill="${color}"/><path d="M-20 130L-24 194M20 130L24 194" stroke="#394b55" stroke-width="17"/><text x="0" y="230" text-anchor="middle" font-size="26" fill="#222a2f">${name}</text></g>`;}
function card(second){return `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620" font-family="Segoe UI,Arial,sans-serif"><title>${second?'R2 Rollen wechseln':'R1 Ein starkes Team'}</title><rect width="1000" height="620" rx="18" fill="${second?'#eaf2ec':'#f5e8dc'}"/><text x="45" y="55" font-size="22" fill="#5b656d">${second?'R2':'R1'} · KONSTRUIERTE WERBEKARTE · ROBOTIK-AG</text><text x="45" y="108" font-size="42" fill="#222a2f" font-weight="700">${second?'Rollen wechseln – alle probieren aus.':'Ein starkes Team.'}</text>${second?person(200,220,.95,'#996a45','Mina')+person(780,220,.95,'#486c86','Leo'):person(260,175,1.15,'#486c86','Leo')+person(800,280,.72,'#996a45','Mina')}<g transform="translate(430 290)"><rect width="145" height="100" rx="12" fill="#a9b4b6" stroke="#394b55" stroke-width="6"/><circle cx="38" cy="115" r="22" fill="#394b55"/><circle cx="110" cy="115" r="22" fill="#394b55"/><circle cx="45" cy="35" r="12" fill="#fff"/><circle cx="100" cy="35" r="12" fill="#fff"/></g>${second?'<path d="M300 260Q500 140 700 260M700 420Q500 490 300 420" fill="none" stroke="#245743" stroke-width="6"/><path d="M680 240L700 260L668 260M322 418L300 420L312 442" fill="none" stroke="#245743" stroke-width="6"/><text x="500" y="175" text-anchor="middle" font-size="26" fill="#222a2f">Steuern · Bauen · Fotografieren</text>':'<rect x="310" y="342" width="110" height="70" rx="8" fill="#394b55"/><circle cx="340" cy="362" r="10" fill="#e6c56b"/><path d="M370 390V353" stroke="#fff" stroke-width="6"/><rect x="720" y="340" width="60" height="42" rx="5" fill="#394b55"/><circle cx="750" cy="361" r="12" fill="#afcbd1"/><text x="47" y="485" font-size="28" fill="#222a2f">Jungs steuern. Mädchen sehen gut aus.</text>'}<text x="45" y="537" font-size="${second?24:29}" fill="#222a2f">${second?'Du musst für eine Aufgabe nicht auf eine bestimmte Weise aussehen.':'Für dein Teamfoto: immer makellos.'}</text><text x="45" y="585" font-size="18" fill="#5b656d">${second?'Auch dieses Werbebild zeigt nur einen ausgewählten Ausschnitt.':'Leo steuert. Mina macht das Teamfoto. Darstellung mit Glättungsfilter gestaltet.'}</text></svg>`;}
for(const [f,b]of[['rollen-A.svg',false],['rollen-B.svg',true]])fs.writeFileSync(path.join(out,'material',f),card(b));
fs.writeFileSync(path.join(out,'fassung.json'),JSON.stringify({fassung:'1.1',datum:'2026-11-03',minuten:270,aufgaben:minutes,phasen:[[10,10,15,10],[10,10,15,10],[15,15,45,15],[10,10,15,10],[10,10,15,10]],quellen:files,html:files.length+1+parts.length},null,2));
console.log(JSON.stringify({out,quellen:files.length,html:files.length+1+parts.length,projektionen:parts.length,minuten:270}));

