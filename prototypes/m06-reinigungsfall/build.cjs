const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

// Only these files are published. Tests, notes and learner data stay out of Pages.
const legacy = ['reinigungsfall.html', 'prueffahrt.html', 'style.css',
  'reinigungsfall.css', 'reinigungsfall-core.js', 'reinigungsfall.js', 'prototype.js',
  'README.md', 'sw.js'];
const current = ['index.html', 'app.css', 'app.js', 'cleaning-core.js', 'lesson-model.js', 'README.md'];
const selfDir = path.resolve(__dirname, '../m06-selbstlernen');
const selfFiles = ['app.css', 'app.js', 'model.js', 'cleaning-core.js'];
const thirdDir = path.resolve(__dirname, '../m06-lernfassung3');
const thirdFiles = ['journey.css','journey.js','journey-model.js'];
const publicLinks = source => source.replaceAll('../m06-reinigungsfall-v2/index.html','../reinigungsfall-v2/index.html').replaceAll('../m06-selbstlernen/', '../selbstlernen/').replaceAll('../m06-lernfassung3/index.html','../lernfassung-3/index.html').replaceAll('../m06-lernwerkstatt/', '../lernwerkstatt/').replaceAll('../m06-lernstudio/', '../lernstudio/').replaceAll('../m05-medienanalyse/', '../medienanalyse/').replaceAll('../m02-quellenquest/', '../quellenquest/');
const workshopDir = path.resolve(__dirname, '../m06-lernwerkstatt');
const workshopFiles = ['index.html','workshop.css','workshop.js','workshop-model.js'];
const studioDir = path.resolve(__dirname, '../m06-lernstudio');
const studioFiles = ['index.html','studio.css','prototype.css','studio.js','studio-model.js','studio-learning.js'];
const mediaDir = path.resolve(__dirname, '../m05-medienanalyse');
const mediaFiles = ['index.html','app.js','content.js','model.js','style.css'];
const questDir = path.resolve(__dirname, '../m02-quellenquest');
const questFiles = ['app.js','content.js','model.js','style.css'];
const currentDir = path.resolve(__dirname, '../m06-reinigungsfall-v2');

