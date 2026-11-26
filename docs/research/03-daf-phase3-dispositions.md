---
id: TRN-RES-04
title: DAF Landscape Phase III Dispositions for Transitus (XRI-009..XRI-014, DEC-007/008/010/011/012)
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0003
decisions: [DF-TRN-2026-0022, DF-TRN-2026-0023, DF-TRN-2026-0024, DF-TRN-2026-0025]
provenance:
  contributions:
    EXE-20261126T203508536Z-de9f55a7:
      operations: [created]
      at: 2026-11-26T20:42:23.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "XRI-009..014 dispositions, capability coverage, assessment and boundary (DAF Phase III)"
      evidence: [kemiller2002/daf-landscape:research/competitive-displacement/data/registers/cross-repository-implications.csv]
    EXE-20261126T205108633Z-a4de7b2b:
      operations: [modified]
      at: 2026-11-26T20:51:39.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Owner resolution of OD-TRN-P3-02 (2026-11-26): DEC-008 kill rule does not gate Transitus (annotation)"
      evidence: [DF-TRN-2026-0026]
    EXE-20261126T210016939Z-536fe55b:
      operations: [modified]
      at: 2026-11-26T21:01:24.000Z
      actor:
        kind: agent
        id: anthropic/claude-code
        provider: anthropic
        model: unknown
        runtime: claude-code
      reason: "Stage I review fixes S1-06/07/08/15 and OD-P3-04 note (WI-0005)"
      evidence: [docs/research/03-daf-phase3-dispositions.md]
---

# DAF Landscape Phase III: dispositions for Transitus

**Authority.** On 2026-11-26 the owner approved DAF Landscape Phase II decisions
DEC-001..DEC-012 and authorized the progression of XRI-001..XRI-018 subject to
their documented conditions. Approval authorizes strategic direction,
requirements refinement, research and planning only. It does not authorize
expenditure, contractual commitments, production deployment, removal of
mandatory controls or implementation. Nothing here moves any decision past
**strategically approved**.

**Sources (cited, not copied).** In `kemiller2002/daf-landscape`:
- `research/competitive-displacement/`: reports 08, 18, 22 and 23, and
  `data/registers/cross-repository-implications.csv` (rows XRI-009..XRI-014,
  read verbatim) and `decisions.csv`.
- `research/commercial-opportunity/migration-integration-tooling/`
  (D-MIT-001/002).
- `research/competitive-advantage/charity-network-and-onboarding/`, reports
  13-17 and 21.

In `kemiller2002/unbound` (read-only):
- `requirements/discovery/2026-11-26-transitus-integration/` (UNB-TRN-001..014);
- `requirements/discovery/2026-11-26-charity-network-and-onboarding/`
  (UNB-ONB-001..033).

Requirement changes are in revision `DAF-P3-2026-11-26` of
`tools/requirements_source.py`: 19 new requirements and 4 refined
requirements, all `proposed`.

## 1. What PR #1 established, and XRI-014

transitus#1 was merged at `d1b97be` on 2026-11-26 (19:59 UTC). It created the
whole repository content. That content covers:
- the Praxis 3.26.0 installation;
- competitive research;
- architecture TRN-ARCH-00..12;
- the threat model;
- 152 `proposed` requirements;
- decision records DF-TRN-2026-0001..0021;
- schemas, demonstration pipelines and basic package manifests;
- reviews TRN-REV-01 and TRN-REV-02.

The owner direction on the PR (comment 7200249612) produced the accepted
records DF-0018..0021. Those records supersede DF-0016 (phase gating and kill
criterion), DF-0014 (mapping packages), DF-0008 (staging) and DF-0006
(Execution extraction timing). The same comment said "do not implement or
merge until Praxis gates pass". The merge therefore records that those gates
passed for research and requirements. Every accepted record still states
that acceptance does not authorize implementation, and no code exists.

**Does Phase II's provisional reliance still hold?** Yes in substance, with
two citation corrections:

