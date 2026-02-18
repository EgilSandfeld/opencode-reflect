#!/usr/bin/env python3
"""OpenCode adapter for capture_learning.

Normalizes OpenCode event payloads and captures user corrections into queue.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.reflect_utils import (  # noqa: E402
    MAX_CAPTURE_PROMPT_LENGTH,
    create_queue_item,
    detect_patterns,
    get_queue_path,
    load_queue,
    save_queue,
    should_include_message,
)


def _first_text_from_message(message_obj):
    if not isinstance(message_obj, dict):
        return ""

    def first_text_from_items(items):
        if not isinstance(items, list):
            return ""

        for item in items:
            if not isinstance(item, dict):
                continue

            item_type = item.get("type")
            if item_type in ("text", "input_text"):
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    return text

            text = item.get("content")
            if isinstance(text, str) and text.strip():
                return text

        return ""

    content = message_obj.get("content")
    if isinstance(content, str) and content.strip():
        return content

    content_text = first_text_from_items(content)
    if content_text:
        return content_text

    parts = message_obj.get("parts")
    parts_text = first_text_from_items(parts)
    if parts_text:
        return parts_text

    return ""


def extract_role(payload):
    def as_text(value):
        return value if isinstance(value, str) else ""

    if not isinstance(payload, dict):
        return ""

    event_obj = payload.get("event")
    event = event_obj if isinstance(event_obj, dict) else {}

    payload_message_obj = payload.get("message")
    payload_message = (
        payload_message_obj if isinstance(payload_message_obj, dict) else {}
    )

    payload_part_obj = payload.get("part")
    payload_part = payload_part_obj if isinstance(payload_part_obj, dict) else {}

    event_message_obj = event.get("message")
    event_message = event_message_obj if isinstance(event_message_obj, dict) else {}

    event_part_obj = event.get("part")
    event_part = event_part_obj if isinstance(event_part_obj, dict) else {}

    candidates = [
        payload.get("role"),
        payload_message.get("role"),
        payload_part.get("role"),
        event.get("role"),
        event_message.get("role"),
        event_part.get("role"),
    ]

    for candidate in candidates:
        value = as_text(candidate).strip()
        if value:
            return value.lower()

    return ""


def extract_prompt(payload):
    candidates = []

    if isinstance(payload, dict):
        candidates.extend(
            [
                payload.get("prompt"),
                payload.get("message"),
                payload.get("text"),
                payload.get("input"),
            ]
        )

        event = payload.get("event")
        if isinstance(event, dict):
            candidates.extend(
                [
                    event.get("prompt"),
                    event.get("message"),
                    event.get("text"),
                    event.get("input"),
                ]
            )
            message_obj = event.get("message")
            if isinstance(message_obj, dict):
                candidates.append(_first_text_from_message(message_obj))

        message_obj = payload.get("message")
        if isinstance(message_obj, dict):
            candidates.append(_first_text_from_message(message_obj))

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

    role = extract_role(payload)
    if role and role != "user":
        return 0

    prompt = extract_prompt(payload)
    if not prompt:
        return 0

    if not should_include_message(prompt):
        return 0

    if len(prompt) > MAX_CAPTURE_PROMPT_LENGTH and "remember:" not in prompt.lower():
        return 0

    queue_path = get_queue_path()
    if not queue_path.exists():
        queue_path.parent.mkdir(parents=True, exist_ok=True)
        queue_path.write_text("[]", encoding="utf-8")

    item_type, patterns, confidence, sentiment, decay_days = detect_patterns(prompt)
    if not item_type:
        return 0

    queue_item = create_queue_item(
        message=prompt,
        item_type=item_type,
        patterns=patterns,
        confidence=confidence,
        sentiment=sentiment,
        decay_days=decay_days,
    )
    items = load_queue()
    items.append(queue_item)
    save_queue(items)

    preview = prompt[:60] + "..." if len(prompt) > 60 else prompt
    print(f"[reflect] learning captured: '{preview}' ({confidence:.0%})")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("REFLECT_RUNTIME", "opencode")
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"Warning: opencode_capture_learning.py error: {exc}", file=sys.stderr)
        sys.exit(0)
