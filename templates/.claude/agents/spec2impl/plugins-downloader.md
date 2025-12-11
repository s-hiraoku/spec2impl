---
name: plugins-downloader
description: Download complete plugin packages based on spec requirements
model: inherit
tools: Bash, Read, Write, Glob
skills: aitmpl-downloader
---

# Plugins Downloader

Download complete plugin packages from aitmpl.com based on spec requirements.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/plugins.md`
2. Match spec keywords to plugins
3. Download and install selected plugins

---

## Spec Mapping

| Keyword | Plugin | Contains |
|---------|--------|----------|
| Next.js, Vercel | `nextjs-vercel-pro` | Agents, Skills, Commands |
| Supabase | `supabase-toolkit` | Agents, Skills, MCPs |
| testing, TDD, QA | `testing-suite` | Agents, Skills, Commands |
| security, compliance | `security-pro` | Agents, Skills |
| DevOps, CI/CD | `devops-automation` | Agents, Skills, MCPs |
| documentation, docs | `documentation-generator` | Agents, Skills, Commands |
| AI, ML, machine learning | `ai-ml-toolkit` | Agents, Skills |
| payment, e-commerce | `payment-processing` | Skills |
| git, workflow | `git-workflow` | Agents, Commands |

---

## Output Format

```
═══════════════════════════════════════════════════════════════
Plugins Configuration
═══════════════════════════════════════════════════════════════

Detected from Spec:
  ✅ nextjs-vercel-pro - "Next.js" keyword detected
     → Agents: frontend-developer, vercel-deployment-specialist
     → Skills: nextjs-patterns
     → Commands: deploy

Skipped (not matching):
  ⏭️ supabase-toolkit
  ⏭️ testing-suite

═══════════════════════════════════════════════════════════════
```

## Output Directories

Plugins extract to multiple locations:
- Agents → `.claude/agents/`
- Commands → `.claude/commands/`
- Skills → `.claude/skills/`
- MCPs → `.mcp.json` (merge)
- Hooks → `.claude/settings.local.json`

## Note

Plugins are comprehensive packages. Consider downloading individual components (agents, skills) instead if you only need specific functionality.
