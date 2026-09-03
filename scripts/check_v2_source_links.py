from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


INVENTORY_PATH = Path("roadmap/v2/foundations/sources/inventory.json")
OUTPUT_PATH = Path("roadmap/v2/foundations/sources/link-audit.json")
SOURCE_REGISTER_PATH = Path("docs/research/phase-0/source-register.json")
CLAIM_LEDGER_PATH = Path("docs/research/phase-0/claim-ledger.json")
USER_AGENT = "IuM-Lernwerk-Source-Audit/1.0 (+https://github.com/H4R7W16/ium-lernwerk)"
MAX_REDIRECTS = 8
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def _request(url: str, method: str, timeout: float) -> tuple[int, str | None]:
    opener = build_opener(NoRedirectHandler())
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request = Request(url, headers=headers, method=method)
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, response.headers.get("Location")
    except HTTPError as error:
        return error.code, error.headers.get("Location")


def normalize_final_url(url: str) -> str:
    """Remove fragments and known non-deterministic Springer error parameters."""
    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True)
    if parts.hostname == "link.springer.com" and any(
        key == "error" and value == "cookies_not_supported" for key, value in query
    ):
        query = [
            (key, value)
            for key, value in query
            if key not in {"error", "code"}
        ]
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query, doseq=True), "")
    )


def _check_url_once(url: str, timeout: float) -> dict[str, object | None]:
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        return {"status": "unresolved", "httpStatus": None, "finalUrl": None}
    current_url = url
    seen_urls: set[str] = set()
    for _redirect_count in range(MAX_REDIRECTS + 1):
        if current_url in seen_urls:
            return {
                "status": "unresolved",
                "httpStatus": None,
                "finalUrl": current_url,
            }
        seen_urls.add(current_url)
        try:
            status_code, location = _request(current_url, "HEAD", timeout)
            if status_code == 405:
                status_code, location = _request(current_url, "GET", timeout)
        except (OSError, URLError, TimeoutError):
            return {
                "status": "unresolved",
                "httpStatus": None,
                "finalUrl": current_url,
            }

        if 200 <= status_code < 300:
            return {
                "status": "resolved",
                "httpStatus": status_code,
                "finalUrl": current_url,
            }
        if 300 <= status_code < 400:
            if not location:
                return {
                    "status": "unresolved",
                    "httpStatus": status_code,
                    "finalUrl": current_url,
                }
            next_url = urljoin(current_url, location)
            if not next_url.startswith(("https://", "http://")):
                return {
                    "status": "unresolved",
                    "httpStatus": status_code,
                    "finalUrl": current_url,
                }
            current_url = next_url
            continue
        if status_code in {401, 403}:
            return {
                "status": "restricted",
                "httpStatus": status_code,
                "finalUrl": current_url,
            }
        if status_code in {404, 410}:
            return {
                "status": "missing",
                "httpStatus": status_code,
                "finalUrl": current_url,
            }
        return {
            "status": "unresolved",
            "httpStatus": status_code,
            "finalUrl": current_url,
        }
    return {
        "status": "unresolved",
        "httpStatus": None,
        "finalUrl": current_url,
    }


def check_url(url: str, timeout: float = 12) -> dict[str, object | None]:
    result: dict[str, object | None] = {
        "status": "unresolved",
        "httpStatus": None,
        "finalUrl": None,
    }
    for _attempt in range(2):
        result = _check_url_once(url, timeout)
        if result["status"] != "unresolved":
            break
    final_url = result.get("finalUrl")
    if isinstance(final_url, str):
        result["finalUrl"] = normalize_final_url(final_url)
    return result


def build_targets(root: Path) -> list[dict[str, object]]:
    inventory = json.loads((root / INVENTORY_PATH).read_text(encoding="utf-8"))
    source_register = json.loads(
        (root / SOURCE_REGISTER_PATH).read_text(encoding="utf-8")
    )
    claim_ledger = json.loads((root / CLAIM_LEDGER_PATH).read_text(encoding="utf-8"))

    reviewed_source_ids = {
        source_id
        for claim in claim_ledger["claims"]
        if claim.get("status") == "reviewed"
        for source_id in claim.get("sourceIds", [])
    }
    overrides = {
        override["sourceId"]: override["url"]
        for override in inventory["locatorOverrides"]
    }
    targets: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for source in source_register["sources"]:
        source_id = source["id"]
        if source_id in seen_ids:
            raise ValueError(f"doppelte Quellen-ID {source_id}")
        seen_ids.add(source_id)
        if source.get("doi"):
            locator_type = "doi"
            locator = f"https://doi.org/{source['doi']}"
        elif source.get("url"):
            locator_type = "url"
            locator = source["url"]
        elif source_id in overrides:
            locator_type = "v2-override"
            locator = overrides[source_id]
        else:
            locator_type = "missing"
            locator = ""
        targets.append(
            {
                "sourceId": source_id,
                "required": (
                    source_id in reviewed_source_ids or source_id.startswith("SRC-CUR-")
                ),
                "locatorType": locator_type,
                "url": locator,
            }
        )

    for source in inventory["lxp01Additions"]:
        source_id = source["sourceId"]
        if source_id in seen_ids:
            raise ValueError(f"doppelte Quellen-ID {source_id}")
        seen_ids.add(source_id)
        targets.append(
            {
                "sourceId": source_id,
                "required": True,
                "locatorType": "doi" if source.get("doi") else "url",
                "url": source["url"],
            }
        )
    return sorted(targets, key=lambda target: str(target["sourceId"]))


