'use strict';
(function(root){
 const commands=['nimm','markiere','lege'];
 function parse(code){
  if(typeof code!=='string'||!code.trim()||code.length>3000)throw Error('Schreibe zuerst einen kurzen Plan.');
  const tokens=[];let line=1;for(const part of code.matchAll(/\s+|[a-z]+|\d+|[\[\]]|./g)){const t=part[0];if(/^\s+$/.test(t)){line+=(t.match(/\n/g)||[]).length;continue;}tokens.push({text:t,line});}
  let i=0;const actions=[];
  while(i<tokens.length){const t=tokens[i++];if(commands.includes(t.text))actions.push({command:t.text,line:t.line,iteration:null});
   else if(t.text==='wiederhole'){
    const n=tokens[i++];if(!n||! /^[1-9]$/.test(n.text))throw Error('Nach wiederhole steht eine feste Zahl von 1 bis 9.');
    if(tokens[i++]?.text!=='[')throw Error('Die wiederholte Gruppe beginnt mit [.');
    const body=[];while(i<tokens.length&&tokens[i].text!==']'){const b=tokens[i++];if(!commands.includes(b.text))throw Error('In die Klammer gehören nimm, markiere oder lege; keine weitere Schleife.');body.push(b);}
    if(tokens[i++]?.text!==']'||!body.length)throw Error('Die Gruppe braucht Befehle und eine schließende Klammer ].');
    for(let iteration=1;iteration<=Number(n.text);iteration++)for(const b of body)actions.push({command:b.text,line:b.line,iteration});
   }else throw Error('Unbekannter Eintrag in Zeile '+t.line+': '+t.text+'. Nutze nimm, markiere, lege oder wiederhole.');
   if(actions.length>120)throw Error('Der Plan darf höchstens 120 einzelne Aktionen ausführen.');
  }return actions;
 }
 function run(code,stock){
  if(!Number.isInteger(stock)||stock<1||stock>9)throw Error('Der Vorrat muss 1 bis 9 Karten enthalten.');
  const actions=parse(code);let remaining=stock,slot=null,output=[],error=null;
  const snapshot=a=>({...a,remaining,slot:slot?{...slot}:null,output:[...output]});
  const trace=[snapshot({command:'Start',line:null,iteration:null,step:0})];
  for(const [i,a]of actions.entries()){
   let message='';
   if(a.command==='nimm'){if(slot)message='Der Platz ist noch belegt. Lege die Karte zuerst ab.';else if(!remaining)message='Der Vorrat ist leer. Es gibt keine weitere Karte.';else{remaining--;slot={marked:false};}}
   if(a.command==='markiere'){if(!slot)message='Auf dem Platz liegt keine Karte.';else if(slot.marked)message='Diese Karte trägt schon eine Markierung.';else slot.marked=true;}
   if(a.command==='lege'){if(!slot)message='Auf dem Platz liegt keine Karte zum Ablegen.';else{output.push(slot.marked);slot=null;}}
   if(message){error={...a,step:i+1,message};break;}
   trace.push(snapshot({...a,step:i+1}));
  }return {trace,end:trace.at(-1),error,actions};
 }
 function advance(result,cursor,all=false){const next=all?result.trace.length-1:Math.min(cursor+1,result.trace.length-1);return {cursor:next,stopped:result.error?(all||cursor===result.trace.length-1):next===result.trace.length-1};}
 function appendRecord(previous,next){const joined=next+(previous.trim()?'\n\nFrüherer Versuch / eigene Notizen:\n'+previous:'');if(joined.length>10000)throw Error('Das Protokoll ist voll. Sichere zuerst deine Arbeitsdatei und schaffe danach selbst Platz. Es wurde nichts ersetzt.');return joined;}
 const api={parse,run,advance,appendRecord};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.CardMachine=api;
})(globalThis);
