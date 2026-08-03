import { defineConfig, type Preset } from '@vite-pwa/assets-generator/config';

const preset: Preset = {
  transparent: { sizes: [192, 512] },
  maskable: { sizes: [512], padding: 0.2 },
  apple: { sizes: [] },
  assetName(type, size) {
    return type === 'maskable'
      ? `icons/maskable-${size.width}x${size.height}.png`
      : `icons/pwa-${size.width}x${size.height}.png`;
  },
};

export default defineConfig({
  preset,
  images: ['apps/lernwerk-portal/public/app-icon.svg'],
  manifestIconsEntry: false,
  logLevel: 'silent',
});
