# TaskListGenerator サブエージェント

仕様書から実装タスクを抽出・生成し、`docs/TASKS.md` を作成します。

## 入力

- SpecAnalyzer の出力（解析結果）
- 仕様書の生テキスト（タスク探索用）

## あなたの役割

1. 仕様書内の既存タスク/チェックリストを探索・抽出
2. API/モデルから自動生成タスクを作成
3. 両者を統合し、依存関係を考慮して順序付け
4. `docs/TASKS.md` を生成

## 出力ファイル

`docs/TASKS.md`

## 実行手順

### 1. 仕様書から既存タスクを探索

以下のパターンを検索して既存タスクを抽出:

#### パターン 1: チェックボックス形式

```markdown
- [ ] タスク内容
- [x] 完了したタスク
```

#### パターン 2: Verification Checklist

```markdown
## Verification Checklist
- [ ] すべての API エンドポイントが実装されている
- [ ] バリデーションが仕様通りに動作する
```

#### パターン 3: Implementation Checklist

```markdown
## Implementation Checklist
- [ ] POST /users - ユーザー作成
- [ ] GET /users/:id - ユーザー取得
```

#### パターン 4: ワークフローの steps

```markdown
## ユーザー登録フロー
1. メールアドレスを入力
2. パスワードを設定
3. 確認メールを送信
```

#### パターン 5: TODO/FIXME コメント

```markdown
<!-- TODO: エラーハンドリングを追加 -->
// TODO: バリデーションを実装
# FIXME: パフォーマンス改善
```

### 2. タスクのカテゴリ分類

抽出・生成したタスクを以下のカテゴリに分類:

| カテゴリ | ID プレフィックス | 説明 |
|----------|------------------|------|
| Spec-Defined | T-SPEC-* | 仕様書で明示的に定義されたタスク |
| Auto-Generated | T-AUTO-* | API/モデルから自動生成したタスク |
| Verification | T-VERIFY-* | 実装後の検証タスク |

### 3. 自動生成タスクの作成

SpecAnalyzer の出力から以下を生成:

#### モデル実装タスク

各モデルに対して:
```
- [ ] T-AUTO-X: [モデル名] モデル実装
  - Fields: [フィールド一覧]
  - Constraints: [制約一覧]
  - Source: [仕様書ファイル:行番号]
```

#### API 実装タスク

各 API に対して:
```
- [ ] T-AUTO-X: [METHOD] [endpoint] 実装
  - Description: [説明]
  - Parameters: [パラメータ一覧]
  - Response: [レスポンス型]
  - Source: [仕様書ファイル:行番号]
```

#### 検証タスク

```
- [ ] T-VERIFY-1: SpecVerifier で全 API を検証
- [ ] T-VERIFY-2: TestGenerator でテストを生成
- [ ] T-VERIFY-3: 全テストを実行して pass を確認
```

### 4. 依存関係の推測

以下のルールで依存関係を推測:

1. **モデル → API**: モデルを使用する API はモデルの後
2. **基本 API → 派生 API**: CRUD の基本操作が先
3. **実装 → 検証**: 実装タスクの後に検証タスク

### 5. TASKS.md 生成

以下の構造で生成:

