---
description: Generate Claude Code implementation environment from specification documents
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
argument-hint: <docs-directory>
---

# spec2impl - Build Implementation Environment from Specifications

Analyze specification documents and build Claude Code implementation environment.

## Arguments

- `$ARGUMENTS`: Directory path containing specification documents (e.g., `docs/`)

## Execution Flow

Execute 12 steps sequentially. Each step:
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
           Total Steps: 12`
})
```

---

## Steps

### Step 1: Specification Analysis
**Agent:** `spec-analyzer.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/spec-analyzer.md and execute.
           Target Directory: ${ARGUMENTS}`
})
```

→ Output: APIs, models, constraints, tech stack
→ Call `approval-presenter` with results

---

### Step 2: Tech Stack Expansion
**Agent:** `tech-stack-expander.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/tech-stack-expander.md and execute.

           Input:
           - techStack: ${specAnalysisResult.techStack}
           - specContent: ${specContent}

           This agent will:
           1. Launch parallel subagents to Web search for related technologies
           2. Discover implicit dependencies (e.g., Next.js → React, TypeScript)
           3. Find technology choices (CSS framework, state management, ORM, etc.)
           4. Check spec for already-decided technologies
           5. Ask user ALL undecided questions (multiple AskUserQuestion calls if needed)
           6. Output expandedTechStack with searchTerms`
})
```

→ Output: expandedTechStack (confirmed technologies + searchTerms)
→ Call `approval-presenter` with expanded tech stack

---

### Step 3: Skills Acquisition (3-Layer)
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

### Step 4: Agents Acquisition (3-Layer)
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

### Step 5: Commands Acquisition (3-Layer)
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

### Step 6: MCP Configuration (3-Layer)
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

### Step 7: Settings Configuration (3-Layer)
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

### Step 8: Deploy Bundled (for UI/Frontend projects)

If spec includes frontend/UI components, deploy ux-psychology:

```bash
# Copy skill to project (outside spec2impl namespace)
cp -r .claude/skills/spec2impl/ux-psychology .claude/skills/

# Copy agent to project (outside spec2impl namespace)
cp .claude/agents/spec2impl/ux-psychology-advisor.md .claude/agents/
```

→ Output: `.claude/skills/ux-psychology/`, `.claude/agents/ux-psychology-advisor.md`

---

### Step 9: Task List Generation
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

### Step 10: CLAUDE.md Update
**Agent:** `claude-md-updater.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/claude-md-updater.md and execute.
           Generated Files: ${fileList}`
})
```

→ Output: `CLAUDE.md` (updated)

---

### Step 11: Harness Guide Generation
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

### Step 12: Cleanup (Optional)

Delete spec2impl files:
- `.claude/commands/spec2impl.md`
- `.claude/agents/spec2impl/`
- `.claude/skills/spec2impl/`

→ Call `approval-presenter` for cleanup confirmation

---

## Available Agents Reference

| Agent | Purpose | Steps |
|-------|---------|-------|
| spec-analyzer | Parse specifications | 1 |
| tech-stack-expander | Expand tech stack via Web search + user questions | 2 |
| skills-downloader | Download skills (3-layer) | 3 |
| agents-downloader | Download agents (3-layer) | 4 |
| commands-downloader | Download commands (3-layer) | 5 |
| mcps-downloader | Download MCPs (3-layer) | 6 |
| settings-downloader | Download settings (3-layer) | 7 |
| category-downloader | Router to category-specific agents | 3-7 |
| task-list-generator | Generate TASKS.md | 9 |
| claude-md-updater | Update CLAUDE.md | 10 |
| harness-guide-generator | Generate HARNESS_GUIDE.md | 11 |
| progress-dashboard | Show progress | All |
| approval-presenter | Get user approval | 1-7, 9, 11, 12 |
| ux-psychology-advisor | UX recommendations | Deployed in 8 |

## Available Skills Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| aitmpl-downloader | Template marketplace (GitHub API) | Steps 3-7 |
| ux-psychology | 43 UX psychology concepts | UI/frontend projects |
| skill-creator | Create new skills | When no template exists |

---

## Completion Report

```
════════════════════════════════════════════════════════════════
spec2impl Complete (12/12 steps)
════════════════════════════════════════════════════════════════

Tech Stack Expanded:
  Original:   ${originalTechStack}
  Expanded:   ${expandedTechStack.confirmed}
  User Chose: ${expandedTechStack.userSelected}

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
