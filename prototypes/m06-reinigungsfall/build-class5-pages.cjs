'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { prepare } = require('./build.cjs');

const rootIndex = '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=klasse5/"><title>IuM Lernwerk · Klasse 5</title></head><body><p><a href="klasse5/">IuM Lernwerk für Klasse 5 öffnen</a></p></body></html>';

function prepareClass5Pages() {
  const all = prepare();
  const assets = new Map([
    ['index.html', rootIndex],
    ['sw.js', all.get('sw.js')],
  ]);
  for (const [name, source] of all) if (name.startsWith('klasse5/')) assets.set(name, source);
  if (!assets.get('sw.js')?.includes('registration.unregister()')) throw new Error('Alter Pages-Service-Worker wird nicht abgelöst.');
  if (!assets.has('klasse5/index.html')) throw new Error('Klasse-5-Einstieg fehlt.');
  for (const [name, source] of assets) {
    if (!name.endsWith('.html')) continue;
    for (const [, reference] of source.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (/^(?:https?:|mailto:|tel:|data:|#)/i.test(reference)) continue;
      const target = new URL(reference, 'https://example.test/ium-lernwerk/' + name);
      if (!target.pathname.startsWith('/ium-lernwerk/')) throw new Error(`${name}: externer Pages-Pfad ${reference}`);
      const local = decodeURIComponent(target.pathname.slice('/ium-lernwerk/'.length));
      const file = local.endsWith('/') ? local + 'index.html' : local;
      if (!assets.has(file)) throw new Error(`${name}: unveröffentlichter Link ${reference}`);
    }
  }
  return assets;
}

function build(output = path.resolve(__dirname, '../../dist/klasse5-pages')) {
  if (fs.existsSync(output)) throw new Error('Buildausgabe existiert bereits; frisches Ziel wählen.');
  const assets = prepareClass5Pages();
  for (const [name, source] of assets) {
    const destination = path.join(output, name);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, source);
  }
  console.log(`Validated and staged ${assets.size} Klasse-5-Pages-Dateien in ${output}`);
}
if (require.main === module) build(process.argv[2] ? path.resolve(process.argv[2]) : undefined);
module.exports = { prepareClass5Pages, build };
