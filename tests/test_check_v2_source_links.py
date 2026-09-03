from __future__ import annotations

from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest

from scripts.check_v2_source_links import (
    check_url,
    main,
    normalize_final_url,
    update_snapshot,
)


class LinkHandler(BaseHTTPRequestHandler):
    flaky_requests = 0

    def do_HEAD(self) -> None:  # noqa: N802 - protocol callback
        if self.path == "/ok":
            self.send_response(200)
        elif self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/ok")
        elif self.path == "/redirect-gone":
            self.send_response(302)
            self.send_header("Location", "/gone")
        elif self.path == "/loop-a":
            self.send_response(302)
            self.send_header("Location", "/loop-b")
        elif self.path == "/loop-b":
            self.send_response(302)
            self.send_header("Location", "/loop-a")
        elif self.path == "/redirect-without-location":
            self.send_response(302)
        elif self.path == "/flaky":
            type(self).flaky_requests += 1
            self.send_response(503 if type(self).flaky_requests == 1 else 200)
        elif self.path == "/restricted":
            self.send_response(403)
        elif self.path == "/gone":
            self.send_response(404)
        elif self.path == "/head-unsupported":
            self.send_response(405)
        else:
            self.send_response(500)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802 - protocol callback
        if self.path == "/head-unsupported":
            self.send_response(200)
        else:
            self.send_response(500)
        self.end_headers()

    def log_message(self, _format: str, *_args: object) -> None:
        return


class CheckV2SourceLinksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), LinkHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        host, port = cls.server.server_address
        cls.base_url = f"http://{host}:{port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_probe_classifies_success_redirect_restriction_missing_and_get_fallback(self) -> None:
        LinkHandler.flaky_requests = 0
        expected = {
            "/ok": "resolved",
            "/redirect": "resolved",
            "/restricted": "restricted",
            "/gone": "missing",
            "/head-unsupported": "resolved",
            "/redirect-gone": "missing",
            "/loop-a": "unresolved",
            "/redirect-without-location": "unresolved",
            "/flaky": "resolved",
        }

        for path, expected_status in expected.items():
            with self.subTest(path=path):
                result = check_url(f"{self.base_url}{path}", timeout=2)
                self.assertEqual(expected_status, result["status"])

    def test_required_failure_keeps_previous_snapshot_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "link-audit.json"
            output.write_text('{"sentinel": true}\n', encoding="utf-8")
            before = output.read_bytes()
            targets = [
                {
                    "sourceId": "SRC-OK",
                    "required": True,
                    "locatorType": "url",
                    "url": f"{self.base_url}/ok",
                },
                {
                    "sourceId": "SRC-MISSING",
                    "required": True,
                    "locatorType": "url",
                    "url": f"{self.base_url}/gone",
                },
            ]

            errors, warnings = update_snapshot(
                targets,
                output,
                checked_at="2026-09-03",
                timeout=2,
            )

            self.assertEqual([], warnings)
            self.assertEqual(
                ["Pflichtquelle SRC-MISSING ist nicht auflösbar (missing)"],
                errors,
            )
            self.assertEqual(before, output.read_bytes())

    def test_optional_failure_warns_and_writes_snapshot_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "link-audit.json"
            targets = [
                {
                    "sourceId": "SRC-OPTIONAL",
                    "required": False,
                    "locatorType": "url",
                    "url": f"{self.base_url}/gone",
                }
            ]

            errors, warnings = update_snapshot(
                targets,
                output,
                checked_at="2026-09-03",
                timeout=2,
            )

            self.assertEqual([], errors)
            self.assertEqual(
                ["Optionale Quelle SRC-OPTIONAL ist nicht auflösbar (missing)"],
                warnings,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(1, payload["summary"]["warnings"])
            self.assertEqual("missing", payload["checks"][0]["status"])

    def test_invalid_date_or_transport_payload_preserves_previous_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "link-audit.json"
            output.write_text('{"sentinel": true}\n', encoding="utf-8")
            before = output.read_bytes()
            targets = [
                {
                    "sourceId": "SRC-OK",
                    "required": True,
                    "locatorType": "url",
                    "url": f"{self.base_url}/ok",
                }
            ]

            errors, _warnings = update_snapshot(
                targets,
                output,
                checked_at="not-a-date",
                timeout=2,
            )
            self.assertIn("Linkaudit-Stichtag muss YYYY-MM-DD sein", errors)
            self.assertEqual(before, output.read_bytes())

            def invalid_probe(_url: str, _timeout: float) -> dict[str, object | None]:
                return {
                    "status": "resolved",
                    "httpStatus": None,
                    "finalUrl": None,
                }

            errors, _warnings = update_snapshot(
                targets,
                output,
                checked_at="2026-09-03",
                timeout=2,
                probe=invalid_probe,
            )
            self.assertIn(
                "Linkprüfung SRC-OK benötigt terminale HTTP-Evidenz für resolved",
                errors,
            )
            self.assertEqual(before, output.read_bytes())

    def test_cli_requires_explicit_write_flag_before_any_audit_work(self) -> None:
        with redirect_stdout(io.StringIO()):
            result = main([])
        self.assertEqual(2, result)

    def test_final_url_normalization_removes_only_volatile_springer_parameters(self) -> None:
        url = (
            "https://link.springer.com/article/10.1007/example"
            "?error=cookies_not_supported&code=volatile-token&stable=kept#fragment"
        )

        normalized = normalize_final_url(url)

        self.assertEqual(
            "https://link.springer.com/article/10.1007/example?stable=kept",
            normalized,
        )


if __name__ == "__main__":
    unittest.main()
