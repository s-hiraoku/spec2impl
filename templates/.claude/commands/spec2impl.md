---
description: Generate Claude Code implementation environment from specification documents and/or project files
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
argument-hint: [docs-directory] [--detect-stack]
---

# spec2impl - Build Implementation Environment from Specifications

Analyze specification documents and/or project files to build Claude Code implementation environment.

## Arguments

- `$ARGUMENTS`: Contains one or both of:
  - `<directory>`: Path to specification documents (e.g., `docs/`)
  - `--detect-stack`: Flag to detect tech stack from project files (package.json, etc.)

## Arguments Parsing

Parse `$ARGUMENTS` to extract:

```typescript
// Parse arguments
const args = "$ARGUMENTS".split(/\s+/).filter(arg => arg.trim() !== "")
let detectStack = args.includes("--detect-stack")
const specDirectory = args.find(arg => !arg.startsWith("--")) || null

// If no arguments provided, ask user about --detect-stack
if (!specDirectory && !detectStack) {
  AskUserQuestion({
    questions: [{
      question: "仕様ディレクトリが指定されていません。プロジェクトファイル（package.json等）から技術スタックを検出しますか？",
      header: "実行モード",
      options: [
        { label: "はい（--detect-stack で実行）", description: "プロジェクトの依存関係から技術スタックを自動検出" },
        { label: "いいえ（キャンセル）", description: "コマンドを終了し、使用例を表示" }
      ],
      multiSelect: false
    }]
  })
  // If user selects "はい", set detectStack = true
  // If user selects "いいえ", show usage and exit
}
```

**Usage Examples:**
- `/spec2impl` → ユーザーに確認後、--detect-stack で実行
- `/spec2impl docs/` → specDirectory="docs/", detectStack=false
- `/spec2impl --detect-stack` → specDirectory=null, detectStack=true
- `/spec2impl docs/ --detect-stack` → specDirectory="docs/", detectStack=true

## Execution Flow

Execute 13 steps sequentially. Each step:
1. Show progress with `progress-dashboard`
2. Execute step logic
3. Present results with `approval-presenter` for user approval

```typescript
// Progress display
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `Read .claude/agents/spec2impl/progress-dashboard.md and execute.
           Mode: workflow
           Current Step: ${stepNumber}
           Total Steps: 13`
})
```

---

## Steps

### Step 1: Specification Analysis (Conditional)
**Agent:** `spec-analyzer.md`
**Condition:** Only if `specDirectory` is provided

```typescript
if (specDirectory) {
  Task({
    subagent_type: "general-purpose",
    prompt: `Read .claude/agents/spec2impl/spec-analyzer.md and execute.
             Target Directory: ${specDirectory}`
  })
  // → specAnalysis with APIs, models, constraints, techStack
  // → Call approval-presenter with results
} else {
  specAnalysis = null  // Skip if only --detect-stack
}
```

→ Output: APIs, models, constraints, tech stack (or null if skipped)
→ Call `approval-presenter` with results (if executed)

---

### Step 2: Project Stack Detection (Conditional)
**Agent:** `project-stack-detector.md`
**Condition:** Only if `--detect-stack` flag is present

```typescript
if (detectStack) {
  Task({
    subagent_type: "general-purpose",
    prompt: `Read .claude/agents/spec2impl/project-stack-detector.md and execute.
             Project Root: ./`
  })
  // → detectedTechStack with frameworks, databases, services, languages
  // → Call approval-presenter with detected technologies
} else {
  detectedTechStack = null  // Skip if only specDirectory
}

// Prepare merged tech stack for Step 3
const initialTechStack = mergeTechStacks(
  specAnalysis?.techStack || {},
  detectedTechStack?.techStack || {}
)
```

→ Output: detectedTechStack (frameworks, databases, services, languages)
→ Call `approval-presenter` with detected technologies (if executed)

---

### Step 3: Tech Stack Expansion
**Agent:** `tech-stack-expander.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/tech-stack-expander.md and execute.

           Input:
           - techStack: ${specAnalysis?.techStack || []}
           - detectedStack: ${detectedTechStack?.techStack || []}
           - specContent: ${specContent || ""}

           Sources:
           - Spec Analysis: ${specDirectory ? "Provided" : "Not provided"}
           - Project Detection: ${detectStack ? "Enabled" : "Disabled"}

           This agent will:
           1. Merge techStack and detectedStack (deduplicate, flag conflicts)
           2. Launch parallel subagents to Web search for related technologies
           3. Discover implicit dependencies (e.g., Next.js → React, TypeScript)
           4. Find technology choices (CSS framework, state management, ORM, etc.)
           5. Check spec for already-decided technologies
           6. Ask user ALL undecided questions (multiple AskUserQuestion calls if needed)
           7. Output expandedTechStack with searchTerms`
})
```

→ Output: expandedTechStack (confirmed technologies + searchTerms)
→ Call `approval-presenter` with expanded tech stack

---

### Step 4: Skills Acquisition (3-Layer)
**Agent:** `skills-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/skills-downloader.md and execute.
           Search Terms: ${expandedTechStack.searchTerms}
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/skills/[name]/`
→ Call `approval-presenter` with downloaded skills

---

### Step 5: Agents Acquisition (3-Layer)
**Agent:** `agents-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/agents-downloader.md and execute.
           Search Terms: ${expandedTechStack.searchTerms}
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/agents/[name].md`
→ Call `approval-presenter` with downloaded agents

---

### Step 6: Commands Acquisition (3-Layer)
**Agent:** `commands-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/commands-downloader.md and execute.
           Search Terms: ${expandedTechStack.searchTerms}
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/commands/[name].md`
→ Call `approval-presenter` with downloaded commands

---

### Step 7: MCP Configuration (3-Layer)
**Agent:** `mcps-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/mcps-downloader.md and execute.
           Search Terms: ${expandedTechStack.searchTerms}
           Services: ${detectedServices}
           Requirements: ${specRequirements}`
})
```

