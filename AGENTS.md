# AGENTS.md

This file provides guidance to OpenCode agents working in this repository.

## Project Overview

`opencode-reflect` is an OpenCode-native reflection plugin with a two-stage flow:
1. **Capture stage (automatic):** hooks detect correction patterns in user prompts and queue them.
2. **Process stage (manual):** `/reflect` reviews queued learnings and writes approved guidance to memory files.

## Architecture

```
.opencode/plugins/reflect.ts  -> OpenCode plugin wiring
.opencode/commands/*.md       -> OpenCode command prompts
scripts/opencode_*.py         -> OpenCode runtime adapters
scripts/*.py                  -> Core extraction/detection utilities
scripts/lib/                  -> Shared utilities (reflect_utils.py, semantic_detector.py)
tests/                        -> Test suite (pytest)
```

## Runtime and Paths

- Runtime: OpenCode only
- Queue path: `~/.config/opencode/learnings-queue.json`
- Backup path: `~/.config/opencode/learnings-backups/`
- Session history path: `~/.config/opencode/projects/`

## Memory Targets

| Target | Path | Type | Description |
|--------|------|------|-------------|
| Project AGENTS.md | `./AGENTS.md` | `root` | Primary project memory target |
| Global AGENTS.md | `~/.config/opencode/AGENTS.md` | `global` | Optional user-wide memory |
| Rules | `./.opencode/rules/*.md`, `~/.config/opencode/rules/*.md` | `rule` | Modular scoped rules |
| Auto Memory | `~/.config/opencode/projects/<project>/memory/*.md` | `auto-memory` | Low-confidence staging |
| Skill Files | `.opencode/commands/*.md` | `skill` | Skill-specific improvements |

## Development Commands

```bash
python -m pytest tests/ -v
python scripts/compare_detection.py --project .
echo '{"prompt":"no, use gpt-5.1 not gpt-5"}' | python3 scripts/opencode_capture_learning.py
```

## Notes

- Prefer command definitions in `.opencode/commands/`.
- Keep the repository OpenCode-only; do not add runtime compatibility layers.
