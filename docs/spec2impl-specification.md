# spec2impl 仕様書

## 概要

spec2impl は、仕様書ドキュメントから Claude Code 用の実装環境を自動構築するツールです。

### コンセプト

```
docs/ ディレクトリを指定するだけで、実装に必要な環境が整う
```

### 目的

- 仕様書から Skills、Subagents を自動生成
- 実装に役立つ MCP Server を自動設定
- CLAUDE.md を更新して実装ワークフローを定義
- Claude Code での実装作業を効率化

---

## 使用方法

```bash
# 基本的な使い方
$ npx spec2impl docs/

# オプション
$ npx spec2impl docs/ --domain <name>    # ドメイン名を指定
$ npx spec2impl docs/ --output <dir>     # 出力先を指定
$ npx spec2impl docs/ --dry-run          # プレビュー（ファイル生成なし）
```

### 実行例

```bash
$ npx spec2impl docs/

Analyzing specifications...
✓ Found: docs/user-api.md, docs/payment-api.md

Generating implementation environment...
✓ Skills generated
✓ Subagents generated
✓ CLAUDE.md updated
✓ .mcp.json updated

⚠️  MCP Setup Required

The following MCP servers were added and require configuration:

┌─────────────────────────────────────────────────────────────┐
│ 1. slack-mcp-server                                         │
│                                                             │
│    Requires: SLACK_TOKEN                                    │
│                                                             │
│    Setup:                                                   │
│    1. Go to https://api.slack.com/apps                      │
│    2. Create an app or select existing                      │
│    3. Get OAuth token from "OAuth & Permissions"            │
│    4. Set environment variable:                             │
│       export SLACK_TOKEN=xoxp-your-token                    │
└─────────────────────────────────────────────────────────────┘

See: .claude/mcp-setup.md for detailed instructions

✨ Implementation environment ready!

Next steps:
  1. Configure required MCP servers (see above)
  2. Start Claude Code: claude
  3. Begin implementing: "User API を実装して"
```

---

## 出力ディレクトリ構造

```
project/
├── docs/                           # 入力（仕様書）
│   ├── user-api.md
│   └── payment-api.md
│
├── .claude/                        # 【生成】
│   ├── skills/
│   │   └── implementation/
│   │       ├── SKILL.md            # メインスキル
│   │       └── patterns/           # 実装パターン
│   │           ├── api.md
│   │           ├── validation.md
│   │           └── error-handling.md
│   │
│   ├── agents/
│   │   └── implementation-agents.md # Subagent 定義
│   │
│   └── mcp-setup.md                # MCP 設定ガイド
│
├── .mcp.json                       # 【生成】MCP 設定
└── CLAUDE.md                       # 【更新】実装ワークフロー
```

---

## コンポーネント仕様

### 1. Spec Analyzer

仕様書を解析して構造化データに変換します。

#### 入力

- Markdown 形式の仕様書（docs/ ディレクトリ内）

#### 出力

```typescript
interface SpecAnalysis {
  meta: {
    title: string;
    domain: string;
    version?: string;
    source: string; // ファイルパス
  };

  // API 定義
  apis: {
    name: string;
    method?: string;
    endpoint?: string;
    description: string;
    parameters: {
      name: string;
      type: string;
      required: boolean;
      description: string;
    }[];
    response?: {
      type: string;
      description: string;
    };
  }[];

  // データモデル
  models: {
    name: string;
    description: string;
    fields: {
      name: string;
      type: string;
      required: boolean;
      description: string;
    }[];
  }[];

  // ワークフロー/ユースケース
  workflows: {
    name: string;
    description: string;
    steps: string[];
  }[];

  // 制約/ルール
  constraints: {
    description: string;
    type: "validation" | "business_rule" | "security";
  }[];

  // 検出された技術スタック（MCP 推奨用）
  techStack: {
    frameworks: string[]; // React, Next.js, etc.
    databases: string[]; // PostgreSQL, MySQL, etc.
    services: string[]; // Slack, GitHub, etc.
  };
}
```

---

### 2. Skills Generator

**Core Principle: Marketplace First, Then Generate**

仕様書から必要なスキルを特定し、`marketplace-plugin-scout` で既存スキルを検索してインストール。その後、まだスキルが足りない、または作った方が良いと判断した場合に生成します。

#### 処理フロー

```
1. Identify   → 仕様書から必要なスキルを特定
2. Search     → marketplace-plugin-scout で Web 検索
3. Evaluate   → 検索結果を評価（更新日、スコア、互換性）
4. Install    → 見つかったスキルを marketplace 経由でインストール
5. Assess     → インストール後、まだ足りないスキルがあるか判断
6. Generate   → 足りないスキル、または作った方が良いスキルを生成
7. Customize  → プロジェクト固有の情報でカスタマイズ
```

