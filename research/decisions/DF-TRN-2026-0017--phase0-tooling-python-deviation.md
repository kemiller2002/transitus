---
id: DF-TRN-2026-0017
title: "The phase-0 requirements renderer is a small Python standard-library script because no .NET SDK was available in the authoring environment; it is to be ported to F# in phase 1"
status: review
decision_type: process
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["tools/render_requirements.py"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:03.812Z
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

Echelon conventions prefer F# tooling (Unbound ported its Python validators to F#). The renderer is deterministic, has a --check mode, and has no third-party dependencies; porting is phase-1 work item 1.

## Rationale and evidence

Authoring environment had no dotnet (observed 2026-11-26).

## Alternatives considered

Hand-maintain three views (rejected: drift); wait for .NET (rejected: blocks deliverable).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
