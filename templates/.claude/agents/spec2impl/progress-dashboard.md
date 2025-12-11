---
name: progress-dashboard
description: Display visual progress dashboard. Mode workflow for spec2impl steps (12 steps), mode tasks for implementation progress from TASKS.md.
model: haiku
tools: Read, Glob, Grep
---

# Progress Dashboard

Display visual progress for spec2impl or implementation tasks.

## Modes

### Workflow Mode (spec2impl execution - 12 steps)

```
════════════════════════════════════════════════════════════════════════════════
  spec2impl Progress
════════════════════════════════════════════════════════════════════════════════

[████████░░░░░░░░░░░░░░░░░░░░░░]  25% (3/12 steps)

Step  1: Specification Analysis     ✅ Complete
Step  2: Tech Stack Expansion       ✅ Complete
Step  3: Skills Acquisition         ✅ Complete
Step  4: Agents Acquisition         🔄 In Progress
Step  5: Commands Acquisition       ⏳ Pending
Step  6: MCP Configuration          ⏳ Pending
Step  7: Settings Configuration     ⏳ Pending
Step  8: Deploy Bundled             ⏳ Pending
Step  9: Task List Generation       ⏳ Pending
Step 10: CLAUDE.md Update           ⏳ Pending
Step 11: Harness Guide Generation   ⏳ Pending
Step 12: Cleanup                    ⏳ Pending

Current: Downloading agents from aitmpl.com
════════════════════════════════════════════════════════════════════════════════
```

### Step Names Reference

| Step | Name | Agent |
|------|------|-------|
| 1 | Specification Analysis | spec-analyzer |
| 2 | Tech Stack Expansion | tech-stack-expander |
| 3 | Skills Acquisition | category-downloader (skills) |
| 4 | Agents Acquisition | category-downloader (agents) |
| 5 | Commands Acquisition | category-downloader (commands) |
| 6 | MCP Configuration (3-Layer) | category-downloader (mcps) |
| 7 | Settings Configuration | category-downloader (settings) |
| 8 | Deploy Bundled | (direct copy) |
| 9 | Task List Generation | task-list-generator |
| 10 | CLAUDE.md Update | claude-md-updater |
| 11 | Harness Guide Generation | harness-guide-generator |
| 12 | Cleanup | (optional) |

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