#### marketplace-plugin-scout の呼び出し

```typescript
// スキル検索
Task({
  subagent_type: "marketplace-plugin-scout",
  prompt: `
    Search for skill plugins:
    - Category: api-implementation
    - Tech Stack: Express, TypeScript
    - Use Case: REST API endpoints
  `
});
```

#### marketplace でのインストール

```typescript
// 検索結果をインストール
Task({
  subagent_type: "general-purpose",
  prompt: `
    Read .claude/agents/spec2impl/marketplace.md and execute:

    Action: install
    Source: github:travisvn/awesome-claude-skills/express-api
    Type: skill
    TargetName: api-implementation
  `
});
```

#### 出力ディレクトリ

```
.claude/skills/
├── api-implementation/    [installed from GitHub]
├── data-modeling/         [installed from GitHub]
├── authentication/        [installed + customized]
├── input-validation/      [installed from npm]
├── error-handling/        [generated]
├── stripe-integration/    [installed from GitHub]
└── README.md
```

#### スキル評価基準

| 基準 | スコア |
|------|--------|
| Official Anthropic | +50 |
| travisvn/awesome-claude-* | +30 |
| 1ヶ月以内に更新 | +30 |
| 3ヶ月以内に更新 | +20 |
| Tech Stack 完全一致 | +30 |
| 1000+ npm downloads/week | +20 |
| 100+ GitHub stars | +15 |

---

### 3. Subagent Generator

検証・テスト生成用の Subagent を定義します。

#### 出力ファイル

**`.claude/agents/implementation-agents.md`**

```markdown
---
domain: implementation
generated_by: spec2impl
generated_at: <timestamp>
---

# Implementation Subagents

## 1. SpecVerifier

**Purpose**: 実装が仕様を満たしているか検証

**Trigger**:

- 実装完了時
- "verify implementation" と言われた時
- "仕様に準拠しているか確認" と言われた時

**Instructions**:
```

You are a specification verifier.

## Your Task

Verify that the implementation matches the specification.

## Steps

1. Read the specification from docs/ directory
2. Read the implementation code
3. Check each requirement:

### API Verification

- [ ] All endpoints are implemented
- [ ] HTTP methods are correct
- [ ] Request parameters match spec
- [ ] Response format matches spec
- [ ] Status codes are correct

### Model Verification

- [ ] All fields are present
- [ ] Types are correct
- [ ] Required fields are enforced

### Constraint Verification

- [ ] All validations are implemented
- [ ] Business rules are enforced
- [ ] Security requirements are met

## Output Format

Report findings as:

✅ PASS: <item> - <details>
❌ FAIL: <item> - Expected: X, Got: Y
⚠️ WARN: <item> - <concern>

## Important

- Be thorough and check every requirement
- Provide specific file locations for issues
- Suggest fixes for failures

```

---

## 2. TestGenerator

**Purpose**: 仕様からテストケースを生成

**Trigger**:
- "generate tests" と言われた時
- "テストを作成" と言われた時

**Instructions**:

```

You are a test generator.

## Your Task

Generate comprehensive tests based on the specification.

## Test Categories

### 1. Happy Path Tests

- Normal operation for each API
- Valid inputs
- Expected outputs

### 2. Validation Tests

- Missing required fields
- Invalid formats
- Out of range values

### 3. Edge Cases

- Boundary values
- Empty inputs
- Maximum lengths

### 4. Error Cases

- Not found scenarios
- Unauthorized access
- Conflict situations

## Output

Generate test files following the project's testing conventions.
Include clear descriptions for each test case.

```

---

## 3. ImplementationGuide

**Purpose**: 仕様に基づく実装支援

**Trigger**:
- "how to implement" と言われた時
- "<feature> を実装したい" と言われた時

**Instructions**:

```

You are an implementation guide.

## Your Task

Help implement features according to the specification.

## Steps

1. Identify the relevant specification section
2. Explain the requirements clearly
3. Suggest implementation approach
4. Reference patterns from .claude/skills/implementation/patterns/
5. List constraints to satisfy
6. Provide verification criteria

## Important

- Always reference the specification
- Follow established patterns
- Consider edge cases
- Remind about testing

```

```

---

### 4. MCP Configurator

**Core Principle: Marketplace First, Then Configure**

仕様書から外部サービスを検出し、`marketplace-plugin-scout` で最新の MCP サーバーを検索。最適なものを選択して設定します。

#### 処理フロー

```
1. Extract   → 仕様書から外部サービス要件を抽出
2. Search    → marketplace-plugin-scout で MCP サーバーを検索
3. Evaluate  → 公式 vs コミュニティ、更新日、ダウンロード数で評価
4. Configure → .mcp.json を生成
5. Document  → docs/mcp-setup/ にセットアップガイドを生成
```

