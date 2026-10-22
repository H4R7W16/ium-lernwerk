'use strict';
(function(root){
 const commands=['vor','rechts','links','hoch','runter'];
 function parse(code){
  if(typeof code!=='string'||!code.trim()||code.length>3000)throw Error('Stelle zuerst einen kurzen Code zusammen (höchstens 3000 Zeichen).');
  const tokens=[];let line=1;
  for(const p of code.matchAll(/\s+|[a-z]+|\d+|[\[\]]|./g)){if(/^\s+$/.test(p[0])){line+=(p[0].match(/\n/g)||[]).length;}else tokens.push({text:p[0],line});}
  let i=0;const actions=[];
  while(i<tokens.length){const t=tokens[i++];
   if(commands.includes(t.text))actions.push({command:t.text,line:t.line,iteration:null});
   else if(t.text==='wiederhole'){
    const n=tokens[i++];if(!n||! /^[1-9]$/.test(n.text))throw Error('Zeile '+t.line+': Nach wiederhole steht eine feste Zahl von 1 bis 9.');
    if(tokens[i++]?.text!=='[')throw Error('Zeile '+t.line+': Die wiederholte Gruppe beginnt mit [.');
    const body=[];while(i<tokens.length&&tokens[i].text!==']'){const b=tokens[i++];if(!commands.includes(b.text))throw Error('Zeile '+b.line+': In die Klammer gehören vor, rechts, links, hoch oder runter. Keine weitere Schleife.');body.push(b);}
    if(tokens[i++]?.text!==']'||!body.length)throw Error('Zeile '+t.line+': Die Gruppe braucht Befehle und eine schließende Klammer ].');
    for(let iteration=1;iteration<=Number(n.text);iteration++)for(const b of body)actions.push({command:b.text,line:b.line,iteration});
   }else throw Error('Zeile '+t.line+': Unbekannter Eintrag „'+t.text+'“. Nutze die Befehlstasten oder die Befehlskarte.');
   if(actions.length>200)throw Error('Der Code darf höchstens 200 einzelne Befehle ausführen.');
  }return actions;
 }
 function run(code){
  const actions=parse(code);let x=1,y=1,dir=0,pen=true,lines=[],error=null;
  const snapshot=a=>({...a,x,y,dir,pen,lines:lines.map(l=>[...l])});
  const trace=[snapshot({command:'Start',line:null,iteration:null,step:0})];
  for(const [i,a]of actions.entries()){
   if(a.command==='vor'){const dx=[1,0,-1,0][dir],dy=[0,1,0,-1][dir],nx=x+dx,ny=y+dy;
    if(nx<0||nx>12||ny<0||ny>8){error={...a,step:i+1,message:'Der nächste Schritt verlässt das Raster. Prüfe Richtung oder Länge.'};break;}
    if(pen)lines.push([x,y,nx,ny]);x=nx;y=ny;
   }else if(a.command==='rechts')dir=(dir+1)%4;
   else if(a.command==='links')dir=(dir+3)%4;
   else pen=a.command==='runter';
   trace.push(snapshot({...a,step:i+1}));
  }return {actions,trace,end:trace.at(-1),error};
 }
 function appendRecord(previous,next){const joined=next+(previous.trim()?'\n\nFrüherer Versuch / eigene Notizen:\n'+previous:'');if(joined.length>10000)throw Error('Das Protokoll ist voll. Sichere deine Arbeitsdatei und schaffe selbst Platz. Nichts wurde ersetzt.');return joined;}
 const api={parse,run,appendRecord};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.DrawingMachine=api;
})(globalThis);
