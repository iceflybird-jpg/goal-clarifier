#!/usr/bin/env python3
"""Persist active Goal XML and checklist for goal-clarify skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def state_dir() -> Path:
    override = os.environ.get("GOAL_STATE_DIR")
    if override:
        return Path(override).expanduser()
    agent_dir = Path.home() / ".agent" / "goal-state"
    cursor_dir = Path.home() / ".cursor" / "goal-state"
    if cursor_dir.exists() and not agent_dir.exists():
        return cursor_dir
    return agent_dir


def workspace_slug(workspace: Path) -> str:
    resolved = str(workspace.resolve())
    digest = hashlib.sha256(resolved.encode()).hexdigest()[:12]
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", workspace.name).strip("-") or "workspace"
    return f"{name}_{digest}"


def state_path(workspace: Path) -> Path:
    return state_dir() / f"{workspace_slug(workspace)}.json"


def parse_output_checklist(goal_xml: str) -> list[dict]:
    m = re.search(r"<output>(.*?)</output>", goal_xml, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        line = line.strip()
        match = re.match(r"^- \[[ xX]\]\s*(.+)$", line)
        if match:
            items.append({"criterion": match.group(1).strip(), "done": "[x]" in line.lower()[:6], "evidence": ""})
    return items


def load_state(workspace: Path) -> dict | None:
    path = state_path(workspace)
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(workspace: Path, data: dict) -> Path:
    state_dir().mkdir(parents=True, exist_ok=True)
    path = state_path(workspace)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def cmd_set(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    if args.xml_file:
        goal_xml = Path(args.xml_file).read_text(encoding="utf-8")
    elif args.xml:
        goal_xml = args.xml
    else:
        print("Error: provide --xml-file or --xml", file=sys.stderr)
        return 1

    checklist = parse_output_checklist(goal_xml)
    data = {
        "status": "active",
        "workspace": str(workspace),
        "goal_xml": goal_xml,
        "checklist": checklist,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    path = save_state(workspace, data)
    print(f"Goal saved: {path}")
    print(f"Checklist items: {len(checklist)}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    data = load_state(workspace)
    if not data:
        print("No active goal for this workspace.")
        return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    data = load_state(workspace)
    if not data:
        print("No active goal.", file=sys.stderr)
        return 1
    idx = args.index - 1
    if idx < 0 or idx >= len(data["checklist"]):
        print(f"Invalid index {args.index}", file=sys.stderr)
        return 1
    data["checklist"][idx]["evidence"] = args.text
    data["checklist"][idx]["done"] = True
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_state(workspace, data)
    print(f"Recorded evidence for item {args.index}")
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    data = load_state(workspace)
    if not data:
        print("No active goal.", file=sys.stderr)
        return 1
    pending = [i + 1 for i, c in enumerate(data["checklist"]) if not c.get("done")]
    if pending and not args.force:
        print(f"Checklist incomplete: items {pending}. Use --force to override.", file=sys.stderr)
        return 1
    data["status"] = "completed"
    data["completed_at"] = datetime.now(timezone.utc).isoformat()
    data["updated_at"] = data["completed_at"]
    save_state(workspace, data)
    print("Goal marked completed.")
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    path = state_path(workspace)
    if path.is_file():
        path.unlink()
        print(f"Cleared: {path}")
    else:
        print("No goal file to clear.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="goal-clarify state persistence")
    sub = parser.add_subparsers(dest="command", required=True)

    p_set = sub.add_parser("set", help="Save active goal XML")
    p_set.add_argument("--workspace", default=".", help="Workspace root")
    p_set.add_argument("--xml-file", help="Path to XML goal file")
    p_set.add_argument("--xml", help="Inline XML string")
    p_set.set_defaults(func=cmd_set)

    p_show = sub.add_parser("show", help="Show active goal JSON")
    p_show.add_argument("--workspace", default=".")
    p_show.set_defaults(func=cmd_show)

    p_ev = sub.add_parser("evidence", help="Record evidence for checklist item")
    p_ev.add_argument("--workspace", default=".")
    p_ev.add_argument("--index", type=int, required=True)
    p_ev.add_argument("--text", required=True)
    p_ev.set_defaults(func=cmd_evidence)

    p_done = sub.add_parser("complete", help="Mark goal completed")
    p_done.add_argument("--workspace", default=".")
    p_done.add_argument("--force", action="store_true")
    p_done.set_defaults(func=cmd_complete)

    p_clear = sub.add_parser("clear", help="Delete goal state file")
    p_clear.add_argument("--workspace", default=".")
    p_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
