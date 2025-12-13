---
name: tech-stack-expander
description: Expand tech stack using Web search and subagents. Discovers implicit dependencies, finds technology choices, asks user questions, and outputs expanded searchTerms.
tools: Read, WebSearch, AskUserQuestion, Task, Glob, Grep
---

# Tech Stack Expander

Expand the tech stack from spec-analyzer and/or project-stack-detector by discovering related technologies via Web search and asking user about unresolved choices.

## Input

- **techStack**: Array of technologies from spec-analyzer (e.g., [Next.js, PostgreSQL, Stripe]). May be empty if no spec provided.
- **detectedStack**: Array of technologies from project-stack-detector (e.g., [React, TypeScript, Prisma]). May be empty if `--detect-stack` not used.
- **specContent**: Original specification content to check for already-decided technologies. May be empty.

## Input Merge Strategy

Before Phase 1, merge input sources:

```typescript
// Combine tech stacks with source tracking
const mergedTechStack = {
  fromSpec: techStack || [],
  fromProject: detectedStack || [],
  combined: [...new Set([...(techStack || []), ...(detectedStack || [])])]
}

// Detect conflicts (e.g., spec says PostgreSQL, project has MySQL)
const conflicts = detectConflicts(mergedTechStack.fromSpec, mergedTechStack.fromProject)
if (conflicts.length > 0) {
  // Present conflicts to user via AskUserQuestion
  // "Your spec mentions PostgreSQL but the project uses MySQL. Which should we use?"
}
```

## Execution Flow

### Phase 1: Parallel Information Gathering

Launch 3 subagents in parallel to gather information:

```typescript
// Subagent 1: Discover implicit dependencies
Task({
  subagent_type: "general-purpose",
  prompt: `Use Web search to discover related technologies and implicit dependencies.

           Tech Stack: ${mergedTechStack.combined.join(", ")}

           Search for each technology:
           - "${tech} recommended tech stack 2025"
           - "${tech} ecosystem tools 2025"
           - "${tech} best practices 2025"

           Output format:
           implicitDependencies:
             Next.js:
               - React (UI library, Next.js foundation)
               - TypeScript (type safety, nearly essential)
               - Vercel (recommended deployment)
             PostgreSQL:
               - SQL (query language)
               ...

           Note: Base your response on actual Web search results.`
})

// Subagent 2: Discover technology choices
Task({
  subagent_type: "general-purpose",
  prompt: `Use Web search to discover technology options.

           Tech Stack: ${mergedTechStack.combined.join(", ")}

           If frontend technologies present:
           - "CSS framework comparison 2025"
           - "state management comparison 2025"
           - "UI component library comparison 2025"
           - "form library comparison 2025"
           - "data fetching library 2025"

           If database technologies present:
           - "ORM comparison Node.js 2025" or "ORM comparison Python 2025"
           - "database migration tools 2025"

           If backend technologies present:
           - "authentication library 2025"
           - "API validation library 2025"
           - "logging library 2025"

           Infrastructure related:
           - "deployment platform comparison 2025"
           - "CI/CD tools comparison 2025"
           - "testing framework comparison 2025"

           Output format:
           choices:
             styling:
               question: "Which CSS framework will you use?"
               options:
                 - label: TailwindCSS
                   description: Utility-first, most popular, rapid development
                 - label: CSS Modules
                   description: Scoped CSS, no additional dependencies
                 - label: styled-components
                   description: CSS-in-JS, component-oriented
                 - label: Panda CSS
                   description: Type-safe CSS-in-JS, emerging
             stateManagement:
               question: "Which state management approach will you use?"
               options:
                 - label: Zustand
                   description: Simple, lightweight, TypeScript support
                 ...

           Note: Present the latest options based on actual Web search results.`
})

// Subagent 3: Extract already-decided technologies from spec AND project
Task({
  subagent_type: "Explore",
  prompt: `Extract technologies already decided from both specification and project detection.

           Sources:
           1. Specification content (if provided):
              ${specContent || "(No spec provided)"}

           2. Project detection (if --detect-stack enabled):
              From Spec: ${mergedTechStack.fromSpec.join(", ") || "(none)"}
              From Project: ${mergedTechStack.fromProject.join(", ") || "(none)"}

           Extract:
           - Explicitly specified technologies from spec (e.g., "using TailwindCSS")
           - Technologies detected from project files (e.g., package.json dependencies)
           - Mark source for each: "spec", "project", or "both"

           Output format:
           alreadyDecided:
             styling: TailwindCSS  # source: spec
             orm: Prisma           # source: project (from package.json)
             database: PostgreSQL  # source: both
             ...

           undecided:
             - stateManagement    # not in spec or project
             - authentication     # not in spec or project
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
        question: "Which CSS framework will you use?",
        header: "Styling",
        options: choices.styling.options,  // From Web search
        multiSelect: false
      },
      {
        question: "Which state management approach will you use?",
        header: "State",
        options: choices.stateManagement.options,
        multiSelect: false
      },
      {
        question: "Will you use a UI component library?",
        header: "UI Library",
        options: choices.uiLibrary.options,
        multiSelect: false
      },
      {
        question: "Which form library will you use?",
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
        question: "Which ORM will you use?",
        header: "ORM",
        options: choices.orm.options,
        multiSelect: false
      },
      {
        question: "Which authentication method will you use?",
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
- `fromSpec`: Technologies from spec-analyzer (may be empty)
- `fromProject`: Technologies from project-stack-detector (may be empty)
- `original`: Combined original tech stack (merged, deduplicated)
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
