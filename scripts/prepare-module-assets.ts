import { copyFile, mkdir, rm, readFile, writeFile } from 'node:fs/promises';
import { relative, resolve, sep } from 'node:path';
import type { BuildProfile } from './build-module-registry.js';

export type PrepareModuleAssetsOptions = Readonly<{
  profile: BuildProfile;
  rootDir: string;
}>;

function assertInside(expectedParent: string, candidate: string): void {
  const relation = relative(resolve(expectedParent), resolve(candidate));
  if (relation === '..' || relation.startsWith(`..${sep}`)) {
    throw new Error(`Generated module asset path escapes public root: ${candidate}`);
  }
}

export async function prepareModuleAssets(
  options: PrepareModuleAssetsOptions,
): Promise<void> {
  const publicRoot = resolve(options.rootDir, 'apps/lernwerk-portal/public');
  const generatedRoot = resolve(publicRoot, 'generated-modules');
  assertInside(publicRoot, generatedRoot);

  await rm(generatedRoot, { recursive: true, force: true });
  await mkdir(generatedRoot, { recursive: true });

  if (options.profile === 'v2-development') {
    const moduleRoot = resolve(options.rootDir, 'modules-v2/V2-G5-M06');
    const content = JSON.parse(await readFile(resolve(moduleRoot, 'content.json'), 'utf8')) as { materials: { path: string }[] };
    for (const entry of [...content.materials, { path: 'teacher/briefing.md' }]) {
      const source = resolve(moduleRoot, entry.path);
      assertInside(moduleRoot, source);
      const target = resolve(generatedRoot, 'v2-g5-m06', entry.path.replace(/\.md$/, '.html'));
      assertInside(generatedRoot, target);
      await mkdir(resolve(target, '..'), { recursive: true });
      const body = await readFile(source, 'utf8');
      if (entry.path.endsWith('.html')) await copyFile(source, target);
      else await writeFile(target, materialPage(body), 'utf8');
    }
    return;
  }
  if (options.profile === 'fixture') {
    return;
  }

  const source = resolve(
    options.rootDir,
    'modules/IUM-5-CORE-05/assets/delivery-robot.svg',
  );
  const targetDirectory = resolve(generatedRoot, 'ium-5-core-05');
  const target = resolve(targetDirectory, 'delivery-robot.svg');
  assertInside(generatedRoot, target);
  await mkdir(targetDirectory, { recursive: true });
  await copyFile(source, target);
}

// The approved packet uses headings, paragraphs, lists, code and tables only.
// Escape every source character before adding our own HTML; no source HTML executes.
function materialPage(markdown: string): string {
  const escape = (text: string) => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
  const inline = (text: string) => escape(text).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  const lines = markdown.split(/\r?\n/);
  const result: string[] = [];
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    if (line.startsWith('```')) {
      const code: string[] = [];
      while (++index < lines.length && !lines[index].startsWith('```')) code.push(lines[index]);
      result.push(`<pre>${escape(code.join('\n'))}</pre>`);
    } else if (line.startsWith('|')) {
      const rows: string[] = [];
      do {
        if (!/^\|[\s:|\-]+\|$/.test(lines[index])) {
          const tag = rows.length === 0 ? 'th' : 'td';
          rows.push(`<tr>${lines[index].slice(1, -1).split('|').map((cell) => `<${tag}>${inline(cell.trim())}</${tag}>`).join('')}</tr>`);
        }
        index++;
      } while (index < lines.length && lines[index].startsWith('|'));
      index--;
      result.push(`<div class="table"><table>${rows.join('')}</table></div>`);
    } else if (/^(?:- |\d+\. )/.test(line)) {
      const ordered = /^\d/.test(line), tag = ordered ? 'ol' : 'ul';
      const items: string[] = [];
      const pattern = ordered ? /^\d+\. / : /^- /;
      do { items.push(`<li>${inline(lines[index].replace(pattern, ''))}</li>`); index++; }
      while (index < lines.length && pattern.test(lines[index]));
      index--;
      result.push(`<${tag}>${items.join('')}</${tag}>`);
    } else {
      const heading = /^(#{1,6}) (.*)$/.exec(line);
      if (heading) result.push(`<h${heading[1].length}>${inline(heading[2])}</h${heading[1].length}>`);
      else if (line.trim()) result.push(`<p>${inline(line)}</p>`);
    }
  }
  return `<!DOCTYPE html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(lines[0].replace(/^# /, ''))}</title><style>body{font:1.1rem/1.6 system-ui;margin:2rem auto;padding:0 1rem;max-width:58rem;color:#183642}table{border-collapse:collapse;width:100%}td,th{border:1px solid #53636a;padding:.5rem;text-align:left}.table{overflow-x:auto}pre,code{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef5f7}a{color:inherit}@media print{body{margin:0;font-size:11pt}}</style><body><main>${result.join('\n')}</main><footer><p>IuM-Lernwerk · Entwicklungskandidat · Inhalte CC BY-SA 4.0</p></footer></body></html>`;
}
