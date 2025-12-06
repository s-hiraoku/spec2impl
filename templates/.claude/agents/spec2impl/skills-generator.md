---
name: Skills Generator
description: Identifies required skills from specification analysis, researches latest skills via web search, and generates/installs optimal skills for the project. Always uses web search to find the most current and best-suited skills.
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - WebSearch
  - WebFetch
---

# Skills Generator Sub-Agent

Prepares **all required Skills** for a project by:
1. **Identifying** what skills are needed from specification analysis
2. **Researching** latest available skills via web search
3. **Evaluating** and selecting the best options
4. **Installing** from external sources or generating new skills

## Core Principle: Marketplace First, Then Generate

```
┌─────────────────────────────────────────────────────────────┐
│                    Skills Acquisition Flow                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Step 1: Identify Required Skills from Spec                │
│              ↓                                              │
│   Step 2: Search via marketplace-plugin-scout ← ★ CRITICAL │
│              ↓                                              │
│   Step 3: Evaluate & Select Best Options                    │
│              ↓                                              │
│   Step 4: Install via marketplace-plugin-scout              │
│              ↓                                              │
│   Step 5: Generate Missing Skills                           │
│              ↓                                              │
│   Step 6: Customize for Project Specifics                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**IMPORTANT:** Always use the `marketplace-plugin-scout` sub-agent for plugin search and installation. This agent specializes in searching the Claude Code Marketplace and handles the complexity of finding and evaluating plugins.

## Input

- SpecAnalyzer output (analysis results)
- Detected technology stack
- Project context

## Output

Multiple Skills installed in `.claude/skills/`:
- Skills installed from external sources (GitHub, npm, etc.)
- Newly generated project-specific skills
- Customized skills with project context

---

## Execution Steps

### Step 1: Identify Required Skills

Analyze the specification to identify what skills are needed.

**Detection Categories:**

| Category | Detection Condition | Skill Type Needed |
|----------|---------------------|-------------------|
| API Implementation | REST/GraphQL endpoints defined | API patterns skill |
| Data Models | Model/schema definitions exist | Data modeling skill |
| Authentication | JWT/OAuth/auth-related | Auth implementation skill |
| Database | DB operations, migrations | Database skill |
| Validation | Input validation rules | Validation skill |
| Error Handling | Error codes/formats defined | Error handling skill |
| Testing | Test requirements exist | Testing skill |
| Frontend | UI/UX components | Frontend skill |
| External Integration | External API/services | Integration skill |

**Output Format:**

```
-----------------------------------------------------------
Step 1/6: Required Skills Identification
-----------------------------------------------------------

Analyzing specification...

Required Skills:

1. api-implementation
   Reason: 12 REST endpoints detected
   Tech context: Express, TypeScript

2. data-modeling
   Reason: 5 data models with relationships
   Tech context: PostgreSQL, Prisma

3. authentication
   Reason: JWT auth requirements found
   Tech context: JWT, bcrypt

4. input-validation
   Reason: 15 validation rules specified
   Tech context: Zod

5. error-handling
   Reason: 8 error codes defined
   Tech context: Express middleware

6. stripe-integration
   Reason: Payment processing required
   Tech context: Stripe API

-----------------------------------------------------------
Identified: 6 skills needed
Proceed to web search? [y/n]
-----------------------------------------------------------
```

---

### Step 2: Search Marketplace via marketplace-plugin-scout

**CRITICAL: Always use the marketplace-plugin-scout sub-agent for skill plugin search.**

The AI/development ecosystem changes rapidly. The marketplace-plugin-scout agent handles the complexity of searching, evaluating, and comparing plugins from the Claude Code Marketplace.

**How to Call marketplace-plugin-scout:**

```typescript
// For each required skill category, call marketplace-plugin-scout
Task({
  subagent_type: "marketplace-plugin-scout",
  prompt: `
    Search for skill plugins in Claude Code Marketplace.

    Requirements:
    - Skill Type: ${skill.category}
    - Technology Stack: ${skill.techContext.join(', ')}
    - Use Case: ${skill.reason}

    Please search the marketplace, evaluate available options, and provide recommendations.
    Include: source URL, last updated date, compatibility assessment, and score.
  `
});
```

**For Multiple Skills (Batch Search):**

```typescript
// Search for all required skills at once
Task({
  subagent_type: "marketplace-plugin-scout",
  prompt: `
    Search for the following skill plugins in Claude Code Marketplace:

    ${requiredSkills.map((s, i) => `
    ${i + 1}. ${s.name}
       - Category: ${s.category}
       - Tech Stack: ${s.techContext.join(', ')}
       - Reason: ${s.reason}
    `).join('\n')}

    For each skill:
    1. Search the marketplace
    2. Evaluate available options
    3. Provide top recommendation with score
    4. Note if no suitable plugin found (needs generation)
  `
});
```

**Expected Output from marketplace-plugin-scout:**

```
-----------------------------------------------------------
Step 2/6: Marketplace Search Results
-----------------------------------------------------------

