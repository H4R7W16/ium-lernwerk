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
const currentDir = path.resolve(__dirname, '../m06-reinigungsfall-v2');

function prepare() {
  const assets = new Map();
  assets.set('index.html', fs.readFileSync(path.join(currentDir, 'pages-entry.html'), 'utf8'));
  for (const name of legacy) assets.set(name, fs.readFileSync(path.join(__dirname, name), 'utf8'));
  for (const name of current) {
    const source = fs.readFileSync(path.join(currentDir, name), 'utf8')
      .replaceAll('../m06-reinigungsfall/reinigungsfall.html', '../reinigungsfall.html')
      .replaceAll('../m06-selbstlernen/index.html', '../selbstlernen/index.html');
    assets.set(`reinigungsfall-v2/${name}`, source);
  }
  assets.set('selbstlernen/index.html', require('../m06-selbstlernen/render.cjs').render().replaceAll('../m06-reinigungsfall-v2/index.html', '../reinigungsfall-v2/index.html'));
  assets.set('selbstlernen/read.html', require('../m06-selbstlernen/render.cjs').renderReading().replaceAll('../m06-reinigungsfall-v2/index.html', '../reinigungsfall-v2/index.html'));
  for (const name of selfFiles) assets.set('selbstlernen/' + name, fs.readFileSync(path.join(selfDir, name), 'utf8'));
  for (const [name, source] of assets) {
    if (/C:[\\/]Users[\\/]|\.\.\/.*Vault\//i.test(source)) throw new Error(`Private path in ${name}`);
    if (name.endsWith('.html')) {
      for (const [, url] of source.matchAll(/(?:href|src)="([^"]+)"/g)) {
        if (url.startsWith('#') || /^https?:/.test(url)) continue;
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
  for (const dir of [__dirname, currentDir, selfDir]) {
    const names = dir === __dirname ? legacy : dir === selfDir ? selfFiles : current;
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
