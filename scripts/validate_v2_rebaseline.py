from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


CONTROL_FILES = (
    Path("roadmap/v2/status.json"),
    Path("roadmap/v2/archive/v1-baseline.json"),
    Path("roadmap/v2/requirements/requirements.json"),
    Path("roadmap/v2/foundations/curriculum/status.json"),
    Path("roadmap/v2/foundations/curriculum/source-basis.json"),
    Path("roadmap/v2/foundations/curriculum/gap-assessments.json"),
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
CURRICULUM_SOURCE_EXPECTATIONS = {
    "SRC-CUR-BMB-2016": {
        "title": "Gymnasium – Basiskurs Medienbildung (Bildungsplan 2016)",
        "binding": "official",
        "normativeStatus": "enacted",
        "repositoryPath": "curriculum/basiskurs-medienbildung/competencies.json",
        "datasetSha256": "2C39832CD6EE373C643994C69DB6F4411539669923704E6C0F45EF63C2112518",
        "sourceAssetSha256": "84609F1CAF3BDB5D3CFDD0BD6287C348F773F6BD5A2DD40F95D9711B1F338536",
        "recordCount": 59,
        "grades": [5],
        "directUrl": "https://www.bildungsplaene-bw.de/%2CLde/LS/BP2016BW/ALLG/GYM/BMB",
        "contentIdentity": "not-byte-compared",
    },
    "SRC-CUR-INF7-2016": {
        "title": "Gymnasium – Aufbaukurs Informatik (Klasse 7), Bildungsplan 2016",
        "binding": "official",
        "normativeStatus": "enacted",
        "repositoryPath": "curriculum/aufbaukurs-informatik/competencies.json",
        "datasetSha256": "DDE81984622A275C9FFEEDC8B601468F22021F19028DE6B162134C4050DBF0C5",
        "sourceAssetSha256": "57A535001B7371D949C761473DA72E05FB99AA01105B7C59AE34BF7DC47F20A9",
        "recordCount": 94,
        "grades": [7],
        "directUrl": "https://www.bildungsplaene-bw.de/%2CLde/LS/BP2016BW/ALLG/GYM/INF7",
        "contentIdentity": "not-byte-compared",
    },
    "SRC-CUR-LESEHILFE-2026-27": {
        "title": (
            "Lesehilfe Informatik und Medienbildung für die Klassen 5 bis 7 "
            "im Schuljahr 2026/2027"
        ),
        "binding": "orientation",
        "normativeStatus": "orientation",
        "repositoryPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "datasetSha256": "4EAF2AB20BDD508D18B821B4D953EFDF6A6B7CAEA05EF8D904C101B3C4E342C8",
        "sourceAssetSha256": "1BC94255AD35D75782B819C1CA425D7C1F21CEDC6B2012378EC828BAC1451008",
        "recordCount": 125,
        "grades": [5, 6, 7],
        "directUrl": "https://km.baden-wuerttemberg.de/fileadmin/redaktion/m-km/intern/PDF/Dateien/Schulart%C3%BCbergreifend/MINT/2026_Lesehilfe_IuM_Gym_und_Sek_I_bf.pdf",
        "contentIdentity": "sha256-match",
    },
}
EXPECTED_CURRICULUM_GAPS = {
    "BMB16-GYM-IK-GM-003": {
        "sourceId": "SRC-CUR-BMB-2016",
        "sourceBinding": "official",
        "sourceDatasetPath": "curriculum/basiskurs-medienbildung/competencies.json",
        "normativeWeight": "enacted",
        "moduleIds": ["IUM-5-CORE-01"],
        "timeReviewId": "TR-BMB16-GYM-IK-GM-003",
        "proposedFulfillmentMode": "cross-cutting",
    },
    "BMB16-GYM-PK-RK-003": {
        "sourceId": "SRC-CUR-BMB-2016",
        "sourceBinding": "official",
        "sourceDatasetPath": "curriculum/basiskurs-medienbildung/competencies.json",
        "normativeWeight": "enacted",
        "moduleIds": ["IUM-5-CORE-07"],
        "timeReviewId": "TR-BMB16-GYM-PK-RK-003",
        "proposedFulfillmentMode": "direct-module",
    },
    "LH26-E-DP-003": {
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "sourceBinding": "orientation",
        "sourceDatasetPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "normativeWeight": "orientation",
        "moduleIds": ["IUM-5-CORE-07"],
        "timeReviewId": "TR-LH26-E-DP-003",
        "proposedFulfillmentMode": "direct-module",
    },
    "LH26-E-PROG-003": {
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "sourceBinding": "orientation",
        "sourceDatasetPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "normativeWeight": "orientation",
        "moduleIds": ["IUM-7-CORE-08"],
        "timeReviewId": "TR-LH26-E-PROG-003",
        "proposedFulfillmentMode": "integrated",
    },
    "LH26-E-PROG-004": {
        "sourceId": "SRC-CUR-LESEHILFE-2026-27",
        "sourceBinding": "orientation",
        "sourceDatasetPath": "curriculum/lesehilfe-2026-27/competencies.json",
        "normativeWeight": "orientation",
        "moduleIds": ["IUM-7-CORE-08"],
        "timeReviewId": "TR-LH26-E-PROG-004",
        "proposedFulfillmentMode": "integrated",
    },
}


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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _is_https_url(value: object) -> bool:
    if not _nonempty_string(value):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _unknown_fields(
    data: dict,
    allowed: set[str],
    label: str,
) -> list[str]:
    unknown = sorted(set(data) - allowed)
    if not unknown:
        return []
    return [f"{label} enthält unbekannte Felder: " + ", ".join(unknown)]


def _load_contract_json(
    root: Path,
    relative_path: str,
    label: str,
    errors: list[str],
) -> object | None:
    if not _is_repository_relative(relative_path):
        errors.append(f"{label} muss repository-relativ sein: {relative_path}")
        return None
    path = root / relative_path
    if not path.is_file():
        errors.append(f"{label} fehlt: {relative_path}")
        return None
    try:
        return load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append(f"{label} ist kein gültiges JSON: {relative_path}")
        return None


def validate_curriculum_source_basis(data: object, root: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Curriculumquellenbasis muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(
            data,
            {
                "schemaVersion",
                "projectId",
                "asOf",
                "baseline",
                "sources",
                "totals",
                "crosswalk",
                "coverageAudit",
                "decisionBasis",
                "statementBoundaries",
            },
            "V2-Curriculumquellenbasis",
        )
    )
    if data.get("schemaVersion") != 1:
        errors.append("V2-Curriculumquellenbasis schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Curriculumquellenbasis projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Curriculumquellenbasis asOf muss YYYY-MM-DD sein")

    baseline = data.get("baseline")
    if not isinstance(baseline, dict):
        errors.append("V2-Curriculumbaseline muss ein Objekt sein")
    else:
        errors.extend(
            _unknown_fields(
                baseline,
                {"status", "commit", "immutablePaths"},
                "V2-Curriculumbaseline",
            )
        )
        if baseline.get("status") != "v1-audit-input":
            errors.append("V2-Curriculumbaseline muss v1-audit-input bleiben")
        if baseline.get("commit") != EXPECTED_MAIN_COMMIT:
            errors.append(
                "V2-Curriculumbaseline muss den versiegelten V1-Commit "
                f"{EXPECTED_MAIN_COMMIT} verwenden"
            )
        immutable_paths = baseline.get("immutablePaths")
        expected_paths = {
            expectation["repositoryPath"]
            for expectation in CURRICULUM_SOURCE_EXPECTATIONS.values()
        } | {"curriculum/crosswalk.json", "roadmap/coverage-plan.json"}
        if not isinstance(immutable_paths, list):
            errors.append(
                "V2-Curriculumbaseline muss alle fünf unveränderten V1-Pfade versiegeln"
            )
        elif not all(
            isinstance(path, str) and _is_repository_relative(path)
            for path in immutable_paths
        ):
            errors.append("V2-Curriculumbaseline enthält einen ungültigen Pfad")
        elif set(immutable_paths) != expected_paths:
            errors.append(
                "V2-Curriculumbaseline muss alle fünf unveränderten V1-Pfade versiegeln"
            )

    sources = data.get("sources")
    if not isinstance(sources, list):
        errors.append("V2-Curriculumquellen müssen eine Liste sein")
        sources = []
    source_ids = [
        source.get("sourceId")
        for source in sources
        if isinstance(source, dict) and _nonempty_string(source.get("sourceId"))
    ]
    if len(source_ids) != len(set(source_ids)):
        errors.append("V2-Curriculumquellen enthalten doppelte sourceIds")
    if set(source_ids) != set(CURRICULUM_SOURCE_EXPECTATIONS):
        errors.append("V2-Curriculumquellen müssen exakt die drei geprüften Quellen enthalten")

    all_record_ids: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            errors.append("V2-Curriculumquelle muss ein Objekt sein")
            continue
        source_id = source.get("sourceId")
        if not _nonempty_string(source_id):
            errors.append("V2-Curriculumquelle benötigt eine sourceId")
            continue
        expectation = CURRICULUM_SOURCE_EXPECTATIONS.get(source_id)
        if expectation is None:
            continue
        errors.extend(
            _unknown_fields(
                source,
                {
                    "sourceId",
                    "title",
                    "binding",
                    "normativeStatus",
                    "repositoryPath",
                    "datasetSha256",
                    "sourceAssetSha256",
                    "recordCount",
                    "grades",
                    "checkedAt",
                    "currentReview",
                },
                f"Curriculumquelle {source_id}",
            )
        )
        if source.get("binding") != expectation["binding"]:
            if source_id == "SRC-CUR-LESEHILFE-2026-27":
                errors.append(
                    "SRC-CUR-LESEHILFE-2026-27 muss als orientation gebunden bleiben"
                )
            else:
                errors.append(f"Curriculumquelle {source_id} muss official gebunden sein")
        for field in (
            "title",
            "normativeStatus",
            "repositoryPath",
            "datasetSha256",
            "sourceAssetSha256",
            "grades",
        ):
            if source.get(field) != expectation[field]:
                errors.append(
                    f"Curriculumquelle {source_id} hat einen abweichenden Wert in {field}"
                )
        if source.get("recordCount") != expectation["recordCount"]:
            errors.append(
                f"Curriculumquelle {source_id} erwartet {expectation['recordCount']} "
                f"Records, deklariert {source.get('recordCount')}"
            )
        if not isinstance(source.get("checkedAt"), str) or not DATE_PATTERN.fullmatch(
            source["checkedAt"]
        ):
            errors.append(f"Curriculumquelle {source_id} checkedAt muss YYYY-MM-DD sein")

        current_review = source.get("currentReview")
        if not isinstance(current_review, dict):
            errors.append(f"Curriculumquelle {source_id} benötigt currentReview")
        else:
            errors.extend(
                _unknown_fields(
                    current_review,
                    {
                        "checkedAt",
                        "status",
                        "landingPageUrl",
                        "directUrl",
                        "contentIdentity",
                        "remoteSha256",
                        "remoteByteLength",
                        "finding",
                    },
                    f"currentReview {source_id}",
                )
            )
            if current_review.get("checkedAt") != "2026-09-03":
                errors.append(f"currentReview {source_id} muss am 2026-09-03 geprüft sein")
            if current_review.get("status") not in {
                "transition-status-rechecked",
                "direct-source-rechecked",
            }:
                errors.append(f"currentReview {source_id} hat unbekannten Prüfstatus")
            for field in ("landingPageUrl", "directUrl"):
                if not _is_https_url(current_review.get(field)):
                    errors.append(f"currentReview {source_id} benötigt eine HTTPS-{field}")
            if current_review.get("directUrl") != expectation["directUrl"]:
                errors.append(f"currentReview {source_id} hat eine abweichende Direktfundstelle")
            if current_review.get("contentIdentity") != expectation[
                "contentIdentity"
            ]:
                errors.append(
                    f"currentReview {source_id} hat einen unbelegten Identitätsstatus"
                )
            if source_id == "SRC-CUR-LESEHILFE-2026-27":
                if current_review.get("remoteSha256") != expectation[
                    "sourceAssetSha256"
                ]:
                    errors.append(
                        "currentReview SRC-CUR-LESEHILFE-2026-27 muss den geprüften Remote-Hash ausweisen"
                    )
                if current_review.get("remoteByteLength") != 246597:
                    errors.append(
                        "currentReview SRC-CUR-LESEHILFE-2026-27 muss 246597 Remote-Bytes ausweisen"
                    )
            elif current_review.get("remoteSha256") is not None or current_review.get(
                "remoteByteLength"
            ) is not None:
                errors.append(
                    f"currentReview {source_id} darf ohne neuen Download keine Remote-Bytes behaupten"
                )
            if not _nonempty_string(current_review.get("finding")):
                errors.append(f"currentReview {source_id} benötigt einen Befund")

        relative_path = expectation["repositoryPath"]
        source_data = _load_contract_json(
            root,
            relative_path,
            f"Curriculumdatensatz {source_id}",
            errors,
        )
        if source_data is None:
            continue
        if _sha256(root / relative_path) != expectation["datasetSha256"]:
            errors.append(
                f"Curriculumdatensatz {source_id} weicht vom versiegelten V1-Hash ab"
            )
        if not isinstance(source_data, dict) or source_data.get("sourceId") != source_id:
            errors.append(f"Curriculumdatensatz {source_id} hat eine falsche sourceId")
            continue
        records = source_data.get("records")
        if not isinstance(records, list):
            errors.append(f"Curriculumdatensatz {source_id} benötigt Records")
            continue
        if len(records) != expectation["recordCount"]:
            errors.append(
                f"Curriculumdatensatz {source_id} enthält {len(records)} statt "
                f"{expectation['recordCount']} Records"
            )
        record_ids = [
            record.get("id")
            for record in records
            if isinstance(record, dict) and _nonempty_string(record.get("id"))
        ]
        if len(record_ids) != len(records) or len(record_ids) != len(set(record_ids)):
            errors.append(f"Curriculumdatensatz {source_id} enthält ungültige oder doppelte IDs")
        all_record_ids.extend(record_ids)
        metadata = source_data.get("metadata")
        if not isinstance(metadata, dict) or metadata.get("sha256") != expectation[
            "sourceAssetSha256"
        ]:
            errors.append(f"Curriculumdatensatz {source_id} hat einen abweichenden Quellasset-Hash")

    totals = data.get("totals")
    if isinstance(totals, dict):
        errors.extend(
            _unknown_fields(
                totals,
                {"recordCount", "uniqueRecordCount"},
                "V2-Curriculumgesamtzählung",
            )
        )
    if totals != {"recordCount": 278, "uniqueRecordCount": 278}:
        errors.append("V2-Curriculumquellenbasis muss 278 Records und 278 eindeutige IDs ausweisen")
    if len(all_record_ids) != 278 or len(set(all_record_ids)) != 278:
        errors.append("Die drei versiegelten Curriculumdatensätze müssen 278 eindeutige Records enthalten")

    crosswalk = data.get("crosswalk")
    if not isinstance(crosswalk, dict):
        errors.append("V2-Curriculumquellenbasis benötigt den V1-Crosswalk")
    else:
        errors.extend(
            _unknown_fields(
                crosswalk,
                {
                    "repositoryPath",
                    "datasetSha256",
                    "status",
                    "recordCount",
                    "relationCount",
                    "unmappedRecordCount",
                    "relationshipCounts",
                },
                "V2-Crosswalk",
            )
        )
        crosswalk_path = "curriculum/crosswalk.json"
        expected_hash = "8522C912C7747AF1D39D2822513A3E75EF410CB7BBE9BD98574BF9CF69AC0720"
        if crosswalk.get("repositoryPath") != crosswalk_path:
            errors.append("V2-Crosswalk muss curriculum/crosswalk.json referenzieren")
        if crosswalk.get("datasetSha256") != expected_hash:
            errors.append("V2-Crosswalk muss den versiegelten V1-Hash ausweisen")
        if crosswalk.get("status") != "v1-audit-input":
            errors.append("V2-Crosswalk muss v1-audit-input bleiben")
        actual_crosswalk = _load_contract_json(
            root, crosswalk_path, "V1-Crosswalk", errors
        )
        if actual_crosswalk is not None:
            if _sha256(root / crosswalk_path) != expected_hash:
                errors.append("V1-Crosswalk weicht vom versiegelten Hash ab")
            expected_counts = {
                "curriculumRecords": 278,
                "relations": 56,
                "unmappedRecords": 107,
                "relationshipCounts": {
                    "equivalent": 2,
                    "extends": 15,
                    "new": 3,
                    "not-comparable": 4,
                    "overlaps": 15,
                    "reframes": 17,
                },
            }
            if not isinstance(actual_crosswalk, dict) or actual_crosswalk.get(
                "counts"
            ) != expected_counts:
                errors.append("V1-Crosswalk-Zählungen weichen vom geprüften Stand ab")
            for field, expected_field in (
                ("recordCount", 278),
                ("relationCount", 56),
                ("unmappedRecordCount", 107),
            ):
                if crosswalk.get(field) != expected_field:
                    errors.append(f"V2-Crosswalk hat einen abweichenden Wert in {field}")
            if crosswalk.get("relationshipCounts") != expected_counts[
                "relationshipCounts"
            ]:
                errors.append("V2-Crosswalk hat abweichende Beziehungstyp-Zählungen")

    coverage_audit = data.get("coverageAudit")
    if not isinstance(coverage_audit, dict):
        errors.append("V2-Curriculumquellenbasis benötigt den V1-Coverage-Audit")
    else:
        errors.extend(
            _unknown_fields(
                coverage_audit,
                {
                    "repositoryPath",
                    "datasetSha256",
                    "status",
                    "entryCount",
                    "byBinding",
                },
                "V2-Coverage-Audit",
            )
        )
        coverage_path = "roadmap/coverage-plan.json"
        expected_hash = "4553BE524D7DBC0E02EA3362869A71EE2F4B28164A18AEC7557FDC2001990929"
        expected_by_binding = {
            "official": {"covered": 74, "partial": 2, "total": 76},
            "orientation": {"covered": 92, "partial": 3, "total": 95},
        }
        if coverage_audit.get("repositoryPath") != coverage_path:
            errors.append("V2-Coverage-Audit muss roadmap/coverage-plan.json referenzieren")
        if coverage_audit.get("datasetSha256") != expected_hash:
            errors.append("V2-Coverage-Audit muss den versiegelten V1-Hash ausweisen")
        if coverage_audit.get("status") != "v1-audit-input":
            errors.append("V2-Coverage-Audit muss v1-audit-input bleiben")
        if coverage_audit.get("entryCount") != 171:
            errors.append("V2-Coverage-Audit muss 171 V1-Einträge ausweisen")
        if coverage_audit.get("byBinding") != expected_by_binding:
            errors.append("V2-Coverage-Audit hat abweichende Bindungszählungen")
        coverage_data = _load_contract_json(
            root, coverage_path, "V1-Coverage-Audit", errors
        )
        if coverage_data is not None:
            if _sha256(root / coverage_path) != expected_hash:
                errors.append("V1-Coverage-Audit weicht vom versiegelten Hash ab")
            entries = coverage_data.get("entries") if isinstance(coverage_data, dict) else None
            if not isinstance(entries, list) or len(entries) != 171:
                errors.append("V1-Coverage-Audit muss 171 Einträge enthalten")
            else:
                actual_counts = {
                    "official": {"covered": 0, "partial": 0, "total": 0},
                    "orientation": {"covered": 0, "partial": 0, "total": 0},
                }
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    binding = (
                        "official"
                        if entry.get("normativeWeight") == "enacted"
                        else "orientation"
                    )
                    status = entry.get("coverageStatus")
                    if status in {"covered", "partial"}:
                        actual_counts[binding][status] += 1
                        actual_counts[binding]["total"] += 1
                if actual_counts != expected_by_binding:
                    errors.append("V1-Coverage-Audit-Zählungen weichen vom geprüften Stand ab")

    decision_basis = data.get("decisionBasis")
    if not isinstance(decision_basis, list) or not decision_basis:
        errors.append("V2-Curriculumquellenbasis benötigt eine Entscheidungsbasis")
    else:
        for pointer in decision_basis:
            errors.extend(
                _validate_evidence_pointer(
                    pointer,
                    "curriculum-source-basis",
                    root,
                    [],
                )
            )
    boundaries = data.get("statementBoundaries")
    if not isinstance(boundaries, list) or len(boundaries) < 2 or not all(
        _nonempty_string(boundary) for boundary in boundaries
    ):
        errors.append("V2-Curriculumquellenbasis benötigt Aussagegrenzen")
    return errors


def _curriculum_record_index(root: Path, errors: list[str]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for expectation in CURRICULUM_SOURCE_EXPECTATIONS.values():
        path = expectation["repositoryPath"]
        data = _load_contract_json(root, path, "Curriculumdatensatz", errors)
        if not isinstance(data, dict):
            continue
        records = data.get("records")
        if not isinstance(records, list):
            continue
        for record in records:
            if isinstance(record, dict) and _nonempty_string(record.get("id")):
                index[record["id"]] = record
    return index


def validate_curriculum_gap_assessments(data: object, root: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["V2-Curriculumlückenregister muss ein Objekt sein"]

    errors: list[str] = []
    errors.extend(
        _unknown_fields(
            data,
            {
                "schemaVersion",
                "projectId",
                "asOf",
                "baselineCoveragePath",
                "coverageBoundary",
                "assessments",
            },
            "V2-Curriculumlückenregister",
        )
    )
    if data.get("schemaVersion") != 1:
        errors.append("V2-Curriculumlückenregister schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append("V2-Curriculumlückenregister projectId muss ium-lernwerk sein")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append("V2-Curriculumlückenregister asOf muss YYYY-MM-DD sein")
    if data.get("baselineCoveragePath") != "roadmap/coverage-plan.json":
        errors.append("V2-Curriculumlückenregister muss den V1-Coverage-Audit referenzieren")
    if not _nonempty_string(data.get("coverageBoundary")):
        errors.append("V2-Curriculumlückenregister benötigt eine Abdeckungsgrenze")

    assessments = data.get("assessments")
    if not isinstance(assessments, list):
        errors.append("V2-Curriculumlücken assessments müssen eine Liste sein")
        assessments = []
    ids = [
        assessment.get("competencyId")
        for assessment in assessments
        if isinstance(assessment, dict)
        and _nonempty_string(assessment.get("competencyId"))
    ]
    if len(ids) != len(set(ids)):
        errors.append("V2-Curriculumlücken enthalten doppelte competencyIds")
    if set(ids) != set(EXPECTED_CURRICULUM_GAPS):
        errors.append(
            "V2-Curriculumlücken müssen exakt die fünf aktuellen V1-partial-Records enthalten"
        )

    coverage_data = _load_contract_json(
        root,
        "roadmap/coverage-plan.json",
        "V1-Coverage-Audit",
        errors,
    )
    coverage_entries: dict[str, dict] = {}
    if isinstance(coverage_data, dict) and isinstance(coverage_data.get("entries"), list):
        coverage_entries = {
            entry["competencyId"]: entry
            for entry in coverage_data["entries"]
            if isinstance(entry, dict) and _nonempty_string(entry.get("competencyId"))
        }
        actual_partial = {
            entry_id
            for entry_id, entry in coverage_entries.items()
            if entry.get("coverageStatus") == "partial"
        }
        if actual_partial != set(EXPECTED_CURRICULUM_GAPS):
            errors.append("Der aktuelle V1-Coverage-Audit enthält nicht die erwarteten fünf Restlücken")

    record_index = _curriculum_record_index(root, errors)
    allowed_assessment_fields = {
        "competencyId",
        "sourceId",
        "sourceBinding",
        "sourceDatasetPath",
        "requirementText",
        "v1Audit",
        "v2Coverage",
        "time",
        "followUp",
        "risk",
        "auditEvidence",
        "v2Evidence",
    }
    for assessment in assessments:
        if not isinstance(assessment, dict):
            errors.append("V2-Curriculumlücke muss ein Objekt sein")
            continue
        competency_id = assessment.get("competencyId")
        if not _nonempty_string(competency_id):
            errors.append("V2-Curriculumlücke benötigt eine competencyId")
            continue
        errors.extend(
            _unknown_fields(
                assessment,
                allowed_assessment_fields,
                f"V2-Curriculumlücke {competency_id}",
            )
        )
        expected = EXPECTED_CURRICULUM_GAPS.get(competency_id)
        if expected is None:
            continue
        for field in ("sourceId", "sourceBinding", "sourceDatasetPath"):
            if assessment.get(field) != expected[field]:
                errors.append(f"V2-Curriculumlücke {competency_id} hat falsches {field}")
        record = record_index.get(competency_id)
        if record is None:
            errors.append(f"Curriculumrecord {competency_id} fehlt im versiegelten Datensatz")
        elif assessment.get("requirementText") != record.get("sourceText"):
            errors.append(f"V2-Curriculumlücke {competency_id} verändert den Quellwortlaut")

        v1_audit = assessment.get("v1Audit")
        if not isinstance(v1_audit, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt v1Audit")
        else:
            errors.extend(
                _unknown_fields(
                    v1_audit,
                    {"status", "normativeWeight", "moduleIds", "timeReviewId"},
                    f"V1-Audit {competency_id}",
                )
            )
            if v1_audit.get("status") != "partial":
                errors.append(f"V1-Auditstatus {competency_id} muss partial bleiben")
            for field in ("normativeWeight", "moduleIds", "timeReviewId"):
                if v1_audit.get(field) != expected[field]:
                    errors.append(f"V1-Audit {competency_id} hat falsches {field}")
            current_entry = coverage_entries.get(competency_id)
            if current_entry is not None:
                if current_entry.get("coverageStatus") != "partial":
                    errors.append(f"V1-Coverage {competency_id} ist nicht mehr partial")
                for current_field, expected_field in (
                    ("normativeWeight", "normativeWeight"),
                    ("moduleIds", "moduleIds"),
                    ("timeReviewId", "timeReviewId"),
                ):
                    if v1_audit.get(expected_field) != current_entry.get(current_field):
                        errors.append(
                            f"V1-Audit {competency_id} weicht im Feld {expected_field} vom Coverage-Plan ab"
                        )

        v2_coverage = assessment.get("v2Coverage")
        if not isinstance(v2_coverage, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt v2Coverage")
        else:
            errors.extend(
                _unknown_fields(
                    v2_coverage,
                    {"status", "proposedFulfillmentMode", "decisionState", "rationale"},
                    f"V2-Abdeckung {competency_id}",
                )
            )
            coverage_status = v2_coverage.get("status")
            if coverage_status == "covered":
                errors.append(
                    f"V2-Curriculumlücke {competency_id} darf ohne neue V2-Evidenz nicht covered sein"
                )
            elif coverage_status != "unassessed":
                errors.append(
                    f"V2-Curriculumlücke {competency_id} muss bis zum V2-Design unassessed bleiben"
                )
            if v2_coverage.get("proposedFulfillmentMode") != expected[
                "proposedFulfillmentMode"
            ]:
                if competency_id == "BMB16-GYM-IK-GM-003":
                    errors.append(
                        "BMB16-GYM-IK-GM-003 muss als cross-cutting geführt werden"
                    )
                else:
                    errors.append(
                        f"V2-Curriculumlücke {competency_id} hat einen falschen vorgesehenen Erfüllungsmodus"
                    )
            if v2_coverage.get("decisionState") not in {"approved-direction", "open"}:
                errors.append(f"V2-Curriculumlücke {competency_id} hat ungültigen decisionState")
            if not _nonempty_string(v2_coverage.get("rationale")):
                errors.append(f"V2-Curriculumlücke {competency_id} benötigt eine V2-Begründung")

        time = assessment.get("time")
        if not isinstance(time, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt einen Zeitstatus")
        else:
            errors.extend(
                _unknown_fields(
                    time,
                    {"status", "additionalMinutes", "rationale"},
                    f"V2-Zeitstatus {competency_id}",
                )
            )
            if competency_id == "BMB16-GYM-IK-GM-003":
                if time.get("status") != "no-additional-time" or time.get(
                    "additionalMinutes"
                ) != 0:
                    errors.append(
                        "BMB16-GYM-IK-GM-003 darf keine zusätzlichen Minuten erzeugen"
                    )
            elif time.get("additionalMinutes") is not None:
                errors.append(
                    f"V2-Curriculumlücke {competency_id} darf vor der Roadmap keine Minuten festlegen"
                )

        follow_up = assessment.get("followUp")
        if not isinstance(follow_up, dict):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt followUp")
        else:
            errors.extend(
                _unknown_fields(
                    follow_up,
                    {"kind", "newLearningTask", "owner", "nextReview", "acceptanceCriterion"},
                    f"V2-Folgeprüfung {competency_id}",
                )
            )
            for field in ("kind", "newLearningTask", "owner", "nextReview", "acceptanceCriterion"):
                if field not in follow_up or (
                    field not in {"newLearningTask"}
                    and not _nonempty_string(follow_up.get(field))
                ):
                    errors.append(f"V2-Curriculumlücke {competency_id} benötigt followUp.{field}")
            if competency_id == "BMB16-GYM-IK-GM-003" and follow_up.get(
                "newLearningTask"
            ) != "not-required":
                errors.append(
                    "BMB16-GYM-IK-GM-003 darf keine künstliche Zusatzaufgabe erzeugen"
                )
        if not _nonempty_string(assessment.get("risk")):
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt ein Risiko")

        audit_evidence = assessment.get("auditEvidence")
        if not isinstance(audit_evidence, list) or not audit_evidence:
            errors.append(f"V2-Curriculumlücke {competency_id} benötigt Audit-Evidenz")
        else:
            for pointer in audit_evidence:
                errors.extend(
                    _validate_evidence_pointer(pointer, competency_id, root, [])
                )
        v2_evidence = assessment.get("v2Evidence")
        if not isinstance(v2_evidence, list):
            errors.append(f"V2-Curriculumlücke {competency_id} v2Evidence muss eine Liste sein")
        elif v2_evidence:
            errors.append(
                f"V2-Curriculumlücke {competency_id} darf in diesem Fundament noch keine V2-Evidenz beanspruchen"
            )
    return errors


def validate_foundation_status(
    data: object,
    expected_id: str,
    requirement_ids: set[str],
    root: Path,
    warnings: list[str] | None = None,
) -> list[str]:
    if not isinstance(data, dict):
        return [f"V2-Fundamentstatus {expected_id} muss ein Objekt sein"]

    errors: list[str] = []
    report_warnings = warnings if warnings is not None else []
    errors.extend(
        _unknown_fields(
            data,
            {
                "schemaVersion",
                "projectId",
                "id",
                "asOf",
                "workStatus",
                "maturity",
                "requirementIds",
                "evidence",
                "openQuestions",
                "nextGate",
            },
            f"V2-Fundamentstatus {expected_id}",
        )
    )
    if data.get("schemaVersion") != 1:
        errors.append(f"V2-Fundamentstatus {expected_id} schemaVersion muss 1 sein")
    if data.get("projectId") != "ium-lernwerk":
        errors.append(f"V2-Fundamentstatus {expected_id} projectId muss ium-lernwerk sein")
    if data.get("id") != expected_id:
        errors.append(f"V2-Fundamentstatus muss die ID {expected_id} tragen")
    if not isinstance(data.get("asOf"), str) or not DATE_PATTERN.fullmatch(
        data["asOf"]
    ):
        errors.append(f"V2-Fundamentstatus {expected_id} asOf muss YYYY-MM-DD sein")
    if data.get("workStatus") not in {"planned", "in_progress", "blocked", "review", "done"}:
        errors.append(f"V2-Fundamentstatus {expected_id} hat unbekannten workStatus")

    maturity = data.get("maturity")
    maturity_fields = {
        "curriculumCoverage": {"unassessed", "uncovered", "partial", "covered", "not-applicable"},
        "foundationConcept": {"missing", "draft", "reviewed", "standard"},
        "dataVerification": {"not-run", "passed", "failed", "stale"},
        "contentImplementation": {"not-started", "working", "implemented"},
        "technicalVerification": {"not-run", "passed", "failed", "stale"},
        "subjectReview": {"not-started", "in-review", "passed", "changes-required"},
        "usageReview": {"not-started", "planned", "running", "passed", "failed", "not-applicable"},
        "classroomPilot": {"not-started", "planned", "running", "completed", "not-applicable"},
        "release": {"closed", "conditional", "released", "not-applicable"},
    }
    if not isinstance(maturity, dict):
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt getrennte Reifeachsen")
    else:
        errors.extend(
            _unknown_fields(maturity, set(maturity_fields), f"Reifeachsen {expected_id}")
        )
        for field, allowed in maturity_fields.items():
            if maturity.get(field) not in allowed:
                errors.append(f"Reifeachse {field} ist ungültig in {expected_id}")

    status_requirement_ids = data.get("requirementIds")
    valid_status_requirement_ids: list[str] = []
    if not isinstance(status_requirement_ids, list) or not status_requirement_ids:
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt requirementIds")
        status_requirement_ids = []
    else:
        valid_status_requirement_ids = [
            requirement_id
            for requirement_id in status_requirement_ids
            if _nonempty_string(requirement_id)
        ]
        if len(valid_status_requirement_ids) != len(status_requirement_ids):
            errors.append(
                f"V2-Fundamentstatus {expected_id} enthält eine ungültige requirementId"
            )
        if len(valid_status_requirement_ids) != len(set(valid_status_requirement_ids)):
            errors.append(f"V2-Fundamentstatus {expected_id} enthält doppelte requirementIds")
    for requirement_id in valid_status_requirement_ids:
        if requirement_id not in requirement_ids:
            errors.append(f"V2-Fundamentstatus {expected_id} referenziert unbekannte Anforderung {requirement_id}")

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt Evidenz")
    else:
        for pointer in evidence:
            errors.extend(
                _validate_evidence_pointer(
                    pointer,
                    f"foundation-{expected_id}",
                    root,
                    report_warnings,
                )
            )

    open_questions = data.get("openQuestions")
    if not isinstance(open_questions, list):
        errors.append(f"V2-Fundamentstatus {expected_id} openQuestions muss eine Liste sein")
    else:
        seen_question_ids: set[str] = set()
        for question in open_questions:
            if not isinstance(question, dict):
                errors.append(f"Offene Frage in {expected_id} muss ein Objekt sein")
                continue
            errors.extend(
                _unknown_fields(
                    question,
                    {"id", "question", "owner", "risk", "disposition"},
                    f"Offene Frage in {expected_id}",
                )
            )
            question_id = question.get("id")
            if not _nonempty_string(question_id):
                errors.append(f"Offene Frage in {expected_id} benötigt eine ID")
            elif question_id in seen_question_ids:
                errors.append(f"Doppelte offene Frage {question_id} in {expected_id}")
            else:
                seen_question_ids.add(question_id)
            for field in ("question", "owner", "risk"):
                if not _nonempty_string(question.get(field)):
                    errors.append(f"Offene Frage {question_id} benötigt {field}")
            if question.get("disposition") not in {"open", "accepted", "resolved"}:
                errors.append(f"Offene Frage {question_id} hat ungültige disposition")
    if not _nonempty_string(data.get("nextGate")):
        errors.append(f"V2-Fundamentstatus {expected_id} benötigt nextGate")

    if expected_id == "curriculum":
        if data.get("workStatus") != "review":
            errors.append("Curriculumfundament muss bis zur Nutzerprüfung im Status review bleiben")
        if set(valid_status_requirement_ids) != {"V2-REQ-CUR-001", "V2-REQ-CUR-002"}:
            errors.append("Curriculumfundament muss beide CUR-Anforderungen referenzieren")
        if isinstance(maturity, dict):
            if maturity.get("curriculumCoverage") != "unassessed":
                errors.append("Curriculumfundament darf noch keine V2-Gesamtabdeckung behaupten")
            if maturity.get("dataVerification") != "passed":
                errors.append("Curriculumfundament muss die versiegelte Datenbasis verifizieren")
            if maturity.get("contentImplementation") != "not-started":
                errors.append(
                    "Curriculumfundament darf bei eingefrorener Inhaltsproduktion keine Implementierung beanspruchen"
                )
            if maturity.get("subjectReview") != "in-review":
                errors.append("Curriculumfundament muss bis zur Nutzerprüfung in-review bleiben")
            if maturity.get("release") != "closed":
                errors.append("Curriculumfundament darf keine Releasefreigabe beanspruchen")
        if data.get("nextGate") != "IUM-V2-CUR-REVIEW":
            errors.append("Curriculumfundament muss IUM-V2-CUR-REVIEW als nächstes Gate führen")
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
    requirement_ids: set[str] = set()
    if path.is_file():
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{requirements_path.as_posix()} ist kein gültiges JSON")
        else:
            errors.extend(validate_requirements(data, root, warnings))
            if isinstance(data, dict) and isinstance(data.get("requirements"), list):
                requirement_ids = {
                    requirement["id"]
                    for requirement in data["requirements"]
                    if isinstance(requirement, dict)
                    and _nonempty_string(requirement.get("id"))
                }

    curriculum_contracts = (
        (
            Path("roadmap/v2/foundations/curriculum/source-basis.json"),
            lambda payload: validate_curriculum_source_basis(payload, root),
        ),
        (
            Path("roadmap/v2/foundations/curriculum/gap-assessments.json"),
            lambda payload: validate_curriculum_gap_assessments(payload, root),
        ),
        (
            Path("roadmap/v2/foundations/curriculum/status.json"),
            lambda payload: validate_foundation_status(
                payload,
                "curriculum",
                requirement_ids,
                root,
                warnings,
            ),
        ),
    )
    for relative_path, validator in curriculum_contracts:
        path = root / relative_path
        if not path.is_file():
            continue
        try:
            data = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{relative_path.as_posix()} ist kein gültiges JSON")
            continue
        errors.extend(validator(data))
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
