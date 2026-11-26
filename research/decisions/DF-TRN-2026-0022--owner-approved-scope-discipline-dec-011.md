---
id: DF-TRN-2026-0022
title: "Owner strategic approval of DAF Landscape DEC-011 (Transitus scope discipline): keep the approved phase-1 scope, develop public-specification and canonical migration capabilities, and defer customer-specific proprietary vendor packages until authorized source data exists"
status: accepted
approval_stage: strategically-approved
decision_type: strategy
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner), DAF Landscape Phase III owner approval of DEC-001..DEC-012 dated 2026-11-26
confidence: high
supersedes: []
superseded_by: []
evidence: ["kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv#DEC-011", "kemiller2002/daf-landscape:research/competitive-displacement/23-executive-decision-register.md", "kemiller2002/daf-landscape:research/competitive-displacement/18-transitus-implications.md"]
tags: [transitus, owner-decision, daf-landscape-phase-3, strategic-approval]
work_item: WI-0003
provenance:
  contributions:
    EXE-20261126T203508536Z-de9f55a7:
      operations: [created]
      at: 2026-11-26T20:36:28.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Record owner strategic approval of DAF Landscape DEC-011 (2026-11-26)"
      evidence: [kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv#DEC-011]
---

# Decision Record

## Decision

The owner approved DAF Landscape Phase II decision **DEC-011** on 2026-11-26
in these terms: *keep the approved initial scope; develop public-specification
and canonical migration capabilities; defer customer-specific proprietary
vendor packages until authorized source data exists.*

For Transitus this decision **reaffirms, and does not supersede**:

- DF-TRN-2026-0018 (phase 1 is the minimal declarative typed linear pipeline);
- DF-TRN-2026-0019 (basic public-specification and target-side canonical
  packages are phase-1 deliverables reusable without a signed customer;
  vendor-specific turnkey packages follow at trigger T3 with a
  customer-authorized sample and licence clearance).

Consequences recorded in requirements revision `DAF-P3-2026-11-26`
(`tools/requirements_source.py`):

- the pre-contract migration assessment (TRN-REQ-ASM-001..008) is built
  from public specifications, the canonical package and synthetic datasets
  only until customer-authorized data exists (TRN-REQ-ASM-008);
- every finding that rests on an unverified vendor-format assumption is
  flagged as such (TRN-REQ-ASM-007);
- no new phase-1 package, adapter or operation is added by this decision;
  the ARC-007 maintenance budget is unchanged.

## Status (status ladder)

**Strategically approved** only (`approval_stage: strategically-approved`). Praxis restricts the DF `status` field to draft, review, accepted, superseded or withdrawn, so `status: accepted` here records only that the owner decided; in this repository `accepted` has never authorized implementation (see `docs/decisions/README.md`). The ladder is: strategically approved →
requirements incorporated → evidence gate satisfied → implementation
authorized → implemented → validated. This record does not advance any
later rung. The requirement rows it motivates are `proposed`. Approval
authorizes strategic direction, requirements refinement, research and
planning; it does **not** authorize expenditure, contractual commitments,
production deployment, removal of mandatory controls or implementation.

## Rationale and evidence

Phase II found that no public export schema exists for the incumbent DAF
platforms and that report-style adapters support balance-level conversion
only (daf-landscape `18-transitus-implications.md` §3, CHL-071/072). The
Phase II recommendation was stated as consistent with D-MIT-002 (revised)
and DF-TRN-2026-0019.

## Alternatives considered

Expand phase 1 with vendor packages now (rejected by the owner: no
authorized source data; inventing proprietary schemas is prohibited by
TRN-REQ-MP-002).
