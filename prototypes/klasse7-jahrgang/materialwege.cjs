'use strict';

// Pfade innerhalb des Jahrgangs. Die Durchführung enthält Aufgaben, Erwartungen und Stundenverläufe.
const yearMaterials = 'lehrpersonen.html#unterrichtsmaterial';
const teachingPlans = {
  medien: 'medienbogen-durchfuhrung-und-auswertung.html',
  daten: 'datenbogen-durchfuhrung-und-auswertung.html',
  gaming: 'gamingbogen-durchfuhrung-und-auswertung.html',
};

function materialTarget(area) {
  if (area === 'programmieren') return 'programmieren/index.html#lehrpersonen';
  return teachingPlans[area] ? area + '/' + teachingPlans[area] : yearMaterials;
}

function currentPage(pages, file) {
  const html = pages.get('klasse7/' + file);
  if (typeof html !== 'string') throw Error('Seite für Unterrichtsmaterial fehlt: ' + file);
  return html;
}

function yearLink() {
  return '<nav class="year-material-routes" data-year-material="jahrgang" aria-label="Weitere Unterrichtsmaterialien">'
    + '<a href="../' + yearMaterials + '">Material für alle vier Lernbögen</a></nav>';
}

function addYearLink(pages, area) {
  const file = materialTarget(area).split('#')[0];
  const html = currentPage(pages, file);
  const heading = area === 'programmieren' ? /<h2 id="lehrpersonen-titel">[^<]*<\/h2>/ : /<h1\b[^>]*>[^<]*<\/h1>/;
  if (!heading.test(html)) throw Error('Materialüberschrift fehlt: ' + file);
  pages.set('klasse7/' + file, html.replace(heading, match => match + yearLink()));
}

function briefingLinks(lesson) {
  return '<a href="' + lesson.task + '">Lernaufgabe ' + lesson.id + '</a> · '
    + '<a href="' + lesson.plan + '#' + lesson.section + '">Stundenverlauf ' + lesson.id + '</a>';
}

function attachBriefing(pages, file, lesson) {
  const html = currentPage(pages, file);
  const main = html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)?.[0];
  if (!main) throw Error('Vorlesetext fehlt: ' + file);
  const oldPlanLink = 'href="' + lesson.plan + '"';
  if (!main.includes(oldPlanLink)) {
    // Die Daten-Briefings enthalten nur den Vorlesetext. Die Links stehen außerhalb davon.
    const nav = '<nav class="year-material-routes" data-year-material="briefing" aria-label="Unterricht zu ' + lesson.id + '">'
      + briefingLinks(lesson) + '</nav>';
    pages.set('klasse7/' + file, html.replace(main, () => main + nav));
    return;
  }

  // Vorhandenen Anhang nutzen, insbesondere die Lernaufgabe und die Bedienkarte in MED-3 erhalten.
  const planHref = 'href="' + lesson.plan + '#' + lesson.section + '" data-year-material-link="verlauf"'
    + ' data-year-original-href="' + lesson.plan + '"';
  const hasTask = main.includes('href="' + lesson.task + '"');
  const appendix = main.replace(/<p\b[^>]*>[\s\S]*?<\/p>/g, paragraph => {
    if (!paragraph.includes(oldPlanLink)) return paragraph;
    const linked = paragraph.replace(/<a href="([^"]+)">([^<]+)<\/a>/g, (link, href, label) => {
      if (href !== lesson.plan) return link;
      const suffix = label.includes(lesson.id) ? '' : '<span data-year-material="stunde"> · ' + lesson.id + '</span>';
      return '<a ' + planHref + '>' + label + suffix + '</a>';
    });
    if (hasTask) return linked;
    const task = '<span data-year-material="aufgabe"> · <a href="' + lesson.task + '">Lernaufgabe ' + lesson.id + '</a></span>';
    return linked.replace(/(\.?)<\/p>$/, (_, period) => task + period + '</p>');
  });
  if (appendix === main) throw Error('Stundenverlauf steht außerhalb des erwarteten Briefing-Anhangs: ' + file);
  pages.set('klasse7/' + file, html.replace(main, () => appendix));
}

