'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const M = require('../shared/work-overview-model.js');
// The optional target binds a regression run to the preserved pre-fix preview.
const P = require(process.env.ALG5_PROJECTS_TEST_TARGET || './work-overview-projects.js');
const id='11111111-1111-4111-8111-111111111111';
const when='2026-11-06T21:00:00.000Z';
const xml=note=>'<project name="Mein Rover"><scenes><scene><stage><notes>'+note+'</notes><sprites/></stage></scene></scenes></project>';
const catalog={grade:7,areas:[{id:'programmieren',name:'Programmieren',path:'programmieren/index.html'}],tasks:[{id:'alg-5',area:'programmieren',title:'Rover',path:'programmieren/lernende/alg-5.html',places:[{id:'',title:'Ganze Aufgabe'}]}]};
class Element {
  constructor(tag,doc){this.tagName=tag.toUpperCase();this.ownerDocument=doc;this.children=[];this.listeners={};this.attributes={};this.parentElement=null;this.textContent='';this.hidden=false;this.disabled=false;this.inert=false;this.files=[];this.value='';const classes=new Set();this.classList={toggle:(name,on)=>{if(on===undefined)on=!classes.has(name);if(on)classes.add(name);else classes.delete(name);},contains:name=>classes.has(name)};if(tag==='iframe')this.contentWindow={LernwerkProjectBridge:doc.bridge};}
  setAttribute(key,value){this.attributes[key]=String(value);if(key==='id')this.id=String(value);}
  getAttribute(key){return this.attributes[key];}
  append(...nodes){for(const node of nodes){node.parentElement=this;this.children.push(node);}}
  after(node){const parent=this.parentElement;assert.ok(parent);node.parentElement=parent;parent.children.splice(parent.children.indexOf(this)+1,0,node);}
  addEventListener(type,listener){(this.listeners[type]||(this.listeners[type]=[])).push(listener);}
  async emit(type){for(const listener of this.listeners[type]||[])await listener({target:this,preventDefault(){}});}
  async click(){if(!this.disabled)await this.emit('click');}
  showModal(){this.open=true;}
  close(){this.open=false;}
  remove(){if(this.parentElement)this.parentElement.children=this.parentElement.children.filter(node=>node!==this);this.parentElement=null;}
  focus(){this.ownerDocument.activeElement=this;}
}
function walk(node){return [node,...node.children.flatMap(walk)];}
async function setup(settings={}){
  let content=xml('Gesicherter eigener Stand'),dirty=false,revision=1,ready=true,recovery=null,fail=false;
  const loads=[],downloads=[],confirms=[],answers=[];
  const bridge={get ready(){return ready;},get recoverySnapshot(){return recovery;},isDirty:()=>dirty||!ready,getSnapshot:()=>{if(!ready)throw Error('Editor nicht bereit');return {xml:content,name:'Mein Rover',revision};},markSaved:()=>{dirty=false;return true;},async openProject(text){loads.push(text);if(fail){recovery={xml:content,name:'Mein Rover'};ready=false;const error=Error('Vorheriger Stand als Rettungskopie verfügbar.');error.recoverySnapshot=recovery;throw error;}content=text;revision++;dirty=false;}};
  let store=M.save(M.empty(),{taskId:'alg-5',place:'',locations:[],next:'Test an Station',inheritAreaHint:false},catalog,{id,now:when}).store;
  if(!settings.withoutProject)store=M.setProject(store,id,{format:'snap-project',version:1,filename:'Eigen.xml',savedAt:when,xml:content},catalog).store;
  const doc={bridge,createElement(tag){return new Element(tag,this);},getElementById(value){return walk(this.body).find(node=>node.id===value)||null;},querySelector(){return null;}};doc.body=new Element('body',doc);
  const win={confirm(message){confirms.push(message);return answers.length?answers.shift():true;}};
  let exports=0;
  const ui=P.createUI({model:M,catalog,getStore:()=>store,commit:next=>{store=next;return {store,volatile:false};},feedback(){},download:(text,filename,mime)=>downloads.push({text,filename,mime}),exportOverview:()=>{exports++;return settings.exportResult!==false;},document:doc,window:win});
  // No real clock is needed: state changes are driven explicitly by these tests.
  const interval=global.setInterval;global.setInterval=()=>0;
  try{await ui.open(id);}finally{global.setInterval=interval;}
  const byId=value=>{const node=doc.getElementById(value);assert.ok(node,value+' exists');return node;};
  return {ui,doc,loads,downloads,confirms,answers,byId,content:()=>content,store:()=>store,exports:()=>exports,edit(note){content=xml(note);dirty=true;revision++;},failLoad(){fail=true;},async file(text){const input=byId('work-project-file');input.files=[{name:'Neu.xml',size:text.length,text:async()=>text}];await input.emit('change');}};
}

