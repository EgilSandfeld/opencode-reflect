---
description: Discover reusable OpenCode command/skill candidates from sessions
---

Analyze recent session patterns and propose new reusable commands.

Sources:
- Prefer OpenCode session/event history if available.
- Fallback to Claude history under `~/.claude/projects/` if needed.

Workflow:
1. Gather recent user requests and corrections (default last 14 days unless user specifies).
2. Group by semantic intent (not keyword-only matching).
3. Exclude patterns that already have commands in `.opencode/commands/`.
4. Propose candidates with:
   - command name
   - one-line purpose
   - evidence count
   - default guardrails learned from corrections
5. Ask which candidates to generate.
6. Create selected files under `.opencode/commands/<name>.md`.

When generating each command:
- Keep templates concise and actionable.
- Add a short description frontmatter.
- Include guardrails only when clearly supported by evidence.
