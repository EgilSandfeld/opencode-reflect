---
description: Clear pending reflection queue without applying
---

Discard queued learnings safely.

Behavior:
1. Check OpenCode queue at `~/.config/opencode/learnings-queue.json`.
2. Show count and short previews before deletion.
3. Ask for explicit confirmation.
4. If confirmed, replace queue file contents with `[]`.
5. Report completion count.
