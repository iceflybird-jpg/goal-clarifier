# Completion Audit

Mandatory **Phase 5** before declaring a `goal-clarify` run complete. Evidence before assertions.

## When to Run

- After execution claims all work is done
- Before `goal_state.py complete`
- Before telling the user the task is finished

## Audit Steps

### 1. Parse checklist

```bash
python3 <skill-root>/scripts/goal_state.py show --workspace "<project-root>"
```

Extract each `- [ ]` line from `<output>` in stored `goal_xml` (or from saved XML file).

### 2. Requirement → evidence table

| # | Output criterion | Evidence type | Evidence | Pass? |
|---|------------------|---------------|----------|-------|
| 1 | ... | file / command / url | path or output snippet | Y/N |

**Valid evidence:** `test -f`, passing test command (exit 0), fetchable URL, explicit counts.

**Invalid evidence:**「应该没问题」、unrun tests、subjective judgment without a defined rubric in `<output>`.

### 3. Gap handling

| Situation | Action |
|-----------|--------|
| Any Pass? = N | Return to Phase 4; do NOT complete |
| Criterion ambiguous | Amend goal with user OR define minimal objective check |
| Partial evidence | Keep working until criterion fully satisfied |

### 4. Audit artifact (recommended)

```text
<project-root>/.agent/goals/goal_<slug>_audit.md
```

```markdown
# Goal Completion Audit — <slug>
Date: YYYY-MM-DD
Workspace: <path>

| # | Criterion | Evidence | Pass |
|---|-----------|----------|------|
| 1 | ... | `path` or command | yes |

## Commands run
- `...`

## Result
ALL PASS / BLOCKED
```

### 5. Close goal

Only when **all** rows pass:

```bash
python3 <skill-root>/scripts/goal_state.py complete --workspace "<project-root>"
```

### 6. Record evidence per item

```bash
python3 <skill-root>/scripts/goal_state.py evidence \
  --workspace "<project-root>" --index <n> --text "<summary>"
```

## Task → Artifact Map

Each `<task>` bullet should map to at least one file, command, or observable behavior. If not, work is incomplete or the bullet belongs in `<context>`.
