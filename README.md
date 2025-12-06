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

### spec-analyzer

Analyzes Markdown specification documents to extract structured implementation data.

| Property | Value |
|----------|-------|
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

### task-list-generator

Extracts and generates implementation tasks, creating a structured `docs/TASKS.md` file.

| Property | Value |
|----------|-------|
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

### subagent-generator

Generates specialized sub-agents using latest design patterns researched via web search.

| Property | Value |
|----------|-------|
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
| Core | Yes | spec-verifier, test-generator |
| Feature-Specific | Conditional | api-implementer, model-designer, auth-implementer, etc. |
| Domain-Specific | Auto-detected | E-commerce, SaaS, CMS-specific agents |

---

### skills-generator

Identifies required Skills from specifications, searches for skill plugins via `marketplace-plugin-scout`, and generates only what's missing.

| Property | Value |
|----------|-------|
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch |
| **Input** | SpecAnalyzer output, tech stack |
| **Output** | `.claude/skills/` directory with Skill files |

**Process:**
1. Identify required skills from specification
2. **Search via marketplace-plugin-scout** for each skill category
3. Evaluate and select best matches
4. **Install via marketplace-plugin-scout** from external sources
5. Generate only missing skills using skill-creator
6. Customize with project-specific information

---

### mcp-configurator

Detects external services, searches for MCP plugins via `marketplace-plugin-scout`, and generates optimal configuration.

| Property | Value |
|----------|-------|
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch |
| **Input** | Tech stack, external service requirements |
| **Output** | `.mcp.json`, `docs/mcp-setup/`, `.env.example` |

**Process:**
1. Extract external services from specification
2. **Search via marketplace-plugin-scout** for MCP servers
3. Evaluate and select best MCPs (official packages preferred)
4. Generate .mcp.json configuration
5. Generate token acquisition guides for each MCP

---

### claude-md-updater

Updates or creates CLAUDE.md with the implementation environment section.

| Property | Value |
|----------|-------|
| **Tools** | Read, Write, Edit, Glob, Bash |
| **Input** | Generated files info, existing CLAUDE.md |
| **Output** | `CLAUDE.md` (merged) |

**Merge Behavior:**
- Preserves existing user-defined sections
- Updates only the `<!-- spec2impl generated section -->` block
- Creates new file with basic structure if absent

---

### marketplace

Internal registry and installer for Claude Code Plugins. Works with `marketplace-plugin-scout` for search functionality.

| Property | Value |
|----------|-------|
| **Tools** | Bash, Read, Write, Edit, Glob, Grep |
| **Sources** | GitHub, npm, Custom URLs |

**Actions (called by Skills Generator and MCP Configurator):**
- `search` - **Delegates to marketplace-plugin-scout**
- `install` - Download and install plugin from source
- `list` - Show installed plugins (skills, MCPs, agents)
- `uninstall` - Remove plugins

**Note:** This agent is called internally by other agents, not directly by users. For plugin discovery, it delegates to `marketplace-plugin-scout`.

---

### marketplace-plugin-scout (External)

Specialized agent for searching, evaluating, and registering plugins from the Claude Code Marketplace.

| Property | Value |
|----------|-------|
| **Location** | `.claude/agents/marketplace-plugin-scout.md` |
| **Purpose** | Plugin discovery via web search, evaluation, and registration |

**Key Responsibilities:**
- Search the Claude Code Marketplace
- Evaluate plugin quality (freshness, popularity, compatibility)
- Compare official vs community packages
- Provide recommendations with scores

**Called by:**
- Skills Generator (for skill plugins)
- MCP Configurator (for MCP server plugins)
- Marketplace (for search delegation)

---

### progress-dashboard

Generates visual progress reports comparing specification requirements against implementation.

| Property | Value |
|----------|-------|
| **Tools** | Read, Glob, Grep |
| **Input** | `docs/TASKS.md` |
| **Output** | Visual dashboard with progress bars |

**Dashboard Sections:**
- Overall progress with visual bar
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
