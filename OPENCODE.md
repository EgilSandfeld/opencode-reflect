# OpenCode Port Notes

This repo contains an OpenCode port of the original reflection workflow.

## What was ported

- Hook wiring moved to `.opencode/plugins/reflect.ts`
- User commands moved to `.opencode/commands/`
- Runtime adapters added in `scripts/opencode_*.py`
- Queue/backup paths support OpenCode home:
  - `~/.config/opencode/learnings-queue.json`
  - `~/.config/opencode/learnings-backups/`

## Event mapping

- `session.created` -> `scripts/opencode_session_start_reminder.py`
- `message.updated` / `message.part.updated` (user role) -> `scripts/opencode_capture_learning.py`
- `experimental.session.compacting` -> `scripts/opencode_check_learnings.py`
- `tool.execute.after` (bash) -> `scripts/opencode_post_commit_reminder.py`

## Compatibility behavior

- Default runtime remains legacy-compatible unless OpenCode is detected.
- Set `REFLECT_RUNTIME=opencode` to force OpenCode paths.
- Existing legacy workflows and tests continue to work.

## Legacy alias deprecations

The following legacy helper names are still available but now emit `DeprecationWarning`:

- `get_claude_dir()` -> use `get_memory_config_dir()`
- `find_claude_files()` -> use `find_memory_files()`
- `suggest_claude_file()` -> use `suggest_memory_file()`

Planned removal marker: no earlier than `v1.0.0` (target date `2026-12-31`).

## Quick verify

1. Start OpenCode in this project.
2. Send a correction like: `no, use gpt-5.1 not gpt-5`.
3. Run `/view-queue`.
4. Run `/reflect` and apply to `AGENTS.md` or `CLAUDE.md`.
