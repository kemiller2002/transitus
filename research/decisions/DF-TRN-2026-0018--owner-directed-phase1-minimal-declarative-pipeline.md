---
id: DF-TRN-2026-0018
title: "Phase 1 is a minimal declarative typed linear pipeline with basic reusable mapping packages, checkpoints, replay, idempotency and dry runs, demonstrated on the IRS feed, a bank/custodian feed and canonical historical migration"
status: accepted
decision_type: process
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner)
confidence: high
supersedes: [DF-TRN-2026-0016]
superseded_by: []
evidence: ["https://github.com/kemiller2002/transitus/pull/1#issuecomment-7200249612"]
tags: [transitus, owner-decision]
work_item: WI-0002
provenance:
  contributions:
    EXE-20261126T181704540Z-e41ec7a0:
      operations: [created]
      at: 2026-11-26T18:20:43.792Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Owner-directed decision recorded from transitus#1 comment 7200249612"
      evidence: [https://github.com/kemiller2002/transitus/pull/1#issuecomment-7200249612]
---

# Decision Record

## Decision

Owner direction (2026-11-26) supersedes DF-TRN-2026-0016.

**Phase 1 includes:**
- A minimal declarative typed pipeline (TRN-REQ-PS-011), composed linearly of these stages:
  - ingest, then immutable raw evidence;
  - isolated temporary staging;
  - deterministic mapping and transformation;
  - validation and reconciliation;
  - authorization, then load through authorized domain APIs;
  - post-load verification, then evidence and retention.
- Versioned, reusable basic mapping packages.
- Checkpoints, replay and idempotency.
- Dry runs, including migration rehearsal.

**Reuse:** Phase 1 reuses Formats, Checks and Evidence as internal libraries, and Echelon.Execution for durable execution.

**Deferred:**
- complex DAGs and bounded set operators (T2);
- advanced AI and vendor-specific turnkey packages (T3);
- visual editing (T4).

**Demonstration:** three theoretical pipelines (`examples/pipelines/`):
- IRS EO BMF;
- bank (camt.053, illustrative) or Schwab custodian;
- canonical historical migration, as a rehearsal and as a pre-go-live import.

**Measurement:** the approach is measured later against hand-written alternatives (TRN-REQ-PF-004); that measurement does not gate phase 1.

**Always blocking:** financial correctness and tenant isolation (TRN-REQ-VR-013).

**Resolved owner questions:**
- OQ-13: canonical historical import and migration rehearsal are required in Unbound release 1.
- OQ-14: Transitus is an independent, embeddable repository with no separate service.

## Rationale and evidence

The owner's decision, given as a comment on the phase-0 PR, after the four-reviewer adversarial review (TRN-REV-01) had recommended a smaller three-library phase 1. The reviewers' complexity and maintenance findings (C3, C11) still apply. They are carried as a phase-1 maintenance budget (TRN-REQ-ARC-007) and as unresolved tensions in docs/open-questions.md, not resolved by this record.

## Alternatives considered

The three-library phase 1 (DF-TRN-2026-0016, superseded); the full original phase 1 including DAGs, AI and UI (rejected by the owner: deferred).

## Status

Accepted: decided by the repository owner in a comment on transitus#1 and recorded by the authoring agent. Acceptance of this decision does not authorize implementation or merge; the owner reserved both until the Praxis gates pass.
