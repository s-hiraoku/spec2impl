# Hooks Category Guide

Download Claude Code hook configurations from claude-code-templates.

## GitHub Path

- Source: `cli-tool/components/hooks`
- API: `https://api.github.com/repos/davila7/claude-code-templates/contents/cli-tool/components/hooks`

## Output Directory

- Target: `.claude/settings.local.json` (hooks section)

## Available Hook Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| PreToolUse | Before tool execution | Validation, logging |
| PostToolUse | After tool execution | Notifications, cleanup |
| Notification | Custom notifications | Alerts, status updates |
| Stop | Execution stop | Cleanup, reporting |

## Commands

```bash
# List all hooks
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py list --category hooks --json

# Search hooks
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py search "<query>" --category hooks --json

# Download specific hook
python3 .claude/skills/spec2impl/aitmpl-downloader/scripts/download.py get "<path>" --output .claude
```

## Hook Configuration Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "echo 'Running: $TOOL_NAME'"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "command": "echo 'Completed: $TOOL_NAME'"
      }
    ],
    "Notification": [
      {
        "command": "notify-send 'Claude Code' '$MESSAGE'"
      }
    ]
  }
}
```

## Spec Mapping

| Requirement | Recommended Hooks |
|-------------|------------------|
| Audit logging | PreToolUse logger |
| Desktop notifications | Notification hook |
| Git auto-commit | PostToolUse git hook |
| Security validation | PreToolUse validator |

## Hook Merge Strategy

When downloading, hooks are merged into arrays:
- Same event type: Append to existing array
- New event type: Add new key

Example:
```json
// Existing
{ "hooks": { "PreToolUse": [{ "matcher": "Bash" }] } }

// Downloaded
{ "hooks": { "PreToolUse": [{ "matcher": "Write" }] } }

// Result
{ "hooks": { "PreToolUse": [{ "matcher": "Bash" }, { "matcher": "Write" }] } }
```

## Note

Hooks are executed as shell commands. Be careful with:
- Command injection risks
- Performance impact (hooks run frequently)
- Error handling (failed hooks may block operations)
