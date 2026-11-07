'use strict';
document.querySelectorAll('[data-pt-root]').forEach(root=>{
const cards=[...root.querySelectorAll('[data-pt-card]')],buttons=[...root.querySelectorAll('[data-pt-view]')],status=root.querySelector('[data-pt-status]');
let current=root.dataset.ptInitial||'a';
function show(id){if(!['a','b','c','all'].includes(id))id='a';current=id;root.classList.toggle('pt-single',id!=='all');cards.forEach(card=>card.hidden=id!=='all'&&card.dataset.ptCard!==id);buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ptView===id)));status.textContent=id==='all'?'Alle drei Ansichten · Auf schmalen Bildschirmen untereinander.':buttons.find(b=>b.dataset.ptView===id).textContent+' · Vergleiche anschließend mit den anderen Räumen.';}
root.querySelector('.pt-controls').hidden=false;
buttons.forEach(b=>b.addEventListener('click',()=>show(b.dataset.ptView)));
show(current);
window.addEventListener('beforeprint',()=>{cards.forEach(c=>c.hidden=false);root.classList.remove('pt-single')});
window.addEventListener('afterprint',()=>show(current));
});

