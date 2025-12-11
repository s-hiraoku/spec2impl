---
name: skills-downloader
description: Download skill templates with 3-layer configuration (Base/Auto-detect/Additional)
model: inherit
tools: Bash, Read, Write, Glob, AskUserQuestion
skills: aitmpl-downloader
---

# Skills Downloader (3-Layer)

Download skill templates from aitmpl.com with 3-layer selection.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/skills.md`
2. Execute 3-layer selection
3. Download selected skills

---

## 3-Layer Configuration

> ⚠️ **Warning: Skills consume context window space**
> Each skill is loaded at session start. Select only essential skills.

### Layer 1: Base Skills (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base skills? These are useful for general development.",
    header: "Base Skills",
    options: [
      {
        label: "skill-creator (Recommended)",
        description: "Guide for creating new skills from templates"
      },
      {
        label: "git-commit-helper",
        description: "Git commit message generation with Conventional Commit"
      },
      {
        label: "changelog-generator",
        description: "Auto-generate CHANGELOG from git commits"
      }
    ],
    multiSelect: true
  }]
})
```

### Layer 2: Auto-Detected (From Spec)

| Keyword | Skill | Description |
|---------|-------|-------------|
| pdf, report, document | `pdf-anthropic` | PDF processing |
| word, docx | `docx` | Word document processing |
| excel, xlsx, spreadsheet | `xlsx` | Excel processing |
| test, testing, e2e, qa | `webapp-testing` | Web app testing |
| mcp, protocol | `mcp-builder` | MCP server building |
| zapier, automation, webhook | `zapier-workflows` | Zapier integration |
| theme, color, ui, design | `theme-factory` | UI theme generation |
| slack, notification, gif | `slack-gif-creator` | Slack GIF creation |

### Layer 3: Additional (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended skills?",
    header: "Additional Skills",
    options: [
      { label: "content-research-writer", description: "Content research and SEO" },
      { label: "theme-factory", description: "UI theme generation" },
      { label: "pdf-anthropic", description: "PDF processing" },
      { label: "mcp-builder", description: "MCP server building" }
    ],
    multiSelect: true
  }]
})
```

---

## Output Format

```
═══════════════════════════════════════════════════════════════
Skills Configuration (3-Layer)
═══════════════════════════════════════════════════════════════

📦 Layer 1: Base Skills (User Selection)
  ✅ skill-creator - Create new skills guide
  ✅ git-commit-helper - Git commit message generation
  ⏭️ changelog-generator - Skipped

🔍 Layer 2: Auto-Detected (From Spec)
  ✅ webapp-testing - "test" keyword detected
  ✅ pdf-anthropic - "PDF" keyword detected

⭐ Layer 3: Additional (User Selection)
  ✅ theme-factory - UI theme generation

═══════════════════════════════════════════════════════════════
```

## Output Directory

- Target: `.claude/skills/`
