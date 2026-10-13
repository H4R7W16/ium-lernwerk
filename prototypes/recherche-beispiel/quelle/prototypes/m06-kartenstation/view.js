/* Kartenansicht: dieselben Zustände wie im Interpreter, keine eigene Ausführung. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.CardView=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
 'use strict';
 function describe(s){
  const cards=s.output.map(Boolean),slot=s.slot===null?[]:[Boolean(s.slot.marked)];
  return {command:s.line?'Zuletzt ausgeführt: '+s.command+' · Zeile '+s.line+(s.iteration?' · Durchlauf '+s.iteration:''):'Start · noch kein Befehl ausgeführt',groups:[
   {name:'Vorrat',cards:Array.from({length:s.remaining},()=>false),text:s.remaining+' Karten'},
   {name:'Ein Platz',cards:slot,text:slot.length?(slot[0]?'markierte Karte':'unmarkierte Karte'):'leer'},
   {name:'Ausgabe · zuerst → zuletzt',cards,text:cards.map((m,i)=>(i+1)+': '+(m?'markiert':'unmarkiert')).join(' · ')||'leer'}]};
 }
 return {describe};
});
