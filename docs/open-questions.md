---
id: TRN-OQ
title: Open Questions, Owner Resolutions and Unresolved Conflicts
status: proposed
version: 0.2.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0002
owner_resolution: https://github.com/kemiller2002/transitus/pull/1#issuecomment-7200249612
---

# Open questions

The owner resolved most questions on 2026-11-26 (transitus#1). The
resolutions are recorded in DF-TRN-2026-0018..0021. Questions that depend
on evidence not yet obtained stay **open** until that evidence exists, as
the owner directed.

## Resolved by the owner

| ID | Question | Owner resolution | Recorded in |
|---|---|---|---|
| OQ-01 | When is Echelon.Execution extracted? | Defer extraction until the shared contract is stable; use it in place meanwhile. | DF-0021, TRN-REQ-EX-001 |
| OQ-02 | Where is the boundary between Strata DIV and Transitus? | DIV virtualizes interactions; Transitus moves data. | DF-0021, TRN-REQ-ARC-010 |
| OQ-04 | Is there a portfolio object store for raw evidence? | Blob port with a database default, subject to sizing. | DF-0020, TRN-REQ-ST-007 |
| OQ-05 | How are destinations without idempotency handled? | Unknown external outcomes must not be blindly retried. | DF-0021, TRN-REQ-EX-007 |
| OQ-08 | Which AI providers are approved? | Provider-independent; authorization per tenant and classification; no blanket provider approval. | DF-0021, TRN-REQ-AI-010 |
| OQ-09 | Event streams or CDC? | Defer CDC. | DF-0021 |
| OQ-10 | Binding retention periods? | By approved classification and sponsor policy; no invented binding durations. Schemas and examples now use `policy:` references. | DF-0021, TRN-REQ-LN-010 |
| OQ-11 | Currency conversion? | FX decisions remain domain-owned. | DF-0021 |
| OQ-13 | Is migration in Unbound release 1? | **Yes.** Canonical historical import and migration rehearsal are required in release 1; vendor-specific turnkey packages may follow. | DF-0018, Unbound UNB-TRN-006/011/012 |
| OQ-14 | Separate repository or inside Unbound? | **Independent embeddable Transitus repository, no separate service.** | DF-0018 |
| OQ-15 | Will Unbound define the domain operations Transitus loads through? | Authorized domain loading interfaces are mandatory. | TRN-REQ-AD-008, Unbound UNB-TRN-005 |

## Open, pending evidence

| ID | Question | Owner direction | Evidence needed | Blocks |
|---|---|---|---|---|
| OQ-03 | Who owns runtime observability (GAP-05), tamper-evident evidence storage (GAP-07) and auditor export (GAP-06)? | Investigate Arca and portfolio ownership before assigning. | An assessment of Arca's fitness, given that ARCA-REC-007 excludes large binaries, and a portfolio owner decision. | Production use, not phase-1 design. |
| OQ-06 | Which bank activity format comes first? | Select it from the first bank partner. | Partner selection and its format specification. `iso20022.camt053` is illustrative only. | Phase-1 bank package content. |
| OQ-07 | Which custodian format comes first? | Prioritize Schwab's documented format. | Schwab's file documentation, obtained under terms that allow use and, if published, redistribution. `custodian.schwab` stays a placeholder until then, with nothing invented. | Phase-1 custodian package content. |
| OQ-12 | Licence: MIT or PolyForm Noncommercial? | Resolve against the authoritative portfolio licensing policy before release. | The portfolio decision OD-GOV-018 (registry DRF-09). | First release, not this research phase. |
| OQ-16 | Can NACHA layouts be redistributed in `nacha.ach`? | Verify NACHA redistribution rights. | A review of the NACHA Operating Rules licence terms. The package is internal-only until then (TRN-REQ-MP-008). | Publishing `nacha.ach`. |

## Unresolved conflicts

These are tensions between the owner-directed scope and other evidence or
governance. Each is recorded rather than silently resolved.

| ID | Conflict | Evidence | Who resolves |
|---|---|---|---|
| UC-1 | Owner phase-1 scope vs adversarial findings C3 (complexity) and C11 (maintenance). Phase 1 now has 117 requirements, 101 of them P0, against 47 P0 in the three-library plan, and up to 7 code packages for a single-owner portfolio. | TRN-REV-01; `agent-reviews/adv-A.md`, `adv-D.md`, `adv-E.md`. | Owner. Mitigated by the linear profile, the ARC-007 budget and the PF-004 later comparison. |
| UC-2 | Migration rehearsal is required in release 1, but there is **no design partner** (Unbound OD-M-14), so no real predecessor export exists to rehearse against. | Unbound `owner-decisions.jsonl` OD-M-14. | Owner and Unbound. Until an export exists, rehearsal is proven on synthetic canonical fixtures only. |
| UC-3 | The simplification discovery's "REQ-X-061 Out (no migration in R1)" record still exists in Unbound and now contradicts the owner's resolution. | `unbound/requirements/discovery/2026-11-24-simplification-economics/01-REVERSE-REQUIREMENTS-ANALYSIS.md:571`. | Unbound owner, through Unbound's ratification process. Not edited by this initiative. |
| UC-4 | Phase-1 loading needs Unbound domain operations that do not exist yet, and an Echelon.Execution that is unbenchmarked (RM-05). Lease renewal, dependency resume, payload purge and metrics are unimplemented (G1–G4). | `unbound/execution/README.md`; Unbound UNB-TRN-005. | Unbound and the INIT-012 owners. Phase-1 load and verify depend on them. |
| UC-5 | The licence directive (MIT) conflicts with the portfolio's component licensing (PolyForm Noncommercial). | Registry DRF-09, OD-GOV-018. | Owner, before release (OQ-12). |
| UC-6 | Staging partition maintenance needs a governed DDL mechanism that Strata does not yet offer (DEP-STRATA-01). Phase 1 falls back to DELETE with measured vacuum cost. | TRN-ARCH-02; Strata README. | Strata owner. |

### Additional conflicts from the independent challenge (TRN-REV-02, `reviews/agent-reviews/adv-E.md` §4)

| ID | Conflict | Evidence | Who resolves |
|---|---|---|---|
| UC-7 | More Unbound records than UC-3 still defer migration. UNB-XIN-OTH-002 says "no migration in R1" in the release-1 scope record. The simplification matrix marks RR-REQ-X-061-r1 and UNB-RCN-WF-020 "defer". | `unbound/requirements/discovery/2026-11-23-cross-industry/17-RELEASE-1-SCOPE.md:108`; `unbound/requirements/discovery/2026-11-24-simplification-economics/02-REQUIREMENT-SIMPLIFICATION-MATRIX.md:1731,1750` | Unbound owner: record the decision in `owner-decisions.jsonl` and re-scope those rows. |
| UC-8 | No canonical historical import shape exists in Unbound. CNV-EXP-002 also requires documents and acknowledgments, which the Transitus value model does not transform; they are passed through as RawEvidence (TRN-REQ-MIG-004). | Unbound repository search; CNV-EXP-002 | Unbound owner and domain owner (proposal UNB-TRN-014) |
| UC-9 | CNV-ARC-001 requires row-level security on every tenant table, but PostgreSQL `COPY` does not work on RLS tables. Phase 1 uses `INSERT`; a `COPY` load table needs a documented exception. | Unbound baseline CNV-ARC-001; PostgreSQL documentation | Unbound architecture owner |
| UC-10 | Rehearsal needs a disposable sponsor cell. Rehearsing on the shared cluster could affect live sponsors. | TRN-REQ-MIG-001; CNV-ARC-001 | Unbound architecture owner (proposal UNB-TRN-013) |
| UC-11 | Staging public BMF data once conflicts with the CNV-TEN-001 SharedStoreRegister, so ST-010 is deferred to phase 2. | Unbound baseline CNV-TEN-001 | Unbound architecture owner |
| UC-12 | Licensing. Porting the `Unbound.Replay` parsers, which carry no licence in Unbound, into an MIT repository. A Schwab specification obtained under NDA cannot go into a public package. NACHA rights are unverified. | Registry DRF-09; OQ-07, OQ-12, OQ-16 | Portfolio owner (OD-GOV-018). Schwab and NACHA also need counsel or contract review. |
| UC-13 | "Schwab documented format" conflicts with Unbound's own statement that no Schwab API or format is assumed. Only third-party code tables are public. | `unbound/requirements/integrations/CUSTODIAN-AND-INVESTMENT-MANAGEMENT.md:5,58,75` | Unbound owner: name the Schwab channel and obtain a licensed specification. |
| UC-14 | "Bank format from the first partner", but no bank or ODFI partner exists. Until one does, the bank package claims conformance only to the public base standard. | OQ-06 | Unbound owner |
| UC-15 | Observability is unowned (GAP-05), and Echelon.Execution metrics are blocked on U-07. Transitus emits OpenTelemetry through the host (OBS-001) but cannot supply monitoring ownership. | Registry OD-GOV-024; `unbound/execution/README.md` | Portfolio owner (OQ-03); Unbound owner for U-07 |
| UC-16 | The registry lists Transitus as `active` against four initiatives before any code exists. | Registry PR #123 | Portfolio owner. Maturity is `requirements`; the status can be lowered to `experimental` if preferred. |
