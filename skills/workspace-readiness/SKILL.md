---
name: workspace-readiness
description: Orchestrate a read-only Workspace Readiness expert team that separately audits Git state, unfinished requirements, independent commit worklines, acceptance readiness, and minimum-delivery quality, then reconciles their evidence into one decision table. Use when the user asks for a full workspace delivery inventory, wants mixed work separated safely, or needs precise boundaries between what is dirty, unfinished, committable, acceptable, and minimally complete.
---

# Workspace Readiness Expert Team

Act only as the lead coordinator. Do not collapse Git cleanliness, requirement completion, commit readiness, acceptance, and minimum delivery into one judgment.

Read [expert-team-contract.md](references/expert-team-contract.md) and [readiness-model.md](references/readiness-model.md) completely before dispatching specialists.

## Preserve the boundary

- Default to `scan`: inspect and classify only. Never stage, commit, push, switch branches, edit project files, deploy, create release artifacts or environment configurations, start authenticated executions, or perform browser/database/business acceptance.
- Follow active project instructions, workspace manifests, repository-specific rules, and authoritative project artifacts.
- Preserve unrelated dirty work. Never clean, reset, apply stashes, or force branch changes.
- Treat unavailable or contradictory evidence as `UNKNOWN`.
- A clean repository does not prove a requirement is done. A passing local test does not prove deployment or business acceptance.

## Select one mode

- `scan` (default): run the complete expert team and inventory relevant worklines.
- `git`: run only the Git expert.
- `requirements [topic]`: run Git discovery as needed, then the Requirements expert.
- `commit <workline>`: run Git, Requirements, Commit, and Minimum Delivery experts for one workline.
- `accept <workline>`: run Requirements, Acceptance, and Minimum Delivery experts; add Git when source identity matters.
- `verify <workline>`: first run the relevant experts, then execute only local checks explicitly authorized by the user. Every external or state-changing acceptance layer requires separate authority.

Do not widen a mode silently. If no workline is named, use `scan` and recommend one smallest next action.

## Dispatch the team

Load the selected specialist Skill files completely before their pass:

1. `$workspace-readiness-git` — `../workspace-readiness-git/SKILL.md`
2. `$workspace-readiness-requirements` — `../workspace-readiness-requirements/SKILL.md`
3. `$workspace-readiness-commit` — `../workspace-readiness-commit/SKILL.md`
4. `$workspace-readiness-acceptance` — `../workspace-readiness-acceptance/SKILL.md`
5. `$workspace-readiness-minimum` — `../workspace-readiness-minimum/SKILL.md`

Use specialist agents when the environment permits, the user authorized expert-team/delegated work, and the scope benefits from independent passes. Otherwise execute the same passes sequentially. Give specialists the raw scope and evidence locations, not another specialist's conclusions. Require their named packet output.

For a full `scan`:

1. Git Expert produces the Git Evidence Packet.
2. Requirements Expert independently produces the Requirement Ledger Packet.
3. Create stable workline IDs by correlating explicit objectives with attributable changes. Preserve `UNATTRIBUTED` separately.
4. Commit Expert consumes Git facts, requirement sources, and exact diffs.
5. Acceptance Expert consumes governing acceptance artifacts and observed evidence.
6. Minimum Delivery Expert inspects each active or proposed workline.
7. Reconcile packets without overwriting specialist statuses.

## Route helper skills

Specialists may use narrower helpers only inside their domain:

- Commit Expert: project quality gates and repository-aware code review.
- Acceptance Expert: independent QA, project verification matrices, and—only with authorization—browser or external-system QA.
- Minimum Delivery Expert: `ponytail-review` or an equivalent lean implementation review.
- Requirements Expert: project-specific specification and status readers.

Helpers provide evidence; they do not replace the named specialist or expand permissions. Do not invoke write-capable reconciliation flows during `scan`.

## Reconcile conflicts

Use this precedence:

1. current explicit user decision and active instructions;
2. current routed governing artifacts;
3. direct evidence for the exact claimed layer;
4. task/session summaries;
5. Git inference.

Examples:

- Git `CLEAN` + unchecked authoritative task → requirement remains `OPEN`.
- Commit `READY` + acceptance environment missing → acceptance may be `BLOCKED`.
- Tests pass + missing consumer → minimum delivery may be `NEEDS_SCOPE` and commit may be `BLOCKED`.
- Task says done + routed verification contradicts it → requirement is `UNKNOWN` until resolved.

## Report

Lead with one overall result, then render:

| Workline ID | Objective / sources | Git | Requirement | Commit | Acceptance | Minimum delivery | Contradiction / next action |
|---|---|---|---|---|---|---|---|

Follow with:

- **Workspace cleanliness** — every inspected and unavailable Git root.
- **Unfinished and unknown requirements** — governing evidence, never Git alone.
- **Commit candidates** — exact paths/hunks, companions, exclusions, and observed checks.
- **Acceptance candidates** — existing evidence versus ready-to-run versus not run.
- **Minimum-delivery findings** — required closure and removable scope.
- **Unattributed changes and contradictions**.
- **Next action** — one smallest action that improves readiness.

Use only the vocabularies defined in `readiness-model.md`. State which specialists ran, which were unavailable, whether they ran independently or sequentially, and which helper Skills were used.
