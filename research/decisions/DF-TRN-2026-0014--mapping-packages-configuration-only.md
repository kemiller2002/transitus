---
id: DF-TRN-2026-0014
title: "Mapping packages are configuration-only, declare their knowledge basis, require vendor licence clearance, and start as synthetic placeholders for undocumented vendors; target-side packages come first"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-09", "TRN-REV-01 C7", "ECH-020", "ECH-021"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:02.980Z
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

No invented proprietary schemas; overlays not forks; promotion requires two independent samples and disclosure plus licence review; reuse is measured and low-reuse vendor packages retired.

## Rationale and evidence

daf-landscape finds no public export schemas; iPhi MSA §3.4; review C7.

## Alternatives considered

Per-vendor code connectors (rejected); invent schemas from marketing material (prohibited).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
