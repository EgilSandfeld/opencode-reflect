#!/usr/bin/env python3
"""OpenCode adapter for session start reminder."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from session_start_reminder import main  # noqa: E402


if __name__ == "__main__":
    os.environ.setdefault("REFLECT_RUNTIME", "opencode")
    try:
        sys.exit(main())
    except Exception as exc:
        print(
            f"Warning: opencode_session_start_reminder.py error: {exc}", file=sys.stderr
        )
        sys.exit(0)
