import { expect, test, type Page } from '@playwright/test';
import { choosePersistent, chooseVolatile, openPersistent, reloadPersistent } from './helpers/storage-choice.js';
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const moduleUrl = '/module/v2-g5-m06/';

test('NA01 prevents typing into an editor before its stored dossier is ready', async ({ page }) => {
  await page.goto(moduleUrl);
  await page.locator('[data-rationale]').focus();
  await page.keyboard.type('DARF-NICHT-VOR-LADEN-EINGEGEBEN-WERDEN');
  await expect(page.locator('[data-rationale]')).toHaveValue('');
  await choosePersistent(page);
  await page.locator('[data-rationale]').fill('NACH-LADEN');
  await page.locator('[data-m06-save]').click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
  await reloadPersistent(page);
  await expect(page.locator('[data-rationale]')).toHaveValue('NACH-LADEN');
});

async function exportDossier(page: Page) {
  const details = page.locator('details').filter({ has: page.locator('[data-export-work]') });
  if ((await details.getAttribute('open')) === null) await details.locator('summary').click();
  const pending = page.waitForEvent('download');
  await page.locator('[data-export-work]').click();
  const path = await (await pending).path();
  return JSON.parse(await readFile(path!, 'utf8')).payload;
}

test('NA01 exports the visible unsaved draft and protects it during document preparation', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.locator('[data-editor="code"] [data-add="move"]').click();
  await page.getByLabel('Begründung der Prüffahrt').fill('AKTUELL-OHNE-SPEICHERN');
  const exported = await exportDossier(page);
  expect(exported.p3.draftProgram).toEqual([{ id: 'cmd-1', kind: 'move' }]);
  expect(exported.p3.evidence.rationale).toBe('AKTUELL-OHNE-SPEICHERN');
  const readiness = await page.evaluate(async () => {
    const pending: Promise<unknown>[] = [];
    document.dispatchEvent(new CustomEvent('ium:reload-request', {
      detail: { add: (task: Promise<unknown>) => pending.push(task) },
    }));
    return Promise.all(pending);
  });
  expect(readiness).toEqual([expect.objectContaining({ safe: true, reason: 'persisted-readback' })]);
  await expect(page.locator('[data-editor="code"] [data-add="move"]')).toBeDisabled();
  await expect(page.locator('[data-rationale]')).toBeDisabled();
  await page.evaluate(() => document.dispatchEvent(new CustomEvent('ium:reload-release')));
  await expect(page.locator('[data-rationale]')).toBeEnabled();
  await reloadPersistent(page);
  await expect(page.locator('[data-rationale]')).toHaveValue('AKTUELL-OHNE-SPEICHERN');
  await expect(page.locator('[data-code-output]')).toContainText('vor');
});

function fullDossier() {
  const program = [{ id: 'cmd-1', kind: 'turn-right' }];
  return {
    schemaVersion: 1,
    p1: { diagram: { program, explanation: 'P1 Grafik' } },
    p2: {
      before: { program, predicted: { position: { column: 2, row: 3 }, direction: 'north' }, steps: [1], rationale: 'P2 vorher' },
      after: { program, predicted: { position: { column: 4, row: 1 }, direction: 'east' }, steps: [1], rationale: 'P2 nachher' }, firstDeviation: 1,
    },
    p3: { diagram: { program, explanation: 'P3 Grafik' }, draftProgram: program,
      evidence: { program, predicted: { position: { column: 1, row: 3 }, direction: 'south' }, steps: [1], rationale: 'P3 Begründung' } },
    p5: { sequence: ['prüfen', 'aufnehmen', 'ablegen'], rationale: 'P5 Transfer' },
    p6: { timeControl: 'P6 Zeit', routeCalculation: 'P6 Weg', boundary: 'P6 Grenze' },
    returnNote: { area: 'dossier', openPoint: 'Rückkehr offen', nextAction: 'Rückkehr weiter' },
  };
}

function importFile() {
  return { name: 'complete.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify({
    format: 'ium-learning-state', formatVersion: 1, moduleId: 'V2-G5-M06', moduleVersion: '0.1.0',
    stateSchemaVersion: 1, workspaceId: '123e4567-e89b-42d3-a456-426614174000',
    savedAt: '2026-09-09T08:00:00.000Z', payload: fullDossier(),
  })) };
}

