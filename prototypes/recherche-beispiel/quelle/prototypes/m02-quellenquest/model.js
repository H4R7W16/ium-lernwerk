(function(root,factory){const api=factory(typeof module==='object'&&module.exports?require('./content.js'):root.QuestContent);if(typeof module==='object'&&module.exports)module.exports=api;else root.QuestModel=api;})(typeof globalThis!=='undefined'?globalThis:this,function(C){
'use strict';
function bankData(bank){return bank==='transfer'?{claims:C.transfer,sources:['D','E','F']}:{claims:C.claims,sources:['A','B','C']};}
function assess(id,answer={},bank='claims',reveal=false){
 const data=bankData(bank),claim=data.claims.find(x=>x.id===id);
 if(!claim)throw new Error('Unbekannte Aussage: '+id);
 const evidenceIds=data.sources.flatMap(x=>C.sources[x].lines.map(l=>l.id)).concat('none');
 if(!C.verdicts.some(v=>v.id===answer.verdict)||!evidenceIds.includes(answer.evidence))return {status:'open',title:'Noch ein Schritt',text:'Wähle ein Urteil und eine Stelle im Dokument. Fehlt eine passende Angabe in allen Quellen, kannst du das ausdrücklich auswählen.'};
 if(answer.verdict!==claim.answer)return {status:'verdict',title:reveal?'Die Erklärung zum Vergleichen':'Schau noch einmal genau hin',text:reveal?claim.feedback:claim.hint};
 if(!claim.evidence.includes(answer.evidence))return {status:'evidence',title:reveal?'Die Erklärung zum Vergleichen':'Urteil und Stelle noch einmal verbinden',text:reveal?claim.feedback:'Deine ausgewählte Stelle trägt dieses Urteil noch nicht. '+claim.hint};
 return {status:'match',title:'Urteil und Beleg passen zusammen',text:claim.feedback+' Erkläre den Zusammenhang auch selbst.'};
}
function evidenceRecord(id,answer={},bank='claims'){
 const data=bankData(bank),claim=data.claims.find(x=>x.id===id);
 if(!claim||!C.verdicts.some(v=>v.id===answer.verdict))return null;
 const source=data.sources.map(id=>C.sources[id]).find(s=>s.lines.some(l=>l.id===answer.evidence));
 if(!source&&answer.evidence!=='none')return null;
 return {claim:claim.text,verdict:C.verdicts.find(v=>v.id===answer.verdict).label,lineId:answer.evidence,quote:source?source.lines.find(l=>l.id===answer.evidence).text:'Keine passende Angabe in den Quellen.',author:source?source.author:'Geprüfte Quellen: '+data.sources.join(', '),date:source?source.date:'',status:assess(id,answer,bank).status};
}
function checkSource(id,answer){
 const q=C.sourceQuestions.find(x=>x.id===id);if(!q)throw new Error('Unbekannte Quellenfrage');
 if(!['A','B','C'].includes(answer))return {status:'open',title:'Wähle zuerst eine Quelle',text:'Lies die Frage und vergleiche die Dokumente.'};
 return {status:answer===q.answer?'match':'revise',title:answer===q.answer?'Diese Quelle passt zur Frage':'Was müsste die Quelle dir sagen?',text:answer===q.answer?q.feedback:q.hint};
}
function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
return {assess,evidenceRecord,checkSource,escapeHtml};
});
