# spec2impl

Generate a Claude Code implementation environment from specification documents.

## Overview

spec2impl analyzes Markdown specifications and automatically generates a comprehensive environment to assist Claude Code with implementation:

- **Skills** - Implementation patterns and guides based on your specifications
- **Sub-agents** - Specialized agents for verification, testing, and implementation
- **MCP Configuration** - Recommended MCP servers based on your tech stack
- **Task List** - Auto-extracted and generated implementation tasks
- **CLAUDE.md** - Implementation workflow documentation

## Features

- **Native Claude Code Integration** - Works as a custom slash command
- **Leverages Claude's Intelligence** - Claude understands spec intent, not just static parsing
- **Step-by-Step Approval** - Review and approve each generation step
- **Task Handoff Support** - Structured task list ensures continuity across sessions

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
Step 2: Skills Generation -> Approve
Step 3: Sub-agents Generation -> Approve
Step 4: MCP Configuration -> Approve
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

### Marketplace Commands

```
/spec2impl marketplace search <query>    # Search for Skills
/spec2impl marketplace install <source>  # Install a Skill
/spec2impl marketplace list              # List installed Skills
/spec2impl marketplace uninstall <name>  # Remove a Skill
```

**Source Formats:**
- `github:user/repo[/path][@branch]` - From GitHub repository
- `npm:@scope/package[@version]` - From npm package
- `https://...` - Direct URL

### Progress Dashboard

```
/spec2impl dashboard
```

Displays visual implementation progress with task status and recommendations.

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

Generates specialized sub-agents tailored to project requirements.

| Property | Value |
|----------|-------|
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, Task |
| **Input** | SpecAnalyzer output, tech stack, project structure |
| **Output** | `.claude/agents/` directory with agent files |

**Generated Agent Types:**

| Type | Always Generated | Description |
|------|------------------|-------------|
| Core | Yes | spec-verifier, test-generator |
| Feature-Specific | Conditional | api-implementer, model-designer, auth-implementer, etc. |
| Domain-Specific | Auto-detected | E-commerce, SaaS, CMS-specific agents |

---

### skills-generator

Identifies required Skills from specifications and generates them using skill-creator.

| Property | Value |
|----------|-------|
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, Task |
| **Input** | SpecAnalyzer output, tech stack |
| **Output** | `.claude/skills/` directory with Skill files |

**Auto-Detected Skill Categories:**

| Category | Detection Trigger |
|----------|-------------------|
| api-implementation | REST/GraphQL endpoints defined |
| data-modeling | Model/schema definitions present |
| authentication | JWT/OAuth/auth requirements |
| input-validation | 5+ validation rules |
| error-handling | Error codes defined |

---

### mcp-configurator

Detects external services, researches MCP servers, and generates configuration.

| Property | Value |
|----------|-------|
| **Tools** | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch |
| **Input** | Tech stack, external service requirements |
| **Output** | `.mcp.json`, `docs/mcp-setup/` |

**Detected Service Categories:**

| Category | Examples |
|----------|----------|
| Database | PostgreSQL, MySQL, MongoDB, Redis |
| Authentication | OAuth, JWT, Auth0, Firebase Auth |
| Storage | S3, GCS, Azure Blob, Cloudinary |
| Messaging | Slack, Discord, Teams, Email |
| Payments | Stripe, PayPal, Square |

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

Package manager for Claude Code Skills from multiple registries.

| Property | Value |
|----------|-------|
| **Tools** | Bash, Read, Write, Edit, Glob, Grep, WebFetch |
| **Registries** | GitHub, npm, Custom URLs |

**Commands:**
- `search` - Search across registries
- `install` - Download and install Skills
- `list` - Show installed Skills
- `uninstall` - Remove Skills

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
