---
id: TRN-ARCH-12
title: Performance and Economic Models (theoretical)
status: proposed
version: 0.1.0
created: 2026-11-26
updated: 2026-11-26
work_item: WI-0001
evidence_quality: theoretical — no measurements exist; nothing here is a benchmark
---

# Performance and economic models

> **Every figure in this document is a theoretical estimate derived from the
> stated assumptions. None has been measured.** Phase 2 must replace each
> assumption with a measurement (TRN-REQ-PF-001) before any figure is used
> for capacity or commercial commitments.

## 1. Assumptions

| ID | Assumption | Value | Basis / how to verify |
|---|---|---|---|
| A1 | Average raw record size (CSV row) | 300 B | typical of BMF/custodian rows; measure per package |
| A2 | Typed staged row on disk incl. tuple header, alignment, one index | 600 B | ≈2× raw; measure with `pg_total_relation_size` |
| A3 | Staged datasets materialized per pipeline (parsed, transformed, load plan) | 3 | pipeline-dependent |
| A4 | Parse + per-record transforms, in-process, per core | 100,000 records/s (4 cores ⇒ 400k/s) | conservative for streaming .NET CSV with typed conversion; benchmark in phase 2 |
| A5 | PostgreSQL binary `COPY` into staging, managed 4-vCPU instance | 50,000 rows/s | benchmark (RM-05-style) |
| A6 | Set operations (dedupe/join/aggregate) in PostgreSQL, one pass | 30,000 rows/s effective | benchmark |
| A7 | Domain API load, one record per durable command (Echelon.Execution: ≈5 commits and 20+ statements per record including command, history, outbox and business writes) | **revised: 300–800 records/s with the sponsor database otherwise idle; 100–250 records/s alongside live traffic** (the original proposal assumed 1,000) | TRN-REV-01 C9, derived from Unbound's only benchmark (bare transactions at 2,127–3,944 tx/s); benchmark with RM-05 |
| A8 | Batch domain operations | **withdrawn as a planning figure** (the original 20,000 records/s was not credible). Batching conflicts with per-fund ordering (UNB-AVL-005), per-key quarantine (UNB-AVL-007) and per-record receipts after go-live; it is allowed only for pre-go-live historical import (TRN-REQ-AD-012, Unbound proposal UNB-TRN-006) | TRN-REV-01 C9 |
| A12 | Echelon.Execution storage per loaded record (command row with payload, history entries, outbox) | 1.5–3 KB/record, retained per that module's policy; purge not yet implemented (EAR-CMD-022) | TRN-REV-01 C8; measure (TRN-REQ-PF-003) |
| A9 | L2 record lineage per destination record | 300 B | §TRN-ARCH-08 |
| A10 | WAL amplification for logged staging | 1.5× staged bytes | `UNLOGGED` staging removes most of it |
| A11 | Chunk size | 10,000 records | checkpoint = one transaction per chunk |

## 2. Model by volume

> **Revised after TRN-REV-01.** The table keeps the original A7/A8 figures for traceability. The load columns are superseded: use the revised A7 range (100–800 records/s) and treat the batched column as void except for pre-go-live historical import. Add A12 Execution storage to the lineage column.

| Records | Raw stored | Peak staging | L2 lineage | Core processing (parse + 3× stage + 1 set pass) | Load, unbatched (A7) | Load, batched (A8) | WAL (logged staging) |
|---|---|---|---|---|---|---|---|
| 1,000 | 300 KB | 2 MB | 300 KB | 0.1 s | 1 s | 0.1 s | 3 MB |
| 100,000 | 30 MB | 180 MB | 30 MB | 10 s | 1.7 min | 5 s | 270 MB |
| 1,000,000 | 300 MB | 1.8 GB | 300 MB | 1.6 min | 17 min | 50 s | 2.7 GB |
| 10,000,000 | 3 GB | 18 GB | 3 GB | 16 min | 2.8 h | 8 min | 27 GB |
| 100,000,000 | 30 GB | 180 GB | 30 GB | 2.7 h | 28 h | 1.4 h | 270 GB |

### Other dimensions

