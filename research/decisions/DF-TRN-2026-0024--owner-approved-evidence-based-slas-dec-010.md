---
id: DF-TRN-2026-0024
title: "Owner strategic approval of DAF Landscape DEC-010 (evidence-based process SLAs): Transitus measures migration timing and onboarding maturity as targets only; no SLA or maturity level is claimed or committed before successful rehearsal and validation (V-4) and contractual review"
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
evidence: ["kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv#DEC-010", "kemiller2002/daf-landscape:research/competitive-displacement/data/registers/cross-repository-implications.csv#XRI-009", "kemiller2002/daf-landscape:research/competitive-displacement/data/registers/cross-repository-implications.csv#XRI-011", "kemiller2002/daf-landscape:research/competitive-displacement/22-commercial-validation-plan.md#V-4"]
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

The owner approved **DEC-010** on 2026-11-26: *evidence-based process SLAs
only after successful migration rehearsals and validation; preserve V-4 and
contractual review requirements.*

For Transitus:

- Transitus records the measurement facts a migration SLA and the onboarding
  maturity model (levels 0-5) would need (TRN-REQ-MET-001, TRN-REQ-MET-003).
  These are **measurement targets**, not commitments.
- The SLA clock, if one is ever offered, starts when an extract is
  determined **conforming** by the deterministic conformance check of the
  declared package, with a declared exclusions list; Transitus produces the
  sponsor validation summary artifact, and approval stays with the host
  (TRN-REQ-MET-003).
- No maturity level may be claimed except from measured data with a stated
  numerator, denominator, window and minimum sample (TRN-REQ-MET-002), and
  no level, SLA figure or outcome commitment may be published or used
  commercially until (1) V-4 (authorised incumbent export rehearsal) has
  passed, (2) the owner has recorded that evidence gate as satisfied, and
  (3) contractual review is complete. Transitus requirements do not make
  that call.
- Any eventual commitment covers Unbound-controlled process steps only,
  with liability capped (Phase II CHL-075); that is commercial policy owned
  outside Transitus.

## Status

**Strategically approved** only (`approval_stage: strategically-approved`). Praxis restricts the DF `status` field to draft, review, accepted, superseded or withdrawn, so `status: accepted` records only that the owner decided; in this repository `accepted` has never authorized implementation (`docs/decisions/README.md`). The ladder is: strategically approved → requirements incorporated → evidence gate satisfied → implementation authorized → implemented → validated. No later rung is advanced by this record; the requirement rows it motivates are `proposed`. Approval authorizes strategic direction, requirements refinement, research and planning; it does **not** authorize expenditure, contractual commitments, production deployment, removal of mandatory controls or implementation.

## Rationale and evidence

Phase II: no rehearsal on a real export has happened (OD-M-14); at 2-4
migrations a year levels 4-5 cannot be evidenced for years (CHL-076); the
Stripe PAN-import pattern (clock starts on valid data, published exclusions,
customer-approved validation summary; SRC-044) is the reference design.

## Alternatives considered

Publish migration SLAs now (rejected by DEC-010).
