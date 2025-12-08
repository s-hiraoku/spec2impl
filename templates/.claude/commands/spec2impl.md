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

Execute 7 steps sequentially. Launch subagents PROACTIVELY using:

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/${agentName}.md and execute. ${input}`
})
```

**CRITICAL: All agents MUST search aitmpl.com FIRST using:**
```bash
python3 .claude/skills/aitmpl-downloader/scripts/download.py search "${query}" --json
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

Output: APIs, models, constraints, tech stack

---

### Step 2: Skills Acquisition
**Agent:** `skills-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/skills-generator.md and execute.
           FIRST: python3 .claude/skills/aitmpl-downloader/scripts/download.py list --json
           Tech Stack: ${techStack}`
})
```

Output: .claude/skills/[name]/SKILL.md

---

### Step 3: Sub-agents Generation
**Agent:** `subagent-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/subagent-generator.md and execute.
           FIRST: python3 .claude/skills/aitmpl-downloader/scripts/download.py list --category agents --json`
})
```

Output: .claude/agents/[name].md

---

### Step 4: MCP Configuration
**Agent:** `mcp-configurator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/mcp-configurator.md and execute.
           FIRST: python3 .claude/skills/aitmpl-downloader/scripts/download.py list --category mcps --json
           Services: ${detectedServices}`
})
```

Output: .mcp.json, docs/mcp-setup/

---

### Step 5: Task List Generation
**Agent:** `task-list-generator.md`

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/task-list-generator.md and execute.
           Spec Analysis: ${specAnalysis}`
})
```

Output: docs/TASKS.md

---

### Step 6: CLAUDE.md Update
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

### Step 7: Cleanup
Delete spec2impl files (optional):
- .claude/commands/spec2impl.md
- .claude/agents/spec2impl/
- .claude/skills/skill-creator/

---

## Completion Report

```
====================================================
spec2impl Complete
====================================================

Skills:     ${installedCount} installed, ${generatedCount} generated
Agents:     ${agentCount} created
MCPs:       ${mcpCount} configured
Tasks:      ${taskCount} tasks in docs/TASKS.md

Next Steps:
1. Configure MCPs (see docs/mcp-setup/)
2. Review docs/TASKS.md
3. Start: "Implement T-SPEC-1"
====================================================
```
