#!/usr/bin/env python3
"""Fail-closed validation for the IUM-5-CORE-05 Gate-B package."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import ipaddress
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATE_B_ROOT = ROOT / "pilot/ium5-gate-b"
SCHEMA_ROOT = GATE_B_ROOT / "schemas"
PROTOCOL_PATH = GATE_B_ROOT / "protocol.json"

SCHEMA_BY_DOCUMENT_TYPE = {
    "ium5-gate-b-technical-evidence": "technical-evidence.schema.json",
    "ium5-gate-b-pilot-evidence": "pilot-evidence.schema.json",
    "ium5-gate-b-decision-package": "decision-package.schema.json",
}

EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])")
IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IPV6_TOKEN_RE = re.compile(r"(?<![0-9A-Fa-f:])[0-9A-Fa-f:]{2,}(?![0-9A-Fa-f:])")
SECRET_40_RE = re.compile(r"^[A-Za-z0-9]{40}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class Issue:
    code: str
    pointer: str
    message: str


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_protocol() -> dict[str, object]:
    protocol = _load_json(PROTOCOL_PATH)
    if not isinstance(protocol, dict):
        raise ValueError("protocol root must be an object")
    return protocol


def _pointer(parent: str, token: object) -> str:
    escaped = str(token).replace("~", "~0").replace("/", "~1")
    return f"{parent}/{escaped}"


def _matches_type(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _resolve_fragment(document: object, fragment: str) -> object:
    if not fragment:
        return document
    if not fragment.startswith("/"):
        raise ValueError("only JSON Pointer fragments are supported")
    current = document
    for raw_token in fragment[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or token not in current:
            raise ValueError(f"unresolved JSON Pointer token: {token}")
        current = current[token]
    return current


def _resolve_ref(reference: str, current_schema_name: str) -> tuple[object, str]:
    if reference.startswith(("http://", "https://")):
        raise ValueError("remote references are forbidden")
    file_part, separator, fragment = reference.partition("#")
    target_name = file_part or current_schema_name
    target_path = (SCHEMA_ROOT / target_name).resolve()
    schema_root = SCHEMA_ROOT.resolve()
    if target_path.parent != schema_root or not target_path.is_file():
        raise ValueError("schema reference escapes or misses the schema directory")
    target_document = _load_json(target_path)
    target = _resolve_fragment(target_document, fragment if separator else "")
    return target, target_name


def _schema_issue(code: str, pointer: str, message: str) -> list[Issue]:
    return [Issue(code, pointer, message)]


def _validate_schema(
    value: object,
    schema: object,
    schema_name: str,
    pointer: str = "$",
) -> list[Issue]:
    if not isinstance(schema, dict):
        return _schema_issue("SCHEMA_DEFINITION_INVALID", pointer, "schema node is not an object")

    reference = schema.get("$ref")
    if reference is not None:
        if not isinstance(reference, str):
            return _schema_issue("SCHEMA_REFERENCE_INVALID", pointer, "$ref must be a string")
        try:
            target, target_name = _resolve_ref(reference, schema_name)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            code = "SCHEMA_REMOTE_REF" if reference.startswith(("http://", "https://")) else "SCHEMA_REFERENCE_INVALID"
            return _schema_issue(code, pointer, str(error))
        return _validate_schema(value, target, target_name, pointer)

    one_of = schema.get("oneOf")
    if one_of is not None:
        if not isinstance(one_of, list):
            return _schema_issue("SCHEMA_ONE_OF", pointer, "oneOf must be an array")
        matches = [
            branch
            for branch in one_of
            if not _validate_schema(value, branch, schema_name, pointer)
        ]
        if len(matches) != 1:
            return _schema_issue("SCHEMA_ONE_OF", pointer, "value must match exactly one branch")
        return []

    issues: list[Issue] = []
    expected_type = schema.get("type")
    if expected_type is not None:
        if not isinstance(expected_type, str) or not _matches_type(value, expected_type):
            return _schema_issue("SCHEMA_TYPE", pointer, f"expected {expected_type}")

    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        issues.append(Issue("SCHEMA_CONST", pointer, "value differs from the required constant"))
    if "enum" in schema and value not in schema["enum"]:
        issues.append(Issue("SCHEMA_ENUM", pointer, "value is outside the allowed enumeration"))

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                issues.append(Issue("SCHEMA_REQUIRED", _pointer(pointer, key), "required property is missing"))
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    issues.append(Issue("SCHEMA_ADDITIONAL_PROPERTY", _pointer(pointer, key), "unknown property"))
        for key, child in value.items():
            if key in properties:
                issues.extend(_validate_schema(child, properties[key], schema_name, _pointer(pointer, key)))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            issues.append(Issue("SCHEMA_MIN_ITEMS", pointer, "array contains too few items"))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            issues.append(Issue("SCHEMA_MAX_ITEMS", pointer, "array contains too many items"))
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                issues.append(Issue("SCHEMA_UNIQUE_ITEMS", pointer, "array items must be unique"))
        if "items" in schema:
            for index, item in enumerate(value):
                issues.extend(_validate_schema(item, schema["items"], schema_name, _pointer(pointer, index)))

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            issues.append(Issue("SCHEMA_MIN_LENGTH", pointer, "string is too short"))
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            issues.append(Issue("SCHEMA_MAX_LENGTH", pointer, "string is too long"))
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            issues.append(Issue("SCHEMA_PATTERN", pointer, "string does not match the required pattern"))

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            issues.append(Issue("SCHEMA_MINIMUM", pointer, "integer is below the minimum"))
        if "maximum" in schema and value > schema["maximum"]:
            issues.append(Issue("SCHEMA_MAXIMUM", pointer, "integer is above the maximum"))
    return issues


def _contains_ip_address(value: str) -> bool:
    for match in IPV4_RE.finditer(value):
        try:
            ipaddress.ip_address(match.group(0))
            return True
        except ValueError:
            pass
    for match in IPV6_TOKEN_RE.finditer(value):
        candidate = match.group(0)
        if ":" not in candidate:
            continue
        try:
            ipaddress.ip_address(candidate)
            return True
        except ValueError:
            pass
    return False


def scan_forbidden_content(
    value: object,
    pointer: str = "$",
    issues: list[Issue] | None = None,
) -> list[Issue]:
    if issues is None:
        issues = []
    prohibited = {str(key).casefold() for key in load_protocol()["prohibitedFieldNames"]}
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = _pointer(pointer, key)
            if str(key).casefold() in prohibited:
                issues.append(Issue("PRIVACY_FORBIDDEN_FIELD", child_pointer, "prohibited field name"))
            scan_forbidden_content(child, child_pointer, issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden_content(child, _pointer(pointer, index), issues)
    elif isinstance(value, str):
        if EMAIL_RE.search(value):
            issues.append(Issue("PRIVACY_EMAIL_ADDRESS", pointer, "email address detected"))
        if _contains_ip_address(value):
            issues.append(Issue("PRIVACY_IP_ADDRESS", pointer, "IP address detected"))
        is_typed_git_sha = pointer.endswith("/build/buildRevision") and GIT_SHA_RE.fullmatch(value)
        if SECRET_40_RE.fullmatch(value) and not is_typed_git_sha:
            issues.append(Issue("PRIVACY_SECRET_40", pointer, "40-character secret candidate detected"))
    return issues


def _validate_schema_contract(schema: object, schema_name: str, pointer: str = "$") -> list[Issue]:
    if isinstance(schema, list):
        issues: list[Issue] = []
        for index, child in enumerate(schema):
            if isinstance(child, (dict, list)):
                issues.extend(_validate_schema_contract(child, schema_name, _pointer(pointer, index)))
        return issues
    if not isinstance(schema, dict):
        return []
    issues: list[Issue] = []
    if schema.get("type") == "object" or "properties" in schema:
        properties = schema.get("properties")
        if schema.get("additionalProperties") is not False:
            issues.append(Issue("PROTOCOL_SCHEMA_OPEN", pointer, "object schema must be closed"))
        if not isinstance(properties, dict) or set(schema.get("required", [])) != set(properties):
            issues.append(Issue("PROTOCOL_SCHEMA_REQUIRED", pointer, "every declared property must be required"))
    reference = schema.get("$ref")
    if reference is not None:
        try:
            _resolve_ref(reference, schema_name)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            issues.append(Issue("PROTOCOL_SCHEMA_REF", pointer, str(error)))
    for key, child in schema.items():
        if isinstance(child, (dict, list)):
            issues.extend(_validate_schema_contract(child, schema_name, _pointer(pointer, key)))
    return issues


def validate_protocol() -> list[Issue]:
    issues: list[Issue] = []
    try:
        protocol = load_protocol()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [Issue("PROTOCOL_INVALID", "$", str(error))]
    if protocol.get("protocolId") != "IUM5-GATE-B-1":
        issues.append(Issue("PROTOCOL_ID", "$/protocolId", "unexpected protocol ID"))
    expected_types = set(SCHEMA_BY_DOCUMENT_TYPE)
    observed_types: set[str] = set()
    for schema_name in SCHEMA_BY_DOCUMENT_TYPE.values():
        try:
            schema = _load_json(SCHEMA_ROOT / schema_name)
        except (OSError, json.JSONDecodeError) as error:
            issues.append(Issue("PROTOCOL_SCHEMA_INVALID", f"$/schemas/{schema_name}", str(error)))
            continue
        issues.extend(_validate_schema_contract(schema, schema_name, f"$/schemas/{schema_name}"))
        try:
            observed_types.add(schema["properties"]["documentType"]["const"])
        except (KeyError, TypeError):
            issues.append(Issue("PROTOCOL_DOCUMENT_TYPE", f"$/schemas/{schema_name}", "fixed document type is missing"))
    if observed_types != expected_types:
        issues.append(Issue("PROTOCOL_DOCUMENT_TYPES", "$/schemas", "document types are incomplete or duplicated"))
    return issues


def _load_schema_for(document_type: str) -> tuple[dict[str, object] | None, list[Issue]]:
    schema_name = SCHEMA_BY_DOCUMENT_TYPE.get(document_type)
    if schema_name is None:
        return None, [Issue("DOCUMENT_TYPE_UNSUPPORTED", "$/documentType", "unsupported document type")]
    try:
        schema = _load_json(SCHEMA_ROOT / schema_name)
    except (OSError, json.JSONDecodeError) as error:
        return None, [Issue("SCHEMA_LOAD_FAILED", "$", str(error))]
    return schema, []


def validate_evidence(document: object) -> list[Issue]:
    issues = scan_forbidden_content(document)
    if not isinstance(document, dict):
        issues.append(Issue("DOCUMENT_ROOT_TYPE", "$", "evidence root must be an object"))
        return issues
    document_type = document.get("documentType")
    if document_type not in {
        "ium5-gate-b-technical-evidence",
        "ium5-gate-b-pilot-evidence",
    }:
        issues.append(Issue("DOCUMENT_TYPE_UNSUPPORTED", "$/documentType", "unsupported evidence document type"))
        return issues
    schema, schema_issues = _load_schema_for(document_type)
    issues.extend(schema_issues)
    if schema is None:
        return issues
    schema_name = SCHEMA_BY_DOCUMENT_TYPE[document_type]
    issues.extend(_validate_schema(document, schema, schema_name))
    if document_type == "ium5-gate-b-technical-evidence" and isinstance(document.get("rows"), list):
        expected_ids = [row["id"] for row in load_protocol()["technicalMatrix"]]
        observed_ids = [row.get("id") for row in document["rows"] if isinstance(row, dict)]
        if observed_ids != expected_ids:
            issues.append(Issue("SEMANTIC_MATRIX_IDS", "$/rows", "matrix row IDs must match protocol order exactly"))
    return issues


def validate_decision(document: object) -> tuple[list[Issue], dict[str, str] | None]:
    issues = scan_forbidden_content(document)
    if not isinstance(document, dict):
        issues.append(Issue("DOCUMENT_ROOT_TYPE", "$", "decision root must be an object"))
        return issues, None
    schema, schema_issues = _load_schema_for(str(document.get("documentType", "")))
    issues.extend(schema_issues)
    if schema is not None:
        issues.extend(_validate_schema(document, schema, "decision-package.schema.json"))
    if issues:
        return issues, None
    derived = document.get("derived")
    return [], dict(derived) if isinstance(derived, dict) else None


def _read_document(path: Path) -> tuple[object | None, list[Issue]]:
    try:
        return _load_json(path), []
    except (OSError, json.JSONDecodeError) as error:
        return None, [Issue("DOCUMENT_LOAD_FAILED", "$", str(error))]


def _print_issues(issues: list[Issue]) -> None:
    for issue in issues:
        print(f"{issue.code}\t{issue.pointer}\t{issue.message}")


def _run_cli(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("protocol")
    evidence_parser = subparsers.add_parser("evidence")
    evidence_parser.add_argument("path", type=Path)
    decision_parser = subparsers.add_parser("decision")
    decision_parser.add_argument("path", type=Path)
    subparsers.add_parser("synthetic")
    args = parser.parse_args(arguments)

    if args.command == "protocol":
        issues = validate_protocol()
        if issues:
            _print_issues(issues)
            return 1
        print("PROTOCOL_VALID")
        return 0

    if args.command == "synthetic":
        print("SYNTHETIC_EXAMPLES_MISSING\t$\tsynthetic examples are not implemented")
        return 1

    document, issues = _read_document(args.path)
    if not issues:
        if args.command == "evidence":
            issues = validate_evidence(document)
            result = None
        else:
            issues, result = validate_decision(document)
    else:
        result = None
    if issues:
        _print_issues(issues)
        return 1
    print("EVIDENCE_VALID" if args.command == "evidence" else "DECISION_VALID")
    if result is not None:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(_run_cli())
