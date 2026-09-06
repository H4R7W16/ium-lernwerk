"""Current decision-bound status. Historical V2 and CUT seals remain historical."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
from validate_v2_cutover import (CUT_REVIEW_COMMIT, CutoverError, LIMITS, PACKET,
                                 current_digest, git, read, require, validate as validate_review)

ROOT = Path(__file__).resolve().parents[1]
DECISION = 'roadmap/v2/cutover/decision.json'
POINTER = 'roadmap/v2/cutover/active-baseline.json'
MIGRATIONS = {
    'package.json', 'packages/project-status/index.mjs',
    'apps/project-dashboard/src/data.mjs', 'apps/project-dashboard/src/layouts/Layout.astro',
    'apps/project-dashboard/src/pages/[...page].astro',
    'tests/dashboard/contract.test.mjs', 'tests/dashboard/snapshot.test.mjs',
    'tests/dashboard/browser/dashboard.spec.ts',
    'scripts/validate_v2_cutover.py', 'tests/test_validate_v2_cutover.py',
}
ADDITIONS = {DECISION, 'roadmap/v2/cutover/activation.md',
             'scripts/validate_v2_activation.py', 'tests/test_validate_v2_activation.py'}


class ActivationError(CutoverError):
    pass


def resolve_decision(decision):
    try:
        require(isinstance(decision, dict) and decision['state'] == 'approved-by-user'
                and decision['decisionBy'] == 'user', 'Ausdrückliche Nutzerentscheidung fehlt')
        require(decision['selection'] in ['accept-planning-baseline', 'defer', 'revise'], 'Unbekannte Auswahl')
        accepted = decision['selection'] == 'accept-planning-baseline'
        return dict(activeBaseline='v2' if accepted else 'v1', v2State='active' if accepted else 'building')
    except (CutoverError, KeyError, TypeError) as exc:
        raise ActivationError(str(exc)) from exc


def required_inputs(review):
    return set(review['inputDigests']) | ADDITIONS


def validate(repo, *, decision=None, pointer=None, vault=None):
    try:
        decision = read(repo, DECISION) if decision is None else decision
        pointer = read(repo, POINTER) if pointer is None else pointer
        require(set(decision) == set('schemaVersion projectId gate state decisionBy decidedAt statement selection acceptedCommit reviewSha256 scope acceptedConditions limits'.split()), 'Unbekannter Entscheidungsvertrag')
        require(set(pointer) == set('schemaVersion projectId activeBaseline v2State scope productBaseline acceptedCommit historicalStatusPath decisionPath decisionSha256 inputDigests'.split()), 'Unbekannter Baseline-Zeiger')
        require(decision['schemaVersion'] == pointer['schemaVersion'] == 1
                and decision['projectId'] == pointer['projectId'] == 'ium-lernwerk'
                and decision['gate'] == 'IUM-V2-CUT', 'Falsches Projekt/Gate')
        require(resolve_decision(decision) == dict(activeBaseline='v2', v2State='active'), 'Vertagung/Nacharbeit autorisiert keinen V2-Zeiger')
        require(pointer['activeBaseline'] == 'v2' and pointer['v2State'] == 'active'
                and pointer['productBaseline'] == 'v1', 'Baseline-/Produktgrenze verletzt')
        require(decision['scope'] == pointer['scope'] == 'planning-development', 'Freigabeumfang überschritten')
        require(decision['acceptedCommit'] == pointer['acceptedCommit'] == CUT_REVIEW_COMMIT, 'Nicht angenommener CUT-Commit')
        git(repo, 'merge-base', '--is-ancestor', CUT_REVIEW_COMMIT, 'HEAD')
        require(decision['decidedAt'] == '2026-09-06' and decision['statement'] == 'V2-Aktivierung freigegeben.', 'Freigabeauszug fehlt')
        require(decision['limits'] == LIMITS, 'Produktion/Pilot/Publikation/Integration nicht freigegeben')
        review_bytes = git(repo, 'show', CUT_REVIEW_COMMIT + ':' + PACKET)
        review = json.loads(review_bytes)
        require(current_digest((repo / PACKET).read_bytes()) == current_digest(review_bytes) == decision['reviewSha256'], 'Angenommener CUT-Bericht verändert')
        require(decision['acceptedConditions'] == [q['id'] for q in review['conditions']], 'Fortgeführte Bedingungen unvollständig')
        require(pointer['historicalStatusPath'] == 'roadmap/v2/status.json'
                and pointer['decisionPath'] == DECISION, 'Ungültiger Belegpfad')
        require(pointer['decisionSha256'] == current_digest((repo / DECISION).read_bytes()), 'Entscheidungsdigest falsch')
        require(decision == read(repo, DECISION), 'Entscheidungsinhalt weicht vom gebundenen Beleg ab')
        require(set(pointer['inputDigests']) == required_inputs(review), 'Aktivierungsinputs fehlen oder unbekannt')
        for path, expected in pointer['inputDigests'].items():
            require(expected == current_digest((repo / path).read_bytes()), 'Aktueller Aktivierungsinput verändert: ' + path)
            if path in review['inputDigests'] and path not in MIGRATIONS:
                require(expected == review['inputDigests'][path], 'Geschützte CUT-Grundlage neu versiegelt: ' + path)
        # Check the complete accepted decision packet against its historical Git
        # inputs, even though its old state correctly still says V1/building.
        validate_review(repo, review, vault=vault, require_verified=True, historical=True)
        if vault:
            manifest = read(repo, 'roadmap/v2/dashboard/gates.json')
            note = (vault / manifest[-1]['path']).read_text(encoding='utf-8-sig')
            require(decision['statement'] in note and CUT_REVIEW_COMMIT in note, 'CUT-Nutzerentscheidung im Vault fehlt')
        status = copy.deepcopy(read(repo, 'roadmap/v2/status.json'))
        status.update(activeBaseline='v2', v2State='active', scope='planning-development', productBaseline='v1')
        status['cutover'] = dict(state='approved', acceptedCommit=CUT_REVIEW_COMMIT, date=decision['decidedAt'])
        status['decision'] = decision
        return status
    except (OSError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError, CutoverError) as exc:
        raise ActivationError(str(exc)) from exc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        status = validate(ROOT, vault=args.vault)
    except ActivationError as exc:
        parser.exit(1, 'V2-Aktivierung ungültig: ' + str(exc) + '\n')
    print(json.dumps(status, ensure_ascii=False) if args.json else 'V2 als Planungs-/Entwicklungsbaseline aktiv; V1-Produktstand und alle Einsatzgrenzen erhalten.')
