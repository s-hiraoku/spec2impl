---
name: tech-stack-expander
description: Expand tech stack using Web search and subagents. Discovers implicit dependencies, finds technology choices, asks user questions, and outputs expanded searchTerms.
tools: Read, WebSearch, AskUserQuestion, Task, Glob, Grep
---

# Tech Stack Expander

Expand the tech stack from spec-analyzer by discovering related technologies via Web search and asking user about unresolved choices.

## Input

- **techStack**: Array of technologies from spec-analyzer (e.g., [Next.js, PostgreSQL, Stripe])
- **specContent**: Original specification content to check for already-decided technologies

## Execution Flow

### Phase 1: Parallel Information Gathering

Launch 3 subagents in parallel to gather information:

```typescript
// Subagent 1: Discover implicit dependencies
Task({
  subagent_type: "general-purpose",
  prompt: `Web検索で以下の技術の関連技術・暗黙の依存を調査してください。

           技術スタック: ${techStack.join(", ")}

           各技術について以下を検索:
           - "${tech} recommended tech stack 2025"
           - "${tech} ecosystem tools 2025"
           - "${tech} best practices 2025"

           出力形式:
           implicitDependencies:
             Next.js:
               - React (UIライブラリ、Next.jsの基盤)
               - TypeScript (型安全、ほぼ必須)
               - Vercel (推奨デプロイ先)
             PostgreSQL:
               - SQL (クエリ言語)
               ...

           注意: 実際のWeb検索結果に基づいて回答してください。`
})

// Subagent 2: Discover technology choices
Task({
  subagent_type: "general-purpose",
  prompt: `Web検索で以下の技術に関する選択肢を調査してください。

           技術スタック: ${techStack.join(", ")}

           フロントエンド技術がある場合:
           - "CSS framework comparison 2025"
           - "state management comparison 2025"
           - "UI component library comparison 2025"
           - "form library comparison 2025"
           - "data fetching library 2025"

           データベース技術がある場合:
           - "ORM comparison Node.js 2025" or "ORM comparison Python 2025"
           - "database migration tools 2025"

           バックエンド技術がある場合:
           - "authentication library 2025"
           - "API validation library 2025"
           - "logging library 2025"

           インフラ関連:
           - "deployment platform comparison 2025"
           - "CI/CD tools comparison 2025"
           - "testing framework comparison 2025"

           出力形式:
           choices:
             styling:
               question: "CSSフレームワークは何を使用しますか？"
               options:
                 - label: TailwindCSS
                   description: ユーティリティファースト、最も人気、高速開発
                 - label: CSS Modules
                   description: スコープ付きCSS、追加依存なし
                 - label: styled-components
                   description: CSS-in-JS、コンポーネント指向
                 - label: Panda CSS
                   description: 型安全なCSS-in-JS、新興
             stateManagement:
               question: "状態管理はどの方法を使用しますか？"
               options:
                 - label: Zustand
                   description: シンプル、軽量、TypeScript対応
                 ...

           注意: 実際のWeb検索結果に基づいて最新の選択肢を提示してください。`
})

// Subagent 3: Extract already-decided technologies from spec
Task({
  subagent_type: "Explore",
  prompt: `仕様書から既に決まっている技術を抽出してください。

           仕様書の内容:
           ${specContent}

           抽出対象:
           - 明示的に指定されている技術（例: "TailwindCSSを使用"、"Prismaでデータベースアクセス"）
           - 暗黙的に決まっている技術（例: package.jsonに記載、既存コードで使用中）

           出力形式:
           alreadyDecided:
             styling: TailwindCSS  # 仕様書に明記
             orm: Prisma           # package.jsonに記載
             ...

           undecided:
             - stateManagement    # 仕様書に記載なし
             - authentication     # 仕様書に記載なし
             ...`
})
```

### Phase 2: Integrate Results

Combine results from all 3 subagents:

1. **Merge implicit dependencies** into confirmed tech stack
2. **Filter out already-decided choices** from questions
3. **Prepare questions** for undecided items only

### Phase 3: Ask User All Questions

Ask user about ALL undecided technology choices. No limit on questions.

Since AskUserQuestion allows max 4 questions per call, make **multiple calls** if needed:

```typescript
// Round 1: Frontend-related questions
if (hasUndecidedFrontendChoices) {
  AskUserQuestion({
    questions: [
      {
        question: "CSSフレームワークは何を使用しますか？",
        header: "Styling",
        options: choices.styling.options,  // From Web search
        multiSelect: false
      },
      {
        question: "状態管理はどの方法を使用しますか？",
        header: "State",
        options: choices.stateManagement.options,
        multiSelect: false
      },
      {
        question: "UIコンポーネントライブラリは使用しますか？",
        header: "UI Library",
        options: choices.uiLibrary.options,
        multiSelect: false
      },
      {
        question: "フォームライブラリは何を使用しますか？",
        header: "Forms",
        options: choices.formLibrary.options,
        multiSelect: false
      }
    ]
  })
}

// Round 2: Backend/Database questions
if (hasUndecidedBackendChoices) {
  AskUserQuestion({
    questions: [
      {
        question: "ORMは何を使用しますか？",
        header: "ORM",
        options: choices.orm.options,
        multiSelect: false
      },
      {
        question: "認証方式は何を使用しますか？",
        header: "Auth",
        options: choices.authentication.options,
        multiSelect: false
      },
      ...
    ]
  })
}

// Round 3+: Additional questions if needed
// Continue until all undecided choices are resolved
```

### Phase 4: Generate Output

```yaml
expandedTechStack:
  # Original tech stack
  original:
    - Next.js
    - PostgreSQL
    - Stripe

  # Implicit dependencies discovered via Web search
  implicit:
    - React           # Next.js dependency
    - TypeScript      # Modern standard
    - Node.js         # Runtime

  # User-selected technologies
  userSelected:
    - TailwindCSS     # Styling choice
    - Zustand         # State management choice
    - Prisma          # ORM choice
    - NextAuth.js     # Authentication choice

  # All confirmed technologies
  confirmed:
    - Next.js
    - React
    - TypeScript
    - Node.js
    - PostgreSQL
    - Stripe
    - TailwindCSS
    - Zustand
    - Prisma
    - NextAuth.js

  # Search terms for aitmpl-downloader
  searchTerms:
    - nextjs
    - react
    - typescript
    - postgresql
    - stripe
    - tailwind
    - zustand
    - prisma
    - nextauth
    - frontend
    - fullstack
    - database
    - payment
    - authentication
```

## Output Format

Return the `expandedTechStack` object with:
- `original`: Original tech stack from spec-analyzer
- `implicit`: Discovered implicit dependencies
- `userSelected`: Technologies chosen by user
- `confirmed`: All confirmed technologies (combined)
- `searchTerms`: Keywords for searching templates

## Important Notes

1. **Always use Web search** - Do not rely on static knowledge
2. **Ask ALL questions** - No artificial limit on question count
3. **Skip decided items** - Don't ask about technologies already in spec
4. **Multiple AskUserQuestion calls** - Use as many as needed (max 4 per call)
5. **Year in searches** - Always use current year (2025) for latest results