| Dimension | Model |
|---|---|
| **Memory** | Bounded and independent of N: `chunkSize × recordSize × parallelism × 2 (in-flight)` ≈ 10,000 × 1 KB × 4 × 2 ≈ **80 MB**, plus reference-set caches (bounded by `memoryBudget`; large lookups go to PostgreSQL). Nothing requires the dataset to fit in memory. |
| **Checkpoint overhead** | One transaction per 10k-record chunk: 100 transactions per 1M records — negligible (<1%) relative to COPY. Smaller chunks raise overhead linearly; 1k chunks ≈ 1,000 tx per 1M. |
| **Database load** | Dominated by staging writes (3 × N × 600 B) and WAL. At 10⁷ records ≈ 18 GB written + 27 GB WAL in ~16 min ≈ 47 MB/s sustained writes — significant for a shared OLTP instance (Unbound runs one cluster per CNV-ARC-001). |
| **Network** | Source download = raw size; domain API traffic ≈ 1–2× payload. Not a bottleneck below 10⁸ records on cloud networking. |
| **Parallelism** | Parse/transform scale with cores until COPY saturates (~A5). Load parallelism is bounded by destination ordering keys and domain write capacity, not by Transitus. |
| **Recovery time** | Logged staging: crash ⇒ lease expiry (configurable, e.g. 5 min) + re-run of at most one chunk per worker. **UNLOGGED staging is truncated on crash**, so recovery then re-runs every staged stage from preserved raw input (TRN-REQ-ST-009). Worst case for a 10⁷ run ≈ lease duration + seconds. Raw preservation means a corrupted staging can be rebuilt by replay (cost = core processing time). |
| **Lineage storage** | L2 grows with loaded records: 10⁷ ⇒ 3 GB, retained for the approved policy period ⇒ consider partition-by-month and compression; L3-static is negligible. Storing per-field values would multiply by fields per record (×20–50) — rejected (DF-TRN-2026-0013). |

## 3. Where database-backed staging becomes inefficient

| Regime | Observation | Response |
|---|---|---|
| ≤10⁶ records per execution | Staging and WAL are small; all on the application database is fine. | Default. |
| 10⁶–10⁷ | WAL and vacuum pressure on a shared OLTP cluster become visible; staging writes compete with production traffic. | Use `UNLOGGED` staging partitions (safe because raw is preserved and stages replay); drop partitions instead of `DELETE`; schedule large runs off-peak; materialize only 2 datasets (stream transform into load plan). |
| ≥10⁷ (and especially 10⁸) | 18–180 GB staging on the OLTP database is unreasonable; core processing hours long. | Opt-in file-backed columnar staging (Parquet chunks in blob store, external sort/merge in engine) — **phase 4, only if a consumer demonstrates this volume**. No Echelon scenario identified today exceeds ~10⁷ records per execution (largest: IRS EO BMF ≈ 1.9M rows across four regional files; a large sponsor migration ≈ 10⁶–10⁷ rows of history). |

The file-backed option introduces **no new deployment component** (blob store
port already exists for raw data; Parquet via a library), satisfying "without
additional deployment complexity". Its cost is engineering complexity
(external sort/merge join), which is why it is deferred.

**Load is the dominant bottleneck, not staging.** With the revised A7, unbatched domain-API
loading of 10⁷ records takes ≈3.5–9 h on an otherwise idle sponsor database, and 11–28 h alongside live traffic (the table above used the original 1,000/s figure). This is acceptable for one-time
migrations for recurring feeds it argues for loading only diffs (BMF) and for a bounded quota share (TRN-REQ-AD-011), not for batching after go-live. See adversarial challenge C9.

## 4. Operating cost (theoretical)

Transitus has **no licence fee and no separate infrastructure**: it runs in
the host process against the host database. Incremental cost is:

| Cost driver | Estimate for a sponsor running BMF weekly (≈2M rows) + daily custodian files (≈50k rows) + one 5M-row migration per year | Basis |
|---|---|---|
| Compute | Absorbed by host app instance; ≈10 min/week BMF + ≈1 min/day custodian (A4–A7) | theoretical |
| Staging storage | transient; peak ≈ 9 GB during migration (A2, A3) | theoretical |
| Raw retention (per approved policy; a multi-year period is assumed only for sizing) | BMF snapshots ≈ 600 MB/week raw — dedupe by hash only helps when unchanged; ≈ 30 GB/year; compress (CSV ≈ 5–8× gzip) ⇒ ≈ 5 GB/year | theoretical |
| Lineage | **Revised (TRN-REV-01 C5/C8):** custodian rows alone ≈ 50k × 250 days × 300 B ≈ 3.75 GB/year; with BMF diffs and 400–600 B/record including indexes, ≈ 5–7 GB/year; plus Echelon.Execution rows (A12) ≈ 1.5–3 KB per loaded record unless purged | theoretical |
| Engineering & maintenance | dominant cost; see §5 | estimate |

## 5. Comparison with commercial and open-source alternatives

Unit prices below are from TRN-RES-01 §2.3 (verified unless stated).

