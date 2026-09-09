import { expect, test, type Page } from '@playwright/test';
import { chooseVolatile } from './helpers/storage-choice.js';
import { openPersistent, reloadPersistent } from './helpers/storage-choice.js';
import { readFile } from 'node:fs/promises';

const moduleUrl = '/module/v2-g5-m06/';

async function predict(page: Page, column: string, row: string, direction: string) {
  await page.locator('[data-run-prediction-column]').fill(column);
  await page.locator('[data-run-prediction-row]').fill(row);
  await page.locator('[data-run-prediction-direction]').selectOption(direction);
}

async function exportedDossier(page: Page) {
  const manager = page.locator('[data-m06-management]');
  if (await manager.getAttribute('open') === null) await manager.locator('summary').click();
  const download = page.waitForEvent('download');
  await page.locator('[data-export-work]').click();
  return JSON.parse(await readFile((await (await download).path())!, 'utf8')).payload;
}

test('NA03 removes the old rectangle trace when ten turns replace its code', async ({ page }) => {
  await openM06(page);
  await enterReferenceProgram(page);
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="10"]').check();
  await page.getByRole('button', { name: 'Code leeren', exact: true }).click();
  for (let index = 0; index < 10; index++) await page.locator('[data-editor="code"] [data-add="turn-right"]').click();
  await expect(page.locator('[data-trace-output] input')).toHaveCount(0);
  await expect(page.locator('[data-save-evidence]')).toBeDisabled();
  expect((await exportedDossier(page)).p3.evidence.steps).toEqual([]);
});

test('NA03 persists an explicitly predicted P3 run and never promotes a free or restored run', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await enterReferenceProgram(page);
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="10"]').check();
  await expect(page.locator('[data-save-evidence]')).toBeDisabled();
  await predict(page, '1', '3', 'east');
  await expect(page.locator('[data-trace-output] input')).toHaveCount(0);
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="10"]').check();
  await page.locator('[data-rationale]').fill('Vorhergesagt und anhand Schritt 10 geprüft.');
  await page.locator('[data-save-evidence]').click();
  await page.locator('[data-m06-save]').click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
  await reloadPersistent(page);
  await expect(page.locator('[data-saved-prediction]')).toContainText('(1,3), Blick rechts');
  await expect(page.locator('[data-save-evidence]')).toBeDisabled();
  const dossier = await exportedDossier(page);
  expect(dossier.p3.evidence.predicted).toEqual({ position: { column: 1, row: 3 }, direction: 'east' });
  expect(dossier.p3.evidence.steps).toEqual([10]);
  await page.locator('[data-import-work]').setInputFiles({ name: 'predicted.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ format: 'ium-learning-state', formatVersion: 1, moduleId: 'V2-G5-M06',
      moduleVersion: '0.1.0', stateSchemaVersion: 1, workspaceId: '123e4567-e89b-42d3-a456-426614174000',
      savedAt: '2026-09-09T10:00:00Z', payload: dossier })) });
  await page.locator('[data-confirm-import]').click();
  await expect(page.locator('[data-saved-prediction]')).toContainText('(1,3), Blick rechts');
  await expect(page.locator('[data-save-evidence]')).toBeDisabled();
  expect(await exportedDossier(page)).toEqual(dossier);
  await page.locator('[data-editor="code"] [data-add="turn-right"]').click();
  await expect(page.locator('[data-trace-output] input')).toHaveCount(0);
  await expect(page.locator('[data-save-evidence]')).toBeDisabled();
});

test('NA03 binds S2 before and after to their own predicted programs and clears selection on rerun', async ({ page }) => {
  await openM06(page);
  await page.locator('[data-editor="code"] [data-add="move"]').click();
  await predict(page, '2', '3', 'east');
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="1"]').check();
  await page.locator('[data-run-scenario]').selectOption('S2');
  await expect(page.locator('[data-trace-output] input')).toHaveCount(0);
  await predict(page, '3', '3', 'east');
  await page.locator('[data-run-code]').click();
  await expect(page.locator('[data-trace-output]')).toContainText('(2,3) → (3,3)');
  await page.locator('[data-trace-output] input[value="1"]').check();
  await expect(page.locator('[data-save-evidence]')).toBeDisabled();
  await page.locator('[data-revision="before"]').click();
  await page.getByRole('button', { name: 'Code leeren', exact: true }).click();
  await page.locator('[data-editor="code"] [data-add="turn-left"]').click();
  await predict(page, '2', '3', 'north');
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="1"]').check();
  await page.locator('[data-run-code]').click();
  await expect(page.locator('[data-trace-output] input:checked')).toHaveCount(0);
  await page.locator('[data-trace-output] input[value="1"]').check();
  await page.locator('[data-revision="after"]').click();
  const dossier = await exportedDossier(page);
  expect(dossier.p2.before.program).toEqual([{ id: 'cmd-1', kind: 'move' }]);
  expect(dossier.p2.after.program).toEqual([{ id: 'cmd-1', kind: 'turn-left' }]);
  expect(dossier.p2.before.predicted).toEqual({ position: { column: 3, row: 3 }, direction: 'east' });
  expect(dossier.p2.after.predicted).toEqual({ position: { column: 2, row: 3 }, direction: 'north' });
});

