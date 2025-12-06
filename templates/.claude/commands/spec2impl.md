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
2. Displaying progress via `progress-dashboard` after each step
3. Obtaining user approval at each step
4. Handling errors appropriately

## Progress Tracking

After completing each step, display progress using the progress-dashboard agent (model: haiku):

```typescript
// After each step completion, show progress
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `
    Read .claude/agents/spec2impl/progress-dashboard.md and execute:

    Mode: workflow
    Current Step: ${currentStep + 1}
    Total Steps: 7
    Completed Steps: ${completedStepsWithSummaries}
    Current: ${nextStepName}
  `
})
```

## Approval Flow

Before each approval checkpoint, use the approval-presenter agent (model: haiku) to present results:

```typescript
// Before requesting approval, present results clearly
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: `
    Read .claude/agents/spec2impl/approval-presenter.md and execute:

    Step: ${currentStep}
    Step Name: ${stepName}
    Summary: ${summaryPoints}
    Details: ${detailsTable}
    Files to Create: ${filesToCreate}
    Risks: ${risks}
    ${step === 4 ? `Token Requirements: ${tokenRequirements}` : ''}
  `
})
```

## Execution Steps

Execute 7 steps sequentially. **Use approval-presenter to display results, then obtain user approval before proceeding to each next step.**

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

### Step 2: Skills Acquisition

**Sub-agent:** `.claude/agents/spec2impl/skills-generator.md`

**Core Principle:** Marketplace First, Then Generate

**Actions:**
1. **Identify** required skills from Step 1 analysis (API, validation, auth, etc.)
2. **Search** via `marketplace-plugin-scout` for existing skill plugins
3. **Evaluate** search results (freshness, tech stack match, score)
4. **Install** found skills via `marketplace` agent
5. **Generate** only missing skills using `skill-creator`
6. **Customize** installed skills with project-specific context

**Progress Display:**
```
----------------------------------------------------
Step 2/7: Skills Acquisition
----------------------------------------------------
Required Skills: 6 identified

Searching marketplace-plugin-scout...

Search Results:
  ✅ api-implementation    (github:travisvn/awesome-claude-skills/express-api) Score: 85
  ✅ data-modeling         (github:anthropics/claude-skills/prisma) Score: 92
  ⚠️ authentication        (github:travisvn/awesome-claude-skills/auth) Score: 65 → customize
  ✅ input-validation      (npm:claude-skill-zod-validation) Score: 78
  ❌ error-handling        → will generate
  ✅ stripe-integration    (github:stripe/claude-stripe-skill) Score: 88

Plan:
  📦 Install from marketplace: 4 skills
  🔧 Install + customize: 1 skill
  ✨ Generate new: 1 skill

Proceed? [y] Yes  [m] Modify  [s] Skip  [q] Abort
----------------------------------------------------
```

**After Approval:**
```
----------------------------------------------------
Installing Skills...
----------------------------------------------------
[1/5] api-implementation     ✅ Installed from GitHub
[2/5] data-modeling          ✅ Installed from GitHub
[3/5] input-validation       ✅ Installed from npm
[4/5] stripe-integration     ✅ Installed from GitHub
[5/5] authentication         ✅ Installed + customized

Generating missing skills...
[1/1] error-handling         ✅ Generated via skill-creator

Files created:
  .claude/skills/
  ├── api-implementation/    [installed]
  ├── data-modeling/         [installed]
  ├── input-validation/      [installed]
  ├── stripe-integration/    [installed]
  ├── authentication/        [installed + customized]
  ├── error-handling/        [generated]
  └── README.md
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

**Core Principle:** Marketplace First, Then Configure

**Actions:**
1. **Extract** external services from specification (DB, payments, messaging, etc.)
2. **Search** via `marketplace-plugin-scout` for latest MCP servers
3. **Evaluate** search results (official packages preferred, freshness, downloads)
4. **Configure** `.mcp.json` with selected MCPs
5. **Generate** setup guides in `docs/mcp-setup/`

**Progress Display:**
```
----------------------------------------------------
Step 4/7: MCP Configuration
----------------------------------------------------
Detected Services: 5

Searching marketplace-plugin-scout...

Search Results:
  ✅ postgres    (@modelcontextprotocol/server-postgres) Score: 95 [Official]
  ✅ stripe      (@stripe/mcp-server) Score: 92 [Official Stripe]
  ✅ github      (@modelcontextprotocol/server-github) Score: 95 [Official]
  ✅ slack       (@anthropic/mcp-slack) Score: 88
  ⚠️ sentry      (sentry-mcp) Score: 55 → Skip, use SDK

Plan:
  📦 Configure MCP: 4 servers
  ⏭️ Skip (use SDK): 1 service

Files to Generate:
  - .mcp.json
  - docs/mcp-setup/README.md
  - docs/mcp-setup/postgres-setup.md
  - docs/mcp-setup/stripe-setup.md
  - docs/mcp-setup/github-setup.md
  - docs/mcp-setup/slack-setup.md
  - .env.example

Proceed? [y] Yes  [m] Modify  [s] Skip  [q] Abort
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

Skills (Marketplace First):
  📦 Installed: 5 skills
  ✨ Generated: 1 skill (gap analysis)
  🔧 Customized: 1 skill

  .claude/skills/
  ├── api-implementation/     [installed]
  ├── data-modeling/          [installed]
  ├── authentication/         [installed + customized]
  ├── input-validation/       [installed]
  ├── error-handling/         [generated]
  └── stripe-integration/     [installed]

Sub-agents:
  [+] .claude/agents/spec-verifier.md
  [+] .claude/agents/test-generator.md
  [+] .claude/agents/implementation-guide.md

MCP Servers (via marketplace-plugin-scout):
  [+] .mcp.json (4 servers configured)
  [+] docs/mcp-setup/README.md
  [+] docs/mcp-setup/*.md (setup guides)
  [+] .env.example

Tasks:
  [+] docs/TASKS.md

Documentation:
  [+] CLAUDE.md (updated)

Action Required:
  ⚠️ MCP setup needed. See docs/mcp-setup/README.md

Next Steps:
  1. Configure MCP servers (copy .env.example to .env)
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
