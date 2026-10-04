/* Freely navigable learning path; open responses are never automatically graded. */
(function(){
'use strict';
const C=window.MediaContent,M=window.MediaModel,e=M.escapeHtml;
const main=document.querySelector('main'),nav=document.querySelector('#steps');
const state={notes:{},answers:{},transferAnswers:{},checked:false,transferChecked:false,calibration:'',calibrationChecked:false,mode:'crop',crop:{...M.presets.left},headline:C.headlines[1],draft:{crop:{...M.presets.full},headline:'',caption:'',reason:''},review:false,criteria:{},revised:false,decision:''};
let current=0;
const announce=text=>{document.querySelector('#announce').textContent=text;};
function svg(scene,selection,id){
 return '<svg'+(id?' id="'+id+'"':'')+' xmlns="http://www.w3.org/2000/svg" viewBox="'+M.viewBox(selection)+'" role="img" aria-label="'+e(M.cropDescription(scene,selection))+'"><image href="assets/'+scene.file+'" width="1536" height="1024"/></svg>';
}
function story(label,scene,selection,headline,id,caption){
 return '<article class="story"><div class="story-top"><b>'+e(label)+'</b><span>Schulzeitung · Übungsbeitrag</span></div>'+svg(scene,selection,id?id+'-image':null)+'<div class="story-copy"><h2'+(id?' id="'+id+'-headline"':'')+'>'+e(headline)+'</h2>'+(caption!==undefined?'<p'+(id?' id="'+id+'-caption"':'')+'>'+e(caption)+'</p>':'')+'</div></article>';
}
function fullFigure(scene){return '<figure class="full-figure">'+svg(scene,M.presets.full)+'<figcaption>Ganzes Bild · KI-Illustration einer erfundenen Situation</figcaption></figure>';}
function context(scene){return '<aside class="context-card"><h3>Situationskarte</h3><p>Zusätzliche Angaben zur erfundenen Geschichte:</p><ul>'+scene.context.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul></aside>';}
function note(key,label,placeholder,rows=3){return '<label class="field"><span>'+e(label)+'</span><textarea maxlength="10000" rows="'+rows+'" data-note="'+key+'" placeholder="'+e(placeholder)+'">'+e(state.notes[key]||'')+'</textarea></label>';}
function teaching(step,example=false){
 const body='<div class="teaching"><h2>So kannst du es erklären</h2><p class="core"><b>Merke</b>'+e(step.core)+'</p><p>'+e(step.explanation)+'</p>'+(example?'<div class="worked"><h3>Am Beispiel</h3><p>'+e(step.example)+'</p></div>':'')+'</div>';
 return window.LernwerkUI&&['wirkung','belege'].includes(step.id)?'<details class="lw-explanation"><summary>Erklärung und Beispiel</summary>'+body+'</details>':body;
}
function support(step){
 return '<aside class="support"><div><h2>Hilfe nach Bedarf</h2>'+step.hints.map((t,i)=>'<details><summary>'+(window.LernwerkMantel?(i===0?'Ein Hinweis':'Eine genauere Hilfe'):'Tipp '+(i+1))+'</summary><p>'+e(t)+'</p></details>').join('')+'<details><summary>Begriffe nachlesen</summary><dl><dt>Beobachtung</dt><dd>Was du sehen kannst.</dd><dt>Deutung</dt><dd>Was du daraus vermutest oder wie es auf dich wirkt.</dd><dt>Beleg</dt><dd>Eine konkrete Stelle, die deine Aussage stützt.</dd><dt>Widerspruch</dt><dd>Das Material spricht gegen die Aussage.</dd></dl></details></div><div class="tips"><h3>Dein Bearbeitungsweg</h3><p>Du kannst die kurzen Ergebnisse hier, im Heft oder mündlich festhalten. Du brauchst sie nur einmal zu formulieren.</p><details><summary>Weitere mögliche Antwort</summary><p>'+e(step.example)+'</p><p>Vergleiche erst nach deinem eigenen Versuch. Andere begründete Antworten können auch passen.</p></details><a href="wissen.html#'+step.id+'" target="_blank" rel="noopener">Wissen und Bilder dazu ↗</a></div></aside>';
}
function cropControls(scope,selection){
 const c=M.crop(selection);
 return '<div class="controls"><p class="small"><b>Bildausschnitt wählen</b></p><div class="row" role="group" aria-label="Vorgegebene Bildausschnitte">'+[['left','Bänke'],['right','Mitmachstände'],['full','Ganzes Bild']].map(([key,label])=>'<button type="button" data-preset="'+key+'" data-scope="'+scope+'" aria-pressed="'+(c.x===M.crop(M.presets[key]).x&&c.width===M.crop(M.presets[key]).width)+'">'+label+'</button>').join('')+'</div><div class="slider-grid"><label class="field"><span>Wie viel vom Bild? <output id="'+scope+'-width-label">'+Math.round(c.width/1536*100)+' %</output></span><input type="range" data-crop="width" data-scope="'+scope+'" min="600" max="1536" step="1" value="'+c.width+'" aria-label="Breite des Bildausschnitts"></label><label class="field"><span>Position: links ↔ rechts</span><input type="range" data-crop="x" data-scope="'+scope+'" min="0" max="'+(1536-c.width)+'" step="1" value="'+c.x+'" aria-label="Horizontale Position des Bildausschnitts"'+(c.width===1536?' disabled':'')+'></label></div><p class="small muted">Die Regler lassen sich auch mit den Pfeiltasten bedienen.</p></div>';
}
function renderFirst(){
 return '<h2 class="section-title">1 · Betrachten und vermuten</h2><div class="pair">'+story('Beitrag A',C.scenes.festival,M.presets.left,'Nichts los beim Schulfest!')+story('Beitrag B',C.scenes.festival,M.presets.right,'Gemeinsam kreativ am Mitmachstand')+'</div><p class="image-label">Zwei Ausschnitte derselben KI-Illustration · erfundenes Schulfest</p><div class="oral-prompt"><b>Zunächst mündlich:</b> „Ich sehe …“ und „Auf mich wirkt das …, weil …“. Was ist Beobachtung, was ist deine Vermutung?</div><details class="panel reveal"><summary>2 · Ganzes Bild öffnen und die Erklärung lesen</summary>'+fullFigure(C.scenes.festival)+teaching(C.steps[0],true)+'</details><section class="panel"><h2>3 · Deine erste Vermutung genauer formulieren</h2><p>Lies die Erklärung im aufgeklappten Abschnitt. Wähle dann einen Satz aus deinem ersten Eindruck: Was passt noch, was musst du ändern?</p>'+note('first-revision','Dein genauerer Satz mit Bildbeleg','Zuerst dachte ich … Genauer ist …, denn im ganzen Bild sehe ich …')+'</section>';
}
function renderExperiment(){
 const pair=M.experiment(state.mode,state.crop,state.headline);
 return '<div class="mode-controls" role="group" aria-label="Was möchtest du untersuchen?"><button data-mode="crop" aria-pressed="'+(state.mode==='crop')+'">1 · Nur Bildausschnitt</button><button data-mode="headline" aria-pressed="'+(state.mode==='headline')+'">2 · Nur Überschrift</button></div><p class="variable-note" id="variable-note">'+(state.mode==='crop'?'Die Überschrift bleibt gleich. Du veränderst nur den Ausschnitt.':'Das Bild bleibt gleich. Du veränderst nur die Überschrift.')+'</p><div class="pair">'+story('Zum Vergleich',C.scenes.festival,pair.before.crop,pair.before.headline,'before')+story('Dein Versuch',C.scenes.festival,pair.after.crop,pair.after.headline,'after')+'</div><p class="image-label">KI-Illustration · erfundenes Schulfest</p><div id="crop-experiment"'+(state.mode!=='crop'?' hidden':'')+'>'+cropControls('experiment',state.crop)+'</div><div id="headline-experiment" class="controls"'+(state.mode!=='headline'?' hidden':'')+'><label class="field"><span>Überschrift für deinen Versuch</span><select id="headline-choice">'+C.headlines.map(t=>'<option'+(state.headline===t?' selected':'')+'>'+e(t)+'</option>').join('')+'</select></label></div>'+teaching(C.steps[1],true)+'<section class="panel"><h2>Deine zwei Vergleiche</h2><p>Wähle jeweils einen Versuch. Ein kurzer Satz genügt. Nenne die Ausschnitte oder Überschriften, damit dein Vergleich verständlich bleibt.</p>'+note('crop-effect','Bildversuch: Was verändert der Ausschnitt?','Ich vergleiche … mit … Die Überschrift bleibt gleich. Dadurch wirkt …, weil …',2)+note('headline-effect','Textversuch: Was verändert die Überschrift?','Das Bild bleibt gleich. Bei der Überschrift … wirkt …, weil das Wort …',2)+'</section>';
}
function claimSet(bank,claims,choices,title){
 const answers=bank==='evidence'?state.answers:state.transferAnswers;
 return '<section class="panel statements" aria-labelledby="'+bank+'-title"><h2 id="'+bank+'-title">'+e(title)+'</h2>'+claims.map((c,i)=>'<fieldset class="claim"><legend>'+(i+1)+'. '+e(c.text)+'</legend><div class="options">'+choices.map(o=>'<label><input type="radio" name="'+bank+'-'+c.id+'" data-bank="'+bank+'" data-claim="'+c.id+'" value="'+o.id+'"'+(answers[c.id]===o.id?' checked':'')+'>'+e(o.label)+'</label>').join('')+'</div><div id="'+bank+'-feedback-'+c.id+'" class="feedback" hidden></div></fieldset>').join('')+'<button class="primary" data-action="check-'+bank+'">'+(bank==='evidence'?'Meine Zuordnung prüfen':'Meine Urteile prüfen')+'</button><p id="'+bank+'-status" class="small" role="status"></p></section>';
}
function renderEvidence(){
 return '<div class="evidence-layout">'+fullFigure(C.scenes.festival)+context(C.scenes.festival)+'</div>'+teaching(C.steps[2],false)+'<div class="answer-key"><h3>Vier Möglichkeiten</h3><ul><li><b>Das sehe ich im Bild:</b> Eine Bildstelle stützt den Satz.</li><li><b>Das steht in der Karte:</b> Eine zusätzliche Angabe stützt ihn.</li><li><b>Das Bild zeigt das Gegenteil:</b> Die Aussage ist widerlegt.</li><li><b>Dazu fehlen Informationen:</b> Du kannst noch nicht entscheiden.</li></ul></div>'+claimSet('evidence',C.claims,C.choices,'Prüfe die vier Aussagen')+'<section class="panel"><h2>Erkläre eine Entscheidung</h2>'+note('evidence-reason','Eine Zuordnung mit Begründung','Bei Aussage … wähle ich …, weil die Bildstelle / der Satz auf der Karte …')+'<p class="oral-prompt"><b>Mündlicher Denkimpuls:</b> Welche Frage bleibt offen? Welche zusätzliche Information könnte helfen?</p></section>';
}
function calibration(){
 const c=C.calibration;
 return '<section class="panel calibration"><h2>1 · Woran erkennst du eine gute Begründung?</h2><p>Zur Überschrift „'+e(c.headline)+'“ gibt es zwei Begründungen. Vergleiche sie, bevor du deinen Beitrag gestaltest.</p><details class="calibration-image"><summary>Das Bild zu den Begründungen ansehen</summary>'+fullFigure(C.scenes.festival)+'</details><div class="note-grid"><blockquote><b>A</b><p>'+e(c.weak)+'</p></blockquote><blockquote><b>B</b><p>'+e(c.strong)+'</p></blockquote></div><fieldset class="claim"><legend>Welche Begründung nennt einen Bildbeleg und eine Grenze des Wissens?</legend><div class="options">'+[['weak','Begründung A'],['strong','Begründung B']].map(([value,label])=>'<label><input type="radio" name="calibration" data-calibration value="'+value+'"'+(state.calibration===value?' checked':'')+'>'+label+'</label>').join('')+'</div></fieldset><button data-action="check-calibration">Begründungen vergleichen</button><div id="calibration-feedback" class="feedback"'+(state.calibrationChecked?'':' hidden')+'></div></section>';
}
function draftFields(){
 return '<label class="field"><span>Deine Überschrift</span><input id="draft-headline-field" data-draft="headline" type="text" maxlength="100" value="'+e(state.draft.headline)+'" placeholder="Welchen Teil oder Moment zeigst du?"></label><label class="field"><span>Deine Bildunterschrift</span><textarea id="draft-caption-field" data-draft="caption" rows="3" maxlength="450" placeholder="Beschreibe den Moment. Ergänze eine wichtige Angabe aus der Karte.">'+e(state.draft.caption)+'</textarea></label><label class="field"><span>Deine Aussage und ihr Beleg</span><textarea id="draft-reason" data-draft="reason" rows="3" maxlength="700" placeholder="Mein Ausschnitt zeigt … und lässt … weg. Mein Satz … passt, denn im Bild / auf der Karte …">'+e(state.draft.reason)+'</textarea></label>';
}
function criteria(){
 return '<div class="criteria" id="draft-review"'+(!state.review?' hidden':'')+'><h3>3 · Prüfen und verbessern</h3><p>Du beurteilst selbst. Die Anwendung bewertet deine Texte nicht. Nutze den Begründungsvergleich oben.</p><p id="draft-missing"></p>'+C.steps[3].criteria.map((t,i)=>'<label><input type="checkbox" data-criterion="'+i+'"'+(state.criteria[i]?' checked':'')+'>'+e(t)+'</label>').join('')+'<p id="review-status" class="revision-note" role="status"></p><label class="field"><span>Meine Entscheidung</span><select id="revision-decision"><option value="">Wähle deine Entscheidung</option><option value="change"'+(state.decision==='change'?' selected':'')+'>Ich verbessere meinen Beitrag.</option><option value="keep"'+(state.decision==='keep'?' selected':'')+'>Ich behalte meinen Beitrag begründet bei.</option></select></label>'+note('revision-reason','Deine Verbesserung oder dein Grund fürs Beibehalten','Ich ändere … zu …, weil … / Ich behalte … bei, weil die Bildstelle oder Kartenangabe …',2)+'<p id="revision-next">'+revisionNext()+'</p><p><b>Leserblick:</b> Lies deinen Beitrag aus Sicht eines anderen Kindes. Welchen Eindruck bekommt es? Falls ihr zu zweit arbeitet: „Welche Stelle belegt diesen Satz?“</p></div>';
}
function revisionNext(){return state.decision==='change'?'Ändere jetzt die betreffende Stelle oben. Prüfe danach die Kriterien für deinen überarbeiteten Beitrag.':state.decision==='keep'?'Nenne eine konkrete Bildstelle oder Kartenangabe, die das Beibehalten begründet.':'Entscheide: Was muss genauer werden? Oder woran zeigst du, dass der Beitrag schon passt?';}
function renderEditor(){
 return calibration()+'<h2 class="section-title">2 · Deinen Beitrag gestalten</h2><p class="section-lead">'+e(C.steps[3].start)+'</p><div class="workspace"><section class="panel"><h3>Deine Redaktion</h3>'+draftFields()+'<details><summary>Situationskarte und ganzes Bild nachlesen</summary>'+fullFigure(C.scenes.festival)+context(C.scenes.festival)+'</details><button class="primary" data-action="review-draft">Meinen Beitrag überprüfen</button>'+criteria()+'</section><div class="preview-side">'+story('Dein Beitrag',C.scenes.festival,state.draft.crop,state.draft.headline||'Hier erscheint deine Überschrift','draft',state.draft.caption||'Hier erscheint deine Bildunterschrift.')+'<p class="image-label">KI-Illustration · erfundenes Schulfest</p>'+cropControls('draft',state.draft.crop)+'</div></div>';
}
function renderTransfer(){
 return '<h2 class="section-title">1 · Erst selbst urteilen</h2><div class="pair">'+story('Beitrag A',C.scenes.library,M.presets.left,'In unserer Bibliothek liest niemand.')+story('Beitrag B',C.scenes.library,M.presets.left,'Freie Plätze in der Leseecke.')+'</div><p class="image-label">Gleicher Ausschnitt, zwei Überschriften · KI-Illustration einer erfundenen Bibliothek</p><p class="oral-prompt"><b>Zunächst mündlich:</b> Welche Überschrift passt? Was spricht dafür oder dagegen? Was müsstest du noch sehen oder wissen? Entscheide vor dem Blick ins ganze Bild.</p><details class="panel reveal"><summary>2 · Ganzes Bild und Situationskarte öffnen</summary><div class="evidence-layout">'+fullFigure(C.scenes.library)+context(C.scenes.library)+'</div></details>'+claimSet('transfer',C.transferClaims,C.judgements,'3 · Jetzt mit dem ganzen Material urteilen')+'<section class="panel"><h2>Deine Erklärung zum Unterschied</h2><p>Vergleiche die beiden Beiträge. Warum reicht der Ausschnitt für eine Aussage aus? Warum nicht für die andere? Nenne zum Schluss eine offene Frage.</p>'+note('transfer-reason','Deine Begründung und eine offene Frage','Beitrag … passt, weil … Bei Beitrag … zeigt das ganze Bild … Noch nicht weiß ich …')+'<details><summary>Nach deinem Versuch: Erklärung und Selbstprüfung</summary>'+teaching(C.steps[4],false)+'<ul>'+C.steps[4].criteria.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul></details></section><div class="finish"><h2>Für den nächsten Beitrag</h2><p>Prüfe Bild und Text zusammen. Ein Ausschnitt kann sinnvoll sein. Frage immer: Was ist belegt, was wird widerlegt und was bleibt offen?</p></div>';
}
const renderers=[renderFirst,renderExperiment,renderEvidence,renderEditor,renderTransfer];
function render(focus=false){
 const id=location.hash.slice(1),index=C.steps.findIndex(s=>s.id===id);current=index<0?0:index;
 const step=C.steps[current];
 nav.innerHTML=window.LernwerkUI?window.LernwerkUI.navigation('Ein Bild – zwei Geschichten',C.steps,step.id):C.steps.map((s,i)=>'<a href="#'+s.id+'"'+(current===i?' aria-current="step"':'')+'><span class="num">'+(i+1)+'</span>'+e(s.short)+'</a>').join('');
 const seriesRoute=window.LernwerkMantel?'<nav class="lw-reading-links" aria-label="Reihe Medienwirkungen"><a href="../medienwirkung/index.html">Zur Reihe: Mehr als ein erster Eindruck</a></nav>':'';
 main.innerHTML=seriesRoute+(window.LernwerkUI?window.LernwerkUI.intro(step.title,step.task):'<header class="intro"><p class="eyebrow">'+e(step.eyebrow)+'</p><h1>'+e(step.title)+'</h1><p>'+e(step.task)+'</p><p class="goal"><b>Du lernst:</b> '+e(step.goal)+'</p></header><ol class="learning-route" aria-label="Dein Weg in diesem Schritt">'+step.route.map(t=>'<li>'+e(t)+'</li>').join('')+'</ol>')+renderers[current]()+(window.LernwerkUI?'<details class="lw-route-help"><summary>Vorwissen und Bearbeitungsweg</summary><p>'+e(step.goal)+'</p><ol>'+step.route.map(t=>'<li>'+e(t)+'</li>').join('')+'</ol></details>'+window.LernwerkUI.criteria(step.criteria,step.outcome):'<div class="outcome"><b>Bereit für den nächsten Schritt?</b><p>'+e(step.outcome)+'</p><p class="small">Erkläre es in eigenen Worten. Wenn du unsicher bist, nutze die Hilfe oder frage nach. Alle Schritte bleiben frei wählbar.</p></div>')+support(step)+'<div class="continue"><p>'+e(step.prompt)+'</p><a class="next-link" href="#'+C.steps[(current+1)%5].id+'">'+(current===4?'Zurück zum Einstieg':'Weiter: '+C.steps[current+1].short)+' →</a></div>';
 if(window.LernwerkMantel){const target={belege:['selbstbild','Weiter in der Reihe: Ein Erfolg – die ganze Geschichte?'],gestalten:['rueckmeldung','Weiter in der Reihe: Rückmeldung und Überarbeitung'],transfer:['handeln','Weiter in der Reihe: Wenn Kommentare verletzen']}[step.id];if(target){const next=main.querySelector('.next-link');next.href='../medienwirkung/schritt-'+target[0]+'.html';next.textContent=target[1]+' →';}}
 if(current===2&&state.checked)showAnswers('evidence');
 if(current===3){if(state.calibrationChecked)showCalibration();if(state.review)updateReview();}
 if(current===4&&state.transferChecked)showAnswers('transfer');
 if(focus){main.focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
function setImage(id,selection,scene=C.scenes.festival){const node=document.getElementById(id);if(!node)return;node.setAttribute('viewBox',M.viewBox(selection));node.setAttribute('aria-label',M.cropDescription(scene,selection));}
function updateExperiment(){const pair=M.experiment(state.mode,state.crop,state.headline);for(const key of ['before','after']){setImage(key+'-image',pair[key].crop);document.getElementById(key+'-headline').textContent=pair[key].headline;}}
function updateCrop(scope){
 const target=scope==='draft'?state.draft:state,c=M.crop(target.crop);target.crop={x:c.x,width:c.width};
 const width=document.querySelector('[data-scope="'+scope+'"][data-crop="width"]'),position=document.querySelector('[data-scope="'+scope+'"][data-crop="x"]');
 width.value=c.width;position.max=1536-c.width;position.value=c.x;position.disabled=c.width===1536;
 document.getElementById(scope+'-width-label').textContent=Math.round(c.width/1536*100)+' %';
 document.querySelectorAll('[data-scope="'+scope+'"][data-preset]').forEach(b=>{const p=M.crop(M.presets[b.dataset.preset]);b.setAttribute('aria-pressed',String(c.x===p.x&&c.width===p.width));});
 if(scope==='draft'){setImage('draft-image',c);invalidateReview();}else updateExperiment();
}
function showAnswers(bank){
 const isEvidence=bank==='evidence',claims=isEvidence?C.claims:C.transferClaims,rows=M.assess(isEvidence?state.answers:state.transferAnswers,claims,isEvidence?C.choices:C.judgements);
 rows.forEach(r=>{
  const node=document.getElementById(bank+'-feedback-'+r.id),answer=claims.find(c=>c.id===r.id).answer;
  const matched={image:'Bildbeleg gefunden',context:'Kartenangabe gefunden',contradicted:'Widerspruch erkannt',unknown:'Fehlende Information erkannt',fits:'Passende Aussage erkannt'}[answer];
  node.hidden=false;node.dataset.status=r.status;node.innerHTML='<b>'+e(r.status==='open'?'Noch offen':r.status==='match'?matched:'Prüfe dein Urteil noch einmal')+'</b>'+e(r.feedback);
 });
 const missing=rows.filter(r=>r.status==='open').length,revise=rows.filter(r=>r.status==='revise').length;
 document.getElementById(bank+'-status').textContent=missing?missing+' Antwort(en) sind noch offen.':revise?'Lies die Hinweise und überarbeite deine Auswahl.':isEvidence?'Die Zuordnungen passen. Begründe unten eine Entscheidung in eigenen Worten.':'Die Urteile passen. Erkläre unten den Unterschied zwischen den Beiträgen.';
}
function showCalibration(){
 const node=document.getElementById('calibration-feedback');node.hidden=false;
 node.dataset.status=state.calibration==='strong'?'match':'revise';
 node.innerHTML=!state.calibration?'<p>Wähle zuerst A oder B. Suche: Welche Begründung zeigt eine konkrete Bildstelle?</p>':'<b>'+(state.calibration==='strong'?'B zeigt den Gedankengang.':'Schau dir B noch einmal an.')+'</b><p>'+e(C.calibration.feedback)+'</p><ol>'+C.calibration.moves.map(([label,text])=>'<li><b>'+e(label)+':</b> '+e(text)+'</li>').join('')+'</ol><p>Übertrage diesen Weg jetzt auf deinen eigenen Beitrag.</p>';
}
function updateReview(){
 const missing=[['headline','eine Überschrift'],['caption','eine Bildunterschrift'],['reason','eine Aussage mit Beleg']].filter(([key])=>!state.draft[key].trim()).map(([,label])=>label);
 document.getElementById('draft-missing').textContent=missing.length?'In den Feldern fehlt noch: '+missing.join(', ')+'. Bei mündlicher oder Heftarbeit prüfst du dein Ergebnis dort.':'Deine Felder sind ausgefüllt. Prüfe jetzt an konkreten Stellen, ob die Aussagen passen.';
 document.getElementById('review-status').textContent=state.revised?'Du hast den Beitrag verändert. Prüfe die Kriterien und deine Entscheidung für diese Fassung erneut.':Object.values(state.criteria).filter(Boolean).length===4?'Du hast die vier Kriterien selbst geprüft. Begründe jetzt deine Entscheidung.':'Hake nur ab, was du an einer Stelle deines Beitrags zeigen kannst.';
}
function invalidateReview(){if(!state.review)return;state.criteria={};state.revised=true;document.querySelectorAll('[data-criterion]').forEach(n=>{n.checked=false;});updateReview();}
main.addEventListener('input',event=>{
 const node=event.target;
 if(node.dataset.note){state.notes[node.dataset.note]=node.value;return;}
 if(node.dataset.draft){
  const key=node.dataset.draft;state.draft[key]=node.value;
  if(key==='headline')document.querySelector('.preview-side #draft-headline').textContent=node.value||'Hier erscheint deine Überschrift';
  if(key==='caption')document.querySelector('.preview-side #draft-caption').textContent=node.value||'Hier erscheint deine Bildunterschrift.';
  invalidateReview();return;
 }
 if(node.dataset.crop){const target=node.dataset.scope==='draft'?state.draft:state;target.crop[node.dataset.crop]=Number(node.value);updateCrop(node.dataset.scope);}
});
main.addEventListener('change',event=>{
 const node=event.target;
 if(node.id==='headline-choice'){state.headline=node.value;updateExperiment();}
 if(node.dataset.bank){
  const bank=node.dataset.bank,answers=bank==='evidence'?state.answers:state.transferAnswers;answers[node.dataset.claim]=node.value;
  if(bank==='evidence')state.checked=false;else state.transferChecked=false;
  document.querySelectorAll('[id^="'+bank+'-feedback-"]').forEach(n=>{n.hidden=true;});
  document.getElementById(bank+'-status').textContent='Auswahl verändert. Prüfe dein Urteil erneut.';
 }
 if(node.hasAttribute('data-calibration')){state.calibration=node.value;state.calibrationChecked=false;document.getElementById('calibration-feedback').hidden=true;}
 if(node.id==='revision-decision'){state.decision=node.value;document.getElementById('revision-next').textContent=revisionNext();}
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
 if(button.dataset.action==='check-evidence'){state.checked=true;showAnswers('evidence');announce('Die Rückmeldungen stehen unter den Aussagen.');}
 if(button.dataset.action==='check-transfer'){state.transferChecked=true;showAnswers('transfer');announce('Die Rückmeldungen stehen unter deinen Urteilen.');}
 if(button.dataset.action==='check-calibration'){state.calibrationChecked=true;showCalibration();announce('Der Begründungsvergleich steht unter der Auswahl.');}
 if(button.dataset.action==='review-draft'){state.review=true;document.getElementById('draft-review').hidden=false;updateReview();document.getElementById('draft-review').scrollIntoView({block:'nearest',behavior:'instant'});announce('Prüfe deinen Beitrag und begründe deine Entscheidung.');}
});
window.addEventListener('hashchange',()=>{if(location.hash==='#main'){main.focus({preventScroll:true});return;}announce('');render(true);});
if(window.LernwerkMantel)window.LernwerkMantel.register({
 capture:()=>({family:'media',state:JSON.parse(JSON.stringify(state)),current}),
 validate:tool=>tool?.family==='media'&&tool.state&&Number.isInteger(tool.current),
 restore:(tool,options={})=>{
  Object.assign(state,JSON.parse(JSON.stringify(tool.state)));
  const target=C.steps.some(s=>s.id===options.step)?options.step:C.steps[tool.current].id;
  history.replaceState(null,'','#'+target);render();
 }
});

render();
})();
