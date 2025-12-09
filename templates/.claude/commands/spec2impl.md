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

Execute 10 steps sequentially. Each step:
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
           Total Steps: 10`
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

### Step 2: Skills Acquisition
**Agent:** `category-downloader.md` (category: skills)

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.
           Category: skills
           Tech Stack: ${techStack}
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/skills/[name]/`
→ Call `approval-presenter` with downloaded skills

---

### Step 3: Agents Acquisition
**Agent:** `category-downloader.md` (category: agents)

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.
           Category: agents
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/agents/[name].md`
→ Call `approval-presenter` with downloaded agents

---

### Step 4: Commands Acquisition
**Agent:** `category-downloader.md` (category: commands)

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.
           Category: commands
           Requirements: ${specRequirements}`
})
```

→ Output: `.claude/commands/[name].md`
→ Call `approval-presenter` with downloaded commands

---

### Step 5: MCP Configuration
**Agent:** `category-downloader.md` (category: mcps)

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.
           Category: mcps
           Services: ${detectedServices}
           Requirements: ${specRequirements}`
})
```

→ Output: `.mcp.json`
→ Call `approval-presenter` with MCP configs (include token requirements)

---

### Step 6: Settings Configuration
**Agent:** `category-downloader.md` (category: settings)

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.
           Category: settings
           Project Type: ${projectType}`
})
```

→ Output: `.claude/settings.local.json`
→ Call `approval-presenter` with settings

---

### Step 7: Deploy Bundled (for UI/Frontend projects)

If spec includes frontend/UI components, deploy ux-psychology:

```bash
# Copy skill to project (outside spec2impl namespace)
cp -r .claude/skills/spec2impl/ux-psychology .claude/skills/

# Copy agent to project (outside spec2impl namespace)
cp .claude/agents/spec2impl/ux-psychology-advisor.md .claude/agents/
```

→ Output: `.claude/skills/ux-psychology/`, `.claude/agents/ux-psychology-advisor.md`

---

### Step 8: Task List Generation
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

### Step 9: CLAUDE.md Update
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

### Step 10: Cleanup (Optional)

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
| category-downloader | Download by category | 2, 3, 4, 5, 6 |
| task-list-generator | Generate TASKS.md | 8 |
| claude-md-updater | Update CLAUDE.md | 9 |
| progress-dashboard | Show progress | All |
| approval-presenter | Get user approval | 1-6, 8, 10 |
| ux-psychology-advisor | UX recommendations | Deployed in 7 |

## Available Skills Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| aitmpl-downloader | Template marketplace (GitHub API) | Steps 2-6 |
| ux-psychology | 43 UX psychology concepts | UI/frontend projects |
| skill-creator | Create new skills | When no template exists |

---

## Completion Report

```
════════════════════════════════════════════════════════════════
spec2impl Complete (10/10 steps)
════════════════════════════════════════════════════════════════

Downloaded from aitmpl.com:
  Skills:     ${downloadedSkills}
  Agents:     ${downloadedAgents}
  Commands:   ${downloadedCommands}
  MCPs:       ${downloadedMCPs}
  Settings:   ${downloadedSettings}

Deployed:
  UX Psychology: ${uxDeployed ? "Yes" : "N/A"}

Tasks: ${taskCount} tasks in docs/TASKS.md

Next Steps:
1. Configure MCPs (see token requirements above)
2. Review docs/TASKS.md
3. Start: "Implement T-SPEC-1"
════════════════════════════════════════════════════════════════
```