async function openM06(page: Page): Promise<void> {
  await page.goto(moduleUrl);
  await chooseVolatile(page);
}

async function enterReferenceProgram(page: Page): Promise<void> {
  const repeat = page.locator('[data-repeat-editor]');
  for (const [index, command] of ['move', 'move', 'turn-left', 'move', 'turn-left'].entries()) {
    await repeat.locator('select').nth(index).selectOption(command);
  }
  await page.getByRole('button', { name: 'Wiederholung einsetzen' }).click();
}

test('executes the five-command S3 loop and exposes attributable trace steps', async ({ page }) => {
  await openM06(page);
  await page.getByLabel('Meine Vorhersage vor dem Ausführen').fill('(1,3), Blick rechts');
  await enterReferenceProgram(page);
  await page.getByRole('button', { name: 'Code ausführen und Spur anzeigen' }).click();
  await expect(page.getByRole('status').filter({ hasText: 'Ziel, Prüfpunkte und Randfahrt' }))
    .toBeVisible();
  const trace = page.getByRole('group', { name: 'Relevante Spurstellen auswählen' });
  await expect(trace.getByRole('checkbox')).toHaveCount(10);
  await expect(trace).toContainText('Befehl cmd-2, Durchlauf 1');
  await expect(trace).toContainText('(1,3) → (1,3), Blick rechts');
});

test('does not accept an empty program merely because it keeps the initial end state', async ({ page }) => {
  await openM06(page);
  await page.getByRole('button', { name: 'Code ausführen und Spur anzeigen' }).click();
  await expect(page.getByRole('status').filter({ hasText: 'Prüfung noch offen' })).toBeVisible();
  await expect(page.getByRole('group', { name: 'Relevante Spurstellen auswählen' })
    .getByRole('checkbox')).toHaveCount(0);
});

test('keeps diagram and executable code independently editable', async ({ page }) => {
  await openM06(page);
  await page.getByRole('button', { name: 'Pfeil vor' }).click();
  await expect(page.locator('[data-diagram-output]')).toContainText('vor');
  await expect(page.locator('[data-code-output]')).toHaveText('Noch kein Code eingegeben.');
  await page.getByRole('button', { name: 'vor', exact: true }).click();
  await expect(page.locator('[data-code-output]')).toContainText('vor');
  await expect(page.locator('[data-diagram-output]')).toHaveText('vor');
});

test('connects retrieval, S4, S5 and return products without revealing the old solution first', async ({ page }) => {
  await openM06(page);
  await expect(page.getByText('Vergleiche Körper, Anzahl und Zustandsänderungen')).toBeHidden();
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await page.getByLabel('Deine Abrufbegründung').fill('Körper und Anzahl zuerst selbst erinnern.');
  await page.getByRole('button', { name: 'Zum eigenen Entwurf' }).click();
  await expect(page.locator('#mein-pruefdossier')).toBeFocused();
  await page.getByLabel('Begründung der Zustandsbedingungen').fill('Jeder Durchlauf beginnt ohne Werkstück.');
  await page.getByLabel('Digitale Zeitsteuerung').fill('Ein Zustand wechselt nach Ablauf der Zeit.');
  await page.getByLabel('Digitale Wegberechnung').fill('Position und Blickrichtung bestimmen den nächsten Schritt.');
  await page.getByLabel('Aussagegrenze für Papier und Standbild').fill('Ein Standbild zeigt keine Ausführung.');
  await page.getByLabel('Arbeitsbereich für die Rückkehr').selectOption('dossier');
  await page.getByLabel('Offener Punkt').fill('Revision begründen');
  await page.getByLabel('Nächste eigene Handlung').fill('Spurstellen vergleichen');
});
