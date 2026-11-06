'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),crypto=require('node:crypto'),path=require('node:path');
const {preparePages,preparePublishedPages}=require('../pages/build.cjs');
const original=preparePages(),published=preparePublishedPages(),ROOT='klasse7/medien/';
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
test('Medienbogen veröffentlicht sämtliche Aufgaben und Lehrmaterialien mit unveränderten Zeitbudgets',()=>{
 const files=[...published.keys()].filter(name=>name.startsWith(ROOT));
 assert.equal(files.filter(name=>name.endsWith('.html')).length,24);
 for(const file of ['index.html','medienbogen-durchfuhrung-und-auswertung.html','medienbogen-sicherung.html','medienbogen-briefing.html','med-3-bedienkarte-bildbearbeitung.html','material/hof-original.png','material/hof-original.svg','material/rollen-A.svg','material/rollen-B.svg'])assert.ok(published.has(ROOT+file),file);
 const f=JSON.parse(published.get(ROOT+'fassung.json'));
 assert.deepEqual(f.aufgaben,[45,45,90,45,45]);assert.equal(f.minuten,270);
 for(let i=1;i<=5;i++){assert.ok(published.has(ROOT+'med-'+i+'-briefing.html'));assert.ok(published.has(ROOT+'projektion-'+i+'.html'));}
});
test('Medien und Programmieren sind von Aufgaben und Startseiten gegenseitig erreichbar', () => {
 const seen = new Set();
 for (const [name, html] of published) {
  const area = name.split('/')[1];
  if (!name.startsWith('klasse7/') || !name.endsWith('.html') || !["medien","programmieren"].includes(area)
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
  for (const [target, label] of [["medien","Medien"],["programmieren","Programmieren"]]) {
   const link = links.find(link => link.target === 'https://example.test/ium-lernwerk/klasse7/' + target + '/index.html');
   assert.ok(link, name + ' → ' + target);
   assert.match(link.label, new RegExp('(?:^|\\s)' + label + '(?:\\s|$)'), name + ': Linkbeschriftung ' + label);
  }
 }
 assert.deepEqual([...seen].sort(), ["medien","programmieren"]);
});

test('Redaktionell geprüfte Texte und Bilder bleiben außerhalb des dokumentierten Publikationsadapters gleich',()=>{
 const fs=require('node:fs'),dir=path.join(__dirname,'inhalt');
 for(const name of fs.readdirSync(dir))if(name.endsWith('.html')){
  const source=fs.readFileSync(path.join(dir,name),'utf8'),html=original.get(ROOT+name);
  assert.ok(html,name);
  const main=x=>x.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1];
  if(!name.includes('produktionsbrief'))assert.equal(main(html),main(source),name);
 }
 const expected=require('./quelle-sha256.json');
 for(const [file,hash]of Object.entries(expected.files))assert.equal(sha(fs.readFileSync(path.join(dir,file))),hash,file);
});
test('Öffentliche Medienausgabe enthält keine lokalen Pfade oder internen Prüfnachweise',()=>{
 for(const [name,data]of published){if(!name.startsWith(ROOT))continue;
  assert.doesNotMatch(name,/(?:^|\/)(?:Nachweise|qa|docs|node_modules|\.git)(?:\/|$)/i,name);
  if(/\.(?:html|css|js|json|svg)$/.test(name))assert.doesNotMatch(String(data),/C:[\\/]Users[\\/]|127\.0\.0\.1|localhost|Lokale Lesefassung/,name);
 }
 const article=published.get(ROOT+'medienbogen-produktionsbrief-und-reihenkommentar.html');
 assert.doesNotMatch(article,/Veröffentlichung auf GitHub\/Pages ist ein eigener Bereitstellungsschritt/);
 assert.match(published.get(ROOT+'med-3-ein-bild-zwei-geschichten.html'),/download="hof-original\.png"/);
});
test('Jahresleitfaden erschließt die vollständigen Medienmaterialien',()=>{
 const html=published.get('klasse7/lehrpersonen.html');
 for(const file of ['medienbogen-durchfuhrung-und-auswertung','medienbogen-sicherung','medienbogen-briefing'])assert.ok(html.includes('href="medien/'+file+'.html"'));
 assert.doesNotMatch(html,/bleiben in Materialproduktion offen/);
});

