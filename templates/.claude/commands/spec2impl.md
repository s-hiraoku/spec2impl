---
description: Generate Claude Code implementation environment from specification documents
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
argument-hint: <docs-directory>
---

# spec2impl - Build Implementation Environment from Specifications

Analyze specification documents and automatically build a comprehensive Claude Code implementation environment.

## Arguments

- `$ARGUMENTS`: Directory path containing specification documents (e.g., `docs/`)

## Orchestrator Role

You are the spec2impl orchestrator responsible for:
1. Executing each sub-agent sequentially
2. Displaying progress and obtaining user approval at each step
3. Handling errors appropriately

## Execution Steps

Execute 7 steps sequentially. **Obtain user approval before proceeding to each next step.**

---

### Step 1: Specification Analysis

**Sub-agent:** `.claude/agents/spec2impl/spec-analyzer.md`

**Actions:**
1. Search for `*.md` files in `$ARGUMENTS` using Glob
2. Read each file and extract:
   - API definitions (endpoints, methods, parameters, responses)
   - Data models (fields, types, constraints)
   - Workflows and use cases
   - Constraints and business rules
   - Technology stack (framework, DB, external services)
3. Check specification quality (detect ambiguities and contradictions)
4. Present results and request approval

**Progress Display:**
```
----------------------------------------------------
Step 1/7: Specification Analysis
----------------------------------------------------
Target Directory: $ARGUMENTS

Detected Files:
  - docs/xxx.md
  - docs/yyy.md

Analysis Summary:
  - API: X endpoints
  - Models: X
  - Constraints: X
  - Tech Stack: [xxx, yyy]

Warnings: (if any)

Proceed? [y] Yes  [n] Re-analyze  [q] Abort
----------------------------------------------------
```

---

### Step 2: Skills Generation

**Sub-agent:** `.claude/agents/spec2impl/skills-generator.md`

**Actions:**
1. Generate based on Step 1 analysis:
   - `.claude/skills/implementation/SKILL.md` - Main implementation skill
   - `.claude/skills/implementation/patterns/api.md` - API patterns
   - `.claude/skills/implementation/patterns/validation.md` - Validation patterns
   - `.claude/skills/implementation/patterns/error-handling.md` - Error handling patterns
2. Display preview and request approval
3. Write files upon approval

**Progress Display:**
```
----------------------------------------------------
Step 2/7: Skills Generation
----------------------------------------------------
Files to Generate:
  - .claude/skills/implementation/SKILL.md
  - .claude/skills/implementation/patterns/api.md
  - .claude/skills/implementation/patterns/validation.md
  - .claude/skills/implementation/patterns/error-handling.md

SKILL.md Preview: (show summary)

Generate? [y] Yes  [n] Modify  [s] Skip  [q] Abort
----------------------------------------------------
```

---

### Step 3: Sub-agents Generation

**Sub-agent:** `.claude/agents/spec2impl/subagent-generator.md`

**Actions:**
1. Generate sub-agent definitions:
   - **SpecVerifier** - Verify implementation meets specifications
   - **TestGenerator** - Generate test cases from specifications
   - **ImplementationGuide** - Guide implementation steps
2. Output to `.claude/agents/implementation-agents.md`
3. Write files upon approval

**Progress Display:**
```
----------------------------------------------------
Step 3/7: Sub-agents Generation
----------------------------------------------------
Files to Generate:
  - .claude/agents/implementation-agents.md

Sub-agents:
  1. SpecVerifier - Implementation verification
  2. TestGenerator - Test generation
  3. ImplementationGuide - Implementation guidance

Generate? [y] Yes  [n] Modify  [s] Skip  [q] Abort
----------------------------------------------------
```

---

### Step 4: MCP Configuration

**Sub-agent:** `.claude/agents/spec2impl/mcp-configurator.md`

**Actions:**
1. Select recommended MCPs based on detected technology stack
2. Generate `.mcp.json` (merge with existing if present)
3. Generate setup instructions in `.claude/mcp-setup.md`
4. Write files upon approval

**Progress Display:**
```
----------------------------------------------------
Step 4/7: MCP Configuration
----------------------------------------------------
Recommended MCP Servers:
  [ok] context7 - Document reference (no auth required)
  [!] postgres - DB operations (requires: POSTGRES_URL)
  [!] slack - Slack integration (requires: SLACK_TOKEN)

Files to Generate:
  - .mcp.json
  - .claude/mcp-setup.md

Proceed? [y] Yes  [n] Modify  [s] Skip  [q] Abort
----------------------------------------------------
```

