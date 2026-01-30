# claude-recover

Session continuity for Claude Code. Never lose your context again.

## The Problem

You're deep in a Claude Code session across multiple projects. Your machine crashes, or you need to restart. Now you're staring at a blank terminal trying to remember:

- Which projects were you working on?
- What services were running?
- Where did you leave off?

## The Solution

```
/recover
```

That's it. One command shows you:

```
Recent sessions (last 48h):

 # |     Time | Msgs | Project                   | Summary
------------------------------------------------------------------------------------------
 1 |    0.3h ago |   47 | trading-bot               | Implementing backtest engine
   |          |      |                           | Docs: NEXT_SESSION.md
 2 |    2.1h ago |   23 | api-gateway               | Fixed auth middleware
   |          |      |                           | Docs: SESSION_DIARY.md
 3 |    5.4h ago |   89 | ml-pipeline               | Training loop optimization
   |          |      |                           | Docs: SESSION_12_training.md
```

Say "recover session 1" and Claude reads your session docs, checks which services are running, and generates a complete handoff prompt to continue exactly where you left off.

## What It Does

1. **Lists recent sessions** across all your projects (taps into Claude Code's session index)
2. **Detects session docs** (NEXT_SESSION.md, SESSION_DIARY.md, SESSION_*.md)
3. **Checks service status** for projects with background processes
4. **Generates handoff prompts** with full context to continue work

## Install

```bash
# Clone and run install script
git clone https://github.com/exodoc-ftl/claude-recover.git
cd claude-recover
./install.sh
```

This copies the scripts to `~/.claude/` where Claude Code can use them.

## Usage

### Basic Recovery

```
/recover                    # List all recent sessions
/recover trading            # Filter by project name
/recover --hours 72         # Look back further
```

Then tell Claude which session to recover:

```
recover session 2
```

Claude will:
1. Read your project's session docs
2. Check if any services should be running
3. Generate a handoff prompt with context, status, and next steps

### Session Docs Convention

For best results, keep a `docs/NEXT_SESSION.md` in your projects:

```markdown
# Next Session

## Current State
[Where things stand]

## Service Recovery
[Commands to check/restart services - see templates/]

## Ready-to-Paste Prompt
[Full context for continuing work]
```

See `templates/` for examples.

### Checkpoint Tracking (Optional)

Track file edits across sessions by enabling the checkpoint hook.

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "postToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "~/.claude/hooks/checkpoint-hook.sh"
      }
    ]
  }
}
```

Now `/recover` also shows recent file changes:

```
Recent checkpoints across all projects (last 20):

      Time | Project              | Action     | Detail
--------------------------------------------------------------------------------
    12m ago | trading-bot          | Edit       | backtest.py
    15m ago | trading-bot          | Write      | test_backtest.py
    1.2h ago | api-gateway          | Edit       | middleware.ts
```

## How It Works

Claude Code maintains a session index at `~/.claude/projects/*/sessions-index.json`. This tool reads that index to find your recent sessions, then looks for documentation files in each project that follow common conventions.

The checkpoint hook (optional) records each file edit to `~/.claude/checkpoints/`, creating a timeline of changes you can review.

## Project Structure

```
claude-recover/
├── scripts/
│   ├── recover.py        # Session discovery and display
│   └── checkpoints.py    # Checkpoint viewer
├── commands/
│   └── recover.md        # Slash command definition
├── hooks/
│   └── checkpoint-hook.sh # Optional edit tracking
├── templates/
│   ├── NEXT_SESSION.md   # Session doc template
│   └── SERVICE_RECOVERY.md # Service recovery template
└── install.sh
```

## The Workflow

This tool is part of a session-based development workflow:

1. **Each session is self-contained** - Session docs have all context needed to continue
2. **Services are documented** - Projects with background processes include recovery instructions
3. **Handoffs are explicit** - Each session ends with a ready-to-paste prompt for the next

After a crash or restart, `/recover` gets you back to work in seconds instead of minutes.

## License

MIT
