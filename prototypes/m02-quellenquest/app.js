(function(){
'use strict';
const C=window.QuestContent,M=window.QuestModel,e=M.escapeHtml;
const answers={claims:{},transfer:{}},active={claims:C.claims[0].id,transfer:C.transfer[0].id};
const $=id=>document.getElementById(id);
const list=bank=>bank==='transfer'?C.transfer:C.claims;
function feedback(id,result){
 const box=$(id);box.replaceChildren();
 const title=document.createElement('strong'),text=document.createElement('p');
 title.textContent=result.title;text.textContent=result.text;box.append(title,text);box.dataset.status=result.status;box.hidden=false;
}
function clearFeedback(id){const box=$(id);if(box){box.hidden=true;box.replaceChildren();}}
function showDocument(bank,id,focus=false){
 const reader=document.querySelector('[data-reader="'+bank+'"]');
 if(!reader||!reader.querySelector('[data-document-panel="'+id+'"]'))return;
 for(const panel of reader.querySelectorAll('[data-document-panel]'))panel.hidden=panel.dataset.documentPanel!==id;
 for(const button of reader.querySelectorAll('[data-document]'))button.setAttribute('aria-pressed',String(button.dataset.document===id));
 if(focus){const title=reader.querySelector('[data-document-panel="'+id+'"] h3');title.tabIndex=-1;title.focus();}
}
function renderPicked(bank,id){
 const answer=answers[bank][id]||{},record=M.evidenceRecord(id,{verdict:answer.verdict||'offen',evidence:answer.evidence},bank);
 const target=document.querySelector('[data-picked="'+bank+'-'+id+'"]');
 if(record){target.innerHTML='<b>'+e(record.lineId==='none'?'Keine Angabe':record.lineId)+'</b> '+e(record.quote)+'<small>'+e(record.author)+(record.date?' · '+e(record.date):'')+'</small>';}
 else target.textContent='Wähle einen Satz im Dokument oder prüfe, ob die Angabe in allen Quellen fehlt.';
 const box=document.querySelector('[data-workbench="'+bank+'"]');
 for(const button of box.querySelectorAll('[data-passage]'))button.setAttribute('aria-pressed',String(button.dataset.passage===answer.evidence));
 const none=box.querySelector('[data-no-evidence="'+id+'"]');none.setAttribute('aria-pressed',String(answer.evidence==='none'));
}
function renderMarkers(bank){
 for(const c of list(bank)){
  const a=answers[bank][c.id],marker=document.querySelector('[data-claim-status="'+bank+'-'+c.id+'"]');
  marker.textContent=a?.checked?(M.assess(c.id,a,bank).status==='match'?'Zuordnung passt':'Noch einmal prüfen'):a?.evidence||a?.verdict?'In Arbeit':'';
 }
}
function activateClaim(bank,id){
 if(!list(bank).some(c=>c.id===id))return;
 active[bank]=id;const box=document.querySelector('[data-workbench="'+bank+'"]');
 for(const button of box.querySelectorAll('[data-claim-select]'))button.setAttribute('aria-pressed',String(button.dataset.claimSelect===id));
 for(const panel of box.querySelectorAll('[data-judgement]'))panel.hidden=panel.dataset.judgement!==id;
 box.querySelector('[data-active-claim]').textContent=list(bank).find(c=>c.id===id).text;
 renderPicked(bank,id);$(bank+'-selection-status').textContent='';
}
function changeAnswer(bank,id,patch){
 const a=answers[bank][id]||(answers[bank][id]={});Object.assign(a,patch,{checked:false});
 clearFeedback(bank+'-'+id+'-feedback');renderPicked(bank,id);renderMarkers(bank);
}
function updateBoard(){
 const board=$('evidence-board');board.replaceChildren();
 for(const c of C.claims){
  const answer=answers.claims[c.id],record=M.evidenceRecord(c.id,answer);
  if(!record)continue;
  const article=document.createElement('article');article.className='evidence-note';
  const status=answer.checked?(record.status==='match'?'Zuordnung verglichen: passt':'Zuordnung verglichen: noch einmal prüfen'):'Deine Auswahl · noch nicht verglichen';
  article.innerHTML='<p class="note-status">'+e(status)+'</p><h3>'+e(record.claim)+'</h3><p class="note-verdict">Dein Urteil: '+e(record.verdict)+'</p><blockquote>'+e(record.quote)+'</blockquote><p class="note-reference">'+e(record.author)+(record.date?' · '+e(record.date):'')+' · '+e(record.lineId)+'</p><a href="#belege" data-return-claim="'+c.id+'">Diese Zuordnung ansehen →</a>';
  board.append(article);
 }
 if(!board.children.length)board.innerHTML='<p class="empty-note">Noch keine Zuordnungen. Für den Direkteinstieg findest du alle Quellen unten. Oder <a href="#belege">untersuche zuerst deine Belege</a>.</p>';
 const reason=$('beleg-grund').value.trim();
 if(reason){const own=document.createElement('p');own.className='own-reason';own.textContent='Deine Erklärung: '+reason;board.append(own);}
 const initial=$('initial-view'),selected=document.querySelector('input[name="initial"]:checked');
 const firstReason=$('initial-reason').value.trim(),question=$('initial-question').value.trim();
 initial.replaceChildren();
 if(selected||firstReason||question){
  const texts=[selected?{ja:'Ich vermute: ja.',nein:'Ich vermute: nein.',unsicher:'Ich bin noch unsicher.'}[selected.value]:'',firstReason,question?'Deine Prüffrage: '+question:''];
  for(const t of texts.filter(Boolean)){const p=document.createElement('p');p.textContent=t;initial.append(p);}
 }else initial.innerHTML='<p>Du bist direkt eingestiegen? Überlege, wie du Milas Nachricht ohne die Quellen eingeschätzt hättest.</p>';
}
function route(focus){
 const candidate=location.hash.slice(1),step=C.steps.find(s=>s.id===candidate)||C.steps[0];
 if(candidate!==step.id)history.replaceState(null,'','#'+step.id);
 for(const section of document.querySelectorAll('.step'))section.hidden=section.id!==step.id;
 for(const a of document.querySelectorAll('[data-step]')){if(a.dataset.step===step.id)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');}
 if(step.id==='antwort')updateBoard();
 document.title=step.title+' · IuM Lernwerk';
 if(focus){$('title-'+step.id).focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
document.addEventListener('click',event=>{
 if(event.target.closest('a.skip')){event.preventDefault();$('main').focus();return;}
 const returnLink=event.target.closest('[data-return-claim]');
 if(returnLink){activateClaim('claims',returnLink.dataset.returnClaim);const c=C.claims.find(c=>c.id===returnLink.dataset.returnClaim);if(c.extra)document.querySelector('.extra-claims').open=true;}
 const button=event.target.closest('button');if(!button)return;
 const bank=button.dataset.bank;
 if(button.dataset.toJudgement){const destination=document.querySelector('[data-workbench="'+button.dataset.toJudgement+'"] [data-judgement="'+active[button.dataset.toJudgement]+'"] legend');destination.tabIndex=-1;destination.focus();destination.scrollIntoView({block:'center'});}

 if(button.dataset.document)showDocument(bank,button.dataset.document);
 if(button.dataset.openSource)showDocument(bank,button.dataset.openSource,true);
 if(button.dataset.claimSelect)activateClaim(bank,button.dataset.claimSelect);
 if(button.dataset.passage){changeAnswer(bank,active[bank],{evidence:button.dataset.passage});$(bank+'-selection-status').textContent='Textstelle '+button.dataset.passage+' für dein Urteil ausgewählt.';}
 if(button.dataset.noEvidence){changeAnswer(bank,button.dataset.noEvidence,{evidence:'none'});$(bank+'-selection-status').textContent='Ausgewählt: Keine passende Angabe in den Quellen.';}
 if(button.dataset.check||button.dataset.reveal){
  const id=button.dataset.check||button.dataset.reveal,a=answers[bank][id]||{};
  const result=M.assess(id,a,bank,Boolean(button.dataset.reveal));
  if(button.dataset.reveal&&result.status==='open'){
   const c=list(bank).find(c=>c.id===id);feedback(bank+'-'+id+'-feedback',{status:'reflection',title:'Die Erklärung zum Vergleichen',text:c.feedback+' Triff anschließend selbst deine Auswahl.'});
  }else feedback(bank+'-'+id+'-feedback',result);
  if(button.dataset.check&&result.status!=='open'){a.checked=true;answers[bank][id]=a;renderMarkers(bank);}
 }
 if(button.dataset.sourceCheck){const id=button.dataset.sourceCheck;feedback('source-'+id+'-feedback',M.checkSource(id,$('source-'+id).value));}
 if(button.id==='answer-review')feedback('answer-feedback',{status:'reflection',title:'Prüfe einen Satz ganz genau',text:$('answer').value.trim()?'Zeige zu einer Aussage die genaue Stelle in deiner Belegübersicht. Erklärt dein Satz, warum sie passt? Überarbeite diese Verbindung und benenne anschließend, was offen bleibt.':'Formuliere deine Antwort zuerst hier, im Heft oder mündlich. Zeige dann zu einer Aussage die genaue Textstelle und erkläre, warum sie dein Urteil trägt.'});
});
document.addEventListener('change',event=>{
 const input=event.target;
 for(const bank of ['claims','transfer'])for(const c of list(bank))if(input.name===bank+'-'+c.id)changeAnswer(bank,c.id,{verdict:input.value});
 for(const q of C.sourceQuestions)if(input.id==='source-'+q.id)clearFeedback('source-'+q.id+'-feedback');
 if(input.name==='review')clearFeedback('answer-feedback');
});
document.addEventListener('input',event=>{if(['answer','revision'].includes(event.target.id))clearFeedback('answer-feedback');});
if(window.LernwerkMantel)window.LernwerkMantel.register({
 capture:()=>({family:'source',answers:JSON.parse(JSON.stringify(answers)),active:{...active},documents:Object.fromEntries(['explore','claims','transfer'].map(bank=>[bank,document.querySelector('[data-reader="'+bank+'"] [data-document-panel]:not([hidden])')?.dataset.documentPanel||null]))}),
 validate:tool=>tool?.family==='source'&&tool.answers&&tool.active,
 restore:(tool,options={})=>{
  for(const bank of ['claims','transfer']){
   answers[bank]=JSON.parse(JSON.stringify(tool.answers[bank]));active[bank]=tool.active[bank];
   for(const c of list(bank)){const a=answers[bank][c.id];for(const radio of document.querySelectorAll('input[name="'+bank+'-'+c.id+'"]'))radio.checked=radio.value===a?.verdict;}
   activateClaim(bank,active[bank]);renderMarkers(bank);
  }
  for(const bank of ['explore','claims','transfer'])if(tool.documents?.[bank])showDocument(bank,tool.documents[bank]);
  if(C.steps.some(s=>s.id===options.step))history.replaceState(null,'','#'+options.step);
  route(false);updateBoard();
 }
});

for(const bank of ['claims','transfer'])activateClaim(bank,active[bank]);
showDocument('explore','A');showDocument('claims','B');showDocument('transfer','E');
window.addEventListener('hashchange',()=>route(true));route(false);
window.addEventListener('load',()=>window.scrollTo({top:0,behavior:'instant'}),{once:true});
})();
