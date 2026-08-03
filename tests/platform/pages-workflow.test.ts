import { readFile } from 'node:fs/promises';
import { parseDocument } from 'yaml';
import { expect, test } from 'vitest';

type WorkflowStep = {
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
};

test('publishes the synthetic device fixture manually with least privilege', async () => {
  const source = await readFile('.github/workflows/device-fixture-pages.yml', 'utf8')
    .catch(() => '');
  expect(source, 'device fixture Pages workflow is missing').not.toBe('');
  if (!source) return;

  const document = parseDocument(source);
  expect(document.errors).toEqual([]);
  const workflow = document.toJS() as {
    on: Record<string, unknown>;
    concurrency: { group?: string; 'cancel-in-progress'?: boolean };
    jobs: Record<string, WorkflowJob>;
  };

  expect(Object.keys(workflow.on)).toEqual(['workflow_dispatch']);
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
    "! grep -q 'self.__WB_MANIFEST' apps/lernwerk-portal/dist/sw.js",
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
});
