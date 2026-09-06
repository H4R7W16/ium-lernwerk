"""Validate the additive CUT review without rewriting sealed predecessor snapshots.

Historical artifact hashes use Git blob bytes; current text input hashes normalize
CRLF to LF, matching the existing V2 seals. The CLI does not approve a baseline. --vault additionally checks the
recorded user approval excerpts against the original task notes.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKET = 'roadmap/v2/cutover/review.json'
CUT_REVIEW_COMMIT = '0032509af1dfe758548f34f37bb633bae403a9fa'
COMMITS = '59df138 fac45a9 e0171a2 1ff08e5 3a3d4c0 be77fe1 370193b 1b8c0f3 22e9978 beaba6d d11a8bc 9f52cdc dc059cf 5146310 c38ff9b 60c7d0a 85ccc94'.split()
ARTIFACTS = [
    ['archive/v1-baseline.json'], ['requirements/requirements.json'],
    ['foundations/curriculum/source-basis.json', 'foundations/curriculum/gap-assessments.json'],
    ['foundations/sources/inventory.json', 'foundations/sources/traceability.json'],
    ['foundations/learning-experience/legacy-audit.json'],
    ['foundations/learning-experience/evidence-register.json', 'foundations/learning-experience/evidence-synthesis.md'],
    ['foundations/learning-experience/learner-profile.json'],
    ['foundations/learning-experience/learning-architecture.json'],
    ['foundations/learning-experience/material-patterns.json'],
    ['foundations/learning-experience/experience-gates.json', 'foundations/learning-experience/teacher-orchestration.md'],
    ['foundations/learning-experience/status.json', 'foundations/learning-experience/validation-report.md'],
    ['foundations/governance/governance-contract.json', 'foundations/governance/status.json'],
    ['audits/artifact-inventory.json', 'audits/lxp05-lessons.json', 'audits/status.json'],
    ['grades/grade-5/roadmap.json', 'grades/grade-5/curriculum-map.json', 'grades/grade-5/status.json'],
    ['grades/grade-6/roadmap.json', 'grades/grade-6/curriculum-map.json', 'grades/grade-6/status.json'],
    ['grades/grade-7/roadmap.json', 'grades/grade-7/progression.json', 'grades/grade-7/status.json'],
    ['dashboard/validation-report.md'],
]
LIMITS = dict(contentProduction='frozen', pilot='not-started', publication='closed', push='not-authorized', merge='not-authorized', lxp05='frozen-unmerged')
RUNS = {'v2', 'cutover', 'dashboard-unit', 'dashboard-browser', 'ium5'}


class CutoverError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CutoverError(message)


def read(repo, path):
    return json.loads((repo / path).read_text(encoding='utf8'))


@lru_cache(maxsize=256)
def git(repo, *args):
    return subprocess.check_output(['git', *args], cwd=repo, stderr=subprocess.PIPE)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def current_digest(data):
    return digest(data.replace(b'\r\n', b'\n'))


def input_paths(repo):
    """Explicit current contract; CUT reports cannot hash themselves."""
    paths = {p.relative_to(repo).as_posix() for p in (repo / 'roadmap/v2').rglob('*')
             if p.is_file() and '/cutover/' not in p.as_posix()}
    paths.update(p.relative_to(repo).as_posix() for p in (repo / 'schemas/v2').rglob('*.json'))
    for directory in ['packages/project-status', 'apps/project-dashboard/src', 'tests/dashboard']:
        paths.update(p.relative_to(repo).as_posix() for p in (repo / directory).rglob('*') if p.is_file())
    paths.update(['roadmap/v2/cutover/README.md', 'package.json', 'package-lock.json', 'scripts/validate_v2_rebaseline.py',
                  'scripts/validate_v2_cutover.py', 'tests/test_validate_v2_cutover.py',
                  'scripts/project-dashboard.mjs', 'scripts/test-dashboard-browser.mjs',
                  'playwright.dashboard.config.mts', 'apps/project-dashboard/astro.config.mjs'])
    return sorted(paths)


def _validate(repo, d, vault, require_verified, historical):
    source_read = lambda path: json.loads(git(repo, 'show', CUT_REVIEW_COMMIT + ':' + path)) if historical else read(repo, path)
    expected_keys = 'schemaVersion projectId asOf workStatus decisionState candidateCommit candidateMeaning recommendation activeBaseline v2State contentProduction gates requirements conditions options inputDigests verification activationPlan'.split()
    require(isinstance(d, dict) and set(d) == set(expected_keys), 'CUT-Felder fehlen oder sind unbekannt')
    require(d['schemaVersion'] == 1 and d['projectId'] == 'ium-lernwerk' and d['asOf'] == '2026-09-06', 'Falscher CUT-Vertrag')
    require(d['workStatus'] == 'review' and d['decisionState'] == 'awaiting-user-decision', 'Nutzerentscheidung fehlt; CUT bleibt Review')
    require((d['activeBaseline'], d['v2State'], d['contentProduction']) == ('v1', 'building', 'frozen'), 'Vorzeitige Aktivierung')
    baseline = source_read('roadmap/v2/status.json')
    require((baseline['activeBaseline'], baseline['v2State'], baseline['contentProduction'], baseline['cutover']['state']) == ('v1', 'building', 'frozen', 'not-approved'), 'Historische Baseline verändert')
    candidate = git(repo, 'rev-parse', COMMITS[-1]).decode().strip()
    require(d['candidateCommit'] == candidate, 'Kandidat muss der angenommene DASH-Stand sein')
    require(d['recommendation'] == 'accept-planning-baseline' and d['candidateMeaning'], 'Empfehlung oder Kandidateneinordnung fehlt')
    manifest = source_read('roadmap/v2/dashboard/gates.json')[:-1]
    require([g['id'] for g in d['gates']] == [g['id'] for g in manifest], '17 Gates fehlen, doppelt oder umsortiert')
    for i, (gate, source, prefix, artifacts) in enumerate(zip(d['gates'], manifest, COMMITS, ARTIFACTS)):
        commit = git(repo, 'rev-parse', prefix).decode().strip()
        require(gate['sequence'] == i + 1 and gate['state'] == 'approved-by-user' and gate['acceptedCommit'] == commit, 'Gate-Freigabe/Commit falsch')
        git(repo, 'merge-base', '--is-ancestor', commit, candidate)
        evidence = gate['approvalEvidence']
        require(evidence['path'] == source['path'] and isinstance(evidence['excerpt'], str)
                and evidence['excerpt'].startswith('- ' + gate['acceptedAt'])
                and ('Nutzer' in evidence['excerpt']) and re.search(r'\d{4}-\d{2}-\d{2}', gate['acceptedAt']), 'Freigabebeleg fehlt')
        if vault:
            note = (vault / evidence['path']).read_text(encoding='utf-8-sig')
            front = note.split('---', 2)[1]
            require(evidence['excerpt'] in note.splitlines() and re.search(r'^status: done\s*$', front, re.M), 'Vault-Freigabe nicht nachweisbar: ' + gate['id'])
        paths = ['roadmap/v2/' + p for p in artifacts]
        if i == 16:
            paths += ['packages/project-status/index.mjs', 'apps/project-dashboard/src/pages/[...page].astro']
        require([a['path'] for a in gate['artifacts']] == paths, 'Historische Pflichtartefakte fehlen')
        for a in gate['artifacts']:
            require(a['sha256'] == digest(git(repo, 'show', commit + ':' + a['path'])), 'Historischer Artefaktdigest falsch')
    acceptance = source_read('roadmap/v2/dashboard/acceptance.json')
    require(acceptance['gate'] == 'IUM-V2-DASH' and acceptance['state'] == 'approved-by-user'
            and acceptance['decisionBy'] == 'user' and acceptance['acceptedCommit'] == candidate
            and acceptance['nextTask'] == 'IUM-V2-CUT', 'DASH-Abnahme fehlt')
    require(all(acceptance[k] == LIMITS[k] for k in ['contentProduction', 'pilot', 'publication']), 'DASH öffnet keine Einsatzgates')
    requirements = source_read('roadmap/v2/requirements/requirements.json')['requirements']
    require([r['id'] for r in d['requirements']] == [r['id'] for r in requirements], 'Acht Anforderungen fehlen')
    for r, source in zip(d['requirements'], requirements):
        require(r['title'] == source['title'] and r['assessment'] == 'planning-contract-verified'
                and r['coverage'] == 'unassessed' and r['boundary'] and r['gateIds']
                and set(r['gateIds']) <= {g['id'] for g in manifest}, 'Anforderungsprüfung überschreitet Planungsumfang')
    # Carry-forward records keep source wording and responsibility, rather than
    # replacing earlier open conditions with a single green overall status.
    expected = {}
    lxf = source_read('roadmap/v2/foundations/learning-experience/status.json')['review']['openQuestions']
    gov = source_read('roadmap/v2/foundations/governance/governance-contract.json')['openQuestions']
    for q in source_read('roadmap/v2/audits/status.json')['carryForward']:
        source = next(x for x in lxf + gov if x['id'] == q['id'])
        expected[q['id']] = ('foundation', 'open', source)
    for grade in [5, 6, 7]:
        for q in source_read(f'roadmap/v2/grades/grade-{grade}/roadmap.json')['entryGates']:
            state = 'planning-condition-met' if q['id'] in ['R6-R7-TRANSITION', 'R7-DASH'] else 'open'
            expected[q['id']] = ('grade-gate', state, dict(q, question=q['condition']))
    progression = source_read('roadmap/v2/grades/grade-7/progression.json')
    for q in progression['privacyCarry'] + progression['newOpenReflectionIds']:
        expected[q] = ('curriculum-evidence', 'open', {})
    for q in source_read('roadmap/v2/audits/follow-up-tasks.json')['tasks']:
        if q['id'].startswith('IUM-V2-FU-'):
            require(q['state'] == 'blocked-follow-up', 'Folgeauftrag unerwartet geöffnet')
            expected[q['id']] = ('follow-up', 'blocked', dict(question=q['title']))
    require(len(d['conditions']) == len(expected) == 46 and {q['id'] for q in d['conditions']} == set(expected), 'Bedingungen verloren oder doppelt')
    for q in d['conditions']:
        kind, state, source = expected[q['id']]
        require(q['kind'] == kind and q['state'] == state, 'Unzulässiger Bedingungsstatus: ' + q['id'])
        for key in ['owner', 'risk', 'trigger', 'question', 'currentAssessment']:
            require(isinstance(q[key], str) and q[key].strip(), 'Bedingung ohne ' + key)
            if key in source:
                require(q[key] == source[key], 'Originalbedingung verändert: ' + q['id'] + '/' + key)
        require(q['sourcePaths'] and all(p in d['inputDigests'] for p in q['sourcePaths']), 'Bedingungsquelle nicht gebunden')
        require(q['evidenceGateIds'] and set(q['evidenceGateIds']) <= {g['id'] for g in manifest}, 'Bedingung ohne gültige Gate-Evidenz')
    require([o['id'] for o in d['options']] == ['accept-planning-baseline', 'defer', 'revise'], 'Drei Entscheidungsoptionen fehlen')
    for i, option in enumerate(d['options']):
        require(option['decision'] == 'not-selected' and all(option[k] == v for k, v in LIMITS.items()), 'Option überspringt Entscheidung oder Einsatzgrenze')
        require((option['activeBaseline'], option['v2State']) == (('v2', 'active') if i == 0 else ('v1', 'building')), 'Optionsfolge falsch')
    activation = d['activationPlan']
    require(activation['state'] == 'proposal-only' and activation['approvalRequired'] is True
            and activation['historicalStatus'] == 'roadmap/v2/status.json'
            and activation['proposedCurrentPointer'] == 'roadmap/v2/cutover/active-baseline.json'
            and len(activation['steps']) == 5, 'Aktivierungsplan nicht entscheidungsgebunden')
    require(historical or not (repo / activation['proposedCurrentPointer']).exists(), 'Aktivierung gehört nicht in die Entscheidungsvorbereitung')
    verification = d['verification']
    require(verification['state'] in ['pending', 'passed'], 'Ungültiger Prüflaufstatus')
    if require_verified or verification['state'] == 'passed':
        require(verification['state'] == 'passed' and {r['id'] for r in verification['runs']} == RUNS
                and all(r['exitCode'] == 0 and r['command'] and r['result'] for r in verification['runs']), 'Aktuelle vollständige Prüfnachweise fehlen')
    require(set(d['inputDigests']) == set(source_read(PACKET)['inputDigests'] if historical else input_paths(repo)), 'Aktuelle Inputbindung unvollständig')
    for path, expected_digest in d['inputDigests'].items():
        require(expected_digest == current_digest(git(repo, 'show', CUT_REVIEW_COMMIT + ':' + path) if historical else (repo / path).read_bytes()), 'Aktueller Input verändert: ' + path)


def validate(repo, packet=None, *, vault=None, require_verified=False, historical=False):
    try:
        _validate(repo, read(repo, PACKET) if packet is None else packet, vault, require_verified, historical)
    except (OSError, KeyError, TypeError, IndexError, StopIteration, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        raise CutoverError('CUT-Evidenz ungültig oder nicht lesbar: ' + str(exc)) from exc
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path)
    parser.add_argument('--require-verified', action='store_true')
    parser.add_argument('--historical-review', action='store_true', help='Angenommenen CUT-Commit als historischen Review prüfen')
    args = parser.parse_args()
    try:
        if not args.historical_review and any((ROOT / ('roadmap/v2/cutover/' + p)).exists() for p in ['decision.json', 'active-baseline.json']):
            from validate_v2_activation import validate as validate_activation
            validate_activation(ROOT, vault=args.vault)
            print('Aktive V2-Planungsbaseline gültig; Einsatzgrenzen geschlossen.')
            raise SystemExit(0)
        validate(ROOT, vault=args.vault, require_verified=args.require_verified, historical=args.historical_review)
    except ValueError as exc:
        parser.exit(1, str(exc) + '\n')
    print('Historischer CUT-Review gültig:' if args.historical_review else 'CUT-Vertrag gültig:', ' 17 Freigaben, 8 Anforderungen, 46 Bedingungseinträge. Nutzerentscheidung ausstehend; V1 aktiv.')
