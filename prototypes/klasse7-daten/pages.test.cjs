'use strict';
const { assertReadingContent } = require('../klasse7-jahrgang/lesefassung-vergleich.cjs');
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {preparePages,preparePublishedPages}=require('../pages/build.cjs');
const original=preparePages(),published=preparePublishedPages(),ROOT='klasse7/daten/';
const main=x=>x.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1],sha=b=>crypto.createHash('sha256').update(b).digest('hex');
test('Datenbogen ist vollständig mit fünf Aufgaben, sechs Briefings, Sicherung und 270 Minuten',()=>{
 assert.equal([...published.keys()].filter(p=>p.startsWith(ROOT)&&p.endsWith('.html')).length,24);
 const meta=JSON.parse(published.get(ROOT+'fassung.json'));assert.equal(meta.minuten,270);assert.deepEqual(meta.aufgaben,[60,45,75,60,30]);
 for(const f of ['index.html','datenbogen-durchfuhrung-und-auswertung.html','datenbogen-sicherung.html','datenbogen-briefing.html','datenbogen-material-und-alternativzugange.html','material/modell-daten.json'])assert.ok(published.has(ROOT+f),f);
 for(let i=1;i<=5;i++){assert.ok(published.has(ROOT+'dat-'+i+'-briefing.html'));assert.ok(published.has(ROOT+'projektion-'+i+'.html'));}
});
test('Geprüfte Quellen, Lernaufträge, Briefings und alle Bilder bleiben gebunden',()=>{
 const manifest=require('./quelle-sha256.json'),dir=path.join(__dirname,'inhalt');assert.equal(Object.keys(manifest.files).length,42);
 for(const [file,hash]of Object.entries(manifest.files)){
  const source=fs.readFileSync(path.join(dir,file));assert.equal(sha(source),hash,file);
  if(file.endsWith('.html')&&!['datenbogen-produktionsbrief-und-reihenkommentar.html','datenbogen-durchfuhrung-und-auswertung.html','datenbogen-quellen-und-nutzungsrechte.html'].includes(file))assertReadingContent(main(published.get(ROOT+file)),main(source.toString()),file);
  if(file.startsWith('material/'))assert.equal(sha(published.get(ROOT+file)),hash,file);
 }
 const plan=main(fs.readFileSync(path.join(dir,'datenbogen-durchfuhrung-und-auswertung.html'),'utf8')).replace('<span class="reference" title="Projektgrundlage im Vault">Klasse 7 - Jahrgangsbrief</span>','<a href="../programmieren/lehrpersonen/jahrgang.html">Klasse 7 – Jahrgangsbrief</a>').replace('Die Startseite der lokalen Lesefassung öffnen.','Die Startseite der Datenwerkstatt öffnen.');
 assertReadingContent(main(published.get(ROOT+'datenbogen-durchfuhrung-und-auswertung.html')),plan,'Durchführung und Auswertung');
});
test('Datenwerkstatt und übrige Klasse-7-Lernbögen sind von Unterseiten gegenseitig erreichbar', () => {
 const seen = new Set();
 for (const [name, html] of published) {
  const area = name.split('/')[1];
  if (!name.startsWith('klasse7/') || !name.endsWith('.html') || !["daten","medien","programmieren"].includes(area)
   || name.includes('/snap/') || /projektion(?:-\d+)?\.html$/.test(name)
   || /<(?:body|main)\b[^>]*class="[^"]*\bprojection\b/.test(html)) continue;
  seen.add(area);
  assert.match(html, /data-grade-switch/, name);
  assert.match(html, /aria-label="Klassenstufe wählen, aktuell Klasse 7"/, name);
  const menu = html.match(/<details class="year-topics"[^>]*>([\s\S]*?)<\/details>/)?.[1];
  assert.ok(menu, name + ': Themenmenü fehlt');
  const links = [...menu.matchAll(/<a\b([^>]*)>([\s\S]*?)<\/a>/g)].map(([, attributes, body]) => ({
   target: new URL(attributes.match(/\bhref="([^"]+)"/)?.[1], 'https://example.test/ium-lernwerk/' + name).href,
   label: (attributes.match(/\baria-label="([^"]+)"/)?.[1] || body.replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim(),
  }));
  for (const [target, label] of [["daten","Daten"],["medien","Medien"],["programmieren","Programmieren"]]) {
   const link = links.find(link => link.target === 'https://example.test/ium-lernwerk/klasse7/' + target + '/index.html');
   assert.ok(link, name + ' → ' + target);
   assert.match(link.label, new RegExp('(?:^|\\s)' + label + '(?:\\s|$)'), name + ': Linkbeschriftung ' + label);
  }
 }
 assert.deepEqual([...seen].sort(), ["daten","medien","programmieren"]);
});

