---
name: goal-clarifier
description: "Transform vague requirements into clear, executable, and verifiable structured goals. Proactively searches for context (code, git history, past conversations, project memory, web), and maintains a context cache to avoid starting from scratch every time. Outputs a Goal organized with XML tags (task/context/constraints/output). Similar to Claude Code's /goal, but does deeper requirements clarification and context gathering before execution. Triggers: clarify requirements, define goal, goal, break down task, requirement to goal."
version: 1.2.0
author: Nova
---

# Goal Clarifier — Vague Requirement → Clear Goal

> Inspired by Claude Code's `/goal` philosophy of "goal-driven + measurable end-state", but applied **before execution** to do deeper requirements clarification and comprehensive context gathering.
> Core belief: **A well-defined problem is half-solved.**
> Core mechanism: **Context Cache** — project knowledge accumulates continuously; the second run is much faster than the first.

## When to Use

Use this skill when the user gives a **vague, incomplete, or ambiguous** requirement that needs to be clarified into a goal that AI (or a human) can directly execute and objectively verify.

**Trigger signals:**
- User says "help me build X", "I want Y", "implement Z" but details are insufficient
- The requirement is a single sentence, missing background, constraints, or acceptance criteria
- The user expects the AI to "figure it out" before executing
- Explicit triggers: `clarify requirements`, `define goal`, `goal`, `goal-clarifier`, `requirement to goal`, `break down task`

**Not applicable:**
- User has already provided a complete, clear, directly executable requirement → execute directly
- Pure Q&A, information lookup → answer directly

---

## Core Philosophy

| Principle | Description |
|-----------|-------------|
| **Context is king** | Vague requirements are often not vague in themselves, but missing context. Exhaustively search first, then make judgments. |
| **Continuous context accumulation** | Every search result is persisted to cache; next run reads from cache instead of starting over. |
| **Measurable end-state** | Inspired by `/goal`: a goal must have an **objectively verifiable end-state**; "done" and "optimized" are not acceptable. |
| **Executor-evaluator separation** | The output `<output>` is the acceptance criteria for the "evaluator"; separated from `<task>` (the task for the "executor"). |
| **Boundaries = value** | `<constraints>` explicitly states "what NOT to do", which is more important than "what to do". Prevents scope creep. |
| **Don't bother the user** | Context search must be proactive and thorough. Only ask the user when truly critical information is missing. |

---

## Context Cache Mechanism ★ Core Feature

### Design Motivation

Searching code, git history, and conversation history from scratch every time is wasteful (tokens and time). But project knowledge is stable — file structure, tech stack, and key decisions don't change every time.

**Solution**: the skill maintains a **project-level context cache file**. Every run reads the cache first (fast), and only searches for information not in the cache or potentially stale (targeted and minimal).

### Cache File Locations

| Level | Path | Purpose |
|-------|------|---------|
| Project-level | `<project-root>/.agent/goal-context.md` | File structure, tech stack, key files, historical decisions for the current project |
| User-level | `~/.agent/goal-context.md` | Cross-project user preferences, common tech choices, work habits |

`<project-root>` is the agent session's working directory root.

### Cache File Format

```markdown
# Goal Context Cache

> Automatically maintained by goal-clarifier skill. Avoid manual edits.
> Last updated: YYYY-MM-DD

## Project Structure
- `<project-root>/` — workspace root
- `<project-root>/README.md` — project description
- `<project-root>/src/` — [to fill: language, framework, main modules]
- `<project-root>/tests/` — test directory
- `<project-root>/docs/` — docs directory (if any)
- `<project-root>/config/` — config directory (if any)

---

## Tech Stack
- **Language**: [to fill]
- **Framework**: [to fill]
- **Dependency management**: [to fill, e.g. package.json / requirements.txt / go.mod]
- **Testing**: [to fill]
- **Build/deploy**: [to fill]
- **APIs/services**: [to fill]

---

## Key Files
- `README.md` — project description
- `package.json` / `requirements.txt` — dependency list

---

## Git Summary
- **Current branch**: [to fill]
- **Recent commit themes**:
  - [to fill: last 5-10 commit subject lines]
- **Frequently changed files** (last 30 days):
  - [to fill]

---

## Past Decisions
- [YYYY-MM-DD] [decision] — [reason]

---

## User Preferences (user-level cache only)
- **Tech preferences**: [to fill]
- **Workflow preferences**: [to fill, e.g.: give results directly, compare multiple options, pilot before full rollout]
- **Communication style**: [to fill]

---

## Cache Metadata
- **Created**: YYYY-MM-DD
- **Last updated**: YYYY-MM-DD
- **Update count**: 0
- **Next full refresh**: YYYY-MM-DD (created/updated + 7 days)
```

