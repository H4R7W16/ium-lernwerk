'use strict';

// Die veröffentlichten Aufgaben und ihre vorhandenen Überschriften sind die
// einzige Quelle für Rücksprungziele. Freie/importierte URLs gehören nicht hierher.
const groups = [
  { id: 'medien', name: 'Medien', prefix: 'MED', count: 5, notes: 'medienbogen-werkstattnotizen.html' },
  { id: 'daten', name: 'Daten', prefix: 'DAT', count: 5, notes: 'datenbogen-werkstattnotizen.html' },
  { id: 'programmieren', name: 'Programmieren', prefix: 'ALG', count: 6 },
  { id: 'gaming', name: 'Gaming und Wohlbefinden', prefix: 'GAM', count: 6, notes: 'gamingbogen-fachnotizen.html' },
];
const dataNotes = ['dat-1-schreibvorlage', 'dat-2-notizen', 'dat-3-rastervorlage', 'dat-4-rechenvorlage', 'dat-5-notizen'];
const privateHeading = /privat|denkpause|gesch[uü]tzt/i;

function textOf(html) {
  const entities = {amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—', middot: '·'};
  return html.replace(/<[^>]+>/g, '').replace(/&(#x[\da-f]+|#\d+|[a-z]+);/gi, (whole, value) => {
    if (value[0] !== '#') return entities[value.toLowerCase()] ?? whole;
    const code = /^#x/i.test(value) ? parseInt(value.slice(2), 16) : Number(value.slice(1));
    return code > 0 && code <= 0x10ffff ? String.fromCodePoint(code) : whole;
  }).replace(/\s+/g, ' ').trim();
}

function publicPlaces(html) {
  const candidates = [];
  for (const match of html.matchAll(/<h2\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/h2>/g)) {
    if (/^\d+-/.test(match[1])) candidates.push({id: match[1], title: textOf(match[2]), index: match.index});
  }
  // Die Programmieraufgaben tragen ihre stabilen IDs am umgebenden Abschnitt.
  for (const match of html.matchAll(/<section\b[^>]*\bid="(abschnitt-\d+)"[^>]*>\s*<h2\b[^>]*>([\s\S]*?)<\/h2>/g)) {
    candidates.push({id: match[1], title: textOf(match[2]), index: match.index});
  }
  return [{id: '', title: 'Ganze Aufgabe'}, ...candidates
    .filter(place => !privateHeading.test(place.id + ' ' + place.title))
    .sort((a, b) => a.index - b.index)
    .map(({id, title}) => ({id, title: title.replace(/^\d+\s*·\s*/, '').replace(/\s*·\s*\d+\s+Minuten.*$/, '')}))];
}

function assertTarget(pages, target, label) {
  if (!target || /^(?:\/|[a-z]+:)|\.\.|private|denkpause|lehrpersonen/i.test(target)) {
    throw Error(label + ': Unzulässiges Arbeitsziel: ' + target);
  }
  const url = new URL(target, 'https://catalog.invalid/klasse7/');
  const file = decodeURIComponent(url.pathname.slice(1));
  const page = pages.get(file);
  if (!page || (url.hash && !page.includes('id="' + decodeURIComponent(url.hash.slice(1)) + '"'))) {
    throw Error(label + ': Arbeitsziel fehlt: ' + target);
  }
}

function createCatalog(pages) {
  const areas = groups.map(group => ({
    id: group.id, name: group.name, path: group.id + '/index.html',
    notesPath: group.notes ? group.id + '/' + group.notes : 'programmieren/index.html#lernweg',
  }));
  const tasks = [];
  for (const group of groups) {
    for (let n = 1; n <= group.count; n++) {
      const code = group.prefix + '-' + n;
      const id = code.toLowerCase();
      const expression = group.id === 'programmieren'
        ? new RegExp('^klasse7/programmieren/lernende/' + id + '\\.html$')
        : new RegExp('^klasse7/' + group.id + '/' + id + '-(?!briefing\\.html$|bedienkarte)[^/]+\\.html$');
      const matches = [...pages.keys()].filter(file => expression.test(file));
      if (matches.length !== 1) throw Error(code + ': Es muss genau eine reguläre Aufgabe vorhanden sein; gefunden: ' + matches.length + '.');
      const file = matches[0];
      const html = pages.get(file);
      const heading = html?.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/)?.[1];
      if (!heading) throw Error(code + ': Aufgabentitel fehlt.');
      const task = {
        id, code, title: textOf(heading).replace(/^(?:MED|DAT|ALG|GAM)-\d+\s*·\s*/, ''),
        area: group.id, path: file.slice('klasse7/'.length),
        places: publicPlaces(html),
      };
      if (task.places.length < 2 || new Set(task.places.map(place => place.id)).size !== task.places.length) {
        throw Error(code + ': Öffentliche Arbeitsstellen fehlen oder sind doppelt.');
      }
      if (group.id === 'programmieren') {
        task.notesPath = task.path + '#abschnitt-' + (n === 6 ? '2' : '3');
        task.snapPath = 'programmieren/snap/lernwerk.html?aufgabe=' + id;
      } else {
        const notesPath = group.id + '/' + group.notes;
        const notes = pages.get('klasse7/' + notesPath);
        if (typeof notes !== 'string') throw Error(code + ': Notizseite fehlt: ' + notesPath);
        const note = group.id === 'daten' ? dataNotes[n - 1] : group.id === 'gaming' ? id + '-fachnotiz'
          : [...notes.matchAll(/<h2\b[^>]*\bid="([^"]+)"/g)].find(match => match[1].startsWith(id + '-'))?.[1];
        if (!note) throw Error(code + ': Notizabschnitt fehlt.');
        task.notesPath = notesPath + '#' + note;
      }
      for (const place of task.places) assertTarget(pages, task.path + (place.id ? '#' + place.id : ''), code);
      assertTarget(pages, task.notesPath, code);
      if (task.snapPath) assertTarget(pages, task.snapPath, code);
      tasks.push(task);
    }
  }
  for (const area of areas) {
    assertTarget(pages, area.path, area.name);
    assertTarget(pages, area.notesPath, area.name);
  }
  return {grade: 7, version: 1, areas, tasks};
}

module.exports = { createCatalog };