test('Öffentliche Datenfassung enthält keine lokalen Pfade, Freigabetexte oder internen Nachweise',()=>{
 for(const [name,value]of published){if(!name.startsWith(ROOT))continue;
  assert.doesNotMatch(name,/(?:^|\/)(?:qa|docs|node_modules|\.git)(?:\/|$)/i,name);
  if(typeof value==='string')assert.doesNotMatch(value,/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost|Lokale Lesefassung|Konzeptfreigabe|nicht Bestandteil dieses Produktionsauftrags|Projektgrundlage im Vault/,name);
 }
 const sources=published.get(ROOT+'datenbogen-quellen-und-nutzungsrechte.html');assert.match(sources,/vollständig in dieser Webfassung enthalten/);
});
test('Alter Jahrgangslink führt zum aktuellen gemeinsamen Leitfaden',()=>{
 const legacy=published.get('klasse7/programmieren/lehrpersonen/jahrgang.html'),guide=published.get('klasse7/lehrpersonen.html');
 assert.match(legacy,/href="\.\.\/\.\.\/lehrpersonen.html"/);
 for(const area of ['medien','daten','programmieren','gaming'])assert.ok(guide.includes('href="'+area+'/index.html"'));
 assert.match(guide,/1620/);assert.match(guide,/29 Zielzuordnungen/);
});

test('Datenmenge und Auflösung bleiben in tatsächlicher Ausgabe konsistent',()=>{
 const model=JSON.parse(published.get(ROOT+'material/modell-daten.json'));
 assert.deepEqual(model.rasters['dreieck-4'],['0000','0110','0110','1111']);
 const plan=published.get(ROOT+'datenbogen-durchfuhrung-und-auswertung.html');
 for(let i=1;i<=12;i++)assert.ok(plan.includes('D'+String(i).padStart(2,'0')));
 for(const term of ['48 Bit','26 Byte'])assert.ok(plan.includes(term),term);
});


test('DAT-5 erhält den Zweckwechsel: eigenes Urteil vor feiner Ansicht und Gegenprüfung',()=>{
 const html=published.get(ROOT+'dat-5-welche-datenmenge-passt-zum-zweck.html');
 const first=html.indexOf('id="zweckwechsel"'),fine=html.indexOf('id="vergleich-8"'),check=html.indexOf('id="gegenpruefung"');
 assert.ok(first<fine&&fine<check);assert.ok(first>html.indexOf('Eine andere Person prüft'));
 for(const id of ['vergleich-8','gegenpruefung'])assert.match(html,new RegExp('<details id="'+id+'">'));
 assert.ok(html.indexOf('schluesselpaar-vorlagen.svg')>check);assert.ok(html.indexOf('Zeile 6, Spalte 8')>check);
 assert.equal((html.match(/id="zweckwechsel"/g)||[]).length,1);
});
test('Schlüsselpaar zeigt einen verlorenen Unterschied bei gleicher Auflösung und Datenmenge',()=>{
 const model=JSON.parse(published.get(ROOT+'material/schluesselpaar-modell.json')).rasters;
 const old=JSON.parse(published.get(ROOT+'material/modell-daten.json')).rasters;
 assert.deepEqual(model.I4,model.II4);assert.deepEqual(model.I4,old['schluessel-4']);assert.deepEqual(model.I8,old['schluessel-8']);
 const differences=[];for(let y=0;y<8;y++)for(let x=0;x<8;x++)if(model.I8[y][x]!==model.II8[y][x])differences.push([y+1,x+1]);
 assert.deepEqual(differences,[[6,8]]);assert.equal(model.I8[5][7],'0');assert.equal(model.II8[5][7],'1');
 for(const [n,rows]of Object.entries(model)){const size=n.endsWith('4')?4:8;assert.equal(rows.length,size);assert.ok(rows.every(row=>row.length===size&&/^[01]+$/.test(row)));}
});


test('DAT-5 bündelt den Abschluss und führt von der Notiz zur passenden Vergleichsstufe',()=>{
 const task=published.get(ROOT+'dat-5-welche-datenmenge-passt-zum-zweck.html'),notes=published.get(ROOT+'datenbogen-werkstattnotizen.html');
 assert.match(task,/Gilt deine Empfehlung für das Leihplansymbol auch für diesen neuen Zweck/);
 assert.match(task,/datenbogen-werkstattnotizen.html#dat-5-zwecknotiz/);assert.match(task,/datenbogen-werkstattnotizen.html#dat-5-feinnotiz/);
 for(const id of ['dat-5-zwecknotiz','dat-5-feinnotiz'])assert.equal([...notes.matchAll(new RegExp('id="'+id+'"','g'))].length,1);
 assert.match(notes,/dat-5-welche-datenmenge-passt-zum-zweck.html#dat-5-feinauftrag/);
 const fine=task.slice(task.indexOf('id="vergleich-8"'),task.indexOf('id="gegenpruefung"'));
 assert.match(fine,/id="dat-5-feinauftrag"/);assert.doesNotMatch(fine,/Begründe auch, was du damit noch nicht über echte Schlüssel weißt/);
});
test('DAT-5 vergrößert dieselben Bilder im Artikel und erhält native Vergleichsstufen',()=>{
 for(const file of ['dat-5-welche-datenmenge-passt-zum-zweck.html','projektion-5.html']){
  const html=published.get(ROOT+file);
  for(const n of ['4','8','vorlagen']){
   assert.equal([...html.matchAll(new RegExp('id="key-zoom-'+n+'"','g'))].length,1);
   assert.match(html,new RegExp('<label[^>]*for="key-zoom-'+n+'"'));
   assert.equal([...html.matchAll(new RegExp('src="material/schluesselpaar-'+n+'\\.svg"','g'))].length,1);
  }
  assert.doesNotMatch(html,/<a[^>]+href="material\/schluesselpaar-[^"]+"/);
  assert.match(html,/<details id="vergleich-8">/);assert.match(html,/<details id="gegenpruefung">/);
 }
});
