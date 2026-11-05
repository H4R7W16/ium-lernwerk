'use strict';

const groups = [
  { area: 'medien', code: 'MED', name: 'Medienbogen', notes: 'medienbogen-werkstattnotizen.html', recall: 'wiederaufnahme-medien.html', recallTitle: 'Stimmt die neue Meldung?' },
  { area: 'daten', code: 'DAT', name: 'Datenbogen', notes: 'datenbogen-werkstattnotizen.html', recall: 'wiederaufnahme-daten.html', recallTitle: 'Kommt das Datenpaket eindeutig an?' },
  { area: 'gaming', code: 'GAM', name: 'Gamingbogen', notes: 'gamingbogen-fachnotizen.html', recall: 'wiederaufnahme-gemischt.html', recallTitle: 'Vier Entscheidungen für ein Schulangebot' },
];

const privatePage = 'gamingbogen-private-denkpause.html';
const privateSections = [null, 'startentscheidung', 'eigene-schulische-medienphase', 'mein-versuch', 'mein-versuch', 'ruckblick-mit-abstand'];
const dataNotes = ['dat-1-schreibvorlage', 'dat-2-notizen', 'dat-3-rastervorlage', 'dat-4-rechenvorlage', 'dat-5-notizen'];
const originalPicker = /<(nav|div) class="course-nav" aria-label="Aufgaben">[\s\S]*?<\/\1>/;

function textOf(html) {
  return html.replace(/<[^>]+>/g, '').trim();
}

function headings(html) {
  return [...html.matchAll(/<h2\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/h2>/g)].map(match => ({
    id: match[1],
    title: textOf(match[2]).replace(/^\d+\s*·\s*/, '').replace(/\s*·\s*\d+\s+Minuten.*$/, ''),
  }));
}

// Die Auswahl der bestehenden Quelle liefert Reihenfolge und Dateien. Titel und
// Arbeitsschritte stammen aus den jeweiligen Aufgaben, auch bei späteren Umbenennungen.
function overviewLabels(html, group) {
  const main = html?.match(/<main\b[^>]*>([\s\S]*?)<\/main>/)?.[1];
  if (!main) throw Error('Lernbogenübersicht fehlt: ' + group.area + '/index.html');
  const labels = new Map();
  for (const link of main.matchAll(/<a\b[^>]*\bhref="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)) {
    // Medien führt die Kennung in einer eigenen Spanne; Daten und Gaming vor dem Kurztitel.
    const label = link[2].match(/<span class="mp-code">([^<]+)<\/span>/)?.[1]
      || textOf(link[2]).match(/^([A-Z]+-\d+)\s*·/)?.[1];
    if (label) labels.set(link[1], label.trim());
  }
  return labels;
}

function readTasks(pages, group, base, recap, notes) {
  const picker = recap?.match(originalPicker);
  if (!picker) throw Error('Aufgabenauswahl fehlt im ' + group.name);
  if (!notes) throw Error('Notizvorlage fehlt: ' + base + group.notes);
  const entries = [...picker[0].matchAll(/<a href="([^"]+)"[^>]*>([^<]+)<\/a>/g)];
  const overview = overviewLabels(pages.get(base + 'index.html'), group);
  if (!entries.length || entries.length !== overview.size) {
    throw Error(group.name + ': Die Aufgabenzahl in Auswahl und Bogenübersicht stimmt nicht überein.');
  }

  const recaps = headings(recap);
  const noteSections = headings(notes);
  return entries.map((match, index) => {
    const file = match[1];
    const code = match[2].trim();
    const expected = group.code + '-' + (index + 1);
    if (code !== expected || overview.get(file) !== code || !file.startsWith(code.toLowerCase() + '-')) {
      throw Error(group.name + ': Für ' + file + ' wird ' + expected + ' erwartet. Auswahl: ' + code
        + ', Bogenübersicht: ' + (overview.get(file) || 'kein Eintrag') + '.');
    }
    const number = index + 1;
    const html = pages.get(base + file);
    const h1 = html?.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/);
    if (!h1) throw Error(code + ': Lernseite mit Aufgabentitel fehlt: ' + base + file);
    const title = textOf(h1[1]).replace(/^(?:MED|DAT|GAM)-\d+\s*·\s*/, '');
    const phases = headings(html).filter(heading => /^\d+-/.test(heading.id));
    const phaseCount = code === 'GAM-6' ? 2 : 4;
    for (let n = 1; n <= phaseCount; n++) {
      if (!phases[n - 1]?.id.startsWith(n + '-')) {
        throw Error(code + ': Nummerierte Arbeitsphase ' + n + ' als Rücksprungziel fehlt in ' + file + '.');
      }
    }
    const work = code === 'MED-5' || code === 'GAM-6' ? phases[1] : phases[2];
    const recapPrefix = group.area === 'daten' ? number + '-' : code.toLowerCase() + '-';
    const recapSection = recaps.find(section => section.id.startsWith(recapPrefix));
    if (!recapSection) throw Error(code + ': Sicherungsabschnitt mit ID-Präfix ' + recapPrefix + ' fehlt im ' + group.name + '.');
    const note = group.area === 'medien' ? noteSections.find(section => section.id.startsWith(code.toLowerCase() + '-'))?.id
      : group.area === 'daten' ? dataNotes[index] : 'gam-' + number + '-fachnotiz';
    if (!note) throw Error(code + ': Notizabschnitt fehlt in ' + group.notes + '.');
    return { file, number, code, title, phases, work, end: phases[phaseCount - 1], recap: recapSection.id, note };
  });
}