def _snapshot_payload(
    targets: list[dict[str, object]],
    checked_at: str,
    timeout: float,
    probe: Callable[[str, float], dict[str, object | None]],
) -> tuple[dict[str, object], list[str], list[str]]:
    checks: list[dict[str, object]] = []
    errors: list[str] = []
    warnings: list[str] = []
    worker_count = max(1, min(8, len(targets)))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        results = list(
            executor.map(
                lambda target: probe(str(target["url"]), timeout),
                targets,
            )
        )
    for target, result in zip(targets, results, strict=True):
        check = {
            "sourceId": target["sourceId"],
            "required": target["required"],
            "locatorType": target["locatorType"],
            "url": target["url"],
            "status": result["status"],
            "httpStatus": result["httpStatus"],
            "finalUrl": result["finalUrl"],
            "checkedAt": checked_at,
        }
        checks.append(check)
        if result["status"] not in {"resolved", "restricted"}:
            message = (
                f"{'Pflichtquelle' if target['required'] else 'Optionale Quelle'} "
                f"{target['sourceId']} ist nicht auflösbar ({result['status']})"
            )
            if target["required"]:
                errors.append(message)
            else:
                warnings.append(message)

    summary = {
        "total": len(checks),
        "required": sum(1 for check in checks if check["required"]),
        "optional": sum(1 for check in checks if not check["required"]),
        "resolved": sum(1 for check in checks if check["status"] == "resolved"),
        "restricted": sum(1 for check in checks if check["status"] == "restricted"),
        "missing": sum(1 for check in checks if check["status"] == "missing"),
        "unresolved": sum(1 for check in checks if check["status"] == "unresolved"),
        "warnings": len(warnings),
    }
    payload: dict[str, object] = {
        "schemaVersion": 1,
        "projectId": "ium-lernwerk",
        "generatedAt": checked_at,
        "inventoryPath": INVENTORY_PATH.as_posix(),
        "policy": {
            "requiredFailure": "block-and-preserve-last-snapshot",
            "optionalFailure": "warn-and-write",
            "acceptedStatuses": ["resolved", "restricted"],
        },
        "summary": summary,
        "checks": checks,
    }
    return payload, errors, warnings


def _is_iso_date(value: object) -> bool:
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_http_url(value: object) -> bool:
    return isinstance(value, str) and value.startswith(("https://", "http://"))


