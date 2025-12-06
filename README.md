# spec2impl

Generate an **implementation harness** for Claude Code from specification documents.

## Overview

spec2impl analyzes Markdown specifications and automatically prepares an **implementation harness** — a comprehensive environment that enables Claude Code to efficiently implement the specification:

- **Skills** - Implementation patterns discovered via web search and generated as needed
- **Sub-agents** - Specialized agents designed using latest AI patterns
- **MCP Configuration** - MCP servers researched and selected via web search
- **Task List** - Auto-extracted and generated implementation tasks
- **CLAUDE.md** - Implementation workflow documentation

### What is an Implementation Harness?

An implementation harness is the scaffolding that supports Claude Code during implementation. Rather than generating code directly, spec2impl prepares the **tools, context, and guidance** that Claude needs to implement the specification correctly and efficiently. This includes specialized agents for different aspects of the implementation, skills that encode best practices and patterns, and MCP integrations for external services.

## Features

- **Web Search First** - Always searches for the latest tools, skills, and patterns before generating
- **Native Claude Code Integration** - Works as a custom slash command
- **Leverages Claude's Intelligence** - Claude understands spec intent, not just static parsing
- **Step-by-Step Approval** - Review and approve each generation step
- **Task Handoff Support** - Structured task list ensures continuity across sessions
- **Always Up-to-Date** - No hardcoded lists; researches current best options for your tech stack

## Installation

### Using npx (Recommended)

Run in your project root:

```bash
npx spec2impl
```

This installs the required files into your `.claude/` directory.

**Options:**
- `--dry-run` - Preview files without installing
- `--force` - Overwrite existing `.claude/` directory

### Manual Installation

Clone and copy the templates:

```bash
git clone https://github.com/your-repo/spec2impl.git
cp -r spec2impl/templates/.claude /path/to/your/project/
```

## Usage

### Basic Usage

In Claude Code, run:

```
/spec2impl docs/
```

This analyzes specifications in `docs/` and builds the implementation environment.

### Execution Flow

```
/spec2impl docs/
       |
Step 1: Specification Analysis -> Approve
Step 2: Skills Acquisition (Search → Install → Assess Gaps → Generate) -> Approve
Step 3: Sub-agents Generation -> Approve
Step 4: MCP Configuration (Search → Configure) -> Approve
Step 5: Task List Generation -> Approve
Step 6: CLAUDE.md Update -> Approve
Step 7: Cleanup (optional) -> Approve
       |
Completion Report
```

---

## Installed Components

### Directory Structure

```
.claude/
├── commands/
│   └── spec2impl.md          # Main command
├── agents/
│   └── spec2impl/
│       ├── spec-analyzer.md
│       ├── skills-generator.md
│       ├── subagent-generator.md
│       ├── mcp-configurator.md
│       ├── task-list-generator.md
│       ├── claude-md-updater.md
│       ├── marketplace.md
│       └── progress-dashboard.md
└── skills/
    └── skill-creator/
        ├── SKILL.md
        ├── references/
        └── scripts/
```

---

## Command Reference

### Main Command

```
/spec2impl <docs-directory>
```

Analyzes specifications and builds the implementation environment.

| Description | Argument |
|-------------|----------|
| Target directory | Path to specification docs (e.g., `docs/`) |

### Note on Marketplace and Dashboard

The Marketplace and Progress Dashboard agents are **internal services** called by other agents during the spec2impl workflow. They are not directly invoked by users. Skills Generator automatically uses Marketplace to search for and install skills, and the main orchestrator can call Progress Dashboard to show implementation status.

---

## Sub-Agents Reference

spec2impl uses specialized sub-agents for each step of the workflow. Below is a summary of each agent:

| Agent | Step | Description |
|-------|------|-------------|
| **Spec Analyzer** | 1 | Analyzes Markdown specs to extract APIs, models, workflows, constraints, and tech stack |
| **Skills Generator** | 2 | Searches marketplace for skills, installs found ones, assesses gaps, generates missing skills |
| **Subagent Generator** | 3 | Researches latest agent design patterns and generates SpecVerifier, TestGenerator, etc. |
| **MCP Configurator** | 4 | Detects external services, searches for MCP servers, generates .mcp.json and setup docs |
| **Task List Generator** | 5 | Extracts tasks from specs and auto-generates implementation tasks with dependencies |
| **CLAUDE.md Updater** | 6 | Updates CLAUDE.md with implementation environment, preserving existing sections |

