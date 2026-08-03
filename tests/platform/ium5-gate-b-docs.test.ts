import { readFile } from 'node:fs/promises';
import { expect, test } from 'vitest';

const root = 'pilot/ium5-gate-b/docs';

async function document(name: string): Promise<string> {
  const source = await readFile(`${root}/${name}`, 'utf8').catch(() => '');
  expect(source, `${name} is missing`).not.toBe('');
  return source;
}

function headings(source: string): string[] {
  return [...source.matchAll(/^## (.+)$/gm)].map((match) => match[1]!);
}

function withoutProhibitedExamples(source: string): string {
  return source.replace(
    /<!-- PRIVACY-PROHIBITED-EXAMPLES:START -->[\s\S]*?<!-- PRIVACY-PROHIBITED-EXAMPLES:END -->/g,
    '',
  );
}

test('technical runbook is a closed execution and cleanup checklist', async () => {
  const source = await document('technical-runbook.md');
  expect(headings(source)).toEqual([
    'Zweck und Nichtfreigabegrenze',
    'Autorisierungsprüfung',
    'Exakte Buildidentität',
    'Veröffentlichung und Rollback',
    'Technische Sechs-Zeilen-Matrix',
    'Evidenzhygiene',
    'Begrenzte Ausnahme',
    'Abbruchbedingungen',
    'Löschung und Übergabe',
  ]);
  expect(source.match(/TECH-[A-Z-]+/g)).toEqual([
    'TECH-IPAD-TOUCH',
    'TECH-IPAD-VO',
    'TECH-DESKTOP-CHROMIUM',
    'TECH-DESKTOP-FIREFOX',
    'TECH-NET-OFFLINE-UPDATE',
    'TECH-LMS-ROUTE',
  ]);
  expect(source).toContain('public-url-control: link-is-not-access-control');
  expect(source).toContain('retention: 30-days-after-decision');
  expect(source).toContain('status-mutation: forbidden');
  expect(source).toContain('workflow-execution-authorized: false');
});

test('pilot guide binds two different classes to the complete observation contract', async () => {
  const source = await document('pilot-guide.md');
  expect(headings(source)).toEqual([
    'Zweck und Grenze der Aussagekraft',
    'Rollen',
    'Eintrittscheckliste',
    'Explorative Durchführung: regular-225',
    'Reparatur-Checkpoint',
    'Bestätigung: extended-270',
    'Neun Beobachtungen',
    'Optionale Drei-Fragen-Rückmeldung',
    'Abbruch und Fallback',
    'Aggregation, Vernichtung und Löschung',
  ]);
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
    'clarity',
    'cognitive-engagement',
    'support-usefulness',
  ]) {
    expect(source).toContain(`\`${id}\``);
  }
  expect(source).toContain('class-relation: different-class-required');
  expect(source).toContain('retention: 30-days-after-decision');
});

test('review guide separates evidence classes, precedence and decisions', async () => {
  const source = await document('review-guide.md');
  expect(headings(source)).toEqual([
    'Evidenzklassen',
    'Buildkonsistenz',
    'Datenschutzvorrang',
    'Regeln für pass, revise und not-evaluable',
    'Vier-Augen-Reviewfolge',
    'Getrennte Pilot-, LMS- und Freigabeentscheidungen',
    'Zulässige abschließende Empfehlung',
  ]);
  for (const value of [
    'pass',
    'revise-required',
    'not-evaluable',
    'limited-accepted',
    'pilot-decision',
    'lms-decision',
    'working-release-review',
    'eligible-for-working-release-review',
  ]) {
    expect(source).toContain(`\`${value}\``);
  }
});

test('guides never instruct collection of identifying or learner-level evidence', async () => {
  const combined = withoutProhibitedExamples([
    await document('technical-runbook.md'),
    await document('pilot-guide.md'),
    await document('review-guide.md'),
  ].join('\n'));
  expect(combined).not.toMatch(/(?:^|\n)\s*(?:Name|Schule|Klasse|Datum)\s*:/i);
  expect(combined).not.toMatch(
    /Freitext|Screenshot der Lernenden|IP-Adresse|Geräte-ID|Einzelantwort/i,
  );
});
