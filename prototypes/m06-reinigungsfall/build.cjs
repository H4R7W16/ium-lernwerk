const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

// Explicit public files: no workspace notes, test evidence or build dependencies.
const files = ['index.html', 'reinigungsfall.html', 'prueffahrt.html', 'style.css',
  'reinigungsfall.css', 'reinigungsfall-core.js', 'reinigungsfall.js', 'prototype.js',
  'README.md', 'sw.js'];
const output = path.resolve(__dirname, '../../dist/reinigungsfall-pages');
if (fs.existsSync(output)) throw new Error('Build output exists; use a fresh checkout for publishing.');
for (const name of files) {
  const source = fs.readFileSync(path.join(__dirname, name), 'utf8');
  if (/C:[\\/]Users[\\/]|\.\.\/.*Vault\//i.test(source)) throw new Error(`Private path in ${name}`);
  if (name.endsWith('.js')) execFileSync(process.execPath, ['--check', path.join(__dirname, name)]);
  if (name.endsWith('.html')) {
    for (const [, url] of source.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (url.startsWith('#') || /^https?:/.test(url)) continue;
      if (!files.includes(url.split('#')[0])) throw new Error(`Unpublished link ${name}: ${url}`);
    }
  }
}
fs.mkdirSync(output, { recursive: true });
for (const name of files) fs.copyFileSync(path.join(__dirname, name), path.join(output, name));
console.log(`Validated and staged ${files.length} public files in ${output}`);
