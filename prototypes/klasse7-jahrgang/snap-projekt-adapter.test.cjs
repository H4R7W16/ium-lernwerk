'use strict';
const fs=require('node:fs'),path=require('node:path'),test=require('node:test'),assert=require('node:assert/strict');
const adapterFile=path.join(__dirname,'snap-projekt-adapter.cjs'),bridgeFile=path.join(__dirname,'snap-projekt-bridge.js');
const adapter=fs.existsSync(adapterFile)?require(adapterFile):null,bridge=fs.existsSync(bridgeFile)?require(bridgeFile):null;
const ROOT='klasse7/programmieren/snap/';
function adapters(){assert.ok(adapter,'ALG-5-Editoradapter fehlt');return adapter;}
function api(){assert.ok(bridge,'ALG-5-Projektbrücke fehlt');return bridge;}
function sources(){const result=new Map(),root=path.join(__dirname,'../klasse7-programmieren/inhalt',ROOT);for(const name of ['lernwerk.html','lernwerk-editor.js','lernwerk-modell.js'])result.set(ROOT+name,fs.readFileSync(path.join(root,name),'utf8'));return result;}
const xml='<project name="Eigener Rover"><scenes><scene><stage><sprites/></stage></scene></scenes></project>';
function parsed(){return {documentElement:{tagName:'project'},querySelector:s=>s==='parsererror'?null:{}};}
function host(){let scene={},version=1,dirty=false,content=xml,ready=true,name='Eigener Rover',stops=0,resets=0,parseCalls=0;
 const h={ready:()=>ready,scene:()=>scene,revision:()=>version,name:()=>name,xml:()=>content,dirty:()=>dirty,stop:()=>{stops++;},markSaved:()=>{dirty=false;resets++;},markDirty:()=>{dirty=true;},afterOpen:()=>{},cancelLoad:()=>{},parseXML:()=>{parseCalls++;return parsed();},openXML:(text,done)=>{scene={};version++;dirty=false;content=text;queueMicrotask(done);}};
 return {h,change:()=>{version++;dirty=true;content=content.replace('</stage>','<variables/></stage>');},nativeOpen:()=>{scene={};version++;dirty=false;content=xml.replace('Eigener Rover','Anderer Rover');},setReady:v=>ready=v,state:()=>({scene,version,dirty,content,stops,resets,parseCalls})};}

