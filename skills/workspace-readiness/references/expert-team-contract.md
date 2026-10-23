# Workspace Readiness Expert Team Contract

## Team roster

| Specialist | Owns | Must not decide |
|---|---|---|
| `$workspace-readiness-git` | Git roots, paths, diffs, lineage, conflicts, stashes, attribution facts | Requirement, commit quality, acceptance, minimum delivery |
| `$workspace-readiness-requirements` | Requirement identity, governing source, `DONE/OPEN/BLOCKED/UNKNOWN` | Git cleanliness, commit boundary, acceptance |
| `$workspace-readiness-commit` | Independent worklines and local commit readiness | Requirement completion, deployment, acceptance |
| `$workspace-readiness-acceptance` | Acceptance contract, layers, prerequisites, evidence freshness | Git state, commit composition, requirement state |
| `$workspace-readiness-minimum` | Smallest complete behavior, missing closure, removable scope | Git state, requirement state, commit or acceptance status |
| `$workspace-readiness` | Scope, dispatch, packet correlation, conflict arbitration, final report | Replacing a specialist's domain analysis |

## Packet rules

Every specialist packet must include:

1. specialist name and inspected scope;
2. authoritative and supporting evidence;
3. observed facts separated from inference;
4. exact status using only that specialist's vocabulary;
5. `UNKNOWN` items and contradictions;
6. smallest next evidence needed;
7. prohibited conclusions.

Use stable workline IDs so packets can be joined without matching on filenames or titles alone. The orchestrator creates the initial IDs after Git and requirement discovery; specialists may propose a split but must not silently rename or merge IDs.

## Arbitration rules

- Requirement authority outranks branch names and diff inference.
- Direct evidence outranks summaries, but only for the layer it actually proves.
- A specialist may challenge another packet by recording a contradiction; it may not rewrite the other specialist's status.
- The orchestrator preserves both claims and resolves them using the governing source. If authority remains unclear, the consolidated result is `UNKNOWN`.
- No `READY`, `ACCEPTED`, or `DONE` status propagates into another column automatically.

## Execution boundary

Default expert-team scans are read-only. Parallel specialists may inspect the same raw evidence but must not receive another specialist's conclusion as ground truth. If subagents are unavailable or not authorized, run the same specialist passes sequentially and keep their packets separate before consolidation.
