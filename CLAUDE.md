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

# Slash command usage in Claude Code
/spec2impl docs/                    # From specification documents
/spec2impl --detect-stack           # From project files (package.json, etc.)
/spec2impl docs/ --detect-stack     # Both: spec + project detection (merged)
```

## Architecture

### Two-Part System

1. **CLI Installer** (`src/cli.ts`, `src/installer.ts`)
   - Copies `templates/.claude/` to user's project
   - Manages spec2impl-owned files (always updates) vs user files (skips unless --force)
   - Published as npm package

2. **Claude Code Integration** (`templates/`)
   - Slash command: `.claude/commands/spec2impl.md` — orchestrates the 13-step workflow
   - Sub-agents in `.claude/agents/spec2impl/` — each handles one step
   - Skills in `.claude/skills/spec2impl/` — aitmpl-downloader, skill-creator, ux-psychology

### spec2impl Workflow (13 Steps)

When user runs `/spec2impl docs/` or `/spec2impl --detect-stack` in Claude Code:

```
Step 1:  spec-analyzer          → Parse specs, extract APIs/models/constraints (if spec provided)
Step 2:  project-stack-detector → Detect tech stack from project files (if --detect-stack)
Step 3:  tech-stack-expander    → Web search + user questions to expand tech stack
Step 4:  skills-downloader      → Download skills from aitmpl.com (3-layer selection)
Step 5:  agents-downloader      → Download agents from aitmpl.com (3-layer selection)
Step 6:  commands-downloader    → Download commands from aitmpl.com (3-layer selection)
Step 7:  mcps-downloader        → Download MCPs, configure .mcp.json (3-layer selection)
Step 8:  settings-downloader    → Configure .claude/settings.local.json (3-layer selection)
Step 9:  Deploy bundled         → Deploy ux-psychology for UI/frontend projects
Step 10: task-list-generator    → Extract/generate tasks → docs/TASKS.md
Step 11: rules-generator         → Generate .claude/rules/spec2impl.md
Step 12: harness-guide-generator → Generate docs/HARNESS_GUIDE.md
Step 13: Cleanup                → Optionally remove spec2impl files
```

### Key Sub-Agents

| Agent | Purpose |
|-------|---------|
| `spec-analyzer` | Parse specifications, extract APIs/models/tech stack |
| `project-stack-detector` | Detect tech stack from project files (package.json, etc.) |
| `tech-stack-expander` | Web search + user questions to expand and confirm tech stack |
| `*-downloader` (x5) | Download components from aitmpl.com (skills, agents, commands, mcps, settings) |
| `marketplace-plugin-scout` | **WebSearch** for plugins from aitmpl.com, GitHub, npm |
| `aitmpl-downloader` | Skill for downloading templates from aitmpl.com marketplace |

### Managed vs User Files

The CLI distinguishes between:
- **spec2impl-managed paths** (`commands/spec2impl.md`, `agents/spec2impl/`, `skills/skill-creator/`) — always updated on reinstall
- **User files** — skipped unless `--force`

## Key Design Decisions

- Sub-agents always use **Web Search** for plugin discovery (no hardcoded lists)
- `marketplace-plugin-scout` must have `WebSearch` and `WebFetch` in its tools
- Skills Generator and MCP Configurator call `marketplace-plugin-scout` directly (not through `marketplace`)
- All agent files use YAML frontmatter with `name`, `description`, and `tools`
