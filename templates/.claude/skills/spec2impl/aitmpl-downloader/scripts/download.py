#!/usr/bin/env python3
"""
aitmpl.com Template Downloader (GitHub API Version)

Downloads Claude Code templates (agents, commands, settings, hooks, mcps, skills, plugins)
from the claude-code-templates repository using GitHub API for real-time directory listing.

Usage:
    download.py list [--category CATEGORY] [--json]
    download.py get <item_path> [--output OUTPUT_DIR]
    download.py search <query> [--category CATEGORY] [--json]

Examples:
    download.py list --category agents --json
    download.py list --category skills --json
    download.py get "cli-tool/components/agents/development-team/frontend-developer.md" --output .claude/agents
    download.py search "security" --category agents --json
"""

import sys
import json
import urllib.request
import urllib.error
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com/repos/davila7/claude-code-templates/contents"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/davila7/claude-code-templates/main"

# Category to GitHub path mapping
CATEGORY_PATHS = {
    "agents": "cli-tool/components/agents",
    "commands": "cli-tool/components/commands",
    "skills": "cli-tool/components/skills",
    "mcps": "cli-tool/components/mcps",
    "settings": "cli-tool/components/settings",
    "hooks": "cli-tool/components/hooks",
    "plugins": ".claude-plugin",
}

# Output directory mapping
OUTPUT_DIRS = {
    "agents": ".claude/agents",
    "commands": ".claude/commands",
    "skills": ".claude/skills",
    "mcps": ".mcp.json",  # Special: merge into file
    "settings": ".claude/settings.local.json",  # Special: merge into file
    "hooks": ".claude/settings.local.json",  # Special: merge into hooks section
    "plugins": ".claude",  # Plugins expand to multiple locations
}

# Cache configuration
CACHE_DIR = Path.home() / ".cache" / "aitmpl-downloader"
CACHE_TTL_MINUTES = 15

# Fallback index (used when API rate limit is hit)
FALLBACK_INDEX_PATH = Path(__file__).parent.parent / "fallback-index.json"


def get_cache_path(category: str) -> Path:
    """Get cache file path for a category."""
    return CACHE_DIR / f"{category}.json"


def is_cache_valid(cache_path: Path) -> bool:
    """Check if cache file exists and is not expired."""
    if not cache_path.exists():
        return False

    mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
    return datetime.now() - mtime < timedelta(minutes=CACHE_TTL_MINUTES)