test('verzögertes Dateilesen verwirft zwischenzeitliche Editoränderung nach Abbruch nicht',async()=>{
  const s=await setup();let resolve;
  const pendingText=new Promise(done=>{resolve=done;});
  const input=s.byId('work-project-file');input.files=[{name:'Neu.xml',size:100,text:()=>pendingText}];
  const change=input.emit('change');
  const frame=walk(s.doc.body).find(node=>node.tagName==='IFRAME');
  const blockedDuringRead=frame.inert;
  s.edit('Während des Lesens hinzugefügt');const expected=s.content();s.answers.push(false);resolve(xml('Andere Datei'));await change;
  assert.equal(s.content(),expected,'Zwischenzeitlicher eigener Stand muss erhalten bleiben');
  assert.equal(s.loads.length,1,'Nach dem abgebrochenen Dateiaustausch darf kein zweiter Load erfolgen');
  assert.equal(blockedDuringRead,true,'Der sichtbare Editor ist während des Austauschs nicht bedienbar');
  assert.equal(frame.inert,false);assert.equal(input.disabled,false);assert.match(s.byId('work-project-status').textContent,/abgebrochen|behalten|erhalten/i);
});

test('fehlgeschlagene Wiederherstellung bietet die Rettungskopie als erreichbaren Download an',async()=>{
  const s=await setup();s.edit('Eigene noch nicht übernommene Arbeit');const expected=s.content();s.failLoad();await s.file(xml('Nicht ladbar'));
  const rescue=s.byId('work-project-recovery');assert.match(rescue.textContent,/Rettungskopie/);assert.equal(s.ui.hasChanges(),true);
  await rescue.click();assert.equal(s.downloads.length,1);assert.equal(s.downloads[0].text,expected);assert.match(s.downloads[0].filename,/\.xml$/);assert.match(s.downloads[0].mime,/application\/xml/);
  assert.equal(s.byId('work-project-recovery'),rescue,'Downloadangebot darf die einzige Rettungskopie nicht entfernen');assert.equal(s.ui.hasChanges(),true,'Downloadangebot ist keine Speicherbestätigung');
  assert.equal(s.byId('work-project-take').disabled,true,'Ein nicht wiederhergestellter Editor darf nicht als übernehmbar erscheinen');
  assert.equal(s.store().cards[0].project.xml,xml('Gesicherter eigener Stand'),'Die zuvor gespeicherte Arbeitskarte bleibt erhalten');
});

test('abgelehnter Übersichtsexport meldet im sichtbaren Dialog keinen angebotenen Download',async()=>{
  const s=await setup({exportResult:false});await s.byId('work-project-pack').click();
  assert.equal(s.exports(),1);assert.doesNotMatch(s.byId('work-project-status').textContent,/Download angeboten/);
  assert.match(s.byId('work-project-status').textContent,/nicht heruntergeladen|fehlgeschlagen|Fehler/);assert.equal(s.byId('work-project-status').getAttribute('role'),'alert');
  assert.equal(s.downloads.length,0);assert.equal(s.ui.hasChanges(),false);
});


test('der Editor behält seine Layoutfläche, bleibt aber bis zur bewussten Auswahl verdeckt und inert',async()=>{
  const s=await setup({withoutProject:true});
  const frame=walk(s.doc.body).find(node=>node.tagName==='IFRAME');
  const cover=walk(s.doc.body).find(node=>node.getAttribute('class')==='work-project-cover');
  assert.ok(cover,'Lade-/Auswahlabdeckung vorhanden');assert.equal(frame.hidden,false,'Snap benötigt schon beim Booten eine tatsächliche Layoutfläche');
  assert.equal(cover.hidden,false);assert.equal(frame.inert,true,'Verdeckter Editor darf per Tab nicht bearbeitet werden');
  const start=walk(s.doc.body).find(node=>node.tagName==='BUTTON'&&node.textContent==='Mit Startprojekt beginnen');assert.ok(start);await start.click();
  assert.equal(cover.hidden,true);assert.equal(frame.inert,false);assert.equal(s.byId('work-project-take').disabled,false);assert.equal(s.ui.hasChanges(),true);
});

test('Startprojekt kann einen laufenden XML-Dateiaustausch nicht entsperren',async()=>{
  const s=await setup({withoutProject:true});let resolve;
  const pendingText=new Promise(done=>{resolve=done;});
  const input=s.byId('work-project-file');input.files=[{name:'Neu.xml',size:100,text:()=>pendingText}];
  const change=input.emit('change');
  const frame=walk(s.doc.body).find(node=>node.tagName==='IFRAME');
  const cover=walk(s.doc.body).find(node=>node.getAttribute('class')==='work-project-cover');
  const start=walk(s.doc.body).find(node=>node.tagName==='BUTTON'&&node.textContent==='Mit Startprojekt beginnen');
  await start.click();
  const stayedBlocked=frame.inert&&cover.hidden===false&&s.byId('work-project-take').disabled;
  resolve(xml('Ausgewählte Datei'));await change;
  assert.equal(stayedBlocked,true,'Start während file.text darf den gesperrten Editor nicht freigeben');
  assert.equal(s.content(),xml('Ausgewählte Datei'));assert.equal(s.loads.length,1);
  assert.equal(frame.inert,false);assert.equal(cover.hidden,true);assert.equal(s.ui.hasChanges(),true);
});