| Phase II reliance (report 18 §1, report 08 §2) | Status at `d1b97be` |
|---|---|
| Pure, total, versioned transformations; content-addressed raw; Merkle-sealed staging (TRN-REQ-TX/ST) | Holds: TX-001..006, ST-001 and ST-005 are phase 1 |
| AI proposes, deterministic gates dispose (DF-0012) | Holds: DF-0012 `review`; AI is phase 3 (AI-001, AI-009) |
| Mapping packages configuration-only (DF-**0014**); basic packages in phase 1 (DF-0019) | Holds, but DF-0014 is **superseded** by DF-0019. DF-0019 carries its rules forward, so cite DF-0019 |
| Generic reconciliation primitives (DF-0011) | Holds: DF-0011 `review`; VR-001..013 |
| Phase gating and kill criterion (DF-**0016**) | **Weakened.** DF-0016 is superseded by DF-0018. The replacement measurement TRN-REQ-PF-004 does **not** gate phase 1 (owner direction). The claim that Transitus has a kill criterion consistent with the gated strategy no longer holds as written. Raised as OD-TRN-P3-02 (§6) **Annotation 2026-11-26:** the owner resolved OD-TRN-P3-02. The DEC-008 kill rule does not gate Transitus (DF-TRN-2026-0026) |
| Evidence stage, rehearsal, canonical import | Holds and is strengthened: MIG-001..004, MP-009, Unbound UNB-TRN-011..014 |

**XRI-014 disposition: Already satisfied.** The status note is now obsolete
because the PR is merged. Phase II should cite DF-0019 rather than DF-0014, and
DF-0018 with PF-004 rather than DF-0016. This is a correction for the
daf-landscape owner. Transitus records nothing beyond this note.

## 2. Cross-repository implications, one by one

Disposition classes:
- Already satisfied
- Requirements updated
- New requirement added
- Existing decision superseded
- Research-only
- Deferred behind an explicit gate
- Blocked by unavailable information
- Requires a new owner decision

### XRI-009: onboarding maturity levels 0-5 as measurement targets

| Field | Content |
|---|---|
| Affected area | Measurement and evidence (`measurement` category) |
| Original evidence | Row: "Add onboarding maturity model levels 0-5 as measurement targets for migrations", requirement-candidate, Track D synthesis, SRC-066. Model and metrics: competitive-displacement `08` §5. "Claim a level only from measured data"; levels 4-5 cannot be evidenced for years (CHL-076) |
| Affected requirements and decisions | LN-003 (evidence package), MIG-001 (rehearsal), PF-004 (later measurement); DEC-010 → DF-TRN-2026-0024 |
| Already addressed? | Partly. The evidence package carries conservation and reconciliation results. It does not carry the progression metrics: default-mapped share, engineering changes, mock-to-live delta, extract-to-go-live time, defects per 1k |
| Conflicts, duplication, gaps | Gap: no metric facts. There is a risk that a level is claimed from one or two migrations. Unbound UNB-ONB-030 measures outcome metrics on the consumer side. Transitus supplies execution facts only, so the work is not duplicated |
| Refinement | MET-001 records facts and marks unobservable ones `unavailable`. MET-002 computes levels only as internal targets, with numerator, denominator, window and minimum sample. Levels are not published until the DEC-010 gate is recorded |
| Disposition | **New requirement added** (MET-001). Level claims are **Deferred behind an explicit gate** (MET-002; gate: V-4 passed, recorded as evidence-gate satisfied, contractual review complete) |
| Acceptance (GWT) | Given a rehearsal with no host-supplied go-live time, When evidence is produced, Then go-live is `unavailable`, not zero. Given two measured migrations and a minimum sample of three, When a level is computed, Then it reads "not evidenced". Given no recorded DEC-010 gate, When an external report is generated, Then levels are omitted |
| Validation requirements | Evidence-schema test for MET-001 fields; property test that missing facts never become zero; report test for MET-002 suppression |

### XRI-010: pre-contract assessment tiers T0/T1/T2+

