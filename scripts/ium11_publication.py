import hashlib
import json
import re


PUBLICATION_CONTRACT_ID = "IUM11-PUBLICATION-CONTRACT"
PUBLICATION_CONTRACT_VERSION = "1.0.0"
PUBLICATION_START_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:START -->"
PUBLICATION_END_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:END -->"
README_HEADING = "## IUM11-Pilotinstrument"
README_SCOPE_END_MARKER = "<!-- IUM11-PUBLICATION-SCOPE:END -->"
README_NEXT_HEADING = "## Zentrale Einstiege"
GUIDE_HEADINGS = {
    "pilot/docs/teacher-guide.md": "# Lehrkräfteanleitung zum IUM11-Pilotinstrument",
    "pilot/docs/review-guide.md": "# Reviewanleitung zum IUM11-Pilotinstrument",
}
PUBLICATION_PATHS = (
    "README.md",
    "pilot/docs/teacher-guide.md",
    "pilot/docs/review-guide.md",
)
STATEMENT_BOUNDARY = "documented-conditions-only"
FUTURE_ALLOWED_CHANGES = [
    {"field": "availabilityStatus", "value": "available"},
    {"field": "timeFeasibilityStatus", "value": "green"},
    {"field": "pilotStatus", "value": "completed"},
]
UNCHANGED_AXES = [
    {"field": "status", "value": "working"},
    {"field": "semanticCoverageStatus", "value": "partial"},
]

_TIME_MODEL_FINGERPRINT = (
    "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1"
)
_VARIANT_ID = "GRADE-7-WORKING-40"
_AVAILABILITY_CONTRACT_ID = "AVAIL-GRADE-7-WORKING-40"
_ANNUAL_PILOT_ID = "ANNUAL-7-WORKING-40"
_ANNUAL_PILOT_ASSIGNMENT_ID = "PILOT-GRADE-7-WORKING-40"
_CURRENT_AXES = {
    "status": "working",
    "availabilityStatus": "conditional",
    "timeFeasibilityStatus": "amber",
    "sequenceEvidenceStatus": "covered",
    "pilotStatus": "not-started",
    "semanticCoverageStatus": "partial",
}
_CLUSTER_IDS = (
    "CLUSTER-7-DATA-CODING",
    "CLUSTER-7-PROGRAMMING",
    "CLUSTER-7-NET-SECURITY",
    "CLUSTER-7-DATA-MEDIA-SOCIETY",
)


class IUM11PublicationError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IUM11PublicationError(message)


def _canonical_sha256(payload):
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _single_raw_variant(time_model):
    _require(isinstance(time_model, dict), "time model must be an object")
    variants = time_model.get("annualVariants")
    _require(isinstance(variants, list), "raw variant boundary requires annual variants")
    matches = [
        variant
        for variant in variants
        if isinstance(variant, dict) and variant.get("id") == _VARIANT_ID
    ]
    _require(len(matches) == 1, "raw variant boundary requires one working variant")
    return matches[0]


def _single_raw_availability(time_model):
    contracts = time_model.get("availabilityContracts")
    _require(isinstance(contracts, list), "availability boundary requires contracts")
    matches = [
        contract
        for contract in contracts
        if isinstance(contract, dict)
        and contract.get("id") == _AVAILABILITY_CONTRACT_ID
        and contract.get("variantId") == _VARIANT_ID
    ]
    _require(len(matches) == 1, "availability boundary requires one matching contract")
    return matches[0]


def _grade_7_judgement(ium10_result):
    judgements = ium10_result.get("gradeJudgements") if isinstance(ium10_result, dict) else None
    _require(isinstance(judgements, dict) and 7 in judgements, "judgement boundary requires Grade 7")
    judgement = judgements[7]
    _require(isinstance(judgement, dict), "judgement boundary requires Grade 7 object")
    return judgement


