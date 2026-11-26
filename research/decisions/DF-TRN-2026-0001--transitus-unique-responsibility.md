---
id: DF-TRN-2026-0001
title: "Transitus owns only what no Echelon component provides: declarative pipeline model, transformation and check libraries, adapter contracts, raw/lineage/evidence, pipeline state machine"
status: review
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: high
supersedes: []
superseded_by: []
evidence: ["TRN-ARCH-11", "TRN-REV-01 C1", "ECH-001", "ECH-003", "ECH-005"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:41:59.449Z
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

Transitus's responsibility is limited to: the pipeline model (phase 2), pure transformation and validation/reconciliation libraries, format/transport/destination adapter contracts, raw-evidence, lineage and evidence assembly, and a pipeline execution state machine on top of Echelon.Execution. Queueing, schema governance, workflow visualization, fault handling, reports, identity and domain rules are consumed from their owners.

## Rationale and evidence

Every repository in the brief and the registry was cloned and searched (TRN-ARCH-11 §1). No component provides typed ingestion with raw preservation, control totals and evidence; several provide adjacent capabilities that must not be duplicated (Echelon.Execution, Strata, Forma, Aegis, Folio). Review C1 found residual duplication with Unbound's RawEvidence model and replay parsers, resolved by DF-0016/ARC-006.

## Alternatives considered

Build a general integration platform (rejected: duplicates Execution/Forma, exceeds demand); build nothing and hand-write feeds in each app (viable baseline — see DF-0016 kill criterion); adopt an external tool (rejected: TRN-ARCH-12 §5).

## Status

Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