See `references/context-cache-template.md` for the full template.

### Cache Update Strategy

| Timing | Action |
|--------|--------|
| **After each goal clarification** | Append/merge newly acquired context into the cache |
| **Project structure change detected** | Re-scan file structure, update `Project Structure` |
| **New high-frequency files in git history** | Update `Git Summary` |
| **User explicitly corrects** | Immediately update the corresponding field |

### Cache Read Strategy

```
This search scope = full search − cache-covered content

Specifically:
- Cache has Project Structure → Skip full Glob scan; only Grep for requirement keywords
- Cache has Tech Stack → Skip full dependency file read; only check for changes
- Cache has Git Summary → git log only searches recent N entries + requirement-keyword-related commits
- Cache stale (> 7 days since last update) → Trigger a full refresh
```

---

## Workflow

### Phase 0: Read Context Cache (Context Cache Warm-up) ★ New

**Goal**: Quickly establish baseline context; avoid redundant searches.

```
1. Read <project-root>/.agent/goal-context.md (if exists)
2. Read ~/.agent/goal-context.md (user-level, if exists)
3. Based on cache content, formulate targeted search plan (only search cache gaps or potentially stale parts)
```

**Cache miss** (first time using this project): proceed to Phase 1 full search, then write to cache after completion.

---

### Phase 1: Context Search (Context Gathering) ★ Core

**Goal**: Collect background information related to the requirement without disturbing the user.

**Search scope = full search − cache-covered content** (see Phase 0).

#### 1.1 Current Working Directory Code Search
```
- Glob: search by file name patterns (**/*.ts, **/*.py, **/config.*, etc.)
  Tip: search README/package.json etc. first, then precise search by requirement keywords
- Grep: search keywords, function names, class names, TODO, FIXME in file contents
- Read: read key files (README, package.json, config files, entry files)
```

#### 1.2 Git History Search
```bash
# Recent commits (understand what the project is currently doing)
git log --oneline -30

# Search commit history by keyword
git log --grep="<requirement keyword>" --oneline -20

# Recent code changes
git diff HEAD~5 --stat

# Current branch and uncommitted changes
git status
git diff --stat
```

#### 1.3 Past Conversation Search
```
Search past conversation history for relevant context.
The specific tool or method depends on the host agent environment:
- If the agent provides a conversation search tool/API, use it with a self-contained query
- If not available, skip this step

Query construction principles:
- Self-contained: the query must be independently understandable
- Include context: restate the current task, explain what to look for and why
- Multi-dimensional: include both technical and business dimensions
```

#### 1.4 Project Memory Search
```
- Read <project-root>/.agent/memory/MEMORY.md (if exists)
- Read recent daily logs (YYYY-MM-DD.md) in the memory directory (if exists)
- Read ~/.agent/MEMORY.md (user-level long-term memory, if exists)
```

#### 1.5 User Notes Search (Optional, user-configured)

If the user has configured a notes path (via memory or explicit告知), search it:
```
# User must specify notes path in ~/.agent/MEMORY.md or in the current conversation
# Example: user says "my project notes are in ~/Documents/notes/"
# Then execute:
grep -rli "<requirement keyword>" <user-specified notes path>/ 2>/dev/null | head -20
```

