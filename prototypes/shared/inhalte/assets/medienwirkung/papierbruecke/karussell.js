(() => {
 const params=new URLSearchParams(location.search);
 if(params.get('lernwerk')==='1'){
  document.querySelectorAll('.back').forEach(a=>a.hidden=false);
  document.querySelectorAll('[data-carry]').forEach(a=>{const u=new URL(a.href);u.searchParams.set('lernwerk','1');a.href=u.href;});
 }
 if(params.has('export')) document.body.classList.add('export');
 const carousel=document.querySelector('.carousel');if(!carousel)return;
 const cards=[...carousel.querySelectorAll('.post')], previous=document.querySelector('#previous'),next=document.querySelector('#next'),live=document.querySelector('.live'),dots=[...document.querySelectorAll('[data-slide]')];
 const requested=Number(params.get('bild')||1);
 let index=Number.isInteger(requested)?Math.max(0,Math.min(3,requested-1)):0;
 function show(i){index=Math.max(0,Math.min(cards.length-1,i));cards.forEach((c,n)=>c.hidden=n!==index);previous.disabled=index===0;next.disabled=index===cards.length-1;live.textContent='Bild '+(index+1)+' von '+cards.length;dots.forEach((d,n)=>d.setAttribute('aria-current',String(n===index)));}
 document.body.classList.add('enhanced');document.querySelector('.controls').hidden=false;document.querySelector('.dots').hidden=false;
 previous.addEventListener('click',()=>show(index-1));next.addEventListener('click',()=>show(index+1));dots.forEach((d,n)=>d.addEventListener('click',()=>show(n)));
 carousel.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();show(index+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(index-1)}});
 let startX=null,startY=null;
 carousel.addEventListener('touchstart',e=>{startX=e.changedTouches[0].clientX;startY=e.changedTouches[0].clientY},{passive:true});
 carousel.addEventListener('touchend',e=>{if(startX===null)return;const dx=e.changedTouches[0].clientX-startX,dy=e.changedTouches[0].clientY-startY;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.4)show(index+(dx<0?1:-1));startX=null},{passive:true});
 show(index);
})();