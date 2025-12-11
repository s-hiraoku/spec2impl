# MCPs Category Guide

Download MCP (Model Context Protocol) server configurations from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/mcps`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/mcps`

## Output Directory

- Target: `.mcp.json` (merge with existing)

---

## 3-Layer MCP Configuration

> ⚠️ **Warning: MCPs consume context window space**
>
> Each MCP loads its tool definitions into the context, so **more MCPs = less context window available**.
> - Select only the MCPs you truly need
> - Less frequently used MCPs can be added later
> - When in doubt, start minimal (context7 + memory)

### Layer 1: Recommended Base MCPs (User Selection)

Present these via `AskUserQuestion` with multiSelect. All are highly recommended for general development.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base MCPs? These are useful for general development.",
    header: "Base MCPs",
    options: [
      {
        label: "context7 (Recommended)",
        description: "Get latest docs and code examples for any library. Useful across all frameworks"
      },
      {
        label: "memory",
        description: "Persist information across sessions. Maintain project knowledge"
      },
      {
        label: "github-integration",
        description: "GitHub API: Create PRs, manage Issues, repository operations (GITHUB_TOKEN required)"
      },
      {
        label: "markitdown",
        description: "Convert PDF/Word/Excel/images to Markdown (Docker required)"
      }
    ],
    multiSelect: true
  }]
})
```

**MCP Details:**

| MCP | Description | Token | Config |
|-----|-------------|-------|--------|
| `context7` | Auto-fetch latest docs and code examples for any library. Access up-to-date info for React, Next.js, Prisma, etc. | None | `npx -y @upstash/context7-mcp` |
| `memory` | Persist information across sessions. Store project decisions, design patterns, learnings | None | `npx -y @modelcontextprotocol/server-memory` |
| `github-integration` | Full GitHub API integration. Create/review PRs, manage Issues, branch operations, repository settings | GITHUB_PERSONAL_ACCESS_TOKEN | `npx -y @modelcontextprotocol/server-github` |
| `markitdown` | Convert various file formats (PDF, Word, Excel, PowerPoint, images, audio) to Markdown | None (Docker required) | `docker run --rm -i markitdown-mcp:latest` |

**Why NOT included by default:**
- `filesystem-access`: Claude Code has built-in Read/Write/Edit tools
- `web-fetch`: Claude Code has built-in WebFetch tool

---

### Layer 2: Auto-Detected MCPs (Spec-based)

These MCPs are **automatically detected** from specification keywords. Show detected items to user for confirmation.

| Keywords in Spec | MCP | Description | Token |
|------------------|-----|-------------|-------|
| PostgreSQL, Postgres, pg | `postgresql-integration` | PostgreSQL query execution and schema management | DATABASE_URL |
| MySQL, MariaDB | `mysql-integration` | MySQL query execution and schema management | DATABASE_URL |
| SQLite | `sqlite` | SQLite local database operations | None |
| MongoDB, Mongo | `mongodb` | MongoDB document DB operations and aggregation queries | MONGODB_URI |
| Supabase | `supabase` | Supabase BaaS integration (Auth, DB, Storage, Realtime) | SUPABASE_URL, SUPABASE_KEY |
| GitHub, PR, Issue | `github-integration` | GitHub API integration (if not selected in Layer 1) | GITHUB_PERSONAL_ACCESS_TOKEN |
| Stripe, Payment | `stripe` | Stripe payment API integration (customers, products, subscriptions) | STRIPE_API_KEY |
| Slack, Channel | `slack` | Slack messaging, channel management, notifications | SLACK_TOKEN |
| Notion, Wiki | `notion` | Notion page and database operations, document management | NOTION_TOKEN |
| Sentry, Error tracking | `sentry` | Sentry error monitoring, Issue management, performance analysis | SENTRY_DSN |
| Playwright, E2E | `mcp-server-playwright` | Playwright browser automation, E2E test execution | None |
| Next.js, Next | `deepgraph-nextjs` | Next.js code analysis, App Router/Pages Router support | None |
| React | `deepgraph-react` | React component analysis, Hooks/state management patterns | None |
| TypeScript | `deepgraph-typescript` | TypeScript type analysis, inference, refactoring support | None |
| Vue, Nuxt | `deepgraph-vue` | Vue/Nuxt component analysis, Composition API support | None |

---

### Layer 3: Additional Recommended MCPs (User Selection)

Present these via `AskUserQuestion` based on detected project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended MCPs?",
    header: "Additional MCPs",
    options: [
      // Options vary based on project type - see below
    ],
    multiSelect: true
  }]
})
```

