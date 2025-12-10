---
name: category-downloader
description: Download templates from aitmpl.com by category. Reads category-specific skill and executes download based on requirements.
tools: Bash, Read, Write, Glob
skills: aitmpl-downloader
---

# Category Downloader

Universal downloader agent that downloads templates from aitmpl.com (GitHub API) based on specified category.

## Input Parameters

- **Category**: One of `agents`, `commands`, `skills`, `mcps`, `settings`, `hooks`, `plugins`
- **Search Terms**: Array of keywords from tech-stack-expander (e.g., `[nextjs, react, typescript, tailwind, prisma]`)
- **Requirements**: Specification requirements to match (e.g., tech stack, features)

## Execution Flow

### Step 1: Read Category Guide

```bash
# Read the category-specific skill guide
Read .claude/skills/spec2impl/aitmpl-downloader/categories/${category}.md
```

### Step 2: Search with Expanded Tech Stack

Use the search terms from tech-stack-expander to find matching items:

```bash
# Search using expanded tech stack terms (OR logic)
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "${searchTerms.join(' ')}" --category ${category} --json

# Example: searchTerms = [nextjs, react, typescript, tailwind, prisma]
# Searches: "nextjs react typescript tailwind prisma" with OR logic
# Returns items matching ANY of these terms
```

### Step 3: Prioritize Results

Based on the category guide's "Spec Mapping" table and search results:
1. **Exact matches**: Items with multiple search term hits
2. **Partial matches**: Items with single search term hit
3. **Plugin bundles**: Prefer plugins that include multiple components

### Step 4: Download Matching Items

```bash
# Download each matching item
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "${item_path}" --output ${output_dir}
```

## Category Output Directories

| Category | Output Directory |
|----------|-----------------|
| agents | `.claude/agents/` |
| commands | `.claude/commands/` |
| skills | `.claude/skills/` |
| mcps | `.mcp.json` (merge) |
| settings | `.claude/settings.local.json` (merge) |
| hooks | `.claude/settings.local.json` (merge) |
| plugins | Multiple locations |

## Example Usage

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `Read .claude/agents/spec2impl/category-downloader.md and execute.

           Category: skills
           Search Terms: [nextjs, react, typescript, tailwind, prisma, postgresql, frontend, database, orm]
           Requirements:
           - Frontend framework patterns
           - Database modeling
           - Testing patterns`
})
```

**Note**: Search Terms come from tech-stack-expander (Step 2) which expands the original tech stack via Web search and user questions.

## Output Format

```
═══════════════════════════════════════════════════════════════
Category Download: ${category}
═══════════════════════════════════════════════════════════════

Available: ${total_count} items
Matched:   ${matched_count} items

Downloaded:
  ✅ ${item1} → ${output_path1}
  ✅ ${item2} → ${output_path2}
  ✅ ${item3} → ${output_path3}

Skipped (not matching requirements):
  ⏭️ ${skipped_item1}
  ⏭️ ${skipped_item2}

═══════════════════════════════════════════════════════════════
```

## Error Handling

- **Category not found**: Check valid categories list
- **No items match**: Report available items for manual selection
- **Download failed**: Retry with `--no-cache` flag, report GitHub API rate limit if applicable

## Cache Management

```bash
# Clear cache if needed (e.g., to get latest updates)
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py clear-cache
```

Cache TTL is 15 minutes by default. Use `--no-cache` flag to bypass.
