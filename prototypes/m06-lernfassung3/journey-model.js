'use strict';
(function(root){
 const M=typeof module!=='undefined'&&module.exports?require('../m06-selbstlernen/model.js'):root.Lesson;
 const bridgeRoom={width:4,height:2,start:[1,2,1]};
 const switchRoom={width:4,height:3,start:[1,2,3]};
 const prior=['1,2','2,2','3,2','4,2','1,3','2,3','3,3','4,3'];
 function bridge({first='',turn='',last=''}={}){
  if(!/^[2-9]$/.test(String(first))||!/^[2-9]$/.test(String(last))||!['links','rechts'].includes(turn))
   return {kind:'input',message:'Ergänze beide Schleifenzahlen und die Drehung. Unser Modell erlaubt ganze Schleifenzahlen von 2 bis 9.',nextStep:'Zähle die Wege zwischen den Kacheln. Wähle dann links oder rechts.'};
  const code='wiederhole '+first+' [vor]\nlinks\nvor\n'+turn+'\nwiederhole '+last+' [vor]';
  return {...M.assessPlan(bridgeRoom,code),code,room:bridgeRoom};
 }
 function switchRow(commands){
  if(!Array.isArray(commands)||commands.length!==3||commands.some(c=>!['vor','links','rechts'].includes(c)))
   return {kind:'input',message:'Wähle für alle drei Stellen eine Anweisung.',nextStep:'Beginne mit der Drehung, die den Pfeil von links nach oben richtet.'};
  const code=commands.join('\n'),result=M.simulate(switchRoom,code);
  result.trace=result.trace.map(frame=>({...frame,cleaned:[...new Set([...prior,...frame.cleaned])]}));
  result.cleaned=[...result.trace.at(-1).cleaned];
  result.missing=['1,1','2,1','3,1','4,1'].filter(cell=>!result.cleaned.includes(cell));
  result.success=result.missing.length===0&&result.status==='complete';
  let kind,message,nextStep;
  if(result.status==='wall'){
   kind='wall';message='Die Fahrt trifft auf die Wand. '+M.describe(result.trace.at(-1),switchRoom);
   nextStep='Gehe eine Anweisung zurück. Prüfe zuerst den Blick, bevor du vor ausführst.';
  }else if(result.end[0]!==1||result.end[1]!==1){
   kind='position';message='Der Roboter endet in Spalte '+result.end[0]+', Reihe '+result.end[1]+'. Das Ziel liegt links oben, in Spalte 1, Reihe 1.';
   nextStep='Untersuche deine erste Drehung: Vom Blick nach links führt rechts nach oben, links dagegen nach unten.';
  }else if(result.end[2]!==1){
   kind='direction';message='Die Zielkachel stimmt. Der Roboter blickt aber nach '+M.directions[result.end[2]]+' statt nach rechts.';
   nextStep='Ändere nur die letzte Drehung. Nach der Fahrt nach oben muss der Pfeil für die obere Reihe nach rechts zeigen.';
  }else{
   kind='success';message='Der Wechsel passt: rechts richtet nach oben, vor erreicht die obere Reihe, rechts richtet in die Reihe. Die acht zuvor erreichten Kacheln bleiben markiert.';
   nextStep='Erkläre, warum dieser Wechsel anders beginnt als am rechten Rand. Verbinde dann beide Wechsel in deinem eigenen 4×3-Plan.';
  }
  return {kind,message,nextStep,code,room:switchRoom,result};
 }
 const api={bridge,switchRow};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PlanningJourney=api;
})(globalThis);
