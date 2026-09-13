const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const modulePath = path.join(__dirname, 'lesson-model.js');
test('Zusätzliche Lernfassung stellt ihre prüfbare Lernlogik bereit', () => {
  assert.ok(fs.existsSync(modulePath), 'lesson-model.js fehlt noch');
});
if (fs.existsSync(modulePath)) {
  const L = require(modulePath);
  test('Körperaktionen bleiben bei gleichen Befehlen und mehreren Durchläufen unterscheidbar', () => {
    const run = L.simulate('klammer', 'wiederhole 4 [vor; vor; links]', {});
    assert.deepEqual(run.trace.slice(1,7).map(s=>[s.bodyIndex,s.iteration,s.count]), [[0,1,4],[1,1,4],[2,1,4],[0,2,4],[1,2,4],[2,2,4]]);
    assert.equal(run.cleaned.length, 8);
    assert.equal(run.success, false);
    assert.ok(L.criteria('klammer',run).every(c=>c.met));
    assert.equal(L.criteria('flaeche',run)[0].met, false);
  });
  test('Vorhersageauftrag verlangt keine vollständige Reinigung; leere Auswahl ist keine Vorhersage', () => {
    const run = L.simulate('vorhersage', 'vor\nlinks\nvor', {x:2,y:1,d:0});
    assert.equal(run.cleaned.length,3);
    assert.equal(L.predictionResult(run).correct,true);
    assert.equal(L.predictionResult(L.simulate('vorhersage','vor\nlinks\nvor',{})).available,false);
  });
  test('Eine Lauferwartung bleibt von späteren Änderungen unabhängig', () => {
    const pred={x:2,y:1,d:0};
    const run=L.simulate('vorhersage','vor\nlinks\nvor',pred);
    pred.x=1;
    assert.equal(run.prediction.x,2);
  });
  test('Neue Ergänzung verlangt bei gedrehter Startlage einen anderen Körper', () => {
    const good=L.simulate('ergaenzung','wiederhole 4 [vor; rechts]',{});
    const bad=L.simulate('ergaenzung','wiederhole 4 [vor; links]',{});
    assert.equal(good.success,true);
    assert.equal(bad.status,'wall');
    assert.deepEqual(good.end,[2,1,2]);
  });
  test('Eigene gültige Route erfüllt Abdeckung und Wiederholung, ungerollte Route nur Abdeckung', () => {
    const good='wiederhole 3 [vor]\nlinks\nvor\nlinks\nwiederhole 3 [vor]\nrechts\nvor\nrechts\nwiederhole 3 [vor]';
    assert.ok(L.criteria('plan',L.simulate('plan',good,{})).every(c=>c.met));
    const unrolled='vor\nvor\nvor\nlinks\nvor\nlinks\nvor\nvor\nvor\nrechts\nvor\nrechts\nvor\nvor\nvor';
    assert.equal(L.criteria('plan',L.simulate('plan',unrolled,{})).find(c=>c.id==='repeat').met,false);
  });
  test('Abrufvergleich erklärt eine konkrete falsch gruppierte Folge', () => {
    assert.equal(L.check('recall','grouped').correct,false);
    assert.match(L.check('recall','grouped').explanation,/links → vor.*links → vor/);
    assert.equal(L.check('recall','links;vor;links;vor').correct,true);
  });
  test('Selbst aufgebaute Abruffolgen werden in ihrer tatsächlichen Reihenfolge geprüft', () => {
    assert.equal(L.check('recall','links;vor;links;vor').correct,true);
    assert.equal(L.check('recall','links;links;vor;vor').correct,false);
    assert.equal(L.check('returnRecall','rechts;vor;rechts;vor').correct,true);
    assert.equal(L.check('returnRecall','rechts;vor').correct,false);
  });
  test('Eine zu große eigene Sicherung wird nicht als später unlesbare Datei ausgegeben', () => {
    const state=L.fresh();state.notes.open='x'.repeat(300001);
    assert.throws(()=>L.encode(state),/groß/);
  });
  test('Sicherung stellt Code, Arbeitsschritt, Erwartung und Erklärung wieder her', () => {
    const state=L.fresh();
    state.screen='plan';state.last='plan';state.work.plan.code='wiederhole 3 [vor]';
    state.work.plan.reason='Eine Zeile nach der anderen.';
    state.work.plan.prediction={x:4,y:3,d:1};
    state.work.plan.attempt={code:state.work.plan.code,prediction:{x:4,y:3,d:1},step:2};
    const restored=L.decode(L.encode(state));
    assert.equal(restored.work.plan.reason,state.work.plan.reason);
    assert.equal(restored.work.plan.attempt.step,2);
    assert.equal(restored.screen,'plan');
    assert.equal(restored.work.plan.prediction.d,1);
  });
  test('Beschädigte, fremde oder übergroße Sicherungen werden abgewiesen', () => {
    for(const text of ['{}','null','{','{"format":"anderes"}', 'x'.repeat(300001)]) assert.throws(()=>L.decode(text));
    const doc=JSON.parse(L.encode(L.fresh())); doc.state.work.plan.code=42;
    assert.throws(()=>L.decode(JSON.stringify(doc)));
    const future=JSON.parse(L.encode(L.fresh())); future.version=99;
    assert.throws(()=>L.decode(JSON.stringify(future)));
    const mixed=JSON.parse(L.encode(L.fresh()));
    mixed.state.work.plan.attempt={code:'vor',prediction:{},step:1};
    assert.throws(()=>L.decode(JSON.stringify(mixed)),/Codefassung/);
  });
}
