#!/usr/bin/env python3
"""
View Claude Code session checkpoints.
Shows recent actions across all projects or filtered by project.

Checkpoints are recorded by hooks that fire on file edits.

Usage: python3 checkpoints.py [project-name] [--last N]
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
CHECKPOINT_DIR = HOME / ".claude/checkpoints"
DEFAULT_LAST = 20


def format_time_ago(timestamp_str):
    """Format timestamp as human-readable time ago."""
    try:
        ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        hours = (now - ts).total_seconds() / 3600

        if hours < 1:
            return f"{int(hours * 60)}m ago"
        elif hours < 24:
            return f"{hours:.1f}h ago"
        else:
            return f"{hours / 24:.1f}d ago"
    except:
        return "?"


def load_checkpoints(project_filter=None, last_n=DEFAULT_LAST):
    """Load checkpoints from all or filtered project files."""
    if not CHECKPOINT_DIR.exists():
        return []

    all_checkpoints = []

    for checkpoint_file in CHECKPOINT_DIR.glob("*.jsonl"):
        project = checkpoint_file.stem

        if project_filter and project_filter.lower() not in project.lower():
            continue

        try:
            with open(checkpoint_file) as f:
                lines = f.readlines()
                for line in lines[-last_n:]:
                    try:
                        cp = json.loads(line.strip())
                        cp['_project_file'] = project
                        all_checkpoints.append(cp)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue

    all_checkpoints.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return all_checkpoints[:last_n]


def print_checkpoints(checkpoints):
    """Print formatted checkpoint table."""
    if not checkpoints:
        print("No checkpoints found.")
        return

    print(f"\n{'Time':>10} | {'Project':<20} | {'Action':<10} | Detail")
    print("-" * 80)

    for cp in checkpoints:
        time_str = format_time_ago(cp.get('timestamp', ''))
        project = cp.get('project', 'unknown')[:20]
        tool = cp.get('tool', '?')[:10]
        detail = cp.get('detail', '')[:40]

        print(f"{time_str:>10} | {project:<20} | {tool:<10} | {detail}")


def main():
    args = sys.argv[1:]
    project_filter = None
    last_n = DEFAULT_LAST

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--last" and i + 1 < len(args):
            try:
                last_n = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        elif not arg.startswith("--"):
            project_filter = arg
            i += 1
        else:
            i += 1

    if project_filter:
        print(f"Checkpoints for '{project_filter}' (last {last_n}):")
    else:
        print(f"Recent checkpoints across all projects (last {last_n}):")

    checkpoints = load_checkpoints(project_filter, last_n)
    print_checkpoints(checkpoints)


if __name__ == "__main__":
    main()
