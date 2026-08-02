import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.ium11_publication import (
    IUM11PublicationError,
    PUBLICATION_END_MARKER,
    PUBLICATION_PATHS,
    PUBLICATION_START_MARKER,
    compile_publication_contract,
    extract_publication_block,
    render_publication_contract_json,
    render_publication_markdown_block,
    replace_publication_block,
    validate_publication_text_boundary,
)
from scripts.build_ium11_publication_contract import (
    CONTRACT_PATH,
    build_publication_contract,
    compile_repository_publication_contract,
    expected_publication_outputs,
)
from scripts.validate_ium10 import validate_ium10_repository
from scripts.validate_ium11 import validate_pilot_protocol

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class IUM11PublicationCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.time_model = load_json(ROOT / "roadmap/time-model.json")
        cls.ium10_result = validate_ium10_repository(ROOT)
        cls.protocol = validate_pilot_protocol(
            load_json(ROOT / "pilot/pilot-protocol.json"),
            cls.time_model,
        )

    def compile(self, protocol=None, time_model=None, ium10_result=None):
        return compile_publication_contract(
            copy.deepcopy(protocol if protocol is not None else self.protocol),
            copy.deepcopy(time_model if time_model is not None else self.time_model),
            copy.deepcopy(
                ium10_result if ium10_result is not None else self.ium10_result
            ),
        )

    def test_compiles_exact_closed_contract(self):
        contract = self.compile()
        self.assertEqual(set(contract), {
            "schemaVersion", "id", "contractVersion", "sourceBindings",
            "corePath", "privacyBoundary", "currentAxes",
            "statementBoundary", "allowedRecommendation",
            "forbiddenMaturityValues", "futureDecisionBoundary",
            "preservationBoundary", "realPilotCompleted",
            "syntheticValidationOnly",
        })
        self.assertEqual(contract["schemaVersion"], 1)
        self.assertEqual(contract["id"], "IUM11-PUBLICATION-CONTRACT")
        self.assertEqual(contract["contractVersion"], "1.0.0")
        self.assertEqual(contract["sourceBindings"], {
            "protocolPath": "pilot/pilot-protocol.json",
            "timeModelPath": "roadmap/time-model.json",
            "protocolVersion": "1.0.0",
            "toolVersion": "1.0.0",
            "timeModelFingerprintAlgorithm": "sha256-canonical-json-v1",
            "timeModelFingerprint": "873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1",
        })
        self.assertEqual(contract["currentAxes"], {
            "status": "working",
            "availabilityStatus": "conditional",
            "timeFeasibilityStatus": "amber",
            "sequenceEvidenceStatus": "covered",
            "pilotStatus": "not-started",
            "semanticCoverageStatus": "partial",
        })

    def test_compiles_exact_core_and_governance_boundaries(self):
        contract = self.compile()
        self.assertEqual(contract["corePath"]["variantId"], "GRADE-7-WORKING-40")
        self.assertEqual(contract["corePath"]["targetUnits"], 40)
        self.assertEqual(contract["corePath"]["clusterCount"], 4)
        self.assertEqual(contract["corePath"]["moduleCount"], 10)
        self.assertEqual(contract["corePath"]["pilotStageCount"], 5)
        self.assertEqual(
            [
                (item["id"], item["order"], item["budgetUnits"], item["fallbackDeltaUnits"])
                for item in contract["corePath"]["clusters"]
            ],
            [
                ("CLUSTER-7-DATA-CODING", 1, 8, 3),
                ("CLUSTER-7-PROGRAMMING", 2, 11, 2),
                ("CLUSTER-7-NET-SECURITY", 3, 11, 3),
                ("CLUSTER-7-DATA-MEDIA-SOCIETY", 4, 10, 6),
            ],
        )
        self.assertEqual(contract["privacyBoundary"], {
            "minimumLearnerResponses": 10,
            "personalDataAllowed": False,
            "realPackagesInRepositoryAllowed": False,
        })
        self.assertEqual(contract["statementBoundary"], "documented-conditions-only")
        self.assertEqual(
            contract["allowedRecommendation"],
            "eligible-for-working-availability-review",
        )
        self.assertEqual(contract["forbiddenMaturityValues"], ["reviewed", "standard"])
        self.assertFalse(contract["realPilotCompleted"])
        self.assertTrue(contract["syntheticValidationOnly"])
        self.assertEqual(contract["preservationBoundary"], {
            "flexibleModulesOutsideCorePreserved": True,
            "flexibleModuleSubstitution": "forbidden",
        })
        self.assertEqual(contract["futureDecisionBoundary"], {
            "requiresCommissionerDecision": True,
            "allowedChanges": [
                {"field": "availabilityStatus", "value": "available"},
                {"field": "timeFeasibilityStatus", "value": "green"},
                {"field": "pilotStatus", "value": "completed"},
            ],
            "unchangedAxes": [
                {"field": "status", "value": "working"},
                {"field": "semanticCoverageStatus", "value": "partial"},
            ],
            "secondIndependentAnnualRunRequiredForMaturity": True,
        })

    def test_emits_exact_nested_field_sets(self):
        contract = self.compile()
        self.assertEqual(set(contract["sourceBindings"]), {
            "protocolPath", "timeModelPath", "protocolVersion", "toolVersion",
            "timeModelFingerprintAlgorithm", "timeModelFingerprint",
        })
        self.assertEqual(set(contract["corePath"]), {
            "variantId", "targetUnits", "clusterCount", "moduleCount",
            "pilotStageCount", "clusters",
        })
        for cluster in contract["corePath"]["clusters"]:
            self.assertEqual(set(cluster), {
                "id", "order", "budgetUnits", "fallbackDeltaUnits",
            })
        self.assertEqual(set(contract["privacyBoundary"]), {
            "minimumLearnerResponses", "personalDataAllowed",
            "realPackagesInRepositoryAllowed",
        })
        self.assertEqual(set(contract["currentAxes"]), {
            "status", "availabilityStatus", "timeFeasibilityStatus",
            "sequenceEvidenceStatus", "pilotStatus", "semanticCoverageStatus",
        })
        self.assertEqual(set(contract["futureDecisionBoundary"]), {
            "requiresCommissionerDecision", "allowedChanges", "unchangedAxes",
            "secondIndependentAnnualRunRequiredForMaturity",
        })
        for row in (
            contract["futureDecisionBoundary"]["allowedChanges"]
            + contract["futureDecisionBoundary"]["unchangedAxes"]
        ):
            self.assertEqual(set(row), {"field", "value"})
        self.assertEqual(set(contract["preservationBoundary"]), {
            "flexibleModulesOutsideCorePreserved", "flexibleModuleSubstitution",
        })

    def test_rejects_source_and_ium10_drift_without_mutating_inputs(self):
        cases = []

        protocol = copy.deepcopy(self.protocol)
        protocol["timeModelFingerprint"] = "0" * 64
        cases.append((protocol, self.time_model, self.ium10_result, "fingerprint"))

        ium10_result = copy.deepcopy(self.ium10_result)
        ium10_result["gradeJudgements"][7]["pilotStatus"] = "completed"
        cases.append((self.protocol, self.time_model, ium10_result, "pilotStatus"))

        ium10_result = copy.deepcopy(self.ium10_result)
        del ium10_result["annualVariants"]["GRADE-7-WORKING-40"]["allocations"][0]
        cases.append((self.protocol, self.time_model, ium10_result, "module"))

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][1]["order"] = 1
        cases.append((protocol, self.time_model, self.ium10_result, "cluster"))

        for protocol, time_model, ium10_result, message in cases:
            with self.subTest(message=message):
                before = copy.deepcopy([protocol, time_model, ium10_result])
                with self.assertRaisesRegex(IUM11PublicationError, message):
                    compile_publication_contract(protocol, time_model, ium10_result)
                after = [protocol, time_model, ium10_result]
                self.assertEqual(after, before)

    def test_rejects_closed_structural_boundaries(self):
        cases = []

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0], protocol["clusters"][1] = (
            protocol["clusters"][1], protocol["clusters"][0]
        )
        cases.append((protocol, self.time_model, self.ium10_result, "cluster"))

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0]["modules"][1]["moduleId"] = "IUM-7-CORE-01"
        cases.append((protocol, self.time_model, self.ium10_result, "module"))

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][3]["modules"].pop()
        cases.append((protocol, self.time_model, self.ium10_result, "module"))

        time_model = copy.deepcopy(self.time_model)
        working_variant = next(
            variant
            for variant in time_model["annualVariants"]
            if variant["id"] == "GRADE-7-WORKING-40"
        )
        time_model["annualVariants"].append(copy.deepcopy(working_variant))
        cases.append((self.protocol, time_model, self.ium10_result, "variant"))

        ium10_result = copy.deepcopy(self.ium10_result)
        del ium10_result["availabilityContracts"]["AVAIL-GRADE-7-WORKING-40"]
        cases.append((self.protocol, self.time_model, ium10_result, "availability"))

        ium10_result = copy.deepcopy(self.ium10_result)
        del ium10_result["gradeJudgements"][7]
        cases.append((self.protocol, self.time_model, ium10_result, "judgement"))

        ium10_result = copy.deepcopy(self.ium10_result)
        ium10_result["annualVariants"]["GRADE-7-WORKING-40"]["targetUnits"] = 41
        cases.append((self.protocol, self.time_model, ium10_result, "variant"))

        for protocol, time_model, ium10_result, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(IUM11PublicationError, message):
                    self.compile(protocol, time_model, ium10_result)

    def test_rejects_protocol_source_and_cluster_identity_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["protocolVersion"] = "2.0.0"
        with self.assertRaisesRegex(IUM11PublicationError, "source"):
            self.compile(protocol=protocol)

        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0]["id"] = "CLUSTER-7-UNBOUND"
        with self.assertRaisesRegex(IUM11PublicationError, "cluster"):
            self.compile(protocol=protocol)

    def test_rejects_compensating_cluster_budget_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["clusters"][0]["budgetUnits"] = 7
        protocol["clusters"][1]["budgetUnits"] = 12

        with self.assertRaisesRegex(IUM11PublicationError, "budget"):
            self.compile(protocol=protocol)

    def test_rejects_annual_pilot_variant_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["variantId"] = "GRADE-7-ROBUST-DEMAND"

        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

    def test_rejects_annual_pilot_identity_and_assignment_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["id"] = "ANNUAL-7-UNBOUND"
        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["pilotAssignmentId"] = "PILOT-INT-7-DATA-CODING"
        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

    def test_rejects_annual_pilot_cluster_order_drift(self):
        protocol = copy.deepcopy(self.protocol)
        protocol["annualPilot"]["clusterIds"][0], protocol["annualPilot"]["clusterIds"][1] = (
            protocol["annualPilot"]["clusterIds"][1],
            protocol["annualPilot"]["clusterIds"][0],
        )

        with self.assertRaisesRegex(IUM11PublicationError, "annual pilot"):
            self.compile(protocol=protocol)

    def test_rejects_grade_7_judgement_availability_drift(self):
        ium10_result = copy.deepcopy(self.ium10_result)
        ium10_result["gradeJudgements"][7]["availabilityStatus"] = "available"

        with self.assertRaisesRegex(IUM11PublicationError, "availabilityStatus"):
            self.compile(ium10_result=ium10_result)


