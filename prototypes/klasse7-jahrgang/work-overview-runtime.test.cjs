'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const Model = require('../shared/work-overview-model.js');
const Storage = require('../shared/work-overview-storage.js');

const catalog = {
  grade: 7, version: 1,
  areas: [
    {id: 'daten', name: 'Daten und Codierung', path: 'daten/index.html', notesPath: 'daten/notizen.html'},
    {id: 'programmieren', name: 'Algorithmen', path: 'programmieren/index.html', notesPath: 'programmieren/notizen.html'}
  ],
  tasks: [
    {id: 'dat-1', code: 'DAT-1', title: 'Nachrichten codieren', area: 'daten', path: 'daten/dat-1.html', notesPath: 'daten/notizen.html', places: [{id: '', title: 'Ganze Aufgabe'}, {id: 'pruefen', title: 'Nachricht prüfen'}]},
    {id: 'dat-2', code: 'DAT-2', title: 'Daten darstellen', area: 'daten', path: 'daten/dat-2.html', notesPath: 'daten/notizen.html', places: [{id: '', title: 'Ganze Aufgabe'}]},
    {id: 'alg-5', code: 'ALG-5', title: 'Eigenes Projekt', area: 'programmieren', path: 'programmieren/alg-5.html', notesPath: 'programmieren/notizen.html', snapPath: 'snap/snap.html', places: [{id: '', title: 'Ganze Aufgabe'}]}
  ]
};
const fixtureId = '11111111-1111-4111-8111-111111111111';
const fixtureTime = '2026-11-06T10:00:00.000Z';
function memory() {
  const data = new Map();
  return {getItem: key => data.has(key) ? data.get(key) : null, setItem: (key, value) => data.set(key, String(value)), removeItem: key => data.delete(key)};
}
function fixtureStore(inheritAreaHint = false) {
  const saved = Model.save(Model.empty(), {taskId: 'dat-1', place: 'pruefen', locations: [{kind: 'heft', hint: 'Heft, Seite 12', filename: ''}], next: 'Nachricht prüfen', inheritAreaHint}, catalog, {id: fixtureId, now: fixtureTime});
  assert.equal(saved.ok, true);
  return saved.store;
}

