---
name: aitmpl-downloader
description: Download Claude Code templates from aitmpl.com (GitHub API). Use PROACTIVELY to search and install agents, commands, skills, mcps, settings, hooks, and plugins.
---

# aitmpl.com Template Downloader

Download Claude Code templates from aitmpl.com using GitHub API for real-time data.

## Architecture

```
aitmpl-downloader/
├── SKILL.md                 # This file - overview and commands
├── scripts/download.py      # Download script (GitHub API)
└── categories/              # Category-specific guides
    ├── agents.md
    ├── commands.md
    ├── skills.md
    ├── mcps.md
    ├── settings.md
    ├── hooks.md
    └── plugins.md
```

## Agent

Use `category-downloader` agent to download by category:

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.
           Category: ${category}
           Requirements: ${requirements}`
})
```

## Categories

| Category | Output Directory | Guide |
|----------|-----------------|-------|
| agents | `.claude/agents/` | categories/agents.md |
| commands | `.claude/commands/` | categories/commands.md |
| skills | `.claude/skills/` | categories/skills.md |
| mcps | `.mcp.json` (merge) | categories/mcps.md |
| settings | `.claude/settings.local.json` | categories/settings.md |
| hooks | `.claude/settings.local.json` | categories/hooks.md |
| plugins | Multiple locations | categories/plugins.md |

## Commands

```bash
# List all items in a category
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category agents --json

# Search across categories
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --json
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category skills --json

# Download specific item
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/agents

# View available categories
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py categories

# Clear cache (get fresh data from GitHub)
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py clear-cache
```

## GitHub API Source

- **Base URL**: `https://api.github.com/repos/davila7/claude-code-templates/contents`
- **Cache**: 15 minutes (use `--no-cache` to bypass)
- **Rate Limit**: Set `GITHUB_TOKEN` env var for higher limits

## GitHub Paths

| Category | GitHub Path |
|----------|-------------|
| agents | `cli-tool/components/agents` |
| commands | `cli-tool/components/commands` |
| skills | `cli-tool/components/skills` |
| mcps | `cli-tool/components/mcps` |
| settings | `cli-tool/components/settings` |
| hooks | `cli-tool/components/hooks` |
| plugins | `.claude-plugin` |

## Output Format (JSON)

```json
[
  {
    "category": "agents",
    "name": "frontend-developer",
    "description": "Agents from development-team",
    "path": "cli-tool/components/agents/development-team/frontend-developer.md",
    "subcategory": "development-team",
    "download_url": "https://raw.githubusercontent.com/..."
  }
]
```

## Workflow

1. **Read category guide** - Understand available items and mapping
2. **List/Search** - Find matching templates
3. **Download** - Get files to local project
4. **Verify** - Confirm installation
