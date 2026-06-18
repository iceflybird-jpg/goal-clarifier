# Search Strategies — Context Search Strategy & Command Templates

## Search Priority

1. **Local code** > 2. **Git history** > 3. **Memory/notes** > 4. **Past conversations** > 5. **Web**

## 1. Local Code Search

### 1.1 Filename Search (Glob)
```
# By extension
**/*.{ts,tsx,js,jsx}     # Frontend
**/*.{py,go,rs}          # Backend
**/*.{json,yaml,yml,toml} # Config

# By directory/module
**/src/**/*              # Source code
**/test*/**/*            # Tests
**/docs/**/*             # Documentation

# By keyword (filename contains)
**/*{auth,login,user}*   # Auth-related
**/*{api,route,handler}* # API-related
```

### 1.2 Content Search (Grep)
```
# Keywords
pattern: "TODO|FIXME|HACK|XXX"  # Pending items & known issues
pattern: "function|class|def "  # Function/class definitions
pattern: "import|require|from"  # Dependencies

# Specific patterns
pattern: "router\.(get|post|put|delete)"  # API routes
pattern: "describe\(|test\(|it\("          # Test cases
```

### 1.3 Key File Reads
```
- README.md / README.*           # Project description
- package.json / requirements.txt / go.mod / Cargo.toml  # Dependencies
- *.config.* / .env.example      # Config
- src/index.* / src/main.*       # Entry point
- docs/                          # Docs directory
```

## 2. Git History Search

### 2.1 Understand Current State
```bash
git status                          # Current changes
git log --oneline -30               # Recent commits
git branch -a                       # All branches
git diff HEAD~5 --stat              # Recent 5 commits change summary
```

### 2.2 Search History by Keyword
```bash
git log --grep="<keyword>" --oneline -20
git log --grep="<keyword>" -p        # With code changes
git log --since="2 weeks ago" --oneline
```

### 2.3 Search File History
```bash
git log --oneline -- <file-path>    # A file's change history
git log -p -- <file-path> | head -100  # Recent change details
```

### 2.4 By Author/Time
```bash
git log --author="<name>" --oneline -20
git log --since="2026-01-01" --until="2026-06-01" --oneline
```

## 3. Project Memory Search

### 3.1 Current Project Memory
```
<project-root>/.agent/memory/
├── MEMORY.md              # Long-term project notes
├── 2026-06-18.md          # Today's log
├── 2026-06-17.md          # Yesterday's log
└── ...
```

### 3.2 User-Level Memory
```
~/.agent/MEMORY.md     # Cross-project user preferences
```

### 3.3 Read Strategy
- Read MEMORY.md first (long-term notes, high info density)
- Then read the last 3-5 days' daily logs
- Use Grep in the memory directory to search for keywords

## 4. Past Conversation Search

### 4.1 Tool Availability

The specific tool or method depends on the host agent environment:
- If the agent provides a conversation search API/tool, use it with a self-contained query
- If not available, skip this step or ask the user if they have relevant context from past sessions

### 4.2 Query Construction Principles
- **Self-contained**: the query must be independently understandable (the tool cannot access the current conversation)
- **Include context**: restate the current task, explain what to look for and why
- **Multi-dimensional**: include both technical and business dimensions

### 4.3 Query Templates
```
# Find technical decisions
"User is currently working on X feature. Find previous discussions about X's tech selection, architecture decisions, encountered problems."

# Find project background
"User is advancing project Y. Find previous discussions about Y's requirements, product direction, user feedback."

# Find code-related info
"User wants to modify file Z. Find previous discussions about Z's implementation, known issues, refactoring plans."
```

### 4.4 Time Range
```
start_date: "2026-01-01"  # ISO 8601
end_date: "2026-06-18"
limit: 10                  # Default 5, adjustable
```

## 5. User Notes Search (Optional, User-Configured)

If the user has configured a notes path (via memory or explicit告知 in conversation), search it:
```
# User must specify notes path in ~/.agent/MEMORY.md or in the current conversation
# Example: user says "my project notes are in ~/Documents/notes/"
# Then execute:
grep -rli "<keyword>" <user-specified notes path>/ 2>/dev/null | head -20
```

**Note**: this skill does not include any hardcoded personal paths. Notes search is an **optional feature** that requires the user to actively configure the path.

## 6. Web Search (On Demand)

### 6.1 Trigger Conditions
- Requirement involves external tech/API/framework
- Needs latest info (beyond knowledge cutoff date)
- Needs best practices / open-source solution references

### 6.2 Search Strategy
```
WebSearch:
  query: main query
  query_keyword_groups: [multi-angle keyword groups]  # Use for comparisons/multi-dimensional

WebFetch:
  url: specific documentation/page URL
  prompt: information to extract
```

## Search Execution Principles

1. **Parallel first**: independent searches in the same message for parallel execution
2. **Broad to narrow**: start with broad Glob/Grep, then Read key files closely
3. **Association tracking**: from an import/reference in one file, trace to another
4. **Time dimension**: git log and conversation search both consider time range
5. **Cut losses promptly**: if a search type yields no results, don't retry repeatedly; move to the next type
6. **Record sources**: annotate information sources in `<context>` (which file, which conversation, which URL)