### Internal Services

These agents are called internally by other agents during the workflow:

| Agent | Description |
|-------|-------------|
| **Progress Dashboard** | Displays workflow progress after each step. Also tracks TASKS.md progress during implementation. |
| **Marketplace Plugin Scout** | Searches and evaluates plugins via web search. Provides scored recommendations. Does NOT install. |
| **Marketplace** | Installs, lists, and removes plugins from GitHub/npm/URLs. Delegates search to Plugin Scout. |

---

### Spec Analyzer

Analyzes Markdown specification documents to extract structured implementation data.

| Property | Value |
|----------|-------|
| **Step** | 1 |
| **Tools** | Glob, Grep, Read |
| **Input** | Directory path containing specs |
| **Output** | Structured YAML with APIs, models, workflows, constraints, tech stack |

**Extraction Targets:**
- API definitions (endpoints, methods, parameters, responses)
- Data models (fields, types, constraints)
- Workflows and use cases
- Constraints and business rules
- Technology stack detection
- Existing tasks/checklists

---

### Skills Generator

Identifies required Skills from specifications, searches for existing skills via marketplace, installs them, assesses gaps, and generates only what's missing.

| Property | Value |
|----------|-------|
| **Step** | 2 |
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch |
| **Input** | SpecAnalyzer output, tech stack |
| **Output** | `.claude/skills/` directory with Skill files |

**7-Step Process (Marketplace First, Then Generate):**
1. **Identify** required skills from specification
2. **Search** via marketplace-plugin-scout for each skill category
3. **Evaluate** and select best matches
4. **Install** found skills via marketplace
5. **Assess Gaps** - evaluate if additional skills needed
6. **Generate** missing skills using skill-creator
7. **Customize** with project-specific information

---

### Subagent Generator

Identifies required sub-agents from specification analysis and generates optimally configured agents.

| Property | Value |
|----------|-------|
| **Step** | 3 |
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch |
| **Input** | SpecAnalyzer output, tech stack, project structure |
| **Output** | `.claude/agents/` directory with agent files |

**Process:**
1. Identify required agents from specification
2. **Web search** for latest agent design patterns
3. Design agent architecture based on research
4. Generate agent files with embedded spec context
5. Configure agent collaboration workflow

**Generated Agent Types:**

| Type | Always Generated | Description |
|------|------------------|-------------|
| Core | Yes | spec-verifier, test-generator, implementation-guide |
| Feature-Specific | Conditional | api-implementer, model-designer, auth-implementer, etc. |
| Domain-Specific | Auto-detected | E-commerce, SaaS, CMS-specific agents |

---

### MCP Configurator

Detects external services from specifications and configures optimal MCP servers.

| Property | Value |
|----------|-------|
| **Step** | 4 |
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch |
| **Input** | Tech stack, external service requirements |
| **Output** | `.mcp.json`, `docs/mcp-setup/`, `.env.example` |

**5-Step Process (Marketplace First, Then Configure):**
1. **Extract** external services from specification
2. **Search** via marketplace-plugin-scout for MCP servers
3. **Evaluate** and select best MCPs (official packages preferred)
4. **Configure** .mcp.json with selected MCPs
5. **Document** token acquisition guides in docs/mcp-setup/

---

### Task List Generator

Extracts existing tasks from specifications and auto-generates implementation tasks.

| Property | Value |
|----------|-------|
| **Step** | 5 |
| **Tools** | Read, Write, Edit, Glob, Grep, Bash |
| **Input** | SpecAnalyzer output |
| **Output** | `docs/TASKS.md` |

**Task Categories:**

| Category | ID Prefix | Description |
|----------|-----------|-------------|
| Spec-Defined | `T-SPEC-*` | Tasks extracted from specifications |
| Auto-Generated | `T-AUTO-*` | Tasks generated from API/model definitions |
| Verification | `T-VERIFY-*` | Post-implementation verification tasks |

---

### CLAUDE.md Updater

Updates or creates CLAUDE.md with the implementation environment section.

| Property | Value |
|----------|-------|
| **Step** | 6 |
| **Tools** | Read, Write, Edit, Glob, Bash |
| **Input** | Generated files info, existing CLAUDE.md |
| **Output** | `CLAUDE.md` (merged) |

