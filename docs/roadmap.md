---
id: TRN-ROADMAP
title: Phased Implementation Roadmap
status: proposed
version: 0.2.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
decisions: [DF-TRN-2026-0016]
---

# Phased implementation roadmap

Revised after the adversarial review (TRN-REV-01). Each phase after phase 1
starts only when its trigger is recorded in a Decision Record
(TRN-REQ-ARC-009). Effort figures are theoretical.

## Phase 0: research, architecture, requirements (this PR)

Complete when the owner has reviewed the decision records and answered the
blocking owner questions OQ-13 and OQ-14.

## Phase 1: Unbound release-1 feed libraries (minimal viable scope)

**Packages, which form the maintenance budget (ARC-007):**
- `Transitus.Formats`
- `Transitus.Checks`
- `Transitus.Evidence`

**Estimated effort:** 4–6 engineer-weeks.

| # | Work item | Traces to (ARC-008) |
|---|---|---|
| 1 | Port `tools/render_requirements.py` to F# (DF-TRN-2026-0017) | governance |
| 2 | `Transitus.Evidence`: RawEvidence records aligned to Unbound UNB-KNOW-023, with rights policy (ST-001); deterministic idempotency keys (EX-006); L0–L2 lineage with HMAC natural keys (LN-002); evidence package and hash chain (LN-003/006) | UNB-EXT-017..029, UNB-KNOW-023/027, CNV-FIN-013 |
| 3 | `Transitus.Checks`: validation and reconciliation primitives (VR-001/002), conservation law (VR-007), zero monetary tolerance (VR-003), blocking-gate result type (VR-004) | CNV-FIN-004, CNV-PAY-005, UNB-CUST-010/011 |
| 4 | `Transitus.Formats`: move IRS EO BMF, Pub 78, auto-revocation and OFAC SDN parsers from `Unbound.Replay/Sources.fs` (ARC-006); strict CSV with limits (SEC-002/006/007) | UNB-EXT-001, CNV-GRT-003, OFAC screening |
| 5 | `Transitus.Formats`: NACHA returns and NOC (fixed-width) | CNV-PAY-005, CNV-PAY-002 |
| 6 | `Transitus.Formats`: one bank activity format, BAI2 or camt.053 (OQ-06) | CNV-PAY-007, UNB-XIN-BNK-003 |
| 7 | `Transitus.Formats`: one custodian format (OQ-07); read-only XLSX with cached values, no formulas (SEC-004) | UNB-CUST-009, OD-M-07 |
| 8 | Abuse-case corpus: zip bomb, XXE, formula injection, zip slip, malformed input, replay (TRN-SEC-01 §5) | security |
| 9 | Conformance and property tests for every library (ARC-003); determinism under different host cultures and time zones (TX-003) | quality |
| 10 | Unbound proposals UNB-TRN-001..008: Unbound writes feed modules and defines domain operations; bulk-load quota share (AD-011) | Unbound |
| 11 | Benchmarks replacing assumptions A1–A12 (PF-001, PF-003), including per-record Echelon.Execution cost on the RM-05 instance | performance |
| 12 | Phase-1 exit review: compare with hand-written per-feed modules (PF-004); decide on T2 | kill criterion |

**Conditional item.** If OQ-13 keeps CNV-EXP-002 in Unbound release 1, add
a historical-import feed using the Unbound canonical import shape
(MP-006). Loading uses pre-go-live batch operations only (AD-012).

**Exit criteria.**
- All phase-1 feeds in Unbound run through the libraries.
- Abuse-case and determinism suites pass.
- The benchmarks are recorded.
- The PF-004 comparison is recorded.

## Phase 2: engine and declarative model (trigger T2)

**Trigger T2** is any one of the following:
- a second consumer is committed (Helix Note or Summa);
- the phase-1 exit review shows the same orchestration duplicated in three or more feed modules;
- non-engineer pipeline authoring becomes a requirement.

**Scope:**
- `Transitus.Model`: DU model and canonical JSON (DF-0002)
- `Transitus.Validation.Definition`: types, DAG, policy, and the authority-and-semantics diff
- `Transitus.Transforms`: operation catalogue, including bounded set operators (TX-011)
- `Transitus.Engine`: state machine on Echelon.Execution
- `Transitus.Storage.Postgres`: tenant-schema staging (DF-0008)
- Extension governance (EXT-001..004)
- Proposal to extract Echelon.Execution (OQ-01)

**Estimated effort:** 8–12 engineer-weeks.

## Phase 3: mapping packages and AI assistance (trigger T3)

**Trigger T3:** a migration is contracted with a customer-authorized sample
and vendor-licence clearance (MP-002), **and** the AI evaluation harness
meets recorded thresholds (AI-008/009).

**Scope:**
- Target-side packages first (MP-006)
- Overlays (MP-003)
- Upgrade diffs (MP-004)
- `Transitus.Assist`
- Reuse metrics (MP-007)

**Estimated effort:** 4–6 engineer-weeks.

## Phase 4: administration UI (trigger T4)

**Trigger T4:** operators other than engineers must configure pipelines.

**Scope:**
- Forma workflow projection with a round-trip guarantee (UI-002)
- Accessible, non-drag alternatives (UI-004)
- Views per TRN-ARCH-10
- Optional OpenLineage export and file-backed staging, only on measured need (ST-008)

**Estimated effort:** 8–12 engineer-weeks.

## Kill and fold criteria

- **Engine not built.** At the phase-1 exit, if hand-written per-feed modules are cheaper (PF-004) and no second consumer is committed, Transitus stays a three-library utility.
- **Folding into Unbound.** If, 6 months after phase 1, Unbound is the only consumer and the libraries have taken on Unbound-specific terms despite VR-006, the owner may fold them into Unbound (OQ-14).
- **Vendor packages retired.** These packages are retired if reuse stays below threshold after three migrations (MP-007).
