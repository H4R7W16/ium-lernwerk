import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { describe, expect, test } from 'vitest';

const componentNames = [
  'ExperienceShell',
  'ContextBand',
  'LearningStateHeader',
  'FocusStage',
  'ActionEdge',
  'JourneyMap',
] as const;

function componentPath(name: string): string {
  return fileURLToPath(new URL(`../../packages/learning-experience/src/components/${name}.astro`, import.meta.url));
}

describe('learning experience primitives', () => {
  test('publishes all six approved primitives', async () => {
    const sources = await Promise.all(componentNames.map((name) => readFile(componentPath(name), 'utf8')));

    expect(sources).toHaveLength(6);
    expect(sources.every((source) => source.trim().length > 0)).toBe(true);
  });

  test('keeps shell slots in context, journey, focus and action order', async () => {
    const source = await readFile(componentPath('ExperienceShell'), 'utf8');
    const indices = ['context', 'journey', 'focus', 'action'].map((name) =>
      source.indexOf(`<slot name="${name}"`));

    expect(indices.every((index) => index >= 0)).toBe(true);
    expect(indices).toEqual([...indices].sort((left, right) => left - right));
  });

  test('uses one focusable labelled region without nesting another main landmark', async () => {
    const source = await readFile(componentPath('FocusStage'), 'utf8');

    expect(source).toContain('<section');
    expect(source).toContain('aria-labelledby={id + \'-heading\'}');
    expect(source).toContain('tabindex="-1"');
    expect(source).not.toContain('<main');
  });

  test('uses ordered journey semantics and native action controls', async () => {
    const journey = await readFile(componentPath('JourneyMap'), 'utf8');
    const action = await readFile(componentPath('ActionEdge'), 'utf8');

    expect(journey).toContain('<ol');
    expect(journey).toContain('aria-label={ariaLabel}');
    expect(journey).toContain('aria-current={item.current ? \'step\' : undefined}');
    expect(action).toContain('<button');
    expect(action).toContain('type="button"');
    expect(action).toContain('<a');
    expect(action).toContain('secondary.length > 2');
  });

  test('contains no positive tabindex, inline click handler or generic button role', async () => {
    const sources = await Promise.all(componentNames.map((name) => readFile(componentPath(name), 'utf8')));
    const combined = sources.join('\n');

    expect(combined).not.toMatch(/tabindex=["'](?:[1-9]|\d{2,})["']/);
    expect(combined).not.toMatch(/on:click=|onclick=/i);
    expect(combined).not.toMatch(/role=["']button["']/i);
  });
});