| Option | Pricing unit | Applying to the scenario above | Structural fit |
|---|---|---|---|
| Fivetran | MAR (500k free tier; $5 minimum per connection from Jan 2026) [SRC-001, SRC-002] | BMF changes + custodian rows likely exceed free tier; vendor-specific custodian/NACHA sources need Connector SDK code anyway. | Targets warehouses, not domain APIs with approval gates; does not load into an application through business invariants. |
| Airbyte Cloud | credits ($20 / 5 credits; Plus from $189/month) [SRC-003] | Low $ for volume; custom file formats need connector development. | Warehouse/lake destinations; self-hosted ≈0.5 FTE/quarter operational burden reported [SRC-068]. |
| AWS Glue | $0.44 / DPU-hour [SRC-004] | A 2-DPU, 15-min job ≈ $0.22/run — cheap compute; cost is in AWS lock-in, cold starts, and building everything else. | Spark-centric; Echelon runs PostgreSQL + F#; adds a second runtime. |
| Azure Data Factory | $1 / 1k activity runs; $0.25 / DIU-hour [SRC-006] | Low $ for runs; data flows need ≥8-vCore Spark clusters [SRC-005]. | JSON definitions + ARM templating; designer-centric. |
| Informatica IDMC | IPU; no list price; reported £74,999 minimum (unverified) [SRC-015, SRC-016] | Disproportionate for a seed-stage product. | Enterprise suite. |
| dlt (open source, Apache-2.0) | free library | Closest architectural analogue [SRC-112]. | **Python** — adds a second language/runtime to an F#-only estate; no approval/reconciliation/domain-API loading model. |
| Meltano/Singer | free | Reusable taps. | Python; process-per-connector. |
| **Transitus** | none | Incremental infra ≈ storage above; engineering is the cost. | Native to Echelon stack; gates, reconciliation, evidence, domain API loading built in. |

Interpretation: on **cash cost**, commercial tools are cheap at Echelon's
volumes (hundreds to low thousands of dollars per year for most). The case
for Transitus is therefore **not** licence savings; it is (1) loading through
domain APIs with blocking financial gates and evidence, which no surveyed
product provides; (2) no second runtime (Python/JVM/Spark) or SaaS data
processor for regulated donor data; (3) reuse across Unbound, Helix Note and
Summa; and (4) migration as a commercial capability (daf-landscape OPP-10
rates data migration as "build early; sell as onboarding + independent
assurance", with a hypothesised $25–75k per project). The adversarial review
(C2) tests whether these benefits justify the engineering cost.

## 5a. Baseline the proposal must beat: hand-written per-feed F# (TRN-REV-01 C2)

The cheapest alternative is neither a vendor tool nor Transitus. It is a short F# module per feed inside Unbound that uses existing .NET parsers and loads through Echelon.Execution. For the roughly six fixed release-1 feeds, the reviewer estimates 3–4 engineer-weeks. The owner directed a larger phase 1, a minimal declarative pipeline (DF-TRN-2026-0018). This baseline is therefore kept as the **later comparison** in TRN-REQ-PF-004, measured within six months of phase-1 exit. It does not gate phase 1.

## 6. Engineering cost estimate (theoretical)

Revised for the owner-directed phase 1 (DF-TRN-2026-0018) using the
independent estimate in TRN-REV-02 (`../reviews/agent-reviews/adv-E.md` §3).
The assumptions are:
- one experienced F# engineer, agent-assisted;
- logged staging;
- no chunk parallelism;
- fake ports until Unbound domain operations exist.

| Phase | Scope | Engineer-weeks |
|---|---|---|
| 1 | Minimal declarative linear pipeline, 13 operations, checks, evidence, engine behind ports, Postgres staging, basic packages, three demonstrations | ≈15–24 |
| 1 (prerequisites, not Transitus) | Unbound domain operations with read-back, canonical shape, rehearsal cell, Echelon.Execution G2/G3, quota share, queue-limit fix, RM-05 benchmark | ≈6–12 |
| 2 (T2) | DAGs, TEL, set operators, extensions, chunk parallelism, scheduling, overlays | ≈6–10 |
| 3 (T3) | Advanced AI, vendor-turnkey packages | 4–6 |
| 4 (T4) | Visual editing | 8–12 |
| Ongoing | Format drift (BMF layout, bank and Schwab specification versions), parser updates, security patches | ≈0.15–0.2 FTE |

Superseded estimates are kept for comparison:
- 4–6 weeks for the three-library phase 1;
- 6–10 weeks for the original phase 1;
- 3–4 weeks for the hand-written per-feed baseline (§5a).

Phase 1 is roughly 2–3× the three-library plan. Its critical path runs
through Unbound and partner prerequisites, not through Transitus.
