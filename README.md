# spec2impl

仕様書ドキュメントから Claude Code 用の実装環境を自動構築するツール。

## 概要

spec2impl は、Markdown 形式の仕様書を解析し、Claude Code での実装を支援する以下の環境を自動生成します：

- **Skills** - 仕様書に基づいた実装パターンとガイド
- **Subagents** - 検証・テスト生成・実装支援エージェント
- **MCP 設定** - 技術スタックに応じた推奨 MCP サーバー
- **タスクリスト** - 実装タスクの自動抽出と管理
- **CLAUDE.md** - 実装ワークフローの定義

## 特徴

- **Claude Code のネイティブ機能として動作** - カスタムスラッシュコマンドとして実装
- **Claude の知性を活用** - 静的解析ではなく、Claude が仕様書の意図を理解して生成
- **段階的な承認フロー** - 各ステップでユーザーの承認を得ながら進行
- **タスク引き継ぎ対応** - エージェントが中断しても、タスクリストで確実に引き継ぎ

## インストール

このプロジェクトの `.claude/` ディレクトリをあなたのプロジェクトにコピーしてください：

```bash
# このリポジトリをクローン
git clone https://github.com/your-repo/spec2impl.git

# .claude ディレクトリをコピー
cp -r spec2impl/.claude /path/to/your/project/
```

または、手動で以下のファイルをコピー：

```
.claude/
├── commands/
│   └── spec2impl.md
└── agents/
    └── spec2impl/
        ├── spec-analyzer.md
        ├── skills-generator.md
        ├── subagent-generator.md
        ├── mcp-configurator.md
        ├── task-list-generator.md
        ├── claude-md-updater.md
        ├── marketplace.md
        └── progress-dashboard.md
```

## 使用方法

### 基本的な使い方

Claude Code を起動し、以下のコマンドを実行：

```
/spec2impl docs/
```

これにより、`docs/` ディレクトリ内の仕様書を解析し、実装環境を構築します。

### 実行フロー

```
/spec2impl docs/
         ↓
Step 1: 仕様書解析 → 承認
Step 2: Skills 生成 → 承認
Step 3: Subagents 生成 → 承認
Step 4: MCP 設定 → 承認
Step 5: タスクリスト生成 → 承認
Step 6: CLAUDE.md 更新 → 承認
         ↓
完了レポート
```

各ステップで結果を確認し、承認してから次に進みます。

### 生成されるファイル

| ファイル | 説明 |
|----------|------|
| `.claude/skills/implementation/SKILL.md` | 仕様書に基づく実装スキル |
| `.claude/skills/implementation/patterns/*.md` | 実装パターン（API、バリデーション、エラーハンドリング） |
| `.claude/agents/implementation-agents.md` | 検証・テスト生成サブエージェント |
| `.mcp.json` | MCP サーバー設定 |
| `.claude/mcp-setup.md` | MCP セットアップガイド |
| `docs/TASKS.md` | 実装タスクリスト |
| `CLAUDE.md` | 実装ワークフロー（更新） |

## コマンドリファレンス

### メインコマンド

```
/spec2impl <docs-directory>
```

仕様書を解析し、実装環境を構築します。

**オプション:**
- `--dry-run` - プレビューのみ（ファイル生成なし）
- `--skip-mcp` - MCP 設定をスキップ
- `--force` - 承認なしで実行（非推奨）

### マーケットプレイス

```
/spec2impl marketplace search <query>   # Skills を検索
/spec2impl marketplace install <source> # Skills をインストール
/spec2impl marketplace list             # インストール済み一覧
/spec2impl marketplace uninstall <name> # Skills をアンインストール
```

**ソース形式:**
- `github:user/repo[/path][@branch]` - GitHub リポジトリから
- `npm:@scope/package[@version]` - npm パッケージから
- `https://...` - URL から直接

### 進捗ダッシュボード

```
/spec2impl dashboard
```

実装の進捗状況を視覚的に表示します。

## 生成されるサブエージェント

実装環境を構築すると、以下のサブエージェントが利用可能になります：

### SpecVerifier

実装が仕様を満たしているか検証します。

```
verify implementation
実装を検証して
```

### TestGenerator

仕様からテストケースを生成します。

```
generate tests for User API
User API のテストを作成して
```

### ImplementationGuide

実装の手順をガイドします。

```
how to implement user creation
ユーザー作成の実装方法を教えて
```

## 仕様書の書き方

spec2impl は以下のパターンを認識します：

### API 定義

```markdown
### POST /users

ユーザーを作成します。

**Parameters:**
- email (string, required): メールアドレス
- name (string, required): 名前

**Response:**
- 201: User object
- 400: Validation error
```

### データモデル

```markdown
### User モデル

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | ユーザーID |
| email | string | Yes | メールアドレス |
| name | string | Yes | 名前 |
```

### 制約/ルール

```markdown
## Constraints

- メールアドレスは一意である必要がある
- パスワードは 8 文字以上
```

### チェックリスト

```markdown
## Implementation Checklist

- [ ] POST /users - ユーザー作成
- [ ] GET /users/:id - ユーザー取得
```

## タスク管理

`docs/TASKS.md` は以下の情報を含みます：

- **Spec-Defined Tasks** - 仕様書から抽出されたタスク
- **Auto-Generated Tasks** - API/モデルから自動生成されたタスク
- **Verification Tasks** - 検証タスク
- **Handoff Notes** - エージェント間の引き継ぎメモ

タスクを実行する際は、タスクの Source を確認して仕様書の該当箇所を参照してください。

## ライセンス

MIT

## 関連プロジェクト

- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Claude Skills カタログ
- [Claude Code](https://claude.ai/claude-code) - Anthropic の CLI ツール
