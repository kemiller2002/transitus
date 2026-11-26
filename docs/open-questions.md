---
id: TRN-OQ
title: Open Questions and Owner Escalations
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
---

# Open questions

"Owner" marks a material decision that needs owner judgment. Every other
question will be resolved with evidence during the phase named.

| ID | Question | Why it matters | Options / recommendation | Owner? | Resolve by |
|---|---|---|---|---|---|
| OQ-01 | When is Echelon.Execution extracted from Unbound into a shared component? | Transitus phase 2 becomes its second consumer, but the module is unbenchmarked (RM-05). | **Recommend:** extract when trigger T2 fires and RM-05 benchmarks exist. Until then, phase-1 feeds use it in place. | **Owner** (INIT-012) | T2 |
| OQ-02 | Where is the boundary between Strata's proposed data-interaction virtualization (STRATA-DIV-001) and Transitus source adapters? | Both touch "external interactions". Registry drift finding DRF-03. | **Recommend:** DIV virtualizes the application's own external calls for testing. Transitus ingests external data; its adapters may run under DIV replay in tests. | **Owner** (INIT-018 boundary review) | before phase 2 |
| OQ-03 | Who owns runtime observability (GAP-05), tamper-evident evidence storage (GAP-07) and auditor export (GAP-06)? | Transitus emits OpenTelemetry and hash-chained evidence but must not become the monitoring product. Vigila is a follow-up tracker, not observability, which corrects an assumption in the brief. | Name a portfolio owner. Transitus integrates once one exists. | **Owner** | before production use |
| OQ-04 | Is there a portfolio-wide object store for raw evidence? | Arca excludes large binaries (ARCA-REC-007). | Transitus defines an `IBlobStore` port with a PostgreSQL default. Re-point the port if an owner emerges. | no | phase 1 |
| OQ-05 | How are destinations with no idempotency handled, such as bank SFTP drops and positive-pay files? | Effectively-once cannot be guaranteed there. | Single attempt, deterministic file ids, OutcomeUnknown with human resolution, and bank-side duplicate rejection where the bank offers it. Confirm with the chosen bank's specification. | no | phase 1 (U15) |
| OQ-06 | Which bank activity format comes first: BAI2 or ISO 20022 camt.053? | Phase-1 format scope (ARC-007 budget). | Depends on Unbound's bank partner. Build one, not both. | Unbound owner | phase 1 |
| OQ-07 | Which custodian file format comes first? | Phase-1 scope. Unbound OD-M-07 describes Schwab-type managers. | Use the first contracted custodian's documented format. | Unbound owner | phase 1 |
| OQ-08 | Which AI providers are approved, per data classification and per tenant? | T23. Helix Note currently calls the OpenAI API directly. | Policy decision. AI is phase 3. | **Owner** | T3 |
| OQ-09 | Are event streams or CDC ever needed? | Deferred by DF-TRN-2026-0009. | No current scenario needs them. Revisit only on demonstrated demand. | no | on demand |
| OQ-10 | What are the binding retention periods for raw input, lineage and evidence? | Defaults of 7 years are placeholders. | Sponsor and Unbound record-keeping policy. | Unbound owner | phase 1 |
| OQ-11 | Does Transitus need currency conversion? | No FX operation in v1. | No. FX belongs to the investment domain. | no | phase 2 |
| OQ-12 | Licence: MIT, as the brief directs for public content, or PolyForm Noncommercial, as all component repositories use (registry DRF-09, OD-GOV-018)? | Transitus is a reusable component; licence affects consumers and commercial plans. | This repository is MIT per the brief. The portfolio-level decision OD-GOV-018 should confirm it or supersede it. | **Owner** | before first release |
| OQ-13 | Is institutional/donor-history migration in Unbound release 1? | The adopted clause CNV-EXP-002 (`initial-implementation`) requires full fund-history import. The simplification discovery proposes "no migration in R1". OD-M-14 says there is no design partner. | Unbound owner decision. If CNV-EXP-002 stands, phase 1 adds the migration feed (U1/U10) using the Unbound canonical import shape (MP-006). | **Owner** (Unbound) | before phase-1 start |
| OQ-14 | Should phase 1 live in this repository, or inside Unbound until a second consumer commits? | All four reviewers favoured the smallest step. Two suggested building inside Unbound. | **Recommend:** this repository, with three domain-free libraries, as the brief directs. The extra cost is small and avoids a later extraction. | **Owner** | before phase-1 start |
| OQ-15 | Will Unbound define the domain operations Transitus loads through (UNB-TRN-005/006)? | Unbound has no domain API yet. Loading depends on it. | Proposed in `unbound/requirements/discovery/2026-11-26-transitus-integration/`. | Unbound owner | phase 1 |
| OQ-16 | Are the NACHA Operating Rules licence terms compatible with publishing the `nacha.ach` package layouts? | Mapping package legality. | Use only the record layouts that are publicly available. Check before publishing. | no | phase 1 |
