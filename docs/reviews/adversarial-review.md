---
id: TRN-REV-01
title: Adversarial Review and Dispositions
status: proposed
version: 1.0.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
reviewers: "Four independent agent reviewers (A–D). Each was briefed only with the document paths, the evidence repositories and the claims to refute, not with the author's conclusions."
full_reviews: [agent-reviews/adv-A.md, agent-reviews/adv-B.md, agent-reviews/adv-C.md, agent-reviews/adv-D.md]
---

# Adversarial review and dispositions

## Method

The brief (§19) lists twelve challenges. Four independent reviewer agents
took three each and were asked to **refute** the proposal with evidence:
repository file and line references, or source-register IDs. Each reviewer
gave a verdict and the revisions it required. The author checked the
reviewers' load-bearing factual claims against the primary sources before
accepting them. Two claims were corrected on that check (marked ⚠).

"Upheld" means the challenge succeeded and the proposal, as written, fails
on that point.

## Summary of verdicts and dispositions

| # | Challenge | Reviewer | Verdict | Disposition (what changed) |
|---|---|---|---|---|
| C1 | Transitus duplicates Strata or existing Echelon capabilities | A | **Partially upheld.** No duplication of Strata. But it re-specified Echelon.Execution semantics, competed with Unbound's `AcquisitionRun/RawEvidence` model, and would have duplicated `Unbound.Replay/Sources.fs`. | Phase 1 **adopts** Unbound's RawEvidence model, **moves** the IRS/OFAC parsers into `Transitus.Formats`, and relies on Echelon.Execution for retries and OutcomeUnknown (TRN-REQ-ARC-006). The raw-bytes rule now honours rights policy (ST-001). Summa and Helix Note are downgraded to *candidate* consumers. |
| C2 | Existing products would be more economical | A | **Partially upheld.** dlt, Meltano and Hop fail the F#-only rule; SaaS tools fail on regulated data. The real cheaper baseline is hand-written per-feed F#, and the proposal never costed it. | The per-feed baseline is added (TRN-ARCH-12 §5a). Phase 1 is reduced to the libraries those modules would otherwise duplicate. TRN-REQ-PF-004 requires a recorded comparison before phase 2, which acts as a kill criterion. Migration revenue is no longer a phase-1 justification. |
| C3 | The pipeline model is too complex | A | **Upheld.** About six fixed release-1 feeds against 89 P0 requirements, 16 stage kinds (the docs claimed 14), a custom expression language, packages, overlays and envelope diffs. | The declarative model, expression language, validator and engine move to **phase 2 behind trigger T2**; packages and AI move to phase 3 (T3). P0 count falls from 89 to 52, of which 47 are phase-1 (51 phase-1 requirements in total). Phase-1 feeds are written in F# against the same stage functions, so the later DU model serializes them without semantic change. Stage count corrected. |
| C4 | Declarative transformations are expressive enough | B | **Upheld (fixable).** Counter-examples from U1, U9, U10, H1 and H2 that the catalogue cannot express: fill-down and running totals, as-of joins, fiscal periods, schedule explosion, duplicate clustering, unpivot, FHIR lists, regex capture. The F# escape hatch covered single values only, and .NET cannot sandbox in-process code. | Bounded set operators added (TRN-REQ-TX-011). Extension governance added (EXT-001..004): set-level extensions are allowed, safety rests on review, signing and allow-listing, and each extension is recorded with the scenario that needed it. Parse operations reclassified from "reversible" to value-preserving irreversible (factual error fixed). |
| C5 | Database staging creates unacceptable bottlenecks | B | **Partially upheld.** The arithmetic mostly held. But the default design was unworkable as written: LIST partitions take one column; per-dataset partitions need runtime DDL; `COPY FROM` is unsupported with RLS; a shared schema conflicts with CNV-ARC-001 schema-per-sponsor; WAL would pass through the synchronous standby; data survives the TTL in backups. The UNLOGGED recovery claim was wrong. | Storage decision rewritten (TRN-ARCH-02, DF-TRN-2026-0008 revised). Phase 1 has **no** Transitus-owned staging. Phase-2 staging goes in the tenant schema, loads through a load table, and uses crypto-shredding. Added ST-009 (UNLOGGED recovery) and ST-010 (shared public reference data). PF-002 raised to P0. |
| C6 | AI-assisted mapping is reliable enough | B | **Partially upheld.** Containment is sound, but the authority check missed *semantic* changes (idempotency keys, auto-approve conditions, code maps, swapped fields). Profile statistics leak personal data. Annotations can carry injected text. Evaluation was not a gate. ⚠ Corrected an earlier author error: Helix Note calls the OpenAI API, not Azure OpenAI (`HelixNote.AI.OpenAI.fs:110`). | PS-008 extended to semantic-critical review. AI-007 masks profile statistics; AI-003 excludes annotations. AI-008 raised to P0 and made an enablement gate (AI-009). AI is phase 3. |
| C7 | Reusable migration packages are practical | C | **Partially upheld.** Vendor packages are impractical. There are no public schemas; "Ren/iPhi" is two systems; the iPhi MSA §3.4 forbids competitive use and reverse engineering; roughly 2–3 platform exits happen per year. Target-side and public-specification packages remain valuable. | MP-002 now requires licence and contract clearance. MP-005 needs two independent samples. Added MP-006 (target-side packages first) and MP-007 (measure reuse, retire low-reuse vendor packages). `daf.grant-record` relabelled as an Echelon draft, not a public standard. |
| C8 | Lineage creates excessive storage cost | C | **Rejected on cost, partially upheld on scope.** The table arithmetic holds. Yearly lineage was understated (≈5–7 GB/yr, not 1.5–5). L2 needs 400–600 B per record once indexed. Echelon.Execution adds 1.5–3 KB per record and stores payloads; purge is unimplemented, which conflicts with CNV-ARC-001 vault references. Natural keys were stored in clear text. | TRN-ARCH-08 and TRN-ARCH-12 corrected. Added EX-013 (no personal values in command payloads), LN-002 (HMAC natural keys), LN-010 (retention) and PF-003 (count Execution rows). |
| C9 | Domain-API loading creates throughput constraints | C | **Partially upheld.** About 5 commits and 20+ statements per record gives a realistic 300–800 records/s on an otherwise idle sponsor database, and 100–250 records/s alongside live traffic. The 20k/s batched figure was not credible, and the Unbound proposal it depended on was undefined. The 10k-per-sponsor queue limit would let imports throttle live donors. Batching conflicts with per-fund ordering, quarantine and receipts after go-live. | A7 revised and A8 withdrawn (TRN-ARCH-12). Added AD-011 (a quota share, lower priority and a separate worker role for bulk loads) and AD-012 (batch historical import only before go-live, through Unbound-defined operations). This is proposed to Unbound as UNB-TRN-006. |
| C10 | The visual designer is necessary | D | **Upheld.** It fails the proposal's own two-scenario rule. Unbound release 1 has no sponsor-written configuration and rejected a no-code engine (SPR-CFG-002). Most of the proposed views duplicate Unbound's case system. | TRN-ARCH-10 made **conditional on trigger T4**. UI-002/004 downgraded. UI-010 reworded as a library API. Added UI-011: exceptions go through the consumer's case system. |
| C11 | Excessive maintenance obligations | D | **Upheld.** 12 packages (the docs said 8), 16 adapters, about 7 parser libraries, 55 operations, 21 checks, 18 mapping packages and 115 requirements, for a single-owner portfolio of about 64 repositories that already shows drift. | Phase 1 limited to **three packages** with a declared maintenance budget (ARC-007), plus a no-duplication rule (ARC-006) and recorded phase triggers (ARC-009). |
| C12 | Transitus distracts from Unbound | D | **Upheld in part.** ⚠ The reviewer's claim that "release 1 excludes migration" holds only in the simplification discovery proposal; the adopted clause CNV-EXP-002 is `initial-implementation`, so Unbound's records conflict. Valid points: what release 1 needs (NACHA, BAI2, SFTP, raw preservation, control totals) sat in Transitus phase 2; OFAC, state registries and positive pay were missing; Unbound has no domain API yet. | Phase 1 is now exactly the release-1 feed libraries (ARC-008 requires tracing to release scope). U13–U15 added. The migration conflict is escalated to the Unbound owner (OQ-13). Echelon.Execution extraction is deferred to T2 (OQ-01). |