#### For Web/Frontend Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `browsermcp` | Browser automation, screenshots, DOM analysis | None |
| `chrome-devtools` | Chrome DevTools integration, debugging, performance measurement | None |
| `figma-dev-mode` | Figma design integration, component info extraction | FIGMA_TOKEN |

#### For API/Backend Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `postman` | Postman collection execution, API test automation | POSTMAN_API_KEY |
| `elasticsearch` | Elasticsearch search queries, index management | ES_URL, ES_API_KEY |

#### For DevOps/Infrastructure Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `terraform` | Terraform infrastructure definition, plan execution, state management | None |
| `grafana` | Grafana dashboards, metrics visualization | GRAFANA_URL, GRAFANA_TOKEN |
| `circleci` | CircleCI pipeline management, build status checking | CIRCLECI_TOKEN |

#### For AI/ML Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `huggingface` | HuggingFace model search, inference execution | HF_TOKEN |
| `elevenlabs` | ElevenLabs text-to-speech, voice synthesis | ELEVENLABS_API_KEY |

---

## Available MCP Servers (59 total)

### By Category

| Category | Count | Examples |
|----------|-------|----------|
| devtools | 34 | context7, sentry, mongodb, grafana, terraform, postman, stripe |
| browser_automation | 7 | playwright variants, browsermcp, browser-use |
| database | 5 | postgresql, mysql, supabase, neon, sqlite |
| deepgraph | 4 | nextjs, react, typescript, vue |
| integration | 2 | github, memory |
| productivity | 2 | monday, notion |
| marketing | 2 | facebook-ads, google-ads |
| web | 1 | web-fetch |
| filesystem | 1 | filesystem-access |
| audio | 1 | elevenlabs |
| deepresearch | 1 | mcp-server-nia |

---

## Commands

```bash
# List all MCPs
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category mcps --json

# Search MCPs
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category mcps --json

# Download specific MCP config
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .
```

---

## MCP Configuration Merge

When downloading, configs are merged into `.mcp.json`:

```json
{
  "mcpServers": {
    "existing-server": { ... },
    "new-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

---

## Token Requirements Summary

| MCP | Token | How to Get |
|-----|-------|------------|
| `github-integration` | GITHUB_PERSONAL_ACCESS_TOKEN | github.com/settings/tokens (repo, workflow scopes) |
| `postgresql-integration` | DATABASE_URL | postgresql://user:pass@host:5432/db |
| `mysql-integration` | DATABASE_URL | mysql://user:pass@host:3306/db |
| `mongodb` | MONGODB_URI | mongodb+srv://user:pass@cluster/db |
| `supabase` | SUPABASE_URL, SUPABASE_KEY | supabase.com/dashboard → Project Settings → API |
| `stripe` | STRIPE_API_KEY | dashboard.stripe.com/apikeys (sk_test_... or sk_live_...) |
| `slack` | SLACK_TOKEN | api.slack.com/apps → OAuth & Permissions |
| `notion` | NOTION_TOKEN | notion.so/my-integrations → Create integration |
| `sentry` | SENTRY_DSN | sentry.io/settings/projects → Client Keys |
| `grafana` | GRAFANA_URL, GRAFANA_TOKEN | grafana.com/account → API Keys |
| `postman` | POSTMAN_API_KEY | postman.com/settings/me/api-keys |
| `huggingface` | HF_TOKEN | huggingface.co/settings/tokens |
| `figma-dev-mode` | FIGMA_TOKEN | figma.com/developers → Personal access tokens |
| `elasticsearch` | ES_URL, ES_API_KEY | Elastic Cloud console or self-hosted |
| `circleci` | CIRCLECI_TOKEN | circleci.com/account/api |
| `elevenlabs` | ELEVENLABS_API_KEY | elevenlabs.io/account → API Key |
