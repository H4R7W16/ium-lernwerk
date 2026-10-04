const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),P=require('./class5-teacher-pages.cjs');
test('Interne Arbeitsverweise werden in Lernseite und Einzelmaterial ausgegeben; fremde Pfade werden abgewiesen',()=>{
 const p=structuredClone(A.load().find(p=>p.area==='speicher-zugang'));
 p.steps[0].blocks[0].links=[{href:'../quellenquest/index.html#quellen',label:'Quellenquest öffnen'}];
 A.validate(p);
 const out=require('./class5-author-render.cjs').render(p);
 for(const file of ['schritt-auftakt.html','baustein-auftakt.html'])assert.match(out.get(file),/href="..\/quellenquest\/index.html#quellen"/);
 for(const href of ['javascript:alert(1)','//fremd.test','../../secret','../x/../y.html','https://fremd.test']){p.steps[0].blocks[0].links[0].href=href;assert.throws(()=>A.validate(p),/Verweis/);}
});
test('Weitere Reihen behalten eigenes Zeitkonto und überschreiten zusammen keine Jahresreserve',()=>{
 const p=structuredClone(P.plan);
 p.additionalSeries=[{...structuredClone(p.series),moduleId:'G5-M02',file:'reihe-recherche.html',label:'Recherche',phases:[{title:'Recherche',minutes:225}],later:{minutes:5,account:'spacedPracticeMinutes'}}];
 assert.doesNotThrow(()=>P.validate(p));
 p.additionalSeries[0].phases[0].minutes=226;assert.throws(()=>P.validate(p),/Reihenzeit/);
 p.additionalSeries[0].phases[0].minutes=225;p.additionalSeries[0].later.minutes=130;assert.throws(()=>P.validate(p),/Abrufkonto/);
});
test('Recherchepaket und Reihenverweise sind im gesamten Build samt Offlinebestand und getrenntem Arbeitsstand',()=>{
 const pack=A.load().find(p=>p.area==='recherche');assert.ok(pack,'Recherchepaket fehlt');
 const out=require('../m06-reinigungsfall/build.cjs').prepare(),R=require('./class5-author-render.cjs');
 for(const file of [...R.render(pack).keys(),...A.assets(pack).keys()]){assert.ok(out.has('klasse5/recherche/'+file),file);assert.ok(out.get('klasse5/mantel-sw.js').includes('recherche/'+file));}
 for(const file of ['lehrkraft.html','stoffverteilung.html','recherche/lehrkraft.html'])assert.match(out.get('klasse5/'+file),/reihe-recherche.html/);
 assert.ok(out.has('klasse5/reihe-recherche.html'));assert.match(out.get('klasse5/mantel-sw.js'),/reihe-recherche.html/);
 const M=require('./mantel-model.js'),u=A.unit(pack),other=A.unit(A.load().find(p=>p.area==='dateien'));
 const record=M.envelope(u,{step:pack.steps[0].id,fields:[{key:u.fields[0],value:'Meine Frage',type:'text'}]},'11111111-1111-4111-8111-111111111111','2026-10-04T11:00:00.000Z');
 assert.equal(M.parse(JSON.stringify(record),[u,other]).ok,true);
 assert.equal(M.parse(JSON.stringify({...record,moduleId:other.id,moduleVersion:other.version}),[u,other]).ok,false);
 for(const step of pack.steps)for(const block of step.blocks)for(const link of block.links||[]){const target=require('node:path').posix.normalize('klasse5/recherche/'+link.href.split('#')[0]);assert.ok(out.has(target),target);}
});

test('Externe Rechercheziele und Quellen bleiben auf Papier mit vollständiger Adresse nutzbar',()=>{
 const p=A.load().find(p=>p.area==='recherche'),out=require('./class5-author-render.cjs').render(p);
 assert.match(out.get('baustein-suchen-ipad.html'),/class="lw-print-url">https:\/\/www\.fragfinn\.de\//);
 assert.match(out.get('baustein-lesen.html'),/class="lw-print-url">https:\/\/www\.timeanddate\.de\/astronomie\/mond\/mondphasen/);
});
