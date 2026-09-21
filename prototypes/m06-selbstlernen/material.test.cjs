'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const M=require('./model.js');
const {pages}=require('./content.cjs');

test('Der Planungszustand behält bei leerem und ungültigem Code alle zwölf Kacheln mit Startblick',()=>{
 const empty=M.planningState(M.rooms.own,'');
 assert.equal(empty.phase,'empty');
 assert.equal(empty.cellCount,12);
 assert.deepEqual(empty.start.pos,[1,3,1]);
 assert.deepEqual(empty.start.cleaned,['1,3']);

 const invalid=M.planningState(M.rooms.own,'wiederhole 3 [vor');
 assert.equal(invalid.phase,'invalid');
 assert.match(invalid.error,/Zeile 1/);
 assert.equal(invalid.cellCount,12);
 assert.deepEqual(invalid.start.pos,[1,3,1]);
});

test('Ein geänderter Entwurf kennzeichnet den vorherigen Lauf als veraltet',()=>{
 const oldCode='wiederhole 3 [vor]';
 const unchanged=M.planningState(M.rooms.own,oldCode,oldCode);
 assert.equal(unchanged.phase,'current');
 assert.equal(unchanged.stale,false);

 const changed=M.planningState(M.rooms.own,oldCode+'\nlinks',oldCode);
 assert.equal(changed.phase,'changed');
 assert.equal(changed.stale,true);
 assert.equal(changed.executedCode,oldCode);
});

test('Eine neue Ausführung öffnet beim passenden Endbild',()=>{
 const run=M.createExecution(M.rooms.own,'wiederhole 3 [vor]');
 const frame=M.executionFrame(run);
 assert.equal(frame.step,3);
 assert.equal(frame.total,3);
 assert.equal(frame.current.action,'vor');
 assert.equal(frame.next,null);
 assert.deepEqual(frame.state.pos,[4,3,1]);
 assert.equal(frame.state.cleaned.length,4);
 assert.equal(frame.resultStatus,'complete');
});

test('Vor und zurück ordnen Codezeile, Durchlauf und nächste Anweisung dem Bild zu',()=>{
 const run=M.createExecution(M.rooms.own,'wiederhole 2 [vor; links]');
 const start=M.executionFrame(run,0);
 assert.equal(start.current,null);
 assert.deepEqual(start.next,{action:'vor',line:1,iteration:1,count:2,position:1,length:2});

 const first=M.executionFrame(run,1);
 assert.deepEqual(first.current,{action:'vor',line:1,iteration:1,count:2,position:1,length:2,error:null});
 assert.deepEqual(first.next,{action:'links',line:1,iteration:1,count:2,position:2,length:2});
 assert.deepEqual(first.state.pos,[2,3,1]);

 const second=M.executionFrame(run,2);
 assert.deepEqual(second.current,{action:'links',line:1,iteration:1,count:2,position:2,length:2,error:null});
 assert.deepEqual(second.next,{action:'vor',line:1,iteration:2,count:2,position:1,length:2});
 assert.deepEqual(second.state.pos,[2,3,0]);
});

test('Ein Wandkontakt öffnet beim Stoppbild und bleibt schrittweise untersuchbar',()=>{
 const run=M.createExecution(M.rooms.own,'wiederhole 4 [vor]');
 const stopped=M.executionFrame(run);
 assert.equal(stopped.resultStatus,'wall');
 assert.equal(stopped.current.error,'wall');
 assert.deepEqual(stopped.state.pos,[4,3,1]);
 assert.equal(stopped.state.cleaned.length,4);

 const beforeWall=M.executionFrame(run,3);
 assert.equal(beforeWall.current.error,null);
 assert.deepEqual(beforeWall.next,{action:'vor',line:1,iteration:4,count:4,position:1,length:1});
 assert.deepEqual(beforeWall.state.pos,[4,3,1]);
});

