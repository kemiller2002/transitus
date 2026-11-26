---
id: DF-TRN-2026-0007
title: "Transitus provides effectively-once business outcomes through deterministic idempotency keys, intent/receipt recording, declared destination guarantees, OutcomeUnknown and verification — never an exactly-once claim"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-05 §6", "ECH-001", "SRC-063", "SRC-093"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:01.136Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Transitus phase-0 decision record after adversarial review TRN-REV-01"
      evidence: [docs/reviews/adversarial-review.md]
---

# Decision Record

## Decision

Destinations declare idempotent-key, natural-upsert, query-before-write or none; ambiguity becomes OutcomeUnknown resolved by read-back or reconciliation; compensation of financial records is never automatic; command payloads carry references only.

## Rationale and evidence

Echelon.Execution OutcomeUnknown semantics; category failure mode 9 (incremental-state correctness bugs); review C8/C9.

## Alternatives considered

Exactly-once claims (rejected: not achievable across external systems).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