test('NA02 retries a genuine local read failure without inventing an empty recovery', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'PRESERVED-AFTER-READ-ERROR');
  await page.evaluate(() => sessionStorage.setItem('na02-read-error', 'pending'));
  await page.addInitScript(() => {
    const original = IDBDatabase.prototype.transaction;
    IDBDatabase.prototype.transaction = function (names, mode, options) {
      if (this.name === 'ium-lernwerk-v2' && mode === 'readonly'
        && sessionStorage.getItem('na02-read-error') === 'pending') {
        sessionStorage.setItem('na02-read-error', 'done');
        throw new DOMException('SYNTHETIC-READ-ERROR', 'UnknownError');
      }
      return original.call(this, names, mode, options);
    };
  });
  await reloadPersistent(page);
  await expect(page.locator('[data-m06-start-error]')).toBeVisible();
  await expect(page.locator('[data-rationale]')).toBeDisabled();
  await expect(page.locator('[data-export-recovery]')).toBeDisabled();
  await expect(page.locator('[data-retry-start]')).toBeVisible();
  await page.locator('[data-retry-start]').click();
  await choosePersistent(page);
  await expect(page.locator('[data-rationale]')).toHaveValue('PRESERVED-AFTER-READ-ERROR');
  expect((await exportDossier(page)).p3.evidence.rationale).toBe('PRESERVED-AFTER-READ-ERROR');
});

test('NA02 discards late file reads after a newer selection or deletion', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'CURRENT-WITH-SLOW-FILE');
  await page.evaluate(() => {
    const original = File.prototype.arrayBuffer;
    File.prototype.arrayBuffer = async function () {
      if (this.name !== 'slow.json') return original.call(this);
      document.documentElement.dataset.slowFile = 'waiting';
      await new Promise<void>((accept) => window.addEventListener('na02:release-file', () => accept(), { once: true }));
      const bytes = await original.call(this);
      document.documentElement.dataset.slowFile = 'finished';
      return bytes;
    };
  });
  await page.getByText('Daten verwalten').click();
  for (const action of ['invalid-selection', 'delete']) {
    await page.locator('[data-import-work]').setInputFiles({ ...importFile(), name: 'slow.json' });
    await expect(page.locator('html')).toHaveAttribute('data-slow-file', 'waiting');
    if (action === 'invalid-selection') {
      await page.locator('[data-import-work]').setInputFiles({ name: 'bad.json', mimeType: 'application/json', buffer: Buffer.from('{bad') });
      await expect(page.locator('[data-m06-save-status]')).toHaveAttribute('data-save-state', 'unsaved');
    } else {
      page.once('dialog', (dialog) => dialog.accept());
      await page.locator('[data-delete-work]').click();
      await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gelöscht.');
    }
    await page.evaluate(() => window.dispatchEvent(new Event('na02:release-file')));
    await expect(page.locator('html')).toHaveAttribute('data-slow-file', 'finished');
    await expect(page.locator('[data-import-preview]')).toBeHidden();
    expect((await exportDossier(page)).p3.evidence.rationale).toBe(action === 'delete' ? '' : 'CURRENT-WITH-SLOW-FILE');
  }
});

test('NA02 previews without replacing work and consumes canceled or invalidated selections', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'CURRENT-BEFORE-IMPORT');
  await page.getByText('Daten verwalten').click();
  await page.locator('[data-import-work]').setInputFiles(importFile());
  await expect(page.locator('[data-import-preview]')).toBeVisible();
  await expect(page.locator('[data-import-preview]')).toContainText('P3 Begründung');
  await expect(page.locator('[data-rationale]')).toHaveValue('CURRENT-BEFORE-IMPORT');
  expect((await exportDossier(page)).p3.evidence.rationale).toBe('CURRENT-BEFORE-IMPORT');
  await page.locator('[data-cancel-import]').click();
  await expect(page.locator('[data-import-preview]')).toBeHidden();
  await page.locator('[data-import-work]').setInputFiles(importFile());
  await expect(page.locator('[data-import-preview]')).toBeVisible();
  await page.locator('[data-import-work]').setInputFiles({ name: 'invalid.json', mimeType: 'application/json', buffer: Buffer.from('{broken') });
  await expect(page.locator('[data-import-preview]')).toBeHidden();
  await expect(page.locator('[data-m06-save-status]')).toHaveAttribute('data-save-state', 'unsaved');
  await reloadPersistent(page);
  await expect(page.locator('[data-rationale]')).toHaveValue('CURRENT-BEFORE-IMPORT');
  await page.getByText('Daten verwalten').click();
  await page.locator('[data-import-work]').setInputFiles(importFile());
  await page.locator('[data-confirm-import]').click();
  await expect(page.locator('[data-rationale]')).toHaveValue('P3 Begründung');
  await reloadPersistent(page);
  expect(await exportDossier(page)).toEqual(fullDossier());
});

