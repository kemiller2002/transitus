---
id: DF-TRN-2026-0006
title: "Durable execution uses Echelon.Execution, in place inside Unbound for phase 1; extraction to a shared component is proposed only when trigger T2 fires"
status: superseded
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: medium
supersedes: []
superseded_by: [DF-TRN-2026-0021]
evidence: ["ECH-001", "ECH-002", "TRN-ARCH-05", "TRN-REV-01 C12"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:00.861Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Transitus phase-0 decision record after adversarial review TRN-REV-01"
      evidence: [docs/reviews/adversarial-review.md]
    EXE-20261126T181704540Z-e41ec7a0:
      operations: [superseded]
      at: 2026-11-26T18:20:45.767Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Superseded by owner-directed decision"
---

# Decision Record

## Decision

Transitus does not build a queue, scheduler loop, lease manager or outbox. Phase-1 feed modules submit Unbound's own Echelon.Execution operations. At T2 the engine becomes Echelon.Execution's second consumer and extraction (DEP-EXEC-01) is proposed with the gaps G1-G4.

## Rationale and evidence

unbound/execution/README.md provides intake, idempotency, ordering, leases, retries, quarantine, OutcomeUnknown, approval waits; it is unbenchmarked (RM-05), so early extraction is premature (review C12).

## Alternatives considered

Own queue (rejected: duplication); immediate extraction (deferred).

## Status

Superseded by DF-TRN-2026-0021 (owner direction, 2026-11-26).


Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
