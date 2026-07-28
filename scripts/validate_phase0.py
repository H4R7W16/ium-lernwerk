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
DESIGN_PRINCIPLE_ID_PREFIX = "PRIN-"
CURRICULUM_RECORD_TYPES = {
    "competency",
    "progression-note",
    "example",
    "operator",
    "process-competency",
}
CURRICULUM_RECORD_STATUSES = {"verified", "plausible", "open"}


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


def _require_nonempty_string_list(value, field, record_id):
    _require(
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value),
        f"{field} must be a nonempty list of nonempty strings: {record_id}",
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


def validate_design_principles(payload, claim_ids):
    _require(
        payload.get("schemaVersion") == 1
        and not isinstance(payload.get("schemaVersion"), bool),
        "design principles schemaVersion must be 1",
    )
    principles = payload.get("principles")
    _require(isinstance(principles, list), "principles must be a list")
    required_fields = (
        "id",
        "title",
        "statement",
        "claimIds",
        "appliesTo",
        "status",
        "phase1Implications",
        "risks",
    )
    for principle in principles:
        _require_fields(principle, required_fields, "design principle")
    ids = [principle["id"] for principle in principles]
    _require(
        all(isinstance(principle_id, str) and principle_id.strip() for principle_id in ids),
        "every design principle needs a nonempty id",
    )
    _require(len(ids) == len(set(ids)), "design principle ids must be unique")
    registered_claim_ids = set(claim_ids)
    for principle in principles:
        principle_id = principle["id"]
        _require(
            principle_id.isascii(),
            f"design principle id must be ASCII: {principle_id}",
        )
        suffix = principle_id[len(DESIGN_PRINCIPLE_ID_PREFIX):]
        _require(
            principle_id.startswith(DESIGN_PRINCIPLE_ID_PREFIX)
            and bool(suffix)
            and all(character.isalnum() or character in "-_." for character in suffix),
            f"invalid design principle id: {principle_id}",
        )
        _require_nonempty_string(principle["title"], "title", principle_id)
        _require_nonempty_string(principle["statement"], "statement", principle_id)
        _require_nonempty_string_list(
            principle["claimIds"], "claimIds", principle_id
        )
        _require(
            len(principle["claimIds"]) == len(set(principle["claimIds"])),
            f"claimIds must be unique within a design principle: {principle_id}",
        )
        _require(
            set(principle["claimIds"]) <= registered_claim_ids,
            f"unknown claim id: {principle_id}",
        )
        _require_nonempty_string_list(
            principle["appliesTo"], "appliesTo", principle_id
        )
        _require(
            principle["status"] in CLAIM_STATUSES,
            f"invalid design principle status: {principle_id}",
        )
        _require_nonempty_string_list(
            principle["phase1Implications"],
            "phase1Implications",
            principle_id,
        )
        _require_nonempty_string_list(
            principle["risks"], "risks", principle_id
        )
    return set(ids)


def validate_curriculum_dataset(payload, source_ids):
    _require(
        payload.get("schemaVersion") == 1,
        "curriculum dataset schemaVersion must be 1",
    )
    source_id = payload.get("sourceId")
    _require(
        isinstance(source_id, str) and source_id in set(source_ids),
        f"unknown curriculum source id: {source_id}",
    )
    records = payload.get("records")
    _require(isinstance(records, list), "curriculum records must be a list")
    required_fields = (
        "id",
        "sourceId",
        "text",
        "grades",
        "level",
        "area",
        "recordType",
        "sourceLocator",
        "status",
    )
    for record in records:
        _require_fields(record, required_fields, "curriculum record")
    ids = [record["id"] for record in records]
    _require(
        all(isinstance(record_id, str) and record_id.strip() for record_id in ids),
        "every curriculum record needs a nonempty id",
    )
    _require(
        all(record_id.isascii() for record_id in ids),
        "curriculum record ids must be ASCII",
    )
    _require(len(ids) == len(set(ids)), "curriculum record ids must be unique")
    for record in records:
        record_id = record["id"]
        _require(
            record["sourceId"] == source_id,
            f"curriculum record source mismatch: {record_id}",
        )
        _require_nonempty_string(record["text"], "text", record_id)
        _require(
            isinstance(record["grades"], list)
            and bool(record["grades"])
            and all(
                isinstance(grade, int)
                and not isinstance(grade, bool)
                and 1 <= grade <= 13
                for grade in record["grades"]
            ),
            f"grades missing or invalid: {record_id}",
        )
        _require_nonempty_string(record["level"], "level", record_id)
        _require_nonempty_string(record["area"], "area", record_id)
        _require(
            record["recordType"] in CURRICULUM_RECORD_TYPES,
            f"invalid curriculum record type: {record_id}",
        )
        locator = record["sourceLocator"]
        _require(
            isinstance(locator, dict),
            f"source locator must be an object: {record_id}",
        )
        page = locator.get("page")
        _require(
            isinstance(page, int) and not isinstance(page, bool) and page > 0,
            f"PDF page must be a positive integer: {record_id}",
        )
        _require_nonempty_string(locator.get("section"), "section", record_id)
        _require(
            record["status"] in CURRICULUM_RECORD_STATUSES,
            f"invalid curriculum record status: {record_id}",
        )
    return set(ids)


def main():
    root = Path(__file__).resolve().parents[1]
    source_ids = validate_source_register(
        load_json(root / "docs/research/phase-0/source-register.json")
    )
    claim_ids = validate_claim_ledger(
        load_json(root / "docs/research/phase-0/claim-ledger.json"),
        source_ids,
    )
    design_principles_file = root / "docs/research/phase-0/design-principles.json"
    if design_principles_file.exists():
        validate_design_principles(
            load_json(design_principles_file),
            claim_ids,
        )
    curriculum_files = sorted((root / "curriculum").glob("**/competencies.json"))
    for curriculum_file in curriculum_files:
        validate_curriculum_dataset(load_json(curriculum_file), source_ids)
    print("phase 0 validation passed")


if __name__ == "__main__":
    main()
