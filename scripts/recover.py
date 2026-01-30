#!/usr/bin/env python3
"""
Recover session helper for Claude Code.
Scans session logs and displays recent sessions with project docs detection.

Usage: python3 recover.py [project-filter] [--hours N]
"""

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DEFAULT_HOURS = 48


def find_sessions_index():
    """Find the sessions index file for the current user."""
    claude_projects = HOME / ".claude" / "projects"
    if not claude_projects.exists():
        return None

    # Look for sessions-index.json in project directories
    for project_dir in claude_projects.iterdir():
        if project_dir.is_dir():
            index_file = project_dir / "sessions-index.json"
            if index_file.exists():
                return index_file
    return None


def load_sessions():
    """Load sessions index JSON."""
    index_file = find_sessions_index()
    if not index_file:
        print("No sessions index found. Make sure you have Claude Code sessions.")
        sys.exit(1)
    with open(index_file) as f:
        return json.load(f)


def get_project_short_name(project_path):
    """Convert full path to readable short name."""
    home = str(HOME)

    # Common project directories
    for projects_dir in ["Projects", "projects", "code", "Code", "dev", "src"]:
        projects_path = f"{home}/{projects_dir}/"
        if project_path.startswith(projects_path):
            return project_path[len(projects_path):]

    if project_path == home:
        return "~"
    elif project_path.startswith(home):
        return "~" + project_path[len(home):]
    return project_path


def detect_session_docs(project_path):
    """Find session documentation files in common locations."""
    if not project_path or project_path == str(HOME):
        return []

    docs_path = Path(project_path) / "docs"
    found = []

    # Check NEXT_SESSION.md (recommended convention)
    next_session = docs_path / "NEXT_SESSION.md"
    if next_session.exists():
        found.append(("NEXT_SESSION.md", str(next_session)))

    # Check SESSION_DIARY.md (alternative convention)
    session_diary = docs_path / "SESSION_DIARY.md"
    if session_diary.exists():
        found.append(("SESSION_DIARY.md", str(session_diary)))

    # Check sessions folder for individual session files
    sessions_dir = docs_path / "sessions"
    if sessions_dir.exists():
        session_files = sorted(sessions_dir.glob("SESSION*.md"), reverse=True)
        for sf in session_files[:3]:
            found.append((sf.name, str(sf)))

    # Check for session files directly in docs/
    if docs_path.exists():
        direct_sessions = sorted(docs_path.glob("SESSION-*.md"), reverse=True)
        for sf in direct_sessions[:2]:
            if sf.name not in [f[0] for f in found]:
                found.append((sf.name, str(sf)))

    return found


def format_time_ago(hours):
    """Format hours as human-readable time."""
    if hours < 1:
        mins = int(hours * 60)
        return f"{mins}m ago"
    elif hours < 24:
        return f"{hours:.1f}h ago"
    else:
        days = hours / 24
        return f"{days:.1f}d ago"


def filter_sessions(entries, filter_term=None, max_hours=DEFAULT_HOURS):
    """Filter sessions by time and optional project name."""
    now = datetime.now(timezone.utc)
    seen_projects = {}

    for entry in entries:
        modified_str = entry.get('modified', '')
        if not modified_str:
            continue

        try:
            modified = datetime.fromisoformat(modified_str.replace('Z', '+00:00'))
        except ValueError:
            continue

        hours_ago = (now - modified).total_seconds() / 3600

        if hours_ago > max_hours:
            continue

        # Skip sidechains (branched conversations)
        if entry.get('isSidechain', False):
            continue

        project = entry.get('projectPath', '')
        if filter_term:
            if filter_term.lower() not in project.lower():
                continue

        # Keep only most recent session per project
        if project in seen_projects:
            if hours_ago >= seen_projects[project]['hours_ago']:
                continue

        docs = detect_session_docs(project)

        session_data = {
            'project': project,
            'short_name': get_project_short_name(project),
            'summary': entry.get('summary', 'No summary')[:60],
            'hours_ago': hours_ago,
            'message_count': entry.get('messageCount', 0),
            'session_id': entry.get('sessionId', ''),
            'first_prompt': (entry.get('firstPrompt', '') or '')[:80],
            'docs': docs
        }

        seen_projects[project] = session_data

    results = list(seen_projects.values())
    results.sort(key=lambda x: x['hours_ago'])
    return results


def print_sessions(sessions, show_docs=True):
    """Print formatted session table."""
    if not sessions:
        print("No sessions found matching criteria.")
        return

    print(f"\n{'#':>2} | {'Time':>8} | {'Msgs':>4} | {'Project':<25} | Summary")
    print("-" * 90)

    for i, s in enumerate(sessions[:15], 1):
        time_str = format_time_ago(s['hours_ago'])
        proj = s['short_name'][:25]
        summary = s['summary'][:40]

        print(f"{i:>2} | {time_str:>8} | {s['message_count']:>4} | {proj:<25} | {summary}")

        if show_docs and s['docs']:
            doc_names = ", ".join(d[0] for d in s['docs'][:2])
            print(f"   |          |      | {'':25} | Docs: {doc_names}")

    print("\n" + "=" * 90)
    print("SESSION DOCS FOR RECOVERY:")
    print("=" * 90)

    for i, s in enumerate(sessions[:15], 1):
        print(f"\n[{i}] {s['short_name']}")
        print(f"    Project: {s['project']}")
        print(f"    Summary: {s['summary']}")
        if s['docs']:
            for doc_name, doc_path in s['docs'][:2]:
                print(f"    Doc: file://{doc_path}")
        else:
            print(f"    Doc: (no session docs found)")


def main():
    args = sys.argv[1:]
    filter_term = None
    max_hours = DEFAULT_HOURS

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--hours" and i + 1 < len(args):
            try:
                max_hours = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        elif not arg.startswith("--"):
            filter_term = arg
            i += 1
        else:
            i += 1

    data = load_sessions()
    sessions = filter_sessions(data.get('entries', []), filter_term, max_hours)

    if filter_term:
        print(f"Sessions matching '{filter_term}' (last {max_hours}h):")
    else:
        print(f"Recent sessions (last {max_hours}h):")

    print_sessions(sessions)

    print("\n" + "-" * 90)
    print("To recover a session, tell Claude the number (e.g., 'recover session 2')")


if __name__ == "__main__":
    main()
