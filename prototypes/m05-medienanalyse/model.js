(function(root,factory){const api=factory(typeof module==='object'&&module.exports?require('./content.js'):root.MediaContent);if(typeof module==='object'&&module.exports)module.exports=api;else root.MediaModel=api;})(typeof globalThis!=='undefined'?globalThis:this,function(content){
'use strict';
const bounded=(value,min,max,fallback)=>Math.max(min,Math.min(max,Number.isFinite(Number(value))?Number(value):fallback));
function crop(input={}){const width=bounded(input.width,600,1536,1536),height=width/1.5;return {x:bounded(input.x,0,1536-width,0),y:(1024-height)/2,width,height};}
const presets={full:{x:0,width:1536},left:{x:0,width:680},right:{x:856,width:680}};
function experiment(mode,selection,headline){
 const neutral=content.headlines[0],full=crop();
 return mode==='headline'?{before:{crop:full,headline:neutral},after:{crop:full,headline:String(headline)}}:{before:{crop:full,headline:neutral},after:{crop:crop(selection),headline:neutral}};
}
function assess(answers={}){
 return content.claims.map(claim=>{const answer=answers[claim.id],valid=content.choices.some(c=>c.id===answer);return {id:claim.id,status:!valid?'open':answer===claim.answer?'match':'revise',feedback:!valid?'Noch offen. Wähle einen Beleg und prüfe dann erneut.':claim.feedback};});
}
function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function viewBox(selection){const c=crop(selection);return [c.x,c.y,c.width,c.height].join(' ');}
function cropDescription(scene,selection){const c=crop(selection);if(c.width===1536)return scene.alt;if(c.x+c.width<800)return scene.name==='Schulfest'?'Ausschnitt links: leere Bänke vor der Bühne. Die Mitmachstände rechts fehlen.':'Ausschnitt links: leere Sessel in der Leseecke. Der Lesetisch rechts fehlt.';if(c.x>=800)return scene.name==='Schulfest'?'Ausschnitt rechts: Kinder und Erwachsene an Basteltischen. Die Bänke vor der Bühne fehlen.':'Ausschnitt rechts: Kinder mit offenen Büchern am Tisch. Die leere Leseecke fehlt.';return 'Mittlerer Ausschnitt aus dieser Szene: '+scene.alt+' Je nach Ausschnitt fehlen Teile der Ränder.';}
return {crop,presets,experiment,assess,escapeHtml,viewBox,cropDescription};
});
