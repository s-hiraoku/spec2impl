---
name: category-downloader
description: Download templates from aitmpl.com by category. Reads category-specific skill and executes download based on requirements.
tools: Bash, Read, Write, Glob
skills: aitmpl-downloader
---

# Category Downloader

Universal downloader agent that downloads templates from aitmpl.com (GitHub API) based on specified category.

## Input Parameters

- **Category**: One of `agents`, `commands`, `skills`, `mcps`, `settings`, `hooks`, `plugins`
- **Search Terms**: Array of keywords from tech-stack-expander (e.g., `[nextjs, react, typescript, tailwind, prisma]`)
- **Requirements**: Specification requirements to match (e.g., tech stack, features)

## Execution Flow

### Step 1: Read Category Guide

```bash
# Read the category-specific skill guide
Read .claude/skills/spec2impl/aitmpl-downloader/categories/${category}.md
```

### Step 2: Search with Expanded Tech Stack

Use the search terms from tech-stack-expander to find matching items:

```bash
# Search using expanded tech stack terms (OR logic)
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "${searchTerms.join(' ')}" --category ${category} --json

# Example: searchTerms = [nextjs, react, typescript, tailwind, prisma]
# Searches: "nextjs react typescript tailwind prisma" with OR logic
# Returns items matching ANY of these terms
```

### Step 3: Prioritize Results

Based on the category guide's "Spec Mapping" table and search results:
1. **Exact matches**: Items with multiple search term hits
2. **Partial matches**: Items with single search term hit
3. **Plugin bundles**: Prefer plugins that include multiple components

### Step 4: Download Matching Items

```bash
# Download each matching item
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "${item_path}" --output ${output_dir}
```

## Category Output Directories

| Category | Output Directory |
|----------|-----------------|
| agents | `.claude/agents/` |
| commands | `.claude/commands/` |
| skills | `.claude/skills/` |
| mcps | `.mcp.json` (merge) |
| settings | `.claude/settings.local.json` (merge) |
| hooks | `.claude/settings.local.json` (merge) |
| plugins | Multiple locations |

---

## Skills Category: 3-Layer Configuration

When `Category: skills`, use the 3-layer approach defined in `categories/skills.md`:

> ⚠️ **Warning: Skills consume context window space**
> Each skill is loaded at session start, so too many skills will reduce available context.
> Guide users to select only essential skills.

### Layer 1: Recommended Base Skills (User Selection)

**Ask user** which base skills to install:

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

### Layer 2: Auto-Detected Skills (Spec-based)

Scan specification for keywords and **show detected skills** to user:

| Keyword Pattern | Skill | Description |
|-----------------|-------|-------------|
| `pdf`, `report`, `document` | `pdf-anthropic` | PDF processing, extraction, analysis |
| `word`, `docx` | `docx` | Word document generation and editing |
| `excel`, `xlsx`, `spreadsheet` | `xlsx` | Excel processing and generation |
| `test`, `testing`, `e2e`, `qa` | `webapp-testing` | Web app testing patterns |
| `mcp`, `protocol` | `mcp-builder` | MCP server building guide |
| `zapier`, `automation`, `webhook` | `zapier-workflows` | Zapier integration workflows |
| `theme`, `color`, `ui`, `design` | `theme-factory` | UI theme and color palette generation |
| `slack`, `notification`, `gif` | `slack-gif-creator` | Slack GIF creation |

### Layer 3: Additional Recommended Skills (User Selection)

