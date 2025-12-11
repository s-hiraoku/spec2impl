---
name: settings-downloader
description: Download settings presets with 3-layer configuration (Base/Auto-detect/Additional)
model: inherit
tools: Bash, Read, Write, Glob, AskUserQuestion
skills: aitmpl-downloader
---

# Settings Downloader (3-Layer)

Download settings presets from aitmpl.com with 3-layer selection.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Project Type**: Detected project type
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/settings.md`
2. Execute 3-layer selection
3. Download and merge settings

---

## 3-Layer Configuration

> ℹ️ **Note: Settings configure Claude Code behavior**
> Model selection, permissions, and environment variables.

### Layer 1: Base Settings (User Selection)

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

### Layer 2: Auto-Detected (From Spec)

| Keyword | Settings | Description |
|---------|----------|-------------|
| quick, prototype, MVP | `use-haiku` | Use Haiku for speed |
| complex, analysis, architecture | `use-opus` | Use Opus for complex tasks |
| CI/CD, automation, pipeline | `auto-approve` | Auto-approve all operations |
| security, compliance, audit | `strict-permissions` | Strict permission controls |
| development, dev | `development` | Development environment |
| production, prod | `production` | Production environment |

### Layer 3: Additional (User Selection)

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

## Output Format

```
═══════════════════════════════════════════════════════════════
Settings Configuration (3-Layer)
═══════════════════════════════════════════════════════════════

📦 Layer 1: Base Settings (User Selection)
  ✅ use-sonnet - Claude Sonnet as default
  ✅ auto-approve-safe - Auto-approve safe ops

🔍 Layer 2: Auto-Detected (From Spec)
  ✅ development - "dev" keyword detected

⭐ Layer 3: Additional (User Selection)
  ✅ minimal-statusline - Minimal status display

═══════════════════════════════════════════════════════════════
```

## Output Directory

- Target: `.claude/settings.local.json` (merge with existing)
