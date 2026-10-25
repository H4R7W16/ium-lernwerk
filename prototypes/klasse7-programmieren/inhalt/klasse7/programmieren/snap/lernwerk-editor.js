/* Lernwerk-Ansicht für Snap! – AGPL-3.0-or-later. Siehe LERNWERK.md. */
/* global WorldMorph, IDE_Morph, Point, StageMorph, SpriteMorph, Process, Color, saveAs, localize, LernwerkModell */
var world;
(function () {
    'use strict';
    const model = LernwerkModell;
    const byId = id => document.getElementById(id);
    const task = model.resolveTask(location.search, location.hash);
    let ide, ready = false, focused = true, lastScene = null, lastUpdate = 0, lastCycle = 0;
    const originalVisibility = new WeakMap();
    const setText = (id, text) => { if (byId(id).textContent !== String(text)) byId(id).textContent = text; };
    const notice = text => setText('notice', text);
    const categories = ['motion', 'looks', 'control', 'operators'];

    function showDialog(dialog) {
        if (dialog.showModal) dialog.showModal();
        else dialog.setAttribute('open', '');
    }
    function closeDialog(dialog) {
        if (dialog.close) dialog.close();
        else dialog.removeAttribute('open');
    }
    function rebuildCategories() {
        const selected = byId('category').value;
        const names = focused ? categories : SpriteMorph.prototype.allCategories();
        byId('category').replaceChildren(...names.map(name => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = localize(name.charAt(0).toUpperCase() + name.slice(1));
            return option;
        }));
        byId('category').value = names.includes(selected) ? selected : 'motion';
        ide.currentCategory = byId('category').value;
    }
    function applyPalette() {
        const original = originalVisibility.get(ide.scene) || {};
        StageMorph.prototype.hiddenPrimitives = model.hiddenPrimitives(SpriteMorph.prototype.blocks, original, focused, SpriteMorph.prototype.blockMigrations);
        ide.flushBlocksCache();
        ide.refreshPalette(true);
    }
    function fitWorkspace() {
        if (!ide || !world) return;
        const area = byId('workspace');
        const layout = model.layout(byId('workspace-scroll').clientWidth);
        const width = layout.width;
        const height = Math.round(area.getBoundingClientRect().height);
        const canvas = byId('world');
        if (canvas.width !== width || canvas.height !== height) {
            canvas.width = width;
            canvas.height = height;
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';
            world.setExtent(new Point(width, height));
        }
        ide.paletteWidth = layout.paletteWidth;
        ide.isSmallStage = true;
        ide.stageRatio = layout.stageRatio;
        ide.reactToWorldResize(world.bounds);
        document.documentElement.style.setProperty('--palette', ide.paletteWidth + 'px');
        document.documentElement.style.setProperty('--stage', ide.stage.width() + 'px');
        world.changed();
    }
    function applyView() {
        if (!ide.stage) return;
        if (!originalVisibility.has(ide.scene)) {
            originalVisibility.set(ide.scene, Object.assign({}, StageMorph.prototype.hiddenPrimitives));
        }
        lastScene = ide.scene;
        Object.assign(ide.config, {hideControls: focused, hideCategories: true,
            noSpriteEdits: focused, noOwnBlocks: focused});
        if (!focused) {
            ide.logo.show(); ide.controlBar.show(); ide.spriteBar.show();
            ide.corralBar.show(); ide.corral.show(); ide.stageHandle.show();
        }
        ide.applyPaneHidingConfigurations();
        ide.zoomBar.hide();
        ide.setColor(new Color(246, 245, 240));
        rebuildCategories();
        applyPalette();
        byId('tools').setAttribute('aria-expanded', String(!focused));
        byId('tools').textContent = focused ? 'Mehr Werkzeuge' : 'Weniger Werkzeuge';
        fitWorkspace();
    }
    function updateState() {
        if (!ready) return;
        if (lastScene !== ide.scene) applyView();
        const name = ide.getProjectName();
        const originalName = task.project.split('/').pop().replace(/\.xml$/, '');
        setText('project-title', name === originalName ? task.id.toUpperCase() + ' · ' + task.title : (name || 'Dein Programm'));
        const stepping = Boolean(Process.prototype.enableSingleStepping);
        const running = ide.isRunning();
        const paused = ide.isPaused();
        const controls = model.controls({stepping, running, paused});
        byId('step').disabled = !controls.canStep;
        byId('pause').disabled = !controls.canPause;
        setText('pause', controls.pauseLabel);
        byId('step-mode').setAttribute('aria-pressed', String(stepping));
        setText('run-state', running ? (paused ? (stepping ? 'Wartet auf einen Schritt' : 'Pausiert') : 'Läuft') : 'Bereit');
        const sprite = ide.currentSprite;
        const number = value => Number.isFinite(value) ? String(Math.round(value * 100) / 100).replace('.', ',') : '–';
        const isFigure = sprite && sprite !== ide.stage && typeof sprite.xPosition === 'function';
        setText('x', isFigure ? number(sprite.xPosition()) : '–');
        setText('y', isFigure ? number(sprite.yPosition()) : '–');
        setText('direction', isFigure ? number(sprite.direction()) : '–');
    }
    function setStepping(enabled) {
        if (Boolean(Process.prototype.enableSingleStepping) !== enabled) ide.toggleSingleStepping();
        Process.prototype.flashTime = enabled ? 0.8 : 0;
        ide.controlBar.refreshSlider();
        updateState();
    }
    function projectXML() {
        return model.withOriginalVisibility(StageMorph.prototype, ide.scene,
            originalVisibility.get(ide.scene) || {}, () => ide.getProjectXML());
    }
    function enable() {
        ready = true;
        ['start', 'stop', 'step-mode', 'save', 'open', 'tools', 'category'].forEach(id => byId(id).disabled = false);
        applyView();
        // Vorbereitete Stapel werden kompakt untereinander angeordnet.
        // Das verändert nur ihre Bildschirmposition, nicht ihre Verbindung oder Befehlsfolge.
        ide.currentSprite.scripts.cleanUp();
        updateState();
        notice('Halte deine Vorhersage fest. Einzelne Stapel startest du durch Antippen.');
    }
    byId('help-open').addEventListener('click', () => showDialog(byId('help-dialog')));
    byId('help-close').addEventListener('click', () => closeDialog(byId('help-dialog')));
    byId('save-cancel').addEventListener('click', () => closeDialog(byId('save-dialog')));
    byId('start').addEventListener('click', () => {
        ide.pressStart();
        notice('Grüne Flagge gestartet. Lose Stapel startest du durch Antippen.');
        updateState();
    });
    byId('stop').addEventListener('click', () => { ide.stopAllScripts(); notice('Ausführung gestoppt. Dein Programm bleibt erhalten.'); updateState(); });
    byId('pause').addEventListener('click', () => { ide.togglePauseResume(); updateState(); });
    byId('step-mode').addEventListener('click', () => {
        const enabled = !Process.prototype.enableSingleStepping;
        setStepping(enabled);
        notice(enabled ? 'Schrittmodus an: Starte mit der grünen Flagge oder tippe einen Stapel an. Danach: Ein Schritt.' : 'Schrittmodus aus. Mit Fortsetzen läuft ein pausiertes Programm weiter.');
    });
    byId('step').addEventListener('click', () => { ide.stage.threads.resumeAll(ide.stage); updateState(); });
    byId('tools').addEventListener('click', () => { focused = !focused; applyView(); notice(focused ? 'Lernwerk-Ansicht: die Bausteine für ALG-1 bis ALG-6.' : 'Vollständige Werkzeuge geöffnet. Dein Programm ist unverändert vorhanden.'); });
    byId('category').addEventListener('change', () => { ide.currentCategory = byId('category').value; ide.refreshPalette(true); });
    byId('save').addEventListener('click', () => {
        byId('filename').value = model.filename(ide.getProjectName() || task.id.toUpperCase()).replace(/\.xml$/, '');
        showDialog(byId('save-dialog'));
        byId('filename').focus(); byId('filename').select();
    });
    byId('save-form').addEventListener('submit', event => {
        event.preventDefault();
        try {
            const name = model.filename(byId('filename').value);
            const xml = projectXML();
            saveAs(new Blob([xml], {type: 'application/xml;charset=utf-8'}), name);
            closeDialog(byId('save-dialog'));
            notice('Download angefordert: ' + name + '. Prüfe den Downloadordner und öffne die Datei erneut.');
        } catch (error) { notice('Die Datei konnte nicht erstellt werden: ' + error.message); }
    });
    byId('open').addEventListener('click', () => byId('file').click());
    byId('file').addEventListener('change', async () => {
        const file = byId('file').files[0];
        if (!file) return;
        try {
            const text = await model.readProject(file);
            const doc = new DOMParser().parseFromString(text, 'application/xml');
            if (doc.querySelector('parsererror') || doc.documentElement.tagName !== 'project' || !doc.querySelector('scene stage')) {
                throw Error('Die Datei ist kein vollständiges, gültiges Snap!-Projekt.');
            }
            if (ide.hasUnsavedEdits() && !confirm('Im aktuellen Projekt gibt es Änderungen. Hast du sie als Datei gesichert? OK ersetzt das aktuelle Projekt; Abbrechen behält es.')) {
                notice('Öffnen abgebrochen. Dein bisheriges Projekt bleibt geöffnet.'); return;
            }
            const previousScene = ide.scene;
            ide.stopAllScripts();
            ide.openProjectString(text, () => {
                if (ide.scene === previousScene) { notice('Die Datei konnte nicht geöffnet werden. Prüfe, ob sie aus Snap! stammt.'); return; }
                setStepping(false);
                applyView();
                updateState();
                notice('Datei geöffnet: ' + file.name + '. Prüfe jetzt deinen Testfall erneut.');
            });
        } catch (error) { notice(error.message); }
        finally { byId('file').value = ''; }
    });
    window.addEventListener('beforeunload', event => {
        if (ready && ide.hasUnsavedEdits()) { event.preventDefault(); event.returnValue = ''; }
    });
    function boot() {
        if (!task) { notice('Diese Aufgabe ist unbekannt. Öffne einen Einstieg über die Lernwegübersicht.'); return; }
        setText('project-title', task.id.toUpperCase() + ' · ' + task.title);
        byId('task-link').href = '../lernende/' + task.id + '.html';
        byId('standard-link').href = 'index.html#open:' + task.project;
        // Legacy-Links dürfen nur auf eines der sechs vorbereiteten Projekte zeigen.
        if (location.hash) history.replaceState(null, '', location.pathname + '?aufgabe=' + task.id);
        world = new WorldMorph(byId('world'), false);
        ide = new IDE_Morph({noCloud: true, lang: 'de', design: 'flat', theme: 'bright',
            blocksZoom: 1.45, zoom: 1, noUserSettings: true, noShare: true, preserveTitle: true,
            hideControls: true, hideCategories: true, noSpriteEdits: true, noOwnBlocks: true,
            mode: 'edit', load: task.project, onload: enable});
        ide.openIn(world);
        // applySavedMagnification liest im Original auch bei noUserSettings einen Zoomwert.
        // Die Lernwerk-Ansicht setzt ihn deshalb ausdrücklich ohne Präferenzspeicherung zurück.
        ide.setZoom(100, true);
        Process.prototype.enableJS = false;
        fitWorkspace();
        function loop(time) {
            if (time - lastCycle >= 1000 / 60) {
                world.doOneCycle();
                lastCycle = Math.max(lastCycle + 1000 / 60, time - 1000 / 60);
            }
            if (time - lastUpdate > 120) { lastUpdate = time; updateState(); }
            requestAnimationFrame(loop);
        }
        requestAnimationFrame(loop);
        let resizePending = false;
        const resize = () => {
            if (resizePending) return;
            resizePending = true;
            requestAnimationFrame(() => { resizePending = false; fitWorkspace(); });
        };
        window.addEventListener('resize', resize);
        if (window.visualViewport) window.visualViewport.addEventListener('resize', resize);
        if (typeof ResizeObserver !== 'undefined') new ResizeObserver(resize).observe(byId('workspace-scroll'));
        setTimeout(() => { if (!ready) notice('Die Datei konnte noch nicht geladen werden. Prüfe die Verbindung oder nutze den bisherigen Snap!-Einstieg im Fußbereich.'); }, 20000);
    }
    window.addEventListener('load', boot, {once: true});
}());