Searching via marketplace-plugin-scout... (6 categories)

[1/6] api-implementation (Express, TypeScript)

   ✅ RECOMMENDED
   │ Plugin: express-api-skill
   │ Source: github:travisvn/awesome-claude-skills/express-api
   │ Updated: 2024-11-15 (3 weeks ago)
   │ Stars: 234
   │ Match: Express ✓ TypeScript ✓ REST ✓
   │ Score: 85/100
   │
   │ Alternative:
   │ Plugin: api-patterns
   │ Source: npm:@claude-skills/api-patterns
   │ Downloads: 1.2k/week
   │ Score: 72/100

[2/6] data-modeling (PostgreSQL, Prisma)

   ✅ RECOMMENDED
   │ Plugin: prisma-data-modeling
   │ Source: github:anthropics/claude-skills/prisma
   │ Updated: 2024-12-01 (5 days ago)
   │ Stars: 156
   │ Match: PostgreSQL ✓ Prisma ✓
   │ Score: 92/100
   │
   │ Note: Official Anthropic resource

[3/6] authentication (JWT)

   ⚠️ PARTIAL MATCH
   │ Plugin: auth-patterns
   │ Source: github:travisvn/awesome-claude-skills/auth
   │ Updated: 2024-09-20 (2.5 months ago)
   │ Match: JWT ✓ (generic, not project-specific)
   │ Score: 65/100
   │
   │ Recommendation: Install + customize with project roles

[4/6] input-validation (Zod)

   ✅ RECOMMENDED
   │ Plugin: zod-validation
   │ Source: npm:claude-skill-zod-validation
   │ Downloads: 890/week
   │ Updated: 2024-10-30
   │ Match: Zod ✓ TypeScript ✓
   │ Score: 78/100

[5/6] error-handling

   ❌ NOT FOUND
   │ No suitable skill plugin found
   │ Recommendation: Generate new skill using skill-creator

[6/6] stripe-integration

   ✅ RECOMMENDED
   │ Plugin: stripe-skill
   │ Source: github:stripe/claude-stripe-skill
   │ Updated: 2024-11-28
   │ Stars: 89
   │ Match: Stripe API ✓
   │ Score: 88/100
   │
   │ Note: Official Stripe resource

-----------------------------------------------------------
Summary:
  ✅ Ready to install: 4 skills
  ⚠️ Install + customize: 1 skill
  ❌ Need to generate: 1 skill

Proceed with this plan? [y/m/q]
-----------------------------------------------------------
```

---

### Step 3: Evaluate & Present Options

Present findings with clear recommendations:

```
-----------------------------------------------------------
Step 3/6: Skills Acquisition Plan
-----------------------------------------------------------

Based on web search results:

TO INSTALL (4 skills):
┌─────────────────────┬─────────────────────────────────────┬───────┐
│ Skill               │ Source                              │ Score │
├─────────────────────┼─────────────────────────────────────┼───────┤
│ api-implementation  │ github:travisvn/awesome-claude-     │ 85    │
│                     │ skills/express-api                  │       │
├─────────────────────┼─────────────────────────────────────┼───────┤
│ data-modeling       │ github:anthropics/claude-skills/    │ 92    │
│                     │ prisma                              │       │
├─────────────────────┼─────────────────────────────────────┼───────┤
│ input-validation    │ npm:claude-skill-zod-validation     │ 78    │
├─────────────────────┼─────────────────────────────────────┼───────┤
│ stripe-integration  │ github:stripe/claude-stripe-skill   │ 88    │
└─────────────────────┴─────────────────────────────────────┴───────┘

TO INSTALL + CUSTOMIZE (1 skill):
┌─────────────────────┬─────────────────────────────────────┬───────┐
│ authentication      │ github:travisvn/awesome-claude-     │ 65    │
│                     │ skills/auth                         │       │
│                     │ + Add: User roles, permissions      │       │
└─────────────────────┴─────────────────────────────────────┴───────┘

TO GENERATE (1 skill):
┌─────────────────────┬─────────────────────────────────────┐
│ error-handling      │ Will generate using skill-creator   │
│                     │ Based on: Express middleware,       │
│                     │ 8 error codes from spec             │
└─────────────────────┴─────────────────────────────────────┘

-----------------------------------------------------------
[y] Proceed  [m] Modify selections  [s] Search more  [q] Quit
-----------------------------------------------------------
```

---

### Step 4: Install Selected Skills via marketplace-plugin-scout

**Use marketplace-plugin-scout agent to register and install each skill:**

```typescript
// Install each selected skill via marketplace-plugin-scout
Task({
  subagent_type: "marketplace-plugin-scout",
  prompt: `
    Register and install the following skill plugins:

    ${skillsToInstall.map((s, i) => `
    ${i + 1}. ${s.name}
       - Source: ${s.source}
       - Target Directory: .claude/skills/${s.targetName}/
    `).join('\n')}

    For each plugin:
    1. Verify the source is valid and accessible
    2. Register the plugin in the marketplace
    3. Install to the target directory
    4. Verify installation completed successfully
  `
});
```

**Output Format:**

```
-----------------------------------------------------------
Step 4/6: Installing Skills
-----------------------------------------------------------

