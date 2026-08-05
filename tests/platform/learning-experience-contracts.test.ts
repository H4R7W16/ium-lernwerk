import { describe, expect, test } from 'vitest';
import {
  parseExperienceContent,
  type ExperienceContentV1,
  type LearningStateId,
  type SupportSpec,
} from '../../packages/learning-experience/src/index.js';

const support: SupportSpec = {
  id: 'support-strategy',
  kind: 'strategy',
  title: 'Prüfstrategie wählen',
  trigger: 'Die Wirkung passt noch nicht zur Vorhersage.',
  content: 'Vergleiche zuerst den erwarteten mit dem beobachteten Zustand.',
  preservesAction: 'Die Auswahl und Deutung des Belegs bleibt bei dir.',
  nextSupportId: null,
};

const valid: ExperienceContentV1 = {
  schemaVersion: 1,
  moduleId: 'ium-informatik-5',
  terminologyVersion: 'lxp04-1',
  start: {
    heading: 'Algorithmen untersuchen',
    guidingQuestion: 'Wie wird aus einer Vermutung ein begründeter Algorithmus?',
    expectedCapability: 'Vermutung bilden, ausführen und mit Belegen überarbeiten.',
    timeWindowMinutes: [35, 50],
    socialForm: 'individual',
    primaryAction: {
      label: 'Mit der Vermutung beginnen',
      result: 'Die erste Vorhersage wird vorbereitet.',
    },
    resumeAction: null,
    resetAction: null,
  },
  actions: [
    {
      id: 'action-predict',
      state: 'LS-DECIDE',
      taskId: 'task-predict',
      purpose: 'Eine prüfbare Erwartung vor der Ausführung festhalten.',
      prompt: 'Beschreibe die erwartete Wirkung des Algorithmus.',
      product: 'Eine strukturierte Vorhersage.',
      criteria: ['Die Vorhersage nennt einen erwarteten Zustand.'],
      primaryAction: {
        label: 'Vorhersage festhalten',
        result: 'Die Ausführung wird zur Prüfung freigegeben.',
      },
      secondaryActions: [
        {
          label: 'Prüfstrategie öffnen',
          purpose: 'Eine Strategiehilfe anzeigen, ohne die Vorhersage zu lösen.',
        },
      ],
      requiredEvidence: ['evidence-card'],
      supportIds: ['support-strategy'],
      checkpointId: 'checkpoint-compare',
      persistence: 'draft',
      next: [
        {
          state: 'LS-ACT',
          guard: 'Eine vollständige Vorhersage liegt vor.',
        },
      ],
    },
  ],
  tasks: [
    {
      id: 'task-predict',
      learningGoal: 'Wirkungen eines Algorithmus vor der Ausführung begründet vorhersagen.',
      purpose: 'Erwartung und beobachtete Wirkung später vergleichen.',
      thinkingAction: 'Vorhersagen und begründen.',
      product: 'Eine strukturierte Vorhersage.',
      materialRefs: ['scenario-delivery-c4'],
      criteria: ['Die Vorhersage ist am dargestellten Ausgangszustand prüfbar.'],
      requiredEvidence: ['evidence-card'],
      supportIds: ['support-strategy'],
      feedbackId: 'feedback-predict',
      socialForm: 'individual',
      roleIds: [],
      persistence: 'draft',
      offlineRequirement: 'core',
      recoverySpecId: 'storage-failed',
    },
  ],
  feedback: [
    {
      id: 'feedback-predict',
      result: 'Die beobachtete Wirkung weicht an einem Schritt von der Vorhersage ab.',
      evidenceRef: 'evidence-card',
      criterion: 'Erwartung und beobachteter Zustand sind auf denselben Schritt bezogen.',
      interpretationPrompt: 'Welche Beziehung erklärt die erste Abweichung?',
      nextCheck: 'Prüfe die Reparaturhypothese am selben Ausgangszustand.',
      strategySupportId: 'support-strategy',
      exampleSupportId: null,
    },
  ],
  supports: [support],
  checkpoints: [
    {
      id: 'checkpoint-compare',
      state: 'LS-INTERPRET',
      purpose: 'Erwartung und beobachtete Wirkung gemeinsam vergleichen.',
      timeWindowMinutes: [2, 4],
      socialForm: 'plenary',
      learnerSignal: 'Ich kann eine relevante Abweichung mit einem Beleg zeigen.',
      ordinaryEvidence: ['Gezeigter Schritt und mündliche Begründung.'],
      teacherPrompt: 'Welche Beziehung erklärt die beobachtete Abweichung?',
      neutralFallback: 'Ein neutraler Fall wird gemeinsam ohne private Geräteeinsicht geprüft.',
      returnState: 'LS-REVISE',
      exitCriterion: 'Eine prüfbare Reparaturhypothese ist formuliert.',
    },
  ],
  evidenceCards: [
    {
      id: 'evidence-card',
      actionKind: 'predict-test',
      requiredFields: [
        'EVC-CONTEXT',
        'EVC-CLAIM',
        'EVC-ACTION',
        'EVC-EFFECT',
        'EVC-INTERPRET',
        'EVC-REVISION',
        'EVC-CONCLUSION',
        'EVC-TRANSFER',
        'EVC-RECOVERY',
      ],
      modelBoundaryPrompt: 'Für welche veränderten Fälle gilt die Kernaussage nicht sicher?',
      transferPromptId: null,
      reentryPromptId: null,
    },
  ],
  resilience: [
    {
      code: 'storage-failed',
      severity: 'block',
      affectedWork: 'Die aktuelle Vorhersage.',
      preservedState: 'Die Eingabe bleibt im Formular erhalten.',
      consequence: 'Der Stand kann noch nicht bestätigt werden.',
      primaryAction: 'Speichern erneut versuchen',
      secondaryAction: 'Lokale Kopie exportieren',
      returnTarget: 'Zur Vorhersage zurückkehren',
    },
  ],
};

