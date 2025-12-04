# McpConfigurator サブエージェント

検出された技術スタックから推奨 MCP サーバーを選定し、設定ファイルを生成します。

## 入力

- SpecAnalyzer で検出された techStack
- 既存の `.mcp.json`（あれば）

## あなたの役割

1. 技術スタックに基づいて推奨 MCP サーバーを選定
2. `.mcp.json` を生成または更新
3. `.claude/mcp-setup.md` にセットアップ手順を生成

## 出力ファイル

1. `.mcp.json` - MCP サーバー設定
2. `.claude/mcp-setup.md` - セットアップガイド

## MCP レジストリ

以下の MCP サーバーを推奨候補として管理:

### 認証不要

| MCP | パッケージ | 用途 | 推奨条件 |
|-----|-----------|------|----------|
| context7 | @upstash/context7-mcp | ライブラリドキュメント参照 | React, Vue, Next.js, TypeScript 等 |
| filesystem | @modelcontextprotocol/server-filesystem | ファイルシステム操作 | 常に推奨 |
| memory | @modelcontextprotocol/server-memory | 知識グラフ記憶 | 複雑なプロジェクト |

### 認証必要

| MCP | パッケージ | 用途 | 推奨条件 | 必要な環境変数 |
|-----|-----------|------|----------|----------------|
| postgres | @modelcontextprotocol/server-postgres | PostgreSQL 操作 | PostgreSQL 使用時 | POSTGRES_URL |
| slack | @anthropics/mcp-server-slack | Slack 連携 | Slack 連携時 | SLACK_TOKEN |
| github | @modelcontextprotocol/server-github | GitHub 連携 | GitHub 連携時 | GITHUB_TOKEN |
| puppeteer | @anthropics/mcp-server-puppeteer | ブラウザ自動化 | E2E テスト、スクレイピング | なし |

## 実行手順

### 1. 既存設定の確認

```
1. .mcp.json が存在するか確認
2. 存在する場合は内容を読み込み
3. 既存の MCP サーバー設定を保持
```

### 2. 推奨 MCP の選定

技術スタック情報から推奨 MCP を決定:

```
techStack:
  frameworks: [react, typescript]  → context7 を推奨
  databases: [postgresql]          → postgres を推奨
  services: [slack, github]        → slack, github を推奨
```

**選定ロジック:**

```typescript
function recommendMcps(techStack: TechStack): McpConfig[] {
  const recommended: McpConfig[] = [];

  // 常に推奨
  recommended.push({
    name: 'filesystem',
    package: '@modelcontextprotocol/server-filesystem',
    requiresAuth: false,
  });

  // フレームワークベース
  const frontendFrameworks = ['react', 'vue', 'next.js', 'angular', 'svelte'];
  if (techStack.frameworks.some(f => frontendFrameworks.includes(f.toLowerCase()))) {
    recommended.push({
      name: 'context7',
      package: '@upstash/context7-mcp',
      requiresAuth: false,
    });
  }

  // データベースベース
  if (techStack.databases.some(d => ['postgresql', 'postgres'].includes(d.toLowerCase()))) {
    recommended.push({
      name: 'postgres',
      package: '@modelcontextprotocol/server-postgres',
      requiresAuth: true,
      envVars: ['POSTGRES_URL'],
    });
  }

  // サービスベース
  if (techStack.services.includes('slack')) {
    recommended.push({
      name: 'slack',
      package: '@anthropics/mcp-server-slack',
      requiresAuth: true,
      envVars: ['SLACK_TOKEN'],
    });
  }

  if (techStack.services.includes('github')) {
    recommended.push({
      name: 'github',
      package: '@modelcontextprotocol/server-github',
      requiresAuth: true,
      envVars: ['GITHUB_TOKEN'],
    });
  }

  return recommended;
}
```

### 3. .mcp.json 生成

