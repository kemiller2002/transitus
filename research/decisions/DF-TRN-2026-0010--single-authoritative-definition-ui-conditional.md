---
id: DF-TRN-2026-0010
title: "The visual editor, if built, is a projection of the JSON definition using Forma's portable workflow capability; the administration UI is conditional on trigger T4"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-10", "TRN-REV-01 C10", "ECH-005"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:01.926Z
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

No separate visual definition can exist; layout is a non-semantic annotation. Until T4 (non-engineer configuration needed), exceptions go through the consumer's case system and pipelines are rendered read-only.

## Rationale and evidence

ECH-005 (Forma workflow exists); review C10 (fails two-scenario rule; SPR-CFG-002).

## Alternatives considered

Own graph editor (rejected: duplicates Forma); UI in phase 1 (rejected).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
