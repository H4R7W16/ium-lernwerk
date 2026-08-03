import { expect, test } from '@playwright/test';

async function confirmPrediction(
  page: import('@playwright/test').Page,
  position: string,
  direction: string,
  success: 'yes' | 'no' | 'unsure',
): Promise<void> {
  await page.getByLabel('Erwartete Endposition').selectOption(position);
  await page.getByLabel('Erwartete Blickrichtung').selectOption(direction);
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption(success);
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
}

test('builds an algorithm by buttons and requires a prediction before execution', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Nimm auf einfügen' }).click();
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(
    page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'),
  ).toHaveCount(2);
  await page.getByRole('button', { name: 'Befehl 2 nach oben' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' }))
    .toBeDisabled();
  await page.getByLabel('Erwartete Endposition').selectOption('A3');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('north');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('unsure');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' }))
    .toBeEnabled();
  await expect(page.locator('[data-prediction-status]')).toContainText(
    'Vorhersage gespeichert – jetzt prüfen',
  );
});

test('predicts, traces, hypothesizes and confirms a repaired algorithm', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await confirmPrediction(page, 'E2', 'east', 'no');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();

  const trace = page.getByRole('table', { name: 'Laufspur' });
  await expect(trace).toContainText('Iteration');
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
    .toContainText('Auftrag noch nicht erfüllt');
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().check();
  await page.getByLabel('Reparaturhypothese').fill(
    'Die Wiederholungszahl ist zu klein. Mit fünf Schritten erreicht der Roboter das Ziel.',
  );
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await page.getByLabel('Wiederholungszahl').fill('5');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeDisabled();

  await page.getByLabel('Begründung zur festen Wiederholung').fill('x'.repeat(501));
  await page.getByRole('button', { name: 'Schleifenentscheidung bestätigen' }).click();
  await expect(page.locator('[data-loop-status]')).toContainText('höchstens 500 Zeichen');
  await page.getByLabel('Begründung zur festen Wiederholung').fill(
    'Fünf Wiederholungen passen, weil die Strecke genau fünf gleichartige Schritte hat.',
  );
  await page.getByRole('button', { name: 'Schleifenentscheidung bestätigen' }).click();
  await expect(page.locator('[data-loop-status]')).toHaveText('Schleifenentscheidung gespeichert.');
});

test('stepwise and complete execution render the same final trace', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await confirmPrediction(page, 'E2', 'east', 'no');
  for (let step = 0; step < 6; step += 1) {
    await page.getByRole('button', { name: 'Schritt ausführen' }).click();
  }
  const stepwiseTrace = await page.getByRole('table', { name: 'Laufspur' })
    .locator('tbody tr').allTextContents();

  await page.reload();
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await confirmPrediction(page, 'E2', 'east', 'no');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  const completeTrace = await page.getByRole('table', { name: 'Laufspur' })
    .locator('tbody tr').allTextContents();
  expect(completeTrace).toEqual(stepwiseTrace);
});

test('moves a correct first draft to the standard repair case without changing it', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Aktives Beispiel öffnen' }).click();
  const correctDraft = await page.getByRole('list', { name: 'Algorithmus' }).innerText();
  await confirmPrediction(page, 'D2', 'east', 'yes');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();

  await expect(page.locator('[data-active-scenario]')).toContainText('repair-standard');
  await expect(page.locator('[data-repair-status]')).toContainText(
    'Eigener Entwurf erfüllt den Auftrag',
  );
  await expect(page.locator('[data-preserved-draft]')).toHaveText(correctDraft);
});

test('shows cause and state before an optional strategy hint', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Drehung öffnen' }).click();
  await confirmPrediction(page, 'C2', 'east', 'no');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();

  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
    .toContainText(/Schritt .*Blickrichtung/);
  await expect(page.getByRole('button', { name: 'Strategiehinweis öffnen' }))
    .toBeVisible();
  await expect(page.getByText('Vollständiges Beispiel', { exact: true })).toBeHidden();
});

for (const [button, cause] of [
  ['Fehlerfall Reihenfolge öffnen', 'Aufnahme ungültig'],
  ['Fehlerfall Fehlender Schritt öffnen', 'Ablage ungültig'],
] as const) {
  test(`shows the specific cause for ${button}`, async ({ page }) => {
    await page.goto('/module/ium-5-core-05/');
    await page.getByRole('button', { name: button }).click();
    await confirmPrediction(page, 'A1', 'north', 'no');
    await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
    await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
      .toContainText(cause);
  });
}

test('reports an obstacle and the hard step limit through button-built algorithms', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Rechts drehen einfügen' }).click();
  for (let index = 0; index < 4; index += 1) {
    await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  }
  await confirmPrediction(page, 'E4', 'east', 'no');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
    .toContainText('Hindernis');

  await page.reload();
  await page.getByRole('button', { name: 'Links drehen einfügen' }).evaluate(
    (button) => {
      for (let index = 0; index < 101; index += 1) {
        (button as HTMLButtonElement).click();
      }
    },
  );
  await confirmPrediction(page, 'A4', 'east', 'no');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' }))
    .toContainText('Schrittgrenze');
});

test('rejects an invalid repeat edit before execution', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await page.getByLabel('Wiederholungszahl').fill('1');

  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeDisabled();
  await expect(page.getByRole('alert')).toContainText(
    'Wiederholungszahl muss zwischen 2 und 9 liegen',
  );
});

test('exposes all five task families and the regular five-lesson path', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  for (const [button, heading] of [
    ['Präzisionskontrast öffnen', 'Präzisionskontrast'],
    ['Aktives Beispiel öffnen', 'Aktives Beispiel'],
    ['Gezielte Fehlerfälle öffnen', 'Gezielte Fehlerfälle'],
    ['Eigenen Lieferauftrag öffnen', 'Eigener Lieferauftrag'],
    ['Algorithmus-Lupe öffnen', 'Algorithmus-Lupe'],
  ] as const) {
    await page.getByRole('button', { name: button }).click();
    await expect(page.getByRole('heading', { name: heading, exact: true })).toBeVisible();
  }
  await expect(page.getByText('225 Minuten · 5 Unterrichtseinheiten')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Zusätzliche Fehlerwerkstatt' }))
    .toBeHidden();
});

test('shows the sixth lesson only through the explicit extended path', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/?path=extended');
  await expect(page.getByText('270 Minuten · 6 Unterrichtseinheiten')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Zusätzliche Fehlerwerkstatt' }))
    .toBeVisible();
  await expect(page.getByText('extended-inherited')).not.toBeVisible();
});

test('persists the chosen phase and confirms a destructive scenario switch', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'UE 5 · Transfer' }).click();
  await expect(page.locator('[data-active-phase]')).toContainText('Algorithmus-Lupe');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await confirmPrediction(page, 'E2', 'east', 'no');
  await page.getByRole('button', { name: 'Karte A auswählen' }).click();
  await expect(page.getByRole('heading', { name: 'Aufgabe wechseln?' })).toBeVisible();
  await page.getByRole('button', { name: 'Wechsel bestätigen' }).click();
  await expect(page.locator('[data-active-scenario]')).toContainText('product-a');
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await page.reload();
  await expect(page.locator('[data-active-phase]')).toContainText('Algorithmus-Lupe');
  await expect(page.locator('[data-active-scenario]')).toContainText('product-a');
});
