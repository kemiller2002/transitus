---
id: DF-TRN-2026-0004
title: "Transformations are pure, total, versioned operations with explicit culture/zone/rounding parameters, a typed total expression language, and bounded set operators"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-04", "TRN-REV-01 C4"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:00.308Z
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

Operations are name@major, return typed errors, never read ambient state, and declare reversibility and information loss. Bounded set operators (ordered scan, as-of join, fiscal periods, unpivot, bounded explode, clustering, linear-time regex capture) are added after review.

## Rationale and evidence

Determinism contract (P4); financial precision (TX-005); review C4 counter-examples.

## Alternatives considered

Allow ambient culture (rejected: non-reproducible); general-purpose language (rejected: P1).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