def read_cache(category: str) -> Optional[List[Dict]]:
    """Read cached items for a category."""
    cache_path = get_cache_path(category)
    if is_cache_valid(cache_path):
        try:
            return json.loads(cache_path.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return None


def write_cache(category: str, items: List[Dict]):
    """Write items to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = get_cache_path(category)
    cache_path.write_text(json.dumps(items, ensure_ascii=False, indent=2))


def load_fallback_index(category: str) -> List[Dict]:
    """Load items from fallback index file when API fails."""
    if not FALLBACK_INDEX_PATH.exists():
        return []

    try:
        data = json.loads(FALLBACK_INDEX_PATH.read_text())
        return data.get(category, [])
    except (json.JSONDecodeError, IOError):
        return []


def fetch_url(url: str, is_api: bool = False) -> Optional[str]:
    """Fetch content from URL with optional GitHub API headers."""
    headers = {
        "User-Agent": "aitmpl-downloader/1.0"
    }
    if is_api:
        headers["Accept"] = "application/vnd.github.v3+json"
        # Optional: Add token for higher rate limits
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def fetch_github_contents(path: str) -> Optional[List[Dict]]:
    """Fetch directory contents from GitHub API."""
    url = f"{GITHUB_API_BASE}/{path}"
    content = fetch_url(url, is_api=True)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing GitHub API response: {e}", file=sys.stderr)
    return None


def extract_name_from_path(path: str) -> str:
    """Extract readable name from file path."""
    filename = Path(path).stem
    return filename


def get_parent_folder(path: str) -> str:
    """Get the parent folder name (used as subcategory)."""
    parts = Path(path).parts
    if len(parts) >= 2:
        return parts[-2]
    return ""


def fetch_items_recursive(base_path: str, category: str, depth: int = 0, max_depth: int = 3) -> List[Dict]:
    """Recursively fetch all items from a GitHub directory."""
    if depth > max_depth:
        return []

    contents = fetch_github_contents(base_path)
    if not contents:
        return []

    items = []

    for entry in contents:
        entry_type = entry.get("type")
        entry_path = entry.get("path", "")
        entry_name = entry.get("name", "")

        if entry_type == "dir":
            # Recurse into subdirectories
            sub_items = fetch_items_recursive(entry_path, category, depth + 1, max_depth)
            items.extend(sub_items)

        elif entry_type == "file":
            # Filter by file extension based on category
            if category in ("agents", "commands", "skills") and not entry_name.endswith(".md"):
                continue
            if category == "mcps" and not entry_name.endswith(".json"):
                continue
            if category == "settings" and not entry_name.endswith(".json"):
                continue
            if category == "hooks" and not entry_name.endswith(".json"):
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


def list_items(category: Optional[str] = None, use_cache: bool = True) -> List[Dict]:
    """List available items from GitHub repository."""
    all_items = []

    categories_to_fetch = [category] if category else list(CATEGORY_PATHS.keys())

    for cat in categories_to_fetch:
        if cat not in CATEGORY_PATHS:
            print(f"Unknown category: {cat}", file=sys.stderr)
            continue

        # Check cache first
        if use_cache:
            cached = read_cache(cat)
            if cached:
                all_items.extend(cached)
                continue

        # Fetch from GitHub API
        base_path = CATEGORY_PATHS[cat]
        items = fetch_items_recursive(base_path, cat)

        # If API fails (empty result), try fallback index
        if not items:
            fallback_items = load_fallback_index(cat)
            if fallback_items:
                print(f"Using fallback index for {cat} (API rate limit or network issue)", file=sys.stderr)
                items = fallback_items

        # Cache the results
        if items:
            write_cache(cat, items)

        all_items.extend(items)

    return all_items


def search_items(query: str, category: Optional[str] = None) -> List[Dict]:
    """Search items by query string.

    Supports multiple search terms separated by spaces.
    Items matching ANY term will be included (OR logic).
    """
    items = list_items(category)

    # Split query into individual terms
    query_terms = [term.lower().strip() for term in query.split() if term.strip()]
    if not query_terms:
        return []

    results = []
    for item in items:
        name = item.get("name", "").lower()
        desc = item.get("description", "").lower()
        subcategory = item.get("subcategory", "").lower()
        path = item.get("path", "").lower()

        searchable = f"{name} {desc} {subcategory} {path}"

        # Match if ANY term is found (OR logic)
        if any(term in searchable for term in query_terms):
            results.append(item)

    return results


def download_file(path: str, output_dir: str = ".") -> bool:
    """Download a file from the repository."""
    # Normalize path
    if path.startswith("./"):
        path = path[2:]

    url = f"{GITHUB_RAW_BASE}/{path}"
    content = fetch_url(url)

    if content is None:
        return False

    # Create output path
    output_path = Path(output_dir) / Path(path).name
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(content)
    print(f"Downloaded: {output_path}")
    return True


def download_skill(path: str, output_dir: str = ".claude/skills") -> bool:
    """Download a skill (which may be a directory with multiple files)."""
    # For skills, we need to check if it's a directory
    contents = fetch_github_contents(path)

    if contents is None:
        # It might be a single file
        return download_file(path, output_dir)

    # It's a directory, download all files
    skill_name = Path(path).name
    skill_output_dir = Path(output_dir) / skill_name
    skill_output_dir.mkdir(parents=True, exist_ok=True)

    success = True
    for entry in contents:
        if entry.get("type") == "file":
            file_url = entry.get("download_url")
            file_name = entry.get("name")
            if file_url and file_name:
                content = fetch_url(file_url)
                if content:
                    (skill_output_dir / file_name).write_text(content)
                    print(f"Downloaded: {skill_output_dir / file_name}")
                else:
                    success = False
        elif entry.get("type") == "dir":
            # Recurse for subdirectories
            sub_path = entry.get("path")
            if sub_path:
                download_skill(sub_path, str(skill_output_dir))

    return success


def download_item(item: dict, output_dir: Optional[str] = None) -> bool:
    """Download an item based on its category."""
    category = item.get("category")
    path = item.get("path", "")

    # Use default output directory if not specified
    if output_dir is None:
        output_dir = OUTPUT_DIRS.get(category, ".")

    if category == "skills":
        # Skills might be directories
        return download_skill(path, output_dir)

    elif category in ("agents", "commands"):
        return download_file(path, output_dir)

    elif category == "mcps":
        # Download MCP config JSON
        content = fetch_url(f"{GITHUB_RAW_BASE}/{path}")
        if content:
            try:
                mcp_config = json.loads(content)
                # Output path for MCP config
                output_path = Path(output_dir) if output_dir.endswith(".json") else Path(output_dir) / Path(path).name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(mcp_config, indent=2))
                print(f"Downloaded MCP config: {output_path}")
                return True
            except json.JSONDecodeError:
                pass
        return False

    elif category in ("settings", "hooks"):
        # Download settings/hooks config JSON
        content = fetch_url(f"{GITHUB_RAW_BASE}/{path}")
        if content:
            try:
                config = json.loads(content)
                output_path = Path(output_dir) if output_dir.endswith(".json") else Path(output_dir) / Path(path).name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(config, indent=2))
                print(f"Downloaded {category} config: {output_path}")
                return True
            except json.JSONDecodeError:
                pass
        return False

    elif category == "plugins":
        # Plugins need special handling - download the plugin.json and all referenced files
        return download_file(path, output_dir)

    print(f"Unknown category: {category}", file=sys.stderr)
    return False


def print_items(items: List[Dict], as_json: bool = False):
    """Pretty print a list of items."""
    if as_json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return

    if not items:
        print("No items found.")
        return

    # Group by category and subcategory
    grouped: Dict[str, Dict[str, List[Dict]]] = {}
    for item in items:
        cat = item.get("category", "other")
        subcat = item.get("subcategory", "general")
        if cat not in grouped:
            grouped[cat] = {}
        if subcat not in grouped[cat]:
            grouped[cat][subcat] = []
        grouped[cat][subcat].append(item)

    for cat, subcats in sorted(grouped.items()):
        print(f"\n{'='*60}")
        print(f" {cat.upper()} ({sum(len(items) for items in subcats.values())} items)")
        print(f"{'='*60}")

        for subcat, items_list in sorted(subcats.items()):
            print(f"\n  [{subcat}]")
            for item in items_list:
                name = item.get("name", "unknown")
                print(f"    • {name}")


def clear_cache():
    """Clear all cached data."""
    if CACHE_DIR.exists():
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()
        print("Cache cleared.")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        sys.exit(0)

    command = args[0]
    as_json = "--json" in args
    no_cache = "--no-cache" in args

    if command == "list":
        category = None
        if "--category" in args:
            idx = args.index("--category")
            if idx + 1 < len(args):
                category = args[idx + 1]

        items = list_items(category, use_cache=not no_cache)
        print_items(items, as_json)

    elif command == "search":
        if len(args) < 2:
            print("Usage: download.py search <query> [--category CATEGORY] [--json]")
            sys.exit(1)

        query = args[1]
        category = None
        if "--category" in args:
            idx = args.index("--category")
            if idx + 1 < len(args):
                category = args[idx + 1]

        items = search_items(query, category)
        print_items(items, as_json)

    elif command == "get":
        if len(args) < 2:
            print("Usage: download.py get <item_path> [--output OUTPUT_DIR]")
            sys.exit(1)

        path = args[1]
        output_dir = "."
        if "--output" in args:
            idx = args.index("--output")
            if idx + 1 < len(args):
                output_dir = args[idx + 1]

        success = download_file(path, output_dir)
        sys.exit(0 if success else 1)

    elif command == "clear-cache":
        clear_cache()

    elif command == "categories":
        # List available categories
        print("Available categories:")
        for cat, path in CATEGORY_PATHS.items():
            output = OUTPUT_DIRS.get(cat, ".")
            print(f"  {cat}: {path} -> {output}")

    else:
        print(f"Unknown command: {command}")
        print("Use 'download.py --help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
