import json
import re
from collections import Counter
from collections.abc import Mapping
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
CROSSWALK_RELATIONSHIPS = {
    "equivalent",
    "overlaps",
    "extends",
    "reframes",
    "new",
    "not-comparable",
}
CROSSWALK_RELATION_STATUSES = {"resolved", "open"}
OPERATOR_KINDS = {"operator", "process-competency"}
SOURCE_AFBS = {"I", "II", "III"}
OPERATOR_COMPLEXITY_BANDS = {
    "guided-reproduction-and-operation",
    "structured-application-and-relation",
    "independent-transfer-design-and-evaluation",
    "context-dependent",
}
INTEGRATION_STATUSES = {"working", "reviewed"}
MODULE_KINDS = {"core", "extension", "transfer", "project"}
MODULE_KIND_TOKENS = {
    "CORE": "core",
    "EXT": "extension",
    "TRANSFER": "transfer",
    "PROJECT": "project",
}
MODULE_STRAND_IDS = {
    "STRAND-A",
    "STRAND-B",
    "STRAND-C",
    "STRAND-D",
    "STRAND-E",
}
MODULE_GRAMMAR_PHASES = (
    "orientation-challenge",
    "activate-prior-knowledge",
    "build-concept",
    "guided-practice",
    "independent-action-product",
    "review-revise-transfer",
    "shared-consolidation",
)
MODULE_ID_PATTERN = re.compile(
    r"^IUM-([5-7])-(CORE|EXT|TRANSFER|PROJECT)-([0-9]{2})$"
)
REQUIRED_CROSSWALK_SOURCE_COMPARISONS = {
    ("SRC-CUR-LESEHILFE-2026-27", "SRC-CUR-BMB-2016"),
    ("SRC-CUR-LESEHILFE-2026-27", "SRC-CUR-INF7-2016"),
    ("SRC-CUR-BMB-2016", "SRC-CUR-INF7-2016"),
}


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
        isinstance(payload, dict),
        "design principles payload must be an object",
    )
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
            isinstance(principle["status"], str),
            f"design principle status must be a string: {principle_id}",
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


