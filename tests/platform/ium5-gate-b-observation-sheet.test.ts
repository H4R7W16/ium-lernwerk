import { readFile } from 'node:fs/promises';
import { expect, test } from 'vitest';

const path = 'pilot/ium5-gate-b/print/observation-sheet.html';

async function sheet(): Promise<string> {
  const source = await readFile(path, 'utf8').catch(() => '');
  expect(source, 'observation sheet is missing').not.toBe('');
  return source;
}

function inputTags(source: string): string[] {
  return source.match(/<input\b[^>]*>/g) ?? [];
}

test('print artifact is self-contained A4 with legible closed controls', async () => {
  const source = await sheet();
  expect(source).toContain('@page { size: A4 portrait; margin: 10mm; }');
  expect(source).toMatch(/body\s*{[^}]*font-size:\s*10pt/s);
  expect(source).toMatch(/input\s*{[^}]*(?:inline-size|width):\s*4\.5mm/s);
  expect(source).toMatch(/input\s*{[^}]*(?:block-size|height):\s*4\.5mm/s);
  expect(source).not.toMatch(/<script\b|https?:\/\/|@font-face|<link\b/i);
  expect(source).toContain('IUM5 Gate B - Analoger Beobachtungsbogen');
  expect(source).toContain('Keine Unterrichts- oder Produktfreigabe');
  expect(source).toContain('data-build-field="sha"');
  expect(source).toContain('data-build-field="preview-id"');
});

test('run, observation and phase contracts have exact closed cardinalities', async () => {
  const source = await sheet();
  const inputs = inputTags(source);
  expect(inputs.filter((tag) => /type="radio"/.test(tag))).toHaveLength(48);
  expect(inputs.filter((tag) => /type="checkbox"/.test(tag))).toHaveLength(18);
  expect(inputs.filter((tag) => /name="run-kind"/.test(tag))).toHaveLength(2);
  expect(source.match(/<tr data-observation-id="[^"]+">/g)).toHaveLength(9);
  expect(source.match(/<tr data-phase-id="LESSON-[1-6]">/g)).toHaveLength(6);
  expect(source.match(/data-closed-code="actual-band"/g)).toHaveLength(6);
  expect(source.match(/data-closed-code="deviation"/g)).toHaveLength(6);
  for (const id of [
    'prediction-used',
    'trace-explained',
    'first-deviation-localized',
    'repair-hypothesis',
    'minimal-revision-retested',
    'loop-decision-justified',
    'systems-transfer',
    'support-preserves-thinking',
    'shared-consolidation',
  ]) {
    expect(inputs.filter((tag) => tag.includes(`name="observation-${id}"`))).toHaveLength(4);
  }
});

test('all disruption, support, fallback and abort choices are closed and labelled', async () => {
  const source = await sheet();
  const inputs = inputTags(source);
  const disruptionCodes = inputs
    .filter((tag) => /name="disruption-code"/.test(tag))
    .map((tag) => tag.match(/value="([^"]+)"/)?.[1]);
  expect(disruptionCodes).toEqual([
    'wrong-build',
    'preview-label-missing',
    'startup-failure',
    'interaction-loss',
    'state-loss',
    'import-export-failure',
    'offline-failure',
    'update-failure',
    'screenreader-blocker',
    'keyboard-blocker',
    'touch-blocker',
    'layout-blocker',
    'network-policy-blocker',
    'lms-routing-blocker',
    'unexpected-third-party-request',
    'privacy-contract-breach',
    'instructional-time-collapse',
    'other-closed-review-required',
  ]);
  expect(inputs.filter((tag) => /name="support-demand"/.test(tag))).toHaveLength(4);
  expect(inputs.filter((tag) => /name="fallback-function"/.test(tag))).toHaveLength(4);
  expect(inputs.filter((tag) => /name="abort-action"/.test(tag))).toHaveLength(2);
  for (const tag of inputs) {
    const id = tag.match(/id="([^"]+)"/)?.[1];
    expect(id).toBeDefined();
    expect(source).toContain(`for="${id}"`);
  }
});

test('source is semantic, learner-safe and explains the analog medium', async () => {
  const source = await sheet();
  expect(source.match(/<table\b/g)).toHaveLength(2);
  expect(source.match(/<caption\b/g)).toHaveLength(2);
  expect(source).toContain('scope="col"');
  expect(source).toContain('scope="row"');
  expect(source).not.toMatch(/<input\b[^>]*type="text"|<textarea\b|contenteditable/i);
  expect(source).not.toMatch(
    /Lernenden-ID|Schüler(?:in)?(?:nen)?-ID|E-Mail|Schule\s*:|Klasse\s*:|Freitext/i,
  );
  expect(source).toContain('data-destruction-reminder');
  expect(source).toContain('data-media-rationale');
  expect(source).toContain('nach geprüfter Aggregatübertragung vernichten');
  expect(source).toContain('Aufmerksamkeit während der Beobachtung im Unterricht');
  expect(source).toContain('unabhängig von der geprüften Anwendung');
});