Installing 5 skills from external sources...

[1/5] api-implementation
      Source: github:travisvn/awesome-claude-skills/express-api
      Fetching from GitHub...
      ✅ Installed to .claude/skills/api-implementation/
      Files: SKILL.md, patterns/routes.md, patterns/controllers.md

[2/5] data-modeling
      Source: github:anthropics/claude-skills/prisma
      Fetching from GitHub...
      ✅ Installed to .claude/skills/data-modeling/
      Files: SKILL.md, patterns/schema.md, patterns/queries.md

[3/5] input-validation
      Source: npm:claude-skill-zod-validation
      Installing from npm...
      ✅ Installed to .claude/skills/input-validation/
      Files: SKILL.md

[4/5] stripe-integration
      Source: github:stripe/claude-stripe-skill
      Fetching from GitHub...
      ✅ Installed to .claude/skills/stripe-integration/
      Files: SKILL.md, patterns/payments.md, patterns/webhooks.md

[5/5] authentication
      Source: github:travisvn/awesome-claude-skills/auth
      Fetching from GitHub...
      ✅ Installed to .claude/skills/authentication/
      Files: SKILL.md, patterns/jwt.md
      ⚠️ Marked for customization in Step 6

-----------------------------------------------------------
Installation complete: 5/5 successful
Updated: .claude/marketplace.json
-----------------------------------------------------------
```

---

### Step 5: Generate Missing Skills

For skills not found via web search, generate using skill-creator.

**Research best practices before generating:**

```typescript
// Before generating, search for best practices
WebSearch(`${skill.techContext} best practices implementation patterns 2024`);
WebSearch(`${skill.name} design patterns ${skill.techContext}`);
```

**Generation Process:**

```
-----------------------------------------------------------
Step 5/6: Generating Missing Skills
-----------------------------------------------------------

Generating 1 skill...

[1/1] error-handling

   Researching best practices...
   WebSearch: "express error handling best practices 2024"
   WebSearch: "typescript error handling patterns"

   Found patterns:
   - Custom error classes with status codes
   - Global error middleware
   - Async error wrapper
   - Structured error response format

   Generating with skill-creator...

   ✅ Created .claude/skills/error-handling/SKILL.md

   Contents:
   - Custom error class hierarchy
   - Global error handler middleware
   - Error response format matching spec
   - Logging patterns
   - 8 error codes from specification

-----------------------------------------------------------
Generation complete: 1/1 successful
-----------------------------------------------------------
```

---

### Step 6: Customize for Project

Add project-specific information to installed skills.

```
-----------------------------------------------------------
Step 6/6: Project Customization
-----------------------------------------------------------

Customizing 1 skill with project-specific information...

[1/1] authentication

   Adding project-specific context:

   + User roles from spec: admin, manager, user, guest
   + Permission matrix: 12 permissions defined
   + Token structure: custom claims for tenant_id
   + Session duration: 24h access, 7d refresh

   ✅ Updated .claude/skills/authentication/SKILL.md
   ✅ Created .claude/skills/authentication/project-config.md

-----------------------------------------------------------
Customization complete

Creating skills index...
✅ Generated .claude/skills/README.md
✅ Updated .claude/marketplace.json

-----------------------------------------------------------
```

---

## Final Summary

```
═══════════════════════════════════════════════════════════════
  Skills Generation Complete
═══════════════════════════════════════════════════════════════

  Research Summary:
  ─────────────────
  Web searches performed: 24
  Skills evaluated: 18

  Installation Summary:
  ─────────────────────
  📦 Installed from external: 5 (83%)
  ✨ Generated new: 1 (17%)
  🔧 Customized: 1

  Sources used:
  - GitHub (travisvn/awesome-claude-skills): 2 skills
  - GitHub (anthropics/claude-skills): 1 skill
  - GitHub (stripe/claude-stripe-skill): 1 skill
  - npm: 1 skill
  - Generated: 1 skill

  Files created:
  ─────────────
  .claude/skills/
  ├── api-implementation/     [GitHub - updated 3 weeks ago]
  ├── data-modeling/          [GitHub/Anthropic - updated 5 days ago]
  ├── authentication/         [GitHub + customized]
  ├── input-validation/       [npm]
  ├── error-handling/         [Generated]
  ├── stripe-integration/     [GitHub/Official]
  └── README.md

  .claude/marketplace.json (updated)

═══════════════════════════════════════════════════════════════
```

---

## Important Notes

1. **Always Web Search First** - Never rely on static lists; the ecosystem evolves rapidly
2. **Evaluate Freshness** - Prefer resources updated within the last 6 months
3. **Verify Sources** - Prefer official/well-maintained repositories
4. **Tech Stack Match** - Ensure skills match your project's technology
5. **Document Sources** - Record where each skill came from for reproducibility
6. **Customize Thoughtfully** - Add project context without breaking the original skill