---

### Step 5: Task List Generation

**Sub-agent:** `.claude/agents/spec2impl/task-list-generator.md`

**Actions:**
1. Search for existing tasks in specifications:
   - `- [ ]` checkboxes
   - Verification/Implementation checklists
   - Workflow steps
   - TODO/FIXME comments
2. Auto-generate tasks from APIs and models
3. Integrate and order by dependencies
4. Generate `docs/TASKS.md`
5. Write files upon approval

**Progress Display:**
```
----------------------------------------------------
Step 5/7: Task List Generation
----------------------------------------------------
Task Summary:
  Extracted from specs: X
  Auto-generated: X
  Verification tasks: X
  ----------------------
  Total: X

Files to Generate:
  - docs/TASKS.md

Preview: (show first few tasks)

Proceed? [y] Yes  [n] Modify  [s] Skip  [q] Abort
----------------------------------------------------
```

---

### Step 6: CLAUDE.md Update

**Sub-agent:** `.claude/agents/spec2impl/claude-md-updater.md`

**Actions:**
1. Read existing CLAUDE.md (or create new)
2. Add/update spec2impl section:
   - Specification list
   - Generated resources
   - MCP servers
   - Workflow description
   - Sub-agent usage guide
3. Merge without breaking existing content
4. Write files upon approval

**Progress Display:**
```
----------------------------------------------------
Step 6/7: CLAUDE.md Update
----------------------------------------------------
Updates:
  - Add Implementation Environment section
  - Add specification references
  - Add workflow guide

Update? [y] Yes  [n] Modify  [s] Skip  [q] Abort
----------------------------------------------------
```

---

### Step 7: Cleanup

After environment generation completes, spec2impl tool files are no longer needed.

**Files to Delete:**
- `.claude/commands/spec2impl.md` - This command
- `.claude/agents/spec2impl/` - spec2impl sub-agents
- `.claude/skills/skill-creator/` - Skill generation tools

**Files to Keep:**
- `.claude/skills/` (generated, except skill-creator)
- `.claude/agents/` (generated, except spec2impl/)
- `docs/TASKS.md`
- `CLAUDE.md`
- `.mcp.json`
- `docs/mcp-setup/`

**Progress Display:**
```
----------------------------------------------------
Step 7/7: Cleanup
----------------------------------------------------
Implementation environment complete.
Delete spec2impl tool files?

To Delete:
  [-] .claude/commands/spec2impl.md
  [-] .claude/agents/spec2impl/ (X files)
  [-] .claude/skills/skill-creator/ (X files)

To Keep:
  [+] .claude/skills/[generated]
  [+] .claude/agents/[generated]
  [+] docs/TASKS.md
  [+] CLAUDE.md
  [+] .mcp.json

Delete? [y] Yes  [n] Keep files
----------------------------------------------------
```

**Execution:**
1. Display files to delete and keep
2. If approved: delete spec2impl files
3. If not approved: keep files, proceed to completion

---

## Completion Report

```
====================================================
spec2impl Complete
====================================================

Generated Files:
  [+] .claude/skills/implementation/SKILL.md
  [+] .claude/skills/implementation/patterns/api.md
  [+] .claude/skills/implementation/patterns/validation.md
  [+] .claude/skills/implementation/patterns/error-handling.md
  [+] .claude/agents/implementation-agents.md
  [+] .mcp.json
  [+] .claude/mcp-setup.md
  [+] docs/TASKS.md
  [+] CLAUDE.md (updated)

Action Required:
  - MCP configuration needed. See .claude/mcp-setup.md

Next Steps:
  1. Configure MCP servers (if needed)
  2. Review tasks in docs/TASKS.md
  3. Start implementation: "Implement T-SPEC-1"
====================================================
```

---

## Error Handling

### Specifications Not Found
```
Error: No Markdown files found

Target: $ARGUMENTS

Check:
  - Path is correct
  - *.md files exist
  - Read permissions available
```

### User Aborted
```
Process aborted

Generated Files: (list if any)
Aborted at: Step X/7

To resume: /spec2impl $ARGUMENTS
```

---

## Important Notes

1. **Obtain approval at each step** - Do not proceed until user enters `y`
2. **Handle existing files** - Confirm before overwriting
3. **Report errors with details** - Indicate problem and solution clearly
4. **Visualize progress** - Display current step and remaining steps
