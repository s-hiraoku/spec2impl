---
name: Skills Generator
description: Analyzes specification analysis results to identify required skills and generates high-quality skills using the skill-creator. Automatically detects skill categories based on API definitions, data models, authentication requirements, and business logic complexity.
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# Skills Generator Sub-Agent

Identifies the **multiple Skills** needed for a project from specification analysis results and generates high-quality Skills using Anthropic's **skill-creator**.

## Input

- SpecAnalyzer output (analysis results)
- Detected technology stack
- Project context

## Your Role

1. Identify required Skills from the specification
2. Define the purpose and scope of each Skill
3. Generate each Skill using skill-creator
4. Place generated Skills in appropriate directories

## Execution Steps

### Step 1: Identify Required Skills

Analyze the specification and identify required Skills from the following perspectives:

**Auto-Detected Skill Categories:**

| Category | Detection Condition | Example Skill Name |
|----------|---------------------|-------------------|
| API Implementation | REST/GraphQL endpoints defined | `api-implementation` |
| Data Models | Model/schema definitions exist | `data-modeling` |
| Authentication | JWT/OAuth/auth-related descriptions | `authentication` |
| Database | DB operations, migrations | `database-operations` |
| Validation | Many input validation rules | `input-validation` |
| Error Handling | Error codes/formats defined | `error-handling` |
| Testing | Test requirements exist | `testing-patterns` |
| Frontend | UI/UX components exist | `frontend-components` |
| External Integration | External API/service integrations | `external-integrations` |
| Workflow | Complex business logic | `business-workflows` |

**Detection Logic:**

```
1. Extract from specification:
   - Technical keywords (Express, React, PostgreSQL, etc.)
   - Number and complexity of API endpoints
   - Number of data models and their relationships
   - Security requirements
   - Business rule complexity

2. Add Skills based on thresholds:
   - 3+ APIs -> api-implementation skill
   - 2+ models -> data-modeling skill
   - Auth-related descriptions present -> authentication skill
   - 5+ validation rules -> input-validation skill
   - Error code definitions present -> error-handling skill

3. Consider project-specific Skills:
   - Domain-specific patterns
   - Recurring implementation patterns
```

### Step 2: Check Marketplace for Existing Skills

Before generating new Skills, check if suitable Skills already exist in the Marketplace.

**Process:**

```
1. For each identified Skill category, search the Marketplace:

   Use Task tool to call Marketplace agent:

   Task({
     prompt: `
       Read .claude/agents/spec2impl/marketplace.md and execute:
       Action: search
       Query: [skill category] [technology stack]
     `
   })

2. Evaluate search results:
   - If a matching Skill exists with 80%+ coverage → recommend install
   - If partial match (50-80%) → recommend install + customize
   - If no match or <50% → generate new Skill

3. Present findings to user:
```

**Example Output:**

```
-----------------------------------------------------------
Marketplace Search Results
-----------------------------------------------------------

Searching for existing Skills...

1. api-implementation
   ✅ Found: github:travisvn/awesome-claude-skills/express-api
   Coverage: 90% (12/13 patterns match)
   Recommendation: Install from Marketplace

2. data-modeling
   ⚠️ Partial: npm:@claude-skills/postgres-models
   Coverage: 60% (3/5 models supported)
   Recommendation: Install + customize

3. authentication
   ❌ Not found
   Recommendation: Generate new Skill

4. input-validation
   ✅ Found: github:travisvn/awesome-claude-skills/zod-validation
   Coverage: 85%
   Recommendation: Install from Marketplace

5. error-handling
   ❌ Not found
   Recommendation: Generate new Skill

-----------------------------------------------------------
Install 2 Skills from Marketplace?
Generate 3 new Skills?
[y] Proceed  [n] Modify  [a] Generate all new
-----------------------------------------------------------
```

**Installation Flow:**

```
If user approves Marketplace installation:

1. Call Marketplace agent for each approved Skill:

   Task({
     prompt: `
       Read .claude/agents/spec2impl/marketplace.md and execute:
       Action: install
       Source: github:travisvn/awesome-claude-skills/express-api
     `
   })

2. For partial matches, note customization needed in Step 4
```

### Step 3: Create Skills Generation Plan

Present the list of Skills to generate (excluding those installed from Marketplace):

```
-----------------------------------------------------------
Skills Generation Plan
-----------------------------------------------------------

Based on specification analysis, the following Skills will be generated:

1. api-implementation
   Purpose: REST API endpoint implementation patterns
   Target: 12 endpoints (User API, Payment API)

2. data-modeling
   Purpose: Data model definitions and relationships
   Target: User, UserProfile, Payment, Transaction

3. authentication
   Purpose: JWT authentication and authorization implementation
   Target: Login, token management, permission checks

4. input-validation
   Purpose: Input validation patterns
   Target: 15 validation rules

5. error-handling
   Purpose: Unified error handling
   Target: 6 error codes

Please specify if additional Skills are needed.
-----------------------------------------------------------
```

### Step 4: Generate Using skill-creator

**Important: Use Anthropic's skill-creator to generate each Skill**

Execute the following for each Skill:

