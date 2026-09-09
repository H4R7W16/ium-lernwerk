import { readFile } from 'node:fs/promises';
import { parseDocument } from 'yaml';
import { expect, test } from 'vitest';

type WorkflowStep = {
  'continue-on-error'?: boolean;
  env?: Record<string, string>;
  id?: string;
  name?: string;
  uses?: string;
  run?: string;
  with?: Record<string, unknown>;
};

type WorkflowJob = {
  if?: string;
  needs?: string;
  permissions?: Record<string, string>;
  environment?: { name?: string; url?: string };
  steps?: WorkflowStep[];
  'runs-on'?: string;
};

test('publishes the synthetic device fixture manually with least privilege', async () => {
  const source = await readFile('.github/workflows/device-fixture-pages.yml', 'utf8')
    .catch(() => '');
  expect(source, 'device fixture Pages workflow is missing').not.toBe('');
  if (!source) return;

  const document = parseDocument(source);
  expect(document.errors).toEqual([]);
  const workflow = document.toJS() as {
    on: {
      workflow_dispatch: {
        inputs: Record<string, Record<string, unknown>>;
      };
    };
    concurrency: { group?: string; 'cancel-in-progress'?: boolean };
    jobs: Record<string, WorkflowJob>;
  };

  expect(Object.keys(workflow.on)).toEqual(['workflow_dispatch']);
  expect(workflow.on.workflow_dispatch.inputs.build_revision).toEqual({
    description: 'Synthetic revision for a controlled device update',
    required: true,
    type: 'string',
  });
  expect(workflow.on.workflow_dispatch.inputs.candidate_mode).toEqual({
    description: 'Candidate integrity for the fail-closed device check',
    required: true,
    default: 'valid',
    type: 'choice',
    options: ['valid', 'broken-missing-offline'],
  });
  expect(workflow.concurrency).toEqual({
    group: 'pages',
    'cancel-in-progress': false,
  });
  expect(Object.keys(workflow.jobs)).toEqual(['build', 'deploy']);

  const build = workflow.jobs.build!;
  expect(build.if).toBe("github.ref == 'refs/heads/main'");
  expect(build.permissions).toEqual({ contents: 'read' });
  const buildUses = build.steps?.flatMap((step) => step.uses ?? []) ?? [];
  expect(buildUses).toEqual([
    'actions/checkout@v6',
    'actions/setup-node@v5',
    'actions/configure-pages@v5',
    'actions/upload-pages-artifact@v4',
  ]);
  const buildCommands = build.steps?.flatMap((step) => step.run ?? []) ?? [];
  expect(buildCommands).toEqual([
    'npm ci',
    'npm run test:platform',
    'npm run build:fixture:subpath',
    'npm run quality:build',
    'npm exec -- tsx scripts/prepare-device-candidate.ts apps/lernwerk-portal/dist ${{ inputs.candidate_mode }}',
    "! grep -q 'self.__WB_MANIFEST' apps/lernwerk-portal/dist/sw.js",
  ]);
  expect(source).not.toContain('npm run build\n');
  expect(source).not.toContain('npm run build:ium5');
  expect(source).not.toContain('IUM-5-CORE-05');
  expect(source).not.toContain('algorithm-workbench');
  expect(
    build.steps?.find((step) => step.name === 'Build synthetic subpath fixture')?.env,
  ).toEqual({
    IUM_BUILD_REVISION: '${{ inputs.build_revision }}',
  });
  expect(build.steps?.at(-1)?.with).toEqual({
    path: 'apps/lernwerk-portal/dist',
  });

  const deploy = workflow.jobs.deploy!;
  expect(deploy.needs).toBe('build');
  expect(deploy.if).toBe("github.ref == 'refs/heads/main'");
  expect(deploy.permissions).toEqual({
    contents: 'read',
    pages: 'write',
    'id-token': 'write',
  });
  expect(deploy.environment).toEqual({
    name: 'github-pages',
    url: '${{ steps.deployment.outputs.page_url }}',
  });
  expect(deploy.steps).toEqual([
    {
      name: 'Deploy GitHub Pages',
      id: 'deployment',
      uses: 'actions/deploy-pages@v4',
    },
  ]);

  expect(workflow).toEqual({
    name: 'Device fixture Pages',
    on: {
      workflow_dispatch: {
        inputs: {
          build_revision: {
            description: 'Synthetic revision for a controlled device update',
            required: true,
            type: 'string',
          },
          candidate_mode: {
            description: 'Candidate integrity for the fail-closed device check',
            required: true,
            default: 'valid',
            type: 'choice',
            options: ['valid', 'broken-missing-offline'],
          },
        },
      },
    },
    concurrency: { group: 'pages', 'cancel-in-progress': false },
    jobs: {
      build: {
        if: "github.ref == 'refs/heads/main'",
        permissions: { contents: 'read' },
        'runs-on': 'ubuntu-latest',
        steps: [
          { name: 'Check out main', uses: 'actions/checkout@v6' },
          {
            name: 'Set up Node.js',
            uses: 'actions/setup-node@v5',
            with: { 'node-version': '22.20.0', cache: 'npm' },
          },
          { name: 'Install locked dependencies', run: 'npm ci' },
          { name: 'Verify platform contracts', run: 'npm run test:platform' },
          {
            name: 'Build synthetic subpath fixture',
            env: { IUM_BUILD_REVISION: '${{ inputs.build_revision }}' },
            run: 'npm run build:fixture:subpath',
          },
          { name: 'Verify build budgets and isolation', run: 'npm run quality:build' },
          {
            name: 'Prepare explicit device candidate',
            run: 'npm exec -- tsx scripts/prepare-device-candidate.ts apps/lernwerk-portal/dist ${{ inputs.candidate_mode }}',
          },
          {
            name: 'Reject an unfinalized service worker',
            run: "! grep -q 'self.__WB_MANIFEST' apps/lernwerk-portal/dist/sw.js",
          },
          { name: 'Configure GitHub Pages', uses: 'actions/configure-pages@v5' },
          {
            name: 'Upload GitHub Pages artifact',
            uses: 'actions/upload-pages-artifact@v4',
            with: { path: 'apps/lernwerk-portal/dist' },
          },
        ],
      },
      deploy: {
        if: "github.ref == 'refs/heads/main'",
        needs: 'build',
        permissions: { contents: 'read', pages: 'write', 'id-token': 'write' },
        environment: {
          name: 'github-pages',
          url: '${{ steps.deployment.outputs.page_url }}',
        },
        'runs-on': 'ubuntu-latest',
        steps: [
          {
            name: 'Deploy GitHub Pages',
            id: 'deployment',
            uses: 'actions/deploy-pages@v4',
          },
        ],
      },
    },
  });
});

