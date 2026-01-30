---
description: List recent Claude Code sessions, recover context, and restart services
argument-hint: [project-name] [--hours N]
allowed-tools: Bash(python3:*), Bash(pgrep:*), Bash(cd:*), Bash(source:*), Bash(tail:*), Bash(ls:*), Bash(crontab:*), Read
---

Find and display recent Claude Code sessions to help recover context and restart services.

## Recent Sessions

!`python3 ~/.claude/scripts/recover.py $ARGUMENTS`

## Recent Checkpoints (Auto-saved Actions)

!`python3 ~/.claude/scripts/checkpoints.py $ARGUMENTS 2>/dev/null || echo "No checkpoints yet (enable hooks for checkpoint tracking)"`

## Instructions

Based on the sessions listed above:

### 1. Session Recovery

**If the user specifies a session number** (e.g., "recover session 2" or just "2"):
- Read that project's session docs using the file paths shown above
- Look for: `NEXT_SESSION.md`, `SESSION_DIARY.md`, or latest `SESSION_*.md`
- Generate a handoff prompt with project path, context, status, and next steps

**If no session specified**, ask which session they want to recover

### 2. Service Recovery (Universal Pattern)

When recovering a project, **always check for and execute service recovery**:

1. **Read the project's session docs** for a "Service Recovery" section
2. **If found**, follow those project-specific instructions
3. **If not found**, use this generic pattern:

```bash
# Generic service check pattern
cd [PROJECT_PATH]

# Check for running processes related to this project
pgrep -fl "[project-name]"

# Check for common service patterns
ls -la *.pid 2>/dev/null          # PID files
ls -la logs/*.log 2>/dev/null     # Recent logs
cat .env 2>/dev/null | head -5    # Environment config

# Check if it's a Python project with venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Look for common entry points
ls -la main.py run.py app.py server.py 2>/dev/null
ls -la scripts/*.py 2>/dev/null
```

4. **Report status** to user:
   - What services are running
   - What services are stopped
   - Offer to start stopped services

5. **Start services** if user confirms, in dependency order:
   - External dependencies first (databases, gateways)
   - Main application second
   - Auxiliary services last (dashboards, monitors)

### 3. Handoff Prompt Format

```
Continuing [Project Name] - [Brief Context]

Project: /path/to/project
Session doc: /path/to/docs/file.md

CONTEXT:
[Key points from session docs]

CURRENT STATUS:
[What was completed, what's in progress]

SERVICE STATUS:
[x] Service A - running (PID: 1234)
[ ] Service B - stopped
[ ] Service C - stopped

NEXT STEPS:
[Clear actionable items]

TO START SERVICES:
[Commands to start stopped services]
```

### 4. Always Include
- The `file://` link to session docs
- Service status check results
- Commands to restart any stopped services