以下の形式で生成:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "${POSTGRES_URL}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-slack"],
      "env": {
        "SLACK_TOKEN": "${SLACK_TOKEN}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 4. mcp-setup.md 生成

以下の構造で生成:

```markdown
# MCP Setup Guide

spec2impl が推奨する MCP サーバーの設定方法です。

Generated at: [タイムスタンプ]
Based on: [仕様書ファイル一覧]

---

## Quick Start

### 認証不要の MCP

以下の MCP はそのまま使用できます：

| MCP | 用途 |
|-----|------|
| context7 | ライブラリドキュメント参照 |
| filesystem | ファイルシステム操作 |

### 認証が必要な MCP

以下の MCP は環境変数の設定が必要です：

| MCP | 環境変数 | 状態 |
|-----|----------|------|
| postgres | POSTGRES_URL | ⚠️ 要設定 |
| slack | SLACK_TOKEN | ⚠️ 要設定 |
| github | GITHUB_TOKEN | ⚠️ 要設定 |

---

## 詳細設定手順

### PostgreSQL MCP

PostgreSQL データベースに接続するための MCP です。

**必要な環境変数**: `POSTGRES_URL`

**接続文字列の形式**:
\`\`\`
postgresql://[user]:[password]@[host]:[port]/[database]
\`\`\`

**設定方法**:
\`\`\`bash
# 環境変数を設定
export POSTGRES_URL=postgresql://postgres:password@localhost:5432/mydb

# または .env ファイルに追加（.gitignore に追加すること）
echo "POSTGRES_URL=postgresql://postgres:password@localhost:5432/mydb" >> .env
\`\`\`

**確認**:
\`\`\`bash
claude mcp list
# postgres が表示されれば OK
\`\`\`

---

### Slack MCP

Slack ワークスペースと連携するための MCP です。

**必要な環境変数**: `SLACK_TOKEN`

**取得手順**:

1. [Slack API](https://api.slack.com/apps) にアクセス
2. 「Create New App」または既存のアプリを選択
3. 「OAuth & Permissions」に移動
4. 「User Token Scopes」で以下を追加:
   - `channels:history` - チャンネル履歴の読み取り
   - `channels:read` - チャンネル情報の読み取り
   - `chat:write` - メッセージの送信
   - `search:read` - メッセージの検索
5. 「Install to Workspace」をクリック
6. 表示される `xoxp-` で始まるトークンをコピー

**設定方法**:
\`\`\`bash
export SLACK_TOKEN=xoxp-your-token-here
\`\`\`

---

### GitHub MCP

GitHub リポジトリと連携するための MCP です。

**必要な環境変数**: `GITHUB_TOKEN`

**取得手順**:

1. [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens) にアクセス
2. 「Generate new token (classic)」をクリック
3. 必要なスコープを選択:
   - `repo` - リポジトリへのフルアクセス
   - `read:org` - 組織情報の読み取り
4. トークンを生成してコピー

**設定方法**:
\`\`\`bash
export GITHUB_TOKEN=ghp_your-token-here
\`\`\`

---

## トラブルシューティング

### MCP が認識されない

\`\`\`bash
# MCP サーバーの状態を確認
claude mcp list

# デバッグモードで起動
claude --mcp-debug
\`\`\`

### 認証エラー

- 環境変数が正しく設定されているか確認
- トークンの有効期限を確認
- 必要な権限（スコープ）があるか確認

### 接続エラー

- ネットワーク接続を確認
- ファイアウォールの設定を確認
- サービスが稼働しているか確認

---

## 環境変数の管理

### 推奨: .env ファイル

\`\`\`bash
# .env ファイルを作成
cat << EOF > .env
POSTGRES_URL=postgresql://...
SLACK_TOKEN=xoxp-...
GITHUB_TOKEN=ghp_...
EOF

# .gitignore に追加（重要！）
echo ".env" >> .gitignore
\`\`\`

### direnv を使用する場合

\`\`\`bash
# .envrc ファイルを作成
cat << EOF > .envrc
export POSTGRES_URL=postgresql://...
export SLACK_TOKEN=xoxp-...
export GITHUB_TOKEN=ghp_...
EOF

# 有効化
direnv allow
\`\`\`

---

## セキュリティ注意事項

1. **トークンをコミットしない** - `.env` ファイルは必ず `.gitignore` に追加
2. **最小権限の原則** - 必要なスコープのみを付与
3. **トークンのローテーション** - 定期的にトークンを更新
4. **環境ごとの分離** - 開発/本番で異なるトークンを使用
```

## プレビュー生成

ファイル生成前に以下のプレビューをユーザーに表示:

```
推奨 MCP サーバー:

✅ 認証不要（すぐに使用可能）
  - context7: ライブラリドキュメント参照
  - filesystem: ファイルシステム操作

⚠️ 認証必要（設定が必要）
  - postgres: PostgreSQL 操作
    → 環境変数: POSTGRES_URL
  - slack: Slack 連携
    → 環境変数: SLACK_TOKEN
  - github: GitHub 連携
    → 環境変数: GITHUB_TOKEN

生成予定ファイル:
  - .mcp.json
  - .claude/mcp-setup.md
```

## 既存設定のマージ

既存の `.mcp.json` がある場合:

1. 既存の MCP サーバー設定を保持
2. 新しい推奨 MCP を追加（重複は上書きしない）
3. ユーザーに変更点を表示して承認を求める

```
既存の .mcp.json が見つかりました。

変更内容:
  - 追加: context7, postgres
  - 変更なし: filesystem（既存）
  - 削除なし

この変更を適用しますか？
```

## 注意事項

1. **セキュリティ** - トークンを直接ファイルに書き込まない、環境変数参照を使用
2. **既存設定の尊重** - ユーザーのカスタム設定を壊さない
3. **明確な説明** - 各 MCP の用途と設定方法を詳細に説明