def _referenced_pilot_ids(compiled_protocol):
    clusters = compiled_protocol.get("clusters") if isinstance(compiled_protocol, dict) else None
    _require(isinstance(clusters, list) and len(clusters) == 4, "cluster boundary requires four clusters")
    pilot_ids = []
    module_ids = []
    cluster_rows = []
    for order, cluster in enumerate(clusters, start=1):
        _require(isinstance(cluster, dict) and cluster.get("order") == order, "cluster order boundary differs")
        _require(
            cluster.get("id") == _CLUSTER_IDS[order - 1],
            "cluster identity boundary differs",
        )
        modules = cluster.get("modules")
        declared_module_ids = cluster.get("moduleIds")
        _require(
            isinstance(modules, list)
            and isinstance(declared_module_ids, list)
            and len(modules) == len(declared_module_ids),
            "module boundary differs from compiled cluster",
        )
        compiled_module_ids = [
            module.get("moduleId") if isinstance(module, dict) else None
            for module in modules
        ]
        _require(compiled_module_ids == declared_module_ids, "module boundary differs from cluster binding")
        _require(
            isinstance(cluster.get("pilotAssignmentId"), str)
            and isinstance(cluster.get("integrationContractId"), str)
            and type(cluster.get("budgetUnits")) is int
            and type(cluster.get("fallbackDeltaUnits")) is int,
            "cluster boundary has invalid values",
        )
        pilot_ids.append(cluster["pilotAssignmentId"])
        pilot_ids.extend(
            module.get("pilotAssignmentId") if isinstance(module, dict) else None
            for module in modules
        )
        module_ids.extend(compiled_module_ids)
        cluster_rows.append({
            "id": cluster.get("id"),
            "order": cluster["order"],
            "budgetUnits": cluster["budgetUnits"],
            "fallbackDeltaUnits": cluster["fallbackDeltaUnits"],
        })
    _require(
        all(isinstance(value, str) and value for value in module_ids)
        and len(module_ids) == 10
        and len(set(module_ids)) == 10,
        "module boundary requires ten unique cluster modules",
    )
    annual_pilot = compiled_protocol.get("annualPilot")
    _require(isinstance(annual_pilot, dict), "annual pilot boundary requires an object")
    _require(
        annual_pilot.get("id") == _ANNUAL_PILOT_ID
        and annual_pilot.get("variantId") == _VARIANT_ID
        and annual_pilot.get("clusterIds") == list(_CLUSTER_IDS)
        and annual_pilot.get("budgetUnits") == 40
        and annual_pilot.get("pilotAssignmentId") == _ANNUAL_PILOT_ASSIGNMENT_ID,
        "annual pilot boundary differs from Working-40 contract",
    )
    annual_pilot_id = annual_pilot.get("pilotAssignmentId")
    _require(isinstance(annual_pilot_id, str), "annual pilot boundary requires assignment")
    pilot_ids.append(annual_pilot_id)
    _require(len(pilot_ids) == 15 and len(set(pilot_ids)) == 15, "pilot boundary requires fifteen assignments")
    return pilot_ids, module_ids, cluster_rows


