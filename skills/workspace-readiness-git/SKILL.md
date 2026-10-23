---
name: workspace-readiness-git
description: Collect read-only Git topology and change facts for a workspace, including registered repositories, clean or dirty state, branch lineage, staged and unstaged paths, untracked files, conflicts, local-only branches, stashes, and exact diffs. Use as the Git specialist inside Workspace Readiness or directly when the user needs repository facts without requirement, commit-quality, minimum-delivery, or acceptance conclusions.
---

# Workspace Readiness · Git Expert

Own only Git facts. Do not decide whether a user requirement is done, a change is correct, a commit is desirable, or acceptance passed.

## Input contract

Require a workspace path or resolve the nearest `workspace.yaml` or Git root. Accept an optional workline name, branch, commit range, or path filter.

Read the applicable `AGENTS.md` and `workspace.yaml` only to resolve repository topology and safety boundaries. Never treat branch names, commit subjects, clean status, or filenames as proof of intent or completion.

## Procedure

1. Run the shared deterministic collector:

   ```bash
   python3 <skill-dir>/scripts/scan_git_state.py --workspace <workspace-root>
   ```

2. Inspect exact staged, unstaged, untracked, and conflicted paths for relevant repositories.
3. When requested, inspect branch ancestry, upstream tracking, ahead/behind counts, local-only commits, stash names, and stash path summaries. Do not fetch or mutate remotes in a read-only scan.
4. Attribute a path to a workline only when an authoritative source or connected diff supports the attribution. Otherwise label it `UNATTRIBUTED`.
5. Classify each Git root as `CLEAN`, `DIRTY_SCOPED`, `DIRTY_MIXED`, `CONFLICTED`, or `UNKNOWN`.

## Output contract

Return a **Git Evidence Packet** containing:

- inspected roots and unresolved roots;
- branch, HEAD, upstream and locally observed ahead/behind facts;
- staged, unstaged, untracked and conflict paths;
- relevant local-only branch and stash facts;
- proposed path/hunk attribution with confidence and evidence;
- explicit `UNKNOWN` facts and inspection errors.

End with `Prohibited conclusions` stating that this packet does not prove requirement completion, commit readiness, deployment, or acceptance.

## Hard prohibitions

Never stage, commit, switch branches, apply or drop stashes, reset, clean, fetch, pull, push, merge, rebase, or edit files. Never output `DONE`, `READY`, `ACCEPTED`, or minimum-delivery judgments.
