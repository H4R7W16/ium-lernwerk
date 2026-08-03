import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/browser',
  testMatch: 'ium5-*.spec.ts',
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4322',
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run preview:ium5',
    url: 'http://127.0.0.1:4322/',
    reuseExistingServer: false,
    timeout: 120_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
