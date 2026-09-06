import { defineConfig } from 'astro/config';
if (!process.env.IUM_DASHBOARD_INPUT || !process.env.IUM_DASHBOARD_OUT) throw new Error('Dashboard über die validierende CLI bauen');
export default defineConfig({
  output: 'static',
  outDir: process.env.IUM_DASHBOARD_OUT,
  build: { format: 'directory', inlineStylesheets: 'always' },
  vite: { build: { emptyOutDir: false } },
});
