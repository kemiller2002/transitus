---
id: DF-TRN-2026-0016
title: "Phase 1 is three pure libraries (Formats, Checks, Evidence) serving Unbound release-1 feeds; later phases require recorded triggers T2-T4; a phase-1 exit review compares against hand-written per-feed modules"
status: superseded
decision_type: process
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: medium
supersedes: []
superseded_by: [DF-TRN-2026-0018]
evidence: ["TRN-REV-01", "docs/roadmap.md"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:03.512Z
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
      at: 2026-11-26T18:20:44.907Z
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

Phase 1 traces every item to Unbound release-1 scope; maintenance budget of three packages; T2 = committed second consumer or demonstrated duplication across >=3 feeds or non-engineer authoring; T3 = contracted migration with authorized sample plus AI evaluation; T4 = non-engineer configuration. Kill: if per-feed modules are cheaper and no second consumer commits, the engine is not built.

## Rationale and evidence

All four adversarial reviews converged on a smaller first step (TRN-REV-01).

## Alternatives considered

Build all phases (rejected: C3, C11, C12); build only inside Unbound with no separate repository (not adopted: brief directs a domain-independent component; escalated as OQ-14).

## Status

Superseded by DF-TRN-2026-0018 (owner direction, 2026-11-26).


Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
