'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { units, isProjection, regularNavigation, projectionNavigation } = require('./kopfzeile.cjs');

const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

function addYearRoutes(source) {
  const all = new Map(source);
  const manifest = require('./quelle-sha256.json');
  for (const [file, hash] of Object.entries(manifest.files)) {
    const bytes = fs.readFileSync(path.join(__dirname, file));
    if (sha(bytes) !== hash) throw Error('Ungebundene Jahresquelle: ' + file);
    if (file.startsWith('inhalt/')) {
      all.set('klasse7/' + file.slice(7), /\.(html|txt)$/.test(file) ? bytes.toString('utf8') : bytes);
    }
  }
  for (const asset of ['jahreswege.css', 'jahrgang-gamepad.svg', 'kopfzeile.css']) {
    all.set('klasse7/' + asset, fs.readFileSync(path.join(__dirname, asset), 'utf8'));
  }
  for (const [name, original] of all) {
    if (!name.startsWith('klasse7/') || !name.endsWith('.html') || name.startsWith('klasse7/programmieren/snap/')) continue;
    const oldHeader = original.match(/<header\b[^>]*>[\s\S]*?<\/header>/)?.[0];
    if (!oldHeader) continue;
    const ref = target => path.posix.relative(path.posix.dirname(name), 'klasse7/' + target);
    const projection = isProjection(name, original);
    const hasLocalMaterials = original.includes('<!--year-plan-->');
    const navigation = projection ? projectionNavigation(name, oldHeader, ref) : regularNavigation(name, oldHeader, ref, hasLocalMaterials);
    let sheets = '<link rel="stylesheet" href="' + ref('jahreswege.css') + '">';
    if (!projection) sheets += '<link rel="stylesheet" href="' + ref('kopfzeile.css') + '">';
    let html = original.replace(oldHeader, navigation)
      .replace('</head>', sheets + '</head>')
      .replace('Lehrmaterial auswählen', 'Material für Lehrpersonen');
    if (hasLocalMaterials) {
      const teacherLink = '<a href="' + ref('lehrpersonen.html') + '">Jahresplanung und Übergänge</a>';
      html = html.replace('<!--year-plan-->', projection ? teacherLink : '');
    }
    // Die alte Adresse verweist auf den aktuellen Jahresleitfaden.
    if (name === 'klasse7/programmieren/lehrpersonen/jahrgang.html') {
      html = html.replace(/<main\b[^>]*>[\s\S]*?<\/main>/, '<main id="main" class="year-legacy"><h1>Jahresplanung für IuM 7</h1><p>Die aktuelle gemeinsame Planung verbindet alle vier Lernbögen, die Eingangsdiagnose und die 90 Minuten spätere Wiederaufnahme.</p><p><a href="' + ref('lehrpersonen.html') + '">Jahresleitfaden mit Durchführung und Materialzugängen öffnen</a></p><p><a href="' + ref('lernziele.html') + '">29 Lernziele und Nachweise</a> · <a href="' + ref('briefing.html') + '">Jahrgangsbriefing</a></p></main>');
    }
    if (name === 'klasse7/programmieren/index.html') {
      html = html.replace('Aufgabenfassung 2.0 vom 25.10.2026', 'Aufgabenfassung 2.2 vom 27.10.2026');
    }
    all.set(name, html);
  }
  return all;
}

module.exports = { addYearRoutes, units };
