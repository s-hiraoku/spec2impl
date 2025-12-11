# Skills Category Guide

Download skill templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/skills`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/skills`

## Output Directory

- Target: `.claude/skills/`

---

## 3-Layer Skills Configuration

> ⚠️ **Warning: Skills consume context window space**
>
> Each skill is loaded at session start, so **more skills installed means less available context**.
> - Select only essential skills
> - Less frequently used skills can be added later
> - When in doubt, start with minimum (skill-creator only)

### Layer 1: Recommended Base Skills (User Selection)

Present these via `AskUserQuestion` with multiSelect. Useful for general development.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base skills? These are useful for general development.",
    header: "Base Skills",
    options: [
      {
        label: "skill-creator (Recommended)",
        description: "Guide for creating new skills. Create project-specific skills from templates"
      },
      {
        label: "git-commit-helper",
        description: "Git commit message generation with Conventional Commit best practices"
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

**Skill Details:**

| Skill | Description | Use Case |
|-------|-------------|----------|
| `skill-creator` | Create new Claude Code skills from templates | Create project-specific skills for any project |
| `git-commit-helper` | Generate Conventional Commit messages | Used in almost all projects |
| `changelog-generator` | Auto-generate CHANGELOG from commit history | Useful for release management |

---

### Layer 2: Auto-Detected Skills (Spec-based)

These skills are **automatically detected** from specification keywords. Show detected items to user for confirmation.

| Keywords in Spec | Skill | Description |
|------------------|-------|-------------|
| PDF, report, document | `pdf-anthropic` | PDF processing, extraction, analysis |
| Word, docx | `docx` | Word document generation and editing |
| Excel, xlsx, spreadsheet | `xlsx` | Excel processing and generation |
| test, testing, E2E, QA | `webapp-testing` | Web app testing patterns |
| MCP, server, protocol | `mcp-builder` | MCP server building guide |
| Zapier, automation, webhook | `zapier-workflows` | Zapier integration workflows |
| theme, color, UI, design | `theme-factory` | UI theme and color palette generation |
| Slack, notification, Bot, GIF | `slack-gif-creator` | Slack GIF creation |

---

### Layer 3: Additional Recommended Skills (User Selection)

Present these via `AskUserQuestion` based on detected project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended skills?",
    header: "Additional Skills",
    options: [
      // Options vary based on project type - see below
    ],
    multiSelect: true
  }]
})
```

#### For Marketing/Business Projects
| Skill | Description |
|-------|-------------|
| `content-research-writer` | Content research, SEO writing, copywriting |
| `competitive-ads-extractor` | Competitive ads analysis and extraction |
| `lead-research-assistant` | Lead generation research, prospect analysis |

#### For Design/Creative Projects
| Skill | Description |
|-------|-------------|
| `theme-factory` | UI theme generation, color palettes, design systems |
| `algorithmic-art` | Algorithmic art, generative design |
| `canvas-design` | Canvas-based design and graphics |

#### For Document Processing Projects
| Skill | Description |
|-------|-------------|
| `pdf-anthropic` | PDF processing, extraction, analysis |
| `pdf-processing-pro` | Advanced PDF processing (OCR, forms) |
| `docx` | Word document processing and generation |
| `xlsx` | Excel spreadsheet processing and generation |

#### For Development/Automation Projects
| Skill | Description |
|-------|-------------|
| `mcp-builder` | MCP server creation and development tools |
| `zapier-workflows` | Zapier automation workflows |
| `artifacts-builder` | Claude artifacts building and management |

---

## Available Skills (by Category)

### business-marketing
| Skill | Description |
|-------|-------------|
| `competitive-ads-extractor` | Competitive ads analysis and extraction |
| `content-research-writer` | Content research and SEO writing |
| `lead-research-assistant` | Lead generation research |

### creative-design
| Skill | Description |
|-------|-------------|
| `algorithmic-art` | Algorithmic art |
| `canvas-design` | Canvas design |
| `slack-gif-creator` | Slack GIF creation |
| `theme-factory` | UI theme and color palette generation |

### development
| Skill | Description |
|-------|-------------|
| `artifacts-builder` | Claude artifacts building |
| `changelog-generator` | CHANGELOG auto-generation |
| `cocoindex` | CocoIndex integration |
| `developer-growth-analysis` | Developer growth analysis |
| `git-commit-helper` | Git commit message generation |
| `mcp-builder` | MCP server building |
| `move-code-quality` | Code quality improvement |
| `skill-creator` | Create new skills |
| `webapp-testing` | Web app testing patterns |
| `zapier-workflows` | Zapier automation workflows |

### document-processing
| Skill | Description |
|-------|-------------|
| `docx` | Word document processing |
| `pdf-anthropic` | PDF processing |
| `pdf-processing-pro` | Advanced PDF processing (OCR, forms) |
| `xlsx` | Excel processing |

---

## Commands

```bash
# List all skills
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category skills --json

# Search skills
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category skills --json

# Download specific skill
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/skills
```

---

## Skill Structure

Skills may be directories containing multiple files:

```
skill-name/
├── SKILL.md           # Main skill definition
├── scripts/           # Helper scripts (optional)
├── templates/         # Code templates (optional)
└── references/        # Reference docs (optional)
```

The downloader handles both single-file and directory-based skills automatically.