def compile_publication_contract(compiled_protocol, time_model, ium10_result):
    """Compile the closed IUM11 publication contract from validated inputs."""
    _require(isinstance(compiled_protocol, dict), "protocol boundary requires an object")
    _require(isinstance(ium10_result, dict), "IUM10 boundary requires an object")

    raw_variant = _single_raw_variant(time_model)
    raw_availability = _single_raw_availability(time_model)
    _require(
        _canonical_sha256(time_model) == _TIME_MODEL_FINGERPRINT,
        "fingerprint boundary differs from approved time model",
    )
    _require(
        compiled_protocol.get("timeModelFingerprint") == _TIME_MODEL_FINGERPRINT,
        "protocol fingerprint boundary differs from approved time model",
    )
    _require(
        compiled_protocol.get("timeModelFingerprintAlgorithm")
        == "sha256-canonical-json-v1",
        "fingerprint algorithm boundary differs",
    )
    _require(
        compiled_protocol.get("protocolVersion") == "1.0.0"
        and compiled_protocol.get("toolVersion") == "1.0.0",
        "source version boundary differs",
    )

    variants = ium10_result.get("annualVariants")
    _require(isinstance(variants, dict), "IUM10 variant boundary requires index")
    indexed_variant = variants.get(_VARIANT_ID)
    _require(isinstance(indexed_variant, dict), "IUM10 variant boundary requires working variant")
    raw_variant_without_allocations = {
        key: value for key, value in raw_variant.items() if key != "allocations"
    }
    indexed_variant_without_allocations = {
        key: value for key, value in indexed_variant.items() if key != "allocations"
    }
    _require(
        raw_variant_without_allocations == indexed_variant_without_allocations,
        "variant boundary differs between raw and IUM10",
    )
    _require(
        raw_variant.get("availabilityContractId") == _AVAILABILITY_CONTRACT_ID,
        "availability boundary differs from variant",
    )
    availability = ium10_result.get("availabilityContracts")
    _require(isinstance(availability, dict), "availability boundary requires IUM10 index")
    indexed_availability = availability.get(_AVAILABILITY_CONTRACT_ID)
    _require(isinstance(indexed_availability, dict), "availability boundary requires indexed contract")
    _require(raw_availability == indexed_availability, "availability boundary differs between raw and IUM10")

    judgement = _grade_7_judgement(ium10_result)
    pilot_ids, module_ids, cluster_rows = _referenced_pilot_ids(compiled_protocol)
    allocations = raw_variant.get("allocations")
    _require(isinstance(allocations, list), "module boundary requires allocations")
    _require(
        allocations == indexed_variant.get("allocations"),
        "module allocation boundary differs between raw and IUM10",
    )
    allocation_module_ids = [
        allocation.get("moduleId") if isinstance(allocation, dict) else None
        for allocation in allocations
    ]
    _require(
        allocation_module_ids == module_ids
        and len(allocation_module_ids) == 10
        and len(set(allocation_module_ids)) == 10,
        "module boundary differs from variant allocations",
    )
    allocation_units_by_module = {
        allocation["moduleId"]: allocation.get("units")
        for allocation in allocations
        if isinstance(allocation, dict)
    }
    _require(
        all(type(units) is int for units in allocation_units_by_module.values()),
        "module allocation boundary has invalid units",
    )
    for cluster in compiled_protocol["clusters"]:
        _require(
            cluster["budgetUnits"]
            == sum(allocation_units_by_module[module_id] for module_id in cluster["moduleIds"]),
            "cluster budget boundary differs from raw allocations",
        )
    _require(
        sum(allocation.get("units", 0) for allocation in allocations) == 40,
        "module allocation boundary differs from target units",
    )
    _require(
        raw_variant.get("targetUnits") == 40
        and compiled_protocol.get("annualPilot", {}).get("budgetUnits") == 40
        and sum(row["budgetUnits"] for row in cluster_rows) == 40,
        "core path boundary differs from 40 units",
    )
    _require(
        raw_variant.get("integrationContractIds")
        == [cluster.get("integrationContractId") for cluster in compiled_protocol["clusters"]],
        "cluster integration boundary differs from variant",
    )
    _require(
        raw_availability.get("fallbackDeltaUnitsByIntegrationContractId")
        == {
            cluster["integrationContractId"]: cluster["fallbackDeltaUnits"]
            for cluster in compiled_protocol["clusters"]
        },
        "cluster fallback boundary differs from availability",
    )

    pilot_assignments = ium10_result.get("pilotAssignments")
    _require(isinstance(pilot_assignments, dict), "pilot boundary requires IUM10 index")
    _require(
        all(
            isinstance(pilot_assignments.get(pilot_id), dict)
            and pilot_assignments[pilot_id].get("personalData") == "prohibited"
            for pilot_id in pilot_ids
        ),
        "privacy boundary requires prohibited personal data",
    )
    annual_assignment = pilot_assignments.get(_ANNUAL_PILOT_ASSIGNMENT_ID)
    _require(
        isinstance(annual_assignment, dict)
        and annual_assignment.get("scopeType") == "annual-variant"
        and annual_assignment.get("scopeIds") == [_VARIANT_ID]
        and annual_assignment.get("contractIds") == [_AVAILABILITY_CONTRACT_ID],
        "annual pilot assignment boundary differs from Working-40 contract",
    )
    _require(
        compiled_protocol.get("minimumLearnerResponses") == 10,
        "privacy boundary requires ten learner responses",
    )
    _require(
        compiled_protocol.get("allowedRecommendation")
        == "eligible-for-working-availability-review",
        "recommendation boundary differs",
    )
    _require(
        compiled_protocol.get("forbiddenRecommendations") == ["reviewed", "standard"],
        "maturity boundary differs",
    )
    _require(
        "flexible-module-substitution"
        in raw_availability.get("forbiddenCompensations", []),
        "preservation boundary requires flexible-module-substitution prohibition",
    )

    gates = raw_availability.get("gates")
    _require(
        isinstance(gates, dict)
        and gates
        and all(isinstance(gate, dict) and gate.get("status") == "not-started" for gate in gates.values()),
        "availability boundary requires not-started gates",
    )
    for axis, expected in _CURRENT_AXES.items():
        if axis in ("status", "availabilityStatus"):
            _require(raw_variant.get(axis) == expected, f"{axis} boundary differs from raw variant")
            _require(indexed_variant.get(axis) == expected, f"{axis} boundary differs from IUM10 variant")
            if axis == "availabilityStatus":
                _require(
                    judgement.get(axis) == expected,
                    f"{axis} boundary differs from Grade 7 judgement",
                )
        elif axis == "status":
            _require(compiled_protocol.get(axis) == expected, "status boundary differs from protocol")
        else:
            _require(judgement.get(axis) == expected, f"{axis} boundary differs from Grade 7 judgement")
    _require(compiled_protocol.get("status") == "working", "status boundary differs from protocol")

    return {
        "schemaVersion": 1,
        "id": PUBLICATION_CONTRACT_ID,
        "contractVersion": PUBLICATION_CONTRACT_VERSION,
        "sourceBindings": {
            "protocolPath": "pilot/pilot-protocol.json",
            "timeModelPath": "roadmap/time-model.json",
            "protocolVersion": compiled_protocol.get("protocolVersion"),
            "toolVersion": compiled_protocol.get("toolVersion"),
            "timeModelFingerprintAlgorithm": compiled_protocol.get("timeModelFingerprintAlgorithm"),
            "timeModelFingerprint": compiled_protocol.get("timeModelFingerprint"),
        },
        "corePath": {
            "variantId": _VARIANT_ID,
            "targetUnits": 40,
            "clusterCount": 4,
            "moduleCount": 10,
            "pilotStageCount": 5,
            "clusters": cluster_rows,
        },
        "privacyBoundary": {
            "minimumLearnerResponses": compiled_protocol["minimumLearnerResponses"],
            "personalDataAllowed": False,
            "realPackagesInRepositoryAllowed": False,
        },
        "currentAxes": dict(_CURRENT_AXES),
        "statementBoundary": STATEMENT_BOUNDARY,
        "allowedRecommendation": compiled_protocol["allowedRecommendation"],
        "forbiddenMaturityValues": list(compiled_protocol["forbiddenRecommendations"]),
        "futureDecisionBoundary": {
            "requiresCommissionerDecision": True,
            "allowedChanges": [dict(change) for change in FUTURE_ALLOWED_CHANGES],
            "unchangedAxes": [dict(axis) for axis in UNCHANGED_AXES],
            "secondIndependentAnnualRunRequiredForMaturity": True,
        },
        "preservationBoundary": {
            "flexibleModulesOutsideCorePreserved": True,
            "flexibleModuleSubstitution": "forbidden",
        },
        "realPilotCompleted": False,
        "syntheticValidationOnly": True,
    }


