'use strict';

const fs = require('node:fs');
const path = require('node:path');
const {refreshWorker} = require('./grade-navigation.cjs');

const cssFile = 'themen-navigation.css';

function markTopic(link, current) {
  return link.replace('<a ', '<a aria-current="' + current + '" ');
}

function topicHeader(header, area, file, relative) {
  const topic = header.match(/<span class="lw-shell-location"><b>([^<]+)<\/b><\/span>/)?.[1];
  if (topic) {
    const context = '<span class="lw-shell-location"><a href="index.html" aria-label="Themenübersicht: ' + topic + '">' + topic + '</a></span>';
    header = header.replace(/<span class="lw-shell-location"><b>[^<]+<\/b><\/span>/, context);
  }
  header = header.replace('media="(max-width: 760px)"', 'media="(max-width: 1050px)"');
  return header.replace(/(<div class="lw-shell-topics">)([\s\S]*?)(<button\b)/, (_, start, topics, close) => {
    let overview = '<a href="' + relative('index.html') + '"><strong>Jahrgangsübersicht</strong></a>';
    if (!area) overview = markTopic(overview, file === 'index.html' ? 'page' : 'true');
    if (area && topic) {
      const target = relative(area + '/index.html');
      const current = file === 'index.html' ? 'page' : 'true';
      const anchor = '<a href="' + target + '">';
      let listed = false;
      topics = topics.replace(/<a href="([^"]+)">/g, (link, href) => {
        if (path.posix.normalize(area + '/' + href) !== area + '/index.html') return link;
        listed = true;
        return markTopic(link, current);
      });
      if (!listed) {
        // Zusatzwerkstätten stehen nur in ihrem eigenen Menü neben den regulären Themen.
        topics += markTopic(anchor + '<strong>' + topic + '</strong><small>Zusätzliche Werkstatt</small></a>', current);
      }
    }
    return start + overview + topics + close;
  });
}

function labelTopicCards(html) {
  return html.replace(/<article class="lw-card"[^>]*>[\s\S]*?<\/article>/g, card => {
    const topic = card.match(/<span class="lw-card-number">\d+ · ([^<]+)<\/span>/)?.[1];
    if (!topic) return card;
    return card.replace('>Lerneinheit öffnen →</a>', '>„' + topic + '“ öffnen →</a>')
      .replace('>Wissen öffnen →</a>', '>Wissen: „' + topic + '“ →</a>')
      .replace('>Material öffnen →</a>', '>Material: „' + topic + '“ →</a>');
  });
}

function prioritizeHome(html, grade) {
  const first = grade === 'klasse5';
  const href = first ? 'geraete/schritt-auftakt.html' : 'jahresstart.html';
  const label = first ? 'Hier beginnen' : 'Gemeinsam starten';
  const lead = first
    ? 'Zum ersten Mal hier? Beginne mit Mias Schulgerät. Wenn ihr schon an einem Thema arbeitet, wähle es direkt aus.'
    : 'Beginnt ihr das Schuljahr gemeinsam? Öffne den Jahresstart. Arbeitet ihr schon an einem Thema, wähle es direkt aus.';
  const actions = '<nav class="lw-home-actions" aria-label="Dein Einstieg">'
    + '<a class="lw-button" href="' + href + '">' + label + ' →</a>'
    + '<a class="lw-button secondary" href="#themen">Thema auswählen ↓</a></nav>';
  const recall = first ? '' : '<p class="lw-home-recall"><a href="wiederholen.html">Vereinbarte Wiederaufnahme finden →</a></p>';
  const overview = html.match(/<div class="lw-home-intro">[\s\S]*?(<p class="lw-lead">[\s\S]*?<\/p>)/)?.[1] || '';
  const orientation = first ? '<p>Die zusätzlichen Werkstätten sind bei ihrer Reihe gekennzeichnet.</p>'
    : '<p>Bei einer vereinbarten Wiederaufnahme nennt dir deine Lehrperson den passenden Fall.</p>';
  // Das Gesamtkonzept bleibt im Lehrpersoneneinstieg. Die Seite beginnt mit dem Lernweg.
  return html.replace(/<nav class="lw-reading-links" aria-label="Gesamtreihe">[\s\S]*?<\/nav>/, '')
    .replace(/(<div class="lw-home-intro">[\s\S]*?<\/h1>)[\s\S]*?<\/div>/,
      (_, title) => title + '<p class="lw-lead">' + lead + '</p>' + actions + recall + '</div>')
    .replace(/<section class="lw-entry-guide"[^>]*>[\s\S]*?<\/section>/, '')
    .replace(/(<section id="themen"[^>]*>[\s\S]*?)(<div class="lw-grid">)/,
      (_, topics, cards) => topics + overview + orientation + cards);
}