test('Medienübersicht führt zuerst zu MED-1 und bietet fünf benannte Aufgaben zur freien Wahl', () => {
  const page = published.get(ROOT + 'index.html');
  const main = page.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1];
  assert.ok(/href="med-1-wer-lenkt-unseren-blick.html">Mit MED-1 beginnen/.test(main), 'Benannter Ersteinstieg fehlt');
  assert.match(main, /href="#aufgaben">Alle Aufgaben/);
  const list = main.match(/<ol[^>]*>([\s\S]*?)<\/ol>/)[1];
  assert.equal([...list.matchAll(/href="med-[1-5]-/g)].length, 5);
  assert.doesNotMatch(page.split('<main')[0], /class="(?:year-tools|course-nav)"/);
});

test('MED-1 zeigt Position, Titelwahl, Arbeitsbeginn und den direkten Weiter- und Rückweg', () => {
  const page = published.get(ROOT + 'med-1-wer-lenkt-unseren-blick.html');
  const main = page.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1];
  assert.ok(main.includes('Medien · Aufgabe 1 von 5'), 'Aufgabenposition fehlt');
  assert.match(main, /<a[^>]*href="med-1-wer-lenkt-unseren-blick.html"[^>]*aria-current="page"/);
  assert.match(main, /href="#1-einen-beitrag-auseinandernehmen-10-minuten"/);
  assert.match(main, /href="index.html">[^<]*Zur Medienübersicht/);
  assert.match(main, /href="med-2-stimmt-die-meldung.html">[^<]*MED-2 · Stimmt die Meldung\?/);
  assert.doesNotMatch(page.split('<main')[0], /class="(?:year-tools|course-nav)"/);
});

test('MED-1 bindet den Fizz-Spot und den Tonvergleich als zugängliche Belege für die Redaktionsnotiz ein', () => {
  const page = published.get(ROOT + 'med-1-wer-lenkt-unseren-blick.html');
  const main = page.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)[1];
  const clips = [...main.matchAll(/<video\b([^>]*)>([\s\S]*?)<\/video>/g)];
  assert.equal(clips.length, 2);

  for (const [index, name] of ['spot', 'tonvergleich'].entries()) {
    const [, attributes, contents] = clips[index];
    assert.match(attributes, /\bcontrols\b/);
    assert.match(attributes, /\bplaysinline\b/);
    assert.match(attributes, /\bpreload="none"/);
    assert.doesNotMatch(attributes, /\bautoplay\b/);
    assert.match(attributes, /\baria-label(?:ledby)?="[^"]+"/);
    assert.ok(clips[index][0].includes('src="material/fizz/' + name + '.mp4"'));
    assert.ok(attributes.includes('poster="material/fizz/' + name + '.jpg"'));
    const track = contents.match(/<track\b[^>]*>/)?.[0] ?? '';
    assert.match(track, /\bkind="captions"/);
    assert.match(track, /\bsrclang="de"/);
    assert.ok(track.includes('src="material/fizz/' + name + '.de.vtt"'));
    const base = ROOT + 'material/fizz/' + name;
    assert.ok(published.get(base + '.mp4')?.length > 0);
    assert.ok(published.get(base + '.jpg')?.length > 0);
    assert.match(String(published.get(base + '.de.vtt')), /^WEBVTT\b/);
  }

  const b = main.search(/<h3\b[^>]*>B\s*·/);
  const c = main.search(/<h3\b[^>]*>C\s*·/);
  assert.ok(b >= 0 && b < clips[0].index && clips[0].index < c, 'Spot gehört zu Beitrag B');
  assert.match(main, /<summary\b[^>]*>[^<]*(?:[Ll]ese|[Tt]ext)/);
  const note = main.match(/<h2\b[^>]*>3\s*·[\s\S]*?(?=<h2\b)/)?.[0] ?? '';
  assert.match(note, /(?:Clip|Spot|Bild|Ton|[Hh]örvergleich)/, 'Redaktionsnotiz greift einen Filmbeleg auf');
  assert.match(note, /(?:Grenze|prüfen|offen|belegt)/i, 'Redaktionsnotiz fordert eine Aussagegrenze');
});
