#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.reflect_utils import (
    find_memory_files,
    get_memory_config_dir,
    get_platform_dir,
    suggest_memory_file,
)


class TestOpenCodePaths(unittest.TestCase):
    def test_platform_dir_is_opencode_config(self):
        path = get_platform_dir()
        self.assertEqual(path, Path.home() / ".config" / "opencode")
        self.assertEqual(path, get_memory_config_dir())

    def test_find_memory_files_detects_agents_and_rules(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "AGENTS.md").write_text("# Project\n", encoding="utf-8")
            (root / ".opencode" / "rules").mkdir(parents=True)
            (root / ".opencode" / "rules" / "guardrails.md").write_text(
                "# Guardrails\n", encoding="utf-8"
            )

            with patch("lib.reflect_utils.get_memory_config_dir") as mock_dir:
                global_dir = root / "global"
                global_dir.mkdir(parents=True)
                (global_dir / "AGENTS.md").write_text("# Global\n", encoding="utf-8")
                mock_dir.return_value = global_dir

                files = find_memory_files(str(root))

            rels = {f["relative_path"] for f in files}
            self.assertIn("./AGENTS.md", rels)
            self.assertIn("~/.config/opencode/AGENTS.md", rels)
            self.assertIn("./.opencode/rules/guardrails.md", rels)

    def test_suggest_memory_file_prefers_global_agents_for_model(self):
        files = [
            {
                "path": "/tmp/rules/model-preferences.md",
                "relative_path": "./.opencode/rules/model-preferences.md",
                "type": "rule",
            }
        ]
        result = suggest_memory_file("use gpt-5.1 for reasoning", files)
        self.assertEqual(result, "./.opencode/rules/model-preferences.md")


if __name__ == "__main__":
    unittest.main()
