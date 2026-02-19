# opencode-reflect

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=flat-square)](#platform-support)

`opencode-reflect` is an OpenCode-only reflection plugin that captures user corrections and turns them into reusable project memory.

## What It Does

1) Capture learnings automatically
- When you correct the agent (for example: `no, use gpt-5.1 not gpt-5`), a learning is queued.

2) Process queued learnings with `/reflect`
- Review, dedupe, and apply approved learnings to `AGENTS.md`.

3) Discover reusable workflows with `/reflect-skills`
- Analyze repeated intents and generate command templates under `.opencode/commands/`.

## Installation

OpenCode auto-loads local plugin files from `.opencode/plugins/` and command files from `.opencode/commands/`.

1. Keep this repo in your project.
2. Start OpenCode in this project.
3. Use `/view-queue`, `/reflect`, `/reflect-skills`, and `/skip-reflect`.

## Queue and State Paths

- `~/.config/opencode/learnings-queue.json`
- `~/.config/opencode/learnings-backups/`
- `~/.config/opencode/projects/`

## Build

```bash
npm run build
```

## Platform Support

- macOS
- Linux
- Windows

## License

MIT
