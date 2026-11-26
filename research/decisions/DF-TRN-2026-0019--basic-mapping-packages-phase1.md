---
id: DF-TRN-2026-0019
title: "Basic mapping packages (public-specification and target-side canonical) are phase-1 deliverables, reusable without a signed customer; vendor-specific turnkey packages follow at T3; redistribution rights are verified before publication"
status: accepted
decision_type: architecture
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner)
confidence: high
supersedes: [DF-TRN-2026-0014]
superseded_by: []
evidence: ["https://github.com/kemiller2002/transitus/pull/1#issuecomment-7200249612"]
tags: [transitus, owner-decision]
work_item: WI-0002
provenance:
  contributions:
    EXE-20261126T181704540Z-e41ec7a0:
      operations: [created]
      at: 2026-11-26T18:20:44.069Z
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

Supersedes DF-TRN-2026-0014.

**Phase-1 packages:**
- `irs.eo-bmf`;
- `nacha.ach` (internal-only until NACHA redistribution rights are verified);
- the first bank partner's format, illustrated by `iso20022.camt053`;
- `custodian.schwab`, a placeholder until Schwab's documentation is obtained under acceptable terms; nothing is invented;
- `unbound.canonical-history`, the target-side canonical shape.

**Rules carried forward from DF-0014:**
- No invented vendor schemas.
- Overlays, not forks.
- Vendor-derived packages need licence clearance.
- Promotion from customer overlays needs two independent samples.

## Rationale and evidence

Owner direction: 'Do not condition basic mapping reuse on a signed customer.' OQ-07 sets Schwab as the custodian priority; OQ-16 requires the NACHA rights check. Review C7's evidence on vendor licence restrictions still applies to vendor-turnkey packages.

## Alternatives considered

Defer all packages to T3 (superseded); build vendor packages from marketing material (prohibited).

## Status

Accepted: decided by the repository owner in a comment on transitus#1 and recorded by the authoring agent. Acceptance of this decision does not authorize implementation or merge; the owner reserved both until the Praxis gates pass.
