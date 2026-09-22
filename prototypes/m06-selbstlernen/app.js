'use strict';
(()=>{
 const M=window.Lesson,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const escape=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  const key=document.body.dataset.storageKey||'ium-schleifen-selbstlernen-v1';let state=M.freshState(),remember=false,dirty=false,previousPage='start',pending=null,lastExecution=null,knowledgeReturn=null;
 const saveStatus=$('#save-status');
 try{const raw=localStorage.getItem(key);if(raw){state=M.decode(raw);remember=true;$('#restore-notice').textContent='Dein gesicherter Stand ist wieder da. Deine Antworten und dein Programm kannst du weiterbearbeiten.';}}
 catch{ $('#restore-notice').textContent='Eine gespeicherte Sicherung konnte nicht geladen werden. Du kannst weiterarbeiten oder eine Sicherungsdatei öffnen.';}
 document.documentElement.classList.add('js');
 function persist(){if(remember){try{localStorage.setItem(key,M.encode(state));dirty=false;saveStatus.textContent='Aktueller Stand in diesem Browser gespeichert.';}catch{dirty=true;saveStatus.textContent='Speichern im Browser hat nicht funktioniert. Lade deinen Stand als Datei herunter.';$('#restore-notice').textContent='Dein Stand konnte nicht im Browser gespeichert werden. Nutze „Stand mitnehmen“ für eine Datei.';}}}
 function change(){dirty=true;persist();}
 function restore(){
  $$('form[data-exercise]').forEach(form=>{const a=state.answers[form.dataset.exercise]||{};form.querySelectorAll('[data-field]').forEach(el=>{if(el.type==='radio')el.checked=a.choice===el.value;else el.value=a[el.dataset.field]||'';});form.querySelector('.feedback').replaceChildren();});
  $('#plan-code').value=state.code;$('#learning-note').value=state.note;$('#remember').checked=remember;
   lastExecution=null;$('#plan-feedback').replaceChildren();$('#own-simulation').replaceChildren();$('#previous-run').hidden=true;
 }
 function showPage(id,focus=false){if(!M.pages.includes(id))return;if(id==='knowledge'&&state.page!=='knowledge')previousPage=state.page;state.page=id;
  $$('.lesson').forEach(s=>s.hidden=s.id!==id);$$('[data-nav]').forEach(a=>{if(a.dataset.nav===id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  $('.mobile-knowledge').href='#'+(id==='knowledge'?previousPage:'knowledge');$('.mobile-knowledge').textContent=id==='knowledge'?'Zurück zur Lernseite':'Wissen nachschlagen';
  document.title=$('#title-'+id).textContent+' · IuM Lernwerk';persist();if(focus){$('#title-'+id).focus({preventScroll:true});window.scrollTo(0,0);}
 }
 window.addEventListener('hashchange',()=>showPage(location.hash.slice(1),true));
 function openKnowledge(trigger,targetId='title-knowledge'){
  const focus=trigger||document.activeElement;knowledgeReturn={page:state.page,scrollY:window.scrollY,focus};previousPage=state.page;
  history.pushState(null,'','#knowledge');showPage('knowledge');
  requestAnimationFrame(()=>{const target=document.getElementById(targetId)||$('#title-knowledge');target.scrollIntoView({block:'start'});target.focus({preventScroll:true});});
 }
 function restoreKnowledgeReturn(){
  const context=knowledgeReturn||{page:previousPage,scrollY:0,focus:null};knowledgeReturn=null;showPage(context.page);history.replaceState(null,'','#'+context.page);
  requestAnimationFrame(()=>{window.scrollTo({top:context.scrollY,left:0,behavior:'auto'});if(context.focus?.isConnected)context.focus.focus({preventScroll:true});else $('#title-'+context.page).focus({preventScroll:true});});
 }
 document.addEventListener('click',event=>{const link=event.target.closest('a[href="#knowledge"], [data-knowledge-target]');if(!link)return;event.preventDefault();if(state.page==='knowledge')restoreKnowledgeReturn();else openKnowledge(link,link.dataset.knowledgeTarget||'title-knowledge');});
 $('#back-from-knowledge').addEventListener('click',restoreKnowledgeReturn);
 restore();showPage(M.pages.includes(location.hash.slice(1))?location.hash.slice(1):state.page);
  function renderSim(el,room,program,options={}){
   const execution=options.execution||M.createExecution(room,program),result=execution.result,blocks=window.CleaningModel.parse(program);let index=options.initial==='end'?execution.index:0;
   el.innerHTML=`<div class="sim-head"><h3>Deine Fahrt untersuchen</h3><span class="step-count"></span></div><details class="sim-program"><summary>Ganzes ausgeführtes Programm</summary><div class="sim-code"></div></details><div class="sim-workbench"><div class="current-instruction"><p class="sim-phase"></p><pre class="current-code"><code></code></pre></div><div class="sim-scene"><div class="board" aria-label="Bodenplan: Spalten von links, Reihen von oben"></div><p class="sim-description" role="status"></p></div><div class="controls"><button type="button" data-action="back" aria-label="Eine Anweisung zurück">← Zurück</button><button type="button" data-action="next" class="primary" aria-label="Eine Anweisung weiter">Weiter →</button></div></div><details class="sim-more"><summary>Weitere Schritte</summary><div class="jump-controls"><button type="button" data-action="reset">Zum Start</button><button type="button" data-action="round">Bis zum Ende des Durchlaufs</button><button type="button" data-action="end">Zum Ergebnis</button></div></details><details><summary>Die ganze Fahrt als Tabelle lesen</summary><div class="table-scroll"><table><thead><tr><th>Schritt</th><th>Anweisung und Wirkung</th></tr></thead><tbody>${result.trace.map((s,i)=>`<tr><th scope="row">${i||'Start'}</th><td>${escape(M.describe(s,room))}</td></tr>`).join('')}</tbody></table></div></details>`;
   function codeLine(block,active){return `${block.repeat?`wiederhole ${block.count} [`:''}${block.body.map((cmd,j)=>`<span class="${active&&active.position===j+1?'active-command':''}">${cmd}</span>`).join('; ')}${block.repeat?']':''}`;}
   function draw(){
    const frame=M.executionFrame(execution,index),s=frame.state,current=frame.current,next=frame.next,active=current||next;index=frame.step;
    const atEnd=frame.step===frame.total,status=frame.step===0?'Start':s.error?'Wandstopp':atEnd?(result.status==='limit'?'Modellgrenze':'Ergebnis'):'Zwischenschritt';
    el.querySelector('.step-count').textContent=`${status} · ${frame.step} / ${frame.total}`;
    const runTitle=el.closest('#previous-run')?.querySelector('#run-title');if(runTitle)runTitle.textContent=atEnd&&frame.step>0?'Ergebnis deines Programms':'Deine Fahrt Schritt für Schritt';
    el.querySelector('.sim-code').innerHTML='<pre><code>'+blocks.map(b=>`<span class="code-line ${active&&active.line===b.line?'active':''}">${codeLine(b,active&&active.line===b.line?active:null)}</span>`).join('')+'</code></pre>';
    const block=blocks.find(b=>b.line===active?.line);
    el.querySelector('.current-code code').innerHTML=block?codeLine(block,active):'Keine Anweisung';
    el.querySelector('.sim-phase').textContent=active?`${current?'Schritt':'Als Erstes'} · Zeile ${active.line}${active.iteration?` · Durchlauf ${active.iteration}/${active.count}${s.error?' abgebrochen':''}`:' · außerhalb der Schleife'}`:'Leeres Programm';
    let cells='<span aria-hidden="true"></span>'+Array.from({length:room.width},(_,i)=>`<span class="axis" aria-hidden="true">${i+1}</span>`).join('');
    for(let y=1;y<=room.height;y++){cells+=`<span class="axis" aria-hidden="true">${y}</span>`;for(let x=1;x<=room.width;x++){const visited=s.cleaned.includes(`${x},${y}`),robot=s.pos[0]===x&&s.pos[1]===y;cells+=`<div class="tile ${visited?'visited':''} ${robot?'robot':''}" role="img" aria-label="Spalte ${x}, Reihe ${y}${visited?', erreicht':''}${robot?', Roboter blickt nach '+M.directions[s.pos[2]]:''}">${visited?'<span class="tick" aria-hidden="true">✓</span>':''}${robot?`<span aria-hidden="true">${['↑','→','↓','←'][s.pos[2]]}</span>`:''}</div>`;}}
    el.querySelector('.board').innerHTML=`<div class="board-grid numbered-grid" style="--cols:${room.width}">${cells}</div>`;
    el.querySelector('.sim-description').textContent=M.describe(s,room,false);
    ['back','reset'].forEach(a=>el.querySelector(`[data-action=${a}]`).disabled=frame.step===0);['next','round','end'].forEach(a=>el.querySelector(`[data-action=${a}]`).disabled=atEnd);
   }
   el.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>{
    const action=button.dataset.action;
    if(action==='reset')index=0;else if(action==='back')index=Math.max(0,index-1);else if(action==='next')index=Math.min(execution.index,index+1);else if(action==='end')index=execution.index;else if(index<execution.index){index++;while(index<execution.index&&result.trace[index].repeat&&result.trace[index].bodyIndex<result.trace[index].bodyLength-1&&!result.trace[index].error)index++;}
    draw();
    if(button.disabled||!['back','next'].includes(action)){const focus=el.querySelector('[data-action=next]:not(:disabled)')||el.querySelector('[data-action=back]:not(:disabled)');focus?.focus({preventScroll:true});}
    const workbench=el.querySelector('.sim-workbench'),rect=workbench.getBoundingClientRect();if(rect.top<8||rect.bottom>window.innerHeight-8)workbench.scrollIntoView({block:'center',behavior:'instant'});
   }));draw();return execution;
  }
 renderSim($('[data-sim=square]'),M.rooms.square,M.examples.square);renderSim($('[data-sim=after]'),M.rooms.square,M.examples.after);renderSim($('[data-sim=plan]'),M.rooms.plan,M.examples.plan);
 const choices={
  start:{correct:'1',yes:'Nach oben. Der Roboter hat sich auf seiner Kachel gedreht.',wrong:['Du hast die Anweisung links als feste Blickrichtung gedeutet. Sie bedeutet eine Vierteldrehung aus Sicht des Roboters. Ein Pfeil nach rechts zeigt danach nach oben.','', 'Eine Linksdrehung führt von rechts nach oben; nach unten wäre eine Rechtsdrehung.'],next:'Zeichne den Pfeil und drehe das Blatt. Versuche danach die neue Probe darunter.'},
  turn:{correct:'2',yes:'Nach rechts. Auch hier bleibt der Roboter auf derselben Kachel.',wrong:['Von unten nach oben wäre eine halbe Drehung. Eine Vierteldrehung nach links endet bei rechts.','Links ist hier die Drehrichtung, nicht das Ziel im Bild. Stell dir vor, du blickst wie der Roboter nach unten. Deine linke Seite ist dann rechts im Bild.',''],next:'Drehe einen Pfeil auf Papier von unten eine Vierteldrehung gegen den Uhrzeigersinn. Wähle dann erneut.'},
  pair:{correct:'1',yes:'Beide Durchläufe enthalten vor und danach links. Du hast die ganze Gruppe wiederholt.',wrong:['Die erste Abweichung liegt an Stelle 2: Dort kommt links, nicht vor. Führe erst das ganze Paar aus, bevor der nächste Durchlauf beginnt.','','Deine Folge zeigt erst einen Durchlauf. Für zwei Durchläufe muss vor → links noch einmal folgen.'],next:'Umrahme jedes Paar vor → links. Schreibe danach unter „Schleifen ausschreiben“ eine neue Schleife aus.'},
  outside:{correct:'0',yes:'Einmal, nach allen vier Durchläufen. Die zweite Zeile steht außerhalb der Klammer.',wrong:['','Die 4 gilt nur für die Anweisungen in der Klammer. Die zweite Zeile wird nicht mit wiederholt.','Die zweite Zeile wird erst nach der Schleife einmal ausgeführt. Es gibt keine zusätzliche Ausführung davor.'],next:'Suche die schließende Klammer. Alles dahinter kommt erst nach der Schleife. Im Lerncheck findest du einen neuen Fall.'}
 };
 function feedback(form,html,ok){const out=form.querySelector('.feedback');out.className='feedback'+(ok?'':' error');out.innerHTML=html;}
 function applicationAction(application){
  if(!application)return '';
  if(application.id==='comma-probe')return `<div class="notice"><strong>Kleine neue Anwendung:</strong> ${escape(application.prompt)} Korrigiere nur das Zeichen und vergleiche danach mit <code>wiederhole 2 [rechts; vor]</code>.</div>`;
  return `<p><strong>Kleine neue Anwendung:</strong> ${escape(application.prompt)} <a href="#${escape(application.id)}" data-open-probe="${escape(application.id)}">Neue kurze Probe öffnen</a>.</p>`;
 }
 $$('form[data-exercise]').forEach(form=>{
  const id=form.dataset.exercise;
  form.addEventListener('input',e=>{const field=e.target.dataset.field;if(!field)return;state.answers[id]??={};state.answers[id][field]=e.target.value;if(field!=='explanation')form.querySelector('.feedback').replaceChildren();change();});
  form.addEventListener('submit',e=>{e.preventDefault();const a=state.answers[id]||{};
   if(choices[id]){const c=choices[id];if(a.choice===undefined){feedback(form,'<p>Wähle zuerst deine Vermutung. Die Lösung kannst du auch direkt darunter öffnen.</p>',false);return;}const ok=a.choice===c.correct;feedback(form,`<p><strong>${ok?'Das passt.':'Schau auf diesen Unterschied:'}</strong> ${ok?c.yes:c.wrong[Number(a.choice)]}</p>${ok?'':`<p>${c.next}</p>`}`,ok);return;}
   const r=M.checkSequence(id,a),ex=M.exercises[id],parts=[];
    if(r.sequence.ok)parts.push('<p><strong>Die Reihenfolge stimmt.</strong> Du hast die ganze Gruppe in der richtigen Reihenfolge wiederholt'+(ex.code.includes('\n')?' und die Anweisung danach angehängt':'')+'.</p>');
    else {const s=r.sequence;let message='',next='';if(s.kind==='empty'){message='Deine Folge ist noch leer; deshalb ist noch keine Fehlidee erkennbar.';next='Schreibe zuerst genau einen vollständigen Durchlauf aus der Klammer auf.';}else if(s.kind==='unknown'){message=`Die erste Abweichung liegt an Stelle ${s.index+1}: Dort steht „${escape(s.actual)}“, das keine Anweisung dieser Folge ist.`;next='Ersetze nur dieses Wort durch vor, links oder rechts und prüfe erneut.';}else if(s.kind==='missing'){message=`Deine Folge endet nach Stelle ${s.index}. An Stelle ${s.index+1} fehlt noch eine Anweisung; bis dorthin stimmt die Reihenfolge.`;next='Umrahme den letzten begonnenen Durchlauf und ergänze ihn vollständig.';}else if(s.kind==='extra'){message=`Die ersten ${s.index} Anweisungen stimmen. An Stelle ${s.index+1} steht zusätzlich ${escape(s.actual)}, obwohl die vorgegebene Folge dort beendet ist.`;next='Streiche nur die zusätzliche Anweisung und prüfe erneut.';}else {message=`Die erste Abweichung liegt an Stelle ${s.index+1}: Bei dir steht ${escape(s.actual)}, in diesem Durchlauf kommt dort ${escape(s.expected)}.`;next=`Umrahme die Gruppe ${escape(M.expand(ex.code).slice(0,M.expand(ex.code)[0].bodyLength).map(step=>step.action).join(' → '))} und ändere zuerst nur Stelle ${s.index+1}.`;}
     parts.push(`<p><strong>${message}</strong></p><p><strong>Nächster Schritt:</strong> ${next}</p>`);}
    if(!r.runs){const c=r.counts.runs,actual=c.actual?`Du hast ${escape(c.actual)} eingetragen`:'Du hast noch keine Zahl eingetragen';parts.push(`<p><strong>Durchläufe:</strong> ${actual}; verlangt sind ${c.expected}. Umrahme jede ganze Gruppe und zähle nur diese Gruppen.</p>`);}
    if(!r.actions){const c=r.counts.actions,actual=c.actual?`Du hast ${escape(c.actual)} eingetragen`:'Du hast noch keine Zahl eingetragen';parts.push(`<p><strong>Ausgeführte Anweisungen:</strong> ${actual}; tatsächlich sind es ${c.expected}. Zähle jedes ausgeführte Wort, also Fahrten und Drehungen, getrennt von den Durchläufen.</p>`);}
    if(r.ok)parts.push('<p>Auch beide Anzahlen passen.'+(id==='final'?' Vergleiche jetzt deine eigene Erklärung anhand der beiden Kriterien darunter.':' Der vollständige Vergleich bleibt direkt darunter erreichbar.')+'</p>');
    else parts.push('<p>Öffne bei Bedarf direkt darunter „Vollständige Lösung verstehen“ und vergleiche genau den genannten Unterschied.</p>');
    if(id==='practice')parts.push(applicationAction({id:'p3-probe',prompt:'Schreibe in der neuen Aufgabe eine andere Zweiergruppe aus und trenne Durchläufe von einzelnen Anweisungen.'}));
    feedback(form,parts.join(''),r.ok);
  });
 });
  function updatePlanningState(showMessage=true){const planning=M.planningState(M.rooms.own,state.code,lastExecution?.code),badge=$('#plan-state'),previous=$('#previous-run'),relationship=$('#run-relationship'),out=$('#plan-feedback');$('#plan-workspace').dataset.phase=planning.phase;
   const labels={empty:'Noch nicht ausgeführt',unrun:'Entwurf · noch nicht ausgeführt',changed:'Entwurf geändert',invalid:'Entwurf nicht ausführbar',current:'Passt zur ausgeführten Fahrt'};badge.textContent=labels[planning.phase];
   previous.hidden=!lastExecution;previous.classList.toggle('stale-run',planning.stale);if(lastExecution)relationship.textContent=planning.stale?'Vorherige Fahrt · gehört zur vorherigen Programmfassung':'Ausgeführte Programmfassung · passt zum aktuellen Entwurf';
   if(showMessage){if(planning.phase==='empty')out.textContent='Der Bodenplan ist bereit. Beginne mit einer Anweisung oder einer Schleife.';else if(planning.phase==='invalid')out.textContent=`${planning.error} Dieser Entwurf wurde noch nicht ausgeführt. Der Start-Planungsraum bleibt erhalten.`;else if(planning.phase==='changed')out.textContent='Entwurf geändert · noch nicht ausgeführt. Die vorherige Fahrt gehört zur vorherigen Programmfassung.';else if(planning.phase==='unrun')out.textContent='Dieser Entwurf wurde noch nicht ausgeführt.';}
   return planning;
  }
  updatePlanningState(false);
  $('#plan-code').addEventListener('input',e=>{state.code=e.target.value;updatePlanningState();change();});
 $('#learning-note').addEventListener('input',e=>{state.note=e.target.value;change();});
 $('#run-plan').addEventListener('click',()=>{
   const out=$('#plan-feedback'),holder=$('#own-simulation');
   try{const program=state.code,assessment=M.assessPlan(M.rooms.own,program);
   if(!assessment.result){updatePlanningState(false);out.innerHTML=`<p><strong>Schreibstelle prüfen:</strong> ${escape(assessment.message)}</p><p><strong>Nächster Schritt:</strong> ${escape(assessment.nextStep)}</p>${applicationAction(assessment.application)}`;return;}
   const r=assessment.result,execution={room:M.rooms.own,code:program,result:r,index:r.trace.length-1};lastExecution=execution;holder.replaceChildren();const node=document.createElement('div');node.className='simulation run-simulation';holder.append(node);renderSim(node,M.rooms.own,program,{execution,initial:'end',title:'Fahrt und Code gemeinsam untersuchen',startLabel:'Fahrt vom Anfang untersuchen'});updatePlanningState(false);$('#previous-run').hidden=false;
   if(assessment.kind==='unclassified'&&r.status==='limit')out.innerHTML='<p><strong>Der Lauf endet an der Grenze von 100 Aktionen.</strong></p><p><strong>Nächster Schritt:</strong> Gehe zum letzten vollständig ausgeführten Durchlauf zurück und teile nur den noch offenen Weg in einen kleineren Abschnitt.</p>';
   else out.innerHTML=`<p><strong>${assessment.kind==='success'?'Die Aufgabenkriterien passen.':'Dieser Unterschied ist im Lauf sichtbar:'}</strong> ${escape(assessment.message)}</p><p><strong>Nächster Schritt:</strong> ${escape(assessment.nextStep)}</p>${applicationAction(assessment.application)}`;
   }catch(e){updatePlanningState(false);out.textContent=e.message+' Dieser Entwurf wurde noch nicht ausgeführt. Der Bodenplan bleibt sichtbar; im Wissensteil findest du die Schreibweise und die Grenzen unseres Modells.';}
 });

 // UX08 notes deliberately stay outside the unchanged saved-state contract.
 let materialDirty=false;
 $$('[data-material-answer]').forEach(el=>el.addEventListener('input',()=>{
  materialDirty=true;
  if(el.id==='a9-code')$('#a9-feedback').replaceChildren();
 }));
 $$('[data-jump]').forEach(link=>link.addEventListener('click',event=>{
  event.preventDefault();const target=document.getElementById(link.dataset.jump);
  target.scrollIntoView({block:'start'});target.tabIndex=-1;target.focus({preventScroll:true});
 }));
 $('[data-group-check=a9]').addEventListener('click',()=>{
  const r=M.checkGrouping($('#a9-code').value,['vor','rechts','vor','vor','rechts','vor','links']);
  const out=$('#a9-feedback'),nextProbe=applicationAction({id:'p9-probe',prompt:'Fasse in der neuen Aufgabe eine andere Siebenerfolge zusammen.'});out.className='feedback'+(r.ok?'':' error');
   if(r.syntax?.kind==='comma')out.innerHTML=`<p><strong>Schreibstelle prüfen:</strong> In Zeile ${r.syntax.line} steht zwischen den Grundanweisungen ein Komma. In dieser Schreibweise trennt ein Semikolon ; die Anweisungen.</p><p><strong>Nächster Schritt:</strong> Ersetze nur das Komma durch ;. Vergleich: <code>${escape(r.syntax.corrected)}</code>. Deine Erklärung wird nicht automatisch geprüft.</p>${applicationAction({id:'comma-probe',prompt:'Berichtige nur das Trennzeichen: wiederhole 2 [rechts, vor].'})}`;
   else if(r.error)out.innerHTML=`<p>${escape(r.error)} Korrigiere zuerst nur die genannte Schreibstelle und prüfe erneut. Deine Erklärung wird nicht automatisch geprüft.</p>${nextProbe}`;
   else if(!r.sequence.ok){const s=r.sequence;out.innerHTML='<p>Die ausgeführte Folge weicht an Stelle '+(s.index+1)+' ab. '+(s.actual?'Dein Programm führt dort '+escape(s.actual)+' aus. ':'Dort fehlt noch eine Anweisung. ')+(s.expected?'Die lange Folge enthält dort '+escape(s.expected)+'.':'Die lange Folge ist dort bereits zu Ende.')+' Ändere zuerst nur diese Stelle und vergleiche bei Bedarf die vollständige Lösung.</p>'+nextProbe;}
   else if(!r.loop)out.innerHTML='<p>Die Reihenfolge stimmt. Zur Aufgabe gehört noch eine Schleife: Vergleiche die ersten drei Anweisungen mit den nächsten drei und fasse nur eine tatsächlich wiederkehrende Gruppe zusammen.</p>'+nextProbe;
   else out.innerHTML='Deine Fassung führt genau dieselbe Folge aus und enthält eine Schleife. Auch eine andere Gruppierung als die Musterlösung gilt. Vergleiche nun selbst: Warum passen deine Gruppe, die Zahl und die Fortsetzung? Die Erklärung wurde nicht automatisch bewertet.'+nextProbe;
  });

 document.addEventListener('click',event=>{const link=event.target.closest('[data-open-probe]');if(!link)return;const target=document.getElementById(link.dataset.openProbe);if(!target)return;event.preventDefault();target.open=true;target.scrollIntoView({block:'start'});target.querySelector('summary')?.focus({preventScroll:true});});

 const dialog=$('#save-dialog');$('#open-save').addEventListener('click',()=>dialog.showModal());$('#close-save').addEventListener('click',()=>dialog.close());
 $('#remember').addEventListener('change',e=>{remember=e.target.checked;if(remember)persist();else{try{localStorage.removeItem(key);saveStatus.textContent='Die Browsersicherung ist entfernt. Die Eingaben im offenen Tab bleiben erhalten.';dirty=true;}catch{saveStatus.textContent='Die Browsersicherung konnte nicht entfernt werden. Bitte nutze die Einstellungen deines Browsers.';}}});
 $('#export').addEventListener('click',()=>{try{const blob=new Blob([M.encode(state)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='ium-schleifen-lernstand.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);dirty=false;saveStatus.textContent='Der Download wurde gestartet. Bewahre die Datei für das nächste Mal auf.';}catch(e){saveStatus.textContent=e.message;}});
 $('#import').addEventListener('change',async e=>{pending=null;$('#import-preview').hidden=true;const file=e.target.files[0];if(!file)return;try{if(file.size>100000)throw new Error('Die Datei ist zu groß (höchstens 100 KB).');pending=M.decode(await file.text());$('#import-summary').textContent=`Gültige Sicherung: ${Object.keys(pending.answers).length} Aufgaben mit Eingaben. Lernseite: ${$('[data-nav='+pending.page+']').textContent.trim()}.`;$('#import-preview').hidden=false;saveStatus.textContent='Datei geprüft, noch nicht übernommen.';}catch(error){saveStatus.textContent=error.message;}e.target.value='';});
 $('#apply-import').addEventListener('click',()=>{if(!pending)return;state=pending;pending=null;restore();change();location.hash=state.page;showPage(state.page,true);$('#import-preview').hidden=true;saveStatus.textContent='Die Sicherung wurde übernommen.';dialog.close();$('#restore-notice').textContent='Deine Datei ist übernommen. Antworten, Programm und Notiz sind wieder da.';});
 $('#cancel-import').addEventListener('click',()=>{pending=null;$('#import-preview').hidden=true;saveStatus.textContent='Import abgebrochen. Dein Stand bleibt erhalten.';});
 let printDetails=[];window.addEventListener('beforeprint',()=>{printDetails=$$('details').filter(d=>!d.open);printDetails.forEach(d=>d.open=true);});window.addEventListener('afterprint',()=>printDetails.forEach(d=>d.open=false));$('#print').addEventListener('click',()=>window.print());
 window.addEventListener('beforeunload',e=>{if(dirty||materialDirty){e.preventDefault();e.returnValue='';}});
window.PlanningJourneyUI?.mount({renderSim});
})();
