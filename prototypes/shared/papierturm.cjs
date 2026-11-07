'use strict';
const fs=require('node:fs'),path=require('node:path');
const A=require('./class5-content.cjs'),e=A.esc,dir='assets/kommunikation/papierturm/';
function active(p){return p.grade===6&&p.area==='kommunikation'&&p.papertower?.version===2;}
function model(p){
 if(!active(p))throw Error('Papierturm V2 nur im Kommunikationspaket');
 const m=p.papertower;
 if(m.image!==dir+'turm.webp'||m.sceneImage!==dir+'tisch-v2.webp'||!m.alt||!m.sceneAlt||!m.post||!m.context||!m.rules||m.views.map(v=>v.id).join()!=='a,b,c')throw Error('Papierturm-Material unvollständig');
 return m;
}
function nav(){return '<nav class="pt-links no-print" aria-label="Papierturm-Material"><a href="papierturm.html">Material groß öffnen ↗</a><a href="papierturm-text.html">Textzugang</a></nav>';}
function card(v,m){
 const analogue=v.id==='a',image=analogue?m.sceneImage:m.image,alt=analogue?m.sceneAlt:m.alt;
 const speaker=analogue?'<p class="pt-spoken">Nuri zeigt auf den Turm und sagt:</p>':'<div class="pt-person"><span class="pt-avatar" aria-hidden="true">N</span><div><strong>Nuri</strong><small>heute, 12:05</small></div></div>';
 return '<article class="pt-card pt-'+v.id+'" data-pt-card="'+v.id+'" aria-labelledby="pt-'+v.id+'-title">'+
 '<header class="pt-card-head"><p class="pt-kicker">Ansicht '+v.id.toUpperCase()+'</p><h3 id="pt-'+v.id+'-title">'+e(v.title)+'</h3><p class="pt-access">'+e(v.access)+'</p><p class="pt-print-post"><strong>Nuri'+(analogue?' sagt:':' · heute, 12:05')+'</strong><br>„'+e(m.post)+'“</p></header>'+
 '<div class="pt-scene"><figure class="pt-photo"><img src="'+e(image)+'" alt="'+e(alt)+'" width="1536" height="1024"><figcaption>'+(analogue?'Gemeinsame Situation am Tisch':'Bildbeitrag: der fertige Turm')+' · KI-Illustration</figcaption></figure>'+
 '<div class="pt-conversation"><p class="pt-channel">'+e(v.channel)+'</p><div class="pt-post">'+speaker+'<p class="pt-message">'+e(m.post)+'</p></div>'+
 (v.id==='c'?'<p class="pt-views">180 Aufrufe</p>':'')+
 '<div class="pt-reactions">'+v.reactions.map(r=>'<div class="pt-reply"><p><strong>'+e(r.name)+'</strong><small>'+e(r.time)+'</small></p><p>'+e(r.text)+'</p></div>').join('')+'</div></div></div>'+
 '<dl class="pt-conditions">'+v.conditions.map(([k,t])=>'<div><dt>'+e(k)+'</dt><dd>'+e(t)+'</dd></div>').join('')+'</dl></article>';
}
function credit(){return '<p class="pt-credit">Fiktiver Fall · Bilder mit KI erzeugt, gestaltete Übungsoberflächen. IuM-Lernwerk · <a href="papierturm-quellen.html">Herkunft und Nutzung</a></p>';}
function rules(p){return '<details class="pt-rules"><summary>Regeln für diesen Übungsfall</summary><p>'+e(model(p).rules)+'</p><p>Diese Regeln sind erfunden und beschreiben keinen echten Dienst.</p></details><p class="pt-print-rules"><b>Fallregeln:</b> '+e(model(p).rules)+'</p>';}
function context(p){return '<section class="pt-context" id="turm-hintergrund"><h2>2 · Was der Bildbeitrag nicht zeigt</h2><p>Erst deinen eigenen Satz mit Beleg formulieren, dann öffnen.</p><details><summary>Hintergrund zum Turm öffnen</summary><div class="pt-reveal"><p>'+e(model(p).context)+'</p></div></details><div class="pt-print-context"><h3>Neue Information zum Fall</h3><p>'+e(model(p).context)+'</p></div></section>';}
function first(){return '<section class="pt-prompt"><h2>1 · Dein erster Eindruck</h2><p>Betrachte B oder C. Welchen Eindruck kann der Beitrag bei jemandem auslösen, dessen Turm noch nicht steht? Formuliere einen eigenen Satz mit Bild- oder Wortbeleg. Mündlich genügt.</p><p class="pt-sentence">„Der Beitrag könnte … auslösen, weil …“</p></section>';}
function revise(){return '<section class="pt-prompt"><h2>3 · Deine Deutung prüfen</h2><p>Greife deinen ersten Satz wieder auf. Bestätige oder präzisiere ihn mit der neuen Information.</p><p class="pt-sentence">„Ich bestätige/ergänze meine Deutung, weil …“</p><p>Was zeigt der Beitrag zuverlässig, und was lässt sich daraus nicht ablesen?</p></section>';}
function gallery(p,{all=false}={}){
 const m=model(p),buttons=[...m.views.map(v=>[v.id,v.label]),['ab','A ↔ B'],['bc','B ↔ C'],['all','Alle drei']];
 return '<section id="papierturm" class="pt-material" data-pt-root data-pt-initial="'+(all?'all':'a')+'"><header class="pt-intro"><p class="pt-kicker">Papierturm · Drei Kommunikationsräume</p><h2>Wer bekommt es mit?</h2></header>'+
 '<div class="pt-controls" hidden aria-label="Ansicht auswählen" role="group">'+buttons.map(([id,t])=>'<button type="button" data-pt-view="'+id+'" aria-pressed="false" aria-controls="pt-cards">'+e(t)+'</button>').join('')+'</div><p class="pt-status" data-pt-status role="status" aria-live="polite"></p>'+
 '<div id="pt-cards" class="pt-cards">'+m.views.map(v=>card(v,m)).join('')+'</div>'+rules(p)+nav()+credit()+'</section>';
}
function text(p){
 const m=model(p);
 return '<article class="lw-author pt-text"><p><a href="schritt-vergleichen.html#papierturm">← Zurück zur Aufgabe</a> · <a href="papierturm.html">Gestaltete Ansichten</a></p><h1>Eine Botschaft in drei Räumen</h1><p><strong>Nuris Wortlaut überall:</strong> „'+e(m.post)+'“</p>'+
 m.views.map(v=>'<section><h2>'+e(v.label)+'</h2><p>'+e(v.access)+' · '+e(v.channel)+'</p><p><strong>Bildbeschreibung:</strong> '+e(v.id==='a'?m.sceneAlt:m.alt)+'</p><p>'+(v.id==='a'?'Nuri sagt den Satz am Tisch.':'Nuri veröffentlicht den Bildbeitrag heute um 12:05.')+'</p>'+
 '<h3>Reaktionen</h3><ul>'+v.reactions.map(r=>'<li>'+e(r.name)+' · '+e(r.time)+': „'+e(r.text)+'“</li>').join('')+'</ul><dl class="pt-conditions">'+v.conditions.map(([k,t])=>'<div><dt>'+e(k)+'</dt><dd>'+e(t)+'</dd></div>').join('')+'</dl></section>').join('')+
 rules(p)+first()+context(p)+revise()+credit()+'<p><a href="schritt-vergleichen.html#papierturm">Zum Lernbogen mit allen Prüfanlässen →</a></p></article>';
}
function integrate(p,pages){
 if(!active(p))return pages;
 model(p);const out=new Map(pages),step=p.steps.find(s=>s.id==='vergleichen'),intro=step.blocks[0],ctx=step.blocks.find(b=>b.title==='Hintergrund zum Turmbeitrag');
 for(const [file,paper]of [['schritt-vergleichen.html',false],['baustein-vergleichen.html',true]]){
  let html=out.get(file);
  for(const [b,replacement]of [[intro,gallery(p,{all:paper})],[ctx,context(p)]]){
   const marker=A.renderBlocks({...step,blocks:[b]},p,{paper});
   if(!html.includes(marker))throw Error('Papierturm-Einfügestelle fehlt: '+file);
   html=html.replace(marker,replacement);
  }
  out.set(file,html);
 }
 out.set('papierturm.html','<article class="lw-author pt-standalone"><p><a href="schritt-vergleichen.html#papierturm">← Zurück zum Lernbogen</a></p><h1 class="pt-page-title">Nuris Papierturm</h1>'+gallery(p)+first()+context(p)+revise()+'<p><a href="schritt-vergleichen.html#papierturm">Raumvergleich und weitere Prüfanlässe im Lernbogen →</a></p></article>');
 out.set('papierturm-text.html',text(p));
 out.set('papierturm-quellen.html','<article class="lw-author lw-readable"><p><a href="papierturm.html">← Zum Material</a></p><h1>Herkunft und Nutzung</h1><p>Fassung 2 · 07.11.2026. Fiktiver Unterrichtsfall des IuM-Lernwerks. Personen, Aussagen und Oberflächen sind erfunden.</p><p>Beide Bilder wurden mit OpenAI ImageGen erzeugt. Das Turmmotiv aus Fassung 1 dient als Referenz für die Tischszene mit Nuri und vier Zuhörenden. B/C verwenden dasselbe Bild des fertigen Turms. Die Bilder dokumentieren keinen echten Bauversuch und sind keine Bauanleitung.</p><p>Aufbereitung: WebP-Kodierung. Nachrichten, Uhrzeiten und Bedingungen sind als HTML-Text gesetzt. Der wahre Erfolgssatz wird erst nach eigener Deutung um den Baukontext ergänzt. Der unbekannte AG-Kontakt ist ein gesonderter Fall im Lernbogen und kommt im öffentlichen Feed nicht vor.</p><p>Eigene Texte und Gestaltung: IuM-Lernwerk, CC BY-SA 4.0. Code MIT. KI-Bilder sind als solche gekennzeichnet und werden, soweit Rechte bestehen, entsprechend zur Nachnutzung bereitgestellt. Keine fremden Marken oder echten Plattformaufnahmen.</p><p><a href="papierturm-text.html">Textzugang</a> · <a href="schritt-vergleichen.html#papierturm">Zum Lernbogen</a></p></article>');
 for(const file of ['briefing.html','lehrkraft.html','material.html'])out.set(file,out.get(file).replace('</h1>','</h1><nav class="pt-links"><a href="schritt-vergleichen.html#papierturm">Papierturm im Lernbogen</a><a href="papierturm.html">Ansichten für die Projektion</a><a href="papierturm-text.html">Textzugang</a></nav>'));
 return out;
}
function assets(p){
 const out=new Map();if(!active(p))return out;const m=model(p);
 for(const file of ['papierturm.css','papierturm.js'])out.set(file,fs.readFileSync(path.join(__dirname,file),'utf8'));
 for(const file of [m.image,m.sceneImage]){
  const data=fs.readFileSync(path.join(__dirname,'inhalte',file));
  if(!data.length||data.length>2*1024*1024)throw Error('Papierturm-Bildgröße ungültig');
  out.set(file,data);
 }
 return out;
}
module.exports={active,gallery,context,integrate,assets};

