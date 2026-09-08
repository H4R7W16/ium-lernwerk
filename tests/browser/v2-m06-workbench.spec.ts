import { expect, test, type Page } from '@playwright/test';
import { chooseVolatile } from './helpers/storage-choice.js';

const moduleUrl = '/module/v2-g5-m06/';

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
