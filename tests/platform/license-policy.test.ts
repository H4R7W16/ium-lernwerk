import { readFile } from 'node:fs/promises';
import { expect, test } from 'vitest';

test('reviews every platform-specific sharp libvips package as build-only', async () => {
  const policy = JSON.parse(await readFile('license-policy.json', 'utf8')) as {
    reviewedExceptions: Array<Record<string, string>>;
  };

  expect(policy.reviewedExceptions).toContainEqual({
    namePattern: '^@img/sharp-libvips-',
    license: 'LGPL-3.0-or-later',
    scope: 'build-only',
    rationale: 'Platform-specific libvips package used only to generate local build assets; not shipped in the static portal.',
  });
});
