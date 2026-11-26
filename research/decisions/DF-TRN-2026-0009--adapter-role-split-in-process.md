---
id: DF-TRN-2026-0009
title: "Adapters split into transport, format and destination roles as in-process F# contracts; Singer/Airbyte protocol compatibility is not built in phase 1"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-03", "TRN-RES-01", "SRC-063", "SRC-110"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:01.656Z
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

The Singer/Airbyte separation of transport, records and state is adopted as an in-process design; external connector protocols are deferred because using existing taps would introduce a Python/container runtime contrary to the single-runtime constraint. Phase-1 formats are only those Unbound release 1 needs.

## Rationale and evidence

TRN-RES-01 §3 patterns 1-3; review C11/C12 maintenance and demand findings.

## Alternatives considered

Out-of-process stdio connector protocol (deferred, could be an optional adapter later); container-per-connector (rejected).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