_AXIS_ASSIGNMENT_PATTERN = re.compile(
    r"(?:(?P<axis_quote>[\"'`])(?:status|availabilityStatus|"
    r"timeFeasibilityStatus|sequenceEvidenceStatus|pilotStatus|"
    r"semanticCoverageStatus)(?P=axis_quote)|(?P<bare_axis>status|"
    r"availabilityStatus|timeFeasibilityStatus|sequenceEvidenceStatus|"
    r"pilotStatus|semanticCoverageStatus)(?!\w))\s*[:=]",
)


def _is_python_identifier_continuation(character):
    return bool(character) and ("a" + character).isidentifier()


RESERVED_OUTSIDE_BLOCK_PATTERNS = (
    re.compile(r"[0-9]+\.[0-9]+\.[0-9]+"),
    re.compile(r"\beligible-for-[a-z0-9-]+\b", re.IGNORECASE),
    _AXIS_ASSIGNMENT_PATTERN,
    re.compile(
        r"\b(?:working|available|unavailable|reviewed|standard|conditional|"
        r"green|amber|red|covered|not-started|partial|completed|"
        r"documented-conditions-only)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bGRADE-7-WORKING-40\b", re.IGNORECASE),
    re.compile(r"\b[0-9]+\s*UE\b", re.IGNORECASE),
    re.compile(r"\b[0-9]+\s*(?:Cluster|Module?|Pilotstufen?)\b", re.IGNORECASE),
    re.compile(r"\bPrivacy-?Schwelle\s*:?[ ]*[0-9]+\b", re.IGNORECASE),
)


