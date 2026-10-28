'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const units=[['medien','Medien'],['daten','Daten'],['programmieren','Programmieren'],['gaming','Gaming']];
const relative=(name,to)=>path.posix.relative(path.posix.dirname(name),to);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function addYearRoutes(source){
 const all=new Map(source),manifest=require('./quelle-sha256.json');
 for(const [file,hash]of Object.entries(manifest.files)){
  const bytes=fs.readFileSync(path.join(__dirname,file));if(sha(bytes)!==hash)throw Error('Ungebundene Jahresquelle: '+file);
  if(file.startsWith('inhalt/'))all.set('klasse7/'+file.slice(7),/\.(html|txt)$/.test(file)?bytes.toString('utf8'):bytes);
 }
 all.set('klasse7/jahreswege.css',fs.readFileSync(path.join(__dirname,'jahreswege.css'),'utf8'));
 for(const [name,original]of [...all]){
  if(!name.startsWith('klasse7/')||!name.endsWith('.html')||name.startsWith('klasse7/programmieren/snap/'))continue;
  const current=units.find(([id])=>name.startsWith('klasse7/'+id+'/'))?.[0];
  const oldHeader=original.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0];if(!oldHeader)continue;
  const ref=target=>relative(name,'klasse7/'+target);
  const links=oldHeader.match(/<nav[^>]*aria-label="Hauptnavigation"[^>]*>([\s\S]*?)<\/nav>/)?.[1]||'';
  const localLinks=[...links.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/g)].map(m=>m[0]).filter(a=>{
   const href=a.match(/href="([^"]+)"/)?.[1];if(!href)return false;
   const url=new URL(href,'https://example.test/ium-lernwerk/'+name);
   return !!url.hash||!units.some(([id])=>url.pathname==='/ium-lernwerk/klasse7/'+id+'/index.html');
  }).join('');
  const brand='<a class="brand" href="'+ref('index.html')+'" aria-label="IuM Lernwerk Klasse 7"><picture><source media="(max-width:700px)" srcset="'+ref('programmieren/brand/ium-lernwerk-7-compact.png')+'"><img src="'+ref('programmieren/brand/ium-lernwerk-7.png')+'" width="1308" height="320" alt="IuM Lernwerk 7 – Informatik und Medienbildung"></picture></a>';
  const nav=[['index.html','Jahrgang',!current],...units.map(([id,label])=>[id+'/index.html',label,id===current])].map(([url,label,active])=>'<a href="'+ref(url)+'"'+(active?' aria-current="'+(url==='index.html'&&name!=='klasse7/index.html'?'true':'page')+'"':'')+'>'+label+'</a>').join('');
  const header='<header class="year-header">'+brand+'<nav class="year-nav" aria-label="Hauptnavigation">'+nav+'</nav></header>';
  const tools='<nav class="year-tools" aria-label="Materialzugänge">'+localLinks+'<a href="'+ref('lehrpersonen.html')+'">Jahresplanung und Übergänge</a></nav>';
  let html=original.replace(oldHeader,header+tools).replace('</head>','<link rel="stylesheet" href="'+ref('jahreswege.css')+'"></head>').replace('Lehrmaterial auswählen','Material für Lehrpersonen');
  // Alten Direktlink erhalten, aber die überholte Jahrgangskopie durch den gemeinsamen Leitfaden ersetzen.
  if(name==='klasse7/programmieren/lehrpersonen/jahrgang.html'){
   html=html.replace(/<main\b[^>]*>[\s\S]*?<\/main>/,'<main id="main" class="year-legacy"><h1>Jahresplanung für IuM 7</h1><p>Die aktuelle gemeinsame Planung verbindet alle vier Lernbögen, die Eingangsdiagnose und die 90 Minuten spätere Wiederaufnahme.</p><p><a href="'+ref('lehrpersonen.html')+'">Jahresleitfaden mit Durchführung und Materialzugängen öffnen</a></p><p><a href="'+ref('lernziele.html')+'">29 Lernziele und Nachweise</a> · <a href="'+ref('briefing.html')+'">Jahrgangsbriefing</a></p></main>');
  }
  if(name==='klasse7/programmieren/index.html')html=html.replace('Aufgabenfassung 2.0 vom 25.10.2026','Aufgabenfassung 2.2 vom 27.10.2026');
  all.set(name,html);
 }
 return all;
}
module.exports={addYearRoutes,units};