function picker(tasks, current) {
  const items = tasks.map(task => {
    const late = task.code === 'GAM-6' ? ' · Späterer Termin' : '';
    const selected = task === current ? ' aria-current="page"' : '';
    return '<li><a' + selected + ' href="' + task.file + '">' + task.code + ' · ' + task.title + late + '</a></li>';
  }).join('');
  return '<nav data-task-routes="selection" class="task-route-picker" aria-label="Aufgabe wählen">'
    + '<details><summary>Aufgabe ' + current.number + ' von ' + tasks.length + ' · ' + current.title + '<span>Aufgabe wechseln</span></summary>'
    + '<ol>' + items + '</ol></details></nav>';
}

function direction(label, href, title) {
  return '<a href="' + href + '"><span>' + label + '</span><strong>' + title + '</strong></a>';
}

function sequence(group, tasks, task) {
  const previous = tasks[task.number - 2];
  const next = tasks[task.number];
  const links = [];
  if (previous) links.push(direction('Vorherige Aufgabe', previous.file, previous.code + ' · ' + previous.title));
  else links.push(direction('Zur Übersicht', 'index.html', group.name));
  if (next) {
    const label = next.code === 'GAM-6' ? 'Zum späteren Termin · 1–2 Wochen nach GAM-4' : 'Nächste Aufgabe';
    links.push(direction(label, next.file, next.code + ' · ' + next.title));
  } else {
    links.push(direction('Zur Bogenübersicht', 'index.html', 'Alle Aufgaben im ' + group.name));
    links.push(direction('Wiederaufnahme zum vereinbarten Termin', '../' + group.recall, group.recallTitle));
  }
  return '<nav data-task-routes="sequence" class="task-route-sequence" aria-label="Vorherige und nächste Aufgabe">' + links.join('') + '</nav>';
}

// Vorhandener Artikeltext und Linkbeschriftung bleiben bei der Präzisierung erhalten.
function pointToSections(html, sections) {
  return html.replace(/<a\b([^>]*?)\bhref="([^"]+)"([^>]*)>/g, (tag, before, href, after) => {
    const section = sections[href];
    if (!section) return tag;
    return '<a' + before + 'data-task-original-href="' + href + '" href="' + href + '#' + section + '"' + after + '>';
  });
}

function taskPage(html, group, tasks, task, recapName) {
  const targets = { [recapName]: task.recap, [group.notes]: task.note };
  if (group.area === 'gaming') targets[privatePage] = privateSections[task.number - 1];
  let page = pointToSections(html, targets).replace(originalPicker, picker(tasks, task));
  if (task.code === 'DAT-3') {
    const heading = new RegExp('(<h2 id="' + task.work.id + '">[^<]+</h2>)');
    page = page.replace(heading, '$1<p data-task-routes="tool" class="task-route-tool"><a href="'
      + group.notes + '#' + task.note + '">Schreibvorlage für dein Bildpaket öffnen</a></p>');
  }
  return page.replace('</main>', '</main>' + sequence(group, tasks, task));
}

function back(task, phase) {
  return '<a href="' + task.file + '#' + phase.id + '">Zurück zu ' + task.code + ' · ' + phase.title + '</a>';
}

function returns(links) {
  return '<nav data-task-routes="return" class="task-route-return" aria-label="Zurück zur Lernaufgabe">' + links.join('') + '</nav>';
}

function afterSections(html, destinations) {
  return html.replace(/(<h2\b[^>]*\bid="([^"]+)"[^>]*>[\s\S]*?)(?=<h2\b|<\/main>)/g,
    (section, body, id) => destinations.has(id) ? body + returns(destinations.get(id)) + '\n' : section);
}

