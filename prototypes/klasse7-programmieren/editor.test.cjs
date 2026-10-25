'use strict';
const fs=require('node:fs'),path=require('node:path'),test=require('node:test'),assert=require('node:assert/strict');
const root=path.join(__dirname,'inhalt/klasse7/programmieren'),file=path.join(root,'snap/lernwerk-modell.js');
const api=fs.existsSync(file)?require(file):null;
function model(){assert.ok(api,'Die zusätzliche Lernwerk-Editoransicht fehlt noch.');return api;}

test('Aufgabenwahl öffnet nur die sechs vorgesehenen Startprojekte',()=>{
 const m=model();assert.equal(m.resolveTask('?aufgabe=alg-6','').project,'../projekte/ALG-6-Fehlersuche.xml');assert.equal(m.resolveTask('','').id,'alg-1');
 assert.equal(m.resolveTask('','#open:../projekte/ALG-2-Start.xml').id,'alg-2');
 for(const [q,h]of [['?aufgabe=alg-9',''],['?aufgabe=alg-1&aufgabe=alg-2',''],['','#open:https://example.org/a.xml'],['','#open:../../private.xml']])assert.equal(m.resolveTask(q,h),null);
});
test('Einstiegspalette erhält Original- und Reparaturblöcke ohne Ausgangseinstellungen zu ändern',()=>{
 const m=model(),base={reportLessThan:true},blocks={receiveGo:{},forward:{},doUntil:{},reportLessThan:{},reportNot:{},doBroadcast:{}};
 assert.deepEqual(m.hiddenPrimitives(blocks,base,true),{reportLessThan:true,doBroadcast:true});assert.deepEqual(base,{reportLessThan:true});assert.deepEqual(m.hiddenPrimitives(blocks,base,false),base);
 function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(p.endsWith('.xml'))for(const [,s]of fs.readFileSync(p,'utf8').matchAll(/<block\s+s="([^"]+)"/g))assert.ok(m.SELECTORS.includes(s),'notwendiger Block '+s+' in '+p);}}walk(root);
});
test('Export lässt die Lernwerkfilter auch bei einem Fehler nicht im Projekt zurück',()=>{
 const m=model(),stage={hiddenPrimitives:{doBroadcast:true}},scene={hiddenPrimitives:{doBroadcast:true}},oldStage=stage.hiddenPrimitives,oldScene=scene.hiddenPrimitives,base={};
 const serialized=m.withOriginalVisibility(stage,scene,base,()=>{assert.deepEqual(stage.hiddenPrimitives,{});scene.hiddenPrimitives=stage.hiddenPrimitives;return '<project/>';});
 assert.equal(serialized,'<project/>');assert.equal(stage.hiddenPrimitives,oldStage);assert.equal(scene.hiddenPrimitives,oldScene);
 assert.throws(()=>m.withOriginalVisibility(stage,scene,base,()=>{throw Error('Export fehlgeschlagen');}),/fehlgeschlagen/);assert.equal(stage.hiddenPrimitives,oldStage);assert.equal(scene.hiddenPrimitives,oldScene);
});
test('Lokales Öffnen akzeptiert XML, weist andere Dateien und Entitäten vorher ab',async()=>{
 const m=model(),xml='<project name="ALG-6"><scenes/></project>';
 assert.equal(await m.readProject(new File([xml],'ALG-6.xml')),xml);
 await assert.rejects(()=>m.readProject(new File(['text'],'notizen.txt')),/XML/);
 await assert.rejects(()=>m.readProject(new File(['<!DOCTYPE x><project></project>'],'fremd.xml')),/XML/);
 await assert.rejects(()=>m.readProject(new File(['<sprite></sprite>'],'figur.xml')),/Projekt/);
 await assert.rejects(()=>m.readProject(new File([new Uint8Array(10*1024*1024+1)],'gross.xml')),/10 MB/);
});
test('Downloadname ist eine XML-Datei ohne Pfadanteile',()=>{const m=model();assert.equal(m.filename(' ALG-6_Kennung.xml '),'ALG-6_Kennung.xml');assert.equal(m.filename('../A:B.xml'),'A_B.xml');assert.equal(m.filename(''),'MeinProgramm.xml');});
test('Einzelschritt ist nur bei aktiver Ausführung im Schrittmodus verfügbar',()=>{
 const m=model();assert.equal(m.controls({running:false,paused:false,stepping:true}).canStep,false);assert.equal(m.controls({running:true,paused:true,stepping:true}).canStep,true);assert.equal(m.controls({running:true,paused:true,stepping:true}).canPause,false);assert.equal(m.controls({running:true,paused:true,stepping:true}).pauseLabel,'Pause');assert.equal(m.controls({running:true,paused:false,stepping:false}).canStep,false);assert.equal(m.controls({running:true,paused:true,stepping:false}).pauseLabel,'Fortsetzen');
});
