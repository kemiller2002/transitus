---
id: DF-TRN-2026-0005
title: "No user-supplied code, SQL or script in pipelines; extension only via reviewed, signed, allow-listed compiled F# packages with capability-free signatures"
status: review
decision_type: security
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-SEC-01 T14", "TRN-REV-01 C4", "ECH-011"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:00.579Z
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

Because .NET cannot sandbox in-process code, extension safety rests on two-person review, conformance testing, signing/hash pinning, allow-listing and pure signatures. Set-level extensions are permitted when the catalogue cannot express a demonstrated scenario and are recorded to drive catalogue evolution.

## Rationale and evidence

Threat T14; Echelon SEC-DB-001; review C4.

## Alternatives considered

Embedded scripting (rejected); out-of-process sandboxed plugins (deferred: adds a runtime/process model).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
