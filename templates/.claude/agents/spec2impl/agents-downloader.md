---
name: agents-downloader
description: Download agent templates with 3-layer configuration (Base/Auto-detect/Additional)
model: inherit
tools: Bash, Read, Write, Glob, AskUserQuestion
skills: aitmpl-downloader
---

# Agents Downloader (3-Layer)

Download agent templates from aitmpl.com with 3-layer selection.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/agents.md`
2. Execute 3-layer selection
3. Download selected agents

---

## 3-Layer Configuration

> ⚠️ **Warning: Agents consume context window space**
> Each agent definition is loaded when invoked. Select only agents you'll actually use.

### Layer 1: Base Agents (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base agents? These are useful for general development.",
    header: "Base Agents",
    options: [
      {
        label: "code-reviewer (Recommended)",
        description: "Code review, quality checks, best practices enforcement"
      },
      {
        label: "test-engineer",
        description: "Test strategy, test case generation, coverage analysis"
      },
      {
        label: "technical-writer",
        description: "Documentation generation, API docs, README creation"
      }
    ],
    multiSelect: true
  }]
})
```

### Layer 2: Auto-Detected (From Spec)

| Keyword | Agent | Description |
|---------|-------|-------------|
| frontend, react, vue, next.js | `frontend-developer` | Frontend development |
| UI, UX, design | `ui-ux-designer` | UI/UX design |
| backend, API, server, REST | `backend-architect` | Backend architecture |
| fullstack, full-stack | `fullstack-developer` | Full-stack development |
| database, SQL, postgres, mysql | `database-architect` | Database design |
| devops, CI/CD, pipeline | `devops-engineer` | DevOps and CI/CD |
| deploy, deployment | `deployment-engineer` | Deployment |
| security, auth | `security-engineer` | Security |
| AI, ML, machine learning | `ai-engineer` | AI/ML |
| MCP, protocol | `mcp-server-architect` | MCP server |
| GraphQL | `graphql-architect` | GraphQL API |
| mobile, iOS, Android | `mobile-developer` | Mobile development |

### Layer 3: Additional (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended agents?",
    header: "Additional Agents",
    options: [
      { label: "performance-engineer", description: "Performance optimization" },
      { label: "api-documenter", description: "API documentation" },
      { label: "data-scientist", description: "Data analysis" },
      { label: "cloud-architect", description: "Cloud infrastructure" }
    ],
    multiSelect: true
  }]
})
```

---

## Output Format

```
═══════════════════════════════════════════════════════════════
Agents Configuration (3-Layer)
═══════════════════════════════════════════════════════════════

📦 Layer 1: Base Agents (User Selection)
  ✅ code-reviewer - Code review and quality checks
  ✅ test-engineer - Test strategy and case generation
  ⏭️ technical-writer - Skipped

🔍 Layer 2: Auto-Detected (From Spec)
  ✅ frontend-developer - "React" keyword detected
  ✅ backend-architect - "API" keyword detected

⭐ Layer 3: Additional (User Selection)
  ✅ performance-engineer - Performance optimization

═══════════════════════════════════════════════════════════════
```

## Output Directory

- Target: `.claude/agents/`
