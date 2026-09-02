import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_v2_rebaseline import (
    validate_repository,
    validate_repository_report,
)


VALID_STATUS = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "activeBaseline": "v1",
    "v2State": "building",
    "contentProduction": "frozen",
    "lxp05": {"state": "frozen", "integration": "unmerged"},
    "cutover": {"state": "not-approved"},
}

VALID_ARCHIVE = {
    "schemaVersion": 1,
    "repository": "H4R7W16/ium-lernwerk",
    "remote": "https://github.com/H4R7W16/ium-lernwerk.git",
    "mainCommit": "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0",
    "candidateRefs": [
        {
            "ref": "origin/feat/lxp05-ium5-experience",
            "commit": "645a1d4ea3c786b08e1320954b522edf86dc9f83",
            "role": "historical-unmerged-review-candidate",
        }
    ],
    "artifactRoots": [
        "docs/research/phase-0",
        "curriculum",
        "roadmap",
        "modules",
        "packages",
        "apps",
        "pilot",
    ],
    "capturedAt": "2026-09-03",
    "statementBoundaries": [
        "V1-Artefakte sind Auditbestand und keine automatisch übernommenen V2-Standards.",
        "Technische Verifikation belegt weder didaktische Qualität noch Lernwirksamkeit.",
        "LXP05 bleibt ungemergt, eingefroren und außerhalb der wiederverwendbaren V2-Basis.",
        "Pilotierung, Veröffentlichung und Cutover sind nicht freigegeben.",
    ],
    "limitations": [
        {
            "id": "dashboard-local-commit",
            "status": "unverified-local",
            "reference": "07bc15e1e70d",
            "statement": (
                "Der im Vault dokumentierte Dashboard-Commit ist nicht als "
                "lokales oder entferntes Git-Objekt reproduzierbar."
            ),
        }
    ],
}

VALID_REQUIREMENT = {
    "id": "V2-REQ-001",
    "title": "V1 und V2 trennen",
    "statement": "V1 bleibt bis zum ausdrücklichen Cutover die aktive Baseline.",
    "domain": "governance",
    "origin": [
        {
            "kind": "vault",
            "target": (
                "2026-09-03 - Entscheidung - Kontrollierte Re-Baseline V2 "
                "und Lern-Experience-Fundament"
            ),
            "label": "Freigegebene Re-Baseline-Entscheidung",
            "required": True,
        }
    ],
    "binding": "project",
    "scope": "system",
    "grades": [5, 6, 7],
    "fulfillmentModes": ["cross-cutting"],
    "coverage": "unassessed",
    "evidence": [],
    "dependencies": [],
    "risks": ["Ein vorzeitiger Cutover vermischt V1- und V2-Aussagen."],
    "gate": "IUM-V2-CUT",
}

VALID_REQUIREMENTS = {
    "schemaVersion": 1,
    "projectId": "ium-lernwerk",
    "asOf": "2026-09-03",
    "requirements": [VALID_REQUIREMENT],
}


def write_json(root: Path, relative_path: str, payload: object) -> None:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_control_files(
    root: Path,
    *,
    status: object = VALID_STATUS,
    archive: object = VALID_ARCHIVE,
    requirements: object | None = None,
    include_requirements: bool = True,
) -> None:
    write_json(root, "roadmap/v2/status.json", status)
    write_json(root, "roadmap/v2/archive/v1-baseline.json", archive)
    if include_requirements:
        write_json(
            root,
            "roadmap/v2/requirements/requirements.json",
            {} if requirements is None else requirements,
        )