function quietReadingStatus(html, workHref) {
  // Der vorhandene dynamische Status bleibt bei einer Warnung neben der Soforthilfe vor dem Inhalt.
  // Im normalen Lernweg genügt der Zugang zur Sicherung am Ende der Seite.
  const note = '<p class="lw-end-work"><a href="' + workHref + '">Deine Arbeit weiterführen und sichern →</a></p>';
  return html.replace('class="lw-state-status" id="lw-storage-status"', 'class="lw-state-status lw-routine-status" id="lw-storage-status"')
    .replace('</main>', '</main>' + note);
}

function startWithNetCase(html) {
  const context = html.match(/<aside class="lw-notice lw-year-context">[\s\S]*?<\/aside>/)?.[0];
  if (!context) return html;
  // Erst die eigene Vermutung, danach der Rückblick auf die gemeinsame Eingangsklärung.
  return html.replace(context, '').replace(/<section class="lw-content-block lw-block-task">[\s\S]*?<\/section>/,
    firstTask => firstTask + context);
}

function addTopicNavigation(source) {
  const pages = new Map(source);
  const css = fs.readFileSync(path.join(__dirname, cssFile), 'utf8');
  for (const [name, original] of source) {
    const page = name.match(/^(klasse[56])\/(?:([^/]+)\/)?([^/]+\.html)$/);
    if (!page || /projektion(?:-\d+)?\.html$/.test(name) || !original.includes('<header class="lw-shell-header">')) continue;
    const [, grade, area, file] = page;
    const relative = target => path.posix.relative(path.posix.dirname(name), grade + '/' + target);
    let html = original.replace(/<header class="lw-shell-header">[\s\S]*?<\/header>/, header => topicHeader(header, area, file, relative));
    html = html.replace('</head>', '<link rel="stylesheet" href="' + relative(cssFile) + '"></head>');
    if (!area && ['index.html', 'material.html', 'wissen.html'].includes(file)) html = labelTopicCards(html);
    if (!area && file === 'index.html') html = prioritizeHome(html, grade);
    if (area || file !== 'arbeit.html') html = quietReadingStatus(html, relative('arbeit.html'));
    if (name === 'klasse6/netze/schritt-einstieg.html') html = startWithNetCase(html);
    if (area && file === 'material.html') {
      const back = '<nav class="lw-reading-links" aria-label="Material im Jahrgang"><a href="' + relative('material.html') + '">← Alle Unterrichtsmaterialien</a></nav>';
      html = html.replace(/<h1\b[^>]*>[\s\S]*?<\/h1>/, heading => heading + back);
    }
    if (name === 'klasse6/jahresstart.html') {
      const next = '<section class="lw-notice"><h2>Nach dem gemeinsamen Start</h2><p>Wenn ihr mit Netzen und Speichern beginnt, öffnet die erste Aufgabe.</p><a href="netze/schritt-einstieg.html">Zur ersten Netzaufgabe: Eine Datei, mehrere Fragen →</a></section>';
      html = html.replace('<details class="lw-year-solutions">', next + '<details class="lw-year-solutions">');
    }
    pages.set(name, html);
  }
  for (const grade of ['klasse5/', 'klasse6/']) {
    pages.set(grade + cssFile, css);
    refreshWorker(pages, grade, [cssFile]);
  }
  return pages;
}

module.exports = {addTopicNavigation};
