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

test('records the provenance and redistribution rights of the IUM5 robot asset', async () => {
  const evidence = JSON.parse(
    await readFile('modules/IUM-5-CORE-05/assets/licenses.json', 'utf8'),
  ) as {
    assets: Array<Record<string, string>>;
  };
  const robot = evidence.assets.find((asset) => asset.path === 'delivery-robot.svg');

  expect(robot).toMatchObject({
    path: 'delivery-robot.svg',
    license: 'CC-BY-SA-4.0',
  });
  expect(robot?.source).toContain('Original project asset');
  expect(robot?.rightsHolder).toBeTruthy();
  expect(robot?.changes).toBeTruthy();

  const svg = await readFile('modules/IUM-5-CORE-05/assets/delivery-robot.svg', 'utf8');
  expect(svg).not.toMatch(/<(?:image|foreignObject)\b/i);
  expect(svg).not.toMatch(/(?:href|src)=["'](?:https?:|data:)/i);
});