def validate_crosswalk(payload, curriculum_ids):
    _require(isinstance(payload, dict), "crosswalk payload must be an object")
    _require_fields(
        payload,
        (
            "schemaVersion",
            "status",
            "requiredSourceComparisons",
            "counts",
            "relations",
            "unmappedRecords",
        ),
        "crosswalk",
    )
    _require(
        payload.get("schemaVersion") == 1
        and not isinstance(payload.get("schemaVersion"), bool),
        "crosswalk schemaVersion must be 1",
    )
    _require(
        isinstance(payload.get("status"), str)
        and payload.get("status") in INTEGRATION_STATUSES,
        "crosswalk status must be working or reviewed",
    )
    relations = payload.get("relations")
    unmapped_records = payload.get("unmappedRecords")
    _require(isinstance(relations, list), "crosswalk relations must be a list")
    _require(
        isinstance(unmapped_records, list),
        "crosswalk unmappedRecords must be a list",
    )
    source_records = curriculum_ids if isinstance(curriculum_ids, dict) else None
    registered_ids = set(curriculum_ids)
    covered_ids = set()
    relation_required_fields = (
        "id",
        "fromIds",
        "toIds",
        "relationship",
        "rationale",
        "status",
        "followUp",
    )
    relation_ids = []
    mapped_ids = set()
    for relation in relations:
        _require_fields(relation, relation_required_fields, "crosswalk relation")
        relation_id = relation["id"]
        _require_nonempty_string(relation_id, "id", relation_id)
        _require_technical_id(
            relation_id,
            ("XW-",),
            "crosswalk relation",
        )
        relation_ids.append(relation_id)
        for field in ("fromIds", "toIds"):
            value = relation[field]
            _require(
                isinstance(value, list)
                and all(isinstance(record_id, str) and record_id for record_id in value),
                f"{field} must be a list of nonempty strings: {relation_id}",
            )
            _require(
                len(value) == len(set(value)),
                f"{field} ids must be unique: {relation_id}",
            )
            _require(
                set(value) <= registered_ids,
                f"unknown curriculum record id in {field}: {relation_id}",
            )
            covered_ids.update(value)
            mapped_ids.update(value)
        _require(
            set(relation["fromIds"]).isdisjoint(relation["toIds"]),
            f"crosswalk relation sides must be disjoint: {relation_id}",
        )
        relationship = relation["relationship"]
        _require(
            isinstance(relationship, str)
            and relationship in CROSSWALK_RELATIONSHIPS,
            f"invalid crosswalk relationship: {relation_id}",
        )
        if relationship in {"equivalent", "overlaps", "extends", "reframes"}:
            _require(
                bool(relation["fromIds"]) and bool(relation["toIds"]),
                f"comparative relationship needs fromIds and toIds: {relation_id}",
            )
        elif relationship == "new":
            _require(
                bool(relation["fromIds"]) and not relation["toIds"],
                f"new relationship needs fromIds and no toIds: {relation_id}",
            )
        else:
            _require(
                bool(relation["fromIds"]) and not relation["toIds"],
                f"not-comparable relationship needs fromIds and no toIds: {relation_id}",
            )
        _require_nonempty_string(
            relation["rationale"],
            "rationale",
            relation_id,
        )
        _require(
            isinstance(relation["status"], str)
            and relation["status"] in CROSSWALK_RELATION_STATUSES,
            f"invalid crosswalk relation status: {relation_id}",
        )
        _require(
            isinstance(relation["followUp"], str),
            f"followUp must be a string: {relation_id}",
        )
        if relation["status"] == "open":
            _require(
                relation["followUp"].strip(),
                f"open crosswalk relation needs followUp: {relation_id}",
            )
    _require(
        len(relation_ids) == len(set(relation_ids)),
        "crosswalk relation ids must be unique",
    )

    unmapped_required_fields = ("recordId", "reason", "followUp")
    unmapped_ids = []
    for unmapped in unmapped_records:
        _require_fields(unmapped, unmapped_required_fields, "unmapped record")
        record_id = unmapped["recordId"]
        _require(
            isinstance(record_id, str) and record_id in registered_ids,
            f"unknown unmapped curriculum record id: {record_id}",
        )
        _require_nonempty_string(unmapped["reason"], "reason", record_id)
        _require_nonempty_string(unmapped["followUp"], "followUp", record_id)
        unmapped_ids.append(record_id)
        covered_ids.add(record_id)
    _require(
        len(unmapped_ids) == len(set(unmapped_ids)),
        "unmapped curriculum record ids must be unique",
    )
    _require(
        mapped_ids.isdisjoint(unmapped_ids),
        "curriculum records cannot be both mapped and unmapped",
    )
    counts = payload["counts"]
    _require_fields(
        counts,
        (
            "curriculumRecords",
            "relations",
            "unmappedRecords",
            "relationshipCounts",
        ),
        "crosswalk counts",
    )
    expected_relationship_counts = dict(
        sorted(
            Counter(
                relation["relationship"] for relation in relations
            ).items()
        )
    )
    expected_counts = {
        "curriculumRecords": len(registered_ids),
        "relations": len(relations),
        "unmappedRecords": len(unmapped_records),
        "relationshipCounts": expected_relationship_counts,
    }
    _require(
        counts == expected_counts,
        "crosswalk counts do not match payload",
    )
    required_comparisons = payload["requiredSourceComparisons"]
    _require(
        isinstance(required_comparisons, list),
        "requiredSourceComparisons must be a list",
    )
    available_source_ids = (
        {
            record["sourceId"]
            for record in source_records.values()
        }
        if source_records is not None
        else set()
    )
    comparison_pairs = []
    for comparison in required_comparisons:
        _require(
            source_records is not None,
            "required source comparisons need curriculum source metadata",
        )
        _require_fields(
            comparison,
            ("fromSourceId", "toSourceId"),
            "required source comparison",
        )
        from_source_id = comparison["fromSourceId"]
        to_source_id = comparison["toSourceId"]
        _require(
            isinstance(from_source_id, str)
            and isinstance(to_source_id, str)
            and from_source_id in available_source_ids
            and to_source_id in available_source_ids
            and from_source_id != to_source_id,
            "invalid required source comparison",
        )
        comparison_pairs.append((from_source_id, to_source_id))
        has_direct_relation = any(
            any(
                source_records[record_id]["sourceId"]
                == from_source_id
                for record_id in relation["fromIds"]
            )
            and any(
                source_records[record_id]["sourceId"]
                == to_source_id
                for record_id in relation["toIds"]
            )
            for relation in relations
        )
        _require(
            has_direct_relation,
            "required source comparison has no direct relation: "
            f"{from_source_id} -> {to_source_id}",
        )
    _require(
        len(comparison_pairs) == len(set(comparison_pairs)),
        "required source comparisons must be unique",
    )
    canonical_source_ids = {
        source_id
        for pair in REQUIRED_CROSSWALK_SOURCE_COMPARISONS
        for source_id in pair
    }
    if canonical_source_ids <= available_source_ids:
        _require(
            set(comparison_pairs)
            == REQUIRED_CROSSWALK_SOURCE_COMPARISONS,
            "canonical curriculum source comparisons are incomplete",
        )

    _require(
        covered_ids == registered_ids,
        "every curriculum record must be mapped or explicitly unmapped",
    )
    return covered_ids