## Smallest viable architecture (outcome)

All four reviewers independently converged on a much smaller first step,
and the author accepts it:

1. **Phase 1 — three pure F# libraries** in this repository:
   `Transitus.Formats`, `Transitus.Checks`, `Transitus.Evidence`
   (TRN-ARCH-11 §2). Unbound writes each release-1 feed as a short F# module
   that composes them and loads through its own Echelon.Execution
   operations. Estimated at 4–6 engineer-weeks; this is theoretical.
2. **No engine, declarative pipeline document, staging, packages, AI or UI**
   until the recorded trigger for each fires (T2, T3, T4).
3. **Kill criterion.** At the phase-1 exit review, if per-feed modules prove
   cheaper (PF-004) and no second consumer is committed, Transitus remains a
   three-library utility and the phase-2 engine is not built.

Where the reviewers recommended an even smaller step, building the feed
libraries *inside* Unbound with no separate repository, the author did not
adopt it. The brief directs that Transitus be established as a
domain-independent component, and keeping the three libraries free of
Unbound terms (VR-006) costs little. This is recorded as owner decision
OQ-14 so the owner can choose otherwise.

## What the review did not change

- **Principles P1–P15 stand.** The review constrained *when* capabilities
  are built, not *what* the rules are: no user code, preserve before parse,
  gates before effects, effectively-once delivery, and loading through
  domain APIs.
- **The threat model stands**, extended by the AI semantic-change and
  annotation findings.
- **The competitive conclusion stands, and is sharpened.** Licence savings
  are not the justification; domain loading, evidence and a single runtime
  are.