function attachUnitBriefings(pages, area, prefix, count) {
  const plan = teachingPlans[area];
  const html = currentPage(pages, area + '/' + plan);
  // Der Stundenplan führt die jeweilige Lernaufgabe direkt unter ihrer Abschnittsüberschrift.
  const sections = [...html.matchAll(/<h2 id="([^"]+)">[\s\S]*?(?=<h2\b|<\/main>)/g)];
  for (let number = 1; number <= count; number++) {
    const key = prefix + '-' + number;
    const section = sections.find(item => item[1].startsWith(key + '-'));
    const task = section && [...section[0].matchAll(/<a href="([^"#]+\.html)"/g)]
      .map(match => match[1])
      .find(href => href.startsWith(key + '-') && !href.includes('-bedienkarte-') && !href.endsWith('-briefing.html'));
    if (!task) throw Error('Lernaufgabe im Stundenverlauf fehlt: ' + key);
    currentPage(pages, area + '/' + task);
    attachBriefing(pages, area + '/' + key + '-briefing.html', { id: key.toUpperCase(), task, plan, section: section[1] });
  }
}

function programmingLessons(pages) {
  const lessons = [];
  for (let number = 1; number <= 6; number++) {
    const key = 'alg-' + number;
    const plan = number === 6 ? 'durchfuehrung-256.html' : key + '-durchfuehrung.html';
    const html = currentPage(pages, 'programmieren/lehrpersonen/' + plan);
    const heading = number === 6 ? 'ALG-6' : 'Verlauf';
    const jump = [...html.matchAll(/<a href="#([^"]+)">([^<]+)<\/a>/g)].find(match => match[2].startsWith(heading));
    if (!jump || !html.includes('id="' + jump[1] + '"')) throw Error('Verlaufsabschnitt fehlt: ' + key);
    const taskFile = 'programmieren/lernende/' + key + '.html';
    currentPage(pages, taskFile);
    lessons.push({ id: key.toUpperCase(), plan, section: jump[1], task: '../lernende/' + key + '.html' });
  }
  return lessons;
}

// Derselbe Materiallink steht in der breiten Vergleichstabelle oder in einer Zeile
// des Lernbogens. Die sichtbaren Feldnamen stammen aus den tatsächlichen Spaltenköpfen.
function adaptMaterialTable(pages) {
  const file = 'lehrpersonen.html';
  const html = currentPage(pages, file);
  const section = /(<h2 id="unterrichtsmaterial">[^<]*<\/h2>\s*)<div class="table-wrap"[^>]*>(<table>[\s\S]*?<\/table>)<\/div>/;
  if (!section.test(html)) throw Error('Materialübersicht fehlt im Jahresleitfaden.');
  const adapted = html.replace(section, (_, heading, table) => {
    const labels = [...table.matchAll(/<th\b[^>]*>([^<]+)<\/th>/g)].map(match => match[1]);
    const rows = table.replace(/<tbody>([\s\S]*?)<\/tbody>/, (_, body) => {
      return '<tbody role="rowgroup">' + body.replace(/<tr>([\s\S]*?)<\/tr>/g, (_, row) => {
        let column = 0;
        const cells = row.replace(/<td\b[^>]*>([\s\S]*?)<\/td>/g, (_, content) => {
          const index = column++;
          if (index === 0) return '<th scope="row" role="rowheader">' + content + '</th>';
          return '<td role="cell"><span class="year-material-label" aria-hidden="true">'
            + labels[index] + '</span>' + content + '</td>';
        });
        if (column !== labels.length) throw Error('Unvollständige Zeile der Materialübersicht.');
        return '<tr role="row">' + cells + '</tr>';
      }) + '</tbody>';
    });
    const accessible = rows.replace('<table>', '<table role="table" aria-labelledby="unterrichtsmaterial">')
      .replace('<thead>', '<thead role="rowgroup">').replace('<tr>', '<tr role="row">')
      .replace(/<th(?! scope="row")\b([^>]*)>/g, '<th scope="col" role="columnheader"$1>');
    return heading + '<div class="table-wrap year-material-table">' + accessible + '</div>';
  });
  pages.set('klasse7/' + file, adapted);
}

function addMaterialRoutes(pages) {
  adaptMaterialTable(pages);
  for (const area of [...Object.keys(teachingPlans), 'programmieren']) addYearLink(pages, area);
  attachUnitBriefings(pages, 'medien', 'med', 5);
  attachUnitBriefings(pages, 'daten', 'dat', 5);
  attachUnitBriefings(pages, 'gaming', 'gam', 6);
  const lessons = programmingLessons(pages);
  // ALG-1 bis ALG-5 haben Einzelbriefings, ALG-6 steht im gemeinsamen Hörbriefing.
  for (const lesson of lessons.slice(0, 5)) {
    attachBriefing(pages, 'programmieren/lehrpersonen/' + lesson.id.toLowerCase() + '-briefing.html', lesson);
  }
  const file = 'programmieren/lehrpersonen/hoerbriefing.html';
  const html = currentPage(pages, file);
  const nav = '<nav class="year-material-routes" data-year-material="briefing" aria-label="Aufgaben und Stundenverläufe">'
    + '<ul>' + lessons.map(lesson => '<li>' + briefingLinks(lesson) + '</li>').join('') + '</ul></nav>';
  pages.set('klasse7/' + file, html.replace('</main>', '</main>' + nav));
  return pages;
}

module.exports = { materialTarget, addMaterialRoutes };
