# spec2impl - 仕様書から実装環境を構築

仕様書ドキュメントを解析し、Claude Code での実装を支援する環境を自動構築します。

## 引数

- `$ARGUMENTS`: 仕様書が格納されているディレクトリパス（例: `docs/`）

## あなたの役割

あなたは spec2impl のオーケストレーターです。以下の責務を持ちます：

1. 各サブエージェントを順次呼び出し、実装環境を構築する
2. 各ステップで進捗を表示し、ユーザーの承認を得る
3. エラーが発生した場合は適切に対処する

## 実行手順

以下の 6 ステップを順次実行してください。各ステップで必ずユーザーの承認を得てから次に進みます。

---

### Step 1: 仕様書解析

**サブエージェント:** SpecAnalyzer (`.claude/agents/spec2impl/spec-analyzer.md`)

1. 指定されたディレクトリ `$ARGUMENTS` 内の Markdown ファイル（*.md）を Glob で検索
2. 各ファイルを Read で読み込み
3. 以下の情報を抽出:
   - API 定義（エンドポイント、メソッド、パラメータ、レスポンス）
   - データモデル（フィールド、型、制約）
   - ワークフロー/ユースケース
   - 制約/ビジネスルール
   - 技術スタック（フレームワーク、DB、外部サービス）
4. 仕様書の品質チェック（曖昧な記述、矛盾の検出）
5. 結果をユーザーに提示し、承認を求める

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 1/6: 仕様書解析
───────────────────────────────────────

対象ディレクトリ: $ARGUMENTS

検出されたファイル:
  - docs/xxx.md
  - docs/yyy.md

解析結果サマリー:
  - API: X 個のエンドポイント
  - モデル: X 個
  - 制約: X 個
  - 技術スタック: [xxx, yyy]

⚠️ 警告: (あれば表示)

✅ この解析結果で進めてよいですか？
   [y] はい  [n] いいえ（再解析）  [q] 中止
───────────────────────────────────────
```

---

### Step 2: Skills 生成

**サブエージェント:** SkillsGenerator (`.claude/agents/spec2impl/skills-generator.md`)

1. Step 1 の解析結果を基に以下を生成:
   - `.claude/skills/implementation/SKILL.md` - メイン実装スキル
   - `.claude/skills/implementation/patterns/api.md` - API 実装パターン
   - `.claude/skills/implementation/patterns/validation.md` - バリデーションパターン
   - `.claude/skills/implementation/patterns/error-handling.md` - エラーハンドリングパターン
2. 生成内容のプレビューを表示
3. ユーザーの承認を得てからファイルを書き込み

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 2/6: Skills 生成
───────────────────────────────────────

生成予定ファイル:
  - .claude/skills/implementation/SKILL.md
  - .claude/skills/implementation/patterns/api.md
  - .claude/skills/implementation/patterns/validation.md
  - .claude/skills/implementation/patterns/error-handling.md

SKILL.md プレビュー:
  (概要を表示)

✅ この Skills を生成してよいですか？
   [y] はい  [n] いいえ（修正）  [s] スキップ  [q] 中止
───────────────────────────────────────
```

---

### Step 3: Subagents 生成

**サブエージェント:** SubagentGenerator (`.claude/agents/spec2impl/subagent-generator.md`)

1. 以下のサブエージェント定義を生成:
   - **SpecVerifier** - 実装が仕様を満たしているか検証
   - **TestGenerator** - 仕様からテストケースを生成
   - **ImplementationGuide** - 実装の手順をガイド
2. `.claude/agents/implementation-agents.md` に出力
3. ユーザーの承認を得てからファイルを書き込み

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 3/6: Subagents 生成
───────────────────────────────────────

生成予定ファイル:
  - .claude/agents/implementation-agents.md

生成されるサブエージェント:
  1. SpecVerifier - 実装検証
  2. TestGenerator - テスト生成
  3. ImplementationGuide - 実装ガイド

✅ この Subagents を生成してよいですか？
   [y] はい  [n] いいえ（修正）  [s] スキップ  [q] 中止
───────────────────────────────────────
```

---

### Step 4: MCP 設定

**サブエージェント:** McpConfigurator (`.claude/agents/spec2impl/mcp-configurator.md`)

1. 検出された技術スタックから推奨 MCP を選定
2. `.mcp.json` を生成（既存があればマージ）
3. `.claude/mcp-setup.md` にセットアップ手順を生成
4. ユーザーの承認を得てからファイルを書き込み

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 4/6: MCP 設定
───────────────────────────────────────

推奨 MCP サーバー:
  ✅ context7 - ドキュメント参照（認証不要）
  ⚠️ postgres - DB 操作（要設定: POSTGRES_URL）
  ⚠️ slack - Slack 連携（要設定: SLACK_TOKEN）

生成予定ファイル:
  - .mcp.json
  - .claude/mcp-setup.md

✅ この MCP 設定でよいですか？
   [y] はい  [n] いいえ（修正）  [s] スキップ  [q] 中止
───────────────────────────────────────
```

---

### Step 5: タスクリスト生成

**サブエージェント:** TaskListGenerator (`.claude/agents/spec2impl/task-list-generator.md`)

1. 仕様書から既存のタスク/チェックリストを探索:
   - `- [ ]` 形式のチェックボックス
   - Verification Checklist
   - Implementation Checklist
   - ワークフローの steps
   - TODO/FIXME コメント
2. API/モデルから自動生成タスクを作成
3. 両者を統合し、依存関係を考慮して順序付け
4. `docs/TASKS.md` を生成
5. ユーザーの承認を得てからファイルを書き込み

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 5/6: タスクリスト生成
───────────────────────────────────────

