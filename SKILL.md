---
name: opencode-reflect
description: Self-learning system that captures corrections during sessions and reminds users to run /reflect to update AGENTS.md. Use when discussing learnings, corrections, or when the user mentions remembering something for future sessions.
---

# OpenCode Reflect - Self-Learning System

A two-stage system that helps OpenCode learn from user corrections.

## How It Works

**Stage 1: Capture (Automatic)**
Hooks detect correction patterns ("no, use X", "actually...", "use X not Y") and queue them to `~/.config/opencode/learnings-queue.json`.

**Stage 2: Process (Manual)**
User runs `/reflect` to review and apply queued learnings to AGENTS.md.

## Available Commands

| Command | Purpose |
|---------|---------|
| `/reflect` | Process queued learnings with human review |
| `/reflect --scan-history` | Scan past sessions for missed learnings |
| `/reflect --dry-run` | Preview changes without applying |
| `/reflect-skills` | Discover skill candidates from repeating patterns |
| `/skip-reflect` | Discard all queued learnings |
| `/view-queue` | View pending learnings without processing |

## When to Remind Users

Remind users about `/reflect` when:
- They complete a feature or meaningful work unit
- They make corrections you should remember for future sessions
- They explicitly say "remember this" or similar
- Context is about to compact and queue has items

## Correction Detection Patterns

High-confidence corrections:
- Tool rejections (user stops an action with guidance)
- "no, use X" / "don't use Y"
- "actually..." / "I meant..."
- "use X not Y" / "X instead of Y"
- "remember:" (explicit marker)

## Learning Destinations

- `./AGENTS.md` - Primary project learnings (OpenCode-first)
- `~/.config/opencode/AGENTS.md` - Optional global user learnings
- `./.opencode/rules/*.md` - Project-scoped modular rules
- `~/.config/opencode/rules/*.md` - Global modular rules
- `~/.config/opencode/projects/<project>/memory/*.md` - Auto memory (low-confidence, exploratory)
- `.opencode/commands/*.md` - Skill improvements (corrections during skill execution)

## Example Interaction

```
User: no, use gpt-5.1 not gpt-5 for reasoning tasks
Assistant: Got it, I'll use gpt-5.1 for reasoning tasks.

[Hook captures this correction to queue]

User: /reflect
Assistant: Found 1 learning queued. "Use gpt-5.1 for reasoning tasks"
        Scope: global
        Apply to ./AGENTS.md? [y/n]
```
