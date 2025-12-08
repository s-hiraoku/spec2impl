---
name: aitmpl-downloader
description: Download Claude Code templates from aitmpl.com. Use PROACTIVELY to search and install agents, commands, mcps, and skills. ALWAYS use this FIRST before web search.
---

# aitmpl.com Template Downloader

Download Claude Code templates from aitmpl.com marketplace.

## PROACTIVE: Use This FIRST

**Before ANY web search, use the download.py script:**

```bash
# Search for templates
python3 .claude/skills/aitmpl-downloader/scripts/download.py search "<query>" --json
python3 .claude/skills/aitmpl-downloader/scripts/download.py search "<query>" --category agents --json

# List all templates in a category
python3 .claude/skills/aitmpl-downloader/scripts/download.py list --category agents --json
python3 .claude/skills/aitmpl-downloader/scripts/download.py list --category mcps --json

# Download a template
python3 .claude/skills/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/agents
```

## Categories

| Category | Output Directory |
|----------|-----------------|
| agents | .claude/agents/ |
| commands | .claude/commands/ |
| mcps | .mcp.json (merge) |
| skills | .claude/skills/ |
| plugins | (contains multiple) |
| settings | .claude/settings.local.json |
| hooks | .claude/hooks/ |

## Commands

```bash
# List
download.py list [--category X] [--json]

# Search
download.py search "<query>" [--category X] [--json]

# Download
download.py get "<path>" [--output DIR]
```

## Output Format (JSON)

```json
[
  {
    "category": "agents",
    "name": "frontend-developer",
    "description": "Agent from nextjs-vercel-pro",
    "path": "./cli-tool/components/agents/development-team/frontend-developer.md",
    "plugin": "nextjs-vercel-pro"
  }
]
```

## Workflow

1. **Search** - Find matching templates
2. **Download** - Get files to local project
3. **Verify** - Confirm installation
