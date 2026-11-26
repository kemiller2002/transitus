---
id: DF-TRN-2026-0020
title: "Isolated temporary staging is a phase-1 capability, located in the consumer's tenant schema with Strata-governed DDL, without COPY into RLS tables, purged by DELETE or governed partition maintenance, and protected in backups by crypto-shredding; the raw blob store is a port with a database default subject to sizing"
status: accepted
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner)
confidence: high
supersedes: [DF-TRN-2026-0008]
superseded_by: []
evidence: ["https://github.com/kemiller2002/transitus/pull/1#issuecomment-7200249612"]
tags: [transitus, owner-decision]
work_item: WI-0002
provenance:
  contributions:
    EXE-20261126T181704540Z-e41ec7a0:
      operations: [created]
      at: 2026-11-26T18:20:44.357Z
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

Supersedes DF-TRN-2026-0008. Only the phase changes: staging moves into phase 1.

**Carried forward unchanged from DF-0008 (review C5):**
- staging lives in the tenant schema (CNV-ARC-001);
- DDL comes only from governed migrations;
- bulk loads use a load table, not COPY into RLS tables;
- crypto-shredding protects purged data in backups;
- the UNLOGGED recovery model is stated;
- public reference data is staged once.

**Owner resolution of OQ-04:** the blob-store port defaults to the database, subject to sizing evidence.

**Still deferred:** file-backed columnar staging (ST-008).

## Rationale and evidence

Owner direction ('isolated temporary staging' is in phase 1); review C5; PostgreSQL limitations on COPY with row-level security and on LIST partitioning.

## Alternatives considered

No staging in phase 1 (superseded); a shared staging schema (rejected by C5).

## Status

Accepted: decided by the repository owner in a comment on transitus#1 and recorded by the authoring agent. Acceptance of this decision does not authorize implementation or merge; the owner reserved both until the Praxis gates pass.
