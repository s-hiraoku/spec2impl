#!/usr/bin/env python3
"""
Generate fallback-index.json from GitHub API.

This script fetches all templates from claude-code-templates repository
and generates a static index file for fallback when API rate limits are hit.

Usage:
    GITHUB_TOKEN=your_token python3 update-index.py

Requires GITHUB_TOKEN environment variable for higher rate limits (5000/hour).
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

GITHUB_API_BASE = "https://api.github.com/repos/davila7/claude-code-templates/contents"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/davila7/claude-code-templates/main"

CATEGORY_PATHS = {
    "agents": "cli-tool/components/agents",
    "commands": "cli-tool/components/commands",
    "skills": "cli-tool/components/skills",
    "mcps": "cli-tool/components/mcps",
    "settings": "cli-tool/components/settings",
    "hooks": "cli-tool/components/hooks",
    "plugins": ".claude-plugin",
}

OUTPUT_FILE = Path(__file__).parent.parent / "fallback-index.json"


def fetch_url(url: str) -> Optional[str]:
    """Fetch content from GitHub API with authentication."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not set. Rate limits will be very low (60/hour).", file=sys.stderr)

    headers = {
        "User-Agent": "aitmpl-downloader/1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            # Check rate limit headers
            remaining = response.headers.get("X-RateLimit-Remaining", "?")
            limit = response.headers.get("X-RateLimit-Limit", "?")
            print(f"  Rate limit: {remaining}/{limit}", file=sys.stderr)
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"Rate limit exceeded! Set GITHUB_TOKEN for higher limits.", file=sys.stderr)
        else:
            print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def fetch_github_contents(path: str) -> Optional[List[Dict]]:
    """Fetch directory contents from GitHub API."""
    url = f"{GITHUB_API_BASE}/{path}"
    content = fetch_url(url)
    if content:
        try:
            result = json.loads(content)
            # Handle case where path is a file, not directory
            if isinstance(result, dict):
                return [result]
            return result
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}", file=sys.stderr)
    return None


def extract_name_from_path(path: str, category: str = "") -> str:
    """Extract readable name from file path.

    For skills with SKILL.md filename, use the parent directory name instead.
    """
    parts = Path(path).parts
    filename = Path(path).stem

    # For SKILL.md files, use the skill directory name instead
    if filename.upper() == "SKILL" and category == "skills":
        # path: cli-tool/components/skills/development/git-commit-helper/SKILL.md
        # → return "git-commit-helper"
        skill_categories = (
            "business-marketing", "creative-design", "development",
            "document-processing", "enterprise-communication",
            "media", "productivity", "utilities"
        )
        for i, part in enumerate(parts):
            if part in skill_categories and i + 1 < len(parts):
                next_part = parts[i + 1]
                # Skip if next part is the SKILL.md file itself
                if not next_part.upper().endswith(".MD"):
                    return next_part
        # Fallback: use parent directory name
        if len(parts) >= 2:
            parent = parts[-2]
            if not parent.upper().endswith(".MD") and parent not in skill_categories:
                return parent

    return filename


def get_parent_folder(path: str) -> str:
    """Get the parent folder name (used as subcategory)."""
    parts = Path(path).parts
    if len(parts) >= 2:
        return parts[-2]
    return ""


# Skills description mapping for better searchability
SKILL_DESCRIPTIONS = {
    # development
    "skill-creator": "Create new Claude Code skills with templates and best practices",
    "git-commit-helper": "Git commit message generation and conventional commit best practices",
    "changelog-generator": "Automated changelog generation from git commits",
    "mcp-builder": "MCP server creation, development tools and best practices",
    "webapp-testing": "Web application testing patterns, E2E testing utilities",
    "artifacts-builder": "Build and manage Claude artifacts",
    "developer-growth-analysis": "Developer productivity and growth analysis",
    "move-code-quality": "Code quality improvement and refactoring patterns",
    "cocoindex": "CocoIndex integration and data indexing",
    "zapier-workflows": "Zapier automation workflows and webhook integration",
    # document-processing
    "pdf-anthropic": "PDF document processing, extraction and analysis",
    "pdf-processing-pro": "Advanced PDF processing with OCR and forms",
    "docx": "Word document (docx) processing and generation",
    "xlsx": "Excel spreadsheet (xlsx) processing and generation",
    # creative-design
    "theme-factory": "UI theme generation, color palettes and design systems",
    "algorithmic-art": "Algorithmic art and generative design patterns",
    "canvas-design": "Canvas-based design and graphics",
    "slack-gif-creator": "Create GIFs for Slack notifications and messages",
    # business-marketing
    "content-research-writer": "Content research, SEO writing and copywriting",
    "competitive-ads-extractor": "Competitive advertising analysis and extraction",
    "lead-research-assistant": "Lead generation research and prospect analysis",
}


