# Commands Category Guide

Download slash command templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/commands`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/commands`

## Output Directory

- Target: `.claude/commands/`

---

## 3-Layer Commands Configuration

> ℹ️ **Note: Commands are invoked on-demand**
> Unlike Skills/MCPs, commands don't consume context until invoked.
> Feel free to install useful commands.

### Layer 1: Recommended Base Commands (User Selection)

Present these via `AskUserQuestion` with multiSelect.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base commands? These are useful for general development.",
    header: "Base Commands",
    options: [
      {
        label: "review (Recommended)",
        description: "Code review workflow with checklist and best practices"
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

**Command Details:**

| Command | Description | Use Case |
|---------|-------------|----------|
| `review` | Code review with quality checklist | Any project with code reviews |
| `test` | Test execution and reporting | Projects with test suites |
| `docs` | Documentation generation | Projects needing documentation |

---

### Layer 2: Auto-Detected Commands (Spec-based)

These commands are **automatically detected** from specification keywords.

| Keywords in Spec | Command | Description |
|------------------|---------|-------------|
| CI/CD, deploy, deployment, hosting | `deploy` | Deployment automation workflow |
| refactor, clean, improve | `refactor` | Refactoring workflow |
| debug, error, bug, fix | `debug` | Debugging assistance workflow |
| release, version, changelog | `release` | Release management workflow |
| analyze, metrics, quality, coverage | `analyze` | Code analysis and metrics |

---

### Layer 3: Additional Recommended Commands (User Selection)

Present these via `AskUserQuestion` based on project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended commands?",
    header: "Additional Commands",
    options: [
      { label: "deploy", description: "Deployment automation workflow" },
      { label: "analyze", description: "Code analysis and metrics" },
      { label: "release", description: "Release management workflow" },
      { label: "refactor", description: "Refactoring workflow" }
    ],
    multiSelect: true
  }]
})
```

---

## Available Commands

| Command | Purpose |
|---------|---------|
| `deploy` | Deployment automation workflow |
| `review` | Code review workflow |
| `test` | Test execution and reporting |
| `docs` | Documentation generation |
| `analyze` | Code analysis and metrics |
| `refactor` | Refactoring workflow |
| `debug` | Debugging assistance |
| `release` | Release management |

## CLI Commands

```bash
# List all commands
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category commands --json

# Search commands
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category commands --json

# Download specific command
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/commands
```

## Note

Commands are slash commands invoked with `/command-name` in Claude Code.
Each command file is a markdown file with YAML frontmatter defining the command behavior.
