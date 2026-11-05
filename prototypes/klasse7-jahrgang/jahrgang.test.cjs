'use strict';
const { assertReadingContent } = require('../klasse7-jahrgang/lesefassung-vergleich.cjs');
const test=require('node:test'),assert=require('node:assert/strict');
const {prepareNavigablePages,preparePublishedPages,preparePages}=require('../pages/build.cjs');
const original=require('../klasse7-programmieren/layout.cjs').applySeriesLayout(preparePages());
const final=preparePublishedPages();
const main=s=>s.match(/<main\b[^>]*>[\s\S]*?<\/main>/)?.[0];
test('22 Aufgaben und fachliche Materialien behalten ihre Hauptinhalte',()=>{
 let count=0;
 for(const [name,html]of original){if(!name.startsWith('klasse7/')||!name.endsWith('.html')||name==='klasse7/index.html'||name.endsWith('/lehrpersonen/jahrgang.html')||name==='klasse7/programmieren/index.html')continue;
  assertReadingContent(main(final.get(name)),main(html),name);count++;
 }assert.ok(count>=22);
 for(let i=1;i<=6;i++)assert.ok(final.has('klasse7/programmieren/lernende/alg-'+i+'.html'));
 for(const [prefix,total]of [['med',5],['dat',5],['gam',6]])assert.equal([...final.keys()].filter(n=>new RegExp('/'+prefix+'-[1-6]-(?!briefing)[^/]+\\.html$').test(n)&&!n.includes('bedienkarte')).length,total);
});
test('Die Kopfzeile führt aus jedem Lernbogen zu Themen, Wissen und Unterrichtsmaterial', () => {
  const topics = ['index.html', 'medien/index.html', 'daten/index.html', 'programmieren/index.html', 'gaming/index.html'];
  const knowledge = {medien:'medien/medienbogen-sicherung.html', daten:'daten/datenbogen-sicherung.html',
    programmieren:'wissen.html#programmieren', gaming:'gaming/gamingbogen-sicherung.html'};
  const href = a => a.match(/\shref="([^"]+)"/)?.[1];
  let count = 0;
  for (const [name, html] of final) {
    if (!name.startsWith('klasse7/') || !name.endsWith('.html')) continue;
    const projection = /projektion(?:-\d+)?\.html$/.test(name) || /<(?:body|main)\b[^>]*class="[^"]*\bprojection\b/.test(html);
    if (name.includes('/snap/') || projection) {
      assert.doesNotMatch(html, /class="year-topics"/, name);
      continue;
    }
    const header = html.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0];
    const menu = header?.match(/<details class="year-topics"[^>]*>([\s\S]*?)<\/details>/)?.[1];
    assert.ok(menu, name);
    assert.match(menu, /<summary\b[^>]*>Themen\b/, name);
    const target = a => {
      const url = new URL(href(a), 'https://example.test/ium-lernwerk/' + name);
      return url.pathname.slice('/ium-lernwerk/klasse7/'.length) + url.hash;
    };
    const area = name.split('/').length > 2 ? name.split('/')[1] : '';
    const links = [...menu.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/g)].map(m => m[0]);
    assert.deepEqual(links.map(target), topics, name);
    const current = area ? area + '/index.html' : 'index.html';
    assert.deepEqual(links.filter(a => a.includes('aria-current=')).map(target), [current], name);
    if (area) {
      const context = header.match(/<a\b[^>]*class="year-shell-context"[^>]*>[\s\S]*?<\/a>/)?.[0];
      assert.ok(context, name);
      assert.equal(target(context), current, name);
    }
    const access = [...header.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/g)].map(m => m[0]);
    const wissen = access.find(a => />Wissen<\/a>/.test(a));
    const material = access.find(a => a.includes('aria-label="Unterrichtsmaterial"'));
    assert.ok(wissen && material, name);
    const knowledgeTarget = target(wissen);
    const [file, fragment] = knowledgeTarget.split('#');
    if (area === 'programmieren') assert.equal(knowledgeTarget, knowledge.programmieren, name);
    else assert.equal(file, knowledge[area] || 'wissen.html', name);
    if (fragment) assert.ok(final.get('klasse7/' + file).includes('id="' + fragment + '"'), name);
    const materials = {
      medien: 'medien/medienbogen-durchfuhrung-und-auswertung.html',
      daten: 'daten/datenbogen-durchfuhrung-und-auswertung.html',
      gaming: 'gaming/gamingbogen-durchfuhrung-und-auswertung.html',
      programmieren: 'programmieren/index.html#lehrpersonen'
    };
    assert.equal(target(material), materials[area] || 'lehrpersonen.html#unterrichtsmaterial', name);
    count++;
  }
  assert.ok(count >= 22);
  for (const [page, destination] of [
    ['gaming/gam-4-eine-strategie-wirklich-ausprobieren.html', 'gamingbogen-private-denkpause.html#mein-versuch'],
    ['programmieren/lernende/alg-5.html', '../snap/lernwerk.html?aufgabe=alg-5']
  ]) {
    const tools = final.get('klasse7/' + page).match(/<nav class="year-tools"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
    assert.ok(tools?.includes(' href="' + destination + '"'), page);
  }
});
test('Jahresmaterialien und vier unveränderte Diagnosedateien sind erreichbar',()=>{
 for(const name of ['index','lehrpersonen','lernziele','briefing','uebergaenge','wiederaufnahme-medien','wiederaufnahme-daten','wiederaufnahme-programmieren','wiederaufnahme-gemischt','wiederaufnahme-lehrpersonen'])assert.ok(final.has('klasse7/'+name+'.html'));
 for(const file of ['eingangsdiagnose-lernende.pdf','eingangsdiagnose-lehrpersonen.pdf','Startdatei.txt','Beobachtungsraster.txt'])assert.ok(final.has('klasse7/material/'+file));
 assert.equal((final.get('klasse7/lernziele.html').match(/<td>3\.2\./g)||[]).length,29);
 assert.equal(270+270+405+270+90+90+135+45+45,36*45);
});
test('Snap-Laufzeit bleibt vom Jahresmantel unberührt und Verweise sind unterpfadfähig',()=>{
 const before=prepareNavigablePages();
 for(const [name,value]of original)if(name.startsWith('klasse7/programmieren/snap/'))assert.deepEqual(before.get(name),value,name);
 for(const [name,html]of final){if(!name.endsWith('.html'))continue;for(const [,ref]of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  if(/^(https?:|mailto:|tel:|data:|#)/.test(ref))continue;
  const url=new URL(ref,'https://example.test/ium-lernwerk/'+name);assert.ok(url.pathname.startsWith('/ium-lernwerk/'),name);
  const target=decodeURIComponent(url.pathname.slice(14));assert.ok(final.has(target.endsWith('/')?target+'index.html':target),name+' -> '+ref);
 }}
});

test('Der Jahrgangseinstieg bietet vier beschriftete Themenkarten und direkte Zugänge wie die Reihe', () => {
  const home = final.get('klasse7/index.html');
  assert.ok(/class="lw-hero lw-home-hero"/.test(home), 'Gemeinsamer Jahrgangseinstieg fehlt');
  assert.match(home, /href="#themen"/);
  const cards = [...home.matchAll(/<article\b[^>]*class="lw-card"[^>]*>([\s\S]*?)<\/article>/g)];
  assert.equal(cards.length, 4);
  for (const [i, slug] of ['medien', 'daten', 'programmieren', 'gaming'].entries()) {
    const card = cards[i][1];
    assert.match(card, new RegExp('href="' + slug + '/index.html"'));
    assert.match(card, /<h3\b[^>]*>[^<]+<\/h3>/);
    assert.match(card, /<img\b[^>]*alt=""/);
    assert.match(card, /Dein Ergebnis/);
    assert.match(card, new RegExp((i === 2 ? 405 : 270) + ' Minuten'));
  }
  for (const id of ['themen', 'wiederaufnahme']) {
    assert.match(home, new RegExp('id="' + id + '"'));
    assert.match(home, new RegExp('href="#' + id + '"'));
  }
  for (const page of ['wiederaufnahme-medien', 'wiederaufnahme-daten', 'wiederaufnahme-programmieren',
    'wiederaufnahme-gemischt', 'lehrpersonen', 'lernziele', 'briefing', 'gesamtkonzept']) {
    assert.ok(main(home).includes('href="' + page + '.html"'), page);
  }
});

test('Alle Jahreswege und das Gesamtkonzept nutzen die gemeinsamen Reihenstile', () => {
  for (const [name, html] of final) {
    if (!/^klasse7\/[^/]+\.html$/.test(name)) continue;
    for (const css of ['mantel.css', 'learning-ui.css', 'identity.css']) {
      assert.ok(html.includes('href="../klasse5/' + css + '"'), name + ': ' + css);
    }
    assert.doesNotMatch(html, /href="medien\/medien\.css"/);
    assert.match(html, /<main\b[^>]*\bid="inhalt"[^>]*tabindex="-1"/);
  }
});

test('15 Aufgaben haben eine benannte Wahl, einen lesbaren Standort und den richtigen Anschluss', () => {
  for (const [area, prefix, total] of [['medien','med',5],['daten','dat',5],['gaming','gam',6]]) {
    const folder = 'klasse7/' + area + '/';
    const tasks = [...final.keys()].filter(file => file.startsWith(folder + prefix + '-')
      && file.endsWith('.html') && !/briefing|bedienkarte/.test(file)).sort();
    assert.equal(tasks.length, total);
    for (const [index, file] of tasks.entries()) {
      if (prefix === 'med' && index === 0) continue; // MED-1 besitzt einen eigenen Lernweg.
      const html = final.get(file);
      const picker = html.match(/<nav data-task-routes="selection"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
      const steps = html.match(/<nav data-task-routes="sequence"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
      assert.ok(picker && steps, file);
      assert.ok(picker.includes('Aufgabe ' + (index + 1) + ' von ' + total), file);
      const choices = [...picker.matchAll(/<li><a([^>]*)>([^<]+)<\/a>/g)];
      assert.equal(choices.length, total, file);
      for (const [n, [, attributes, title]] of choices.entries()) {
        assert.ok(title.startsWith(prefix.toUpperCase() + '-' + (n + 1) + ' · '), file);
        assert.ok(attributes.includes(' href="' + tasks[n].slice(folder.length) + '"'), file);
        assert.equal(attributes.includes('aria-current="page"'), n === index, file);
      }
      if (index > 0) assert.ok(steps.includes(' href="' + tasks[index - 1].slice(folder.length) + '"'), file);
      const onward = index < tasks.length - 1 ? tasks[index + 1].slice(folder.length) : 'index.html';
      assert.ok(steps.includes(' href="' + onward + '"'), file);
      if (prefix === 'gam' && index === 4) assert.match(steps, /späteren Termin[^<]*1–2 Wochen nach GAM-4/, file);
    }
  }
});

test('Das Briefing jeder Stunde führt zur Lernaufgabe und an eine vorhandene Stelle im Stundenplan', () => {
  for (const [area, prefix, total] of [['medien','med',5],['daten','dat',5],['gaming','gam',6],['programmieren','alg',6]]) {
    const codeDir = area === 'programmieren' ? 'programmieren/lehrpersonen' : area;
    for (let n = 1; n <= total; n++) {
      const code = prefix + '-' + n;
      const file = 'klasse7/' + codeDir + '/' + (code === 'alg-6' ? 'hoerbriefing.html' : code + '-briefing.html');
      const html = final.get(file);
      const content = html.slice(html.indexOf('<main')).split('<aside')[0];
      const shownLinks = [...content.matchAll(/<a\s[^>]*?\bhref="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)];
      assert.ok(shownLinks.some(([, href]) => {
        const page = href.split('/').pop();
        return page === code + '.html' || (page.startsWith(code + '-') && !/(?:briefing|bedienkarte|durchfuehrung)/.test(page));
      }), file);
      const plan = shownLinks.find(([, href, title]) => href.includes('#') && /durchfuhrung|durchfuehrung/.test(href)
        && (code !== 'alg-6' || title.includes('ALG-6')));
      assert.ok(plan, file);
      const url = new URL(plan[1], 'https://example.test/' + file);
      assert.ok(final.get(url.pathname.slice(1)).includes('id="' + url.hash.slice(1) + '"'), file);
      if (prefix !== 'alg') assert.ok(url.hash.slice(1).startsWith(code + '-'), file);
    }
  }
});

test('Wissen und Arbeitsvorlagen führen zu den zugehörigen Lernaufgaben zurück', () => {
  const root = 'klasse7/';
  const routes = [
    ['medien/medienbogen-sicherung.html', 'med-2-stimmt-die-meldung.html#4-ruckmeldung-neuer-fall-und-private-denkpause-10-minuten'],
    ['daten/datenbogen-werkstattnotizen.html', 'dat-3-vom-bild-zum-pixelraster-und-zuruck.html#3-dein-eigenes-bildpaket-30-minuten'],
    ['gaming/gamingbogen-private-denkpause.html', 'gam-4-eine-strategie-wirklich-ausprobieren.html#3-erproben-und-beobachten-15-minuten'],
    ['gaming/gamingbogen-private-denkpause.html', 'gam-5-grenzen-schutzen-hilfe-erreichen.html#3-deine-entscheidung-20-minuten']
  ];
  for (const [file, expected] of routes) {
    assert.ok(final.get(root + file).includes(' href="' + expected + '"'), file);
    const url = new URL(expected, 'https://example.test/' + root + file);
    assert.ok(final.get(url.pathname.slice(1)).includes('id="' + url.hash.slice(1) + '"'), expected);
  }
  const section = final.get(root + 'wissen.html').split('<h2 id="programmieren">')[1].split('<h2 id="gaming">')[0];
  const list = section.match(/<nav data-task-routes="programming-return"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
  assert.ok(list && list.includes('Zurück zu deiner Programmieraufgabe'));
  for (let i = 1; i <= 6; i++) {
    assert.ok(list.includes('href="programmieren/lernende/alg-' + i + '.html"'), 'ALG-' + i);
  }
});
