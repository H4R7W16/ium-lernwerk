import { gzipSync } from 'node:zlib';
import {
  mkdir,
  readFile,
  readdir,
  stat,
  writeFile,
} from 'node:fs/promises';
import { dirname, relative, resolve, sep } from 'node:path';

const COLD_TRANSFER_LIMIT = 250 * 1024;
const INITIAL_JAVASCRIPT_LIMIT = 100 * 1024;
const PRECACHE_LIMIT = 2 * 1024 * 1024;

export type BuildQualityReport = Readonly<{
  basePath: string;
  coldTransferGzipBytes: number;
  initialJavaScriptGzipBytes: number;
  precacheDecodedBytes: number;
  totalBuildBytes: number;
  thirdPartyUrls: readonly string[];
  nonBaseAwarePaths: readonly string[];
  testIdentifiers: readonly string[];
  violations: readonly string[];
}>;

async function collectFiles(root: string): Promise<string[]> {
  const result: string[] = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) result.push(...await collectFiles(path));
    else if (entry.isFile()) result.push(path);
  }
  return result.sort();
}

function toPosix(value: string): string {
  return value.split(sep).join('/');
}

function routeForHtml(path: string, basePath: string): string {
  if (path === 'index.html') return basePath;
  return `${basePath}${path.replace(/index\.html$/, '')}`;
}

function isExternal(value: string): boolean {
  return /^https?:\/\//i.test(value) || /^\/\//.test(value);
}

function localBuildPath(value: string, route: string, basePath: string): string | null {
  if (!value || value.startsWith('#') || /^(?:data|blob|mailto|tel):/i.test(value)) return null;
  if (isExternal(value)) return null;
  const url = new URL(value, `https://ium.invalid${route}`);
  if (!url.pathname.startsWith(basePath)) return null;
  const withoutBase = url.pathname.slice(basePath.length);
  return decodeURIComponent(withoutBase || 'index.html').replace(/\/$/, '/index.html');
}

function resourceReferences(html: string): string[] {
  const result = new Set<string>();
  for (const tag of html.matchAll(/<(?:script|link|img)\b[^>]*>/gi)) {
    for (const attribute of tag[0].matchAll(/\b(?:src|href)=["']([^"']+)["']/gi)) {
      result.add(attribute[1]!);
    }
  }
  return [...result].sort();
}

function allReferences(source: string): string[] {
  return [...source.matchAll(/\b(?:src|href)=["']([^"']+)["']/gi)]
    .map((match) => match[1]!);
}

