# Feature List Format (features.json)

Schema and guidelines for the `docs/features.json` file used to track implementation progress.

## Schema

```json
{
  "project": {
    "name": "string",
    "generatedAt": "ISO 8601 datetime",
    "techStack": ["string"]
  },
  "features": [
    {
      "id": "F-NNN",
      "name": "string",
      "description": "string",
      "status": "pending | in_progress | completed | failed",
      "priority": "critical | high | medium | low",
      "tasks": ["T-XXX-NNN"],
      "dependencies": ["F-NNN"],
      "notes": "string"
    }
  ],
  "summary": {
    "total": "number",
    "pending": "number",
    "in_progress": "number",
    "completed": "number",
    "failed": "number"
  }
}
```

## Status Values

| Status | Description | When to Use |
|--------|-------------|-------------|
| `pending` | Not started | Initial state for all features |
| `in_progress` | Currently being implemented | When work begins on a feature |
| `completed` | Successfully implemented and tested | When feature passes all tests |
| `failed` | Implementation blocked or failed | When feature cannot be completed |

## Priority Values

| Priority | Description | Examples |
|----------|-------------|----------|
| `critical` | Must be done first, blocks everything | Core infrastructure, auth |
| `high` | Important for MVP | Primary user flows |
| `medium` | Should be done but not blocking | Secondary features |
| `low` | Nice to have | Polish, optimizations |

## Feature ID Convention

```
F-{category}-{number}
```

| Category | Prefix | Description |
|----------|--------|-------------|
| Core | F-CORE-* | Infrastructure, setup |
| Auth | F-AUTH-* | Authentication, authorization |
| API | F-API-* | API endpoints |
| UI | F-UI-* | User interface components |
| Data | F-DATA-* | Data models, database |
| Int | F-INT-* | Integrations, external services |

## Example: E-commerce Project

```json
{
  "project": {
    "name": "e-commerce-store",
    "generatedAt": "2025-01-15T10:30:00Z",
    "techStack": ["Next.js", "TypeScript", "Prisma", "PostgreSQL", "Stripe"]
  },
  "features": [
    {
      "id": "F-CORE-001",
      "name": "Project Setup",
      "description": "Initialize Next.js project with TypeScript, ESLint, Prettier",
      "status": "completed",
      "priority": "critical",
      "tasks": ["T-AUTO-001", "T-AUTO-002"],
      "dependencies": [],
      "notes": "Using Next.js 14 with App Router"
    },
    {
      "id": "F-DATA-001",
      "name": "Database Schema",
      "description": "Define Prisma schema for products, users, orders",
      "status": "completed",
      "priority": "critical",
      "tasks": ["T-AUTO-003", "T-AUTO-004", "T-AUTO-005"],
      "dependencies": ["F-CORE-001"],
      "notes": ""
    },
    {
      "id": "F-AUTH-001",
      "name": "User Authentication",
      "description": "Implement sign up, sign in, sign out with NextAuth.js",
      "status": "in_progress",
      "priority": "high",
      "tasks": ["T-AUTO-010", "T-AUTO-011", "T-AUTO-012"],
      "dependencies": ["F-DATA-001"],
      "notes": "Using credentials provider for MVP"
    },
    {
      "id": "F-UI-001",
      "name": "Product Catalog",
      "description": "Display products with filtering and pagination",
      "status": "pending",
      "priority": "high",
      "tasks": ["T-AUTO-020", "T-AUTO-021"],
      "dependencies": ["F-DATA-001"],
      "notes": ""
    },
    {
      "id": "F-INT-001",
      "name": "Stripe Integration",
      "description": "Payment processing with Stripe Checkout",
      "status": "pending",
      "priority": "high",
      "tasks": ["T-AUTO-030", "T-AUTO-031", "T-AUTO-032"],
      "dependencies": ["F-AUTH-001", "F-UI-001"],
      "notes": "Using Stripe Checkout for simplicity"
    }
  ],
  "summary": {
    "total": 5,
    "pending": 2,
    "in_progress": 1,
    "completed": 2,
    "failed": 0
  }
}
```

## Granularity Guidelines

### Small Projects (< 10 features)
- One feature per endpoint or component
- Fine-grained tracking
- Example: "Implement POST /users", "Create UserCard component"

### Medium Projects (10-50 features)
- Group related functionality
- One feature per functional area
- Example: "User Authentication", "Product Management"

### Large Projects (50+ features)
- High-level feature groups
- Use subtasks for detailed tracking
- Example: "E-commerce Cart System" with multiple tasks

## Linking to TASKS.md

Features link to tasks via the `tasks` array:

```json
{
  "id": "F-AUTH-001",
  "tasks": ["T-AUTO-010", "T-AUTO-011", "T-AUTO-012"]
}
```

These task IDs correspond to entries in `docs/TASKS.md`:

```markdown
### T-AUTO-010: Implement sign up endpoint
- [ ] Create POST /auth/signup route
- [ ] Add input validation
- [ ] Hash password with bcrypt
- Depends: T-AUTO-003 (User model)
```

## Updating Summary

Always keep the `summary` section in sync when changing feature status:

```typescript
// After updating a feature status
const features = JSON.parse(fs.readFileSync('docs/features.json'))

features.summary = {
  total: features.features.length,
  pending: features.features.filter(f => f.status === 'pending').length,
  in_progress: features.features.filter(f => f.status === 'in_progress').length,
  completed: features.features.filter(f => f.status === 'completed').length,
  failed: features.features.filter(f => f.status === 'failed').length
}

fs.writeFileSync('docs/features.json', JSON.stringify(features, null, 2))
```