test('publishes the IUM5 Gate-B non-release preview only through its manual contract', async () => {
  const source = await readFile('.github/workflows/ium5-gate-b-preview.yml', 'utf8')
    .catch(() => '');
  expect(source, 'IUM5 Gate-B Pages workflow is missing').not.toBe('');
  if (!source) return;

  const document = parseDocument(source);
  expect(document.errors).toEqual([]);
  const workflow = document.toJS() as {
    on: {
      workflow_dispatch: {
        inputs: Record<string, Record<string, unknown>>;
      };
    };
    concurrency: { group?: string; 'cancel-in-progress'?: boolean };
    jobs: Record<string, WorkflowJob>;
  };

  expect(Object.keys(workflow.on)).toEqual(['workflow_dispatch']);
  expect(workflow.on.workflow_dispatch.inputs).toEqual({
    acknowledge_non_release: {
      description: 'I acknowledge that this is not a teaching or product release',
      required: true,
      type: 'boolean',
    },
    preview_id: {
      description: 'Closed Gate-B preview identifier',
      required: true,
      type: 'string',
    },
  });
  expect(workflow.concurrency).toEqual({
    group: 'pages',
    'cancel-in-progress': false,
  });
  expect(Object.keys(workflow.jobs)).toEqual(['build', 'deploy']);

  const build = workflow.jobs.build!;
  expect(build.if?.replace(/\s+/g, ' ').trim()).toBe(
    "github.ref == 'refs/heads/main' && inputs.acknowledge_non_release == true",
  );
  expect(build.permissions).toEqual({ contents: 'read' });
  expect(build['runs-on']).toBe('ubuntu-latest');
  expect(build.steps?.flatMap((step) => step.run ?? [])).toEqual([
    "node -e \"if (!/^ium5-gate-b-[a-z0-9-]{8,48}$/.test(process.env.PREVIEW_ID ?? '')) process.exit(1)\"",
    'npm ci',
    'npm run verify:ium5',
    'npm run verify:ium5:gate-b',
    'npm run build:gate-b-preview',
    'npm run quality:build',
  ]);
  expect(build.steps?.flatMap((step) => step.uses ?? [])).toEqual([
    'actions/checkout@v6',
    'actions/setup-node@v5',
    'actions/configure-pages@v5',
    'actions/upload-pages-artifact@v4',
  ]);
  expect(build.steps?.filter((step) => step.env)).toEqual([
    {
      name: 'Validate Preview-ID',
      env: { PREVIEW_ID: '${{ inputs.preview_id }}' },
      run: "node -e \"if (!/^ium5-gate-b-[a-z0-9-]{8,48}$/.test(process.env.PREVIEW_ID ?? '')) process.exit(1)\"",
    },
    {
      name: 'Build Gate-B preview',
      env: {
        IUM_BUILD_REVISION: '${{ github.sha }}',
        IUM_PREVIEW_ID: '${{ inputs.preview_id }}',
      },
      run: 'npm run build:gate-b-preview',
    },
  ]);
  expect(build.steps?.at(-1)?.with).toEqual({
    path: 'apps/lernwerk-portal/dist',
  });

  const deploy = workflow.jobs.deploy!;
  expect(deploy.needs).toBe('build');
  expect(deploy.if).toBe("github.ref == 'refs/heads/main'");
  expect(deploy.permissions).toEqual({
    contents: 'read',
    pages: 'write',
    'id-token': 'write',
  });
  expect(deploy.environment).toEqual({
    name: 'github-pages',
    url: '${{ steps.deployment.outputs.page_url }}',
  });
  expect(deploy.steps).toEqual([
    {
      name: 'Deploy GitHub Pages',
      id: 'deployment',
      uses: 'actions/deploy-pages@v4',
    },
  ]);

  expect(source).not.toMatch(/\b(?:schedule|push|pull_request|workflow_run):/);
  expect(source).not.toContain('secrets.');
  expect(source).not.toContain('actions/upload-artifact');
  expect(source).not.toMatch(/module\.yaml|deviceVerified|device-verified|status mutation/i);
  expect(source).not.toContain('pilot/ium5-gate-b');
});

