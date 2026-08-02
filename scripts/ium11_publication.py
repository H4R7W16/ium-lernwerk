import hashlib
import json
import re
from html.parser import HTMLParser


PUBLICATION_CONTRACT_ID = "IUM11-PUBLICATION-CONTRACT"
PUBLICATION_CONTRACT_VERSION = "1.0.0"
PUBLICATION_START_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:START -->"
PUBLICATION_END_MARKER = "<!-- IUM11-PUBLICATION-CONTRACT:END -->"
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


def _fence_opening(body):
    opening = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", body)
    if opening is None:
        return None
    token = opening.group(1)
    if token.startswith("`") and "`" in body[opening.end():]:
        return None
    return token


def _fenced_code_ranges(text):
    ranges = []
    active = None
    offset = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if active is None:
            token = _fence_opening(body)
            if token is not None:
                active = (token[0], len(token), offset)
        else:
            character, minimum_length, start = active
            closing = re.fullmatch(
                rf"[ ]{{0,3}}{re.escape(character)}{{{minimum_length},}}[ \t]*",
                body,
            )
            if closing:
                ranges.append((start, offset + len(line)))
                active = None
        offset += len(line)
    if active is not None:
        ranges.append((active[2], len(text)))
    return ranges


def _leading_indentation_width(body):
    width = 0
    for character in body:
        if character == " ":
            width += 1
        elif character == "\t":
            width += 4 - (width % 4)
        else:
            break
    return width


def _indented_code_ranges(text, fenced_ranges):
    ranges = []
    active_start = None
    previous_blank = True
    offset = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        blank = not body.strip(" \t")
        indentation = _leading_indentation_width(body)
        in_fence = _position_in_ranges(offset, fenced_ranges)

        if active_start is not None and not blank and indentation < 4:
            ranges.append((active_start, offset))
            active_start = None

        if (
            active_start is None
            and not in_fence
            and not blank
            and indentation >= 4
            and previous_blank
        ):
            active_start = offset

        if in_fence:
            previous_blank = False
        elif active_start is None:
            previous_blank = blank
        offset += len(line)

    if active_start is not None:
        ranges.append((active_start, len(text)))
    return ranges


def _position_in_ranges(position, ranges):
    return any(start <= position < end for start, end in ranges)


