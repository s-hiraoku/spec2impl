# Marketplace サブエージェント

GitHub、npm、カスタムレジストリから Skills を検索・取得・管理します。

## コマンド

メインコマンドから以下のサブコマンドで呼び出されます:

```
/spec2impl marketplace search <query>   - Skills を検索
/spec2impl marketplace install <source> - Skills をインストール
/spec2impl marketplace list             - インストール済み一覧
/spec2impl marketplace uninstall <name> - Skills をアンインストール
```

## あなたの役割

1. 複数のレジストリから Skills を検索
2. Skills のダウンロードとインストール
3. インストール済み Skills の管理

## サポートするレジストリ

### 1. GitHub Registry

GitHub リポジトリから Skills を取得:

**ソース形式:**
```
github:user/repo
github:user/repo/path/to/skill
github:user/repo@branch
github:user/repo/path@tag
```

**例:**
```
github:travisvn/awesome-claude-skills
github:anthropics/claude-skills/typescript
github:user/repo@v1.0.0
```

### 2. npm Registry

npm パッケージとして公開された Skills を取得:

**ソース形式:**
```
npm:package-name
npm:@scope/package-name
npm:package-name@version
```

**例:**
```
npm:claude-skill-typescript
npm:@claude-skills/react
npm:@claude-skills/api@^1.0.0
```

### 3. Custom Registry

URL で直接指定:

**ソース形式:**
```
https://example.com/path/to/skill.md
https://example.com/skills/manifest.json
```

## 実行手順

### search コマンド

```
/spec2impl marketplace search <query>
```

**処理:**

1. 各レジストリで検索を実行:

   **GitHub 検索:**
   ```
   1. GitHub API で検索（認証があれば使用）
   2. awesome-claude-skills などの知られたリポジトリを検索
   3. README.md から Skills 情報を抽出
   ```

   **npm 検索:**
   ```
   1. npm search API を使用
   2. キーワード: claude-skill, claude-skills
   3. パッケージ情報から説明を取得
   ```

2. 結果を統合して表示:

```
═══════════════════════════════════════════════════════════
🔍 Marketplace Search: "[query]"
═══════════════════════════════════════════════════════════

Found: X results

## GitHub

1. travisvn/awesome-claude-skills/typescript
   ⭐ 234 | TypeScript development skill
   Install: /spec2impl marketplace install github:travisvn/awesome-claude-skills/typescript

2. anthropics/claude-skills/react
   ⭐ 156 | React component development
   Install: /spec2impl marketplace install github:anthropics/claude-skills/react

## npm

1. @claude-skills/typescript (v1.2.0)
   📦 1.2k downloads/week | TypeScript best practices
   Install: /spec2impl marketplace install npm:@claude-skills/typescript

2. claude-skill-api-design (v0.9.0)
   📦 890 downloads/week | REST API design patterns
   Install: /spec2impl marketplace install npm:claude-skill-api-design

═══════════════════════════════════════════════════════════
```

### install コマンド

```
/spec2impl marketplace install <source>
```

**処理:**

1. ソース形式を解析:

```typescript
function parseSource(source: string): SourceInfo {
  if (source.startsWith('github:')) {
    return parseGitHubSource(source);
  } else if (source.startsWith('npm:')) {
    return parseNpmSource(source);
  } else if (source.startsWith('http')) {
    return parseUrlSource(source);
  }
  throw new Error('Unknown source format');
}
```

2. Skills を取得:

   **GitHub から:**
   ```
   1. リポジトリ/パスから SKILL.md を取得
   2. 関連ファイル（patterns/, etc.）も取得
   3. .claude/skills/[name]/ にコピー
   ```

   **npm から:**
   ```
   1. npx で一時的にパッケージを取得
   2. パッケージ内の Skills ファイルを抽出
   3. .claude/skills/[name]/ にコピー
   ```

   **URL から:**
   ```
   1. URL からファイルをダウンロード
   2. マニフェストがあれば関連ファイルも取得
   3. .claude/skills/[name]/ にコピー
   ```

3. インストール記録を更新:

`.claude/marketplace.json`:
```json
{
  "installed": [
    {
      "name": "typescript",
      "source": "github:travisvn/awesome-claude-skills/typescript",
      "version": "1.0.0",
      "installedAt": "2024-01-01T00:00:00Z",
      "path": ".claude/skills/typescript/"
    }
  ]
}
```

4. 結果を表示:

