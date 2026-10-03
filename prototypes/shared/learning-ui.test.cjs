const test=require('node:test'),assert=require('node:assert/strict');
const build=require('../m06-reinigungsfall/build.cjs');
const configs=[['medienanalyse',require('../m05-medienanalyse/content.js')],['quellenquest',require('../m02-quellenquest/content.js')]];
test('Materialübersichten haben je fünf eindeutige Zugänge ohne vollständige Aufgaben-Duplikate',()=>{
 const assets=build.prepare();
 for(const [area,c] of configs){const index=assets.get('klasse5/'+area+'/material.html');
  assert.equal((index.match(/href="baustein-/g)||[]).length,5,area);
  assert.ok(!index.includes('class="material-section"'),area+' keeps selection separate');
  for(const s of c.steps){const sheet=assets.get('klasse5/'+area+'/baustein-'+s.id+'.html');
   assert.ok(sheet.includes('data-lw-return'),s.id+' return');
   assert.ok(sheet.includes('Prüfe dein Ergebnis'),s.id+' criteria');
   assert.ok(sheet.includes('Mögliche Lösung'),s.id+' solution');
   assert.ok(sheet.includes('index.html#'+s.id),s.id+' entry');
   const escape=require('./learning-ui.js').escape;
   if(area==='quellenquest')for(const id of s.sources)for(const line of c.sources[id].lines)assert.ok(sheet.includes(escape(line.text)),s.id+' source '+line.id);
   else assert.ok(sheet.includes('assets/'+(s.id==='transfer'?'bibliothek':'schulfest')+'.png'),s.id+' image');
  }
 }
});
test('Wissen bietet fachliche Fragen und frühe Rückkehr bei stabilen Direktankern',()=>{
 const assets=build.prepare();
 for(const [area,c] of configs){const html=assets.get('klasse5/'+area+'/wissen.html');
  assert.ok(html.includes('Was möchtest du verstehen?'),area);
  assert.ok(html.indexOf('data-lw-return')<html.indexOf('id="'+c.steps[0].id+'"'));
  for(const s of c.steps)assert.ok(html.includes('id="'+s.id+'"'),s.id);
 }
});
test('Gemeinsamer Einstieg zeigt drei Fachvorschauen und führt zu allen Lernwegen',()=>{
 const html=build.prepare().get('klasse5/index.html');
 for(const area of ['lernstudio','medienanalyse','quellenquest']){
  assert.ok(html.includes('data-preview="'+area+'"'),area+' preview');
  assert.ok(html.includes('href="'+area+'/index.html"'),area+' route');
 }
});
