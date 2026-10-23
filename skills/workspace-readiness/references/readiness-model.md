# Readiness Model

Use these vocabularies exactly so that “can commit,” “can accept,” and “done” do not collapse into one claim.

## Evidence precedence

When sources disagree, prefer the source that governs the claim and the newest direct evidence:

1. Current explicit user decision and active project instructions.
2. Authoritative specification, task, verification, closeout, contract, or other governing artifact.
3. Direct repository, test, runtime, browser, database, release-artifact, environment-configuration, or deployment evidence.
4. Current or prior task final reports and workspace session summaries.
5. Inference from diffs, filenames, timestamps, or branch names.

Lower evidence may locate a workline but cannot override a contradictory governing source. Git proves changes and history; it does not prove user intent, requirement completion, deployment, or business acceptance.

## Workspace state

- `CLEAN`: no staged, unstaged, untracked, or conflicted paths in the inspected Git root.
- `DIRTY_SCOPED`: all changes are attributed to one workline or an explicitly defined compatible set.
- `DIRTY_MIXED`: changes belong to multiple worklines or include unattributed changes.
- `CONFLICTED`: unresolved Git conflicts exist.
- `UNKNOWN`: the root or status could not be inspected reliably.

## Requirement state

- `DONE`: the governing source marks the objective complete and required evidence does not contradict it.
- `OPEN`: explicit applicable work remains.
- `BLOCKED`: explicit work remains but a named decision, permission, environment, or dependency prevents progress.
- `UNKNOWN`: intent, governing source, attribution, or completion evidence is missing or contradictory.

Do not derive this state from clean/dirty Git status alone.

## Commit readiness

- `READY`: the exact paths or hunks form one coherent minimum change, contain required companions, have no unresolved conflicts or blocking review findings, and have proportionate local evidence.
- `NEEDS_SPLIT`: useful work is present but mixed with another objective or unrelated edits; provide an exact proposed partition.
- `NEEDS_REVIEW`: the boundary is isolated but correctness, security, compatibility, or minimum-delivery review is missing.
- `NEEDS_VERIFICATION`: the boundary is isolated and reviewed, but a required local check is missing or failing.
- `BLOCKED`: conflicts, secrets, destructive/generated artifacts, missing required consumers/migrations/contracts, or an inseparable broken intermediate state make a safe commit inappropriate.
- `NO_CHANGES`: no implementation change belongs to the workline.
- `UNKNOWN`: attribution or evidence is insufficient.

`READY` means ready for a local commit. It does not imply ready to push, merge, deploy, or accept.

## Acceptance readiness

- `ACCEPTED`: the applicable acceptance layers were actually run in the required environment with current evidence and passed.
- `READY_TO_ACCEPT`: prerequisites, target, entry point, data, and expected result are defined; acceptance itself has not necessarily run.
- `PARTIAL`: some required layers passed, while others are missing, stale, or failed.
- `NOT_READY`: implementation or prerequisites are incomplete.
- `BLOCKED`: acceptance is defined but a named permission, environment, dependency, or external state prevents it.
- `NOT_APPLICABLE`: the workline has no acceptance obligation beyond already-recorded local checks.
- `UNKNOWN`: no authoritative acceptance contract or sufficient evidence was found.

Report applicable layers separately: source/static, unit, integration, build/typecheck, database/migration, local runtime, API, browser/UI, release artifact, environment configuration, deployment, and business acceptance.

## Minimum delivery

- `PASS`: one smallest complete behavior satisfies the objective and includes required error handling, tests, contracts, and consumers without speculative extras.
- `NEEDS_TRIM`: the complete behavior exists but avoidable abstractions, options, refactors, or unrelated cleanup enlarge the change.
- `NEEDS_SCOPE`: the diff omits a necessary part of the smallest complete behavior or mixes several objectives that need a decision.
- `FAIL`: the proposed boundary cannot deliver its stated behavior safely.
- `UNKNOWN`: the objective or connected behavior cannot be established.

Ask five questions:

1. What user- or operator-observable behavior does this workline complete?
2. Which changed lines are required for that behavior?
3. Which required tests, consumers, contracts, migrations, failure paths, or rollback steps are missing?
4. Which lines implement a future option rather than the present objective?
5. Can the workline be reverted independently without corrupting another workline?

## Workline split rules

An independently committable workline must have:

- one explicit objective and evidence source;
- an exact path or hunk set;
- all required production, test, schema, contract, generated, and consumer changes;
- no reliance on unstaged leftovers to compile or behave correctly;
- no hidden dependency on an unrelated workline;
- a truthful verification statement.

Do not split merely to make commits smaller when doing so creates an invalid contract, uncompilable intermediate state, unsafe migration order, or misleading review boundary.

## Report example

```text
Overall: mixed workspace; one exact workline is commit-ready, two requirements remain UNKNOWN.

| Workline | Sources | Repositories / changes | Requirement | Commit | Acceptance | Minimum delivery | Blocker / next action |
| ... |

Verification layers
- Source/static: PASS — <observed command/evidence>
- Browser/UI: NOT RUN — requires explicit authorization
```
