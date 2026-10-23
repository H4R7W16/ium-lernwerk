'use strict';
document.addEventListener('DOMContentLoaded',()=>{for(const root of document.querySelectorAll('[data-draw-tool]')){
 const input=root.querySelector('textarea'),step=root.dataset.step,status=root.querySelector('.draw-status'),state=root.querySelector('.draw-state'),list=root.querySelector('.draw-trace'),svg=root.querySelector('svg');
 const dirs=['rechts','unten','links','oben'];let result=null,cursor=0,code='',stopped=false;
 function draw(){const s=result?.trace[cursor]||{x:1,y:1,dir:0,pen:true,lines:[]};let h='<title>Zeichenraster: '+s.x+' nach rechts, '+s.y+' nach unten. Blick '+dirs[s.dir]+'. Stift '+(s.pen?'unten':'oben')+'.</title>';
  for(let x=0;x<=12;x++)h+='<line x1="'+(35+x*37)+'" y1="35" x2="'+(35+x*37)+'" y2="331" stroke="#c9d8d5"/><text x="'+(35+x*37)+'" y="23" text-anchor="middle" font-size="13">'+x+'</text>';
  for(let y=0;y<=8;y++)h+='<line x1="35" y1="'+(35+y*37)+'" x2="479" y2="'+(35+y*37)+'" stroke="#c9d8d5"/><text x="20" y="'+(40+y*37)+'" text-anchor="middle" font-size="13">'+y+'</text>';
  for(const [x,y,nx,ny]of s.lines)h+='<line x1="'+(35+x*37)+'" y1="'+(35+y*37)+'" x2="'+(35+nx*37)+'" y2="'+(35+ny*37)+'" stroke="#075c55" stroke-width="5" stroke-linecap="round"/>';
  h+='<circle cx="72" cy="72" r="6" fill="#fff" stroke="#222" stroke-width="2"/><path d="M -9 -8 L 12 0 L -9 8 Z" transform="translate('+(35+s.x*37)+' '+(35+s.y*37)+') rotate('+(s.dir*90)+')" fill="#ac4100" stroke="#fff" stroke-width="1.5"/><text x="35" y="357" font-size="14">Kreis: Start · Dreieck: Position und Blickrichtung</text>';svg.innerHTML=h;
  state.textContent='Punkt ('+s.x+'|'+s.y+') · Blick '+dirs[s.dir]+' · Stift '+(s.pen?'unten':'oben')+' · '+cursor+' Befehle ausgeführt.';
  list.replaceChildren();for(const t of (result?.trace||[]).slice(1,cursor+1)){const li=document.createElement('li');li.textContent=t.command+' → ('+t.x+'|'+t.y+'), '+dirs[t.dir]+', Stift '+(t.pen?'unten':'oben')+' · Zeile '+t.line+(t.iteration?' / Durchlauf '+t.iteration:'');list.append(li);}list.scrollTop=list.scrollHeight;
 }
 function reset(message){result=null;cursor=0;code='';stopped=false;status.textContent=message;draw();}
 input.addEventListener('input',()=>reset('Code geändert. Sage die Wirkung voraus und starte neu.'));
 root.addEventListener('click',ev=>{const insert=ev.target.closest('[data-insert]');if(insert){const at=input.selectionStart??input.value.length,end=input.selectionEnd??at,v=(at&& !/\s/.test(input.value[at-1])?' ':'')+insert.dataset.insert+' ';if(input.value.length+v.length-(end-at)>3000){status.textContent='Der Code ist zu lang.';return;}input.setRangeText(v,at,end,'end');if(insert.dataset.insert.startsWith('wiederhole')){const inside=at+v.indexOf('[')+2;input.setSelectionRange(inside,inside);}input.dispatchEvent(new Event('input',{bubbles:true}));input.focus();return;}
  const action=ev.target.closest('[data-draw]')?.dataset.draw;if(!action)return;
  if(action==='reset'){reset('Ausführung zurück am Start. Dein Code und Protokoll bleiben erhalten.');return;}
  if(action==='record'){if(!result||cursor===0){status.textContent='Führe zuerst mindestens einen Befehl aus.';return;}const target=document.getElementById('answer-'+step+'-spur');if(!target)return;
   const lines=['Code:\n'+code,...result.trace.slice(0,cursor+1).map(t=>t.step+' '+t.command+': ('+t.x+'|'+t.y+'), Blick '+dirs[t.dir]+', Stift '+(t.pen?'unten':'oben'))];if(stopped&&result.error)lines.push('Stopp: '+result.error.message);
   try{target.value=DrawingMachine.appendRecord(target.value,lines.join('\n'));target.dispatchEvent(new Event('input',{bubbles:true}));status.textContent='Versuch ergänzt. Erkläre selbst, warum das Ergebnis zu deiner Vorhersage passt oder davon abweicht.';}catch(e){status.textContent=e.message;}return;
  }
  try{if(!result||code!==input.value){code=input.value;result=DrawingMachine.run(code);cursor=0;stopped=false;}}catch(e){reset(e.message);return;}
  cursor=action==='all'?result.trace.length-1:Math.min(cursor+1,result.trace.length-1);stopped=cursor===result.trace.length-1;
  status.textContent=stopped?(result.error?'Stopp vor Befehl '+result.error.step+' (Zeile '+result.error.line+'): '+result.error.message:'Programm beendet. Vergleiche Zeichnung und Schlussrichtung mit deinem Auftrag; beendet bedeutet nicht automatisch richtig.'):'Befehl '+cursor+' ausgeführt. Sage den nächsten Zustand voraus.';draw();
 });draw();
}});