**Merge Behavior:**
- Preserves existing user-defined sections
- Updates only the `<!-- spec2impl generated section -->` block
- Creates new file with basic structure if absent

---

### Marketplace Plugin Scout

Searches and evaluates plugins (Skills, MCP servers, Agents) via web search.

| Property | Value |
|----------|-------|
| **Type** | Internal Service |
| **Tools** | WebSearch, WebFetch, Read, Glob, Grep |
| **Called By** | Skills Generator, MCP Configurator |

**Key Responsibilities:**
- Search GitHub, npm, and other sources for latest plugins
- Evaluate plugin quality (freshness, stars, compatibility)
- Compare official vs community packages
- Provide recommendations with scores

**Important:** This agent searches and evaluates only. It does NOT install plugins - that's delegated to the Marketplace agent.

---

### Marketplace

Internal registry and installer for Claude Code Plugins.

| Property | Value |
|----------|-------|
| **Type** | Internal Service |
| **Tools** | Bash, Read, Write, Edit, Glob, Grep |
| **Sources** | GitHub, npm, Custom URLs |

**Actions:**
- `install` - Download and install plugin from source
- `list` - Show installed plugins (skills, MCPs, agents)
- `uninstall` - Remove plugins

**Important:** For plugin discovery, this agent delegates to `marketplace-plugin-scout`.

---

### Progress Dashboard

Generates visual progress reports with two modes.

| Property | Value |
|----------|-------|
| **Type** | Internal Service |
| **Tools** | Read, Glob, Grep |
| **Modes** | `workflow` (spec2impl steps), `tasks` (TASKS.md progress) |

**Workflow Mode (during spec2impl):**
- Step-by-step progress (Step 1/7, Step 2/7, etc.)
- Completed step summaries
- Current step status
- Visual progress bar

**Tasks Mode (during implementation):**
- Overall task progress with visual bar
- Category breakdown (Spec-Defined, Models, APIs, Verification)
- Current focus and recent activity
- Next recommended tasks with dependency analysis
- Blockers and warnings

---

## Skills Reference

### skill-creator

Guide for creating effective Claude Code Skills.

| Property | Value |
|----------|-------|
| **Location** | `.claude/skills/skill-creator/` |
| **Purpose** | Create or update Skills that extend Claude's capabilities |

**Included Resources:**
- `SKILL.md` - Main skill guide
- `references/output-patterns.md` - Output format patterns
- `references/workflows.md` - Workflow templates
- `scripts/` - Utility scripts for skill development

**Core Principles:**
1. **Concise is Key** - Only add context Claude doesn't already have
2. **Set Appropriate Freedom** - Match specificity to task fragility
3. **Bundle Resources** - Include scripts and references for complex tasks

---

## Specification Format

spec2impl recognizes these patterns in your Markdown specifications:

### API Definitions

```markdown
### POST /users

Create a new user.

**Parameters:**
- email (string, required): Email address
- name (string, required): User name

**Response:**
- 201: User object
- 400: Validation error
```

### Data Models

```markdown
### User Model

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | User ID |
| email | string | Yes | Email address |
| name | string | Yes | User name |
```

### Constraints

```markdown
## Constraints

- Email address must be unique
- Password must be 8+ characters
```

### Checklists

```markdown
## Implementation Checklist

- [ ] POST /users - Create user
- [ ] GET /users/:id - Get user
```

---

## Generated Files

After running `/spec2impl docs/`, these files are generated:

| File | Description |
|------|-------------|
| `.claude/skills/implementation/SKILL.md` | Implementation patterns based on specs |
| `.claude/skills/implementation/patterns/*.md` | API, validation, error handling patterns |
| `.claude/agents/*.md` | Generated sub-agents |
| `.mcp.json` | MCP server configuration |
| `docs/mcp-setup/*.md` | MCP setup guides with token instructions |
| `docs/TASKS.md` | Implementation task list |
| `CLAUDE.md` | Updated with implementation workflow |

---

## Generated Sub-Agents Usage

After environment setup, these sub-agents become available:

### SpecVerifier

Verify implementation matches specifications.

```
verify implementation
```

### TestGenerator

Generate test cases from specifications.

```
generate tests for User API
```

### ImplementationGuide

Get guidance on implementing features.

```
how to implement user creation
```

---

## License

MIT

## Related Projects

- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Claude Skills catalog
- [Claude Code](https://claude.ai/claude-code) - Anthropic's CLI tool
