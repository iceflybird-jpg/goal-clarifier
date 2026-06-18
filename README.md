# goal-clarifier

A universal AI agent skill that transforms vague requirements into clear, executable, and verifiable structured goals.

> **Inspired by Claude Code's `/goal`**, but applied *before execution* to do deeper requirements clarification and comprehensive context gathering.

## What It Does

When a user gives a vague, incomplete, or ambiguous requirement, this skill:

1. **Proactively searches for context** — code, git history, past conversations, project memory, web — before asking the user.
2. **Maintains a context cache** — project knowledge accumulates across runs; the second use is much faster than the first.
3. **Outputs a structured Goal** in XML tags: `<task>`, `<context>`, `<constraints>`, `<output>`.
4. **Acts as a product partner** — questions surface requirements, offers better directions, and gives judgments (not just options).

## Quick Start

### For Claude Code Users

Copy the `SKILL.md` file to your Claude Code skills directory. The skill will auto-trigger on vague requirements or when you explicitly say `clarify requirements`, `define goal`, etc.

### For OpenClacky Users

Copy the entire `goal-clarifier/` directory (including `references/`) to your OpenClacky skills directory. OpenClacky will pick it up via the `invoke_skill` meta-tool.

### For Other Agents

The `SKILL.md` file is written in a **host-agnostic** format:
- All tool references are generic (e.g., "search past conversations" instead of a specific tool name)
- Path placeholders use `<project-root>` and `~/.agent/` instead of host-specific paths
- The XML output format is parseable by any AI agent

## Structured Output Format

```xml
<task>[Clear, executable goal definition]</task>

<context>[Project background, related code, history, constraints, references]</context>

<constraints>[Must do / Must NOT do / Technical constraints / Resource constraints]</constraints>

<output>[Definition of Done + Verification method + Termination condition]</output>
```

## Context Cache Mechanism ★ Core Feature

The skill maintains a **project-level context cache** at `<project-root>/.agent/goal-context.md`:

- **First run**: full context search → writes cache
- **Subsequent runs**: reads cache first → only searches for new/changed info
- **Result**: significantly fewer tokens and faster response after the first use

See `references/context-cache-template.md` for the cache file format.

## File Structure

```
goal-clarifier/
├── SKILL.md                          # Main skill definition (host-agnostic)
└── references/
    ├── search-strategies.md          # Detailed search strategies & command templates
    ├── goal-quality-rubric.md       # Goal quality scoring criteria (self-check)
    ├── example-goals.md              # Complete example set (3 scenarios)
    └── context-cache-template.md     # Context cache file template
```

## Key Design Decisions

| Decision | Rationale |
|-----------|------------|
| Host-agnostic format | Works with Claude Code, OpenClacky, WorkBuddy, or any agent that supports skill files |
| XML output tags | Structured, parseable by AI; separates task (executor) from output (evaluator) |
| Context cache | Avoids re-searching stable project knowledge; addresses the "starting from scratch every time" problem |
| Product partner behavior | Questions surface requirements and gives judgments; not just a "requirement clarifier" but a thinking partner |

## Comparison with Claude Code `/goal`

| Aspect | `/goal` (Claude Code) | `goal-clarifier` (this skill) |
|---------|----------------------|-------------------------------|
| Timing | During execution (self-evaluation loop) | Before execution (requirement clarification) |
| Assumes | Goal is already clear | Goal is NOT clear yet |
| Core mechanism | Stop Hook + dual model (executor/evaluator) | Context search + cache + structured output |
| Prevents | Premature termination | Vague/vague requirements |
| Can be chained? | Yes, after this skill | Yes, before `/goal`-style execution |

## Examples

See `references/example-goals.md` for complete examples:
- **Feature development**: "Add a shopping cart" → structured Goal with acceptance criteria
- **Optimization task**: "Optimize API response time" → baseline measurement + optimization plan
- **Content creation**: "Write a technical blog post" → audience-aware content brief

## License

MIT

## Author

Nova (product partner AI — inspired by Steve Jobs' Standards + Zhang Xiaolong's restraint + AI's speed)

---

**Feedback / Contributions welcome.** This is a living skill — if you have improvements, open an issue or PR.
