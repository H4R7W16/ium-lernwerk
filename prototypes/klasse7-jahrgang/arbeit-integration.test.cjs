'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { preparePages, preparePublishedPages } = require('../pages/build.cjs');
const { createCatalog } = require('./arbeit-katalog.cjs');
const { addWorkOverview } = require('./arbeit-adapter.cjs');
const { assertReadingContent } = require('./lesefassung-vergleich.cjs');
const input = preparePages();
input.set('klasse7/wissen.html', require('node:fs').readFileSync(require('node:path').join(__dirname, 'inhalt/wissen.html'), 'utf8'));
// Die Katalogquelle endet direkt vor dem neuen Adapter; die vorhandenen
// Aufgabenwege liefern bereits die stabilen Notiz-Anker.
for (const [file, html] of input) {
  if (!/^klasse7\//.test(file) || !file.endsWith('.html') || file.includes('/snap/')) continue;
  const oldHeader = html.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0];
  if (!oldHeader) continue;
  const ref = target => require('node:path').posix.relative(require('node:path').posix.dirname(file), 'klasse7/' + target);
  input.set(file, html.replace(oldHeader, require('./kopfzeile.cjs').regularNavigation(file, oldHeader, ref, false)));
}
const source = require('./aufgabenwege.cjs').addTaskRoutes(input);
const catalog = createCatalog(source);
const main = html => html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)?.[0];

test('Der Klasse-7-Katalog registriert genau die 22 regulären Aufgaben mit gültigen Zielen', () => {
  assert.equal(catalog.grade, 7);
  assert.equal(catalog.version, 1);
  assert.deepEqual(catalog.areas.map(area => area.id), ['medien', 'daten', 'programmieren', 'gaming']);
  assert.equal(catalog.tasks.length, 22);
  assert.equal(new Set(catalog.tasks.map(task => task.id)).size, 22);
  for (const [prefix, total] of [['med', 5], ['dat', 5], ['alg', 6], ['gam', 6]]) {
    assert.deepEqual(catalog.tasks.filter(task => task.id.startsWith(prefix + '-')).map(task => task.id),
      Array.from({length: total}, (_, i) => prefix + '-' + (i + 1)));
  }
  function assertTarget(ref) {
    assert.doesNotMatch(ref, /^(?:\/|[a-z]+:)|\.\.|private|denkpause|lehrpersonen/i);
    const [file, fragment] = ref.split('?')[0].split('#');
    const html = source.get('klasse7/' + file);
    assert.ok(html, ref);
    if (fragment) assert.ok(html.includes('id="' + fragment + '"'), ref);
  }
  for (const area of catalog.areas) {
    assertTarget(area.path);
    assertTarget(area.notesPath);
  }
  for (const task of catalog.tasks) {
    assertTarget(task.path);
    assertTarget(task.notesPath);
    if (task.snapPath) assertTarget(task.snapPath);
    assert.deepEqual(task.places[0], {id: '', title: 'Ganze Aufgabe'});
    assert.ok(task.places.length >= 3, task.id);
    assert.equal(new Set(task.places.map(place => place.id)).size, task.places.length);
    for (const place of task.places) {
      assert.doesNotMatch(place.id + ' ' + place.title, /private?|denkpause|gesch[uü]tzte/i);
      assert.ok(place.title && !/[<>]|&(?:amp|lt|gt);/.test(place.title));
      assertTarget(task.path + (place.id ? '#' + place.id : ''));
    }
  }
});

test('DAT-1 und ALG-5 führen in die vorhandene Arbeit und zu den passenden Notizen', () => {
  const dat = catalog.tasks.find(task => task.id === 'dat-1');
  assert.equal(dat.title, 'Kommt wirklich dieselbe Nachricht an?');
  assert.equal(dat.notesPath, 'daten/datenbogen-werkstattnotizen.html#dat-1-schreibvorlage');
  assert.ok(dat.places.some(place => place.id === '3-besteht-dein-code-den-fremdtest-25-minuten'
    && place.title === 'Besteht dein Code den Fremdtest?'));
  const alg = catalog.tasks.find(task => task.id === 'alg-5');
  assert.equal(alg.title, 'Dein Rover, dein Härtetest');
  assert.ok(alg.places.some(place => place.id === 'abschnitt-3' && place.title === 'Bauen und selbst testen'));
  assert.equal(alg.notesPath, 'programmieren/lernende/alg-5.html#abschnitt-3');
  assert.equal(alg.snapPath, 'programmieren/snap/lernwerk.html?aufgabe=alg-5');
});

