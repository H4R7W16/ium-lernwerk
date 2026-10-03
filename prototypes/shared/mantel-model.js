(function(root,factory){const api=factory(root,typeof module==='object'&&module.exports?{W:require('../m06-lernwerkstatt/workshop-model.js'),S:require('../m06-lernstudio/studio-model.js')}:null);if(typeof module==='object'&&module.exports)module.exports=api;else root.LernwerkMantelModel=api;})(globalThis,function(root,models){
'use strict';
const MAX_BYTES=2*1024*1024,uuid=/^[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
const clone=value=>JSON.parse(JSON.stringify(value));
function plain(o){return o!==null&&typeof o==='object'&&!Array.isArray(o);}
function keys(o,allowed){return plain(o)&&Object.keys(o).every(k=>allowed.includes(k));}
const str=(v,max=10000)=>typeof v==='string'&&v.length<=max;
const int=(v,a,b)=>Number.isInteger(v)&&v>=a&&v<=b;
function safe(o,depth=0){if(depth>16)return false;if(typeof o==='string')return o.length<=20000;if(typeof o==='number')return Number.isFinite(o);if(o===null||typeof o==='boolean')return true;if(Array.isArray(o))return o.length<=1000&&o.every(v=>safe(v,depth+1));return plain(o)&&Object.keys(o).length<=300&&Object.entries(o).every(([k,v])=>!['__proto__','constructor','prototype'].includes(k)&&safe(v,depth+1));}
function toolValid(tool,unit){
 if(tool===null||tool===undefined)return true;
 if(!plain(tool)||tool.family!==unit.family||!safe(tool))return false;
 if(unit.family==='algorithm'){
  const W=models?.W||root.Workshop,S=models?.S||root.Studio,d=tool.data;
  if(!W||!S||!keys(tool,['family','data','display'])||!keys(d,['version','current','works'])||d.version!==1||!S.order.includes(d.current)||!plain(d.works))return false;
  try{
   for(const [id,s]of Object.entries(d.works)){
    if(!S.order.includes(id)||!keys(s,['code','note','step','observed','checked','independent','attempts','choice','help','prediction','sequence','undo','previous','plan','compared'])||!str(s.code,2500)||!str(s.note)||!int(s.step,0,10000)||!int(s.attempts,0,999)||!int(s.help,0,3)||!(s.choice===null||int(s.choice,0,2))||!['A','B'].includes(s.plan))return false;
    if(!['observed','checked','independent'].every(k=>typeof s[k]==='boolean')||!Array.isArray(s.sequence)||s.sequence.length>30||!s.sequence.every(x=>['vor','links','rechts'].includes(x))||!Array.isArray(s.undo)||s.undo.length>30||!s.undo.every(x=>str(x,2500))||!Array.isArray(s.compared)||!s.compared.every(x=>['A','B'].includes(x)))return false;
    W.blocks(s.code);for(const code of s.undo)W.blocks(code);
    const lesson=W.lesson(id),trace=id==='transfer'?W.station(s.plan):S.run(id,s.code);
    if(s.step>=trace.trace.length)return false;
    if(s.prediction!==null&&(!lesson.room||!Array.isArray(s.prediction)||s.prediction.length!==3||!int(s.prediction[0],1,lesson.room.width)||!int(s.prediction[1],1,lesson.room.height)||!int(s.prediction[2],0,3)))return false;
    if(s.previous!==null&&(!keys(s.previous,['code','step','pos','cleaned','error'])||!str(s.previous.code,2500)||!int(s.previous.step,0,10000)||!Array.isArray(s.previous.pos)||s.previous.pos.length!==3||!s.previous.pos.every(Number.isInteger)||!int(s.previous.cleaned,0,1000)||typeof s.previous.error!=='boolean'))return false;
   }
   const v=tool.display;
   if(v!==undefined){
    if(!keys(v,['showTrail','speed','comparisonStep','rawDraft','editor'])||typeof v.showTrail!=='boolean'||!int(v.speed,100,3000)||!int(v.comparisonStep,0,10000)||!(v.rawDraft===null||str(v.rawDraft,2500)))return false;
    if(v.editor!==undefined&&v.editor!==null){
     const x=v.editor,b=x.block;
     if(!keys(x,['index','indexNew','block'])||!int(x.index,0,30)||typeof x.indexNew!=='boolean'||!keys(b,['repeat','count','body'])||typeof b.repeat!=='boolean'||!int(b.count,1,9)||!Array.isArray(b.body)||b.body.length>5||!b.body.every(a=>['vor','links','rechts'].includes(a)))return false;
    }
   }
   return true;
  }catch{return false;}
 }
 if(unit.family==='media'){
  const s=tool.state;
  if(!keys(tool,['family','state','current'])||!keys(s,['notes','answers','transferAnswers','checked','transferChecked','calibration','calibrationChecked','mode','crop','headline','draft','review','criteria','revised','decision'])||!int(tool.current,0,unit.steps.length-2)||!plain(s.notes)||!keys(s.draft,['crop','headline','caption','reason']))return false;
  const crop=c=>keys(c,['x','width'])&&Number.isFinite(c.x)&&Number.isFinite(c.width)&&c.width>=600&&c.width<=1536&&c.x>=0&&c.x<=1536-c.width;
  const answers=(a,ids,choices)=>plain(a)&&Object.entries(a).every(([id,v])=>ids.includes(id)&&(v===''||choices.includes(v)));
  return crop(s.crop)&&crop(s.draft.crop)&&['crop','headline'].includes(s.mode)&&str(s.headline,100)&&str(s.draft.headline,100)&&str(s.draft.caption,450)&&str(s.draft.reason,700)&&['','change','keep'].includes(s.decision)&&['','weak','strong'].includes(s.calibration)&&Object.entries(s.notes).every(([id,v])=>unit.fields.includes('d:'+id)&&str(v))&&answers(s.answers,unit.mediaClaims,unit.mediaChoices)&&answers(s.transferAnswers,unit.mediaTransfer,unit.mediaTransferChoices)&&plain(s.criteria)&&Object.entries(s.criteria).every(([k,v])=>['0','1','2','3'].includes(k)&&typeof v==='boolean')&&['checked','transferChecked','calibrationChecked','review','revised'].every(k=>typeof s[k]==='boolean');
 }
 if(unit.family==='source'){
  if(!keys(tool,['family','answers','active','documents'])||!keys(tool.answers,['claims','transfer'])||!plain(tool.answers.claims)||!plain(tool.answers.transfer)||!keys(tool.active,['claims','transfer']))return false;
  if(!unit.claims)return true;
  if(tool.documents!==undefined&&(!keys(tool.documents,['explore','claims','transfer'])||Object.entries(tool.documents).some(([bank,id])=>!unit.sourceBanks[bank].includes(id))))return false;
  return ['claims','transfer'].every(bank=>unit.claims[bank].includes(tool.active[bank])&&Object.entries(tool.answers[bank]).every(([id,a])=>unit.claims[bank].includes(id)&&keys(a,['verdict','evidence','checked'])&&['','belegt','widerlegt','offen',undefined].includes(a.verdict)&&(a.evidence===undefined||a.evidence===''||a.evidence==='none'||unit.sourceBanks[bank].some(doc=>unit.evidence[doc].some(line=>line.id===a.evidence)))&&(!('checked' in a)||typeof a.checked==='boolean')));
 }
 return false;
}
function genericFieldAllowed(unit,key){return unit.family!=='algorithm'&&unit.family!=='media'||key==='i:lw-retrieval';}
function envelope(unit,payload,id,date){return {format:'ium-learning-state',formatVersion:1,moduleId:unit.id,moduleVersion:unit.version,stateSchemaVersion:1,workspaceId:id,savedAt:date,payload:{schema:'klasse5-mantel-1',family:unit.family,...clone(payload)}};}
function parse(text,units){
 const bad=message=>({ok:false,message});if(typeof text!=='string'||new TextEncoder().encode(text).length>MAX_BYTES)return bad('Die Arbeitsdatei ist zu groß (höchstens 2 MB).');
 try{
 const r=JSON.parse(text);if(!safe(r)||!keys(r,['format','formatVersion','moduleId','moduleVersion','stateSchemaVersion','workspaceId','savedAt','payload'])||r.format!=='ium-learning-state'||r.formatVersion!==1||r.stateSchemaVersion!==1||!uuid.test(r.workspaceId)||typeof r.savedAt!=='string'||!Number.isFinite(Date.parse(r.savedAt)))return bad('Die Datei ist keine unterstützte Lernwerk-Arbeitsdatei.');
 const unit=units.find(u=>u.id===r.moduleId);if(!unit||r.moduleVersion!==unit.version)return bad('Diese Arbeitsdatei passt nicht zu einer verfügbaren Lerneinheit/Fassung.');
 const p=r.payload;if(!keys(p,['schema','family','step','fields','tool'])||p.schema!=='klasse5-mantel-1'||p.family!==unit.family||!unit.steps.some(s=>s.id===p.step)||!Array.isArray(p.fields)||p.fields.length>300||!toolValid(p.tool,unit))return bad('Aufgabe oder Werkzeugdaten sind nicht kompatibel.');
 if(p.fields.some(f=>!keys(f,['key','value','type','label','category'])||!unit.fields.includes(f.key)||!['text','radio','checkbox','select','range'].includes(f.type)||!(f.type==='checkbox'?typeof f.value==='boolean':str(f.value))||('category' in f&&f.category!=='work')||('label' in f&&!str(f.label,120))))return bad('Die Datei enthält unbekannte oder private Datenfelder.');
 return {ok:true,record:clone(r),unit};
 }catch{return bad('Diese Datei konnte nicht gelesen werden. Deine bisherige Arbeit bleibt erhalten.');}
}
function accept(store,record,mode,newId){
 const next=clone(store),r=clone(record);if(mode==='separate'){if(!uuid.test(newId))throw new Error('Ungültige Stand-ID');r.workspaceId=newId;next.records.push(r);}
 else if(mode==='replace'){const index=next.records.findIndex(x=>x.workspaceId===newId&&x.moduleId===r.moduleId);if(index<0)throw new Error('Der zu ersetzende Stand fehlt.');r.workspaceId=newId;next.records[index]=r;}
 else throw new Error('Unbekannte Übernahme');
 next.active[r.moduleId]=r.workspaceId;return next;
}
return {MAX_BYTES,clone,parse,envelope,accept,toolValid,genericFieldAllowed};
});
