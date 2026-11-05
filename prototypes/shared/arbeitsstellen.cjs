'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { refreshWorker } = require('./grade-navigation.cjs');

function plain(html) {
  return html.replace(/<[^>]*>/g, '').replace(/&amp;/g, '&').replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim();
}

function slug(label) {
  return label.toLowerCase().replaceAll('ß', 'ss').normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function markWorkplaces(main, registered) {
  const ids = new Set([...main.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]));
  function mark(tag, suggested, label) {
    const existing = tag.match(/\bid="([^"]+)"/)?.[1];
    let id = existing || 'arbeitsstelle-' + suggested;
    if (!existing) {
      let suffix = 1;
      while (ids.has(id)) id = 'arbeitsstelle-' + suggested + '-' + ++suffix;
      ids.add(id);
    }
    registered[id] = label;
    return tag.replace(/>$/, (existing ? '' : ' id="' + id + '"') + ' data-arbeitsstelle>');
  }

  // Arbeitsblöcke und Bilder der Recherche-Referenz haben bereits veröffentlichte Direktanker.
  main = main.replace(/(<section\b[^>]*>)(\s*<h[23]\b[^>]*>([\s\S]*?)<\/h[23]>)/g,
    (whole, tag, heading, title) => {
      if (!/\b(?:lw-content-block|lw-ref-block|lw-ref-workplace|step)\b/.test(tag) || tag.includes('data-private')) return whole;
      const label = plain(title);
      return mark(tag, slug(label), label) + heading;
    });
  main = main.replace(/<figure\b[^>]*>[\s\S]*?<\/figure>/g, figure => {
    const image = figure.match(/\bhref="bild-([a-z0-9-]+)\.html"/);
    if (!image) return figure;
    return figure.replace(/^<figure\b[^>]*>/, tag => mark(tag, 'bild-' + image[1], 'Bild in der Aufgabe'));
  });
  // Der Anker gehört zur Beschriftung. Der Rücksprung fokussiert kein Eingabefeld.
  let currentBlock = 'Deine Antwort';
  return main.replace(/<section\b[^>]* data-arbeitsstelle>|<label\b[^>]*\bfor="answer-([a-z0-9-]+)"[^>]*>/g,
    (tag, field) => {
      if (field) return mark(tag, field, currentBlock);
      currentBlock = registered[tag.match(/\bid="([^"]+)"/)[1]];
      return tag;
    });
}

function relevant(file) {
  return /^(?:(?:schritt|baustein|bild|hilfe)-[a-z0-9-]+|wissen|material|index|quellen|leas-weg-[a-z0-9-]+)\.html$/.test(file);
}

function addArbeitsstellen(source) {
  const pages = new Map(source);
  const controller = fs.readFileSync(path.join(__dirname, 'arbeitsstellen.js'), 'utf8');
  const style = fs.readFileSync(path.join(__dirname, 'arbeitsstellen.css'), 'utf8');
  for (const root of ['klasse5/', 'klasse6/']) {
    const origins = {};
    for (const [name, original] of source) {
      if (!name.startsWith(root)) continue;
      const relative = name.slice(root.length);
      const match = /^([a-z0-9-]+)\/([a-z0-9-]+\.html)$/.exec(relative);
      if (!match || !relevant(match[2]) || !original.includes('class="lw-shell-header"')) continue;
      const file = match[2];
      let html = original;
      if (file.startsWith('schritt-') || (file === 'index.html' && /<section class="step" id="/.test(html))) {
        const places = {};
        html = html.replace(/<main\b[^>]*>[\s\S]*?<\/main>/, main => markWorkplaces(main, places));
        if (Object.keys(places).length) origins[relative] = places;
      }
      const assets = '<link rel="stylesheet" href="../arbeitsstellen.css"><script src="../arbeitsstellen.js" defer></script>';
      pages.set(name, html.replace('</head>', assets + '</head>'));
    }
    pages.set(root + 'arbeitsstellen.css', style);
    pages.set(root + 'arbeitsstellen.js', controller.replace('/* PUBLIC_ORIGINS */ {}', () => JSON.stringify(origins)));
    refreshWorker(pages, root, ['arbeitsstellen.css', 'arbeitsstellen.js']);
  }
  return pages;
}

module.exports = { addArbeitsstellen };