def validate_operators(payload, curriculum_ids):
    _require(isinstance(payload, dict), "operators payload must be an object")
    _require(
        payload.get("schemaVersion") == 1
        and not isinstance(payload.get("schemaVersion"), bool),
        "operators schemaVersion must be 1",
    )
    _require(
        isinstance(payload.get("status"), str)
        and payload.get("status") in INTEGRATION_STATUSES,
        "operators status must be working or reviewed",
    )
    entries = payload.get("entries")
    _require(isinstance(entries, list), "operator entries must be a list")
    required_fields = (
        "id",
        "kind",
        "exactOfficialTerm",
        "sourceRecordId",
        "sourceDefinition",
        "sourceAfb",
        "expectedObservableAction",
        "likelyComplexityBand",
        "applicableGrades",
        "notesOnAmbiguity",
        "status",
    )
    source_records = curriculum_ids if isinstance(curriculum_ids, dict) else None
    registered_ids = set(curriculum_ids)
    source_record_ids = []
    entry_ids = []
    for entry in entries:
        _require_fields(entry, required_fields, "operator entry")
        entry_id = entry["id"]
        _require_nonempty_string(entry_id, "id", entry_id)
        _require_technical_id(entry_id, ("OPMAP-",), "operator entry")
        entry_ids.append(entry_id)
        _require(
            isinstance(entry["kind"], str)
            and entry["kind"] in OPERATOR_KINDS,
            f"invalid operator entry kind: {entry_id}",
        )
        _require_nonempty_string(
            entry["exactOfficialTerm"],
            "exactOfficialTerm",
            entry_id,
        )
        source_record_id = entry["sourceRecordId"]
        _require(
            isinstance(source_record_id, str)
            and source_record_id in registered_ids,
            f"unknown operator source record: {entry_id}",
        )
        source_record_ids.append(source_record_id)
        _require_nonempty_string(
            entry["sourceDefinition"],
            "sourceDefinition",
            entry_id,
        )
        _require(
            entry["sourceAfb"] is None
            or (
                isinstance(entry["sourceAfb"], str)
                and entry["sourceAfb"] in SOURCE_AFBS
            ),
            f"invalid sourceAfb: {entry_id}",
        )
        _require_nonempty_string(
            entry["expectedObservableAction"],
            "expectedObservableAction",
            entry_id,
        )
        _require(
            isinstance(entry["likelyComplexityBand"], str)
            and entry["likelyComplexityBand"] in OPERATOR_COMPLEXITY_BANDS,
            f"invalid likelyComplexityBand: {entry_id}",
        )
        _require(
            isinstance(entry["applicableGrades"], list)
            and bool(entry["applicableGrades"])
            and all(
                isinstance(grade, int)
                and not isinstance(grade, bool)
                and grade in {5, 6, 7}
                for grade in entry["applicableGrades"]
            ),
            f"invalid applicableGrades: {entry_id}",
        )
        _require(
            isinstance(entry["notesOnAmbiguity"], str),
            f"notesOnAmbiguity must be a string: {entry_id}",
        )
        _require(
            isinstance(entry["status"], str)
            and entry["status"] in INTEGRATION_STATUSES,
            f"invalid operator entry status: {entry_id}",
        )
        if entry["kind"] == "operator":
            _require(
                entry["sourceAfb"] in SOURCE_AFBS,
                f"operator needs sourceAfb: {entry_id}",
            )
        else:
            _require(
                entry["sourceAfb"] is None,
                f"process competency must use null sourceAfb: {entry_id}",
            )
        if source_records is not None:
            source_record = source_records[source_record_id]
            expected_term = (
                source_record["operator"]
                if source_record["recordType"] == "operator"
                else source_record["text"]
            )
            expected_afb = (
                source_record["afb"]
                if source_record["recordType"] == "operator"
                else None
            )
            _require(
                entry["kind"] == source_record["recordType"],
                f"operator kind differs from source record: {entry_id}",
            )
            _require(
                entry["exactOfficialTerm"] == expected_term,
                f"official term differs from source record: {entry_id}",
            )
            _require(
                entry["sourceDefinition"] == source_record["text"],
                f"source definition differs from source record: {entry_id}",
            )
            _require(
                entry["sourceAfb"] == expected_afb,
                f"sourceAfb differs from source record: {entry_id}",
            )
            _require(
                entry["applicableGrades"] == source_record["grades"],
                f"applicableGrades differ from source record: {entry_id}",
            )
    _require(
        len(entry_ids) == len(set(entry_ids)),
        "operator entry ids must be unique",
    )
    _require(
        len(source_record_ids) == len(set(source_record_ids)),
        "operator source records must be unique",
    )
    source_record_id_set = set(source_record_ids)
    _require(
        source_record_id_set == registered_ids,
        "every requested operator or process competency needs an entry",
    )
    return source_record_id_set


