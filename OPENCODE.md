# OpenCode Port Notes

This repo is now OpenCode-only.

## What was ported

- Hook wiring moved to `.opencode/plugins/reflect.ts`
- User commands moved to `.opencode/commands/`
- Runtime adapters added in `scripts/opencode_*.py`
- Queue/backup paths use OpenCode home:
  - `~/.config/opencode/learnings-queue.json`
  - `~/.config/opencode/learnings-backups/`

## Event mapping

- `session.created` -> `scripts/opencode_session_start_reminder.py`
- `message.updated` / `message.part.updated` (user role) -> `scripts/opencode_capture_learning.py`
- `experimental.session.compacting` -> `scripts/opencode_check_learnings.py`
- `tool.execute.after` (bash) -> `scripts/opencode_post_commit_reminder.py`

## Runtime behavior

- Runtime is OpenCode only.
- Reflection data is read and written only under `~/.config/opencode/`.

## Quick verify

1. Start OpenCode in this project.
2. Send a correction like: `no, use gpt-5.1 not gpt-5`.
3. Run `/view-queue`.
4. Run `/reflect` and apply to `AGENTS.md`.
