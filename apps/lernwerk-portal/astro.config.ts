import { resolve } from 'node:path';
import { defineConfig } from 'astro/config';

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

export default defineConfig({
  output: 'static',
  base,
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  ...(outputDirectory === undefined
    ? {}
    : {
        outDir: resolve(outputDirectory),
      }),
});
