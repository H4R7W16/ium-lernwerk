import json
from pathlib import Path


class ValidationError(ValueError):
    pass


SOURCE_KINDS = {
    "official",
    "systematic-review",
    "meta-analysis",
    "empirical-study",
    "research-synthesis",
    "handbook",
    "professional-standard",
    "secondary",
}
VERIFICATION_STATUSES = {
    "primary-checked",
    "metadata-checked",
    "secondary-only",
}
NORMATIVE_STATUSES = {
    "enacted",
    "orientation",
    "administrative-information",
    "superseded",
}
CLAIM_STATUSES = {"draft", "working", "reviewed", "standard"}
EVIDENCE_LEVELS = {"low", "medium", "high", "normative"}
REVIEWED_CLAIM_STATUSES = {"reviewed", "standard"}
SOURCE_ID_PREFIX = "SRC-"
CLAIM_ID_PREFIXES = ("CLAIM-INF-", "CLAIM-MED-", "CLAIM-LP-", "CLAIM-DLE-")


class SourceIndex(set):
    """Set-compatible source IDs with metadata for claim validation."""

    def __init__(self, sources):
        super().__init__(source["id"] for source in sources)
        self.verification_statuses = {
            source["id"]: source["verificationStatus"] for source in sources
        }


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition, message):
    if not condition:
        raise ValidationError(message)


def _require_fields(record, fields, record_type):
    _require(isinstance(record, dict), f"{record_type} must be an object")
    missing_fields = [field for field in fields if field not in record]
    _require(not missing_fields, f"{record_type} missing fields: {', '.join(missing_fields)}")


def _require_nonempty_string(value, field, record_id):
    _require(
        isinstance(value, str) and value.strip(),
        f"{field} missing or invalid: {record_id}",
    )


def _require_string_or_none(value, field, record_id):
    _require(
        value is None or isinstance(value, str),
        f"{field} must be a string or null: {record_id}",
    )


def _require_technical_id(value, prefixes, record_type):
    _require(value.isascii(), f"{record_type} id must be ASCII: {value}")
    _require(
        any(value.startswith(prefix) and len(value) > len(prefix) for prefix in prefixes),
        f"invalid {record_type} id prefix: {value}",
    )


def validate_source_register(payload):
    _require(payload.get("schemaVersion") == 1, "source register schemaVersion must be 1")
    sources = payload.get("sources")
    _require(isinstance(sources, list), "sources must be a list")
    required_fields = (
        "id",
        "package",
        "sourceKind",
        "title",
        "authors",
        "year",
        "url",
        "doi",
        "license",
        "accessed",
        "verificationStatus",
        "normativeStatus",
        "relevance",
    )
    for source in sources:
        _require_fields(source, required_fields, "source")
    ids = [source["id"] for source in sources]
    _require(
        all(isinstance(source_id, str) and source_id for source_id in ids),
        "every source needs an id",
    )
    _require(len(ids) == len(set(ids)), "source ids must be unique")
    for source in sources:
        source_id = source["id"]
        _require_nonempty_string(source_id, "id", source_id)
        _require_technical_id(source_id, (SOURCE_ID_PREFIX,), "source")
        _require_nonempty_string(source["package"], "package", source_id)
        _require(
            source["sourceKind"] in SOURCE_KINDS,
            f"invalid source kind: {source_id}",
        )
        _require_nonempty_string(source["title"], "title", source_id)
        _require(
            isinstance(source["authors"], list),
            f"authors must be a list: {source_id}",
        )
        _require(
            source["year"] is None
            or (isinstance(source["year"], (int, float)) and not isinstance(source["year"], bool)),
            f"year must be a number or null: {source_id}",
        )
        _require_string_or_none(source["url"], "url", source_id)
        _require_string_or_none(source["doi"], "doi", source_id)
        _require_nonempty_string(source["license"], "license", source_id)
        _require_nonempty_string(source["accessed"], "accessed", source_id)
        _require(
            source["verificationStatus"] in VERIFICATION_STATUSES,
            f"invalid verification status: {source_id}",
        )
        if source["sourceKind"] == "official":
            _require(
                source["normativeStatus"] in NORMATIVE_STATUSES,
                f"official source needs valid normative status: {source_id}",
            )
        else:
            _require(
                source["normativeStatus"] is None,
                f"non-official source must use null normative status: {source_id}",
            )
        _require(
            isinstance(source["relevance"], list) and source["relevance"],
            f"relevance missing: {source_id}",
        )
    return SourceIndex(sources)


def validate_claim_ledger(payload, source_ids):
    _require(payload.get("schemaVersion") == 1, "claim ledger schemaVersion must be 1")
    claims = payload.get("claims")
    _require(isinstance(claims, list), "claims must be a list")
    required_fields = (
        "id",
        "package",
        "statement",
        "scope",
        "status",
        "evidenceLevel",
        "sourceIds",
        "limitations",
        "designImplications",
    )
    for claim in claims:
        _require_fields(claim, required_fields, "claim")
    ids = [claim["id"] for claim in claims]
    _require(len(ids) == len(set(ids)), "claim ids must be unique")
    source_id_set = set(source_ids)
    verification_statuses = getattr(source_ids, "verification_statuses", None)
    for claim in claims:
        claim_id = claim["id"]
        _require_nonempty_string(claim_id, "id", claim_id)
        _require_technical_id(claim_id, CLAIM_ID_PREFIXES, "claim")
        _require_nonempty_string(claim["package"], "package", claim_id)
        _require_nonempty_string(claim["statement"], "statement", claim_id)
        _require_nonempty_string(claim["scope"], "scope", claim_id)
        _require(
            claim["status"] in CLAIM_STATUSES,
            f"invalid claim status: {claim_id}",
        )
        _require(
            claim["evidenceLevel"] in EVIDENCE_LEVELS,
            f"invalid evidence level: {claim_id}",
        )
        _require(
            isinstance(claim["sourceIds"], list)
            and all(isinstance(source_id, str) and source_id for source_id in claim["sourceIds"]),
            f"source ids must be a list of nonempty strings: {claim_id}",
        )
        _require(
            isinstance(claim["limitations"], str),
            f"limitations must be a string: {claim_id}",
        )
        _require(
            isinstance(claim["designImplications"], list),
            f"design implications must be a list: {claim_id}",
        )
        _require(
            set(claim["sourceIds"]) <= source_id_set,
            f"unknown source id: {claim_id}",
        )
        if claim["status"] in REVIEWED_CLAIM_STATUSES:
            _require(claim["sourceIds"], f"reviewed claim has no source: {claim_id}")
            _require(
                claim["limitations"].strip(),
                f"reviewed claim has no limitations: {claim_id}",
            )
            _require(
                verification_statuses is not None,
                f"reviewed claim requires source verification metadata: {claim_id}",
            )
            _require(
                any(
                    verification_statuses[source_id] == "primary-checked"
                    for source_id in claim["sourceIds"]
                ),
                f"reviewed claim has no primary-checked source: {claim_id}",
            )
    return set(ids)


def main():
    root = Path(__file__).resolve().parents[1]
    source_ids = validate_source_register(
        load_json(root / "docs/research/phase-0/source-register.json")
    )
    validate_claim_ledger(
        load_json(root / "docs/research/phase-0/claim-ledger.json"),
        source_ids,
    )
    print("phase 0 validation passed")


if __name__ == "__main__":
    main()
