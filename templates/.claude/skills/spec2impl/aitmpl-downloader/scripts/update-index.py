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


def extract_name_from_path(path: str) -> str:
    """Extract readable name from file path."""
    return Path(path).stem


def get_parent_folder(path: str) -> str:
    """Get the parent folder name (used as subcategory)."""
    parts = Path(path).parts
    if len(parts) >= 2:
        return parts[-2]
    return ""


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

            items.append({
                "category": category,
                "name": extract_name_from_path(entry_name),
                "description": f"{category.title()} from {subcategory}" if subcategory else f"{category.title()}",
                "path": entry_path,
                "subcategory": subcategory,
                "download_url": entry.get("download_url", f"{GITHUB_RAW_BASE}/{entry_path}"),
                "size": entry.get("size", 0),
            })

    return items


def generate_index() -> Dict:
    """Generate complete index for all categories."""
    index = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "https://github.com/davila7/claude-code-templates",
    }

    for category, path in CATEGORY_PATHS.items():
        print(f"\nFetching {category}...", file=sys.stderr)
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
