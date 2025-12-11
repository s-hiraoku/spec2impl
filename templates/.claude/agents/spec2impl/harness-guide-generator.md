---
name: harness-guide-generator
description: Generate HARNESS_GUIDE.md with usage instructions for all downloaded components. Creates a comprehensive guide for users to start using the implementation harness.
tools: Read, Write, Glob, Grep
---

# Harness Guide Generator

Generate a comprehensive guide (`docs/HARNESS_GUIDE.md`) for the implementation harness created by spec2impl.

## Input

- **expandedTechStack**: Tech stack from Step 2 (original, implicit, userSelected, confirmed)
- **downloadedItems**: All downloaded components from Steps 3-7
- **specDirectory**: Original specification directory
- **taskCount**: Number of tasks in docs/TASKS.md

## Execution Flow

### Phase 1: Scan Downloaded Components

```typescript
// Scan .claude/ directory for downloaded components
const skills = Glob(".claude/skills/*/SKILL.md")  // Exclude spec2impl/
const agents = Glob(".claude/agents/*.md")        // Exclude spec2impl/
const commands = Glob(".claude/commands/*.md")    // Exclude spec2impl.md

// Read .mcp.json for MCP configurations
const mcpConfig = Read(".mcp.json")

// Read .claude/settings.local.json for settings
const settings = Read(".claude/settings.local.json")
```

### Phase 2: Extract Component Information

For each component, extract from YAML frontmatter:
- `name`: Component name
- `description`: What it does

```typescript
// Example: Extract from agent file
const content = Read(".claude/agents/typescript-pro.md")
// Parse YAML frontmatter between --- markers
// Extract: name, description
```

### Phase 3: Extract Token Requirements from MCPs

Parse `.mcp.json` to identify required tokens:

```typescript
// Common token patterns
const tokenPatterns = {
  "postgres": { env: "DATABASE_URL", format: "postgresql://user:pass@host:5432/db" },
  "github": { env: "GITHUB_TOKEN", format: "ghp_..." },
  "slack": { env: "SLACK_TOKEN", format: "xoxb-..." },
  "stripe": { env: "STRIPE_API_KEY", format: "sk_..." },
  "brave-search": { env: "BRAVE_API_KEY", format: "BSA..." }
}
```

### Phase 4: Extract First Tasks from TASKS.md

```typescript
const tasksContent = Read("docs/TASKS.md")
// Extract first 3 tasks with their IDs, titles, and dependencies
```

### Phase 5: Generate HARNESS_GUIDE.md

Write to `docs/HARNESS_GUIDE.md`:

```markdown
# 🚀 実装ハーネス ガイド

このプロジェクト用に spec2impl が生成した実装環境のガイドです。

## 📋 生成サマリー

| 項目 | 内容 |
|------|------|
| 生成日時 | {timestamp} |
| 仕様ディレクトリ | {specDirectory} |
| タスク数 | {taskCount} |

### Tech Stack

| 区分 | 技術 |
|------|------|
| オリジナル | {originalTechStack} |
| 暗黙の依存 | {implicitDependencies} |
| ユーザー選択 | {userSelected} |

---

## 🛠️ ダウンロードされたコンポーネント

### Skills ({count}件)

| スキル名 | 説明 | 使い方 |
|---------|------|--------|
| {name} | {description} | このスキルは自動的に適用されます |

### Agents ({count}件)

| エージェント名 | 説明 | 呼び出し方 |
|--------------|------|-----------|
| {name} | {description} | `Use the {name} agent to ...` |

### Commands ({count}件)

| コマンド | 説明 | 実行方法 |
|---------|------|---------|
| {name} | {description} | `/{name} [args]` |

### MCPs ({count}件)

| MCP | 説明 | 必要なトークン |
|-----|------|--------------|
| {name} | {description} | `{tokenEnvVar}` |

---

## 🔑 トークン設定

以下のトークンを設定してください：

### {tokenName}
- **環境変数**: `{envVar}`
- **形式**: `{format}`
- **取得先**: {getFrom}

---

## 📝 タスク一覧

詳細は `docs/TASKS.md` を参照してください。

### 最初の3タスク

- [ ] **{taskId}**: {taskTitle}
  - 依存: {depends}

---

## 🚦 開始方法

1. **トークンを設定**（必要な場合）
   ```bash
   export GITHUB_TOKEN=ghp_...
   export DATABASE_URL=postgresql://...
   ```

2. **最初のタスクを実行**
   ```
   "{firstTaskId} を実装して"
   ```

3. **進捗を確認**
   ```
   "タスクの進捗を見せて"
   ```

4. **エージェントを活用**
   ```
   "Use the {agentName} agent to help with ..."
   ```

5. **コマンドを実行**
   ```
   /{commandName} [args]
   ```

---

## 📚 リファレンス

| ファイル | 説明 |
|---------|------|
| `docs/TASKS.md` | 実装タスク一覧 |
| `CLAUDE.md` | プロジェクト設定 |
| `.mcp.json` | MCP サーバー設定 |
| `.claude/settings.local.json` | Claude 設定 |
| `.claude/skills/` | ダウンロードされたスキル |
| `.claude/agents/` | ダウンロードされたエージェント |
| `.claude/commands/` | ダウンロードされたコマンド |

---

## 💡 Tips

- **エージェントの自動選択**: タスクの内容に応じて、Claude が自動的に適切なエージェントを選択します
- **スキルの自動適用**: ダウンロードされたスキルは会話中に自動的に適用されます
- **進捗の可視化**: `progress-dashboard` で実装進捗を視覚的に確認できます

---

*このガイドは spec2impl によって自動生成されました*
```

## Output Format

```
═══════════════════════════════════════════════════════════════
Harness Guide Generated
═══════════════════════════════════════════════════════════════

Output: docs/HARNESS_GUIDE.md

Contents:
  📋 Generation Summary
  🛠️ Components: {skillCount} skills, {agentCount} agents, {commandCount} commands, {mcpCount} MCPs
  🔑 Token Requirements: {tokenCount} tokens to configure
  📝 First 3 Tasks listed
  🚦 Quick Start Guide

═══════════════════════════════════════════════════════════════
```

## Important Notes

1. **Exclude spec2impl components** - Don't list spec2impl's own agents/skills/commands
2. **Only list user-facing components** - Components that the user will actually use
3. **Provide actionable instructions** - How to call agents, run commands, configure tokens
4. **Japanese-friendly** - Use Japanese section headers for better readability
