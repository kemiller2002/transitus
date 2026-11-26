---
id: TRN-ROADMAP
title: Phased Implementation Roadmap
status: proposed
version: 0.4.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0002
decisions: [DF-TRN-2026-0018, DF-TRN-2026-0019, DF-TRN-2026-0020, DF-TRN-2026-0021, DF-TRN-2026-0022, DF-TRN-2026-0023, DF-TRN-2026-0024, DF-TRN-2026-0025]
revision_note: "WI-0003 (2026-11-26): DAF Landscape Phase III owner strategic approvals; see docs/research/03-daf-phase3-dispositions.md"
provenance:
  contributions:
    EXE-20261126T203508536Z-de9f55a7:
      operations: [modified]
      at: 2026-11-26T20:42:23.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "DAF Landscape Phase III revision: trigger TA, DEC-007 ordering, new owner decisions and conflicts"
      evidence: [docs/research/03-daf-phase3-dispositions.md]
---

# Phased implementation roadmap

This roadmap is revised per owner direction (transitus#1, 2026-11-26), which
supersedes DF-TRN-2026-0016. It was then challenged independently
(TRN-REV-02, `reviews/agent-reviews/adv-E.md`). All effort figures are
theoretical. **Neither implementation nor merge is authorized by this
document.** The owner reserved both until the Praxis gates pass.

## Phase 0: research, architecture, requirements (this PR)

Phase 0 is complete when the owner has accepted or revised the remaining
`review`-status decision records and the Praxis gates pass.

## DAF Landscape Phase III revision (WI-0003, 2026-11-26)

The owner strategically approved DEC-007, DEC-008, DEC-010, DEC-011 and DEC-012 (DF-TRN-2026-0022..0025). For this roadmap:
- **Phase-1 scope and budget are unchanged** (DEC-011). The revision adds
  requirements that reuse existing stages:
  - profile and schema discovery (PRF-001/002);
  - non-money sampling (VR-014);
  - the mapping-test harness (MIG-005);
  - typed absence reasons (MIG-006);
  - the effects manifest (MIG-007);
  - measurement facts (MET-001).
- **Trigger TA** gates the pre-contract assessment (ASM-001..004/006, PRF-003) and the gated measurement outputs (MET-002/003 commercial use waits for DEC-010).
- **V-4 is the Transitus evidence gate** (DF-0025). Synthetic rehearsal is a cheaper precursor that cannot satisfy it.
- The effort figures below are theoretical and are **not approved expenditure** (DEC-008).

## Phase 1: minimal declarative typed pipeline (owner-directed)

**Scope (DF-TRN-2026-0018):**

- **Pipeline:** linear and typed, conforming to `schemas/pipeline-phase1.schema.json`. In order:
  - ingest;
  - immutable raw evidence;
  - isolated temporary staging;
  - deterministic mapping and transformation, using the 13 operations of TRN-REQ-TX-009 and the closed vocabulary of TRN-REQ-PS-012;
  - validation and reconciliation, blocking with no overrides in phase 1;
  - authorization;
  - authorized domain-API load;
  - post-load verification;
  - evidence;
  - retention by policy reference.
- **Execution features:**
  - stage-granular checkpoints;
  - replay with identical keys;
  - idempotency keys;
  - dry runs;
  - migration rehearsal into a disposable sponsor cell.
- **Basic mapping packages, reusable without a signed customer:**
  - `irs.eo-bmf`;
  - the first bank partner's format (`iso20022.camt053` is illustrative);
  - `custodian.schwab` (once documentation is obtained);
  - `unbound.canonical-history`;
  - `nacha.ach` (once rights are verified).
- **Packages (budget ARC-007):** Model, Formats, Transforms, Checks, Evidence, Engine and Storage.Postgres. A 5-package variant is acceptable.
- **Ports:** two host-implemented ports, durable commands and domain destination. Echelon.Execution is used in place and never referenced (ARC-011).

**Demonstrations (theoretical, in `examples/pipelines/`):**

1. IRS EO BMF ingestion.
2. Bank activity (camt.053, illustrative) and the Schwab custodian placeholder.
3. Canonical historical migration: rehearsal, then a pre-go-live import.

**Estimated effort (TRN-REV-02 §3):**

| Work | Engineer-weeks |
|---|---|
| Formats: IRS port, bank, Schwab, canonical reader, NACHA | 3.5–6.5 |
| Checks + Evidence + 13 operations | 3–4.5 |
| Model: DU, JCS, validator, manifests | 2–3 |
| Engine: state machine, checkpoints, dry run, replay, approval, load and verify | 3–4.5 |
| Storage.Postgres with Strata-governed DDL and isolation tests | 1.5–2.5 |
| Basic mapping packages with fixtures | 1.5–2.5 |
| Abuse corpus, determinism suite, benchmark harness | 1–1.5 |
| **Transitus total** | **≈15–24** |
| **Prerequisites outside Transitus** (Unbound domain operations with read-back; canonical shape; MigrationRun and rehearsal cell; Echelon.Execution G2/G3, quota share, queue-limit fix, RM-05 benchmark) | **≈6–12** |

For comparison, earlier estimates were:
- 4–6 weeks for the three-library plan (superseded);
- 6–10 weeks for the original phase 1;
- 3–4 weeks for hand-written per-feed modules.

### Sequencing (critical path is outside Transitus)

| Step | Work | Can start | Traces to |
|---|---|---|---|
| 1 | Port the requirements renderer to F# (DF-0017) | now, once authorized | governance |
| 2 | Formats: move the `Unbound.Replay` IRS/OFAC parsers (ARC-006); strict CSV with limits | now (unlicensed-code question: OQ-12) | UNB-EXT-001, CNV-GRT-003 |
| 3 | Model + Transforms + Checks + Evidence against fakes | now | PS-011/012, TX-009, VR-*, LN-* |
| 4 | Engine against fake ports | now | EX-*, ARC-011 |
| 5 | Storage.Postgres: RLS staging with `INSERT`, isolation tests (SEC-020) | after the UC-9 decision, if `COPY` is wanted | ST-003, CNV-ARC-001 |
| 6 | `irs.eo-bmf` package + IRS demonstration end to end with a fake destination | after 2–4 | MP-009 |
| 7 | `unbound.canonical-history` package + rehearsal | **blocked** until Unbound defines the canonical shape (UNB-TRN-014) and the rehearsal cell (UNB-TRN-013) | MIG-001..004 |
| 8 | Bank package | **blocked** on the first bank partner (OQ-06) | CNV-PAY-007 |
| 9 | Schwab package | **blocked** on Schwab documentation and terms (OQ-07, MP-008) | UNB-CUST-009 |
| 10 | NACHA package | **blocked** on rights verification (OQ-16) | CNV-PAY-005 |
| 11 | Real load and verify integration | **blocked** on Unbound domain operations (UNB-TRN-005) and Echelon.Execution prerequisites | AD-008, EX-001 |
| 12 | Benchmarks (PF-001, PF-003, PF-005) | after 5 and 11 | performance |

**Exit criteria:**
- All three demonstrations run against Unbound integration environments.
- Abuse, determinism and tenant-isolation suites pass.
- Benchmarks are recorded.
- Rehearsal evidence shows zero unexplained differences on fixtures.

## Phase 2: complex DAGs (trigger T2)

**Trigger T2:** a demonstrated scenario that the phase-1 model cannot express.

**Scope:**
- routes, unions and joins;
- the expression language (TEL);
- bounded set operators (TX-011);
- governed extensions (EXT-*);
- chunk parallelism and in-engine scheduling;
- overlays (MP-003);
- Folio evidence reports;
- extraction of Echelon.Execution, once its port contract is stable.

**Estimated effort:** 6–10 engineer-weeks (theoretical).

## Phase 3: advanced AI and vendor-specific turnkey packages (trigger T3)

**Trigger T3:** AI evaluation thresholds are met (AI-008/009). For vendor packages, a customer-authorized sample and licence clearance are also needed (MP-002).

**Scope:**
- `Transitus.Assist`, provider-independent (AI-010);
- vendor packages, built only on two independent samples (MP-005).

**Ordering rule (DEC-007, MP-010).** The first vendor-specific package targets one incumbent source cluster, chosen by a recorded decision. That decision cites V-5 evidence and a customer-authorized sample. No incumbent is selected yet. Report-style sources are versioned per report version, with a drift test (MP-004).

## Pre-contract migration assessment (trigger TA)

**Trigger TA:** a recorded owner authorization naming the consumer requirement that needs the assessment. Unbound UNB-ONB-003 is `commercial-availability`.

**Scope:**
- T0 template (ASM-002);
- T1 offline profiler with disclosure controls (ASM-003, PRF-001);
- T2+ assessment in an isolated cell (ASM-004);
- deterministic mapping suggestions (PRF-003);
- the assessment report (ASM-006).

**Built from:** synthetic data and public specifications only, until customer-authorized data exists (ASM-008).

**Blocked on:** OD-TRN-P3-01 (tier legal basis) and OQ-17 (thresholds). No estimate is given; none is approved.

## Phase 4: visual editing (trigger T4)

**Trigger T4:** operators other than engineers must configure pipelines.

**Scope:** a Forma workflow projection with a round-trip guarantee and accessible alternatives (UI-001..004).

## Measurement, retirement and folding

TRN-REQ-PF-004 applies within six months of phase-1 exit. It compares the
three demonstration scenarios against hand-written alternatives on three
measures:
- effort per feed;
- defect escape rate;
- change lead time.

If the hand-written approach is materially better on all three and no second
consumer exists, the owner decides whether to retire or fold the engine.
Per owner direction, this does not gate phase 1.