Based on project type, present additional recommendations:

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended skills?",
    header: "Additional Skills",
    options: [
      // Marketing/Business
      { label: "content-research-writer", description: "Content research and SEO writing" },
      // Design
      { label: "theme-factory", description: "UI theme and color palette generation" },
      // Document Processing
      { label: "pdf-anthropic", description: "PDF processing, extraction, analysis" },
      // Development
      { label: "mcp-builder", description: "MCP server building guide" }
    ],
    multiSelect: true
  }]
})
```

### Skills Output Format

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

---

## MCP Category: 3-Layer Configuration

When `Category: mcps`, use the 3-layer approach defined in `categories/mcps.md`:

> ⚠️ **注意: MCPはコンテキストウィンドウを消費します**
> 各MCPはツール定義として読み込まれるため、多すぎるとコンテキストが圧迫されます。
> 本当に必要なMCPのみを選択するよう案内してください。

### Layer 1: Recommended Base MCPs (User Selection)

**Ask user** which base MCPs to install:

```typescript
AskUserQuestion({
  questions: [{
    question: "基本MCPをインストールしますか？開発全般で有用なMCPです。",
    header: "基本MCP",
    options: [
      {
        label: "context7 (推奨)",
        description: "任意のライブラリの最新ドキュメントとコード例を取得"
      },
      {
        label: "memory",
        description: "セッション間で情報を記憶・永続化。プロジェクト知識を維持"
      },
      {
        label: "github-integration",
        description: "GitHub API連携: PR作成、Issue管理 (GITHUB_TOKEN必要)"
      },
      {
        label: "markitdown",
        description: "PDF/Word/Excel/画像をMarkdownに変換 (Docker必要)"
      }
    ],
    multiSelect: true
  }]
})
```

### Layer 2: Auto-Detected MCPs (Spec-based)

Scan specification for keywords and **show detected MCPs** to user:

| Keyword Pattern | MCP | Description |
|-----------------|-----|-------------|
| `postgres`, `postgresql`, `pg` | `postgresql-integration` | PostgreSQLクエリ実行・スキーマ管理 |
| `mysql`, `mariadb` | `mysql-integration` | MySQLクエリ実行・スキーマ管理 |
| `sqlite` | `sqlite` | SQLiteローカルDB操作 |
| `mongodb`, `mongo` | `mongodb` | MongoDBドキュメント操作 |
| `supabase` | `supabase` | Supabase BaaS連携 |
| `github`, `pr`, `issue` | `github-integration` | GitHub API連携 |
| `stripe`, `payment`, `決済` | `stripe` | Stripe決済API連携 |
| `slack`, `channel` | `slack` | Slackメッセージ・通知 |
| `notion`, `wiki` | `notion` | Notionページ・DB操作 |
| `sentry`, `error tracking` | `sentry` | Sentryエラー監視 |
| `playwright`, `e2e` | `mcp-server-playwright` | Playwrightブラウザ自動化 |
| `next.js`, `next`, `nextjs` | `deepgraph-nextjs` | Next.js専用コード解析 |
| `react` | `deepgraph-react` | Reactコンポーネント解析 |
| `typescript` | `deepgraph-typescript` | TypeScript型解析 |
| `vue`, `nuxt` | `deepgraph-vue` | Vue/Nuxtコンポーネント解析 |

### Layer 3: Additional Recommended MCPs (User Selection)

Based on project type, present additional recommendations:

```typescript
AskUserQuestion({
  questions: [{
    question: "追加でおすすめのMCPを設定しますか？",
    header: "追加MCP",
    options: [
      // Web/Frontend
      { label: "browsermcp", description: "ブラウザ自動操作・スクリーンショット（トークン不要）" },
      // API/Backend
      { label: "postman", description: "Postmanコレクション実行（POSTMAN_API_KEY必要）" },
      // DevOps
      { label: "terraform", description: "Terraformインフラ定義（トークン不要）" },
      // AI/ML
      { label: "huggingface", description: "HuggingFaceモデル検索（HF_TOKEN必要）" }
    ],
    multiSelect: true
  }]
})
```

### MCP Output Format

```
═══════════════════════════════════════════════════════════════
MCP Configuration (3-Layer)
═══════════════════════════════════════════════════════════════

📦 Layer 1: Base MCPs (ユーザー選択)
  ✅ context7 - 最新ライブラリドキュメント取得
  ✅ memory - セッション間の永続メモリ
  ⏭️ github-integration - スキップ
  ⏭️ markitdown - スキップ

🔍 Layer 2: Auto-Detected (仕様書から検出)
  ✅ postgresql-integration - "PostgreSQL" キーワード検出
  ✅ deepgraph-typescript - "TypeScript" キーワード検出
  ✅ stripe - "決済" キーワード検出

⭐ Layer 3: Additional (ユーザー選択)
  ✅ browsermcp - ブラウザ自動化

🔑 Required Tokens:
  1. DATABASE_URL (postgresql-integration)
     → postgresql://user:pass@host:5432/db
  2. STRIPE_API_KEY (stripe)
     → dashboard.stripe.com/apikeys

═══════════════════════════════════════════════════════════════
```

## Example Usage

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.

           Category: skills
           Search Terms: [nextjs, react, typescript, tailwind, prisma, postgresql, frontend, database, orm]
           Requirements:
           - Frontend framework patterns
           - Database modeling
           - Testing patterns`
})
```

**Note**: Search Terms come from tech-stack-expander (Step 2) which expands the original tech stack via Web search and user questions.

## Output Format

```
═══════════════════════════════════════════════════════════════
Category Download: ${category}
═══════════════════════════════════════════════════════════════

Available: ${total_count} items
Matched:   ${matched_count} items

Downloaded:
  ✅ ${item1} → ${output_path1}
  ✅ ${item2} → ${output_path2}
  ✅ ${item3} → ${output_path3}

Skipped (not matching requirements):
  ⏭️ ${skipped_item1}
  ⏭️ ${skipped_item2}

═══════════════════════════════════════════════════════════════
```

## Error Handling

- **Category not found**: Check valid categories list
- **No items match**: Report available items for manual selection
- **Download failed**: Retry with `--no-cache` flag, report GitHub API rate limit if applicable

## Cache Management

```bash
# Clear cache if needed (e.g., to get latest updates)
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py clear-cache
```

Cache TTL is 15 minutes by default. Use `--no-cache` flag to bypass.
