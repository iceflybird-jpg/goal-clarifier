# Goal XML Template

Structured Goal output for `goal-clarify`. Use exactly four top-level tags.

## Canonical Template

```xml
<task>
- [Verb-led outcome: what will exist when done]
</task>

<context>
- [source-type] path or URL: one-sentence fact
- ...
</context>

<constraints>
## Must Do
- ...

## Must NOT Do
- ...

## Technical / Resource
- ...
</constraints>

<output>
## Definition of Done
- [ ] [Verifiable criterion — command, file path, or measurable check]
- [ ] ...

## Verification Method
[Commands or steps to prove each item]

## Termination Condition
- All criteria met, OR
- Blocked on human decision, OR
- N execution rounds without progress (state explicitly)
</output>
```

> **Alias:** `<constrains>` is accepted for backward compatibility; prefer `<constraints>`.

## Field Rules

| Tag | Quality bar |
|-----|-------------|
| `<task>` | 1–3 bullets; verb-led; single theme; no vague "improve" without object |
| `<context>` | Each bullet cites source; ≥5 for non-trivial work |
| `<constraints>` | Explicit out-of-scope; assumptions labeled |
| `<output>` | Every `- [ ]` is pass/fail without subjective judgment |

## Source-Type Prefixes

| Prefix | Meaning |
|--------|---------|
| `[user]` | Current user message |
| `[doc]` | README, docs/, spec files |
| `[rule]` | `.cursorrules`, `AGENTS.md`, host rules |
| `[code]` | Source files, configs |
| `[git]` | git log, branch, diff |
| `[memory]` | `.agent/memory`, goal-context cache |
| `[transcript]` | Past agent conversation |
| `[web]` | External URL |
| `[history]` | Same thread, earlier turns |

## Good vs Bad

**Good `<output>`:**

```xml
- [ ] `npm test` exits 0
- [ ] `src/auth/login.ts` handles invalid password with 401
```

**Bad `<output>`:**

```xml
- [ ] User is happy
- [ ] Looks professional
```

## Presentation

1. Show full XML in the reply.
2. End with: **请确认以上 Goal；确认后开始执行。**
3. Do NOT implement until user confirms (HARD GATE).

## After Approval

```bash
python3 <skill-root>/scripts/goal_state.py set \
  --workspace <project-root> \
  --xml-file <project-root>/.agent/goals/goal_<slug>.xml
```

Proceed to Phase 4 per `SKILL.md`.
