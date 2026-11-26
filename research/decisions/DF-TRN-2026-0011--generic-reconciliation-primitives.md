---
id: DF-TRN-2026-0011
title: "Transitus provides generic validation and reconciliation primitives with zero default monetary tolerance; accounting rules, tolerances and posting consequences stay in consumer-owned profiles"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-06", "ECH-014"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:02.203Z
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

Blocking gates precede any system-of-record effect; overrides are elevated authorizations recorded in evidence and never alter data; no balancing entries or silent discards; conservation law enforced per stage.

## Rationale and evidence

CNV-FIN-004 (no silent write-offs); P5, P8, P13.

## Alternatives considered

Embed Unbound accounting rules (rejected: domain leakage).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
