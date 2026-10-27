'use strict';
// Publikationsadapter: gemeinsame Reihenidentität, unveränderte Lern- und Snap-Quellen.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ROOT='klasse7/programmieren/',VERSION='20261027';
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
const relative=(name,file)=>path.posix.relative(path.posix.dirname(name),ROOT+file);
function brand(name){
 const ref=file=>relative(name,'brand/'+file);
 return '<a class="lw-shell-brand" href="'+relative(name,'index.html')+'" aria-label="IuM Lernwerk – Klasse 7 – Übersicht"><picture><source media="(max-width: 760px)" srcset="'+ref('ium-lernwerk-7-compact.png')+'" width="746" height="134"><img class="lw-brand-logo" src="'+ref('ium-lernwerk-7.png')+'" width="1308" height="320" alt="IuM Lernwerk 7 – Informatik und Medienbildung"></picture><span class="lw-brand-subject" aria-hidden="true">Informatik und Medienbildung</span></a>';
}
function enhance(name,html){
 const header=html.match(/<header class="(site-header|editor-header)">[\s\S]*?<\/header>/);
 if(!header)return html;
 const editor=header[1]==='editor-header';
 let nextHeader;
 if(editor){
  nextHeader=header[0].replace('class="editor-header"','class="editor-header lw-shell-header"').replace(/<a class="brand"[^>]*>[\s\S]*?<\/a>/,'<div class="lw-shell-identity">'+brand(name)+'</div>');
 }else{
  const links=header[0].match(/<nav class="header-links"[^>]*>([\s\S]*?)<\/nav>/);
  if(!links)throw Error('Fehlende Hauptnavigation: '+name);
  nextHeader='<header class="lw-shell-header"><div class="lw-shell-identity">'+brand(name)+'<span class="lw-shell-location"><b>Programmieren</b></span></div><nav class="lw-shell-nav" aria-label="Hauptnavigation">'+links[1]+'</nav></header>';
 }
 const styles=['mantel.css','identity.css','reihenlayout.css'].map(file=>'<link rel="stylesheet" href="'+relative(name,file)+'?v='+VERSION+'">').join('');
 const icon='<link rel="icon" href="'+relative(name,'brand/favicon.svg')+'" type="image/svg+xml">';
 const result=html.replace(/(<nav class="course-nav teacher-nav"[^>]*>[\s\S]*?<\/nav>)/, '<details class="teacher-menu"><summary>Lehrmaterial auswählen</summary>$1</details>');
 return result.replace(header[0],nextHeader).replace('<body>','<body class="lw-mantel lw-grade7'+(editor?' lw-grade7-editor':'')+'" data-lw-area="programmieren">').replace('</head>',styles+icon+'</head>');
}
function applySeriesLayout(source){
 const all=new Map(source);
 for(const [name,html]of source)if(name.startsWith(ROOT)&&name.endsWith('.html'))all.set(name,enhance(name,html));
 for(const file of ['mantel.css','identity.css']){
  const value=source.get('klasse5/'+file);
  if(typeof value!=='string')throw Error('Gemeinsame Reihenquelle fehlt: '+file);
  all.set(ROOT+file,value);
 }
 all.set(ROOT+'reihenlayout.css',fs.readFileSync(path.join(__dirname,'reihenlayout.css'),'utf8'));
 for(const file of fs.readdirSync(path.join(__dirname,'brand')))all.set(ROOT+'brand/'+file,fs.readFileSync(path.join(__dirname,'brand',file)));
 const name=ROOT+'snap/lernwerk-herkunft.json',manifest=JSON.parse(all.get(name));
 manifest.layout={version:'1.0.0',date:'2026-10-27',scope:'Gemeinsame IuM-Reihenidentität im Editor-Kopf; Programmierfläche und Laufzeit unverändert',sourceShellSha256:manifest.files['lernwerk.html'],assets:{}};
 for(const file of ['mantel.css','identity.css','reihenlayout.css','brand/ium-lernwerk-7.png','brand/ium-lernwerk-7-compact.png','brand/favicon.svg'])manifest.layout.assets['../'+file]=sha(all.get(ROOT+file));
 manifest.files['lernwerk.html']=sha(all.get(ROOT+'snap/lernwerk.html'));
 all.set(name,JSON.stringify(manifest,null,2)+'\n');
 return all;
}
module.exports={applySeriesLayout};
