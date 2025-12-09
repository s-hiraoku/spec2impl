---
name: progress-dashboard
description: Display visual progress dashboard. Mode workflow for spec2impl steps (10 steps), mode tasks for implementation progress from TASKS.md.
model: haiku
tools: Read, Glob, Grep
---

# Progress Dashboard

Display visual progress for spec2impl or implementation tasks.

## Modes

### Workflow Mode (spec2impl execution - 10 steps)

```
════════════════════════════════════════════════════════════════════════════════
  spec2impl Progress
════════════════════════════════════════════════════════════════════════════════

[████████░░░░░░░░░░░░░░░░░░░░░░]  30% (3/10 steps)

Step  1: Specification Analysis     ✅ Complete
Step  2: Skills Acquisition         ✅ Complete
Step  3: Agents Acquisition         ✅ Complete
Step  4: Commands Acquisition       🔄 In Progress
Step  5: MCP Configuration          ⏳ Pending
Step  6: Settings Configuration     ⏳ Pending
Step  7: Deploy Bundled             ⏳ Pending
Step  8: Task List Generation       ⏳ Pending
Step  9: CLAUDE.md Update           ⏳ Pending
Step 10: Cleanup                    ⏳ Pending

Current: Downloading commands from aitmpl.com
════════════════════════════════════════════════════════════════════════════════
```

### Step Names Reference

| Step | Name | Agent |
|------|------|-------|
| 1 | Specification Analysis | spec-analyzer |
| 2 | Skills Acquisition | category-downloader (skills) |
| 3 | Agents Acquisition | category-downloader (agents) |
| 4 | Commands Acquisition | category-downloader (commands) |
| 5 | MCP Configuration | category-downloader (mcps) |
| 6 | Settings Configuration | category-downloader (settings) |
| 7 | Deploy Bundled | (direct copy) |
| 8 | Task List Generation | task-list-generator |
| 9 | CLAUDE.md Update | claude-md-updater |
| 10 | Cleanup | (optional) |

### Tasks Mode (implementation)

Read docs/TASKS.md and display:

```
════════════════════════════════════════════════════════════════════════════════
  Implementation Progress
════════════════════════════════════════════════════════════════════════════════

[████████████████░░░░░░░░░░░░░░]  42% (10/24 tasks)

By Category:
  Spec-Defined:  [████████████░░░░░░░░]  60% (6/10)
  Models:        [████████████████░░░░]  80% (4/5)
  APIs:          [████████░░░░░░░░░░░░]  40% (4/10)
  Verification:  [░░░░░░░░░░░░░░░░░░░░]   0% (0/4)

Current:
  🔄 T-AUTO-5: PUT /users/:id

Next:
  → T-AUTO-7: POST /payments (ready)
════════════════════════════════════════════════════════════════════════════════
```

## Progress Bar Generation

```
percentage = (completed / total) * 100
bar_length = 30
filled = round(percentage / 100 * bar_length)
empty = bar_length - filled
bar = "[" + "█" * filled + "░" * empty + "]"
```

## Status Icons

| Status | Icon |
|--------|------|
| Complete | ✅ |
| In Progress | 🔄 |
| Pending | ⏳ |
| Skipped | ⏭️ |
| Error | ❌ |
