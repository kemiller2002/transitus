---
id: DF-TRN-2026-0023
title: "Owner strategic approval of DAF Landscape DEC-007 (concentrated migration strategy): the first vendor-specific source package targets one incumbent source cluster selected on recorded evidence, never arbitrarily"
status: accepted
approval_stage: strategically-approved
decision_type: strategy
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner), DAF Landscape Phase III owner approval of DEC-001..DEC-012 dated 2026-11-26
confidence: medium
supersedes: []
superseded_by: []
evidence: ["kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv#DEC-007", "kemiller2002/daf-landscape:research/competitive-displacement/08-frictionless-onboarding.md", "kemiller2002/daf-landscape:research/competitive-displacement/22-commercial-validation-plan.md#V-5"]
tags: [transitus, owner-decision, daf-landscape-phase-3, strategic-approval]
work_item: WI-0003
provenance:
  contributions:
    EXE-20261126T203508536Z-de9f55a7:
      operations: [created]
      at: 2026-11-26T20:37:30.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Record owner strategic approval of DAF Landscape Phase II decisions (2026-11-26)"
      evidence: [kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv]
---

# Decision Record

## Decision

The owner approved **DEC-007** on 2026-11-26: *concentrate early migrations on
one incumbent source platform where commercially practical; preserve V-5; do
not select an incumbent arbitrarily without evidence.*

For Transitus:

- Vendor-specific source packages remain deferred behind trigger T3
  (DF-TRN-2026-0019, TRN-REQ-ARC-009). DEC-007 adds an ordering rule for
  when T3 is reached: the **first** vendor-specific package MUST target a
  single incumbent source cluster chosen by a recorded selection that cites
  (a) the V-5 contract-end calendar result or equivalent evidence of buyers
  in active evaluation, and (b) at least one customer-authorized sample from
  that source (TRN-REQ-MP-010).
- **No incumbent is selected by this record.** Phase II named NPact/FIMS
  legacy and iPhi community foundations only as examples (decisions.csv
  DEC-007); they are not a selection.
- Source adapters are versioned per incumbent report version with a drift
  test (Phase II CHL-071), extending TRN-REQ-MP-004.

## Status

**Strategically approved** only (`approval_stage: strategically-approved`). Praxis restricts the DF `status` field to draft, review, accepted, superseded or withdrawn, so `status: accepted` records only that the owner decided; in this repository `accepted` has never authorized implementation (`docs/decisions/README.md`). The ladder is: strategically approved → requirements incorporated → evidence gate satisfied → implementation authorized → implemented → validated. No later rung is advanced by this record; the requirement rows it motivates are `proposed`. Approval authorizes strategic direction, requirements refinement, research and planning; it does **not** authorize expenditure, contractual commitments, production deployment, removal of mandatory controls or implementation.

## Rationale and evidence

Phase II §4 of `08-frictionless-onboarding.md` infers (INFERENCE, Medium)
that the second migration from the same source costs far less than the first;
no public source measures the reusable share. That inference is untested,
which is why selection waits for V-5 evidence and an authorized sample.

## Alternatives considered

Build packages for several incumbents in parallel (rejected: no authorized
samples; multiplies the most expensive first-instance cost).
