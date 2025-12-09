# Plugins Category Guide

Download complete plugin packages from claude-code-templates.

## GitHub Path

- Source: `.claude-plugin`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/.claude-plugin`

## Output Directory

- Target: Multiple locations (based on plugin contents)

## Available Plugins

| Plugin | Description | Contains |
|--------|-------------|----------|
| nextjs-vercel-pro | Next.js + Vercel development | Agents, Skills, Commands |
| supabase-toolkit | Supabase database integration | Agents, Skills, MCPs |
| testing-suite | Comprehensive testing tools | Agents, Skills, Commands |
| security-pro | Security and compliance | Agents, Skills |
| devops-automation | CI/CD and deployment | Agents, Skills, MCPs |
| documentation-generator | Documentation tools | Agents, Skills, Commands |
| ai-ml-toolkit | AI/ML development | Agents, Skills |
| project-management-suite | Project management | Agents |
| payment-processing | Payment integration | Skills |
| git-workflow | Git workflow tools | Agents, Commands |

## Commands

```bash
# List all plugins
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category plugins --json

# Search plugins
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category plugins --json

# Download plugin manifest
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .
```

## Plugin Structure

Each plugin contains a manifest (`plugin.json`) and components:

```
plugin-name/
├── plugin.json        # Plugin manifest
├── agents/            # Agent definitions
│   ├── agent1.md
│   └── agent2.md
├── commands/          # Slash commands
│   └── command1.md
├── skills/            # Skill definitions
│   └── skill-name/
└── mcpServers/        # MCP configurations
    └── server.json
```

## Plugin Installation

Installing a plugin extracts components to respective directories:

| Component | Destination |
|-----------|-------------|
| agents/ | `.claude/agents/` |
| commands/ | `.claude/commands/` |
| skills/ | `.claude/skills/` |
| mcpServers | `.mcp.json` (merge) |
| hooks | `.claude/settings.local.json` |

## Spec Mapping

| Project Type | Recommended Plugins |
|--------------|-------------------|
| Next.js web app | nextjs-vercel-pro |
| Full-stack with Supabase | supabase-toolkit |
| Test-driven development | testing-suite |
| Security-critical app | security-pro |
| Containerized deployment | devops-automation |
| API documentation | documentation-generator |
| ML/AI project | ai-ml-toolkit |
| E-commerce | payment-processing |

## Note

Plugins are comprehensive packages. Consider downloading individual components (agents, skills) instead if you only need specific functionality.
