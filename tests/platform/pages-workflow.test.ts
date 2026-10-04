import { readFile } from 'node:fs/promises';
import { parseDocument } from 'yaml';
import { expect, test } from 'vitest';

type WorkflowStep = {
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

test('preserves the retired synthetic device fixture build contract', async () => {
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
  expect(deploy.if).toBe('${{ false }}');
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
        if: '${{ false }}',
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

test('preserves the retired IUM5 Gate-B preview build contract', async () => {
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
  expect(deploy.if).toBe('${{ false }}');
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

test('CI validates Gate-B without adding a deployment path or a fifth job', async () => {
  const source = await readFile('.github/workflows/ci.yml', 'utf8');
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
});


test('publishes only the current Klasse 5 export and retires older Pages deployments', async () => {
  const source = await readFile('.github/workflows/klasse5-pages.yml', 'utf8').catch(() => '');
  expect(source, 'Klasse-5-Pages-Workflow fehlt').not.toBe('');
  if (!source) return;
  const document = parseDocument(source);
  expect(document.errors).toEqual([]);
  const workflow = document.toJS() as {
    on: { push: { branches: string[] }; workflow_dispatch: unknown };
    jobs: Record<string, WorkflowJob>;
  };
  expect(Object.keys(workflow.on).sort()).toEqual(['push', 'workflow_dispatch']);
  expect(workflow.on.push.branches).toEqual(['main']);
  expect(Object.keys(workflow.jobs)).toEqual(['build', 'deploy']);
  const build = workflow.jobs.build!;
  expect(build.permissions).toEqual({ contents: 'read' });
  expect(build.steps?.find(step => step.run?.includes('build-class5-pages.cjs'))?.run)
    .toBe('node prototypes/m06-reinigungsfall/build-class5-pages.cjs');
  expect(build.steps?.find(step => step.uses === 'actions/upload-pages-artifact@v4')?.with)
    .toEqual({ path: 'dist/klasse5-pages' });
  const deploy = workflow.jobs.deploy!;
  expect(deploy.needs).toBe('build');
  expect(deploy.permissions).toEqual({ contents: 'read', pages: 'write', 'id-token': 'write' });
  expect(deploy.steps?.at(-1)?.uses).toBe('actions/deploy-pages@v4');
  for (const filename of ['reinigungsfall-pages.yml','selbstlernen-pages.yml','ium5-gate-b-preview.yml','device-fixture-pages.yml']) {
    const old = parseDocument(await readFile('.github/workflows/' + filename, 'utf8'));
    expect(old.errors).toEqual([]);
    expect((old.toJS() as {jobs: Record<string, WorkflowJob>}).jobs.deploy?.if, filename).toBe('${{ false }}');
  }
});
