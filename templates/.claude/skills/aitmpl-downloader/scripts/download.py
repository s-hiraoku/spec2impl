#!/usr/bin/env python3
"""
aitmpl.com Template Downloader

Downloads Claude Code templates (agents, commands, settings, hooks, mcps, skills, plugins)
from the claude-code-templates repository.

Usage:
    download.py list [--category CATEGORY] [--json]
    download.py get <item_path> [--output OUTPUT_DIR]
    download.py search <query> [--category CATEGORY] [--json]

Examples:
    download.py list --category agents --json
    download.py get .claude/agents/frontend-developer.md --output .claude/agents
    download.py search "security" --category agents --json
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/davila7/claude-code-templates/main"
MARKETPLACE_URL = f"{GITHUB_RAW_BASE}/.claude-plugin/marketplace.json"

# Known template paths in the repository
TEMPLATE_PATHS = {
    "agents": ".claude/agents",
    "commands": ".claude/commands",
    "settings": ".claude",
    "hooks": ".claude",
    "mcps": ".claude",
    "skills": ".claude/skills",
    "plugins": ".claude-plugin",
}


def fetch_url(url: str) -> Optional[str]:
    """Fetch content from URL."""
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def fetch_marketplace() -> Optional[dict]:
    """Fetch and parse marketplace.json."""
    content = fetch_url(MARKETPLACE_URL)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing marketplace.json: {e}", file=sys.stderr)
    return None


def extract_name_from_path(path: str) -> str:
    """Extract readable name from file path."""
    # ./cli-tool/components/agents/git/git-flow-manager.md -> git-flow-manager
    filename = Path(path).stem
    return filename


def list_items(category: Optional[str] = None) -> list:
    """List available items from marketplace."""
    marketplace = fetch_marketplace()
    if not marketplace:
        return []

    items = []
    plugins = marketplace.get("plugins", [])

    for plugin in plugins:
        plugin_name = plugin.get("name", "unknown")
        plugin_desc = plugin.get("description", "")

        # Collect items by category
        # agents and commands are path strings
        if category is None or category == "agents":
            for agent_path in plugin.get("agents", []):
                if isinstance(agent_path, str):
                    items.append({
                        "category": "agents",
                        "name": extract_name_from_path(agent_path),
                        "description": f"Agent from {plugin_name}",
                        "path": agent_path,
                        "plugin": plugin_name
                    })

        if category is None or category == "commands":
            for cmd_path in plugin.get("commands", []):
                if isinstance(cmd_path, str):
                    items.append({
                        "category": "commands",
                        "name": extract_name_from_path(cmd_path),
                        "description": f"Command from {plugin_name}",
                        "path": cmd_path,
                        "plugin": plugin_name
                    })

        # mcpServers can be path strings or objects
        if category is None or category == "mcps":
            for mcp in plugin.get("mcpServers", []):
                if isinstance(mcp, str):
                    items.append({
                        "category": "mcps",
                        "name": extract_name_from_path(mcp),
                        "description": f"MCP from {plugin_name}",
                        "path": mcp,
                        "plugin": plugin_name
                    })
                elif isinstance(mcp, dict):
                    items.append({
                        "category": "mcps",
                        "name": mcp.get("name", "unknown"),
                        "description": mcp.get("description", f"MCP from {plugin_name}"),
                        "config": mcp.get("config", {}),
                        "path": mcp.get("path", ""),
                        "plugin": plugin_name
                    })

        # plugins themselves as downloadable items
        if category is None or category == "plugins":
            items.append({
                "category": "plugins",
                "name": plugin_name,
                "description": plugin_desc,
                "keywords": plugin.get("keywords", []),
                "plugin": plugin_name
            })

        if category is None or category == "settings":
            settings = plugin.get("settings", {})
            if settings:
                items.append({
                    "category": "settings",
                    "name": f"{plugin_name} settings",
                    "description": f"Settings for {plugin_name}",
                    "config": settings,
                    "plugin": plugin_name
                })

        if category is None or category == "hooks":
            for hook in plugin.get("hooks", []):
                if isinstance(hook, dict):
                    items.append({
                        "category": "hooks",
                        "name": hook.get("event", "unknown"),
                        "description": f"Hook for {hook.get('event', '')}",
                        "config": hook,
                        "plugin": plugin_name
                    })

    return items


def search_items(query: str, category: Optional[str] = None) -> list:
    """Search items by query string."""
    items = list_items(category)
    query_lower = query.lower()

    results = []
    for item in items:
        name = item.get("name", "").lower()
        desc = item.get("description", "").lower()
        if query_lower in name or query_lower in desc:
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


def download_item(item: dict, output_dir: str = ".") -> bool:
    """Download an item based on its category."""
    category = item.get("category")

    if category in ("agents", "commands", "skills"):
        path = item.get("path")
        if path:
            return download_file(path, output_dir)

    elif category == "mcps":
        # MCP servers are config-based, output as JSON
        config = item.get("config", {})
        name = item.get("name", "mcp")
        output_path = Path(output_dir) / f"{name}.mcp.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(config, indent=2))
        print(f"Downloaded MCP config: {output_path}")
        return True

    elif category == "hooks":
        config = item.get("config", {})
        event = config.get("event", "hook")
        output_path = Path(output_dir) / f"{event}.hook.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(config, indent=2))
        print(f"Downloaded hook config: {output_path}")
        return True

    elif category == "settings":
        config = item.get("config", {})
        output_path = Path(output_dir) / "settings.local.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(config, indent=2))
        print(f"Downloaded settings: {output_path}")
        return True

    print(f"Unknown category: {category}", file=sys.stderr)
    return False


def print_items(items: list, as_json: bool = False):
    """Pretty print a list of items."""
    if as_json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return

    if not items:
        print("No items found.")
        return

    for i, item in enumerate(items, 1):
        cat = item.get("category", "?")
        name = item.get("name", "unknown")
        desc = item.get("description", "")[:60]
        plugin = item.get("plugin", "")

        print(f"{i}. [{cat}] {name}")
        if desc:
            print(f"    {desc}...")
        if plugin:
            print(f"    Plugin: {plugin}")
        print()


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        sys.exit(0)

    command = args[0]

    as_json = "--json" in args

    if command == "list":
        category = None
        if "--category" in args:
            idx = args.index("--category")
            if idx + 1 < len(args):
                category = args[idx + 1]

        items = list_items(category)
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

    else:
        print(f"Unknown command: {command}")
        print("Use 'download.py --help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
