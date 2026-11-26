---
id: DF-TRN-2026-0026
title: "Owner resolution of OD-TRN-P3-02: the DAF Landscape DEC-008 kill rule does not pause or gate Transitus work, including work beyond phase 1"
status: accepted
approval_stage: strategically-approved
decision_type: strategy
created: 2026-11-26
updated: 2026-11-26
created_by_agent: claude
decided_by: kemiller2002 (repository owner), stated in the DAF Landscape Phase III session on 2026-11-26
confidence: high
supersedes: []
superseded_by: []
evidence: ["Owner statement 2026-11-26, relayed by the Phase III coordinator: \"Kill rule doesn't stop Transitus.\"", "kemiller2002/daf-landscape:research/competitive-displacement/22-commercial-validation-plan.md (kill rule)", "DF-TRN-2026-0025"]
tags: [transitus, owner-decision, daf-landscape-phase-3]
work_item: WI-0004
provenance:
  contributions:
    EXE-20261126T205108633Z-a4de7b2b:
      operations: [created]
      at: 2026-11-26T20:51:38.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Owner resolution of OD-TRN-P3-02 (2026-11-26): DEC-008 kill rule does not gate Transitus"
      evidence: [DF-TRN-2026-0025]
    EXE-20261126T210016939Z-536fe55b:
      operations: [modified]
      at: 2026-11-26T21:01:25.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Stage I review fixes S1-06/07/08/15 and OD-P3-04 note (WI-0005)"
      evidence: [docs/research/03-daf-phase3-dispositions.md]
---

# Decision Record

## Decision

Resolves **OD-TRN-P3-02**, which DF-TRN-2026-0025 §5 raised. The owner's
words (2026-11-26): *"Kill rule doesn't stop Transitus."*

The DEC-008 kill rule pauses the commercial thesis before platform capital
beyond Release 1. Its triggers are:
- no named channel partner by month 6;
- no referenceable live pilot by month 24.

That rule does **not** pause or gate Transitus work, including work beyond
phase 1. Transitus phase transitions remain governed only by their own
recorded triggers:
- T2, T3, TA and T4 (TRN-REQ-ARC-009);
- the TRN-REQ-PF-004 measurement, which stays non-gating for phase 1.

## Note: when the kill rule's clock starts

Owner decision OD-P3-04 ("Significant is when it becomes its own cost
center") defines when the DEC-008 no-named-partner clock starts. It is
recorded here because this record describes the kill rule. It does not
change this decision: the kill rule does not gate Transitus.

## Limits

This resolution does not authorize expenditure, contractual commitments,
production deployment or implementation. The Transitus scope stays as
before:
- DEC-011 phase 1 (DF-TRN-2026-0018, 0019, 0022);
- vendor-specific packages deferred behind T3 and the DEC-007 selection
  rule (DF-TRN-2026-0023);
- the pre-contract assessment behind trigger TA.

The DEC-008 kill rule continues to apply to the commercial thesis and to
capital deployment outside Transitus. This record does not change how it
applies there.

## Status

Owner decision: `status: accepted`, `approval_stage: strategically-approved`.
Praxis allows only draft, review, accepted, superseded or withdrawn as a
decision status, so the rung is carried in `approval_stage`. No later rung of
the status ladder is advanced.

## Effect on other records

The following are annotated, not rewritten:
- DF-TRN-2026-0025 §5 (resolution note added; the original text is kept);
- `docs/open-questions.md` (OD-TRN-P3-02 resolved; UC-19 annotated);
- `docs/research/03-daf-phase3-dispositions.md` §1 and §6.

## Alternatives considered

The alternative was to apply the DEC-008 kill rule to Transitus phases 2 and
later. The owner rejected it.