**Note**: this skill does not include any hardcoded personal paths. Notes search is an **optional feature** that requires the user to actively configure the path.

#### 1.6 Web Search (on demand)
```
- Only when the requirement involves external tech, APIs, or latest solutions
- Search official docs, open-source projects, best practices
```

**Search strategy:**
- **Cache first**: Phase 0 already read cache; Phase 1 only fills gaps
- **Parallel first**: independent search commands go in the same message for parallel execution
- **Broad to narrow**: start with broad searches (Glob/Grep), then read key files closely
- **Association tracking**: from a reference in one file, trace to another related file
- **Time dimension**: git log by time; conversation search by time range

---

### Phase 2: Requirement Understanding & Reframing

**Goal**: Based on collected context, reframe the vague requirement into a clear goal.

**Thinking framework (internal, not output):**

1. **What does the user really want?** (not the literal words, but the intent)
   - Surface requirement vs. deep requirement
   - The business/product goal behind this requirement

2. **What is known? What is unknown?**
   - What information was obtained from context search
   - What critical information is still missing

3. **Is there a better direction?**
   - As a product partner, is there a better solution?
   - Is the user solving the "wrong problem"?

4. **How to verify completion?**
   - What state counts as "done"
   - How to objectively measure it

**Key decision points:**
- If context is sufficient → directly proceed to Phase 3 output
- If **critical** information is missing (cannot define acceptance criteria) → ask the user precise questions, **only ask what's necessary**
- If the user's direction seems problematic → **directly offer a different opinion** (this is the product partner's responsibility)

---

### Phase 3: Structured Output

**Output format: strictly use the following XML tags.**

```xml
<task>
<!-- Goal/Task: transform the requirement into a clear, executable goal -->

[Define the core goal in one sentence]

[Detailed task description]
- Specifically what to do
- Why do it (business/product intent)
- Expected final state
</task>

<context>
<!-- Background/Context: all relevant background information, as detailed as possible -->

## Project Background
[Project info obtained from context search]

## Related Code/Files
[Involved file paths, modules, functions, with brief descriptions]

## History
[Git history, past conversations, past decisions]

## Known Constraints
[Tech stack, dependencies, time, resource limits already known]

## Related References
[External materials found, open-source projects, best practices]
</context>

<constraints>
<!-- Constraints/Requirements: clear boundaries, including "what to do" and "what NOT to do" -->

## Must Do
- [Required criteria]

## Must NOT Do
- [Explicitly prohibited scope, prevent scope creep]

## Technical Constraints
- [Tech stack, versions, compatibility, etc.]

## Resource Constraints
- [Time, manpower, token budget, etc.]
</constraints>

<output>
<!-- Acceptance Criteria: objectively verifiable completion standards, inspired by /goal's measurable end-state -->

## Definition of Done
- [ ] [Specific verifiable criterion 1]
- [ ] [Specific verifiable criterion 2]
- [ ] ...

## Verification Method
[How to verify: what command to run, what output to check, what test to pass]

## Termination Condition
- All above acceptance criteria met, OR
- Execution exceeds [N] rounds without completion (prevent infinite loop), OR
- Encounter a clear blocking point requiring human intervention
</output>
```

---

### Phase 4: Confirm & Handoff

After outputting the structured Goal:

1. **Brief explanation**: 2-3 sentences explaining what searches were done and why the goal was defined this way
2. **If there's a different opinion**: directly state where you think there's a better approach
3. **Ask next step**:
   - "Is this Goal accurate? What needs adjustment?"
   - "After confirmation, I can start executing directly."

---

### Phase 5: Update Context Cache (Context Cache Update) ★ New

**Goal**: Write newly acquired knowledge from this search into the cache for next use.

