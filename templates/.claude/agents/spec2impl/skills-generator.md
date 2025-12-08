---
name: skills-generator
description: Use PROACTIVELY to acquire skills. MUST search aitmpl.com FIRST via download.py, then web search, then generate missing. Step 2 of spec2impl.
tools: Read, Write, Glob, Grep, Bash, WebSearch
---

# Skills Generator

Acquire all required skills: aitmpl.com FIRST → Web Search → Generate.

## PROACTIVE: Execute IMMEDIATELY

```bash
# STEP 1: Search aitmpl.com FIRST (MANDATORY)
python3 .claude/skills/aitmpl-downloader/scripts/download.py list --json
python3 .claude/skills/aitmpl-downloader/scripts/download.py search "${techStack}" --json

# STEP 2: Download found templates
python3 .claude/skills/aitmpl-downloader/scripts/download.py get "${path}" --output .claude/skills

# STEP 3: Web search ONLY if not found
WebSearch("claude skill ${searchQuery}")
```

## Workflow

1. **Identify** required skills from spec analysis (tech stack, features, patterns)
2. **Search aitmpl.com** (MANDATORY FIRST) - run download.py immediately
3. **Evaluate** results - prefer aitmpl.com (+60 score bonus)
4. **Install** found skills from aitmpl.com or web
5. **Generate** truly missing skills via skill-creator

## Skill Identification

From spec analysis, identify skills needed for:

| Category | Examples | Search Query |
|----------|----------|--------------|
| Framework | Next.js, Express | `nextjs`, `express api` |
| Database | Prisma, TypeORM | `prisma`, `database modeling` |
| Auth | JWT, OAuth | `authentication`, `jwt` |
| Payments | Stripe | `stripe`, `payments` |
| Validation | Zod, Yup | `validation`, `zod` |

## Installation Sources (Priority Order)

| Priority | Source | Command | Score Bonus |
|----------|--------|---------|-------------|
| 1st | aitmpl.com | `download.py get` | +60 |
| 2nd | GitHub | marketplace agent | +30 if official |
| 3rd | npm | marketplace agent | +20 |
| Last | Generate | skill-creator | 0 |

## Skill Generation (when not found)

If skill not found anywhere, use skill-creator:

```bash
# Read skill-creator instructions
Read(".claude/skills/skill-creator/SKILL.md")

# Generate new skill with structure:
.claude/skills/${skillName}/
├── SKILL.md          # Main skill file (required)
├── patterns/         # Implementation patterns
│   └── ${pattern}.md
└── references/       # Reference materials
    └── ${ref}.md
```

**SKILL.md format:**
```yaml
---
name: skill-name
description: What this skill does and when to use it.
---

# Skill Name

## Instructions
Step-by-step guidance for using this skill.

## Patterns
Common implementation patterns.

## Examples
Concrete code examples.
```

## Output Format

```
═══════════════════════════════════════════════════════════════
Skills Acquisition Complete
═══════════════════════════════════════════════════════════════

Identified: 6 skills needed
Searched: aitmpl.com (found 3), web (found 2)

Results:
  ✅ nextjs-patterns     [aitmpl.com] Score: 85
  ✅ prisma-modeling     [aitmpl.com] Score: 80
  ✅ stripe-integration  [aitmpl.com] Score: 78
  ✅ jwt-auth            [github] Score: 72
  ✅ zod-validation      [npm] Score: 68
  ✨ error-handling      [generated]

Files Created:
  .claude/skills/nextjs-patterns/SKILL.md
  .claude/skills/prisma-modeling/SKILL.md
  .claude/skills/stripe-integration/SKILL.md
  .claude/skills/jwt-auth/SKILL.md
  .claude/skills/zod-validation/SKILL.md
  .claude/skills/error-handling/SKILL.md

═══════════════════════════════════════════════════════════════
```