test('zusätzlicher ALG-5-Editor erhält alle vorhandenen Snap-Dateien und erzwingt nur ALG-5',()=>{
 const source=sources(),before=new Map(source),out=adapters().addSnapProjectEditor(source);
 assert.notEqual(out,source);for(const [name,text]of before)assert.equal(out.get(name),text,name);assert.equal(source.size,before.size);
 for(const name of ['arbeit.html','arbeit-editor.js','arbeit-bridge.js','arbeit-herkunft.json'])assert.ok(out.has(ROOT+name),name);
 assert.match(out.get(ROOT+'arbeit.html'),/arbeit-bridge\.js/);assert.match(out.get(ROOT+'arbeit.html'),/arbeit-editor\.js/);assert.doesNotMatch(out.get(ROOT+'arbeit.html'),/src="lernwerk-editor\.js/);
 assert.match(out.get(ROOT+'arbeit-editor.js'),/resolveTask\('\?aufgabe=alg-5', ''\)/);assert.match(out.get(ROOT+'arbeit-editor.js'),/xml: projectXML/);
 const provenance=JSON.parse(out.get(ROOT+'arbeit-herkunft.json'));assert.equal(provenance.taskId,'alg-5');assert.equal(provenance.license,'AGPL-3.0-or-later');
});
test('unerwartete Quellmarker oder vorhandene Zielseiten werden abgewiesen',()=>{
 const source=sources();source.set(ROOT+'lernwerk-editor.js','unerwarteter Quellstand');assert.throws(()=>adapters().addSnapProjectEditor(source),/marker/i);
 const other=sources();other.set(ROOT+'arbeit.html','vorhanden');assert.throws(()=>adapters().addSnapProjectEditor(other),/vorhanden/);
});
test('Erfassen stoppt die Ausführung und bestätigt den exakt erfassten Stand',()=>{
 const x=host(),b=api().createBridge(x.h);assert.equal(b.ready,true);assert.equal(b.isDirty(),false);
 x.change();const snapshot=b.getSnapshot();assert.equal(snapshot.xml,x.state().content);assert.equal(snapshot.name,'Eigener Rover');assert.equal(x.state().stops,1);assert.equal(b.isDirty(),true);
 assert.equal(b.markSaved(snapshot.revision),true);assert.equal(b.isDirty(),false);
});
test('spätere Änderungen oder native Dateiöffnung werden nicht versehentlich als gesichert markiert',()=>{
 const x=host(),b=api().createBridge(x.h);const snapshot=b.getSnapshot();x.change();assert.equal(b.markSaved(snapshot.revision),false);assert.equal(b.isDirty(),true);
 const current=b.getSnapshot();assert.equal(b.markSaved(current.revision),true);x.nativeOpen();assert.equal(x.state().dirty,false);assert.equal(b.isDirty(),true);assert.equal(b.markSaved(current.revision),false);
});
test('Wiederöffnen bestätigt erst tatsächlich geladenen eigenen Stand und schützt Änderungen',async()=>{
 const x=host(),b=api().createBridge(x.h);await b.openProject(xml);assert.equal(b.isDirty(),false);
 x.change();const prior=x.state().content;await assert.rejects(b.openProject(xml),/Änderungen/);assert.equal(x.state().content,prior);
 await b.openProject(xml,{discardChanges:true});assert.equal(b.isDirty(),false);assert.equal(x.state().content,xml);
});
test('ungültige, übergroße und nicht vollständige XML verändern kein Projekt',async()=>{
 const x=host(),b=api().createBridge(x.h);for(const invalid of ['',42,'<!DOCTYPE project><project></project>','<!ENTITY a "b"><project></project>','x'.repeat(10*1024*1024+1)])await assert.rejects(b.openProject(invalid));
 x.h.parseXML=()=>({documentElement:{tagName:'svg'},querySelector:()=>null});await assert.rejects(b.openProject('<svg/>'),/Snap/);assert.equal(x.state().content,xml);assert.equal(x.state().stops,0);
});
test('Snap-Ladefehler stellt bisherigen Inhalt wieder her und meldet keinen Erfolg',async()=>{
 const x=host(),normal=x.h.openXML,b=api().createBridge(x.h);x.change();const prior=x.state().content;let attempts=0;
 x.h.openXML=(text,done)=>{attempts++;if(attempts===1){queueMicrotask(done);}else normal(text,done);};
 await assert.rejects(b.openProject(xml,{discardChanges:true}),/wiederhergestellt/);assert.equal(x.state().content,prior);assert.equal(b.isDirty(),true);assert.equal(attempts,2);
});
test('während eines Ladevorgangs kann kein zweiter Auftrag oder falscher Snapshot starten',async()=>{
 const x=host(),normal=x.h.openXML,b=api().createBridge(x.h);let complete;x.h.openXML=(text,done)=>{complete=()=>normal(text,done);};const pending=b.openProject(xml);
 assert.equal(b.ready,false);await assert.rejects(b.openProject(xml),/geladen/);assert.throws(()=>b.getSnapshot(),/geladen/);complete();await pending;assert.equal(b.ready,true);
});

test('abgeleitete Links erhalten das offene Projekt und die Runtime bleibt gültiges JavaScript',()=>{
 const pages=adapters().addSnapProjectEditor(sources()),html=pages.get(ROOT+'arbeit.html'),script=pages.get(ROOT+'arbeit-editor.js');
 for(const [,attrs]of html.matchAll(/<a\b([^>]*?)>/g))if(!/href="#/.test(attrs)){assert.match(attrs,/target="_blank"/);assert.match(attrs,/rel="noopener"/);}
 assert.match(script,/await window\.LernwerkProjectBridge\.openProject\(text, \{discardChanges: true\}\)/);
 assert.match(script,/window\.parent === window/);assert.match(script,/afterOpen:.*Process\.prototype\.enableJS = false/);
 new (require('node:vm').Script)(script);
 const manifest=JSON.parse(pages.get(ROOT+'arbeit-herkunft.json'));
 for(const [file,digest]of Object.entries(manifest.files))assert.equal(require('node:crypto').createHash('sha256').update(pages.get(ROOT+file)).digest('hex'),digest);
});
test('fehlgeschlagene Wiederherstellung hält eine Rettungskopie bereit und meldet keinen fertigen Editor',async()=>{
 const x=host(),b=api().createBridge(x.h);x.change();const previous=x.state().content;x.h.openXML=(text,done)=>queueMicrotask(done);
 await assert.rejects(b.openProject(xml,{discardChanges:true}),/Rettungskopie/);assert.equal(b.ready,false);assert.equal(b.recoverySnapshot.xml,previous);assert.equal(b.isDirty(),true);assert.equal(b.markSaved(),false);
});
test('kein Stand kann vor Bereitschaft erfasst oder geladen werden',async()=>{
 const x=host();x.setReady(false);const b=api().createBridge(x.h);assert.equal(b.ready,false);assert.throws(()=>b.getSnapshot(),/nicht bereit/);await assert.rejects(b.openProject(xml),/nicht bereit/);assert.equal(x.state().stops,0);
});
test('anderweitiges Speichern in Snap bestätigt keinen veränderten Stand der Arbeitskarte',()=>{
 const x=host(),b=api().createBridge(x.h);assert.equal(b.isDirty(),false);x.change();x.h.markSaved();assert.equal(x.state().dirty,false);assert.equal(b.isDirty(),true);
});
test('Zeitüberschreitung beim Öffnen bricht den alten Ladeauftrag ab und stellt den Inhalt wieder her',async()=>{
 const x=host(),normal=x.h.openXML;let attempts=0,cancelled=0;x.h.timeoutMs=5;x.h.cancelLoad=()=>cancelled++;x.h.openXML=(text,done)=>{if(++attempts>1)normal(text,done);};const b=api().createBridge(x.h);
 await assert.rejects(b.openProject(xml),/wiederhergestellt/);assert.equal(attempts,2);assert.ok(cancelled>=1);assert.equal(b.ready,true);assert.equal(b.isDirty(),false);
});
test('Übernehmen und Wiederöffnen starten keine durch Speicherereignisse ausgelösten Programme',async()=>{
 const x=host();let running=false;const stop=x.h.stop,save=x.h.markSaved;
 x.h.stop=()=>{stop();running=false;};x.h.markSaved=()=>{save();running=true;};
 const b=api().createBridge(x.h),snapshot=b.getSnapshot();assert.equal(b.markSaved(snapshot.revision),true);assert.equal(running,false);assert.equal(b.isDirty(),false);
 await b.openProject(xml);assert.equal(running,false);assert.equal(b.isDirty(),false);
});
test('Wiederherstellung geänderter Arbeit startet keine Änderungsereignis-Programme',async()=>{
 const x=host(),normal=x.h.openXML;let attempts=0,running=false;const stop=x.h.stop,mark=x.h.markDirty;x.h.stop=()=>{stop();running=false;};x.h.markDirty=()=>{mark();running=true;};
 x.h.openXML=(text,done)=>{if(++attempts===1)queueMicrotask(done);else normal(text,done);};const b=api().createBridge(x.h);x.change();
 await assert.rejects(b.openProject(xml,{discardChanges:true}),/wiederhergestellt/);assert.equal(running,false);assert.equal(b.isDirty(),true);
});
test('native Dateiöffnung beendet ihre Änderungsereignisse vor Rückkehr zur Bedienung',async()=>{
 const pages=adapters().addSnapProjectEditor(sources()),script=pages.get(ROOT+'arbeit-editor.js');
 const native=script.match(/await window\.LernwerkProjectBridge\.openProject\(text, \{discardChanges: true\}\);([\s\S]*?)notice\('Datei geöffnet:/);assert.ok(native);
 let running=false;const ide={recordUnsavedChanges:()=>{running=true;},stop:()=>{running=false;}};
 new Function('ide',native[1])(ide);assert.equal(running,false);
});