def validate_module_candidates(payload, curriculum_ids):
    _require(
        isinstance(payload, dict),
        "module candidates payload must be an object",
    )
    _require_fields(
        payload,
        ("schemaVersion", "status", "modules"),
        "module candidates payload",
    )
    _require(
        payload["schemaVersion"] == 1
        and not isinstance(payload["schemaVersion"], bool),
        "module candidates schemaVersion must be 1",
    )
    _require(
        isinstance(payload["status"], str)
        and payload["status"] in INTEGRATION_STATUSES,
        "module candidates status must be working or reviewed",
    )
    modules = payload["modules"]
    _require(
        isinstance(modules, list) and bool(modules),
        "module candidates modules must be a nonempty list",
    )
    _require(
        isinstance(curriculum_ids, Mapping),
        "module candidates need a curriculum grade mapping",
    )
    curriculum_grade_map = {}
    for curriculum_id, curriculum_grades in curriculum_ids.items():
        _require(
            isinstance(curriculum_id, str)
            and bool(curriculum_id.strip())
            and isinstance(curriculum_grades, (list, tuple, set))
            and bool(curriculum_grades)
            and all(
                isinstance(curriculum_grade, int)
                and not isinstance(curriculum_grade, bool)
                and curriculum_grade in {5, 6, 7}
                for curriculum_grade in curriculum_grades
            ),
            f"invalid curriculum grade contract: {curriculum_id}",
        )
        curriculum_grade_map[curriculum_id] = set(curriculum_grades)
    registered_curriculum_ids = set(curriculum_grade_map)
    _require(
        bool(registered_curriculum_ids),
        "module candidates need registered curriculum ids",
    )
    required_fields = (
        "id",
        "title",
        "grade",
        "kind",
        "strandIds",
        "competencyIds",
        "prerequisiteModuleIds",
        "lessonRange",
        "centralQuestion",
        "centralLearningAction",
        "centralLearningProduct",
        "moduleGrammar",
        "mediumRationale",
        "analogMaterials",
        "assessmentWorkingNotes",
        "status",
    )
    module_ids = []
    module_kinds = {}
    module_grades = {}
    prerequisite_ids_by_module = {}
    core_curriculum_ids = set()
    grammar_phase_order = {
        phase: index
        for index, phase in enumerate(MODULE_GRAMMAR_PHASES)
    }
    for module in modules:
        _require_fields(module, required_fields, "module candidate")
        module_id = module["id"]
        _require_nonempty_string(module_id, "id", module_id)
        match = MODULE_ID_PATTERN.fullmatch(module_id)
        _require(match is not None, f"invalid module candidate id: {module_id}")
        module_ids.append(module_id)
        _require_nonempty_string(module["title"], "title", module_id)
        grade = module["grade"]
        _require(
            isinstance(grade, int)
            and not isinstance(grade, bool)
            and grade in {5, 6, 7},
            f"invalid module grade: {module_id}",
        )
        kind = module["kind"]
        _require(
            isinstance(kind, str) and kind in MODULE_KINDS,
            f"invalid module kind: {module_id}",
        )
        _require(
            int(match.group(1)) == grade
            and MODULE_KIND_TOKENS[match.group(2)] == kind,
            f"module id, grade and kind do not match: {module_id}",
        )
        module_kinds[module_id] = kind
        module_grades[module_id] = grade
        strand_ids = module["strandIds"]
        _require(
            isinstance(strand_ids, list)
            and bool(strand_ids)
            and all(
                isinstance(strand_id, str)
                and strand_id in MODULE_STRAND_IDS
                for strand_id in strand_ids
            )
            and len(strand_ids) == len(set(strand_ids)),
            f"invalid strandIds: {module_id}",
        )
        competency_ids = module["competencyIds"]
        _require(
            isinstance(competency_ids, list)
            and bool(competency_ids)
            and all(
                isinstance(competency_id, str) and competency_id
                for competency_id in competency_ids
            )
            and len(competency_ids) == len(set(competency_ids)),
            f"invalid competencyIds: {module_id}",
        )
        _require(
            set(competency_ids) <= registered_curriculum_ids,
            f"unknown competency id: {module_id}",
        )
        _require(
            all(
                grade in curriculum_grade_map[competency_id]
                for competency_id in competency_ids
                if competency_id in curriculum_grade_map
            ),
            f"competency grade does not match module grade: {module_id}",
        )
        if kind == "core":
            core_curriculum_ids.update(competency_ids)
        prerequisite_ids = module["prerequisiteModuleIds"]
        _require(
            isinstance(prerequisite_ids, list)
            and all(
                isinstance(prerequisite_id, str) and prerequisite_id
                for prerequisite_id in prerequisite_ids
            )
            and len(prerequisite_ids) == len(set(prerequisite_ids)),
            f"invalid prerequisiteModuleIds: {module_id}",
        )
        prerequisite_ids_by_module[module_id] = prerequisite_ids
        lesson_range = module["lessonRange"]
        _require_fields(
            lesson_range,
            ("min", "max"),
            f"lessonRange for {module_id}",
        )
        minimum_lessons = lesson_range["min"]
        maximum_lessons = lesson_range["max"]
        _require(
            isinstance(minimum_lessons, int)
            and not isinstance(minimum_lessons, bool)
            and isinstance(maximum_lessons, int)
            and not isinstance(maximum_lessons, bool)
            and minimum_lessons > 0
            and minimum_lessons <= maximum_lessons,
            f"invalid lessonRange: {module_id}",
        )
        for field in (
            "centralQuestion",
            "centralLearningAction",
            "centralLearningProduct",
            "mediumRationale",
            "assessmentWorkingNotes",
        ):
            _require_nonempty_string(module[field], field, module_id)
        module_grammar = module["moduleGrammar"]
        _require(
            isinstance(module_grammar, list)
            and bool(module_grammar)
            and all(
                isinstance(phase, str)
                and phase in grammar_phase_order
                for phase in module_grammar
            )
            and len(module_grammar) == len(set(module_grammar)),
            f"invalid moduleGrammar: {module_id}",
        )
        _require(
            module_grammar
            == sorted(
                module_grammar,
                key=grammar_phase_order.__getitem__,
            ),
            f"moduleGrammar phases are out of order: {module_id}",
        )
        if kind == "core":
            _require(
                module_grammar == list(MODULE_GRAMMAR_PHASES),
                f"core module needs all grammar phases: {module_id}",
            )
        analog_materials = module["analogMaterials"]
        _require(
            isinstance(analog_materials, list),
            f"analogMaterials must be a list: {module_id}",
        )
        for analog_material in analog_materials:
            _require_fields(
                analog_material,
                ("title", "didacticRationale", "digitalReconnection"),
                f"analog material for {module_id}",
            )
            for field in (
                "title",
                "didacticRationale",
                "digitalReconnection",
            ):
                _require_nonempty_string(
                    analog_material[field],
                    field,
                    module_id,
                )
        _require(
            isinstance(module["status"], str)
            and module["status"] in INTEGRATION_STATUSES,
            f"invalid module candidate status: {module_id}",
        )
    _require(
        len(module_ids) == len(set(module_ids)),
        "module candidate ids must be unique",
    )
    module_id_set = set(module_ids)
    _require(
        set(module_kinds.values()) == MODULE_KINDS,
        "module candidates must include all hybrid module kinds",
    )
    for module_id, prerequisite_ids in prerequisite_ids_by_module.items():
        _require(
            set(prerequisite_ids) <= module_id_set,
            f"unknown prerequisite module id: {module_id}",
        )
        _require(
            module_id not in prerequisite_ids,
            f"module cannot depend on itself: {module_id}",
        )
        _require(
            all(
                module_grades[prerequisite_id] <= module_grades[module_id]
                for prerequisite_id in prerequisite_ids
            ),
            f"module cannot depend on a later grade: {module_id}",
        )
        if module_kinds[module_id] == "core":
            _require(
                all(
                    module_kinds[prerequisite_id] == "core"
                    for prerequisite_id in prerequisite_ids
                ),
                f"core module cannot depend on flexible module: {module_id}",
            )
        else:
            _require(
                all(
                    module_kinds[prerequisite_id] == "core"
                    for prerequisite_id in prerequisite_ids
                ),
                f"flexible module prerequisites must be core: {module_id}",
            )
    _require(
        core_curriculum_ids == registered_curriculum_ids,
        "core modules must jointly cover every required curriculum id",
    )
    visit_state = {}

    def visit(module_id):
        state = visit_state.get(module_id, "unvisited")
        _require(
            state != "visiting",
            f"module dependency cycle detected at: {module_id}",
        )
        if state == "visited":
            return
        visit_state[module_id] = "visiting"
        for prerequisite_id in prerequisite_ids_by_module[module_id]:
            visit(prerequisite_id)
        visit_state[module_id] = "visited"

    for module_id in module_ids:
        visit(module_id)
    return module_id_set