#### marketplace-plugin-scout の呼び出し

```typescript
// MCP 検索
Task({
  subagent_type: "marketplace-plugin-scout",
  prompt: `
    Search for MCP server plugins:
    - Service: PostgreSQL
    - Category: Database
    - Use Case: SQL queries, schema introspection
  `
});
```

#### MCP 評価基準

| 基準 | スコア |
|------|--------|
| Official @modelcontextprotocol | +50 |
| 公式ベンダー（Stripe, Slackなど） | +40 |
| 1ヶ月以内に更新 | +30 |
| 3ヶ月以内に更新 | +20 |
| 1000+ npm downloads/week | +25 |
| ドキュメントが充実 | +20 |

**重要**: ハードコードされたレジストリは使用しない。常に Web 検索で最新の MCP を探す。

#### 出力ファイル

**`.mcp.json`**

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "slack-mcp-server"],
      "env": {
        "SLACK_MCP_XOXP_TOKEN": "${SLACK_TOKEN}"
      }
    }
  }
}
```

**`.claude/mcp-setup.md`**

````markdown
# MCP Setup Guide

spec2impl が推奨する MCP サーバーの設定方法です。

## 認証不要

以下の MCP はそのまま使用できます：

| MCP      | 用途                       |
| -------- | -------------------------- |
| context7 | ライブラリドキュメント参照 |

---

## 認証が必要

### Slack MCP Server

Slack ワークスペースと連携するための MCP です。

**必要な環境変数**: `SLACK_TOKEN`

**取得手順**:

1. [Slack API](https://api.slack.com/apps) にアクセス
2. 「Create New App」または既存のアプリを選択
3. 「OAuth & Permissions」に移動
4. 「User Token Scopes」で以下を追加:
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `search:read`
5. 「Install to Workspace」をクリック
6. 表示される `xoxp-` で始まるトークンをコピー

**設定方法**:

```bash
# 方法 1: 環境変数
export SLACK_TOKEN=xoxp-your-token-here

# 方法 2: .env ファイル（.gitignore に追加すること）
echo "SLACK_TOKEN=xoxp-your-token-here" >> .env
```
````

**確認**:

```bash
claude mcp list
# slack が表示されれば OK
```

---

## トラブルシューティング

### MCP が認識されない

```bash
# MCP サーバーの状態を確認
claude mcp list

# デバッグモードで起動
claude --mcp-debug
```

### 認証エラー

- 環境変数が正しく設定されているか確認
- トークンの有効期限を確認
- 必要な権限（スコープ）があるか確認

````

---

### 5. CLAUDE.md Updater

CLAUDE.md に実装環境の情報を追記します。

#### 追記内容

```markdown
<!-- spec2impl generated section - DO NOT EDIT MANUALLY -->
## 📋 Implementation Environment

> Generated by spec2impl
> Generated at: <timestamp>
> Sources: docs/user-api.md, docs/payment-api.md

### Specifications

| File | Description |
|------|-------------|
| `docs/user-api.md` | User Management API |
| `docs/payment-api.md` | Payment Processing API |

### Resources

| Type | Location | Description |
|------|----------|-------------|
| Skill | `.claude/skills/implementation/SKILL.md` | 実装パターンと制約 |
| Patterns | `.claude/skills/implementation/patterns/` | 実装パターン詳細 |
| Subagents | `.claude/agents/implementation-agents.md` | 検証・テスト生成 |
| MCP Setup | `.claude/mcp-setup.md` | MCP 設定ガイド |

### MCP Servers

| MCP | 用途 | 認証 |
|-----|------|------|
| context7 | ドキュメント参照 | 不要 |
| slack | Slack 連携 | 要設定 |

⚠️ 認証が必要な MCP は `.claude/mcp-setup.md` を参照して設定してください。

### Workflow

#### 実装開始時

````

1. Read .claude/skills/implementation/SKILL.md
2. Understand the specification for the feature
3. Follow patterns in .claude/skills/implementation/patterns/

```

#### 実装完了時

```

Use subagent SpecVerifier to verify implementation

```

#### テスト作成時

```

Use subagent TestGenerator to create tests

```

### Subagent Usage

- **検証**: `Use SpecVerifier to check if implementation matches spec`
- **テスト生成**: `Use TestGenerator to create tests for <feature>`
- **実装ガイド**: `Use ImplementationGuide to explain how to implement <feature>`

### Implementation Checklist

<!-- API実装チェックリスト -->
- [ ] POST /users - ユーザー作成
- [ ] GET /users/:id - ユーザー取得
- [ ] PUT /users/:id - ユーザー更新
- [ ] DELETE /users/:id - ユーザー削除
- [ ] POST /payments - 支払い作成
- [ ] GET /payments/:id - 支払い取得

<!-- end spec2impl generated section -->
```

