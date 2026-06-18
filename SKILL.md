---
name: goal-clarify
description: >-
  Transform vague requirements into clear, executable, verifiable XML Goals
  (task/context/constraints/output). Proactively searches code, git, docs, memory,
  and web; maintains a project context cache. Gates execution on user confirmation,
  optionally persists goal state and audits completion with evidence. Triggers:
  /goal-clarify, clarify requirements, define goal, break down task, 拆解目标,
  模糊需求, goal clarify, requirement to goal.
version: 2.0.0
---

# Goal Clarify — Vague Requirement → Structured Goal → Execution Loop

> **Announce at start:**「使用 goal-clarify：先读缓存并做上下文搜索，产出 XML Goal，确认后再执行。」

## When to Use

Use when the user gives a **vague, incomplete, or ambiguous** requirement that must become an executable, verifiable goal.

**Triggers:** `/goal-clarify`, `clarify requirements`, `define goal`, `break down task`, `拆解目标`, `模糊需求`, `@goal-clarify`

**Skip when:** the user already provided a complete, directly executable requirement — execute directly.

## Phases

| Phase | Purpose |
|-------|---------|
| 0 Cache warm-up | Read `<project-root>/.agent/goal-context.md` and `~/.agent/goal-context.md` |
| 1 Context search | Parallel search per `references/context-search-playbook.md` (cache gaps only) |
| 2 Draft XML Goal | `<task>` `<context>` `<constraints>` `<output>` |
| 2b Clarify | ≤2 blocking questions only |
| **GATE** | User must confirm Goal before implementation |
| 3 Persist | Optional: `scripts/goal_state.py set` |
| 4 Execute | Implement per Goal; large work → planning skill if available |
| 5 Audit | Evidence map per `references/completion-audit.md` |
| 6 Close | Optional: `goal_state.py complete` + audit artifact |
| 7 Update cache | Merge new knowledge into `.agent/goal-context.md` |

**vs brainstorming:** automated context search + XML contract + optional execution audit (not design Q&A only).

**vs Claude `/goal`:** clarifies fuzzy input *before* execution; `/goal` assumes the goal text is already clear.

## HARD GATE — Clarification Before Execution

Until the user explicitly confirms the XML Goal (e.g.「确认」「可以执行」「按这个 goal 做」「looks good」):

- **FORBIDDEN:** production code, commits, pushes, large file edits
- **ALLOWED:** read-only search, drafting XML, ≤2 clarifying questions

## Required Reads (before Phase 2)

1. `references/context-search-playbook.md`
2. `references/goal-xml-template.md`
3. `references/example-goals.md` (density reference)

## Phase 0: Context Cache

```
1. Read <project-root>/.agent/goal-context.md (if exists)
2. Read ~/.agent/goal-context.md (user-level, if exists)
3. Plan Phase 1 searches = full search − cache-covered content
```

Cache stale (>7 days since last update) → refresh structure and git summary.

See `references/context-cache-template.md` for format.

## Phase 1: Context Search

Execute layers **in parallel** per playbook. Minimum: **L0** (rules/README) + **L2** (code/git).

Each `<context>` bullet:

```text
- [source-type] path or URL: one-sentence summary
```

Source prefixes: `[user]` `[doc]` `[rule]` `[code]` `[git]` `[memory]` `[transcript]` `[web]` `[history]`

## Phase 2: Draft XML Goal

```xml
<task>...</task>
<context>...</context>
<constraints>...</constraints>
<output>...</output>
```

Rules:

- `<task>`: 1–3 verb-led bullets; one theme
- `<context>`: ≥5 sourced bullets for non-trivial work
- `<constraints>`: Must do / Must NOT do / technical / resource limits; stated assumptions
- `<output>`: `- [ ]` lines that are objectively verifiable; include verification method and termination condition

Self-check with `references/goal-quality-rubric.md` (target score ≥7).

End message with: **请确认以上 Goal；确认后开始执行。**

### Phase 2b: Clarifying Questions

Ask only 1–2 **scope-changing** unknowns. Document other defaults in `<constraints>`.

If you see a better direction than the literal request, state it directly (one paragraph max).

## Phase 3: Persist (after user confirms)

Save XML to workspace (recommended):

```text
<project-root>/.agent/goals/goal_<slug>.xml
```

Activate state (optional but recommended for multi-step work):

```bash
python3 <skill-root>/scripts/goal_state.py set \
  --workspace "<absolute-project-root>" \
  --xml-file "<path-to-goal.xml>"
```

`<skill-root>` = directory containing this `SKILL.md`.

## Phase 4: Execute

1. Re-read goal: `goal_state.py show --workspace ...` (if persisted)
2. Creative / multi-file work: invoke planning skill if host provides one
3. Straight execution: implement against `<task>` and `<output>`
4. Respect `<constraints>` and project rules (`.cursorrules`, `AGENTS.md`, etc.)

Track each `- [ ]` in `<output>`.

## Phase 5: Completion Audit

Read `references/completion-audit.md`. **Mandatory** before claiming done.

1. Build requirement → evidence table
2. Run verification commands; capture paths / output
3. Per checklist item:

```bash
python3 <skill-root>/scripts/goal_state.py evidence \
  --workspace "<path>" --index <n> --text "<evidence summary>"
```

4. Optional audit file: `<project-root>/.agent/goals/goal_<slug>_audit.md`

No success claims without command or file proof.

## Phase 6: Close

When all `<output>` items pass:

```bash
python3 <skill-root>/scripts/goal_state.py complete --workspace "<path>"
```

Report: deliverables, audit path, cleared active goal.

To abandon: `goal_state.py clear --workspace "<path>"`

## Phase 7: Update Context Cache

After clarification (and optionally after completion):

1. Merge new key files, tech stack, git summary, decisions into `.agent/goal-context.md`
2. Update `Last updated` timestamp
3. Keep file concise (<500 lines); archive old entries when needed

## goal_state.py

| Command | Purpose |
|---------|---------|
| `set --workspace PATH --xml-file FILE` | Activate goal |
| `show --workspace PATH` | Print JSON state |
| `evidence --workspace PATH --index N --text "..."` | Mark item done with proof |
| `complete --workspace PATH` | Close when checklist complete |
| `clear --workspace PATH` | Delete state file |

Default state directory: `~/.agent/goal-state/` (override with env `GOAL_STATE_DIR`).

## Anti-Patterns

| Do not | Do instead |
|--------|------------|
| Skip search on「简单任务」| Minimum L0 + L2 |
| Subjective output（用户满意）| File/command checks |
| Implement before user confirms | HARD GATE |
| Mark complete without audit | Phase 5 table + evidence |
| Re-search stable project facts every run | Read cache first |

## References

| File | Purpose |
|------|---------|
| `references/context-search-playbook.md` | Layered search strategy |
| `references/search-strategies.md` | Command templates |
| `references/goal-xml-template.md` | XML format |
| `references/goal-quality-rubric.md` | Self-check scoring |
| `references/completion-audit.md` | Evidence-based close |
| `references/context-cache-template.md` | Cache file template |
| `references/example-goals.md` | Full examples |

## File Map

```text
goal-clarify/
├── SKILL.md
├── README.md
├── references/
├── examples/
└── scripts/
    └── goal_state.py
```