def render_publication_contract_json(contract):
    return (
        json.dumps(contract, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    ).encode("utf-8")


def _markdown_value(value):
    if value is True:
        text = "true"
    elif value is False:
        text = "false"
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _facts(*pairs):
    return "; ".join(f"{field}: {_markdown_value(value)}" for field, value in pairs)


def render_publication_markdown_block(contract):
    """Render the stable, human-readable projection of the publication contract."""
    source = contract["sourceBindings"]
    core = contract["corePath"]
    privacy = contract["privacyBoundary"]
    axes = contract["currentAxes"]
    future = contract["futureDecisionBoundary"]
    preservation = contract["preservationBoundary"]
    rows = [
        ("Vertragsbindung", _facts(
            ("schemaVersion", contract["schemaVersion"]),
            ("id", contract["id"]),
            ("contractVersion", contract["contractVersion"]),
            *((field, source[field]) for field in (
                "protocolPath", "timeModelPath", "protocolVersion", "toolVersion",
                "timeModelFingerprintAlgorithm", "timeModelFingerprint",
            )),
        )),
        ("Kernpfad", _facts(*((field, core[field]) for field in (
            "variantId", "targetUnits", "clusterCount", "moduleCount", "pilotStageCount",
        )))),
        ("Clusterbudgets und Rückfälle", "; ".join(_facts(*((field, cluster[field]) for field in (
            "id", "order", "budgetUnits", "fallbackDeltaUnits",
        ))) for cluster in core["clusters"])),
        ("Privacygrenze", _facts(*((field, privacy[field]) for field in (
            "minimumLearnerResponses", "personalDataAllowed", "realPackagesInRepositoryAllowed",
        )))),
        ("Aktuelle Urteilachsen", _facts(*((field, axes[field]) for field in (
            "status", "availabilityStatus", "timeFeasibilityStatus", "sequenceEvidenceStatus",
            "pilotStatus", "semanticCoverageStatus",
        )))),
        ("Aussagegrenze", _facts(("statementBoundary", contract["statementBoundary"]))),
        ("Zulässige Empfehlung", _facts(("allowedRecommendation", contract["allowedRecommendation"]))),
        ("Gesperrte Reifegrade", "; ".join(
            _facts(("forbiddenMaturityValues", value))
            for value in contract["forbiddenMaturityValues"]
        )),
        ("Spätere Auftraggeberentscheidung", "; ".join((
            _facts(
                ("requiresCommissionerDecision", future["requiresCommissionerDecision"]),
                ("secondIndependentAnnualRunRequiredForMaturity", future["secondIndependentAnnualRunRequiredForMaturity"]),
            ),
            *(
                _facts(("allowedChanges", f"{item['field']}: {item['value']}"))
                for item in future["allowedChanges"]
            ),
            *(
                _facts(("unchangedAxes", f"{item['field']}: {item['value']}"))
                for item in future["unchangedAxes"]
            ),
        ))),
        ("Reale Pilotierung", _facts(
            ("realPilotCompleted", contract["realPilotCompleted"]),
            ("syntheticValidationOnly", contract["syntheticValidationOnly"]),
        )),
        ("Flexible Module", _facts(
            ("flexibleModulesOutsideCorePreserved", preservation["flexibleModulesOutsideCorePreserved"]),
            ("flexibleModuleSubstitution", preservation["flexibleModuleSubstitution"]),
        ) + "; Flexible Vertiefungs-, Transfer- und Projektmodule bleiben sichtbar erhalten."),
    ]
    table_rows = ["| Bereich | Verbindliche Fakten |", "| --- | --- |"]
    table_rows.extend(f"| {label} | {facts} |" for label, facts in rows)
    return "\n".join((
        PUBLICATION_START_MARKER,
        "<!-- Generiert aus Pilotprotokoll und Zeitmodell; nicht manuell bearbeiten. -->",
        *table_rows,
        PUBLICATION_END_MARKER,
    ))


def extract_publication_block(text):
    _require(text.count(PUBLICATION_START_MARKER) == 1, "publication start marker must occur once")
    _require(text.count(PUBLICATION_END_MARKER) == 1, "publication end marker must occur once")
    start = text.index(PUBLICATION_START_MARKER)
    end = text.index(PUBLICATION_END_MARKER)
    _require(start < end, "publication markers are out of order")
    return text[start:end + len(PUBLICATION_END_MARKER)]


def replace_publication_block(text, block):
    current = extract_publication_block(text)
    _require(block.startswith(PUBLICATION_START_MARKER), "rendered block start differs")
    _require(block.endswith(PUBLICATION_END_MARKER), "rendered block end differs")
    return text.replace(current, block, 1)


def _exact_line_count(text, line):
    return text.split("\n").count(line)


def _publication_layout(relative_path, text):
    normalized_path = str(relative_path).replace("\\", "/")
    _require("\r" not in text, f"{relative_path}: publication text must use LF")
    block = extract_publication_block(text)
    block_start = text.index(block)
    block_end = block_start + len(block)

    if normalized_path == "README.md":
        _require(
            _exact_line_count(text, README_HEADING) == 1,
            "README.md: IUM11 section heading must occur once",
        )
        _require(
            text.count(README_SCOPE_END_MARKER) == 1,
            "README.md: IUM11 scope end marker must occur once",
        )
        _require(
            f"{README_HEADING}\n\n{block}" in text,
            "README.md: publication block must immediately follow IUM11 heading",
        )
        scope_end = text.index(README_SCOPE_END_MARKER)
        _require(
            block_end < scope_end,
            "README.md: IUM11 scope end marker must follow publication block",
        )
        _require(
            text[scope_end - 2:scope_end] == "\n\n",
            "README.md: IUM11 scope end marker must follow one blank line",
        )
        _require(
            text.startswith(
                f"{README_SCOPE_END_MARKER}\n\n{README_NEXT_HEADING}",
                scope_end,
            ),
            "README.md: IUM11 scope end marker must precede central entries",
        )
        return block, text[block_end:scope_end]

    heading = GUIDE_HEADINGS.get(normalized_path)
    _require(heading is not None, f"unsupported publication path: {relative_path}")
    _require(
        text.startswith(f"{heading}\n\n{block}"),
        f"{relative_path}: publication block must immediately follow canonical H1",
    )
    return block, text[:block_start] + text[block_end:]


def validate_publication_embedding(relative_path, text):
    """Require the generated block in its exact source-controlled anchor."""
    _publication_layout(relative_path, text)


def validate_publication_text_boundary(relative_path, text):
    """Reject lexical publication declarations outside the generated IUM11 block."""
    _, inspected = _publication_layout(relative_path, text)
    for pattern in RESERVED_OUTSIDE_BLOCK_PATTERNS:
        for match in pattern.finditer(inspected):
            if pattern is _AXIS_ASSIGNMENT_PATTERN and match.group("bare_axis"):
                preceding = inspected[match.start() - 1] if match.start() else ""
                if _is_python_identifier_continuation(preceding):
                    continue
            raise IUM11PublicationError(
                f"{relative_path}: reserved publication form {match.group(0)!r}"
            )
