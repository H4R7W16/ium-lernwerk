(function () {
  'use strict';

  const PACKAGE_FIELDS = [
    'schemaVersion', 'packageType', 'packageId', 'protocolVersion',
    'protocolFingerprint', 'toolVersion', 'timeModelFingerprint', 'scopeType',
    'scopeId', 'context', 'deliveryTimeEvidence', 'learningQualityEvidence',
    'learnerPulseEvidence', 'technicalPrivacyEvidence', 'result',
    'developmentWarnings', 'retentionClass'
  ];
  const FORM_FIELDS = [
    'context', 'deliveryTimeEvidence', 'learningQualityEvidence',
    'learnerPulseEvidence', 'technicalPrivacyEvidence'
  ];
  const CONTEXT_FIELDS = [
    'schoolYear', 'term', 'classSizeBand', 'deviceClass', 'browserFamily',
    'networkMode'
  ];
  const DELIVERY_FIELDS = [
    'plannedUnits', 'actualUnits', 'completedPhaseIds',
    'requiredLearningPhasesCompleted', 'fallbackActivated',
    'technicalStartupMinutes', 'supportDemandBand', 'externalDisruptionCode'
  ];
  const LEARNING_QUALITY_FIELDS = ['moduleResults', 'integrationResults'];
  const MODULE_RESULT_FIELDS = ['pilotAssignmentId', 'moduleId', 'criteria', 'result'];
  const INTEGRATION_RESULT_FIELDS = [
    'pilotAssignmentId', 'integrationContractId', 'criteria',
    'handoffProductPresent', 'handoffReused', 'result'
  ];
  const CRITERION_FIELDS = ['criterionId', 'band'];
  const PULSE_ITEM_FIELDS = ['itemId', 'agree', 'partly', 'disagree', 'noAnswer'];
  const TECHNICAL_PRIVACY_FIELDS = [
    'technicalFunction', 'fallbackEquivalentLearningFunction', 'problemCode',
    'severity', 'privacyGate'
  ];
  const WARNING_FIELDS = ['id', 'itemId', 'status'];
  const RESULT_VALUES = ['pass', 'fail', 'not-evaluable'];
  const BAND_VALUES = ['strong', 'mixed', 'weak'];
  const PACKAGE_ID_PATTERN = /^PKG-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
  const FINGERPRINT_PATTERN = /^[0-9a-f]{64}$/;
  const SCHOOL_YEAR_PATTERN = /^[0-9]{4}-[0-9]{2}$/;

  function requireCondition(condition, message) {
    if (!condition) {
      throw new Error(message);
    }
  }

  function isObject(value) {
    return value !== null && typeof value === 'object' && !Array.isArray(value);
  }

  function assertJsonCompatible(value, label, ancestors) {
    const valueType = typeof value;
    if (value === null || valueType === 'string' || valueType === 'boolean') {
      return;
    }
    if (valueType === 'number') {
      requireCondition(Number.isFinite(value), `${label} must be JSON-compatible`);
      return;
    }
    requireCondition(valueType === 'object', `${label} must be JSON-compatible`);
    const seen = ancestors || new Set();
    requireCondition(!seen.has(value), `${label} must not be cyclic`);
    seen.add(value);
    if (Array.isArray(value)) {
      const expectedKeys = Array.from({length: value.length}, function (_, index) {
        return String(index);
      });
      requireCondition(
        JSON.stringify(Object.keys(value)) === JSON.stringify(expectedKeys),
        `${label} array must be dense and closed`
      );
      value.forEach(function (item, index) {
        assertJsonCompatible(item, `${label}[${index}]`, seen);
      });
    } else {
      const prototype = Object.getPrototypeOf(value);
      requireCondition(
        prototype === Object.prototype || prototype === null,
        `${label} must be a plain object`
      );
      Object.keys(value).forEach(function (key) {
        assertJsonCompatible(value[key], `${label}.${key}`, seen);
      });
    }
    seen.delete(value);
  }

  function assertExactKeys(value, expected, label) {
    requireCondition(isObject(value), `${label} must be an object`);
    const actual = Object.keys(value).sort();
    const wanted = expected.slice().sort();
    requireCondition(
      JSON.stringify(actual) === JSON.stringify(wanted),
      `${label} fields differ from contract`
    );
  }

  function requireInteger(value, label, minimum) {
    requireCondition(
      Number.isInteger(value) && value >= (minimum === undefined ? 0 : minimum),
      `${label} must be an integer of at least ${minimum === undefined ? 0 : minimum}`
    );
  }

  function requireBoolean(value, label) {
    requireCondition(typeof value === 'boolean', `${label} must be a boolean`);
  }

  function requireEnum(value, values, label) {
    requireCondition(typeof value === 'string' && values.includes(value), `${label} is invalid`);
  }

  function cloneJson(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function sameJson(left, right) {
    if (left === right) {
      return true;
    }
    if (typeof left !== typeof right || left === null || right === null) {
      return false;
    }
    if (Array.isArray(left) || Array.isArray(right)) {
      return Array.isArray(left) && Array.isArray(right) &&
        left.length === right.length &&
        left.every(function (item, index) {
          return sameJson(item, right[index]);
        });
    }
    if (typeof left !== 'object') {
      return false;
    }
    const leftKeys = Object.keys(left);
    const rightKeys = Object.keys(right);
    return leftKeys.length === rightKeys.length && leftKeys.every(function (key) {
      return Object.prototype.hasOwnProperty.call(right, key) &&
        sameJson(left[key], right[key]);
    });
  }

  function findCluster(protocol, clusterId) {
    const cluster = protocol.clusters.find(function (candidate) {
      return candidate.id === clusterId;
    });
    requireCondition(Boolean(cluster), 'cluster scopeId differs from contract');
    return cluster;
  }

  function evaluateLearnerPulse(payload, protocol) {
    assertJsonCompatible(payload, 'learnerPulseEvidence');
    assertJsonCompatible(protocol, 'protocol');
    if (payload.status === 'suppressed-small-group') {
      assertExactKeys(payload, ['status'], 'learnerPulseEvidence');
      return {status: 'suppressed-small-group', warnings: []};
    }
    assertExactKeys(
      payload,
      ['status', 'classResponseCount', 'items'],
      'learnerPulseEvidence'
    );
    requireCondition(
      payload.status === 'reported' &&
        Number.isInteger(payload.classResponseCount) &&
        payload.classResponseCount >= protocol.minimumLearnerResponses,
      'reported learner pulse requires at least 10 responses'
    );
    requireCondition(
      Array.isArray(payload.items) && payload.items.length === protocol.learnerPulseItems.length,
      'learner pulse items differ from contract'
    );
    const warnings = [];
    protocol.learnerPulseItems.forEach(function (definition, index) {
      const item = payload.items[index];
      assertExactKeys(item, PULSE_ITEM_FIELDS, 'learner pulse item');
      requireCondition(item.itemId === definition.id, 'learner pulse item order differs');
      ['agree', 'partly', 'disagree', 'noAnswer'].forEach(function (field) {
        requireInteger(item[field], `learner pulse ${field}`);
      });
      const valid = item.agree + item.partly + item.disagree;
      const total = valid + item.noAnswer;
      requireCondition(
        total === payload.classResponseCount && valid >= protocol.minimumLearnerResponses,
        'learner pulse sums or ids differ'
      );
      if (
        item.disagree * protocol.learnerWarningRatio.denominator >=
        valid * protocol.learnerWarningRatio.numerator
      ) {
        warnings.push({
          id: `WARN-${definition.id}`,
          itemId: definition.id,
          status: 'open'
        });
      }
    });
    return {status: 'reported', warnings: warnings};
  }

  function deriveModuleResultsForModules(payload, modules) {
    const evidence = payload.learningQualityEvidence.moduleResults;
    requireCondition(Array.isArray(evidence), 'module results differ from contract');
    requireCondition(evidence.length === modules.length, 'module results differ from contract');
    const evidenceIds = new Set(evidence.map(function (item) { return item.moduleId; }));
    const expectedIds = new Set(modules.map(function (item) { return item.moduleId; }));
    requireCondition(
      evidenceIds.size === expectedIds.size &&
        Array.from(evidenceIds).every(function (item) { return expectedIds.has(item); }),
      'module results differ from contract'
    );
    return modules.map(function (module, index) {
      const item = evidence[index];
      requireCondition(item.moduleId === module.moduleId, 'module result order differs from contract');
      return {
        pilotAssignmentId: module.pilotAssignmentId,
        moduleId: module.moduleId,
        criteria: cloneJson(item.criteria),
        result: item.criteria.every(function (criterion) {
          return criterion.band === 'strong';
        }) ? 'pass' : 'fail'
      };
    });
  }

  function deriveModuleResults(payload, cluster) {
    return deriveModuleResultsForModules(payload, cluster.modules);
  }

  function deriveIntegrationResultsForContracts(payload, integrations) {
    const evidence = payload.learningQualityEvidence.integrationResults;
    requireCondition(
      Array.isArray(evidence) && evidence.length === integrations.length,
      'integration results differ from contract'
    );
    return integrations.map(function (integration, index) {
      const item = evidence[index];
      requireCondition(
        item.integrationContractId === integration.integrationContractId,
        'integration result differs from contract'
      );
      const passed = item.criteria.every(function (criterion) {
        return criterion.band === 'strong';
      }) && item.handoffProductPresent && item.handoffReused;
      return {
        pilotAssignmentId: integration.pilotAssignmentId,
        integrationContractId: integration.integrationContractId,
        criteria: cloneJson(item.criteria),
        handoffProductPresent: item.handoffProductPresent,
        handoffReused: item.handoffReused,
        result: passed ? 'pass' : 'fail'
      };
    });
  }

  function deriveIntegrationResult(payload, cluster) {
    return deriveIntegrationResultsForContracts(payload, [cluster.integration])[0];
  }

  function clusterRequiredPhasesCompleted(payload, cluster) {
    const phaseIds = [];
    cluster.modules.forEach(function (module) {
      module.requiredPhaseIds.forEach(function (phaseId) {
        if (!phaseIds.includes(phaseId)) {
          phaseIds.push(phaseId);
        }
      });
    });
    phaseIds.sort();
    return payload.deliveryTimeEvidence.requiredLearningPhasesCompleted === true &&
      sameJson(payload.deliveryTimeEvidence.completedPhaseIds, phaseIds);
  }

  function deriveClusterResult(payload, cluster, protocol) {
    assertJsonCompatible(payload, 'evidence package');
    assertJsonCompatible(cluster, 'cluster');
    assertJsonCompatible(protocol, 'protocol');
    const delivery = payload.deliveryTimeEvidence;
    const technicalPrivacy = payload.technicalPrivacyEvidence;
    const notEvaluable = delivery.externalDisruptionCode === 'interpretability-lost';
    const moduleResults = deriveModuleResults(payload, cluster);
    const integrationResult = deriveIntegrationResult(payload, cluster);
    const pulse = evaluateLearnerPulse(payload.learnerPulseEvidence, protocol);
    const technicalPathPassed = technicalPrivacy.technicalFunction === 'pass' ||
      (delivery.fallbackActivated && technicalPrivacy.fallbackEquivalentLearningFunction);
    const failed = delivery.actualUnits > cluster.budgetUnits ||
      !clusterRequiredPhasesCompleted(payload, cluster) ||
      moduleResults.some(function (item) { return item.result !== 'pass'; }) ||
      integrationResult.result !== 'pass' ||
      !technicalPathPassed ||
      technicalPrivacy.privacyGate !== 'pass' ||
      pulse.warnings.length > 0;
    const result = notEvaluable ? 'not-evaluable' : failed ? 'fail' : 'pass';
    return {
      result: result,
      moduleResults: moduleResults,
      integrationResult: integrationResult,
      developmentWarnings: pulse.warnings,
      fallbackDeltaUnits: result === 'fail' ? cluster.fallbackDeltaUnits : 0
    };
  }

  function validateCriteria(criteria, expected, label) {
    requireCondition(
      Array.isArray(criteria) && criteria.length === expected.length,
      `${label} criteria differ from contract`
    );
    criteria.forEach(function (criterion, index) {
      assertExactKeys(criterion, CRITERION_FIELDS, `${label} criterion`);
      requireCondition(
        criterion.criterionId === expected[index].criterionId,
        `${label} criterion IDs differ from contract`
      );
      requireEnum(criterion.band, BAND_VALUES, `${label} criterion band`);
    });
  }

  function validateContext(context, protocol) {
    assertExactKeys(context, CONTEXT_FIELDS, 'context');
    requireCondition(
      typeof context.schoolYear === 'string' && SCHOOL_YEAR_PATTERN.test(context.schoolYear),
      'schoolYear is invalid'
    );
    Object.keys(protocol.contextEnums).forEach(function (field) {
      requireEnum(context[field], protocol.contextEnums[field], `context ${field}`);
    });
  }

  function validateDeliveryTime(payload, scope, isAnnual) {
    const expectedFields = isAnnual
      ? DELIVERY_FIELDS.concat(['clusterOrder', 'clusterActualUnits'])
      : DELIVERY_FIELDS;
    assertExactKeys(payload, expectedFields, 'delivery time evidence');
    ['plannedUnits', 'actualUnits', 'technicalStartupMinutes'].forEach(function (field) {
      requireInteger(payload[field], field);
    });
    requireCondition(payload.plannedUnits === scope.budgetUnits, 'plannedUnits differs from scope budget');
    requireCondition(
      Array.isArray(payload.completedPhaseIds) &&
        payload.completedPhaseIds.every(function (phaseId) { return typeof phaseId === 'string'; }),
      'completedPhaseIds must contain strings'
    );
    const sortedUnique = Array.from(new Set(payload.completedPhaseIds)).sort();
    requireCondition(sameJson(payload.completedPhaseIds, sortedUnique), 'completedPhaseIds must be sorted and unique');
    requireBoolean(payload.requiredLearningPhasesCompleted, 'requiredLearningPhasesCompleted');
    requireBoolean(payload.fallbackActivated, 'fallbackActivated');
    requireEnum(payload.supportDemandBand, ['low', 'medium', 'high'], 'supportDemandBand');
    requireEnum(payload.externalDisruptionCode, ['none', 'interpretability-lost'], 'externalDisruptionCode');
    if (isAnnual) {
      requireCondition(sameJson(payload.clusterOrder, scope.clusterIds), 'annual cluster order differs from contract');
      requireCondition(
        Array.isArray(payload.clusterActualUnits) && payload.clusterActualUnits.length === scope.clusterIds.length,
        'annual cluster actual units differ from contract'
      );
      payload.clusterActualUnits.forEach(function (record, index) {
        assertExactKeys(record, ['clusterId', 'actualUnits'], 'annual cluster actual units');
        requireCondition(record.clusterId === scope.clusterIds[index], 'annual cluster actual unit order differs');
        requireInteger(record.actualUnits, 'annual cluster actualUnits');
      });
      const actualSum = payload.clusterActualUnits.reduce(function (sum, record) {
        return sum + record.actualUnits;
      }, 0);
      requireCondition(payload.actualUnits === actualSum, 'annual actualUnits sum differs');
    }
  }

  function validateLearningQuality(payload, modules, integrations) {
    assertExactKeys(payload, LEARNING_QUALITY_FIELDS, 'learning quality evidence');
    requireCondition(
      Array.isArray(payload.moduleResults) && payload.moduleResults.length === modules.length,
      'module results differ from contract'
    );
    payload.moduleResults.forEach(function (result, index) {
      const expected = modules[index];
      assertExactKeys(result, MODULE_RESULT_FIELDS, 'module result');
      requireCondition(result.pilotAssignmentId === expected.pilotAssignmentId, 'module pilot assignment differs from contract');
      requireCondition(result.moduleId === expected.moduleId, 'module ID differs from contract');
      validateCriteria(result.criteria, expected.criteria, 'module');
      requireEnum(result.result, RESULT_VALUES, 'module result');
    });
    requireCondition(
      Array.isArray(payload.integrationResults) && payload.integrationResults.length === integrations.length,
      'integration results differ from contract'
    );
    payload.integrationResults.forEach(function (result, index) {
      const expected = integrations[index];
      assertExactKeys(result, INTEGRATION_RESULT_FIELDS, 'integration result');
      requireCondition(result.pilotAssignmentId === expected.pilotAssignmentId, 'integration pilot assignment differs from contract');
      requireCondition(result.integrationContractId === expected.integrationContractId, 'integration contract differs from contract');
      validateCriteria(result.criteria, expected.criteria, 'integration');
      requireBoolean(result.handoffProductPresent, 'handoffProductPresent');
      requireBoolean(result.handoffReused, 'handoffReused');
      requireEnum(result.result, RESULT_VALUES, 'integration result');
    });
  }

  function validateTechnicalPrivacy(payload) {
    assertExactKeys(payload, TECHNICAL_PRIVACY_FIELDS, 'technical privacy evidence');
    requireEnum(payload.technicalFunction, ['pass', 'fail'], 'technicalFunction');
    requireBoolean(payload.fallbackEquivalentLearningFunction, 'fallbackEquivalentLearningFunction');
    requireEnum(payload.problemCode, ['none', 'startup', 'execution', 'import', 'export'], 'problemCode');
    requireEnum(payload.severity, ['none', 'minor', 'major', 'blocking'], 'severity');
    requireCondition(payload.privacyGate === 'pass', 'privacyGate fail cannot be exported');
  }

  function validateWarnings(payload, warnings) {
    requireCondition(Array.isArray(payload), 'developmentWarnings must be a list');
    payload.forEach(function (warning) {
      assertExactKeys(warning, WARNING_FIELDS, 'development warning');
      requireCondition(warning.id === `WARN-${warning.itemId}`, 'development warning ID is invalid');
      requireCondition(warning.status === 'open', 'development warning status is invalid');
    });
    requireCondition(sameJson(payload, warnings), 'developmentWarnings differ from learner pulse warnings');
  }

  function requiredPhaseIds(modules) {
    const ids = [];
    modules.forEach(function (module) {
      module.requiredPhaseIds.forEach(function (phaseId) {
        if (!ids.includes(phaseId)) {
          ids.push(phaseId);
        }
      });
    });
    return ids.sort();
  }

  function validateEvidencePackage(payload, protocol) {
    assertJsonCompatible(payload, 'evidence package');
    assertJsonCompatible(protocol, 'protocol');
    assertExactKeys(payload, PACKAGE_FIELDS, 'evidence package');
    requireCondition(payload.schemaVersion === 1, 'package schemaVersion must be 1');
    requireCondition(typeof payload.packageId === 'string' && PACKAGE_ID_PATTERN.test(payload.packageId), 'packageId is invalid');
    requireCondition(typeof payload.packageType === 'string', 'packageType must be a string');
    requireCondition(typeof payload.scopeType === 'string', 'scopeType must be a string');
    requireCondition(typeof payload.scopeId === 'string', 'scopeId must be a string');
    requireCondition(typeof payload.protocolFingerprint === 'string' && FINGERPRINT_PATTERN.test(payload.protocolFingerprint), 'protocolFingerprint is invalid');
    requireCondition(typeof payload.timeModelFingerprint === 'string' && FINGERPRINT_PATTERN.test(payload.timeModelFingerprint), 'timeModelFingerprint is invalid');
    requireCondition(payload.protocolVersion === protocol.protocolVersion && protocol.protocolVersion === '1.0.0', 'protocolVersion differs from contract');
    requireCondition(payload.toolVersion === protocol.toolVersion && protocol.toolVersion === '1.0.0', 'toolVersion differs from contract');
    requireCondition(payload.protocolFingerprint === protocol.protocolFingerprint, 'protocolFingerprint differs from contract');
    requireCondition(payload.timeModelFingerprint === protocol.timeModelFingerprint, 'timeModelFingerprint differs from contract');
    requireCondition(payload.retentionClass === 'until-decision', 'retentionClass differs from contract');
    requireEnum(payload.result, RESULT_VALUES, 'package result');
    validateContext(payload.context, protocol);

    const isCluster = payload.packageType === 'cluster-evidence' && payload.scopeType === 'cluster';
    const isAnnual = payload.packageType === 'annual-evidence' && payload.scopeType === 'annual';
    requireCondition(isCluster || isAnnual, 'package type and scope type differ');
    let scope;
    let modules;
    let integrations;
    if (isCluster) {
      scope = findCluster(protocol, payload.scopeId);
      modules = scope.modules;
      integrations = [scope.integration];
    } else {
      scope = protocol.annualPilot;
      requireCondition(payload.scopeId === scope.id, 'annual scopeId differs from contract');
      const clusters = scope.clusterIds.map(function (clusterId) {
        return findCluster(protocol, clusterId);
      });
      modules = clusters.reduce(function (all, cluster) {
        return all.concat(cluster.modules);
      }, []);
      integrations = clusters.map(function (cluster) { return cluster.integration; });
    }

    validateDeliveryTime(payload.deliveryTimeEvidence, scope, isAnnual);
    requireCondition(
      sameJson(payload.deliveryTimeEvidence.completedPhaseIds, requiredPhaseIds(modules)),
      'completedPhaseIds differ from required learning phases'
    );
    requireCondition(
      payload.deliveryTimeEvidence.requiredLearningPhasesCompleted === true,
      'required learning phases must be complete'
    );
    validateLearningQuality(payload.learningQualityEvidence, modules, integrations);
    const learnerPulse = evaluateLearnerPulse(payload.learnerPulseEvidence, protocol);
    validateTechnicalPrivacy(payload.technicalPrivacyEvidence);
    validateWarnings(payload.developmentWarnings, learnerPulse.warnings);
    if (isCluster) {
      const derived = deriveClusterResult(payload, scope, protocol);
      requireCondition(
        sameJson(payload.learningQualityEvidence.moduleResults, derived.moduleResults),
        'module results differ from derived evidence'
      );
      requireCondition(
        sameJson(payload.learningQualityEvidence.integrationResults, [derived.integrationResult]),
        'integration results differ from derived evidence'
      );
      requireCondition(
        payload.result === derived.result,
        'cluster budget or result differs from derived evidence'
      );
    } else {
      const derived = deriveAnnualEvidenceResult(payload, protocol);
      requireCondition(
        sameJson(payload.learningQualityEvidence.moduleResults, derived.moduleResults),
        'annual module results differ from derived evidence'
      );
      requireCondition(
        sameJson(payload.learningQualityEvidence.integrationResults, derived.integrationResults),
        'annual integration results differ from derived evidence'
      );
      requireCondition(payload.result === derived.result, 'annual result differs from derived evidence');
    }
    return cloneJson(payload);
  }

  function technicalPathPassed(payload) {
    return payload.technicalPrivacyEvidence.technicalFunction === 'pass' ||
      (payload.deliveryTimeEvidence.fallbackActivated &&
        payload.technicalPrivacyEvidence.fallbackEquivalentLearningFunction);
  }

  function deriveAnnualEvidenceResult(annualPayload, protocol) {
    const clusters = protocol.annualPilot.clusterIds.map(function (clusterId) {
      return findCluster(protocol, clusterId);
    });
    const modules = clusters.reduce(function (all, cluster) {
      return all.concat(cluster.modules);
    }, []);
    const integrations = clusters.map(function (cluster) { return cluster.integration; });
    const moduleResults = deriveModuleResultsForModules(annualPayload, modules);
    const integrationResults = deriveIntegrationResultsForContracts(
      annualPayload, integrations
    );
    const delivery = annualPayload.deliveryTimeEvidence;
    requireCondition(delivery.actualUnits <= 40, 'annual budget exceeded');
    requireCondition(sameJson(delivery.clusterOrder, protocol.annualPilot.clusterIds), 'annual sequence differs');
    requireCondition(
      Array.isArray(delivery.clusterActualUnits) && delivery.clusterActualUnits.length === protocol.annualPilot.clusterIds.length,
      'annual cluster actual units differ from contract'
    );
    delivery.clusterActualUnits.forEach(function (record, index) {
      const clusterId = protocol.annualPilot.clusterIds[index];
      requireCondition(
        record.clusterId === clusterId && record.actualUnits <= findCluster(protocol, clusterId).budgetUnits,
        `annual cluster budget exceeded: ${clusterId}`
      );
    });
    const integrationsPassed = integrationResults.every(function (item) {
      return item.result === 'pass';
    });
    const modulesPassed = moduleResults.every(function (item) {
      return item.result === 'pass';
    });
    const pulse = evaluateLearnerPulse(annualPayload.learnerPulseEvidence, protocol);
    const capacityPassed = delivery.actualUnits === 40;
    const integration = integrationsPassed ? 'passed' : 'failed';
    const technical = technicalPathPassed(annualPayload) ? 'passed' : 'failed';
    const privacy = annualPayload.technicalPrivacyEvidence.privacyGate === 'pass' ? 'passed' : 'failed';
    const notEvaluable = delivery.externalDisruptionCode === 'interpretability-lost';
    const failed = !capacityPassed || integration === 'failed' || technical === 'failed' ||
      privacy === 'failed' || !modulesPassed || pulse.warnings.length > 0;
    const result = notEvaluable ? 'not-evaluable' : failed ? 'fail' : 'pass';
    return {
      result: result,
      actualUnits: delivery.actualUnits,
      availabilityGateResults: {
        capacity: capacityPassed ? 'passed' : 'failed',
        integration: integration,
        technical: technical,
        privacy: privacy,
        pilot: result === 'pass' ? 'passed' : 'failed'
      },
      moduleResults: moduleResults,
      integrationResults: integrationResults,
      developmentWarnings: pulse.warnings
    };
  }

  function deriveAnnualResult(annualPayload, clusterPackages, protocol) {
    assertJsonCompatible(annualPayload, 'annual evidence package');
    assertJsonCompatible(clusterPackages, 'cluster evidence packages');
    assertJsonCompatible(protocol, 'protocol');
    requireCondition(Array.isArray(clusterPackages), 'annual result requires cluster packages');
    clusterPackages.forEach(function (item) {
      requireCondition(isObject(item), 'annual result requires known cluster packages');
      findCluster(protocol, item.scopeId);
    });
    const ordered = clusterPackages.slice().sort(function (left, right) {
      return findCluster(protocol, left.scopeId).order - findCluster(protocol, right.scopeId).order;
    });
    requireCondition(ordered.length === 4, 'annual result requires four cluster packages');
    requireCondition(new Set(ordered.map(function (item) { return item.scopeId; })).size === 4, 'annual result requires distinct cluster packages');
    const annualSources = ordered.concat([annualPayload]);
    requireCondition(new Set(annualSources.map(function (item) { return item.packageId; })).size === 5, 'annual result requires distinct source package IDs');
    ['protocolVersion', 'protocolFingerprint', 'toolVersion', 'timeModelFingerprint'].forEach(function (field) {
      requireCondition(new Set(annualSources.map(function (item) { return item[field]; })).size === 1, `annual source ${field} values differ`);
    });
    requireCondition(annualPayload.protocolVersion === protocol.protocolVersion, 'annual protocolVersion differs');
    requireCondition(annualPayload.protocolFingerprint === protocol.protocolFingerprint, 'annual protocolFingerprint differs');
    requireCondition(annualPayload.toolVersion === protocol.toolVersion, 'annual toolVersion differs');
    requireCondition(annualPayload.timeModelFingerprint === protocol.timeModelFingerprint, 'annual timeModelFingerprint differs');
    requireCondition(
      sameJson(ordered.map(function (item) { return item.scopeId; }), protocol.annualPilot.clusterIds),
      'annual cluster sequence differs'
    );
    ordered.forEach(function (item) {
      const cluster = findCluster(protocol, item.scopeId);
      requireCondition(item.deliveryTimeEvidence.actualUnits <= cluster.budgetUnits, `cluster budget exceeded: ${item.scopeId}`);
    });
    ordered.forEach(function (item) {
      validateEvidencePackage(item, protocol);
    });
    requireCondition(ordered.every(function (item) { return item.result === 'pass'; }), 'annual result requires positive clusters');
    const derived = deriveAnnualEvidenceResult(annualPayload, protocol);
    return {
      result: derived.result,
      actualUnits: derived.actualUnits,
      availabilityGateResults: derived.availabilityGateResults
    };
  }

  function createPackageId() {
    let uuid;
    if (typeof require === 'function') {
      uuid = require('node:crypto').randomUUID();
    } else {
      requireCondition(
        typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function',
        'crypto.randomUUID is unavailable'
      );
      uuid = crypto.randomUUID();
    }
    return `PKG-${uuid}`;
  }

  function createEvidencePackage(scopeId, formValue, protocol) {
    assertJsonCompatible(scopeId, 'scopeId');
    assertJsonCompatible(formValue, 'evidence package form');
    assertJsonCompatible(protocol, 'protocol');
    requireCondition(typeof scopeId === 'string', 'scopeId must be a string');
    const isAnnual = scopeId === protocol.annualPilot.id;
    const cluster = isAnnual ? null : protocol.clusters.find(function (candidate) {
      return candidate.id === scopeId;
    });
    requireCondition(isAnnual || Boolean(cluster), 'scopeId differs from contract');
    assertExactKeys(
      formValue,
      isAnnual ? FORM_FIELDS.concat(['clusterPackages']) : FORM_FIELDS,
      'evidence package form'
    );
    const evidence = {};
    FORM_FIELDS.forEach(function (field) {
      evidence[field] = cloneJson(formValue[field]);
    });
    const payload = Object.assign({
      schemaVersion: 1,
      packageType: isAnnual ? 'annual-evidence' : 'cluster-evidence',
      packageId: createPackageId(),
      protocolVersion: protocol.protocolVersion,
      protocolFingerprint: protocol.protocolFingerprint,
      toolVersion: protocol.toolVersion,
      timeModelFingerprint: protocol.timeModelFingerprint,
      scopeType: isAnnual ? 'annual' : 'cluster',
      scopeId: scopeId
    }, evidence, {
      result: 'not-evaluable',
      developmentWarnings: [],
      retentionClass: 'until-decision'
    });
    if (isAnnual) {
      const local = deriveAnnualEvidenceResult(payload, protocol);
      requireCondition(
        sameJson(payload.learningQualityEvidence.moduleResults, local.moduleResults),
        'annual module results differ from derived evidence'
      );
      requireCondition(
        sameJson(payload.learningQualityEvidence.integrationResults, local.integrationResults),
        'annual integration results differ from derived evidence'
      );
      const derived = deriveAnnualResult(
        payload, cloneJson(formValue.clusterPackages), protocol
      );
      payload.result = derived.result;
      payload.developmentWarnings = local.developmentWarnings;
    } else {
      const derived = deriveClusterResult(payload, cluster, protocol);
      requireCondition(
        sameJson(payload.learningQualityEvidence.moduleResults, derived.moduleResults),
        'module results differ from derived evidence'
      );
      requireCondition(
        sameJson(payload.learningQualityEvidence.integrationResults, [derived.integrationResult]),
        'integration results differ from derived evidence'
      );
      payload.result = derived.result;
      payload.developmentWarnings = derived.developmentWarnings;
    }
    return validateEvidencePackage(payload, protocol);
  }

  function serializePackage(payload) {
    assertJsonCompatible(payload, 'evidence package');
    requireCondition(isObject(payload), 'evidence package must be an object');
    return `${JSON.stringify(payload, null, 2)}\n`;
  }

  function parsePackage(source, protocol) {
    requireCondition(typeof source === 'string', 'serialized package must be a string');
    let payload;
    try {
      payload = JSON.parse(source);
    } catch (error) {
      throw new Error('serialized package is invalid JSON');
    }
    requireCondition(isObject(payload), 'serialized package must contain an object');
    return validateEvidencePackage(payload, protocol);
  }

  const READINESS_IDS = [
    'readiness-materials', 'readiness-handbook', 'readiness-anchor-tasks',
    'readiness-tools-fallback', 'readiness-privacy', 'readiness-capacity',
    'readiness-fingerprint'
  ];
  const CONTEXT_CONTROL_IDS = {
    term: 'context-term',
    classSizeBand: 'context-class-size-band',
    deviceClass: 'context-device-class',
    browserFamily: 'context-browser-family',
    networkMode: 'context-network-mode'
  };
  const FLOW_CAUSES = {
    'readiness-incomplete': 'Das Bereitschaftsgate ist unvollständig.',
    'scope-required': 'Es wurde keine zulässige Pilotstufe gewählt.',
    'annual-clusters-required': 'Der Jahresmodus benötigt vier positive, versionsgleiche Clusterpakete in Protokollreihenfolge.',
    'privacy-blocked': 'Das Privacygate ist verletzt; dieses Paket darf nicht exportiert werden.',
    'invalid-evidence': 'Die aggregierten Eingaben sind unvollständig oder widersprüchlich.',
    'import-invalid': 'Der lokale Import ist beschädigt oder verletzt den Paketvertrag.',
    'learner-warning': 'Eine verpflichtende Entwicklungswarnung verhindert ein positives Ergebnis.',
    'export-blocked': 'Es liegt kein frisch abgeleitetes und validiertes Paket für den Download vor.'
  };

  function slug(value) {
    return String(value).toLowerCase().replace(/[^a-z0-9]+/g, '-');
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function optionMarkup(values, labels) {
    return values.map(function (value) {
      const label = labels && labels[value] ? labels[value] : value;
      return `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`;
    }).join('');
  }

  function makeFlowError(code, scopeId, nextStep) {
    return {code: code, scopeId: scopeId || 'nicht gewählt', nextStep: nextStep};
  }

  function isFlowError(value) {
    return isObject(value) &&
      Object.keys(value).sort().join(',') === 'code,nextStep,scopeId';
  }

  function createDomAdapter(sourceDocument) {
    function get(id) {
      const element = sourceDocument.getElementById(id);
      requireCondition(Boolean(element), `cockpit control is missing: ${id}`);
      return element;
    }
    return {
      checked: function (id) { return get(id).checked === true; },
      files: function (id) { return Array.from(get(id).files || []); },
      focus: function (id) { get(id).focus(); },
      on: function (id, type, handler) { get(id).addEventListener(type, handler); },
      reset: function () {
        const form = sourceDocument.querySelector('form');
        requireCondition(Boolean(form), 'cockpit form is missing');
        form.reset();
      },
      setDisabled: function (id, disabled) { get(id).disabled = disabled; },
      setHidden: function (id, hidden) { get(id).hidden = hidden; },
      setHtml: function (id, html) { get(id).innerHTML = html; },
      setText: function (id, value) { get(id).textContent = value; },
      value: function (id) { return get(id).value; }
    };
  }

  function readInteger(dom, id, label) {
    const source = String(dom.value(id)).trim();
    requireCondition(source !== '', `${label} is required`);
    const value = Number(source);
    requireCondition(Number.isInteger(value) && value >= 0, `${label} must be a nonnegative integer`);
    return value;
  }

  function scopeParts(scopeId, protocol) {
    if (scopeId === protocol.annualPilot.id) {
      const clusters = protocol.annualPilot.clusterIds.map(function (clusterId) {
        return findCluster(protocol, clusterId);
      });
      return {
        scope: protocol.annualPilot,
        modules: clusters.reduce(function (all, cluster) {
          return all.concat(cluster.modules);
        }, []),
        integrations: clusters.map(function (cluster) { return cluster.integration; }),
        isAnnual: true
      };
    }
    const cluster = findCluster(protocol, scopeId);
    return {
      scope: cluster,
      modules: cluster.modules,
      integrations: [cluster.integration],
      isAnnual: false
    };
  }

  function renderProtocolOptions(dom, protocol) {
    const scopeOptions = protocol.clusters.map(function (cluster) {
      return `<option value="${escapeHtml(cluster.id)}">Cluster ${cluster.order}: ${escapeHtml(cluster.id)} (${cluster.budgetUnits} UE)</option>`;
    });
    scopeOptions.push(
      `<option value="${escapeHtml(protocol.annualPilot.id)}">Jahrespfad (${protocol.annualPilot.budgetUnits} UE)</option>`
    );
    dom.setHtml('scope-id', '<option value="">Bitte auswählen</option>' + scopeOptions.join(''));
    const labels = {
      'first-half': 'erstes Halbjahr',
      'second-half': 'zweites Halbjahr',
      'full-year': 'gesamtes Schuljahr',
      'under-10': 'unter 10',
      '10-19': '10 bis 19',
      '20-29': '20 bis 29',
      '30-plus': '30 oder mehr',
      desktop: 'Desktop', laptop: 'Laptop', tablet: 'Tablet', mixed: 'gemischt',
      chromium: 'Chromium', firefox: 'Firefox', safari: 'Safari',
      offline: 'offline',
      'school-network': 'Schulnetz',
      'local-fallback': 'lokaler Fallback'
    };
    Object.keys(CONTEXT_CONTROL_IDS).forEach(function (field) {
      dom.setHtml(
        CONTEXT_CONTROL_IDS[field],
        optionMarkup(protocol.contextEnums[field], labels)
      );
    });
    const pulseMarkup = protocol.learnerPulseItems.map(function (item) {
      const itemId = slug(item.id);
      const countFields = [
        ['agree', 'stimme zu'], ['partly', 'teils/teils'],
        ['disagree', 'stimme nicht zu'], ['noAnswer', 'keine Antwort']
      ].map(function (definition) {
        const id = `pulse-${itemId}-${slug(definition[0])}`;
        return `<div class="field"><label for="${id}">${escapeHtml(definition[1])}</label><input id="${id}" type="number" min="0" step="1" required></div>`;
      }).join('');
      return `<div class="pulse-card"><h3>${escapeHtml(item.prompt)}</h3><div class="pulse-grid">${countFields}</div></div>`;
    }).join('');
    dom.setHtml('pulse-fields', pulseMarkup);
  }

  function renderScopeFields(dom, scopeId, protocol) {
    if (!scopeId) {
      dom.setText('planned-units', 'Geplantes Budget: –');
      dom.setHtml('phase-fields', '<h3 id="phase-title">Abgeschlossene Pflichtphasen</h3>');
      dom.setHtml('quality-fields', '');
      dom.setHtml('annual-unit-fields', '<h3 id="annual-units-title">Tatsächliche UE je Cluster</h3>');
      dom.setHidden('annual-unit-fields', true);
      return;
    }
    const parts = scopeParts(scopeId, protocol);
    dom.setText('planned-units', `Geplantes Budget: ${parts.scope.budgetUnits} UE`);
    const phaseMarkup = requiredPhaseIds(parts.modules).map(function (phaseId) {
      const id = `phase-${slug(phaseId)}`;
      return `<div class="check-row"><input id="${id}" type="checkbox"><label for="${id}">${escapeHtml(phaseId)}</label></div>`;
    }).join('');
    dom.setHtml(
      'phase-fields',
      '<h3 id="phase-title">Abgeschlossene Pflichtphasen</h3>' + phaseMarkup
    );
    const qualityMarkup = [];
    parts.modules.forEach(function (module) {
      const criteria = module.criteria.map(function (criterion) {
        const id = `criterion-${slug(criterion.criterionId)}`;
        return `<div class="field"><label for="${id}">${escapeHtml(criterion.criterionId)}</label><select id="${id}">${optionMarkup(BAND_VALUES)}</select></div>`;
      }).join('');
      qualityMarkup.push(`<div class="criterion-card"><h3>Modul ${escapeHtml(module.moduleId)}</h3><div class="criterion-grid">${criteria}</div></div>`);
    });
    parts.integrations.forEach(function (integration) {
      const integrationId = slug(integration.integrationContractId);
      const criteria = integration.criteria.map(function (criterion) {
        const id = `criterion-${slug(criterion.criterionId)}`;
        return `<div class="field"><label for="${id}">${escapeHtml(criterion.criterionId)}</label><select id="${id}">${optionMarkup(BAND_VALUES)}</select></div>`;
      }).join('');
      qualityMarkup.push(
        `<div class="criterion-card"><h3>Integration ${escapeHtml(integration.integrationContractId)}</h3><div class="criterion-grid">${criteria}</div>` +
        `<div class="check-row"><input id="handoff-present-${integrationId}" type="checkbox"><label for="handoff-present-${integrationId}">Übergabeprodukt liegt vor.</label></div>` +
        `<div class="check-row"><input id="handoff-reused-${integrationId}" type="checkbox"><label for="handoff-reused-${integrationId}">Übergabeprodukt wurde funktional weiterverwendet.</label></div></div>`
      );
    });
    dom.setHtml('quality-fields', qualityMarkup.join(''));
    if (parts.isAnnual) {
      const annualUnits = protocol.clusters.map(function (cluster) {
        const id = `annual-units-${slug(cluster.id)}`;
        return `<div class="field"><label for="${id}">${escapeHtml(cluster.id)} (maximal ${cluster.budgetUnits} UE)</label><input id="${id}" type="number" min="0" max="${cluster.budgetUnits}" step="1" required></div>`;
      }).join('');
      dom.setHtml(
        'annual-unit-fields',
        '<h3 id="annual-units-title">Tatsächliche UE je Cluster</h3><div class="form-grid">' + annualUnits + '</div>'
      );
      dom.setHidden('annual-unit-fields', false);
    } else {
      dom.setHtml('annual-unit-fields', '<h3 id="annual-units-title">Tatsächliche UE je Cluster</h3>');
      dom.setHidden('annual-unit-fields', true);
    }
  }

  function collectContext(dom, protocol) {
    const startYear = readInteger(dom, 'context-school-year', 'schoolYear');
    requireCondition(startYear >= 2020 && startYear <= 2099, 'schoolYear is invalid');
    const context = {
      schoolYear: `${startYear}-${String((startYear + 1) % 100).padStart(2, '0')}`
    };
    Object.keys(CONTEXT_CONTROL_IDS).forEach(function (field) {
      const value = dom.value(CONTEXT_CONTROL_IDS[field]);
      requireEnum(value, protocol.contextEnums[field], `context ${field}`);
      context[field] = value;
    });
    return context;
  }

  function collectDeliveryTime(dom, parts, protocol) {
    const phases = requiredPhaseIds(parts.modules);
    const completed = phases.filter(function (phaseId) {
      return dom.checked(`phase-${slug(phaseId)}`);
    });
    const delivery = {
      plannedUnits: parts.scope.budgetUnits,
      actualUnits: readInteger(dom, 'actual-units', 'actualUnits'),
      completedPhaseIds: completed,
      requiredLearningPhasesCompleted: completed.length === phases.length,
      fallbackActivated: dom.checked('fallback-activated'),
      technicalStartupMinutes: readInteger(dom, 'technical-startup-minutes', 'technicalStartupMinutes'),
      supportDemandBand: dom.value('support-demand-band'),
      externalDisruptionCode: dom.value('external-disruption-code')
    };
    if (parts.isAnnual) {
      delivery.clusterOrder = protocol.annualPilot.clusterIds.slice();
      delivery.clusterActualUnits = protocol.clusters.map(function (cluster) {
        return {
          clusterId: cluster.id,
          actualUnits: readInteger(dom, `annual-units-${slug(cluster.id)}`, `${cluster.id} actualUnits`)
        };
      });
    }
    return delivery;
  }

  function collectLearningQuality(dom, parts) {
    const moduleResults = parts.modules.map(function (module) {
      const criteria = module.criteria.map(function (criterion) {
        return {
          criterionId: criterion.criterionId,
          band: dom.value(`criterion-${slug(criterion.criterionId)}`)
        };
      });
      return {
        pilotAssignmentId: module.pilotAssignmentId,
        moduleId: module.moduleId,
        criteria: criteria,
        result: criteria.every(function (criterion) { return criterion.band === 'strong'; }) ? 'pass' : 'fail'
      };
    });
    const integrationResults = parts.integrations.map(function (integration) {
      const integrationId = slug(integration.integrationContractId);
      const criteria = integration.criteria.map(function (criterion) {
        return {
          criterionId: criterion.criterionId,
          band: dom.value(`criterion-${slug(criterion.criterionId)}`)
        };
      });
      const handoffProductPresent = dom.checked(`handoff-present-${integrationId}`);
      const handoffReused = dom.checked(`handoff-reused-${integrationId}`);
      return {
        pilotAssignmentId: integration.pilotAssignmentId,
        integrationContractId: integration.integrationContractId,
        criteria: criteria,
        handoffProductPresent: handoffProductPresent,
        handoffReused: handoffReused,
        result: criteria.every(function (criterion) { return criterion.band === 'strong'; }) &&
          handoffProductPresent && handoffReused ? 'pass' : 'fail'
      };
    });
    return {moduleResults: moduleResults, integrationResults: integrationResults};
  }

  function collectLearnerPulse(dom, protocol) {
    const status = dom.value('learner-pulse-status');
    if (status === 'suppressed-small-group') {
      return {status: 'suppressed-small-group'};
    }
    requireCondition(status === 'reported', 'learner pulse status is invalid');
    return {
      status: 'reported',
      classResponseCount: readInteger(dom, 'class-response-count', 'classResponseCount'),
      items: protocol.learnerPulseItems.map(function (item) {
        const itemId = slug(item.id);
        return {
          itemId: item.id,
          agree: readInteger(dom, `pulse-${itemId}-agree`, `${item.id} agree`),
          partly: readInteger(dom, `pulse-${itemId}-partly`, `${item.id} partly`),
          disagree: readInteger(dom, `pulse-${itemId}-disagree`, `${item.id} disagree`),
          noAnswer: readInteger(dom, `pulse-${itemId}-noanswer`, `${item.id} noAnswer`)
        };
      })
    };
  }

  function collectTechnicalPrivacy(dom) {
    return {
      technicalFunction: dom.value('technical-function'),
      fallbackEquivalentLearningFunction: dom.checked('fallback-equivalent'),
      problemCode: dom.value('problem-code'),
      severity: dom.value('severity'),
      privacyGate: dom.value('privacy-gate')
    };
  }

  function collectFormValue(dom, state, protocol) {
    const parts = scopeParts(state.scopeId, protocol);
    const formValue = {
      context: collectContext(dom, protocol),
      deliveryTimeEvidence: collectDeliveryTime(dom, parts, protocol),
      learningQualityEvidence: collectLearningQuality(dom, parts),
      learnerPulseEvidence: collectLearnerPulse(dom, protocol),
      technicalPrivacyEvidence: collectTechnicalPrivacy(dom)
    };
    if (parts.isAnnual) {
      formValue.clusterPackages = protocol.annualPilot.clusterIds.map(function (clusterId) {
        return cloneJson(state.importedClusters.get(clusterId));
      });
    }
    return formValue;
  }

  function downloadPackage(payload) {
    const blob = new Blob([serializePackage(payload)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `ium11-${payload.scopeId.toLowerCase()}-${payload.packageId}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function readLocalFile(file) {
    return new Promise(function (resolve, reject) {
      const reader = new FileReader();
      reader.onload = function () { resolve(String(reader.result)); };
      reader.onerror = function () { reject(new Error('local JSON file could not be read')); };
      reader.readAsText(file);
    });
  }

  function hasAnnualImports(state, protocol) {
    const imported = Array.from(state.importedClusters.values());
    return imported.length === protocol.annualPilot.clusterIds.length &&
      sameJson(
        imported.map(function (payload) { return payload.scopeId; }),
        protocol.annualPilot.clusterIds
      ) &&
      imported.every(function (payload) {
        return payload.packageType === 'cluster-evidence' &&
          payload.result === 'pass' &&
          payload.protocolVersion === protocol.protocolVersion &&
          payload.protocolFingerprint === protocol.protocolFingerprint &&
          payload.toolVersion === protocol.toolVersion &&
          payload.timeModelFingerprint === protocol.timeModelFingerprint;
      });
  }

  function initializeCockpit(sourceDocument, protocol) {
    const dom = createDomAdapter(sourceDocument);
    const state = {
      readiness: new Set(),
      scopeId: null,
      importedClusters: new Map(),
      draft: null,
      validatedPackage: null
    };

    function readinessComplete() {
      return state.readiness.size === READINESS_IDS.length;
    }

    function showError(error) {
      const cause = FLOW_CAUSES[error.code] || FLOW_CAUSES['invalid-evidence'];
      dom.setText(
        'error-summary',
        `Ursache: ${cause} Betroffener Scope: ${error.scopeId}. Nächster Schritt: ${error.nextStep}`
      );
      dom.setHidden('error-summary', false);
      dom.focus('error-summary');
    }

    function clearError() {
      dom.setText('error-summary', '');
      dom.setHidden('error-summary', true);
    }

    function renderWarnings(warnings) {
      if (!warnings.length) {
        dom.setHtml('warning-list', '<li>✓ Keine offene Entwicklungswarnung.</li>');
        return;
      }
      dom.setHtml(
        'warning-list',
        warnings.map(function (warning) {
          return `<li>⚠ Entwicklungswarnung: ${escapeHtml(warning.itemId)}</li>`;
        }).join('')
      );
    }

    function invalidateDraft() {
      state.draft = null;
      state.validatedPackage = null;
      dom.setDisabled('download-button', true);
    }

    function updateControls() {
      const ready = readinessComplete();
      const annualSelected = state.scopeId === protocol.annualPilot.id;
      const annualReady = annualSelected && hasAnnualImports(state, protocol);
      const evidenceEnabled = ready && Boolean(state.scopeId) && (!annualSelected || annualReady);
      dom.setDisabled('pilot-context-fields', !ready);
      dom.setDisabled('import-fields', !ready || !annualSelected);
      dom.setDisabled(
        'import-button',
        !ready || !annualSelected || dom.files('cluster-import').length !== 4
      );
      dom.setDisabled('evidence-fields', !evidenceEnabled);
      dom.setDisabled('validate-button', !evidenceEnabled);
      dom.setDisabled('download-button', !state.validatedPackage);
      dom.setHidden('annual-lock-note', !annualSelected || annualReady);
      dom.setText(
        'readiness-status',
        `${ready ? '✓' : '○'} ${state.readiness.size} von ${READINESS_IDS.length} Voraussetzungen bestätigt.`
      );
      dom.setText(
        'import-status',
        `${annualReady ? '✓' : '○'} ${state.importedClusters.size} von 4 Clusterpaketen geprüft.`
      );
    }

    function refreshReadiness() {
      state.readiness.clear();
      READINESS_IDS.forEach(function (id) {
        if (dom.checked(id)) {
          state.readiness.add(id);
        }
      });
      if (!readinessComplete()) {
        invalidateDraft();
      }
      updateControls();
    }

    function selectScope() {
      invalidateDraft();
      state.importedClusters.clear();
      state.scopeId = dom.value('scope-id') || null;
      renderScopeFields(dom, state.scopeId, protocol);
      clearError();
      dom.setText('derived-result', '–');
      renderWarnings([]);
      updateControls();
    }

    function updatePulseVisibility() {
      const suppressed = dom.value('learner-pulse-status') === 'suppressed-small-group';
      dom.setHidden('learner-count-fields', suppressed);
      dom.setDisabled('learner-count-fields', suppressed);
      invalidateDraft();
      updateControls();
    }

    async function importClusterPackages() {
      invalidateDraft();
      state.importedClusters.clear();
      try {
        const files = dom.files('cluster-import');
        if (files.length !== 4) {
          throw makeFlowError(
            'annual-clusters-required', state.scopeId,
            'Wählen Sie genau vier aktuelle Clusterpakete in Protokollreihenfolge aus.'
          );
        }
        const sources = await Promise.all(files.map(readLocalFile));
        const parsed = sources.map(function (source) {
          return parsePackage(source, protocol);
        });
        const expectedIds = protocol.annualPilot.clusterIds;
        requireCondition(
          sameJson(parsed.map(function (payload) { return payload.scopeId; }), expectedIds),
          'cluster import order differs from protocol'
        );
        requireCondition(
          new Set(parsed.map(function (payload) { return payload.packageId; })).size === 4,
          'cluster imports require distinct package IDs'
        );
        requireCondition(
          parsed.every(function (payload) {
            return payload.packageType === 'cluster-evidence' && payload.result === 'pass';
          }),
          'annual imports require positive cluster packages'
        );
        parsed.forEach(function (payload) {
          state.importedClusters.set(payload.scopeId, payload);
        });
        clearError();
        dom.setText('status-message', '✓ Vier Clusterpakete wurden lokal geprüft. Der Jahresmodus ist freigeschaltet.');
      } catch (error) {
        state.importedClusters.clear();
        const flowError = isFlowError(error) ? error : makeFlowError(
          'import-invalid', state.scopeId,
          'Korrigieren oder ersetzen Sie die lokale JSON-Datei und importieren Sie alle vier Pakete erneut.'
        );
        showError(flowError);
        dom.setText('status-message', '✕ Import abgewiesen; kein Wert wurde übernommen.');
      }
      updateControls();
    }

    function validateDraft() {
      clearError();
      invalidateDraft();
      try {
        if (!readinessComplete()) {
          throw makeFlowError(
            'readiness-incomplete', state.scopeId,
            'Bestätigen Sie alle sieben Bereitschaftsvoraussetzungen.'
          );
        }
        if (!state.scopeId) {
          throw makeFlowError(
            'scope-required', state.scopeId,
            'Wählen Sie eine Pilotstufe aus.'
          );
        }
        if (state.scopeId === protocol.annualPilot.id && !hasAnnualImports(state, protocol)) {
          throw makeFlowError(
            'annual-clusters-required', state.scopeId,
            'Importieren Sie vier positive Clusterpakete in Protokollreihenfolge.'
          );
        }
        const formValue = collectFormValue(dom, state, protocol);
        if (formValue.technicalPrivacyEvidence.privacyGate === 'fail') {
          const parts = scopeParts(state.scopeId, protocol);
          const derived = parts.isAnnual
            ? deriveAnnualEvidenceResult(formValue, protocol)
            : deriveClusterResult(formValue, parts.scope, protocol);
          state.draft = cloneJson(formValue);
          dom.setText('derived-result', derived.result);
          renderWarnings(derived.developmentWarnings || []);
          throw makeFlowError(
            'privacy-blocked', state.scopeId,
            'Entfernen Sie die Privacyverletzung und führen Sie den Pilot erneut durch.'
          );
        }
        const created = createEvidencePackage(state.scopeId, formValue, protocol);
        state.draft = cloneJson(created);
        state.validatedPackage = validateEvidencePackage(created, protocol);
        dom.setText('derived-result', state.validatedPackage.result);
        renderWarnings(state.validatedPackage.developmentWarnings);
        if (state.validatedPackage.developmentWarnings.length) {
          showError(makeFlowError(
            'learner-warning', state.scopeId,
            'Bearbeiten Sie die benannte Lernbedingung und wiederholen Sie diesen Pilot-Scope.'
          ));
          dom.setText('status-message', '⚠ Paket validiert; Ergebnis fail mit offener Entwicklungswarnung.');
        } else {
          dom.setText(
            'status-message',
            `✓ Paket frisch abgeleitet und validiert; Ergebnis ${state.validatedPackage.result}.`
          );
        }
      } catch (error) {
        if (!isFlowError(error)) {
          state.draft = null;
          state.validatedPackage = null;
          showError(makeFlowError(
            'invalid-evidence', state.scopeId,
            'Prüfen Sie die markierten Aggregat-, Summen- und Pflichtangaben und leiten Sie erneut ab.'
          ));
          dom.setText('status-message', '✕ Paket nicht validiert; Download bleibt gesperrt.');
        } else {
          showError(error);
          dom.setText('status-message', '✕ Gate nicht bestanden; Download bleibt gesperrt.');
        }
      }
      updateControls();
    }

    function exportValidatedPackage() {
      try {
        if (!state.validatedPackage) {
          throw makeFlowError(
            'export-blocked', state.scopeId,
            'Leiten Sie das Paket nach der letzten Eingabeänderung erneut ab.'
          );
        }
        const validated = validateEvidencePackage(state.validatedPackage, protocol);
        requireCondition(validated.technicalPrivacyEvidence.privacyGate === 'pass', 'privacyGate blocks export');
        downloadPackage(validated);
        dom.setText('status-message', '✓ Das validierte JSON-Paket wurde bewusst heruntergeladen.');
      } catch (error) {
        showError(isFlowError(error) ? error : makeFlowError(
          'export-blocked', state.scopeId,
          'Prüfen Sie Privacy und Evidenz erneut, bevor Sie einen Download auslösen.'
        ));
      }
      updateControls();
    }

    function clearState() {
      state.readiness.clear();
      state.scopeId = null;
      state.importedClusters.clear();
      state.draft = null;
      state.validatedPackage = null;
      dom.reset();
      renderScopeFields(dom, null, protocol);
      clearError();
      dom.setText('derived-result', '–');
      renderWarnings([]);
      dom.setText('status-message', '○ Flüchtiger Zustand vollständig verworfen.');
      updateControls();
    }

    renderProtocolOptions(dom, protocol);
    renderScopeFields(dom, null, protocol);
    renderWarnings([]);
    READINESS_IDS.forEach(function (id) {
      dom.on(id, 'change', refreshReadiness);
    });
    dom.on('scope-id', 'change', selectScope);
    dom.on('learner-pulse-status', 'change', updatePulseVisibility);
    dom.on('cluster-import', 'change', updateControls);
    dom.on('import-button', 'click', importClusterPackages);
    dom.on('validate-button', 'click', validateDraft);
    dom.on('download-button', 'click', exportValidatedPackage);
    dom.on('clear-button', 'click', clearState);
    dom.on('pilot-form', 'input', function () {
      invalidateDraft();
      updateControls();
    });
    updatePulseVisibility();
    refreshReadiness();
    return state;
  }

  const api = {
    evaluateLearnerPulse: evaluateLearnerPulse,
    deriveClusterResult: deriveClusterResult,
    deriveAnnualResult: deriveAnnualResult,
    validateEvidencePackage: validateEvidencePackage,
    createPackageId: createPackageId,
    createEvidencePackage: createEvidencePackage,
    serializePackage: serializePackage,
    parsePackage: parsePackage
  };

  if (typeof window !== 'undefined') {
    window.IUM11 = api;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    const start = function () {
      requireCondition(Boolean(window.IUM11_PROTOCOL), 'IUM11 protocol is missing');
      initializeCockpit(document, window.IUM11_PROTOCOL);
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', start, {once: true});
    } else {
      start();
    }
  }
}());
