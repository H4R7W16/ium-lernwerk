(function(){
'use strict';
const C=window.QuestContent,M=window.QuestModel;
function feedback(id,result){
 const box=document.getElementById(id);box.replaceChildren();
 const title=document.createElement('strong'),text=document.createElement('p');
 title.textContent=result.title;text.textContent=result.text;box.append(title,text);
 box.dataset.status=result.status;box.hidden=false;
}
function clearFeedback(id){const box=document.getElementById(id);if(box){box.hidden=true;box.replaceChildren();}}
function route(focus){
 const candidate=location.hash.slice(1),step=C.steps.find(s=>s.id===candidate)||C.steps[0];
 if(candidate!==step.id)history.replaceState(null,'','#'+step.id);
 for(const section of document.querySelectorAll('.step'))section.hidden=section.id!==step.id;
 for(const a of document.querySelectorAll('[data-step]')){
  if(a.dataset.step===step.id)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');
 }
 document.title=step.title+' · IuM Quellenquest';
 if(focus){document.getElementById('title-'+step.id).focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
document.addEventListener('click',event=>{
 const skip=event.target.closest('a.skip');
 if(skip){event.preventDefault();document.getElementById('main').focus();return;}
 const button=event.target.closest('button');if(!button)return;
 if(button.id==='mission-check'){
  const selected=document.querySelector('input[name="mission"]:checked')?.value;
  feedback('mission-feedback',!selected?{status:'open',title:'Wähle zuerst eine Prüffrage',text:'Lies noch einmal, was Mila genau behauptet.'}:selected==='whole'?{status:'match',title:'Diese Frage trifft Milas Behauptung',text:'Du prüfst die ganze Wiese und den Zeitpunkt. Ob die Aussage stimmt, klärst du jetzt mit den Quellen.'}:{status:'revise',title:'Interessant – aber eine andere Frage',text:'Mila behauptet, dass ab Montag die ganze Wiese zum Garten wird. Genau diesen Satz sollst du prüfen.'});
 }
 if(button.dataset.sourceCheck){
  const id=button.dataset.sourceCheck;feedback('source-'+id+'-feedback',M.checkSource(id,document.getElementById('source-'+id).value));
 }
 if(button.dataset.check){
  const id=button.dataset.check,bank=button.dataset.bank;
  feedback(bank+'-'+id+'-feedback',M.assess(id,{verdict:document.querySelector('input[name="'+bank+'-'+id+'"]:checked')?.value,evidence:document.getElementById(bank+'-'+id+'-evidence').value},bank));
 }
 if(button.id==='answer-review'){
  const answer=document.getElementById('answer').value.trim(),revision=document.getElementById('revision').value.trim(),checked=document.querySelectorAll('input[name="review"]:checked').length;
  const text=!answer?'Formuliere zuerst deine Antwort im Textfeld, im Heft oder mündlich. Vergleiche sie dann mit den vier Kriterien.':checked<4?'Prüfe die noch offenen Kriterien. Ergänze oder verbessere deinen Text dort, wo etwas fehlt. Die Beispielantwort kann dir helfen.':!revision?'Du hast alle Kriterien abgehakt. Erkläre jetzt noch, was du verbessert hast oder warum du einen Satz beibehältst.':'Lies deinen Text mit deinen Belegen noch einmal durch oder lass ihn dir von einem anderen Kind erklären. Probiere danach den neuen Fall. Ob deine Begründung trägt, zeigt ihr Inhalt – nicht die Zahl der Häkchen.';
  feedback('answer-feedback',{status:'reflection',title:'Dein nächster Schritt',text});
 }
});
document.addEventListener('change',event=>{
 const input=event.target,claim=input.closest('[data-claim]');
 if(claim)clearFeedback(claim.dataset.bank+'-'+claim.dataset.claim+'-feedback');
 if(input.name==='mission')clearFeedback('mission-feedback');
 for(const q of C.sourceQuestions)if(input.id==='source-'+q.id)clearFeedback('source-'+q.id+'-feedback');
 if(input.name==='review')clearFeedback('answer-feedback');
});
document.addEventListener('input',event=>{if(['answer','revision'].includes(event.target.id))clearFeedback('answer-feedback');});
window.addEventListener('hashchange',()=>route(true));
route(false);
window.addEventListener('load',()=>window.scrollTo({top:0,behavior:'instant'}),{once:true});
})();
