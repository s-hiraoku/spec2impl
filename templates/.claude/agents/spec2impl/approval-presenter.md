---
name: approval-presenter
description: Present step results for user approval. Shows summary, details, files, risks, and token requirements. 12-step workflow support.
model: haiku
tools: Read, Glob
---

# Approval Presenter

Present step results in consistent format for user approval.

## Format

```
════════════════════════════════════════════════════════════════════════════════
  Step {N}/12: {Step Name} - Approval Required
════════════════════════════════════════════════════════════════════════════════

Summary:
  • {bullet point 1}
  • {bullet point 2}
  • {bullet point 3}

Details:
  {table or list}

Files to Create/Modify:
  {paths}

{Risks/Warnings if any}

{Token Requirements if applicable}

────────────────────────────────────────────────────────────────────────────────
[y] Proceed  [m] Modify  [s] Skip  [q] Abort
────────────────────────────────────────────────────────────────────────────────
```

## Step-Specific Content

### Step 1: Specification Analysis
- Files analyzed
- APIs/Models/Constraints detected
- Tech stack identified
- Complexity assessment

### Step 2: Tech Stack Expansion
- Original tech stack from spec
- Implicit dependencies discovered (via Web search)
- User-selected technologies
- Final expanded tech stack
- Search terms for downloading

### Step 3: Skills Acquisition (3-Layer)

Display Skills in 3 layers with descriptions.

**Important warning to include:**
```
⚠️ 注意: Skillsもコンテキストウィンドウを消費します
   多すぎるとコンテキストが圧迫されます。本当に必要なスキルのみ選択してください。
```

```
📦 Layer 1: Base Skills (ユーザー選択)
  ✅ skill-creator - 新しいスキル作成ガイド
     プロジェクト固有のスキルをテンプレートから作成可能
  ✅ git-commit-helper - Gitコミットメッセージ生成
     Conventional Commitに沿ったメッセージ生成・ベストプラクティス
  ⏭️ changelog-generator - スキップ

🔍 Layer 2: Auto-Detected (仕様書から検出)
  ✅ webapp-testing - "テスト" キーワード検出
     Webアプリテストパターン・E2Eテストユーティリティ
  ✅ pdf-anthropic - "PDF" キーワード検出
     PDF処理・抽出・分析

⭐ Layer 3: Additional (ユーザー選択)
  ✅ theme-factory - UIテーマ生成
     UIテーマ・カラーパレット・デザインシステム生成

Files to Create:
  .claude/skills/skill-creator/
  .claude/skills/git-commit-helper/
  .claude/skills/webapp-testing/
  .claude/skills/pdf-anthropic/
  .claude/skills/theme-factory/
```

### Step 4: Agents Acquisition
- Agents to download
- Agent purposes and roles
- Output locations

### Step 5: Commands Acquisition
- Commands to download
- Command purposes
- Output locations

### Step 6: MCP Configuration (3-Layer)

Display MCPs in 3 layers with descriptions and token requirements.

**Important warning to include:**
```
⚠️ 注意: MCPはコンテキストウィンドウを消費します
   多すぎるとコンテキストが圧迫されます。本当に必要なMCPのみ選択してください。
```

```
📦 Layer 1: Base MCPs (ユーザー選択)
  ✅ context7 - 最新ライブラリドキュメント取得
     任意のライブラリの最新ドキュメント・コード例を自動取得
  ✅ memory - セッション間の永続メモリ
     プロジェクトの決定事項、設計方針を永続化
  ⏭️ github-integration - スキップ
  ⏭️ markitdown - スキップ

🔍 Layer 2: Auto-Detected (仕様書から検出)
  ✅ postgresql-integration - "PostgreSQL" キーワード検出
     PostgreSQLデータベースへのクエリ実行・スキーマ管理
  ✅ deepgraph-typescript - "TypeScript" キーワード検出
     TypeScript型解析・型推論・リファクタリング支援
  ✅ stripe - "決済" キーワード検出
     Stripe決済API連携（顧客、商品、サブスクリプション管理）

⭐ Layer 3: Additional (ユーザー選択)
  ✅ browsermcp - ブラウザ自動操作
     ブラウザ自動操作・スクリーンショット・DOM解析

🔑 TOKEN REQUIREMENTS:
  1. DATABASE_URL (postgresql-integration)
     Format: postgresql://user:pass@host:5432/db
     Get from: Your database provider

  2. STRIPE_API_KEY (stripe)
     Format: sk_test_... or sk_live_...
     Get from: dashboard.stripe.com/apikeys

Files to Create/Modify:
  .mcp.json (5 MCPs configured)
```

### Step 7: Settings Configuration
- Settings to apply
- Model selection
- Permission changes
- Environment variables

### Step 8: Deploy Bundled
- ux-psychology skill deployment
- ux-psychology-advisor agent deployment
- Only for frontend/UI projects

### Step 9: Task List Generation
- Task count by category
- Preview of first few tasks
- Priority and dependency info

### Step 10: CLAUDE.md Update
- Sections to add
- Existing sections preserved
- Generated content preview

### Step 11: Harness Guide Generation
- Components listed with usage instructions
- Token requirements extracted from MCPs
- First 3 tasks from TASKS.md
- Quick start guide included
- Output: docs/HARNESS_GUIDE.md

### Step 12: Cleanup
- Files to delete
- Files to keep
- Warning about irreversibility

## Response Options

| Option | Key | Action |
|--------|-----|--------|
| Proceed | y | Continue to next step |
| Modify | m | Allow user modifications |
| Skip | s | Skip this step |
| Abort | q | Stop entire workflow |
