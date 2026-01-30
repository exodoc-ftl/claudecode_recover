#!/bin/bash
# Checkpoint hook for Claude Code
# Records file edits to enable checkpoint tracking
#
# Add to ~/.claude/settings.json:
# {
#   "hooks": {
#     "postToolUse": [
#       {
#         "matcher": "Edit|Write",
#         "command": "~/.claude/hooks/checkpoint-hook.sh"
#       }
#     ]
#   }
# }

CHECKPOINT_DIR="$HOME/.claude/checkpoints"
mkdir -p "$CHECKPOINT_DIR"

# Read hook input from stdin
INPUT=$(cat)

# Extract fields from JSON input
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool',''))" 2>/dev/null)
PROJECT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('cwd','').split('/')[-1])" 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); i=d.get('input',{}); print(i.get('file_path',''))" 2>/dev/null)

# Skip if no project detected
if [ -z "$PROJECT" ] || [ "$PROJECT" = "" ]; then
    exit 0
fi

# Create checkpoint entry
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DETAIL=$(basename "$FILE_PATH" 2>/dev/null || echo "unknown")

# Append to project-specific checkpoint file
echo "{\"timestamp\":\"$TIMESTAMP\",\"tool\":\"$TOOL\",\"project\":\"$PROJECT\",\"detail\":\"$DETAIL\",\"path\":\"$FILE_PATH\"}" >> "$CHECKPOINT_DIR/$PROJECT.jsonl"
