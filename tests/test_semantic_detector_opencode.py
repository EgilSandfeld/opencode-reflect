#!/usr/bin/env python3
import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch, Mock
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.semantic_detector import semantic_analyze


class TestSemanticDetectorOpenCode(unittest.TestCase):
    @patch("lib.semantic_detector.subprocess.run")
    def test_uses_opencode_cli(self, mock_run: Mock):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["opencode"],
            returncode=0,
            stdout='{"result": {"is_learning": true, "type": "correction", "confidence": 0.8, "reasoning": "ok", "extracted_learning": "Use tests"}}',
            stderr="",
        )

        result = semantic_analyze("no, use tests")

        self.assertIsNotNone(result)
        self.assertTrue(result["is_learning"])
        cmd = (
            mock_run.call_args.kwargs["args"]
            if "args" in mock_run.call_args.kwargs
            else mock_run.call_args[0][0]
        )
        self.assertEqual(cmd[:3], ["opencode", "run", "--format"])

    @patch("lib.semantic_detector.subprocess.run")
    def test_handles_missing_cli(self, mock_run: Mock):
        mock_run.side_effect = FileNotFoundError("opencode not found")
        self.assertIsNone(semantic_analyze("remember: use tests"))


if __name__ == "__main__":
    unittest.main()
