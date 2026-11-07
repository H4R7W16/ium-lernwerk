(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LernwerkSnapProjectModel = factory();
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  var MAX_PROJECT_BYTES = 10 * 1024 * 1024;
  function fail(message) { throw new Error(message); }
  function bytes(value) { return typeof TextEncoder !== 'undefined' ? new TextEncoder().encode(value).length : unescape(encodeURIComponent(value)).length; }
  function validCodePoint(value) { return value === 9 || value === 10 || value === 13 || (value >= 32 && value <= 0xD7FF) || (value >= 0xE000 && value <= 0xFFFD) || (value >= 0x10000 && value <= 0x10FFFF); }
  function entities(value) {
    if (/&(?!(?:amp|lt|gt|apos|quot|#[0-9]+|#x[0-9a-fA-F]+);)/.test(value)) fail('Die XML-Datei enthält eine ungültige Zeichenreferenz.');
    value.replace(/&#(x[0-9a-fA-F]+|[0-9]+);/g, function (_, number) { if (!validCodePoint(number[0] === 'x' ? parseInt(number.slice(1), 16) : Number(number))) fail('Die XML-Datei enthält ein ungültiges Zeichen.'); return _; });
  }
  function attributes(value) {
    var pos = 0, names = new Set(), expression = /\s+([A-Za-z_:][A-Za-z0-9_.:-]*)\s*=\s*(?:"([^"<]*)"|'([^'<]*)')/y;
    while (pos < value.length) {
      if (/^\s*$/.test(value.slice(pos))) break;
      expression.lastIndex = pos; var match = expression.exec(value);
      if (!match || names.has(match[1])) fail('Die XML-Datei enthält ungültige oder doppelte Eigenschaften.');
      names.add(match[1]); entities(match[2] === undefined ? match[3] : match[2]); pos = expression.lastIndex;
    }
  }
  // Only structural XML validation. Snap itself must load the project before offering editing.
  // No parser executes XML, resolves entities, fetches files or judges program correctness.
  function xmlStructure(xml) {
    if (typeof xml !== 'string' || !xml.trim()) fail('Der Projektstand enthält keine XML-Datei.');
    if (bytes(xml) > MAX_PROJECT_BYTES) fail('Der Projektstand ist größer als 10 MiB. Sichere ihn als einzelne XML-Datei.');
    if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f\uD800-\uDFFF\uFFFE\uFFFF]/u.test(xml)) fail('Die XML-Datei enthält ein ungültiges Zeichen.');
    if (/<!DOCTYPE|<!ENTITY/i.test(xml)) fail('Diese XML-Datei enthält nicht unterstützte Angaben.');
    var source = xml.trim(), pos = 0, stack = [], rootSeen = false, rootClosed = false, stage = false, count = 0;
    while (pos < source.length) {
      if (source.slice(pos, pos + 4) === '<!--') {
        var end = source.indexOf('-->', pos + 4);
        if (end < 0 || /--|-$/.test(source.slice(pos + 4, end))) fail('Die XML-Datei enthält einen ungültigen Kommentar.');
        pos = end + 3; continue;
      }
      if (source.slice(pos, pos + 9) === '<![CDATA[') {
        var dataEnd = source.indexOf(']]>', pos + 9);
        if (!stack.length || dataEnd < 0) fail('Die XML-Datei ist nicht vollständig.');
        pos = dataEnd + 3; continue;
      }
      if (source.slice(pos, pos + 2) === '<?') {
        var declarationEnd = source.indexOf('?>', pos + 2);
        if (pos !== 0 || declarationEnd < 0 || !/^<\?xml\s/.test(source)) fail('Die XML-Datei enthält eine nicht unterstützte Anweisung.');
        var declaration = source.slice(0, declarationEnd + 2);
        if (!/^<\?xml\s+version\s*=\s*(["'])1\.[01]\1(?:\s+encoding\s*=\s*(["'])[A-Za-z][A-Za-z0-9._-]*\2)?(?:\s+standalone\s*=\s*(["'])(?:yes|no)\3)?\s*\?>$/.test(declaration)) fail('Die XML-Datei enthält eine ungültige XML-Deklaration.');
        attributes(source.slice(5, declarationEnd)); pos = declarationEnd + 2; continue;
      }
      if (source[pos] !== '<') {
        var next = source.indexOf('<', pos); if (next < 0) next = source.length;
        var content = source.slice(pos, next);
        if ((!stack.length && content.trim()) || /\]\]>/.test(content)) fail('Die XML-Datei enthält Text außerhalb des Projekts.');
        entities(content); pos = next; continue;
      }
      var quote = '', close = pos + 1;
      for (; close < source.length; close++) {
        var character = source[close];
        if (quote) { if (character === quote) quote = ''; }
        else if (character === '"' || character === "'") quote = character;
        else if (character === '>') break;
        else if (character === '<') fail('Die XML-Datei ist nicht vollständig.');
      }
      if (close === source.length || quote) fail('Die XML-Datei ist nicht vollständig.');
      var body = source.slice(pos + 1, close), ending = /^\/([A-Za-z_:][A-Za-z0-9_.:-]*)\s*$/.exec(body);
      if (ending) {
        if (stack.pop() !== ending[1]) fail('Die XML-Datei enthält nicht zusammenpassende Elemente.');
        if (!stack.length) rootClosed = true;
      } else {
        var selfClosing = /\/\s*$/.test(body); if (selfClosing) body = body.replace(/\/\s*$/, '');
        var opening = /^([A-Za-z_:][A-Za-z0-9_.:-]*)([\s\S]*)$/.exec(body);
        if (!opening || rootClosed) fail('Bitte wähle ein vollständiges Snap!-Projekt als XML.');
        attributes(opening[2]);
        if (!stack.length) { if (rootSeen || opening[1] !== 'project') fail('Bitte wähle ein vollständiges Snap!-Projekt als XML.'); rootSeen = true; }
        if (opening[1] === 'stage' && (stack.join('/') === 'project' || stack.join('/') === 'project/scenes/scene')) stage = true;
        if (++count > 200000 || stack.length > 256) fail('Die XML-Datei ist zu stark verschachtelt oder zu umfangreich.');
        if (!selfClosing) stack.push(opening[1]); else if (!stack.length) rootClosed = true;
      }
      pos = close + 1;
    }
    if (!rootSeen || !rootClosed || stack.length || !stage) fail('Bitte wähle ein vollständiges Snap!-Projekt mit Bühne als XML.');
  }
  function validateProject(project) {
    try {
      if (!project || typeof project !== 'object' || Array.isArray(project) || Object.getPrototypeOf(project) !== Object.prototype || Object.keys(project).sort().join(',') !== 'filename,format,savedAt,version,xml') fail('Der Projektstand hat ein unbekanntes Format.');
      if (project.format !== 'snap-project' || project.version !== 1) fail('Diese Fassung des Projektstands wird nicht unterstützt.');
      if (typeof project.filename !== 'string' || project.filename.length > 160 || !project.filename.trim() || !/\.xml$/i.test(project.filename) || /[<>:"/\\|?*\x00-\x1f\x7f]/.test(project.filename) || /^[. ]|[. ]$/.test(project.filename)) fail('Bitte verwende einen Dateinamen ohne Ordnerpfad mit der Endung .xml.');
      if (typeof project.savedAt !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(project.savedAt) || !Number.isFinite(Date.parse(project.savedAt)) || new Date(project.savedAt).toISOString() !== project.savedAt) fail('Der Zeitpunkt des Projektstands ist ungültig.');
      xmlStructure(project.xml);
      return {ok: true, project: JSON.parse(JSON.stringify(project))};
    } catch (error) { return {ok: false, error: error.message || 'Der Projektstand konnte nicht gelesen werden.'}; }
  }
  return Object.freeze({MAX_PROJECT_BYTES: MAX_PROJECT_BYTES, validateProject: validateProject});
}));
