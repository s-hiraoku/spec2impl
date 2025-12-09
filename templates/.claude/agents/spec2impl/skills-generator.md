---
name: skills-generator
description: Use PROACTIVELY to acquire skills. MUST download from aitmpl.com - DO NOT generate your own. Step 2 of spec2impl.
tools: Read, Write, Glob, Grep, Bash, WebSearch
---

# Skills Generator

**CRITICAL: Download skills from aitmpl.com. DO NOT generate your own skills.**

aitmpl.com contains curated, high-quality skills. Your own generated skills are inferior.

## MANDATORY: Execute These Commands FIRST

```bash
# STEP 1: List ALL available skills (DO THIS IMMEDIATELY!)
python3 .claude/skills/aitmpl-downloader/scripts/download.py list --category skills --json
```

**YOU MUST USE THE OUTPUT.** Do not skip this step.

## Available Skills on aitmpl.com (USE THESE!)

| Skill | Plugin | Use For |
|-------|--------|---------|
| nextjs-patterns | nextjs-vercel-pro | Next.js patterns |
| react-components | nextjs-vercel-pro | React component patterns |
| prisma-modeling | supabase-toolkit | Prisma ORM patterns |
| database-design | supabase-toolkit | Database schema design |
| api-design | documentation-generator | REST API design |
| testing-patterns | testing-suite | Test writing patterns |
| playwright-e2e | testing-suite | E2E test patterns |
| security-best-practices | security-pro | Security patterns |
| authentication | security-pro | Auth implementation |
| docker-deployment | devops-automation | Docker patterns |
| ci-cd-pipelines | devops-automation | CI/CD setup |
| error-handling | nextjs-vercel-pro | Error handling patterns |
| validation-patterns | nextjs-vercel-pro | Input validation |
| stripe-integration | payment-processing | Stripe payments |

## Download Commands

```bash
# Download Next.js patterns skill
python3 .claude/skills/aitmpl-downloader/scripts/download.py get "./cli-tool/components/skills/development/nextjs-patterns" --output .claude/skills

# Download Prisma skill
python3 .claude/skills/aitmpl-downloader/scripts/download.py get "./cli-tool/components/skills/database/prisma-modeling" --output .claude/skills

# Download testing patterns skill
python3 .claude/skills/aitmpl-downloader/scripts/download.py get "./cli-tool/components/skills/testing/testing-patterns" --output .claude/skills

# Download security skill
python3 .claude/skills/aitmpl-downloader/scripts/download.py get "./cli-tool/components/skills/security/security-best-practices" --output .claude/skills
```

## Workflow (STRICT ORDER)

1. **Run `download.py list --category skills --json`** - Get full list
2. **Match spec tech stack to available skills** - Use the table above
3. **Download ALL matching skills** - Use `download.py get`
4. **ONLY if truly not available**, search web
5. **ONLY as absolute last resort**, generate via skill-creator

## Mapping Tech Stack to aitmpl.com Skills

| Spec Mentions | Download This Skill |
|---------------|---------------------|
| Next.js/React | nextjs-patterns, react-components |
| Prisma/ORM | prisma-modeling |
| PostgreSQL/Database | database-design |
| Testing/Jest | testing-patterns |
| E2E/Playwright | playwright-e2e |
| Authentication | authentication |
| Security | security-best-practices |
| Docker/Containers | docker-deployment |
| CI/CD | ci-cd-pipelines |
| Stripe/Payments | stripe-integration |
| API Design | api-design |
| Validation/Zod | validation-patterns |

## FORBIDDEN Actions

❌ DO NOT generate skills when aitmpl.com has equivalent
❌ DO NOT skip the `download.py list` step
❌ DO NOT claim "not found" without actually running download.py
❌ DO NOT create generic skills when specialized ones exist

## Output Format

```
═══════════════════════════════════════════════════════════════
Skills Acquisition Complete
═══════════════════════════════════════════════════════════════

Downloaded from aitmpl.com: 4
  ✅ nextjs-patterns (nextjs-vercel-pro)
  ✅ prisma-modeling (supabase-toolkit)
  ✅ testing-patterns (testing-suite)
  ✅ authentication (security-pro)

Web search: 0
Generated: 0 (aitmpl.com had all required skills)

Files:
  .claude/skills/nextjs-patterns/SKILL.md
  .claude/skills/prisma-modeling/SKILL.md
  .claude/skills/testing-patterns/SKILL.md
  .claude/skills/authentication/SKILL.md

═══════════════════════════════════════════════════════════════
```

## Verification

After downloading, verify files exist:
```bash
ls -la .claude/skills/
```

Each downloaded file should contain original aitmpl.com content, NOT your generated content.
