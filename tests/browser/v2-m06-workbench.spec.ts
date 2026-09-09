import { expect, test, type Page } from '@playwright/test';
import { chooseVolatile } from './helpers/storage-choice.js';
import { openPersistent, reloadPersistent } from './helpers/storage-choice.js';
import { readFile } from 'node:fs/promises';

const moduleUrl = '/module/v2-g5-m06/';

test('NA04 opens S0 and S1 from their own starts and exposes S2 cause separately from boundary', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await expect(page.locator('[data-case="S0"]')).toContainText('3 × 3');
  await expect(page.locator('[data-case="S0"]')).toContainText('Blick oben');
  await page.locator('[data-example-next="S0"]').click();
  await expect(page.locator('[data-example-trace="S0"]')).toContainText('(1,3) → (1,2)');
  await expect(page.locator('[data-case="S1"]')).toContainText('(2,3)');
  await page.locator('[data-example-next="S1"]').click();
  await expect(page.locator('[data-example-trace="S1"]')).toContainText('(2,3) → (3,3)');
  await page.locator('[data-load-s2]').click();
  await predict(page, '4', '3', 'east');
  await page.locator('[data-run-code]').click();
  await expect(page.locator('[data-trace-output]')).toContainText('Schritt 3');
  await page.locator('[data-compare-s2]').click();
  await expect(page.locator('[data-s2-comparison]')).toContainText('Erste fachliche Abweichung: Aktion 2');
  await expect(page.locator('[data-s2-comparison]')).toContainText('Rastergrenze: Aktion 3');
  await page.locator('[data-trace-output] input[value="2"]').check();
  await page.locator('[data-rationale]').fill('Drehung steht außerhalb des Körpers.');
  await page.locator('[data-first-deviation]').fill('2');
  await page.locator('[data-revision="before"]').click();
  await page.locator('[data-editor="code"] [data-clear]').click();
  await page.locator('#m06-repeat-count').fill('4');
  await page.locator('[data-repeat-body]').nth(0).selectOption('move');
  await page.locator('[data-repeat-body]').nth(1).selectOption('turn-left');
  await page.locator('[data-add-repeat]').click();
  await predict(page, '2', '3', 'east');
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="2"]').check();
  await page.locator('[data-rationale]').fill('vor und links stehen nun im selben Körper.');
  await page.locator('[data-revision="after"]').click();
  const dossier = await exportedDossier(page);
  expect(dossier.p2.before.program).toHaveLength(2);
  expect(dossier.p2.after.program[0].body).toHaveLength(2);
  expect(dossier.p2.firstDeviation).toBe(2);
  await page.locator('[data-m06-save]').click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
  await reloadPersistent(page);
  expect(await exportedDossier(page)).toEqual(dossier);
});

test('NA04 edits framed P1 and P3 diagrams independently and restores all product paths', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.locator('[data-p1-starter]').click();
  await page.locator('[data-p1-body-kind]').selectOption('turn-left');
  await page.locator('[data-p1-body-add]').click();
  await page.locator('[data-p1-explanation]').fill('Der ganze Körper wird viermal wiederholt.');
  await expect(page.locator('[data-graphic="p1"]')).toContainText('Start');
  await expect(page.locator('[data-graphic="p1"]')).toContainText('Ende');
  await expect(page.locator('[data-graphic="p1"] .m06-body-frame')).toContainText('links');
  await page.locator('[data-editor="diagram"] [data-add="move"]').click();
  await page.locator('[data-editor="diagram"] [data-add="turn-left"]').click();
  await page.locator('[data-graphic="diagram"] [data-move-up]').nth(1).click();
  await expect(page.locator('[data-diagram-output]')).toHaveText('links\nvor');
  await expect(page.locator('[data-code-output]')).toHaveText('Noch kein Code eingegeben.');
  await enterReferenceProgram(page);
  await predict(page, '1', '3', 'east');
  await page.locator('[data-run-code]').click();
  await page.locator('[data-trace-output] input[value="10"]').check();
  await page.locator('[data-save-evidence]').click();
  await page.locator('[data-transfer-rationale]').fill('A beginnt jeden Durchlauf frei; B scheitert beim zweiten Aufnehmen.');
  await page.locator('[data-system="timeControl"]').fill('Zeitwert vergleichen und Aktion auslösen.');
  await page.locator('[data-system="routeCalculation"]').fill('Verbindungen verarbeiten.');
  await page.locator('[data-system="boundary"]').fill('Papier verarbeitet nichts; Standbild belegt keinen Ablauf.');
  await page.locator('[data-return-next]').fill('P2 noch prüfen.');
  const before = await exportedDossier(page);
  await page.locator('[data-m06-save]').click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
  await reloadPersistent(page);
  expect(await exportedDossier(page)).toEqual(before);
  await expect(page.locator('[data-graphic="p1"] .m06-body-frame')).toContainText('links');
  await expect(page.locator('[data-transfer-rationale]')).toHaveValue(before.p5.rationale);
});

test('NA04 retrieval hides old work and materials until a deliberate comparison', async ({ page }) => {
  await openM06(page);
  await page.locator('[data-editor="diagram"] [data-add="move"]').click();
  await page.locator('[data-m06-open-retrieval]').click();
  await expect(page.locator('#mein-pruefdossier')).toBeHidden();
  await expect(page.locator('[data-materials]')).toBeHidden();
  await expect(page.locator('[data-case="S1"]')).toBeHidden();
  await expect(page.locator('[data-m06-retrieval-panel]')).toContainText('zwei vollständige Durchläufe');
  await expect(page.locator('[data-retrieval-compare]')).toBeDisabled();
  await page.locator('[data-m06-retrieval]').fill('vor; links / vor; links; vor; links / Blick oben / Unsicher beim Ort.');
  await page.locator('[data-retrieval-compare]').click();
  await expect(page.locator('[data-retrieval-solution]')).toContainText('vor');
  await page.locator('[data-m06-own-draft]').click();
  await expect(page.locator('#mein-pruefdossier')).toBeVisible();
  expect(JSON.stringify(await exportedDossier(page))).not.toContain('Unsicher beim Ort');
});

test('NA04 all ten materials and briefing remain readable offline', async ({ page, context }) => {
  await openM06(page);
  await page.evaluate(async () => { await navigator.serviceWorker.ready; });
  await page.reload();
  await chooseVolatile(page);
  const links = await page.locator('[data-materials] a').evaluateAll((nodes) => nodes.map((node) => (node as HTMLAnchorElement).href));
  expect(links).toHaveLength(11);
  await context.setOffline(true);
  for (const href of links) {
    await page.goto(href);
    await expect(page.locator('body')).not.toBeEmpty();
    await expect(page.locator('body')).toContainText(/MAT-|M06|Prüf|Briefing/);
  }
});

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