test('CI validates Gate-B and V2 without adding a deployment path or a sixth job', async () => {
  const source = await readFile('.github/workflows/ci.yml', 'utf8');
  const v2Verifier = await readFile('scripts/verify-v2-m06.ts', 'utf8');
  const document = parseDocument(source);
  expect(document.errors).toEqual([]);
  const workflow = document.toJS() as {
    jobs: Record<string, WorkflowJob>;
  };

  expect(Object.keys(workflow.jobs)).toEqual([
    'legacy',
    'contracts-build',
    'browser',
    'offline-quality',
    'v2-m06',
  ]);
  const legacyCommands = workflow.jobs.legacy?.steps?.flatMap((step) => step.run ?? []) ?? [];
  const pythonIndex = legacyCommands.indexOf('npm run test:python');
  expect(legacyCommands.slice(pythonIndex + 1, pythonIndex + 3)).toEqual([
    'python -B scripts/validate_ium5_gate_b.py protocol',
    'python -B scripts/validate_ium5_gate_b.py synthetic',
  ]);

  const contracts = workflow.jobs['contracts-build']!;
  expect(
    contracts.steps?.find((step) => step.run === 'npm run build:gate-b-preview'),
  ).toEqual({
    env: {
      IUM_BUILD_REVISION: '1111111111111111111111111111111111111111',
      IUM_PREVIEW_ID: 'ium5-gate-b-ci-test-0001',
    },
    run: 'npm run build:gate-b-preview',
  });

  expect(source).not.toMatch(/actions\/(?:configure-pages|upload-pages-artifact|deploy-pages)@/);
  for (const job of Object.values(workflow.jobs)) {
    expect(job.permissions ?? {}).not.toHaveProperty('pages');
    expect(job.permissions ?? {}).not.toHaveProperty('id-token');
  }

  const runSteps = Object.values(workflow.jobs)
    .flatMap((job) => job.steps ?? [])
    .flatMap((step) => step.run ?? []);
  expect(runSteps).toContain('npm run verify:v2:m06');
  expect(workflow.jobs['v2-m06']?.steps?.find((step) => step.uses === 'actions/setup-node@v5')?.with)
    .toEqual({ 'node-version': '22.23.2', cache: 'npm' });
  expect(runSteps).toContain('npm install --global npm@10.9.8');
  const v2Steps = workflow.jobs['v2-m06']?.steps ?? [];
  // needs failure normally skips the entire job before any step-level if can run.
  expect(workflow.jobs['v2-m06']?.needs).toBe('contracts-build');
  expect(workflow.jobs['v2-m06']?.if).toBe('always()');
  const verify = v2Steps.find((step) => step.run === 'npm run verify:v2:m06');
  expect(verify).toMatchObject({
    if: 'always()',
    env: {
      IUM_BUILD_REVISION: '${{ github.sha }}',
      IUM_VERIFICATION_RUN_ID: '${{ github.run_id }}-${{ github.run_attempt }}',
    },
  });
  const upload = v2Steps.find((step) => step.uses === 'actions/upload-artifact@v4');
  expect(upload?.with).toMatchObject({
    name: 'v2-m06-verification-${{ github.run_id }}-${{ github.run_attempt }}-${{ github.sha }}',
  });
  expect(String(upload?.with?.path)).toContain('reports/v2-m06/');
  expect(String(upload?.with?.path)).toContain('reports/phase1/');
  expect(v2Steps.find((step) => step.name === 'Install V2 browser matrix')?.['continue-on-error']).toBe(true);
  for (const requiredPath of [
    'tests/browser/v2-storage.spec.ts',
    'tests/browser/v2-update.spec.ts',
    'verify:v2:activation:historical',
    'test:v2:m06:workbench',
    'test:v2:m06:state',
    'test:v2:m06:accessibility',
    'test:v2:m06:offline',
    'refused fallback port',
  ]) expect(v2Verifier).toContain(requiredPath);
});
