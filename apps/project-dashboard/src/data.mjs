import { readFileSync } from 'node:fs';
export const snapshot = JSON.parse(readFileSync(process.env.IUM_DASHBOARD_INPUT,'utf8'));
export { axes, labels } from '../../../packages/project-status/index.mjs';
export const pages = [
  ['','Überblick','Entwicklungsstand auf einen Blick'],
  ['baselines','Baselines',snapshot.baseline.activeBaseline==='v2'?'V2 ist Planungsbaseline. V1 bleibt Produktstand.':'V1 bleibt aktiv. V2 wächst kontrolliert.'],
  ['foundations','Grundlagen','Vier getrennte Fundamente'],
  ['experience','Lern-Experience','Von Evidenz zu tragfähigen Lernwegen'],
  ['audit','Übernahmeaudit','Bestand wird einzeln bewertet'],
  ['grades','Jahrgänge','Planung 5–7 mit sichtbaren Grenzen'],
  ['gates','Gates','Freigaben in verbindlicher Reihenfolge'],
  ['evidence','Evidenz','Quellenstand und Prüfnachweise'],
];
