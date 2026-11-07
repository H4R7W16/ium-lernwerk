'use strict';
document.querySelectorAll('[data-pt-root]').forEach(root=>{
 const cards=[...root.querySelectorAll('[data-pt-card]')],buttons=[...root.querySelectorAll('[data-pt-view]')],status=root.querySelector('[data-pt-status]');
 const sets={a:['a'],b:['b'],c:['c'],ab:['a','b'],bc:['b','c'],all:['a','b','c']};
 let current=root.dataset.ptInitial||'a';
 function show(id){
  if(!sets[id])id='a';current=id;
  root.classList.toggle('pt-single',sets[id].length===1);root.classList.toggle('pt-pair',sets[id].length===2);
  cards.forEach(c=>c.hidden=!sets[id].includes(c.dataset.ptCard));
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ptView===id)));
  status.textContent=sets[id].length===1?'Betrachte die Reaktionen und ihre Zeitangaben.':(id==='all'?'Alle drei Ansichten':'Vergleich '+id.toUpperCase().split('').join(' / '))+' · Auf schmalen Bildschirmen untereinander.';
 }
 root.querySelector('.pt-controls').hidden=false;buttons.forEach(b=>b.addEventListener('click',()=>show(b.dataset.ptView)));show(current);
 window.addEventListener('beforeprint',()=>{cards.forEach(c=>c.hidden=false);root.classList.remove('pt-single','pt-pair')});
 window.addEventListener('afterprint',()=>show(current));
});

