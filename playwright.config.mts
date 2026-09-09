import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/browser',
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4321',
    trace: 'retain-on-failure',
  },
  webServer: process.env.IUM_MANAGED_PREVIEW === '1' ? undefined : {
    command: 'node --import tsx scripts/preview-portal.ts fixture device-fixture / 4321',
    url: 'http://127.0.0.1:4321/',
    reuseExistingServer: false,
    timeout: 120_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        launchOptions: process.platform === 'win32'
          ? { env: { ...process.env, MOZ_DISABLE_CONTENT_SANDBOX: '1' } }
          : undefined,
      },
    },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
