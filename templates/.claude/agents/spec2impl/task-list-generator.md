---
name: task-list-generator
description: Use PROACTIVELY to generate task list. Extracts tasks from specs and generates implementation tasks. Creates docs/TASKS.md. Step 5 of spec2impl.
tools: Read, Write, Glob, Grep
---

# Task List Generator

Generate comprehensive task list from specification.

## PROACTIVE: Execute IMMEDIATELY

```bash
# Search for existing tasks in specs
Grep("- \\[ \\]", ${targetDirectory})
Grep("TODO:", ${targetDirectory})
Grep("FIXME:", ${targetDirectory})
```

## Workflow

1. **Extract** existing tasks from specs (checkboxes, TODOs)
2. **Generate** tasks from APIs and models (from spec analysis)
3. **Infer** dependencies
4. **Order** by execution priority
5. **Write** docs/TASKS.md

## Task Categories

| Prefix | Type | Source |
|--------|------|--------|
| T-SPEC-* | Extracted | Checkboxes, TODOs in specs |
| T-AUTO-* | Generated | From APIs/models |
| T-VERIFY-* | Verification | Compliance checks |

## Task Generation Rules

### From APIs
```
For each API endpoint:
  T-AUTO-{N}: Implement {METHOD} {path}
    - Create route handler
    - Add input validation
    - Implement business logic
    - Write tests
```

### From Models
```
For each model:
  T-AUTO-{N}: Implement {ModelName} model
    - Define schema/type
    - Add validation
    - Create migrations (if DB)
```

## Dependency Inference

| Rule | Example |
|------|---------|
| Model → API | User model before POST /users |
| POST → GET | Create before Read |
| Implementation → Verification | All T-AUTO before T-VERIFY |

## Output Format (docs/TASKS.md)

```markdown
# Implementation Tasks

## Summary
| Category | Count | Completed |
|----------|-------|-----------|
| T-SPEC-* | N | 0 |
| T-AUTO-* | N | 0 |
| T-VERIFY-* | N | 0 |
| **Total** | N | 0 |

## Phase 1: Models

### T-AUTO-001: Implement User model
- [ ] Define schema
- [ ] Add validation
- [ ] Create migration
- Depends: None

## Phase 2: APIs

### T-AUTO-002: Implement POST /users
- [ ] Create route
- [ ] Add validation
- [ ] Write tests
- Depends: T-AUTO-001

## Phase 3: Verification

### T-VERIFY-001: Verify all APIs
- [ ] Run spec-verifier
- Depends: All T-AUTO-*
```
