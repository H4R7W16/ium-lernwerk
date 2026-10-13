/* Finite teaching model: possible paths, no Internet routing algorithm. MIT. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.NetModel=api;})(globalThis,function(){
'use strict';
const graphs={main:['K-A','A-L','A-B','A-C','B-C','B-D','C-D','D-W'],transfer:['K-X','X-Y','X-Z','Y-Z','Y-L','Z-W']};
const copy=x=>JSON.parse(JSON.stringify(x));
const edges=(g='main')=>graphs[g]||[];
const neighbors=(node,g='main')=>edges(g).filter(e=>e.split('-').includes(node)).map(e=>e.split('-').find(n=>n!==node));
const edge=(a,b)=>edges().find(e=>e===a+'-'+b||e===b+'-'+a);
function reachable(config,g='main'){const seen=new Set(['K']),queue=['K'];while(queue.length){const n=queue.shift();if(['L','W'].includes(n))continue;for(const e of edges(g)){if((config.disabled||[]).includes(e))continue;const ns=e.split('-');if(!ns.includes(n))continue;const v=ns.find(x=>x!==n);if(!seen.has(v)){seen.add(v);queue.push(v);}}}return [...seen];}
function create(){return {version:1,draft:{target:'W',disabled:[],service:true,prediction:''},current:null,history:[]};}
function configure(state,patch){if(state.current)throw new Error('Beende zuerst den laufenden Versuch.');const s=copy(state);s.draft={...s.draft,...patch};if(!valid(s))throw new Error('Ungültige Versuchseinstellung.');return s;}
function start(state){if(state.current)throw new Error('Der Versuch läuft bereits.');if(!state.draft.prediction.trim())throw new Error('Notiere zuerst deine Vermutung und einen Grund.');if(state.history.length>=50)throw new Error('50 Versuche sind gespeichert. Sichere deine Arbeitsdatei; beginne einen neuen Stand unter „Deine Arbeit“.');const s=copy(state);const {prediction,...config}=s.draft;s.current={config,prediction,moves:[]};return s;}
function observe(t){const result={phase:'request',path:['K'],at:'K',outcome:null,trace:['Anfrage nach plan.txt startet bei K.']};let replyIndex=0;
 for(const n of t.moves){if(result.outcome)throw new Error('Versuch war bereits beendet.');if(n==='stop'){result.outcome='stopped';result.trace.push('Versuch vorzeitig beendet. Keine Aussage über alle Wege.');continue;}
 if(result.phase==='reply'){if(n!=='reply')throw new Error('Antwort: einen Schritt zurück wählen.');result.at=result.path[--replyIndex];result.trace.push('Dateiantwort erreicht '+result.at+'.');if(replyIndex===0)result.outcome='answered';continue;}
 if(!neighbors(result.at).includes(n)||result.path.includes(n))throw new Error('Wähle einen benachbarten, noch nicht besuchten Knoten.');const e=edge(result.at,n);if(t.config.disabled.includes(e)){result.outcome='blocked';result.trace.push('Anfrage stoppt vor '+e+': Verbindung unterbrochen. Nur dieser Versuch ist gescheitert.');continue;}
 result.at=n;result.path.push(n);result.trace.push('Anfrage erreicht '+n+'.');if(['L','W'].includes(n)){if(n!==t.config.target){result.outcome='wrong-target';result.trace.push('Anderer Endknoten erreicht; Endknoten leiten hier nicht weiter.');}else if(!t.config.service){result.outcome='no-service';result.trace.push('Ziel erreicht, Dateidienst nicht bereit: keine Dateiantwort.');}else{result.phase='reply';replyIndex=result.path.length-1;result.trace.push(n+' stellt plan.txt bereit. Die Antwort folgt hier vereinfacht dem gewählten Weg zurück.');}}
 }return result;}
function move(state,node){if(!state.current)throw new Error('Starte zuerst einen Versuch.');const s=copy(state);s.current.moves.push(node);const r=observe(s.current);if(r.outcome){s.history.push(s.current);s.current=null;}return s;}
const stop=s=>move(s,'stop');
function reset(state){if(state.current)throw new Error('Beende zuerst den laufenden Versuch.');return {...copy(state),draft:create().draft};}
const exact=(o,ks)=>o&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).length===ks.length&&Object.keys(o).every(k=>ks.includes(k));
const config=c=>exact(c,['target','disabled','service'])&&['L','W'].includes(c.target)&&typeof c.service==='boolean'&&Array.isArray(c.disabled)&&c.disabled.length<=8&&new Set(c.disabled).size===c.disabled.length&&c.disabled.every(e=>edges().includes(e));
const prediction=p=>typeof p==='string'&&p.length<=2000;
function valid(s){try{if(!exact(s,['version','draft','current','history'])||s.version!==1||!exact(s.draft,['target','disabled','service','prediction']))return false;const {prediction:p,...c}=s.draft;if(!config(c)||!prediction(p)||!Array.isArray(s.history)||s.history.length>50)return false;const trial=(t,finished)=>exact(t,['config','prediction','moves'])&&config(t.config)&&prediction(t.prediction)&&!!t.prediction.trim()&&Array.isArray(t.moves)&&t.moves.length<=16&&Boolean(observe(t).outcome)===finished;if(!s.history.every(t=>trial(t,true)))return false;return s.current===null||(s.history.length<50&&trial(s.current,false)&&s.current.prediction===s.draft.prediction&&JSON.stringify(s.current.config)===JSON.stringify(c));}catch{return false;}}
return {create,configure,start,move,stop,reset,observe,reachable,neighbors,edges,valid};
});
