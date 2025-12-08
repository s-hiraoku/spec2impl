---
name: claude-md-updater
description: Use PROACTIVELY to update CLAUDE.md. Merges spec2impl section with existing content. Step 6 of spec2impl.
tools: Read, Write, Edit, Glob
---

# CLAUDE.md Updater

Update CLAUDE.md with implementation environment section.

## PROACTIVE: Execute IMMEDIATELY

```bash
# Check if CLAUDE.md exists
Glob("CLAUDE.md")

# Read existing content
Read("CLAUDE.md")

# Generate and write spec2impl section
```

## Workflow

1. **Check** if CLAUDE.md exists
2. **Read** existing content (preserve user sections)
3. **Generate** spec2impl section
4. **Merge** without overwriting user content
5. **Write** updated CLAUDE.md

## Section Format

```markdown
<!-- spec2impl generated section - DO NOT EDIT MANUALLY -->

## Implementation Environment

### Skills
- skill-name: description

### Agents
- agent-name: description

### MCPs
- mcp-name: description

### Tasks
See docs/TASKS.md

<!-- end spec2impl generated section -->
```

## Merge Rules

- Preserve all existing sections
- Add/update only between spec2impl markers
- Never delete user-defined content
