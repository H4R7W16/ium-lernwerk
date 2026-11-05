'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),path=require('node:path');
const build=require('./build.cjs');
const base=build.prepareNavigablePages(),published=require('../shared/grade-navigation.cjs').addGradeNavigation(base);
const roots=['klasse5/','klasse6/','klasse7/programmieren/','klasse7/medien/','klasse7/daten/','klasse7/gaming/','klasse7/'];
const targets=['klasse5/index.html','klasse6/index.html','klasse7/index.html'];
const editable=[...base].filter(([name,data])=>/^klasse[567]\//.test(name)&&name.endsWith('.html')&&/<header\b[^>]*>[\s\S]*?<a class="(?:lw-shell-brand|brand)"/.test(data));
function header(html){return html.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0];}
function local(ref,name){return new URL(ref,'https://example.test/ium-lernwerk/'+name).pathname.slice('/ium-lernwerk/'.length);}

test('Jahrgangstitel öffnen eine native Auswahl mit drei gültigen Jahrgangseinstiegen',()=>{
 assert.ok(editable.length>150,'Reguläre Jahrgangsseiten vollständig prüfen');
 for(const [name]of editable){
  const html=published.get(name),grade=name.match(/^klasse(\d)/)[1];
  assert.match(html,/<details\b[^>]*data-grade-switch/,name);
  assert.match(html,new RegExp('aria-label="Klassenstufe wählen, aktuell Klasse '+grade+'"'),name);
  const deps=[...html.matchAll(/(?:href|src)="([^"]*grade-navigation\.(?:css|js))"/g)].map(m=>local(m[1],name)).sort();
  const root=name.startsWith('klasse7/gaming/')?'klasse7/gaming/':name.startsWith('klasse7/daten/')?'klasse7/daten/':name.startsWith('klasse7/medien/')?'klasse7/medien/':name.startsWith('klasse7/programmieren/')?'klasse7/programmieren/':grade==='7'?'klasse7/':roots[Number(grade)-5];
  assert.deepEqual(deps,[root+'grade-navigation.css',root+'grade-navigation.js'].sort(),name);
  const nav=html.match(/<nav class="lw-grade-options"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
  assert.ok(nav,'Jahrgangsnavigation '+name);
  const links=[...nav.matchAll(/<a href="([^"]+)"([^>]*)>/g)];
  assert.equal(links.length,3,name);
  assert.deepEqual(links.map(m=>local(m[1],name)),targets,name);
  assert.equal(links.filter(m=>m[2].includes('aria-current="true"')).length,1,name);
  assert.match(links[Number(grade)-5][2],/aria-current="true"/,name);
 }
});

test('tatsächliche Ausgabe verändert nur Header, Menüreferenzen und die zwei regulären Offlinepakete',()=>{
 const supported=new Set(editable.map(([name])=>name));
 for(const [name,old]of base){
  const value=published.get(name);assert.notEqual(value,undefined,name);
  if(supported.has(name)){
   const restored=value.replace(/<link rel="stylesheet" href="[^"]*grade-navigation\.css">/,'').replace(/<script src="[^"]*grade-navigation\.js" defer><\/script>/,'').replace(header(value),header(old));
   assert.equal(restored,old,'Außerhalb des Headers verändert: '+name);
  }else if(!['klasse5/mantel-sw.js','klasse6/mantel-sw.js','klasse7/programmieren/snap/lernwerk-herkunft.json'].includes(name))assert.deepEqual(value,old,name);
 }
 const added=[...published.keys()].filter(name=>!base.has(name));
 assert.deepEqual(added.sort(),roots.flatMap(root=>[root+'grade-navigation.css',root+'grade-navigation.js']).sort());
});

test('neue lokale Menüdateien und aktualisierte Version stehen in beiden regulären Offlinepaketen',()=>{
 for(const root of roots.slice(0,2)){
  const worker=published.get(root+'mantel-sw.js');
  assert.notEqual(worker.match(/const VERSION='([^']+)'/)[1],base.get(root+'mantel-sw.js').match(/const VERSION='([^']+)'/)[1],root);
  for(const file of ['grade-navigation.css','grade-navigation.js']){assert.ok(published.has(root+file),root+file);assert.ok(worker.includes(JSON.stringify(file)),root+file);}
 }
});

test('alle veröffentlichten HTML-Verweise bleiben unter dem Pages-Unterpfad und finden eine Datei',()=>{
 for(const [name,value]of published){if(!name.endsWith('.html'))continue;
  for(const [,ref]of value.matchAll(/(?:href|src)="([^"]+)"/g)){
   if(/^(https?:|mailto:|tel:|data:|#)/i.test(ref))continue;
   const url=new URL(ref,'https://example.test/ium-lernwerk/'+name);
   assert.ok(url.pathname.startsWith('/ium-lernwerk/'),name+' → '+ref);
   const target=decodeURIComponent(url.pathname.slice('/ium-lernwerk/'.length));
   assert.ok(published.has(target.endsWith('/')?target+'index.html':target),name+' → '+ref);
  }
 }
});

test('Herkunftsbindungen bleiben auch in der tatsächlichen Snap-Ausgabe korrekt',()=>{
 const crypto=require('node:crypto'),sha=b=>crypto.createHash('sha256').update(b).digest('hex'),root='klasse7/programmieren/snap/';
 for(const manifestFile of ['provenienz.json','lernwerk-herkunft.json']){const m=JSON.parse(published.get(root+manifestFile));for(const [file,expected]of Object.entries(m.files))assert.equal(sha(published.get(root+file)),expected,file);}
 const before=JSON.parse(base.get(root+'lernwerk-herkunft.json')),after=JSON.parse(published.get(root+'lernwerk-herkunft.json'));
 assert.equal(after.navigation.sourceShellSha256,before.files['lernwerk.html']);
 for(const [file,expected]of Object.entries(after.navigation.assets))assert.equal(sha(published.get(path.posix.normalize(root+file))),expected,file);
 for(const file of Object.keys(before.files))if(file!=='lernwerk.html')assert.equal(after.files[file],before.files[file],file);
});

test('Gesamtkonzept ergänzt die finale Ausgabe, Altvergleich und Offlinebindung',()=>{const final=require('../shared/gesamtkonzept.cjs').addConcept(published);for(const grade of [5,6,7]){const name='klasse'+grade+'/gesamtkonzept.html';assert.ok(final.has(name));assert.match(final.get(name),/Individueller Nachweis/);const id=grade===7?'inhalt':'main';assert.match(final.get(name),new RegExp('id="'+id+'"'));if(grade<7)assert.ok(final.get('klasse'+grade+'/mantel-sw.js').includes('"gesamtkonzept.html"'));}assert.match(final.get('beispiele/recherche/klasse5/recherche/index.html'),/Historischer Vergleichsstand/);require('../shared/grade-navigation.cjs').validateLinks(final);});

test('In Klasse 5/6 finden Lernende die Themenübersicht und Lehrende das gesamte Material des Jahrgangs', () => {
  const source = require('../shared/gesamtkonzept.cjs').addConcept(published);
  const final = require('../shared/themen-navigation.cjs').addTopicNavigation(source);
  for (const [name, prior] of source) {
    if (!/^klasse[56]\//.test(name) || name === 'klasse6/medienprodukt/projektion.html') {
      assert.deepEqual(final.get(name), prior, name);
      continue;
    }
    const match = name.match(/^(klasse[56])\/([^/]+)\/([^/]+\.html)$/);
    if (!match || !prior.includes('<span class="lw-shell-location"><b>')) continue;
    const [,grade,area,file] = match;
    const markup = header(final.get(name));
    assert.match(markup, /class="lw-shell-location"><a href="index.html"/, name);
    const topics = markup.match(/<div class="lw-shell-topics">([\s\S]*?)<button/)[1];
    const current = [...topics.matchAll(/<a\b([^>]*aria-current[^>]*)>/g)];
    assert.equal(current.length, 1, name);
    assert.equal(local(current[0][1].match(/\shref="([^"]+)"/)[1], name), grade + '/' + area + '/index.html', name);
    assert.ok(topics.includes('Jahrgangsübersicht'), name);
    if (file === 'material.html') assert.match(final.get(name), /href="\.\.\/material.html">← Alle Unterrichtsmaterialien<\/a>/, name);
  }
  for (const [grade, total] of [[5,10],[6,7]]) {
    const name = 'klasse' + grade + '/index.html';
    const cards = final.get(name).match(/<article class="lw-card"[^>]*>[\s\S]*?<\/article>/g);
    assert.equal(cards.length, total);
    const labels = cards.map(card => card.match(/<a[^>]*>([^<]*öffnen →)<\/a>/)?.[1]);
    assert.ok(labels.every(Boolean), name);
    assert.equal(new Set(labels).size, total);
  }
  assert.match(final.get('klasse6/jahresstart.html'), /href="netze\/schritt-einstieg.html">Zur ersten Netzaufgabe/);
});
