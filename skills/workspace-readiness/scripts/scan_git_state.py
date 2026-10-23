#!/usr/bin/env python3
"""Collect read-only Git state for a workspace and its registered members."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_git(path: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", os.fspath(path), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def find_workspace(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "workspace.yaml").is_file():
            return candidate
    result = run_git(current, "rev-parse", "--show-toplevel")
    if result.returncode == 0:
        return Path(result.stdout.decode("utf-8", "replace").strip()).resolve()
    raise RuntimeError(f"no workspace.yaml or Git root found from {current}")


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def read_members(workspace_file: Path) -> list[dict[str, str]]:
    if not workspace_file.is_file():
        return []

    members: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_members = False
    for raw_line in workspace_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line == "members:":
            in_members = True
            continue
        if in_members and line and not line.startswith(" "):
            break
        if not in_members or not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- id:"):
            if current and current.get("path"):
                members.append(current)
            current = {"id": unquote_yaml_scalar(stripped.split(":", 1)[1])}
        elif current is not None and stripped.startswith("path:"):
            current["path"] = unquote_yaml_scalar(stripped.split(":", 1)[1])
    if current and current.get("path"):
        members.append(current)
    return members


def decode(value: bytes) -> str:
    return value.decode("utf-8", "replace")


def parse_status(raw: bytes) -> dict[str, Any]:
    records = raw.split(b"\0")
    branch: dict[str, Any] = {
        "head": None,
        "oid": None,
        "upstream": None,
        "ahead": None,
        "behind": None,
    }
    changes: list[dict[str, Any]] = []
    index = 0

    while index < len(records):
        text = decode(records[index])
        index += 1
        if not text:
            continue
        if text.startswith("# branch.head "):
            branch["head"] = text[len("# branch.head ") :]
            continue
        if text.startswith("# branch.oid "):
            branch["oid"] = text[len("# branch.oid ") :]
            continue
        if text.startswith("# branch.upstream "):
            branch["upstream"] = text[len("# branch.upstream ") :]
            continue
        if text.startswith("# branch.ab "):
            fields = text[len("# branch.ab ") :].split()
            for field in fields:
                if field.startswith("+"):
                    branch["ahead"] = int(field[1:])
                elif field.startswith("-"):
                    branch["behind"] = int(field[1:])
            continue
        if text.startswith("? "):
            changes.append(
                {"path": text[2:], "kind": "untracked", "index": "?", "worktree": "?"}
            )
            continue
        if text.startswith("! "):
            continue

        record_type = text[0]
        if record_type not in {"1", "2", "u"}:
            changes.append({"path": None, "kind": "unknown", "raw": text})
            continue

        if record_type == "1":
            maxsplit = 8
        elif record_type == "2":
            maxsplit = 9
        else:
            maxsplit = 10
        fields = text.split(" ", maxsplit)
        xy = fields[1] if len(fields) > 1 else "??"
        path = fields[-1] if fields else None
        change: dict[str, Any] = {
            "path": path,
            "kind": "conflict" if record_type == "u" else "tracked",
            "index": xy[0] if len(xy) > 0 else "?",
            "worktree": xy[1] if len(xy) > 1 else "?",
        }
        if record_type == "2":
            if index < len(records):
                change["original_path"] = decode(records[index])
                index += 1
            change["kind"] = "renamed_or_copied"
        changes.append(change)

    staged = [c["path"] for c in changes if c.get("index") not in {".", "?", None}]
    unstaged = [c["path"] for c in changes if c.get("worktree") not in {".", "?", None}]
    untracked = [c["path"] for c in changes if c.get("kind") == "untracked"]
    conflicts = [
        c["path"]
        for c in changes
        if c.get("kind") == "conflict"
        or "U" in {c.get("index"), c.get("worktree")}
        or (c.get("index"), c.get("worktree")) in {("A", "A"), ("D", "D")}
    ]
    return {
        "branch": branch,
        "clean": not changes,
        "counts": {
            "staged": len(staged),
            "unstaged": len(unstaged),
            "untracked": len(untracked),
            "conflicts": len(conflicts),
        },
        "staged_paths": staged,
        "unstaged_paths": unstaged,
        "untracked_paths": untracked,
        "conflict_paths": conflicts,
        "changes": changes,
    }


def inspect_repository(candidate: Path, labels: list[str]) -> dict[str, Any]:
    top = run_git(candidate, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        return {
            "candidate": os.fspath(candidate),
            "labels": labels,
            "status": "UNKNOWN",
            "error": decode(top.stderr).strip() or "not a Git worktree",
        }

    root = Path(decode(top.stdout).strip()).resolve()
    status = run_git(
        root,
        "status",
        "--porcelain=v2",
        "--branch",
        "-z",
        "--untracked-files=all",
    )
    if status.returncode != 0:
        return {
            "path": os.fspath(root),
            "labels": labels,
            "status": "UNKNOWN",
            "error": decode(status.stderr).strip() or "git status failed",
        }

    parsed = parse_status(status.stdout)
    parsed.update(
        {
            "path": os.fspath(root),
            "labels": labels,
            "status": "CLEAN" if parsed["clean"] else "DIRTY",
        }
    )
    return parsed


def collect(workspace: Path) -> dict[str, Any]:
    workspace_file = workspace / "workspace.yaml"
    members = read_members(workspace_file)
    candidates: list[tuple[Path, str]] = [(workspace, "workspace")]
    candidates.extend((workspace / member["path"], member["id"]) for member in members)

    repositories_by_root: dict[str, dict[str, Any]] = {}
    unresolved: list[dict[str, Any]] = []
    for candidate, label in candidates:
        if not candidate.exists():
            unresolved.append(
                {
                    "candidate": os.fspath(candidate),
                    "labels": [label],
                    "status": "UNKNOWN",
                    "error": "path does not exist",
                }
            )
            continue
        inspected = inspect_repository(candidate, [label])
        root = inspected.get("path")
        if root and root in repositories_by_root:
            labels = repositories_by_root[root]["labels"]
            if label not in labels:
                labels.append(label)
        elif root:
            repositories_by_root[root] = inspected
        else:
            unresolved.append(inspected)

    repositories = sorted(repositories_by_root.values(), key=lambda item: item["path"])
    return {
        "workspace": os.fspath(workspace),
        "workspace_file": os.fspath(workspace_file) if workspace_file.is_file() else None,
        "members": members,
        "summary": {
            "repositories": len(repositories),
            "clean": sum(repo.get("status") == "CLEAN" for repo in repositories),
            "dirty": sum(repo.get("status") == "DIRTY" for repo in repositories),
            "unknown": len(unresolved),
        },
        "repositories": repositories,
        "unresolved": unresolved,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read Git state for a workspace and registered workspace.yaml members."
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace path or a descendant path (default: current directory).",
    )
    args = parser.parse_args()
    try:
        workspace = find_workspace(Path(args.workspace))
        result = collect(workspace)
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
