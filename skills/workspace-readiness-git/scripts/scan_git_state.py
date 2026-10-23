#!/usr/bin/env python3
"""Run the shared deterministic Workspace Readiness Git collector."""

from pathlib import Path
import runpy


COLLECTOR = (
    Path(__file__).resolve().parents[2]
    / "workspace-readiness"
    / "scripts"
    / "scan_git_state.py"
)

if not COLLECTOR.is_file():
    raise SystemExit(f"shared Git collector not found: {COLLECTOR}")

runpy.run_path(str(COLLECTOR), run_name="__main__")