// Only DOM operations used by this runtime are implemented. Events bubble through
// the form, so the tests exercise the browser input/change order and dirty guards.
class Element {
  constructor(tagName, ownerDocument) {
    this.tagName = tagName.toUpperCase(); this.ownerDocument = ownerDocument;
    this.children = []; this.parentElement = null; this.attributes = new Map();
    this.listeners = new Map(); this._text = ''; this._value = undefined;
    this.hidden = false; this.disabled = false; this.checked = false; this.open = false;
    this.files = [];
    this.classList = {toggle: (name, enabled) => {
      const values = new Set(this.className.split(/\s+/).filter(Boolean));
      const use = enabled === undefined ? !values.has(name) : enabled;
      if (use) values.add(name); else values.delete(name);
      this.className = [...values].join(' '); return use;
    }};
  }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(''); }
  set textContent(value) { this.replaceChildren(); this._text = String(value); }
  get className() { return this.getAttribute('class') || ''; }
  set className(value) { this.setAttribute('class', value); }
  get value() {
    if (this.tagName === 'SELECT') {
      const options = this.querySelectorAll('option');
      if (this._value !== undefined) return options.some(option => option.value === this._value) ? this._value : '';
      return options[0]?.value || '';
    }
    return this._value ?? this.getAttribute('value') ?? '';
  }
  set value(value) { this._value = String(value); }
  setAttribute(name, value) { this.attributes.set(name, String(value)); }
  getAttribute(name) { return this.attributes.has(name) ? this.attributes.get(name) : null; }
  hasAttribute(name) { return this.attributes.has(name); }
  append(...nodes) {
    for (const node of nodes) {
      node.remove(); node.parentElement = this; this.children.push(node);
    }
  }
  replaceChildren(...nodes) {
    for (const child of this.children) child.parentElement = null;
    this.children = []; this._text = '';
    if (this.tagName === 'SELECT') this._value = undefined;
    this.append(...nodes);
  }
  before(node) {
    const parent = this.parentElement;
    if (!parent) return;
    node.remove(); node.parentElement = parent;
    parent.children.splice(parent.children.indexOf(this), 0, node);
  }
  remove() {
    if (!this.parentElement) return;
    const siblings = this.parentElement.children;
    siblings.splice(siblings.indexOf(this), 1); this.parentElement = null;
  }
  addEventListener(type, handler) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(handler);
  }
  matches(selector) {
    const parsed = selector.match(/^([a-z][a-z0-9]*)?(?:\[([a-z0-9-]+)(?:="([^"]*)")?\])?$/i);
    if (!parsed) throw new Error('Unsupported fixture selector: ' + selector);
    const [, tag, attribute, value] = parsed;
    return (!tag || this.tagName === tag.toUpperCase()) && (!attribute || this.hasAttribute(attribute) && (value === undefined || this.getAttribute(attribute) === value));
  }
  closest(selector) {
    for (let node = this; node instanceof Element; node = node.parentElement) if (node.matches(selector)) return node;
    return null;
  }
  querySelectorAll(selector) {
    const split = selector.indexOf(' ');
    if (split !== -1) return this.querySelectorAll(selector.slice(0, split)).flatMap(node => node.querySelectorAll(selector.slice(split + 1)));
    const found = [];
    for (const child of this.children) {
      if (child.matches(selector)) found.push(child);
      found.push(...child.querySelectorAll(selector));
    }
    return found;
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  focus() { this.ownerDocument.activeElement = this; }
  showModal() { this.open = true; }
  close() { this.open = false; }
  click() {
    if (this.disabled) return Promise.resolve();
    if (this.tagName === 'A' && this.hasAttribute('download')) this.ownerDocument.downloads.push({href: this.getAttribute('href'), filename: this.getAttribute('download')});
    return emit(this, 'click');
  }
}
class Document {
  constructor() {
    this.listeners = new Map(); this.downloads = []; this.activeElement = null;
    this.body = new Element('body', this); this.body.parentElement = this;
  }
  createElement(tag) { return new Element(tag, this); }
  getElementById(id) { return this.body.querySelector('[id="' + id + '"]'); }
  querySelector(selector) { return this.body.querySelector(selector); }
  addEventListener(type, handler) { Element.prototype.addEventListener.call(this, type, handler); }
}
async function emit(target, type, extra = {}) {
  const event = {type, target, defaultPrevented: false, returnValue: undefined, preventDefault() { this.defaultPrevented = true; }, ...extra};
  const promises = [];
  const eventPath = [];
  for (let node = target; node; node = node.parentElement) eventPath.push(node);
  for (const node of eventPath) {
    for (const handler of node.listeners?.get(type) || []) {
      const result = handler(event);
      if (result && typeof result.then === 'function') promises.push(result);
    }
  }
  await Promise.all(promises);
  return event;
}
function boot({seed, query = '', blocked = false} = {}) {
  const session = memory(), local = memory(), doc = new Document();
  if (seed) {
    const saver = Storage.create({session, local, catalog}); saver.load();
    assert.equal(saver.save(seed).tabSaved, true);
  }
  function node(tag, id, parent = doc.body) {
    const value = doc.createElement(tag); value.setAttribute('id', id); parent.append(value); return value;
  }
  const app = node('main', 'work-app'); app.hidden = true;
  node('script', 'work-catalog').textContent = JSON.stringify(catalog);
  for (const [id, tag] of Object.entries({'work-feedback':'p', 'work-storage-status':'p', 'work-storage-warning':'div', 'work-add':'button', 'work-export':'button', 'work-print':'button', 'work-persistent':'input', 'work-remove-device':'button', 'work-import-file':'input', 'work-import-dialog':'dialog', 'work-snap-dialog':'dialog'})) node(tag, id, app);
  const overview = node('section', 'work-overview', app);
  node('h2', 'work-list-heading', overview); node('p', 'work-empty', overview); node('div', 'work-cards', overview);
  node('section', 'work-editor', app).hidden = true;
  const confirms = [], answers = [], blobs = new Map(), windowListeners = new Map();
  let serial = 0;
  class BrowserURL extends URL {}
  BrowserURL.createObjectURL = blob => { const url = 'blob:test-' + blobs.size; blobs.set(url, blob); return url; };
  BrowserURL.revokeObjectURL = () => {};
  const denied = {getItem() { throw new Error('Storage denied'); }, setItem() { throw new Error('Storage denied'); }, removeItem() { throw new Error('Storage denied'); }};
  const context = {
    document: doc, location: {search: query, pathname: '/klasse7/arbeit.html', hash: ''}, sessionStorage: blocked ? denied : session, localStorage: blocked ? denied : local,
    URL: BrowserURL, URLSearchParams, Blob, TextEncoder, console,
    crypto: {randomUUID: () => '99999999-9999-4999-8999-' + String(++serial).padStart(12, '0')},
    setTimeout: () => 1, print: () => {},
    confirm: text => { confirms.push(text); return answers.length ? answers.shift() : true; },
    addEventListener: (type, handler) => {
      if (!windowListeners.has(type)) windowListeners.set(type, []);
      windowListeners.get(type).push(handler);
    }
  };
  context.history = {replaceState: (_state, _title, target) => { const url = new URL(target, 'https://lernw.test'); context.location = {search: url.search, pathname: url.pathname, hash: url.hash}; }};
  context.window = context;
  vm.createContext(context);
  for (const file of ['../shared/work-overview-model.js', '../shared/work-overview-storage.js', './work-overview.js']) {
    const filename = path.resolve(__dirname, file);
    vm.runInContext(fs.readFileSync(filename, 'utf8'), context, {filename});
  }
  const byId = id => { const value = doc.getElementById(id); assert.ok(value, id + ' exists'); return value; };
  const field = name => { const value = byId('work-editor').querySelector('[name="' + name + '"]'); assert.ok(value, name + ' field exists'); return value; };
  return {
    doc, confirms, answers, blobs, session, local, byId, field,
    async chooseTask(value) { const select = field('task'); select.value = value; await emit(select, 'input'); await emit(select, 'change'); },
    async type(name, value) { const input = field(name); input.value = value; await emit(input, 'input'); },
    async submit() { return emit(byId('work-editor').querySelector('form'), 'submit'); },
    currentStore() { const raw = session.getItem(Storage.KEY); assert.ok(raw, 'tab cache exists'); return JSON.parse(raw).store; },
    async beforeUnload() { return emit({listeners: windowListeners}, 'beforeunload'); }
  };
}

test('erste Aufgabenwahl sendet input vor change und fragt nicht nach dem Verwerfen leerer Angaben', async () => {
  const page = boot();
  await page.byId('work-add').click();
  await page.chooseTask('dat-1');
  assert.equal(page.confirms.length, 0);
  assert.equal(page.field('task').value, 'dat-1');
  assert.ok(page.field('place').querySelectorAll('option').some(option => option.value === 'pruefen'));
});

test('abgebrochener Aufgabenwechsel erhält Aufgabe und eingegebene Hinweise', async () => {
  const page = boot({query: '?aufgabe=dat-1'});
  await page.type('location-hint', 'Heft, Seite 18');
  await page.type('next', 'Meine zweite Nachricht prüfen');
  page.answers.push(false);
  await page.chooseTask('alg-5');
  assert.equal(page.confirms.length, 1);
  assert.equal(page.field('task').value, 'dat-1');
  assert.equal(page.field('location-hint').value, 'Heft, Seite 18');
  assert.equal(page.field('next').value, 'Meine zweite Nachricht prüfen');
});

test('Downloadangebot für einen flüchtigen Stand hebt die Warnung beim Verlassen nicht auf', async () => {
  const page = boot({query: '?aufgabe=dat-1', blocked: true});
  await page.type('next', 'Nachricht noch einmal prüfen');
  await page.submit();
  assert.equal(page.byId('work-cards').querySelectorAll('article').length, 1);
  assert.equal(page.byId('work-storage-warning').hidden, false);
  await page.byId('work-export').click();
  assert.equal(page.doc.downloads.length, 1);
  const offered = page.blobs.get(page.doc.downloads[0].href);
  const exported = Model.parseFile(await offered.text(), catalog);
  assert.equal(exported.ok, true);
  assert.equal(exported.cards[0].next, 'Nachricht noch einmal prüfen');
  const leaving = await page.beforeUnload();
  assert.equal(leaving.defaultPrevented, true);
  assert.equal(leaving.returnValue, '');
});

test('Import aus unverändert geöffnetem Editor zeigt nach Übernahme die neue Übersicht', async () => {
  const page = boot();
  await page.byId('work-add').click();
  assert.equal(page.byId('work-editor').hidden, false);
  const json = Model.exportFile(fixtureStore(), catalog, fixtureTime);
  const picker = page.byId('work-import-file');
  picker.files = [{size: Buffer.byteLength(json), text: async () => json}];
  await emit(picker, 'change');
  const dialog = page.byId('work-import-dialog');
  assert.equal(dialog.open, true);
  const accept = dialog.querySelectorAll('button').find(button => button.textContent === 'Ausgewählte Einträge übernehmen');
  assert.ok(accept);
  await accept.click();
  assert.equal(dialog.open, false);
  assert.equal(page.byId('work-editor').hidden, true);
  assert.equal(page.byId('work-overview').hidden, false);
  assert.equal(page.byId('work-cards').querySelectorAll('article').length, 1);
  assert.equal(page.doc.activeElement, page.byId('work-list-heading'));
});

test('DAT-2 übernimmt Reihenhinweis als Ausgangspunkt; eigene Änderung lässt DAT-1 unverändert', async () => {
  const page = boot({seed: fixtureStore(true), query: '?aufgabe=dat-2'});
  assert.equal(page.field('location-hint').value, 'Heft, Seite 12');
  assert.equal(page.field('inherit').checked, false);
  await page.type('location-hint', 'Heft, Seite 24');
  await page.submit();
  const stored = page.currentStore();
  assert.equal(stored.cards.length, 2);
  const dat1 = stored.cards.find(card => card.taskId === 'dat-1');
  const dat2 = stored.cards.find(card => card.taskId === 'dat-2');
  assert.equal(Model.effectiveLocations(stored, dat1)[0].hint, 'Heft, Seite 12');
  assert.equal(Model.effectiveLocations(stored, dat2)[0].hint, 'Heft, Seite 24');
  assert.equal(dat2.inheritAreaHint, false);
});

test('bestehende Karte über Aufgabenwahl öffnen lässt Export und Verlassen ohne neue Änderungswarnung zu', async () => {
  const page = boot({seed: fixtureStore()});
  await page.byId('work-add').click();
  await page.chooseTask('dat-1');
  assert.equal(page.field('task').disabled, true);
  assert.equal(page.field('next').value, 'Nachricht prüfen');
  assert.equal(page.confirms.length, 0);
  await page.byId('work-export').click();
  assert.equal(page.doc.downloads.length, 1);
  assert.equal((await page.beforeUnload()).defaultPrevented, false);
});

test('während des Dateilesens eingegebener Text bleibt erhalten und verhindert die Importvorschau', async () => {
  const page = boot();
  await page.byId('work-add').click();
  const json = Model.exportFile(fixtureStore(), catalog, fixtureTime);
  let finishReading;
  const reading = new Promise(resolve => { finishReading = resolve; });
  const picker = page.byId('work-import-file');
  picker.files = [{size: Buffer.byteLength(json), text: () => reading}];
  const importing = emit(picker, 'change');
  await page.type('next', 'Diesen neuen Text möchte ich behalten');
  finishReading(json);
  await importing;
  assert.equal(page.byId('work-import-dialog').open, false);
  assert.equal(page.byId('work-editor').hidden, false);
  assert.equal(page.field('next').value, 'Diesen neuen Text möchte ich behalten');
  assert.equal(page.byId('work-cards').querySelectorAll('article').length, 0);
  assert.equal((await page.beforeUnload()).defaultPrevented, true);
});
