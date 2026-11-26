---
id: DF-TRN-2026-0008
title: "Phase 1 owns no staging; phase-2 staging lives in the consumer's tenant schema with Strata-governed DDL, load tables, and crypto-shredding; raw blobs behind a port with a PostgreSQL default; file-backed staging only on measured need"
status: superseded
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
confidence: medium
supersedes: []
superseded_by: [DF-TRN-2026-0020]
evidence: ["TRN-ARCH-02", "TRN-REV-01 C5"]
tags: [transitus]
work_item: WI-0001
provenance:
  contributions:
    EXE-20261126T151721856Z-671cd5b7:
      operations: [created]
      at: 2026-11-26T15:42:01.392Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Transitus phase-0 decision record after adversarial review TRN-REV-01"
      evidence: [docs/reviews/adversarial-review.md]
    EXE-20261126T181704540Z-e41ec7a0:
      operations: [superseded]
      at: 2026-11-26T18:20:45.485Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Superseded by owner-directed decision"
---

# Decision Record

## Decision

Revised after review C5: the shared LIST-partitioned staging schema was unworkable (single-column LIST, runtime DDL, COPY with RLS, schema-per-sponsor, synchronous standby, backup retention).

## Rationale and evidence

TRN-REV-01 C5; CNV-ARC-001; PostgreSQL documentation on COPY and partitioning.

## Alternatives considered

Shared staging schema (rejected); temp tables (rejected: session-bound); new storage engine (rejected: infrastructure minimalism).

## Status

Superseded by DF-TRN-2026-0020 (owner direction, 2026-11-26).


Proposed by the authoring agent after adversarial review (TRN-REV-01); acceptance is an owner decision. Reversible: yes, through a superseding Decision Record.
