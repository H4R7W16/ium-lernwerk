'use strict';
document.addEventListener('DOMContentLoaded',()=>{
 for(const tool of document.querySelectorAll('[data-card-tool]')){
 const input=tool.querySelector('textarea'),stock=Number(tool.dataset.stock),step=tool.dataset.step,status=tool.querySelector('[data-card-status]');let result=null,cursor=0,stopped=false;
 const desc=s=>s?(s.marked?'markierte Karte':'unmarkierte Karte'):'leer';
 const el=(tag,text)=>{const x=document.createElement(tag);x.textContent=text;return x;};
 function draw(){const s=result?.trace[cursor]||{remaining:stock,slot:null,output:[]};const host=tool.querySelector('[data-card-state]');host.replaceChildren();for(const [name,text]of [['Vorrat',s.remaining+' Karten'],['Ein Platz',desc(s.slot)],['Ausgabe · zuerst → zuletzt',s.output.map((m,i)=>(i+1)+': '+(m?'markiert':'unmarkiert')).join(' · ')||'leer']]){const box=el('div','');box.append(el('b',name),el('p',text));host.append(box);}
 const table=el('table',''),head=el('tr','');for(const t of ['Schritt / Code','Vorrat','Platz','Ausgabe'])head.append(el('th',t));table.append(head);
 for(const row of result?result.trace.slice(0,cursor+1):[]){const tr=el('tr','');for(const text of [row.step+' · '+row.command+(row.line?' (Zeile '+row.line+(row.iteration?', Durchlauf '+row.iteration:'')+')':''),String(row.remaining),desc(row.slot),row.output.map(m=>m?'●':'○').join(' ')||'leer'])tr.append(el('td',text));table.append(tr);}
 tool.querySelector('[data-card-trace]').replaceChildren(table);
 }
 function reset(message='Startzustand wiederhergestellt. Deine Vorhersage bleibt im Antwortfeld.'){result=null;cursor=0;stopped=false;status.textContent=message;draw();}
 input.addEventListener('input',()=>reset('Code geändert. Der nächste Lauf beginnt wieder am Start.'));
 tool.addEventListener('click',event=>{const action=event.target.closest('[data-card]')?.dataset.card;if(!action)return;
 if(action==='reset'){reset();return;}
 if(action==='copy'){
  if(!result||(cursor===0&&!stopped)){status.textContent='Führe zuerst mindestens einen Befehl aus.';return;}
  const target=document.getElementById('answer-'+step+'-spur');if(!target)return;
  const lines=['Code:\n'+input.value,'Ausgeführte Spur: ○ unmarkiert, ● markiert',...result.trace.slice(0,cursor+1).map(s=>s.step+' '+s.command+': Vorrat '+s.remaining+', Platz '+desc(s.slot)+', Ausgabe '+(s.output.map(m=>m?'●':'○').join(' ')||'leer'))];if(stopped&&result.error)lines.push('Stopp bei Schritt '+result.error.step+': '+result.error.message);
  try{target.value=CardMachine.appendRecord(target.value,lines.join('\n'));}catch(error){status.textContent=error.message;return;}target.dispatchEvent(new Event('input',{bubbles:true}));status.textContent='Spur im Protokoll ergänzt. Erkläre darunter selbst die Abweichung oder Übereinstimmung.';return;
 }
 try{if(!result)result=CardMachine.run(input.value,stock);}catch(error){status.textContent=error.message;return;}
 const progress=CardMachine.advance(result,cursor,action==='all');cursor=progress.cursor;stopped=progress.stopped;
 if(stopped&&result.error)status.textContent='Stopp vor Schritt '+result.error.step+' (Zeile '+result.error.line+'): '+result.error.message;
 else if(stopped){const expected=step==='entwurf'?[false,true,true,true]:[true,true,true];const ok=JSON.stringify(result.end.output)===JSON.stringify(expected)&&result.end.remaining===0&&result.end.slot===null;status.textContent='Programm beendet. '+(ok?'Ausgabe und leerer Platz passen zum Kartenauftrag. Erkläre jetzt Grafik und Spur.':'Vergleiche deine Ausgabe mit dem Auftrag. Ein beendetes Programm kann trotzdem das falsche Ergebnis liefern.');}
 else{const s=result.trace[cursor];status.textContent='Schritt '+cursor+': '+s.command+' · Zeile '+s.line+(s.iteration?' · Durchlauf '+s.iteration:'')+'. Sage den nächsten Zustand voraus.';}
 draw();
 });draw();
 }
});
