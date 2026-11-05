'use strict';
const crypto = require('node:crypto');

function expected(baseline, ...revisions) {
 const files = { ...baseline.files };
 for (const revision of revisions) {
  const digest = crypto.createHash('sha256').update(JSON.stringify(files)).digest('hex');
  if (revision.base !== digest) throw Error('Historische Bindung der Prüffassung stimmt nicht');
  for (const [name, change] of Object.entries(revision.changes)) {
   if (name.startsWith('beispiele/') || name.includes('/snap/')) throw Error('Geschützte Ressource in Revision: ' + name);
   if ((files[name] || null) !== change.before || !/^[a-f0-9]{64}$/.test(change.after)) throw Error('Ungebundene Änderung: ' + name);
   files[name] = change.after;
  }
 }
 return { files };
}
module.exports = { expected };
