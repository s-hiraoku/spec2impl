# Skills Category Guide

Download skill templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/skills`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/skills`

## Output Directory

- Target: `.claude/skills/`

---

## 3-Layer Skills Configuration

> ⚠️ **注意: Skillsもコンテキストウィンドウを消費します**
>
> 各スキルはセッション開始時に読み込まれるため、**インストールするスキルが多いほどコンテキストウィンドウが圧迫**されます。
> - 本当に必要なスキルのみを選択してください
> - 使用頻度の低いスキルは後から追加できます
> - 迷った場合は最小限（skill-creator のみ）から始めることを推奨

### Layer 1: Recommended Base Skills (User Selection)

Present these via `AskUserQuestion` with multiSelect. Useful for general development.

```typescript
AskUserQuestion({
  questions: [{
    question: "基本スキルをインストールしますか？開発全般で有用なスキルです。",
    header: "基本スキル",
    options: [
      {
        label: "skill-creator (推奨)",
        description: "新しいスキル作成ガイド。プロジェクト固有のスキルを作成可能"
      },
      {
        label: "git-commit-helper",
        description: "Gitコミットメッセージ生成・Conventional Commitベストプラクティス"
      },
      {
        label: "changelog-generator",
        description: "Gitコミットから CHANGELOG を自動生成"
      }
    ],
    multiSelect: true
  }]
})
```

**Skill Details:**

| Skill | Description | Use Case |
|-------|-------------|----------|
| `skill-creator` | 新しいClaude Codeスキルをテンプレートから作成 | どのプロジェクトでも固有スキルを作れる |
| `git-commit-helper` | Conventional Commitに沿ったメッセージ生成 | ほぼ全プロジェクトで使用 |
| `changelog-generator` | コミット履歴からCHANGELOG自動生成 | リリース管理で有用 |

---

### Layer 2: Auto-Detected Skills (Spec-based)

These skills are **automatically detected** from specification keywords. Show detected items to user for confirmation.

| Keywords in Spec | Skill | Description |
|------------------|-------|-------------|
| PDF, 帳票, レポート, document | `pdf-anthropic` | PDF処理・抽出・分析 |
| Word, docx, 文書 | `docx` | Word文書生成・編集 |
| Excel, xlsx, 表計算, spreadsheet | `xlsx` | Excel処理・生成 |
| テスト, testing, E2E, QA | `webapp-testing` | Webアプリテストパターン |
| MCP, サーバー連携, protocol | `mcp-builder` | MCPサーバー構築ガイド |
| Zapier, 自動化, webhook, automation | `zapier-workflows` | Zapier連携ワークフロー |
| テーマ, カラー, UI, デザイン, theme | `theme-factory` | UIテーマ・カラーパレット生成 |
| Slack, 通知, Bot, GIF | `slack-gif-creator` | Slack用GIF作成 |

---

### Layer 3: Additional Recommended Skills (User Selection)

Present these via `AskUserQuestion` based on detected project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "追加でおすすめのスキルを設定しますか？",
    header: "追加スキル",
    options: [
      // Options vary based on project type - see below
    ],
    multiSelect: true
  }]
})
```

#### For Marketing/Business Projects
| Skill | Description |
|-------|-------------|
| `content-research-writer` | コンテンツリサーチ・SEOライティング・コピーライティング |
| `competitive-ads-extractor` | 競合広告分析・抽出 |
| `lead-research-assistant` | リード生成リサーチ・見込み客分析 |

#### For Design/Creative Projects
| Skill | Description |
|-------|-------------|
| `theme-factory` | UIテーマ生成・カラーパレット・デザインシステム |
| `algorithmic-art` | アルゴリズミックアート・ジェネラティブデザイン |
| `canvas-design` | キャンバスベースのデザイン・グラフィックス |

#### For Document Processing Projects
| Skill | Description |
|-------|-------------|
| `pdf-anthropic` | PDF処理・抽出・分析 |
| `pdf-processing-pro` | 高度なPDF処理（OCR・フォーム） |
| `docx` | Word文書処理・生成 |
| `xlsx` | Excelスプレッドシート処理・生成 |

#### For Development/Automation Projects
| Skill | Description |
|-------|-------------|
| `mcp-builder` | MCPサーバー作成・開発ツール |
| `zapier-workflows` | Zapier自動化ワークフロー |
| `artifacts-builder` | Claudeアーティファクト構築・管理 |

---

## Available Skills (by Category)

### business-marketing
| Skill | Description |
|-------|-------------|
| `competitive-ads-extractor` | 競合広告分析・抽出 |
| `content-research-writer` | コンテンツリサーチ・SEOライティング |
| `lead-research-assistant` | リード生成リサーチ |

### creative-design
| Skill | Description |
|-------|-------------|
| `algorithmic-art` | アルゴリズミックアート |
| `canvas-design` | キャンバスデザイン |
| `slack-gif-creator` | Slack用GIF作成 |
| `theme-factory` | UIテーマ・カラーパレット生成 |

### development
| Skill | Description |
|-------|-------------|
| `artifacts-builder` | Claudeアーティファクト構築 |
| `changelog-generator` | CHANGELOG自動生成 |
| `cocoindex` | CocoIndex連携 |
| `developer-growth-analysis` | 開発者成長分析 |
| `git-commit-helper` | Gitコミットメッセージ生成 |
| `mcp-builder` | MCPサーバー構築 |
| `move-code-quality` | コード品質改善 |
| `skill-creator` | 新しいスキル作成 |
| `webapp-testing` | Webアプリテストパターン |
| `zapier-workflows` | Zapier自動化ワークフロー |

### document-processing
| Skill | Description |
|-------|-------------|
| `docx` | Word文書処理 |
| `pdf-anthropic` | PDF処理 |
| `pdf-processing-pro` | 高度なPDF処理（OCR・フォーム） |
| `xlsx` | Excel処理 |

---

## Commands

```bash
# List all skills
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category skills --json

# Search skills
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category skills --json

# Download specific skill
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/skills
```

---

## Skill Structure

Skills may be directories containing multiple files:

```
skill-name/
├── SKILL.md           # Main skill definition
├── scripts/           # Helper scripts (optional)
├── templates/         # Code templates (optional)
└── references/        # Reference docs (optional)
```

The downloader handles both single-file and directory-based skills automatically.
