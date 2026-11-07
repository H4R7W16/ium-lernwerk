(function () {
  'use strict';
  const M = window.LernwerkWorkOverviewModel;
  const S = window.LernwerkWorkOverviewStorage;
  const $ = id => document.getElementById(id);
  const app = $('work-app');
  if (!app || !M || !S) return;
  const catalog = JSON.parse($('work-catalog').textContent);
  const storage = S.create({session: () => window.sessionStorage, local: () => window.localStorage, catalog});
  let state = storage.load();
  let store = state.store;
  let dirty = false;
  
  let pendingImport = null;
  const projects = window.LernwerkWorkProjects?.createUI({model:M, catalog, getStore:()=>store, commit:save, feedback, download, exportOverview});
  const kinds = {heft: 'Heft / Papier', dokument: 'Dokument', bild: 'Bild', snap: 'Snap-Datei (.xml)', anderes: 'Anderer Ort'};
  const uuid = () => typeof crypto.randomUUID === 'function' ? crypto.randomUUID() : '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, c => (Number(c) ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> Number(c) / 4).toString(16));
  function el(tag, text, attrs = {}) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = text;
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    return node;
  }
  function button(text, action, primary = false) {
    const node = el('button', text, {type: 'button'});
    if (primary) node.className = 'work-primary';
    node.addEventListener('click', action);
    return node;
  }
  function link(text, href) { return el('a', text, {href}); }
  function field(text, input) {
    const label = el('label', null, {class: 'work-field'});
    label.append(el('span', text), input);
    return label;
  }
  function option(text, value) { return el('option', text, {value}); }
  function feedback(text, error = false) {
    $('work-feedback').textContent = text;
    $('work-feedback').classList.toggle('work-error', error);
    $('work-feedback').setAttribute('role', error ? 'alert' : 'status');
  }
  function download(text, filename, mime = 'application/json;charset=utf-8') {
    const url = URL.createObjectURL(new Blob([text], {type: mime}));
    const a = el('a', '', {href: url, download: filename});
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  }
  function save(next) {
    state = storage.save(next); store = state.store;
    render(); return state;
  }
  function needsLeaveWarning() { return dirty || Boolean(projects?.hasChanges()) || (state.volatile && store.cards.length > 0); }
  function leavePrompt() {
    if (projects?.hasChanges()) return 'Dein Projektstand ist noch nicht in die Übersicht übernommen. Trotzdem verlassen und diese Änderungen verwerfen?';
    return dirty ? 'Deine Änderungen sind noch nicht gemerkt. Trotzdem verwerfen?'
      : 'Deine Übersicht ist nur auf dieser Seite verfügbar. Lade sie zuerst herunter, wenn du sie behalten möchtest. Trotzdem verlassen?';
  }
  function dateText(value) {
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? 'Datum unbekannt' : date.toLocaleString('de-DE', {dateStyle: 'medium', timeStyle: 'short'});
  }
  function locationText(locations) {
    return locations.length ? locations.map(l => [kinds[l.kind], l.hint, l.filename].filter(Boolean).join(' · ')).join('\n') : 'Noch kein Ablagehinweis. Du kannst ihn später ergänzen.';
  }
  function renderStorage() {
    $('work-persistent').checked = state.persistent;
    $('work-remove-device').disabled = !state.deviceCopyExists;
    $('work-storage-status').textContent = state.deviceSaved && state.persistent
      ? 'Diese Übersicht wird zusätzlich auf diesem Gerät behalten. Beim Löschen der Browserdaten geht diese Kopie verloren.'
      : state.tabSaved ? 'Deine Übersicht bleibt beim Weiterarbeiten in diesem Browser-Tab erhalten. Zum sicheren Mitnehmen lädst du die Übersichtsdatei herunter.'
        : 'Deine Angaben sind zurzeit nur auf dieser geöffneten Seite verfügbar.';
    const box = $('work-storage-warning'); box.replaceChildren();
    const recoveries = state.recoveries || [];
    box.hidden = !state.volatile && !recoveries.length && !(state.errors || []).length && !state.needsDeviceConfirmation;
    if (state.needsDeviceConfirmation && state.deviceStore) {
      box.append(el('p', 'Auf diesem Gerät liegt eine andere Übersicht. Du kannst diese vorhandene Kopie zuerst herunterladen. Entscheide danach, ob du sie durch die hier angezeigte Übersicht ersetzen möchtest.'));
      box.append(button('Vorhandene Gerätekopie herunterladen', () => download(M.exportFile(state.deviceStore, catalog, new Date().toISOString()), 'ium7-vorhandene-geraetekopie.json')));
      box.append(button('Gerätekopie durch aktuelle Übersicht ersetzen', () => {
        if (!window.confirm('Die vorhandene Gerätekopie durch die aktuell angezeigte Übersicht ersetzen?')) return;
        state = storage.setPersistent(true, {replaceExisting: true}); store = state.store; renderStorage();
      }));
      box.append(button('Vorhandene Gerätekopie behalten', () => { state = storage.setPersistent(false); store = state.store; renderStorage(); }));
    }
    if (state.volatile) box.append(el('p', 'Diese Übersicht konnte im Browser nicht behalten werden. Deine Angaben sind noch hier. Lade die Übersicht herunter, bevor du diese Seite verlässt.'));
    else if ((state.errors || []).length) box.append(el('p', 'Eine Browserkopie konnte nicht aktualisiert werden. Nimm die aktuelle Übersicht als Datei mit.'));
    for (const recovery of recoveries) {
      box.append(el('p', 'Eine vorhandene ' + (recovery.source === 'device' ? 'Gerätekopie' : 'Tab-Kopie') + ' kann nicht gelesen werden. Sie wurde nicht überschrieben. Sichere diese Rohkopie zur Klärung.'));
      box.append(button('Unlesbare ' + (recovery.source === 'device' ? 'Gerätekopie' : 'Tab-Kopie') + ' herunterladen', () => download(recovery.raw, 'ium7-rohkopie-' + recovery.source + '.json')));
    }
  }
  function openSnap(task) {
    const dialog = $('work-snap-dialog'); dialog.replaceChildren();
    dialog.append(el('h2', 'Dein eigenes Snap-Projekt öffnen', {id: 'work-snap-heading'}));
    const steps = el('ol');
    for (const text of ['Öffne den Editor. Er kann zuerst das Startprojekt zeigen.', 'Wähle im Editor „Datei öffnen“ und wähle deine eigene XML-Datei an deinem Ablageort.', 'Prüfe, ob dein Code da ist. Wiederhole einen Test, bevor du weiterbaust.']) steps.append(el('li', text));
    dialog.append(steps, el('p', 'Diese Übersicht enthält deinen Dateinamen und Ablagehinweis. Dein Programm selbst liegt in der XML-Datei.'));
    const actions = el('div', null, {class: 'work-actions'});
    const editor = link('Editor öffnen', task.snapPath); editor.target = '_blank'; editor.rel = 'noopener';
    actions.append(editor, button('Schließen', () => dialog.close())); dialog.append(actions); dialog.showModal();
  }
  function renderCards() {
    const container = $('work-cards'); container.replaceChildren();
    $('work-empty').hidden = store.cards.length > 0;
    $('work-export').disabled = !store.cards.length;
    $('work-print').disabled = !store.cards.length;
    for (const card of [...store.cards].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))) {
      const resolved = M.resolve(card, catalog);
      const article = el('article', null, {class: 'work-card', 'data-card-id': card.id});
      article.append(el('h3', (resolved.task?.code || card.taskId.toUpperCase()) + ' · ' + (resolved.task?.title || card.title), {tabindex: '-1'}));
      const dl = el('dl');
      for (const [name, value] of [['Arbeitsstelle', resolved.place?.title || card.placeTitle || 'Ganze Aufgabe'], ['Dein Ablagehinweis', locationText(M.effectiveLocations(store, card))], ['Dein nächster Schritt', card.next || 'Noch nicht notiert.']]) dl.append(el('dt', name), el('dd', value));
      article.append(dl, el('p', 'Zuletzt gemerkt: ' + dateText(card.updatedAt), {class: 'work-meta'}));
      if (card.importedAt) article.append(el('p', 'Aus einer Übersichtsdatei übernommen: ' + dateText(card.importedAt), {class: 'work-meta'}));
      if (card.inheritAreaHint) article.append(el('p', 'Nutzt den gemeinsamen Ablagehinweis für ' + (resolved.area?.name || card.area) + '.', {class: 'work-help'}));
      if (resolved.missingTask || resolved.missingPlace) article.append(el('p', resolved.missingTask ? 'Diese Aufgabe ist nicht mehr im aktuellen Lernwerk. Deine Hinweise bleiben hier; der Link führt zur Themenübersicht.' : 'Diese Arbeitsstelle ist nicht mehr vorhanden. Deine Hinweise bleiben hier; der Link führt zum Anfang der Aufgabe.', {class: 'work-context'}));
      const actions = el('div', null, {class: 'work-actions'});
      actions.append(link(resolved.missingTask ? 'Zum Thema' : 'Zur Aufgabe', resolved.target));
      projects?.decorateCard(card, article, actions);
      if (resolved.task?.snapPath && card.taskId !== 'alg-5') actions.append(button('Eigenes Projekt öffnen – Anleitung', () => openSnap(resolved.task)));
      if (resolved.task) actions.append(button('Angaben ändern', () => openEditor(card.taskId, card)));
      actions.append(button('Eintrag entfernen', () => {
        if (!window.confirm(card.project ? 'Diese Karte einschließlich ihrer enthaltenen Projektkopie entfernen? Lade die Übersicht vorher herunter, wenn du sie behalten möchtest.' : 'Diesen Merkeintrag entfernen? Dein Heft und deine Dateien bleiben bestehen.')) return;
        save(M.remove(store, card.id)); feedback('Merkeintrag entfernt. Deine externen Dateien und dein Heft bleiben bestehen.'); $('work-add').focus();
      }));
      article.append(actions); container.append(article);
    }
  }
  function render() { renderCards(); renderStorage(); }
  function clearIntent() { if (location.search) history.replaceState(null, '', location.pathname + location.hash); }
  function showOverview() { dirty = false; clearIntent(); $('work-editor').hidden = true; $('work-overview').hidden = false; }
  function closeEditor() {
    if (dirty && !window.confirm(leavePrompt())) return;
    showOverview(); $('work-add').focus();
  }
  function openEditor(taskId, card) {
    if (!card && taskId) card = [...store.cards].filter(c => c.taskId === taskId).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))[0];
    if (dirty && !window.confirm(leavePrompt())) return;
    dirty = false;
    const panel = $('work-editor'); panel.replaceChildren(); panel.hidden = false; $('work-overview').hidden = true;
    const heading = el('h2', card ? 'Deinen Merkeintrag ändern' : 'Eine Arbeitsstelle merken', {id: 'work-editor-heading', tabindex: '-1'});
    panel.append(heading, el('p', 'Merke deine Arbeitsstelle. Ablagehinweis und nächster Schritt sind freiwillig. Du musst hier keine Ergebnisse übertragen.'));
    const form = el('form');
    const taskSelect = el('select', null, {name: 'task', required: '', 'aria-label': 'Aufgabe'});
    taskSelect.append(option('Aufgabe auswählen', ''));
    for (const area of catalog.areas) {
      const group = el('optgroup', null, {label: area.name});
      for (const task of catalog.tasks.filter(t => t.area === area.id)) group.append(option(task.code + ' · ' + task.title, task.id));
      taskSelect.append(group);
    }
    taskSelect.value = taskId || ''; taskSelect.disabled = Boolean(card);
    form.append(field('1 · Welche Aufgabe?', taskSelect));
    const placeSelect = el('select', null, {name: 'place', 'aria-label': 'Arbeitsstelle'});
    form.append(field('2 · Wo möchtest du weitermachen?', placeSelect));
    const help = el('p', '', {class: 'work-context'}); form.append(help);
    const locations = el('div');
    form.append(el('h3', '3 · Wo liegt dein Ergebnis? (freiwillig)'), el('p', 'Du merkst hier, wo dein Ergebnis liegt. Deine Dateien bleiben an ihrem bisherigen Ort.', {class: 'work-help'}), locations);
    let rows = [];
    function addLocation(value = {}) {
      if (rows.length >= 5) return;
      const row = el('fieldset', null, {class: 'work-location'});
      const legend = el('legend', 'Ablagehinweis'); row.append(legend);
      const kind = el('select', null, {name: 'location-kind', 'aria-label': 'Art der Ablage'});
      for (const [id, label] of Object.entries(kinds)) kind.append(option(label, id));
      kind.value = value.kind || 'heft';
      const hint = el('input', null, {type: 'text', name: 'location-hint', maxlength: '300', placeholder: 'Zum Beispiel: Heft, S. 18–19 oder Schulordner / Informatik'}); hint.value = value.hint || '';
      const filename = el('input', null, {type: 'text', name: 'location-filename', maxlength: '160', placeholder: 'Zum Beispiel: ALG-5_Kennung.xml'}); filename.value = value.filename || '';
      const filenameField = field('Dateiname (falls vorhanden)', filename);
      function toggleFilename() { filenameField.hidden = kind.value === 'heft' && !filename.value; }
      toggleFilename(); kind.addEventListener('change', toggleFilename);
      const data = {row, kind, hint, filename};
      row.append(field('Art der Ablage', kind), field('Ablageort / Seite', hint), filenameField, button('Diesen Ablagehinweis entfernen', () => { rows = rows.filter(r => r !== data); row.remove(); dirty = true; add.disabled = false; }));
      rows.push(data); locations.append(row);
      add.disabled = rows.length >= 5;
    }
    const add = button('Weiteren Ablageort ergänzen', () => { addLocation(); dirty = true; rows.at(-1).kind.focus(); }); form.append(add);
    const sharedDetails = el('details'); const sharedSummary = el('summary', 'Ablagehinweis für weitere Aufgaben nutzen'); sharedDetails.append(sharedSummary);
    const inherit = el('input', null, {type: 'checkbox', name: 'inherit'}); const sharedLabelText = el('span');
    const sharedLabel = el('label', null, {class: 'work-check'}); sharedLabel.append(inherit, sharedLabelText); sharedDetails.append(sharedLabel, el('p', 'Änderungen an diesem gemeinsamen Hinweis gelten auch für alle Merkeinträge, die ihn nutzen. Einträge mit eigenen Hinweisen bleiben unverändert.', {class: 'work-help'})); form.append(sharedDetails);
    const sharedWarning = el('p', 'Dieser Eintrag nutzt gemeinsame Ablagehinweise. Wenn du sie änderst, ändern sie sich auch bei anderen Einträgen dieses Themas. Schalte die gemeinsame Nutzung aus, wenn die Änderung nur hier gelten soll.', {class: 'work-context'}); sharedWarning.hidden = true; locations.before(sharedWarning);
    inherit.addEventListener('change', () => { sharedWarning.hidden = !inherit.checked; });
    const next = el('textarea', null, {name: 'next', maxlength: '500', rows: '3'}); next.value = card?.next || '';
    form.append(field('4 · Was möchtest du als Nächstes tun? (freiwillig)', next));
    const error = el('div', '', {class: 'work-error', role: 'alert'}); form.append(error);
    function selectTask(initial) {
      const task = catalog.tasks.find(t => t.id === taskSelect.value);
      placeSelect.replaceChildren();
      for (const place of task?.places || [{id: '', title: 'Zuerst eine Aufgabe wählen'}]) placeSelect.append(option(place.title, place.id));
      if (initial && card && task?.places.some(p => p.id === card.place)) placeSelect.value = card.place;
      else if (initial && !card) {
        const wanted = new URLSearchParams(location.search).get('stelle');
        if (task?.places.some(p => p.id === wanted)) placeSelect.value = wanted;
      }
      const area = catalog.areas.find(a => a.id === task?.area);
      sharedLabelText.textContent = 'Diese Ablagehinweise auch für weitere Aufgaben aus ' + (area?.name || 'diesem Thema') + ' verwenden';
      inherit.checked = Boolean(initial && card && card.inheritAreaHint);
      sharedDetails.open = inherit.checked; sharedWarning.hidden = !inherit.checked;
      rows = []; locations.replaceChildren();
      const initialLocations = initial && card ? M.effectiveLocations(store, card) : store.areaHints[task?.area] || [];
      if (initialLocations.length) initialLocations.forEach(addLocation);
      else { addLocation({kind: task?.snapPath ? 'snap' : 'heft'}); }
      help.replaceChildren();
      if (task?.snapPath) help.append(el('span', 'Merke die Ablage deiner XML-Datei und deiner Plan- und Testnotizen getrennt. Speichere die XML zuerst im Editor. '));
      else help.append(el('span', 'Ein kurzer Hinweis reicht. Du kannst die Arbeitsstelle auch ohne weitere Angaben merken. '));
      if (task?.notesPath) help.append(link('Aufgabe / Notizenhilfe', task.notesPath));
      next.placeholder = task?.id === 'alg-5' ? 'Zum Beispiel: Start an meiner Station prüfen: Stoppt der Rover sofort?' : task?.id === 'dat-1' ? 'Zum Beispiel: Zweite Nachricht zurückübersetzen und mit der Partnerperson vergleichen.' : 'Zum Beispiel: Mein Ergebnis mit einem neuen Fall prüfen.';
    }
    let selectedTask = taskSelect.value;
    taskSelect.addEventListener('change', () => {
      if (dirty && !window.confirm('Aufgabe wechseln und die noch nicht gemerkten Angaben verwerfen?')) { taskSelect.value = selectedTask; return; }
      selectedTask = taskSelect.value;
      const existing = [...store.cards].filter(c => c.taskId === selectedTask).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))[0];
      if (existing) { dirty = false; openEditor(selectedTask, existing); return; }
      next.value = ''; selectTask(false); dirty = true;
    });
    selectTask(true);
    form.addEventListener('input', event => { if (event.target !== taskSelect) dirty = true; }); form.addEventListener('change', event => { if (event.target !== taskSelect) dirty = true; });
    const actions = el('div', null, {class: 'work-actions'}); const submit = el('button', 'Arbeitsstelle merken', {type: 'submit', class: 'work-primary'});
    actions.append(submit, button('Abbrechen', closeEditor)); form.append(actions);
    form.addEventListener('submit', event => {
      event.preventDefault();
      const draft = {taskId: taskSelect.value, place: placeSelect.value, locations: rows.map(r => ({kind: r.kind.value, hint: r.hint.value.trim(), filename: r.filename.value.trim()})).filter(r => r.hint || r.filename), next: next.value.trim(), inheritAreaHint: inherit.checked};
      if (card) draft.id = card.id;
      const result = M.save(store, draft, catalog, {id: uuid(), now: new Date().toISOString()});
      if (!result.ok) { error.textContent = result.error; error.tabIndex = -1; error.focus(); return; }
      showOverview();
      save(result.store); feedback(state.volatile ? 'Arbeitsstelle gemerkt. Lade die Übersicht herunter, bevor du die Seite verlässt.' : 'Arbeitsstelle gemerkt. Deine Ergebnisse bleiben in deinem Heft oder deinen eigenen Dateien.');
      document.querySelector('[data-card-id="' + result.card.id + '"] h3')?.focus();
    });
    panel.append(form); heading.focus();
  }
  function showImport(cards) {
    pendingImport = cards;
    const dialog = $('work-import-dialog'); dialog.replaceChildren();
    dialog.append(el('h2', 'Welche Einträge möchtest du übernehmen?', {id: 'work-import-heading'}), el('p', 'Prüfe die Hinweise. Standardmäßig werden ausgewählte Einträge zusätzlich aufgenommen. Vorhandene Einträge bleiben bestehen.'));
    const selections = [];
    for (const card of cards) {
      const block = el('div', null, {class: 'work-import-card'});
      const check = el('input', null, {type: 'checkbox'}); check.checked = true;
      const label = el('label', null, {class: 'work-check'}); label.append(check, el('strong', card.taskId.toUpperCase() + ' · ' + card.title));
      block.append(label, el('p', 'Arbeitsstelle: ' + (card.placeTitle || 'Ganze Aufgabe') + '\n' + locationText(card.locations) + (card.next ? '\nNächster Schritt: ' + card.next : '')));
      if (card.project) block.append(el('p', 'Enthält Projektkopie: ' + card.project.filename + ' · übernommen ' + dateText(card.project.savedAt), {class:'work-project-meta'}));
      const resolved = M.resolve(card, catalog);
      if (resolved.missingTask || resolved.missingPlace) block.append(el('p', 'Das frühere Ziel hat sich verändert. Die Hinweise bleiben erhalten; du erreichst die aktuelle Aufgabe oder das Thema.', {class: 'work-context'}));
      const mode = el('select'); mode.append(option('Als zusätzlichen Eintrag übernehmen', 'add'));
      for (const existing of store.cards.filter(c => c.taskId === card.taskId)) mode.append(option('Ersetzen: ' + (existing.placeTitle || 'Ganze Aufgabe') + ' · ' + dateText(existing.updatedAt) + (existing.next ? ' · ' + existing.next : ''), existing.id));
      block.append(field('Übernahme für ' + card.taskId.toUpperCase(), mode)); dialog.append(block); selections.push({check, mode, card});
    }
    const error = el('div', '', {role: 'alert', class: 'work-error'}); dialog.append(error);
    const actions = el('div', null, {class: 'work-actions'});
    actions.append(button('Ausgewählte Einträge übernehmen', () => {
      if (dirty) { error.textContent = 'Deine Angaben wurden inzwischen geändert. Brich den Import ab und merke zuerst deine Änderungen.'; return; }
      const choices = selections.filter(s => s.check.checked).map(s => s.mode.value === 'add' ? {sourceId: s.card.id, mode: 'add', newId: uuid()} : {sourceId: s.card.id, mode: 'replace', targetId: s.mode.value});
      if (!choices.length) { error.textContent = 'Wähle mindestens einen Eintrag oder brich ab.'; return; }
      const result = M.applyImport(store, pendingImport, choices, catalog, new Date().toISOString());
      if (!result.ok) { error.textContent = result.error; return; }
      showOverview(); save(result.store); dialog.close(); pendingImport = null; feedback(choices.length + (choices.length === 1 ? ' Eintrag übernommen.' : ' Einträge übernommen.') + ' Weitere Dateien benötigst du zusätzlich; enthaltene ALG-5-Projektkopien sind übernommen.'); $('work-list-heading').tabIndex = -1; $('work-list-heading').focus();
    }, true), button('Abbrechen', () => { pendingImport = null; dialog.close(); })); dialog.append(actions); dialog.showModal();
  }
  $('work-add').addEventListener('click', () => openEditor());
  function exportOverview() {
    if (dirty || projects?.hasChanges()) { feedback('Übernimm zuerst deine Änderungen oder brich die Bearbeitung ab. Danach enthält der Export den angezeigten Stand.', true); return false; }
    try {
      download(M.exportFile(store, catalog, new Date().toISOString()), 'ium7-deine-arbeit-' + new Date().toISOString().slice(0, 10) + '.json');
      feedback('Download angeboten. Prüfe, ob die Übersichtsdatei an deinem gewünschten Ort angekommen ist. Enthaltene ALG-5-Projektkopien sind dabei; andere Ergebnisdateien nimmst du separat mit.'); return true;
    } catch (error) { feedback('Die Übersicht konnte nicht heruntergeladen werden: ' + error.message, true); return false; }
  }
  $('work-export').addEventListener('click', exportOverview);
  $('work-import-file').addEventListener('change', async event => {
    const file = event.target.files[0]; event.target.value = ''; if (!file) return;
    if (dirty) { feedback('Merke zuerst deine Änderungen oder brich die Bearbeitung ab. Wähle danach die Übersichtsdatei erneut.', true); return; }
    if (file.size > M.MAX_BYTES) { feedback('Diese Datei ist zu groß. Wähle eine Übersichtsdatei von höchstens 32 MiB.', true); return; }
    try {
      const result = M.parseFile(await file.text(), catalog);
      if (!result.ok) { feedback('Diese Datei wurde nicht übernommen. ' + result.error, true); return; }
      if (!result.cards.length) { feedback('Diese Übersichtsdatei enthält keine Merkeinträge.', true); return; }
      if (dirty) { feedback('Deine Angaben wurden inzwischen geändert. Merke sie zuerst und wähle die Übersichtsdatei danach erneut.', true); return; }
      showImport(result.cards);
    } catch (_) { feedback('Die Datei konnte nicht gelesen werden. Wähle eine heruntergeladene Übersichtsdatei für Klasse 7.', true); }
  });
  $('work-print').addEventListener('click', () => { if (dirty) feedback('Merke zuerst deine Änderungen oder brich die Bearbeitung ab.', true); else { showOverview(); window.print(); } });
  $('work-persistent').addEventListener('change', event => {
    const enabled = event.target.checked;
    state = storage.setPersistent(enabled);

    store = state.store; renderStorage();
  });
  $('work-remove-device').addEventListener('click', () => {
    if (!window.confirm('Die gespeicherte Gerätekopie entfernen? Die aktuelle Übersicht in diesem Tab und heruntergeladene Dateien bleiben erhalten.')) return;
    state = storage.removeDeviceCopy(); store = state.store; renderStorage();
    feedback(state.deviceCopyExists ? 'Die Gerätekopie konnte nicht entfernt werden. Bitte prüfe die Browsereinstellungen.' : 'Gerätekopie entfernt. Die aktuelle Übersicht ist weiterhin hier.');
  });
  window.addEventListener('beforeunload', event => { if (needsLeaveWarning()) { event.preventDefault(); event.returnValue = ''; } });
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (!anchor || anchor.hasAttribute('download') || anchor.target === '_blank' || anchor.getAttribute('href').startsWith('#')) return;
    if (needsLeaveWarning() && !window.confirm(leavePrompt())) event.preventDefault();
  });
  app.hidden = false; render();
  const wantedTask = new URLSearchParams(location.search).get('aufgabe');
  if (wantedTask && catalog.tasks.some(t => t.id === wantedTask)) openEditor(wantedTask);
}());