test('Die Planungsseite rendert den 4×3-Startplan vor jeder Eingabe als eigene Arbeitsfläche',()=>{
 const html=pages.find(page=>page.id==='plan').html;
 const board=html.match(/<div id="plan-board"[\s\S]*?<\/div><p class="caption">/u)?.[0]||'';
 assert.match(html,/class="plan-workspace"/u);
 assert.match(html,/id="plan-state"/u);
 assert.match(html,/id="previous-run"/u);
 assert.equal((board.match(/class="tile /gu)||[]).length,12);
 assert.match(board,/Roboter blickt nach rechts/u);
});

// UX08: Handrechnung, Koordinaten (Spalte, Reihe von oben, Blick 0/1/2/3).
// Erwartungen sind Literale, niemals aus simulate/expand erzeugt.
// Drehen bleibt am Ort; die vier Richtungen werden am Papierpfeil geprüft.
for(const [label,start,program,want] of [
 ['Fahren',[1,2,1],'vor',[2,2,1]],
 ['Links am Ort',[1,2,1],'links',[1,2,0]],
 ['Rechts am Rand',[1,2,1],'rechts',[1,2,2]],
 ['A1 links',[2,1,2],'links',[2,1,1]],
 ['A1 rechts',[2,1,2],'rechts',[2,1,3]],
 ['P1 Fahrt',[2,2,3],'vor',[1,2,3]],
 ['A7 nach oben',[1,2,3],'rechts\nvor\nrechts',[1,1,1]],
 ['P7 nach unten',[1,2,3],'links\nvor\nlinks',[1,3,1]],
]) test(label,()=>assert.deepEqual(M.simulate({width:4,height:3,start},program).trace.at(-1).pos,want));

test('Vergleich: vier Aktionen bedeuten nicht dieselbe Reihenfolge',()=>{
 assert.deepEqual(M.expand('wiederhole 2 [vor; rechts]').map(s=>s.action),['vor','rechts','vor','rechts']);
 assert.deepEqual(M.expand('wiederhole 2 [vor]\nwiederhole 2 [rechts]').map(s=>s.action),['vor','vor','rechts','rechts']);
});

test('Folgenprüfung trennt erste Abweichung, Durchläufe und Anweisungszahl',()=>{
 const r=M.checkSequence('practice',{
  sequence:'rechts rechts rechts vor vor vor',
  runs:'6',
  actions:'3'
 });
 assert.deepEqual(r.sequence,{ok:false,kind:'different',index:1,expected:'vor',actual:'rechts'});
 assert.deepEqual(r.counts.runs,{ok:false,actual:'6',expected:3});
 assert.deepEqual(r.counts.actions,{ok:false,actual:'3',expected:6});
});

test('Programmeingabe zeigt das Komma als konkrete Schreibstelle',()=>{
 const r=M.inspectProgram('wiederhole 3 [vor, links]');
 assert.equal(r.ok,false);
 assert.equal(r.kind,'comma');
 assert.equal(r.line,1);
 assert.equal(r.actual,',');
 assert.equal(r.expected,';');
 assert.equal(r.corrected,'wiederhole 3 [vor; links]');
});

test('Die Gruppierungsprüfung übernimmt die konkrete Komma-Diagnose',()=>{
 const r=M.checkGrouping('wiederhole 2 [vor, rechts]\nvor\nrechts\nvor\nlinks',['vor','rechts','vor','vor','rechts','vor','links']);
 assert.equal(r.ok,false);
 assert.equal(r.syntax.kind,'comma');
 assert.equal(r.syntax.line,1);
 assert.equal(r.syntax.corrected,'wiederhole 2 [vor; rechts]');
});

test('Komma-Rückmeldung erklärt Unterschied, nächsten Schritt und neue Schreibprobe',()=>{
 const r=M.assessPlan(M.rooms.own,'wiederhole 3 [vor, links]');
 assert.equal(r.kind,'comma');
 assert.match(r.message,/Komma/u);
 assert.match(r.message,/Semikolon/u);
 assert.match(r.nextStep,/Ersetze/u);
 assert.equal(r.application.id,'comma-probe');
 assert.match(r.application.prompt,/wiederhole 2 \[rechts, vor\]/u);
});

test('Der belegte falsche zweite Reihenwechsel wird an der ersten Richtungsentscheidung erklärt',()=>{
 const wrong=M.examples.own.replaceAll('rechts','links');
 const r=M.assessPlan(M.rooms.own,wrong);
 assert.equal(r.kind,'second-row-switch');
 assert.deepEqual(r.difference,{index:10,actual:'links',expected:'rechts'});
 assert.match(r.message,/links in der Mitte/u);
 assert.match(r.nextStep,/Anweisung 10/u);
 assert.equal(r.application.id,'p7-probe');
});

test('Wandkontakt nennt die erfolglose Fahrt und lässt die Ursache bei anderen Plänen offen',()=>{
 const r=M.assessPlan(M.rooms.own,'wiederhole 4 [vor]');
 assert.equal(r.kind,'wall');
 assert.deepEqual(r.wall,{step:4,line:1,iteration:4,position:[4,3,1]});
 assert.match(r.message,/vierten Fahrt/u);
 assert.match(r.nextStep,/drei Wege/u);
 assert.equal(r.application.id,'p6-probe');

 const other=M.assessPlan(M.rooms.own,'links\nwiederhole 3 [vor]');
 assert.equal(other.kind,'wall');
 assert.doesNotMatch(other.message,/Reihenwechsel/u);
});

test('Ein anderer unvollständiger Plan erhält nur beobachtbare Laufdaten',()=>{
 const r=M.assessPlan(M.rooms.own,'wiederhole 2 [vor]');
 assert.equal(r.kind,'incomplete');
 assert.equal(r.result.cleaned.length,3);
 assert.deepEqual(r.result.trace.at(-1).pos,[3,3,1]);
 assert.deepEqual(r.result.missing,['1,1','2,1','3,1','4,1','1,2','2,2','3,2','4,2','4,3']);
 assert.match(r.message,/3 von 12/u);
 assert.match(r.message,/Spalte 1, Reihe 1/u);
 assert.doesNotMatch(r.message,/Fehlidee|Reihenwechsel/u);
 assert.equal(r.application.id,'p8-probe');
});

test('Verschiedene vollständige Programme mit Schleife werden gleich anerkannt',()=>{
 const column='links\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]';
 for(const program of [M.examples.own,column]){
  const r=M.assessPlan(M.rooms.own,program);
  assert.equal(r.kind,'success');
  assert.equal(r.result.success,true);
  assert.match(r.message,/anderer Weg/u);
 }
});

test('Vollständige Fläche ohne Schleife wird anerkannt und nur an der Aufgabenanforderung weitergeführt',()=>{
 const expanded=M.expand(M.examples.own).map(step=>step.action).join('\n');
 const r=M.assessPlan(M.rooms.own,expanded);
 assert.equal(r.kind,'missing-loop');
 assert.equal(r.result.success,true);
 assert.match(r.message,/alle zwölf Kacheln/u);
 assert.match(r.nextStep,/Musterweg/u);
 assert.equal(r.application.id,'p9-probe');
});

test('Die neuen Proben sind für Rückmeldungen direkt adressierbar',()=>{
 const html=pages.map(page=>page.html).join('\n');
 for(const id of ['p3','p6','p7','p8','p9'])assert.match(html,new RegExp(`id="${id}-probe"`,'u'));
});

test('Die Oberfläche bindet Folgenbefunde und Plananalyse an erreichbare neue Proben',()=>{
 const source=fs.readFileSync(require.resolve('./app.js'),'utf8');
 assert.match(source,/r\.counts\.runs/u);
 assert.match(source,/M\.assessPlan\(M\.rooms\.own,program\)/u);
 assert.match(source,/data-open-probe/u);
});

test('4×2: drei Übergänge je Reihe, sieben Fahrten und zwei Drehungen',()=>{
 const r=M.simulate({width:4,height:2,start:[1,2,1]},'wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]');
 assert.deepEqual(r.trace.map(s=>s.pos),[[1,2,1],[2,2,1],[3,2,1],[4,2,1],[4,2,0],[4,1,0],[4,1,3],[3,1,3],[2,1,3],[1,1,3]]);
 assert.equal(r.cleaned.length,8);assert.equal(r.status,'complete');
});

test('4×3: Reihenroute, Spaltenroute und doppelte Linkswende unabhängig abgleichen',()=>{
 const row='wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]';
 const col='links\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]\nlinks\nvor\nlinks\nwiederhole 2 [vor]\nrechts\nvor\nrechts\nwiederhole 2 [vor]';
 for(const [program,count,steps,end] of [[row,12,15,[4,1,1]],[col,12,18,[4,3,2]],[row.replaceAll('rechts','links'),8,15,[4,3,1]]]){
  const r=M.simulate(M.rooms.own,program);assert.equal(r.cleaned.length,count);assert.equal(r.trace.length-1,steps);assert.deepEqual(r.trace.at(-1).pos,end);assert.equal(r.status,'complete');
 }
});

test('Randfahrt: nur zehn Kacheln; zwei verschiedene Ergänzungen erreichen die Mitte',()=>{
 const edge='wiederhole 3 [vor]\nlinks\nwiederhole 2 [vor]\nlinks\nwiederhole 3 [vor]\nlinks\nwiederhole 2 [vor]\nlinks';
 const r=M.simulate(M.rooms.own,edge);
 assert.deepEqual([...r.missing].sort(),['2,2','3,2']);assert.equal(r.cleaned.length,10);assert.deepEqual(r.trace.at(-1).pos,[1,3,1]);assert.equal(r.trace.length-1,14);
 for(const n of [2,3]){const fixed=M.simulate(M.rooms.own,edge+'\nlinks\nvor\nrechts\nwiederhole '+n+' [vor]');assert.equal(fixed.success,true);assert.deepEqual(fixed.trace.at(-1).pos,[n+1,2,1]);}
});

test('Neuer Start A11: ganze Dreiergruppe, dann einmal vor',()=>{
 const r=M.simulate({width:4,height:3,start:[1,1,1]},'wiederhole 2 [rechts; vor; links]\nvor');
 assert.deepEqual(r.trace.map(s=>s.pos),[[1,1,1],[1,1,2],[1,2,2],[1,2,1],[1,2,2],[1,3,2],[1,3,1],[2,3,1]]);assert.equal(r.cleaned.length,4);
});

test('Eigene Gruppierung akzeptiert äquivalente Schleifen statt nur Mustertext',()=>{
 const target=['vor','rechts','vor','vor','rechts','vor','links'];
 assert.equal(M.checkGrouping('wiederhole 2 [vor; rechts; vor]\nlinks',target).ok,true);
 assert.equal(M.checkGrouping('vor\nrechts\nwiederhole 2 [vor]\nrechts\nvor\nlinks',target).ok,true);
 assert.equal(M.checkGrouping('wiederhole 2 [vor; rechts; vor; links]',target).ok,false);
 assert.equal(M.checkGrouping(target.join('\n'),target).ok,false);
 assert.equal(M.checkGrouping('',target).ok,false);
});

test('Quadrat und Fortsetzung: nächste Lage, ganze Durchläufe und einmaliger Anschluss',()=>{
 const r=M.simulate({width:2,height:2,start:[1,2,1]},'wiederhole 4 [vor; links]\nvor');
 assert.deepEqual(r.trace.map(s=>s.pos),[[1,2,1],[2,2,1],[2,2,0],[2,1,0],[2,1,3],[1,1,3],[1,1,2],[1,2,2],[1,2,1],[2,2,1]]);
 assert.equal(r.cleaned.length,4);assert.equal(r.trace[2].iteration,1);assert.equal(r.trace[4].iteration,2);assert.equal(r.trace[9].repeat,false);
});

test('3×2-Modellweg: jede Kachel in der erklärten Reihenfolge',()=>{
 const r=M.simulate(M.rooms.plan,M.examples.plan);
 assert.deepEqual(r.trace.map(s=>s.pos),[[1,2,1],[2,2,1],[3,2,1],[3,2,0],[3,1,0],[3,1,3],[2,1,3],[1,1,3]]);
 assert.deepEqual(r.cleaned,['1,2','2,2','3,2','3,1','2,1','1,1']);
});

test('Neue kurze Proben: veränderter Start verändert die nötige Zahl und den Endstand',()=>{
 for(const [start,program,end,steps] of [
  [[2,2,1],'wiederhole 2 [vor]',[4,2,1],2],
  [[2,1,1],'wiederhole 2 [vor]',[4,1,1],2],
  [[3,1,1],'vor',[4,1,1],1],
  [[1,3,1],'wiederhole 2 [links; vor; rechts]\nvor',[2,1,1],7]
 ]){const r=M.simulate({width:4,height:3,start},program);assert.deepEqual(r.trace.at(-1).pos,end);assert.equal(r.trace.length-1,steps);assert.equal(r.status,'complete');}
 const over=M.simulate({width:4,height:2,start:[2,2,1]},'wiederhole 3 [vor]');assert.equal(over.status,'wall');assert.deepEqual(over.trace.at(-1).pos,[4,2,1]);
});

test('Neue Folgen behalten ganze Gruppen und Fortsetzung',()=>{
 for(const [program,want] of [
  ['wiederhole 3 [rechts; vor]',['rechts','vor','rechts','vor','rechts','vor']],
  ['wiederhole 2 [links; vor]',['links','vor','links','vor']],
  ['wiederhole 3 [links; vor]\nrechts',['links','vor','links','vor','links','vor','rechts']],
  ['wiederhole 2 [rechts; vor; vor]\nlinks',['rechts','vor','vor','rechts','vor','vor','links']]
 ])assert.deepEqual(M.expand(program).map(s=>s.action),want);
});

test('Der veröffentlichungsfreie 4×3-Musterinhalt hat die unabhängig berechnete Spur',()=>{
 const r=M.simulate(M.rooms.own,M.examples.own);
 assert.deepEqual(r.trace.map(s=>s.pos),[[1,3,1],[2,3,1],[3,3,1],[4,3,1],[4,3,0],[4,2,0],[4,2,3],[3,2,3],[2,2,3],[1,2,3],[1,2,0],[1,1,0],[1,1,1],[2,1,1],[3,1,1],[4,1,1]]);
 assert.deepEqual(r.cleaned,['1,3','2,3','3,3','4,3','4,2','3,2','2,2','1,2','1,1','2,1','3,1','4,1']);
});

test('UX10 verwendet klare Aufgabenbezeichnungen und zeigt Grundbewegungen vor der ersten Aufgabe',()=>{
 const start=pages.find(page=>page.id==='start');
 const all=pages.map(page=>page.label+'\n'+page.title+'\n'+page.intro+'\n'+page.html).join('\n');
 assert.doesNotMatch(all,/Selbst entfalten|Brücke 1|Brücke 2/u);
 assert.match(start.label,/Fahren und drehen/u);
 assert.ok(start.html.indexOf('<h2>Fahren und Drehen ansehen</h2>')<start.html.indexOf('id="a1"'));
});

test('UX10 verlinkt Fachbegriffe direkt mit gekennzeichneten Wissenseinträgen',()=>{
 const html=pages.map(page=>page.html).join('\n');
 for(const id of ['wissen-anweisung','wissen-schleife','wissen-durchlauf','wissen-klammern','wissen-programm','wissen-raum']){
  assert.match(html,new RegExp(`id="${id}"`,'u'));
  assert.match(html,new RegExp(`data-knowledge-target="${id}"`,'u'));
 }
});

test('UX10 erklärt Raumangaben sichtbar statt unbeschriftete Koordinaten zu verwenden',()=>{
 const html=pages.map(page=>page.html).join('\n');
 assert.doesNotMatch(html,/\([1-4],[1-3],[←↑→↓]\)/u);
 assert.match(html,/Spalten von links, Reihen von oben/u);
});

test('UX10 hält Rückkehrkontext und zeigt nur den aktuellen Simulationsschritt',()=>{
 const source=fs.readFileSync(require.resolve('./app.js'),'utf8');
 assert.match(source,/knowledgeReturn=\{page:state\.page,scrollY:window\.scrollY,focus/u);
 assert.match(source,/restoreKnowledgeReturn/u);
 assert.match(source,/data-knowledge-target/u);
 assert.doesNotMatch(source,/Gerade ausgeführt:[\s\S]*Als Nächstes:/u);
});


// UX11-Nacharbeit: fachliche Statusaussagen, keine Sicherungsfunktionen.
test('UX11: kurze Ortsangabe im kleinen Raum unterscheidet Bewegung und Blick',()=>{
 const r=M.simulate(M.rooms.square,M.examples.square);
 const description=M.describe(r.trace[2],M.rooms.square);
 assert.match(description,/rechts unten/u);
 assert.match(description,/Blick oben/u);
 assert.match(description,/am Ort/u);
 assert.ok(description.length<115);
});
test('UX11: der erfolglose Wandversuch beendet keinen Durchlauf',()=>{
 const r=M.simulate(M.rooms.own,'wiederhole 4 [vor]');
 const description=M.describe(r.trace.at(-1),M.rooms.own);
 assert.match(description,/Wand/u);
 assert.match(description,/abgebrochen/u);
 assert.doesNotMatch(description,/ist beendet/u);
});


test('UX11: ein Umweg bei bereits besuchter oberer Reihe erhält keine Reihenwechsel-Diagnose',()=>{
 const code='links\nwiederhole 2 [vor]\nrechts\nwiederhole 3 [vor]\nrechts\nwiederhole 2 [vor]\nrechts\nwiederhole 3 [vor]\nrechts\nvor\nlinks\nlinks\nvor\nlinks\nvor\nlinks\nvor';
 const r=M.assessPlan(M.rooms.own,code);
 assert.deepEqual(r.result.missing,['3,2']);assert.deepEqual(r.result.end,[2,2,0]);
 assert.equal(r.kind,'incomplete');assert.doesNotMatch(r.message,/zweiten Reihenwechsel/u);
 assert.equal(M.assessPlan(M.rooms.own,code+'\nrechts\nvor').kind,'success');
 assert.equal(M.assessPlan(M.rooms.own,'links\nvor\nlinks\nlinks\nvor').kind,'incomplete');
});
test('UX11: Kommahilfe gilt auch bei Großschreibung und schon im Entwurf',()=>{
 const code='WIEDERHOLE 3 [vor, links]';
 assert.equal(M.assessPlan(M.rooms.own,code).kind,'comma');
 assert.match(M.planningState(M.rooms.own,code).error,/Komma/u);
 assert.doesNotMatch(M.planningState(M.rooms.own,code).error,/verschachtelt/u);
});
test('UX11: Tippfehler und leere Anweisung nennen die konkrete Schreibstelle',()=>{
 const typo=M.assessPlan(M.rooms.own,'wiederhole 3 [vorr; links]');
 assert.match(typo.message,/vorr/u);assert.match(typo.message,/Zeile 1/u);assert.doesNotMatch(typo.message,/verschachtelt/u);
 const empty=M.assessPlan(M.rooms.own,'wiederhole 3 [vor; ; links]');assert.match(empty.message,/leere Anweisung/u);
});


test('UX11: Rückmeldungen verwenden keine redaktionellen Probenkennungen',()=>{
 const candidates=[M.assessPlan(M.rooms.own,M.examples.own),M.assessPlan(M.rooms.own,'wiederhole 2 [vor]'),M.assessPlan(M.rooms.own,'wiederhole 4 [vor]')];
 for(const r of candidates)assert.doesNotMatch(r.application?.prompt||'',/\bP\d+\b/u);
 const source=fs.readFileSync(require.resolve('./app.js'),'utf8');
 assert.doesNotMatch(source,/prompt:'[^']*\bP\d+\b/u);
});