| Field | Content |
|---|---|
| Affected area | New `assessment` and `profiling` categories |
| Original evidence | Row: "T0 no-install template; T1 profiler after sponsor IT approval with minimum fund count and dominance suppression; T2+ only under MSA + DPA; synthetic runs are conformance checks only", SRC-066. Also `08` §3 (revision 2, CHL-017/040/069/070/072) and charity-network `13` (T0-T4 ladder, readiness report, effort drivers) |
| Affected requirements and decisions | AI-007 (masked profile statistics), EX-004 (dry run), MIG-001, MP-001/002; DEC-011 → DF-0022; DEC-012 → DF-0025 |
| Already addressed? | No. The `profile` stage existed only as an optional stage kind in TRN-ARCH-01, with no requirement, no disclosure control and no assessment mode |
| Conflicts, duplication, gaps | **Conflict (UC-17):** the legal-basis level differs. Phase II revision 2 says T1 needs sponsor IT approval and T2+ needs an MSA and a DPA. Charity-network `13` and Unbound UNB-ONB-003 say T0-T1 need an NDA and T2 needs an NDA/DPA. Transitus adopts the stricter Phase II form as **required host-supplied references** and leaves legal sufficiency to the host and counsel (ASM-001). This is escalated as OD-TRN-P3-01. **Gap:** disclosure-control thresholds. Research proposes k = 10. No threshold is adopted as binding (OQ-17). **Duplication avoided:** pricing and onboarding estimates (UNB-ONB-004), the extraction plan (UNB-ONB-002) and the migration class (UNB-ONB-001) stay in Unbound |
| Refinement | PRF-001 (profile with disclosure controls), PRF-002 (schema discovery), PRF-003 (deterministic mapping suggestions), ASM-001..008 (§4) |
| Disposition | **New requirement added.** ASM-001..004/006 and PRF-003 are **Deferred behind an explicit gate** (trigger TA in ARC-009). ASM-005/007/008 apply now as constraints |
| Acceptance (GWT) | In each ASM/PRF row, for example: Given a T1 engagement, When a record-level file is submitted, Then it is rejected before persistence |
| Validation requirements | Tier-enforcement tests; disclosure-control property tests (no emitted cell below k; dominance rule); direct-identifier scan corpus; determinism (same inputs → same report hash); a test that synthetic runs never emit quality, effort or timeline |

### XRI-011: migration SLA clock from a conforming extract, with a published exclusions list

| Field | Content |
|---|---|
| Affected area | Measurement and conformance |
| Original evidence | Row: "SLA clock that starts on a conforming extract plus a published exclusions list (Stripe pattern)", CLM-022, SRC-044/SRC-066. Report `18` §2 adds a sponsor-approved validation summary; `08` §6 says process SLAs only, capped liability, after V-4 (CHL-074/075) |
| Affected requirements and decisions | MP-004 (format detectors), VR-001/002, LN-003; DEC-010 → DF-0024 |
| Already addressed? | No. Conforming-extract determination was not specified |
| Conflicts, duplication, gaps | UNB-ONB-030 already counts delivery "from receipt of a usable extract". Transitus defines what *conforming* means mechanically. Unbound owns any commitment. No SLA figure is adopted; the Stripe 10-business-day figure is an external reference only |
| Refinement | MET-003: deterministic conformance, clock-start timestamp, host-supplied exclusions list, sponsor validation summary for host approval |
| Disposition | **Deferred behind an explicit gate.** The measurement capability is added (MET-003, P2). Any commitment or publication waits for the DEC-010 gate |
| Acceptance (GWT) | Given an extract without its control file, When conformance runs, Then it is non-conforming and no clock start is recorded. Given a conforming extract, Then the clock start equals the determination time and a validation summary is produced |
| Validation requirements | Conformance fixtures (missing control file, wrong version, truncated file); summary-schema test; review that no SLA duration exists in Transitus |

### XRI-012: statistical sampling for non-money attributes alongside exact money reconciliation

| Field | Content |
|---|---|
| Affected area | Validation and reconciliation |
| Original evidence | Row: "Add statistical-sampling validation for non-money attributes alongside exact money reconciliation", JAMIA evidence SRC-045 (also GAO-22-103718, SRC-046). Charity-network `16` L11/G28 (stratified attested sample) and G29 (invariants plus mutation detection) |
| Affected requirements and decisions | VR-002/003 (exact money, zero tolerance), VR-010 (post-load verification), DF-0011; the verify-stage `sample` in TRN-ARCH-01 |
| Already addressed? | Partly. The verify stage had an illustrative `sample: {rate, min}`, with no rule against sampling money and no stratification, seed or evidence |
| Conflicts, duplication, gaps | Risk: sampling could be applied to money. VR-010 is now explicit that money and counts are exact over the full population. Gap: total-preserving mis-mappings, which aggregate ties cannot see. Added MIG-005 (mutation and invariant harness). Mapping approval states stay in Unbound (UNB-ONB-005) |
| Refinement | VR-014 (deterministic, seeded, stratified, consumer-parameterized, refuses money); VR-010 refined; MIG-005 |
| Disposition | **New requirement added** (VR-014, MIG-005) and **Requirements updated** (VR-010) |
| Acceptance (GWT) | Given a sampled check declared on a money field, When it is published, Then validation rejects it. Given the same seed, Then the same sample. Given a total-preserving swap of two codes, When the harness runs, Then totals pass and the mutation/invariant check fails |
| Validation requirements | Property tests: determinism under a seed; no sample frame includes money, quantity or count fields; mutation-detection fixtures |