for (const damage of ['payload', 'version'] as const) {
test(`NA02 exports a damaged local ${damage} before a deliberate replacement`, async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'ORIGINAL-BEFORE-DAMAGE');
  const damaged = await page.evaluate(async (damage) => {
    const database = await new Promise<IDBDatabase>((accept, reject) => {
      const request = indexedDB.open('ium-lernwerk-v2');
      request.onsuccess = () => accept(request.result); request.onerror = () => reject(request.error);
    });
    const transaction = database.transaction('states', 'readwrite');
    let original: unknown;
    const request = transaction.objectStore('states').get('V2-G5-M06');
    request.onsuccess = () => {
      const row = request.result;
      if (damage === 'payload') row.state.payload = { damaged: 'LOCAL-ORIGINAL-SENTINEL' };
      else row.state.moduleVersion = '99.0.0';
      original = row.state;
      transaction.objectStore('states').put(row);
    };
    await new Promise<void>((accept, reject) => {
      transaction.oncomplete = () => accept(); transaction.onerror = () => reject(transaction.error);
    });
    database.close(); return original;
  }, damage);
  await reloadPersistent(page);
  await expect(page.locator('[data-m06-start-error]')).toBeVisible();
  await expect(page.locator('[data-rationale]')).toBeDisabled();
  await expect(page.locator('[data-export-recovery]')).toBeEnabled();
  const download = page.waitForEvent('download');
  await page.locator('[data-export-recovery]').click();
  const exported = await download;
  expect(exported.suggestedFilename()).toContain('recovery-original');
  expect(JSON.parse(await readFile((await exported.path())!, 'utf8'))).toEqual(damaged);
  if (damage === 'version') {
    await page.locator('[data-import-work]').setInputFiles(importFile());
    await expect(page.locator('[data-import-preview]')).toBeVisible();
    await expect(page.locator('[data-rationale]')).toBeDisabled();
    await page.locator('[data-confirm-import]').click();
    await expect(page.locator('[data-rationale]')).toHaveValue('P3 Begründung');
    await reloadPersistent(page);
    expect(await exportDossier(page)).toEqual(fullDossier());
    return;
  }
  page.once('dialog', (dialog) => dialog.dismiss());
  await page.locator('[data-start-new]').click();
  await expect(page.locator('[data-rationale]')).toBeDisabled();
  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-start-new]').click();
  await expect(page.locator('[data-m06-start-error]')).toBeHidden();
  await expect(page.locator('[data-rationale]')).toBeEnabled();
  await saveP3(page, 'RECOVERED-NEW-WORK');
  await reloadPersistent(page);
  await expect(page.locator('[data-rationale]')).toHaveValue('RECOVERED-NEW-WORK');
  expect(JSON.stringify(await exportDossier(page))).not.toContain('LOCAL-ORIGINAL-SENTINEL');
});
}

test('NA02 deletion clears all products and pending preview then permits a durable new draft', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByText('Daten verwalten').click();
  await page.locator('[data-import-work]').setInputFiles(importFile());
  await page.locator('[data-confirm-import]').click();
  await expect(page.locator('[data-rationale]')).toHaveValue('P3 Begründung');
  await page.locator('[data-import-work]').setInputFiles(importFile());
  await expect(page.locator('[data-import-preview]')).toBeVisible();
  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-delete-work]').click();
  await expect(page.locator('[data-m06-save-status]')).toContainText('gelöscht');
  await expect(page.locator('[data-import-preview]')).toBeHidden();
  for (const selector of ['[data-rationale]', '[data-diagram-explanation]', '[data-p1-explanation]',
    '[data-revision-rationale="before"]', '[data-revision-rationale="after"]', '[data-transfer-rationale]',
    '[data-system="timeControl"]', '[data-system="routeCalculation"]', '[data-system="boundary"]',
    '[data-return-open]', '[data-return-next]']) {
    await expect(page.locator(selector)).toHaveValue('');
  }
  await page.locator('[data-editor="code"] [data-add="turn-left"]').click();
  await saveP3(page, 'NEW-AFTER-DELETE');
  await reloadPersistent(page);
  const dossier = await exportDossier(page);
  expect(dossier.p3.draftProgram).toEqual([{ id: 'cmd-1', kind: 'turn-left' }]);
  expect(dossier.p3.evidence.rationale).toBe('NEW-AFTER-DELETE');
  expect(dossier.p1.diagram.program).toEqual([]);
  expect(dossier.p6).toEqual({ timeControl: '', routeCalculation: '', boundary: '' });
});

