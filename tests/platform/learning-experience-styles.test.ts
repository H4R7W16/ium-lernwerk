import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { describe, expect, test } from 'vitest';

const packageRoot = fileURLToPath(new URL('../../packages/learning-experience/', import.meta.url));
const tokensPath = fileURLToPath(new URL('src/styles/tokens.css', new URL(`file:///${packageRoot.replaceAll('\\', '/')}/`)));
const foundationPath = fileURLToPath(new URL('src/styles/foundation.css', new URL(`file:///${packageRoot.replaceAll('\\', '/')}/`)));
const motionPath = fileURLToPath(new URL('src/styles/motion.css', new URL(`file:///${packageRoot.replaceAll('\\', '/')}/`)));
const patternsPath = fileURLToPath(new URL('src/styles/patterns.css', new URL(`file:///${packageRoot.replaceAll('\\', '/')}/`)));
const indexPath = fileURLToPath(new URL('src/styles/index.css', new URL(`file:///${packageRoot.replaceAll('\\', '/')}/`)));

function channel(value: number): number {
  const normalized = value / 255;
  return normalized <= 0.04045
    ? normalized / 12.92
    : ((normalized + 0.055) / 1.055) ** 2.4;
}

function luminance(hex: string): number {
  const value = hex.replace('#', '');
  const channels = [0, 2, 4].map((offset) => channel(Number.parseInt(value.slice(offset, offset + 2), 16)));
  return (0.2126 * channels[0]!) + (0.7152 * channels[1]!) + (0.0722 * channels[2]!);
}

function contrast(left: string, right: string): number {
  const [lighter, darker] = [luminance(left), luminance(right)].sort((a, b) => b - a) as [number, number];
  return (lighter + 0.05) / (darker + 0.05);
}

describe('learning experience semantic styles', () => {
  test('publishes the approved semantic palette and typography roles', async () => {
    const css = await readFile(tokensPath, 'utf8');

    expect(css).toContain('--lx-color-canvas: #f7f5f0');
    expect(css).toContain('--lx-color-surface: #ffffff');
    expect(css).toContain('--lx-color-ink: #17212b');
    expect(css).toContain('--lx-color-action: #005a70');
    expect(css).toContain('--lx-color-focus: #d97706');
    expect(css).toContain('--lx-font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif');
    expect(css).toContain('--lx-font-code: ui-monospace, "Cascadia Mono", Consolas, monospace');
    expect(css).toContain('--lx-measure-reading: 68ch');
  });

  test.each([
    ['canvas/ink', '#f7f5f0', '#17212b', 7],
    ['surface/ink', '#ffffff', '#17212b', 7],
    ['action/white', '#005a70', '#ffffff', 4.5],
    ['info', '#0b3a82', '#eaf2ff', 4.5],
    ['confirmed', '#246b47', '#eaf6ee', 4.5],
    ['warning', '#7a4b00', '#fff4d6', 4.5],
    ['danger', '#9b1c31', '#fdecef', 4.5],
    ['focus/white', '#d97706', '#ffffff', 3],
    ['focus/ink', '#d97706', '#17212b', 3],
  ])('keeps %s above its minimum contrast', (_name, foreground, background, minimum) => {
    expect(contrast(foreground, background)).toBeGreaterThanOrEqual(minimum);
  });

  test('defines focus, readable measure and minimum target behavior', async () => {
    const css = await readFile(foundationPath, 'utf8');

    expect(css).toMatch(/:focus-visible\s*\{[^}]*outline:\s*3px\s+solid\s+var\(--lx-color-focus\)/s);
    expect(css).toContain('max-inline-size: var(--lx-measure-reading)');
    expect(css).toContain('min-block-size: 2.75rem');
    expect(css).toContain('min-inline-size: 2.75rem');
    expect(css).toContain('container-type: inline-size');
    expect(css).toContain('container-name: experience');
  });

  test('removes nonessential motion when requested', async () => {
    const css = await readFile(motionPath, 'utf8');

    expect(css).toMatch(/prefers-reduced-motion:\s*reduce/);
    expect(css).toContain('animation-duration: 0.01ms');
    expect(css).toContain('transition-duration: 0.01ms');
    expect(css).toContain('scroll-behavior: auto');
  });

  test('defines compact, standard and wide experience containers', async () => {
    const css = await readFile(patternsPath, 'utf8');

    expect(css).toContain('@container experience (max-width: 39.999rem)');
    expect(css).toContain('@container experience (min-width: 40rem) and (max-width: 69.999rem)');
    expect(css).toContain('@container experience (min-width: 70rem)');
  });

  test('publishes the style layers in deterministic order', async () => {
    const css = await readFile(indexPath, 'utf8');

    expect(css.trim().split(/\r?\n/)).toEqual([
      "@import './tokens.css';",
      "@import './foundation.css';",
      "@import './motion.css';",
      "@import './patterns.css';",
    ]);
  });
});
