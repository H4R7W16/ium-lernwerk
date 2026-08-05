import type { ResilienceSpec } from '../contracts.js';

export type SaveState = 'idle' | 'saving' | 'saved' | 'failed';
export type ConnectivityState = 'online' | 'offline';
export type RecoveryAction = 'retry' | 'export' | 'reset';

export type TechnicalResilienceFact =
  | Readonly<{ type: 'save'; state: SaveState; affectedWork: string }>
  | Readonly<{ type: 'connectivity'; state: ConnectivityState; affectedWork: string }>
  | Readonly<{ type: 'storage'; state: 'persistent' | 'volatile'; affectedWork: string }>
  | Readonly<{ type: 'update'; state: 'available' | 'failed'; affectedWork: string }>;

const SAVE_MESSAGES: Readonly<Record<SaveState, string>> = {
  idle: 'Keine Änderungen ausstehend',
  saving: 'Wird auf diesem Gerät gespeichert',
  saved: 'Auf diesem Gerät gespeichert',
  failed: 'Speichern nicht möglich',
};

export function getSaveMessage(state: SaveState): string {
  return SAVE_MESSAGES[state];
}

export function adaptResilienceState(fact: TechnicalResilienceFact): ResilienceSpec {
  if (fact.type === 'save') {
    if (fact.state === 'failed') {
      return {
        code: 'SAVE_FAILED',
        severity: 'block',
        affectedWork: fact.affectedWork,
        preservedState: 'Deine Eingabe bleibt in dieser Ansicht erhalten.',
        consequence: 'Der aktuelle Stand ist noch nicht dauerhaft lokal gespeichert.',
        primaryAction: 'Erneut speichern',
        secondaryAction: 'Arbeitsstand lokal exportieren',
        returnTarget: 'Zur aktuellen Eingabe',
      };
    }
    return {
      code: `SAVE_${fact.state.toUpperCase()}`,
      severity: 'info',
      affectedWork: fact.affectedWork,
      preservedState: 'Deine Eingabe bleibt in dieser Ansicht erhalten.',
      consequence: getSaveMessage(fact.state),
      primaryAction: fact.state === 'saving' ? 'Speichern abwarten' : 'Weiterarbeiten',
      secondaryAction: null,
      returnTarget: 'Zur aktuellen Eingabe',
    };
  }

  if (fact.type === 'connectivity') {
    return fact.state === 'offline'
      ? {
          code: 'CONNECTIVITY_OFFLINE',
          severity: 'limit',
          affectedWork: fact.affectedWork,
          preservedState: 'Der lokale Arbeitsstand bleibt erhalten.',
          consequence: 'Nur bereits lokal verfügbare Inhalte und Aktionen funktionieren.',
          primaryAction: 'Lokal weiterarbeiten',
          secondaryAction: 'Arbeitsstand lokal exportieren',
          returnTarget: 'Zum aktuellen Lernschritt',
        }
      : {
          code: 'CONNECTIVITY_ONLINE',
          severity: 'info',
          affectedWork: fact.affectedWork,
          preservedState: 'Der lokale Arbeitsstand bleibt erhalten.',
          consequence: 'Die Verbindung ist verfügbar.',
          primaryAction: 'Weiterarbeiten',
          secondaryAction: null,
          returnTarget: 'Zum aktuellen Lernschritt',
        };
  }

  if (fact.type === 'storage') {
    return {
      code: fact.state === 'persistent' ? 'STORAGE_PERSISTENT' : 'STORAGE_VOLATILE',
      severity: fact.state === 'persistent' ? 'info' : 'limit',
      affectedWork: fact.affectedWork,
      preservedState: fact.state === 'persistent'
        ? 'Der Stand wird dauerhaft auf diesem Gerät gespeichert.'
        : 'Der Stand bleibt nur in dieser geöffneten Sitzung erhalten.',
      consequence: fact.state === 'persistent'
        ? 'Du kannst die Arbeit später auf diesem Gerät fortsetzen.'
        : 'Beim Schließen kann der Arbeitsstand verloren gehen.',
      primaryAction: 'Weiterarbeiten',
      secondaryAction: fact.state === 'volatile' ? 'Arbeitsstand lokal exportieren' : null,
      returnTarget: 'Zum aktuellen Lernschritt',
    };
  }

  return {
    code: fact.state === 'available' ? 'UPDATE_AVAILABLE' : 'UPDATE_FAILED',
    severity: fact.state === 'available' ? 'limit' : 'block',
    affectedWork: fact.affectedWork,
    preservedState: 'Die bisherige Version und der aktuelle Stand bleiben aktiv.',
    consequence: fact.state === 'available'
      ? 'Die Aktualisierung wird erst nach bewusstem Bestätigen aktiviert.'
      : 'Die Aktualisierung konnte nicht aktiviert werden.',
    primaryAction: fact.state === 'available' ? 'Speichern und aktualisieren' : 'Später erneut versuchen',
    secondaryAction: 'Später',
    returnTarget: 'Zum aktuellen Lernschritt',
  };
}
