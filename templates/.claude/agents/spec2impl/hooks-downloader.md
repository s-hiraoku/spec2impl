---
name: hooks-downloader
description: Download hook configurations based on spec requirements
model: inherit
tools: Bash, Read, Write, Glob
skills: aitmpl-downloader
---

# Hooks Downloader

Download hook configurations from aitmpl.com based on spec requirements.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/hooks.md`
2. Match spec keywords to hooks
3. Download and merge selected hooks

---

## Spec Mapping

| Keyword | Hook | Description |
|---------|------|-------------|
| audit, log, logging | `audit-logger` | Log all tool executions |
| notification, alert | `notification-hook` | Desktop notifications |
| git, commit, auto-commit | `git-auto-commit` | Auto-commit after changes |
| security, validate | `security-validator` | Validate before execution |

---

## Output Format

```
═══════════════════════════════════════════════════════════════
Hooks Configuration
═══════════════════════════════════════════════════════════════

Detected from Spec:
  ✅ notification-hook - "notification" keyword detected
  ✅ git-auto-commit - "git" keyword detected

Skipped (not matching):
  ⏭️ audit-logger
  ⏭️ security-validator

═══════════════════════════════════════════════════════════════
```

## Output Directory

- Target: `.claude/settings.local.json` (hooks section, merge)
