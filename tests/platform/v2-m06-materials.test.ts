import { cp, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, test } from 'vitest';
import { checkMaterialPacket } from '../../scripts/check-v2-m06-materials.js';

const modulePath = join('modules-v2', 'V2-G5-M06');

describe('V2 M06 material packet', () => {
  test('production materials preserve all 22 approved time segments', async () => {
    const result = await checkMaterialPacket(process.cwd());
    expect(result.issues).toEqual([]);
  });

  test('rejects a missing MAT-08 and a fabricated 270-minute path', async () => {
    const fixture = await mkdtemp(join(tmpdir(), 'ium-v2-m06-materials-'));
    try {
      const target = join(fixture, modulePath);
      await cp(join(process.cwd(), modulePath), target, { recursive: true });
      const contentPath = join(target, 'content.json');
      const content = JSON.parse(await readFile(contentPath, 'utf8')) as {
        materials: { id: string }[];
        segments: { id: string; minutes: number }[];
      };
      content.materials = content.materials.filter((entry) => entry.id !== 'MAT-08');
      const last = content.segments.find((entry) => entry.id === 'T5-22');
      if (last === undefined) throw new Error('fixture segment missing');
      last.minutes += 45;
      await writeFile(contentPath, `${JSON.stringify(content, null, 2)}\n`, 'utf8');

      const result = await checkMaterialPacket(fixture);
      expect(result.issues).toEqual(expect.arrayContaining([
        expect.stringMatching(/MAT-08/),
        expect.stringMatching(/225|T5-22/),
      ]));
    } finally {
      await rm(fixture, { recursive: true, force: true });
    }
  });

  test('separates the learner prompt, teacher solution and readable print route', async () => {
    const [learner, teacher, briefing, print] = await Promise.all([
      readFile(join(modulePath, 'materials', 'own-program.md'), 'utf8'),
      readFile(join(modulePath, 'teacher', 'handbook.md'), 'utf8'),
      readFile(join(modulePath, 'teacher', 'briefing.md'), 'utf8'),
      readFile(join(modulePath, 'print', 'learner.html'), 'utf8'),
    ]);
    const completeS3Code = 'wiederhole 2 [vor; vor; links; vor; links]';
    expect(learner).not.toContain(completeS3Code);
    expect(teacher).toContain(completeS3Code);
    expect(briefing).not.toMatch(/```|^\s*\|/m);
    expect(print).toContain('@page { size: A4 portrait;');
    expect(print).toContain('P0');
    expect(print).toContain('P6');
    expect(print).toContain('vollständigen digitalen Nachweis');
    expect(print).not.toContain(completeS3Code);
    expect(print).not.toMatch(/https?:\/\//);
  });
});
