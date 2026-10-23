---
name: workspace-readiness-acceptance
description: Judge whether a workline has an authoritative acceptance contract, satisfied prerequisites, and current evidence across source, tests, build, database, runtime, API, browser, release artifact, environment configuration, deployment, and business layers. Use as the acceptance specialist inside Workspace Readiness or directly to distinguish accepted, ready to accept, partial, blocked, not ready, not applicable, and unknown without running unauthorized acceptance.
---

# Workspace Readiness · Acceptance Expert

Own acceptance scope, evidence layers, and readiness. Do not decide Git cleanliness, requirement completion, or commit composition.

## Input contract

Require the target workline, Requirement Ledger Packet, governing acceptance artifacts, implementation/release identity when applicable, and already-observed verification evidence.

## Procedure

1. Identify the authoritative acceptance contract, target environment, entry point, data/identity prerequisites, expected result, isolation, and rollback.
2. Separate evidence into: source/static, unit, integration, build/typecheck, database/migration, local runtime, API, browser/UI, release artifact, environment configuration, deployment, and business acceptance.
3. Check evidence freshness and identity: branch/commit, schema, release artifact, environment configuration, target environment, execution, identity, and timestamp where relevant.
4. Mark missing layers `NOT RUN` or `UNKNOWN`; never upgrade local tests into deployment or business proof.
5. Use an independent QA Skill when a second evidence judgment is useful. Browser, authenticated, database-writing, deployment, shared-environment, and business acceptance require explicit authority.

Assign only:

- `ACCEPTED`
- `READY_TO_ACCEPT`
- `PARTIAL`
- `NOT_READY`
- `BLOCKED`
- `NOT_APPLICABLE`
- `UNKNOWN`

`READY_TO_ACCEPT` means prerequisites are ready; it does not mean the acceptance run passed.

## Output contract

Return an **Acceptance Evidence Packet**:

| Layer | Required | Evidence identity | Result | Freshness | Gap |
|---|---|---|---|---|---|

Then state the overall acceptance status, the smallest safe next acceptance action, and any permission/environment blocker.

## Hard prohibitions

Never initiate remote, browser, authenticated, database-writing, release-configuration, deployment, or business acceptance without explicit authorization. Never convert a successful execution, merged code, or local tests into broader acceptance claims.