test('NA02 delete readback failure clears old fields and allows a safe reload', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'MUST-NOT-REVIVE-AFTER-DELETE');
  await page.evaluate(() => {
    const original = IDBDatabase.prototype.transaction;
    IDBDatabase.prototype.transaction = function (names, mode, options) {
      if (this.name === 'ium-lernwerk-v2' && mode === 'readonly') {
        IDBDatabase.prototype.transaction = original;
        throw new DOMException('SYNTHETIC-DELETE-READBACK', 'UnknownError');
      }
      return original.call(this, names, mode, options);
    };
  });
  await page.getByText('Daten verwalten').click();
  page.once('dialog', (dialog) => dialog.accept());
  await page.locator('[data-delete-work]').click();
  await expect(page.locator('[data-m06-start-error]')).toBeVisible();
  await expect(page.locator('[data-rationale]')).toHaveValue('');
  await expect(page.locator('[data-rationale]')).toBeDisabled();
  await expect(page.locator('[data-export-work]')).toBeDisabled();
  await page.locator('[data-retry-start]').click();
  await choosePersistent(page);
  await saveP3(page, 'NEW-AFTER-READBACK-ERROR');
  await reloadPersistent(page);
  expect((await exportDossier(page)).p3.evidence.rationale).toBe('NEW-AFTER-READBACK-ERROR');
});

test('NA01 hydrates every durable product after import and reload and preserves its neighbours', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.locator('[data-editor="code"] [data-add="move"]').click();
  await page.getByText('Daten verwalten').click();
  const dossier = fullDossier();
  await page.locator('[data-import-work]').setInputFiles({ name: 'complete.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ format: 'ium-learning-state', formatVersion: 1,
      moduleId: 'V2-G5-M06', moduleVersion: '0.1.0', stateSchemaVersion: 1,
      workspaceId: '123e4567-e89b-42d3-a456-426614174000', savedAt: '2026-09-09T08:00:00.000Z', payload: dossier })) });
  await page.locator('[data-confirm-import]').click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Importierter Arbeitsstand gespeichert.');
  for (const reload of [false, true]) {
    if (reload) await reloadPersistent(page);
    await expect(page.locator('[data-code-output]')).toContainText('rechts');
    await expect(page.locator('[data-diagram-explanation]')).toHaveValue('P3 Grafik');
    await expect(page.locator('[data-rationale]')).toHaveValue('P3 Begründung');
    await expect(page.locator('[data-p1-explanation]')).toHaveValue('P1 Grafik');
    await expect(page.locator('[data-revision-rationale="before"]')).toHaveValue('P2 vorher');
    await expect(page.locator('[data-revision-rationale="after"]')).toHaveValue('P2 nachher');
    await expect(page.locator('[data-revision-output="before"]')).toContainText('Vorhersage: (2,3), Blick oben');
    await expect(page.locator('[data-revision-output="after"]')).toContainText('Vorhersage: (4,1), Blick rechts');
    await expect(page.locator('[data-saved-prediction]')).toContainText('(1,3), Blick unten');
    await expect(page.locator('[data-trace-output] input[value="1"]')).toBeChecked();
    await expect(page.locator('[data-first-deviation]')).toHaveValue('1');
    await expect(page.locator('[data-transfer-sequence]')).toHaveValue('prüfen, aufnehmen, ablegen');
    await expect(page.locator('[data-transfer-rationale]')).toHaveValue('P5 Transfer');
    await expect(page.locator('[data-system="timeControl"]')).toHaveValue('P6 Zeit');
    await expect(page.locator('[data-system="routeCalculation"]')).toHaveValue('P6 Weg');
    await expect(page.locator('[data-system="boundary"]')).toHaveValue('P6 Grenze');
    await expect(page.locator('[data-return-area]')).toHaveValue('dossier');
    await expect(page.locator('[data-return-open]')).toHaveValue('Rückkehr offen');
    await expect(page.locator('[data-return-next]')).toHaveValue('Rückkehr weiter');
    expect(await exportDossier(page)).toEqual(dossier);
  }
  await page.locator('[data-system="routeCalculation"]').fill('P6 neuer Weg');
  let exported = await exportDossier(page);
  expect(exported).toEqual({ ...dossier, p6: { ...dossier.p6, routeCalculation: 'P6 neuer Weg' } });
  await page.locator('[data-p1-explanation]').fill('P1 ergänzt');
  await page.locator('[data-revision-rationale="before"]').fill('P2 Ursache ergänzt');
  await page.locator('[data-transfer-rationale]').fill('P5 ergänzt');
  exported = await exportDossier(page);
  expect(exported.p1.diagram.explanation).toBe('P1 ergänzt');
  expect(exported.p2.before.rationale).toBe('P2 Ursache ergänzt');
  expect(exported.p2.after).toEqual(dossier.p2.after);
  expect(exported.p3).toEqual(dossier.p3);
  expect(exported.p5).toEqual({ ...dossier.p5, rationale: 'P5 ergänzt' });
  await page.locator('[data-editor="code"] [data-add="turn-left"]').click();
  exported = await exportDossier(page);
  expect(exported.p3.draftProgram.map((command: { kind: string }) => command.kind)).toEqual(['turn-right', 'turn-left']);
  await page.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
  await reloadPersistent(page);
  await expect(page.locator('[data-system="timeControl"]')).toHaveValue('P6 Zeit');
  await expect(page.locator('[data-system="routeCalculation"]')).toHaveValue('P6 neuer Weg');
});

