---
id: DF-TRN-2026-0021
title: "Owner resolutions: defer Echelon.Execution extraction until its shared contract is stable; DIV virtualizes interactions while Transitus moves data; unknown outcomes are never blindly retried; AI is provider-independent with per-tenant/classification authorization; CDC deferred; retention from approved policy with no invented durations; FX domain-owned; authorized domain loading interfaces mandatory"
status: accepted
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner)
confidence: high
supersedes: [DF-TRN-2026-0006]
superseded_by: []
evidence: ["https://github.com/kemiller2002/transitus/pull/1#issuecomment-7200249612"]
tags: [transitus, owner-decision]
work_item: WI-0002
provenance:
  contributions:
    EXE-20261126T181704540Z-e41ec7a0:
      operations: [created]
      at: 2026-11-26T18:20:44.635Z
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

Supersedes DF-TRN-2026-0006 on extraction timing.

**Resolved by the owner:**

| Question | Resolution | Requirement |
|---|---|---|
| OQ-01 Echelon.Execution extraction | Defer until the shared contract is stable; use it in place meanwhile. | EX-001 |
| OQ-02 Strata DIV boundary | DIV virtualizes interactions; Transitus moves data. | ARC-010 |
| OQ-04 blob store | Port with a database default, subject to sizing. | ST-007 |
| OQ-05 unknown external outcomes | Never blindly retried. | EX-007 |
| OQ-08 AI providers | Provider-independent; authorization per tenant and classification; no blanket approval. | AI-010 |
| OQ-09 CDC | Deferred. | — |
| OQ-10 retention | From approved classification or sponsor policy; no invented binding durations. Schema and examples now use `policy:` references. | LN-010 |
| OQ-11 FX | Decisions remain domain-owned. | — |
| OQ-15 domain loading | Authorized domain loading interfaces are mandatory. | AD-008, Unbound UNB-TRN-005 |

**Still open, pending evidence:**
- OQ-03 observability ownership: investigate Arca and portfolio ownership first.
- OQ-06 bank format: select from the first partner.
- OQ-07 Schwab documentation: obtain it.
- OQ-12 licence: resolve against authoritative portfolio policy before release.
- OQ-16 NACHA rights: verify.

## Rationale and evidence

Owner comment of 2026-11-26.

## Alternatives considered

—

## Status

Accepted: decided by the repository owner in a comment on transitus#1 and recorded by the authoring agent. Acceptance of this decision does not authorize implementation or merge; the owner reserved both until the Praxis gates pass.
