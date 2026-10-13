'use strict';
(function(root){
 const Core=typeof module!=='undefined'&&module.exports?require('./cleaning-core.js'):root.CleaningModel;
 const pages=['start','loop','practice','after','plan','check','return','knowledge'];
 const rooms={square:{width:2,height:2,start:[1,2,1]},plan:{width:3,height:2,start:[1,2,1]},own:{width:4,height:3,start:[1,3,1]}};
 const examples={square:'wiederhole 4 [vor; links]',after:'wiederhole 4 [vor; links]\nvor',plan:'wiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]',own:'wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]'};
 const exercises={practice:{code:'wiederhole 3 [rechts; vor]',runs:3,actions:6},final:{code:'wiederhole 3 [links; vor]\nrechts',runs:3,actions:7},retry:{code:'wiederhole 2 [vor; rechts]\nlinks',runs:2,actions:5},return:{code:'wiederhole 2 [rechts; vor; links]\nvor',runs:2,actions:7}};
 function expand(code){return Core.parse(code).flatMap(b=>Array.from({length:b.count},(_,i)=>b.body.map((action,bodyIndex)=>({action,line:b.line,iteration:b.repeat?i+1:null,repeat:b.repeat,count:b.count,bodyIndex,bodyLength:b.body.length}))).flat());}
 function simulate(room,code){const result=Core.run(room,Core.parse(code)),steps=expand(code);result.trace=result.trace.map((s,i)=>({...s,...(i?steps[i-1]:{})}));return result;}
 function compare(text,expected){
  const actual=text.trim().toLowerCase().split(/[\s;|,→]+/u).filter(Boolean);
  if(!actual.length)return {ok:false,kind:'empty',index:0,expected:expected[0]};
  for(let i=0;i<Math.max(actual.length,expected.length);i++){if(actual[i]!==undefined&&!['vor','links','rechts'].includes(actual[i]))return {ok:false,kind:'unknown',index:i,actual:actual[i]};if(actual[i]!==expected[i])return {ok:false,kind:actual[i]===undefined?'missing':expected[i]===undefined?'extra':'different',index:i,expected:expected[i],actual:actual[i]};}
  return {ok:true};
 }
 function checkSequence(id,a){const e=exercises[id];if(!e)throw new Error('Unbekannte Aufgabe');const sequence=compare(a.sequence||'',expand(e.code).map(s=>s.action)),actualRuns=String(a.runs??'').trim(),actualActions=String(a.actions??'').trim(),runs=String(e.runs)===actualRuns,actions=String(e.actions)===actualActions;return {sequence,runs,actions,counts:{runs:{ok:runs,actual:actualRuns,expected:e.runs},actions:{ok:actions,actual:actualActions,expected:e.actions}},ok:sequence.ok&&runs&&actions};}
 function checkGrouping(program,expected){
   const syntax=inspectProgram(program);
   if(!syntax.ok)return {ok:false,error:syntax.kind==='comma'?`Zeile ${syntax.line}: Zwischen den Grundanweisungen steht ein Komma. In dieser Schreibweise trennt ein Semikolon ; die Anweisungen.`:syntax.message,syntax};
   try{const blocks=syntax.blocks,actual=expand(program).map(s=>s.action),sequence=compare(actual.join(' '),expected),loop=blocks.some(b=>b.repeat);return {ok:sequence.ok&&loop,sequence,loop};}
   catch(e){return {ok:false,error:e.message};}
  }
 function inspectProgram(code){
  const lines=String(code??'').split(/\r?\n/u);
  for(let index=0;index<lines.length;index++){
   const line=lines[index],comma=line.indexOf(',');
   if(comma>=0&&/^\s*wiederhole\s+\d+\s*\[[^\]]*,[^\]]*\]\s*$/iu.test(line))return {ok:false,kind:'comma',line:index+1,column:comma+1,actual:',',expected:';',corrected:line.slice(0,comma)+';'+line.slice(comma+1)};
  }
  // Localize an invalid basic instruction before falling back to the parser.
  for(let index=0;index<lines.length;index++){
   const match=/^\s*wiederhole\s+\d+\s*\[([^\[\]]*)\]\s*$/iu.exec(lines[index]);if(!match)continue;
   const words=match[1].split(';').map(word=>word.trim());
   const wrong=words.findIndex(word=>!['vor','links','rechts'].includes(word.toLowerCase()));
   if(wrong>=0)return {ok:false,kind:'syntax',line:index+1,message:words[wrong]?`Zeile ${index+1}: „${words[wrong]}“ ist keine Grundanweisung. Schreibe an dieser Stelle vor, links oder rechts; trenne Anweisungen mit ;.`:`Zeile ${index+1}: In der Klammer steht eine leere Anweisung an Stelle ${wrong+1}. Ergänze vor, links oder rechts oder entferne das zusätzliche Semikolon.`};
  }
  try{return {ok:true,blocks:Core.parse(String(code??''))};}
  catch(error){return {ok:false,kind:'syntax',message:error.message.replace(' Keine verschachtelte Wiederholung.','')};}
 }
 function assessPlan(room,code){
  const syntax=inspectProgram(code);
  if(!syntax.ok){
   if(syntax.kind==='comma')return {...syntax,message:`In Zeile ${syntax.line} steht zwischen den Grundanweisungen ein Komma. In dieser Schreibweise trennt ein Semikolon ; die Anweisungen.`,nextStep:`Ersetze in Zeile ${syntax.line} nur das Komma durch ; und führe den Plan erneut aus. Vergleich: ${syntax.corrected}`,application:{id:'comma-probe',prompt:'Berichtige nur das Trennzeichen: wiederhole 2 [rechts, vor].'}};
   return {...syntax,nextStep:'Korrigiere zuerst nur die genannte Schreibstelle. Erst mit ausführbarem Code lässt sich die Fahrt beurteilen.',application:null};
  }
  const result=simulate(room,code),trace=result.trace;
  if(result.status==='wall'){
   const stopped=trace.at(-1),step=trace.length-1,wall={step,line:stopped.line,iteration:stopped.iteration,position:[...stopped.pos]};
   const fourAcross=step===4&&trace.slice(1).every(entry=>entry.action==='vor')&&room.start[0]===1&&room.start[2]===1&&room.width===4;
   return {kind:'wall',result,wall,message:fourAcross?'Bei der vierten Fahrt steht der Roboter bereits rechts unten und blickt zur Wand. Diese Fahrt erreicht keine weitere Kachel; das Programm hält dort an.':`In Schritt ${step}, Zeile ${stopped.line}${stopped.iteration?', Durchlauf '+stopped.iteration:''}, trifft vor auf eine Wand. Der Roboter bleibt in Spalte ${stopped.pos[0]}, Reihe ${stopped.pos[1]} stehen; spätere Anweisungen werden nicht ausgeführt.`,nextStep:fourAcross?'Markiere die vier Kacheln. Zwischen ihnen liegen nur drei Wege: Ändere die Schleifenzahl auf 3 und führe erneut aus.':'Gehe in der Fahrt eine Anweisung zurück. Prüfe dort Standort und Blick, und ändere nur die nächste Fahrt oder die unmittelbar davor geplante Drehung.',application:{id:'p6-probe',prompt:'Probiere die neue Aufgabe ab Spalte 2: Wie viele Fahrten bleiben bis zum Rand?'}};
  }
  const lowerRows=Array.from({length:room.width},(_,x)=>[`${x+1},2`,`${x+1},3`]).flat();
  const upperRow=Array.from({length:room.width},(_,x)=>`${x+1},1`);
  const secondSwitch=room.width===4&&room.height===3&&upperRow.every(cell=>result.missing.includes(cell))?trace.findIndex((step,index)=>index>0&&index<trace.length-1&&step.action==='links'&&trace[index-1].pos[0]===1&&trace[index-1].pos[1]===2&&trace[index-1].pos[2]===3&&lowerRows.every(cell=>trace[index-1].cleaned.includes(cell))&&trace[index+1].action==='vor'&&trace[index+1].pos[0]===1&&trace[index+1].pos[1]===3):-1;
  if(result.status==='complete'&&!result.success&&secondSwitch>0)return {kind:'second-row-switch',result,difference:{index:secondSwitch,actual:'links',expected:'rechts'},message:'Die untere und mittlere Reihe sind erreicht, die obere bleibt offen. Beim Wechsel steht der Roboter links in der Mitte und blickt nach links. links und vor führen zurück nach unten.',nextStep:`Gehe zu Anweisung ${secondSwitch}. Drehe dort den Pfeil probeweise mit rechts nach oben und führe dann nur rechts → vor → rechts aus.`,application:{id:'p7-probe',prompt:'Probiere die neue Aufgabe mit einem Ziel unterhalb des Roboters.'}};
  if(result.status==='complete'&&!result.success){const end=result.end,missing=result.missing.map(cell=>{const [x,y]=cell.split(',');return `Spalte ${x}, Reihe ${y}`;});return {kind:'incomplete',result,message:`Das Programm endet in Spalte ${end[0]}, Reihe ${end[1]}, Blick nach ${directions[end[2]]}. Erreicht sind ${result.cleaned.length} von ${room.width*room.height} Kacheln. Noch offen: ${missing.join('; ')}.`,nextStep:`Wähle eine offene Kachel, zum Beispiel ${missing[0]}, und verfolge im Endbild, an welcher Stelle dein geplanter Weg sie erreichen sollte. Ändere zunächst nur diesen Teil.`,application:{id:'p8-probe',prompt:'Probiere die neue Aufgabe mit zwei offenen Kacheln und einem neuen Endstand.'}};}
  if(result.success&&!syntax.blocks.some(block=>block.repeat)){const total=room.width*room.height===12?'zwölf':room.width*room.height;return {kind:'missing-loop',result,message:`Dein Weg erreicht alle ${total} Kacheln ohne Wandstopp. Zur Aufgabe gehört zusätzlich mindestens eine Schleife; an der Flächendeckung liegt der Unterschied nicht.`,nextStep:'Vergleiche einen Reihenabschnitt aus dem ersten Musterweg. Überarbeite nur einen passenden Teil deines Wegs als Schleife und führe das Programm erneut aus.',application:{id:'p9-probe',prompt:'Finde in der neuen Aufgabe eine wiederkehrende Gruppe.'}};}
  if(result.success&&syntax.blocks.some(block=>block.repeat))return {kind:'success',result,message:`Das Programm läuft ohne Wandstopp und erreicht alle ${room.width*room.height} Kacheln. Eine Schleife ist enthalten. Auch ein anderer Weg als die Musterlösung ist gültig, wenn diese Kriterien erfüllt sind.`,nextStep:'Vergleiche jetzt nur deine Erklärung: Warum passt die Schleifenzahl, und warum führt deine gewählte Drehung zum Ziel?',application:{id:'p8-probe',prompt:'Wende deinen Plan in der neuen Aufgabe auf einen veränderten Endstand an.'}};
  return {kind:'unclassified',result,blocks:syntax.blocks};
 }
 const directions=['oben','rechts','unten','links'];
 function describe(s,room,withIteration=true){
  const place=room.width===2&&room.height===2?`${s.pos[0]===1?'links':'rechts'} ${s.pos[1]===1?'oben':'unten'}`:`Spalte ${s.pos[0]}, Reihe ${s.pos[1]}`;
  const location=`${place} · Blick ${directions[s.pos[2]]}.`;
  if(!s.line)return `Start: ${location}`;
  const effect=s.error?'Wand: keine Fahrt, Programm angehalten.':s.action==='vor'?'vor: eine Kachel weiter.':`${s.action}: Drehung am Ort.`;
  const iteration=withIteration&&s.repeat?` Durchlauf ${s.iteration} von ${s.count}${s.error?' abgebrochen':s.bodyIndex===s.bodyLength-1?' beendet':', Anweisung '+(s.bodyIndex+1)+' von '+s.bodyLength}.`:'';
  return `${effect} ${location}${iteration}`;
 }
 function planningState(room,draftCode,executedCode=null){
  const code=String(draftCode??''),hasRun=typeof executedCode==='string';let error=null;
  if(code.trim()){const syntax=inspectProgram(code);if(!syntax.ok)error=syntax.kind==='comma'?`Zeile ${syntax.line}: Hier steht ein Komma. Trenne die Anweisungen mit einem Semikolon ;.`:syntax.message;}
  const stale=hasRun&&executedCode!==code;
  return {phase:!code.trim()?'empty':error?'invalid':stale?'changed':hasRun?'current':'unrun',error,stale,
   draftCode:code,executedCode:hasRun?executedCode:null,cellCount:room.width*room.height,
   start:{pos:[...room.start],cleaned:[`${room.start[0]},${room.start[1]}`]}};
 }
 function createExecution(room,code){const result=simulate(room,code);return {room,code,result,index:result.trace.length-1};}
 function actionAt(s,includeError=false){if(!s||!s.line)return null;const action={action:s.action,line:s.line,iteration:s.iteration,count:s.count,position:s.bodyIndex+1,length:s.bodyLength};if(includeError)action.error=s.error;return action;}
 function executionFrame(execution,index=execution.index){
  const trace=execution.result.trace,step=Math.max(0,Math.min(Number(index)||0,trace.length-1)),state=trace[step];
  return {step,total:trace.length-1,state,current:actionAt(state,true),next:actionAt(trace[step+1]),resultStatus:execution.result.status};
 }
 function freshState(){return {format:'ium-schleifen',version:1,page:'start',answers:{},code:'',note:''};}
 function decode(raw){
  if(typeof raw!=='string'||new TextEncoder().encode(raw).length>100000)throw new Error('Die Datei ist zu groß (höchstens 100 KB).');
  let s;try{s=JSON.parse(raw);}catch{throw new Error('Das ist keine lesbare Sicherungsdatei.');}
  const obj=v=>v&&typeof v==='object'&&!Array.isArray(v),short=(v,n)=>typeof v==='string'&&v.length<=n;
  if(!obj(s)||s.format!=='ium-schleifen'||s.version!==1||!pages.includes(s.page)||!short(s.code,10000)||!short(s.note,4000)||!obj(s.answers))throw new Error('Diese Datei passt nicht zu „Mit Schleifen planen“. Dein Stand bleibt erhalten.');
  const clean=freshState(); clean.page=s.page;clean.code=s.code;clean.note=s.note;
  for(const [id,a]of Object.entries(s.answers)){
   if(!['start','turn','pair','outside',...Object.keys(exercises)].includes(id)||!obj(a))throw new Error('Unbekannte Aufgabe in der Sicherung.');
   clean.answers[id]={};
   for(const [k,v]of Object.entries(a)){if(!['sequence','runs','actions','explanation','choice'].includes(k)||!short(v,4000))throw new Error('Ungültige Antwort in der Sicherung.');if(k==='choice'&&!['0','1','2'].includes(v))throw new Error('Ungültige Auswahl in der Sicherung.');clean.answers[id][k]=v;}
  }
  return clean;
 }
 function encode(state){const raw=JSON.stringify(state,null,2);decode(raw);return raw;}
 const api={pages,rooms,examples,exercises,expand,simulate,compare,checkSequence,checkGrouping,inspectProgram,assessPlan,describe,planningState,createExecution,executionFrame,directions,freshState,decode,encode};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.Lesson=api;
})(globalThis);