---

## パッケージ構造

```
spec2impl/
├── package.json
├── tsconfig.json
├── README.md
├── LICENSE
│
├── src/
│   ├── index.ts                 # ライブラリエントリポイント
│   ├── cli.ts                   # CLI エントリポイント
│   │
│   ├── analyzer/
│   │   ├── index.ts
│   │   ├── markdown-parser.ts   # Markdown 仕様書パーサー
│   │   └── types.ts             # SpecAnalysis 型定義
│   │
│   ├── generators/
│   │   ├── index.ts
│   │   ├── skills-generator.ts  # Skills 生成
│   │   └── subagent-generator.ts # Subagent 生成
│   │
│   ├── configurators/
│   │   └── mcp-configurator.ts  # MCP 設定
│   │
│   ├── updaters/
│   │   └── claude-md-updater.ts # CLAUDE.md 更新
│   │
│   ├── templates/
│   │   ├── skill.md.hbs         # SKILL.md テンプレート
│   │   ├── agents.md.hbs        # Subagents テンプレート
│   │   ├── mcp-setup.md.hbs     # MCP設定ガイドテンプレート
│   │   ├── claude-md-section.md.hbs
│   │   └── patterns/
│   │       ├── api.md.hbs
│   │       ├── validation.md.hbs
│   │       └── error-handling.md.hbs
│   │
│   ├── mcp-registry/
│   │   └── index.ts             # MCP レジストリ
│   │
│   └── utils/
│       ├── file.ts              # ファイル操作
│       └── logger.ts            # ログ出力
│
├── templates/                    # 配布用テンプレート（src/templates のコピー）
│
└── tests/
    ├── analyzer.test.ts
    ├── generators.test.ts
    └── fixtures/
        ├── simple-api.md
        └── complex-api.md
```

---

## package.json

```json
{
  "name": "spec2impl",
  "version": "0.1.0",
  "description": "Generate Claude Code implementation environment from specification documents",
  "author": "",
  "license": "MIT",
  "keywords": [
    "claude",
    "claude-code",
    "ai",
    "skills",
    "mcp",
    "subagent",
    "specification",
    "code-generation"
  ],
  "repository": {
    "type": "git",
    "url": ""
  },
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "bin": {
    "spec2impl": "./dist/cli.js"
  },
  "files": ["dist", "templates"],
  "scripts": {
    "dev": "tsx src/cli.ts",
    "build": "tsup src/cli.ts src/index.ts --format esm --dts --clean",
    "test": "vitest",
    "lint": "eslint src/",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "commander": "^12.0.0",
    "chalk": "^5.3.0",
    "handlebars": "^4.7.8",
    "gray-matter": "^4.0.3",
    "marked": "^12.0.0",
    "ora": "^8.0.0",
    "yaml": "^2.4.0",
    "glob": "^10.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsup": "^8.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.4.0",
    "vitest": "^1.0.0",
    "eslint": "^8.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

---

## CLI 仕様

### コマンド

```bash
# メインコマンド
spec2impl <docs-directory>

# オプション
-d, --domain <name>     # ドメイン名を指定（デフォルト: 自動推測）
-o, --output <dir>      # 出力先ディレクトリ（デフォルト: カレントディレクトリ）
--dry-run               # プレビューのみ（ファイル生成なし）
--skip-mcp              # MCP 設定をスキップ
-v, --version           # バージョン表示
-h, --help              # ヘルプ表示

# サブコマンド
spec2impl validate <docs-directory>  # 仕様書の検証のみ
spec2impl init                       # 設定ファイルの初期化
```

### 終了コード

| コード | 意味                 |
| ------ | -------------------- |
| 0      | 成功                 |
| 1      | 一般的なエラー       |
| 2      | 仕様書が見つからない |
| 3      | 仕様書のパースエラー |

---

## 将来の拡張（P1 以降）

### P1: 追加機能

- OpenAPI/Swagger 仕様書のサポート
- GraphQL スキーマのサポート
- 複数ドメインの分離管理

### P2: 高度な機能

- カスタムテンプレート
- CI/CD 統合
- Slack 連携（進捗通知など）
- プライベート Plugin リポジトリのサポート

### 実装済み機能

- ✅ Marketplace からの Skills/MCP 取得 (`marketplace-plugin-scout`)
- ✅ Web Search による最新プラグイン検索
- ✅ プラグインのインストール・管理 (`marketplace`)

---

## 参考プロジェクト

- [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - ドキュメントから Skills 生成
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Skills カタログ
- [obra/superpowers](https://github.com/obra/superpowers) - Claude Code ワークフロー
- [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) - Slack MCP
