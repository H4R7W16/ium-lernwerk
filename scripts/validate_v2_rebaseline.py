from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath


CONTROL_FILES = (
    Path("roadmap/v2/status.json"),
    Path("roadmap/v2/archive/v1-baseline.json"),
    Path("roadmap/v2/requirements/requirements.json"),
)

FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXPECTED_REPOSITORY = "H4R7W16/ium-lernwerk"
EXPECTED_REMOTE = "https://github.com/H4R7W16/ium-lernwerk.git"
EXPECTED_MAIN_COMMIT = "dcaff3e4b6e96d8c1da3dd1d4dd56f6df6b35ef0"
EXPECTED_LXP05_REF = {
    "ref": "origin/feat/lxp05-ium5-experience",
    "commit": "645a1d4ea3c786b08e1320954b522edf86dc9f83",
    "role": "historical-unmerged-review-candidate",
}
UNVERIFIED_DASHBOARD_COMMIT = "07bc15e1e70d"
EXPECTED_STATEMENT_BOUNDARIES = (
    "V1-Artefakte sind Auditbestand und keine automatisch übernommenen V2-Standards.",
    "Technische Verifikation belegt weder didaktische Qualität noch Lernwirksamkeit.",
    "LXP05 bleibt ungemergt, eingefroren und außerhalb der wiederverwendbaren V2-Basis.",
    "Pilotierung, Veröffentlichung und Cutover sind nicht freigegeben.",
)
REQUIREMENT_DOMAINS = {
    "curriculum",
    "didactics",
    "sources",
    "platform",
    "privacy",
    "governance",
    "public-perception",
    "experience",
}
REQUIREMENT_BINDINGS = {
    "official",
    "project",
    "orientation",
    "candidate",
    "optional",
}
REQUIREMENT_SCOPES = {
    "module",
    "cross-cutting",
    "year",
    "cross-grade",
    "system",
}
REQUIREMENT_GRADES = {5, 6, 7}
FULFILLMENT_MODES = {"direct-module", "integrated", "cross-cutting"}
REQUIREMENT_COVERAGE = {
    "unassessed",
    "uncovered",
    "partial",
    "covered",
    "not-applicable",
}
EVIDENCE_KINDS = {"repo", "git", "vault", "url", "doi"}
REQUIREMENTS_TOP_LEVEL_FIELDS = {
    "schemaVersion",
    "projectId",
    "asOf",
    "requirements",
}
REQUIREMENT_FIELDS = {
    "id",
    "title",
    "statement",
    "domain",
    "origin",
    "binding",
    "scope",
    "grades",
    "fulfillmentModes",
    "coverage",
    "evidence",
    "dependencies",
    "risks",
    "gate",
}
EVIDENCE_FIELDS = {"kind", "target", "label", "required"}
REQUIREMENT_ID_PATTERN = re.compile(r"^V2-REQ-[A-Z0-9-]+$")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_status(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["V2 status muss ein Objekt sein"]

    errors: list[str] = []
    unknown_fields = sorted(
        set(data)
        - {
            "schemaVersion",
            "projectId",
            "activeBaseline",
            "v2State",
            "contentProduction",
            "lxp05",
            "cutover",
        }
    )
    if unknown_fields:
        errors.append(
            "V2 status enthält unbekannte Felder: " + ", ".join(unknown_fields)
        )
    if data.get("schemaVersion") != 1:
        errors.append("V2 schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2 projectId muss ium-lernwerk sein")

    v2_state = data.get("v2State")
    if v2_state != "building":
        errors.append("v2State muss building sein")
    if data.get("activeBaseline") != "v1":
        if v2_state == "building":
            errors.append(
                "activeBaseline muss v1 sein, solange v2State building ist"
            )
        else:
            errors.append("activeBaseline muss v1 sein")
    if data.get("contentProduction") != "frozen":
        errors.append("contentProduction muss frozen sein")

    lxp05 = data.get("lxp05")
    if not isinstance(lxp05, dict) or lxp05 != {
        "state": "frozen",
        "integration": "unmerged",
    }:
        errors.append("LXP05 muss frozen und unmerged bleiben")

    cutover = data.get("cutover")
    if not isinstance(cutover, dict) or cutover != {"state": "not-approved"}:
        errors.append("cutover muss not-approved sein")
    return errors


def _is_repository_relative(value: object) -> bool:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_archive(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["V1-Archiv muss ein Objekt sein"]

    errors: list[str] = []
    unknown_fields = sorted(
        set(data)
        - {
            "schemaVersion",
            "repository",
            "remote",
            "mainCommit",
            "candidateRefs",
            "artifactRoots",
            "capturedAt",
            "statementBoundaries",
            "limitations",
        }
    )
    if unknown_fields:
        errors.append(
            "V1-Archiv enthält unbekannte Felder: " + ", ".join(unknown_fields)
        )
    if data.get("schemaVersion") != 1:
        errors.append("V1 schemaVersion muss 1 sein")
    if data.get("repository") != EXPECTED_REPOSITORY:
        errors.append(f"V1 repository muss {EXPECTED_REPOSITORY} sein")
    if data.get("remote") != EXPECTED_REMOTE:
        errors.append("V1 remote muss das geprüfte GitHub-Remote sein")
    if not isinstance(data.get("mainCommit"), str) or not FULL_SHA_PATTERN.fullmatch(
        data["mainCommit"]
    ):
        errors.append("V1 mainCommit muss eine vollständige 40-stellige SHA sein")
    elif data["mainCommit"] != EXPECTED_MAIN_COMMIT:
        errors.append(
            "V1 mainCommit muss den verifizierten main-Stand "
            f"{EXPECTED_MAIN_COMMIT} referenzieren"
        )

    candidate_refs = data.get("candidateRefs")
    if not isinstance(candidate_refs, list):
        candidate_refs = []
    for candidate in candidate_refs:
        if not isinstance(candidate, dict):
            errors.append("V1 candidateRef muss ein Objekt sein")
            continue
        ref = candidate.get("ref")
        commit = candidate.get("commit")
        if not isinstance(commit, str) or not FULL_SHA_PATTERN.fullmatch(commit):
            errors.append(
                "V1 candidateRef commit muss eine vollständige 40-stellige SHA sein: "
                f"{ref if isinstance(ref, str) else '<unbekannt>'}"
            )
    if EXPECTED_LXP05_REF not in candidate_refs:
        errors.append(
            "V1-Archiv muss den verifizierten ungemergten LXP05-Kandidaten enthalten"
        )

    artifact_roots = data.get("artifactRoots")
    if not isinstance(artifact_roots, list) or not artifact_roots:
        errors.append("V1 artifactRoots dürfen nicht leer sein")
    else:
        for artifact_root in artifact_roots:
            if not _is_repository_relative(artifact_root):
                errors.append(
                    "V1 artifactRoot muss repository-relativ sein: "
                    f"{artifact_root}"
                )

    captured_at = data.get("capturedAt")
    if not isinstance(captured_at, str) or not DATE_PATTERN.fullmatch(captured_at):
        errors.append("V1 capturedAt muss YYYY-MM-DD sein")

    statement_boundaries = data.get("statementBoundaries")
    if statement_boundaries != list(EXPECTED_STATEMENT_BOUNDARIES):
        errors.append("V1-Archiv muss alle verbindlichen Aussagegrenzen enthalten")

    limitations = data.get("limitations")
    dashboard_limited = isinstance(limitations, list) and any(
        isinstance(item, dict)
        and item.get("reference") == UNVERIFIED_DASHBOARD_COMMIT
        and item.get("status") == "unverified-local"
        for item in limitations
    )
    if not dashboard_limited:
        errors.append(
            "V1-Archiv muss den Dashboard-Commit 07bc15e1e70d als "
            "unverified-local begrenzen"
        )
    return errors


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_evidence_pointer(
    pointer: object,
    requirement_id: str,
    root: Path | None,
    warnings: list[str],
) -> list[str]:
    if not isinstance(pointer, dict):
        return [f"Evidenzreferenz muss ein Objekt sein in {requirement_id}"]

    errors: list[str] = []
    unknown_fields = sorted(set(pointer) - EVIDENCE_FIELDS)
    if unknown_fields:
        errors.append(
            f"Evidenzreferenz enthält unbekannte Felder in {requirement_id}: "
            + ", ".join(unknown_fields)
        )

    kind = pointer.get("kind")
    if not isinstance(kind, str) or kind not in EVIDENCE_KINDS:
        errors.append(f"unbekannter Evidenztyp {kind} in {requirement_id}")

    required = pointer.get("required")
    if not isinstance(required, bool):
        errors.append(
            f"Evidenzreferenz required muss boolesch sein in {requirement_id}"
        )

    target = pointer.get("target")
    if not _nonempty_string(target):
        if required is True:
            errors.append(f"Pflichtreferenz ohne Ziel in {requirement_id}")
        else:
            errors.append(f"optionale Referenz ohne Ziel in {requirement_id}")

    if not _nonempty_string(pointer.get("label")):
        errors.append(f"Evidenzreferenz ohne Label in {requirement_id}")

    if kind == "repo" and _nonempty_string(target):
        if not _is_repository_relative(target):
            errors.append(
                f"Repository-Referenz muss repository-relativ sein in "
                f"{requirement_id}: {target}"
            )
        elif root is not None and not (root / target).exists():
            if required is True:
                errors.append(
                    f"Pflichtreferenz im Repository fehlt in {requirement_id}: "
                    f"{target}"
                )
            elif required is False:
                warnings.append(
                    f"optionale Repository-Referenz fehlt in {requirement_id}: "
                    f"{target}"
                )
    elif kind == "vault" and _nonempty_string(target) and required is False:
        warnings.append(
            f"optionale Vault-Referenz lokal nicht auflösbar in {requirement_id}: "
            f"{target}"
        )
    elif (
        kind == "git"
        and _nonempty_string(target)
        and not FULL_SHA_PATTERN.fullmatch(target)
    ):
        errors.append(
            "Git-Referenz muss eine vollständige 40-stellige SHA sein in "
            f"{requirement_id}: {target}"
        )
    return errors


def _dependency_cycle(requirements_by_id: dict[str, dict]) -> list[str] | None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(requirement_id: str) -> list[str] | None:
        state[requirement_id] = 1
        stack.append(requirement_id)
        dependencies = requirements_by_id[requirement_id].get("dependencies", [])
        if isinstance(dependencies, list):
            for dependency in sorted(
                item for item in dependencies if isinstance(item, str)
            ):
                if dependency not in requirements_by_id:
                    continue
                if state.get(dependency, 0) == 1:
                    start = stack.index(dependency)
                    return stack[start:] + [dependency]
                if state.get(dependency, 0) == 0:
                    cycle = visit(dependency)
                    if cycle is not None:
                        return cycle
        stack.pop()
        state[requirement_id] = 2
        return None

    for requirement_id in sorted(requirements_by_id):
        if state.get(requirement_id, 0) == 0:
            cycle = visit(requirement_id)
            if cycle is not None:
                return cycle
    return None


def validate_requirements(
    data: object,
    root: Path | None = None,
    warnings: list[str] | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Anforderungsregister muss ein Objekt sein"]

    report_warnings = warnings if warnings is not None else []
    errors: list[str] = []
    unknown_fields = sorted(set(data) - REQUIREMENTS_TOP_LEVEL_FIELDS)
    if unknown_fields:
        errors.append(
            "V2-Anforderungsregister enthält unbekannte Felder: "
            + ", ".join(unknown_fields)
        )
    if data.get("schemaVersion") != 1:
        errors.append("V2-Anforderungsregister schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Anforderungsregister projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Anforderungsregister asOf muss YYYY-MM-DD sein")

    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append("V2 requirements dürfen nicht leer sein")
        return errors

    seen_ids: set[str] = set()
    requirements_by_id: dict[str, dict] = {}
    for index, requirement in enumerate(requirements):
        if not isinstance(requirement, dict):
            errors.append(f"V2-Anforderung an Position {index} muss ein Objekt sein")
            continue

        requirement_id_value = requirement.get("id")
        requirement_id = (
            requirement_id_value
            if _nonempty_string(requirement_id_value)
            else f"<Position {index}>"
        )
        unknown_requirement_fields = sorted(set(requirement) - REQUIREMENT_FIELDS)
        if unknown_requirement_fields:
            errors.append(
                f"V2-Anforderung enthält unbekannte Felder in {requirement_id}: "
                + ", ".join(unknown_requirement_fields)
            )

        if not _nonempty_string(requirement_id_value):
            errors.append(
                f"Pflichtfeld id fehlt oder ist leer in {requirement_id}"
            )
        elif not REQUIREMENT_ID_PATTERN.fullmatch(requirement_id_value):
            errors.append(f"ungültige Anforderungs-ID {requirement_id_value}")
        elif requirement_id_value in seen_ids:
            errors.append(f"doppelte Anforderungs-ID {requirement_id_value}")
        else:
            seen_ids.add(requirement_id_value)
            requirements_by_id[requirement_id_value] = requirement

        for field in ("title", "statement", "gate"):
            if not _nonempty_string(requirement.get(field)):
                errors.append(
                    f"Pflichtfeld {field} fehlt oder ist leer in {requirement_id}"
                )

        domain = requirement.get("domain")
        if not isinstance(domain, str) or domain not in REQUIREMENT_DOMAINS:
            errors.append(f"unbekannte Domäne {domain}")
        binding = requirement.get("binding")
        if not isinstance(binding, str) or binding not in REQUIREMENT_BINDINGS:
            errors.append(f"unbekannte Bindung {binding} in {requirement_id}")
        scope = requirement.get("scope")
        if not isinstance(scope, str) or scope not in REQUIREMENT_SCOPES:
            errors.append(f"unbekannter Scope {scope} in {requirement_id}")
        coverage = requirement.get("coverage")
        if not isinstance(coverage, str) or coverage not in REQUIREMENT_COVERAGE:
            errors.append(
                f"unbekannter Abdeckungsstatus {coverage} in {requirement_id}"
            )

        grades = requirement.get("grades")
        if not isinstance(grades, list) or not grades:
            errors.append(f"grades dürfen nicht leer sein in {requirement_id}")
        else:
            for grade in grades:
                if not isinstance(grade, int) or grade not in REQUIREMENT_GRADES:
                    errors.append(
                        f"unbekannte Klassenstufe {grade} in {requirement_id}"
                    )
            if len(grades) != len(set(str(grade) for grade in grades)):
                errors.append(f"doppelte Klassenstufe in {requirement_id}")

        modes = requirement.get("fulfillmentModes")
        if not isinstance(modes, list) or not modes:
            errors.append(
                f"fulfillmentModes dürfen nicht leer sein in {requirement_id}"
            )
        else:
            for mode in modes:
                if not isinstance(mode, str) or mode not in FULFILLMENT_MODES:
                    errors.append(
                        f"unbekannter Erfüllungsmodus {mode} in {requirement_id}"
                    )
            if len(modes) != len(set(str(mode) for mode in modes)):
                errors.append(f"doppelter Erfüllungsmodus in {requirement_id}")

        for pointer_field in ("origin", "evidence"):
            pointers = requirement.get(pointer_field)
            if not isinstance(pointers, list) or (
                pointer_field == "origin" and not pointers
            ):
                qualifier = "nicht leer" if pointer_field == "origin" else "eine Liste"
                errors.append(
                    f"{pointer_field} muss {qualifier} sein in {requirement_id}"
                )
                continue
            for pointer in pointers:
                errors.extend(
                    _validate_evidence_pointer(
                        pointer,
                        requirement_id,
                        root,
                        report_warnings,
                    )
                )

        evidence = requirement.get("evidence")
        if coverage == "covered" and (
            not isinstance(evidence, list) or not evidence
        ):
            errors.append(
                f"V2-Abdeckung covered benötigt Evidenz in {requirement_id}"
            )

        dependencies = requirement.get("dependencies")
        if not isinstance(dependencies, list):
            errors.append(f"dependencies muss eine Liste sein in {requirement_id}")
        elif not all(_nonempty_string(item) for item in dependencies):
            errors.append(
                f"dependencies enthält eine leere ID in {requirement_id}"
            )
        elif len(dependencies) != len(set(dependencies)):
            errors.append(f"doppelte Abhängigkeit in {requirement_id}")

        risks = requirement.get("risks")
        if not isinstance(risks, list) or not risks or not all(
            _nonempty_string(risk) for risk in risks
        ):
            errors.append(f"risks dürfen nicht leer sein in {requirement_id}")

    for requirement_id, requirement in sorted(requirements_by_id.items()):
        dependencies = requirement.get("dependencies", [])
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if _nonempty_string(dependency) and dependency not in requirements_by_id:
                errors.append(f"unbekannte Abhängigkeit {dependency}")

    cycle = _dependency_cycle(requirements_by_id)
    if cycle is not None:
        errors.append(
            "zyklische Anforderungsabhängigkeit " + " -> ".join(cycle)
        )
    return errors


def validate_repository_report(root: Path) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors = [
        f"{path.as_posix()} fehlt"
        for path in CONTROL_FILES
        if not (root / path).is_file()
    ]
    validators = (
        (Path("roadmap/v2/status.json"), validate_status),
        (Path("roadmap/v2/archive/v1-baseline.json"), validate_archive),
    )
    for relative_path, validator in validators:
        path = root / relative_path
        if not path.is_file():
            continue
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{relative_path.as_posix()} ist kein gültiges JSON")
            continue
        errors.extend(validator(data))

    requirements_path = Path("roadmap/v2/requirements/requirements.json")
    path = root / requirements_path
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{requirements_path.as_posix()} ist kein gültiges JSON")
        else:
            errors.extend(validate_requirements(data, root, warnings))
    return errors, warnings


def validate_repository(root: Path) -> list[str]:
    errors, _warnings = validate_repository_report(root)
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors, warnings = validate_repository_report(root)
    for warning in warnings:
        print(f"WARNUNG: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("V2 re-baseline validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
