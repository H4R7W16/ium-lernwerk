'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { createCatalog } = require('./arbeit-katalog.cjs');
const { addSnapProjectEditor } = require('./snap-projekt-adapter.cjs');

function addWorkOverview(source) {
  const pages = new Map(source);
  const catalog = createCatalog(pages);
  // Erst beim Bauen laden: Katalog und Modell bleiben unabhängig von der Oberfläche.
  const { renderWorkPage } = require('./arbeit-seite.cjs');
  pages.set('klasse7/arbeit.html', renderWorkPage(catalog));
  for (const asset of ['snap-project-model.js', 'work-overview-model.js', 'work-overview-storage.js', 'work-overview-projects.js', 'work-overview.js', 'work-overview.css']) {
    const folder = asset === 'snap-project-model.js' || asset === 'work-overview-model.js' || asset === 'work-overview-storage.js' ? '../shared' : '.';
    pages.set('klasse7/' + asset, fs.readFileSync(path.join(__dirname, folder, asset), 'utf8'));
  }
  for (const task of catalog.tasks) {
    const file = 'klasse7/' + task.path;
    const html = pages.get(file);
    if (html.includes('data-work-overview="bookmark"')) throw Error(task.code + ': Merken-Link bereits vorhanden.');
    const href = path.posix.relative(path.posix.dirname(file), 'klasse7/arbeit.html') + '?aufgabe=' + task.id;
    const bookmark = '<nav data-work-overview="bookmark" class="year-work-bookmark" aria-label="Deine Arbeit">'
      + '<a href="' + href + '">Für später merken</a></nav>';
    pages.set(file, html.replace(/(<main\b[^>]*>[\s\S]*?<\/h1>)/, '$1' + bookmark));
  }
  return addSnapProjectEditor(pages);
}

module.exports = { addWorkOverview };
