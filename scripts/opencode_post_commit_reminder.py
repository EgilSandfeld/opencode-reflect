#!/usr/bin/env python3
"""OpenCode adapter for git commit reminders."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.reflect_utils import load_queue  # noqa: E402


def extract_command(payload):
    candidates = []

    if isinstance(payload, dict):
        candidates.extend(
            [
                payload.get("command"),
                payload.get("cmd"),
            ]
        )

        event = payload.get("event")
        if isinstance(event, dict):
            candidates.extend(
                [
                    event.get("command"),
                    event.get("cmd"),
                ]
            )
            input_obj = event.get("input")
            if isinstance(input_obj, dict):
                candidates.extend(
                    [
                        input_obj.get("command"),
                        input_obj.get("cmd"),
                    ]
                )
            args_obj = event.get("args")
            if isinstance(args_obj, dict):
                candidates.extend(
                    [
                        args_obj.get("command"),
                        args_obj.get("cmd"),
                    ]
                )

    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate

    return ""


def main() -> int:
    raw = sys.stdin.read()
    if not raw:
        return 0

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    command = extract_command(payload)
    if not command or "git commit" not in command or "--amend" in command:
        return 0

    items = load_queue()
    if items:
        print(
            f"[reflect] git commit detected. {len(items)} queued learning(s) pending; run /reflect."
        )
    else:
        print(
            "[reflect] git commit detected. Run /reflect if you made important corrections this session."
        )
    return 0


if __name__ == "__main__":
    os.environ.setdefault("REFLECT_RUNTIME", "opencode")
    try:
        sys.exit(main())
    except Exception as exc:
        print(
            f"Warning: opencode_post_commit_reminder.py error: {exc}", file=sys.stderr
        )
        sys.exit(0)
