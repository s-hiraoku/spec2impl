# Commands Category Guide

Download slash command templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/commands`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/commands`

## Output Directory

- Target: `.claude/commands/`

## Available Commands

| Command | Purpose |
|---------|---------|
| deploy | Deployment automation workflow |
| review | Code review workflow |
| test | Test execution and reporting |
| docs | Documentation generation |
| analyze | Code analysis and metrics |
| refactor | Refactoring workflow |
| debug | Debugging assistance |
| release | Release management |

## Commands

```bash
# List all commands
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category commands --json

# Search commands
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category commands --json

# Download specific command
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/commands
```

## Spec Mapping

| Spec Mentions | Recommended Commands |
|---------------|---------------------|
| CI/CD | deploy |
| Code quality | review, analyze |
| Testing | test |
| Documentation | docs |
| Refactoring | refactor |
| Debugging | debug |
| Release process | release |

## Note

Commands are slash commands that can be invoked with `/command-name` in Claude Code.
Each command file is a markdown file with YAML frontmatter defining the command behavior.
