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


def validate_repository(root: Path) -> list[str]:
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
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("V2 re-baseline validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
