---
id: DF-TRN-2026-0025
title: "Owner strategic approval of DAF Landscape DEC-012 (commercial validation plan) and DEC-008 (gated capital deployment) as constraints on Transitus: V-4 is the Transitus evidence gate, synthetic rehearsal is a lower-cost precursor that cannot satisfy it, and Transitus effort estimates are not approved expenditure"
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
evidence: ["kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv#DEC-012", "kemiller2002/daf-landscape:research/competitive-displacement/data/registers/decisions.csv#DEC-008", "kemiller2002/daf-landscape:research/competitive-displacement/22-commercial-validation-plan.md"]
tags: [transitus, owner-decision, daf-landscape-phase-3, strategic-approval]
work_item: WI-0003
provenance:
  contributions:
    EXE-20261126T203508536Z-de9f55a7:
      operations: [created]
      at: 2026-11-26T20:37:31.000Z
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

The owner approved, on 2026-11-26:

- **DEC-012**: *adopt the existing validation plan and its gates; where
  possible develop lower-cost methods of satisfying them;*
- **DEC-008**: *staged investment, measurable milestones, explicit
  termination criteria; modeled funding amounts are not approved
  expenditures; challenge and minimize them.*

Constraints on Transitus:

1. **V-4 is the Transitus evidence gate** (authorised incumbent export
   through Transitus phase 1 with full per-fund reconciliation; pass rule
   100% money tie-out, history depth documented, freeze plan ≤5 business
   days). It informs DEC-010 and is a precondition of any migration SLA or
   maturity claim (DF-TRN-2026-0024).
2. **Lower-cost precursor, not a substitute.** The synthetic canonical
   rehearsal (TRN-REQ-MIG-001 on fixtures) and the T0 template and T1
   profiler (TRN-REQ-ASM-002/003) can de-risk V-4 and reduce its cost, but
   synthetic runs are conformance checks only (TRN-REQ-ASM-005) and cannot
   satisfy V-4.
3. **No expenditure.** The Transitus effort figures in `docs/roadmap.md`
   (≈15-24 engineer-weeks plus ≈6-12 outside Transitus) are theoretical
   estimates, not approved spend. Nothing here authorizes paid research,
   outreach, contracts, production deployment or implementation.
4. **Minimization.** This revision adds no package, adapter or operation to
   the phase-1 budget (TRN-REQ-ARC-007); new requirements reuse the
   existing profile, validate, reconcile, verify and evidence stages.
5. **Termination criteria.** Transitus's only standing retirement rule is
   TRN-REQ-PF-004, which the owner made non-gating for phase 1. Whether the
   DEC-008 kill rule (no named partner by month 6; no referenceable pilot by
   month 24) should also pause Transitus work beyond phase 1 is raised as
   owner decision **OD-TRN-P3-02** (`docs/open-questions.md`); it is not
   assumed here.

## Status

**Strategically approved** only (`approval_stage: strategically-approved`). Praxis restricts the DF `status` field to draft, review, accepted, superseded or withdrawn, so `status: accepted` records only that the owner decided; in this repository `accepted` has never authorized implementation (`docs/decisions/README.md`). The ladder is: strategically approved → requirements incorporated → evidence gate satisfied → implementation authorized → implemented → validated. No later rung is advanced by this record; the requirement rows it motivates are `proposed`. Approval authorizes strategic direction, requirements refinement, research and planning; it does **not** authorize expenditure, contractual commitments, production deployment, removal of mandatory controls or implementation.

## Rationale and evidence

daf-landscape `22-commercial-validation-plan.md` (V-1..V-9, budgets,
kill rule); `decisions.csv` DEC-008 and DEC-012.

## Alternatives considered

Treat synthetic rehearsal as satisfying V-4 (rejected: it cannot predict
record-level defects; Phase II CHL-017/069/070).
