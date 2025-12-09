# Skills Category Guide

Download skill templates from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/skills`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/skills`

## Output Directory

- Target: `.claude/skills/`

## Available Skill Categories

| Category | Description | Examples |
|----------|-------------|----------|
| business-marketing | Business and marketing | marketing-strategy, business-analysis |
| creative-design | Design and creativity | ui-design, graphic-design |
| database | Database patterns | prisma-modeling, database-design |
| development | Development patterns | nextjs-patterns, react-components |
| document-processing | Document handling | pdf-processing, excel-automation |
| enterprise-communication | Communication | email-templates, slack-integration |
| media | Media processing | image-processing, video-editing |
| productivity | Productivity tools | task-management, time-tracking |
| utilities | Utility scripts | file-management, automation-scripts |

## Commands

```bash
# List all skills
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category skills --json

# Search skills
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category skills --json

# Download specific skill
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude/skills
```

## Spec Mapping

| Spec Mentions | Recommended Skills |
|---------------|-------------------|
| Next.js/React | nextjs-patterns, react-components |
| Prisma/ORM | prisma-modeling |
| Database | database-design |
| Testing | testing-patterns |
| E2E/Playwright | playwright-e2e |
| Authentication | authentication |
| Security | security-best-practices |
| Docker | docker-deployment |
| CI/CD | ci-cd-pipelines |
| Payments/Stripe | stripe-integration |

## Skill Structure

Skills may be directories containing multiple files:

```
skill-name/
├── SKILL.md           # Main skill definition
├── scripts/           # Helper scripts (optional)
├── templates/         # Code templates (optional)
└── references/        # Reference docs (optional)
```

The downloader handles both single-file and directory-based skills automatically.
