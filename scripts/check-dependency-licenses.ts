import { spawnSync } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

type QueryPackage = Readonly<{
  name?: string;
  version?: string;
  license?: string;
  location?: string;
}>;

type LicenseException = Readonly<{
  name?: string;
  namePattern?: string;
  license: string;
  scope: string;
  rationale: string;
}>;

type LicensePolicy = Readonly<{
  schemaVersion: number;
  baseAllowedExpressions: string[];
  reviewedExceptions: LicenseException[];
}>;

type CycloneComponent = {
  name?: string;
  version?: string;
  purl?: string;
  ['bom-ref']?: string;
};

type CycloneDx = {
  metadata?: { component?: CycloneComponent };
  components?: CycloneComponent[];
};

function npmJson(args: string[]): unknown {
  const npmEntrypoint = process.env.npm_execpath;
  if (!npmEntrypoint) {
    throw new Error('npm_execpath is unavailable; run this gate through npm run quality:licenses');
  }
  const result = spawnSync(process.execPath, [npmEntrypoint, ...args], {
    cwd: process.cwd(),
    encoding: 'utf8',
    maxBuffer: 128 * 1024 * 1024,
  });
  if (result.status !== 0) {
    throw new Error(
      `npm ${args.join(' ')} failed (${result.status ?? 'no status'}):\n`
      + `${result.error?.message ?? ''}${result.stderr ?? ''}`,
    );
  }
  return JSON.parse(result.stdout) as unknown;
}

function packageKey(name: string, version: string): string {
  return `${name}@${version}`;
}

function keyFromPurl(purl: string): string | null {
  if (!purl.startsWith('pkg:npm/')) return null;
  const decoded = decodeURIComponent(purl.slice('pkg:npm/'.length).split(/[?#]/, 1)[0]!);
  const versionSeparator = decoded.lastIndexOf('@');
  if (versionSeparator < 1) return null;
  return packageKey(decoded.slice(0, versionSeparator), decoded.slice(versionSeparator + 1));
}

function matchesException(item: QueryPackage, exception: LicenseException): boolean {
  if (item.license !== exception.license || typeof item.name !== 'string') return false;
  if (exception.name !== undefined) return item.name === exception.name;
  return exception.namePattern !== undefined && new RegExp(exception.namePattern).test(item.name);
}

async function main(): Promise<void> {
  const rootPackage = JSON.parse(await readFile('package.json', 'utf8')) as {
    name: string;
    version: string;
  };
  const policy = JSON.parse(await readFile('license-policy.json', 'utf8')) as LicensePolicy;
  if (policy.schemaVersion !== 1) throw new Error('Unsupported license policy schema');

  // npm 10.9 rejects the plan shorthand `.`; this equivalent selector includes root and all descendants.
  const queried = npmJson(['query', ':root, :root *', '--json']) as QueryPackage[];
  const installed = queried.filter(
    (item): item is QueryPackage & { name: string; version: string } =>
      typeof item.name === 'string' && typeof item.version === 'string',
  );
  const invalid: string[] = [];
  const reviewed: Array<Record<string, string>> = [];
  const packageRows = installed.map((item) => {
    if (typeof item.license !== 'string' || item.license.length === 0) {
      invalid.push(`${packageKey(item.name, item.version)}:missing-license`);
      return { name: item.name, version: item.version, license: null, decision: 'rejected' };
    }
    if (policy.baseAllowedExpressions.includes(item.license)) {
      return { name: item.name, version: item.version, license: item.license, decision: 'base-allowed' };
    }
    const exception = policy.reviewedExceptions.find((candidate) => matchesException(item, candidate));
    if (!exception) {
      invalid.push(`${packageKey(item.name, item.version)}:${item.license}`);
      return { name: item.name, version: item.version, license: item.license, decision: 'rejected' };
    }
    reviewed.push({
      name: item.name,
      version: item.version,
      license: item.license,
      scope: exception.scope,
      rationale: exception.rationale,
    });
    return { name: item.name, version: item.version, license: item.license, decision: 'reviewed-exception' };
  }).sort((left, right) => (
    `${left.name}@${left.version}`.localeCompare(`${right.name}@${right.version}`)
  ));

  const sbom = npmJson(['sbom', '--sbom-format', 'cyclonedx']) as CycloneDx;
  const rootPurl = `pkg:npm/${encodeURIComponent(rootPackage.name)}@${rootPackage.version}`;
  sbom.metadata ??= {};
  sbom.metadata.component ??= {};
  Object.assign(sbom.metadata.component, {
    name: rootPackage.name,
    version: rootPackage.version,
    purl: rootPurl,
    'bom-ref': rootPurl,
  });
  const sbomKeys = new Set(
    (sbom.components ?? []).flatMap((component) => (
      typeof component.purl === 'string' ? [keyFromPurl(component.purl)] : []
    )).filter((key): key is string => key !== null),
  );
  const expectedKeys = new Set(
    installed
      .filter((item) => item.name !== rootPackage.name || item.version !== rootPackage.version)
      .map((item) => packageKey(item.name, item.version)),
  );
  const missingFromSbom = [...expectedKeys].filter((key) => !sbomKeys.has(key)).sort();
  if (missingFromSbom.length > 0) {
    invalid.push(...missingFromSbom.map((key) => `${key}:missing-from-sbom`));
  }

  const report = {
    schemaVersion: 1,
    policy: 'license-policy.json',
    packageCount: expectedKeys.size + 1,
    sbomComponentCount: sbomKeys.size + 1,
    reviewedExceptions: reviewed.sort((left, right) => (
      `${left.name}@${left.version}`.localeCompare(`${right.name}@${right.version}`)
    )),
    invalid: invalid.sort(),
    packages: packageRows,
  };
  const reportPath = resolve('reports/phase1/license-audit.json');
  const sbomPath = resolve('reports/phase1/sbom.cdx.json');
  await mkdir(dirname(reportPath), { recursive: true });
  await writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  await writeFile(sbomPath, `${JSON.stringify(sbom, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    packageCount: report.packageCount,
    sbomComponentCount: report.sbomComponentCount,
    reviewedExceptionCount: reviewed.length,
    invalid: report.invalid,
  }, null, 2));
  if (invalid.length > 0) process.exitCode = 1;
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
