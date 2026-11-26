---
id: DF-TRN-2026-0012
title: "AI may only propose pipeline diffs; the runtime path contains no model calls; enablement is gated on measured mapping precision"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-07", "TRN-SEC-01", "TRN-REV-01 C6"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:02.477Z
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

Proposals pass the same validation, dry run and approval as human changes plus semantic-critical review; profile statistics are masked by classification; annotations excluded from AI context; AI is phase 3.

## Rationale and evidence

Threats T09/T23; review C6.

## Alternatives considered

AI in the transformation path (rejected: non-deterministic, costly); ungated AI suggestions (rejected).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
