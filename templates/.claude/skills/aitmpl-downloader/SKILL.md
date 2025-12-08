---
name: aitmpl-downloader
description: Download Claude Code templates (agents, commands, settings, hooks, mcps, skills, plugins) from aitmpl.com. Use when users want to browse, search, or install templates from the aitmpl.com marketplace. Triggers on requests like "download agent from aitmpl", "find security templates", "install MCP from marketplace", or "browse aitmpl.com".
---

# aitmpl.com Template Downloader

Download Claude Code templates from the aitmpl.com marketplace (davila7/claude-code-templates).

## Available Categories

- **agents**: AI specialist agents (security-auditor, frontend-developer, etc.)
- **commands**: Slash commands for specific workflows
- **mcps**: MCP server configurations
- **plugins**: Complete plugin bundles with multiple components
- **settings**: Configuration presets
- **hooks**: Event automation hooks

## Workflow

### Step 1: Search for Templates

Run the download script to find matching templates:

```bash
scripts/download.py search "<query>" [--category <category>]
```

Examples:
```bash
scripts/download.py search "security"              # All security-related
scripts/download.py search "database" --category mcps  # Database MCPs only
scripts/download.py list --category agents         # List all agents
```

### Step 2: Present Options to User

After getting search results, use `AskUserQuestion` to let the user choose:

```
Found N templates matching "<query>":
1. [category] name - description (Plugin: plugin-name)
2. ...

Which would you like to download?
```

### Step 3: Download Selected Items

For agents/commands (file-based):
```bash
scripts/download.py get "<path>" --output .claude/agents
```

Output directories by category:
- agents → `.claude/agents/`
- commands → `.claude/commands/`
- mcps → `.mcp.json` (merge into existing)
- settings → `.claude/settings.local.json`

### Step 4: Post-Download Actions

**For agents/commands**: Confirm file location
**For MCPs**: Show how to add to `.mcp.json`
**For plugins**: List all included components

## Script Reference

| Command | Description |
|---------|-------------|
| `list [--category X]` | List all items, optionally filtered |
| `search <query> [--category X]` | Search by name/description |
| `get <path> [--output DIR]` | Download a file |
| `--json` | Output as JSON (for parsing) |

Categories: `agents`, `commands`, `mcps`, `plugins`, `settings`, `hooks`
