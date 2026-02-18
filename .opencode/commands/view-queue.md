---
description: Show pending reflection learnings queue
---

Show queued learnings in a compact format.

Use this order:
1. Read `~/.config/opencode/learnings-queue.json`
2. If missing/empty, read `~/.claude/learnings-queue.json`

For each item show:
- confidence
- type
- first ~70 chars of message
- relative timestamp

If queue is empty, say it is empty and suggest running `/reflect` after making corrections in normal chat.
