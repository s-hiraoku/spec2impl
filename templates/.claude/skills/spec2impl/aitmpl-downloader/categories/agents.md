# Agents Category Guide

Download agent templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/agents`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/agents`

## Output Directory

- Target: `.claude/agents/`

---

## 3-Layer Agents Configuration

> ⚠️ **Warning: Agents consume context window space**
>
> Each agent definition is loaded when invoked, so **too many agents can impact performance**.
> - Select only agents you'll actually use
> - Additional agents can be added later
> - When in doubt, start with base agents only

### Layer 1: Recommended Base Agents (User Selection)

Present these via `AskUserQuestion` with multiSelect. Useful for any development project.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install base agents? These are useful for general development.",
    header: "Base Agents",
    options: [
      {
        label: "code-reviewer (Recommended)",
        description: "Code review, quality checks, best practices enforcement"
      },
      {
        label: "test-engineer",
        description: "Test strategy, test case generation, coverage analysis"
      },
      {
        label: "technical-writer",
        description: "Documentation generation, API docs, README creation"
      }
    ],
    multiSelect: true
  }]
})
```

**Agent Details:**

| Agent | Description | Use Case |
|-------|-------------|----------|
| `code-reviewer` | Reviews code for quality, patterns, and best practices | Code quality in any project |
| `test-engineer` | Creates test strategies and generates test cases | Testing in any project |
| `technical-writer` | Generates documentation and technical writing | Documentation for any project |

---

### Layer 2: Auto-Detected Agents (Spec-based)

These agents are **automatically detected** from specification keywords. Show detected items to user for confirmation.

| Keywords in Spec | Agent | Description |
|------------------|-------|-------------|
| frontend, react, vue, next.js, UI | `frontend-developer` | Frontend development specialist |
| frontend, react, vue, UI, design | `ui-ux-designer` | UI/UX design and implementation |
| backend, API, server, REST | `backend-architect` | Backend architecture and API design |
| fullstack, full-stack | `fullstack-developer` | Full-stack development |
| database, SQL, postgres, mysql | `database-architect` | Database design and optimization |
| database, query, performance | `database-optimizer` | Database query optimization |
| devops, CI/CD, pipeline | `devops-engineer` | DevOps and CI/CD pipelines |
| deploy, deployment, hosting | `deployment-engineer` | Deployment and hosting |
| security, auth, authentication | `security-engineer` | Security implementation |
| security, audit, compliance | `security-auditor` | Security auditing |
| AI, ML, machine learning | `ai-engineer` | AI/ML implementation |
| ML, model, training | `ml-engineer` | ML model development |
| MCP, protocol, server | `mcp-server-architect` | MCP server architecture |
| MCP, integration | `mcp-expert` | MCP integration expertise |
| GraphQL, schema | `graphql-architect` | GraphQL API design |
| mobile, iOS, Android | `mobile-developer` | Mobile app development |
| game, unity, unreal | `game-designer` | Game development |

---

### Layer 3: Additional Recommended Agents (User Selection)

Present these via `AskUserQuestion` based on detected project type.

```typescript
AskUserQuestion({
  questions: [{
    question: "Install additional recommended agents?",
    header: "Additional Agents",
    options: [
      // Options vary based on project type - see below
    ],
    multiSelect: true
  }]
})
```

#### For Web Application Projects
| Agent | Description |
|-------|-------------|
| `frontend-developer` | Frontend development specialist |
| `backend-architect` | Backend architecture and API design |
| `ui-ux-designer` | UI/UX design and implementation |
| `performance-engineer` | Performance optimization |

#### For API/Backend Projects
| Agent | Description |
|-------|-------------|
| `graphql-architect` | GraphQL API design |
| `api-documenter` | API documentation generation |
| `database-architect` | Database design |
| `security-engineer` | Security implementation |

#### For Data/Analytics Projects
| Agent | Description |
|-------|-------------|
| `data-scientist` | Data analysis and modeling |
| `data-engineer` | Data pipeline development |
| `ml-engineer` | ML model development |
| `quant-analyst` | Quantitative analysis |

#### For DevOps/Infrastructure Projects
| Agent | Description |
|-------|-------------|
| `cloud-architect` | Cloud infrastructure design |
| `terraform-specialist` | Infrastructure as code |
| `monitoring-specialist` | Monitoring and observability |
| `security-engineer` | Security implementation |

---

## Available Agents (by Subcategory)

### development-team
| Agent | Description |
|-------|-------------|
| `frontend-developer` | Frontend development |
| `backend-architect` | Backend architecture |
| `fullstack-developer` | Full-stack development |
| `mobile-developer` | Mobile development |
| `ios-developer` | iOS development |
| `ui-ux-designer` | UI/UX design |
| `devops-engineer` | DevOps engineering |
| `cli-ui-designer` | CLI UI design |

### development-tools
| Agent | Description |
|-------|-------------|
| `code-reviewer` | Code review |
| `test-engineer` | Test engineering |
| `debugger` | Debugging specialist |
| `error-detective` | Error analysis |
| `performance-profiler` | Performance profiling |
| `unused-code-cleaner` | Dead code removal |
| `mcp-expert` | MCP expertise |
| `dx-optimizer` | Developer experience |

### database
| Agent | Description |
|-------|-------------|
| `database-architect` | Database design |
| `database-optimizer` | Query optimization |
| `database-admin` | Database administration |
| `nosql-specialist` | NoSQL databases |
| `supabase-schema-architect` | Supabase schema design |
| `neon-database-architect` | Neon database design |

### devops-infrastructure
| Agent | Description |
|-------|-------------|
| `cloud-architect` | Cloud architecture |
| `deployment-engineer` | Deployment |
| `terraform-specialist` | Terraform/IaC |
| `monitoring-specialist` | Monitoring |
| `network-engineer` | Networking |
| `security-engineer` | Security |
| `vercel-deployment-specialist` | Vercel deployment |

### data-ai
| Agent | Description |
|-------|-------------|
| `ai-engineer` | AI engineering |
| `ml-engineer` | ML engineering |
| `data-scientist` | Data science |
| `data-engineer` | Data engineering |
| `nlp-engineer` | NLP |
| `computer-vision-engineer` | Computer vision |
| `mlops-engineer` | MLOps |
| `quant-analyst` | Quantitative analysis |

### documentation
| Agent | Description |
|-------|-------------|
| `technical-writer` | Technical writing |
| `api-documenter` | API documentation |
| `changelog-generator` | Changelog generation |
| `docusaurus-expert` | Docusaurus documentation |

### security
| Agent | Description |
|-------|-------------|
| `security-engineer` | Security implementation |
| `security-auditor` | Security auditing |

### mcp-dev-team
| Agent | Description |
|-------|-------------|
| `mcp-server-architect` | MCP server design |
| `mcp-protocol-specialist` | MCP protocol |
| `mcp-integration-engineer` | MCP integration |
| `mcp-testing-engineer` | MCP testing |
| `mcp-security-auditor` | MCP security |

---

## Commands

```bash
# List all agents
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category agents --json

# Search agents
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category agents --json

# Download specific agent
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/agents
```
