---
description: Process queued learnings and update AGENTS.md/CLAUDE.md
---

You are running opencode-reflect in OpenCode mode.

Runtime rules:
- Prefer OpenCode queue/state paths under `~/.config/opencode/`
- Keep legacy fallback paths (`~/.claude/`) if OpenCode files do not exist
- Prefer writing approved learnings to `AGENTS.md`; also support `CLAUDE.md` when it exists

Context:
- Working directory: !`pwd`
- OpenCode queue: !`cat ~/.config/opencode/learnings-queue.json 2>/dev/null || echo "[]"`
- Legacy fallback queue: !`cat ~/.claude/learnings-queue.json 2>/dev/null || echo "[]"`

Your task:
1. Load queued learnings from OpenCode queue first, then Claude fallback queue if empty.
2. Classify each item as global, project, or skill-specific guidance.
3. Remove obvious duplicates and merge semantically similar entries.
4. Ask the user what to apply (apply all / select / skip all).
5. Write approved items to the right target(s):
   - `AGENTS.md` (primary)
   - `CLAUDE.md` (compatibility)
   - `commands/*.md` when an item is clearly a skill improvement
6. Clear only the queue that was used.

Output requirements:
- Show a concise review table with confidence and target suggestion before writing.
- Preserve existing file structure and section headings.
- Add new learnings as bullet points.
- If no queue items exist, explain how to generate them (normal conversation + plugin hooks).
