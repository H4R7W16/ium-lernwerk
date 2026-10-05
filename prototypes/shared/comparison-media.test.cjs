const test=require('node:test'),assert=require('node:assert/strict');
const A=require('./class5-content.cjs'),R=require('./class5-author-render.cjs');
function pair(){
 const p=structuredClone(A.load().find(p=>p.area==='geraete'));
 p.media=[{id:'first',kind:'image',file:'assets/geraete/first.svg',title:'A & eins',alt:'Erster Gerätezustand',caption:'Ein Gerät vor dem Wechsel.',creator:'Lernwerk',license:'CC BY-SA 4.0',sourceId:'eigen'},{id:'second',kind:'image',file:'assets/geraete/second.svg',title:'B <zwei>',alt:'Zweiter Gerätezustand',caption:'Dasselbe Gerät danach.',creator:'Lernwerk',license:'CC BY-SA 4.0',sourceId:'eigen'}];
 p.preview='first';for(const k of p.knowledge){delete k.media;delete k.mediaLayout;}for(const s of p.steps)for(const b of s.blocks)delete b.media;
 const b=p.steps[0].blocks[0];b.media=['first','second'];b.mediaLayout='comparison';
 return p;
}
test('Bildvergleich bleibt mit beschrifteten Zuständen in Lernschritt und Einzelblatt zusammen',()=>{
 const p=pair();A.validate(p);const pages=R.render(p);
 for(const file of ['schritt-auftakt.html','baustein-auftakt.html']){
  const html=pages.get(file),group=html.match(/<div class="lw-media-comparison" role="group" aria-label="Bildvergleich">([\s\S]*?)<\/div>/);
  assert.ok(group,file+': zusammengehörender Bildvergleich fehlt');
  assert.equal((group[1].match(/<figure/g)||[]).length,2);
  assert.match(group[1],/alt="Erster Gerätezustand"/);assert.match(group[1],/alt="Zweiter Gerätezustand"/);
  assert.match(group[1],/A &amp; eins/);assert.match(group[1],/B &lt;zwei&gt;/);
  assert.ok(group[1].indexOf('first.svg')<group[1].indexOf('second.svg'));
  assert.ok(html.indexOf('lw-media-comparison')<html.indexOf('lw-solution'),'Beobachtungsmaterial darf nicht erst in der Lösung stehen');
 }
});
test('Bildvergleich weist unbrauchbare Gruppen und unbekannte Darstellungsformen vor dem Build ab',()=>{
 for(const mutate of [p=>p.steps[0].blocks[0].media=['first'],p=>p.steps[0].blocks[0].media=['first','first'],p=>p.media[1]={...p.media[1],kind:'download',file:'assets/geraete/second.txt',printText:'Datei'},p=>p.steps[0].blocks[0].mediaLayout='carousel']){
  const p=pair();mutate(p);assert.throws(()=>A.validate(p),/Bildvergleich|Mediendarstellung/);
 }
});
test('Einzelbilder und normale Medienlisten behalten ihre vorhandene Darstellung',()=>{
 const p=pair();delete p.steps[0].blocks[0].mediaLayout;
 assert.doesNotMatch(A.renderBlocks(p.steps[0],p),/lw-media-comparison/);
});

test('Wissensartikel zeigen denselben beschrifteten Bildvergleich',()=>{
 const p=pair(),k=p.knowledge[0];k.media=['first','second'];k.mediaLayout='comparison';A.validate(p);const html=R.render(p).get('wissen.html');assert.match(html,/<div class="lw-media-comparison" role="group" aria-label="Bildvergleich">/);assert.match(html,/A &amp; eins/);assert.match(html,/B &lt;zwei&gt;/);
});
