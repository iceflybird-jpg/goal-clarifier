# Context Search Playbook

Run **Phase 1** of `goal-clarify` after Phase 0 cache read. Prefer parallel tool calls. Every fact in `<context>` must carry a source prefix (see `goal-xml-template.md`).

**Search scope** = full search − content already in `.agent/goal-context.md`

## Stop Condition

Stop when:

- You can fill `<task>` without guessing user intent
- `<context>` has ≥5 sourced bullets (≥8 for large or cross-repo work)
- Remaining unknowns are in `<constraints>` as assumptions or blocked on ≤2 user questions

Do not search endlessly; note low-impact gaps as assumptions.

## Search Priority

1. Cache (Phase 0) → 2. Local code/docs → 3. Git → 4. Memory → 5. Past conversations → 6. Web

Command templates: `references/search-strategies.md`

## Layer L0 — User Intake

| Action | Notes |
|--------|-------|
| Restate request in one sentence | — |
| List ambiguities (scope, deliverable, audience, deadline) | — |
| Note explicit paths, repos, skill names | — |

## Layer L1 — Project Documents

Search under `<project-root>`:

| Typical paths | When |
|---------------|------|
| `README.md`, `docs/`, `doc/` | Project overview, architecture |
| `Doc/`, `docs/spec/`, `requirements/` | Formal specs if present |
| `CHANGELOG*`, `*.md` in root | Recent decisions |

```text
Grep keywords from user request
Glob **/*<keyword>*
Read top 2–3 matching files (sections only)
```

## Layer L2 — Workspace Rules

| File | Why |
|------|-----|
| `.cursorrules`, `AGENTS.md`, `CLAUDE.md` | Compliance, directory conventions |
| `.cursor/rules/**` | Host-specific rules |

Always scan L2 when rules files exist.

## Layer L3 — Code & Tests

```text
Glob: **/*.{ts,tsx,js,py,go,rs} by relevance
Grep: symbols, env vars, TODO/FIXME, route definitions
SemanticSearch: "how does X work" in scoped directory
Read: package.json / go.mod / pyproject.toml, entry files, configs
```

Focus on modules related to the request keyword; avoid full-repo reads.

## Layer L4 — Git (read-only)

Run in the repo that owns the work:

```bash
git status -sb
git log --oneline -20
git log --grep="<keyword>" --oneline -10
git branch -vv
git diff HEAD~5 --stat   # if useful
```

Capture: branch, recent related commits, uncommitted changes.

## Layer L5 — Agent Memory & Transcripts

**Project memory:**

```text
<project-root>/.agent/memory/MEMORY.md
<project-root>/.agent/memory/*.md (recent daily logs)
```

**User memory:** `~/.agent/MEMORY.md`

**Past conversations** (if host provides search):

- Self-contained query with task context
- Time-bounded when possible
- Host-specific paths (e.g. agent transcript folders) — only if documented by host

## Layer L6 — Web (optional)

When the task needs external APIs, frameworks, or facts beyond the repo:

- Official docs first
- Cite URLs in `<context>` as `[web] URL: summary`

## Mapping Results → XML

| Finding | Tag |
|---------|-----|
| User's executable ask | `<task>` |
| Background, paths, history, references | `<context>` |
| Out of scope, compliance, assumptions | `<constraints>` |
| Pass/fail checks | `<output>` |

## Parallel Batch Example

For one fuzzy request, launch together:

1. Read `.agent/goal-context.md` + `README.md`
2. Grep `<project-root>` for keywords
3. Read workspace rules if present
4. SemanticSearch or Grep in likely code dirs
5. `git log -15` + `git status`
6. Grep memory / transcripts if available

Then synthesize XML in one pass.

## After Search

Update `.agent/goal-context.md` (Phase 7) with new key files, stack, git summary, decisions.
