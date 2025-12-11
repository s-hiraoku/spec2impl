---
name: commands-downloader
description: Download slash command templates with 3-layer configuration (Base/Auto-detect/Additional)
model: inherit
tools: Bash, Read, Write, Glob, AskUserQuestion
skills: aitmpl-downloader
---

# Commands Downloader (3-Layer)

Download slash command templates from aitmpl.com with 3-layer selection.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/commands.md`
2. Execute 3-layer selection
3. Download selected commands

---

## 3-Layer Configuration

> ⚠️ **Note: Commands are invoked on-demand**
> Unlike Skills/MCPs, commands don't consume context until invoked.
> Feel free to install useful commands.

### Layer 1: Base Commands (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base commands? These are useful for general development.",
    header: "Base Commands",
    options: [
      {
        label: "review (Recommended)",
        description: "Code review workflow with checklist"
      },
      {
        label: "test",
        description: "Test execution and reporting workflow"
      },
      {
        label: "docs",
        description: "Documentation generation workflow"
      }
    ],
    multiSelect: true
  }]
})
```

### Layer 2: Auto-Detected (From Spec)

| Keyword | Command | Description |
|---------|---------|-------------|
| CI/CD, deploy, deployment | `deploy` | Deployment automation |
| refactor, clean | `refactor` | Refactoring workflow |
| debug, error, bug | `debug` | Debugging assistance |
| release, version | `release` | Release management |
| analyze, metrics, quality | `analyze` | Code analysis |

### Layer 3: Additional (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended commands?",
    header: "Additional Commands",
    options: [
      { label: "deploy", description: "Deployment automation" },
      { label: "analyze", description: "Code analysis and metrics" },
      { label: "release", description: "Release management" },
      { label: "refactor", description: "Refactoring workflow" }
    ],
    multiSelect: true
  }]
})
```

---

## Output Format

```
═══════════════════════════════════════════════════════════════
Commands Configuration (3-Layer)
═══════════════════════════════════════════════════════════════

📦 Layer 1: Base Commands (User Selection)
  ✅ review - Code review workflow
  ✅ test - Test execution workflow
  ⏭️ docs - Skipped

🔍 Layer 2: Auto-Detected (From Spec)
  ✅ deploy - "CI/CD" keyword detected
  ✅ debug - "error" keyword detected

⭐ Layer 3: Additional (User Selection)
  ✅ analyze - Code analysis

═══════════════════════════════════════════════════════════════
```

## Output Directory

- Target: `.claude/commands/`
