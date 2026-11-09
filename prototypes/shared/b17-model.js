/* B17: erfundenes Auswahlmodell; Zustand bleibt ausschließlich in dieser Ansicht. */
(function(root,factory){'use strict';const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else{root.B17Model=api;const boot=()=>root.document.querySelectorAll('[data-b17-model]').forEach(api.mount);if(root.document.readyState==='loading')root.document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();}})(typeof window==='undefined'?globalThis:window,function(){
'use strict';
const original=['lesen','zeichnen','zeichnen'],phases=['predict-start','choose','predict-change','compare'];
function topic(t){if(!['lesen','zeichnen'].includes(t))throw new Error('Ungültiges Thema');return t;}
function evaluate(current,visits){topic(current);if(!Array.isArray(visits))throw new Error('Besuchsliste fehlt');const counts={lesen:0,zeichnen:0};for(const t of visits)counts[topic(t)]++;const tie=counts.lesen===counts.zeichnen,ad=t=>t==='lesen'?'buch':'stifte';return{context:ad(current),history:ad(tie?current:counts.lesen>counts.zeichnen?'lesen':'zeichnen'),counts,tie};}
function createState(){return{phase:'predict-start',selected:null};}
function validate(s){if(!s||!phases.includes(s.phase)||(['predict-start','choose'].includes(s.phase)?s.selected!==null:!Number.isInteger(s.selected)||s.selected<0||s.selected>2))throw new Error('Ungültiger Zustand');}
function historyFor(s){validate(s);return original.map((t,i)=>i===s.selected?(t==='lesen'?'zeichnen':'lesen'):t);}
function transition(s,action,index){validate(s);if(action==='RESET')return createState();if(action==='CHECK_START'&&s.phase==='predict-start')return{phase:'choose',selected:null};if(action==='CHOOSE_VISIT'&&['choose','predict-change'].includes(s.phase)&&Number.isInteger(index)&&index>=0&&index<3)return{phase:'predict-change',selected:index};if(action==='CHECK_CHANGE'&&s.phase==='predict-change')return{...s,phase:'compare'};throw new Error('Aktion hier nicht möglich');}
const label=t=>t==='lesen'?'Lesen':'Zeichnen',ad=a=>a==='buch'?'Buchwerbung':'Stiftewerbung';

function comparison(s){validate(s);return{start:s.phase==='predict-start'?null:evaluate('lesen',original),after:s.phase==='compare'?evaluate('lesen',historyFor(s)):null};}
function mount(root){
 if(root.dataset.b17Ready)return;root.dataset.b17Ready='true';let state=createState();
 const q=s=>root.querySelector(s),radios=[...root.querySelectorAll('input[name="b17-visit"]')],start=q('[data-b17-start]'),check=q('[data-b17-check]'),reset=q('[data-b17-reset]'),status=q('[data-b17-status]'),results=q('[data-b17-results]'),title=q('[data-b17-result-title]');
 const block=root.closest('.lw-content-block'),answer=block.querySelector('#answer-modell-versuch'),back=block.querySelector('[data-b17-return]');
 function paint(){
  const s=state,visits=historyFor(s),c=comparison(s);
  radios.forEach((r,i)=>{r.disabled=['predict-start','compare'].includes(s.phase);r.checked=s.selected===i;q('[data-b17-topic="'+i+'"]').textContent=s.selected===i?label(original[i])+' → '+label(visits[i]):label(visits[i]);r.closest('label').classList.toggle('b17-changed',s.selected===i);});
  start.hidden=s.phase!=='predict-start';check.hidden=s.phase!=='predict-change';reset.hidden=s.phase==='predict-start';results.hidden=!c.start;
  root.querySelectorAll('[data-b17-after]').forEach(n=>{n.hidden=!c.after;});
  for(const [side,value]of [['start',c.start],['after',c.after]])for(const key of ['context','history','counts'])q('[data-b17-cell="'+key+'-'+side+'"]').textContent=!value?'':key==='counts'?value.counts.lesen+' Lesen · '+value.counts.zeichnen+' Zeichnen':ad(value[key]);
  q('[data-b17-explain]').hidden=s.phase!=='compare';
  q('[data-b17-list-label]').textContent=s.selected===null?'Frühere Besuche · Start':'Frühere Besuche · dein Eingriff';
  status.textContent={
   'predict-start':'1 · Sage K und V für den Start voraus. Halte deine Vorhersage fest. Dann: Start prüfen.',
   choose:'2 · Wähle genau einen früheren Besuch. Sein Thema wechselt. Die aktuelle Seite bleibt Lesen.',
   'predict-change':'3 · Sage K und V nach deinem Eingriff voraus. Halte auch diese Vorhersage fest. Dann: Änderung prüfen.',
   compare:'4 · Vergleiche K, V und die Zählungen. Erkläre in deiner Versuchsspur, warum die Auswahl gleich bleibt oder sich ändert.'
  }[s.phase];
 }
 function act(action,index){state=transition(state,action,index);paint();if(action==='CHECK_START')radios[0].focus();if(action==='CHECK_CHANGE'){title.focus();title.scrollIntoView({block:'start'});}if(action==='RESET')start.focus();}
 start.addEventListener('click',()=>act('CHECK_START'));check.addEventListener('click',()=>act('CHECK_CHANGE'));reset.addEventListener('click',()=>act('RESET'));
 root.querySelectorAll('[data-b17-to-answer]').forEach(link=>link.addEventListener('click',e=>{e.preventDefault();answer.focus();answer.scrollIntoView({block:'center'});}));
 back.addEventListener('click',e=>{e.preventDefault();root.closest('details').open=true;const target=state.phase==='predict-start'?start:state.phase==='choose'?radios[0]:state.phase==='predict-change'?check:title;target.focus();target.scrollIntoView({block:'center'});});
 root.addEventListener('input',e=>e.stopPropagation());root.addEventListener('change',e=>{e.stopPropagation();if(radios.includes(e.target))act('CHOOSE_VISIT',Number(e.target.value));});paint();
}
return{evaluate,createState,transition,historyFor,comparison,mount};
});