class IUM11PublicationRenderTests(IUM11PublicationCompilerTests):
    def test_json_and_markdown_are_deterministic_utf8_lf(self):
        contract = self.compile()
        rendered_json = render_publication_contract_json(contract)
        rendered_block = render_publication_markdown_block(contract)
        self.assertIsInstance(rendered_json, bytes)
        self.assertFalse(rendered_json.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(rendered_json.endswith(b"\n"))
        self.assertNotIn(b"\r\n", rendered_json)
        self.assertEqual(json.loads(rendered_json.decode("utf-8")), contract)
        self.assertEqual(rendered_block.count(PUBLICATION_START_MARKER), 1)
        self.assertEqual(rendered_block.count(PUBLICATION_END_MARKER), 1)
        self.assertIn(
            "Flexible Vertiefungs-, Transfer- und Projektmodule bleiben",
            rendered_block,
        )
        self.assertIn("status: working", rendered_block)
        self.assertIn("pilotStatus: not-started", rendered_block)
        self.assertIn("availabilityStatus: available", rendered_block)

    def test_marker_replacement_requires_one_ordered_pair(self):
        block = render_publication_markdown_block(self.compile())
        source = (
            f"vor\n{PUBLICATION_START_MARKER}\nalt\n"
            f"{PUBLICATION_END_MARKER}\nnach\n"
        )
        replaced = replace_publication_block(source, block)
        self.assertEqual(extract_publication_block(replaced), block)
        for malformed in (
            "ohne marker\n",
            f"{PUBLICATION_START_MARKER}\n",
            f"{PUBLICATION_END_MARKER}\n{PUBLICATION_START_MARKER}\n",
            source + source,
            f"{PUBLICATION_START_MARKER}\n{PUBLICATION_START_MARKER}\n"
            f"{PUBLICATION_END_MARKER}\n{PUBLICATION_END_MARKER}\n",
        ):
            with self.subTest(malformed=malformed):
                with self.assertRaises(IUM11PublicationError):
                    replace_publication_block(malformed, block)

    def test_outside_block_boundary_is_lexical_and_readme_scoped(self):
        block = render_publication_markdown_block(self.compile())
        guide = f"# Anleitung\n\n{block}\n\nErklärende deutsche Prosa.\n"
        validate_publication_text_boundary("pilot/docs/teacher-guide.md", guide)
        reserved = (
            "Version 9.9.9", "eligible-for-standard-review",
            "status: available", "available", "GRADE-7-WORKING-40",
            "41 UE", "5 Cluster", "11 Module", "6 Pilotstufen",
            "Privacy-Schwelle 9",
        )
        for declaration in reserved:
            with self.subTest(declaration=declaration):
                with self.assertRaises(IUM11PublicationError) as raised:
                    validate_publication_text_boundary(
                        "pilot/docs/teacher-guide.md", guide + declaration + "\n",
                    )
                self.assertIn("pilot/docs/teacher-guide.md", str(raised.exception))

        readme = (
            "## Phase 0\nKlasse 5: available.\n\n"
            "## IUM11-Pilotinstrument\n" + block + "\nErklärende Prosa.\n\n"
            "## Zentrale Einstiege\nIUM10 ist working.\n"
        )
        validate_publication_text_boundary("README.md", readme)

    def test_every_reserved_form_is_rejected_outside_each_publication_block(self):
        block = render_publication_markdown_block(self.compile())
        declarations = (
            "9.9.9", "eligible-for-standard-review", "status: available",
            "available", "GRADE-7-WORKING-40", "41 UE", "5 Cluster",
            "11 Module", "6 Pilotstufen", "Privacy-Schwelle 9",
        )
        documents = {
            "README.md": (
                "## IUM11-Pilotinstrument\n" + block + "\n",
                "\n## Zentrale Einstiege\n",
            ),
            "pilot/docs/teacher-guide.md": ("# Anleitung\n" + block + "\n", ""),
            "pilot/docs/review-guide.md": ("# Review\n" + block + "\n", ""),
        }
        for relative_path, (prefix, suffix) in documents.items():
            validate_publication_text_boundary(relative_path, prefix + suffix)
            for declaration in declarations:
                with self.subTest(relative_path=relative_path, declaration=declaration):
                    with self.assertRaises(IUM11PublicationError):
                        validate_publication_text_boundary(
                            relative_path,
                            prefix + declaration + "\n" + suffix,
                        )

    def test_boundary_requires_exactly_one_readme_section_and_one_marker_pair(self):
        block = render_publication_markdown_block(self.compile())
        cases = (
            ("## Andere Überschrift\n" + block, "README IUM11 section"),
            (
                "## IUM11-Pilotinstrument\n" + block + "\n"
                "## IUM11-Pilotinstrument\nOhne zweiten Block\n",
                "README IUM11 section",
            ),
            ("# Anleitung\n" + block + "\n" + PUBLICATION_START_MARKER, "publication start marker"),
        )
        for text, message in cases:
            with self.subTest(text=text):
                with self.assertRaisesRegex(IUM11PublicationError, message):
                    validate_publication_text_boundary("README.md", text)

    def test_real_build_matches_compiled_contract_and_is_idempotent(self):
        contract = compile_repository_publication_contract(ROOT)
        expected = expected_publication_outputs(ROOT)
        self.assertEqual(expected[ROOT / CONTRACT_PATH], render_publication_contract_json(contract))
        block = render_publication_markdown_block(contract)
        for relative_path in ("README.md", "pilot/docs/teacher-guide.md", "pilot/docs/review-guide.md"):
            self.assertEqual(
                extract_publication_block(expected[ROOT / relative_path].decode("utf-8")),
                block,
            )
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "repository"
            shutil.copytree(ROOT, fixture, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            build_publication_contract(fixture)
            first = {path: path.read_bytes() for path in expected_publication_outputs(fixture)}
            build_publication_contract(fixture)
            self.assertEqual(
                {path: path.read_bytes() for path in expected_publication_outputs(fixture)},
                first,
            )

    def test_repository_check_subprocess_is_current_and_read_only(self):
        before = {
            ROOT / relative: (ROOT / relative).read_bytes()
            for relative in (CONTRACT_PATH, "README.md", "pilot/docs/teacher-guide.md", "pilot/docs/review-guide.md")
            if (ROOT / relative).exists()
        }
        result = subprocess.run(
            ["python", "-B", "scripts/build_ium11_publication_contract.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {
            path: path.read_bytes()
            for path in before
        }
        self.assertEqual(after, before)

    def test_check_is_read_only_and_reports_every_drift(self):
        relative_paths = (
            CONTRACT_PATH,
            "README.md",
            "pilot/docs/teacher-guide.md",
            "pilot/docs/review-guide.md",
        )
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "repository"
            shutil.copytree(
                ROOT,
                fixture,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            (fixture / CONTRACT_PATH).write_bytes(b"{}\n")
            for index, relative_path in enumerate(PUBLICATION_PATHS, start=2):
                target = fixture / relative_path
                payload = target.read_bytes()
                self.assertEqual(payload.count(PUBLICATION_START_MARKER.encode()), 1)
                self.assertEqual(payload.count(PUBLICATION_END_MARKER.encode()), 1)
                self.assertIn(b"schemaVersion: 1", payload)
                target.write_bytes(
                    payload.replace(
                        b"schemaVersion: 1",
                        f"schemaVersion: {index}".encode("ascii"),
                        1,
                    )
                )

            before = {
                fixture / relative_path: (fixture / relative_path).read_bytes()
                for relative_path in relative_paths
            }
            with self.assertRaises(IUM11PublicationError) as raised:
                build_publication_contract(fixture, check=True)
            self.assertEqual(
                {path: path.read_bytes() for path in before},
                before,
            )
            message = str(raised.exception).replace("\\", "/")
            for relative_path in relative_paths:
                with self.subTest(relative_path=relative_path):
                    self.assertIn(relative_path, message)

    def test_builder_rejects_shifted_or_hidden_blocks_before_writing(self):
        def move_readme_block_outside_section(text):
            block = extract_publication_block(text)
            return block + "\n\n" + text.replace(block, "", 1)

        def move_guide_block_after_intro(text):
            block = extract_publication_block(text)
            without_block = text.replace(block, "", 1)
            heading_end = without_block.index("\n") + 1
            return (
                without_block[:heading_end]
                + "\nEinleitender Hinweis.\n\n"
                + block
                + without_block[heading_end:]
            )

        def hide_readme_heading(text):
            return text.replace(
                "## IUM11-Pilotinstrument",
                "```markdown\n## IUM11-Pilotinstrument\n```",
                1,
            )

        def wrap_block(text, opening, closing):
            block = extract_publication_block(text)
            return text.replace(
                block,
                f"{opening}\n{block}\n{closing}",
                1,
            )

        def add_second_h1(text):
            block = extract_publication_block(text)
            return text.replace(block, "# Zweite Hauptüberschrift\n\n" + block, 1)

        cases = (
            ("README.md", "outside-readme-section", move_readme_block_outside_section),
            ("README.md", "hidden-readme-heading", hide_readme_heading),
            (
                "pilot/docs/teacher-guide.md",
                "after-guide-introduction",
                move_guide_block_after_intro,
            ),
            (
                "pilot/docs/teacher-guide.md",
                "backtick-fence",
                lambda text: wrap_block(text, "```markdown", "```"),
            ),
            (
                "pilot/docs/review-guide.md",
                "tilde-fence",
                lambda text: wrap_block(text, "~~~markdown", "~~~"),
            ),
            (
                "pilot/docs/review-guide.md",
                "html-comment",
                lambda text: wrap_block(text, "<!-- hidden", "-->"),
            ),
            ("pilot/docs/review-guide.md", "second-h1", add_second_h1),
        )
        for relative_path, mutation_name, mutate in cases:
            with self.subTest(mutation=mutation_name):
                with tempfile.TemporaryDirectory() as temporary:
                    fixture = Path(temporary) / "repository"
                    shutil.copytree(
                        ROOT,
                        fixture,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"),
                    )
                    target = fixture / relative_path
                    target.write_bytes(
                        mutate(target.read_bytes().decode("utf-8")).encode("utf-8")
                    )
                    publication_targets = (
                        CONTRACT_PATH,
                        *PUBLICATION_PATHS,
                    )
                    before = {
                        fixture / path: (fixture / path).read_bytes()
                        for path in publication_targets
                    }

                    with self.assertRaises(IUM11PublicationError):
                        build_publication_contract(fixture)

                    self.assertEqual(
                        {path: path.read_bytes() for path in before},
                        before,
                    )

    def test_builder_rejects_commonmark_indented_h2_and_h1_headings(self):
        def add_readme_h2(text, indentation, heading_text):
            block = extract_publication_block(text)
            return text.replace(
                block,
                f"{' ' * indentation}##{heading_text}\n\n{block}",
                1,
            )

        def add_guide_h1(text, indentation, heading_text):
            return text + f"\n{' ' * indentation}#{heading_text}\n"

        cases = (
            (
                "README.md",
                add_readme_h2,
                "README.md: publication block must be inside the IUM11 section",
            ),
            (
                "pilot/docs/teacher-guide.md",
                add_guide_h1,
                "pilot/docs/teacher-guide.md: guide must contain exactly one H1",
            ),
        )
        for indentation in (1, 2, 3):
            for heading_text in (" Nachfolgender Abschnitt", ""):
                for relative_path, mutate, expected_error in cases:
                    with self.subTest(
                        indentation=indentation,
                        heading_text=heading_text,
                        relative_path=relative_path,
                    ):
                        with tempfile.TemporaryDirectory() as temporary:
                            fixture = Path(temporary) / "repository"
                            shutil.copytree(
                                ROOT,
                                fixture,
                                ignore=shutil.ignore_patterns(".git", "__pycache__"),
                            )
                            target = fixture / relative_path
                            target.write_bytes(
                                mutate(
                                    target.read_bytes().decode("utf-8"),
                                    indentation,
                                    heading_text,
                                ).encode("utf-8")
                            )

                            with self.assertRaises(IUM11PublicationError) as raised:
                                build_publication_contract(fixture)

                            self.assertEqual(str(raised.exception), expected_error)

    def test_builder_accepts_four_space_pseudo_headings(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "repository"
            shutil.copytree(
                ROOT,
                fixture,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            readme = fixture / "README.md"
            readme_text = readme.read_bytes().decode("utf-8")
            readme_block = extract_publication_block(readme_text)
            readme.write_bytes(
                readme_text.replace(
                    readme_block,
                    f"    ## Codebeispiel\n\n{readme_block}",
                    1,
                ).encode("utf-8")
            )
            guide = fixture / "pilot/docs/teacher-guide.md"
            guide.write_bytes(
                (
                    guide.read_bytes().decode("utf-8")
                    + "\n    # Eingerücktes Codebeispiel\n"
                ).encode("utf-8")
            )

            outputs = build_publication_contract(fixture, check=True)

            self.assertEqual(len(outputs), 4)

    def test_build_failure_is_per_file_atomic_and_later_check_reports_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "repository"
            shutil.copytree(ROOT, fixture, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            outputs = expected_publication_outputs(fixture)
            for path in outputs:
                if path.name == "publication-contract.json":
                    path.write_bytes(b"{}\n")
                else:
                    path.write_text(
                        replace_publication_block(
                            path.read_text(encoding="utf-8"),
                            f"{PUBLICATION_START_MARKER}\nstale\n{PUBLICATION_END_MARKER}",
                        ),
                        encoding="utf-8",
                    )
            originals = {path: path.read_bytes() for path in outputs if path.exists()}
            real_replace = __import__("os").replace
            replacements = 0

            def fail_second_replace(source, destination):
                nonlocal replacements
                replacements += 1
                if replacements == 2:
                    raise OSError("simulated interruption")
                return real_replace(source, destination)

            with mock.patch(
                "scripts.build_ium11_publication_contract.os.replace",
                side_effect=fail_second_replace,
            ):
                with self.assertRaisesRegex(OSError, "simulated interruption"):
                    build_publication_contract(fixture)

            for path, original in originals.items():
                self.assertIn(path.read_bytes(), (original, outputs[path]))
            self.assertFalse(list(fixture.rglob(".*.tmp")))
            with self.assertRaises(IUM11PublicationError) as raised:
                build_publication_contract(fixture, check=True)
            self.assertIn("drift", str(raised.exception))
            build_publication_contract(fixture)
            build_publication_contract(fixture, check=True)
