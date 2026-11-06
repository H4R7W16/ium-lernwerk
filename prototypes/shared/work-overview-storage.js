(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./work-overview-model.js'));
  else root.LernwerkWorkOverviewStorage = factory(root.LernwerkWorkOverviewModel);
}(typeof globalThis !== 'undefined' ? globalThis : this, function (Model) {
  'use strict';
  var KEY = 'ium-klasse7-work-overview-v1', PREF = KEY + '-persistent';
  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
  function create(options) {
    var validate = options.validator || function (value) { return Model.parseStore(value, options.catalog); };
    var store = Model.empty(), persistent = false, tabSaved = false, deviceSaved = false, loaded = false;
    var errors = [], recoveries = [], needsDeviceConfirmation = false, stamp = 0;
    var slots = {tab: {source: 'tab', provider: options.session, raw: null, blocked: false, parsed: null}, device: {source: 'device', provider: options.local, raw: null, blocked: false, parsed: null}};
    function label(slot) { return slot.source === 'tab' ? 'Tabsicherung' : 'Gerätekopie'; }
    function error(message) { errors.push(message); }
    function storage(slot) {
      var value = typeof slot.provider === 'function' ? slot.provider() : slot.provider;
      if (!value || typeof value.getItem !== 'function' || typeof value.setItem !== 'function' || typeof value.removeItem !== 'function') throw new Error('Speicher nicht verfügbar');
      return value;
    }
    function parseCache(raw) {
      try {
        var envelope = JSON.parse(raw);
        if (!envelope || typeof envelope !== 'object' || Array.isArray(envelope) || Object.keys(envelope).sort().join(',') !== 'format,grade,stamp,store,version' || envelope.format !== 'ium-work-overview-cache' || envelope.version !== 1 || envelope.grade !== 7 || !Number.isSafeInteger(envelope.stamp) || envelope.stamp < 0) return {ok: false, error: 'Nicht unterstütztes Speicherformat für Klasse 7.'};
        var checked = validate(JSON.stringify(envelope.store));
        return checked.ok ? {ok: true, store: checked.store, stamp: envelope.stamp} : checked;
      } catch (_) { return {ok: false, error: 'Die gespeicherte Übersicht ist nicht lesbar.'}; }
    }
    function updateRecovery(slot) {
      recoveries = recoveries.filter(function (entry) { return entry.source !== slot.source; });
      if (slot.raw !== null && slot.parsed && !slot.parsed.ok) recoveries.push({source: slot.source, raw: slot.raw, error: slot.parsed.error});
    }
    function read(slot) {
      try {
        slot.raw = storage(slot).getItem(KEY);
        slot.parsed = slot.raw === null ? null : parseCache(slot.raw);
        slot.blocked = Boolean(slot.parsed && !slot.parsed.ok);
        if (slot.parsed && slot.parsed.ok) stamp = Math.max(stamp, slot.parsed.stamp);
        updateRecovery(slot);
        if (slot.blocked) error(label(slot) + ' ist nicht lesbar und bleibt unverändert.');
      } catch (_) { slot.blocked = Boolean(slot.parsed && !slot.parsed.ok); error(label(slot) + ' kann nicht gelesen werden.'); }
    }
    function freshStamp() {
      var time = options.now ? options.now() : Date.now();
      stamp = Math.max(Number.isSafeInteger(time) && time >= 0 ? time : 0, stamp + 1);
      return stamp;
    }
    function envelope() { return JSON.stringify({format: 'ium-work-overview-cache', version: 1, grade: 7, stamp: freshStamp(), store: store}); }
    function changedDevice(slot, raw) {
      if (raw === slot.raw) return false;
      slot.raw = raw; slot.parsed = raw === null ? null : parseCache(raw); slot.blocked = Boolean(slot.parsed && !slot.parsed.ok); updateRecovery(slot);
      needsDeviceConfirmation = true; slot.requiresConfirmation = true;
      error('Die Gerätekopie wurde inzwischen geändert. Bitte die vorhandene Kopie prüfen, bevor du sie ersetzt.');
      return true;
    }
    function write(slot, raw, allowChanged) {
      if (slot.blocked) { error(label(slot) + ' bleibt geschützt. Deine Änderungen sind weiterhin hier geöffnet.'); return false; }
      try {
        var target = storage(slot), existing = target.getItem(KEY);
        if (slot.source === 'device' && slot.requiresConfirmation && !allowChanged) {
          needsDeviceConfirmation = true; error('Die geänderte Gerätekopie bleibt geschützt, bis du ausdrücklich Ersetzen wählst.'); return false;
        }
        if (slot.source === 'tab' && existing !== slot.raw) {
          slot.raw = existing; slot.parsed = existing === null ? null : parseCache(existing);
          slot.blocked = Boolean(slot.parsed && !slot.parsed.ok); updateRecovery(slot);
        }
        if (slot.source === 'device' && changedDevice(slot, existing) && !allowChanged) return false;
        if (slot.blocked) { error(label(slot) + ' ist nicht lesbar und wird nicht überschrieben.'); return false; }
        target.setItem(KEY, raw);
        if (target.getItem(KEY) !== raw) throw new Error('Schreibprüfung fehlgeschlagen');
        slot.raw = raw; slot.parsed = parseCache(raw); slot.requiresConfirmation = false; updateRecovery(slot);
        return true;
      } catch (_) { error(label(slot) + ' konnte nicht bestätigt werden. Deine Änderungen bleiben hier geöffnet.'); return false; }
    }
    function preference(value) {
      try {
        var target = storage(slots.device);
        target.setItem(PREF, value ? '1' : '0');
        if (target.getItem(PREF) !== (value ? '1' : '0')) throw new Error('Schreibprüfung fehlgeschlagen');
        return true;
      } catch (_) { error('Die Einstellung zur Gerätespeicherung konnte nicht bestätigt werden.'); return false; }
    }
    function snapshot(ok) {
      var validDevice = slots.device.parsed && slots.device.parsed.ok;
      return {ok: typeof ok === 'boolean' ? ok : errors.length === 0, store: clone(store), persistent: persistent, tabSaved: tabSaved, deviceSaved: deviceSaved, volatile: !tabSaved && !deviceSaved && (store.cards.length > 0 || Object.keys(store.areaHints).length > 0), deviceCopyExists: slots.device.raw !== null, deviceStore: validDevice ? clone(slots.device.parsed.store) : null, recoveries: clone(recoveries), errors: errors.slice(), needsDeviceConfirmation: needsDeviceConfirmation};
    }
    function load() {
      if (loaded) return snapshot();
      errors = []; read(slots.tab); read(slots.device);
      try { persistent = storage(slots.device).getItem(PREF) === '1'; } catch (_) { persistent = false; error('Die Einstellung zur Gerätespeicherung kann nicht gelesen werden.'); }
      var tab = slots.tab.parsed && slots.tab.parsed.ok ? slots.tab.parsed : null;
      var device = persistent && slots.device.parsed && slots.device.parsed.ok ? slots.device.parsed : null;
      var chosen = device && (!tab || device.stamp > tab.stamp) ? device : tab;
      if (chosen) store = clone(chosen.store);
      tabSaved = Boolean(tab && same(tab.store, store)); deviceSaved = Boolean(device && same(device.store, store));
      loaded = true; return snapshot();
    }
    function save(value) {
      if (!loaded) load();
      errors = []; needsDeviceConfirmation = false;
      var checked;
      try { checked = validate(JSON.stringify(value)); } catch (_) { checked = {ok: false, error: 'Die Übersicht ist ungültig.'}; }
      if (!checked.ok) { error(checked.error); return snapshot(false); }
      store = clone(checked.store);
      var raw = envelope(); tabSaved = write(slots.tab, raw, false); deviceSaved = false;
      if (persistent) {
        try {
          if (storage(slots.device).getItem(PREF) === '1') deviceSaved = write(slots.device, raw, false);
          else { persistent = false; error('Die Gerätespeicherung wurde inzwischen ausgeschaltet. Die vorhandene Gerätekopie bleibt erhalten.'); }
        } catch (_) { error('Die Einstellung zur Gerätespeicherung kann gerade nicht geprüft werden. Es wurde keine Gerätekopie geschrieben.'); }
      }
      return snapshot();
    }
    function setPersistent(enabled, settings) {
      if (!loaded) load();
      errors = []; needsDeviceConfirmation = false; settings = settings || {};
      if (!enabled) {
        if (preference(false)) { persistent = false; deviceSaved = false; }
        return snapshot();
      }
      var before = slots.device.raw;
      read(slots.device);
      if (slots.device.blocked) { deviceSaved = false; return snapshot(false); }
      var existing = slots.device.parsed;
      if (existing && existing.ok && !same(existing.store, store) && !settings.replaceExisting) {
        needsDeviceConfirmation = true; deviceSaved = false;
        error('Eine andere Gerätekopie ist vorhanden. Bitte ausdrücklich entscheiden, ob du sie ersetzen möchtest.');
        return snapshot(false);
      }
      // read() updates the baseline only after the caller has opted in; corrupt data remains blocked.
      if (before !== slots.device.raw && existing && existing.ok) stamp = Math.max(stamp, existing.stamp);
      var written = write(slots.device, envelope(), settings.replaceExisting === true);
      if (written && preference(true)) { persistent = true; deviceSaved = true; }
      else deviceSaved = false;
      return snapshot();
    }
    function removeDeviceCopy() {
      if (!loaded) load();
      errors = []; needsDeviceConfirmation = false;
      if (!preference(false)) return snapshot(false);
      persistent = false; deviceSaved = false;
      try {
        var target = storage(slots.device); target.removeItem(KEY);
        if (target.getItem(KEY) !== null) throw new Error('Löschprüfung fehlgeschlagen');
        slots.device.raw = null; slots.device.parsed = null; slots.device.blocked = false; slots.device.requiresConfirmation = false; updateRecovery(slots.device);
        target.removeItem(PREF);
        if (target.getItem(PREF) !== null) throw new Error('Einstellung blieb erhalten');
      } catch (_) { error('Die Gerätekopie konnte nicht vollständig entfernt werden.'); read(slots.device); }
      return snapshot();
    }
    return Object.freeze({load: load, save: save, setPersistent: setPersistent, removeDeviceCopy: removeDeviceCopy, snapshot: function () { if (!loaded) load(); return snapshot(); }});
  }
  return Object.freeze({KEY: KEY, PREFERENCE_KEY: PREF, create: create});
}));
