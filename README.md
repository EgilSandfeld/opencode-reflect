# opencode-reflect

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=flat-square)](#platform-support)

A self-reflection plugin for OpenCode that captures corrections during normal use and helps convert them into durable project memory and reusable commands.

## Credits

This project is based on the excellent work by Bayram Annakov:
- Original repo: https://github.com/BayramAnnakov/claude-reflect

The core ideas and much of the detection pipeline came from that project and were adapted for OpenCode.

## What It Does

### 1) Capture learnings automatically

When you correct the agent (for example: `no, use gpt-5.1 not gpt-5`), the plugin queues a learning item.

### 2) Process queued learnings with `/reflect`

Run `/reflect` to review, dedupe, and apply approved learnings to memory files (prefer `AGENTS.md`, support `CLAUDE.md` as fallback compatibility).

### 3) Discover repeating workflows with `/reflect-skills`

Analyze repeated intents and generate command templates under `.opencode/commands/`.

## OpenCode Installation (Local Plugin)

OpenCode auto-loads local plugin files from `.opencode/plugins/` and command files from `.opencode/commands/`.

1. Keep this repo in your project.
2. Start OpenCode in this project.
3. Use:
   - `/view-queue`
   - `/reflect`
   - `/reflect-skills`
   - `/skip-reflect`

No extra registration step is required for local usage.

## npm Plugin Scaffold

This repo includes an npm-publishable scaffold so the plugin can be distributed as a package.

- Source entry: `src/plugin.ts`
- Package entry: `dist/index.js` (built output)
- Commands and Python scripts are included in the package files list

Build command:

```bash
npm run build
```

## Commands

| Command | Description |
|---|---|
| `/reflect` | Process queued learnings and apply approved changes |
| `/view-queue` | View pending learnings |
| `/skip-reflect` | Discard queued learnings |
| `/reflect-skills` | Propose new reusable command templates |

## File Layout

```text
opencode-reflect/
├── .opencode/
│   ├── plugins/
│   │   └── reflect.ts
│   └── commands/
│       ├── reflect.md
│       ├── reflect-skills.md
│       ├── skip-reflect.md
│       └── view-queue.md
├── scripts/
│   ├── lib/
│   │   ├── reflect_utils.py
│   │   └── semantic_detector.py
│   ├── opencode_capture_learning.py
│   ├── opencode_check_learnings.py
│   ├── opencode_post_commit_reminder.py
│   └── opencode_session_start_reminder.py
├── src/
│   ├── index.ts
│   └── plugin.ts
└── tests/
```

## Queue and State Paths

- OpenCode primary:
  - `~/.config/opencode/learnings-queue.json`
  - `~/.config/opencode/learnings-backups/`
- Compatibility fallback:
  - `~/.claude/learnings-queue.json`

## Platform Support

- macOS
- Linux
- Windows

## License

MIT
