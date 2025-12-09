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

Execute 8 steps sequentially. Launch subagents PROACTIVELY using:

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/${agentName}.md and execute. ${input}`
})
```

**CRITICAL: All download operations MUST use the aitmpl-downloader agent.**

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

Output: APIs, models, constraints, tech stack

---

### Step 2: Skills Acquisition
**Agent:** `skills-generator.md` → calls `aitmpl-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/skills-generator.md and execute.
           Use aitmpl-downloader agent for ALL downloads.
           Tech Stack: ${techStack}`
})
```

Output: .claude/skills/[name]/SKILL.md

---

### Step 3: Sub-agents Generation
**Agent:** `subagent-generator.md` → calls `aitmpl-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/subagent-generator.md and execute.
           Use aitmpl-downloader agent for ALL downloads.`
})
```

Output: .claude/agents/[name].md

---

### Step 4: MCP Configuration
**Agent:** `mcp-configurator.md` → calls `aitmpl-downloader.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/mcp-configurator.md and execute.
           Use aitmpl-downloader agent for ALL downloads.
           Services: ${detectedServices}`
})
```

Output: .mcp.json, docs/mcp-setup/

---

### Step 5: UX Psychology Analysis (for UI/Frontend projects)
**Agent:** `ux-psychology-advisor.md` + **Skill:** `ux-psychology`

If spec includes frontend/UI components:

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/ux-psychology-advisor.md and
           .claude/skills/ux-psychology/SKILL.md.
           Analyze UI requirements from spec and provide UX recommendations.
           Spec Analysis: ${specAnalysis}`
})
```

Output: UX recommendations for UI implementation

---

### Step 6: Task List Generation
**Agent:** `task-list-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/task-list-generator.md and execute.
           Include UX recommendations if applicable.
           Spec Analysis: ${specAnalysis}`
})
```

Output: docs/TASKS.md

---

### Step 7: CLAUDE.md Update
**Agent:** `claude-md-updater.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/claude-md-updater.md and execute.
           Generated Files: ${fileList}`
})
```

Output: CLAUDE.md (updated)

---

### Step 8: Cleanup
Delete spec2impl files (optional):
- .claude/commands/spec2impl.md
- .claude/agents/spec2impl/
- .claude/skills/skill-creator/
- .claude/skills/aitmpl-downloader/

---

## Available Agents Reference

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| aitmpl-downloader | Download from aitmpl.com | Every download operation |
| ux-psychology-advisor | UX recommendations | Frontend/UI projects |
| spec-analyzer | Parse specifications | Step 1 |
| skills-generator | Acquire skills | Step 2 |
| subagent-generator | Acquire agents | Step 3 |
| mcp-configurator | Configure MCPs | Step 4 |
| task-list-generator | Generate TASKS.md | Step 6 |
| claude-md-updater | Update CLAUDE.md | Step 7 |

## Available Skills Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| aitmpl-downloader | Template marketplace | All download operations |
| ux-psychology | 43 UX psychology concepts | UI/frontend design |
| skill-creator | Create new skills | When no template exists |

---

## Completion Report

```
====================================================
spec2impl Complete
====================================================

Downloaded from aitmpl.com:
  Skills:     ${downloadedSkills} downloaded
  Agents:     ${downloadedAgents} downloaded
  MCPs:       ${downloadedMCPs} configured

Generated (not found on aitmpl.com):
  Skills:     ${generatedSkills}
  Agents:     ${generatedAgents}

Tasks:      ${taskCount} tasks in docs/TASKS.md
UX Applied: ${uxApplied ? "Yes" : "N/A"}

Next Steps:
1. Configure MCPs (see docs/mcp-setup/)
2. Review docs/TASKS.md
3. Start: "Implement T-SPEC-1"
====================================================
```