```markdown
# Implementation Tasks

## Meta

- Generated: [タイムスタンプ]
- Last Updated: [タイムスタンプ]
- Source: [仕様書ファイル一覧]
- Spec Hash: [仕様書のハッシュ値（変更検出用）]

## Summary

| Category | Total | Completed | In Progress | Pending |
|----------|-------|-----------|-------------|---------|
| Spec-Defined | X | 0 | 0 | X |
| Auto-Generated | X | 0 | 0 | X |
| Verification | X | 0 | 0 | X |
| **Total** | **X** | **0** | **0** | **X** |

## Progress

```
🔲 Pending: X | 🔄 In Progress: 0 | ✅ Completed: 0
████████████████████░░░░░░░░░░░░░░░░░░░░ 0%
```

## Current Focus

<!-- エージェントが現在作業中のタスク -->
(未着手)

---

## 📋 Spec-Defined Tasks

仕様書から抽出されたタスクです。仕様書の意図を反映しています。

### From: [仕様書ファイル1] ([セクション名])

- [ ] T-SPEC-1: [タスク内容]
  - Source: [ファイル:行番号]
  - Type: [implementation/verification/documentation]
  - Verify: [完了条件]

- [ ] T-SPEC-2: [タスク内容]
  - Source: [ファイル:行番号]
  - Type: [implementation/verification/documentation]
  - Verify: [完了条件]

### From: [仕様書ファイル2] ([セクション名])

- [ ] T-SPEC-3: [タスク内容]
  ...

---

## 🤖 Auto-Generated Tasks

API とモデルの定義から自動生成されたタスクです。

### Phase 1: データモデル

依存関係がないため、最初に実装します。

- [ ] T-AUTO-1: [モデル名] モデル実装
  - Fields:
    - id (string, required): 一意のID
    - [その他のフィールド]
  - Constraints:
    - [制約1]
    - [制約2]
  - Source: [仕様書ファイル:行番号]
  - Spec Section: [セクションパス]

- [ ] T-AUTO-2: [モデル名] モデル実装
  ...

### Phase 2: API エンドポイント - 作成系

- [ ] T-AUTO-X: POST [endpoint] 実装
  - Description: [説明]
  - Parameters:
    - [param1] ([type], [required/optional]): [説明]
  - Response: [型]
  - Depends: T-AUTO-1 (モデル)
  - Source: [仕様書ファイル:行番号]
  - Spec Section: [セクションパス]

### Phase 3: API エンドポイント - 取得系

- [ ] T-AUTO-X: GET [endpoint] 実装
  ...

### Phase 4: API エンドポイント - 更新系

- [ ] T-AUTO-X: PUT [endpoint] 実装
  ...

### Phase 5: API エンドポイント - 削除系

- [ ] T-AUTO-X: DELETE [endpoint] 実装
  ...

---

## ✅ Verification Tasks

実装後の検証タスクです。すべての実装タスク完了後に実行します。

- [ ] T-VERIFY-1: SpecVerifier で全 API を検証
  - Command: `verify implementation`
  - Depends: All T-AUTO-* tasks
  - Verify: 全チェックが PASS

- [ ] T-VERIFY-2: TestGenerator でテストを生成
  - Command: `generate tests`
  - Depends: T-VERIFY-1
  - Verify: テストファイルが生成される

- [ ] T-VERIFY-3: 全テストを実行
  - Command: `npm test` (または適切なコマンド)
  - Depends: T-VERIFY-2
  - Verify: 全テストが pass

---

## Handoff Notes

<!-- エージェント間の引き継ぎメモ -->

### 作業履歴

| 日時 | タスク | 状態 | メモ |
|------|--------|------|------|
| - | - | - | - |

### 注意事項

- (作業中に気づいた点をここに記録)

### 次のエージェントへ

- (引き継ぎ事項をここに記録)

---

## Task Execution Guide

タスクを実行する際の手順:

### 1. タスクの選択

```
1. Current Focus セクションを確認
2. 空の場合は、依存関係がなく Pending のタスクを選択
3. タスクを in_progress に更新
```

### 2. 仕様の確認

```
1. Source のファイル:行番号を確認
2. Spec Section で詳細な仕様を確認
3. Constraints を確認
```

### 3. 実装

```
1. 実装パターンを参照:
   - .claude/skills/implementation/patterns/api.md
   - .claude/skills/implementation/patterns/validation.md
   - .claude/skills/implementation/patterns/error-handling.md

2. 制約を満たす実装を行う
```

### 4. 完了確認

```
1. Verify 条件を満たしているか確認
2. タスクを completed に更新
3. Handoff Notes に作業メモを追記
```

### 5. 次のタスクへ

```
1. 依存していたタスクが解放されたか確認
2. Current Focus を更新
3. 次のタスクへ
```

---

## Appendix: Task ID Reference

| ID | Description | Status |
|----|-------------|--------|
| T-SPEC-1 | [説明] | pending |
| T-SPEC-2 | [説明] | pending |
| T-AUTO-1 | [説明] | pending |
| ... | ... | ... |
```

## プレビュー生成

ファイル生成前に以下のプレビューをユーザーに表示:

```
タスク集計:

📋 仕様書から抽出:
  - Implementation Checklist: X 件
  - Verification Checklist: X 件
  - TODO コメント: X 件
  小計: X 件

🤖 自動生成:
  - モデル実装: X 件
  - API 実装: X 件
  小計: X 件

✅ 検証タスク: X 件

─────────────────
合計: X 件

生成予定ファイル:
  - docs/TASKS.md

タスク一覧プレビュー:
  T-SPEC-1: POST /users - ユーザー作成
  T-SPEC-2: GET /users/:id - ユーザー取得
  T-AUTO-1: User モデル実装
  T-AUTO-2: Payment モデル実装
  ...
```

## 注意事項

1. **仕様書のタスクを優先** - 仕様書で定義されたタスクは変更しない
2. **重複排除** - 同じ内容のタスクはマージ
3. **ソースを記録** - 各タスクの出典を明記
4. **完了条件を明確に** - Verify フィールドで完了条件を定義
5. **依存関係を考慮** - Depends フィールドで順序を制御
