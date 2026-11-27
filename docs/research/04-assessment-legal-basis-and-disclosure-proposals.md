---
id: TRN-RES-05
title: Evidence-Based Proposals for OD-TRN-P3-01 (Assessment Tier Legal Basis) and OQ-17 (T1 Disclosure Thresholds)
status: proposed
version: 0.1.0
created: 2026-11-27
updated: 2026-11-27
work_item: WI-0006
decisions: [DF-TRN-2026-0022, DF-TRN-2026-0025]
provenance:
  contributions:
    EXE-20261127T023211757Z-766c3a85:
      operations: [created]
      at: 2026-11-27T02:33:58.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Evidence-based proposals for OD-TRN-P3-01 and OQ-17 per owner direction"
      evidence: [https://github.com/kemiller2002/transitus/pull/2#issuecomment-7208145101]
---

# Proposals for owner decision: OD-TRN-P3-01 and OQ-17

**Status:** proposals for owner decision only. The owner asked, on transitus#2
(comment 7208145101, 2026-11-27), that these questions be resolved "through
evidence-based proposals; do not invent legal conclusions or waive gates".

This document is **not legal advice** and draws **no legal conclusion**. Each
legal question below is marked **for counsel**. Until the owner decides, the
stricter defaults already in TRN-REQ-ASM-001 and TRN-REQ-PRF-001 stay in
force:
- T1 requires a recorded sponsor IT approval;
- T2+ requires a recorded executed MSA and DPA;
- no binding threshold defaults are shipped.

In both questions Transitus checks that host-supplied references and
host-policy parameters are present. It never decides whether they are
sufficient (ASM-001, PRF-001). So the owner is deciding the default
references and parameter values a host (Unbound) must supply. Transitus
behaviour does not change.

## Evidence base

Internal sources are cited by repository path. External sources are cited
as published works. External references were not re-retrieved in this
session; verify them before relying on any specific figure.

| Ref | Source | Used for |
|---|---|---|
| E1 | daf-landscape `research/competitive-displacement/08-frictionless-onboarding.md` §3 (revision 2; CHL-017, 040, 069, 070, 072) | Installing a profiler is a software-installation and security event. Record-level data needs an MSA, a DPA and a written information-security programme. Synthetic runs are conformance only |
| E2 | daf-landscape `research/competitive-advantage/charity-network-and-onboarding/13-pre-contract-migration-assessment.md` §2-§3 | T0-T4 ladder. Proposes an NDA for T0-T1 and an NDA plus DPA for T2-T4. k-suppression default 10. Tokenized samples remain personal data. State privacy laws reaching nonprofits [MIG-020]. GLBA probably not directly binding [MIG-021], flagged for counsel. Check of the sponsor's donor privacy notice |
| E3 | Unbound `requirements/discovery/2026-11-26-charity-network-and-onboarding` UNB-ONB-003 | T2 row-level data only after an executed NDA/DPA with a deletion commitment |
| E4 | Data-processing agreement practice, e.g. EU GDPR Art. 28(3) (controller-processor contract terms) and US state comprehensive privacy laws with processor-contract provisions (summarized in E2 [MIG-020]) | Typical processor terms: purpose limitation, confidentiality, security measures, sub-processor control, deletion or return, and assistance. A reference model only; applicability to any sponsor is **for counsel** |
| E5 | L. Sweeney, "k-anonymity: a model for protecting privacy", *Int. J. Uncertainty, Fuzziness and Knowledge-Based Systems* 10(5), 2002 | Minimum group size as a disclosure-control principle |
| E6 | A. Hundepool et al., *Statistical Disclosure Control*, Wiley, 2012 (tabular data chapter) | Threshold (minimum frequency) rule; dominance (n,k) rule and p% rule for magnitude tables; need for secondary (complementary) suppression |
| E7 | US Centers for Medicare & Medicaid Services, cell-size suppression policy (cells representing 1-10 individuals not displayed) | One published minimum-cell-size convention (threshold 11) |
| E8 | NIST SP 800-188, *De-Identifying Government Datasets* (2023) and NIST SP 800-226, *Guidelines for Evaluating Differential Privacy Guarantees* (2025; cited in E2 [MIG-019]) | Aggregation and suppression as de-identification techniques; differential privacy breaks exact totals (E2) |

## 1. OD-TRN-P3-01: legal basis and approval preconditions per tier

**Conflict.** E1 (Phase II revision 2) requires sponsor IT approval for T1 and
an MSA plus a DPA for T2+. E2 and E3 require an NDA for T0-T1 and an NDA plus
DPA for T2.

**What the evidence supports (no legal conclusion):**
- **T1 is an installation and security event regardless of output content.**
  A profiler runs inside the sponsor's environment (E1), so an IT or security
  approval reference is a precondition independent of any confidentiality
  agreement. E2 and E3 do not address installation.
- **T1 output is designed to contain no personal data** (PRF-001 disclosure
  controls, ASM-003 identifier scan). Whether an NDA alone suffices for that
  output is **for counsel**. The design reduces, but does not eliminate,
  disclosure risk (§2).
- **T2+ involves record-level personal data.** E2 records that tokenized
  samples remain personal data. Processor terms (E4) are the usual
  instrument, plus confirmation that the sponsor's donor privacy notice
  permits the disclosure (E2 §3). Whether a stand-alone DPA under an NDA (E2,
  E3) or a DPA under an executed MSA (E1) is required is **for counsel**, and
  is also commercial: an MSA presupposes a contracting relationship.

**Options for the owner:**

| Option | T0 | T1 | T2+ | Trade-off |
|---|---|---|---|---|
| A (current default, stricter) | engagement reference | sponsor IT approval + NDA | executed MSA + DPA (+ privacy-notice check, documented sponsor authority) | Highest assurance. T2 waits for an MSA, which can lengthen pre-contract assessment |
| B (E2/E3) | NDA | NDA | NDA + DPA with deletion commitment | Earlier T2. Omits the T1 installation approval that E1 identifies |
| C (hybrid, **proposed**) | engagement reference | sponsor IT approval + NDA | DPA with purpose limitation, deletion deadline and no-training clause, plus privacy-notice confirmation, under **either** an MSA or a stand-alone pre-contract evaluation agreement, as counsel approves | Keeps E1's installation control. Lets counsel choose the T2 contract vehicle |

**Proposal:** adopt option C as the Unbound-supplied default reference set,
subject to counsel confirming the T2 instrument. Keep option A in force until
counsel and the owner decide. In Transitus the decision only changes which
reference *types* ASM-001 requires for each tier; ASM-001's text already
leaves sufficiency to the host and counsel.

**Evidence still needed:** a counsel opinion on the T2 instrument and the
processor terms under applicable state laws (E2 [MIG-020]); the sponsor IT
approval process from design-partner interviews (E2 open questions).

## 2. OQ-17: T1 disclosure-control thresholds

PRF-001 needs three host-policy parameters:
- a minimum contributor count per cell;
- a minimum population below which no aggregates leave the sponsor;
- a dominance rule for monetary cells.

**What the evidence supports:**
- **Threshold rule.** Minimum frequency per published cell is the standard
  first control for frequency tables (E5, E6). Published conventions vary.
  One widely cited US health convention suppresses cells for 1-10
  individuals, a threshold of 11 (E7). E2 proposes k = 10.
- **Dominance for magnitude (money) cells.** Frequency thresholds alone do not
  protect a magnitude cell dominated by one or two contributors. A single
  very large DAF contribution can identify a donor (E2). The (n,k) dominance
  rule and the p% rule are the standard sensitivity rules (E6). Their
  parameters are set by each statistical agency and are not universal (E6).
- **Secondary suppression is needed.** If T1 emits control totals per
  grouping, a suppressed cell can be recovered by subtracting the published
  cells from the total. Complementary suppression, or omitting margins, is
  required (E6). **This is a gap in PRF-001 as written.** It is proposed
  below for ratification and is not added silently.
- **Exact reconciliation is not affected.** T1 aggregates are assessment
  evidence only. Exact monetary reconciliation happens over full populations
  at T2+ and in rehearsal (VR-002, VR-003, VR-010, MIG-001). Differential
  privacy is unsuitable for T1 totals for the same reason (E2, E8).

**Proposed parameter defaults:** host policy, for owner decision and privacy
review. These are proposals, not binding values.

| Parameter | Proposed default | Basis |
|---|---|---|
| Minimum contributors per cell (k) | 11 | Stricter of E7 (11) and E2 (10) |
| Minimum population for any aggregate output | Fewer than 11 funds in the book: schema and coverage only, no aggregates | Consistent with k. Phase II "minimum fund count" (E1) gives no figure |
| Dominance rule for monetary cells | (n,k) rule with n = 1 and n = 2. The k% values are chosen by the owner after a synthetic-data utility test; no value is proposed without that test | E6. Agencies set parameters themselves |
| Secondary suppression | Required whenever a margin or total is emitted | E6 |

**Proposed requirement refinement (not applied; for ratification):**
TRN-REQ-PRF-001 should add: "when a margin or total is emitted alongside
suppressed cells, complementary suppression MUST prevent recovery of any
suppressed cell by subtraction".

**Evidence still needed:**
- a utility test on synthetic DAF books (various sizes and skews) measuring
  how much of the T1 report survives each parameter set;
- a privacy review of the result.

Both are research tasks with no expenditure.

## 3. What does not change

- Exact monetary reconciliation and authorized data access are preserved
  (dispositions doc §9).
- Trigger TA still gates ASM-001..004/006 and PRF-003.
- The DEC-010 / V-4 gate is untouched.
- No implementation or expenditure is authorized.
