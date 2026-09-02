from __future__ import annotations

import json
from pathlib import Path


CONTROL_FILES = (
    Path("roadmap/v2/status.json"),
    Path("roadmap/v2/archive/v1-baseline.json"),
    Path("roadmap/v2/requirements/requirements.json"),
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_repository(root: Path) -> list[str]:
    return [
        f"{path.as_posix()} fehlt"
        for path in CONTROL_FILES
        if not (root / path).is_file()
    ]


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