test('Ein fehlendes oder doppeltes Aufgabenziel bricht den Katalogaufbau verständlich ab', () => {
  const missing = new Map(source);
  missing.delete('klasse7/' + catalog.tasks[0].path);
  assert.throws(() => createCatalog(missing), /MED-1.*(?:fehlt|genau)/);
  const duplicate = new Map(source);
  duplicate.set('klasse7/medien/med-1-doppelt.html', source.get('klasse7/' + catalog.tasks[0].path));
  assert.throws(() => createCatalog(duplicate), /MED-1.*genau/);
});

test('Der Adapter ergänzt ausschließlich Übersicht, Assets und 22 ausdrücklich markierte Merken-Links', () => {
  const adapted = addWorkOverview(source);
  assert.ok(adapted.has('klasse7/arbeit.html'));
  for (const file of ['work-overview-model.js', 'work-overview-storage.js', 'work-overview.js', 'work-overview.css']) {
    assert.ok(adapted.has('klasse7/' + file), file);
  }
  const tasks = new Map(catalog.tasks.map(task => ['klasse7/' + task.path, task]));
  for (const [file, before] of source) {
    const after = adapted.get(file);
    const task = tasks.get(file);
    if (!task) { assert.deepEqual(after, before, file); continue; }
    const bookmarks = [...after.matchAll(/<nav data-work-overview="bookmark"[^>]*>([\s\S]*?)<\/nav>/g)];
    assert.equal(bookmarks.length, 1, file);
    const href = bookmarks[0][1].match(/href="([^"]+)"/)?.[1];
    const url = new URL(href, 'https://example.test/unterpfad/' + file);
    assert.equal(url.pathname, '/unterpfad/klasse7/arbeit.html', file);
    assert.equal(url.searchParams.get('aufgabe'), task.id, file);
    assert.match(bookmarks[0][1], />Für später merken<\/a>/);
    assertReadingContent(main(after), main(before), file);
    assert.doesNotMatch(after, /<script[^>]*work-overview|localStorage|sessionStorage/, file);
  }
  assert.equal([...source.values()].filter(value => typeof value === 'string' && value.includes('data-work-overview="bookmark"')).length, 0);
});

test('Nur der exakt gekennzeichnete Merken-Navigationszusatz ist vom Lesetextvergleich ausgenommen', () => {
  const before = '<main><h1>Fachliche Aufgabe</h1><p>Unveränderter Auftrag.</p></main>';
  assertReadingContent(before.replace('</h1>', '</h1><nav data-work-overview="bookmark"><a href="../arbeit.html?aufgabe=dat-1">Für später merken</a></nav>'), before, 'erlaubte Navigation');
  assert.throws(() => assertReadingContent(before.replace('Auftrag.', 'anderer Auftrag.'), before, 'Fachänderung'));
  assert.throws(() => assertReadingContent(before.replace('</h1>', '</h1><p data-work-overview="bookmark">Fachlicher Zusatz</p>'), before, 'kein Navigationszusatz'));
  assert.throws(() => assertReadingContent(before.replace('</h1>', '</h1><nav data-work-overview="beliebig">Weiterer Inhalt</nav>'), before, 'unbekannte Markierung'));
});

test('Die veröffentlichte Übersicht ist erreichbar; alle regulären Köpfe bieten Deine Arbeit', () => {
  const pages = preparePublishedPages();
  const work = pages.get('klasse7/arbeit.html');
  assert.match(work, /id="work-app"/);
  const json = work.match(/<script\b[^>]*id="work-catalog"[^>]*>([\s\S]*?)<\/script>/)?.[1];
  assert.deepEqual(JSON.parse(json), catalog);
  for (const [file, html] of pages) {
    if (!file.startsWith('klasse7/') || !file.endsWith('.html')) continue;
    const excluded = file.includes('/snap/') || /projektion(?:-\d+)?\.html$/.test(file)
      || /<(?:body|main)\b[^>]*class="[^"]*\bprojection\b/.test(html);
    const header = html.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0] || '';
    if (excluded) {
      assert.doesNotMatch(header, />Deine Arbeit<\/a>/, file);
      continue;
    }
    const link = header.match(/<a\b([^>]*)>Deine Arbeit<\/a>/);
    assert.ok(link, file);
    const url = new URL(link[1].match(/href="([^"]+)"/)[1], 'https://example.test/unterpfad/' + file);
    assert.equal(url.pathname, '/unterpfad/klasse7/arbeit.html', file);
    assert.equal(link[1].includes('aria-current="page"'), file === 'klasse7/arbeit.html', file);
  }
});
