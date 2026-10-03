'use strict';
(()=>{
 const W=window.Workshop,S=window.Studio,L=window.Lesson,P=window.StudioLearning;
 const $=(s,root=document)=>root.querySelector(s),$$=(s,root=document)=>[...root.querySelectorAll(s)];
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const arrows=['↑','→','↓','←'],dirs=['oben','rechts','unten','links'],glyph={vor:'↑',links:'↶',rechts:'↷'};
 let showTrail=false,comparisonStep=0,probeCommands=[];
 const key='ium-lernstudio-v1';
 let data={version:1,current:'start',works:{}},persist=false,timer=null,speed=850,insight=false,editor=null,sequenceFeedback='',angle=0,lastDirection=0;
 if(!window.LernwerkMantel)try{const saved=S.restore(localStorage.getItem(key));if(saved){data=saved;persist=true;}}catch{}
 const hash=location.hash.slice(1);if(S.order.includes(hash))data.current=hash;
 const lesson=()=>P.lesson(data.current),state=()=>data.works[data.current]||(data.works[data.current]=S.fresh(data.current));
 const run=()=>lesson().station?W.station(state().plan):S.run(data.current,state().code);
 function announce(text){$('#announce').textContent=text;}
 function save(){if(window.LernwerkMantel){window.LernwerkMantel.changed();return;}if(!persist)return;try{localStorage.setItem(key,JSON.stringify(data));}catch{persist=false;announce('Speichern ist auf diesem Gerät nicht verfügbar. Deine Arbeit bleibt in diesem geöffneten Fenster erhalten.');}}
 function stop(){clearTimeout(timer);timer=null;const b=$('[data-action="play"]');if(b)b.innerHTML='▶ <span>Starten</span>';}
 function dialog(title,html){
  stop();const overlay=$('#overlay'),active=overlay.open?document.activeElement:null;
  const attr=active?.getAttributeNames().find(n=>n.startsWith('data-')),value=attr?active.getAttribute(attr):null;
  $('#dialog-title').textContent=title;$('#dialog-body').innerHTML=html;
  if(!overlay.open)overlay.showModal();else if(attr){const next=$('#dialog-body').querySelector('['+attr+'="'+CSS.escape(value)+'"]');if(next&&!next.disabled)next.focus();else ($('#dialog-body [data-action="save-block"]')||$('#dialog-body button:not([disabled])'))?.focus();}
 }
 function close(){ $('#overlay').close();editor=null;const panel=$('#block-editor');if(panel){panel.hidden=true;$('.program-panel').classList.remove('editing');$('#toolbox').hidden=false;$$('[data-edit]').forEach(b=>b.disabled=false);$$('.scene-controls [data-editor-disabled]').forEach(control=>{control.disabled=control.dataset.editorDisabled==='true';delete control.dataset.editorDisabled;});}}
 function chapter(){return S.chapters.find(c=>c.ids.includes(data.current));}
 function renderNav(){
  $('#chapters').innerHTML=S.chapters.map((c,i)=>'<button class="chapter" data-go="'+c.ids[0]+'" '+(c===chapter()?'aria-current="step"':'')+'><span class="chapter-number">'+(i+1)+'</span><span>'+c.title+'<small>'+c.caption+'</small></span></button>').join('');
 }
 function navigate(id){stop();if(!S.order.includes(id))return;data.current=id;insight=false;comparisonStep=0;sequenceFeedback='';close();if(window.LernwerkMantel&&location.hash!=='#'+id)history.pushState(null,'','#'+id);else history.replaceState(null,'','#'+id);save();render();$('#main').focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
 function codeHTML(){
  const l=lesson(),s=state();
  if(l.station)return s.plan==='A'?'<div class="block loop"><div class="loop-head">wiederhole <span class="loop-count">3</span> mal</div><div class="body-commands"><span class="command" data-station-action="aufnehmen">aufnehmen</span><span class="command" data-station-action="prüfen">prüfen</span><span class="command" data-station-action="ablegen">ablegen</span></div></div>':['aufnehmen','prüfen','ablegen'].map(a=>'<div class="block loop"><div class="loop-head">wiederhole <span class="loop-count">3</span> mal</div><span class="command" data-station-action="'+a+'">'+a+'</span></div>').join('');
  const blocks=W.blocks(s.code);if(!blocks.length)return '<div class="empty-code">Dein Plan beginnt hier.<br><b>Füge den ersten Baustein hinzu.</b></div>';
  return blocks.map((b,i)=>'<'+(l.editable?'button':'div')+' class="block '+(b.repeat?'loop':'')+'" data-line="'+(i+1)+'" '+(l.editable?'data-edit="'+i+'" aria-label="Baustein '+(i+1)+' bearbeiten: '+esc(b.repeat?'wiederhole '+b.count+' ['+b.body.join('; ')+']':b.body[0])+'"':'')+'>'+(l.editable?'<span class="edit-mark" aria-hidden="true">✎</span>':'')+(b.repeat?'<div class="loop-head"><span class="line-num">'+(i+1)+'</span>wiederhole <span class="loop-count">'+b.count+'</span> mal</div><div class="body-commands">'+b.body.map((a,j)=>'<span class="command" data-body="'+j+'">'+glyph[a]+' '+a+'</span>').join('')+'</div>':'<span class="line-num">'+(i+1)+'</span><span class="command" data-body="0">'+glyph[b.body[0]]+' '+b.body[0]+'</span>')+'</'+(l.editable?'button':'div')+'>').join('');
 }
 function robot(){return '<div class="robot no-motion" id="robot" aria-hidden="true"><svg viewBox="0 0 100 100"><rect x="6" y="32" width="13" height="35" rx="6" fill="#263148"/><rect x="81" y="32" width="13" height="35" rx="6" fill="#263148"/><circle cx="50" cy="52" r="39" fill="#fff" stroke="#d1d5e5" stroke-width="3"/><circle cx="50" cy="52" r="31" fill="#505bcc"/><path d="M50 17 39 34h22z" fill="#fff"/><rect x="31" y="41" width="38" height="20" rx="10" fill="#253065"/><circle cx="41" cy="50" r="3" fill="#d4f7ef"/><circle cx="59" cy="50" r="3" fill="#d4f7ef"/><path d="M39 73h22" stroke="#c7ccf4" stroke-width="3" stroke-linecap="round"/></svg></div>';}
 function floorHTML(){
  const l=lesson();
  if(l.station)return '<div class="machine"><div class="machine-line"><div class="machine-tray"><div class="pieces" id="waiting-pieces"></div>Vorrat</div><span aria-hidden="true">→</span><div class="machine-unit" id="machine-unit"></div><span aria-hidden="true">→</span><div class="machine-tray"><div class="pieces" id="done-pieces"></div>Fertig</div></div><p class="machine-caption" id="machine-caption"></p></div>';
  const {width:w,height:h}=l.room;
  return '<div class="floor-wrap" data-size="'+w+'" style="--cols:'+w+';--rows:'+h+'"><div class="x-labels" aria-hidden="true">'+Array.from({length:w},(_,i)=>'<span>'+(i+1)+'</span>').join('')+'</div><div class="y-labels" aria-hidden="true">'+Array.from({length:h},(_,i)=>'<span>'+(i+1)+'</span>').join('')+'</div><div class="floor" id="floor" role="group" aria-label="Raum mit '+w+' Spalten und '+h+' Reihen">'+Array.from({length:h},(_,y)=>Array.from({length:w},(_,x)=>'<'+(l.predict?'button':'div')+' class="tile '+(l.predict?'predictable':'')+'" data-cell="'+(x+1)+','+(y+1)+'" '+(l.predict?'data-predict="'+(x+1)+','+(y+1)+'"':'role="img"')+' aria-label="Spalte '+(x+1)+', Reihe '+(y+1)+'"></'+(l.predict?'button':'div')+'>').join('')).join('')+'<svg class="path-trail" id="path-trail" aria-hidden="true" preserveAspectRatio="none" hidden></svg>'+robot()+'</div><div class="legend"><span><i></i>noch Krümel</span><span><i class="clean-dot"></i>sauber</span>'+(l.predict?'<span><i class="guess-dot"></i>deine Vermutung</span>':'')+'</div></div>';
 }
 function predictionHTML(){return '<div class="prediction"><div class="prediction-label"><b>Erst vermuten, dann prüfen</b><span id="prediction-label">Tippe auf die Endkachel. Wähle den Blick.</span></div><div class="direction-picks" role="group" aria-label="Vermutete Blickrichtung">'+dirs.map((d,i)=>'<button data-direction="'+i+'" aria-label="Vermuteter Blick: '+d+'" aria-pressed="false">'+arrows[i]+'</button>').join('')+'</div></div>';}
 function render() {
  const l=lesson(),s=state(),c=chapter(),i=S.order.indexOf(l.id);
  renderNav();
  $('#main').innerHTML=`<section class="lesson-intro" aria-labelledby="lesson-title">
   <div class="intro-copy"><p class="eyebrow">Sauber geplant · ${c.title}</p><h1 id="lesson-title">${l.title}</h1><p>${l.task}</p></div>
   <div class="lesson-position">Station ${i+1} von 11<div class="station-dots" aria-hidden="true">${c.ids.map(id=>`<span class="${id===l.id?'current':''}"></span>`).join('')}</div></div></section>
   <div class="entry-strip"><details><summary>Das brauchst du für diese Station</summary><p>${l.entry}</p><p>Schon gemeinsam besprochen? Wähle im <button class="text-button" data-action="map">Lernweg</button> direkt deine nächste Übung. Du kannst jederzeit zurück.</p></details><a href="wissen.html#${l.id}" target="_blank" rel="noopener">Wissen nachlesen ↗</a></div>
   ${l.id==='start'?'<details class="probe"><summary>Neu hier? Probiere erst einzelne Befehle aus.</summary><p>Beobachte Kachel und Blick. Dieser kleine Versuch gehört noch nicht zur Aufgabe.</p><div id="probe-content"></div></details>':''}
   <p class="core-sentence"><b>Merke</b> ${l.core}</p>
   <div class="workbench">
    <section class="program-panel" aria-labelledby="program-title"><div class="panel-heading"><h2 id="program-title" tabindex="-1">${l.editable?'Dein Programm':'Das Programm'}</h2>${l.station?`<div class="plan-picker"><button data-plan="A" aria-pressed="${s.plan==='A'}">A</button><button data-plan="B" aria-pressed="${s.plan==='B'}">B</button></div>`:`<small>${l.editable?'Tippen zum Bearbeiten':'Von oben nach unten'}</small>`}</div>
    <p class="program-caption">${l.station?'Vergleiche Plan A und B.':l.editable?'Baue, prüfe und verbessere deinen Weg.':'Die Markierung zeigt den ausgeführten Befehl.'}</p>
    <div class="code-list" id="code-list">${codeHTML()}</div>
    ${l.editable?`<div class="toolbox" id="toolbox">${['vor','links','rechts'].map(a=>`<button data-add="${a}" aria-label="${a} zum Programm hinzufügen">+ ${glyph[a]} ${a}</button>`).join('')}<button data-add="loop">+ Schleife</button></div><section id="block-editor" class="inline-editor" hidden aria-labelledby="editor-title"></section>`:''}
    ${l.predict?predictionHTML():''}
    <div class="program-footer">${l.station?'<p>Ein Platz: aufnehmen, prüfen, ablegen.</p>':'<div class="command-guide"><span><b>↑ vor</b> · eine Kachel in Blickrichtung</span><span><b>↶ links / ↷ rechts</b> · auf der Stelle drehen</span></div>'}
    <div class="support-buttons"><button data-action="hint">Einen Hinweis</button><button data-action="insight" aria-expanded="${insight}" aria-controls="insight">Erklärung öffnen</button></div><div id="hint-region"></div>
    ${l.editable?`<div class="button-row"><button class="quiet small" data-action="undo" ${!s.undo.length?'disabled':''}>↶ Rückgängig</button><button class="quiet small" data-action="raw">Code schreiben</button></div>`:''}</div>
    <section class="insight context-explanation" id="insight" ${insight?'':'hidden'} aria-labelledby="insight-title"><div class="insight-header"><h2 id="insight-title" tabindex="-1">So funktioniert es</h2><button data-action="insight" aria-label="Erklärung schließen">×</button></div><article>${l.explain}</article><details id="solution"><summary>Eine Lösung nachvollziehen</summary><pre>${esc(l.solution)}</pre></details><a href="wissen.html#${l.id}" target="_blank" rel="noopener">In Ruhe nachlesen ↗</a></section></section>
    <section class="scene-panel" aria-labelledby="scene-title"><div class="panel-heading scene-heading"><h2 id="scene-title">${l.station?'Werkstücke prüfen':'Dein Experimentierfeld'}</h2><span class="pill" id="clean-count"></span></div><div class="scene-area">${floorHTML()}</div>
    <div class="scene-controls"><div class="play-row"><button class="primary" data-action="play">▶ <span>Starten</span></button><button class="icon-button" data-action="back" aria-label="Einen Schritt zurück">‹</button><button data-action="step">Schritt ›</button><span class="step-count" id="step-count"></span></div><div class="readout" id="readout" role="status" aria-live="off"></div>
    <div class="timeline"><label for="timeline">Ablauf untersuchen</label><input id="timeline" type="range" min="0" max="1" value="0" aria-label="Schritt im Ablauf"></div>
    <div class="secondary-controls"><button data-action="reset">↺ Zum Start</button>${!l.station?'<button data-action="cycle">Ein Durchlauf</button><label class="trail-label"><input id="show-trail" type="checkbox" '+(showTrail?'checked':'')+'> Spur</label>':''}<label>Tempo <select id="speed" aria-label="Simulationstempo"><option value="1300">Ruhig</option><option value="850">Normal</option><option value="450">Zügig</option></select></label></div></div></section>
   </div><div id="result-region"></div><div id="compare-region"></div>
   <div class="below-workspace"><section class="think-card" aria-labelledby="think-title"><p class="eyebrow">Jetzt erklärst du</p><h2 id="think-title">${l.id==='own'?'Begründe deinen Weg.':'Was steckt dahinter?'}</h2><p>${l.question}</p>
   ${l.sequence?`<div class="sequence-editor"><b>${l.id==='loop'?'Zwei Durchläufe ausschreiben':'Die ganze Folge ausschreiben'}</b><div class="sequence-output" id="sequence-output"></div><div class="button-row">${['vor','links','rechts'].map(a=>`<button class="small" data-sequence="${a}">${glyph[a]} ${a}</button>`).join('')}<button class="small" data-action="sequence-check">Folge prüfen</button></div><p id="sequence-feedback" role="status"></p></div>`:''}
   <p class="sentence-starter"><b>So kannst du anfangen:</b> ${l.prompt}</p><details class="explain-criteria"><summary>Prüfe deine Erklärung</summary><ul>${l.criteria.map(x=>`<li>${x}</li>`).join('')}</ul><p>Erkläre mündlich, im Heft oder hier. Vergleiche mit den Kriterien. Das Lernstudio bewertet deine Erklärung nicht automatisch.</p></details>
   <details class="note-details"><summary>Meine Erklärung aufschreiben</summary><label class="sr-only" for="note">Meine Erklärung zu dieser Station</label><textarea id="note" maxlength="2000" placeholder="${esc(l.prompt)}">${esc(s.note)}</textarea><small>${window.LernwerkMantel?'Du findest deine Erklärung und die Sicherung unter „Deine Arbeit“.':persist?'Wird auf diesem Gerät gespeichert.':'Bleibt in diesem geöffneten Fenster. Speichern ist unter Optionen möglich.'}</small></details>
   <p class="evidence-status" id="task-status"></p><div class="button-row optional-check"><button data-action="check">Zusatzfrage zum Ankreuzen</button><span id="check-status" class="muted"></span></div>
   ${l.id==='own'?'<details class="challenge"><summary>Noch eine Herausforderung: Zwei gültige Wege vergleichen</summary><p>Ein Reihenweg und ein Spaltenweg lösen denselben Auftrag. Vergleiche ihre Teilpläne, Fahrten und Drehungen. Ist weniger Code immer ein kürzerer Weg?</p><a href="wissen.html#wege" target="_blank" rel="noopener">Beide Beispielwege mit Erklärung öffnen ↗</a></details>':''}</section>
   <aside class="continue-card"><p class="eyebrow">${i<10?'Dein nächster Schritt':'Dein Lernprodukt'}</p><h3>${i<10?P.lesson(S.order[i+1]).short:'Ein Plan, den du erklären kannst.'}</h3><p>${i<10?(i===9?'Diese Aufgabe ist für später. Versuche sie nach einer Pause zunächst aus dem Kopf.':'Prüfe deine Erklärung. Gehe danach weiter oder wähle mit deiner Lehrperson eine andere Station.'):'Zeige deinen geprüften Flächenplan und erkläre seine Teilpläne.'}</p><button class="primary" data-go="${i<10?S.order[i+1]:'own'}">${i<10?'Zur nächsten Station →':'Meinen Flächenplan öffnen →'}</button><button class="quiet back-link" data-action="map">Alle Stationen frei wählen</button>${i>0?`<button class="quiet back-link" data-go="${S.order[i-1]}">← Vorige Station</button>`:''}</aside></div>`;
  $('#speed').value=String(speed);paint(true);renderSequence();renderCheckStatus();renderCompare();renderProbe();
 }
 function currentTrace(){const r=run(),s=state();s.step=Math.max(0,Math.min(s.step,r.trace.length-1));return {r,s,t:r.trace[s.step]};}
 function paint(initial=false){
  const l=lesson(),{r,s,t}=currentTrace();
  $('#step-count').textContent='Schritt '+s.step+' / '+(l.station?9:(s.code.trim()?L.expand(s.code).length:0));
  $('[data-action="back"]').disabled=s.step===0;$('[data-action="step"]').disabled=s.step===r.trace.length-1;
  const cycle=$('[data-action="cycle"]');if(cycle)cycle.disabled=s.step===r.trace.length-1;
  $$('.command.active,.block.executing').forEach(e=>e.classList.remove('active','executing'));
  if(l.station){
   $('#clean-count').textContent=t.completed+' von 3 fertig';
   const held=t.state!=='frei'?1:0;
   $('#waiting-pieces').innerHTML='<i class="piece"></i>'.repeat(Math.max(0,3-t.completed-held));
   $('#done-pieces').innerHTML='<i class="piece done"></i>'.repeat(t.completed);
   $('#machine-unit').innerHTML=(held?'<i class="piece '+(t.state==='geprüft'?'done':'')+'"></i>':'<span class="muted" style="font-size:.8rem">Platz frei</span>')+'<i class="lamp '+(t.state==='geprüft'?'ready':'')+'"></i>';
   $('#machine-caption').textContent=t.error?'Stopp: Der Platz ist noch belegt.':'Die Station ist '+t.state+'.';
   if(s.step)$('[data-station-action="'+t.action+'"]')?.classList.add('active');
   $('#readout').innerHTML='<span class="action-tag">'+esc(t.action)+'</span><span>'+(t.error?'Zweites Aufnehmen geht hier nicht.':t.state==='frei'?'Bereit für ein neues Werkstück.':t.state==='belegt'?'Das Werkstück wartet auf die Prüfung.':'Geprüft. Jetzt kann es abgelegt werden.')+'</span>';
  }else{
   const {width:w,height:h}=l.room;
   $('#clean-count').textContent=t.cleaned.length+' / '+(w*h)+' sauber';
   $$('.tile').forEach(tile=>{const xy=tile.dataset.cell,clean=t.cleaned.includes(xy),p=s.prediction,pred=p&&p.slice(0,2).join()===xy;tile.classList.toggle('clean',clean);tile.classList.toggle('predicted',Boolean(pred));tile.dataset.arrow=p?arrows[p[2]]:'';tile.setAttribute('aria-label','Spalte '+xy[0]+', Reihe '+xy[2]+', '+(clean?'sauber':'noch Krümel')+(pred?', deine Vermutung: Blick '+dirs[p[2]]:''));if(l.predict){tile.setAttribute('aria-pressed',String(Boolean(pred)));tile.disabled=s.step>0;}});
   if(initial){angle=t.pos[2]*90;lastDirection=t.pos[2];}
   else{let delta=t.pos[2]-lastDirection;if(delta>2)delta-=4;if(delta<-2)delta+=4;angle+=delta*90;lastDirection=t.pos[2];}
   const bot=$('#robot');bot.classList.toggle('no-motion',initial);
   bot.style.setProperty('--rx','calc(7px + (100% - 14px - '+(w-1)*5+'px) / '+w+' * '+(t.pos[0]-.5)+' + '+(t.pos[0]-1)*5+'px)');
   bot.style.setProperty('--ry','calc(7px + (100% - 14px - '+(h-1)*5+'px) / '+h+' * '+(t.pos[1]-.5)+' + '+(t.pos[1]-1)*5+'px)');
   bot.style.setProperty('--angle',angle+'deg');
   if(t.line){const block=$('[data-line="'+t.line+'"]');block?.classList.add('executing');$('[data-body="'+(t.bodyIndex||0)+'"]',block)?.classList.add('active');if(block){const list=$('#code-list');if(block.offsetTop<list.scrollTop||block.offsetTop+block.offsetHeight>list.scrollTop+list.clientHeight)list.scrollTop=block.offsetTop-12;}}
   const loop=t.repeat?' · Durchlauf '+t.iteration+' von '+t.count:'';
   $('#readout').innerHTML='<span class="action-tag">'+esc(t.action)+'</span><span>'+(t.error?'Am Rand gestoppt. Der Roboter bleibt stehen.':'Spalte '+t.pos[0]+', Reihe '+t.pos[1]+' · Blick '+dirs[t.pos[2]])+loop+'</span>';
   if(l.predict){$('#prediction-label').textContent=s.prediction?'Spalte '+s.prediction[0]+', Reihe '+s.prediction[1]+' · Blick '+dirs[s.prediction[2]]:'Tippe auf die Endkachel. Wähle den Blick.';$$('[data-direction]').forEach(b=>{b.setAttribute('aria-pressed',String(s.prediction?.[2]===Number(b.dataset.direction)));b.disabled=s.step>0;});}
  }
  if(s.step===r.trace.length-1&&s.step>0){s.observed=true;if(l.station&&!s.compared.includes(s.plan))s.compared.push(s.plan);showResult();save();}else $('#result-region').innerHTML='';
  const timeline=$('#timeline');timeline.max=r.trace.length-1;timeline.value=s.step;timeline.disabled=r.trace.length<2;timeline.setAttribute('aria-valuetext','Schritt '+s.step+' von '+(r.trace.length-1));
  paintTrail(r,s);renderCheckStatus();
 }
 function showResult(){
  const l=lesson(),s=state();let title,message,warning=false;
  if(l.station){const r=run();warning=Boolean(r.error);title=warning?'Plan B stoppt beim zweiten Aufnehmen.':'Plan A bearbeitet alle drei Werkstücke.';message=warning?'Ein Werkstück liegt noch auf der Station. Vergleiche mit Plan A: Wann wird der Platz frei?':'Jeder Durchlauf macht den Platz wieder frei. Vergleiche jetzt mit Plan B.';}
  else{
   const a=W.assess(l.id,s.code);({title,message}=a);warning=!a.ok;
   if(l.predict&&s.prediction){const ok=S.prediction(l.id,s.prediction);title=ok?'Deine Vermutung passt – Ort und Blick stimmen.':'Vergleiche deine Vermutung mit dem Ende.';warning=!ok;message=ok?'Erkläre jetzt, welche Anweisung den Blick verändert und welche den Ort.':'Deine Markierung bleibt sichtbar. Gehe schrittweise zurück und suche die erste Abweichung.';}
   else if(l.predict)message='Das Ende ist sichtbar. Gehe zurück zum Start und erkläre jeden Schritt. Bei der nächsten Aufgabe: erst eine Vermutung festhalten.';
  }
  $('#result-region').innerHTML='<section class="result '+(warning?'warning':'')+'" aria-label="Rückmeldung zur Fahrt"><span class="result-icon" aria-hidden="true">'+(warning?'!':'✓')+'</span><div><h3>'+title+'</h3><p>'+message+'</p></div></section>';
 }
 function tick(manual=false){
  const r=run(),s=state();if(s.step<r.trace.length-1)s.step++;paint();
  if(manual)announce($('#readout').textContent);
  if(s.step>=r.trace.length-1){stop();announce($('#result-region').textContent);}save();
 }
 function animateTo(end){
  const next=()=>{tick();if(state().step<end){timer=setTimeout(next,speed);$('[data-action="play"]').innerHTML='Ⅱ <span>Pause</span>';}else stop();};
  timer=setTimeout(next,speed);$('[data-action="play"]').innerHTML='Ⅱ <span>Pause</span>';
 }
 function play(){if(timer){stop();return;}const r=run();if(r.trace.length<2){announce('Füge zuerst einen Befehl zu deinem Plan hinzu.');return;}if(state().step>=r.trace.length-1){state().step=0;$('#code-list').scrollTop=0;paint(true);}animateTo(r.trace.length-1);}
 function updateCode(text){
  stop();const s=state();if(s.step>0){const t=currentTrace().t;s.previous={code:s.code,step:s.step,pos:t.pos,cleaned:t.cleaned.length,error:Boolean(t.error)};}
  S.change(s,text);comparisonStep=0;save();render();$('#program-title').focus({preventScroll:true});announce('Programm geändert. Prüfe den neuen Weg vom Start aus.');
 }
 function renderCheckStatus() {
  const s=state(),check=$('#check-status'),task=$('#task-status'),e=P.evidence(data.current,s);
  if(task){task.textContent=e.label+' · Eigene Erklärung mit den Kriterien prüfen.';task.dataset.kind=e.kind;}
  if(check)check.textContent=s.checked?'Zusatzfrage richtig beantwortet.':'';
 }
 function renderSequence(){const el=$('#sequence-output');if(!el)return;const s=state();el.innerHTML=s.sequence.length?s.sequence.map((a,i)=>'<button data-remove-sequence="'+i+'" aria-label="Anweisung '+(i+1)+' '+a+' entfernen">'+a+' <span aria-hidden="true">×</span></button>').join(''):'<span class="muted" style="font-size:.8rem">Tippe die Befehle in ihrer Reihenfolge an.</span>';$('#sequence-feedback').textContent=sequenceFeedback;renderCheckStatus();}
 function renderCompare() {
  const p=state().previous,el=$('#compare-region');if(!el||!p)return;
  el.innerHTML='<details class="compare-panel"><summary>Vorher und jetzt: Was bewirkt deine Änderung?</summary><p>Beide Bilder zeigen denselben Schritt. Ein beendeter oder gestoppter Versuch bleibt bei seinem letzten Zustand stehen.</p><label for="compare-step">Gemeinsamer Schritt <output id="comparison-number">0</output></label><input id="compare-step" type="range" min="0" value="0"><div id="comparison-views" class="comparison-views"></div><p>Wo unterscheiden sich die Versuche zum ersten Mal? Erkläre die Wirkung deiner Änderung.</p></details>';
  paintComparison();
 }
 function showCheck(){
  const id=data.current,q=S.checks[id],s=state(),chosen=s.choice;
  dialog('Zusatzfrage zum Ankreuzen','<p class="eyebrow">'+esc(lesson().short)+'</p><h3>'+q.prompt+'</h3><div class="check-options">'+q.options.map((a,i)=>'<button class="check-option '+(chosen===i&&s.checked?'correct':'')+'" data-answer="'+i+'" aria-pressed="'+(chosen===i)+'"><span class="option-letter">'+['A','B','C'][i]+'</span>'+a+'</button>').join('')+'</div>'+
  (chosen!==null?'<div class="feedback '+(!s.checked?'wrong':'')+'" role="status"><b>'+(s.checked?'Das passt.':'Denk noch einmal nach.')+'</b> '+q.feedback[chosen]+'</div>':'<p class="muted">Entscheide zuerst aus dem Kopf. Nutze danach bei Bedarf die Erklärung.</p>')+
  (s.checked?'<p class="muted">'+(s.independent?'Beim ersten Versuch ohne geöffnete Hilfe gelöst.':'Mit Unterstützung oder nach einem weiteren Versuch gelöst.')+' Das zeigt diesen einzelnen Check – erkläre das Prinzip zusätzlich in eigenen Worten.</p>':'')+
  '<div class="button-row"><button data-action="close" class="primary">Zurück zum Experiment</button><button data-action="check-help">Erklärung öffnen</button></div>');
 }
 function showMap() {
  dialog('Dein Lernweg', '<p>Alle Stationen sind frei wählbar. Arbeite der Reihe nach oder steige dort ein, wo ihr im Unterricht seid. Die Rückmeldung zeigt deinen Versuch. Deine eigene Erklärung gehört dazu; eine Zusatzfrage ersetzt sie nicht.</p>'+S.chapters.map((c,i)=>'<section class="map-chapter"><h3>'+String(i+1).padStart(2,'0')+' · '+c.title+'</h3>'+c.ids.map(id=>'<button class="map-row" data-go="'+id+'" '+(id===data.current?'aria-current="step"':'')+'><span>'+P.lesson(id).short+'</span><small>'+P.evidence(id,data.works[id]).label+'</small></button>').join('')+'</section>').join(''));
 }
 function showSettings(){
  dialog('Dein Lernstudio','<label class="storage-row"><input type="checkbox" id="persist" '+(persist?'checked':'')+'><span><b>Auf diesem Gerät speichern</b><br><small>Optional. Ohne Häkchen bleibt deine Arbeit nur im geöffneten Fenster. Auf geteilten Schul-iPads anschließend löschen.</small></span></label><button data-action="forget">Gespeicherten Lernstand löschen</button><p id="storage-feedback" class="muted" style="margin-top:10px"></p><h3 style="margin:24px 0 8px">Die Fassungen vergleichen</h3><nav class="variant-list" aria-label="Weitere Fassungen"><a href="../m06-lernwerkstatt/index.html">Lernwerkstatt</a><a href="../m06-reinigungsfall-v2/index.html">Interaktiver Reinigungsfall</a><a href="../m06-selbstlernen/index.html">Selbstlernstrecke</a><a href="../m06-selbstlernen/read.html">Ausführliche Lesefassung</a><a href="../m06-lernfassung3/index.html">Lernfassung 3</a></nav>');
 }
 function showEditor(index,type) {
  stop();const bs=W.blocks(state().code);
  editor={index,indexNew:index===bs.length,block:index<bs.length?structuredClone(bs[index]):{repeat:type==='loop',count:type==='loop'?2:1,body:['vor']}};
  $$('.scene-controls button,.scene-controls input,.scene-controls select').forEach(control=>{control.dataset.editorDisabled=String(control.disabled);control.disabled=true;});
  editorHTML();$('#editor-title').focus({preventScroll:true});
 }
 function editorHTML() {
  const e=editor,b=e.block,el=$('#block-editor'),active=el.contains(document.activeElement)?document.activeElement:null;
  const attr=active?.getAttributeNames().find(n=>n.startsWith('data-')),value=attr?active.getAttribute(attr):null;
  el.hidden=false;$('.program-panel').classList.add('editing');$('#toolbox').hidden=true;
  $$('[data-edit]').forEach(button=>button.disabled=true);
  el.innerHTML=`<div class="inline-heading"><h3 id="editor-title" tabindex="-1">${e.indexNew?'Neue Schleife':'Baustein '+(e.index+1)+' ändern'}</h3><button data-action="cancel-editor" aria-label="Bearbeitung abbrechen">×</button></div>
   ${b.repeat?`<p>Wiederhole die ganze Gruppe in der Klammer.</p><p class="editor-label">Wie viele Durchläufe?</p><div class="count-picker"><button data-count="-1" aria-label="Ein Durchlauf weniger" ${b.count<=2?'disabled':''}>−</button><output>${b.count}</output><button data-count="1" aria-label="Ein Durchlauf mehr" ${b.count>=9?'disabled':''}>+</button></div><p class="editor-label">Befehle in der Klammer · Tippen entfernt einen Befehl</p><div class="body-editor"><div class="body-commands">${b.body.map((a,i)=>`<button data-body-remove="${i}" aria-label="Befehl ${i+1} ${a} entfernen">${glyph[a]} ${a} ×</button>`).join('')}</div><div class="button-row">${['vor','links','rechts'].map(a=>`<button data-body-add="${a}" ${b.body.length>=5?'disabled':''}>+ ${a}</button>`).join('')}</div></div>`:`<p>Welcher Befehl soll hier stehen?</p><div class="button-row">${['vor','links','rechts'].map(a=>`<button data-single="${a}" aria-pressed="${b.body[0]===a}">${glyph[a]} ${a}</button>`).join('')}</div>`}
   <p id="editor-error" class="field-error" role="status"></p><div class="editor-actions">${!e.indexNew?`<button data-action="delete-block" class="danger">Entfernen</button><button data-move="-1" aria-label="Baustein nach oben" ${e.index===0?'disabled':''}>↑</button><button data-move="1" aria-label="Baustein nach unten" ${e.index===W.blocks(state().code).length-1?'disabled':''}>↓</button>`:''}<button data-action="save-block" class="primary">Übernehmen</button><button data-action="cancel-editor">Abbrechen</button></div>`;
  if(attr){const next=el.querySelector('['+attr+'="'+CSS.escape(value)+'"]');if(next&&!next.disabled)next.focus({preventScroll:true});else $('[data-action="save-block"]',el).focus({preventScroll:true});}
 }
 function showInsight(open=true) {
  stop();insight=open;$('#insight').hidden=!open;
  $$('[aria-controls="insight"]').forEach(b=>{b.setAttribute('aria-expanded',String(open));b.textContent=open?'Erklärung schließen':'Erklärung öffnen';});
  if(open){state().help=Math.max(state().help,2);save();$('#insight-title').focus();}
  else $('[data-action="insight"]').focus({preventScroll:true});
 }
 function miniFloor(l,t,label) {
  const w=l.room.width,h=l.room.height;
  return `<div class="mini-floor" style="--cols:${w};--rows:${h}" role="img" aria-label="${esc(label)}: Spalte ${t.pos[0]}, Reihe ${t.pos[1]}, Blick ${dirs[t.pos[2]]}; ${t.cleaned.length} ${t.cleaned.length===1?'Kachel':'Kacheln'} sauber"><div class="mini-tiles">${Array.from({length:h},(_,y)=>Array.from({length:w},(_,x)=>`<span class="mini-tile ${t.cleaned.includes((x+1)+','+(y+1))?'clean':''}"><small>${x+1},${y+1}</small>${t.pos[0]===x+1&&t.pos[1]===y+1?`<b>${arrows[t.pos[2]]}</b>`:''}</span>`).join('')).join('')}</div></div>`;
 }
 function paintComparison() {
  const p=state().previous;if(!p||!$('#compare-step'))return;
  const pair=P.compare(data.current,p.code,state().code,comparisonStep);
  $('#comparison-number').textContent=pair.step;const slider=$('#compare-step');slider.max=pair.max;slider.value=pair.step;slider.setAttribute('aria-valuetext','Schritt '+pair.step+' von '+pair.max);
  $('#comparison-views').innerHTML=[['Vorher',pair.before,p.code],['Jetzt',pair.after,state().code]].map(([name,part,code])=>`<section><h3>${name} · Schritt ${part.step}${part.ended?(part.trace.error?' · Stopp':' · Ende'):''}</h3>${miniFloor(lesson(),part.trace,name)}<p>Spalte ${part.trace.pos[0]}, Reihe ${part.trace.pos[1]} · Blick ${dirs[part.trace.pos[2]]}<br>${part.trace.cleaned.length} ${part.trace.cleaned.length===1?'Kachel':'Kacheln'} sauber · ${esc(part.trace.action)}</p><details><summary>Programm ${name.toLowerCase()}</summary><pre>${esc(code)}</pre></details></section>`).join('');
 }
 function paintTrail(r,s) {
  const svg=$('#path-trail');if(!svg)return;svg.toggleAttribute('hidden',!showTrail);
  const positions=r.trace.slice(0,s.step+1).map(t=>t.pos).filter((p,i,a)=>i===0||p[0]!==a[i-1][0]||p[1]!==a[i-1][1]);
  const w=lesson().room.width,h=lesson().room.height;
  svg.setAttribute('viewBox',`0 0 ${w*100} ${h*100}`);
  svg.innerHTML=`<polyline points="${positions.map(p=>(p[0]*100-50)+','+(p[1]*100-50)).join(' ')}" fill="none" stroke="#515ca4" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>`;
 }
 function renderProbe() {
  const el=$('#probe-content');if(!el)return;
  const r=S.run('start',probeCommands.join('\n')),t=r.trace.at(-1),stopped=r.status==='wall';
  el.innerHTML=`<div class="probe-layout">${miniFloor(P.lesson('start'),t,'Befehle ausprobieren')}<div><p><b>${esc(t.action)}</b>: Spalte ${t.pos[0]}, Reihe ${t.pos[1]} · Blick ${dirs[t.pos[2]]}</p><div class="button-row">${['vor','links','rechts'].map(a=>`<button data-probe="${a}" ${stopped||probeCommands.length>=20?'disabled':''}>${glyph[a]} ${a}</button>`).join('')}<button data-action="reset-probe">Neu probieren</button></div><p>${stopped?'Am Rand gestoppt. Beginne neu und drehe vor der nächsten Fahrt.':probeCommands.length>=20?'Genug probiert? Beginne neu oder löse jetzt die Aufgabe.':'Drehungen ändern den Blick. Nur vor ändert die Kachel.'}</p></div></div>`;
 }

 document.addEventListener('click',event=>{
  const target=event.target.closest('button');if(!target)return;
  if(target.dataset.go){navigate(target.dataset.go);return;}
  if(target.dataset.probe){probeCommands.push(target.dataset.probe);renderProbe();const next=$('[data-probe="'+target.dataset.probe+'"]');(next.disabled?$('[data-action="reset-probe"]'):next).focus({preventScroll:true});announce($('.probe-layout p').textContent);return;}
  if(target.dataset.predict){stop();const xy=target.dataset.predict.split(',').map(Number);state().prediction=[...xy,state().prediction?.[2]??lesson().room.start[2]];save();paint();return;}
  if(target.dataset.direction!==undefined){stop();const s=state(),xy=s.prediction?.slice(0,2)||lesson().room.start.slice(0,2);s.prediction=[...xy,Number(target.dataset.direction)];save();paint();return;}
  if(target.dataset.plan){stop();state().plan=target.dataset.plan;state().step=0;save();render();return;}
  if(target.dataset.edit!==undefined){showEditor(Number(target.dataset.edit));return;}
  if(target.dataset.add){const bs=W.blocks(state().code);if(bs.length>=30){announce('Der Plan hat bereits 30 Bausteine. Fasse passende Befehle in einer Schleife zusammen.');return;}if(target.dataset.add==='loop')showEditor(bs.length,'loop');else{bs.push({body:[target.dataset.add],count:1,repeat:false});updateCode(W.code(bs));$('#code-list').scrollTop=$('#code-list').scrollHeight;$('[data-add="'+target.dataset.add+'"]').focus({preventScroll:true});}return;}
  if(target.dataset.count){editor.block.count=Math.max(2,Math.min(9,editor.block.count+Number(target.dataset.count)));editorHTML();return;}
  if(target.dataset.bodyRemove!==undefined){editor.block.body.splice(Number(target.dataset.bodyRemove),1);editorHTML();return;}
  if(target.dataset.bodyAdd){if(editor.block.body.length>=5)return;editor.block.body.push(target.dataset.bodyAdd);editorHTML();return;}
  if(target.dataset.single){editor.block.body=[target.dataset.single];editorHTML();return;}
  if(target.dataset.move){if(!editor.block.body.length){$('#editor-error').textContent='Füge zuerst einen Befehl zum Körper hinzu.';return;}const bs=W.blocks(state().code),i=editor.index,n=i+Number(target.dataset.move);if(n<0||n>=bs.length)return;bs[i]=editor.block;[bs[i],bs[n]]=[bs[n],bs[i]];close();updateCode(W.code(bs));return;}
  if(target.dataset.answer!==undefined){S.answer(data.current,state(),Number(target.dataset.answer));save();showCheck();$('[data-answer="'+state().choice+'"]').focus();renderCheckStatus();return;}
  if(target.dataset.sequence){if(state().sequence.length<30)state().sequence.push(target.dataset.sequence);sequenceFeedback='';renderSequence();save();return;}
  if(target.dataset.removeSequence!==undefined){state().sequence.splice(Number(target.dataset.removeSequence),1);sequenceFeedback='';renderSequence();save();return;}
  const action=target.dataset.action,s=state();
  switch(action){
   case 'cancel-editor':close();$('#program-title').focus({preventScroll:true});break;
   case 'reset-probe':probeCommands=[];renderProbe();$('[data-probe="vor"]').focus({preventScroll:true});break;
   case 'play':play();break;
   case 'step':stop();tick(true);break;
   case 'back':stop();s.step=Math.max(0,s.step-1);paint(true);announce($('#readout').textContent);break;
   case 'reset':stop();s.step=0;$('#code-list').scrollTop=0;paint(true);announce('Wieder am Start. Dein Programm und deine Vermutung bleiben erhalten.');break;
   case 'cycle':{
    stop();const r=run();let n=Math.min(s.step+1,r.trace.length-1);const first=r.trace[n];
    if(first?.repeat){while(n+1<r.trace.length&&r.trace[n+1].line===first.line&&r.trace[n+1].iteration===first.iteration)n++;}
    animateTo(n);break;
   }
   case 'hint':{
    stop();s.help=Math.min(3,s.help+1);const index=Math.min(s.help-1,1);$('#hint-region').innerHTML='<div class="hint"><b>Hinweis '+(index+1)+'</b><p>'+lesson().hints[index]+'</p>'+(index===0?'<button data-action="hint">Noch einen Hinweis</button>':'<button data-action="insight">Ausführlich verstehen</button>')+'</div>';save();break;
   }
   case 'insight':showInsight(!insight);break;
   case 'back-to-work':$('.workbench').scrollIntoView({behavior:'instant',block:'start'});$('[data-action="play"]').focus({preventScroll:true});break;
   case 'check-help':close();showInsight();break;
   case 'map':showMap();break;
   case 'check':showCheck();break;
   case 'settings':showSettings();break;
   case 'close':close();break;
   case 'about':dialog('Ein Modell zum Denken','<p>In diesem Lernstudio lernst du, Befehle zu ordnen, ganze Gruppen zu wiederholen und einen eigenen Flächenplan zu begründen.</p><p>Der Boden besteht aus Kacheln. Die Startkachel ist bereits sauber. <b>vor</b> fährt eine Kachel; <b>links</b> und <b>rechts</b> drehen auf der Stelle. Am Rand stoppt der Versuch. Der Roboter besitzt hier keine Sensoren. Die Prüfstation hat genau einen Platz.</p><p>Die Gestaltung nutzt klare Teilaufgaben, räumlich zugeordnetes Feedback, ausgearbeitete Beispiele, abnehmende Hilfen und Abrufübungen. Diese Fassung ist ein erprobbarer Prototyp. Ihre Wirkung auf das Lernen muss im Unterricht untersucht werden.</p><button data-action="close" class="primary">Zurück zum Lernstudio</button>');break;
   case 'undo':if(s.undo.length){const code=s.undo.pop(),stack=[...s.undo];updateCode(code);state().undo=stack;save();render();}break;
   case 'raw':dialog('Deinen Plan als Code schreiben','<p>Eine Anweisung pro Zeile. Eine Schleife sieht so aus: <code>wiederhole 3 [vor; links]</code>. Ohne verschachtelte Schleifen, mit 2 bis 9 Durchläufen.</p><label class="sr-only" for="raw-code">Programmcode</label><textarea id="raw-code" maxlength="2500" spellcheck="false" autocapitalize="off">'+esc(s.code)+'</textarea><p id="raw-error" class="field-error" role="status"></p><button class="primary" data-action="save-raw">Programm übernehmen</button>');break;
   case 'save-raw':{try{const text=W.code(W.blocks($('#raw-code').value));if(W.blocks(text).length>30)throw new Error('Nutze höchstens 30 Bausteine.');S.run(data.current,text);close();updateCode(text);}catch(e){$('#raw-error').textContent=e.message;}break;}
   case 'save-block':{if(!editor.block.body.length){$('#editor-error').textContent='Füge mindestens einen Befehl zum Körper hinzu.';return;}const bs=W.blocks(s.code);bs[editor.index]=editor.block;const text=W.code(bs);close();updateCode(text);break;}
   case 'delete-block':{const bs=W.blocks(s.code);bs.splice(editor.index,1);close();updateCode(W.code(bs));break;}
   case 'sequence-check':{const result=L.compare(s.sequence.join(' '),lesson().sequence);sequenceFeedback=result.ok?'Die Folge passt. Erkläre nun, wo ein Durchlauf endet.':!s.sequence.length?'Schreibe zuerst die Anweisungen mit den drei Tasten aus.':'Die Folge passt noch nicht. Prüfe Anweisung '+(result.index+1)+': Was kommt dort nach dem Programm?';renderSequence();announce(sequenceFeedback);break;}
   case 'forget':{try{localStorage.removeItem(key);persist=false;$('#persist').checked=false;$('#storage-feedback').textContent='Der gespeicherte Lernstand wurde gelöscht. Die aktuelle Arbeit bleibt bis zum Schließen dieses Fensters erhalten.';}catch{$('#storage-feedback').textContent='Der Gerätespeicher ist nicht zugänglich.';}break;}
  }
 });
 document.addEventListener('change',event=>{
  if(event.target.id==='show-trail'){showTrail=event.target.checked;paint(true);return;}
  if(event.target.id==='speed'){speed=Number(event.target.value);return;}
  if(event.target.id==='persist'){
   persist=event.target.checked;
   if(persist){save();$('#storage-feedback').textContent=persist?'Der Lernstand wird nur auf diesem Gerät gespeichert.':'Speichern ist auf diesem Gerät nicht verfügbar.';event.target.checked=persist;}
   else {try{localStorage.removeItem(key);}catch{}$('#storage-feedback').textContent='Speichern ist aus. Die bisherige gespeicherte Kopie wurde entfernt.';}
  }
 });
 document.addEventListener('input',event=>{if(event.target.id==='timeline'){stop();state().step=Number(event.target.value);paint(true);return;}if(event.target.id==='compare-step'){comparisonStep=Number(event.target.value);paintComparison();return;}if(event.target.id==='note'){state().note=event.target.value;save();}});
 document.addEventListener('toggle',event=>{if(event.target.id==='solution'&&event.target.open){state().help=3;save();}},true);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 window.addEventListener('pagehide',()=>{stop();save();});
 window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(S.order.includes(id))navigate(id);});
 $('#overlay').addEventListener('click',event=>{if(event.target===$('#overlay')){const b=$('#overlay').getBoundingClientRect();if(event.clientX<b.left||event.clientX>b.right||event.clientY<b.top||event.clientY>b.bottom)close();}});
 function validateMantel(tool){
  try{if(!tool||tool.family!=='algorithm'||!tool.data||tool.data.version!==1)return false;
   for(const [id,s]of Object.entries(tool.data.works)){if(!S.order.includes(id))return false;const trace=P.lesson(id).station?W.station(s.plan):S.run(id,s.code);if(s.step>=trace.trace.length)return false;}
   return true;
  }catch{return false;}
 }
 if(window.LernwerkMantel)window.LernwerkMantel.register({
  capture:()=>({family:'algorithm',data:JSON.parse(JSON.stringify(data)),display:{showTrail,speed,comparisonStep,rawDraft:$('#raw-code')?.value??null,editor:editor?JSON.parse(JSON.stringify(editor)):null}}),
  validate:validateMantel,flush:stop,
  restore:(tool,options={})=>{
   if(!validateMantel(tool))throw new Error('Unvereinbarer Programmstand');
   data=JSON.parse(JSON.stringify(tool.data));persist=false;
   if(S.order.includes(options.step))data.current=options.step;
   showTrail=tool.display?.showTrail===true;speed=Number.isFinite(tool.display?.speed)?tool.display.speed:850;comparisonStep=Number.isInteger(tool.display?.comparisonStep)?tool.display.comparisonStep:0;
   history.replaceState(null,'','#'+data.current);render();
   if(tool.display?.editor){const x=tool.display.editor;showEditor(x.index,x.block.repeat?'loop':'single');editor=JSON.parse(JSON.stringify(x));editorHTML();}
   if(typeof tool.display?.rawDraft==='string'){dialog('Deinen Plan als Code weiterschreiben','<label for="raw-code">Programmcode</label><textarea id="raw-code" maxlength="2500" spellcheck="false">'+esc(tool.display.rawDraft)+'</textarea><p id="raw-error" role="status"></p><button class="primary" data-action="save-raw">Programm übernehmen</button>');}
  }
 });

 render();
})();