→ Output: `.mcp.json`
→ Call `approval-presenter` with MCP configs (include token requirements)

---

### Step 8: Settings Configuration (3-Layer)
**Agent:** `settings-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/settings-downloader.md and execute.
           Search Terms: ${expandedTechStack.searchTerms}
           Project Type: ${projectType}
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/settings.local.json`
→ Call `approval-presenter` with settings

---

### Step 9: Deploy Bundled (for UI/Frontend projects)

If spec includes frontend/UI components, deploy ux-psychology:

```bash
# Copy skill to project (outside spec2impl namespace)
cp -r .claude/skills/spec2impl/ux-psychology .claude/skills/

# Copy agent to project (outside spec2impl namespace)
cp .claude/agents/spec2impl/ux-psychology-advisor.md .claude/agents/
```

→ Output: `.claude/skills/ux-psychology/`, `.claude/agents/ux-psychology-advisor.md`

---

### Step 10: Task List Generation
**Agent:** `task-list-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/task-list-generator.md and execute.
           Include UX recommendations if applicable.
           Spec Analysis: ${specAnalysis}
           Downloaded: ${downloadedItems}`
})
```

→ Output: `docs/TASKS.md`
→ Call `approval-presenter` with task summary

---

### Step 11: Rules Generation
**Agent:** `rules-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/rules-generator.md and execute.
           Generated Files: ${fileList}`
})
```

→ Output: `.claude/rules/spec2impl.md` (created)

---

### Step 12: Harness Guide Generation
**Agent:** `harness-guide-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/harness-guide-generator.md and execute.

           Input:
           - expandedTechStack: ${expandedTechStack}
           - downloadedItems: ${downloadedItems}
           - specDirectory: ${ARGUMENTS}
           - taskCount: ${taskCount}

           Generate docs/HARNESS_GUIDE.md with:
           1. Generation summary (tech stack, task count)
           2. Downloaded components with usage instructions
           3. Token requirements from MCPs
           4. First 3 tasks from TASKS.md
           5. Quick start guide`
})
```

→ Output: `docs/HARNESS_GUIDE.md`
→ Call `approval-presenter` with guide summary

---

### Step 13: Cleanup (Optional)

Delete spec2impl files:
- `.claude/commands/spec2impl.md`
- `.claude/agents/spec2impl/`
- `.claude/skills/spec2impl/`
- `.claude/rules/spec2impl.md`

→ Call `approval-presenter` for cleanup confirmation

---

## Available Agents Reference

| Agent | Purpose | Steps |
|-------|---------|-------|
| spec-analyzer | Parse specifications | 1 |
| project-stack-detector | Detect tech stack from project files | 2 |
| tech-stack-expander | Expand tech stack via Web search + user questions | 3 |
| skills-downloader | Download skills (3-layer) | 4 |
| agents-downloader | Download agents (3-layer) | 5 |
| commands-downloader | Download commands (3-layer) | 6 |
| mcps-downloader | Download MCPs (3-layer) | 7 |
| settings-downloader | Download settings (3-layer) | 8 |
| category-downloader | Router to category-specific agents | 4-8 |
| task-list-generator | Generate TASKS.md | 10 |
| rules-generator | Generate .claude/rules/spec2impl.md | 11 |
| harness-guide-generator | Generate HARNESS_GUIDE.md | 12 |
| progress-dashboard | Show progress | All |
| approval-presenter | Get user approval | 1-8, 10, 12, 13 |
| ux-psychology-advisor | UX recommendations | Deployed in 9 |

## Available Skills Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| aitmpl-downloader | Template marketplace (GitHub API) | Steps 4-8 |
| ux-psychology | 43 UX psychology concepts | UI/frontend projects |
| skill-creator | Create new skills | When no template exists |

---

## Completion Report

```
════════════════════════════════════════════════════════════════
spec2impl Complete (13/13 steps)
════════════════════════════════════════════════════════════════

Sources Used:
  Spec Analysis:     ${specDirectory ? specDirectory : "N/A"}
  Project Detection: ${detectStack ? "Enabled" : "Disabled"}

Tech Stack:
  From Spec:     ${specAnalysis?.techStack || "N/A"}
  From Project:  ${detectedTechStack?.techStack || "N/A"}
  Expanded:      ${expandedTechStack.confirmed}
  User Chose:    ${expandedTechStack.userSelected}

Downloaded from aitmpl.com:
  Skills:     ${downloadedSkills}
  Agents:     ${downloadedAgents}
  Commands:   ${downloadedCommands}
  MCPs:       ${downloadedMCPs}
  Settings:   ${downloadedSettings}

Deployed:
  UX Psychology: ${uxDeployed ? "Yes" : "N/A"}

Tasks: ${taskCount} tasks in docs/TASKS.md

📚 Harness Guide: docs/HARNESS_GUIDE.md
   → Component usage, token configuration, quick start guide

Next Steps:
1. Read docs/HARNESS_GUIDE.md for usage instructions
2. Configure tokens (see guide for details)
3. Start: "Implement T-SPEC-1"
════════════════════════════════════════════════════════════════
```
