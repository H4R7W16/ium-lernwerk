from pathlib import Path
import tempfile
import unittest

from scripts.validate_v2_rebaseline import validate_repository


class ValidateV2RebaselineTests(unittest.TestCase):
    def test_missing_control_files_fail_closed(self) -> None:
        """Catches a validator that silently accepts an absent V2 control plane."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        self.assertIn("roadmap/v2/status.json fehlt", errors)
        self.assertIn("roadmap/v2/archive/v1-baseline.json fehlt", errors)
        self.assertIn("roadmap/v2/requirements/requirements.json fehlt", errors)


if __name__ == "__main__":
    unittest.main()
