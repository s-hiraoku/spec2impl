# MCPs Category Guide

Download MCP (Model Context Protocol) server configurations from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/mcps`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/mcps`

## Output Directory

- Target: `.mcp.json` (merge with existing)

## Available MCP Servers

| MCP Server | Purpose | Provider |
|------------|---------|----------|
| filesystem | File system operations | @modelcontextprotocol |
| postgres | PostgreSQL database access | @modelcontextprotocol |
| sqlite | SQLite database access | @modelcontextprotocol |
| github | GitHub API integration | @modelcontextprotocol |
| slack | Slack integration | @modelcontextprotocol |
| puppeteer | Browser automation | @anthropics |
| brave-search | Web search | community |
| fetch | HTTP requests | @modelcontextprotocol |
| memory | Persistent memory | @modelcontextprotocol |
| google-maps | Google Maps API | community |
| time | Time and timezone | @modelcontextprotocol |

## Commands

```bash
# List all MCPs
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category mcps --json

# Search MCPs
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category mcps --json

# Download specific MCP config
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .
```

## Spec Mapping

| Spec Mentions | Recommended MCPs |
|---------------|-----------------|
| Database/PostgreSQL | postgres |
| SQLite | sqlite |
| File operations | filesystem |
| GitHub integration | github |
| Slack/notifications | slack |
| Browser automation | puppeteer |
| Web search | brave-search |
| API calls | fetch |
| Persistent state | memory |

## MCP Configuration Merge

When downloading, configs are merged into `.mcp.json`:

```json
{
  "mcpServers": {
    "existing-server": { ... },
    "new-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Token Requirements

Some MCPs require API tokens. Document in setup guide:
- `postgres`: DATABASE_URL
- `github`: GITHUB_TOKEN
- `slack`: SLACK_TOKEN
- `brave-search`: BRAVE_API_KEY
