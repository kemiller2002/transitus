---
id: DF-TRN-2026-0002
title: "Phase-2 pipeline definitions are versioned canonical JSON (RFC 8785) interpreted against an F# discriminated-union model; published versions are immutable and identified by content hash"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-01", "TRN-RES-01", "SRC-030", "SRC-032", "SRC-061"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:41:59.705Z
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

Pipelines are data. The F# DU model is normative; canonical JSON is the stored, hashed, diffable artifact; YAML is accepted only as input and converted. Annotations (layout) are excluded from the hash. Published versions are immutable.

## Rationale and evidence

Category failure mode 5 (merge pain with designer-coupled XML: SSIS .dtsx, PDI .ktr) and the AI-generation advantage of schema-validated specs (TRN-RES-01 §4, §6). JCS gives a stable hash across key order.

## Alternatives considered

F# DSL only (phase 1 uses F# composition; serialization deferred); YAML canonical (rejected: 1.1/1.2 ambiguity); proprietary XML (rejected).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