**Must execute:**
```
1. Read existing cache file (if exists)
2. Merge newly acquired project knowledge:
   - Newly discovered key files → append to Key Files
   - Newly understood tech stack info → update Tech Stack
   - Historical decisions related to this requirement → append to Past Decisions
   - Project structure changes → update Project Structure
3. Update "Last updated" timestamp
4. Write back to <project-root>/.agent/goal-context.md
```

**Merge strategy:**
- Append within same field, don't overwrite (preserve history)
- If same file/decision has new info, update the corresponding entry
- Keep file concise (< 500 lines), periodically archive old entries

---

## Quality Checklist (Self-Check Before Output)

Before outputting the structured Goal, **must** pass the following self-check:

- [ ] **Measurable**: every acceptance criterion in `<output>` is objectively verifiable (run command, check output, pass test); cannot be "done", "optimized"
- [ ] **Complete**: `<context>` includes all relevant info obtained from search
- [ ] **Clear boundaries**: `<constraints>` explicitly states "what NOT to do"
- [ ] **Executable**: `<task>` is specific enough for AI to execute directly
- [ ] **No hidden assumptions**: no unverified assumptions buried in the goal (if any, either verify via search or list in constraints as "assumptions to verify")
- [ ] **Loop prevention**: `<output>` includes termination condition
- [ ] **Cache updated**: Phase 5 executed, context persisted

---

## Behavior Guidelines

### Search Behavior
- **Cache first**: read cache first, then decide search scope
- **Thorough but efficient**: exhaustive search, but use parallel commands to reduce round-trips
- **Association thinking**: trace from one clue to another, forming complete context
- **Time dimension**: both git log and conversation search should consider time range

### Communication Behavior
- **Give judgments directly**: if there's a better direction, say it directly; don't just list options
- **Don't bother the user**: search for what can be searched; don't ask
- **Ask precisely**: only ask for truly missing and unsearchable critical info
- **Structured output**: strictly follow XML format for easy AI subsequent reading

### Product Partner Behavior
- **Question surface requirements**: user says "add a feature", first think "do we really need this feature"
- **Offer better solutions**: if a better direction is seen, proactively propose it
- **Honest feedback**: if the requirement itself has problems, directly point them out

---

## Example

**User input (vague):**
> "Help me optimize the AI generation feature of my app"

**Execution flow:**

1. **Phase 0**: read cache (if available) → quickly understand project background
2. **Phase 1**: targeted search (cache already has tech stack → skip; cache missing "generation feature" related code → focus search there)
3. **Phase 2**: reframe requirement → "optimize" is too vague; based on context, judge it means "end-to-end generation quality"
4. **Phase 3**: output structured Goal
5. **Phase 4**: confirm
6. **Phase 5**: write this search result into cache

---

## References

- [references/search-strategies.md](references/search-strategies.md) — detailed search strategies and command templates
- [references/goal-quality-rubric.md](references/goal-quality-rubric.md) — Goal quality scoring criteria
- [references/example-goals.md](references/example-goals.md) — complete example set
- [references/context-cache-template.md](references/context-cache-template.md) — context cache file template

---

## Design Notes

This skill's design is inspired by:
- **Claude Code `/goal`**: executor-evaluator separation, measurable end-state, infinite loop prevention
- **Anthropic Building Effective Agents**: Prompt Chaining, Evaluator-Optimizer patterns
- **Product management practices**: Definition of Done, acceptance criteria, scope management
- **Incremental learning**: context cache mechanism, avoid repeated searches, continuously improve efficiency

Difference from `/goal`:
- `/goal` is an **in-execution** self-evaluation loop; this skill is **pre-execution** requirement clarification
- `/goal` assumes the goal is already clear; this skill solves the "goal not clear" problem
- The two can be chained: first use this skill to clarify a clear Goal, then use a `/goal`-style loop for execution

**Version history:**
- v1.2.0: Generalized format — removed all WorkBuddy-specific terms and paths; now usable as a universal agent skill
- v1.1.0: added Context Cache mechanism (Phase 0 + Phase 5); removed hardcoded personal paths
- v1.0.0: initial version
