(function(root,factory){const api=factory(typeof module==='object'&&module.exports?require('./content.js'):root.QuestContent);if(typeof module==='object'&&module.exports)module.exports=api;else root.QuestModel=api;})(typeof globalThis!=='undefined'?globalThis:this,function(C){
'use strict';
function assess(id,answer={},bank='claims'){
 const claim=(bank==='transfer'?C.transfer:C.claims).find(x=>x.id===id);
 if(!claim)throw new Error('Unbekannte Aussage: '+id);
 const sourceIds=bank==='transfer'?['D','E']:['B','C'];
 const evidenceIds=sourceIds.flatMap(x=>C.sources[x].lines.map(l=>l.id)).concat('none');
 if(!C.verdicts.some(v=>v.id===answer.verdict)||!evidenceIds.includes(answer.evidence))return {status:'open',title:'Noch nicht vollständig',text:'Wähle ein Urteil und einen Textbeleg. Wenn keine Quelle etwas dazu sagt, wähle „Keine passende Angabe“.'};
 if(answer.verdict!==claim.answer)return {status:'verdict',title:'Prüfe dein Urteil noch einmal',text:claim.feedback};
 if(!claim.evidence.includes(answer.evidence))return {status:'evidence',title:'Das Urteil passt. Prüfe deinen Beleg.',text:'Deine gewählte Stelle trägt dieses Urteil nicht. '+claim.feedback};
 return {status:'match',title:'Urteil und Beleg passen zusammen',text:claim.feedback+' Erkläre den Zusammenhang auch in eigenen Worten.'};
}
function checkSource(id,answer){
 const q=C.sourceQuestions.find(x=>x.id===id);if(!q)throw new Error('Unbekannte Quellenfrage');
 if(!['A','B','C'].includes(answer))return {status:'open',title:'Wähle zuerst eine Quelle',text:'Lies die Frage und vergleiche die drei Quellen.'};
 return {status:answer===q.answer?'match':'revise',title:answer===q.answer?'Diese Quelle passt zur Frage':'Prüfe, wer genau diese Frage beantworten kann',text:q.feedback};
}
function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
return {assess,checkSource,escapeHtml};
});
