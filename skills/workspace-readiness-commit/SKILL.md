---
name: workspace-readiness-commit
description: Partition staged, unstaged, committed-local, and stashed workspace changes into independently committable worklines and judge local commit readiness. Use as the commit-curation specialist inside Workspace Readiness or directly when a mixed worktree must be separated by objective, contracts, migrations, tests, consumers, generated files, or hunks without staging or committing anything.
---

# Workspace Readiness · Commit Expert

Own workline boundaries and local commit readiness. Do not determine whether a requirement is finished or whether runtime/business acceptance passed.

## Input contract

Require a Git Evidence Packet, Requirement Ledger Packet, exact diff or commit range, and applicable project instructions. If either packet is missing, collect only the minimum needed facts and label unresolved attribution `UNKNOWN`.

## Procedure

1. Partition by one explicit objective, not by directory alone.
2. Keep production code with required tests, contracts, schemas, migrations, generated files, and consumers.
3. Split unrelated formatting, experiments, logs, screenshots, and pre-existing edits.
4. Refuse a split that creates an uncompilable, unsafe, contract-inconsistent, or misleading intermediate commit.
5. Inspect exact paths and hunks. List inclusions, exclusions, dependencies, and commands already observed.
6. Use a repository-aware review Skill when correctness or security review is required. Treat its findings as evidence, not as authority over requirement or acceptance state.

Assign only:

- `READY`
- `NEEDS_SPLIT`
- `NEEDS_REVIEW`
- `NEEDS_VERIFICATION`
- `BLOCKED`
- `NO_CHANGES`
- `UNKNOWN`

`READY` means ready for one local commit only. It does not mean ready to push, merge, deploy, or accept.

## Output contract

Return a **Commit Workline Packet**:

| Workline | Objective/source | Include paths or hunks | Required companions | Exclude | Dependencies | Observed checks | Status | Blocker |
|---|---|---|---|---|---|---|---|---|

List `UNATTRIBUTED` changes separately. For `NEEDS_SPLIT`, provide an exact proposed partition. For locally committed branches, say `NO_CHANGES` for new commit work and report branch-promotion prerequisites separately.

## Hard prohibitions

Never stage, commit, amend, switch branches, apply stashes, push, merge, rebase, or edit files. Never call a commit accepted or a requirement done.
