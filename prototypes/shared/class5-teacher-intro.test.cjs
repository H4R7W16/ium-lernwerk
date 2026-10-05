const test=require('node:test'),assert=require('node:assert/strict');
const path=require('node:path');
const assets=require('../m06-reinigungsfall/build.cjs').prepare();
const key='klasse5/einfuehrung.html';
test('Einführung ist aus Lehrpersonenübersicht erreichbar und alle Direktwege haben Ziele',()=>{
 assert.ok(assets.has(key),'Einführung fehlt im Build');
 assert.match(assets.get('klasse5/lehrkraft.html'),/href="einfuehrung.html"/);
 const html=assets.get(key),ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(new Set(ids).size,ids.length,'Doppelte IDs');
 for(const [,url] of html.matchAll(/href="([^"]+)"/g)){
  if(url.startsWith('#'))assert.ok(ids.includes(url.slice(1)),url);
  else if(!/^(?:https?:|mailto:)/i.test(url))assert.ok(assets.has(path.posix.normalize(path.posix.join('klasse5',url.split('#')[0]))),url);
 }
 for(const id of ['merkmale','konzeption','beispiel','begleiten','vorbereiten'])assert.ok(ids.includes(id),id);
 assert.match(assets.get('klasse5/mantel-sw.js'),/einfuehrung\.html/);
 assert.ok(assets.has('klasse5/einfuehrung.css'));
});
test('Mitmachbeispiel bleibt an Originalinhalt gebunden und Vertiefungen frei erreichbar',()=>{
 assert.ok(assets.has(key),'Einführung fehlt im Build');
 const html=assets.get(key),p=require('./class5-content.cjs').load().find(p=>p.area==='dateien');
 const b=p.steps[0].blocks[0];
 const escape=require('./class5-content.cjs').esc;
 for(const row of b.table.rows)for(const cell of row)assert.ok(html.includes(escape(cell)));
 assert.ok(html.includes(escape(b.help[0].text)));
 assert.ok(html.includes(escape(b.solution)));
 assert.match(html,/<details[^>]*>\s*<summary>Eine mögliche Erklärung/);
 assert.doesNotMatch(html,/<details[^>]*\bopen\b/);
 assert.match(html,/href="dateien\/schritt-ablegen\.html"/);
 assert.match(html,/href="dateien\/lehrkraft\.html"/);
 assert.doesNotMatch(html,/<textarea|<iframe|data-response|data-private/);
});test('Einführung erhält sichtbare Warnung und Rettung für bestehende Arbeit',()=>{
 const html=assets.get(key),css=assets.get('klasse5/einfuehrung.css');
 assert.match(html,/id="lw-storage-warning"/);assert.match(html,/id="lw-emergency-export"/);
 for(const [,selectors,body]of css.matchAll(/([^{}]+)\{([^{}]*)\}/g)){
  if(/display\s*:\s*none/.test(body))assert.doesNotMatch(selectors,/#lw-storage-warning|\.lw-storage-warning|#lw-emergency-export|\.lw-emergency-export/,'Speicherhilfe wird ausgeblendet');
 }
});