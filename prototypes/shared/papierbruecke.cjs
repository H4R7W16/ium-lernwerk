'use strict';
const fs=require('node:fs'),path=require('node:path');
const PREFIX='assets/medienwirkung/papierbruecke/';
const active=pack=>pack.grade===5&&pack.area==='medienwirkung'&&!!pack.paperbridge;
const e=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function validate(pack){
 if(!pack.paperbridge)return false;
 if(!active(pack))throw new Error('Papierbrücken-Bundle nur im vorgesehenen Klasse-5-Fall');
 const b=pack.paperbridge;
 if(!Array.isArray(b.files)||new Set(b.files).size!==b.files.length||!b.files.length)throw new Error('Papierbrücken-Dateiliste ungültig');
 for(const name of b.files)if(!/^[a-z0-9/-]+\.(html|css|js|png|webp|jpg|jpeg|woff2|txt|json)$/.test(name)||name.includes('..')||name.includes('//')||name.startsWith('/'))throw new Error('Papierbrücken-Pfad ungültig: '+name);
 for(const name of ['index.html','alle.html','texte.html'])if(!b.files.includes(name))throw new Error('Papierbrücken-Zugang fehlt: '+name);
 if(!Array.isArray(b.cards)||b.cards.length!==4||new Set(b.cards.map(c=>c.file)).size!==4)throw new Error('Papierbrücke braucht vier verschiedene Karten');
 for(const card of b.cards)if(!b.files.includes(card.file)||!/\.(png|webp|jpg|jpeg)$/.test(card.file)||typeof card.alt!=='string'||!card.alt.trim())throw new Error('Papierbrücken-Karte oder Alternativtext fehlt');
 return true;
}
function assets(pack){
 const out=new Map();if(!validate(pack))return out;
 const base=fs.realpathSync(path.join(__dirname,'inhalte')),root=fs.realpathSync(path.join(base,PREFIX));
 if(!root.startsWith(base+path.sep))throw new Error('Papierbrücken-Bundle außerhalb des Inhaltsordners');
 for(const name of pack.paperbridge.files){
  const file=fs.realpathSync(path.join(root,name));
  if(!file.startsWith(root+path.sep))throw new Error('Papierbrücken-Datei außerhalb des Bundles');
  const data=fs.readFileSync(file);
  if(!data.length||data.length>2*1024*1024)throw new Error('Papierbrücken-Dateigröße unzulässig: '+name);
  out.set(PREFIX+name,/\.(html|css|js|txt|json)$/.test(name)?data.toString('utf8'):data);
 }
 out.set('assets/medienwirkung/video.svg',fs.readFileSync(path.join(base,'assets/medienwirkung/video.svg')));
 return out;
}
function links(){
 return '<nav class="lw-reading-links no-print" aria-label="Jules’ Bilderbeitrag"><a href="'+PREFIX+'index.html?lernwerk=1">Jules’ Bilderbeitrag öffnen →</a><a href="'+PREFIX+'alle.html?lernwerk=1">Alle vier Bilder zusammen ansehen</a><a href="'+PREFIX+'texte.html?lernwerk=1">Den Beitrag als Text lesen</a></nav>';
}
function integrate(pack,pages){
 if(!validate(pack))return pages;
 const A=require('./class5-content.cjs'),out=new Map(pages);
 const poster=A.mediaHTML(['video'],pack);
 const media=pack.media.find(m=>m.id==='video');
 const intro='<div id="jules-beitrag"><a class="lw-papierbruecke-poster" href="'+PREFIX+'index.html?lernwerk=1" aria-label="Jules’ Bilderbeitrag: vier Bilder öffnen"><img src="'+e(media.file)+'" alt="'+e(media.alt)+'" style="display:block;width:100%;max-width:420px;height:auto;border-radius:12px"></a>'+links()+'<p class="lw-small">'+e(media.caption)+'</p></div>';
 const cards='<div id="jules-beitrag" class="lw-papierbruecke-print">'+pack.paperbridge.cards.map((card,i)=>'<figure class="lw-content-figure" style="break-inside:avoid;page-break-inside:avoid"><h3>B · Bild '+(i+1)+' von 4</h3><img src="'+PREFIX+e(card.file)+'" alt="'+e(card.alt)+'" style="max-width:420px;height:auto"><figcaption>'+e(media.creator)+' · '+e(media.license)+'</figcaption></figure>').join('')+'</div>'+links();
 for(const [file,replacement]of [['schritt-werbung.html',intro],['baustein-werbung.html',cards]]){
  const html=out.get(file);if(!html?.includes(poster))throw new Error('Papierbrücken-Einfügestelle fehlt: '+file);
  out.set(file,html.replace(poster,replacement));
 }
 const link='<p><a href="schritt-werbung.html#jules-beitrag">Zum Werbevergleich mit Jules’ Bilderbeitrag →</a></p>';
 for(const file of ['briefing.html','lehrkraft.html'])out.set(file,out.get(file).replace('</h1>','</h1>'+link));
 const viewer=out.get('bild-video.html');
 if(viewer)out.set('bild-video.html',viewer.replace('</h1>','</h1>'+links()));
 return out;
}
module.exports={active,validate,assets,integrate};
