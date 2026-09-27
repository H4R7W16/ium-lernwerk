/* Independent, freely navigable media-analysis learning surface. */
(function(){
'use strict';
const C=window.MediaContent,M=window.MediaModel,e=M.escapeHtml;
const main=document.querySelector('main'),nav=document.querySelector('#steps');
const state={notes:{},answers:{},checked:false,mode:'crop',crop:{...M.presets.left},headline:C.headlines[1],draft:{crop:{...M.presets.full},headline:'',caption:'',reason:''},review:false,criteria:{},revised:false};
let current=0;
const announce=text=>{document.querySelector('#announce').textContent=text;};
function svg(scene,selection,id){
 const description=M.cropDescription(scene,selection);
 return '<svg'+(id?' id="'+id+'"':'')+' xmlns="http://www.w3.org/2000/svg" viewBox="'+M.viewBox(selection)+'" role="img" aria-label="'+e(description)+'"><image href="assets/'+scene.file+'" width="1536" height="1024"/></svg>';
}
function story(label,scene,selection,headline,id,caption){
 return '<article class="story"><div class="story-top"><b>'+e(label)+'</b><span>Schulzeitung · Übungsbeitrag</span></div>'+svg(scene,selection,id? id+'-image':null)+'<div class="story-copy"><h2'+(id?' id="'+id+'-headline"':'')+'>'+e(headline)+'</h2>'+(caption!==undefined?'<p'+(id?' id="'+id+'-caption"':'')+'>'+e(caption)+'</p>':'')+'</div></article>';
}
function fullFigure(scene){
 return '<figure class="full-figure">'+svg(scene,M.presets.full)+'<figcaption>Ganzes Bild · KI-Illustration einer erfundenen Situation</figcaption></figure>';
}
function context(scene){
 return '<aside class="context-card"><h3>Situationskarte</h3><p>Zusätzliche Angaben zu unserer erfundenen Geschichte:</p><ul>'+scene.context.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul></aside>';
}
function note(key,label,placeholder,rows=3){
 return '<label class="field"><span>'+e(label)+'</span><textarea rows="'+rows+'" data-note="'+key+'" placeholder="'+e(placeholder)+'">'+e(state.notes[key]||'')+'</textarea></label>';
}
function support(step){
 return '<div class="support"><div><p class="core"><b>Merke</b>'+e(step.core)+'</p><details><summary>Erklärung lesen</summary><p>'+e(step.explanation)+'</p></details><details><summary>Ein mögliches Beispiel ansehen</summary><p>'+e(step.example)+'</p><p class="small muted">Vergleiche mit deiner eigenen Antwort. Auch andere begründete Antworten können passen.</p></details><a href="wissen.html#'+step.id+'" target="_blank" rel="noopener">Im Wissen nachlesen ↗</a></div><aside class="tips"><h3>Wenn du Unterstützung brauchst</h3>'+step.hints.map((t,i)=>'<details><summary>Tipp '+(i+1)+'</summary><p>'+e(t)+'</p></details>').join('')+'<p class="small muted">Du kannst deine Begründung auch mündlich geben oder ins Heft schreiben.</p></aside></div>';
}
function cropControls(scope,selection){
 const c=M.crop(selection);
 return '<div class="controls"><p class="small"><b>Bildausschnitt wählen</b></p><div class="row" role="group" aria-label="Vorgegebene Bildausschnitte">'+[['left','Bänke'],['right','Mitmachstände'],['full','Ganzes Bild']].map(([key,label])=>'<button type="button" data-preset="'+key+'" data-scope="'+scope+'" aria-pressed="'+(c.x===M.crop(M.presets[key]).x&&c.width===M.crop(M.presets[key]).width)+'">'+label+'</button>').join('')+'</div><div class="slider-grid"><label class="field"><span>Wie viel vom Bild? <output id="'+scope+'-width-label">'+Math.round(c.width/1536*100)+' %</output></span><input type="range" data-crop="width" data-scope="'+scope+'" min="600" max="1536" step="1" value="'+c.width+'" aria-label="Breite des Bildausschnitts"></label><label class="field"><span>Position: links ↔ rechts</span><input type="range" data-crop="x" data-scope="'+scope+'" min="0" max="'+(1536-c.width)+'" step="1" value="'+c.x+'" aria-label="Horizontale Position des Bildausschnitts"'+(c.width===1536?' disabled':'')+'></label></div><p class="small muted">Die Regler lassen sich auch mit den Pfeiltasten bedienen.</p></div>';
}
function renderFirst(){
 return '<div class="pair">'+story('Beitrag A',C.scenes.festival,M.presets.left,'Nichts los beim Schulfest!')+story('Beitrag B',C.scenes.festival,M.presets.right,'Gemeinsam kreativ am Mitmachstand')+'</div><p class="image-label">Beide Beiträge verwenden Ausschnitte derselben KI-Illustration. Die Schule und das Fest sind erfunden.</p><div class="panel"><div class="note-grid">'+note('see','Was siehst du tatsächlich?','Ich sehe im linken / rechten Bild …')+note('impression','Welchen Eindruck bekommst du?','Die Wörter … / der Ausschnitt … lassen es so wirken, als …')+'</div><details><summary>Ganzes Bild aufdecken</summary>'+fullFigure(C.scenes.festival)+'<p class="small">Welche Vermutung würdest du jetzt ändern? Begründe mit einer Bildstelle.</p></details></div>';
}
function renderExperiment(){
 const pair=M.experiment(state.mode,state.crop,state.headline);
 return '<div class="mode-controls" role="group" aria-label="Was möchtest du untersuchen?"><button data-mode="crop" aria-pressed="'+(state.mode==='crop')+'">1 · Nur Bildausschnitt</button><button data-mode="headline" aria-pressed="'+(state.mode==='headline')+'">2 · Nur Überschrift</button></div><p class="variable-note" id="variable-note">'+(state.mode==='crop'?'Die Überschrift bleibt gleich. Du veränderst nur den Ausschnitt.':'Das Bild bleibt gleich. Du veränderst nur die Überschrift.')+'</p><div class="pair">'+story('Zum Vergleich',C.scenes.festival,pair.before.crop,pair.before.headline,'before')+story('Dein Versuch',C.scenes.festival,pair.after.crop,pair.after.headline,'after')+'</div><p class="image-label">KI-Illustration · erfundenes Schulfest</p><div id="crop-experiment"'+(state.mode!=='crop'?' hidden':'')+'>'+cropControls('experiment',state.crop)+'</div><div id="headline-experiment" class="controls"'+(state.mode!=='headline'?' hidden':'')+'><label class="field"><span>Überschrift für deinen Versuch</span><select id="headline-choice" aria-label="Überschrift für deinen Versuch">'+C.headlines.map(t=>'<option'+(state.headline===t?' selected':'')+'>'+e(t)+'</option>').join('')+'</select></label></div>'+note('effect','Erkläre einen Unterschied','Ich habe … verändert. … blieb gleich. Dadurch wirkt …, weil …');
}
function renderEvidence(){
 return '<div class="evidence-layout">'+fullFigure(C.scenes.festival)+context(C.scenes.festival)+'</div><section class="panel statements" aria-labelledby="claims-title"><h2 id="claims-title">Worauf stützt du die Aussage?</h2><p class="small">„So nicht belegbar“ gilt, wenn eine Information fehlt oder das Material der Aussage widerspricht.</p>'+C.claims.map((c,i)=>'<fieldset class="claim"><legend>'+(i+1)+'. '+e(c.text)+'</legend><div class="options">'+C.choices.map(o=>'<label><input type="radio" name="'+c.id+'" value="'+o.id+'"'+(state.answers[c.id]===o.id?' checked':'')+'>'+e(o.label)+'</label>').join('')+'</div><div id="feedback-'+c.id+'" class="feedback" hidden></div></fieldset>').join('')+'<button class="primary" data-action="check-evidence">Meine Zuordnung prüfen</button><p id="evidence-status" class="small" role="status"></p></section>'+note('limit','Welche Frage bleibt offen?','Aus dem Bild und der Karte weiß ich noch nicht, …',2);
}
function draftFields(){
 return '<label class="field"><span>Deine Überschrift</span><input id="draft-headline-field" data-draft="headline" type="text" maxlength="100" value="'+e(state.draft.headline)+'" placeholder="Worauf möchtest du aufmerksam machen?"></label><label class="field"><span>Deine Bildunterschrift</span><textarea id="draft-caption-field" data-draft="caption" rows="3" maxlength="450" placeholder="Beschreibe den gezeigten Moment. Ergänze bei Bedarf eine Angabe der Situationskarte.">'+e(state.draft.caption)+'</textarea></label><label class="field"><span>Begründe deine Gestaltung</span><textarea id="draft-reason" data-draft="reason" rows="3" maxlength="700" placeholder="Mein Ausschnitt zeigt … und lässt … weg. Meine Überschrift passt, weil …">'+e(state.draft.reason)+'</textarea></label>';
}
function criteria(){
 return '<div class="criteria" id="draft-review"'+(!state.review?' hidden':'')+'><h3>Prüfe deinen Beitrag</h3><p>Hier beurteilst du selbst. Die Anwendung bewertet deine Texte nicht.</p><p id="draft-missing"></p>'+C.steps[3].criteria.map((t,i)=>'<label><input type="checkbox" data-criterion="'+i+'"'+(state.criteria[i]?' checked':'')+'>'+e(t)+'</label>').join('')+'<p id="review-status" class="revision-note"></p><p><b>Überarbeiten:</b> Ändere einen Text oder den Ausschnitt, wenn etwas noch nicht passt. Prüfe danach erneut.</p><details class="examples"><summary>Zwei mögliche Beiträge vergleichen</summary><p>'+e(C.steps[3].example)+'</p></details></div>';
}
function renderEditor(){
 return '<div class="workspace"><section class="panel"><h2>Deine Redaktion</h2><p class="small">Informiere andere Kinder über einen Ausschnitt des Festes. Du kannst deinen Beitrag jederzeit verändern.</p>'+draftFields()+'<details><summary>Situationskarte nachlesen</summary>'+context(C.scenes.festival)+'</details><button class="primary" data-action="review-draft">Meinen Beitrag überprüfen</button>'+criteria()+'</section><div class="preview-side">'+story('Dein Beitrag',C.scenes.festival,state.draft.crop,state.draft.headline||'Hier erscheint deine Überschrift','draft',state.draft.caption||'Hier erscheint deine Bildunterschrift.')+'<p class="image-label">KI-Illustration · erfundenes Schulfest · Vorschau deines Beitrags</p>'+cropControls('draft',state.draft.crop)+'</div></div>';
}
function renderTransfer(){
 return '<div class="workspace"><div><h2>Prüfe die Behauptung</h2>'+note('transfer-claim','Was ist an „niemand“ problematisch?','Der Ausschnitt zeigt … Die Überschrift behauptet aber …')+note('transfer-title','Deine genauere Überschrift','Zum Ausschnitt würde besser passen: …',2)+note('transfer-reason','Begründe und nenne eine offene Frage','Meine Überschrift passt, weil … Unklar bleibt …')+'</div><div>'+story('Neuer Fall',C.scenes.library,M.presets.left,'Hier liest doch niemand!')+'<p class="image-label">KI-Illustration · erfundene Schulbibliothek</p></div></div><details class="panel transfer-reveal"><summary>Ganzes Bild und Situationskarte öffnen</summary><div class="evidence-layout">'+fullFigure(C.scenes.library)+context(C.scenes.library)+'</div></details><details class="panel"><summary>Meine Begründung selbst prüfen</summary><ul>'+C.steps[4].criteria.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul><p>Zeige eine Bildstelle zu deiner Erklärung. Eine Partnerperson oder deine Lehrperson kann nachfragen.</p></details><div class="finish"><h2>Dein Blick auf den nächsten Beitrag</h2><ol><li>Was sehe ich wirklich?</li><li>Welche Behauptung machen Bild und Überschrift?</li><li>Welche zusätzliche Information brauche ich?</li></ol><p>Erkläre an einem unserer Beispiele, warum ein Ausschnitt sinnvoll sein kann und wann er einen falschen Eindruck erzeugt.</p></div>';
}
const renderers=[renderFirst,renderExperiment,renderEvidence,renderEditor,renderTransfer];
function render(focus=false){
 const id=location.hash.slice(1),index=C.steps.findIndex(s=>s.id===id);current=index<0?0:index;
 const step=C.steps[current];
 nav.innerHTML=C.steps.map((s,i)=>'<a href="#'+s.id+'"'+(current===i?' aria-current="step"':'')+'><span class="num">'+(i+1)+'</span>'+e(s.short)+'</a>').join('');
 main.innerHTML='<header class="intro"><p class="eyebrow">'+e(step.eyebrow)+'</p><h1>'+e(step.title)+'</h1><p>'+e(step.task)+'</p></header><details class="entry"><summary>Was du für diesen Schritt brauchst</summary><p><b>Dein Ziel:</b> '+e(step.goal)+'</p><p>'+e(step.start)+'</p><p>Alle fünf Schritte sind frei wählbar. Wenn ihr einen Inhalt gemeinsam besprochen habt, kannst du direkt beim passenden Auftrag weiterarbeiten.</p></details>'+renderers[current]()+support(step)+'<div class="continue"><p>'+e(step.prompt)+'</p><a class="next-link" href="#'+C.steps[(current+1)%5].id+'">'+(current===4?'Zurück zum Einstieg':'Weiter: '+C.steps[current+1].short)+' →</a></div>';
 if(current===2&&state.checked) showEvidence();
 if(current===3&&state.review) updateReview();
 if(focus){main.focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
function setImage(id,selection,scene=C.scenes.festival){
 const node=document.getElementById(id);if(!node)return;
 node.setAttribute('viewBox',M.viewBox(selection));node.setAttribute('aria-label',M.cropDescription(scene,selection));
}
function updateExperiment(){
 const pair=M.experiment(state.mode,state.crop,state.headline);
 for(const key of ['before','after']){setImage(key+'-image',pair[key].crop);document.getElementById(key+'-headline').textContent=pair[key].headline;}
}
function updateCrop(scope){
 const target=scope==='draft'?state.draft:state,c=M.crop(target.crop);target.crop={x:c.x,width:c.width};
 const width=document.querySelector('[data-scope="'+scope+'"][data-crop="width"]'),position=document.querySelector('[data-scope="'+scope+'"][data-crop="x"]');
 width.value=c.width;position.max=1536-c.width;position.value=c.x;position.disabled=c.width===1536;
 document.getElementById(scope+'-width-label').textContent=Math.round(c.width/1536*100)+' %';
 document.querySelectorAll('[data-scope="'+scope+'"][data-preset]').forEach(b=>{const p=M.crop(M.presets[b.dataset.preset]);b.setAttribute('aria-pressed',String(c.x===p.x&&c.width===p.width));});
 if(scope==='draft'){setImage('draft-image',c);invalidateReview();}else updateExperiment();
}
function showEvidence(){
 const rows=M.assess(state.answers);
 rows.forEach(r=>{const node=document.getElementById('feedback-'+r.id);node.hidden=false;node.dataset.status=r.status;node.innerHTML='<b>'+({open:'Noch offen',match:'Passender Beleg',revise:'Prüfe deinen Beleg noch einmal'}[r.status])+'</b>'+e(r.feedback);});
 const missing=rows.filter(r=>r.status==='open').length,revise=rows.filter(r=>r.status==='revise').length;
 document.getElementById('evidence-status').textContent=missing?missing+' Zuordnung(en) sind noch offen.':revise? 'Lies die Hinweise und überarbeite deine Zuordnung.':'Die vier Zuordnungen passen zum Material. Begründe jetzt eine davon in eigenen Worten.';
}
function updateReview(){
 const missing=[['headline','eine eigene Überschrift'],['caption','eine Bildunterschrift'],['reason','deine Begründung']].filter(([key])=>!state.draft[key].trim()).map(([,label])=>label);
 document.getElementById('draft-missing').textContent=missing.length?'In den Eingabefeldern fehlt noch: '+missing.join(', ')+'. Wenn du mündlich oder im Heft arbeitest, prüfe dort.':'Deine Felder sind ausgefüllt. Ob die Aussagen passen, prüfst du mit den Kriterien.';
 document.getElementById('review-status').textContent=state.revised?'Du hast deinen Beitrag verändert. Prüfe die Kriterien für diese Fassung erneut.':Object.values(state.criteria).filter(Boolean).length===4?'Du hast alle vier Kriterien selbst geprüft. Erkläre eine Entscheidung an deinem Beitrag.':'Hake nur ab, was du an deinem eigenen Beitrag begründen kannst.';
}
function invalidateReview(){
 if(!state.review)return;state.criteria={};state.revised=true;
 document.querySelectorAll('[data-criterion]').forEach(n=>{n.checked=false;});updateReview();
}
main.addEventListener('input',event=>{
 const node=event.target;
 if(node.dataset.note){state.notes[node.dataset.note]=node.value;return;}
 if(node.dataset.draft){
  const key=node.dataset.draft;state.draft[key]=node.value;

  // Only preview nodes are changed: typing keeps caret, selection and focus.
  if(key==='headline')document.querySelector('.preview-side #draft-headline').textContent=node.value||'Hier erscheint deine Überschrift';
  if(key==='caption')document.querySelector('.preview-side #draft-caption').textContent=node.value||'Hier erscheint deine Bildunterschrift.';
  invalidateReview();return;
 }
 if(node.dataset.crop){const target=node.dataset.scope==='draft'?state.draft:state;target.crop[node.dataset.crop]=Number(node.value);updateCrop(node.dataset.scope);}
});
main.addEventListener('change',event=>{
 const node=event.target;
 if(node.id==='headline-choice'){state.headline=node.value;updateExperiment();}
 if(node.type==='radio'){
  state.answers[node.name]=node.value;state.checked=false;
  document.querySelectorAll('.claim .feedback').forEach(n=>{n.hidden=true;});
  document.getElementById('evidence-status').textContent='Auswahl verändert. Prüfe deine Zuordnung erneut.';
 }
 if(node.dataset.criterion!==undefined){state.criteria[node.dataset.criterion]=node.checked;state.revised=false;updateReview();}
});
main.addEventListener('click',event=>{
 const button=event.target.closest('button');if(!button)return;
 if(button.dataset.mode){
  state.mode=button.dataset.mode;
  document.querySelectorAll('[data-mode]').forEach(n=>n.setAttribute('aria-pressed',String(n.dataset.mode===state.mode)));
  document.getElementById('crop-experiment').hidden=state.mode!=='crop';document.getElementById('headline-experiment').hidden=state.mode!=='headline';
  document.getElementById('variable-note').textContent=state.mode==='crop'?'Die Überschrift bleibt gleich. Du veränderst nur den Ausschnitt.':'Das Bild bleibt gleich. Du veränderst nur die Überschrift.';
  updateExperiment();announce(document.getElementById('variable-note').textContent);
 }
 if(button.dataset.preset){const target=button.dataset.scope==='draft'?state.draft:state;target.crop={...M.presets[button.dataset.preset]};updateCrop(button.dataset.scope);announce('Bildausschnitt: '+button.textContent);}
 if(button.dataset.action==='check-evidence'){state.checked=true;showEvidence();announce('Hinweise stehen jetzt unter jeder Aussage.');}
 if(button.dataset.action==='review-draft'){state.review=true;document.getElementById('draft-review').hidden=false;updateReview();document.getElementById('draft-review').scrollIntoView({block:'nearest',behavior:'instant'});announce('Die Kriterien zur Selbstprüfung sind geöffnet.');}
});
window.addEventListener('hashchange',()=>{if(location.hash==='#main'){main.focus({preventScroll:true});return;}announce('');render(true);});
render();
})();