function externalRuntimeReferences(source: string): string[] {
  return [...source.matchAll(
    /\b(?:fetch|importScripts?|Request)\s*\(\s*[`"']((?:https?:)?\/\/[^`"']+)/gi,
  )].map((match) => match[1]!);
}

async function readJson(path: string): Promise<Record<string, unknown>> {
  return JSON.parse(await readFile(path, 'utf8')) as Record<string, unknown>;
}

export async function inspectBuild(distDir: string): Promise<BuildQualityReport> {
  const root = resolve(distDir);
  const files = await collectFiles(root);
  const relativeFiles = files.map((path) => toPosix(relative(root, path)));
  const fileSet = new Set(relativeFiles);
  const manifestPath = relativeFiles.find((path) => path.endsWith('.webmanifest'));
  const manifest = manifestPath ? await readJson(resolve(root, manifestPath)) : {};
  const basePath = typeof manifest.scope === 'string' ? manifest.scope : '/';
  const thirdPartyUrls = new Set<string>();
  const nonBaseAwarePaths = new Set<string>();
  const testIdentifiers = new Set<string>();
  const violations = new Set<string>();
  let totalBuildBytes = 0;
  let coldTransferGzipBytes = 0;
  let initialJavaScriptGzipBytes = 0;

  const contents = new Map<string, Buffer>();
  for (const path of relativeFiles) {
    if (path.endsWith('.map') || path.startsWith('reports/')) continue;
    const bytes = await readFile(resolve(root, path));
    contents.set(path, bytes);
    totalBuildBytes += bytes.byteLength;
    if (/\.(?:html|css|js|json|webmanifest)$/i.test(path)) {
      const source = bytes.toString('utf8');
      if (source.includes('TEST-')) testIdentifiers.add(path);
      if (/\.js$/i.test(path)) {
        for (const url of externalRuntimeReferences(source)) thirdPartyUrls.add(url);
        if (/\beval\s*\(/.test(source)) violations.add(`dynamic-code:eval:${path}`);
        if (/\bnew\s+Function\s*\(/.test(source)) violations.add(`dynamic-code:new-function:${path}`);
      } else {
        for (const match of source.matchAll(/(?:https?:\/\/|\/\/)[^\s"'<>]+/g)) {
          thirdPartyUrls.add(match[0]);
        }
      }
    }
  }

  for (const path of relativeFiles.filter((candidate) => candidate.endsWith('.html'))) {
    const html = contents.get(path)!.toString('utf8');
    if (!html.includes('Inhalte CC BY-SA 4.0') || !html.includes('Code MIT')) {
      violations.add(`oer-label:missing:${path}`);
    }
    const route = routeForHtml(path, basePath);
    const coldFiles = new Set<string>([path]);
    const initialJavaScript = new Set<string>();
    for (const reference of allReferences(html)) {
      if (isExternal(reference)) thirdPartyUrls.add(reference);
      if (reference.startsWith('/') && !reference.startsWith(basePath)) {
        nonBaseAwarePaths.add(`${path}:${reference}`);
      }
    }
    for (const reference of resourceReferences(html)) {
      const buildPath = localBuildPath(reference, route, basePath);
      if (!buildPath || !fileSet.has(buildPath)) continue;
      coldFiles.add(buildPath);
      if (buildPath.endsWith('.js')) initialJavaScript.add(buildPath);
      if (buildPath.endsWith('.webmanifest')) {
        const webManifest = await readJson(resolve(root, buildPath));
        const icons = Array.isArray(webManifest.icons) ? webManifest.icons : [];
        for (const icon of icons) {
          if (!icon || typeof icon !== 'object' || !('src' in icon) || typeof icon.src !== 'string') continue;
          const iconPath = localBuildPath(icon.src, basePath, basePath);
          if (iconPath && fileSet.has(iconPath)) coldFiles.add(iconPath);
        }
      }
    }
    const coldBytes = [...coldFiles].reduce(
      (total, resource) => total + gzipSync(contents.get(resource)!, { level: 9 }).byteLength,
      0,
    );
    const javascriptBytes = [...initialJavaScript].reduce(
      (total, resource) => total + gzipSync(contents.get(resource)!, { level: 9 }).byteLength,
      0,
    );
    coldTransferGzipBytes = Math.max(coldTransferGzipBytes, coldBytes);
    initialJavaScriptGzipBytes = Math.max(initialJavaScriptGzipBytes, javascriptBytes);
  }

  const serviceWorkerPath = relativeFiles.find((path) => /(?:^|\/)sw\.js$/.test(path));
  const precachePaths = new Set<string>();
  if (serviceWorkerPath) {
    const serviceWorker = contents.get(serviceWorkerPath)!.toString('utf8');
    for (const match of serviceWorker.matchAll(
      /\{"revision":(?:null|"[^"]*"),"url":"([^"]+)"\}/g,
    )) {
      const buildPath = localBuildPath(match[1]!, basePath, basePath);
      if (buildPath && fileSet.has(buildPath)) precachePaths.add(buildPath);
    }
  }
  const precacheDecodedBytes = [...precachePaths].reduce(
    (total, path) => total + (contents.get(path)?.byteLength ?? 0),
    0,
  );

  const evidencePath = 'asset-licenses.json';
  if (!fileSet.has(evidencePath)) {
    violations.add('license-evidence:missing');
  } else {
    try {
      const evidence = await readJson(resolve(root, evidencePath));
      const assets = Array.isArray(evidence.assets) ? evidence.assets : [];
      const evidencedPaths = new Set(assets.flatMap((asset) => (
        asset && typeof asset === 'object' && 'path' in asset && typeof asset.path === 'string'
          ? [asset.path]
          : []
      )));
      for (const asset of relativeFiles.filter((path) => /\.(?:png|svg)$/i.test(path))) {
        if (!evidencedPaths.has(asset)) violations.add(`license-evidence:missing-asset:${asset}`);
      }
    } catch (error) {
      violations.add(`license-evidence:invalid:${String(error)}`);
    }
  }

  if (coldTransferGzipBytes > COLD_TRANSFER_LIMIT) violations.add('budget:cold-transfer');
  if (initialJavaScriptGzipBytes > INITIAL_JAVASCRIPT_LIMIT) violations.add('budget:initial-javascript');
  if (precacheDecodedBytes > PRECACHE_LIMIT) violations.add('budget:precache-decoded');
  for (const url of thirdPartyUrls) violations.add(`third-party-url:${url}`);
  for (const path of nonBaseAwarePaths) violations.add(`non-base-aware:${path}`);
  const fixtureRoutePresent = relativeFiles.some(
    (path) => path.startsWith('module/test-platform-reference/'),
  );
  if (!fixtureRoutePresent && testIdentifiers.size > 0) {
    violations.add('production-output:test-identifier');
  }

  return {
    basePath,
    coldTransferGzipBytes,
    initialJavaScriptGzipBytes,
    precacheDecodedBytes,
    totalBuildBytes,
    thirdPartyUrls: [...thirdPartyUrls].sort(),
    nonBaseAwarePaths: [...nonBaseAwarePaths].sort(),
    testIdentifiers: [...testIdentifiers].sort(),
    violations: [...violations].sort(),
  };
}

async function main(): Promise<void> {
  const distDir = resolve(process.argv[2] ?? 'apps/lernwerk-portal/dist');
  const report = await inspectBuild(distDir);
  const reportPath = resolve('reports/phase1/build-quality.json');
  await mkdir(dirname(reportPath), { recursive: true });
  await writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(report, null, 2));
  if (report.violations.length > 0) process.exitCode = 1;
}

if (process.argv[1]?.endsWith('check-build-output.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
