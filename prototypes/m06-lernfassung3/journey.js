'use strict';
window.PlanningJourneyUI={
 mount({renderSim}){
  const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],J=window.PlanningJourney;
  const panels=$$('[data-stage-panel]');
  function selectStage(index,focus=false){
   panels.forEach((panel,i)=>panel.hidden=i!==index);
   $$('[data-stage]').forEach(button=>{
    const current=Number(button.dataset.stage)===index;
    if(current)button.setAttribute('aria-current','step');else button.removeAttribute('aria-current');
   });
   $('#journey-position').textContent='Etappe '+(index+1)+' von 4 · Alle Etappen sind frei zugänglich.';
   $('#plan').dataset.lastStage=String(index===3);
   if(focus){const heading=$('#stage-title-'+index);heading.scrollIntoView({block:'start'});heading.focus({preventScroll:true});}
  }
  $$('[data-stage]').forEach(button=>button.addEventListener('click',()=>selectStage(Number(button.dataset.stage),true)));
  // Reveal an anchored exercise before the base app scrolls/focuses it.
  document.addEventListener('click',event=>{
   const link=event.target.closest('[data-jump],[data-open-probe]');
   if(!link)return;
   const target=document.getElementById(link.dataset.jump||link.dataset.openProbe);
   const panel=target?.closest('[data-stage-panel]');
   if(panel)selectStage(Number(panel.dataset.stagePanel));
  },true);
  selectStage(0);
  function connect(id,inputs,assess){
   const out=$('#'+id+'-feedback'),holder=$('#'+id+'-run-holder'),sim=$('#'+id+'-simulation');
   inputs.forEach(input=>input.addEventListener('input',()=>{
    holder.hidden=true;sim.replaceChildren();out.classList.remove('error');
    out.textContent='Eingaben geändert · noch nicht ausgeführt. Starte die Fahrt, um diesen Entwurf zu prüfen.';
   }));
   $('#'+id+'-run').addEventListener('click',()=>{
    const a=assess();out.replaceChildren();out.classList.toggle('error',a.kind!=='success');
    const message=document.createElement('p');message.textContent=a.message;
    const next=document.createElement('p');next.textContent='Nächster Schritt: '+a.nextStep;out.append(message,next);
    holder.hidden=!a.result;
    if(!a.result){sim.replaceChildren();return;}
    const execution={room:a.room,code:a.code,result:a.result,index:a.result.trace.length-1};
    renderSim(sim,a.room,a.code,{execution,initial:'end'});
   });
  }
  connect('bridge',[$('#a6-first'),$('#a6-turn'),$('#a6-last')],()=>J.bridge({first:$('#a6-first').value,turn:$('#a6-turn').value,last:$('#a6-last').value}));
  connect('switch',[$('#a7-first'),$('#a7-next'),$('#a7-last')],()=>J.switchRow([$('#a7-first').value,$('#a7-next').value,$('#a7-last').value]));
 }
};
