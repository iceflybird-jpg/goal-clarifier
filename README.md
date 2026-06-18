# goal-clarify

A host-agnostic AI agent skill that turns vague requirements into clear, executable, verifiable structured goals — with optional execution tracking and evidence-based completion.

Invoke as **`/goal-clarify`** or `@goal-clarify` when the requirement is fuzzy; skip when the user already gave a complete spec.

## What It Does

1. **Reads a context cache** at `<project-root>/.agent/goal-context.md` to avoid re-searching stable project knowledge.
2. **Searches proactively** — code, git, docs, project memory, past conversations (if available), web — before asking the user.
3. **Outputs a structured Goal** in XML: `<task>`, `<context>`, `<constraints>`, `<output>`.
4. **Gates execution** until the user confirms the Goal.
5. **Optionally persists state** via `scripts/goal_state.py` and audits completion with objective evidence.

## Install

Copy the entire `goal-clarify/` directory into your agent's skills folder:

| Host | Typical path |
|------|----------------|
| Cursor | `~/.cursor/skills/goal-clarify/` |
| Claude Code | skills directory per your setup |
| Other agents | Any path your host loads `SKILL.md` from |

Requirements: Python 3.9+ (only for optional `goal_state.py`).

## Quick Start

1. User: `/goal-clarify 帮我优化一下登录流程`
2. Agent: reads cache → searches repo → drafts XML Goal → asks for confirmation.
3. User: `确认`
4. Agent: executes against `<task>` / `<output>`, records evidence, closes goal.

## XML Output

```xml
<task>Clear, executable goal (1–3 bullets)</task>
<context>Sourced background bullets</context>
<constraints>Must do / must NOT do / limits / assumptions</constraints>
<output>- [ ] Verifiable checklist + verification method</output>
```

See `references/goal-xml-template.md` and `references/example-goals.md`.

## Context Cache

- **Project:** `<project-root>/.agent/goal-context.md`
- **User (optional):** `~/.agent/goal-context.md`
- **First run:** full search → write cache
- **Later runs:** read cache → search only gaps or stale sections

Template: `references/context-cache-template.md`.

## Goal State (optional)

```bash
python3 scripts/goal_state.py set --workspace /path/to/project --xml-file goal.xml
python3 scripts/goal_state.py show --workspace /path/to/project
python3 scripts/goal_state.py evidence --workspace /path/to/project --index 1 --text "tests pass"
python3 scripts/goal_state.py complete --workspace /path/to/project
```

State files default to `~/.agent/goal-state/`. Set `GOAL_STATE_DIR` to override.

## vs Claude Code `/goal`

| | `/goal` | `goal-clarify` |
|---|---------|----------------|
| Timing | During execution | Before execution |
| Assumes | Goal is clear | Goal is fuzzy |
| Mechanism | Executor/evaluator loop | Search + cache + XML contract |
| Chain | After this skill | Before `/goal`-style loops |

## License

MIT
