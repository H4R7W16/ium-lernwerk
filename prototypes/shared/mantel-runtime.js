/* Shared browser controller; no network transmission of learner work. */
(function(){
'use strict';
const initialHash=location.hash.slice(1),scriptUrl=document.currentScript.src,base=new URL('./',scriptUrl),M=window.LernwerkMantelModel,KEY='ium-klasse'+(/\/klasse6\/$/.test(base.pathname)?6:5)+'-mantel-v1',PERSIST=KEY+'-persistent',RECOVERY=KEY+'-recovery';
let pendingAdapter=null,booted=false,restoring=false,dirty=false,store={version:1,records:[],active:{}},units=[],unit=null,currentId=null,device=false,tabOk=true,captureOk=true,quarantineOk=true,adapter=null,preview=null,fileGeneration=0,installEvent=null,recoveryRaw=null,privateNote='';
const $=id=>document.getElementById(id),copy=M.clone,e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function uuid(){return crypto.randomUUID();}
function announce(message){const node=$('lw-work-message')||$('lw-storage-warning')||$('lw-storage-status');if(node)node.textContent=message;}
function status(){const backup=$('lw-emergency-export');if(backup)backup.hidden=tabOk&&captureOk;const n=$('lw-storage-status');if(n)n.textContent=device?'Deine Antworten und Programme sind in diesem Browser auf diesem Gerät gespeichert. Sichere eine Arbeitsdatei für ein anderes Gerät.':'Deine Antworten und Programme bleiben im geöffneten Lernwerk.'+(tabOk?' Sichere eine Arbeitsdatei, bevor du es schließt.':' Speichern ist eingeschränkt; sichere jetzt eine Arbeitsdatei.');}
function save(){
 if(!quarantineOk){tabOk=false;status();return false;}
 try{sessionStorage.setItem(KEY,JSON.stringify(store));tabOk=true;}catch{tabOk=false;announce('Tabsicherung ist eingeschränkt. Deine aktuelle Arbeit bleibt hier; sichere sie vor einem Seitenwechsel als Datei.');}
 if(device){try{localStorage.setItem(KEY,JSON.stringify(store));localStorage.setItem(PERSIST,'1');}catch{device=false;announce('Speichern hat nicht geklappt. Deine Arbeit bleibt in diesem Tab. Sichere eine Arbeitsdatei.');}}
 status();return tabOk;
}
function load(){
 let raw=null;try{raw=sessionStorage.getItem(KEY);recoveryRaw=sessionStorage.getItem(RECOVERY);}catch{tabOk=false;}
 try{device=localStorage.getItem(PERSIST)==='1';}catch{}
 try{if(!raw&&device){raw=localStorage.getItem(KEY);device=true;}}catch{}
 if(!raw)return;
 try{const s=JSON.parse(raw);if(s.version!==1||!Array.isArray(s.records)||(!s.active||typeof s.active!=='object'||Array.isArray(s.active))||s.records.some(r=>!M.parse(JSON.stringify(r),units).ok))throw new Error('unvereinbar');store=s;store.views=store.views||{};}
 catch{recoveryRaw=raw;device=false;try{sessionStorage.setItem(RECOVERY,raw);}catch{quarantineOk=false;tabOk=false;}try{localStorage.setItem(PERSIST,'0');}catch{}announce('Die ältere Gerätekopie ist nicht kompatibel. Sie wurde nicht gelöscht oder überschrieben.');}
}
function rememberView(){if(!unit||document.body.dataset.lwPage!=='index.html'||!selected())return;store.views=store.views||{};store.views[unit.id+':'+currentId]={step:step(),scrollY:Math.max(0,window.scrollY||0)};save();}
function selected(){return unit?store.records.find(r=>r.moduleId===unit.id&&r.workspaceId===currentId):null;}
function step(){
 if(!unit)return null;if(document.body.dataset.lwPage==='wiederaufnahme.html')return 'wiederaufnahme';
 const h=location.hash.slice(1);return unit.steps.some(s=>s.id===h)?h:(document.body.dataset.lwPage.startsWith('schritt-')?document.body.dataset.lwPage.slice(8,-5):null)||selected()?.payload.step||unit.steps[0].id;
}
function fieldKey(n){return n.type==='radio'&&n.name?'n:'+n.name:n.id?'i:'+n.id:n.dataset.note?'d:'+n.dataset.note:null;}
function fields(){
 const found=new Map();
 for(const n of document.querySelectorAll('main input,main textarea,main select')){
 if(n.closest('[data-private],[data-category="private"]')||n.type==='file'||n.type==='button'||n.type==='submit')continue;
 const key=fieldKey(n);if(!key||!unit.fields.includes(key)||!M.genericFieldAllowed(unit,key))continue;
 let type=n.type==='checkbox'?'checkbox':n.type==='radio'?'radio':n.tagName==='SELECT'?'select':n.type==='range'?'range':'text';
 if(type==='radio'&&found.has(key)&&!n.checked)continue;
 const value=type==='checkbox'?n.checked:type==='radio'?(n.checked?n.value:''):n.value;
 const label=(n.closest('label')?.textContent||n.getAttribute('aria-label')||n.id||n.name||'Dein Ergebnis').trim().slice(0,120);
 found.set(key,{key,type,value,label,category:'work'});
 }return [...found.values()];
}
function capture(stopTool=false){
 if(!unit||restoring)return;
 if(stopTool&&adapter?.flush)adapter.flush();
 if(!dirty)return;
 const old=selected(),fieldMap=new Map((old?.payload.fields||[]).filter(f=>M.genericFieldAllowed(unit,f.key)).map(f=>[f.key,f]));
 for(const f of fields())fieldMap.set(f.key,f);
 const payload={step:step(),fields:[...fieldMap.values()],tool:adapter?adapter.capture():old?.payload.tool||null};
 const record=M.envelope(unit,payload,currentId,new Date().toISOString()),checked=M.parse(JSON.stringify(record),units);
 if(!checked.ok){captureOk=false;status();announce('Dieser Stand kann noch nicht vollständig gesichert werden: '+checked.message);return;}
 captureOk=true;
 const index=store.records.findIndex(r=>r.workspaceId===currentId&&r.moduleId===unit.id);
 if(index<0)store.records.push(record);else store.records[index]=record;
 store.active[unit.id]=currentId;save();dirty=false;
}
function restoreFields(record){
 for(const f of record.payload.fields){
 if(!M.genericFieldAllowed(unit,f.key))continue;
 const nodes=[...document.querySelectorAll('main input,main textarea,main select')].filter(n=>fieldKey(n)===f.key&&!n.closest('[data-private],[data-category="private"]'));
 for(const n of nodes){if(f.type==='radio')n.checked=n.value===f.value;else if(f.type==='checkbox')n.checked=f.value===true;else n.value=f.value;}
 }
}
function restore(){
 if(!unit)return;adapter=pendingAdapter;
 const record=selected();if(!record)return;
 restoring=true;
 try{restoreFields(record);if(adapter&&record.payload.tool)adapter.restore(copy(record.payload.tool),{step:initialHash||record.payload.step});restoreFields(record);}
 catch{announce('Der Werkzeugstand konnte nicht geöffnet werden. Die gesicherte Arbeit bleibt unter „Deine Arbeit“ erreichbar.');}
 finally{restoring=false;}
}
window.LernwerkMantel={register(value){pendingAdapter=value;if(booted)restore();},changed(){if(restoring)return;dirty=true;queueMicrotask(capture);},capture};
function products(record){
 const u=units.find(x=>x.id===record.moduleId),items=record.payload.fields.filter(f=>M.genericFieldAllowed(u,f.key)&&f.type==='text'&&String(f.value).trim()).map(f=>({title:f.label||'Deine Erklärung',text:String(f.value)})),tool=record.payload.tool;
 if(tool?.kind==='network')for(const [i,h]of tool.state.history.entries())items.push({title:'Netzversuch '+(i+1),text:'Ziel '+h.config.target+' · Unterbrochen: '+(h.config.disabled.join(', ')||'keine')+' · Dienst bereit: '+(h.config.service?'ja':'nein')+'\nVorhersage: '+h.prediction+'\n'+window.NetModel.observe(h).trace.join('\n')});
 if(tool?.family==='algorithm')for(const [id,w]of Object.entries(tool.data.works)){if(w.note&&!items.some(x=>x.text===w.note))items.push({title:u.steps.find(s=>s.id===id)?.title||id,text:w.note});if(w.code)items.push({title:'Programm · '+(u.steps.find(s=>s.id===id)?.title||id),text:w.code});}
 if(tool?.family==='media'&&tool.state.draft.headline)items.push({title:'Dein Bildbeitrag',text:tool.state.draft.headline+'\n'+tool.state.draft.caption+'\nBegründung: '+tool.state.draft.reason+'\nAusschnitt: '+JSON.stringify(tool.state.draft.crop)});
 if(tool?.family==='source')for(const bank of ['claims','transfer'])for(const [id,a]of Object.entries(tool.answers[bank]))if(a.verdict||a.evidence)items.push({title:'Deine Quellenzuordnung · '+id,text:'Urteil: '+(a.verdict||'offen')+'\nTextstelle: '+(a.evidence||'noch nicht gewählt')+(Object.entries(u.evidence).flatMap(([doc,lines])=>lines.map(line=>({...line,doc}))).find(line=>line.id===a.evidence)?'\nQuelle '+a.evidence[0]+': '+Object.values(u.evidence).flat().find(line=>line.id===a.evidence).text:'')});
 return items;
}
function date(r){return new Date(r.savedAt).toLocaleString('de-DE',{timeZone:'Europe/Berlin'});}
function destination(r){const u=units.find(x=>x.id===r.moduleId);return u.area+'/'+(u.family==='content'?'schritt-'+r.payload.step+'.html':r.payload.step==='wiederaufnahme'?'wiederaufnahme.html':'index.html#'+r.payload.step);}
function download(content,name,type){
 const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);announce('Datei angeboten. Prüfe, ob du sie an einem wiederfindbaren Ort gespeichert hast.');
}
function renderWork(){
 const root=$('lw-work-list');if(!root)return;
 root.innerHTML=store.records.length?store.records.map(r=>{
 const u=units.find(x=>x.id===r.moduleId),p=products(r);
 return '<article class="lw-card" style="margin:20px 0"><p class="lw-eyebrow">'+e(u.topic)+' · Begonnen</p><h2>'+e(u.title)+'</h2><p>Stand vom '+e(date(r))+' · '+e(u.steps.find(s=>s.id===r.payload.step)?.title)+'</p><details><summary>Eigenes Produkt ansehen</summary>'+(p.length?p.map(x=>'<h3>'+e(x.title)+'</h3><p class="lw-product">'+e(x.text)+'</p>').join(''):'<p>Ein Werkzeugstand ist vorhanden. Öffne die Aufgabe, um ihn zu untersuchen.</p>')+'</details><div class="lw-actions"><a class="lw-button" data-lw-open="'+e(r.workspaceId)+'" href="'+destination(r)+'">Weiterarbeiten</a><button class="lw-button secondary" data-lw-export="'+e(r.workspaceId)+'">Arbeitsdatei sichern<small>Zum Weiterarbeiten im Lernwerk</small></button><button class="lw-button secondary" data-lw-product="'+e(r.workspaceId)+'">Lesbares Ergebnis sichern<small>Zum Lesen und Zeigen</small></button><button class="lw-button secondary" data-lw-delete="'+e(r.workspaceId)+'">Diesen Stand löschen</button></div><a href="'+u.area+'/index.html?neu=1">Neu beginnen – bisherigen Stand behalten</a></article>';
 }).join(''):'<div class="lw-notice"><p>Hier sind noch keine Antworten oder Werkzeugstände im Lernwerk gespeichert. Wenn du mündlich, im Heft oder in „Dateien“ bzw. im Datei-Explorer gearbeitet hast, erscheint das hier nicht. Deine Gerätearbeit kann trotzdem gelungen sein.</p><a href="index.html">Lerneinheit wählen</a></div>';
 if($('lw-persist'))$('lw-persist').checked=device;
}
async function openFile(file){
 const generation=++fileGeneration;preview=null;const dialog=$('lw-import-dialog');if(dialog.open)dialog.close();if(!file)return;
 if(file.size>M.MAX_BYTES){announce('Diese Datei ist größer als 2 MB. Deine Arbeit bleibt erhalten.');return;}
 let result;try{result=M.parse(await file.text(),units);}catch{result={ok:false,message:'Die Datei konnte nicht gelesen werden.'};}
 if(generation!==fileGeneration)return;
 if(!result.ok){announce(result.message);return;}preview=result.record;
 $('lw-import-preview').innerHTML='<p><b>'+e(result.unit.title)+'</b> · Fassung '+e(result.record.moduleVersion)+'</p><p>Stand vom '+e(date(result.record))+'. '+products(result.record).length+' eigene Ergebnisanteile. Die bestehende Arbeit wird erst bei bestätigter Übernahme geändert.</p>';
 const matches=store.records.filter(r=>r.moduleId===result.record.moduleId);
 $('lw-replace-target').innerHTML=matches.map(r=>'<option value="'+e(r.workspaceId)+'">'+e(date(r))+'</option>').join('');
 document.querySelector('[name=lw-import-mode][value=replace]').disabled=!matches.length;
 document.querySelector('[name=lw-import-mode][value=separate]').checked=true;
 dialog.showModal();
}
async function offline(){
 const target=$('lw-offline-message');if(!navigator.serviceWorker){target.textContent='Diese Umgebung unterstützt das Offlinepaket nicht.';return;}
 target.textContent='Offlinepaket wird vollständig vorbereitet …';
 try{
 const registration=await navigator.serviceWorker.register(new URL('mantel-sw.js',base).href,{scope:base.pathname});
 registration.addEventListener('updatefound',()=>{const installing=registration.installing;installing?.addEventListener('statechange',()=>{if(installing.state==='installed'&&registration.waiting&&navigator.serviceWorker.controller){$('lw-update').hidden=false;target.textContent='Neue Fassung vorbereitet. Übernimm sie, wenn du bereit bist.';}});});
 await registration.update();
 if(registration.waiting){$('lw-update').hidden=false;target.textContent='Neue Fassung vorbereitet. Deine bisherige Fassung bleibt bis zur Übernahme verfügbar.';return;}
 const ready=await Promise.race([navigator.serviceWorker.ready,new Promise((_,reject)=>setTimeout(()=>reject(new Error('Offlinevorbereitung nicht abgeschlossen.')),25000))]);
 const worker=ready.active;if(!worker)throw new Error('Kein aktives Offlinepaket.');
 const channel=new MessageChannel();
 const info=await new Promise((resolve,reject)=>{const timeout=setTimeout(()=>reject(new Error('Prüfung hat nicht geantwortet.')),20000);channel.port1.onmessage=ev=>{clearTimeout(timeout);resolve(ev.data);};worker.postMessage({type:'verify'},[channel.port2]);});
 target.textContent=info.ok?'Offline bereit: alle '+info.count+' Ressourcen geprüft. Fassung '+info.version+'.':'Offlinepaket ist unvollständig. Erneut vorbereiten; benötigte Inhalte bleiben online erreichbar.';
 }catch{target.textContent='Offlinepaket konnte nicht vollständig vorbereitet werden. Deine bisherige Arbeit und ein früheres Paket bleiben erhalten.';}
}
function boot(){
 units=JSON.parse($('lw-catalog').textContent);unit=units.find(u=>u.area===document.body.dataset.lwArea)||null;load();
 if(unit){
 const url=new URL(location.href),fresh=url.searchParams.get('neu')==='1';
 currentId=fresh?uuid():store.active[unit.id]||uuid();
 if(fresh){url.searchParams.delete('neu');history.replaceState(null,'',url);}
 if(unit.family==='content'){
  if(!store.reading||typeof store.reading!=='object'||Array.isArray(store.reading))store.reading={};
  if(fresh)delete store.reading[unit.id];
  const pageStep=document.body.dataset.lwPage.match(/^schritt-(.+)\.html$/)?.[1];
  if(unit.steps.some(s=>s.id===pageStep)){store.reading[unit.id]=pageStep;save();}
 }
 booted=true;restore();
 const view=store.views?.[unit.id+':'+currentId];if(document.body.dataset.lwPage==='index.html'&&view&&(!initialHash||initialHash===view.step))setTimeout(()=>window.scrollTo(0,view.scrollY),100);
 }else booted=true;
 status();renderWork();
 for(const link of document.querySelectorAll('[data-lw-return]')){
 const reading=store.reading?.[unit?.id],r=selected();
 if(unit?.family==='content'&&unit.steps.some(s=>s.id===reading))link.href='schritt-'+reading+'.html';
 else if(r)link.href=destination(r).replace(unit.area+'/','');
 }
 if(recoveryRaw){const button=document.createElement('button');button.id='lw-recovery-export';button.className='lw-button secondary';button.textContent='Ältere Arbeitsdaten unverändert als Datei sichern';button.onclick=()=>download(recoveryRaw,'lernwerk-aeltere-arbeitsdaten.json','application/json');($('lw-work-message')||$('lw-storage-warning')).after(button);}
 if($('lw-emergency-export'))$('lw-emergency-export').onclick=()=>{capture(true);const record=selected();if(!captureOk){const current={fields:fields(),tool:adapter?.capture()||null};download('Lesbare Rettung der aktuellen Eingaben. Keine wiederimportierbare Arbeitsdatei.\n\n'+JSON.stringify(current,null,2),'lernwerk-aktuelle-eingaben.txt','text/plain;charset=utf-8');}else if(record)download(JSON.stringify(record,null,2),'lernwerk-'+record.moduleId+'-'+record.workspaceId+'.json','application/json');else announce('Es liegt noch kein sicherbarer Stand vor.');};
 document.addEventListener('keydown',event=>{if(event.key==='Escape')for(const menu of document.querySelectorAll('[data-lw-menu][open]')){menu.open=false;menu.querySelector('summary').focus();}});
 document.addEventListener('input',event=>{if(unit&&(event.target.closest('main')||event.target.id==='raw-code')&&!event.target.closest('[data-private],[data-category=private]'))window.LernwerkMantel.changed();});
 document.addEventListener('change',event=>{if(unit&&(event.target.closest('main')||event.target.id==='raw-code')&&!event.target.closest('[data-private],[data-category=private]'))window.LernwerkMantel.changed();});
 document.addEventListener('click',event=>{
 const close=event.target.closest('[data-lw-close-menu]');if(close){const menu=close.closest('details');menu.open=false;menu.querySelector('summary').focus();}
 const link=event.target.closest('a');if(link){
 if(link.dataset.lwOpen){const r=store.records.find(x=>x.workspaceId===link.dataset.lwOpen);if(r){store.active[r.moduleId]=r.workspaceId;save();}}
 if(unit){rememberView();capture(true);}
 if((!tabOk&&store.records.length||!captureOk||!quarantineOk)&&link.target!=='_blank'&&!link.href.startsWith(location.href.split('#')[0]+'#')){event.preventDefault();announce('Deine aktuelle Arbeit ist noch nicht sicher mitnehmbar. Sichere sie hier als Datei oder korrigiere die Eingabe, bevor du die Seite verlässt.');}
 }
 const button=event.target.closest('button');if(!button)return;
 if(unit&&button.closest('main'))window.LernwerkMantel.changed();
 if(button.dataset.privateExport){privateNote=$(button.dataset.privateExport).value;$('lw-private-preview').textContent=privateNote;$('lw-private-dialog').showModal();}
 const id=button.dataset.lwExport||button.dataset.lwProduct||button.dataset.lwDelete;
 const record=store.records.find(r=>r.workspaceId===id);
 if(record&&button.dataset.lwExport)download(JSON.stringify(record,null,2),'lernwerk-'+record.moduleId+'-'+record.workspaceId+'.json','application/json');
 if(record&&button.dataset.lwProduct)download(products(record).map(p=>p.title+'\n'+p.text).join('\n\n'),'lernwerk-ergebnis-'+record.moduleId+'.txt','text/plain;charset=utf-8');
 if(record&&button.dataset.lwDelete&&confirm('Nur diesen eigenen Arbeitsstand löschen? Bereits heruntergeladene Dateien bleiben erhalten.')){store.records=store.records.filter(r=>r.workspaceId!==id);if(store.active[record.moduleId]===id)delete store.active[record.moduleId];save();renderWork();}
 });
 window.addEventListener('pagehide',()=>{rememberView();capture(true);});
 window.addEventListener('beforeunload',event=>{capture();if((!tabOk&&store.records.length)||!captureOk||!quarantineOk){event.preventDefault();event.returnValue='';}});
 if($('lw-private-confirm'))$('lw-private-confirm').onclick=()=>{download(privateNote,'lernwerk-private-notiz.txt','text/plain;charset=utf-8');$('lw-private-dialog').close();privateNote='';};
 if($('lw-private-cancel'))$('lw-private-cancel').onclick=()=>{$('lw-private-dialog').close();privateNote='';};
 // Open only the selected editorial helpers for printing, then restore the reading state.
 const printMode=$('lw-print-mode'), printDetails=new Map();
 if(printMode){
  document.body.dataset.lwPrint=printMode.value;
  printMode.addEventListener('change',()=>{document.body.dataset.lwPrint=printMode.value;});
 }
 window.addEventListener('beforeprint',()=>{
  const mode=printMode?.value||'learner';
  document.body.dataset.lwPrint=mode;
  for(const detail of document.querySelectorAll('.lw-author .lw-help,.lw-author .lw-solution,.lw-author .lw-device-route')){
   if(!printDetails.has(detail))printDetails.set(detail,detail.open);
   detail.open=detail.classList.contains('lw-device-route')||(detail.classList.contains('lw-solution')?mode==='solutions':mode!=='learner');
  }
 });
 window.addEventListener('afterprint',()=>{for(const [detail,open] of printDetails)detail.open=open;printDetails.clear();});
 if($('lw-print'))$('lw-print').onclick=()=>window.print();
 if($('lw-persist'))$('lw-persist').addEventListener('change',event=>{
 device=event.target.checked;
 if(device)save();else{try{localStorage.setItem(PERSIST,'0');}catch{}status();announce('Neue Gerätesicherung ausgeschaltet. Eine ältere Gerätekopie bleibt bis zum ausdrücklichen Löschen.');}
 event.target.checked=device;
 });
 if($('lw-file'))$('lw-file').addEventListener('change',event=>{const file=event.target.files[0];event.target.value='';openFile(file);});
 if($('lw-import-dialog')){
 $('lw-import-dialog').addEventListener('close',()=>{preview=null;});
 $('lw-import-cancel').onclick=()=>{++fileGeneration;preview=null;$('lw-import-dialog').close();};
 $('lw-import-confirm').onclick=()=>{
 if(!preview)return;const mode=document.querySelector('[name=lw-import-mode]:checked').value;
 try{store=M.accept(store,preview,mode,mode==='separate'?uuid():$('lw-replace-target').value);const secured=save();$('lw-import-dialog').close();preview=null;renderWork();announce(secured?'Arbeitsstand übernommen und im Tab gesichert. Öffne ihn mit „Weiterarbeiten“.':'Arbeitsstand ist nur hier geöffnet. Tabsicherung fehlgeschlagen: Sichere ihn als Arbeitsdatei, bevor du wechselst.');}catch{announce('Übernahme nicht möglich. Deine Arbeit bleibt erhalten.');}
 };
 }
 if($('lw-delete-device'))$('lw-delete-device').onclick=()=>{if(confirm('Die Gerätekopie löschen? Die Arbeit im geöffneten Tab bleibt erhalten.')){try{localStorage.removeItem(KEY);localStorage.removeItem(PERSIST);device=false;status();$('lw-persist').checked=false;announce('Gerätekopie gelöscht; Tabarbeit bleibt erhalten.');}catch{announce('Gerätespeicher ist nicht zugänglich.');}}};
 if($('lw-delete-all'))$('lw-delete-all').onclick=()=>{if(confirm('Alle eigenen Klasse-5-Lernwerkstände dieses Browserprofils löschen? Heruntergeladene Dateien bleiben außerhalb des Lernwerks.')){try{sessionStorage.removeItem(KEY);sessionStorage.removeItem(RECOVERY);localStorage.removeItem(KEY);localStorage.removeItem(PERSIST);store={version:1,records:[],active:{}};device=false;recoveryRaw=null;quarantineOk=true;captureOk=true;tabOk=true;$('lw-recovery-export')?.remove();renderWork();status();}catch{announce('Nicht alle Speicherbereiche konnten gelöscht werden. Prüfe den Browser.');}}};
 if($('lw-offline'))$('lw-offline').onclick=offline;
 if($('lw-update'))$('lw-update').onclick=async()=>{capture();const r=await navigator.serviceWorker.getRegistration(base.href);if(r?.waiting){if(!tabOk||!captureOk||!quarantineOk){announce('Tabsicherung ist eingeschränkt. Sichere zuerst eine Arbeitsdatei; die neue Fassung wurde noch nicht übernommen.');return;}navigator.serviceWorker.addEventListener('controllerchange',()=>location.reload(),{once:true});r.waiting.postMessage({type:'activate'});}};
 if(installEvent&&$('lw-install'))$('lw-install').hidden=false;
 if($('lw-install'))$('lw-install').onclick=async()=>{if(installEvent){await installEvent.prompt();installEvent=null;$('lw-install').hidden=true;}};
}
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installEvent=event;if($('lw-install'))$('lw-install').hidden=false;});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
