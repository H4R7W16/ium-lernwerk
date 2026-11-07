'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const M = require('../shared/work-overview-model.js');
const file = path.join(__dirname, 'work-overview-projects.js');
const P = fs.existsSync(file) ? require(file) : {};
const catalog = {grade:7,areas:[{id:'programmieren',name:'Programmieren',path:'programmieren/index.html'}],tasks:[{id:'alg-5',area:'programmieren',title:'Rover',path:'programmieren/lernende/alg-5.html',places:[{id:'',title:'Ganze Aufgabe'}]}]};
const id='11111111-1111-4111-8111-111111111111';
const when='2026-11-06T21:00:00.000Z';
const xml='<project name="Eigener Rover" app="Snap! 11"><notes>Mein Test</notes><thumbnail></thumbnail><scenes select="1"><scene name="Szene"><notes></notes><hidden></hidden><headers></headers><code></code><blocks></blocks><variables></variables><stage name="Stage" width="480" height="360"><variables></variables><sprites></sprites><scripts></scripts></stage></scene></scenes></project>';
function setup() {
 assert.equal(typeof P.createSession,'function','ALG-5-Projektsitzung fehlt');
 let store=M.save(M.empty(),{taskId:'alg-5',place:'',locations:[{kind:'heft',hint:'Heft S.24',filename:''}],next:'Start an Station prüfen',inheritAreaHint:false},catalog,{id,now:when}).store;
 let dirty=false,revision=1,failOpen=false,markCalls=0;
 const bridge={ready:true,async openProject(value){if(failOpen)throw Error('Projekt kann nicht geöffnet werden');this.xml=value;dirty=false;revision++;},getSnapshot(){return {xml:this.xml||xml,name:'Mein Rover',revision};},isDirty(){return dirty;},markSaved(value){markCalls++;if(value!==revision)return false;dirty=false;return true;}};
 const session=P.createSession({model:M,catalog,getStore:()=>store,commit:next=>{store=next;return {store,volatile:false};},now:()=>when});
 session.connect(bridge,id);
 return {session,bridge,getStore:()=>store,setStore:s=>store=s,change:()=>{dirty=true;revision++;},fail:()=>{failOpen=true;},markCalls:()=>markCalls};
}
test('eigene XML bleibt bis zur bewussten Übernahme ungesichert; Karte behält Hinweise',async()=>{
 const s=setup();await s.session.openFile(xml,'Mein_Rover.xml');
 assert.equal(s.getStore().cards[0].project,undefined);assert.equal(s.session.hasChanges(),true);
 const result=s.session.capture('Mein_Rover.xml');assert.equal(result.ok,true);assert.equal(s.session.hasChanges(),false);
 assert.equal(s.getStore().cards[0].project.xml,xml);assert.equal(s.getStore().cards[0].next,'Start an Station prüfen');assert.equal(s.getStore().cards[0].locations[0].hint,'Heft S.24');
});
test('fehlgeschlagenes Öffnen ändert gespeichertes Projekt nicht',async()=>{
 const s=setup();await s.session.openFile(xml,'Eigen.xml');s.session.capture('Eigen.xml');const before=JSON.stringify(s.getStore());
 s.fail();await assert.rejects(s.session.openFile(xml.replace('Mein Test','Anderer Test'),'Anderes.xml'),/nicht geöffnet/);
 assert.equal(JSON.stringify(s.getStore()),before);
});
test('Änderung nach Wiederöffnung bleibt bis erneuter Übernahme sichtbar',async()=>{
 const s=setup();await s.session.openFile(xml,'Eigen.xml');s.session.capture('Eigen.xml');await s.session.openStored();assert.equal(s.session.hasChanges(),false);
 s.change();assert.equal(s.session.hasChanges(),true);s.session.capture('Eigen.xml');assert.equal(s.session.hasChanges(),false);
});
test('bei abgelehnter Speicherung wird der Editor nicht als übernommen markiert',async()=>{
 const s=setup();const session=P.createSession({model:M,catalog,getStore:s.getStore,commit:()=>({store:s.getStore(),volatile:true}),now:()=>when});session.connect(s.bridge,id);await session.openFile(xml,'Eigen.xml');
 const result=session.capture('Eigen.xml');assert.equal(result.ok,false);assert.equal(s.markCalls(),0);assert.equal(session.hasChanges(),true);
});
test('flüchtige RAM-Übernahme bleibt exportierbar und wird ausdrücklich gemeldet',async()=>{
 const s=setup();const session=P.createSession({model:M,catalog,getStore:s.getStore,commit:next=>{s.setStore(next);return {store:next,volatile:true};},now:()=>when});session.connect(s.bridge,id);await session.openFile(xml,'Eigen.xml');
 const result=session.capture('Eigen.xml');assert.equal(result.ok,true);assert.equal(result.volatile,true);assert.match(M.exportFile(s.getStore(),catalog,when),/Eigener Rover/);
});
test('eine zwischenzeitlich entfernte Karte wird nicht durch Projektübernahme neu angelegt',async()=>{
 const s=setup();await s.session.openFile(xml,'Eigen.xml');s.setStore(M.empty());assert.equal(s.session.capture('Eigen.xml').ok,false);assert.equal(s.markCalls(),0);
});