function anchoredTag(tag, id) {
  return '<' + tag + ' data-task-anchor="true" id="' + id + '">';
}

function dataNotepad(html, tasks) {
  // DAT-1, DAT-3 und DAT-4 haben konkrete Vorlagen, die übrigen zwei Aufgaben eigene Tabellenzeilen.
  let page = html.replace(/<p>Für DAT-(1|4):[\s\S]*?<\/p>|<p>Für DAT-3:<\/p>\s*<pre>[\s\S]*?<\/pre>/g, block => {
    const number = Number(block.match(/DAT-(\d)/)[1]);
    const task = tasks[number - 1];
    return block.replace('<p>', anchoredTag('p', task.note)) + returns([back(task, task.work)]);
  });
  return page.replace(/<tr>(\s*<td>DAT-(2|5)<\/td>\s*<td>)([\s\S]*?)<\/td>\s*<\/tr>/g, (row, cells, number, description) => {
    const task = tasks[Number(number) - 1];
    return anchoredTag('tr', task.note) + cells + description + returns([back(task, task.work)]) + '</td>\n</tr>';
  });
}

function gamingNotepad(html, tasks) {
  return html.replace(/<tr>(\s*<td>)(<a href="([^"]+)">GAM-(\d)<\/a>)/g, (row, cell, anchor, href, number) => {
    const task = tasks[Number(number) - 1];
    return anchoredTag('tr', task.note) + cell + pointToSections(anchor, { [href]: task.work.id });
  });
}

function supportPages(pages, group, tasks, base, recapName) {
  const recapBack = new Map(tasks.map(task => [task.recap, [back(task, task.end)]]));
  pages.set(base + recapName, afterSections(pages.get(base + recapName), recapBack));
  const notes = pages.get(base + group.notes);
  if (group.area === 'medien') {
    const noteBack = new Map(tasks.map(task => [task.note, [back(task, task.work)]]));
    pages.set(base + group.notes, afterSections(notes, noteBack));
    const card = base + 'med-3-bedienkarte-bildbearbeitung.html';
    pages.set(card, pages.get(card).replace('</main>', returns([back(tasks[2], tasks[2].work)]) + '</main>'));
  } else if (group.area === 'daten') {
    pages.set(base + group.notes, dataNotepad(notes, tasks));
  } else {
    pages.set(base + group.notes, gamingNotepad(notes, tasks));
    const privateBack = new Map();
    for (const task of tasks) {
      const section = privateSections[task.number - 1];
      if (!section) continue;
      const phase = task.code === 'GAM-6' ? task.phases[0] : task.work;
      const links = privateBack.get(section) || [];
      links.push(back(task, phase));
      privateBack.set(section, links);
    }
    const page = base + privatePage;
    pages.set(page, afterSections(pages.get(page), privateBack));
  }
}

function addProgrammingReturn(pages) {
  const name = 'klasse7/wissen.html';
  const html = pages.get(name);
  const insertion = /(<h2 id="programmieren">[\s\S]*?<\/p>)(?=\s*<h2 id="gaming">)/;
  if (!html || !insertion.test(html)) throw Error('Abschnitt für die ALG-Rückwege auf ' + name + ' fehlt.');

  const items = [];
  for (let number = 1; number <= 6; number++) {
    const href = 'programmieren/lernende/alg-' + number + '.html';
    const heading = pages.get('klasse7/' + href)?.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/);
    if (!heading) throw Error('Aufgabentitel für den Wissensrückweg fehlt: ' + href);
    items.push('<li><a href="' + href + '">' + textOf(heading[1]) + '</a></li>');
  }
  const label = 'Zurück zu deiner Programmieraufgabe';
  const nav = '<nav data-task-routes="programming-return" class="task-route-programming" aria-label="' + label + '">'
    + '<details><summary>' + label + '</summary><ul>' + items.join('') + '</ul></details></nav>';
  pages.set(name, html.replace(insertion, section => section + '\n' + nav));
}

function addTaskRoutes(source) {
  const pages = new Map(source);
  for (const group of groups) {
    const base = 'klasse7/' + group.area + '/';
    const recapName = group.area + 'bogen-sicherung.html';
    const tasks = readTasks(pages, group, base, pages.get(base + recapName), pages.get(base + group.notes));
    for (const task of tasks) {
      if (task.code === 'MED-1') continue; // Eigener Lernweg mit Titeleinstiegen und Weiterlink.
      const name = base + task.file;
      pages.set(name, taskPage(pages.get(name), group, tasks, task, recapName));
    }
    supportPages(pages, group, tasks, base, recapName);
  }
  addProgrammingReturn(pages);
  return pages;
}

module.exports = { addTaskRoutes };
