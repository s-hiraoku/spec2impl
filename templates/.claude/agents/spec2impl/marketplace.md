---
name: marketplace
description: Install plugins from GitHub/npm after marketplace-plugin-scout finds them. Manages local plugin registry. Does NOT search - use marketplace-plugin-scout for search.
tools: Bash, Read, Write, Edit, Glob, Grep
---

# Marketplace

Install, list, and uninstall plugins from external sources.

## IMPORTANT: Does NOT Search

- **Search**: Use `marketplace-plugin-scout` (aitmpl.com first, then web)
- **Install/List/Uninstall**: Use this agent

## Actions

### Install

```yaml
Action: install
Source: github:user/repo/path | npm:@scope/package
Type: skill | mcp | agent
TargetName: local-name
```

**Install Locations:**
- skill → `.claude/skills/{name}/`
- mcp → `.mcp.json` + `docs/mcp-setup/`
- agent → `.claude/agents/{name}.md`

### List

```yaml
Action: list
Type: skill | mcp | agent | all
```

### Uninstall

```yaml
Action: uninstall
Name: plugin-name
```

## Source Formats

| Format | Example |
|--------|---------|
| GitHub | `github:user/repo/path` |
| npm | `npm:@scope/package` |
| URL | `https://...` |

## Output

```
✅ Installed: {name}
   Type: {type}
   Location: {path}
```
