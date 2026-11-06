(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LernwerkWorkOverviewModel = factory();
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  var MAX_BYTES = 524288, MAX_CARDS = 200, MAX_LOCATIONS = 5;
  var AREA_BY_PREFIX = {med: 'medien', dat: 'daten', alg: 'programmieren', gam: 'gaming'};
  var AREAS = Object.keys(AREA_BY_PREFIX).map(function (key) { return AREA_BY_PREFIX[key]; });
  var KINDS = ['heft', 'dokument', 'bild', 'snap', 'anderes'];
  var UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  function fail(message) { throw new Error(message); }
  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function object(value, keys, required, name) {
    if (!value || typeof value !== 'object' || Array.isArray(value) || Object.getPrototypeOf(value) !== Object.prototype) fail(name + ' muss ein Objekt sein.');
    Object.keys(value).forEach(function (key) { if (keys.indexOf(key) === -1) fail(name + ': unbekanntes Feld „' + key + '“.'); });
    required.forEach(function (key) { if (!Object.prototype.hasOwnProperty.call(value, key)) fail(name + ': Feld „' + key + '“ fehlt.'); });
  }
  function text(value, max, name, nonempty) {
    if (typeof value !== 'string' || value.length > max || (nonempty && !value.trim()) || /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(value)) fail(name + ' ist ungültig oder zu lang (höchstens ' + max + ' Zeichen).');
  }
  function date(value, name) { if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value) || !Number.isFinite(Date.parse(value)) || new Date(value).toISOString() !== value) fail(name + ' ist kein gültiger Zeitpunkt.'); }
  function uuid(value) { if (typeof value !== 'string' || !UUID.test(value)) fail('Eine Kartenkennung ist ungültig.'); }
  function locations(value) {
    if (!Array.isArray(value) || value.length > MAX_LOCATIONS) fail('Eine Karte darf höchstens fünf Ablagehinweise haben.');
    value.forEach(function (entry) {
      object(entry, ['kind', 'hint', 'filename'], ['kind', 'hint', 'filename'], 'Ablagehinweis');
      if (KINDS.indexOf(entry.kind) === -1) fail('Unbekannte Art des Ablagehinweises.');
      text(entry.hint, 300, 'Ablagehinweis'); text(entry.filename, 160, 'Dateiname');
    });
  }
  function card(value, imported) {
    var keys = ['id', 'taskId', 'area', 'title', 'place', 'placeTitle', 'locations', 'next', 'updatedAt', 'inheritAreaHint', 'importedAt'];
    object(value, keys, keys.slice(0, 10), 'Merkkarte'); uuid(value.id);
    if (typeof value.taskId !== 'string' || !/^(med|dat|alg|gam)-[1-9]\d?$/.test(value.taskId)) fail('Die Aufgabenkennung ist ungültig.');
    if (value.area !== AREA_BY_PREFIX[value.taskId.split('-')[0]]) fail('Aufgabe und Themenbereich passen nicht zusammen.');
    text(value.title, 250, 'Aufgabentitel', true); text(value.placeTitle, 250, 'Arbeitsstelle', true);
    if (typeof value.place !== 'string' || (value.place !== '' && !/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,199}$/.test(value.place))) fail('Die Arbeitsstellenkennung ist ungültig.');
    locations(value.locations); text(value.next, 500, 'Nächster Schritt'); date(value.updatedAt, 'Änderungszeitpunkt');
    if (typeof value.inheritAreaHint !== 'boolean' || (imported && value.inheritAreaHint)) fail('Importierte Ablagehinweise müssen zur einzelnen Karte gehören.');
    if (Object.prototype.hasOwnProperty.call(value, 'importedAt')) date(value.importedAt, 'Importzeitpunkt');
  }
  function cards(value, imported) {
    if (!Array.isArray(value) || value.length > MAX_CARDS) fail('Die Übersicht darf höchstens 200 Merkkarten enthalten.');
    var ids = new Set();
    value.forEach(function (entry) { card(entry, imported); if (ids.has(entry.id)) fail('Eine Kartenkennung ist doppelt vorhanden.'); ids.add(entry.id); });
  }
  function checkCatalog(catalog) { if (!catalog || catalog.grade !== 7 || !Array.isArray(catalog.tasks) || !Array.isArray(catalog.areas)) fail('Der Aufgabenkatalog für Klasse 7 fehlt.'); }
  function checkStore(store, catalog) {
    checkCatalog(catalog);
    object(store, ['format', 'version', 'grade', 'cards', 'areaHints'], ['format', 'version', 'grade', 'cards', 'areaHints'], 'Übersicht');
    if (store.format !== 'ium-work-overview-store' || store.version !== 1 || store.grade !== 7) fail('Diese Übersicht gehört nicht zum unterstützten Format für Klasse 7.');
    cards(store.cards, false); object(store.areaHints, AREAS, [], 'Reihenhinweise');
    Object.keys(store.areaHints).forEach(function (area) { locations(store.areaHints[area]); });
    store.cards.forEach(function (entry) { if (entry.inheritAreaHint && !Object.prototype.hasOwnProperty.call(store.areaHints, entry.area)) fail('Der gemeinsame Reihenhinweis einer Karte fehlt.'); });
    return store;
  }
  function byteLength(value) {
    if (typeof TextEncoder !== 'undefined') return new TextEncoder().encode(value).length;
    return unescape(encodeURIComponent(value)).length;
  }
  function parse(textValue) {
    if (typeof textValue !== 'string' || byteLength(textValue) > MAX_BYTES) fail('Die Datei ist zu groß. Erlaubt sind höchstens 512 KiB.');
    try { return JSON.parse(textValue); } catch (_) { fail('Die Datei enthält keine lesbare JSON-Übersicht.'); }
  }
  function result(fn) { try { return fn(); } catch (error) { return {ok: false, error: error.message || 'Die Übersicht konnte nicht verarbeitet werden.'}; } }
  function empty() { return {format: 'ium-work-overview-store', version: 1, grade: 7, cards: [], areaHints: {}}; }
  function effectiveLocations(store, entry) { return clone(entry.inheritAreaHint && Object.prototype.hasOwnProperty.call(store.areaHints, entry.area) ? store.areaHints[entry.area] : entry.locations); }
  function safePath(value) { return typeof value === 'string' && /^(?:[a-zA-Z0-9_-]+\/)*[a-zA-Z0-9_-]+\.html$/.test(value); }
  function resolve(entry, catalog) {
    checkCatalog(catalog);
    var task = catalog.tasks.find(function (value) { return value.id === entry.taskId; });
    var area = catalog.areas.find(function (value) { return value.id === entry.area; });
    var place = task && task.places.find(function (value) { return value.id === entry.place; });
    var target = task && safePath(task.path) ? task.path : (area && safePath(area.path) ? area.path : 'index.html');
    if (task && place && place.id && /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,199}$/.test(place.id)) target += '#' + encodeURIComponent(place.id);
    return {target: target, task: task, area: area, place: place, missingTask: !task, missingPlace: Boolean(task && !place)};
  }
  function exportObject(store, catalog, now) {
    checkStore(store, catalog); date(now, 'Exportzeitpunkt');
    return {format: 'ium-work-overview', version: 1, grade: 7, exportedAt: now, cards: store.cards.map(function (entry) { var copy = clone(entry); copy.locations = effectiveLocations(store, entry); copy.inheritAreaHint = false; return copy; })};
  }
  function exportFile(store, catalog, now) {
    var output = JSON.stringify(exportObject(store, catalog, now), null, 2);
    if (byteLength(output) > MAX_BYTES) fail('Die Übersicht ist für eine einzelne Datei zu groß (höchstens 512 KiB). Bitte einige Karten entfernen.');
    return output;
  }
  function save(store, draft, catalog, options) {
    return result(function () {
      checkStore(store, catalog);
      object(draft, ['id', 'taskId', 'place', 'locations', 'next', 'inheritAreaHint'], ['taskId', 'place', 'locations', 'next', 'inheritAreaHint'], 'Karteneingabe');
      var task = catalog.tasks.find(function (value) { return value.id === draft.taskId; });
      if (!task) fail('Bitte eine vorhandene Aufgabe auswählen.');
      var place = task.places.find(function (value) { return value.id === draft.place; });
      if (!place) fail('Bitte eine vorhandene Arbeitsstelle auswählen.');
      var existing = draft.id ? store.cards.find(function (value) { return value.id === draft.id; }) : null;
      if (draft.id && !existing) fail('Die zu bearbeitende Karte ist nicht mehr vorhanden.');
      if (existing && existing.taskId !== task.id) fail('Eine bestehende Karte kann keiner anderen Aufgabe zugeordnet werden.');
      var entry = {id: existing ? existing.id : options.id, taskId: task.id, area: task.area, title: task.title, place: place.id, placeTitle: place.title, locations: clone(draft.locations), next: draft.next, updatedAt: options.now, inheritAreaHint: draft.inheritAreaHint};
      if (existing && existing.importedAt) entry.importedAt = existing.importedAt;
      card(entry, false);
      var nextStore = clone(store);
      if (existing) nextStore.cards[nextStore.cards.findIndex(function (value) { return value.id === existing.id; })] = entry;
      else nextStore.cards.push(entry);
      if (entry.inheritAreaHint) nextStore.areaHints[entry.area] = clone(entry.locations);
      checkStore(nextStore, catalog); exportFile(nextStore, catalog, options.now);
      return {ok: true, store: nextStore, card: clone(entry)};
    });
  }
  function remove(store, id) { var copy = clone(store); copy.cards = copy.cards.filter(function (entry) { return entry.id !== id; }); return copy; }
  function parseStore(value, catalog) { return result(function () { return {ok: true, store: clone(checkStore(parse(value), catalog))}; }); }
  function parseFile(value, catalog) {
    return result(function () {
      checkCatalog(catalog); var file = parse(value);
      object(file, ['format', 'version', 'grade', 'exportedAt', 'cards'], ['format', 'version', 'grade', 'exportedAt', 'cards'], 'Datei');
      if (file.format !== 'ium-work-overview' || file.version !== 1 || file.grade !== 7) fail('Diese Datei ist keine unterstützte Arbeitsübersicht für Klasse 7.');
      date(file.exportedAt, 'Exportzeitpunkt'); cards(file.cards, true);
      return {ok: true, cards: clone(file.cards)};
    });
  }
  function applyImport(store, importedCards, choices, catalog, now) {
    return result(function () {
      checkStore(store, catalog); cards(importedCards, true); date(now, 'Importzeitpunkt');
      if (!Array.isArray(choices)) fail('Die Kartenauswahl ist ungültig.');
      var nextStore = clone(store), sources = new Set(), targets = new Set();
      choices.forEach(function (choice) {
        object(choice, ['sourceId', 'mode', 'newId', 'targetId'], ['sourceId', 'mode'], 'Importauswahl');
        if (sources.has(choice.sourceId)) fail('Eine Importkarte wurde mehrfach ausgewählt.'); sources.add(choice.sourceId);
        var source = importedCards.find(function (entry) { return entry.id === choice.sourceId; });
        if (!source) fail('Die ausgewählte Importkarte fehlt.');
        var copy = clone(source); copy.inheritAreaHint = false; copy.importedAt = now;
        if (choice.mode === 'add') {
          if (Object.prototype.hasOwnProperty.call(choice, 'targetId')) fail('Zusätzlich übernehmen darf keine vorhandene Zielkarte angeben.');
          uuid(choice.newId); copy.id = choice.newId; nextStore.cards.push(copy);
        } else if (choice.mode === 'replace') {
          if (Object.prototype.hasOwnProperty.call(choice, 'newId')) fail('Ersetzen darf keine neue Kartenkennung angeben.');
          uuid(choice.targetId);
          if (targets.has(choice.targetId)) fail('Eine Zielkarte wurde mehrfach ausgewählt.'); targets.add(choice.targetId);
          var target = store.cards.find(function (entry) { return entry.id === choice.targetId; });
          if (!target || target.taskId !== source.taskId) fail('Ersetzen ist nur bei einer gewählten Karte derselben Aufgabe möglich.');
          copy.id = target.id; nextStore.cards[nextStore.cards.findIndex(function (entry) { return entry.id === target.id; })] = copy;
        } else fail('Unbekannte Importentscheidung.');
      });
      checkStore(nextStore, catalog); exportFile(nextStore, catalog, now);
      return {ok: true, store: nextStore};
    });
  }
  return Object.freeze({MAX_BYTES: MAX_BYTES, MAX_CARDS: MAX_CARDS, MAX_LOCATIONS: MAX_LOCATIONS, empty: empty, save: save, remove: remove, effectiveLocations: effectiveLocations, resolve: resolve, parseStore: parseStore, exportFile: exportFile, parseFile: parseFile, applyImport: applyImport});
}));
