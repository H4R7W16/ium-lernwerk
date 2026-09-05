"""Closed pre-production governance contract; no natural-language truth inference."""
from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlparse

BASE = 'roadmap/v2/foundations/governance/'
LXF = 'roadmap/v2/foundations/learning-experience/'
CONTRACT = BASE + 'governance-contract.json'
SCHEMA = 'schemas/v2/governance.schema.json'
FILES = (CONTRACT, BASE + 'status.json', BASE + 'README.md', BASE + 'inventory.md',
         BASE + 'validation-report.md', SCHEMA)
REVIEW_INPUTS = frozenset(p for p in FILES if p != BASE + 'status.json') | {
    'roadmap/v2/status.json', 'roadmap/v2/requirements/requirements.json',
    'roadmap/v2/foundations/curriculum/status.json',
    'roadmap/v2/foundations/curriculum/gap-assessments.json',
    'roadmap/v2/foundations/sources/source-register.json',
    LXF + 'status.json', LXF + 'validation-report.md', LXF + 'evidence-register.json',
    LXF + 'learning-architecture.json', LXF + 'experience-gates.json',
    'docs/superpowers/specs/2026-09-03-ium-v2-controlled-rebaseline-design.md',
    'docs/platform/README.md', 'docs/platform/device-verification.md',
    'pilot/ium5-gate-b/protocol.json', 'pilot/docs/publication-contract.json',
    'LICENSE', 'LICENSE-CONTENT.md', 'license-policy.json',
    'apps/lernwerk-portal/public/asset-licenses.json',
    'modules/IUM-5-CORE-05/assets/licenses.json',
}
BASE_COMMIT = 'd11a8bc69775525ec0162516275bb39f5dc9c441'
BOUNDARIES = {
    'contentProduction': 'frozen', 'publication': 'closed', 'classroomPilot': 'not-started',
    'cutover': 'not-approved', 'automaticPromotion': False, 'personalTelemetryAllowed': False,
    'privateReflectionCollectionAllowed': False, 'realEvidenceInRepositoryAllowed': False,
    'thirdPartyRelicensingAllowed': False, 'fictionalCaseFulfillsOwnReflection': False,
}
FORBIDDEN = ['wissenschaftlich bewiesen', 'für alle geeignet', 'vollständig barrierefrei',
             'garantiert lernwirksam']
CLAIMS = {
    'curriculum': ('checked-curriculum-mapping', 'subject-didactics-reviewer', 'not-established',
                   {'roadmap/v2/foundations/curriculum/status.json', 'roadmap/v2/requirements/requirements.json'}),
    'evidence': ('reviewed-evidence-and-design-contract', 'source-reviewer', 'foundation-only',
                 {LXF+'status.json', LXF+'evidence-register.json', LXF+'learning-architecture.json'}),
    'accessibility': ('scoped-accessibility-review-with-limitations', 'accessibility-reviewer', 'foundation-only',
                      {LXF+'validation-report.md', 'docs/platform/device-verification.md'}),
    'technical': ('tests-at-exact-revision', 'technical-reviewer', 'foundation-only',
                  {LXF+'status.json', LXF+'validation-report.md'}),
    'usage': ('documented-participant-walkthrough-or-usability-test', 'teacher-reviewer', 'not-established', {LXF+'status.json'}),
    'pilot': ('documented-classroom-pilot', 'teacher-reviewer', 'not-established',
              {LXF+'status.json', 'pilot/ium5-gate-b/protocol.json'}),
    'effect': ('robust-contextualized-learning-effect-evidence', 'effect-reviewer', 'not-established',
               {LXF+'status.json', LXF+'evidence-register.json'}),
}
CLAIM_LABELS = dict(curriculum='curricular zugeordnet', evidence='evidenzorientiert gestaltet',
    accessibility='barrierearm entwickelt', technical='technisch verifiziert', usage='mit Nutzenden geprüft',
    pilot='unterrichtlich pilotiert', effect='lernwirksam')
ROLE_IDS = {'author', 'project-decision', 'subject-didactics-reviewer', 'source-reviewer',
            'accessibility-reviewer', 'technical-reviewer', 'teacher-reviewer', 'effect-reviewer',
            'privacy-reviewer', 'rights-reviewer', 'integration-reviewer', 'operator', 'school-controller'}
