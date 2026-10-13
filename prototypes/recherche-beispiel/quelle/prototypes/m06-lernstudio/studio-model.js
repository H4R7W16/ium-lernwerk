'use strict';
(function(root){
 const W=typeof module!=='undefined'&&module.exports?require('../m06-lernwerkstatt/workshop-model.js'):root.Workshop;
 const chapters=[
  {title:'Entdecken',ids:['start'],caption:'Ort & Richtung'},
  {title:'Schleifen',ids:['loop','after','repair'],caption:'Gruppen wiederholen'},
  {title:'Planen',ids:['example','rows','switch','own'],caption:'Vom Beispiel zum eigenen Weg'},
  {title:'Übertragen',ids:['check','transfer'],caption:'Genau hinsehen'},
  {title:'Wiederholen',ids:['return'],caption:'Nach einer Pause'}
 ];
 const order=chapters.flatMap(c=>c.ids);
 const checks={
 start:{prompt:'Was verändert der Befehl „links“?',options:['Ort und Blickrichtung.','Nur die Blickrichtung.','Nur den Ort.'],answer:1,feedback:['Für einen anderen Ort braucht der Roboter „vor“. Eine Drehung allein fährt nicht.','Genau: Er dreht sich auf derselben Kachel um eine Vierteldrehung.','„links“ dreht auf der Stelle. Nur „vor“ verändert den Ort.']},
 loop:{prompt:'Wie viele einzelne Aktionen führt „wiederhole 4 [vor; links]“ aus?',options:['4 Aktionen.','8 Aktionen.','10 Aktionen.'],answer:1,feedback:['Ein Durchlauf enthält zwei Aktionen. Wiederhole das ganze Paar viermal.','Vier Durchläufe mit je zwei Aktionen: 4 × 2 = 8.','Die 4 zählt alle Durchläufe. Es gibt keinen zusätzlichen ersten Durchlauf.']},
 after:{prompt:'Wann wird das „vor“ hinter der Schleife ausgeführt?',options:['Am Ende jedes Durchlaufs.','Einmal, nach allen vier Durchläufen.','Es gehört nicht zum Programm.'],answer:1,feedback:['Nur die Anweisungen in der Klammer werden wiederholt.','Richtig: Erst endet die ganze Schleife. Danach kommt die einzelne Anweisung.','Auch eine Anweisung nach der Klammer gehört zum Programm – sie folgt einmal.']},
 repair:{prompt:'Warum hilft eine andere Zahl allein nicht beim fehlerhaften Plan?',options:['Weil „links“ in jedem Durchlauf gebraucht wird.','Weil vier Wiederholungen immer falsch sind.','Weil man Drehungen nicht wiederholen kann.'],answer:0,feedback:['Genau. Ohne die Drehung im Körper fährt der Roboter immer weiter geradeaus.','Vier ganze Paare funktionieren. Die Gruppierung war das Problem.','Auch Drehungen lassen sich wiederholen. Fahren und Drehen müssen hier gemeinsam in den Körper.']},
 example:{prompt:'Eine Reihe hat drei Kacheln. Warum genügen zwei Schritte?',options:['Weil Drehen ebenfalls eine Kachel reinigt.','Weil die Startkachel bereits erreicht ist.','Weil eine Schleife schneller fährt.'],answer:1,feedback:['Drehen erreicht keinen neuen Ort. Denke an den bereits belegten Start.','Zwischen drei Kacheln liegen zwei Übergänge. Die erste Kachel ist schon erreicht.','Eine Schleife spart Schreibarbeit, aber keine einzelnen Fahrbewegungen.']},
 rows:{prompt:'Der Boden wird eine Kachel breiter. Was ändert sich im Reihenplan?',options:['Jede gerade Fahrt wird um einen Schritt länger.','Nur die erste Fahrt wird länger.','Die beiden Linksdrehungen werden zu Rechtsdrehungen.'],answer:0,feedback:['Richtig: Beide Reihen sind breiter. Ihre geraden Fahrten brauchen jeweils einen Schritt mehr.','Beide Reihen müssen vollständig erreicht werden. Passe beide geraden Teilpläne an.','Der Übergang bleibt am rechten Rand gleich. Geändert hat sich die Länge der Reihen.']},
 switch:{prompt:'Er blickt nach links. Welche Drehung richtet ihn nach oben aus?',options:['links','rechts','Zweimal rechts'],answer:1,feedback:['Denke aus seiner Sicht: links würde ihn hier nach unten richten.','Genau. Welche Drehung passt, hängt von seiner aktuellen Blickrichtung ab.','Zwei Vierteldrehungen richten ihn nach rechts. Hier brauchst du nur eine.']},
 own:{prompt:'Was zeigt, dass dein Flächenplan den Auftrag erfüllt?',options:['Er kommt zum Start zurück.','Er enthält möglichst wenig Code.','Alle Kacheln sind erreicht, ohne Wandstopp und mit einer Schleife.'],answer:2,feedback:['Eine Randrunde kommt zurück und kann innen trotzdem Krümel übrig lassen.','Kurzer Code allein beweist weder eine saubere Fläche noch einen gültigen Weg.','Das sind die drei Kriterien. Erkläre zusätzlich, wie deine Teilpläne die ganze Fläche abdecken.']},
 check:{prompt:'Warum beweist die Rückkehr zum Start keine saubere Fläche?',options:['Weil der Blick am Ende immer falsch ist.','Weil im Inneren unbesuchte Kacheln liegen können.','Weil man jede Kachel genau zweimal besuchen muss.'],answer:1,feedback:['Auch mit gleichem Blick kann innen Schmutz bleiben. Entscheidend sind die besuchten Kacheln.','Genau: Die Randrunde ist ein Gegenbeispiel. Endpunkt und Flächenabdeckung sind verschiedene Kriterien.','Ein Besuch genügt in diesem Modell. Aber jede Kachel muss mindestens einmal erreicht werden.']},
 transfer:{prompt:'Warum stoppt Plan B schon beim zweiten Aufnehmen?',options:['Der einzige Platz ist noch belegt.','Jeder Befehl darf nur einmal vorkommen.','Drei Werkstücke sind zu viele.'],answer:0,feedback:['Genau: Erst prüfen und ablegen macht den Platz wieder frei. Der ganze Ablauf gehört in den Körper.','Befehle dürfen wiederkehren. Entscheidend ist hier ihre Reihenfolge.','Plan A schafft drei Werkstücke. Er gibt den Platz nach jedem Werkstück wieder frei.']},
 return:{prompt:'Dreimal [vor; links], danach rechts. Wie viele Aktionen sind das?',options:['6','7','9'],answer:1,feedback:['Die Schleife hat sechs Aktionen. Eine einzelne Drehung folgt danach.','3 × 2 + 1 = 7. Die letzte Rechtsdrehung steht außerhalb der Klammer.','„rechts“ gehört nicht in den Körper. Es wird nach der Schleife nur einmal ausgeführt.']}
 };
 function fresh(id){return {code:W.lesson(id).code||'',step:0,observed:false,checked:false,independent:false,attempts:0,choice:null,help:0,note:'',prediction:null,sequence:[],undo:[],previous:null,plan:'A',compared:[]};}
 function change(s,code){W.blocks(code);s.undo.push(s.code);s.undo=s.undo.slice(-30);s.code=code;s.step=0;s.observed=false;s.checked=false;s.independent=false;s.attempts=0;s.choice=null;}
 function answer(id,s,choice){const q=checks[id];if(!Number.isInteger(choice)||choice<0||choice>=q.options.length)throw new Error('Ungültige Antwort');s.attempts++;s.choice=choice;const ok=q.answer===choice;s.checked=ok;s.independent=ok&&s.attempts===1&&s.help===0;return {ok,message:q.feedback[choice]};}
 function run(id,code){
  if(code.trim())return W.run(id,code);
  const l=W.lesson(id),pos=[...l.room.start],cleaned=[...new Set([...(l.prior||[]),pos.slice(0,2).join()])];
  const missing=Array.from({length:l.room.height},(_,y)=>Array.from({length:l.room.width},(_,x)=>(x+1)+','+(y+1))).flat().filter(x=>!cleaned.includes(x));
  return {trace:[{pos,cleaned,action:'Start',line:null,iteration:null}],end:pos,cleaned,missing,status:'empty',success:false};
 }
 function prediction(id,p){if(!p)return null;return W.run(id,W.lesson(id).code).end.join()===p.join();}
 function restore(text){
  try{
   const raw=JSON.parse(text);if(!raw||raw.version!==1||typeof raw.works!=='object'||!raw.works)return null;
   const data={version:1,current:order.includes(raw.current)?raw.current:'start',works:{}};
   for(const id of order){
    const r=raw.works[id];if(!r||typeof r!=='object')continue;
    const s=fresh(id),l=W.lesson(id);
    if(typeof r.code==='string'&&r.code.length<=2500){try{const bs=W.blocks(r.code);if(l.editable&&bs.length<=30)s.code=W.code(bs);}catch{}}
    s.note=typeof r.note==='string'?r.note.slice(0,2000):'';
    for(const k of ['observed','checked','independent'])s[k]=r[k]===true;
    s.attempts=Number.isInteger(r.attempts)?Math.max(0,Math.min(999,r.attempts)):0;
    s.help=Number.isInteger(r.help)?Math.max(0,Math.min(3,r.help)):0;
    s.choice=Number.isInteger(r.choice)&&r.choice>=0&&r.choice<3?r.choice:null;
    s.checked=s.checked&&s.choice===checks[id].answer;
    s.independent=s.checked&&s.independent&&s.help===0&&s.attempts===1;
    if(l.room&&Array.isArray(r.prediction)&&r.prediction.length===3&&r.prediction.every(Number.isInteger)&&r.prediction[0]>=1&&r.prediction[0]<=l.room.width&&r.prediction[1]>=1&&r.prediction[1]<=l.room.height&&r.prediction[2]>=0&&r.prediction[2]<=3)s.prediction=[...r.prediction];
    s.sequence=Array.isArray(r.sequence)?r.sequence.filter(x=>['vor','links','rechts'].includes(x)).slice(0,30):[];
    s.plan=r.plan==='B'?'B':'A';
    data.works[id]=s;
   }return data;
  }catch{return null;}
 }
 const api={chapters,order,checks,fresh,change,answer,prediction,restore,run};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.Studio=api;
})(globalThis);
