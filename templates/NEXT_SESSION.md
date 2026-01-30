# Next Session

**Last Updated**: [date]
**Previous Session**: [link to SESSION_XX or description]

## Current State

[Brief status of where things stand]

## Priority Tasks

1. [Task with verification criteria]
2. [Task with verification criteria]

## Service Recovery

When recovering from a crash or starting fresh:

### 1. Check Service Status
```bash
# Check what's running
pgrep -fl "[service-name-or-project]"
```

### 2. Start Services (if not running)
```bash
cd /path/to/project
source .venv/bin/activate  # if Python

# Start in dependency order:
# 1. External deps (databases, gateways)
# 2. Main application
# 3. Auxiliary (dashboards, monitors)
[startup commands here]
```

### 3. Verify Running
```bash
tail -f logs/[logfile].log
# or
curl localhost:[port]/health
```

### 4. Common Issues

| Issue | Check | Fix |
|-------|-------|-----|
| Service won't start | Check logs | [fix] |
| Port in use | `lsof -i :[port]` | Kill stale process |
| Missing deps | Check .env | Restore from .env.example |

## Ready-to-Paste Prompt

```
[Full prompt that can be pasted into a fresh Claude session with all necessary context]
```

## Session Link

file:///path/to/project/docs/sessions/SESSION_XX_name.md