function cloneValid(): Record<string, unknown> {
  return structuredClone(valid) as unknown as Record<string, unknown>;
}

describe('ExperienceContentV1', () => {
  test('accepts the smallest closed document and returns a deep copy', () => {
    const input: ExperienceContentV1 = {
      ...valid,
      actions: [],
      tasks: [],
      feedback: [],
      supports: [],
      checkpoints: [],
      evidenceCards: [],
      resilience: [],
    };

    const result = parseExperienceContent(input);

    expect(result).toEqual({ ok: true, value: input });
    if (result.ok) {
      expect(result.value).not.toBe(input);
      expect(result.value.start).not.toBe(input.start);
    }
  });

  test('accepts the complete reference document', () => {
    expect(parseExperienceContent(valid)).toEqual({ ok: true, value: valid });
  });

  test('accepts every controlled enum value', () => {
    const states: readonly LearningStateId[] = [
      'LS-ORIENT',
      'LS-READY',
      'LS-DECIDE',
      'LS-ACT',
      'LS-OBSERVE',
      'LS-INTERPRET',
      'LS-REVISE',
      'LS-SECURE',
      'LS-TRANSFER',
      'LS-PAUSE',
      'LS-RECOVER',
    ];
    const socialForms = ['individual', 'pair', 'group', 'plenary'] as const;
    const persistence = ['none', 'draft', 'confirmed-product', 'evidence'] as const;
    const supportKinds = ['operation', 'concept', 'strategy', 'example'] as const;
    const actionKinds = [
      'predict-test',
      'create-revise',
      'analyze-judge',
      'secure-transfer',
    ] as const;
    const severities = ['info', 'limit', 'block'] as const;
    const offlineRequirements = ['core', 'enhancement'] as const;

    for (const state of states) {
      const document = structuredClone(valid);
      document.actions[0]!.state = state;
      document.actions[0]!.next = [{ state, guard: 'Der Übergang ist fachlich geklärt.' }];
      document.checkpoints[0]!.state = state;
      document.checkpoints[0]!.returnState = state;
      expect(parseExperienceContent(document).ok, state).toBe(true);
    }
    for (const socialForm of socialForms) {
      const document = structuredClone(valid);
      document.start.socialForm = socialForm;
      document.tasks[0]!.socialForm = socialForm;
      document.checkpoints[0]!.socialForm = socialForm;
      expect(parseExperienceContent(document).ok, socialForm).toBe(true);
    }
    for (const value of persistence) {
      const document = structuredClone(valid);
      document.actions[0]!.persistence = value;
      document.tasks[0]!.persistence = value;
      expect(parseExperienceContent(document).ok, value).toBe(true);
    }
    for (const kind of supportKinds) {
      const document = structuredClone(valid);
      document.supports[0]!.kind = kind;
      expect(parseExperienceContent(document).ok, kind).toBe(true);
    }
    for (const actionKind of actionKinds) {
      const document = structuredClone(valid);
      document.evidenceCards[0]!.actionKind = actionKind;
      expect(parseExperienceContent(document).ok, actionKind).toBe(true);
    }
    for (const severity of severities) {
      const document = structuredClone(valid);
      document.resilience[0]!.severity = severity;
      expect(parseExperienceContent(document).ok, severity).toBe(true);
    }
    for (const offlineRequirement of offlineRequirements) {
      const document = structuredClone(valid);
      document.tasks[0]!.offlineRequirement = offlineRequirement;
      expect(parseExperienceContent(document).ok, offlineRequirement).toBe(true);
    }
  });

  test('rejects unknown top-level and nested fields without coercion', () => {
    const topLevel = { ...cloneValid(), analytics: {} };
    const nested = cloneValid();
    (nested.start as Record<string, unknown>).trackingId = 'person-1';

    const topResult = parseExperienceContent(topLevel);
    const nestedResult = parseExperienceContent(nested);

    expect(topResult.ok).toBe(false);
    expect(nestedResult.ok).toBe(false);
    if (!topResult.ok && !nestedResult.ok) {
      expect(topResult.errors).toContainEqual(expect.objectContaining({
        path: '$.analytics',
        code: 'unknown_field',
      }));
      expect(nestedResult.errors).toContainEqual(expect.objectContaining({
        path: '$.start.trackingId',
        code: 'unknown_field',
      }));
    }
  });

  test('rejects missing fields, unsupported versions and open state values', () => {
    const missing = cloneValid();
    delete (missing.start as Record<string, unknown>).guidingQuestion;
    const unsupported = { ...cloneValid(), schemaVersion: 2 };
    const openState = cloneValid();
    ((openState.actions as Record<string, unknown>[])[0]!).state = 'prediction';

    for (const [document, path] of [
      [missing, '$.start.guidingQuestion'],
      [unsupported, '$.schemaVersion'],
      [openState, '$.actions[0].state'],
    ] as const) {
      const result = parseExperienceContent(document);
      expect(result.ok, path).toBe(false);
      if (!result.ok) {
        expect(result.errors).toContainEqual(expect.objectContaining({ path }));
      }
    }
  });

  test('rejects duplicate IDs and dangling references', () => {
    const duplicate = structuredClone(valid);
    duplicate.supports = [support, support];
    const dangling = structuredClone(valid);
    dangling.actions[0]!.taskId = 'missing-task';
    dangling.tasks[0]!.feedbackId = 'missing-feedback';
    dangling.tasks[0]!.recoverySpecId = 'missing-recovery';
    dangling.feedback[0]!.strategySupportId = 'missing-support';

    const duplicateResult = parseExperienceContent(duplicate);
    const danglingResult = parseExperienceContent(dangling);

    expect(duplicateResult.ok).toBe(false);
    expect(danglingResult.ok).toBe(false);
    if (!duplicateResult.ok && !danglingResult.ok) {
      expect(duplicateResult.errors.map((error) => error.code)).toContain('duplicate_id');
      expect(danglingResult.errors.map((error) => error.path)).toEqual(expect.arrayContaining([
        '$.actions[0].taskId',
        '$.tasks[0].feedbackId',
        '$.tasks[0].recoverySpecId',
        '$.feedback[0].strategySupportId',
      ]));
    }
  });

  test('rejects inaccessible labels and Unicode code-point limit violations', () => {
    const inaccessible = structuredClone(valid);
    inaccessible.actions[0]!.primaryAction.label = 'Weiter';
    const oversized = structuredClone(valid);
    oversized.supports[0]!.content = '🧭'.repeat(1_201);

    const inaccessibleResult = parseExperienceContent(inaccessible);
    const oversizedResult = parseExperienceContent(oversized);

    expect(inaccessibleResult.ok).toBe(false);
    expect(oversizedResult.ok).toBe(false);
    if (!inaccessibleResult.ok && !oversizedResult.ok) {
      expect(inaccessibleResult.errors).toContainEqual(expect.objectContaining({
        path: '$.actions[0].primaryAction.label',
        code: 'invalid_value',
      }));
      expect(oversizedResult.errors).toContainEqual(expect.objectContaining({
        path: '$.supports[0].content',
        code: 'limit_exceeded',
      }));
    }
  });

  test('rejects forbidden analytics and personal-data field names anywhere', () => {
    const document = cloneValid();
    ((document.tasks as Record<string, unknown>[])[0]!).attemptCount = 1;
    (document.start as Record<string, unknown>).name = 'Ada';

    const result = parseExperienceContent(document);

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.errors.map((error) => error.path)).toEqual(expect.arrayContaining([
        '$.tasks[0].attemptCount',
        '$.start.name',
      ]));
    }
  });
});
