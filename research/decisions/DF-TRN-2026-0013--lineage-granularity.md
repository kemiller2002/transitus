---
id: DF-TRN-2026-0013
title: "Lineage is L0 execution + L1 chunk + L2 record for system-of-record loads, with static field-level lineage per pipeline version; no per-field value storage; personal natural keys HMAC'd"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-08", "TRN-REV-01 C8"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:02.724Z
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

Field-level lineage is a property of the pipeline version and is re-derivable from preserved raw input; record lineage costs ≈400-600 B per record indexed (revised), plus Echelon.Execution rows that must be counted and purged.

## Rationale and evidence

TRN-ARCH-08 cost model; review C8.

## Alternatives considered

Per-field value lineage (rejected: 20-50x storage); dataset-only lineage (rejected: insufficient for financial traceability).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
