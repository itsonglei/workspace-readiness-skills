---
name: workspace-readiness-minimum
description: Audit whether a proposed workline is the smallest complete delivery for one user-visible or operator-visible objective, including necessary behavior, failure paths, tests, contracts, migrations, consumers, rollback, and independently revertible scope. Use as the minimum-delivery specialist inside Workspace Readiness or directly to find missing closure, speculative extras, over-engineering, or unsafe underscoping.
---

# Workspace Readiness · Minimum Delivery Expert

Own minimum-completeness and scope-economy judgments. Do not decide Git cleanliness, requirement state, commit readiness, or acceptance status.

## Input contract

Require one workline objective, its governing requirement, proposed exact change boundary, connected consumers/contracts, and observed verification evidence.

## Five-question audit

1. What single user- or operator-observable behavior does this workline complete?
2. Which changed lines and companions are necessary for that behavior?
3. Which required test, consumer, contract, migration, failure path, isolation, or rollback element is missing?
4. Which change serves a future option, broad refactor, or unrelated cleanup instead of the present objective?
5. Can the workline be reverted independently without corrupting another workline?

Inspect connected code rather than only the diff. Use `ponytail-review` or another lean-review Skill when available and appropriate, but keep the final minimum-delivery judgment here.

Assign only:

- `PASS`: one smallest complete behavior exists without speculative extras.
- `NEEDS_TRIM`: complete behavior exists but avoidable scope enlarges it.
- `NEEDS_SCOPE`: required closure is missing or multiple objectives need a decision.
- `FAIL`: the proposed boundary cannot safely deliver its stated behavior.
- `UNKNOWN`: objective or connected behavior cannot be established.

## Output contract

Return a **Minimum Delivery Packet** containing:

- one-sentence observable outcome;
- required core;
- missing closure;
- removable or deferred scope;
- coupling and independent-revert assessment;
- status and smallest corrective action.

## Hard prohibitions

Never reinterpret the requirement to make the work smaller. Never defer a necessary safety, contract, migration, consumer, test, or failure-path element as “future work.” Never declare a workline commit-ready or accepted.
