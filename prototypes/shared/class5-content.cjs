'use strict';
const fs=require('node:fs'),path=require('node:path'),{functions}=require('./class5-catalog.cjs');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text=(v,name)=>{if(typeof v!=='string'||!v.trim())throw new Error('Inhalt fehlt: '+name);return v;};
const id=v=>typeof v==='string'&&/^[a-z][a-z0-9-]{1,60}$/.test(v);
function validate(pack){
 if(!id(pack.area)||!/^IUM-5-[A-Z0-9-]+$/.test(pack.id)||!/^\d+\.\d+\.\d+$/.test(pack.version)||pack.grade!==5||pack.family!=='content'||!Array.isArray(pack.steps)||!pack.steps.length)throw new Error('Ungültiger Klasse-5-Inhalt');
 for(const key of ['title','topic','description','product'])text(pack[key],key);
 if(!Array.isArray(pack.prerequisites)||!Array.isArray(pack.teacher)||!pack.teacher.length)throw new Error('Voraussetzungen/Lehrpersonenhinweise fehlen');
 const names=new Set();for(const step of pack.steps){
  if(!id(step.id)||names.has(step.id))throw new Error('Schritt-ID ist ungültig/doppelt');names.add(step.id);text(step.title,'Schritt');text(step.goal,'Ziel');
  if(!Array.isArray(step.criteria)||!step.criteria.length||!Array.isArray(step.blocks)||!step.blocks.length)throw new Error('Schritt ohne Kriterien oder Inhalt');
  const fields=new Set();for(const b of step.blocks){
   if(!['explanation','example','task','external','cooperative','private','retrieval'].includes(b.type))throw new Error('Unbekannter Inhaltsbaustein: '+b.type);
   text(b.title,'Bausteintitel');text(b.text,'Bausteintext');
   if(['task','external','cooperative','private','retrieval'].includes(b.type)){if(!id(b.id)||fields.has(b.id))throw new Error('Antwort-ID ungültig/doppelt');fields.add(b.id);text(b.prompt,'Eigenes Produkt');}
   if(b.type==='external'){for(const k of ['preparation','action','return'])text(b[k],k);const u=new URL(b.url);if(u.protocol!=='https:')throw new Error('Externer Zugang muss HTTPS verwenden');}
   if(b.type==='cooperative')for(const k of ['contribution','exchange','return'])text(b[k],k);
   if(b.type==='retrieval'){text(b.when,'Zeitpunkt');text(b.solution,'Vergleich nach Abruf');}
  }
 }
 for(const f of functions)if(!Array.isArray(pack.coverage?.[f])||!pack.coverage[f].length||pack.coverage[f].some(s=>!names.has(s)))throw new Error('Lernbogenfunktion fehlt: '+f);
 return pack;
}
function renderBlocks(step){
 let privateUsed=false;
 const html=step.blocks.map(b=>{
  let extra='';
  if(b.type==='external')extra='<h3>Vorbereiten</h3><p>'+esc(b.preparation)+'</p><h3>Im anderen Werkzeug arbeiten</h3><p>'+esc(b.action)+'</p><p><a href="'+esc(b.url)+'" target="_blank" rel="noopener noreferrer">Werkzeug öffnen · neuer Tab, Internet nötig</a></p><h3>Zurück im Lernwerk</h3><p>'+esc(b.return)+'</p>';
  if(b.type==='cooperative')extra='<h3>Dein Beitrag</h3><p>'+esc(b.contribution)+'</p><h3>Gemeinsam austauschen</h3><p>'+esc(b.exchange)+'</p><h3>Danach wieder selbst</h3><p>'+esc(b.return)+'</p>';
  if(b.type==='retrieval')extra='<p><b>Später wieder aufgreifen:</b> '+esc(b.when)+'</p>';
  const field=['task','external','cooperative','private','retrieval'].includes(b.type);
  if(b.type==='private')privateUsed=true;
  return '<section class="lw-notice"'+(b.type==='private'?' data-private':'')+'><h2>'+esc(b.title)+'</h2><p>'+esc(b.text)+'</p>'+extra+(field?'<label for="'+(b.type==='private'?'private-':'answer-')+step.id+'-'+b.id+'">'+esc(b.prompt)+'</label><textarea id="'+(b.type==='private'?'private-':'answer-')+step.id+'-'+b.id+'" maxlength="10000"></textarea>':'')+(b.type==='private'?'<p>Bleibt hier persönlich. Wird nicht in „Deine Arbeit“, Arbeitsdateien oder Druckausgaben übernommen. Bei einem Seitenwechsel kann diese Notiz verloren gehen.</p><button class="lw-button secondary" data-private-export="private-'+step.id+'-'+b.id+'">Nur diese private Notiz gesondert sichern</button>':'')+(b.solution?'<details><summary>'+(b.type==='retrieval'?'Jetzt vergleichen':'Mögliche Lösung nachvollziehen')+'</summary><p>'+esc(b.solution)+'</p></details>':'')+'</section>';
 }).join('');
 return html+(privateUsed?'<dialog id="lw-private-dialog" aria-labelledby="lw-private-title"><h2 id="lw-private-title">Nur deine private Notiz</h2><p>Diese Datei enthält die folgende persönliche Notiz. Andere Personen mit Zugriff auf die Datei können sie lesen.</p><pre id="lw-private-preview" class="lw-product"></pre><button id="lw-private-confirm" class="lw-button">Diese Notiz als eigene Textdatei anbieten</button><button id="lw-private-cancel" class="lw-button secondary">Abbrechen</button></dialog>':'');
}
function load(){
 const dir=path.join(__dirname,'inhalte');if(!fs.existsSync(dir))return [];
 return fs.readdirSync(dir).filter(n=>n.endsWith('.json')).sort().map(n=>validate(JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'))));
}
function unit(pack){return {...pack,kind:pack.kind||'core',status:'working',schemaVersion:1,learningDesign:{goal:pack.product,coverage:Object.fromEntries(Object.entries(pack.coverage).map(([k,v])=>[k,v.join('/')]))},fields:pack.steps.flatMap(s=>s.blocks.filter(b=>['task','external','cooperative','retrieval'].includes(b.type)).map(b=>'i:answer-'+s.id+'-'+b.id))};}
module.exports={validate,renderBlocks,load,unit,esc};
