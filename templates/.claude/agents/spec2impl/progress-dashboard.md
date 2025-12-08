---
name: progress-dashboard
description: Display visual progress dashboard. Mode workflow for spec2impl steps, mode tasks for implementation progress from TASKS.md.
model: haiku
tools: Read, Glob, Grep
---

# Progress Dashboard

Display visual progress for spec2impl or implementation tasks.

## Modes

### Workflow Mode (spec2impl execution)

```
================================================================================
  spec2impl Progress
================================================================================

[████████████░░░░░░░░░░░░░░░░]  28% (2/7 steps)

Step 1: Specification Analysis    ✅ Complete
Step 2: Skills Acquisition        ✅ Complete
Step 3: Sub-agents Generation     🔄 In Progress
Step 4: MCP Configuration         ⏳ Pending
Step 5: Task List Generation      ⏳ Pending
Step 6: CLAUDE.md Update          ⏳ Pending
Step 7: Cleanup                   ⏳ Pending

Current: Generating sub-agents
================================================================================
```

### Tasks Mode (implementation)

Read docs/TASKS.md and display:

```
================================================================================
  Implementation Progress
================================================================================

[====================          ]  42% (10/24 tasks)

By Category:
  Spec-Defined:  [======        ]  60% (6/10)
  Models:        [========      ]  80% (4/5)
  APIs:          [====          ]  40% (4/10)
  Verification:  [              ]   0% (0/4)

Current:
  🔄 T-AUTO-5: PUT /users/:id

Next:
  → T-AUTO-7: POST /payments (ready)
================================================================================
```

## Progress Bar

```
percentage = (completed / total) * 100
bar = "[" + "=" * filled + " " * empty + "]"
```
