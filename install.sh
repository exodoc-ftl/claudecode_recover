#!/bin/bash
# Install claude-recover
# Run: curl -fsSL https://raw.githubusercontent.com/exodoc-ftl/claudecode_recover/main/install.sh | bash

set -e

CLAUDE_DIR="$HOME/.claude"
REPO_URL="https://github.com/exodoc-ftl/claudecode_recover"

echo "Installing claude-recover..."

# Create directories
mkdir -p "$CLAUDE_DIR/scripts"
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/checkpoints"

# Determine install source
if [ -d "$(dirname "$0")/scripts" ]; then
    # Local install
    SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
    echo "Installing from local directory: $SOURCE_DIR"

    cp "$SOURCE_DIR/scripts/recover.py" "$CLAUDE_DIR/scripts/"
    cp "$SOURCE_DIR/scripts/checkpoints.py" "$CLAUDE_DIR/scripts/"
    cp "$SOURCE_DIR/commands/recover.md" "$CLAUDE_DIR/commands/"
    cp "$SOURCE_DIR/hooks/checkpoint-hook.sh" "$CLAUDE_DIR/hooks/"
else
    # Remote install (curl | bash)
    echo "Installing from GitHub..."

    curl -fsSL "$REPO_URL/raw/main/scripts/recover.py" -o "$CLAUDE_DIR/scripts/recover.py"
    curl -fsSL "$REPO_URL/raw/main/scripts/checkpoints.py" -o "$CLAUDE_DIR/scripts/checkpoints.py"
    curl -fsSL "$REPO_URL/raw/main/commands/recover.md" -o "$CLAUDE_DIR/commands/recover.md"
    curl -fsSL "$REPO_URL/raw/main/hooks/checkpoint-hook.sh" -o "$CLAUDE_DIR/hooks/checkpoint-hook.sh"
fi

# Make scripts executable
chmod +x "$CLAUDE_DIR/scripts/recover.py"
chmod +x "$CLAUDE_DIR/scripts/checkpoints.py"
chmod +x "$CLAUDE_DIR/hooks/checkpoint-hook.sh"

echo ""
echo "Installed:"
echo "  - /recover command"
echo "  - checkpoint tracking scripts"
echo ""
echo "To enable checkpoint tracking, add this to ~/.claude/settings.json:"
echo ""
echo '  "hooks": {'
echo '    "postToolUse": ['
echo '      {'
echo '        "matcher": "Edit|Write",'
echo '        "command": "~/.claude/hooks/checkpoint-hook.sh"'
echo '      }'
echo '    ]'
echo '  }'
echo ""
echo "Done! Try: /recover"
