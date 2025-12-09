# Agents Category Guide

Download agent templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/agents`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/agents`

## Output Directory

- Target: `.claude/agents/`

## Available Subcategories

| Subcategory | Description | Examples |
|-------------|-------------|----------|
| development-team | Development roles | frontend-developer, backend-developer, fullstack-developer |
| testing | QA and testing | test-engineer, qa-automation-engineer |
| security | Security specialists | security-auditor, penetration-tester, compliance-specialist |
| devops | DevOps and cloud | devops-engineer, cloud-architect, kubernetes-specialist |
| documentation | Technical writing | technical-writer, api-documentation-specialist |
| data | Data engineering | data-engineer, data-scientist |
| ai-ml | AI/ML specialists | ai-engineer, ml-engineer |
| management | Technical leadership | tech-lead, business-analyst |
| git | Git workflow | git-flow-manager |

## Commands

```bash
# List all agents
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category agents --json

# Search agents
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category agents --json

# Download specific agent
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/agents
```

## Spec Mapping

| Spec Mentions | Recommended Agents |
|---------------|-------------------|
| Frontend/React/Next.js | frontend-developer |
| Backend/API | backend-developer, fullstack-developer |
| Testing/QA | test-engineer, qa-automation-engineer |
| Security/Auth | security-auditor, compliance-specialist |
| Database | data-engineer |
| Documentation | technical-writer |
| CI/CD/Deployment | devops-engineer |
| AI/ML | ai-engineer, ml-engineer |
