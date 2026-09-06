import { defineConfig, devices } from '@playwright/test';
if(process.env.IUM_DASHBOARD_TEST_SERVER !== 'owned') throw new Error('Browsergate über npm run test:dashboard:browser starten');
export default defineConfig({
  testDir: './tests/dashboard/browser',
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  workers: 1,
  reporter: 'list',
  timeout: 90_000,
  use: { baseURL:`http://127.0.0.1:${process.env.IUM_DASHBOARD_TEST_PORT ?? '4324'}`, trace:'retain-on-failure' },
  projects: [{ name:'chromium', use:{...devices['Desktop Chrome']} }],
});
