'use strict';
const fs=require('node:fs'),path=require('node:path');
const S=require('../m06-lernstudio/studio-model.js'),P=require('../m06-lernstudio/studio-learning.js');
const Q=require('../m02-quellenquest/content.js'),C=require('../m05-medienanalyse/content.js');
const functions=['entry','explanation','example','practice','application','revision','securing','transfer','retrieval'];
function validate(unit){if(unit.grade!==5||!unit.id||!unit.version||!unit.title||!unit.steps.length||functions.some(f=>!unit.learningDesign.coverage[f]||unit.learningDesign.coverage[f].split('/').some(id=>!unit.steps.some(s=>s.id===id))))throw new Error('Unvollständiger Lernbogen: '+unit.area);return unit;}
function fields(area,html){
 const app=fs.readFileSync(path.join(__dirname,'../',{'lernstudio':'m06-lernstudio/studio.js','medienanalyse':'m05-medienanalyse/app.js','quellenquest':'m02-quellenquest/app.js'}[area]),'utf8');
 const text=html+'\n'+app,result=new Set(['i:lw-retrieval']);
 for(const [,id]of text.matchAll(/id=["']([a-z][a-z0-9-]*)["']/gi))result.add('i:'+id);
 for(const [,name]of text.matchAll(/name=["']([a-z][a-z0-9-]*)["']/gi))result.add('n:'+name);
 for(const [,name]of app.matchAll(/note\(['"]([^'"]+)['"]/g))result.add('d:'+name);
 if(area==='quellenquest'){
 for(const q of Q.sourceQuestions)result.add('i:source-'+q.id);
 for(const bank of ['claims','transfer'])for(const q of Q[bank])result.add('n:'+bank+'-'+q.id);
 }if(area==='medienanalyse'){for(const c of C.claims)result.add('n:evidence-'+c.id);for(const c of C.transferClaims)result.add('n:transfer-'+c.id);}
 return [...result];
}
function catalog(assets){
 const records=[
 {area:'lernstudio',id:'IUM-5-CORE-06',family:'algorithm',title:'Sauber geplant',topic:'Algorithmen',description:'Befehle erproben, Schleifen verstehen und eigene Abläufe entwickeln.',product:'Ein eigener Plan mit begründeter Erklärung.',steps:S.order.map(id=>{const l=P.lesson(id);return {id,title:l.short,goal:l.entry,criteria:l.criteria};}),coverage:{entry:'start',explanation:'start',example:'example',practice:'loop/after/repair',application:'own',revision:'repair/own',securing:'own',transfer:'transfer',retrieval:'return/wiederaufnahme'}},
 {area:'medienanalyse',id:'IUM-5-CORE-05',family:'media',mediaClaims:C.claims.map(c=>c.id),mediaTransfer:C.transferClaims.map(c=>c.id),mediaChoices:C.choices.map(c=>c.id),mediaTransferChoices:C.judgements.map(c=>c.id),title:'Ein Bild – zwei Geschichten',topic:'Bilder und ihre Wirkung',description:'Ausschnitte und Überschriften untersuchen und einen eigenen Beitrag überarbeiten.',product:'Ein eigener Bildbeitrag mit begründeter Gestaltung.',steps:C.steps.map(s=>({id:s.id,title:s.title,goal:s.goal,criteria:s.criteria})),coverage:{entry:C.steps[0].id,explanation:C.steps[0].id,example:C.steps[1].id,practice:C.steps[1].id,application:C.steps[3].id,revision:C.steps[3].id,securing:C.steps[3].id,transfer:C.steps[4].id,retrieval:'wiederaufnahme'}},
 {area:'quellenquest',id:'IUM-5-CORE-02',family:'source',title:'Was wird aus unserer Pausenwiese?',topic:'Quellen prüfen',description:'Nachrichten untersuchen, passende Textstellen finden und mit Belegen antworten.',product:'Eine sachliche Antwort mit Beleg und offener Frage.',steps:Q.steps.map(s=>({id:s.id,title:s.short,goal:s.goal,criteria:s.criteria})),sourceBanks:{explore:['A','B','C'],claims:['A','B','C'],transfer:['D','E','F']},evidence:Object.fromEntries(Object.entries(Q.sources).map(([id,s])=>[id,s.lines])),claims:{claims:Q.claims.map(c=>c.id),transfer:Q.transfer.map(c=>c.id)},passages:[...Object.values(Q.sources).flatMap(s=>s.lines.map(l=>l.id)),'none'],coverage:{entry:'auftrag',explanation:'quellen',example:'quellen',practice:'belege',application:'antwort',revision:'antwort',securing:'antwort',transfer:'transfer',retrieval:'wiederaufnahme'}}
 ];
 return records.map(r=>validate({...r,schemaVersion:1,version:'1.0.0',grade:5,kind:'core',status:'working',prerequisites:['Kurze Aufträge lesen; mündliche und schriftliche Erklärung sind möglich.'],learningDesign:{goal:r.product,coverage:r.coverage},fields:fields(r.area,assets.get(r.area+'/index.html')),steps:[...r.steps,{id:'wiederaufnahme',title:'Später wieder aufgreifen',goal:'Erkläre die Beziehung erneut, bevor du nachliest.',criteria:['Ich rekonstruiere zuerst selbst.','Ich vergleiche und verbessere meine Erklärung.']}]}));
}
module.exports={catalog,validate,functions};
