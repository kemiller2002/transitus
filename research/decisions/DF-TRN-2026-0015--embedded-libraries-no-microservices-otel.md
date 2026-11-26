---
id: DF-TRN-2026-0015
title: "Transitus is distributed as F# libraries hosted by the consumer (component monolith); no microservice; operational telemetry via OpenTelemetry through the host; Vigila used only for optional follow-ups"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-11", "ECH-008", "ECH-009", "ECH-016"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:03.236Z
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

Charter direction; registry finds runtime monitoring unowned (GAP-05) and Vigila is a follow-up tracker, so Transitus does not build monitoring and escalates the owner question.

## Rationale and evidence

ECH-008, ECH-009; ADR-EVA-001/CNV-ARC-001.

## Alternatives considered

Separate integration service (rejected without explicit approval); build a monitoring stack (rejected).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
