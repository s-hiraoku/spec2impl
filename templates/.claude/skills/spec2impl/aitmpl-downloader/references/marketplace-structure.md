# aitmpl.com Marketplace Structure

## Data Source

- **Repository**: `davila7/claude-code-templates`
- **Marketplace JSON**: `https://raw.githubusercontent.com/davila7/claude-code-templates/main/.claude-plugin/marketplace.json`

## JSON Structure

```json
{
  "name": "claude-code-templates",
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "keywords": ["keyword1", "keyword2"],
      "commands": ["./path/to/command.md", ...],
      "agents": ["./path/to/agent.md", ...],
      "mcpServers": ["./path/to/mcp.json", ...],
      "settings": { ... },
      "hooks": [{ "event": "...", ... }]
    }
  ]
}
```

## Available Plugins (as of 2024)

| Plugin | Focus | Agents | Commands | MCPs |
|--------|-------|--------|----------|------|
| git-workflow | Git automation | 1 | 5 | 0 |
| supabase-toolkit | Database | 2 | 5 | 3 |
| nextjs-vercel-pro | Frontend | 2 | 7 | 1 |
| testing-suite | QA | 2 | 7 | 0 |
| security-pro | Security | 4 | 4 | 0 |
| ai-ml-toolkit | AI/ML | 5 | 5 | 0 |
| devops-automation | DevOps | 4 | 7 | 3 |
| documentation-generator | Docs | 3 | 5 | 0 |
| performance-optimizer | Performance | 2 | 4 | 0 |
| project-management-suite | PM | 3 | 5 | 2 |

## File Paths

Templates are stored under `./cli-tool/components/`:

```
cli-tool/components/
├── agents/
│   ├── development-team/
│   ├── security/
│   ├── data-ai/
│   └── ...
├── commands/
│   ├── git/
│   ├── database/
│   ├── testing/
│   └── ...
└── mcps/
    ├── database/
    ├── devtools/
    └── ...
```

## Downloading Files

Raw file URL pattern:
```
https://raw.githubusercontent.com/davila7/claude-code-templates/main/{path}
```

Example:
```
https://raw.githubusercontent.com/davila7/claude-code-templates/main/cli-tool/components/agents/security/security-auditor.md
```
