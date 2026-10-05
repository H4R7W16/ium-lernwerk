'use strict';
const fs=require('node:fs'),path=require('node:path'),{functions}=require('./class5-catalog.cjs');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text=(v,name)=>{if(typeof v!=='string'||!v.trim())throw new Error('Inhalt fehlt: '+name);return v;};
const id=v=>typeof v==='string'&&/^[a-z][a-z0-9-]{1,60}$/.test(v);
const texts=(v,name)=>{if(!Array.isArray(v)||!v.length)throw new Error('Liste fehlt: '+name);v.forEach(x=>text(x,name));};
const https=v=>{if(new URL(v).protocol!=='https:')throw new Error('Quelle/Zugang muss HTTPS verwenden');};
function records(values,name){if(!Array.isArray(values))throw new Error('Liste fehlt: '+name);const ids=new Set();for(const v of values){if(!id(v.id)||ids.has(v.id))throw new Error('Ungültige/doppelte ID: '+name);ids.add(v.id);}return ids;}
function refs(values,ids,name){if(values===undefined)return;if(!Array.isArray(values)||values.some(v=>!ids.has(v)))throw new Error('Ungültiger Verweis: '+name);}
function validateEditorial(pack,steps){
 const sources=records(pack.sources,'Quellen'),media=records(pack.media,'Medien'),knowledge=records(pack.knowledge,'Wissen');
 const layout=m=>{if(m.mediaLayout===undefined)return;if(m.mediaLayout!=='comparison')throw new Error('Unbekannte Mediendarstellung');if(m.media?.length!==2||new Set(m.media).size!==2||m.media.some(id=>pack.media.find(x=>x.id===id)?.kind!=='image'))throw new Error('Bildvergleich braucht zwei verschiedene Bilder');};
 const aid=a=>{text(a.title,'Hilfetitel');text(a.text,'Hilfe');if(a.step)refs([a.step],steps,'Hilfeschritt');if(a.knowledge)refs([a.knowledge],knowledge,'Hilfewissen');if(a.step||a.knowledge)text(a.label,'Hilfelink');};
 if(pack.experiencedEntry){aid(pack.experiencedEntry);if(!pack.experiencedEntry.step)throw new Error('Einstiegsschritt fehlt');}
 if(!sources.size||!knowledge.size)throw new Error('Quellen/Wissen fehlen');
 text(pack.duration,'Zeitannahme');text(pack.curriculum?.moduleId,'Planungsmodul');texts(pack.curriculum?.goalIds,'Lernziele');text(pack.curriculum.scope,'Abdeckungsgrenze');refs([pack.curriculum.source],sources,'Curriculum');
 for(const s of pack.sources){for(const k of ['title','author','license','checked'])text(s[k],'Quelle '+k);https(s.url);}
 for(const m of pack.media){
  for(const k of ['title','creator','license'])text(m[k],'Medium '+k);
  if(!['image','download'].includes(m.kind)||typeof m.file!=='string'||!/^assets\/[a-z0-9/-]+\.(svg|png|jpg|jpeg|webp|txt)$/.test(m.file)||m.file.includes('..')||m.file.includes('//'))throw new Error('Unzulässiger Medienpfad/Typ');
  if(m.kind==='image'){if(!/\.(svg|png|jpg|jpeg|webp)$/.test(m.file))throw new Error('Bildformat ungültig');text(m.alt,'Alternativtext');text(m.caption,'Bildunterschrift');}
  else{if(!m.file.endsWith('.txt'))throw new Error('Unbekanntes Downloadformat');text(m.printText,'Druckinhalt der Datei');}
  if(m.downloadable!==undefined&&(m.kind!=='image'||typeof m.downloadable!=='boolean'))throw new Error('Bilddownload ungültig');
  refs([m.sourceId],sources,'Medienquelle');
 }
 for(const k of pack.knowledge){layout(k);text(k.title,'Wissensfrage');texts(k.paragraphs,'Wissen');text(k.example,'Beispiel');text(k.boundary,'Aussagegrenze');if(!k.steps?.length)throw new Error('Wissensbezug fehlt');refs(k.steps,steps,'Wissensschritt');refs(k.media,media,'Wissensmedium');refs(k.sources,sources,'Wissensquelle');}
 for(const s of pack.steps){
  if(s.layout!==undefined&&(s.layout!=='model-task'||s.blocks.length!==2||s.blocks[0].type!=='example'||s.blocks[1].type!=='task'))throw new Error('Modell-Aufgaben-Paar ungültig');
  if(s.materialNeeds)texts(s.materialNeeds,'Materialbedarf');
  if(s.deviceNeeds)for(const [device,needs]of Object.entries(s.deviceNeeds)){if(!['ipad','windows'].includes(device))throw new Error('Gerät ungültig');texts(needs,'Gerätebedarf');}
  if(s.checkHelp){if(!Array.isArray(s.checkHelp)||!s.checkHelp.length)throw new Error('Prüfhilfe fehlt');s.checkHelp.forEach(aid);}
  if(s.prerequisites)texts(s.prerequisites,'Schrittvoraussetzungen');if(s.timing!==undefined&&!['now','later'].includes(s.timing))throw new Error('Ungültiger Zeitpunkt');if(s.completion){text(s.completion.title,'Abschlusstitel');text(s.completion.text,'Abschluss');}text(s.task,'Auftrag');text(s.outcome,'Ergebnis');if(!s.knowledge?.length)throw new Error('Wissensbezug fehlt');refs(s.knowledge,knowledge,'Schrittwissen');texts(s.criteria,'Kriterien');
  for(const b of s.blocks){
   if(b.network!==undefined&&(b.network!==true||pack.toolKind!=='network'||pack.grade!==6))throw new Error('Netzmodell ungültig');
   layout(b);refs(b.media,media,'Material');refs(b.sources,sources,'Blockquelle');
   if(b.links){if(!Array.isArray(b.links)||!b.links.length)throw new Error('Verweise fehlen');for(const l of b.links){text(l.label,'Verweistext');if(typeof l.href!=='string'||! /^(?:\.\.\/[a-z0-9-]+\/|\.\.\/)?[a-z0-9-]+\.html(?:#[a-z0-9-]+)?$/.test(l.href))throw new Error('Verweis ungültig');}}
   if(b.deviceFollowup){if(b.type!=='external'||b.context!=='device')throw new Error('Geräteprobe nur am Geräteauftrag');text(b.deviceFollowup.title,'Prüfanleitung');text(b.deviceFollowup.text,'Prüfanleitung');texts(b.deviceFollowup.items,'Prüfschritte');texts(b.deviceFollowup.paragraphs,'Prüfgrenze');}
   if(b.responseTable){texts(b.responseTable.headers,'Antworttabelle');if(!Array.isArray(b.responseTable.rows)||!b.responseTable.rows.length)throw new Error('Antworttabelle fehlt');for(const row of b.responseTable.rows){texts(row,'Antwortzeile');if(row.length!==b.responseTable.headers.length)throw new Error('Antwortspalten passen nicht');}}
   if(b.responseHint)text(b.responseHint,'Antwortumfang');if(b.responseMode!==undefined&&!['written','oral'].includes(b.responseMode))throw new Error('Ungültige Antwortform');if(b.storageNotice)text(b.storageNotice,'Speicherhinweis');
   if(b.paragraphs)texts(b.paragraphs,'Absätze');if(b.items)texts(b.items,'Liste');
   if(b.table){texts(b.table.headers,'Tabellenkopf');if(!Array.isArray(b.table.rows)||!b.table.rows.length)throw new Error('Tabelle fehlt');for(const row of b.table.rows){texts(row,'Tabellenzeile');if(row.length!==b.table.headers.length)throw new Error('Tabellenspalten passen nicht');}}
   if(b.help)b.help.forEach(aid);
   if(b.routes)for(const r of b.routes){text(r.title,'Geräteweg');if(r.device!==undefined&&!['ipad','windows'].includes(r.device))throw new Error('Gerät ungültig');if(!Array.isArray(r.items)||!r.items.length)throw new Error('Bedienung fehlt');for(const item of r.items){if(typeof item==='string')text(item,'Bedienung');else{if(!item||typeof item!=='object')throw new Error('Bedienung ungültig');text(item.title,'Bedienschritt');text(item.text,'Bedienung');refs(item.media,media,'Gerätemedium');}}refs(r.sources,sources,'Gerätequelle');}
  }
 }
 if(pack.teacherSections)for(const section of pack.teacherSections){text(section.title,'Lehrhinweis');texts(section.paragraphs,'Lehrhinweis');}
 if(pack.briefing)texts(pack.briefing,'Lehrpersonenbriefing');
 refs(pack.preview?[pack.preview]:[],media,'Themenvorschau');
}
function validate(pack){
 if(pack.authorVersion!==undefined&&pack.authorVersion!==2)throw new Error('Unbekannte Autorenversion');
 if(!id(pack.area)||!new RegExp('^IUM-'+pack.grade+'-[A-Z0-9-]+$').test(pack.id)||!/^\d+\.\d+\.\d+$/.test(pack.version)||![5,6].includes(pack.grade)||pack.family!=='content'||!Array.isArray(pack.steps)||!pack.steps.length)throw new Error('Ungültiger Jahrgangsinhalt');
 for(const key of ['title','topic','description','product'])text(pack[key],key);
 if(!Array.isArray(pack.prerequisites)||!Array.isArray(pack.teacher)||!pack.teacher.length)throw new Error('Voraussetzungen/Lehrpersonenhinweise fehlen');
 const names=new Set();for(const step of pack.steps){
  if(!id(step.id)||names.has(step.id))throw new Error('Schritt-ID ist ungültig/doppelt');names.add(step.id);text(step.title,'Schritt');text(step.goal,'Ziel');
  if(!Array.isArray(step.criteria)||!step.criteria.length||!Array.isArray(step.blocks)||!step.blocks.length)throw new Error('Schritt ohne Kriterien oder Inhalt');
  const fields=new Set();for(const b of step.blocks){
   if(!['explanation','example','task','external','cooperative','private','retrieval'].includes(b.type))throw new Error('Unbekannter Inhaltsbaustein: '+b.type);
   text(b.title,'Bausteintitel');text(b.text,'Bausteintext');
   if(['task','external','cooperative','private','retrieval'].includes(b.type)){if(!id(b.id)||fields.has(b.id))throw new Error('Antwort-ID ungültig/doppelt');fields.add(b.id);text(b.prompt,'Eigenes Produkt');}
   if(b.type==='external'){for(const k of ['preparation','action','return'])text(b[k],k);if(b.context==='device'){if(pack.authorVersion!==2||!b.routes?.length)throw new Error('Geräteweg fehlt');}else https(b.url);}
   if(b.type==='cooperative')for(const k of ['contribution','exchange','return'])text(b[k],k);
   if(b.type==='retrieval'){text(b.when,'Zeitpunkt');text(b.solution,'Vergleich nach Abruf');}
  }
 }
 for(const f of functions)if(!Array.isArray(pack.coverage?.[f])||!pack.coverage[f].length||pack.coverage[f].some(s=>!names.has(s)))throw new Error('Lernbogenfunktion fehlt: '+f);
 if(pack.authorVersion===2)validateEditorial(pack,names);
 return pack;
}
const paragraphs=values=>(values||[]).map(v=>'<p>'+esc(v)+'</p>').join('');
function citations(ids,pack){return (ids||[]).length?'<p class="lw-citation">Grundlage: '+ids.map(id=>{const s=pack.sources.find(s=>s.id===id);return '<a href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer">'+esc(s.title)+'</a><span class="lw-print-url">'+esc(s.url)+'</span>';}).join(' · ')+'</p>':'';}
function mediaHTML(ids,pack,layout){
 const comparison=layout==='comparison';
 const html= (ids||[]).map(id=>{const m=pack.media.find(m=>m.id===id);
  const credit='<small>'+esc(m.creator)+' · '+esc(m.license)+'</small>';
  return m.kind==='image'?'<figure class="lw-content-figure">'+(comparison?'<h3 class="lw-media-title">'+esc(m.title)+'</h3>':'')+'<img src="'+esc(m.file)+'" alt="'+esc(m.alt)+'"><figcaption>'+esc(m.caption)+' '+credit+'</figcaption>'+(m.downloadable?'<p class="no-print"><a class="lw-button secondary" href="'+esc(m.file)+'" download>'+esc(m.title)+' herunterladen</a></p>':'')+'</figure>':'<div class="lw-download"><a class="lw-button secondary" href="'+esc(m.file)+'" download>'+esc(m.title)+' herunterladen</a><p class="lw-small">Textdatei · '+credit+'</p><div class="lw-print-file"><h3>'+esc(m.title)+' · Dateiinhalt</h3><pre>'+esc(m.printText)+'</pre></div></div>';
 }).join('');
 return comparison?'<div class="lw-media-comparison" role="group" aria-label="Bildvergleich">'+html+'</div>':html;
}
function actionLink(h){return h.step?'<a href="schritt-'+esc(h.step)+'.html">'+esc(h.label)+' →</a>':h.knowledge?'<a href="wissen.html#'+esc(h.knowledge)+'">'+esc(h.label)+' →</a>':'';}
function renderBlocks(step,pack={},options={}){
 let privateUsed=false;
 const html=step.blocks.filter(b=>!options.paper||b.type!=='private').map(original=>{
  let b=original;
  if(options.paper&&pack.area==='ablaeufe'&&b.id==='code')b={...b,text:(step.id==='entwurf'?'Schreibe deinen eigenen Code für vier Karten auf.':'Schreibe wiederhole 3 [nimm markiere lege] auf.')+' Verfolge jeden Befehl mit Papierkarten. Halte nach jedem Schritt Vorrat, Platz und Ausgabe im Protokoll fest. Die digitale Eingabe und Ausführung im Interpreter holst du später im Lernwerk nach.',responseHint:'Papierweg: Code aufschreiben und mit Karten ausführen. Die praktische Programmierung bleibt noch offen.'};
  if(options.paper&&pack.area==='ablaeufe'&&b.id==='bedienung')b={...b,text:'Für die spätere Arbeit am Gerät: Öffne den Lernschritt Vorhersagen. Ausführen. Erklären. über den Link unten. Dort steht die Kartenstation direkt beim Codefeld. Die folgenden Gerätewege erklären diese Bildschirmfassung.'};
  if(options.paper&&pack.area==='ablaeufe'&&b.id==='spur')b={...b,text:'Schreibe die ausgeführte Folge und nach jedem Befehl Vorrat, Platz und Ausgabe auf. Bewahre den ersten Versuch auf. Ergänze in eigenen Worten, warum die Zustandsänderungen zu deinem Code passen und wo sie von der Vorhersage abweichen.'};
  let extra='';
  if(b.type==='external')extra='<div class="lw-device-task"><h3>Vorbereiten</h3><p>'+esc(b.preparation)+'</p><h3>'+(b.context==='device'?'Jetzt am Gerät':'Im anderen Werkzeug arbeiten')+'</h3><p>'+esc(b.action)+'</p>'+(b.context==='device'?'':'<p><a href="'+esc(b.url)+'" target="_blank" rel="noopener noreferrer">Werkzeug öffnen · neuer Tab, Internet nötig</a><span class="lw-print-url">'+esc(b.url)+'</span></p>')+'<h3>Zurück im Lernwerk</h3><p>'+esc(b.return)+'</p></div>';
  if(b.type==='cooperative')extra='<h3>Dein Beitrag</h3><p>'+esc(b.contribution)+'</p><h3>Gemeinsam austauschen</h3><p>'+esc(b.exchange)+'</p><h3>Danach wieder selbst</h3><p>'+esc(b.return)+'</p>';
  if(b.type==='retrieval')extra='<p><b>Später wieder aufgreifen:</b> '+esc(b.when)+'</p>';
  const field=['task','external','cooperative','private','retrieval'].includes(b.type),fieldId=(b.type==='private'?'private-':'answer-')+step.id+'-'+b.id;
  if(b.type==='private')privateUsed=true;
  const routes=(b.routes||[]).filter(r=>!options.device||!r.device||r.device===options.device).map(r=>'<details class="lw-device-route"'+(options.paper?' open':'')+'><summary>'+esc(r.title)+'</summary><ol class="lw-device-steps">'+r.items.map(t=>typeof t==='string'?'<li>'+esc(t)+'</li>':'<li><h4>'+esc(t.title)+'</h4><p>'+esc(t.text)+'</p>'+mediaHTML(t.media,pack)+'</li>').join('')+'</ol>'+citations(r.sources,pack)+'</details>').join('');
  if(b.type==='external'&&b.context==='device')extra='<div class="lw-start-place"><h3>Dein Startort</h3><p>'+esc(b.preparation)+'</p></div><p>'+esc(b.action)+'</p><div class="lw-device-routes">'+routes+'</div><p><b>Zurück im Lernwerk:</b> '+esc(b.return)+'</p>';
  if(b.deviceFollowup)extra=extra.replace('<p><b>Zurück im Lernwerk:</b>', '<aside class="lw-device-followup"><h3>'+esc(b.deviceFollowup.title)+'</h3><p>'+esc(b.deviceFollowup.text)+'</p><ol>'+b.deviceFollowup.items.map(t=>'<li>'+esc(t)+'</li>').join('')+'</ol>'+paragraphs(b.deviceFollowup.paragraphs)+'</aside><p><b>Zurück im Lernwerk:</b>');
  if(b.responseTable)extra+='<div class="lw-table-wrap"><table><caption>Dein Vergleich – Gerüst für Stichwörter oder deine Erklärung</caption><thead><tr>'+b.responseTable.headers.map(t=>'<th scope="col">'+esc(t)+'</th>').join('')+'</tr></thead><tbody>'+b.responseTable.rows.map(row=>'<tr>'+row.map((t,i)=>i?'<td>'+esc(t)+'</td>':'<th scope="row">'+esc(t)+'</th>').join('')+'</tr>').join('')+'</tbody></table></div>';
  const hint=b.responseHint?'<p class="lw-response-hint" id="'+fieldId+'-hint">'+esc(b.responseHint)+'</p>':'';
  let input='<label for="'+fieldId+'">'+esc(b.prompt)+'</label><textarea id="'+fieldId+'" aria-label="'+esc(b.prompt)+'"'+(b.responseHint?' aria-describedby="'+fieldId+'-hint"':'')+' rows="2" maxlength="10000"></textarea>';
  if(!options.paper&&pack.area==='ablaeufe'&&b.id==='code')input=require('../m06-kartenstation/render.cjs').enhance(input,step.id);
  const answer=!field?'':options.paper?hint+'<p><b>'+esc(b.prompt)+'</b></p>'+(b.responseMode==='oral'?'':'<div class="lw-answer-space" aria-label="Platz für deine Antwort"></div>'):hint+(b.responseMode==='oral'?'<p><b>'+esc(b.prompt)+'</b></p><details class="lw-optional-answer"><summary>Wenn du möchtest: hier notieren</summary>'+input+'</details>':input);
  const help=(b.help||[]).map(h=>'<details class="lw-help"><summary>'+esc(h.title)+'</summary><p>'+esc(h.text)+'</p>'+actionLink(h)+'</details>').join('');
  const links=b.links?'<nav class="lw-reading-links" aria-label="Material und Arbeitsweg">'+b.links.map(l=>'<a href="'+esc(l.href)+'">'+esc(l.label)+' →</a>').join('')+'</nav>':'';
  const table=b.table?'<div class="lw-table-wrap"><table><thead><tr>'+b.table.headers.map(v=>'<th scope="col">'+esc(v)+'</th>').join('')+'</tr></thead><tbody>'+b.table.rows.map(row=>'<tr>'+row.map(v=>'<td>'+esc(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>':'';
  return '<section class="lw-content-block lw-block-'+b.type+'"'+(b.type==='private'?' data-private':'')+'><h2>'+esc(b.title)+'</h2><p>'+esc(b.text)+'</p>'+paragraphs(b.paragraphs)+(b.items?'<ol>'+b.items.map(t=>'<li>'+esc(t)+'</li>').join('')+'</ol>':'')+table+links+mediaHTML(b.media,pack,b.mediaLayout)+extra+(b.context==='device'?'':routes)+(b.storageNotice?'<aside class="lw-work-notice"><b>Antworten und Dateien</b><p>'+esc(b.storageNotice)+'</p></aside>':'')+(b.network?require('../m01-netze/render.cjs').render(!!options.paper):'')+answer+help+(b.type==='private'?'<p>Bleibt hier persönlich. Wird nicht in „Deine Arbeit“, Arbeitsdateien oder Druckausgaben übernommen. Bei einem Seitenwechsel kann diese Notiz verloren gehen.</p><button class="lw-button secondary" data-private-export="'+fieldId+'">Nur diese private Notiz gesondert sichern</button>':'')+(b.solution?'<details class="lw-solution"><summary>'+(b.type==='retrieval'?'Nach deinem Versuch vergleichen':'Mögliche Lösung vergleichen')+'</summary><p>'+esc(b.solution)+'</p></details>':'')+citations(b.sources,pack)+'</section>';
 }).join('');
 return html+(privateUsed?'<dialog id="lw-private-dialog" aria-labelledby="lw-private-title"><h2 id="lw-private-title">Nur deine private Notiz</h2><p>Diese Datei enthält die folgende persönliche Notiz. Andere Personen mit Zugriff auf die Datei können sie lesen.</p><pre id="lw-private-preview" class="lw-product"></pre><button id="lw-private-confirm" class="lw-button">Diese Notiz als eigene Textdatei anbieten</button><button id="lw-private-cancel" class="lw-button secondary">Abbrechen</button></dialog>':'');
}
function load(grade=5){
 const dir=path.join(__dirname,'inhalte',grade===5?'':'klasse'+grade);if(![5,6].includes(grade))throw new Error('Unbekannter Jahrgang');if(!fs.existsSync(dir))return [];
 const packs=fs.readdirSync(dir).filter(n=>n.endsWith('.json')).sort().map(n=>validate(JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'))));
 return grade===6?packs.sort((a,b)=>a.curriculum.moduleId.localeCompare(b.curriculum.moduleId,'de',{numeric:true})):packs;
}
function assets(pack){
 const root=fs.realpathSync(path.join(__dirname,'inhalte')),out=new Map();
 for(const m of pack.media||[]){
  const file=fs.realpathSync(path.join(root,m.file));if(!file.startsWith(root+path.sep))throw new Error('Medium außerhalb des Inhaltsordners');
  const data=fs.readFileSync(file);if(data.length>2*1024*1024)throw new Error('Medium überschreitet 2 MB: '+m.file);
  if(m.file.endsWith('.svg')&&/<script|<foreignObject|\bon\w+\s*=|(?:href|src)\s*=\s*["'](?:https?:|data:|javascript:)/i.test(data.toString()))throw new Error('Aktiver SVG-Inhalt unzulässig');
  if(m.kind==='download'&&data.toString('utf8').trim()!==m.printText.trim())throw new Error('Datei und Druckinhalt weichen ab: '+m.file);
  out.set(m.file,data);
 }return out;
}
function unit(pack){return {...pack,kind:pack.kind||'core',status:'working',schemaVersion:1,learningDesign:{goal:pack.product,coverage:Object.fromEntries(Object.entries(pack.coverage).map(([k,v])=>[k,v.join('/')]))},fields:pack.steps.flatMap(s=>s.blocks.filter(b=>['task','external','cooperative','retrieval'].includes(b.type)).map(b=>'i:answer-'+s.id+'-'+b.id))};}
module.exports={actionLink,validate,renderBlocks,load,unit,assets,esc,paragraphs,mediaHTML,citations};
