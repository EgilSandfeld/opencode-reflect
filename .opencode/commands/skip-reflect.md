---
description: Clear pending reflection queue without applying
---

Discard queued learnings safely.

Behavior:
1. Check OpenCode queue at `~/.config/opencode/learnings-queue.json`.
2. If that queue is empty, check Claude fallback queue at `~/.claude/learnings-queue.json`.
3. Show count and short previews before deletion.
4. Ask for explicit confirmation.
5. If confirmed, replace the selected queue file contents with `[]`.
6. Report completion count and which queue file was cleared.
