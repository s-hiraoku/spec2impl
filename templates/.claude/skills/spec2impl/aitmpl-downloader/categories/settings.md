# Settings Category Guide

Download Claude Code settings presets from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/settings`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/settings`

## Output Directory

- Target: `.claude/settings.local.json` (merge with existing)

---

## 3-Layer Settings Configuration

> ℹ️ **Note: Settings configure Claude Code behavior**
> Model selection, permissions, and environment variables.

### Layer 1: Recommended Base Settings (User Selection)

Present these via `AskUserQuestion` with multiSelect.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base settings? Configure model and permissions.",
    header: "Base Settings",
    options: [
      {
        label: "use-sonnet (Recommended)",
        description: "Use Claude Sonnet as default model"
      },
      {
        label: "auto-approve-safe",
        description: "Auto-approve safe operations (Read, Glob, Grep)"
      }
    ],
    multiSelect: true
  }]
})
```

**Settings Details:**

| Settings | Description | Use Case |
|----------|-------------|----------|
| `use-sonnet` | Claude Sonnet as default model | Balanced speed and capability |
| `auto-approve-safe` | Auto-approve read operations | Faster workflow |

---

### Layer 2: Auto-Detected Settings (Spec-based)

These settings are **automatically detected** from specification keywords.

| Keywords in Spec | Settings | Description |
|------------------|----------|-------------|
| quick, prototype, MVP, fast | `use-haiku` | Use Haiku for speed |
| complex, analysis, architecture, deep | `use-opus` | Use Opus for complex tasks |
| CI/CD, automation, pipeline, batch | `auto-approve` | Auto-approve all operations |
| security, compliance, audit, strict | `strict-permissions` | Strict permission controls |
| development, dev, local | `development` | Development environment |
| production, prod, deploy | `production` | Production environment |

---

### Layer 3: Additional Recommended Settings (User Selection)

Present these via `AskUserQuestion` based on project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional settings presets?",
    header: "Additional Settings",
    options: [
      { label: "use-haiku", description: "Fast model for quick tasks" },
      { label: "use-opus", description: "Powerful model for complex tasks" },
      { label: "minimal-statusline", description: "Minimal status display" },
      { label: "detailed-statusline", description: "Detailed status display" }
    ],
    multiSelect: true
  }]
})
```

---

## Available Settings Categories

| Category | Description | Examples |
|----------|-------------|----------|
| model | Model selection | use-haiku.json, use-sonnet.json, use-opus.json |
| statusline | Status line customization | minimal-statusline.json, detailed-statusline.json |
| permissions | Permission presets | auto-approve.json, strict-permissions.json |
| environment | Environment configs | development.json, production.json |

## CLI Commands

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

## Settings Merge Strategy

When downloading, settings are deep-merged:
- **Objects**: Recursive merge (new values override)
- **Arrays**: Concatenate (deduplicated)
- **Primitives**: New value wins
