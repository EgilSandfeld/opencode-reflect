#!/usr/bin/env python3
"""Tests for OpenCode adapter payload parsing.

This is a lightweight event harness that replays representative OpenCode
payload shapes to ensure parser functions keep working when payload structure
varies.
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from opencode_capture_learning import extract_prompt, extract_role
from opencode_post_commit_reminder import extract_command


class TestOpenCodeCapturePromptExtraction(unittest.TestCase):
    def test_extract_prompt_direct_prompt(self):
        self.assertEqual(
            extract_prompt({"prompt": "no, use gpt-5.1"}), "no, use gpt-5.1"
        )

    def test_extract_prompt_event_text(self):
        payload = {"event": {"text": "remember: run tests first"}}
        self.assertEqual(extract_prompt(payload), "remember: run tests first")

    def test_extract_prompt_message_content_list(self):
        payload = {
            "event": {
                "message": {
                    "content": [{"type": "input_text", "text": "actually, use Python"}]
                }
            }
        }
        self.assertEqual(extract_prompt(payload), "actually, use Python")

    def test_extract_prompt_empty_when_no_candidate(self):
        self.assertEqual(extract_prompt({"event": {"message": {"content": []}}}), "")

    def test_extract_prompt_event_message_parts(self):
        payload = {
            "event": {
                "message": {"parts": [{"type": "text", "text": "don't use that"}]}
            }
        }
        self.assertEqual(extract_prompt(payload), "don't use that")


class TestOpenCodeCaptureRoleExtraction(unittest.TestCase):
    def test_extract_role_from_event_message(self):
        payload = {"event": {"message": {"role": "user"}}}
        self.assertEqual(extract_role(payload), "user")

    def test_extract_role_from_top_level(self):
        payload = {"role": "assistant"}
        self.assertEqual(extract_role(payload), "assistant")

    def test_extract_role_empty_when_missing(self):
        self.assertEqual(extract_role({"event": {}}), "")


class TestOpenCodeCommitCommandExtraction(unittest.TestCase):
    def test_extract_command_top_level(self):
        self.assertEqual(
            extract_command({"command": "git commit -m x"}), "git commit -m x"
        )

    def test_extract_command_nested_input(self):
        payload = {"event": {"input": {"command": "git commit -m feat"}}}
        self.assertEqual(extract_command(payload), "git commit -m feat")

    def test_extract_command_nested_args_cmd(self):
        payload = {"event": {"args": {"cmd": "git commit -m test"}}}
        self.assertEqual(extract_command(payload), "git commit -m test")

    def test_extract_command_empty_when_missing(self):
        self.assertEqual(extract_command({"event": {"args": {}}}), "")


if __name__ == "__main__":
    unittest.main()