タスク集計:
  📋 仕様書から抽出: X 個
  🤖 自動生成: X 個
  ✅ 検証タスク: X 個
  ─────────────────
  合計: X 個

生成予定ファイル:
  - docs/TASKS.md

タスク一覧プレビュー:
  (最初の数個を表示)

✅ このタスクリストでよいですか？
   [y] はい  [n] いいえ（修正）  [s] スキップ  [q] 中止
───────────────────────────────────────
```

---

### Step 6: CLAUDE.md 更新

**サブエージェント:** ClaudeMdUpdater (`.claude/agents/spec2impl/claude-md-updater.md`)

1. 既存の CLAUDE.md を読み込み（なければ新規作成）
2. spec2impl セクションを追加/更新:
   - 仕様書一覧
   - 生成されたリソース一覧
   - MCP サーバー一覧
   - ワークフロー説明
   - サブエージェントの使い方
3. 既存の内容を壊さないようにマージ
4. ユーザーの承認を得てからファイルを書き込み

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 6/7: CLAUDE.md 更新
───────────────────────────────────────

更新内容:
  - Implementation Environment セクションを追加
  - 仕様書リファレンスを追加
  - ワークフローガイドを追加

✅ CLAUDE.md を更新してよいですか？
   [y] はい  [n] いいえ（修正）  [s] スキップ  [q] 中止
───────────────────────────────────────
```

---

### Step 7: spec2impl ツールのクリーンアップ

実装環境の構築が完了したら、spec2impl 自体のファイル（コマンド、エージェント、skill-creator）は不要になります。
ユーザーの承認を得て、これらを削除します。

**削除対象ファイル:**
- `.claude/commands/spec2impl.md` - このコマンド自体
- `.claude/agents/spec2impl/` - spec2impl のサブエージェント群
- `.claude/skills/skill-creator/` - Skill 生成用ツール

**保持するファイル（生成されたもの）:**
- `.claude/skills/` 配下の生成された Skills（skill-creator 以外）
- `.claude/agents/` 配下の生成されたエージェント（spec2impl/ 以外）
- `docs/TASKS.md`
- `CLAUDE.md`
- `.mcp.json`
- `docs/mcp-setup/`

**進捗表示:**
```
───────────────────────────────────────
📋 spec2impl - Step 7/7: クリーンアップ
───────────────────────────────────────

実装環境の構築が完了しました。

spec2impl ツール自体はもう不要です。
以下のファイルを削除しますか？

削除対象:
  🗑️ .claude/commands/spec2impl.md
  🗑️ .claude/agents/spec2impl/ (8 files)
  🗑️ .claude/skills/skill-creator/ (6 files)

保持されるファイル:
  ✅ .claude/skills/[生成された Skills]
  ✅ .claude/agents/[生成されたエージェント]
  ✅ docs/TASKS.md
  ✅ CLAUDE.md
  ✅ .mcp.json
  ✅ docs/mcp-setup/

✅ spec2impl ツールを削除してよいですか？
   [y] はい（削除）  [n] いいえ（残す）
───────────────────────────────────────
```

**実行手順:**

1. 削除対象ファイルの一覧を表示
2. 保持されるファイル（生成物）の一覧を表示
3. ユーザーの承認を求める
4. 承認された場合:
   - `rm .claude/commands/spec2impl.md`
   - `rm -rf .claude/agents/spec2impl/`
   - `rm -rf .claude/skills/skill-creator/`
5. 承認されなかった場合:
   - ファイルを残して完了レポートへ進む

---

## 完了レポート

全ステップ完了後、以下の形式でレポートを表示:

```
═══════════════════════════════════════════════════════════
✨ spec2impl 完了
═══════════════════════════════════════════════════════════

生成されたファイル:
  ✅ .claude/skills/implementation/SKILL.md
  ✅ .claude/skills/implementation/patterns/api.md
  ✅ .claude/skills/implementation/patterns/validation.md
  ✅ .claude/skills/implementation/patterns/error-handling.md
  ✅ .claude/agents/implementation-agents.md
  ✅ .mcp.json
  ✅ .claude/mcp-setup.md
  ✅ docs/TASKS.md
  ✅ CLAUDE.md (updated)

⚠️ 要対応:
  - MCP 設定が必要です。詳細は .claude/mcp-setup.md を参照

次のステップ:
  1. MCP サーバーを設定（必要な場合）
  2. docs/TASKS.md でタスクを確認
  3. 実装を開始: 「T-SPEC-1 を実装して」

═══════════════════════════════════════════════════════════
```

---

## エラーハンドリング

### 仕様書が見つからない場合
```
❌ エラー: 指定されたディレクトリに Markdown ファイルが見つかりません

対象ディレクトリ: $ARGUMENTS

確認してください:
  - パスが正しいか
  - *.md ファイルが存在するか
  - ファイルの読み取り権限があるか
```

### ユーザーが中止した場合
```
🛑 処理を中止しました

生成済みファイル: (あれば一覧表示)

中止時点: Step X/6

再開する場合は /spec2impl $ARGUMENTS を実行してください。
```

---

## 追加コマンド

### マーケットプレイス
```
/spec2impl marketplace search <query>  - Skills を検索
/spec2impl marketplace install <source> - Skills をインストール
/spec2impl marketplace list            - インストール済み一覧
```

### 進捗ダッシュボード
```
/spec2impl dashboard  - 実装進捗を表示
```

---

## 重要な注意事項

1. **必ず各ステップで承認を得る** - ユーザーが `y` を入力するまで次に進まない
2. **既存ファイルの扱い** - 上書き前に必ず確認する
3. **エラー時は詳細を報告** - 問題箇所と対処法を明示する
4. **進捗を可視化** - 現在のステップと残りを常に表示する