class ValidateV2RebaselineTests(unittest.TestCase):
    def test_missing_control_files_fail_closed(self) -> None:
        """Catches a validator that silently accepts an absent V2 control plane."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        self.assertIn("roadmap/v2/status.json fehlt", errors)
        self.assertIn("roadmap/v2/archive/v1-baseline.json fehlt", errors)
        self.assertIn("roadmap/v2/requirements/requirements.json fehlt", errors)

    def test_building_v2_keeps_v1_as_active_baseline(self) -> None:
        """Catches activating V2 before the explicit cutover decision."""
        status = copy.deepcopy(VALID_STATUS)
        status["activeBaseline"] = "v2"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status)
            errors = validate_repository(root)

        self.assertIn(
            "activeBaseline muss v1 sein, solange v2State building ist",
            errors,
        )

    def test_content_production_remains_frozen(self) -> None:
        """Catches opening learner-content work during the re-baseline."""
        status = copy.deepcopy(VALID_STATUS)
        status["contentProduction"] = "open"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status)
            errors = validate_repository(root)

        self.assertIn("contentProduction muss frozen sein", errors)

    def test_lxp05_remains_frozen_and_unmerged(self) -> None:
        """Catches treating the rejected LXP05 candidate as active product work."""
        status = copy.deepcopy(VALID_STATUS)
        status["lxp05"] = {"state": "active", "integration": "merged"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status)
            errors = validate_repository(root)

        self.assertIn("LXP05 muss frozen und unmerged bleiben", errors)

    def test_status_rejects_wrong_fixed_contract_values(self) -> None:
        """Catches weakening any fixed IUM-V2-00 control-state boundary."""
        cases = (
            ("schemaVersion", 2, "V2 schemaVersion muss 1 sein"),
            ("projectId", "other", "V2 projectId muss ium-lernwerk sein"),
            ("v2State", "active", "v2State muss building sein"),
            (
                "cutover",
                {"state": "approved"},
                "cutover muss not-approved sein",
            ),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                status = copy.deepcopy(VALID_STATUS)
                status[field] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_control_files(root, status=status)
                    errors = validate_repository(root)
                self.assertIn(expected, errors)

    def test_main_commit_requires_a_full_sha(self) -> None:
        """Catches an archive that cannot identify the immutable V1 commit."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["mainCommit"] = "dcaff3e"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 mainCommit muss eine vollständige 40-stellige SHA sein",
            errors,
        )

    def test_main_commit_must_match_the_verified_v1_baseline(self) -> None:
        """Catches replacing V1 with a different but syntactically valid commit."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["mainCommit"] = "a" * 40
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 mainCommit muss den verifizierten main-Stand "
            "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0 referenzieren",
            errors,
        )

    def test_candidate_commit_requires_a_full_sha(self) -> None:
        """Catches an ambiguous candidate reference in the V1 archive."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["candidateRefs"][0]["commit"] = "645a1d4"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 candidateRef commit muss eine vollständige 40-stellige SHA sein: "
            "origin/feat/lxp05-ium5-experience",
            errors,
        )

    def test_archive_rejects_wrong_fixed_contract_values(self) -> None:
        """Catches changing the identity or provenance of the V1 baseline."""
        cases = (
            ("schemaVersion", 2, "V1 schemaVersion muss 1 sein"),
            (
                "repository",
                "other/repository",
                "V1 repository muss H4R7W16/ium-lernwerk sein",
            ),
            (
                "remote",
                "https://example.invalid/repository.git",
                "V1 remote muss das geprüfte GitHub-Remote sein",
            ),
            ("capturedAt", "03.09.2026", "V1 capturedAt muss YYYY-MM-DD sein"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                archive = copy.deepcopy(VALID_ARCHIVE)
                archive[field] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_control_files(root, archive=archive)
                    errors = validate_repository(root)
                self.assertIn(expected, errors)

    def test_archive_requires_the_verified_lxp05_candidate(self) -> None:
        """Catches dropping the known unmerged candidate from V1 history."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["candidateRefs"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1-Archiv muss den verifizierten ungemergten LXP05-Kandidaten enthalten",
            errors,
        )

    def test_unknown_top_level_fields_fail_closed(self) -> None:
        """Catches bypassing either contract with an ungoverned status field."""
        status = copy.deepcopy(VALID_STATUS)
        status["progressPercent"] = 80
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["githubDashboardUrl"] = "https://example.invalid/07bc15e1e70d"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, status=status, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V2 status enthält unbekannte Felder: progressPercent",
            errors,
        )
        self.assertIn(
            "V1-Archiv enthält unbekannte Felder: githubDashboardUrl",
            errors,
        )

    def test_archive_requires_all_statement_boundaries(self) -> None:
        """Catches an archive that preserves files but loses their claim limits."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["statementBoundaries"].pop()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1-Archiv muss alle verbindlichen Aussagegrenzen enthalten",
            errors,
        )

    def test_artifact_roots_must_be_repository_relative(self) -> None:
        """Catches leaking a local absolute path into the portable archive."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["artifactRoots"][0] = "C:/Users/Jan/IuM"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1 artifactRoot muss repository-relativ sein: C:/Users/Jan/IuM",
            errors,
        )

    def test_dashboard_commit_stays_an_unverified_limitation(self) -> None:
        """Catches promoting the unavailable dashboard commit to Git evidence."""
        archive = copy.deepcopy(VALID_ARCHIVE)
        archive["limitations"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, archive=archive)
            errors = validate_repository(root)

        self.assertIn(
            "V1-Archiv muss den Dashboard-Commit 07bc15e1e70d als unverified-local begrenzen",
            errors,
        )

    def test_invalid_json_fails_closed(self) -> None:
        """Catches a malformed control file being treated like a valid state."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root)
            (root / "roadmap/v2/status.json").write_text("{", encoding="utf-8")
            errors = validate_repository(root)

        self.assertIn("roadmap/v2/status.json ist kein gültiges JSON", errors)

    def test_valid_archive_waits_only_for_the_requirements_gate(self) -> None:
        """Catches false archive errors once IUM-V2-00 is complete."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, include_requirements=False)
            errors = validate_repository(root)

        self.assertEqual(
            ["roadmap/v2/requirements/requirements.json fehlt"],
            errors,
        )

    def test_duplicate_requirement_ids_fail_closed(self) -> None:
        """Catches ambiguous evidence and dependencies caused by duplicate IDs."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"].append(copy.deepcopy(VALID_REQUIREMENT))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("doppelte Anforderungs-ID V2-REQ-001", errors)

    def test_unknown_requirement_domain_fails_closed(self) -> None:
        """Catches an ungoverned domain bypassing the eight-domain contract."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["domain"] = "ui-decoration"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("unbekannte Domäne ui-decoration", errors)

    def test_malformed_enum_type_fails_closed_without_crashing(self) -> None:
        """Catches non-scalar JSON values crashing enum validation."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["domain"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("unbekannte Domäne []", errors)

    def test_unknown_requirement_enum_values_fail_closed(self) -> None:
        """Catches invalid bindings, scopes, modes, coverage, grades, and evidence kinds."""
        cases = (
            ("binding", "accidental", "unbekannte Bindung accidental in V2-REQ-001"),
            ("scope", "page", "unbekannter Scope page in V2-REQ-001"),
            (
                "fulfillmentModes",
                ["decorative"],
                "unbekannter Erfüllungsmodus decorative in V2-REQ-001",
            ),
            (
                "coverage",
                "complete",
                "unbekannter Abdeckungsstatus complete in V2-REQ-001",
            ),
            ("grades", [8], "unbekannte Klassenstufe 8 in V2-REQ-001"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                requirements = copy.deepcopy(VALID_REQUIREMENTS)
                requirements["requirements"][0][field] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_control_files(root, requirements=requirements)
                    errors = validate_repository(root)
                self.assertIn(expected, errors)

        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0]["kind"] = "file"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)
        self.assertIn("unbekannter Evidenztyp file in V2-REQ-001", errors)

    def test_required_evidence_pointer_needs_a_target(self) -> None:
        """Catches a mandatory source that cannot be followed or reviewed."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0]["target"] = ""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("Pflichtreferenz ohne Ziel in V2-REQ-001", errors)

    def test_required_repository_reference_must_resolve(self) -> None:
        """Catches a required repository source that does not exist."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0] = {
            "kind": "repo",
            "target": "docs/does-not-exist.md",
            "label": "Fehlende Pflichtquelle",
            "required": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "Pflichtreferenz im Repository fehlt in V2-REQ-001: "
            "docs/does-not-exist.md",
            errors,
        )

    def test_optional_missing_repository_reference_is_only_a_warning(self) -> None:
        """Catches historical source gaps incorrectly blocking the V2 gate."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0] = {
            "kind": "repo",
            "target": "docs/historical-source-not-recovered.md",
            "label": "Nicht wiedergefundene historische Quelle",
            "required": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors, warnings = validate_repository_report(root)

        self.assertEqual([], errors)
        self.assertIn(
            "optionale Repository-Referenz fehlt in V2-REQ-001: "
            "docs/historical-source-not-recovered.md",
            warnings,
        )

    def test_optional_vault_reference_is_reported_as_unresolved_warning(self) -> None:
        """Catches an unverifiable historical Vault link being silently accepted."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0]["required"] = False
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors, warnings = validate_repository_report(root)

        self.assertEqual([], errors)
        self.assertIn(
            "optionale Vault-Referenz lokal nicht auflösbar in V2-REQ-001: "
            "2026-09-03 - Entscheidung - Kontrollierte Re-Baseline V2 und "
            "Lern-Experience-Fundament",
            warnings,
        )

    def test_git_evidence_requires_a_full_commit_sha(self) -> None:
        """Catches ambiguous Git proof that is not bound to an immutable commit."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["origin"][0] = {
            "kind": "git",
            "target": "dcaff3e",
            "label": "Zu kurzer Commit",
            "required": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "Git-Referenz muss eine vollständige 40-stellige SHA sein in "
            "V2-REQ-001: dcaff3e",
            errors,
        )

    def test_unknown_requirement_dependency_fails_closed(self) -> None:
        """Catches a sequencing rule that points to no registered requirement."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["dependencies"] = ["V2-REQ-999"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn("unbekannte Abhängigkeit V2-REQ-999", errors)

    def test_cyclic_requirement_dependency_fails_closed(self) -> None:
        """Catches an impossible gate order in the requirements graph."""
        first = copy.deepcopy(VALID_REQUIREMENT)
        first["dependencies"] = ["V2-REQ-002"]
        second = copy.deepcopy(VALID_REQUIREMENT)
        second["id"] = "V2-REQ-002"
        second["dependencies"] = ["V2-REQ-001"]
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"] = [first, second]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "zyklische Anforderungsabhängigkeit V2-REQ-001 -> V2-REQ-002 -> "
            "V2-REQ-001",
            errors,
        )

    def test_covered_requirement_requires_v2_evidence(self) -> None:
        """Catches automatic V2 coverage inferred from the existence of V1 work."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        requirements["requirements"][0]["coverage"] = "covered"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "V2-Abdeckung covered benötigt Evidenz in V2-REQ-001",
            errors,
        )

    def test_missing_required_requirement_field_fails_closed(self) -> None:
        """Catches an incomplete requirement entering the control register."""
        requirements = copy.deepcopy(VALID_REQUIREMENTS)
        del requirements["requirements"][0]["title"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_control_files(root, requirements=requirements)
            errors = validate_repository(root)

        self.assertIn(
            "Pflichtfeld title fehlt oder ist leer in V2-REQ-001",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
