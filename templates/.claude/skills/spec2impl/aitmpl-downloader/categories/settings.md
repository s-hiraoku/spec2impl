# Settings Category Guide

Download Claude Code settings presets from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/settings`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/settings`

## Output Directory

- Target: `.claude/settings.local.json` (merge with existing)

## Available Settings Categories

| Category | Description | Examples |
|----------|-------------|----------|
| model | Model selection | use-haiku.json, use-sonnet.json, use-opus.json |
| statusline | Status line customization | minimal-statusline.json, detailed-statusline.json |
| permissions | Permission presets | auto-approve.json, strict-permissions.json |
| environment | Environment configs | development.json, production.json |

## Commands

```bash
# List all settings
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category settings --json

# Search settings
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category settings --json

# Download specific settings
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude
```

## Settings Structure

```json
{
  "model": "claude-sonnet-4-20250514",
  "permissions": {
    "allow": ["Bash(*)", "Read", "Write"],
    "deny": []
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

## Spec Mapping

| Project Type | Recommended Settings |
|--------------|---------------------|
| Quick prototyping | use-haiku.json |
| Production apps | use-sonnet.json |
| Complex analysis | use-opus.json |
| CI/CD automation | auto-approve.json |
| Security-sensitive | strict-permissions.json |

## Settings Merge Strategy

When downloading, settings are deep-merged:
- **Objects**: Recursive merge (new values override)
- **Arrays**: Concatenate (deduplicated)
- **Primitives**: New value wins

Example merge:
```json
// Existing
{ "model": "claude-sonnet", "permissions": { "allow": ["Read"] } }

// Downloaded
{ "permissions": { "allow": ["Write"] } }

// Result
{ "model": "claude-sonnet", "permissions": { "allow": ["Read", "Write"] } }
```