def _mask_ranges(text, ranges):
    masked = list(text)
    for start, end in ranges:
        for index in range(start, end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    return "".join(masked)


def _html_comment_ranges(text, fenced_ranges):
    searchable = _mask_ranges(text, fenced_ranges)
    ranges = []
    cursor = 0
    while True:
        start = searchable.find("<!--", cursor)
        if start < 0:
            break
        closing = searchable.find("-->", start + 4)
        if closing < 0:
            ranges.append((start, len(text)))
            break
        end = closing + 3
        ranges.append((start, end))
        cursor = end
    return ranges


_HTML_VOID_TAGS = frozenset({
    "area",
    "base",
    "basefont",
    "bgsound",
    "br",
    "col",
    "command",
    "embed",
    "frame",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
})


class _RawHtmlContainerParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.line_starts = [0]
        self.line_starts.extend(
            match.end() for match in re.finditer("\n", source)
        )
        self.open_containers = []
        self.ranges = []

    def _offset(self):
        line, column = self.getpos()
        return self.line_starts[line - 1] + column

    def _record_start_tag_token(self):
        start = self._offset()
        token = self.get_starttag_text()
        end = start + len(token) if token is not None else start
        self.ranges.append((start, end))
        return start

    def handle_starttag(self, tag, attrs):
        normalized = tag.lower()
        opening_start = self._record_start_tag_token()
        if normalized not in _HTML_VOID_TAGS:
            self.open_containers.append((normalized, opening_start))

    def handle_startendtag(self, tag, attrs):
        normalized = tag.lower()
        opening_start = self._record_start_tag_token()
        if normalized not in _HTML_VOID_TAGS:
            self.open_containers.append((normalized, opening_start))

    def handle_endtag(self, tag):
        normalized = tag.lower()
        closing_start = self._offset()
        closing_end = self.source.find(">", closing_start)
        closing_end = len(self.source) if closing_end < 0 else closing_end + 1
        self.ranges.append((closing_start, closing_end))
        matching_index = next(
            (
                index
                for index in range(len(self.open_containers) - 1, -1, -1)
                if self.open_containers[index][0] == normalized
            ),
            None,
        )
        if matching_index is None:
            return
        for _, opening_start in self.open_containers[matching_index:]:
            self.ranges.append((opening_start, closing_end))
        del self.open_containers[matching_index:]

    def finish(self):
        self.close()
        self.ranges.extend(
            (opening_start, len(self.source))
            for _, opening_start in self.open_containers
        )
        return sorted(self.ranges)


def _raw_html_container_ranges(text, code_ranges, comment_ranges):
    searchable = _mask_ranges(text, (*code_ranges, *comment_ranges))
    parser = _RawHtmlContainerParser(searchable)
    parser.feed(searchable)
    return parser.finish()


def _markdown_visibility_ranges(text):
    fenced_ranges = _fenced_code_ranges(text)
    indented_ranges = _indented_code_ranges(text, fenced_ranges)
    code_ranges = (*fenced_ranges, *indented_ranges)
    comment_ranges = _html_comment_ranges(text, code_ranges)
    raw_html_ranges = _raw_html_container_ranges(
        text,
        code_ranges,
        comment_ranges,
    )
    return fenced_ranges, indented_ranges, comment_ranges, raw_html_ranges


def _position_enclosed_by_comment(position, comment_ranges):
    return any(start < position < end for start, end in comment_ranges)


def _atx_heading_level(body):
    match = re.match(r"^[ ]{0,3}(#{1,6})(?:[ \t]+|$)", body)
    return len(match.group(1)) if match else None


def _is_thematic_break(body):
    return bool(re.fullmatch(
        r"[ ]{0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})",
        body,
    ))


def _is_html_block_start(body):
    return bool(re.match(
        r"^[ ]{0,3}(?:</?[A-Za-z][A-Za-z0-9-]*(?:[ \t/>]|$)|"
        r"<!--|<\?|<![A-Z]|<!\[CDATA\[)",
        body,
        re.IGNORECASE,
    ))


def _is_setext_paragraph_text(body):
    stripped = body.lstrip(" ")
    indentation = len(body) - len(stripped)
    if (
        not stripped
        or indentation > 3
        or stripped.startswith("\t")
        or _fence_opening(body) is not None
        or _atx_heading_level(body) is not None
        or _is_thematic_break(body)
        or _is_html_block_start(body)
        or re.match(r"^[ ]{0,3}>", body)
        or re.match(
            r"^[ ]{0,3}(?:[-+*](?:[ \t]+|$)|[0-9]{1,9}[.)](?:[ \t]+|$))",
            body,
        )
    ):
        return False
    return True


def _visible_heading_spans(text, invisible_ranges):
    lines = []
    offset = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        lines.append((offset, offset + len(line), body))
        offset += len(line)

    headings = []
    for index, (line_start, line_end, body) in enumerate(lines):
        atx_match = re.match(r"^[ ]{0,3}(#{1,6})(?:[ \t]+|$)", body)
        if atx_match:
            marker_position = line_start + atx_match.start(1)
            if not _position_in_ranges(marker_position, invisible_ranges):
                headings.append((len(atx_match.group(1)), line_start, line_end))

        setext_match = re.fullmatch(r"[ ]{0,3}(=+|-+)[ \t]*", body)
        if not setext_match or index == 0:
            continue
        previous_start, _, previous_body = lines[index - 1]
        if not _is_setext_paragraph_text(previous_body):
            continue
        stripped_previous = previous_body.lstrip(" ")
        previous_indentation = len(previous_body) - len(stripped_previous)
        text_position = previous_start + previous_indentation
        underline_position = line_start + setext_match.start(1)
        if (
            _position_in_ranges(text_position, invisible_ranges)
            or _position_in_ranges(underline_position, invisible_ranges)
        ):
            continue
        level = 1 if setext_match.group(1).startswith("=") else 2
        headings.append((level, previous_start, line_end))
    return headings


def _readme_ium11_section_span(text, invisible_ranges=None):
    headings = list(re.finditer(
        r"^## IUM11-Pilotinstrument[ \t]*(?=\r?$)",
        text,
        re.MULTILINE,
    ))
    _require(len(headings) == 1, "README IUM11 section must occur once")
    if invisible_ranges is None:
        visibility_ranges = _markdown_visibility_ranges(text)
        invisible_ranges = tuple(
            span
            for ranges in visibility_ranges
            for span in ranges
        )
    heading = headings[0]
    _require(
        not _position_in_ranges(heading.start(), invisible_ranges),
        "README.md: IUM11 section heading must be visible",
    )
    start = heading.end()
    next_headings = [
        heading_start
        for level, heading_start, _ in _visible_heading_spans(
            text,
            invisible_ranges,
        )
        if level == 2 and heading_start >= start
    ]
    end = min(next_headings) if next_headings else len(text)
    return heading.start(), start, end


def _readme_ium11_section(text):
    _, start, end = _readme_ium11_section_span(text)
    return text[start:end]


def _visible_h1_spans(text, invisible_ranges):
    return [
        (start, end)
        for level, start, end in _visible_heading_spans(text, invisible_ranges)
        if level == 1
    ]


def validate_publication_embedding(relative_path, text):
    """Require the generated block in its visible canonical Markdown anchor."""
    block = extract_publication_block(text)
    block_start = text.index(block)
    block_end = block_start + len(block)
    end_marker_start = block_end - len(PUBLICATION_END_MARKER)
    (
        fenced_ranges,
        indented_ranges,
        comment_ranges,
        raw_html_ranges,
    ) = _markdown_visibility_ranges(text)
    invisible_ranges = (
        *fenced_ranges,
        *indented_ranges,
        *comment_ranges,
        *raw_html_ranges,
    )
    _require(
        not _position_in_ranges(block_start, fenced_ranges)
        and not _position_in_ranges(end_marker_start, fenced_ranges),
        f"{relative_path}: publication marker must not be inside a code fence",
    )
    _require(
        not _position_in_ranges(block_start, indented_ranges)
        and not _position_in_ranges(end_marker_start, indented_ranges),
        f"{relative_path}: publication marker must not be inside indented code",
    )
    _require(
        not _position_enclosed_by_comment(block_start, comment_ranges)
        and not _position_enclosed_by_comment(end_marker_start, comment_ranges),
        f"{relative_path}: publication marker must not be inside an HTML comment",
    )
    _require(
        not _position_in_ranges(block_start, raw_html_ranges)
        and not _position_in_ranges(end_marker_start, raw_html_ranges),
        f"{relative_path}: publication marker must not be inside raw HTML",
    )

    normalized_path = str(relative_path).replace("\\", "/")
    if normalized_path == "README.md":
        _, section_start, section_end = _readme_ium11_section_span(
            text,
            invisible_ranges,
        )
        _require(
            section_start <= block_start and block_end <= section_end,
            "README.md: publication block must be inside the IUM11 section",
        )
        return

    headings = _visible_h1_spans(text, invisible_ranges)
    _require(len(headings) == 1, f"{relative_path}: guide must contain exactly one H1")
    _, heading_end = headings[0]
    _require(
        heading_end <= block_start and not text[heading_end:block_start].strip(),
        f"{relative_path}: publication block must be first content after H1",
    )


def validate_publication_text_boundary(relative_path, text):
    """Reject lexical publication declarations outside the generated IUM11 block."""
    validate_publication_embedding(relative_path, text)
    block = extract_publication_block(text)
    remaining = text.replace(block, "", 1)
    inspected = (
        _readme_ium11_section(remaining)
        if str(relative_path).replace("\\", "/") == "README.md"
        else remaining
    )
    for pattern in RESERVED_OUTSIDE_BLOCK_PATTERNS:
        for match in pattern.finditer(inspected):
            if pattern is _AXIS_ASSIGNMENT_PATTERN and match.group("bare_axis"):
                preceding = inspected[match.start() - 1] if match.start() else ""
                if _is_python_identifier_continuation(preceding):
                    continue
            raise IUM11PublicationError(
                f"{relative_path}: reserved publication form {match.group(0)!r}"
            )