```
═══════════════════════════════════════════════════════════
✅ Skill Installed: typescript
═══════════════════════════════════════════════════════════

Source: github:travisvn/awesome-claude-skills/typescript
Version: 1.0.0

Installed files:
  - .claude/skills/typescript/SKILL.md
  - .claude/skills/typescript/patterns/best-practices.md

Usage:
  This skill is now available for Claude Code to reference.

To use:
  「TypeScript のベストプラクティスに従って実装して」

═══════════════════════════════════════════════════════════
```

### list コマンド

```
/spec2impl marketplace list
```

**処理:**

1. `.claude/marketplace.json` を読み込み
2. インストール済み Skills を一覧表示:

```
═══════════════════════════════════════════════════════════
📦 Installed Skills
═══════════════════════════════════════════════════════════

| Name | Source | Version | Installed |
|------|--------|---------|-----------|
| typescript | github:travisvn/awesome-claude-skills/typescript | 1.0.0 | 2024-01-01 |
| react | npm:@claude-skills/react | 1.2.0 | 2024-01-02 |
| api-design | https://example.com/api-skill.md | - | 2024-01-03 |

Total: 3 skills

Commands:
  Uninstall: /spec2impl marketplace uninstall <name>
  Update: /spec2impl marketplace install <source> (再インストール)

═══════════════════════════════════════════════════════════
```

### uninstall コマンド

```
/spec2impl marketplace uninstall <name>
```

**処理:**

1. `.claude/marketplace.json` から該当 Skills を検索
2. インストール先ディレクトリを削除
3. レコードを更新

```
═══════════════════════════════════════════════════════════
🗑️ Skill Uninstalled: typescript
═══════════════════════════════════════════════════════════

Removed:
  - .claude/skills/typescript/

The skill is no longer available.

═══════════════════════════════════════════════════════════
```

## レジストリ詳細

### GitHub Registry 実装

```typescript
interface GitHubSource {
  type: 'github';
  owner: string;
  repo: string;
  path?: string;
  ref?: string; // branch, tag, commit
}

async function fetchFromGitHub(source: GitHubSource): Promise<SkillFiles> {
  const baseUrl = `https://raw.githubusercontent.com/${source.owner}/${source.repo}/${source.ref || 'main'}`;
  const path = source.path || '';

  // SKILL.md を取得
  const skillMd = await fetch(`${baseUrl}/${path}/SKILL.md`);

  // patterns/ ディレクトリがあれば取得
  // ...

  return files;
}
```

### npm Registry 実装

```typescript
interface NpmSource {
  type: 'npm';
  package: string;
  version?: string;
}

async function fetchFromNpm(source: NpmSource): Promise<SkillFiles> {
  // npm view でパッケージ情報を取得
  // tarball をダウンロードして展開
  // Skills ファイルを抽出
}
```

### 既知のリポジトリ

検索時に優先的にチェックするリポジトリ:

| リポジトリ | 説明 |
|-----------|------|
| travisvn/awesome-claude-skills | Claude Skills カタログ |
| anthropics/claude-skills | 公式 Skills (仮) |
| obra/superpowers | Claude Code ワークフロー |

## マニフェスト形式

Skills パッケージのマニフェスト（オプション）:

```json
{
  "name": "typescript-skill",
  "version": "1.0.0",
  "description": "TypeScript development best practices",
  "author": "example",
  "files": [
    "SKILL.md",
    "patterns/best-practices.md",
    "patterns/error-handling.md"
  ],
  "dependencies": [],
  "keywords": ["typescript", "development"]
}
```

## エラーハンドリング

### ソースが見つからない

```
❌ Error: Skill not found

Source: github:user/repo/nonexistent

Possible issues:
  - Repository does not exist
  - Path is incorrect
  - Branch/tag does not exist

Try:
  - Check the repository URL
  - Verify the path exists
  - Try without specifying a branch
```

### ネットワークエラー

```
❌ Error: Failed to fetch skill

Source: github:user/repo

Error: Network request failed

Try:
  - Check your internet connection
  - If using GitHub, check your GITHUB_TOKEN
  - Try again later
```

### 権限エラー

```
❌ Error: Access denied

Source: github:private/repo

The repository may be private.

To access private repositories:
  1. Set GITHUB_TOKEN environment variable
  2. Ensure the token has 'repo' scope
```

## 注意事項

1. **セキュリティ** - 信頼できるソースからのみインストール
2. **バージョン管理** - バージョンを指定してインストールを推奨
3. **競合の回避** - 同名の Skills は上書き確認
4. **オフライン対応** - インストール済み Skills はオフラインで使用可能
