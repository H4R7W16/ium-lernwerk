'use strict';

const { materialTarget } = require('./materialwege.cjs');

const units = [
  ['medien', 'Medien'],
  ['daten', 'Daten'],
  ['programmieren', 'Programmieren'],
  ['gaming', 'Gaming'],
];

const knowledgePages = {
  medien: 'medien/medienbogen-sicherung.html',
  daten: 'daten/datenbogen-sicherung.html',
  programmieren: 'wissen.html#programmieren',
  gaming: 'gaming/gamingbogen-sicherung.html',
};

function isProjection(name, html) {
  return /(?:^|[/-])projektion(?:-\d+)?\.html$/.test(name)
    || /<(?:body|main)\b[^>]*\bclass="[^"]*\bprojection\b[^"]*"/.test(html);
}

function brand(ref, projection) {
  const breakpoint = projection ? 700 : 760;
  const subtitle = projection ? '' : '<span class="year-brand-subject" aria-hidden="true">Informatik und Medienbildung</span>';
  return '<a class="brand" href="' + ref('index.html') + '" aria-label="IuM Lernwerk Klasse 7">'
    + '<picture><source media="(max-width:' + breakpoint + 'px)" srcset="' + ref('programmieren/brand/ium-lernwerk-7-compact.png') + '">'
    + '<img src="' + ref('programmieren/brand/ium-lernwerk-7.png') + '" width="1308" height="320" alt="IuM Lernwerk 7 – Informatik und Medienbildung"></picture>'
    + subtitle + '</a>';
}

function unitTools(name, oldHeader, knowledgePage) {
  const nav = oldHeader.match(/<nav[^>]*aria-label="Hauptnavigation"[^>]*>([\s\S]*?)<\/nav>/);
  if (!nav) return '';
  const unitsToVisit = units.map(([id]) => 'klasse7/' + id + '/index.html');
  const links = nav[1].match(/<a\b[^>]*>[\s\S]*?<\/a>/g) || [];
  return links.filter(link => {
    const href = link.match(/href="([^"]+)"/)?.[1];
    if (!href) return false;
    const target = new URL(href, 'https://example.test/' + name);
    const file = target.pathname.slice(1);
    return Boolean(target.hash) || (!unitsToVisit.includes(file) && file !== knowledgePage);
  }).join('');
}

function topicLink(name, current, id, target, label, ref) {
  const isCurrentPage = name === 'klasse7/' + target;
  const selected = current === id;
  const status = isCurrentPage ? ' aria-current="page"' : selected ? ' aria-current="true"' : '';
  return '<a' + status + ' href="' + ref(target) + '">' + label + '</a>';
}

function regularNavigation(name, oldHeader, ref, hasLocalMaterials) {
  const unit = units.find(([id]) => name.startsWith('klasse7/' + id + '/'));
  const current = unit?.[0];
  const location = unit ? { target: current + '/index.html', label: unit[1] }
    : { target: 'index.html', label: 'Jahrgang 7' };
  const context = name === 'klasse7/index.html' ? ''
    : '<a class="year-shell-context" href="' + ref(location.target) + '">' + location.label + '</a>';
  const topics = [
    topicLink(name, current, undefined, 'index.html', 'Jahrgangsübersicht', ref),
    ...units.map(([id, label]) => topicLink(name, current, id, id + '/index.html', label, ref)),
  ].join('');
  const knowledge = knowledgePages[current] || 'wissen.html';
  const onKnowledgePage = name === 'klasse7/' + knowledge;
  const header = '<header class="year-header year-shell-header">'
    + '<div class="year-shell-identity">' + brand(ref, false) + context + '</div>'
    + '<nav class="year-shell-nav" aria-label="Lernwerk">'
    + '<details class="year-topics" data-lw-menu><summary>Themen <span aria-hidden="true">▾</span></summary>'
    + '<div class="year-topic-links">' + topics + '</div></details>'
    + '<a' + (onKnowledgePage ? ' aria-current="page"' : '') + ' href="' + ref(knowledge) + '">Wissen</a>'
    + '<a href="' + ref(materialTarget(current)) + '" aria-label="Unterrichtsmaterial">'
    + '<span class="year-nav-full">Unterrichtsmaterial</span><span class="year-nav-short">Material</span></a></nav></header>';
  if (hasLocalMaterials) return header;
  const tools = unitTools(name, oldHeader, 'klasse7/' + knowledge);
  return tools ? header + '<nav class="year-tools" aria-label="Arbeitsmittel im Lernbogen">' + tools + '</nav>' : header;
}

// Projektionsseiten behalten ihre eigene Navigation und die bisherige Markenbreite.
function projectionNavigation(name, oldHeader, ref) {
  const current = units.find(([id]) => name.startsWith('klasse7/' + id + '/'))?.[0];
  const links = [
    ['index.html', 'Jahrgang', !current],
    ...units.map(([id, label]) => [id + '/index.html', label, id === current]),
  ].map(([url, label, active]) =>
    '<a href="' + ref(url) + '"' + (active ? ' aria-current="page"' : '') + '>' + label + '</a>'
  ).join('');
  const yearPlan = '<a href="' + ref('lehrpersonen.html') + '">Jahresplanung und Übergänge</a>';
  return '<header class="year-header">' + brand(ref, true)
    + '<nav class="year-nav" aria-label="Hauptnavigation">' + links + '</nav></header>'
    + '<nav class="year-tools" aria-label="Materialzugänge">' + unitTools(name, oldHeader) + yearPlan + '</nav>';
}

module.exports = { units, isProjection, regularNavigation, projectionNavigation };