def validate_curriculum_integrations(
    root,
    curriculum_ids,
    operator_record_ids,
):
    curriculum_root = Path(root) / "curriculum"
    validated_operator_ids = validate_operators(
        load_json(curriculum_root / "operators.json"),
        operator_record_ids,
    )
    validated_curriculum_ids = validate_crosswalk(
        load_json(curriculum_root / "crosswalk.json"),
        curriculum_ids,
    )
    return {
        "curriculumIds": validated_curriculum_ids,
        "operatorRecordIds": validated_operator_ids,
    }


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
    curriculum_records = {}
    operator_records = {}
    for curriculum_file in curriculum_files:
        curriculum_payload = load_json(curriculum_file)
        validated_curriculum_ids = validate_curriculum_dataset(
            curriculum_payload,
            source_ids,
        )
        curriculum_records.update(
            {
                record["id"]: record
                for record in curriculum_payload["records"]
                if record["id"] in validated_curriculum_ids
            }
        )
        operator_records.update(
            {
                record["id"]: record
                for record in curriculum_payload["records"]
                if record["recordType"] in OPERATOR_KINDS
            }
        )
    validate_curriculum_integrations(
        root,
        curriculum_records,
        operator_records,
    )
    required_curriculum_grades = {
        record_id: set(record["grades"])
        for record_id, record in curriculum_records.items()
        if record["recordType"] not in {"example", "operator"}
    }
    validate_module_candidates(
        load_json(root / "roadmap/module-candidates.json"),
        required_curriculum_grades,
    )
    print("phase 0 validation passed")


if __name__ == "__main__":
    main()
