'use strict';

const assert = require('node:assert/strict');

// Die Quellenprüfung vergleicht den Lesetext einschließlich seiner ursprünglichen Verweise.
// Ausgenommen sind nur die ausdrücklich gekennzeichneten Navigationszusätze dieser Ausgabe.
function readingContent(main) {
  if (main == null) return main;
  return main
    .replace(/<(nav|p|span)\b[^>]*\bdata-(?:task-routes|year-material)(?=[\s=>])[^>]*>[\s\S]*?<\/\1>/g, '')
    .replace(/<[\w-]+\b[^>]*>/g, restoreAttributes)
    .replace(/>\s+</g, '><')
    .trim();
}

function restoreAttributes(tag) {
  const originalHref = tag.match(/\sdata-(?:task|year)-original-href="([^"]+)"/);
  if (originalHref) {
    tag = tag.replace(originalHref[0], '').replace(/\shref="[^"]*"/, () => ' href="' + originalHref[1] + '"');
  }
  if (/\sdata-task-anchor="true"/.test(tag)) {
    tag = tag.replace(/\sdata-task-anchor="true"/, '').replace(/\sid="[^"]+"/, '');
  }
  return tag.replace(/\sdata-year-material-link="[^"]+"/, '');
}

function assertReadingContent(actual, expected, file) {
  if (actual === expected) return;
  assert.equal(readingContent(actual), readingContent(expected), file);
}

module.exports = { assertReadingContent };
