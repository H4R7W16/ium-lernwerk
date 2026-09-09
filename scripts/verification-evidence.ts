import { createHash, randomUUID } from 'node:crypto';
import { copyFileSync, cpSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const sha256 = (bytes: string | Buffer) => createHash('sha256').update(bytes).digest('hex');
export const writeEvidence = (path: string, value: unknown) => writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);

export function createRunDirectory(parent: string, label: string): string {
  const directory = resolve(parent, `${label.replace(/[^a-zA-Z0-9_-]/g, '-').slice(0, 100)}-${randomUUID()}`);
  mkdirSync(directory, { recursive: true });
  return directory;
}

export function archiveBuild(runDirectory: string, outputDir: string,
  identity: { revision: string; sourceRevision?: string; profile: string; base: string }) {
  const directory = createRunDirectory(resolve(runDirectory, 'builds'), identity.profile);
  const files: { path: string; sha256: string; bytes: number }[] = [];
  const walk = (relative = '') => {
    for (const entry of readdirSync(resolve(outputDir, relative), { withFileTypes: true })) {
      if (entry.name === '.vite-cache') continue;
      const path = relative ? `${relative}/${entry.name}` : entry.name;
      if (entry.isSymbolicLink()) throw new Error(`Build evidence refuses symlink: ${path}`);
      if (entry.isDirectory()) { walk(path); continue; }
      const source = resolve(outputDir, path);
      const bytes = readFileSync(source);
      const target = resolve(directory, 'files', path);
      mkdirSync(dirname(target), { recursive: true });
      copyFileSync(source, target);
      if (sha256(readFileSync(target)) !== sha256(bytes)) throw new Error(`Build changed during archival: ${path}`);
      files.push({ path, sha256: sha256(bytes), bytes: bytes.length });
    }
  };
  walk();
  if (!files.length) throw new Error('Empty build cannot produce evidence');
  files.sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  const digest = sha256(files.map((file) => `${file.path}\n${file.sha256}`).join('\n'));
  const manifest = resolve(directory, 'manifest.json');
  writeEvidence(manifest, { schemaVersion: 1, ...identity, runDirectory, stepId: process.env.IUM_VERIFICATION_STEP_ID ?? null,
    createdAt: new Date().toISOString(), node: process.version, sha256: digest,
    algorithm: 'SHA-256 of UTF-8 LF-joined sorted path + LF + file SHA-256; no final LF; excludes .vite-cache', files });
  return { directory, manifest, sha256: digest };
}

export function browserEvidence(runDirectory: string, label: string, buildManifest: string) {
  const build = JSON.parse(readFileSync(buildManifest, 'utf8')) as { revision: string; sha256: string };
  const directory = createRunDirectory(resolve(runDirectory, 'browser'), label);
  // Native Firefox/WebKit downloads fail at long Windows paths. Keep their work
  // directory short and unique; archive it with the group when the process exits.
  const outputDir = resolve('reports/pw', randomUUID().slice(0, 12));
  writeEvidence(resolve(directory, 'group.json'), { schemaVersion: 1, label, runDirectory,
    stepId: process.env.IUM_VERIFICATION_STEP_ID ?? null, revision: build.revision,
    buildManifest, buildSha256: build.sha256, results: 'results.json', artifacts: 'test-results', originalOutputDir: outputDir, startedAt: new Date().toISOString() });
  return { directory, outputDir, args: ['--output', outputDir, '--reporter', 'list,json'],
    env: { PLAYWRIGHT_JSON_OUTPUT_NAME: resolve(directory, 'results.json') },
    finish: () => {
      if (existsSync(outputDir)) cpSync(outputDir, resolve(directory, 'test-results'), { recursive: true });
    } };
}
