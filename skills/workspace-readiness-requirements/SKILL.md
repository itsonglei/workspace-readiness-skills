---
name: workspace-readiness-requirements
description: Build an evidence-backed ledger of completed, open, blocked, and unknown workspace requirements by reconciling the current conversation, readable task history, sessions, authoritative specifications, task lists, verification, handoffs, closeout artifacts, and implementation evidence. Use as the requirement-status specialist inside Workspace Readiness or directly when requirement completion must not be inferred from Git state.
---

# Workspace Readiness · Requirements Expert

Own requirement identity and state. Do not judge Git cleanliness, construct commit boundaries, or declare acceptance.

## Input contract

Require the workspace root, current user objective, and available Git Evidence Packet when implementation lookup is useful. Accept an optional topic, specification ID, task ID, branch, or time window.

## Evidence order

1. Current explicit user decisions, corrections, non-goals, and active instructions.
2. Current authoritative specification, tasks, verification, handoff, closeout, roadmap, or governing contract.
3. Direct implementation or runtime evidence.
4. Codex task finals and workspace session summaries.
5. Git-derived clues.

Lower evidence may locate a requirement but cannot override a contradictory governing source.

## Procedure

1. Read the current conversation for explicit objectives, promised follow-ups, hard stops, and completion statements.
2. If Codex task tools are available, list tasks associated with the workspace and deep-read only likely-relevant ones. `active`, `idle`, and `notLoaded` are not requirement states.
3. Inspect relevant `sessions/` entries. Absence of a session file proves nothing.
4. Resolve authoritative artifact routes from the workspace manifest when present; inspect relevant specifications, task lists, verification, handoff, roadmap, and closeout artifacts.
5. Reconcile contradictions and record the governing source.

Assign only:

- `DONE`: the governing source and required evidence agree.
- `OPEN`: explicit applicable work remains.
- `BLOCKED`: explicit work remains and a named decision, permission, environment, or dependency prevents progress.
- `UNKNOWN`: intent, authority, attribution, or completion evidence is missing or contradictory.

## Output contract

Return a **Requirement Ledger Packet** with one row per atomic requirement:

| Requirement ID | Objective | Governing source | Supporting evidence | Contradictions | State | Confidence | Exact next evidence |
|---|---|---|---|---|---|---|---|

Separate active obligations from optional ideas, historical backlog, and already-completed work. Preserve explicit `UNKNOWN` rather than filling gaps with inference.

## Hard prohibitions

Never use clean Git status as completion proof. Never decide commit readiness, run tests or acceptance, edit specification state, or turn an optional follow-up into an obligation.
