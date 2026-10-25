/* Lernwerk-Ansicht für Snap! – AGPL-3.0-or-later. Quelltext und Herkunft: LERNWERK.md */
(function (root, factory) {
    'use strict';
    if (typeof module === 'object' && module.exports) module.exports = factory();
    else root.LernwerkModell = factory();
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
    'use strict';
    const TASKS = Object.freeze([
        ['alg-1', 'Feste Wiederholung', 'ALG-1-Start.xml'],
        ['alg-2', 'Werte und Wirkung', 'ALG-2-Start.xml'],
        ['alg-3', 'Ein Programm entscheidet', 'ALG-3-Start.xml'],
        ['alg-4', 'Wann ist Schluss?', 'ALG-4-Fehlersuche.xml'],
        ['alg-5', 'Deine eigene Steuerung', 'ALG-5-Start.xml'],
        ['alg-6', 'Code unter der Lupe', 'ALG-6-Fehlersuche.xml']
    ].map(([id, title, file]) => Object.freeze({id, title, project: '../projekte/' + file})));
    const SELECTORS = Object.freeze([
        'receiveGo', 'gotoXY', 'setHeading', 'forward', 'turn', 'turnLeft', 'xPosition',
        'yPosition', 'direction', 'bubble', 'doRepeat', 'doUntil', 'doIf', 'doIfElse',
        'reportSum', 'reportDifference', 'reportProduct', 'reportQuotient',
        'reportEquals', 'reportLessThan', 'reportGreaterThan', 'reportNot', 'reportAnd', 'reportOr'
    ]);
    function resolveTask(search, hash) {
        const params = new URLSearchParams(search);
        if (params.getAll('aufgabe').length > 1) return null;
        if (params.has('aufgabe')) return TASKS.find(t => t.id === params.get('aufgabe')) || null;
        if (hash) {
            if (!hash.startsWith('#open:')) return null;
            let project;
            try { project = decodeURIComponent(hash.slice(6)); } catch (_) { return null; }
            return TASKS.find(t => t.project === project) || null;
        }
        return TASKS[0];
    }
    function hiddenPrimitives(blocks, original, focused, migrations = {}) {
        const hidden = Object.assign({}, original);
        const allowed = new Set(SELECTORS);
        SELECTORS.forEach(initial => {
            let selector = initial; const seen = new Set();
            while (migrations[selector] && migrations[selector].selector && !seen.has(selector)) {
                seen.add(selector); selector = migrations[selector].selector; allowed.add(selector);
            }
        });
        if (focused) Object.keys(blocks).forEach(selector => {
            if (!allowed.has(selector)) hidden[selector] = true;
        });
        return hidden;
    }
    function withOriginalVisibility(stage, scene, original, operation) {
        const stageHidden = stage.hiddenPrimitives, sceneHidden = scene.hiddenPrimitives;
        stage.hiddenPrimitives = original;
        scene.hiddenPrimitives = original;
        try { return operation(); }
        finally { stage.hiddenPrimitives = stageHidden; scene.hiddenPrimitives = sceneHidden; }
    }
    async function readProject(file) {
        if (!file || !/\.xml$/i.test(file.name)) throw Error('Bitte wähle eine XML-Datei aus Snap!.');
        if (file.size > 10 * 1024 * 1024) throw Error('Die Datei ist größer als 10 MB.');
        const text = await file.text();
        if (/<!DOCTYPE|<!ENTITY/i.test(text)) throw Error('Diese XML-Datei enthält nicht unterstützte Angaben.');
        const body = text.trim().replace(/^<\?xml[^?]*\?>\s*/i, '');
        if (!/^<project(?:\s|>)/.test(body) || !/<\/project>\s*$/.test(body)) {
            throw Error('Bitte öffne ein vollständiges Snap!-Projekt als XML.');
        }
        return body;
    }
    function filename(raw) {
        const name = String(raw || '').trim().replace(/\.xml$/i, '')
            .replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').replace(/^[._ -]+/, '').slice(0, 80).trim();
        return (name || 'MeinProgramm') + '.xml';
    }
    function layout(availableWidth) {
        const width = Math.max(840, Math.round(availableWidth || 840));
        // Binär exakte Faktoren bewahren die ganzzahligen Grenzwerte dieser Aufgaben.
        return {width, paletteWidth: width >= 1100 ? 300 : 280,
            stageRatio: width >= 1100 ? 0.75 : (width >= 1000 ? 0.5 : 0.375)};
    }
    function controls(state) {
        return {canStep: Boolean(state.running && state.stepping),
            canPause: Boolean(state.running && !state.stepping), pauseLabel: state.stepping ? 'Pause' : (state.paused ? 'Fortsetzen' : 'Pause')};
    }
    return Object.freeze({TASKS, SELECTORS, resolveTask, hiddenPrimitives,
        withOriginalVisibility, readProject, filename, layout, controls});
}));
