import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import type { AstroIntegration } from 'astro';
import { VitePWA } from 'vite-plugin-pwa';

const profile = process.env.IUM_BUILD_PROFILE ?? '';
if (profile !== 'production' && profile !== 'fixture') {
  throw new Error(`Invalid IUM_BUILD_PROFILE: ${profile}`);
}
const base = process.env.IUM_BASE_PATH ?? '';
if (
  !base.startsWith('/')
  || !base.endsWith('/')
  || base.includes('..')
  || /[?#\\]/.test(base)
  || base.includes('://')
) {
  throw new Error(`Invalid IUM_BASE_PATH: ${base}`);
}
const outputDirectory = process.env.IUM_OUTPUT_DIR;
const pwaOutputDirectory = outputDirectory
  ?? resolve(fileURLToPath(new URL('.', import.meta.url)), 'dist');
const pwaPlugins = VitePWA({
  strategies: 'injectManifest',
  srcDir: 'src',
  outDir: pwaOutputDirectory,
  filename: 'sw.ts',
  registerType: 'prompt',
  injectRegister: null,
  includeAssets: [
    'app-icon.svg',
    'asset-licenses.json',
    'icons/pwa-192x192.png',
    'icons/pwa-512x512.png',
    'icons/maskable-512x512.png',
  ],
  manifest: {
    name: 'IuM-Lernwerk',
    short_name: 'IuM-Lernwerk',
    description: 'Modulares digitales Lernwerk für Informatik und Medienbildung',
    lang: 'de',
    dir: 'ltr',
    display: 'standalone',
    start_url: base,
    scope: base,
    background_color: '#f4f7fb',
    theme_color: '#175e75',
    icons: [
      {
        src: `${base}icons/pwa-192x192.png`,
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: `${base}icons/pwa-512x512.png`,
        sizes: '512x512',
        type: 'image/png',
      },
      {
        src: `${base}icons/maskable-512x512.png`,
        sizes: '512x512',
        type: 'image/png',
        purpose: 'maskable',
      },
    ],
  },
  injectManifest: {
    globPatterns: ['**/*.{html,css,js,png,svg,webmanifest}'],
    globIgnores: [
      'app-icon.svg',
      'icons/**',
      'manifest.webmanifest',
    ],
    modifyURLPrefix: { '': base },
    maximumFileSizeToCacheInBytes: 2 * 1024 * 1024,
    minify: true,
    enableWorkboxModulesLogs: false,
  },
});
const pwaApi = (pwaPlugins[0] as unknown as {
  api: { generateSW(): Promise<void> };
}).api;
const finalizePwa: AstroIntegration = {
  name: 'ium-pwa-finalize',
  hooks: {
    'astro:build:done': async () => {
      await pwaApi.generateSW();
    },
  },
};
const profileIsolationPlugin = {
  name: 'ium-profile-output-isolation',
  generateBundle(
    _options: unknown,
    bundle: Record<string, unknown>,
  ) {
    for (const fileName of Object.keys(bundle)) {
      const fixtureBundle = fileName.includes(
        'FixtureWorkspace.astro_astro_type_script',
      );
      const workbenchBundle = fileName.includes('AlgorithmWorkbench')
        || fileName.includes('algorithm-workbench');
      if (
        (profile === 'production' && fixtureBundle)
        || (profile === 'fixture' && workbenchBundle)
      ) {
        delete bundle[fileName];
      }
    }
  },
};

export default defineConfig({
  output: 'static',
  base,
  trailingSlash: 'always',
  integrations: [finalizePwa],
  build: {
    format: 'directory',
  },
  vite: {
    cacheDir: resolve(pwaOutputDirectory, '.vite-cache'),
    plugins: [profileIsolationPlugin, ...pwaPlugins],
  },
  ...(outputDirectory === undefined
    ? {}
    : {
        outDir: resolve(outputDirectory),
      }),
});
