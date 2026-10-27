'use strict';
/* Native disclosure and normal links; existing workspace/unload guards stay in charge. */
(() => {
 document.addEventListener('click',event=>{
  if(event.target.closest?.('.lw-grade-summary'))for(const menu of document.querySelectorAll('[data-lw-menu][open]'))menu.open=false;
  for(const menu of document.querySelectorAll('[data-grade-switch][open]'))if(!menu.contains(event.target))menu.open=false;
 });
 document.addEventListener('keydown',event=>{
  if(event.key!=='Escape')return;
  const menus=[...document.querySelectorAll('[data-grade-switch][open]')];
  for(const menu of menus)menu.open=false;
  if(menus.length){menus[0].querySelector('summary').focus();event.preventDefault();}
 });
})();