function prepare() {
  const assets = new Map();
  assets.set('index.html', fs.readFileSync(path.join(currentDir, 'pages-entry.html'), 'utf8'));
  for (const name of legacy) assets.set(name, fs.readFileSync(path.join(__dirname, name), 'utf8'));
  for (const name of current) {
    const source = fs.readFileSync(path.join(currentDir, name), 'utf8')
      .replaceAll('../m06-reinigungsfall/reinigungsfall.html', '../reinigungsfall.html')
      .replaceAll('../m06-selbstlernen/index.html', '../selbstlernen/index.html')
      .replaceAll('../m06-lernfassung3/index.html', '../lernfassung-3/index.html').replaceAll('../m06-lernwerkstatt/index.html','../lernwerkstatt/index.html');
    assets.set(`reinigungsfall-v2/${name}`, source);
  }
  assets.set('selbstlernen/index.html', publicLinks(require('../m06-selbstlernen/render.cjs').render()));
  assets.set('selbstlernen/read.html', publicLinks(require('../m06-selbstlernen/render.cjs').renderReading()));
  for (const name of selfFiles) assets.set('selbstlernen/' + name, fs.readFileSync(path.join(selfDir, name), 'utf8'));
  assets.set('lernfassung-3/index.html', publicLinks(require('../m06-lernfassung3/render.cjs').render()));
  assets.set('lernfassung-3/read.html', publicLinks(require('../m06-lernfassung3/render.cjs').renderReading()));
  for (const name of thirdFiles) assets.set('lernfassung-3/' + name, fs.readFileSync(path.join(thirdDir,name),'utf8'));
  for (const name of workshopFiles) assets.set('lernwerkstatt/' + name, publicLinks(fs.readFileSync(path.join(workshopDir,name),'utf8')));
  for (const name of studioFiles) assets.set('lernstudio/' + name, publicLinks(fs.readFileSync(path.join(studioDir,name),'utf8')));
  assets.set('lernstudio/wissen.html', require('../m06-lernstudio/studio-guides.cjs').render());
  assets.set('lernstudio/lehrkraft.html', require('../m06-lernstudio/studio-guides.cjs').render(true));
  for (const name of mediaFiles) assets.set('medienanalyse/' + name, publicLinks(fs.readFileSync(path.join(mediaDir,name),'utf8')));
  for (const name of ['schulfest.png','bibliothek.png']) assets.set('medienanalyse/assets/' + name, fs.readFileSync(path.join(mediaDir,'assets',name)));
  const mediaGuides = require('../m05-medienanalyse/guides.cjs');
  assets.set('medienanalyse/wissen.html', mediaGuides.renderKnowledge());
  assets.set('medienanalyse/lehrkraft.html', mediaGuides.renderTeacher());
  assets.set('medienanalyse/material.html', mediaGuides.renderMaterials());
  for (const step of require('../m05-medienanalyse/content.js').steps) assets.set('medienanalyse/baustein-' + step.id + '.html', mediaGuides.renderMaterials(step.id));
  const quest = require('../m02-quellenquest/render.cjs');
  assets.set('quellenquest/index.html', quest.index());
  assets.set('quellenquest/wissen.html', quest.knowledge());
  assets.set('quellenquest/lehrkraft.html', quest.teacher());
  assets.set('quellenquest/material.html', quest.material());
  for (const step of require('../m02-quellenquest/content.js').steps) assets.set('quellenquest/baustein-' + step.id + '.html', quest.material(step.id));
  for (const name of questFiles) assets.set('quellenquest/' + name, fs.readFileSync(path.join(questDir,name),'utf8'));
  assets.set('prototype-navigation.css', fs.readFileSync(path.resolve(__dirname, '../shared/prototype-navigation.css'),'utf8'));
  const navigation = require('../shared/prototype-navigation.cjs');
  for (const [name, source] of assets) {
    const area = name.split('/')[0];
    if (name.endsWith('.html') && ['lernstudio','medienanalyse','quellenquest'].includes(area)) assets.set(name, navigation.inject(source,area,name));
  }
  require('../shared/mantel-render.cjs').augment(assets);
  require('../shared/class6-render.cjs').augment(assets);
  for (const [name, source] of assets) {
    if (Buffer.isBuffer(source)) continue;
    if (/C:[\\/]Users[\\/]|\.\.\/.*Vault\//i.test(source)) throw new Error(`Private path in ${name}`);
    if (name.endsWith('.html')) {
      for (const [, url] of source.matchAll(/(?:href|src)="([^"]+)"/g)) {
        if (url.startsWith('#') || /^(?:https?:|mailto:)/i.test(url)) continue;
        const relative = url.split('#')[0];
        const target = path.posix.normalize(path.posix.join(path.posix.dirname(name), relative.endsWith('/') ? `${relative}index.html` : relative));
        if (!assets.has(target)) throw new Error(`Unpublished link ${name}: ${url}`);
      }
    }
  }
  return assets;
}
function build(output = path.resolve(__dirname, '../../dist/reinigungsfall-pages')) {
  if (fs.existsSync(output)) throw new Error('Build output exists; use a fresh output directory for publishing.');
  const assets = prepare();
  for (const dir of [__dirname, currentDir, selfDir, thirdDir, workshopDir, studioDir, mediaDir, questDir]) {
    const names = dir === __dirname ? legacy : dir === selfDir ? selfFiles : dir === thirdDir ? thirdFiles : dir === workshopDir ? workshopFiles : dir === studioDir ? studioFiles : dir === mediaDir ? mediaFiles : dir === questDir ? questFiles : current;
    for (const name of names.filter(n => n.endsWith('.js'))) execFileSync(process.execPath, ['--check', path.join(dir, name)]);
  }
  for (const [name, source] of assets) {
    const destination = path.join(output, name);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, source);
  }
  console.log(`Validated and staged ${assets.size} public files in ${output}`);
}
if (require.main === module) build(process.argv[2] ? path.resolve(process.argv[2]) : undefined);
module.exports = { prepare, build };
