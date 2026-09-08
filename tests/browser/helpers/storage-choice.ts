import type { Page } from '@playwright/test';

export async function choosePersistent(page: Page): Promise<void> {
  await page.getByRole('button', { name: 'Auf diesem Gerät speichern' }).click();
}

export async function chooseVolatile(page: Page): Promise<void> {
  await page.getByRole('button', { name: 'Nur in dieser Sitzung arbeiten' }).click();
}

export async function openPersistent(
  page: Page,
  url: string,
  options?: Parameters<Page['goto']>[1],
): Promise<void> {
  await page.goto(url, options);
  await choosePersistent(page);
}

export async function reloadPersistent(
  page: Page,
  options?: Parameters<Page['reload']>[0],
): Promise<void> {
  await page.reload(options);
  await choosePersistent(page);
}