test('NA01 protects real M06 clients through worker veto, timeout and activation', async ({ context, page }) => {
  test.setTimeout(90_000);
  await openPersistent(page, moduleUrl);
  await expect(page.locator('[data-connection-status]')).toHaveAttribute('data-pwa-state', 'ready', { timeout: 20_000 });
  await reloadPersistent(page);
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
  await page.locator('[data-editor="code"] [data-add="move"]').click();
  await page.locator('[data-rationale]').fill('VOR-UPDATE-UNGESPEICHERT');
  const sibling = await context.newPage();
  await sibling.goto(moduleUrl);
  await chooseVolatile(sibling);
  await expect.poll(() => sibling.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
  await sibling.locator('[data-rationale]').fill('FLÜCHTIG-ERHALTEN');
  const workerPath = resolve('apps/lernwerk-portal/dist/sw.js');
  const original = await readFile(workerPath, 'utf8');
  try {
    // A byte-distinct installable worker with the same verified asset manifest.
    // This isolates activation/state protection from unrelated content changes.
    await writeFile(workerPath, `${original}\n// NA01 synthetic update ${Date.now()}\n`, 'utf8');
    await page.evaluate(async () => { await (await navigator.serviceWorker.ready).update(); });
    await expect(page.locator('[data-update-prompt]')).toBeVisible({ timeout: 20_000 });
    await page.evaluate(() => {
      document.addEventListener('ium:reload-request', ((event: CustomEvent<{ add(task: Promise<unknown>): void }>) => {
        event.detail.add(new Promise((accept) => setTimeout(() => accept({ safe: true, reason: 'no-work', revision: 0 }), 1_500)));
      }) as EventListener, { once: true });
    });
    await page.getByRole('button', { name: 'Speichern und aktualisieren', exact: true }).click();
    await expect(page.locator('[data-rationale]')).toBeDisabled();
    await expect(page.locator('[data-editor="code"] [data-add="move"]')).toBeDisabled();
    await expect(page.locator('[data-update-status]')).toContainText('ungesicherter Sitzungsstand');
    await expect(page.locator('[data-rationale]')).toBeEnabled();
    await expect(sibling.locator('[data-rationale]')).toBeEnabled();
    expect((await exportDossier(sibling)).p3.evidence.rationale).toBe('FLÜCHTIG-ERHALTEN');
    await sibling.close();
    const legacy = await context.newPage();
    await legacy.goto('/app-icon.svg');
    await expect.poll(() => legacy.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
    await page.getByRole('button', { name: 'Speichern und aktualisieren', exact: true }).click();
    await expect(page.locator('[data-update-status]')).toContainText('Nicht alle offenen Seiten', { timeout: 10_000 });
    await expect(page.locator('[data-rationale]')).toBeEnabled();
    await legacy.close();
    await page.locator('[data-rationale]').fill('NACH-TIMEOUT-UNGESPEICHERT');
    const previousOrigin = await page.evaluate(() => performance.timeOrigin);
    await page.getByRole('button', { name: 'Speichern und aktualisieren', exact: true }).click();
    await choosePersistent(page);
    expect(await page.evaluate(() => performance.timeOrigin)).toBeGreaterThan(previousOrigin);
    await expect(page.locator('[data-rationale]')).toHaveValue('NACH-TIMEOUT-UNGESPEICHERT');
    await expect(page.locator('[data-code-output]')).toContainText('vor');
    expect(await page.evaluate(async () => (await navigator.serviceWorker.ready).waiting)).toBeNull();
  } finally {
    await writeFile(workerPath, original, 'utf8');
  }
});

async function saveP3(page: Page, text: string): Promise<void> {
  await page.getByLabel('Begründung der Prüffahrt').fill(text);
  await page.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
}

test('P4 is not restored from the dossier and P3 remains editable', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await page.getByLabel('Deine Abrufbegründung').fill('SYNTHETIC-P4-SENTINEL');
  await page.getByRole('button', { name: 'Zum eigenen Entwurf' }).click();
  await saveP3(page, 'SYNTHETIC-P3-SENTINEL');
  await reloadPersistent(page);
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('SYNTHETIC-P3-SENTINEL');
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await expect(page.getByLabel('Deine Abrufbegründung')).toHaveValue('');
});

test('keeps P0 and P4 sentinels out of the stored envelope and conscious export', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByLabel('Meine Vorhersage vor dem Ausführen').fill('SYNTHETIC-P0-SENTINEL');
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await page.getByLabel('Deine Abrufbegründung').fill('SYNTHETIC-P4-SENTINEL');
  await saveP3(page, 'SYNTHETIC-P3-SENTINEL');
  const stored = await page.evaluate(async () => {
    const request = indexedDB.open('ium-lernwerk-v2');
    const database = await new Promise<IDBDatabase>((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    const names = [...database.objectStoreNames];
    const rows: unknown[] = [];
    for (const name of names) {
      const transaction = database.transaction(name, 'readonly');
      const values = await new Promise<unknown[]>((resolve, reject) => {
        const query = transaction.objectStore(name).getAll();
        query.onsuccess = () => resolve(query.result);
        query.onerror = () => reject(query.error);
      });
      rows.push(...values);
    }
    database.close();
    return JSON.stringify(rows);
  });
  expect(stored).toContain('SYNTHETIC-P3-SENTINEL');
  expect(stored).not.toContain('SYNTHETIC-P0-SENTINEL');
  expect(stored).not.toContain('SYNTHETIC-P4-SENTINEL');

  await page.getByText('Daten verwalten').click();
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand exportieren' }).click();
  const path = await (await download).path();
  expect(path).not.toBeNull();
  const exported = await (await import('node:fs/promises')).readFile(path!, 'utf8');
  expect(exported).toContain('SYNTHETIC-P3-SENTINEL');
  expect(exported).not.toContain('SYNTHETIC-P0-SENTINEL');
  expect(exported).not.toContain('SYNTHETIC-P4-SENTINEL');
});

test('rejects a damaged import without replacing a valid active dossier', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'VALID-ACTIVE-DOSSIER');
  await page.getByText('Daten verwalten').click();
  await page.getByLabel('Arbeitsstand importieren').setInputFiles({
    name: 'damaged.json',
    mimeType: 'application/json',
    buffer: Buffer.from('{"schemaVersion":999,"payload":{"p3":"broken"}}'),
  });
  await expect(page.locator('[data-m06-save-status]')).toHaveAttribute('data-save-state', 'unsaved');
  await reloadPersistent(page);
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('VALID-ACTIVE-DOSSIER');
});

test('reports a conflict between two pages and prevents revival after deletion', async ({ context, page }) => {
  await openPersistent(page, moduleUrl);
  const sibling = await context.newPage();
  await sibling.goto(moduleUrl);
  await choosePersistent(sibling);
  await saveP3(page, 'PAGE-A');
  await sibling.getByLabel('Begründung der Prüffahrt').fill('PAGE-B');
  await sibling.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(sibling.locator('[data-m06-save-status]')).toContainText(/geändert|gelöscht/);

  page.on('dialog', (dialog) => dialog.accept());
  await page.getByText('Daten verwalten').click();
  await page.getByRole('button', { name: 'Arbeitsstand dieses Moduls löschen' }).click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gelöscht.');
  await sibling.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(sibling.locator('[data-m06-save-status]')).toContainText(/geändert|gelöscht/);
});