QUESTIONS = {
    'GOV-Q-OPERATOR': ('project-decision', {'publication'}),
    'GOV-Q-SCHOOL': ('project-decision', {'usage', 'pilot'}),
    'GOV-Q-REVIEWERS': ('project-decision', {'publication', 'pilot'}),
    'CUR-Q-002': ('IUM-V2-CUR', {'own-reflection-module'}),
    'GOV-Q-RIGHTS': ('project-decision', {'publication'}),
}
RECHECKS = {'law': 'privacy-reviewer', 'source': 'source-reviewer', 'product': 'technical-reviewer',
            'rights': 'rights-reviewer', 'claim': 'integration-reviewer', 'incident': 'project-decision'}
SOURCE_IDS = {'GOV-SRC-GDPR', 'GOV-SRC-BW', 'GOV-SRC-CC', 'GOV-SRC-WCAG'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def fields(value, expected, label, errors):
    if not isinstance(value, dict) or set(value) != set(expected):
        errors.append(f'GOV {label}: ungültige Felder')
        return False
    return True


def string_set(value):
    return (isinstance(value, list) and bool(value) and all(nonempty(v) for v in value)
            and len(set(value)) == len(value))


def dated(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return False
    try:
        return date.fromisoformat(value) <= date.today()
    except ValueError:
        return False


def records(value, expected_ids, expected_fields, label, errors):
    if not isinstance(value, list):
        errors.append(f'GOV {label}: Liste erforderlich')
        return []
    valid = []
    ids = []
    for item in value:
        if fields(item, expected_fields, label, errors) and nonempty(item.get('id')):
            ids.append(item['id'])
            valid.append(item)
        else:
            errors.append(f'GOV {label}: ungültiger Eintrag')
    if set(ids) != set(expected_ids) or len(ids) != len(set(ids)):
        errors.append(f'GOV {label}: IDs fehlen, sind unbekannt oder doppelt')
    return [item for item in valid if item['id'] in expected_ids]


def read_input(root, relative):
    if not isinstance(relative, str) or '\\' in relative or ':' in relative:
        raise ValueError('kein relativer Repositorypfad')
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Pfad verlässt Repository')
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Pfad verlässt Repository')
    text = target.read_text(encoding='utf-8')
    if not text.strip():
        raise ValueError('leerer Beleg')
    return text


def validate_contract(data, root):
    errors = []
    if not fields(data, ('schemaVersion', 'projectId', 'asOf', 'requirementIds', 'boundaries',
                         'forbiddenClaims', 'roles', 'claims', 'openQuestions', 'rechecks', 'sources'), 'Vertrag', errors):
        return errors
    if type(data['schemaVersion']) is not int or data['schemaVersion'] != 1 or data['projectId'] != 'ium-lernwerk':
        errors.append('GOV Vertragsidentität ungültig')
    if not dated(data['asOf']) or data['requirementIds'] != ['V2-REQ-GOV-001']:
        errors.append('GOV Stichtag oder Anforderungsbezug ungültig')
    boundaries = data['boundaries']
    if (not isinstance(boundaries, dict) or boundaries != BOUNDARIES
            or any(type(boundaries.get(k)) is not type(v) for k,v in BOUNDARIES.items())):
        errors.append('GOV Vorproduktionsgrenzen müssen geschlossen bleiben')
    if data['forbiddenClaims'] != FORBIDDEN:
        errors.append('GOV pauschale Aussagen müssen ausgeschlossen bleiben')
    roles = records(data['roles'], ROLE_IDS, ('id','assignedTo','authority','responsibility'), 'Rollen', errors)
    for role in roles:
        assigned, authority = {
            'author': ('Codex', 'document-preparation'),
            'project-decision': ('Jan', 'project-acceptance'),
            'operator': (None, 'institutional-release'),
            'school-controller': (None, 'institutional-release'),
        }.get(role['id'], (None, 'specialist-review'))
        if role['assignedTo'] != assigned or role['authority'] != authority or not nonempty(role['responsibility']):
            errors.append(f"GOV Rolle {role['id']}: Befugnis oder Besetzung nicht belegt")
    claims = records(data['claims'], CLAIMS, ('id','label','minimumEvidence','reviewerRole','assessment',
                                             'publicUseAllowed','limitation','evidencePaths'), 'Aussagen', errors)
    for claim in claims:
        minimum, reviewer, assessment, refs = CLAIMS[claim['id']]
        if (claim['minimumEvidence'] != minimum or claim['reviewerRole'] != reviewer or claim['assessment'] != assessment
                or claim['publicUseAllowed'] is not False):
            errors.append(f"GOV Aussage {claim['id']}: Mindestnachweis oder öffentliche Sperre verletzt")
        if claim['label'] != CLAIM_LABELS[claim['id']] or not nonempty(claim['limitation']):
            errors.append(f"GOV Aussage {claim['id']}: Aussagegrenze fehlt")
        if not string_set(claim['evidencePaths']) or set(claim['evidencePaths']) != refs:
            errors.append(f"GOV Aussage {claim['id']}: erforderliche Bestandsbelege fehlen")
        else:
            for relative in claim['evidencePaths']:
                try:
                    read_input(root, relative)
                except (OSError, UnicodeError, ValueError):
                    errors.append(f'GOV Beleg unlesbar oder außerhalb Repository: {relative}')
    questions = records(data['openQuestions'], QUESTIONS, ('id','owner','trigger','question','risk','blocks','status'), 'Folgefragen', errors)
    for question in questions:
        owner, gates = QUESTIONS[question['id']]
        if (question['owner'] != owner or question['status'] != 'open'
                or not all(nonempty(question[k]) for k in ('trigger','question','risk'))
                or not string_set(question['blocks']) or set(question['blocks']) != gates):
            errors.append(f"GOV Folgefrage {question['id']}: Eigentümer, Sperre oder Weitergabe fehlt")
    rechecks = records(data['rechecks'], RECHECKS, ('id','ownerRole','trigger','action'), 'Rechecks', errors)
    for item in rechecks:
        if item['ownerRole'] != RECHECKS[item['id']] or not nonempty(item['trigger']) or not nonempty(item['action']):
            errors.append(f"GOV Recheck {item['id']}: unvollständig")
    sources = records(data['sources'], SOURCE_IDS, ('id','title','url','locator','kind','accessed','limitation'), 'Quellen', errors)
    for source in sources:
        valid = all(nonempty(source[k]) for k in ('title','url','locator','kind','limitation')) and dated(source['accessed'])
        if valid:
            try:
                parsed = urlparse(source['url'])
                valid = parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password
            except ValueError:
                valid = False
        if not valid:
            errors.append(f"GOV Quelle {source['id']}: Referenz oder Prüfgrenze ungültig")
    return errors


def validate_status(data, root):
    errors = []
    expected = dict(schemaVersion=1,projectId='ium-lernwerk',id='governance',asOf='2026-09-05',
        workStatus='review',concept='reviewed',reviewType='ai-assisted-document-self-review',reviewer='Codex',
        userAcceptance='pending',baseCommit=BASE_COMMIT,
        lxf07Acceptance=dict(state='approved-by-user',date='2026-09-05',commit=BASE_COMMIT,
                            evidence='2026-09-03 - LXF07 Lern- und Experience-Fundament reviewen'),
        contentProduction='frozen',pilot='not-started',release='closed',nextGate='IUM-V2-AUD',
        nextGateCondition='explicit-gov-user-approval')
    if not fields(data, (*expected, 'inputDigests'), 'Status', errors):
        return errors
    if any(data[k] != v or type(data[k]) is not type(v) for k,v in expected.items()):
        errors.append('GOV Status muss Dokumentenselbstreview, Nutzerabnahme und Freigaben trennen')
    digests = data['inputDigests']
    if not isinstance(digests, dict) or set(digests) != REVIEW_INPUTS:
        errors.append('GOV Prüfumfang unvollständig oder verändert')
        return errors
    for relative in sorted(REVIEW_INPUTS):
        try:
            actual = hashlib.sha256(read_input(root, relative).encode('utf-8')).hexdigest()
            if digests[relative] != actual:
                errors.append(f'GOV Review veraltet: {relative}')
        except (OSError, UnicodeError, ValueError):
            errors.append(f'GOV Prüfeingang fehlt oder ist ungültig: {relative}')
    return errors


def validate_repository(root):
    errors = [f'{relative} fehlt' for relative in FILES if not (root / relative).is_file()]
    for relative, validator in ((CONTRACT, validate_contract), (BASE+'status.json', validate_status)):
        if not (root / relative).is_file():
            continue
        try:
            data = json.loads(read_input(root, relative))
        except (OSError, UnicodeError, ValueError):
            errors.append(f'GOV ungültiges JSON: {relative}')
        else:
            errors.extend(validator(data, root))
    return errors
