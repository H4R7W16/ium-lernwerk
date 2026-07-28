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
CLAIM_STATUSES = {"draft", "working", "reviewed", "standard"}
EVIDENCE_LEVELS = {"low", "medium", "high", "normative"}


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition, message):
    if not condition:
        raise ValidationError(message)


def validate_source_register(payload):
    _require(payload.get("schemaVersion") == 1, "source register schemaVersion must be 1")
    sources = payload.get("sources")
    _require(isinstance(sources, list), "sources must be a list")
    ids = [source.get("id") for source in sources]
    _require(
        all(isinstance(source_id, str) and source_id for source_id in ids),
        "every source needs an id",
    )
    _require(len(ids) == len(set(ids)), "source ids must be unique")
    for source in sources:
        _require(
            source.get("sourceKind") in SOURCE_KINDS,
            f"invalid source kind: {source.get('id')}",
        )
        _require(
            source.get("verificationStatus") in VERIFICATION_STATUSES,
            f"invalid verification status: {source.get('id')}",
        )
        _require(
            isinstance(source.get("title"), str) and source["title"].strip(),
            f"title missing: {source.get('id')}",
        )
        _require(
            isinstance(source.get("relevance"), list) and source["relevance"],
            f"relevance missing: {source.get('id')}",
        )
    return set(ids)


def validate_claim_ledger(payload, source_ids):
    _require(payload.get("schemaVersion") == 1, "claim ledger schemaVersion must be 1")
    claims = payload.get("claims")
    _require(isinstance(claims, list), "claims must be a list")
    ids = [claim.get("id") for claim in claims]
    _require(len(ids) == len(set(ids)), "claim ids must be unique")
    for claim in claims:
        _require(
            claim.get("status") in CLAIM_STATUSES,
            f"invalid claim status: {claim.get('id')}",
        )
        _require(
            claim.get("evidenceLevel") in EVIDENCE_LEVELS,
            f"invalid evidence level: {claim.get('id')}",
        )
        _require(
            set(claim.get("sourceIds", [])) <= source_ids,
            f"unknown source id: {claim.get('id')}",
        )
        if claim.get("status") in {"reviewed", "standard"}:
            _require(claim.get("sourceIds"), f"reviewed claim has no source: {claim.get('id')}")
            _require(
                str(claim.get("limitations", "")).strip(),
                f"reviewed claim has no limitations: {claim.get('id')}",
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
