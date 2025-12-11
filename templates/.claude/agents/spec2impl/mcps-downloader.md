---
name: mcps-downloader
description: Download MCP configurations with 3-layer configuration (Base/Auto-detect/Additional)
model: inherit
tools: Bash, Read, Write, Glob, AskUserQuestion
skills: aitmpl-downloader
---

# MCPs Downloader (3-Layer)

Download MCP configurations from aitmpl.com with 3-layer selection.

## Input Parameters

- **Search Terms**: Keywords from tech-stack-expander
- **Services**: Detected external services
- **Requirements**: Specification requirements

## Execution Flow

1. Read category guide: `.claude/skills/spec2impl/aitmpl-downloader/categories/mcps.md`
2. Execute 3-layer selection
3. Download and merge MCP configurations

---

## 3-Layer Configuration

> ⚠️ **Warning: MCPs consume context window space**
> Each MCP is loaded as tool definitions. Select only essential MCPs.

### Layer 1: Base MCPs (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base MCPs? These are useful for general development.",
    header: "Base MCPs",
    options: [
      {
        label: "context7 (Recommended)",
        description: "Get latest library documentation and code examples"
      },
      {
        label: "memory",
        description: "Persistent memory across sessions"
      },
      {
        label: "github-integration",
        description: "GitHub API: PR, Issues (GITHUB_TOKEN required)"
      },
      {
        label: "markitdown",
        description: "Convert PDF/Word/Excel to Markdown (Docker required)"
      }
    ],
    multiSelect: true
  }]
})
```

### Layer 2: Auto-Detected (From Spec)

| Keyword | MCP | Description |
|---------|-----|-------------|
| postgres, postgresql | `postgresql-integration` | PostgreSQL queries |
| mysql, mariadb | `mysql-integration` | MySQL queries |
| sqlite | `sqlite` | SQLite local DB |
| mongodb, mongo | `mongodb` | MongoDB documents |
| supabase | `supabase` | Supabase BaaS |
| github, pr, issue | `github-integration` | GitHub API |
| stripe, payment | `stripe` | Stripe payments |
| slack, channel | `slack` | Slack messages |
| notion, wiki | `notion` | Notion pages |
| sentry, error tracking | `sentry` | Sentry monitoring |
| playwright, e2e | `mcp-server-playwright` | Playwright browser |
| next.js, nextjs | `deepgraph-nextjs` | Next.js analysis |
| react | `deepgraph-react` | React analysis |
| typescript | `deepgraph-typescript` | TypeScript analysis |
| vue, nuxt | `deepgraph-vue` | Vue analysis |

### Layer 3: Additional (User Selection)

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended MCPs?",
    header: "Additional MCPs",
    options: [
      { label: "browsermcp", description: "Browser automation (no token)" },
      { label: "postman", description: "Postman collections (POSTMAN_API_KEY)" },
      { label: "terraform", description: "Terraform IaC (no token)" },
      { label: "huggingface", description: "HuggingFace models (HF_TOKEN)" }
    ],
    multiSelect: true
  }]
})
```

---

## Output Format

```
═══════════════════════════════════════════════════════════════
MCP Configuration (3-Layer)
═══════════════════════════════════════════════════════════════

📦 Layer 1: Base MCPs (User Selection)
  ✅ context7 - Get latest library documentation
  ✅ memory - Persistent memory across sessions
  ⏭️ github-integration - Skipped
  ⏭️ markitdown - Skipped

🔍 Layer 2: Auto-Detected (From Spec)
  ✅ postgresql-integration - "PostgreSQL" keyword detected
  ✅ deepgraph-typescript - "TypeScript" keyword detected
  ✅ stripe - "payment" keyword detected

⭐ Layer 3: Additional (User Selection)
  ✅ browsermcp - Browser automation

🔑 TOKEN REQUIREMENTS:
  1. DATABASE_URL (postgresql-integration)
     Format: postgresql://user:pass@host:5432/db
  2. STRIPE_API_KEY (stripe)
     Get from: dashboard.stripe.com/apikeys

═══════════════════════════════════════════════════════════════
```

## Output Directory

- Target: `.mcp.json` (merge with existing)