def validate_generated_payload(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["Generierter Linkaudit muss ein Objekt sein"]
    errors: list[str] = []
    if not _is_iso_date(payload.get("generatedAt")):
        errors.append("Linkaudit-Stichtag muss YYYY-MM-DD sein")
    checks = payload.get("checks")
    if not isinstance(checks, list):
        return errors + ["Generierter Linkaudit benötigt checks"]
    for check in checks:
        if not isinstance(check, dict):
            errors.append("Generierte Linkprüfung muss ein Objekt sein")
            continue
        source_id = check.get("sourceId")
        label = source_id if isinstance(source_id, str) and source_id else "<unbekannt>"
        required_fields = {
            "sourceId",
            "required",
            "locatorType",
            "url",
            "status",
            "httpStatus",
            "finalUrl",
            "checkedAt",
        }
        for field in sorted(required_fields - set(check)):
            errors.append(f"Linkprüfung {label} benötigt Pflichtfeld {field}")
        if not isinstance(source_id, str) or not source_id:
            errors.append("Linkprüfung benötigt sourceId")
        if not isinstance(check.get("required"), bool):
            errors.append(f"Linkprüfung {label} required muss boolesch sein")
        if not _is_http_url(check.get("url")):
            errors.append(f"Linkprüfung {label} benötigt HTTP(S)-Locator")
        status = check.get("status")
        http_status = check.get("httpStatus")
        final_url = check.get("finalUrl")
        if not isinstance(status, str) or status not in {
            "resolved",
            "restricted",
            "missing",
            "unresolved",
        }:
            errors.append(f"Linkprüfung {label} hat unbekannten Status")
        if isinstance(status, str) and status in {"resolved", "restricted"} and (
            not _is_plain_int(http_status)
            or not 100 <= http_status <= 599
            or not _is_http_url(final_url)
        ):
            errors.append(
                f"Linkprüfung {label} benötigt terminale HTTP-Evidenz für {status}"
            )
        if status == "resolved" and (
            not _is_plain_int(http_status) or not 200 <= http_status <= 299
        ):
            errors.append(f"Linkprüfung {label} resolved benötigt terminalen 2xx-Status")
        if status == "restricted" and (
            not _is_plain_int(http_status) or http_status not in {401, 403}
        ):
            errors.append(f"Linkprüfung {label} restricted benötigt HTTP 401 oder 403")
        if status == "missing" and (
            not _is_plain_int(http_status) or http_status not in {404, 410}
        ):
            errors.append(f"Linkprüfung {label} missing benötigt HTTP 404 oder 410")
        if check.get("checkedAt") != payload.get("generatedAt"):
            errors.append(f"Linkprüfung {label} hat einen abweichenden Stichtag")

    summary = payload.get("summary")
    expected_summary = {
        "total": len(checks),
        "required": sum(1 for check in checks if isinstance(check, dict) and check.get("required") is True),
        "optional": sum(1 for check in checks if isinstance(check, dict) and check.get("required") is False),
        "resolved": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "resolved"),
        "restricted": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "restricted"),
        "missing": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "missing"),
        "unresolved": sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "unresolved"),
        "warnings": sum(
            1
            for check in checks
            if isinstance(check, dict)
            and check.get("required") is False
            and (
                not isinstance(check.get("status"), str)
                or check.get("status") not in {"resolved", "restricted"}
            )
        ),
    }
    if summary != expected_summary:
        errors.append("Generierte Linkaudit-Summary stimmt nicht mit checks überein")
    return errors


def update_snapshot(
    targets: list[dict[str, object]],
    output_path: Path,
    *,
    checked_at: str,
    timeout: float = 12,
    probe: Callable[[str, float], dict[str, object | None]] = check_url,
    contract_root: Path | None = None,
) -> tuple[list[str], list[str]]:
    if not _is_iso_date(checked_at):
        return ["Linkaudit-Stichtag muss YYYY-MM-DD sein"], []
    payload, errors, warnings = _snapshot_payload(
        targets,
        checked_at,
        timeout,
        probe,
    )
    if errors:
        return errors, warnings
    errors.extend(validate_generated_payload(payload))
    if contract_root is not None:
        try:
            from scripts.validate_v2_rebaseline import validate_source_link_audit
        except ModuleNotFoundError:
            from validate_v2_rebaseline import validate_source_link_audit

        contract_warnings: list[str] = []
        errors.extend(
            validate_source_link_audit(payload, contract_root, contract_warnings)
        )
        for warning in contract_warnings:
            if warning not in warnings:
                warnings.append(warning)
    if errors:
        return errors, warnings

    output_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, output_path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prüft V2-Quellenfundstellen und aktualisiert den Audit atomar."
    )
    parser.add_argument("--checked-at", default=date.today().isoformat())
    parser.add_argument("--timeout", type=float, default=12)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Bestätigt explizit die atomare Aktualisierung des Audit-Snapshots.",
    )
    args = parser.parse_args(argv)
    if not args.write:
        print("FEHLER: Der Linkaudit schreibt nur mit ausdrücklichem --write.")
        return 2
    root = Path(__file__).resolve().parents[1]
    try:
        targets = build_targets(root)
        errors, warnings = update_snapshot(
            targets,
            root / OUTPUT_PATH,
            checked_at=args.checked_at,
            timeout=args.timeout,
            contract_root=root,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"FEHLER: Quellenprüfung konnte nicht vorbereitet werden: {error}")
        return 1
    for warning in warnings:
        print(f"WARNUNG: {warning}")
    for error in errors:
        print(f"FEHLER: {error}")
    if errors:
        print("Quellen-Linkaudit fehlgeschlagen; vorhandener Snapshot blieb unverändert.")
        return 1
    print(f"Quellen-Linkaudit erfolgreich: {len(targets)} Fundstellen geprüft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