def generate_description(category: str, item_name: str, subcategory: str) -> str:
    """Generate searchable description for items."""
    # Use predefined description if available
    if category == "skills" and item_name in SKILL_DESCRIPTIONS:
        return SKILL_DESCRIPTIONS[item_name]

    # Default description
    if subcategory:
        return f"{category.title()} from {subcategory}"
    return f"{category.title()}"


def fetch_items_recursive(base_path: str, category: str, depth: int = 0, max_depth: int = 4) -> List[Dict]:
    """Recursively fetch all items from a GitHub directory."""
    if depth > max_depth:
        return []

    print(f"  Fetching: {base_path}", file=sys.stderr)
    contents = fetch_github_contents(base_path)
    if not contents:
        return []

    items = []

    for entry in contents:
        entry_type = entry.get("type")
        entry_path = entry.get("path", "")
        entry_name = entry.get("name", "")

        if entry_type == "dir":
            sub_items = fetch_items_recursive(entry_path, category, depth + 1, max_depth)
            items.extend(sub_items)

        elif entry_type == "file":
            # Filter by file extension based on category
            if category in ("agents", "commands") and not entry_name.endswith(".md"):
                continue
            if category == "skills" and not entry_name.endswith(".md"):
                continue
            if category == "mcps" and not entry_name.endswith(".json"):
                continue
            if category == "settings" and not entry_name.endswith(".json"):
                continue
            if category == "hooks" and not entry_name.endswith(".json"):
                continue
            if category == "plugins" and not entry_name.endswith(".json"):
                continue

            subcategory = get_parent_folder(entry_path)
            item_name = extract_name_from_path(entry_path, category)
            description = generate_description(category, item_name, subcategory)

            items.append({
                "category": category,
                "name": item_name,
                "description": description,
                "path": entry_path,
                "subcategory": subcategory,
                "download_url": entry.get("download_url", f"{GITHUB_RAW_BASE}/{entry_path}"),
                "size": entry.get("size", 0),
            })

    return items


def fetch_marketplace_plugins() -> List[Dict]:
    """Fetch and parse plugins from marketplace.json."""
    print("  Fetching marketplace.json for plugins...", file=sys.stderr)
    marketplace_url = f"{GITHUB_RAW_BASE}/.claude-plugin/marketplace.json"

    try:
        request = urllib.request.Request(
            marketplace_url,
            headers={"User-Agent": "aitmpl-downloader/1.0"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"  Error fetching marketplace.json: {e}", file=sys.stderr)
        return []

    try:
        data = json.loads(content)
        plugins = data.get("plugins", [])

        items = []
        for plugin in plugins:
            plugin_name = plugin.get("name", "")
            plugin_desc = plugin.get("description", "")

            # Extract components for searchability
            commands = plugin.get("commands", [])
            agents = plugin.get("agents", [])
            skills = plugin.get("skills", [])

            # Build searchable keywords from component paths
            keywords = []
            for path in commands + agents + skills:
                if isinstance(path, str):
                    name = Path(path).stem
                    keywords.append(name)
                elif isinstance(path, dict):
                    keywords.append(path.get("name", ""))

            items.append({
                "category": "plugins",
                "name": plugin_name,
                "description": plugin_desc,
                "path": ".claude-plugin/marketplace.json",
                "subcategory": "marketplace",
                "download_url": marketplace_url,
                "keywords": " ".join(keywords),
                "commands_count": len(commands),
                "agents_count": len(agents),
                "skills_count": len(skills),
            })

        return items
    except json.JSONDecodeError as e:
        print(f"  Error parsing marketplace.json: {e}", file=sys.stderr)
        return []


def generate_index() -> Dict:
    """Generate complete index for all categories."""
    index = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "https://github.com/davila7/claude-code-templates",
    }

    for category, path in CATEGORY_PATHS.items():
        print(f"\nFetching {category}...", file=sys.stderr)
        if category == "plugins":
            items = fetch_marketplace_plugins()
        else:
            items = fetch_items_recursive(path, category)
        index[category] = items
        print(f"  Found {len(items)} items", file=sys.stderr)

    return index


def main():
    print("Generating fallback-index.json...", file=sys.stderr)
    print(f"Output: {OUTPUT_FILE}", file=sys.stderr)

    index = generate_index()

    # Calculate totals
    total = sum(len(index.get(cat, [])) for cat in CATEGORY_PATHS.keys())
    print(f"\nTotal items: {total}", file=sys.stderr)

    # Write output
    OUTPUT_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"\nSaved to: {OUTPUT_FILE}", file=sys.stderr)

    # Print summary
    print("\nSummary:", file=sys.stderr)
    for category in CATEGORY_PATHS.keys():
        count = len(index.get(category, []))
        print(f"  {category}: {count} items", file=sys.stderr)


if __name__ == "__main__":
    main()
