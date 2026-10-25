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
 assert.equal(await m.readProject(new File(['<?xml version='+String.fromCharCode(34)+'1.0'+String.fromCharCode(34)+'?>'+xml],'mit-kopf.xml')),xml,'XML-Kopf vor Übergabe an Snap entfernen');
 await assert.rejects(()=>m.readProject(new File(['text'],'notizen.txt')),/XML/);
 await assert.rejects(()=>m.readProject(new File(['<!DOCTYPE x><project></project>'],'fremd.xml')),/XML/);
 await assert.rejects(()=>m.readProject(new File(['<sprite></sprite>'],'figur.xml')),/Projekt/);
 await assert.rejects(()=>m.readProject(new File([new Uint8Array(10*1024*1024+1)],'gross.xml')),/10 MB/);
});
test('Downloadname ist eine XML-Datei ohne Pfadanteile',()=>{const m=model();assert.equal(m.filename(' ALG-6_Kennung.xml '),'ALG-6_Kennung.xml');assert.equal(m.filename('../A:B.xml'),'A_B.xml');assert.equal(m.filename(''),'MeinProgramm.xml');});
test('Einzelschritt ist nur bei aktiver Ausführung im Schrittmodus verfügbar',()=>{
 const m=model();assert.equal(m.controls({running:false,paused:false,stepping:true}).canStep,false);assert.equal(m.controls({running:true,paused:true,stepping:true}).canStep,true);assert.equal(m.controls({running:true,paused:true,stepping:true}).canPause,false);assert.equal(m.controls({running:true,paused:true,stepping:true}).pauseLabel,'Pause');assert.equal(m.controls({running:true,paused:false,stepping:false}).canStep,false);assert.equal(m.controls({running:true,paused:true,stepping:false}).pauseLabel,'Fortsetzen');
});

test('native Blockmigrationen lassen benötigte Rechnungen und Vergleiche in der Palette sichtbar',()=>{
 const m=model(),vm=require('node:vm'),source=fs.readFileSync(path.join(root,'snap/src/objects.js'),'utf8');
 const match=source.match(/SpriteMorph\.prototype\.blockMigrations\s*=\s*(\{[\s\S]*?\n\s*\});/);assert.ok(match,'registrierte native Migrationen');
 const migrations=vm.runInNewContext('('+match[1]+')',{}, {timeout:1000});
 const blocks={reportVariadicSum:{},reportVariadicProduct:{},reportVariadicEquals:{},reportVariadicLessThan:{},reportVariadicGreaterThan:{},reportVariadicAnd:{},reportVariadicOr:{},reportNot:{},doBroadcast:{}};
 assert.deepEqual(m.hiddenPrimitives(blocks,{},true,migrations),{doBroadcast:true});
});
test('Bühnenskalierung erhält die ganzzahligen Grenzwerte des Programmierbogens exakt',()=>{
 const m=model();assert.equal(typeof m.layout,'function','Layout-Verhalten fehlt');
 for(const width of [390,834,1024,1265,1440]){
  const box=m.layout(width),center=box.width-240*box.stageRatio;let pixel=center;
  for(let step=1;step<=8;step++){pixel+=10*box.stageRatio;assert.equal((pixel-center)/box.stageRatio,step*10,'Grenzwert bei Breite '+width);}
  assert.ok(box.paletteWidth>=280,'lange Palettenblöcke lesbar');
 }
});

test('beide Editoreinstiege jeder Lernseite öffnen die zugehörige Aufgabe in der Lernwerk-Ansicht',()=>{
 const m=model();for(let n=1;n<=6;n++){
  const html=fs.readFileSync(path.join(root,'lernende/alg-'+n+'.html'),'utf8');
  const links=[...html.matchAll(/href="(\.\.\/snap\/[^" ]+\.html[^" ]*)"/g)].map(x=>x[1]);assert.equal(links.length,2,'Editorzugänge ALG-'+n);
  for(const link of links){const url=new URL(link,'https://example.test/klasse7/programmieren/lernende/alg-'+n+'.html');assert.equal(url.pathname,'/klasse7/programmieren/snap/lernwerk.html');assert.equal(m.resolveTask(url.search.replace(/&amp;/g,'&'),url.hash).id,'alg-'+n);}
 }
});
