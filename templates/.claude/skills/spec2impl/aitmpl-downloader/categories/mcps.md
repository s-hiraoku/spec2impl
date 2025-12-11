# MCPs Category Guide

Download MCP (Model Context Protocol) server configurations from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/mcps`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/mcps`

## Output Directory

- Target: `.mcp.json` (merge with existing)

---

## 3-Layer MCP Configuration

> ⚠️ **注意: MCPはコンテキストウィンドウを消費します**
>
> 各MCPはツール定義としてコンテキストに読み込まれるため、**インストールするMCPが多いほどコンテキストウィンドウが圧迫**されます。
> - 本当に必要なMCPのみを選択してください
> - 使用頻度の低いMCPは後から追加できます
> - 迷った場合は最小限（context7 + memory）から始めることを推奨

### Layer 1: Recommended Base MCPs (User Selection)

Present these via `AskUserQuestion` with multiSelect. All are highly recommended for general development.

```typescript
AskUserQuestion({
  questions: [{
    question: "基本MCPをインストールしますか？開発全般で有用なMCPです。",
    header: "基本MCP",
    options: [
      {
        label: "context7 (推奨)",
        description: "任意のライブラリの最新ドキュメントとコード例を取得。フレームワーク問わず有用"
      },
      {
        label: "memory",
        description: "セッション間で情報を記憶・永続化。プロジェクト知識を維持"
      },
      {
        label: "github-integration",
        description: "GitHub API連携: PR作成、Issue管理、リポジトリ操作 (GITHUB_TOKEN必要)"
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

**MCP Details:**

| MCP | Description | Token | Config |
|-----|-------------|-------|--------|
| `context7` | 任意のライブラリの最新ドキュメント・コード例を自動取得。React, Next.js, Prisma等あらゆるライブラリで最新情報にアクセス | 不要 | `npx -y @upstash/context7-mcp` |
| `memory` | セッション間で情報を記憶。プロジェクトの決定事項、設計方針、学習内容を永続化 | 不要 | `npx -y @modelcontextprotocol/server-memory` |
| `github-integration` | GitHub API完全連携。PR作成・レビュー、Issue管理、ブランチ操作、リポジトリ設定 | GITHUB_PERSONAL_ACCESS_TOKEN | `npx -y @modelcontextprotocol/server-github` |
| `markitdown` | 各種ファイル形式（PDF, Word, Excel, PowerPoint, 画像, 音声）をMarkdownに変換 | 不要 (Docker必要) | `docker run --rm -i markitdown-mcp:latest` |

**Why NOT included by default:**
- `filesystem-access`: Claude Code has built-in Read/Write/Edit tools
- `web-fetch`: Claude Code has built-in WebFetch tool

---

### Layer 2: Auto-Detected MCPs (Spec-based)

These MCPs are **automatically detected** from specification keywords. Show detected items to user for confirmation.

| Keywords in Spec | MCP | Description | Token |
|------------------|-----|-------------|-------|
| PostgreSQL, Postgres, pg | `postgresql-integration` | PostgreSQLデータベースへのクエリ実行・スキーマ管理 | DATABASE_URL |
| MySQL, MariaDB | `mysql-integration` | MySQLデータベースへのクエリ実行・スキーマ管理 | DATABASE_URL |
| SQLite | `sqlite` | SQLiteデータベースのローカル操作 | 不要 |
| MongoDB, Mongo | `mongodb` | MongoDBドキュメントDB操作・集計クエリ | MONGODB_URI |
| Supabase | `supabase` | Supabase BaaS連携（Auth, DB, Storage, Realtime） | SUPABASE_URL, SUPABASE_KEY |
| GitHub, PR, Issue | `github-integration` | GitHub API連携（Layer 1で未選択の場合） | GITHUB_PERSONAL_ACCESS_TOKEN |
| Stripe, Payment, 決済 | `stripe` | Stripe決済API連携（顧客、商品、サブスクリプション管理） | STRIPE_API_KEY |
| Slack, Channel | `slack` | Slackメッセージ送信・チャンネル管理・通知連携 | SLACK_TOKEN |
| Notion, Wiki | `notion` | Notionページ・データベース操作・ドキュメント管理 | NOTION_TOKEN |
| Sentry, Error tracking | `sentry` | Sentryエラー監視・Issue管理・パフォーマンス分析 | SENTRY_DSN |
| Playwright, E2E | `mcp-server-playwright` | Playwrightブラウザ自動化・E2Eテスト実行 | 不要 |
| Next.js, Next | `deepgraph-nextjs` | Next.js専用コード解析・App Router/Pages Router対応 | 不要 |
| React | `deepgraph-react` | Reactコンポーネント解析・Hooks/状態管理パターン | 不要 |
| TypeScript | `deepgraph-typescript` | TypeScript型解析・型推論・リファクタリング支援 | 不要 |
| Vue, Nuxt | `deepgraph-vue` | Vue/Nuxtコンポーネント解析・Composition API対応 | 不要 |

---

### Layer 3: Additional Recommended MCPs (User Selection)

Present these via `AskUserQuestion` based on detected project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "追加でおすすめのMCPを設定しますか？",
    header: "追加MCP",
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
| `browsermcp` | ブラウザ自動操作・スクリーンショット・DOM解析 | 不要 |
| `chrome-devtools` | Chrome DevTools連携・デバッグ・パフォーマンス計測 | 不要 |
| `figma-dev-mode` | Figmaデザイン連携・コンポーネント情報取得 | FIGMA_TOKEN |

#### For API/Backend Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `postman` | Postmanコレクション実行・APIテスト自動化 | POSTMAN_API_KEY |
| `elasticsearch` | Elasticsearch検索クエリ・インデックス管理 | ES_URL, ES_API_KEY |

#### For DevOps/Infrastructure Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `terraform` | Terraformインフラ定義・プラン実行・状態管理 | 不要 |
| `grafana` | Grafanaダッシュボード・メトリクス可視化 | GRAFANA_URL, GRAFANA_TOKEN |
| `circleci` | CircleCI パイプライン管理・ビルド状況確認 | CIRCLECI_TOKEN |

#### For AI/ML Projects
| MCP | Description | Token |
|-----|-------------|-------|
| `huggingface` | HuggingFaceモデル検索・推論実行 | HF_TOKEN |
| `elevenlabs` | ElevenLabsテキスト音声変換・音声合成 | ELEVENLABS_API_KEY |

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
