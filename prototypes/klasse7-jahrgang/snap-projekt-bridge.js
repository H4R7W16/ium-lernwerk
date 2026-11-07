/* ALG-5-Projektbrücke für die abgeleitete Snap!-Ansicht. AGPL-3.0-or-later. */
(function(root,factory){
 'use strict';const api=factory(root);
 if(typeof module==='object'&&module.exports)module.exports=api;
 else root.LernwerkProjectBridgeFactory=api.createBridge;
}(typeof globalThis!=='undefined'?globalThis:this,function(root){
 'use strict';
 const MAX_BYTES=10*1024*1024;
 function validateProjectXML(xml,parseXML){
  if(typeof xml!=='string'||!xml.trim())throw Error('Bitte wähle ein vollständiges Snap!-Projekt.');
  if(new TextEncoder().encode(xml).length>MAX_BYTES)throw Error('Dieses Projekt ist größer als 10 MB. Sichere es als eigene XML-Datei.');
  if(/<!DOCTYPE|<!ENTITY/i.test(xml))throw Error('Dieses Snap!-Projekt enthält nicht unterstützte XML-Angaben.');
  const parse=parseXML||(text=>new root.DOMParser().parseFromString(text,'application/xml'));
  const doc=parse(xml);
  if(!doc||doc.querySelector('parsererror')||doc.documentElement?.tagName!=='project'||!doc.querySelector('scene stage'))throw Error('Die Datei ist kein vollständiges, gültiges Snap!-Projekt.');
  return xml;
 }
 function createBridge(host){
  let baseline=null,lastCapture=null,sequence=0,busy=false,broken=false,recovery=null;
  const nativeState=()=>({scene:host.scene(),version:host.revision()});
  function ensureBaseline(){if(!baseline&&host.ready())baseline=nativeState();}
  function checkReady(){if(busy)throw Error('Ein Projekt wird gerade geladen. Bitte warte kurz.');if(!host.ready()||broken)throw Error('Der Editor ist noch nicht bereit. Dein gesicherter Stand bleibt erhalten.');ensureBaseline();}
  function isDirty(){if(busy||broken)return true;if(!host.ready())return false;ensureBaseline();return host.scene()!==baseline.scene||host.revision()!==baseline.version||Boolean(host.dirty());}
  function capture(){host.stop();const xml=validateProjectXML(host.xml(),host.parseXML);return {xml,name:String(host.name()||'Mein Rover'),...nativeState()};}
  function getSnapshot(){checkReady();const current=capture();lastCapture={...current,revision:++sequence};return {xml:current.xml,name:current.name,revision:lastCapture.revision};}
  function markSaved(revision){
   if(busy||broken||!lastCapture||(revision!==undefined&&revision!==lastCapture.revision)||!host.ready())return false;
   if(host.scene()!==lastCapture.scene||host.revision()!==lastCapture.version)return false;
   // Edits can share a millisecond timestamp; compare the actual captured XML too.
   if(host.xml()!==lastCapture.xml)return false;
   host.markSaved();host.stop();baseline=nativeState();lastCapture=null;return true;
  }
  function load(xml){
   const previousScene=host.scene();
   return new Promise((resolve,reject)=>{
    let settled=false;
    const timer=setTimeout(()=>{if(settled)return;settled=true;host.cancelLoad?.();reject(Error('Das Öffnen dauert zu lange.'));},host.timeoutMs||20000);
    const complete=()=>{if(settled)return;settled=true;clearTimeout(timer);
     try{if(host.scene()===previousScene)throw Error('Snap! konnte dieses Projekt nicht öffnen.');host.afterOpen();resolve();}catch(error){reject(error);}
    };
    try{host.openXML(xml,complete);}catch(error){if(!settled){settled=true;clearTimeout(timer);reject(error);}}
   });
  }
  async function openProject(xml,options={}){
   checkReady();validateProjectXML(xml,host.parseXML);
   if(isDirty()&&!options.discardChanges)throw Error('Im geöffneten Projekt gibt es Änderungen. Übernimm sie zuerst oder bestätige ausdrücklich das Verwerfen.');
   const previousDirty=isDirty(),previous=capture();busy=true;lastCapture=null;recovery=null;
   try{await load(xml);host.markSaved();host.stop();baseline=nativeState();return {name:String(host.name()||'Mein Rover')};}
   catch(error){
    host.cancelLoad?.();
    try{await load(previous.xml);if(previousDirty){host.markDirty();host.stop();}else{host.markSaved();host.stop();baseline=nativeState();}}
    catch(restoreError){broken=true;recovery={xml:previous.xml,name:previous.name};const failure=Error('Das Projekt konnte nicht geöffnet und die vorherige Ansicht nicht wiederhergestellt werden. Der zuvor erfasste Projektstand ist als Rettungskopie verfügbar.');failure.recoverySnapshot=recovery;throw failure;}
    throw Error('Das Projekt konnte nicht geöffnet werden. Dein vorheriger Stand wurde wiederhergestellt.');
   }finally{busy=false;}
  }
  return Object.freeze({get ready(){ensureBaseline();return Boolean(host.ready()&&!busy&&!broken);},get recoverySnapshot(){return recovery;},getSnapshot,openProject,isDirty,markSaved});
 }
 return Object.freeze({createBridge,validateProjectXML,MAX_BYTES});
}));


