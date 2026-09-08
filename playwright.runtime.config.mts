import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/browser',
  testMatch: 'v2-storage.spec.ts',
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4321',
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run preview:fixture',
    url: 'http://127.0.0.1:4321/tests/v2-runtime/',
    reuseExistingServer: true,
    timeout: 120_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
