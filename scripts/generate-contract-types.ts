import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { compile } from 'json-schema-to-typescript';

const CHECK_FLAG = '--check';
const banner = `/*
 * Generated from the canonical Phase-1 JSON Schema.
 * Do not edit by hand; run npm run contracts:generate.
 */`;

const contracts = [
  {
    schema: 'schemas/module-manifest.schema.json',
    output: 'packages/module-contract/src/generated/module-manifest.d.ts',
    name: 'ModuleManifest',
  },
  {
    schema: 'schemas/learning-state-envelope.schema.json',
    output: 'packages/module-contract/src/generated/learning-state-envelope.d.ts',
    name: 'LearningStateEnvelope',
  },
] as const;

async function generateContract(
  schemaPath: string,
  outputPath: string,
  name: string,
  check: boolean,
): Promise<void> {
  const absoluteSchema = resolve(schemaPath);
  const absoluteOutput = resolve(outputPath);
  const schema = JSON.parse(await readFile(absoluteSchema, 'utf8')) as object;
  const generated = await compile(schema, name, {
    additionalProperties: false,
    bannerComment: banner,
    cwd: dirname(absoluteSchema),
    enableConstEnums: false,
    style: {
      bracketSpacing: true,
      printWidth: 100,
      semi: true,
      singleQuote: true,
      tabWidth: 2,
      trailingComma: 'all',
      useTabs: false,
    },
    unknownAny: true,
  });
  const bytes = generated.replaceAll('\r\n', '\n');

  if (check) {
    let current: string;
    try {
      current = await readFile(absoluteOutput, 'utf8');
    } catch {
      throw new Error(`Generated contract is missing: ${outputPath}`);
    }
    if (current !== bytes) {
      throw new Error(`Generated contract has drifted: ${outputPath}`);
    }
    return;
  }

  await mkdir(dirname(absoluteOutput), { recursive: true });
  await writeFile(absoluteOutput, bytes, 'utf8');
}

async function main(): Promise<void> {
  const check = process.argv.slice(2).includes(CHECK_FLAG);
  for (const contract of contracts) {
    await generateContract(contract.schema, contract.output, contract.name, check);
  }
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
