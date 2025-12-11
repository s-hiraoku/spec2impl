---
name: category-downloader
description: Router agent that dispatches to category-specific downloaders
model: inherit
tools: Read
---

# Category Downloader (Router)

Routes download requests to category-specific downloader agents.

## Input Parameters

- **Category**: One of `agents`, `commands`, `skills`, `mcps`, `settings`, `hooks`, `plugins`
- **Search Terms**: Array of keywords from tech-stack-expander
- **Requirements**: Specification requirements

## Routing Table

| Category | Agent | 3-Layer? |
|----------|-------|----------|
| agents | `agents-downloader.md` | ✅ Yes |
| skills | `skills-downloader.md` | ✅ Yes |
| mcps | `mcps-downloader.md` | ✅ Yes |
| commands | `commands-downloader.md` | ✅ Yes |
| settings | `settings-downloader.md` | ✅ Yes |
| hooks | `hooks-downloader.md` | ❌ Simple |
| plugins | `plugins-downloader.md` | ❌ Simple |

## Usage

```typescript
// For agents
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/agents-downloader.md and execute.
           Search Terms: ${searchTerms}
           Requirements: ${requirements}`
})

// For skills
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/skills-downloader.md and execute.
           Search Terms: ${searchTerms}
           Requirements: ${requirements}`
})

// For MCPs
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/mcps-downloader.md and execute.
           Search Terms: ${searchTerms}
           Services: ${detectedServices}
           Requirements: ${requirements}`
})
```

## Output Directories

| Category | Output Directory |
|----------|-----------------|
| agents | `.claude/agents/` |
| commands | `.claude/commands/` |
| skills | `.claude/skills/` |
| mcps | `.mcp.json` (merge) |
| settings | `.claude/settings.local.json` (merge) |
| hooks | `.claude/settings.local.json` (merge) |
| plugins | Multiple locations |