### XRI-013: vendor packages deferred until an authorized sample exists; one source cluster first

| Field | Content |
|---|---|
| Affected area | Roadmap and mapping packages |
| Original evidence | Row: roadmap-note, DEC-007 and DEC-011, SRC-006. `08` §4 (inference that a second migration from the same source costs less; CHL-071 report-version drift; CHL-072 report adapters are balance-level only) |
| Affected requirements and decisions | DF-0019, ARC-009 (T3), MP-002, MP-004, MP-006; DEC-011 → DF-0022; DEC-007 → DF-0023 |
| Already addressed? | **Deferral: yes** (DF-0019, ARC-009, MP-006). **Single-cluster ordering and per-report-version drift tests: no** |
| Conflicts, duplication, gaps | No incumbent is chosen. The Phase II examples (NPact/FIMS, iPhi) are not a selection (DEC-007: "do not select arbitrarily") |
| Refinement | MP-010 (the first vendor package needs a recorded selection citing V-5 evidence and an authorized sample; **revised 2026-11-26, review finding S1-07:** Transitus consumes Unbound's selection record, UNB-CDD-ONB-002, which is its single owner, rather than requiring its own); MP-004 refined (per report version, drift test); ARC-009 refined; roadmap note |
| Disposition | **Requirements updated** (MP-004, ARC-009). The deferral is **Already satisfied**. The first-package rule is **New requirement added** (MP-010), itself **Deferred behind an explicit gate** (T3) and **Blocked by unavailable information** (no customer-authorized sample; V-5 not run) |
| Acceptance (GWT) | Given no recorded selection, When a vendor package is proposed, Then publication is refused. Given an input matching no declared report version, When the drift test runs, Then it fails |
| Validation requirements | Package-lint rule for the selection reference; drift-test fixture |

### XRI-014: PR #1 unmerged; provisional evidence

See §1. **Disposition: Already satisfied.** No requirement change. The
citation corrections are listed for daf-landscape.

## 3. Capability coverage (task scope)

The existing requirements are refined, not duplicated. "New" marks a gap closed
in this revision.

| Capability | Requirements | Owner split |
|---|---|---|
| Source acquisition | AD-001..006, ST-001 (acquisition metadata), ST-002 | Transitus. The Extraction Plan is Unbound's (UNB-ONB-002) |
| Immutable staging | ST-001, ST-003, ST-005 (Merkle seal), ST-006 | Transitus; the cell and DDL are host |
| Profiling | **PRF-001 (new)**, AI-007 | Transitus generic |
| Schema discovery | **PRF-002 (new)**, MP-004 (refined) | Transitus generic |
| Mapping suggestions | **PRF-003 (new, TA)**, AI-001/009 (phase 3) | Transitus proposes; approval is the host's |
| Deterministic transformation | TX-001..006, TX-009, AI-005 | Transitus |
| Canonical data contracts | MP-001, MP-009, MIG-002, **MIG-006 (new)** | Mechanism is Transitus; the shape is Unbound's (UNB-TRN-014, UNB-ONB-006) |
| Validation | VR-001, VR-004, VR-013 | Transitus primitives; Unbound profiles |
| Reconciliation, exact money | VR-002, VR-003, VR-010 (refined), MIG-001 | Transitus primitives; tolerances are Unbound's (VR-006) |
| Reconciliation, non-money sampling | **VR-014 (new)**, **MIG-005 (new)** | Transitus primitive; strata and parameters are Unbound's |
| Historical preservation | ST-001, MIG-002, MIG-004, LN-001 | Transitus evidence; the legacy partition and epoch are Unbound's (UNB-ONB-007) |
| Domain-API integration | AD-008, AD-011, AD-012, ARC-011 | Transitus port; operations are Unbound's (UNB-TRN-005) |
| Idempotency | EX-006, EX-007, EX-008 | Transitus |
| Replay | EX-014, SEC-016 | Transitus |
| Rehearsal | MIG-001 (refined), MP-009 | Transitus run; the cell and run count are Unbound's (UNB-TRN-013, UNB-ONB-011) |
| Cutover | MIG-003 (no MigrationRun change; fence check) | Unbound (MigrationRun, fence, cutover decision) |
| Rollback | **MIG-007 (new, effects manifest)**, EX-009 (no automatic compensation) | The boundary and rollback are Unbound's (UNB-ONB-017) |
| Evidence generation | LN-003, LN-006, **MET-001 (new)** | Transitus |

## 4. Pre-contract migration assessment

Specified by ASM-001..008 with PRF-001..003. The assessment answers, per
tier:
- source data quality;
- mapping complexity;
- missing information, including history depth per entity;
- reconciliation risks;
- estimated effort, as driver counts × labelled assumptions with ranges, with
  no currency figures;
- required customer participation;
- potential timeline, as ranges with incumbent-dependent steps marked.

Every finding states its tier and basis. A finding that cannot be assessed at
the current tier names the tier that would resolve it.

| Tier | What leaves the sponsor | Precondition reference (host-supplied) | Transitus capability |
|---|---|---|---|
| T0 | Nothing record-level: a sponsor-completed template | none beyond engagement | ASM-002 template and validation |
| T1 | Disclosure-controlled structural aggregates only | Recorded sponsor IT approval (Phase II rev 2); legal basis per OD-TRN-P3-01 | ASM-003 offline profiler (PRF-001 controls; identifier scan; signed profile) |
| T2+ | Record-level data in an isolated assessment cell | Executed MSA **and** DPA | ASM-004 (dry run, no system-of-record effect, purge by policy) |
| Synthetic | Nothing | none | ASM-005: conformance check only; never quality, effort or timeline |

Until customer-authorized data exists, development and tests use synthetic
data and public specifications only (ASM-008). Every element that rests on an
unverified vendor assumption is flagged `vendor-assumption-unverified`
(ASM-007). All of ASM-001..004/006 and PRF-003 wait for trigger **TA**, a
recorded owner authorization naming the consumer requirement that needs them.
Unbound UNB-ONB-003 is `commercial-availability`, not release 1. The phase-1
budget (ARC-007) is unchanged.

> **Correction (2026-11-26, WI-0005, review finding S1-06; text above kept):**
> only the ARC-007 counts are unchanged. revision DAF-P3-2026-11-26 added 18 phase-1 requirement rows (phase-1 total 121 → 139; P0 106 → 108: MIG-006 and MIG-007). Eight are gated and excluded from phase-1 exit (TA: ASM-001..004/006, PRF-003; DEC-010: MET-002/003, see TRN-REQ-ARC-009). Ten are ungated: PRF-001/002, VR-014, MIG-005/006/007, MET-001 and the constraints ASM-005/007/008. Their statements name no new code package, third-party parser, mapping package, transformation operation (of the 13) or port, so the ARC-007 *counts* are not exceeded on the text; they do add work inside existing packages (Formats: PRF-002; Checks: PRF-001, VR-014, MIG-005; Model: MIG-006; Engine/Evidence: MIG-007, MET-001) that is **not estimated**. Phase-1 scope therefore grows; these are proposed additions pending owner acceptance, not an unchanged scope.
> TRN-REQ-ARC-009 now names the phase-1 rows that are TA-gated or
> DEC-010-gated.

## 5. Boundary: generic Transitus vs Unbound-specific

This boundary is consistent with the Unbound transitus-integration package
("Boundary") and UNB-ONB-*.

| Capability | Generic Transitus | Unbound-specific |
|---|---|---|
| Parsing, raw evidence, staging, lineage, evidence packages | ✓ | RawEvidence model alignment (UNB-TRN-002) |
| Profiling with disclosure controls; schema discovery | ✓ (mechanism) | Threshold values (policy) |
| Mapping suggestions | ✓ (proposals only) | Mapping lifecycle and approvals: Proposed → Tested → SponsorConfirmed → Pinned (UNB-ONB-005) |
| Mapping test harness (round-trip, invariants, mutation) | ✓ | Invariant rules and swap catalogue for DAF entities |
| Validation and reconciliation primitives, including sampling | ✓ | Gate set G01-G29, tolerances, strata, materiality (UNB-ONB-013, CNV-FIN-011) |
| Typed absence reasons | ✓ (mechanism) | The enumeration and canonical history shape (UNB-ONB-006, UNB-TRN-014) |
| Idempotency, replay, dry run, rehearsal execution | ✓ | Rehearsal cell, minimum trial-run count (UNB-TRN-013, UNB-ONB-011) |
| Effects manifest | ✓ | Rollback boundary, effects ledger and rollback (UNB-ONB-017) |
| Domain loading | Port only (AD-008, ARC-011) | Domain operations (UNB-TRN-005), MigrationRun, fence, cutover (UNB-TRN-011, MIG-003) |
| Assessment tiers and report | ✓ (mechanism, tier enforcement, report) | Legal basis, migration class, extraction plan, pricing/estimate band (UNB-ONB-001/002/003/004) |
| Measurement facts, conformance clock | ✓ | Outcome report and any service commitment (UNB-ONB-030), gated by DEC-010 |
| First-vendor selection | Package rule (MP-010): consumes the selection record | The selection record itself (UNB-CDD-ONB-002), citing V-5 evidence |

## 6. Owner decisions and questions raised

None of these is resolved by this revision.

| ID | Question | Why |
|---|---|---|
| OD-TRN-P3-01 | Which legal-basis and approval preconditions bind each assessment tier: Phase II revision 2 (T1 after sponsor IT approval; T2+ under MSA + DPA) or charity-network `13` / UNB-ONB-003 (T0-T1 NDA; T2 NDA/DPA)? | The sources conflict (UC-17). Transitus requires the stricter references by default; counsel and the owner decide |
| OD-TRN-P3-02 | Does the DEC-008 kill rule (no named partner by month 6; no referenceable pilot by month 24) pause Transitus work beyond phase 1, given that PF-004 is non-gating? | DEC-008 asks for explicit termination criteria. Transitus has none that gate (§1) | **Resolved 2026-11-26 by the owner** ("Kill rule doesn't stop Transitus"; DF-TRN-2026-0026).
| OQ-17 | Disclosure-control thresholds for T1: minimum contributor count, minimum population (fund count), dominance share | Research proposes k = 10 (charity-network `13`). No binding default is adopted (PRF-001) |

## 7. Decision status (status ladder)

| Decision | Transitus record | Rung |
|---|---|---|
| DEC-011 | DF-TRN-2026-0022 | Strategically approved. Transitus requirements incorporated as `proposed` rows (ASM-005/007/008 and others); not evidence-gate-satisfied |
| DEC-007 | DF-TRN-2026-0023 | Strategically approved. Requirements incorporated as `proposed` (MP-010, MP-004, ARC-009) |
| DEC-010 | DF-TRN-2026-0024 | Strategically approved. Requirements incorporated as `proposed` (MET-001..003); the V-4 gate is not satisfied |
| DEC-012, DEC-008 | DF-TRN-2026-0025 | Strategically approved (constraints only) |

## 7a. DEC-005 trace: AI and mapping suggestions are advisory (review finding S1-15)

DEC-005 (owner-approved 2026-11-26) says AI assessments and inferred records are advisory. They never silently become authoritative facts or financial, regulatory or eligibility decisions. In Transitus this is implemented by these existing rows. No new requirement is needed.

| Requirement or decision | How it implements DEC-005 |
|---|---|
| DF-TRN-2026-0012 | AI may only propose pipeline diffs; deterministic gates dispose |
| TRN-REQ-AI-001 | AI output is a PipelineDiff proposal only; it cannot execute, publish, approve or load |
| TRN-REQ-AI-002 | AI-generated configuration passes the same deterministic validation, dry run and authorization as human changes |
| TRN-REQ-AI-005 | The runtime path contains no model calls; results are deterministic |
| TRN-REQ-AI-006 | AI proposals record model, provider, prompt version and hashes (labelled, traceable) |
| TRN-REQ-AI-008, AI-009 | No accuracy claim and no enablement without measured precision |
| TRN-REQ-PRF-003 | Mapping suggestions, deterministic or AI, are proposals and are unusable until accepted through the human publish path |
| TRN-REQ-PRF-002 | Schema discovery reports candidates; it never selects or publishes |
| TRN-REQ-MIG-005 | The harness produces evidence only; mapping approval states stay with the consumer (UNB-ONB-005) |
| TRN-REQ-ASM-005, ASM-007 | Synthetic or unverified-assumption findings are labelled and excluded from evidenced totals |

## 8. Validation requirements for this revision

- `python3 -I tools/render_requirements.py --check`: the generated register
  matches the source.
- `python3 -I tools/validate_specs.py`: schemas and examples are unchanged
  and valid.
- `./praxis registry build`, then `./praxis validate`.
- Future implementation tests are named in each requirement's acceptance
  criteria. None can run yet: there is no code, and implementation is not
  authorized.