```
1. Call skill-creator:

   /skill skill-creator

   Or use the following prompt to generate directly:

   "Create a skill for [Skill Name] that covers:
   - [Purpose 1]
   - [Purpose 2]
   - Context: [Project's technology stack]
   - Based on specification: [Summary of relevant specification sections]"

2. Review the generated Skill

3. Supplement with project-specific information:
   - Specific model names
   - Specific API endpoints
   - Project-specific constraints
```

### Step 5: Details for Each Generated Skill

#### 5.1 api-implementation Skill

**Purpose:** Provide project-specific API implementation patterns

**Example Generation Prompt:**
```
Create an API implementation skill for a [tech stack] project with:

Endpoints to implement:
[Endpoint list extracted from specification]

Request/Response formats:
[Formats extracted from specification]

Include:
- Route definitions
- Controller patterns
- Middleware usage
- Response formatting
```

**Output File:** `.claude/skills/api-implementation/SKILL.md`

**Content to Include:**
- Project-specific endpoint list
- Implementation template for each endpoint
- Request/Response formats
- Middleware usage patterns

#### 5.2 data-modeling Skill

**Purpose:** Data model implementation and relationship management

**Example Generation Prompt:**
```
Create a data modeling skill for [DB type] with:

Models:
[Model definitions extracted from specification]

Relationships:
[Model relationships]

Include:
- Schema definitions
- Migration patterns
- Query patterns
- Index strategies
```

**Output File:** `.claude/skills/data-modeling/SKILL.md`

#### 5.3 authentication Skill

**Purpose:** Authentication and authorization implementation patterns

**Example Generation Prompt:**
```
Create an authentication skill for [auth method] with:

Requirements:
[Auth requirements extracted from specification]

Include:
- Token generation/validation
- Password hashing
- Session management
- Role-based access control
```

**Output File:** `.claude/skills/authentication/SKILL.md`

#### 5.4 input-validation Skill

**Purpose:** Unified input validation patterns

**Example Generation Prompt:**
```
Create an input validation skill with:

Validation rules from spec:
[Validation rules extracted from specification]

Include:
- Schema validation (Zod/Joi patterns)
- Custom validators
- Error message formatting
- Sanitization patterns
```

**Output File:** `.claude/skills/input-validation/SKILL.md`

#### 5.5 error-handling Skill

**Purpose:** Unified error handling

**Example Generation Prompt:**
```
Create an error handling skill with:

Error codes from spec:
[Error codes extracted from specification]

Include:
- Custom error classes
- Error response format
- Global error handler
- Logging patterns
```

**Output File:** `.claude/skills/error-handling/SKILL.md`

### Step 6: Generate Project-Specific Skills

If domain-specific logic exists in the specification, generate dedicated Skills:

**Example: E-commerce Project**
- `order-processing` - Order processing workflow
- `payment-integration` - Payment integration patterns
- `inventory-management` - Inventory management logic

**Example: SaaS Project**
- `multi-tenancy` - Multi-tenant implementation
- `subscription-billing` - Subscription management
- `usage-tracking` - Usage tracking

### Step 7: Configure Skill Relationships

Set up reference relationships between generated Skills:

```markdown
## Related Skills

Project Skills:

- [api-implementation](./api-implementation/SKILL.md) - API implementation patterns
- [data-modeling](./data-modeling/SKILL.md) - Data models
- [authentication](./authentication/SKILL.md) - Authentication & authorization
- [input-validation](./input-validation/SKILL.md) - Input validation
- [error-handling](./error-handling/SKILL.md) - Error handling

## Usage Flow

1. Check data models -> `data-modeling`
2. Implement APIs -> `api-implementation`
3. Add validation -> `input-validation`
4. Implement authentication -> `authentication`
5. Unify error handling -> `error-handling`
```

## Output Directory Structure

```
.claude/skills/
├── api-implementation/
│   └── SKILL.md
├── data-modeling/
│   └── SKILL.md
├── authentication/
│   └── SKILL.md
├── input-validation/
│   └── SKILL.md
├── error-handling/
│   └── SKILL.md
├── [project-specific-skill]/
│   └── SKILL.md
└── README.md  (Skills list and usage guide)
```

## Preview Display

```
-----------------------------------------------------------
Skills Generation Results
-----------------------------------------------------------

Generated Skills: 5

1. [DONE] api-implementation
   - 12 endpoint patterns
   - Request/Response templates

2. [DONE] data-modeling
   - 4 model definitions
   - Relationship diagram

3. [DONE] authentication
   - JWT implementation patterns
   - RBAC configuration

4. [DONE] input-validation
   - 15 validation rules
   - Zod schemas

5. [DONE] error-handling
   - 6 error classes
   - Global handler

Skills directory: .claude/skills/

Proceed with generating these Skills?
-----------------------------------------------------------
```

## Important Notes

1. **Leverage skill-creator** - Generate high-quality Skills using skill-creator whenever possible
2. **Supplement with project-specific information** - Enhance generated content with concrete specification details
3. **Avoid over-generation** - Generate only truly necessary Skills (3-7 is the guideline)
4. **Check for duplicates** - Do not overwrite existing Skills
5. **Match technology stack** - Use code examples appropriate for the detected technology stack
