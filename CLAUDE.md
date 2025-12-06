# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

spec2impl generates an **implementation harness** for Claude Code from specification documents. It creates the scaffolding (skills, agents, MCP configuration, task lists) that Claude needs to implement a specification efficiently.

**Core principle:** Web Search First — always search for the latest tools, skills, and patterns before generating anything.

## Commands

```bash
# Development
npm run dev              # Run CLI in development mode (tsx)
npm run build            # Build with tsup (ESM + types)
npm test                 # Run tests with vitest

# Usage (after npm link or npx)
npx spec2impl            # Install templates to current project
npx spec2impl --dry-run  # Preview files without installing
npx spec2impl --force    # Overwrite all existing files
```

## Architecture

### Two-Part System

1. **CLI Installer** (`src/cli.ts`, `src/installer.ts`)
   - Copies `templates/.claude/` to user's project
   - Manages spec2impl-owned files (always updates) vs user files (skips unless --force)
   - Published as npm package

2. **Claude Code Integration** (`templates/`)
   - Slash command: `.claude/commands/spec2impl.md` — orchestrates the 7-step workflow
   - Sub-agents in `.claude/agents/spec2impl/` — each handles one step
   - Skills in `.claude/skills/skill-creator/` — guides skill creation

### spec2impl Workflow (7 Steps)

When user runs `/spec2impl docs/` in Claude Code:

```
Step 1: spec-analyzer      → Parse specs, extract APIs/models/constraints
Step 2: skills-generator   → Search marketplace-plugin-scout, install/generate skills
Step 3: subagent-generator → Web search for patterns, generate project agents
Step 4: mcp-configurator   → Search marketplace-plugin-scout for MCPs, configure .mcp.json
Step 5: task-list-generator → Extract/generate tasks → docs/TASKS.md
Step 6: claude-md-updater  → Merge generated section into CLAUDE.md
Step 7: Cleanup            → Optionally remove spec2impl files
```

### Key Sub-Agents

| Agent | Purpose |
|-------|---------|
| `marketplace-plugin-scout` | **WebSearch** for plugins (skills, MCPs) from GitHub/npm |
| `marketplace` | Install/list/uninstall plugins (delegates search to scout) |
| `skills-generator` | Calls scout to find skills, generates missing ones |
| `mcp-configurator` | Calls scout for MCPs, generates .mcp.json + setup guides |

### Managed vs User Files

The CLI distinguishes between:
- **spec2impl-managed paths** (`commands/spec2impl.md`, `agents/spec2impl/`, `skills/skill-creator/`) — always updated on reinstall
- **User files** — skipped unless `--force`

## Key Design Decisions

- Sub-agents always use **Web Search** for plugin discovery (no hardcoded lists)
- `marketplace-plugin-scout` must have `WebSearch` and `WebFetch` in its tools
- Skills Generator and MCP Configurator call `marketplace-plugin-scout` directly (not through `marketplace`)
- All agent files use YAML frontmatter with `name`, `description`, and `tools`
